"""Analysis job endpoints — create, track, and query analysis tasks."""

import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from pydantic import BaseModel

from src.web.services.supabase_data import get_data_service

router = APIRouter(prefix="/api/analyze", tags=["analyze"])


# ------------------------------------------------------------------
# Request models
# ------------------------------------------------------------------

class SingleMarketRequest(BaseModel):
    market: str
    target_operator: str
    analysis_period: str = "CQ4_2025"
    n_quarters: int = 8
    competitors: list[str] = []


class GroupAnalysisRequest(BaseModel):
    group_id: str
    analysis_period: str = "CQ4_2025"
    n_quarters: int = 8
    selected_markets: list[str] = []


# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------

@router.post("/single")
def create_single_analysis(req: SingleMarketRequest,
                           background_tasks: BackgroundTasks):
    """Create a single-market analysis job and auto-trigger execution."""
    svc = get_data_service()

    # Validate operator exists
    op = svc.get_operator(req.target_operator)
    if not op:
        raise HTTPException(404, f"Operator '{req.target_operator}' not found")

    job_data = {
        "job_type": "single_market",
        "market": req.market,
        "target_operator": req.target_operator,
        "analysis_period": req.analysis_period,
        "n_quarters": req.n_quarters,
        "status": "pending",
        "progress": json.dumps({req.market: "pending"}),
        "config": json.dumps({
            "competitors": req.competitors,
        }),
    }

    try:
        job = svc.create_analysis_job(job_data)
        job_id = job.get("id")

        # Auto-trigger execution in background
        background_tasks.add_task(_execute_single, job_id)

        return {"job_id": job_id, "status": "pending"}
    except Exception as e:
        raise HTTPException(500, f"Failed to create job: {e}")


@router.post("/group")
def create_group_analysis(req: GroupAnalysisRequest,
                          background_tasks: BackgroundTasks):
    """Create a group analysis job and auto-trigger execution."""
    svc = get_data_service()

    # Validate group exists
    group = svc.get_operator_group(req.group_id)
    if not group:
        raise HTTPException(404, f"Group '{req.group_id}' not found")

    # Get subsidiaries to determine markets
    subs = svc.get_group_subsidiaries(req.group_id)
    all_markets = [s["market"] for s in subs]

    # Filter to selected markets if specified
    markets = req.selected_markets if req.selected_markets else all_markets

    # Initialize progress for each market
    progress = {m: "pending" for m in markets}

    job_data = {
        "job_type": "group_analysis",
        "group_id": req.group_id,
        "analysis_period": req.analysis_period,
        "n_quarters": req.n_quarters,
        "status": "pending",
        "progress": json.dumps(progress),
        "config": json.dumps({
            "selected_markets": markets,
        }),
    }

    try:
        job = svc.create_analysis_job(job_data)
        job_id = job.get("id")

        # Auto-trigger execution in background
        background_tasks.add_task(_execute_group, job_id)

        return {"job_id": job_id, "status": "pending", "markets": markets}
    except Exception as e:
        raise HTTPException(500, f"Failed to create job: {e}")


@router.get("/{job_id}")
def get_analysis_status(job_id: int):
    """Query analysis job progress."""
    svc = get_data_service()
    job = svc.get_analysis_job(job_id)
    if not job:
        raise HTTPException(404, f"Job #{job_id} not found")

    # Parse JSON fields
    progress_str = job.get("progress", "{}")
    if isinstance(progress_str, str):
        try:
            job["progress"] = json.loads(progress_str)
        except json.JSONDecodeError:
            job["progress"] = {}

    config_str = job.get("config", "{}")
    if isinstance(config_str, str):
        try:
            job["config"] = json.loads(config_str)
        except json.JSONDecodeError:
            job["config"] = {}

    return job


@router.get("/{job_id}/results")
def get_analysis_results(job_id: int):
    """Get analysis results for a completed job."""
    svc = get_data_service()
    job = svc.get_analysis_job(job_id)
    if not job:
        raise HTTPException(404, f"Job #{job_id} not found")

    if job.get("status") != "completed":
        return {
            "job_id": job_id,
            "status": job.get("status"),
            "message": "Analysis not yet completed",
        }

    # Return associated outputs
    outputs = svc.get_analysis_outputs()
    return {
        "job_id": job_id,
        "status": "completed",
        "outputs": outputs,
    }


@router.post("/{job_id}/execute")
def execute_analysis(job_id: int, background_tasks: BackgroundTasks):
    """Trigger analysis execution for a pending or failed job.

    On Vercel (hobby): will timeout after 10s — use CLI instead.
    On self-hosted / Vercel Pro: runs via BackgroundTasks.
    """
    svc = get_data_service()
    job = svc.get_analysis_job(job_id)
    if not job:
        raise HTTPException(404, f"Job #{job_id} not found")

    if job.get("status") not in ("pending", "failed"):
        raise HTTPException(
            400,
            f"Job #{job_id} is '{job.get('status')}' — can only execute pending or failed jobs",
        )

    job_type = job.get("job_type", "single_market")
    if job_type == "group_analysis":
        background_tasks.add_task(_execute_group, job_id)
    else:
        background_tasks.add_task(_execute_single, job_id)

    return {"job_id": job_id, "status": "executing"}


@router.get("")
def list_analysis_jobs(status: Optional[str] = Query(None)):
    """List all analysis jobs, optionally filtered by status."""
    svc = get_data_service()
    return svc.get_analysis_jobs(status=status)


# ------------------------------------------------------------------
# Background execution helpers
# ------------------------------------------------------------------

def _execute_single(job_id: int) -> None:
    """Background task: run a single-market analysis."""
    try:
        from src.web.services.analysis_runner import AnalysisRunnerService
        svc = get_data_service()
        runner = AnalysisRunnerService(svc)
        runner.run_single(job_id)
    except Exception as e:
        print(f"[!] Background single analysis #{job_id} failed: {e}")
        import traceback
        traceback.print_exc()


def _execute_group(job_id: int) -> None:
    """Background task: run a group analysis."""
    try:
        from src.web.services.analysis_runner import AnalysisRunnerService
        svc = get_data_service()
        runner = AnalysisRunnerService(svc)
        runner.run_group(job_id)
    except Exception as e:
        print(f"[!] Background group analysis #{job_id} failed: {e}")
        import traceback
        traceback.print_exc()
