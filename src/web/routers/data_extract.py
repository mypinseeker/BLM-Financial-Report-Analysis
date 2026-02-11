"""Data extraction API endpoints — Gemini AI pipeline for extracting telecom data.

Step-by-step architecture to stay under Vercel's 10s timeout per request:
  1. POST /api/extract/discover    — Gemini finds earnings report PDF
  2. POST /api/extract/download    — Download PDF + upload to Gemini Files
  3. POST /api/extract/run         — Extract one table at a time
  4. GET  /api/extract/{job_id}    — Query job status and data
  5. POST /api/extract/{job_id}/approve — Approve → upsert to 5 tables
  6. POST /api/extract/{job_id}/reject  — Reject → discard
  7. GET  /api/extract              — List all extraction jobs
"""

import json
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from src.web.services.supabase_data import get_data_service
from src.web.services.extraction_service import ExtractionService
from src.web.services.gemini_service import GeminiError, get_gemini_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/extract", tags=["extract"])


# ------------------------------------------------------------------
# Request models
# ------------------------------------------------------------------

class DiscoverRequest(BaseModel):
    operator_id: str
    market: str


class DownloadRequest(BaseModel):
    job_id: int
    pdf_url: str | None = None  # Optional override


class RunRequest(BaseModel):
    job_id: int
    table_type: str  # financial | subscriber | tariff | macro | network
    target_quarter: str = "CQ4_2025"
    n_quarters: int = 4


# ------------------------------------------------------------------
# Helper: get or create extraction service
# ------------------------------------------------------------------

def _get_extraction_service() -> ExtractionService:
    try:
        return ExtractionService(get_gemini_service())
    except GeminiError as e:
        raise HTTPException(500, f"Gemini init failed: {e}")
    except Exception as e:
        raise HTTPException(500, f"Extraction service init failed: {e}")


# ------------------------------------------------------------------
# 1. Discover report
# ------------------------------------------------------------------

@router.post("/discover")
async def discover_report(req: DiscoverRequest):
    """Use Gemini + Google Search to find the latest earnings report PDF."""
    svc = get_data_service()
    ext = _get_extraction_service()

    # Create extraction job
    job = svc.create_extraction_job({
        "operator_id": req.operator_id,
        "market": req.market,
        "status": "discovering",
        "current_step": "discover",
        "started_at": datetime.utcnow().isoformat(),
    })
    job_id = job.get("id")

    try:
        result = await ext.discover_report(req.operator_id)

        # Update job with discovery results
        svc.update_extraction_job(job_id, {
            "status": "discovered",
            "current_step": "discovered",
            "discovered_pdf_url": result.get("pdf_url", ""),
            "report_title": result.get("report_title", ""),
            "report_period": result.get("report_period", ""),
            "ir_url": result.get("ir_page_url", ""),
        })

        return {
            "job_id": job_id,
            "status": "discovered",
            **result,
        }

    except (GeminiError, Exception) as e:
        logger.exception("Discovery failed for %s", req.operator_id)
        svc.update_extraction_job(job_id, {
            "status": "error",
            "current_step": "discover",
            "error_message": str(e),
        })
        raise HTTPException(500, f"Discovery failed: {e}")


# ------------------------------------------------------------------
# 2. Download PDF + upload to Gemini
# ------------------------------------------------------------------

