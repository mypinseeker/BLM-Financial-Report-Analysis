"""Market-related API endpoints."""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from src.web.services.supabase_data import get_data_service

router = APIRouter(prefix="/api/markets", tags=["markets"])


@router.get("")
def list_markets():
    """Return all available markets."""
    svc = get_data_service()
    return svc.get_available_markets()


@router.get("/{market}/operators")
def market_operators(market: str):
    """Return operators in a market."""
    svc = get_data_service()
    ops = svc.get_operators_in_market(market)
    if not ops:
        raise HTTPException(404, f"No operators found for market '{market}'")
    return ops


@router.get("/{market}/tariffs")
def market_tariffs(market: str,
                   plan_type: Optional[str] = Query(None),
                   period: Optional[str] = Query(None)):
    """Return tariffs for a market with optional filters."""
    svc = get_data_service()
    return svc.get_tariffs_for_market(market, plan_type=plan_type, period=period)


@router.get("/{market}/competitive-scores")
def market_competitive_scores(market: str,
                              quarter: Optional[str] = Query(None)):
    """Return competitive scores for a market."""
    svc = get_data_service()
    return svc.get_competitive_scores(market, quarter=quarter)


@router.get("/{market}/macro")
def market_macro(market: str):
    """Return macro-economic data for a market (uses market_id as country)."""
    svc = get_data_service()
    return svc.get_macro_data(market)
