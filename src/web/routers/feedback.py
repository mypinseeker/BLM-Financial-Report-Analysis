"""Feedback API — review findings, persist feedback, generate final reports."""
from __future__ import annotations

import json
import tempfile
import traceback
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, HTTPException

from src.web.services.supabase_data import get_data_service
from src.web.services.finding_extractor import (
    FindingExtractor,
    feedback_to_ppt_decisions,
    feedback_to_key_message_overrides,
)

router = APIRouter(prefix="/api/feedback", tags=["feedback"])

BUCKET = "blm-outputs"


@router.get("/{job_id}/findings")
def get_findings(job_id: int):
    """Extract findings from the analysis JSON and merge existing feedback.

    1. Look up analysis job → get market/operator/period
    2. Find JSON output in analysis_outputs table
    3. Download JSON from Supabase Storage
    4. Run FindingExtractor.extract_all()
    5. Merge existing feedback from user_feedback table
    6. Return {findings, existing_feedback, job}
    """
    svc = get_data_service()

    # 1. Get job metadata
    job = svc.get_analysis_job(job_id)
    if not job:
        raise HTTPException(404, f"Analysis job #{job_id} not found")

    market = job.get("market", "")
    operator = job.get("target_operator", "")
    period = job.get("analysis_period", "")

    # 2. Find JSON output
    outputs = svc.get_analysis_outputs(market_id=market)
    json_output = None
    for out in outputs:
        if (out.get("output_type") == "json"
                and out.get("operator_id") == operator
                and out.get("analysis_period") == period):
            json_output = out
            break

    if not json_output:
        raise HTTPException(404, f"No JSON output found for job #{job_id}")

    # 3. Download JSON
    storage_path = json_output.get("storage_path", "")
    try:
        raw = svc.download_output_file(storage_path)
        json_data = json.loads(raw)
    except Exception as e:
        raise HTTPException(500, f"Failed to download JSON: {e}")

    # 4. Extract findings
    extractor = FindingExtractor()
    findings = extractor.extract_all(json_data)

    # 5. Get existing feedback
    existing = svc.get_feedback(job_id, operator_id=operator)

    return {
        "findings": findings,
        "existing_feedback": existing,
        "job": {
            "id": job_id,
            "market": market,
            "operator": operator,
            "period": period,
            "status": job.get("status", ""),
        },
    }


@router.post("/{job_id}/save")
def save_feedback(job_id: int, payload: dict):
    """Upsert feedback items to user_feedback table.

    Body: {operator_id, period, items: [{look_category, finding_ref,
           feedback_type, user_comment, user_value, original_value}]}
    """
    svc = get_data_service()

    job = svc.get_analysis_job(job_id)
    if not job:
        raise HTTPException(404, f"Analysis job #{job_id} not found")

    items = payload.get("items", [])
    if not items:
        return {"saved": 0}

    operator_id = payload.get("operator_id", job.get("target_operator", ""))
    period = payload.get("period", job.get("analysis_period", ""))

    rows = []
    now = datetime.utcnow().isoformat()
    for item in items:
        rows.append({
            "analysis_job_id": job_id,
            "operator_id": operator_id,
            "look_category": item.get("look_category", ""),
            "finding_ref": item.get("finding_ref", ""),
            "feedback_type": item.get("feedback_type", "confirmed"),
            "original_value": item.get("original_value"),
            "user_comment": item.get("user_comment", ""),
            "user_value": item.get("user_value"),
            "period": period,
            "created_at": now,
        })

    saved = svc.upsert_feedback(rows)
    return {"saved": len(saved)}


@router.post("/{job_id}/finalize")
def finalize_report(job_id: int, background_tasks: BackgroundTasks):
    """Generate final PPT + MD reports incorporating user feedback.

    1. Load feedback from user_feedback
    2. Download JSON output → parse
    3. Generate final PPT (mode='final', user_decisions, key_message_overrides)
    4. Generate final MD (mode='final', feedback)
    5. Upload to Supabase Storage as *_final.{pptx,md}
    6. Register in analysis_outputs
    """
    svc = get_data_service()

    job = svc.get_analysis_job(job_id)
    if not job:
        raise HTTPException(404, f"Analysis job #{job_id} not found")

    # Trigger finalization in background
    background_tasks.add_task(_run_finalization, svc, job_id, job)
    return {"status": "started", "message": "Final report generation started"}


