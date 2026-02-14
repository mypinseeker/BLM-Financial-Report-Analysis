"""Dashboard API endpoints — aggregate KPIs and cross-market data."""

import json
from typing import Optional

from fastapi import APIRouter, Query

from src.web.services.supabase_data import get_data_service

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary")
def dashboard_summary():
    """Aggregate KPIs across all markets."""
    svc = get_data_service()
    markets = svc.get_available_markets()
    cloud = svc.get_cloud_status()

    total_operators = 0
    for m in markets:
        ops = svc.get_operators_in_market(m.get("market_id", ""))
        m["operators_count"] = len(ops)
        total_operators += len(ops)

    # Analysis jobs summary
    jobs = svc.get_analysis_jobs()
    completed = [j for j in jobs if j.get("status") == "completed"]
    pending = [j for j in jobs if j.get("status") == "pending"]
    failed = [j for j in jobs if j.get("status") == "failed"]

    return {
        "total_markets": len(markets),
        "total_operators": total_operators,
        "total_data_rows": cloud.get("total", 0),
        "financial_records": cloud.get("financial_quarterly", 0),
        "subscriber_records": cloud.get("subscriber_quarterly", 0),
        "tariff_records": cloud.get("tariffs", 0),
        "analysis_jobs": {
            "total": len(jobs),
            "completed": len(completed),
            "pending": len(pending),
            "failed": len(failed),
        },
        "latest_job": completed[-1] if completed else None,
        "markets": markets,
    }


@router.get("/comparison")
def market_comparison(period: str = Query("CQ4_2025")):
    """Cross-market comparison with financial metrics."""
    svc = get_data_service()
    markets = svc.get_available_markets()

    comparison = []
    for m in markets:
        mid = m.get("market_id", "")
        ops = svc.get_operators_in_market(mid)

        # Get latest financial data for each operator
        market_row = {
            "market_id": mid,
            "display_name": m.get("display_name", mid.replace("_", " ").title()),
            "country": m.get("country", ""),
            "currency": m.get("currency", "EUR"),
            "operators_count": len(ops),
            "operators": [],
            "total_revenue": 0,
            "total_subs_k": 0,
        }

        for op in ops:
            op_id = op.get("operator_id", "")
            fin = svc.get_financial_timeseries(op_id)
            subs = svc.get_subscriber_timeseries(op_id)

            # Latest financial
            latest_fin = fin[-1] if fin else {}
            latest_subs = subs[-1] if subs else {}

            rev = latest_fin.get("total_revenue") or 0
            ebitda = latest_fin.get("ebitda") or 0
            ebitda_margin = latest_fin.get("ebitda_margin_pct") or 0
            mobile = latest_subs.get("mobile_total_k") or 0
            bb = latest_subs.get("broadband_total_k") or 0

            # Build revenue trend (last 8 quarters)
            rev_trend = [f.get("total_revenue") or 0 for f in fin[-8:]]

            market_row["operators"].append({
                "operator_id": op_id,
                "display_name": op.get("display_name", ""),
                "revenue": rev,
                "ebitda": ebitda,
                "ebitda_margin": round(ebitda_margin, 1),
                "mobile_subs_k": mobile,
                "broadband_subs_k": bb,
                "total_subs_k": mobile + bb,
                "revenue_trend": rev_trend,
                "period": latest_fin.get("calendar_quarter", period),
            })

            market_row["total_revenue"] += rev
            market_row["total_subs_k"] += mobile + bb

        market_row["total_revenue"] = round(market_row["total_revenue"], 1)
        comparison.append(market_row)

    # Sort by total revenue descending
    comparison.sort(key=lambda x: x["total_revenue"], reverse=True)
    return comparison


@router.get("/report-data/{output_id}")
def get_report_data(output_id: int):
    """Download and return analysis JSON for the report viewer."""
    svc = get_data_service()
    record = svc.get_output(output_id)
    if not record:
        return {"error": "Output not found"}

    storage_path = record.get("storage_path", "")
    if not storage_path.endswith(".json"):
        return {"error": "Not a JSON output"}

    try:
        data = svc.download_output_file(storage_path)
        return json.loads(data)
    except Exception as exc:
        return {"error": f"Failed to load: {exc}"}
