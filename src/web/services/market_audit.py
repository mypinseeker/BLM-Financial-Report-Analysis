"""MarketAuditService — Three-layer market readiness audit.

Compares a target market/operator against a reference (or absolute thresholds)
across Data, Analysis, and Provenance layers. Produces scored, graded reports
with actionable recommendations.

Usage:
    svc = SupabaseDataService(client)
    audit = MarketAuditService(svc)
    report = audit.run_audit("chile", "entel_cl", "germany", "vodafone_germany", "CQ4_2025", 8)
    print(audit.format_console_report(report))
"""

from __future__ import annotations

import tempfile
import traceback
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.web.services.supabase_data import SupabaseDataService


# ======================================================================
# Dataclasses
# ======================================================================

@dataclass
class TableAudit:
    table_name: str
    operator_id: str = ""
    row_count: int = 0
    reference_row_count: int = 0
    field_completeness: float = 0.0       # 0-1 ratio of non-null fields
    reference_completeness: float = 0.0
    quarter_coverage: list = field(default_factory=list)
    reference_quarters: list = field(default_factory=list)

    @property
    def row_ratio(self) -> float:
        if self.reference_row_count == 0:
            return 1.0 if self.row_count > 0 else 0.0
        return min(self.row_count / self.reference_row_count, 1.0)

    @property
    def quarter_ratio(self) -> float:
        if not self.reference_quarters:
            return 1.0 if self.quarter_coverage else 0.0
        return min(len(self.quarter_coverage) / len(self.reference_quarters), 1.0)

    @property
    def score(self) -> float:
        return (0.40 * self.row_ratio + 0.35 * self.field_completeness + 0.25 * self.quarter_ratio) * 100

    def to_dict(self) -> dict:
        return {
            "table_name": self.table_name,
            "operator_id": self.operator_id,
            "row_count": self.row_count,
            "reference_row_count": self.reference_row_count,
            "field_completeness": round(self.field_completeness, 3),
            "reference_completeness": round(self.reference_completeness, 3),
            "quarter_count": len(self.quarter_coverage),
            "reference_quarter_count": len(self.reference_quarters),
            "score": round(self.score, 1),
        }


@dataclass
class AnalysisMetrics:
    """Counts extracted from a FiveLooksResult."""
    # Look 1 - Trends
    pest_factor_count: int = 0
    policy_opportunities: int = 0
    policy_threats: int = 0
    # Look 2 - Market/Customer
    market_changes: int = 0
    market_opportunities: int = 0
    customer_segments: int = 0
    appeals_dimensions: int = 0
    # Look 3 - Competition
    competitor_deep_dives: int = 0
    competitor_fields_filled: int = 0
    # Look 4 - Self
    segment_analyses: int = 0
    exposure_points: int = 0
    bmc_fields_filled: int = 0
    # SWOT
    swot_total: int = 0
    strategy_count: int = 0
    # Look 5 - Opportunities
    span_positions: int = 0
    opportunity_items: int = 0
    # Provenance
    unique_sources: int = 0
    estimated_pct: float = 0.0
    total_data_points: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DimensionScore:
    dimension: str
    target_value: float = 0
    reference_value: float = 0
    score_pct: float = 0.0
    grade: str = ""
    recommendation: str = ""

    def to_dict(self) -> dict:
        return {
            "dimension": self.dimension,
            "target_value": self.target_value,
            "reference_value": self.reference_value,
            "score_pct": round(self.score_pct, 1),
            "grade": self.grade,
            "recommendation": self.recommendation,
        }


@dataclass
class AuditReport:
    target_market: str
    reference_market: str
    target_operator: str
    reference_operator: str
    period: str
    timestamp: str
    # Data layer
    data_audit: list = field(default_factory=list)
    data_score: float = 0.0
    # Analysis layer
    target_metrics: AnalysisMetrics = field(default_factory=AnalysisMetrics)
    reference_metrics: AnalysisMetrics = field(default_factory=AnalysisMetrics)
    analysis_dimensions: list = field(default_factory=list)
    analysis_score: float = 0.0
    # Provenance layer
    provenance_dimensions: list = field(default_factory=list)
    provenance_score: float = 0.0
    # Overall
    overall_score: float = 0.0
    overall_grade: str = ""
    top_recommendations: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "target_market": self.target_market,
            "reference_market": self.reference_market,
            "target_operator": self.target_operator,
            "reference_operator": self.reference_operator,
            "period": self.period,
            "timestamp": self.timestamp,
            "data_audit": [t.to_dict() if hasattr(t, "to_dict") else t for t in self.data_audit],
            "data_score": round(self.data_score, 1),
            "target_metrics": self.target_metrics.to_dict(),
            "reference_metrics": self.reference_metrics.to_dict(),
            "analysis_dimensions": [d.to_dict() if hasattr(d, "to_dict") else d for d in self.analysis_dimensions],
            "analysis_score": round(self.analysis_score, 1),
            "provenance_dimensions": [d.to_dict() if hasattr(d, "to_dict") else d for d in self.provenance_dimensions],
            "provenance_score": round(self.provenance_score, 1),
            "overall_score": round(self.overall_score, 1),
            "overall_grade": self.overall_grade,
            "top_recommendations": self.top_recommendations,
        }


