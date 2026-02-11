"""Operator groups API endpoints."""

from fastapi import APIRouter, HTTPException
from src.web.services.supabase_data import get_data_service

router = APIRouter(prefix="/api/groups", tags=["groups"])


@router.get("")
def list_groups():
    """Return all operator groups."""
    svc = get_data_service()
    return svc.get_operator_groups()


@router.get("/{group_id}")
def get_group(group_id: str):
    """Return group details with subsidiaries."""
    svc = get_data_service()
    group = svc.get_operator_group(group_id)
    if not group:
        raise HTTPException(404, f"Group '{group_id}' not found")

    subs = svc.get_group_subsidiaries(group_id)
    group["subsidiaries"] = subs
    return group


@router.get("/{group_id}/data-status")
def get_group_data_status(group_id: str):
    """Return data completeness for each subsidiary market."""
    svc = get_data_service()
    group = svc.get_operator_group(group_id)
    if not group:
        raise HTTPException(404, f"Group '{group_id}' not found")

    return svc.get_group_data_status(group_id)


@router.get("/{group_id}/markets")
def get_group_markets(group_id: str):
    """Return markets where the group operates."""
    svc = get_data_service()
    subs = svc.get_group_subsidiaries(group_id)
    markets = []
    seen = set()
    for s in subs:
        m = s.get("market", "")
        if m and m not in seen:
            seen.add(m)
            market_info = svc.get_market(m)
            if market_info:
                # Attach competitors
                all_ops = svc.get_operators_in_market(m)
                competitors = [
                    o for o in all_ops
                    if o["operator_id"] != s.get("operator_id")
                ]
                market_info["tigo_operator"] = s.get("operator_id", "")
                market_info["local_brand"] = s.get("local_brand", "")
                market_info["competitors"] = competitors
                markets.append(market_info)
    return markets
