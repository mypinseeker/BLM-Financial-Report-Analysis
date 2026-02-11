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
    # Operator Groups
    # ------------------------------------------------------------------

    def get_operator_groups(self) -> list[dict]:
        """Return all operator groups."""
        return self._select("operator_groups", order="group_name")

    def get_operator_group(self, group_id: str) -> dict | None:
        rows = self._select("operator_groups", filters={"group_id": group_id}, limit=1)
        return rows[0] if rows else None

    def get_group_subsidiaries(self, group_id: str) -> list[dict]:
        """Return subsidiaries for a group with operator details."""
        subs = self._select("group_subsidiaries", filters={"group_id": group_id})
        for s in subs:
            op = self.get_operator(s.get("operator_id", ""))
            if op:
                s["operator_display_name"] = op.get("display_name", "")
                s["country"] = op.get("country", "")
        return subs

    def get_group_data_status(self, group_id: str) -> list[dict]:
        """Return data completeness for each subsidiary market."""
        subs = self.get_group_subsidiaries(group_id)
        results = []
        for s in subs:
            market = s.get("market", "")
            op_id = s.get("operator_id", "")
            status = self._get_data_status_for_operator(op_id, market)
            status["market"] = market
            status["operator_id"] = op_id
            status["local_brand"] = s.get("local_brand", "")
            status["country"] = s.get("country", "")
            results.append(status)
        return results

    def _get_data_status_for_operator(self, operator_id: str, market: str) -> dict:
        """Check data completeness for a specific operator."""
        tables = {
            "financial": ("financial_quarterly", {"operator_id": operator_id}),
            "subscriber": ("subscriber_quarterly", {"operator_id": operator_id}),
            "network": ("network_infrastructure", {"operator_id": operator_id}),
        }
        # Market-level tables
        market_tables = {
            "tariffs": ("tariffs", None),  # need operator IDs
            "macro": ("macro_environment", {"country": market.replace("_", " ").title()}),
        }

        result = {}
        for key, (table, filters) in tables.items():
            try:
                rows = self._select(table, filters=filters, limit=1)
                result[key] = len(rows) > 0
            except Exception:
                result[key] = False

        # Tariffs: check if any operator in this market has tariff data
        try:
            ops = self.get_operators_in_market(market)
            op_ids = [o["operator_id"] for o in ops]
            if op_ids:
                q = self._client.table("tariffs").select("id", count="exact").in_("operator_id", op_ids).limit(1)
                resp = q.execute()
                result["tariffs"] = (resp.count or 0) > 0
            else:
                result["tariffs"] = False
        except Exception:
            result["tariffs"] = False

        for key, (table, filters) in market_tables.items():
            if key == "tariffs":
                continue
            try:
                rows = self._select(table, filters=filters, limit=1)
                result[key] = len(rows) > 0
            except Exception:
                result[key] = False

        # Calculate overall completeness percentage
        checks = list(result.values())
        result["completeness_pct"] = int(sum(checks) / max(len(checks), 1) * 100)
        return result

    def get_data_status_for_market(self, market_id: str) -> dict:
        """Return data completeness summary for a market."""
        ops = self.get_operators_in_market(market_id)
        if not ops:
            return {"completeness_pct": 0, "operators": []}

        op_statuses = []
        for op in ops:
            status = self._get_data_status_for_operator(
                op["operator_id"], market_id
            )
            status["operator_id"] = op["operator_id"]
            status["display_name"] = op.get("display_name", "")
            op_statuses.append(status)

        avg_pct = int(
            sum(s["completeness_pct"] for s in op_statuses) / max(len(op_statuses), 1)
        )
        return {
            "market_id": market_id,
            "completeness_pct": avg_pct,
            "operators": op_statuses,
        }

    # ------------------------------------------------------------------
    # Analysis Jobs
    # ------------------------------------------------------------------

    def create_analysis_job(self, job_data: dict) -> dict:
        """Create a new analysis job and return it."""
        resp = self._client.table("analysis_jobs").insert(job_data).execute()
        return resp.data[0] if resp.data else {}

    def get_analysis_job(self, job_id: int) -> dict | None:
        rows = self._select("analysis_jobs", filters={"id": job_id}, limit=1)
        return rows[0] if rows else None

    def update_analysis_job(self, job_id: int, updates: dict) -> dict | None:
        resp = (
            self._client.table("analysis_jobs")
            .update(updates)
            .eq("id", job_id)
            .execute()
        )
        return resp.data[0] if resp.data else None

    def get_analysis_jobs(self, status: str | None = None) -> list[dict]:
        filters = {}
        if status:
            filters["status"] = status
        return self._select("analysis_jobs", filters=filters, order="created_at")

    # ------------------------------------------------------------------
    # Extraction Jobs
    # ------------------------------------------------------------------

    def create_extraction_job(self, job_data: dict) -> dict:
        """Create a new extraction job and return it."""
        resp = self._client.table("extraction_jobs").insert(job_data).execute()
        return resp.data[0] if resp.data else {}

    def get_extraction_job(self, job_id: int) -> dict | None:
        rows = self._select("extraction_jobs", filters={"id": job_id}, limit=1)
        return rows[0] if rows else None

    def update_extraction_job(self, job_id: int, updates: dict) -> dict | None:
        resp = (
            self._client.table("extraction_jobs")
            .update(updates)
            .eq("id", job_id)
            .execute()
        )
        return resp.data[0] if resp.data else None

    def list_extraction_jobs(self, status: str | None = None) -> list[dict]:
        filters = {}
        if status:
            filters["status"] = status
        return self._select("extraction_jobs", filters=filters, order="created_at")

    # ------------------------------------------------------------------
    # 5-Table Upsert (for extraction pipeline)
    # ------------------------------------------------------------------

    def upsert_financial_quarterly(self, rows: list[dict]) -> list[dict]:
        """Upsert financial_quarterly rows. Conflict: operator_id,calendar_quarter."""
        if not rows:
            return []
        resp = (
            self._client.table("financial_quarterly")
            .upsert(rows, on_conflict="operator_id,calendar_quarter")
            .execute()
        )
        return resp.data or []

    def upsert_subscriber_quarterly(self, rows: list[dict]) -> list[dict]:
        """Upsert subscriber_quarterly rows. Conflict: operator_id,calendar_quarter."""
        if not rows:
            return []
        resp = (
            self._client.table("subscriber_quarterly")
            .upsert(rows, on_conflict="operator_id,calendar_quarter")
            .execute()
        )
        return resp.data or []

    def upsert_tariffs(self, rows: list[dict]) -> list[dict]:
        """Upsert tariffs rows. Conflict: operator_id,plan_name,plan_type,snapshot_period."""
        if not rows:
            return []
        resp = (
            self._client.table("tariffs")
            .upsert(rows, on_conflict="operator_id,plan_name,plan_type,snapshot_period")
            .execute()
        )
        return resp.data or []

    def upsert_macro_environment(self, rows: list[dict]) -> list[dict]:
        """Upsert macro_environment rows. Conflict: country,calendar_quarter."""
        if not rows:
            return []
        resp = (
            self._client.table("macro_environment")
            .upsert(rows, on_conflict="country,calendar_quarter")
            .execute()
        )
        return resp.data or []

    def upsert_network_infrastructure(self, rows: list[dict]) -> list[dict]:
        """Upsert network_infrastructure rows. Conflict: operator_id,calendar_quarter."""
        if not rows:
            return []
        resp = (
            self._client.table("network_infrastructure")
            .upsert(rows, on_conflict="operator_id,calendar_quarter")
            .execute()
        )
        return resp.data or []

    # ------------------------------------------------------------------
    # Source Registry & Provenance
    # ------------------------------------------------------------------

    def register_source(self, source_data: dict) -> dict:
        """Register a data source. Upsert on source_id."""
        resp = (
            self._client.table("source_registry")
            .upsert(source_data, on_conflict="source_id")
            .execute()
        )
        return resp.data[0] if resp.data else {}

    def record_provenance(self, provenance_rows: list[dict]) -> int:
        """Insert provenance records. Returns count of inserted rows."""
        if not provenance_rows:
            return 0
        resp = (
            self._client.table("data_provenance")
            .insert(provenance_rows)
            .execute()
        )
        return len(resp.data) if resp.data else 0

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