# ======================================================================
# Absolute thresholds (used when no reference market)
# ======================================================================

ABSOLUTE_THRESHOLDS = {
    "pest_factor_count": 12,
    "policy_opportunities": 3,
    "policy_threats": 2,
    "market_changes": 5,
    "market_opportunities": 4,
    "customer_segments": 5,
    "appeals_dimensions": 8,
    "competitor_deep_dives": 2,
    "segment_analyses": 3,
    "exposure_points": 2,
    "bmc_fields_filled": 7,
    "span_positions": 20,
    "opportunity_items": 5,
    "unique_sources": 5,
    "total_data_points": 20,
}

# Tables to audit with their key fields for completeness checking
AUDIT_TABLES = {
    "financial_quarterly": {
        "key_fields": [
            "total_revenue", "service_revenue", "ebitda", "ebitda_margin_pct",
            "capex", "mobile_service_revenue", "fixed_service_revenue",
            "b2b_revenue", "net_income",
        ],
        "quarter_col": "calendar_quarter",
        "operator_col": "operator_id",
    },
    "subscriber_quarterly": {
        "key_fields": [
            "total_mobile_subs", "postpaid_subs", "prepaid_subs",
            "fixed_broadband_subs", "tv_subs", "mobile_arpu",
            "postpaid_arpu", "churn_rate_pct",
        ],
        "quarter_col": "calendar_quarter",
        "operator_col": "operator_id",
    },
    "network_infrastructure": {
        "key_fields": [
            "coverage_4g_pct", "coverage_5g_pct", "fiber_homes_passed",
            "fiber_homes_connected", "cable_homes_passed",
        ],
        "quarter_col": "calendar_quarter",
        "operator_col": "operator_id",
    },
    "tariffs": {
        "key_fields": [
            "plan_name", "plan_type", "monthly_price", "data_gb",
            "speed_down_mbps",
        ],
        "quarter_col": "snapshot_period",
        "operator_col": "operator_id",
    },
    "intelligence_events": {
        "key_fields": [
            "title", "category", "description", "impact_type",
            "source_url",
        ],
        "quarter_col": None,
        "operator_col": None,
        "market_col": "market",
    },
    "competitive_scores": {
        "key_fields": [
            "dimension", "score", "explanation",
        ],
        "quarter_col": "calendar_quarter",
        "operator_col": "operator_id",
    },
    "macro_environment": {
        "key_fields": [
            "gdp_growth_pct", "inflation_pct", "unemployment_pct",
            "population_millions", "internet_penetration_pct",
        ],
        "quarter_col": "calendar_quarter",
        "operator_col": None,
        "market_col": "country",
    },
    "earnings_call_highlights": {
        "key_fields": [
            "topic", "speaker", "quote", "sentiment",
        ],
        "quarter_col": "calendar_quarter",
        "operator_col": "operator_id",
    },
}


# ======================================================================
# Service
# ======================================================================