def _run_finalization(svc, job_id: int, job: dict):
    """Background task: generate final reports."""
    market = job.get("market", "")
    operator = job.get("target_operator", "")
    period = job.get("analysis_period", "")

    try:
        # 1. Load feedback
        feedback = svc.get_feedback(job_id, operator_id=operator)
        if not feedback:
            print(f"  [!] No feedback found for job #{job_id}, generating final with no changes")

        # 2. Download JSON
        outputs = svc.get_analysis_outputs(market_id=market)
        json_output = None
        for out in outputs:
            if (out.get("output_type") == "json"
                    and out.get("operator_id") == operator
                    and out.get("analysis_period") == period):
                json_output = out
                break

        if not json_output:
            print(f"  [!] No JSON output found for job #{job_id}")
            return

        raw = svc.download_output_file(json_output["storage_path"])
        json_data = json.loads(raw)

        # 3. Reconstruct FiveLooksResult from JSON
        result = _json_to_result(json_data)

        tmp_dir = tempfile.mkdtemp(prefix="blm_final_")
        output_dir = Path(tmp_dir)
        safe_op = operator.replace(" ", "_").lower()
        storage_prefix = f"{market}/{operator}/{period}"

        svc.ensure_bucket(BUCKET)

        # 4. Generate final PPT
        try:
            from src.output.ppt_generator import BLMPPTGenerator
            from src.output.ppt_styles import get_style

            ppt_decisions = feedback_to_ppt_decisions(feedback)
            km_overrides = feedback_to_key_message_overrides(feedback)

            style = get_style(operator)
            ppt_gen = BLMPPTGenerator(
                style=style, operator_id=operator,
                output_dir=str(output_dir),
            )
            ppt_name = f"blm_{safe_op}_analysis_{period.lower()}_final.pptx"
            ppt_path = ppt_gen.generate(
                result, mode="final",
                user_decisions=ppt_decisions,
                key_message_overrides=km_overrides,
                filename=ppt_name,
            )

            # Upload
            ppt_data = Path(ppt_path).read_bytes()
            ppt_storage = f"{storage_prefix}/{ppt_name}"
            svc.upload_output_file(BUCKET, ppt_storage, ppt_data,
                                   "application/vnd.openxmlformats-officedocument.presentationml.presentation")
            svc.register_analysis_output({
                "market_id": market,
                "operator_id": operator,
                "analysis_period": period,
                "output_type": "pptx_final",
                "module_name": None,
                "file_name": ppt_name,
                "storage_path": ppt_storage,
                "file_size_bytes": Path(ppt_path).stat().st_size,
                "updated_at": datetime.utcnow().isoformat(),
            })
            print(f"    Final PPT: {ppt_name}")
        except ImportError:
            print("    [i] Final PPT skipped (python-pptx not installed)")
        except Exception as e:
            print(f"    [!] Final PPT generation failed: {e}")
            traceback.print_exc()

        # 5. Generate final MD
        try:
            from src.output.md_generator import BLMMdGenerator

            md_gen = BLMMdGenerator()
            md_name = f"blm_{safe_op}_analysis_{period.lower()}_final.md"
            md_content = md_gen.generate(result, mode="final", feedback=feedback)
            md_path = output_dir / md_name
            md_path.write_text(md_content, encoding="utf-8")

            # Upload
            md_data = md_path.read_bytes()
            md_storage = f"{storage_prefix}/{md_name}"
            svc.upload_output_file(BUCKET, md_storage, md_data, "text/markdown")
            svc.register_analysis_output({
                "market_id": market,
                "operator_id": operator,
                "analysis_period": period,
                "output_type": "md_final",
                "module_name": None,
                "file_name": md_name,
                "storage_path": md_storage,
                "file_size_bytes": md_path.stat().st_size,
                "updated_at": datetime.utcnow().isoformat(),
            })
            print(f"    Final MD: {md_name}")
        except Exception as e:
            print(f"    [!] Final MD generation failed: {e}")
            traceback.print_exc()

        # Cleanup
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)

        print(f"  Finalization complete for job #{job_id}")

    except Exception as e:
        print(f"  [!] Finalization failed for job #{job_id}: {e}")
        traceback.print_exc()


# ======================================================================
# JSON → FiveLooksResult reconstruction
# ======================================================================

class _AttrDict:
    """Lightweight attribute-access wrapper over a dict.

    Recursively wraps nested dicts so that `obj.attr.nested` works,
    matching the dataclass attribute access pattern used by generators.
    """

    def __init__(self, data: dict):
        self._data = data or {}

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        val = self._data.get(name)
        if isinstance(val, dict):
            return _AttrDict(val)
        if isinstance(val, list):
            return [_AttrDict(v) if isinstance(v, dict) else v for v in val]
        return val

    def __iter__(self):
        return iter(self._data)

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __contains__(self, item):
        return item in self._data

    def __len__(self):
        return len(self._data)

    def __bool__(self):
        return bool(self._data)


def _json_to_result(json_data: dict):
    """Reconstruct a FiveLooksResult-compatible object from JSON export data.

    The generators only need attribute access (.trends, .market_customer, etc.)
    and getattr/safe_get access on nested objects. _AttrDict provides this.
    """
    meta = json_data.get("meta", {})
    five = json_data.get("five_looks", {})

    result = _AttrDict({
        "target_operator": meta.get("target_operator", ""),
        "market": meta.get("market", ""),
        "analysis_period": meta.get("analysis_period", ""),
        "trends": five.get("trends"),
        "market_customer": five.get("market_customer"),
        "competition": five.get("competition"),
        "self_analysis": five.get("self_analysis"),
        "swot": five.get("swot"),
        "opportunities": five.get("opportunities"),
        "tariff_analysis": None,
        "provenance": None,
        "three_decisions": None,
    })
    return result