@router.post("/download")
async def download_report(req: DownloadRequest):
    """Download the discovered PDF and upload to Gemini Files API."""
    svc = get_data_service()
    ext = _get_extraction_service()

    job = svc.get_extraction_job(req.job_id)
    if not job:
        raise HTTPException(404, f"Job #{req.job_id} not found")

    pdf_url = req.pdf_url or job.get("discovered_pdf_url", "")
    if not pdf_url:
        raise HTTPException(400, "No PDF URL available. Run discovery first or provide a URL.")

    # Update status
    svc.update_extraction_job(req.job_id, {
        "status": "downloading",
        "current_step": "download",
        "discovered_pdf_url": pdf_url,
    })

    try:
        display_name = f"{job['operator_id']}_{job.get('report_period', 'report')}"
        file_uri = await ext.download_and_upload(pdf_url, display_name)

        svc.update_extraction_job(req.job_id, {
            "status": "uploaded",
            "current_step": "uploaded",
            "gemini_file_uri": file_uri,
        })

        return {
            "job_id": req.job_id,
            "status": "uploaded",
            "file_uri": file_uri,
            "mode": "pdf",
        }

    except Exception as e:
        # PDF download failed — fall back to search-based extraction
        logger.warning("PDF download failed for job %d: %s. Falling back to search mode.", req.job_id, e)
        svc.update_extraction_job(req.job_id, {
            "status": "uploaded",
            "current_step": "search_fallback",
            "gemini_file_uri": "search",
            "error_message": f"PDF download failed, using search mode: {e}",
        })

        return {
            "job_id": req.job_id,
            "status": "uploaded",
            "file_uri": "search",
            "mode": "search_fallback",
            "message": f"PDF not downloadable, will use Google Search for extraction",
        }


# ------------------------------------------------------------------
# 3. Extract one table
# ------------------------------------------------------------------

@router.post("/run")
async def run_extraction(req: RunRequest):
    """Extract data for one table type from the uploaded PDF."""
    svc = get_data_service()
    ext = _get_extraction_service()

    job = svc.get_extraction_job(req.job_id)
    if not job:
        raise HTTPException(404, f"Job #{req.job_id} not found")

    file_uri = job.get("gemini_file_uri", "")
    if not file_uri:
        raise HTTPException(400, "No file uploaded. Run download step first.")

    valid_types = ["financial", "subscriber", "tariff", "macro", "network"]
    if req.table_type not in valid_types:
        raise HTTPException(400, f"Invalid table_type. Must be one of: {valid_types}")

    # Update status
    svc.update_extraction_job(req.job_id, {
        "status": "extracting",
        "current_step": f"extracting_{req.table_type}",
    })

    try:
        rows = await ext.extract_table(
            file_uri=file_uri,
            table_type=req.table_type,
            operator_id=job["operator_id"],
            target_quarter=req.target_quarter,
            n_quarters=req.n_quarters,
        )

        # Merge into extracted_data
        extracted = job.get("extracted_data") or {}
        if isinstance(extracted, str):
            extracted = json.loads(extracted)
        extracted[req.table_type] = rows

        # Determine overall status
        extracted_types = set(extracted.keys())
        all_done = extracted_types >= set(valid_types)
        new_status = "extracted" if all_done else "extracting"

        svc.update_extraction_job(req.job_id, {
            "status": new_status,
            "current_step": f"extracted_{req.table_type}",
            "extracted_data": json.dumps(extracted),
        })

        return {
            "job_id": req.job_id,
            "table_type": req.table_type,
            "rows_extracted": len(rows),
            "rows": rows,
            "status": new_status,
            "tables_done": sorted(extracted_types),
        }

    except Exception as e:
        logger.exception("Extraction failed for job %d table %s", req.job_id, req.table_type)
        svc.update_extraction_job(req.job_id, {
            "status": "error",
            "current_step": f"extract_{req.table_type}",
            "error_message": str(e),
        })
        raise HTTPException(500, f"Extraction failed: {e}")


# ------------------------------------------------------------------
# Debug: check env vars
# ------------------------------------------------------------------

@router.get("/debug/env")
def debug_env():
    """Debug: check if required env vars are set (values masked)."""
    import os
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    supabase_url = os.getenv("SUPABASE_URL", "")
    return {
        "GEMINI_API_KEY": f"{gemini_key[:8]}...{gemini_key[-4:]}" if len(gemini_key) > 12 else ("SET" if gemini_key else "MISSING"),
        "SUPABASE_URL": supabase_url[:30] + "..." if supabase_url else "MISSING",
    }


# ------------------------------------------------------------------
# 4. Get job status and data
# ------------------------------------------------------------------

