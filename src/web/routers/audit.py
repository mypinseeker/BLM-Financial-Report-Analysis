"""Market readiness audit API endpoint."""

from fastapi import APIRouter, HTTPException, Query

from src.web.services.supabase_data import get_data_service
from src.web.services.market_audit import MarketAuditService

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.get("/{market}")
def audit_market(
    market: str,
    operator: str = Query(..., description="Target operator ID"),
    reference: str = Query(None, description="Reference market ID (omit for absolute thresholds)"),
    ref_operator: str = Query(None, description="Reference operator ID"),
    period: str = Query("CQ4_2025", description="Analysis period"),
    n_quarters: int = Query(8, description="Historical range in quarters"),
):
    """Run a market readiness audit.

    GET /api/audit/chile?operator=entel_cl&reference=germany&ref_operator=vodafone_germany
    """
    svc = get_data_service()

    # Validate target market
    target_ops = svc.get_operators_in_market(market)
    if not target_ops:
        raise HTTPException(404, f"No operators found for market '{market}'")

    op_ids = [o["operator_id"] for o in target_ops]
    if operator not in op_ids:
        raise HTTPException(404, f"Operator '{operator}' not found in market '{market}'")

    # Validate reference if provided
    if reference and ref_operator:
        ref_ops = svc.get_operators_in_market(reference)
        ref_ids = [o["operator_id"] for o in ref_ops]
        if ref_operator not in ref_ids:
            raise HTTPException(404, f"Operator '{ref_operator}' not found in market '{reference}'")

    audit_svc = MarketAuditService(svc)
    report = audit_svc.run_audit(
        target_market=market,
        target_operator=operator,
        reference=reference or "",
        ref_operator=ref_operator or "",
        period=period,
        n_quarters=n_quarters,
    )

    return report.to_dict()
