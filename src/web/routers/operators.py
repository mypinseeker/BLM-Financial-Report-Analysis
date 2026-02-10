"""Operator-related API endpoints."""

from fastapi import APIRouter, HTTPException

from src.web.services.supabase_data import get_data_service

router = APIRouter(prefix="/api/operators", tags=["operators"])


@router.get("/{operator_id}")
def get_operator(operator_id: str):
    """Return operator info."""
    svc = get_data_service()
    op = svc.get_operator(operator_id)
    if not op:
        raise HTTPException(404, f"Operator '{operator_id}' not found")
    return op


@router.get("/{operator_id}/financial")
def operator_financial(operator_id: str):
    """Return financial time series for an operator."""
    svc = get_data_service()
    return svc.get_financial_timeseries(operator_id)


@router.get("/{operator_id}/subscribers")
def operator_subscribers(operator_id: str):
    """Return subscriber time series for an operator."""
    svc = get_data_service()
    return svc.get_subscriber_timeseries(operator_id)