@router.get("/{job_id}")
def get_extraction_job(job_id: int):
    """Query extraction job status and extracted data."""
    svc = get_data_service()
    job = svc.get_extraction_job(job_id)
    if not job:
        raise HTTPException(404, f"Job #{job_id} not found")

    # Parse JSON fields
    for field in ("extracted_data", "approved_data"):
        val = job.get(field)
        if isinstance(val, str):
            try:
                job[field] = json.loads(val)
            except json.JSONDecodeError:
                job[field] = {}

    return job


# ------------------------------------------------------------------
# 5. Approve → upsert to all tables + provenance
# ------------------------------------------------------------------

@router.post("/{job_id}/approve")
def approve_extraction(job_id: int):
    """Approve extracted data and write to Supabase tables."""
    svc = get_data_service()
    job = svc.get_extraction_job(job_id)
    if not job:
        raise HTTPException(404, f"Job #{job_id} not found")

    extracted = job.get("extracted_data") or {}
    if isinstance(extracted, str):
        extracted = json.loads(extracted)

    if not extracted:
        raise HTTPException(400, "No extracted data to approve")

    results = {}
    source_id = f"extraction_job_{job_id}"
    operator_id = job.get("operator_id", "")

    # Register source
    svc.register_source({
        "source_id": source_id,
        "source_type": "earnings_report",
        "url": job.get("discovered_pdf_url", ""),
        "document_name": job.get("report_title", ""),
        "publisher": operator_id,
        "publication_date": datetime.utcnow().strftime("%Y-%m-%d"),
    })

    # Upsert each table type
    upsert_map = {
        "financial": svc.upsert_financial_quarterly,
        "subscriber": svc.upsert_subscriber_quarterly,
        "tariff": svc.upsert_tariffs,
        "macro": svc.upsert_macro_environment,
        "network": svc.upsert_network_infrastructure,
    }

    provenance_rows = []

    for table_type, rows in extracted.items():
        if not rows or table_type not in upsert_map:
            continue

        # Strip fields not in the DB schema for each table type
        clean_rows = []
        for row in rows:
            confidence = row.pop("confidence", None)
            # Remove fields that don't exist in certain tables
            row = _clean_row_for_table(table_type, row)
            clean_rows.append(row)
            # Build provenance
            if confidence is not None:
                provenance_rows.append({
                    "entity_type": _table_name(table_type),
                    "entity_id": 0,  # Will be resolved after insert
                    "field_name": "_all",
                    "source_id": source_id,
                    "confidence": float(confidence),
                    "extraction_method": "gemini_ai",
                })

        try:
            result = upsert_map[table_type](clean_rows)
            results[table_type] = {
                "rows_written": len(result),
                "status": "ok",
            }
        except Exception as e:
            logger.exception("Upsert failed for %s", table_type)
            results[table_type] = {
                "rows_written": 0,
                "status": "error",
                "error": str(e),
            }

    # Record provenance
    try:
        svc.record_provenance(provenance_rows)
    except Exception as e:
        logger.warning("Provenance recording failed: %s", e)

    # Update job
    svc.update_extraction_job(job_id, {
        "status": "approved",
        "current_step": "approved",
        "approved_data": json.dumps(extracted),
        "approved_at": datetime.utcnow().isoformat(),
        "source_id": source_id,
    })

    return {
        "job_id": job_id,
        "status": "approved",
        "results": results,
    }


# ------------------------------------------------------------------
# 6. Reject
# ------------------------------------------------------------------

@router.post("/{job_id}/reject")
def reject_extraction(job_id: int):
    """Reject and discard extracted data."""
    svc = get_data_service()
    job = svc.get_extraction_job(job_id)
    if not job:
        raise HTTPException(404, f"Job #{job_id} not found")

    svc.update_extraction_job(job_id, {
        "status": "rejected",
        "current_step": "rejected",
    })

    return {"job_id": job_id, "status": "rejected"}


# ------------------------------------------------------------------
# 7. List all extraction jobs
# ------------------------------------------------------------------