class MarketAuditService:
    """Three-layer market readiness audit: Data → Analysis → Provenance."""

    WEIGHT_DATA = 0.35
    WEIGHT_ANALYSIS = 0.45
    WEIGHT_PROVENANCE = 0.20

    def __init__(self, svc: SupabaseDataService):
        self.svc = svc

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run_audit(
        self,
        target_market: str,
        target_operator: str,
        reference: str = "",
        ref_operator: str = "",
        period: str = "CQ4_2025",
        n_quarters: int = 8,
    ) -> AuditReport:
        """Run a complete three-layer audit.

        1. Pull target + reference data into temp SQLite DBs
        2. Audit data layer (row counts, field completeness, quarter coverage)
        3. Run engine on both → FiveLooksResult
        4. Extract AnalysisMetrics, compare analysis richness
        5. Assess provenance quality
        6. Score, grade, generate recommendations
        """
        report = AuditReport(
            target_market=target_market,
            reference_market=reference,
            target_operator=target_operator,
            reference_operator=ref_operator,
            period=period,
            timestamp=datetime.utcnow().isoformat(),
        )

        target_tmp = None
        ref_tmp = None

        try:
            # 1. Pull data
            print(f"\n  [1/6] Pulling data for target market: {target_market}")
            target_tmp = tempfile.mkdtemp(prefix="audit_target_")
            target_db_path = str(Path(target_tmp) / "target.db")
            target_db = self._pull_market(target_market, target_db_path)

            ref_db = None
            if reference and ref_operator:
                print(f"  [1/6] Pulling data for reference market: {reference}")
                ref_tmp = tempfile.mkdtemp(prefix="audit_ref_")
                ref_db_path = str(Path(ref_tmp) / "reference.db")
                ref_db = self._pull_market(reference, ref_db_path)

            # 2. Audit data layer
            print(f"  [2/6] Auditing data layer...")
            data_audits, data_score = self._audit_data_layer(
                target_db, ref_db, target_operator, ref_operator, target_market, reference
            )
            report.data_audit = data_audits
            report.data_score = data_score

            # 3. Run engine on target
            print(f"  [3/6] Running engine on target: {target_operator}")
            target_result = self._run_engine_safe(
                target_db, target_operator, target_market, period, n_quarters
            )

            # 4. Run engine on reference (if provided)
            ref_result = None
            if ref_db and ref_operator:
                print(f"  [4/6] Running engine on reference: {ref_operator}")
                ref_result = self._run_engine_safe(
                    ref_db, ref_operator, reference, period, n_quarters
                )
            else:
                print(f"  [4/6] No reference market — using absolute thresholds")

            # 5. Extract metrics and compare
            print(f"  [5/6] Comparing analysis output richness...")
            target_metrics = self._extract_metrics(target_result) if target_result else AnalysisMetrics()
            ref_metrics = self._extract_metrics(ref_result) if ref_result else AnalysisMetrics()
            report.target_metrics = target_metrics
            report.reference_metrics = ref_metrics

            analysis_dims, analysis_score = self._compare_analysis(
                target_metrics, ref_metrics, has_reference=bool(ref_result)
            )
            report.analysis_dimensions = analysis_dims
            report.analysis_score = analysis_score

            # 6. Provenance
            print(f"  [6/6] Assessing provenance quality...")
            prov_dims, prov_score = self._audit_provenance(
                target_metrics, ref_metrics, has_reference=bool(ref_result)
            )
            report.provenance_dimensions = prov_dims
            report.provenance_score = prov_score

            # Overall scoring
            report.overall_score = (
                self.WEIGHT_DATA * report.data_score
                + self.WEIGHT_ANALYSIS * report.analysis_score
                + self.WEIGHT_PROVENANCE * report.provenance_score
            )
            report.overall_grade = self._grade(report.overall_score)
            report.top_recommendations = self._generate_recommendations(report)

            # Cleanup
            if target_db:
                target_db.close()
            if ref_db:
                ref_db.close()

        except Exception as e:
            print(f"  [!] Audit error: {e}")
            traceback.print_exc()
            report.top_recommendations = [f"Audit failed: {e}"]
        finally:
            self._cleanup_temp(target_tmp)
            self._cleanup_temp(ref_tmp)

        return report

    # ------------------------------------------------------------------
    # Data layer
    # ------------------------------------------------------------------

    def _pull_market(self, market: str, db_path: str):
        """Reuse BLMCloudSync.pull_all() pattern from AnalysisRunnerService."""
        from src.database.db import TelecomDatabase
        from src.database.supabase_sync import BLMCloudSync

        db = TelecomDatabase(db_path)
        db.init()

        syncer = BLMCloudSync(local_db=db)
        report = syncer.pull_all(market)
        total_rows = sum(report.tables.values())
        print(f"    Pulled {total_rows} rows across {len(report.tables)} tables")
        return db

    def _audit_data_layer(
        self, target_db, ref_db, target_op: str, ref_op: str,
        target_market: str, ref_market: str,
    ) -> tuple:
        """Audit tables: row counts, field completeness, quarter coverage."""
        audits = []

        for table_name, config in AUDIT_TABLES.items():
            key_fields = config["key_fields"]
            quarter_col = config.get("quarter_col")
            operator_col = config.get("operator_col")
            market_col = config.get("market_col")

            # Build WHERE clause for target
            target_rows = self._query_table(
                target_db, table_name, operator_col, target_op, market_col, target_market
            )
            ref_rows = []
            if ref_db:
                ref_rows = self._query_table(
                    ref_db, table_name, operator_col, ref_op, market_col, ref_market
                )

            # Field completeness
            target_completeness = self._calc_field_completeness(target_rows, key_fields)
            ref_completeness = self._calc_field_completeness(ref_rows, key_fields) if ref_rows else 0.0

            # Quarter coverage
            target_quarters = self._extract_quarters(target_rows, quarter_col) if quarter_col else []
            ref_quarters = self._extract_quarters(ref_rows, quarter_col) if quarter_col and ref_rows else []

            audit = TableAudit(
                table_name=table_name,
                operator_id=target_op,
                row_count=len(target_rows),
                reference_row_count=len(ref_rows),
                field_completeness=target_completeness,
                reference_completeness=ref_completeness,
                quarter_coverage=target_quarters,
                reference_quarters=ref_quarters,
            )
            audits.append(audit)

        # Average score
        if audits:
            data_score = sum(a.score for a in audits) / len(audits)
        else:
            data_score = 0.0

        return audits, data_score

    def _query_table(self, db, table_name: str, operator_col: str | None,
                     operator_id: str, market_col: str | None, market: str) -> list:
        """Query rows from a SQLite table with optional operator/market filters."""
        conditions = []
        params = []
        if operator_col and operator_id:
            conditions.append(f"{operator_col} = ?")
            params.append(operator_id)
        if market_col and market:
            conditions.append(f"{market_col} = ?")
            params.append(market)

        where = f" WHERE {' AND '.join(conditions)}" if conditions else ""
        try:
            cursor = db.conn.execute(f"SELECT * FROM {table_name}{where}", params)
            return [dict(row) for row in cursor.fetchall()]
        except Exception:
            return []

    def _calc_field_completeness(self, rows: list, key_fields: list) -> float:
        """Calculate ratio of non-null key fields across all rows."""
        if not rows or not key_fields:
            return 0.0
        total_cells = 0
        filled_cells = 0
        for row in rows:
            for f in key_fields:
                total_cells += 1
                val = row.get(f)
                if val is not None and val != "" and val != 0:
                    filled_cells += 1
        return filled_cells / total_cells if total_cells > 0 else 0.0

    def _extract_quarters(self, rows: list, quarter_col: str) -> list:
        """Get unique quarters present in the data."""
        quarters = set()
        for row in rows:
            q = row.get(quarter_col)
            if q:
                quarters.add(q)
        return sorted(quarters)

    # ------------------------------------------------------------------
    # Analysis layer
    # ------------------------------------------------------------------

    def _run_engine_safe(self, db, operator: str, market: str,
                         period: str, n_quarters: int):
        """Run BLMAnalysisEngine.run_five_looks(), return None on failure."""
        try:
            from src.blm.engine import BLMAnalysisEngine

            engine = BLMAnalysisEngine(
                db=db,
                target_operator=operator,
                market=market,
                target_period=period,
                n_quarters=n_quarters,
            )
            return engine.run_five_looks()
        except Exception as e:
            print(f"    [!] Engine failed for {operator}: {e}")
            traceback.print_exc()
            return None

    def _extract_metrics(self, result) -> AnalysisMetrics:
        """Count items from each look's output dataclass."""
        m = AnalysisMetrics()

        # Look 1 - Trends
        if result.trends and result.trends.pest:
            pest = result.trends.pest
            m.pest_factor_count = (
                len(pest.political_factors)
                + len(pest.economic_factors)
                + len(pest.society_factors)
                + len(pest.technology_factors)
            )
            m.policy_opportunities = len(pest.policy_opportunities)
            m.policy_threats = len(pest.policy_threats)

        # Look 2 - Market/Customer
        if result.market_customer:
            mc = result.market_customer
            m.market_changes = len(mc.changes)
            m.market_opportunities = len(mc.opportunities)
            m.customer_segments = len(mc.customer_segments)
            m.appeals_dimensions = len(mc.appeals_assessment)

        # Look 3 - Competition
        if result.competition:
            comp = result.competition
            m.competitor_deep_dives = len(comp.competitor_analyses)
            # Count filled fields across all deep dives
            filled = 0
            for _op, dd in comp.competitor_analyses.items():
                if dd.growth_strategy:
                    filled += 1
                if dd.business_model:
                    filled += 1
                if dd.product_portfolio:
                    filled += 1
                if dd.problems:
                    filled += 1
                if dd.ma_activity:
                    filled += 1
            m.competitor_fields_filled = filled

        # Look 4 - Self
        if result.self_analysis:
            sa = result.self_analysis
            m.segment_analyses = len(sa.segment_analyses)
            m.exposure_points = len(sa.exposure_points)
            # BMC fields filled
            bmc = sa.bmc
            bmc_count = 0
            for fld in [
                "key_partners", "key_activities", "key_resources",
                "value_propositions", "customer_relationships",
                "channels", "customer_segments", "cost_structure",
                "revenue_streams",
            ]:
                if getattr(bmc, fld, None):
                    bmc_count += 1
            m.bmc_fields_filled = bmc_count

        # SWOT
        if result.swot:
            sw = result.swot
            m.swot_total = (
                len(sw.strengths) + len(sw.weaknesses)
                + len(sw.opportunities) + len(sw.threats)
            )
            m.strategy_count = (
                len(sw.so_strategies) + len(sw.wo_strategies)
                + len(sw.st_strategies) + len(sw.wt_strategies)
            )

        # Look 5 - Opportunities
        if result.opportunities:
            opp = result.opportunities
            m.span_positions = len(opp.span_positions)
            m.opportunity_items = len(opp.opportunities)

        # Provenance
        if result.provenance:
            qr = result.provenance.quality_report()
            m.unique_sources = qr.get("unique_sources", 0)
            m.total_data_points = qr.get("total_data_points", 0)
            estimated = qr.get("estimated", 0)
            m.estimated_pct = (estimated / m.total_data_points * 100) if m.total_data_points > 0 else 100.0

        return m

    def _compare_analysis(
        self, target: AnalysisMetrics, reference: AnalysisMetrics,
        has_reference: bool = True,
    ) -> tuple:
        """Compare 16 analysis dimensions. Returns (list[DimensionScore], avg_score)."""
        dimensions = [
            ("PEST Factors", "pest_factor_count"),
            ("Policy Opportunities", "policy_opportunities"),
            ("Policy Threats", "policy_threats"),
            ("Market Changes", "market_changes"),
            ("Market Opportunities", "market_opportunities"),
            ("Customer Segments", "customer_segments"),
            ("APPEALS Dimensions", "appeals_dimensions"),
            ("Competitor Deep Dives", "competitor_deep_dives"),
            ("Competitor Fields Filled", "competitor_fields_filled"),
            ("Segment Analyses", "segment_analyses"),
            ("Exposure Points", "exposure_points"),
            ("BMC Fields Filled", "bmc_fields_filled"),
            ("SWOT Total Items", "swot_total"),
            ("Strategy Count", "strategy_count"),
            ("SPAN Positions", "span_positions"),
            ("Opportunity Items", "opportunity_items"),
        ]

        scores = []
        for label, attr in dimensions:
            t_val = getattr(target, attr, 0)
            if has_reference:
                r_val = getattr(reference, attr, 0)
            else:
                r_val = ABSOLUTE_THRESHOLDS.get(attr, 1)

            if r_val > 0:
                pct = min(t_val / r_val, 1.0) * 100
            elif t_val > 0:
                pct = 100.0
            else:
                pct = 0.0

            grade = self._grade(pct)
            rec = self._dimension_recommendation(label, t_val, r_val, grade, has_reference)

            scores.append(DimensionScore(
                dimension=label,
                target_value=t_val,
                reference_value=r_val,
                score_pct=pct,
                grade=grade,
                recommendation=rec,
            ))

        avg = sum(d.score_pct for d in scores) / len(scores) if scores else 0.0
        return scores, avg

    def _dimension_recommendation(
        self, label: str, target: float, ref: float,
        grade: str, has_reference: bool,
    ) -> str:
        """Generate actionable recommendation for a dimension."""
        if grade in ("A", "B"):
            return ""
        ref_text = f"vs {int(ref)} in reference" if has_reference else f"(threshold: {int(ref)})"
        if target == 0:
            return f"Missing: 0 {ref_text} — add data/events to populate this dimension"
        return f"Low: {int(target)} {ref_text} — enrich input data for better coverage"

    # ------------------------------------------------------------------
    # Provenance layer
    # ------------------------------------------------------------------

    def _audit_provenance(
        self, target: AnalysisMetrics, reference: AnalysisMetrics,
        has_reference: bool = True,
    ) -> tuple:
        """Assess provenance quality across 3 dimensions."""
        dims = []

        # 1. Unique sources
        t_sources = target.unique_sources
        r_sources = reference.unique_sources if has_reference else ABSOLUTE_THRESHOLDS.get("unique_sources", 5)
        if r_sources > 0:
            src_pct = min(t_sources / r_sources, 1.0) * 100
        elif t_sources > 0:
            src_pct = 100.0
        else:
            src_pct = 0.0

        dims.append(DimensionScore(
            dimension="Unique Sources",
            target_value=t_sources,
            reference_value=r_sources,
            score_pct=src_pct,
            grade=self._grade(src_pct),
            recommendation="" if self._grade(src_pct) in ("A", "B") else
                f"{t_sources} sources — run extraction pipeline to add real source documents",
        ))

        # 2. Non-estimated data %
        t_non_est = 100.0 - target.estimated_pct
        r_non_est = (100.0 - reference.estimated_pct) if has_reference else 80.0
        if r_non_est > 0:
            non_est_pct = min(t_non_est / r_non_est, 1.0) * 100
        elif t_non_est > 0:
            non_est_pct = 100.0
        else:
            non_est_pct = 0.0

        dims.append(DimensionScore(
            dimension="Non-Estimated Data %",
            target_value=round(t_non_est, 1),
            reference_value=round(r_non_est, 1),
            score_pct=non_est_pct,
            grade=self._grade(non_est_pct),
            recommendation="" if self._grade(non_est_pct) in ("A", "B") else
                f"{t_non_est:.0f}% non-estimated — add source_url to data rows for provenance",
        ))

        # 3. Data point coverage
        t_dp = target.total_data_points
        r_dp = reference.total_data_points if has_reference else ABSOLUTE_THRESHOLDS.get("total_data_points", 20)
        if r_dp > 0:
            dp_pct = min(t_dp / r_dp, 1.0) * 100
        elif t_dp > 0:
            dp_pct = 100.0
        else:
            dp_pct = 0.0

        dims.append(DimensionScore(
            dimension="Tracked Data Points",
            target_value=t_dp,
            reference_value=r_dp,
            score_pct=dp_pct,
            grade=self._grade(dp_pct),
            recommendation="" if self._grade(dp_pct) in ("A", "B") else
                f"{t_dp} tracked points — engine produced fewer provenance-tracked values",
        ))

        avg = sum(d.score_pct for d in dims) / len(dims) if dims else 0.0
        return dims, avg

    # ------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------

    @staticmethod
    def _grade(score: float) -> str:
        """A>=85, B>=70, C>=55, D>=40, F<40"""
        if score >= 85:
            return "A"
        if score >= 70:
            return "B"
        if score >= 55:
            return "C"
        if score >= 40:
            return "D"
        return "F"

    def _generate_recommendations(self, report: AuditReport) -> list:
        """Scan D/F grades across all dimensions, sort by severity."""
        recs = []

        # Analysis dimensions
        for dim in report.analysis_dimensions:
            if dim.grade in ("D", "F") and dim.recommendation:
                recs.append((dim.grade, "Analysis", dim.dimension, dim.recommendation))

        # Provenance dimensions
        for dim in report.provenance_dimensions:
            if dim.grade in ("D", "F") and dim.recommendation:
                recs.append((dim.grade, "Provenance", dim.dimension, dim.recommendation))

        # Data layer — flag tables with score < 55
        for ta in report.data_audit:
            if ta.score < 55:
                recs.append((
                    self._grade(ta.score), "Data",
                    ta.table_name,
                    f"{ta.row_count} rows vs {ta.reference_row_count} — "
                    f"completeness {ta.field_completeness:.0%}",
                ))

        # Sort: F before D, then alphabetically
        grade_order = {"F": 0, "D": 1}
        recs.sort(key=lambda r: (grade_order.get(r[0], 2), r[2]))

        return [f"[{g}] {layer}: {dim} — {msg}" for g, layer, dim, msg in recs]

    # ------------------------------------------------------------------
    # Console report
    # ------------------------------------------------------------------

    def format_console_report(self, report: AuditReport) -> str:
        """Format a full audit report for terminal display."""
        w = 80
        lines = []

        # Header
        lines.append("=" * w)
        lines.append("  BLM MARKET READINESS AUDIT")
        lines.append(f"  Target:    {report.target_market} ({report.target_operator})")
        if report.reference_market:
            lines.append(f"  Reference: {report.reference_market} ({report.reference_operator})")
        else:
            lines.append(f"  Reference: absolute thresholds")
        lines.append(f"  Period:    {report.period}")
        lines.append("=" * w)

        # Overall
        grade_desc = {
            "A": "Market ready — minor polishing needed",
            "B": "Good foundation — targeted improvements needed",
            "C": "Significant gaps remain",
            "D": "Major gaps — substantial work required",
            "F": "Not ready — foundational data missing",
        }
        desc = grade_desc.get(report.overall_grade, "")
        lines.append(f"\n  OVERALL SCORE: {report.overall_score:.0f}/100 [{report.overall_grade}] — {desc}")

        # [1] Data layer
        lines.append("\n" + "=" * w)
        lines.append(f"[1] DATA LAYER{' ' * 40}Score: {report.data_score:.0f}/100 [{self._grade(report.data_score)}]")
        lines.append("=" * w)
        lines.append("")
        lines.append(f"  {'Table':<25} | {'Target':>6} | {'Ref':>5} | {'Ratio':>5} | {'Completeness':>12}")
        lines.append(f"  {'-' * 25}-+{'-' * 8}-+{'-' * 7}-+{'-' * 7}-+{'-' * 14}")
        for ta in report.data_audit:
            ratio_str = f"{ta.row_ratio:.0%}"
            comp_str = f"{ta.field_completeness:.0%}"
            lines.append(
                f"  {ta.table_name:<25} | {ta.row_count:>6} | {ta.reference_row_count:>5} "
                f"| {ratio_str:>5} | {comp_str:>12}"
            )

        # [2] Analysis layer
        lines.append("\n" + "=" * w)
        lines.append(f"[2] ANALYSIS LAYER{' ' * 36}Score: {report.analysis_score:.0f}/100 [{self._grade(report.analysis_score)}]")
        lines.append("=" * w)
        lines.append("")
        lines.append(f"  {'Dimension':<28} | {'Target':>6} | {'Ref':>5} | {'Score':>5} | {'Grade':>5}")
        lines.append(f"  {'-' * 28}-+{'-' * 8}-+{'-' * 7}-+{'-' * 7}-+{'-' * 7}")
        for dim in report.analysis_dimensions:
            score_str = f"{dim.score_pct:.0f}%"
            lines.append(
                f"  {dim.dimension:<28} | {int(dim.target_value):>6} | {int(dim.reference_value):>5} "
                f"| {score_str:>5} | {dim.grade:>5}"
            )

        # [3] Provenance layer
        lines.append("\n" + "=" * w)
        lines.append(f"[3] PROVENANCE LAYER{' ' * 34}Score: {report.provenance_score:.0f}/100 [{self._grade(report.provenance_score)}]")
        lines.append("=" * w)
        lines.append("")
        for dim in report.provenance_dimensions:
            t_str = str(int(dim.target_value)) if dim.dimension != "Non-Estimated Data %" else f"{dim.target_value:.0f}%"
            r_str = str(int(dim.reference_value)) if dim.dimension != "Non-Estimated Data %" else f"{dim.reference_value:.0f}%"
            lines.append(f"  {dim.dimension:<28} | {t_str:>6} | {r_str:>5} | {dim.score_pct:.0f}% | {dim.grade}")

        # [4] Recommendations
        lines.append("\n" + "=" * w)
        lines.append("[4] TOP RECOMMENDATIONS (by impact)")
        lines.append("=" * w)
        lines.append("")
        if report.top_recommendations:
            for i, rec in enumerate(report.top_recommendations, 1):
                lines.append(f"  {i}. {rec}")
        else:
            lines.append("  No critical gaps found — market is well-populated!")
        lines.append("\n" + "=" * w)

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _cleanup_temp(tmp_dir: str | None) -> None:
        if tmp_dir:
            import shutil
            try:
                shutil.rmtree(tmp_dir, ignore_errors=True)
            except Exception:
                pass
