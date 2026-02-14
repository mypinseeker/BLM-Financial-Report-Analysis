"""TelecomDatabase - SQLite-backed data layer for BLM analysis.

All upsert methods auto-compute calendar_quarter via PeriodConverter.
Query methods return list[dict] for easy DataFrame conversion.
Supports :memory: databases for testing.
"""

import json
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

from src.database.period_utils import PeriodConverter, get_converter


class TelecomDatabase:
    """SQLite database for telecom operator financial and operational data.

    Args:
        db_path: Path to SQLite database file. Use ":memory:" for testing.
    """

    def __init__(self, db_path: str = "data/telecom.db"):
        self.db_path = db_path
        self.conn = None

    def init(self):
        """Initialize database: create connection and run schema."""
        if self.db_path == ":memory:":
            self.conn = sqlite3.connect(":memory:")
        else:
            db_file = Path(self.db_path)
            db_file.parent.mkdir(parents=True, exist_ok=True)
            self.conn = sqlite3.connect(str(db_file))

        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.execute("PRAGMA journal_mode = WAL")

        # Run schema
        schema_path = Path(__file__).parent / "schema.sql"
        with open(schema_path, "r") as f:
            schema_sql = f.read()
        self.conn.executescript(schema_sql)
        self.conn.commit()
        return self

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # =========================================================================
    # Upsert Methods
    # =========================================================================

    def upsert_operator(self, operator_id: str, **data):
        """Insert or update an operator record."""
        fields = {
            "operator_id": operator_id,
            "display_name": data.get("display_name", operator_id),
            "parent_company": data.get("parent_company"),
            "country": data.get("country", ""),
            "region": data.get("region"),
            "market": data.get("market", ""),
            "operator_type": data.get("operator_type"),
            "ir_url": data.get("ir_url"),
            "fiscal_year_start_month": data.get("fiscal_year_start_month", 1),
            "fiscal_year_label": data.get("fiscal_year_label", ""),
            "quarter_naming": data.get("quarter_naming", "calendar"),
            "currency": data.get("currency", "EUR"),
            "is_active": data.get("is_active", 1),
        }

        columns = ", ".join(fields.keys())
        placeholders = ", ".join(["?"] * len(fields))
        updates = ", ".join([
            f"{k} = excluded.{k}" for k in fields.keys()
            if k != "operator_id"
        ])

        sql = f"""
            INSERT INTO operators ({columns})
            VALUES ({placeholders})
            ON CONFLICT(operator_id) DO UPDATE SET {updates}
        """
        self.conn.execute(sql, list(fields.values()))
        self.conn.commit()

    def upsert_financial(self, operator_id: str, period: str, data: dict):
        """Insert or update a quarterly financial record.

        Auto-converts the operator period to calendar quarter using PeriodConverter.

        Args:
            operator_id: Operator identifier
            period: Operator-specific period string (e.g., "Q3 FY26" or "Q4 2025")
            data: Dict of financial metrics
        """
        converter = get_converter(operator_id)
        pi = converter.to_calendar_quarter(period)

        fields = {
            "operator_id": operator_id,
            "period": period,
            "calendar_quarter": pi.calendar_quarter,
            "period_start": pi.period_start.isoformat(),
            "period_end": pi.period_end.isoformat(),
            "report_date": data.get("report_date"),
            "report_status": data.get("report_status", "published"),
            "total_revenue": data.get("total_revenue"),
            "service_revenue": data.get("service_revenue"),
            "service_revenue_growth_pct": data.get("service_revenue_growth_pct"),
            "mobile_service_revenue": data.get("mobile_service_revenue"),
            "mobile_service_growth_pct": data.get("mobile_service_growth_pct"),
            "fixed_service_revenue": data.get("fixed_service_revenue"),
            "fixed_service_growth_pct": data.get("fixed_service_growth_pct"),
            "b2b_revenue": data.get("b2b_revenue"),
            "b2b_growth_pct": data.get("b2b_growth_pct"),
            "tv_revenue": data.get("tv_revenue"),
            "wholesale_revenue": data.get("wholesale_revenue"),
            "other_revenue": data.get("other_revenue"),
            "ebitda": data.get("ebitda"),
            "ebitda_margin_pct": data.get("ebitda_margin_pct"),
            "ebitda_growth_pct": data.get("ebitda_growth_pct"),
            "net_income": data.get("net_income"),
            "capex": data.get("capex"),
            "capex_to_revenue_pct": data.get("capex_to_revenue_pct"),
            "opex": data.get("opex"),
            "opex_to_revenue_pct": data.get("opex_to_revenue_pct"),
            "employees": data.get("employees"),
            "source_url": data.get("source_url"),
            "notes": data.get("notes"),
        }

        columns = ", ".join(fields.keys())
        placeholders = ", ".join(["?"] * len(fields))
        updates = ", ".join([
            f"{k} = excluded.{k}" for k in fields.keys()
            if k not in ("operator_id", "calendar_quarter")
        ])

        sql = f"""
            INSERT INTO financial_quarterly ({columns})
            VALUES ({placeholders})
            ON CONFLICT(operator_id, calendar_quarter) DO UPDATE SET {updates}
        """
        self.conn.execute(sql, list(fields.values()))
        self.conn.commit()

    def upsert_subscriber(self, operator_id: str, period: str, data: dict):
        """Insert or update a quarterly subscriber record.

        Auto-converts the operator period to calendar quarter.
        """
        converter = get_converter(operator_id)
        pi = converter.to_calendar_quarter(period)

        fields = {
            "operator_id": operator_id,
            "period": period,
            "calendar_quarter": pi.calendar_quarter,
            "period_start": pi.period_start.isoformat(),
            "period_end": pi.period_end.isoformat(),
            "report_status": data.get("report_status", "published"),
            "mobile_total_k": data.get("mobile_total_k"),
            "mobile_postpaid_k": data.get("mobile_postpaid_k"),
            "mobile_prepaid_k": data.get("mobile_prepaid_k"),
            "mobile_net_adds_k": data.get("mobile_net_adds_k"),
            "mobile_churn_pct": data.get("mobile_churn_pct"),
            "mobile_arpu": data.get("mobile_arpu"),
            "iot_connections_k": data.get("iot_connections_k"),
            "broadband_total_k": data.get("broadband_total_k"),
            "broadband_net_adds_k": data.get("broadband_net_adds_k"),
            "broadband_cable_k": data.get("broadband_cable_k"),
            "broadband_fiber_k": data.get("broadband_fiber_k"),
            "broadband_dsl_k": data.get("broadband_dsl_k"),
            "broadband_fwa_k": data.get("broadband_fwa_k"),
            "broadband_arpu": data.get("broadband_arpu"),
            "tv_total_k": data.get("tv_total_k"),
            "tv_net_adds_k": data.get("tv_net_adds_k"),
            "fmc_total_k": data.get("fmc_total_k"),
            "fmc_penetration_pct": data.get("fmc_penetration_pct"),
            "b2b_customers_k": data.get("b2b_customers_k"),
            "source_url": data.get("source_url"),
            "notes": data.get("notes"),
        }

        columns = ", ".join(fields.keys())
        placeholders = ", ".join(["?"] * len(fields))
        updates = ", ".join([
            f"{k} = excluded.{k}" for k in fields.keys()
            if k not in ("operator_id", "calendar_quarter")
        ])

        sql = f"""
            INSERT INTO subscriber_quarterly ({columns})
            VALUES ({placeholders})
            ON CONFLICT(operator_id, calendar_quarter) DO UPDATE SET {updates}
        """
        self.conn.execute(sql, list(fields.values()))
        self.conn.commit()

    def upsert_network(self, operator_id: str, calendar_quarter: str, data: dict):
        """Insert or update network infrastructure data."""
        fields = {
            "operator_id": operator_id,
            "calendar_quarter": calendar_quarter,
            "five_g_coverage_pct": data.get("five_g_coverage_pct"),
            "four_g_coverage_pct": data.get("four_g_coverage_pct"),
            "fiber_homepass_k": data.get("fiber_homepass_k"),
            "fiber_connected_k": data.get("fiber_connected_k"),
            "cable_homepass_k": data.get("cable_homepass_k"),
            "cable_docsis31_pct": data.get("cable_docsis31_pct"),
            "technology_mix": (
                json.dumps(data["technology_mix"])
                if "technology_mix" in data and data["technology_mix"] is not None
                else None
            ),
            "quality_scores": (
                json.dumps(data["quality_scores"])
                if "quality_scores" in data and data["quality_scores"] is not None
                else None
            ),
            "source_url": data.get("source_url"),
            "notes": data.get("notes"),
        }

        columns = ", ".join(fields.keys())
        placeholders = ", ".join(["?"] * len(fields))
        updates = ", ".join([
            f"{k} = excluded.{k}" for k in fields.keys()
            if k not in ("operator_id", "calendar_quarter")
        ])

        sql = f"""
            INSERT INTO network_infrastructure ({columns})
            VALUES ({placeholders})
            ON CONFLICT(operator_id, calendar_quarter) DO UPDATE SET {updates}
        """
        self.conn.execute(sql, list(fields.values()))
        self.conn.commit()

    def upsert_competitive_scores(self, operator_id: str,
                                   calendar_quarter: str,
                                   scores_dict: dict):
        """Insert or update competitive scores for an operator.

        Args:
            operator_id: Operator identifier
            calendar_quarter: e.g., "CQ4_2025"
            scores_dict: Maps dimension name to score (1-100),
                         e.g., {"Network Coverage": 80, "Brand Strength": 82}
        """
        for dimension, score in scores_dict.items():
            sql = """
                INSERT INTO competitive_scores
                    (operator_id, calendar_quarter, dimension, score)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(operator_id, calendar_quarter, dimension)
                DO UPDATE SET score = excluded.score
            """
            self.conn.execute(sql, [operator_id, calendar_quarter, dimension, score])
        self.conn.commit()

    def upsert_intelligence(self, event_data: dict):
        """Insert an intelligence event."""
        fields = {
            "operator_id": event_data.get("operator_id"),
            "market": event_data.get("market"),
            "event_date": event_data.get("event_date"),
            "category": event_data.get("category"),
            "title": event_data.get("title"),
            "description": event_data.get("description"),
            "impact_type": event_data.get("impact_type"),
            "severity": event_data.get("severity"),
            "source_url": event_data.get("source_url"),
            "notes": event_data.get("notes"),
        }

        columns = ", ".join(fields.keys())
        placeholders = ", ".join(["?"] * len(fields))

        sql = f"""
            INSERT INTO intelligence_events ({columns})
            VALUES ({placeholders})
        """
        self.conn.execute(sql, list(fields.values()))
        self.conn.commit()

    def upsert_macro(self, country: str, calendar_quarter: str, data: dict):
        """Insert or update macro environment data."""
        fields = {
            "country": country,
            "calendar_quarter": calendar_quarter,
            "gdp_growth_pct": data.get("gdp_growth_pct"),
            "inflation_pct": data.get("inflation_pct"),
            "unemployment_pct": data.get("unemployment_pct"),
            "telecom_market_size_eur_b": data.get("telecom_market_size_eur_b"),
            "telecom_growth_pct": data.get("telecom_growth_pct"),
            "five_g_adoption_pct": data.get("five_g_adoption_pct"),
            "fiber_penetration_pct": data.get("fiber_penetration_pct"),
            "regulatory_environment": data.get("regulatory_environment"),
            "digital_strategy": data.get("digital_strategy"),
            "energy_cost_index": data.get("energy_cost_index"),
            "consumer_confidence_index": data.get("consumer_confidence_index"),
            "source_url": data.get("source_url"),
            "notes": data.get("notes"),
        }

        columns = ", ".join(fields.keys())
        placeholders = ", ".join(["?"] * len(fields))
        updates = ", ".join([
            f"{k} = excluded.{k}" for k in fields.keys()
            if k not in ("country", "calendar_quarter")
        ])

        sql = f"""
            INSERT INTO macro_environment ({columns})
            VALUES ({placeholders})
            ON CONFLICT(country, calendar_quarter) DO UPDATE SET {updates}
        """
        self.conn.execute(sql, list(fields.values()))
        self.conn.commit()

    def upsert_executive(self, operator_id: str, data: dict):
        """Insert or update an executive record."""
        fields = {
            "operator_id": operator_id,
            "name": data.get("name"),
            "title": data.get("title"),
            "start_date": data.get("start_date"),
            "end_date": data.get("end_date"),
            "is_current": data.get("is_current", 1),
            "background": data.get("background"),
            "notes": data.get("notes"),
        }

        columns = ", ".join(fields.keys())
        placeholders = ", ".join(["?"] * len(fields))
        updates = ", ".join([
            f"{k} = excluded.{k}" for k in fields.keys()
            if k not in ("operator_id", "name", "title")
        ])

        sql = f"""
            INSERT INTO executives ({columns})
            VALUES ({placeholders})
            ON CONFLICT(operator_id, name, title) DO UPDATE SET {updates}
        """
        self.conn.execute(sql, list(fields.values()))
        self.conn.commit()

    def upsert_tariff(self, operator_id: str, plan_name: str,
                       plan_type: str, snapshot_period: str, data: dict):
        """Insert or update a tariff record.

        Args:
            operator_id: Operator identifier
            plan_name: Plan name (e.g., "GigaMobil M")
            plan_type: Plan type (e.g., "mobile_postpaid")
            snapshot_period: Half-year period (e.g., "H1_2026")
            data: Dict with plan details (monthly_price, data_allowance, etc.)
        """
        fields = {
            "operator_id": operator_id,
            "plan_name": plan_name,
            "plan_type": plan_type,
            "snapshot_period": snapshot_period,
            "plan_tier": data.get("plan_tier"),
            "monthly_price": data.get("monthly_price"),
            "data_allowance": data.get("data_allowance"),
            "speed_mbps": data.get("speed_mbps"),
            "contract_months": data.get("contract_months"),
            "includes_5g": data.get("includes_5g", 0),
            "technology": data.get("technology"),
            "effective_date": data.get("effective_date"),
            "source_url": data.get("source_url"),
            "notes": data.get("notes"),
        }

        columns = ", ".join(fields.keys())
        placeholders = ", ".join(["?"] * len(fields))
        updates = ", ".join([
            f"{k} = excluded.{k}" for k in fields.keys()
            if k not in ("operator_id", "plan_name", "plan_type", "snapshot_period")
        ])

        sql = f"""
            INSERT INTO tariffs ({columns})
            VALUES ({placeholders})
            ON CONFLICT(operator_id, plan_name, plan_type, snapshot_period)
            DO UPDATE SET {updates}
        """
        self.conn.execute(sql, list(fields.values()))
        self.conn.commit()

    def upsert_earnings_highlight(self, operator_id: str,
                                   calendar_quarter: str, data: dict):
        """Insert an earnings call highlight."""
        fields = {
            "operator_id": operator_id,
            "calendar_quarter": calendar_quarter,
            "segment": data.get("segment"),
            "highlight_type": data.get("highlight_type"),
            "content": data.get("content"),
            "speaker": data.get("speaker"),
            "source_url": data.get("source_url"),
            "notes": data.get("notes"),
        }

        columns = ", ".join(fields.keys())
        placeholders = ", ".join(["?"] * len(fields))

        sql = f"""
            INSERT INTO earnings_call_highlights ({columns})
            VALUES ({placeholders})
        """
        self.conn.execute(sql, list(fields.values()))
        self.conn.commit()

    # =========================================================================
    # User Feedback
    # =========================================================================

    def upsert_feedback(self, feedback_data: dict):
        """Insert or update a user feedback record.

        Conflict on (analysis_job_id, operator_id, look_category, finding_ref).
        """
        fields = {
            "analysis_job_id": feedback_data.get("analysis_job_id"),
            "operator_id": feedback_data.get("operator_id", ""),
            "period": feedback_data.get("period", ""),
            "look_category": feedback_data["look_category"],
            "finding_ref": feedback_data.get("finding_ref", ""),
            "feedback_type": feedback_data.get("feedback_type", "confirmed"),
            "original_value": feedback_data.get("original_value"),
            "user_comment": feedback_data.get("user_comment", ""),
            "user_value": feedback_data.get("user_value"),
        }

        columns = ", ".join(fields.keys())
        placeholders = ", ".join(["?"] * len(fields))
        updates = ", ".join([
            f"{k} = excluded.{k}" for k in fields.keys()
            if k not in ("analysis_job_id", "operator_id", "look_category", "finding_ref")
        ])

        sql = f"""
            INSERT INTO user_feedback ({columns})
            VALUES ({placeholders})
            ON CONFLICT(analysis_job_id, operator_id, look_category, finding_ref)
            DO UPDATE SET {updates}
        """
        self.conn.execute(sql, list(fields.values()))
        self.conn.commit()

    def get_feedback(self, analysis_job_id: Optional[int] = None,
                     operator_id: Optional[str] = None,
                     look_category: Optional[str] = None) -> list:
        """Query user feedback with optional filters."""
        conditions = []
        params = []

        if analysis_job_id is not None:
            conditions.append("analysis_job_id = ?")
            params.append(analysis_job_id)
        if operator_id is not None:
            conditions.append("operator_id = ?")
            params.append(operator_id)
        if look_category is not None:
            conditions.append("look_category = ?")
            params.append(look_category)

        where_clause = (" WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = f"""
            SELECT * FROM user_feedback
            {where_clause}
            ORDER BY created_at DESC
        """
        rows = self.conn.execute(sql, params).fetchall()
        return self._rows_to_dicts(rows)

    def clear_feedback(self, analysis_job_id: int,
                       operator_id: str) -> int:
        """Delete all feedback for a given job + operator. Returns deleted count."""
        cursor = self.conn.execute(
            "DELETE FROM user_feedback WHERE analysis_job_id = ? AND operator_id = ?",
            [analysis_job_id, operator_id],
        )
        self.conn.commit()
        return cursor.rowcount

    # =========================================================================
    # Query Methods
    # =========================================================================

    def _rows_to_dicts(self, rows) -> list:
        """Convert sqlite3.Row objects to list of dicts."""
        return [dict(row) for row in rows]

    def get_financial_timeseries(self, operator_id: str,
                                 n_quarters: int = 8,
                                 end_cq: Optional[str] = None) -> list:
        """Get financial data time series for an operator.

        Returns list of dicts ordered by calendar_quarter ascending.
        """
        timeline = get_converter(operator_id).generate_timeline(
            n_quarters=n_quarters, end_cq=end_cq
        )

        placeholders = ", ".join(["?"] * len(timeline))
        sql = f"""
            SELECT * FROM financial_quarterly
            WHERE operator_id = ?
              AND calendar_quarter IN ({placeholders})
            ORDER BY period_start ASC
        """
        rows = self.conn.execute(sql, [operator_id] + timeline).fetchall()
        return self._rows_to_dicts(rows)

    def get_subscriber_timeseries(self, operator_id: str,
                                   n_quarters: int = 8,
                                   end_cq: Optional[str] = None) -> list:
        """Get subscriber data time series for an operator."""
        timeline = get_converter(operator_id).generate_timeline(
            n_quarters=n_quarters, end_cq=end_cq
        )

        placeholders = ", ".join(["?"] * len(timeline))
        sql = f"""
            SELECT * FROM subscriber_quarterly
            WHERE operator_id = ?
              AND calendar_quarter IN ({placeholders})
            ORDER BY period_start ASC
        """
        rows = self.conn.execute(sql, [operator_id] + timeline).fetchall()
        return self._rows_to_dicts(rows)

    def get_market_comparison(self, market: str,
                               calendar_quarter: str) -> list:
        """Get all operators' data for a single quarter in a market.

        Joins operators + financial_quarterly + subscriber_quarterly.
        Returns one row per operator.
        """
        sql = """
            SELECT
                o.operator_id,
                o.display_name,
                o.operator_type,
                f.calendar_quarter,
                f.total_revenue,
                f.service_revenue,
                f.service_revenue_growth_pct,
                f.mobile_service_revenue,
                f.mobile_service_growth_pct,
                f.fixed_service_revenue,
                f.fixed_service_growth_pct,
                f.b2b_revenue,
                f.b2b_growth_pct,
                f.ebitda,
                f.ebitda_margin_pct,
                f.ebitda_growth_pct,
                f.capex,
                f.capex_to_revenue_pct,
                s.mobile_total_k,
                s.mobile_postpaid_k,
                s.mobile_churn_pct,
                s.mobile_arpu,
                s.broadband_total_k,
                s.broadband_net_adds_k,
                s.broadband_fiber_k,
                s.tv_total_k,
                s.fmc_total_k,
                s.fmc_penetration_pct,
                s.b2b_customers_k
            FROM operators o
            LEFT JOIN financial_quarterly f
                ON o.operator_id = f.operator_id
                AND f.calendar_quarter = ?
            LEFT JOIN subscriber_quarterly s
                ON o.operator_id = s.operator_id
                AND s.calendar_quarter = ?
            WHERE o.market = ?
              AND o.is_active = 1
            ORDER BY f.total_revenue DESC
        """
        rows = self.conn.execute(
            sql, [calendar_quarter, calendar_quarter, market]
        ).fetchall()
        return self._rows_to_dicts(rows)

    def get_market_timeseries(self, market: str,
                               n_quarters: int = 8,
                               end_cq: Optional[str] = None) -> list:
        """Get all operators' financial data across quarters for a market.

        Returns list of dicts with operator_id and calendar_quarter.
        """
        # Use a generic converter for timeline generation
        converter = PeriodConverter()
        timeline = converter.generate_timeline(
            n_quarters=n_quarters, end_cq=end_cq
        )

        placeholders = ", ".join(["?"] * len(timeline))
        sql = f"""
            SELECT
                o.operator_id,
                o.display_name,
                o.operator_type,
                f.*
            FROM operators o
            JOIN financial_quarterly f
                ON o.operator_id = f.operator_id
            WHERE o.market = ?
              AND o.is_active = 1
              AND f.calendar_quarter IN ({placeholders})
            ORDER BY f.period_start ASC, f.total_revenue DESC
        """
        rows = self.conn.execute(sql, [market] + timeline).fetchall()
        return self._rows_to_dicts(rows)

    def get_macro_data(self, country: str,
                        n_quarters: int = 8,
                        end_cq: Optional[str] = None) -> list:
        """Get macro environment data for a country."""
        converter = PeriodConverter()
        timeline = converter.generate_timeline(
            n_quarters=n_quarters, end_cq=end_cq
        )

        placeholders = ", ".join(["?"] * len(timeline))
        sql = f"""
            SELECT * FROM macro_environment
            WHERE country = ?
              AND calendar_quarter IN ({placeholders})
            ORDER BY calendar_quarter ASC
        """
        rows = self.conn.execute(sql, [country] + timeline).fetchall()
        return self._rows_to_dicts(rows)

    def get_network_data(self, operator_id: str,
                          calendar_quarter: Optional[str] = None) -> dict:
        """Get network infrastructure data.

        If calendar_quarter is None, returns the latest available.
        """
        if calendar_quarter:
            sql = """
                SELECT * FROM network_infrastructure
                WHERE operator_id = ? AND calendar_quarter = ?
            """
            row = self.conn.execute(sql, [operator_id, calendar_quarter]).fetchone()
        else:
            sql = """
                SELECT * FROM network_infrastructure
                WHERE operator_id = ?
                ORDER BY calendar_quarter DESC
                LIMIT 1
            """
            row = self.conn.execute(sql, [operator_id]).fetchone()

        if row:
            result = dict(row)
            # Parse JSON fields
            if result.get("technology_mix"):
                result["technology_mix"] = json.loads(result["technology_mix"])
            if result.get("quality_scores"):
                result["quality_scores"] = json.loads(result["quality_scores"])
            return result
        return {}

    def get_competitive_scores(self, market: str,
                                calendar_quarter: str) -> list:
        """Get competitive scores for all operators in a market for a quarter."""
        sql = """
            SELECT
                o.operator_id,
                o.display_name,
                cs.dimension,
                cs.score,
                cs.notes
            FROM operators o
            JOIN competitive_scores cs
                ON o.operator_id = cs.operator_id
            WHERE o.market = ?
              AND cs.calendar_quarter = ?
            ORDER BY o.operator_id, cs.dimension
        """
        rows = self.conn.execute(sql, [market, calendar_quarter]).fetchall()
        return self._rows_to_dicts(rows)

    def get_intelligence_events(self, market: Optional[str] = None,
                                 operator_id: Optional[str] = None,
                                 category: Optional[str] = None,
                                 days_back: int = 180) -> list:
        """Get intelligence events with optional filters."""
        cutoff = (date.today() - timedelta(days=days_back)).isoformat()
        conditions = ["event_date >= ?"]
        params = [cutoff]

        if market:
            conditions.append("market = ?")
            params.append(market)
        if operator_id:
            conditions.append("operator_id = ?")
            params.append(operator_id)
        if category:
            conditions.append("category = ?")
            params.append(category)

        where_clause = " AND ".join(conditions)
        sql = f"""
            SELECT * FROM intelligence_events
            WHERE {where_clause}
            ORDER BY event_date DESC
        """
        rows = self.conn.execute(sql, params).fetchall()
        return self._rows_to_dicts(rows)

    def get_operators_in_market(self, market: str) -> list:
        """Get all active operators in a market."""
        sql = """
            SELECT * FROM operators
            WHERE market = ? AND is_active = 1
            ORDER BY operator_type, display_name
        """
        rows = self.conn.execute(sql, [market]).fetchall()
        return self._rows_to_dicts(rows)

    def get_executives(self, operator_id: str) -> list:
        """Get executives for an operator."""
        sql = """
            SELECT * FROM executives
            WHERE operator_id = ?
            ORDER BY is_current DESC, start_date DESC
        """
        rows = self.conn.execute(sql, [operator_id]).fetchall()
        return self._rows_to_dicts(rows)

    def get_earnings_highlights(self, operator_id: str,
                                 calendar_quarter: Optional[str] = None) -> list:
        """Get earnings call highlights."""
        if calendar_quarter:
            sql = """
                SELECT * FROM earnings_call_highlights
                WHERE operator_id = ? AND calendar_quarter = ?
                ORDER BY highlight_type, segment
            """
            rows = self.conn.execute(sql, [operator_id, calendar_quarter]).fetchall()
        else:
            sql = """
                SELECT * FROM earnings_call_highlights
                WHERE operator_id = ?
                ORDER BY calendar_quarter DESC, highlight_type, segment
            """
            rows = self.conn.execute(sql, [operator_id]).fetchall()
        return self._rows_to_dicts(rows)

    def get_tariffs(self, operator_id: Optional[str] = None,
                     market: Optional[str] = None,
                     plan_type: Optional[str] = None,
                     snapshot_period: Optional[str] = None) -> list:
        """Get tariffs with optional filters.

        Joins operators table when filtering by market.
        """
        conditions = []
        params = []

        if market:
            conditions.append("o.market = ?")
            params.append(market)
        if operator_id:
            conditions.append("t.operator_id = ?")
            params.append(operator_id)
        if plan_type:
            conditions.append("t.plan_type = ?")
            params.append(plan_type)
        if snapshot_period:
            conditions.append("t.snapshot_period = ?")
            params.append(snapshot_period)

        where_clause = (" WHERE " + " AND ".join(conditions)) if conditions else ""

        sql = f"""
            SELECT t.*, o.display_name, o.market
            FROM tariffs t
            JOIN operators o ON t.operator_id = o.operator_id
            {where_clause}
            ORDER BY t.operator_id, t.plan_type, t.plan_tier, t.snapshot_period
        """
        rows = self.conn.execute(sql, params).fetchall()
        return self._rows_to_dicts(rows)

    def get_tariff_comparison(self, market: str, plan_type: str,
                               snapshot_period: str) -> list:
        """Cross-operator tariff comparison for a given plan type and period.

        Returns one row per tariff, grouped by operator, sorted by monthly_price.
        """
        sql = """
            SELECT
                t.operator_id,
                o.display_name,
                t.plan_name,
                t.plan_type,
                t.plan_tier,
                t.monthly_price,
                t.data_allowance,
                t.speed_mbps,
                t.includes_5g,
                t.snapshot_period
            FROM tariffs t
            JOIN operators o ON t.operator_id = o.operator_id
            WHERE o.market = ?
              AND t.plan_type = ?
              AND t.snapshot_period = ?
            ORDER BY t.plan_tier, t.monthly_price ASC
        """
        rows = self.conn.execute(sql, [market, plan_type, snapshot_period]).fetchall()
        return self._rows_to_dicts(rows)