@router.get("")
def list_extraction_jobs(status: Optional[str] = Query(None)):
    """List all extraction jobs, optionally filtered by status.

    Returns summary metadata only (excludes large extracted_data/approved_data
    payloads to avoid Vercel timeout on list queries).
    """
    svc = get_data_service()
    jobs = svc.list_extraction_jobs(status=status)

    # Strip large JSON payloads — return row counts instead
    for job in jobs:
        for field in ("extracted_data", "approved_data"):
            raw = job.get(field)
            if raw:
                if isinstance(raw, str):
                    try:
                        parsed = json.loads(raw)
                    except json.JSONDecodeError:
                        parsed = {}
                else:
                    parsed = raw
                # Replace payload with summary: {"financial": 4, "subscriber": 3, ...}
                job[field] = {
                    k: len(v) if isinstance(v, list) else 1
                    for k, v in parsed.items()
                } if isinstance(parsed, dict) else {}
            else:
                job[field] = {}

    return jobs


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _table_name(table_type: str) -> str:
    """Map short type to actual DB table name."""
    return {
        "financial": "financial_quarterly",
        "subscriber": "subscriber_quarterly",
        "tariff": "tariffs",
        "macro": "macro_environment",
        "network": "network_infrastructure",
    }.get(table_type, table_type)


# Allowed columns per table (from schema.sql). Extra fields are stripped before upsert.
_TABLE_COLUMNS: dict[str, set[str]] = {
    "financial": {
        "operator_id", "period", "calendar_quarter", "period_start", "period_end",
        "report_date", "report_status", "total_revenue", "service_revenue",
        "service_revenue_growth_pct", "mobile_service_revenue", "mobile_service_growth_pct",
        "fixed_service_revenue", "fixed_service_growth_pct", "b2b_revenue", "b2b_growth_pct",
        "tv_revenue", "wholesale_revenue", "other_revenue", "ebitda", "ebitda_margin_pct",
        "ebitda_growth_pct", "net_income", "capex", "capex_to_revenue_pct", "opex",
        "opex_to_revenue_pct", "employees", "source_url", "notes",
    },
    "subscriber": {
        "operator_id", "period", "calendar_quarter", "period_start", "period_end",
        "report_status", "mobile_total_k", "mobile_postpaid_k", "mobile_prepaid_k",
        "mobile_net_adds_k", "mobile_churn_pct", "mobile_arpu", "iot_connections_k",
        "broadband_total_k", "broadband_net_adds_k", "broadband_cable_k", "broadband_fiber_k",
        "broadband_dsl_k", "broadband_fwa_k", "broadband_arpu", "tv_total_k", "tv_net_adds_k",
        "fmc_total_k", "fmc_penetration_pct", "b2b_customers_k", "source_url", "notes",
    },
    "tariff": {
        "operator_id", "plan_name", "plan_type", "plan_tier", "monthly_price",
        "data_allowance", "speed_mbps", "contract_months", "includes_5g", "technology",
        "effective_date", "snapshot_period", "source_url", "notes",
    },
    "macro": {
        "country", "calendar_quarter", "gdp_growth_pct", "inflation_pct",
        "unemployment_pct", "telecom_market_size_eur_b", "telecom_growth_pct",
        "five_g_adoption_pct", "fiber_penetration_pct", "regulatory_environment",
        "digital_strategy", "energy_cost_index", "consumer_confidence_index",
        "source_url", "notes",
    },
    "network": {
        "operator_id", "calendar_quarter", "five_g_coverage_pct", "four_g_coverage_pct",
        "fiber_homepass_k", "fiber_connected_k", "cable_homepass_k", "cable_docsis31_pct",
        "technology_mix", "quality_scores", "source_url", "notes",
    },
}


def _clean_row_for_table(table_type: str, row: dict) -> dict:
    """Strip fields that don't exist in the target DB table."""
    allowed = _TABLE_COLUMNS.get(table_type)
    if not allowed:
        return row
    return {k: v for k, v in row.items() if k in allowed}


