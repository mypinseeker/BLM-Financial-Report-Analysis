"""SupabaseDataService — Web-specific data layer querying Supabase REST API.

Wraps BLMSupabaseClient with methods tailored for the FastAPI web app.
All queries go directly to Supabase (no SQLite, no heavy deps).
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from supabase import create_client, Client


class SupabaseDataService:
    """Stateless data service for web queries against Supabase."""

    def __init__(self, client: Client):
        self._client = client

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------

    def _select(self, table: str, columns: str = "*",
                filters: dict | None = None,
                order: str | None = None,
                limit: int = 1000) -> list[dict]:
        """Generic select helper."""
        q = self._client.table(table).select(columns).limit(limit)
        if filters:
            for col, val in filters.items():
                q = q.eq(col, val)
        if order:
            q = q.order(order)
        resp = q.execute()
        return resp.data or []

    def _count(self, table: str) -> int:
        resp = self._client.table(table).select("*", count="exact").execute()
        return resp.count if resp.count is not None else 0

    # ------------------------------------------------------------------
    # Markets
    # ------------------------------------------------------------------

    def get_available_markets(self) -> list[dict]:
        """Return all market configs."""
        rows = self._select("market_configs", order="market_id")
        for m in rows:
            m.setdefault("display_name", m.get("market_name", ""))
        return rows

    def get_market(self, market_id: str) -> dict | None:
        rows = self._select("market_configs", filters={"market_id": market_id}, limit=1)
        if rows:
            rows[0].setdefault("display_name", rows[0].get("market_name", ""))
            return rows[0]
        return None

    # ------------------------------------------------------------------
    # Operators
    # ------------------------------------------------------------------

    def get_operators_in_market(self, market: str) -> list[dict]:
        """Active operators in a market, sorted by type then name."""
        rows = self._select(
            "operators",
            filters={"market": market, "is_active": True},
        )
        rows.sort(key=lambda r: (r.get("operator_type", ""), r.get("display_name", "")))
        return rows

    def get_operator(self, operator_id: str) -> dict | None:
        rows = self._select("operators", filters={"operator_id": operator_id}, limit=1)
        return rows[0] if rows else None

    # ------------------------------------------------------------------
    # Financial time series
    # ------------------------------------------------------------------

    def get_financial_timeseries(self, operator_id: str) -> list[dict]:
        """Financial quarterly data for an operator, ordered by period_start."""
        return self._select(
            "financial_quarterly",
            filters={"operator_id": operator_id},
            order="period_start",
        )

    # ------------------------------------------------------------------
    # Subscriber time series
    # ------------------------------------------------------------------

    def get_subscriber_timeseries(self, operator_id: str) -> list[dict]:
        """Subscriber quarterly data, ordered by period_start."""
        return self._select(
            "subscriber_quarterly",
            filters={"operator_id": operator_id},
            order="period_start",
        )

    # ------------------------------------------------------------------
    # Tariffs
    # ------------------------------------------------------------------

    def get_tariffs_for_market(self, market: str,
                               plan_type: Optional[str] = None,
                               period: Optional[str] = None) -> list[dict]:
        """Get tariffs for all operators in a market.

        Two-step: get operator IDs, then query tariffs.
        """
        operators = self.get_operators_in_market(market)
        if not operators:
            return []

        op_ids = [o["operator_id"] for o in operators]
        op_name_map = {o["operator_id"]: o["display_name"] for o in operators}

        # Supabase .in_() filter
        q = self._client.table("tariffs").select("*").in_("operator_id", op_ids)
        if plan_type:
            q = q.eq("plan_type", plan_type)
        if period:
            q = q.eq("snapshot_period", period)
        q = q.order("operator_id").order("plan_type").order("monthly_price")
        resp = q.execute()
        rows = resp.data or []

        # Attach display name
        for r in rows:
            r["display_name"] = op_name_map.get(r.get("operator_id"), "")

        return rows

    # ------------------------------------------------------------------
    # Competitive scores
    # ------------------------------------------------------------------

    def get_competitive_scores(self, market: str,
                               quarter: Optional[str] = None) -> list[dict]:
        """Competitive scores for all operators in a market."""
        operators = self.get_operators_in_market(market)
        if not operators:
            return []

        op_ids = [o["operator_id"] for o in operators]
        op_name_map = {o["operator_id"]: o["display_name"] for o in operators}

        q = self._client.table("competitive_scores").select("*").in_("operator_id", op_ids)
        if quarter:
            q = q.eq("calendar_quarter", quarter)
        q = q.order("operator_id").order("dimension")
        resp = q.execute()
        rows = resp.data or []

        for r in rows:
            r["display_name"] = op_name_map.get(r.get("operator_id"), "")

        return rows

    # ------------------------------------------------------------------
    # Macro environment
    # ------------------------------------------------------------------

    def get_macro_data(self, country: str) -> list[dict]:
        return self._select(
            "macro_environment",
            filters={"country": country},
            order="calendar_quarter",
        )

    # ------------------------------------------------------------------
    # Analysis outputs
    # ------------------------------------------------------------------

    def get_analysis_outputs(self, market_id: Optional[str] = None) -> list[dict]:
        filters = {}
        if market_id:
            filters["market_id"] = market_id
        return self._select("analysis_outputs", filters=filters, order="created_at")

    def get_output(self, output_id: int) -> dict | None:
        rows = self._select("analysis_outputs", filters={"id": output_id}, limit=1)
        return rows[0] if rows else None

    # ------------------------------------------------------------------
    # Storage download
    # ------------------------------------------------------------------

    def download_output_file(self, storage_path: str) -> bytes:
        """Download a file from Supabase Storage (blm-outputs bucket)."""
        return self._client.storage.from_("blm-outputs").download(storage_path)

    # ------------------------------------------------------------------
    # Cloud status
    # ------------------------------------------------------------------

    def get_cloud_status(self) -> dict:
        """Return row counts for all core tables."""
        tables = [
            "market_configs", "operators", "financial_quarterly",
            "subscriber_quarterly", "tariffs", "competitive_scores",
            "macro_environment", "network_infrastructure",
            "intelligence_events", "executives",
            "earnings_call_highlights", "analysis_outputs",
        ]
        status = {}
        for t in tables:
            try:
                status[t] = self._count(t)
            except Exception:
                status[t] = -1
        status["total"] = sum(v for v in status.values() if v > 0)
        return status


# ------------------------------------------------------------------
# Singleton factory
# ------------------------------------------------------------------

_service: SupabaseDataService | None = None


def get_data_service() -> SupabaseDataService:
    """Return a cached SupabaseDataService instance."""
    global _service
    if _service is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")
        if not url or not key:
            raise RuntimeError(
                "Missing SUPABASE_URL or SUPABASE_SERVICE_KEY env vars"
            )
        client = create_client(url, key)
        _service = SupabaseDataService(client)
    return _service
