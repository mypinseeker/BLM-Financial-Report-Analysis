"""HTML page routes — renders Jinja2 templates."""

from fastapi import APIRouter, Request, HTTPException

from src.web.app import templates
from src.web.services.supabase_data import get_data_service

router = APIRouter(tags=["pages"])


@router.get("/")
def dashboard(request: Request):
    svc = get_data_service()
    markets = svc.get_available_markets()

    # Attach operator count to each market
    for m in markets:
        ops = svc.get_operators_in_market(m.get("market_id", ""))
        m["operators_count"] = len(ops)

    cloud_status = svc.get_cloud_status()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "markets": markets,
        "cloud_status": cloud_status,
    })


@router.get("/analyze")
def analyze_page(request: Request):
    """Analysis target selection wizard."""
    svc = get_data_service()
    markets = svc.get_available_markets()
    groups = svc.get_operator_groups()

    return templates.TemplateResponse("analyze.html", {
        "request": request,
        "markets": markets,
        "groups": groups,
    })


@router.get("/market/{market_id}")
def market_page(request: Request, market_id: str):
    svc = get_data_service()
    market_info = svc.get_market(market_id)
    if not market_info:
        raise HTTPException(404, f"Market '{market_id}' not found")

    operators = svc.get_operators_in_market(market_id)
    tariffs = svc.get_tariffs_for_market(market_id)
    macro = svc.get_macro_data(market_info.get("country", market_id.capitalize()))
    market_outputs = svc.get_analysis_outputs(market_id=market_id)
    network = svc.get_network_data(market_id)

    return templates.TemplateResponse("market.html", {
        "request": request,
        "market_id": market_id,
        "market_info": market_info,
        "operators": operators,
        "tariffs": tariffs,
        "macro": macro,
        "market_outputs": market_outputs,
        "network": network,
    })


@router.get("/operator/{operator_id}")
def operator_page(request: Request, operator_id: str):
    svc = get_data_service()
    operator = svc.get_operator(operator_id)
    if not operator:
        raise HTTPException(404, f"Operator '{operator_id}' not found")

    financial = svc.get_financial_timeseries(operator_id)
    subscribers = svc.get_subscriber_timeseries(operator_id)

    return templates.TemplateResponse("operator.html", {
        "request": request,
        "operator": operator,
        "financial": financial,
        "subscribers": subscribers,
    })


@router.get("/outputs")
def outputs_page(request: Request):
    svc = get_data_service()
    outputs = svc.get_analysis_outputs()
    recent = svc.get_recent_outputs(10)
    markets = svc.get_available_markets()

    # Build market display-name lookup
    market_names = {m["market_id"]: m.get("display_name", m["market_id"]) for m in markets}

    # Group outputs by market_id
    by_market: dict[str, list[dict]] = {}
    for o in outputs:
        mid = o.get("market_id") or "unknown"
        by_market.setdefault(mid, []).append(o)

    # Alphabetically sorted market IDs (only those with outputs)
    sorted_markets = sorted(by_market.keys(), key=lambda m: market_names.get(m, m).lower())

    return templates.TemplateResponse("outputs.html", {
        "request": request,
        "outputs": outputs,
        "recent": recent,
        "by_market": by_market,
        "sorted_markets": sorted_markets,
        "market_names": market_names,
    })


# ------------------------------------------------------------------
# API: data status for a market (used by analyze wizard)
# ------------------------------------------------------------------

@router.get("/api/data-status/{market_id}")
def data_status_api(market_id: str):
    """Return data completeness for a market."""
    svc = get_data_service()
    return svc.get_data_status_for_market(market_id)


# ------------------------------------------------------------------
# Review pages
# ------------------------------------------------------------------

@router.get("/feedback/{job_id}")
def feedback_page(request: Request, job_id: int):
    """Feedback review page for an analysis job."""
    svc = get_data_service()
    job = svc.get_analysis_job(job_id)
    if not job:
        raise HTTPException(404, f"Analysis job #{job_id} not found")
    return templates.TemplateResponse("feedback.html", {
        "request": request,
        "job": job,
        "job_id": job_id,
    })


@router.get("/report/{output_id}")
def report_page(request: Request, output_id: int):
    """Interactive report viewer for analysis JSON output."""
    svc = get_data_service()
    output = svc.get_analysis_outputs()
    record = None
    for o in output:
        if o.get("id") == output_id:
            record = o
            break
    if not record:
        raise HTTPException(404, f"Output #{output_id} not found")
    return templates.TemplateResponse("report.html", {
        "request": request,
        "output_id": output_id,
        "record": record,
    })


@router.get("/audit")
def audit_page(request: Request):
    """Market readiness audit dashboard."""
    svc = get_data_service()
    markets = svc.get_available_markets()
    # Build operator map for each market
    market_operators = {}
    for m in markets:
        mid = m.get("market_id", "")
        ops = svc.get_operators_in_market(mid)
        market_operators[mid] = [
            {"operator_id": o["operator_id"], "display_name": o.get("display_name", "")}
            for o in ops
        ]
    import json as _json
    return templates.TemplateResponse("audit_page.html", {
        "request": request,
        "markets": markets,
        "market_operators_json": _json.dumps(market_operators),
    })


@router.get("/review")
def review_list_page(request: Request):
    """List all extraction jobs for review."""
    svc = get_data_service()
    jobs = svc.list_extraction_jobs()
    return templates.TemplateResponse("review_list.html", {
        "request": request,
        "jobs": jobs,
    })


@router.get("/review/{job_id}")
def review_page(request: Request, job_id: int):
    """Review a specific extraction job."""
    import json
    svc = get_data_service()
    job = svc.get_extraction_job(job_id)

    # Parse JSON fields
    extracted = {}
    if job:
        raw = job.get("extracted_data") or {}
        if isinstance(raw, str):
            try:
                extracted = json.loads(raw)
            except json.JSONDecodeError:
                extracted = {}
        else:
            extracted = raw

    return templates.TemplateResponse("review.html", {
        "request": request,
        "job": job,
        "extracted_json": json.dumps(extracted) if job else "{}",
    })
