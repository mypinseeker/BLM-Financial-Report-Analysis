"""Comprehensive tests for BLM Five Looks data models."""
import sys
import os
import pytest
from datetime import datetime, timedelta

# Ensure project root is on sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.models.provenance import (
    SourceType, Confidence, FreshnessStatus,
    SourceReference, TrackedValue, ProvenanceStore,
)
from src.models.trend import PESTFactor, PESTAnalysis, TrendAnalysis
from src.models.market import (
    MarketChange, CustomerSegment, APPEALSAssessment, MarketCustomerInsight,
)
from src.models.competition import (
    CompetitorImplication, PorterForce, CompetitorDeepDive, CompetitionInsight,
)
from src.models.self_analysis import (
    SegmentChange, ChangeAttribution, SegmentAnalysis, NetworkAnalysis,
    ExposurePoint, BMCCanvas, SelfInsight,
)
from src.models.swot import SWOTAnalysis
from src.models.opportunity import SPANPosition, OpportunityItem, OpportunityInsight
from src.models.feedback import UserFeedback, FEEDBACK_TYPES


# =====================================================================
# Enum Tests
# =====================================================================

class TestSourceTypeEnum:
    def test_all_expected_members(self):
        expected = [
            "FINANCIAL_REPORT_PDF", "EARNINGS_CALL_TRANSCRIPT",
            "INVESTOR_PRESENTATION", "REGULATORY_REPORT",
            "GOVERNMENT_STATISTICS", "ANALYST_REPORT",
            "NEWS_ARTICLE", "NETWORK_TEST",
            "COMPANY_PRESS_RELEASE", "WEBSITE_SCRAPE",
            "AI_EXTRACTED", "CALCULATED", "MANUAL", "DATABASE_SEED",
        ]
        for name in expected:
            assert hasattr(SourceType, name), f"SourceType missing member: {name}"

    def test_values_are_strings(self):
        for member in SourceType:
            assert isinstance(member.value, str)


class TestConfidenceEnum:
    def test_all_expected_members(self):
        expected = ["HIGH", "MEDIUM", "LOW", "ESTIMATED"]
        for name in expected:
            assert hasattr(Confidence, name), f"Confidence missing member: {name}"

    def test_values(self):
        assert Confidence.HIGH.value == "high"
        assert Confidence.MEDIUM.value == "medium"
        assert Confidence.LOW.value == "low"
        assert Confidence.ESTIMATED.value == "estimated"


class TestFreshnessStatusEnum:
    def test_all_expected_members(self):
        expected = ["CURRENT", "STALE", "EXPIRED", "UNKNOWN"]
        for name in expected:
            assert hasattr(FreshnessStatus, name), f"FreshnessStatus missing member: {name}"


# =====================================================================
# SourceReference Tests
# =====================================================================

class TestSourceReference:
    def test_minimal_instantiation(self):
        ref = SourceReference(source_type=SourceType.FINANCIAL_REPORT_PDF)
        assert ref.source_type == SourceType.FINANCIAL_REPORT_PDF
        assert ref.source_id is not None
        assert len(ref.source_id) == 8
        assert ref.url is None
        assert ref.document_name is None
        assert ref.confidence == Confidence.HIGH

    def test_full_instantiation(self):
        ref = SourceReference(
            source_type=SourceType.ANALYST_REPORT,
            url="https://example.com/report.pdf",
            document_name="Q3 2025 Analysis",
            page_number=42,
            table_index=3,
            section="Revenue Breakdown",
            publisher="Goldman Sachs",
            author="John Doe",
            publication_date=datetime(2025, 10, 15),
            data_period="Q3_2025",
            confidence=Confidence.MEDIUM,
        )
        assert ref.url == "https://example.com/report.pdf"
        assert ref.page_number == 42
        assert ref.publisher == "Goldman Sachs"

    def test_to_citation_with_all_fields(self):
        ref = SourceReference(
            source_type=SourceType.FINANCIAL_REPORT_PDF,
            document_name="Annual Report 2024",
            publisher="Vodafone",
            publication_date=datetime(2024, 5, 15),
            page_number=10,
            section="Revenue",
        )
        citation = ref.to_citation()
        assert "Annual Report 2024" in citation
        assert "by Vodafone" in citation
        assert "(2024-05-15)" in citation
        assert "p.10" in citation
        assert "\u00a7Revenue" in citation

    def test_to_citation_minimal(self):
        ref = SourceReference(source_type=SourceType.MANUAL)
        citation = ref.to_citation()
        assert citation == "[manual]"

    def test_to_citation_partial_fields(self):
        ref = SourceReference(
            source_type=SourceType.NEWS_ARTICLE,
            document_name="5G Rollout Update",
        )
        citation = ref.to_citation()
        assert citation == "5G Rollout Update"

    def test_freshness_unknown_when_no_expiry(self):
        ref = SourceReference(source_type=SourceType.MANUAL)
        assert ref.freshness == FreshnessStatus.UNKNOWN

    def test_freshness_current(self):
        ref = SourceReference(
            source_type=SourceType.MANUAL,
            expires_at=datetime.now() + timedelta(days=30),
        )
        assert ref.freshness == FreshnessStatus.CURRENT

    def test_freshness_stale(self):
        ref = SourceReference(
            source_type=SourceType.MANUAL,
            expires_at=datetime.now() - timedelta(days=15),
        )
        assert ref.freshness == FreshnessStatus.STALE

    def test_freshness_expired(self):
        ref = SourceReference(
            source_type=SourceType.MANUAL,
            expires_at=datetime.now() - timedelta(days=60),
        )
        assert ref.freshness == FreshnessStatus.EXPIRED

    def test_default_collected_at(self):
        before = datetime.now()
        ref = SourceReference(source_type=SourceType.MANUAL)
        after = datetime.now()
        assert before <= ref.collected_at <= after


# =====================================================================
# TrackedValue Tests
# =====================================================================

class TestTrackedValue:
    def test_minimal_instantiation(self):
        tv = TrackedValue(value=42.5, field_name="revenue")
        assert tv.value == 42.5
        assert tv.field_name == "revenue"
        assert tv.operator is None
        assert tv.period is None
        assert tv.primary_source is None
        assert tv.alternative_sources == []
        assert tv.derived_from == []
        assert tv.unit is None

    def test_confidence_with_source(self):
        source = SourceReference(
            source_type=SourceType.FINANCIAL_REPORT_PDF,
            confidence=Confidence.MEDIUM,
        )
        tv = TrackedValue(value=100, field_name="subscribers", primary_source=source)
        assert tv.confidence == Confidence.MEDIUM

    def test_confidence_without_source(self):
        tv = TrackedValue(value=100, field_name="subscribers")
        assert tv.confidence == Confidence.ESTIMATED

    def test_has_conflict_false(self):
        tv = TrackedValue(value=100, field_name="test")
        assert tv.has_conflict is False

    def test_has_conflict_true(self):
        alt = SourceReference(source_type=SourceType.ANALYST_REPORT)
        tv = TrackedValue(value=100, field_name="test", alternative_sources=[alt])
        assert tv.has_conflict is True

    def test_explain_minimal(self):
        tv = TrackedValue(value=42, field_name="revenue")
        explanation = tv.explain()
        assert "revenue = 42" in explanation
        assert "Confidence: estimated" in explanation

    def test_explain_full(self):
        source = SourceReference(
            source_type=SourceType.FINANCIAL_REPORT_PDF,
            document_name="Q3 Report",
            confidence=Confidence.HIGH,
        )
        tv = TrackedValue(
            value=11200,
            field_name="total_revenue",
            operator="Vodafone DE",
            period="Q3_2025",
            primary_source=source,
            unit="EUR million",
            derivation_formula="mobile + fixed + b2b",
        )
        explanation = tv.explain()
        assert "total_revenue = 11200 EUR million" in explanation
        assert "Operator: Vodafone DE" in explanation
        assert "Period: Q3_2025" in explanation
        assert "Confidence: high" in explanation
        assert "Source: Q3 Report" in explanation
        assert "Formula: mobile + fixed + b2b" in explanation

    def test_explain_returns_string(self):
        tv = TrackedValue(value="test", field_name="test_field")
        result = tv.explain()
        assert isinstance(result, str)
        assert len(result) > 0


# =====================================================================
# ProvenanceStore Tests
# =====================================================================

class TestProvenanceStore:
    def test_init_empty(self):
        store = ProvenanceStore()
        assert store.quality_report()["total_data_points"] == 0
        assert store.quality_report()["unique_sources"] == 0

    def test_register_source(self):
        store = ProvenanceStore()
        source = SourceReference(source_type=SourceType.FINANCIAL_REPORT_PDF)
        sid = store.register_source(source)
        assert sid == source.source_id
        assert store.quality_report()["unique_sources"] == 1

    def test_register_value(self):
        store = ProvenanceStore()
        tv = TrackedValue(value=100, field_name="revenue")
        store.register_value(tv)
        assert store.quality_report()["total_data_points"] == 1

    def test_track(self):
        store = ProvenanceStore()
        source = SourceReference(
            source_type=SourceType.FINANCIAL_REPORT_PDF,
            confidence=Confidence.HIGH,
        )
        tv = store.track(
            value=11200,
            field_name="total_revenue",
            operator="Vodafone DE",
            period="Q3_2025",
            source=source,
            unit="EUR million",
        )
        assert isinstance(tv, TrackedValue)
        assert tv.value == 11200
        assert tv.field_name == "total_revenue"
        assert tv.operator == "Vodafone DE"
        assert tv.period == "Q3_2025"
        assert tv.primary_source == source
        assert tv.unit == "EUR million"
        assert store.quality_report()["total_data_points"] == 1

    def test_get_values_no_filter(self):
        store = ProvenanceStore()
        store.track(value=100, field_name="revenue", operator="VF")
        store.track(value=200, field_name="revenue", operator="DT")
        assert len(store.get_values()) == 2

    def test_get_values_by_operator(self):
        store = ProvenanceStore()
        store.track(value=100, field_name="revenue", operator="VF")
        store.track(value=200, field_name="revenue", operator="DT")
        results = store.get_values(operator="VF")
        assert len(results) == 1
        assert results[0].value == 100

    def test_get_values_by_field_name(self):
        store = ProvenanceStore()
        store.track(value=100, field_name="revenue", operator="VF")
        store.track(value=50, field_name="subscribers", operator="VF")
        results = store.get_values(field_name="subscribers")
        assert len(results) == 1
        assert results[0].value == 50

    def test_get_values_by_period(self):
        store = ProvenanceStore()
        store.track(value=100, field_name="revenue", period="Q1_2025")
        store.track(value=110, field_name="revenue", period="Q2_2025")
        results = store.get_values(period="Q2_2025")
        assert len(results) == 1
        assert results[0].value == 110

    def test_get_values_combined_filters(self):
        store = ProvenanceStore()
        store.track(value=100, field_name="revenue", operator="VF", period="Q1")
        store.track(value=200, field_name="revenue", operator="DT", period="Q1")
        store.track(value=110, field_name="revenue", operator="VF", period="Q2")
        results = store.get_values(operator="VF", period="Q1")
        assert len(results) == 1
        assert results[0].value == 100

    def test_quality_report(self):
        store = ProvenanceStore()
        src_high = SourceReference(
            source_type=SourceType.FINANCIAL_REPORT_PDF,
            confidence=Confidence.HIGH,
        )
        src_med = SourceReference(
            source_type=SourceType.ANALYST_REPORT,
            confidence=Confidence.MEDIUM,
        )
        store.register_source(src_high)
        store.register_source(src_med)
        store.track(value=100, field_name="rev", source=src_high)
        store.track(value=200, field_name="rev2", source=src_med)
        store.track(value=300, field_name="rev3")  # no source -> estimated

        report = store.quality_report()
        assert report["total_data_points"] == 3
        assert report["high_confidence"] == 1
        assert report["medium_confidence"] == 1
        assert report["estimated"] == 1
        assert report["unique_sources"] == 2

    def test_quality_report_with_conflicts(self):
        store = ProvenanceStore()
        alt = SourceReference(source_type=SourceType.ANALYST_REPORT)
        tv = TrackedValue(value=100, field_name="rev", alternative_sources=[alt])
        store.register_value(tv)
        report = store.quality_report()
        assert report["with_conflicts"] == 1

    def test_to_footnotes(self):
        store = ProvenanceStore()
        src1 = SourceReference(
            source_type=SourceType.FINANCIAL_REPORT_PDF,
            document_name="Annual Report 2024",
        )
        src2 = SourceReference(
            source_type=SourceType.NEWS_ARTICLE,
            document_name="Reuters Article",
        )
        store.track(value=100, field_name="rev", source=src1)
        store.track(value=200, field_name="rev2", source=src2)
        store.track(value=300, field_name="rev3", source=src1)  # same source

        footnotes = store.to_footnotes()
        assert len(footnotes) == 2
        assert "Annual Report 2024" in footnotes[0]
        assert "Reuters Article" in footnotes[1]

    def test_to_footnotes_empty(self):
        store = ProvenanceStore()
        store.track(value=100, field_name="rev")  # no source
        assert store.to_footnotes() == []


# =====================================================================
# Trend Model Tests
# =====================================================================

class TestPESTFactor:
    def test_minimal_instantiation(self):
        f = PESTFactor(dimension="P", dimension_name="Political", factor_name="EU Regulation")
        assert f.dimension == "P"
        assert f.dimension_name == "Political"
        assert f.factor_name == "EU Regulation"

    def test_defaults(self):
        f = PESTFactor(dimension="E", dimension_name="Economic", factor_name="GDP")
        assert f.current_status == ""
        assert f.trend == ""
        assert f.trend_direction == "stable"
        assert f.industry_impact == ""
        assert f.company_impact == ""
        assert f.impact_type == "neutral"
        assert f.severity == "medium"
        assert f.time_horizon == "medium_term"
        assert f.predictability == "uncertain"
        assert f.evidence == []
        assert f.data_source == ""

    def test_fields_are_correct_types(self):
        f = PESTFactor(
            dimension="T",
            dimension_name="Technology",
            factor_name="5G Rollout",
            evidence=["Study A", "Report B"],
        )
        assert isinstance(f.dimension, str)
        assert isinstance(f.dimension_name, str)
        assert isinstance(f.factor_name, str)
        assert isinstance(f.evidence, list)
        assert isinstance(f.severity, str)
        assert isinstance(f.time_horizon, str)

    def test_evidence_list_independence(self):
        """Each PESTFactor should have its own evidence list."""
        f1 = PESTFactor(dimension="P", dimension_name="Political", factor_name="A")
        f2 = PESTFactor(dimension="P", dimension_name="Political", factor_name="B")
        f1.evidence.append("test")
        assert f2.evidence == []


class TestPESTAnalysis:
    def test_defaults(self):
        pa = PESTAnalysis()
        assert pa.political_factors == []
        assert pa.economic_factors == []
        assert pa.society_factors == []
        assert pa.technology_factors == []
        assert pa.overall_weather == "mixed"
        assert pa.weather_explanation == ""
        assert pa.policy_opportunities == []
        assert pa.policy_threats == []
        assert pa.tech_addressable_market == ""
        assert pa.key_message == ""

    def test_with_factors(self):
        factor = PESTFactor(dimension="P", dimension_name="Political", factor_name="Regulation")
        pa = PESTAnalysis(political_factors=[factor])
        assert len(pa.political_factors) == 1
        assert pa.political_factors[0].factor_name == "Regulation"


class TestTrendAnalysis:
    def test_defaults(self):
        ta = TrendAnalysis()
        assert isinstance(ta.pest, PESTAnalysis)
        assert ta.industry_market_size == ""
        assert ta.industry_growth_rate == ""
        assert ta.industry_profit_trend == ""
        assert ta.industry_concentration == ""
        assert ta.industry_lifecycle_stage == ""
        assert ta.new_business_models == []
        assert ta.technology_revolution == []
        assert ta.key_success_factors == []
        assert ta.value_transfer_trends == []

    def test_has_key_message(self):
        ta = TrendAnalysis()
        assert hasattr(ta, "key_message")
        assert ta.key_message == ""

    def test_with_data(self):
        ta = TrendAnalysis(
            industry_market_size="EUR 60B",
            industry_lifecycle_stage="mature",
            key_message="German telecom market is mature with limited growth",
        )
        assert ta.industry_market_size == "EUR 60B"
        assert ta.key_message == "German telecom market is mature with limited growth"


# =====================================================================
# Market Model Tests
# =====================================================================

class TestMarketChange:
    def test_minimal_instantiation(self):
        mc = MarketChange(change_type="pricing")
        assert mc.change_type == "pricing"
        assert mc.description == ""
        assert mc.evidence == []

    def test_defaults(self):
        mc = MarketChange(change_type="merger")
        assert mc.source == ""
        assert mc.time_horizon == "medium_term"
        assert mc.impact_type == "neutral"
        assert mc.severity == "medium"


class TestCustomerSegment:
    def test_minimal_instantiation(self):
        cs = CustomerSegment(segment_name="Young Adults")
        assert cs.segment_name == "Young Adults"
        assert cs.segment_type == "consumer"

    def test_defaults(self):
        cs = CustomerSegment(segment_name="SME")
        assert cs.size_estimate == ""
        assert cs.growth_trend == "stable"
        assert cs.our_share == ""
        assert cs.unmet_needs == []
        assert cs.pain_points == []
        assert cs.purchase_decision_factors == []
        assert cs.competitor_gaps == []
        assert cs.opportunity == ""


class TestAPPEALSAssessment:
    def test_minimal_instantiation(self):
        a = APPEALSAssessment(dimension="$", dimension_name="Price")
        assert a.dimension == "$"
        assert a.dimension_name == "Price"

    def test_defaults(self):
        a = APPEALSAssessment(dimension="P1", dimension_name="Packaging")
        assert a.our_score == 0.0
        assert a.competitor_scores == {}
        assert a.customer_priority == "important"
        assert a.gap_analysis == ""


class TestMarketCustomerInsight:
    def test_defaults(self):
        mci = MarketCustomerInsight()
        assert mci.market_snapshot == {}
        assert mci.changes == []
        assert mci.opportunities == []
        assert mci.threats == []
        assert mci.customer_segments == []
        assert mci.appeals_assessment == []
        assert mci.customer_value_migration == ""
        assert mci.market_outlook == "mixed"

    def test_has_key_message(self):
        mci = MarketCustomerInsight()
        assert hasattr(mci, "key_message")
        assert mci.key_message == ""


# =====================================================================
# Competition Model Tests
# =====================================================================

class TestCompetitorImplication:
    def test_minimal_instantiation(self):
        ci = CompetitorImplication(implication_type="opportunity")
        assert ci.implication_type == "opportunity"
        assert ci.description == ""
        assert ci.evidence == []
        assert ci.suggested_action == ""


class TestPorterForce:
    def test_minimal_instantiation(self):
        pf = PorterForce(force_name="new_entrants")
        assert pf.force_name == "new_entrants"
        assert pf.force_level == "medium"

    def test_defaults(self):
        pf = PorterForce(force_name="substitutes")
        assert pf.key_factors == []
        assert pf.implications == []


class TestCompetitorDeepDive:
    def test_minimal_instantiation(self):
        cd = CompetitorDeepDive(operator="Deutsche Telekom")
        assert cd.operator == "Deutsche Telekom"

    def test_defaults(self):
        cd = CompetitorDeepDive(operator="Telefonica")
        assert cd.financial_health == {}
        assert cd.subscriber_health == {}
        assert cd.network_status == {}
        assert cd.product_portfolio == []
        assert cd.new_product_pipeline == []
        assert cd.growth_strategy == ""
        assert cd.supply_chain_status == ""
        assert cd.ecosystem_partners == []
        assert cd.core_control_points == []
        assert cd.business_model == ""
        assert cd.org_structure == ""
        assert cd.incentive_system == ""
        assert cd.talent_culture == ""
        assert cd.ma_activity == []
        assert cd.strengths == []
        assert cd.weaknesses == []
        assert cd.problems == []
        assert cd.likely_future_actions == []
        assert cd.implications == []


class TestCompetitionInsight:
    def test_defaults(self):
        ci = CompetitionInsight()
        assert ci.five_forces == {}
        assert ci.overall_competition_intensity == "medium"
        assert ci.competitor_analyses == {}
        assert ci.comparison_table == {}
        assert ci.competitive_landscape == ""

    def test_has_key_message(self):
        ci = CompetitionInsight()
        assert hasattr(ci, "key_message")
        assert ci.key_message == ""


# =====================================================================
# Self Analysis Model Tests
# =====================================================================

class TestSegmentChange:
    def test_minimal_instantiation(self):
        sc = SegmentChange(metric="revenue")
        assert sc.metric == "revenue"
        assert sc.current_value is None
        assert sc.previous_value is None

    def test_defaults(self):
        sc = SegmentChange(metric="arpu")
        assert sc.yoy_value is None
        assert sc.change_qoq == 0.0
        assert sc.change_yoy == 0.0
        assert sc.direction == "stable"
        assert sc.significance == "minor"


class TestChangeAttribution:
    def test_minimal_instantiation(self):
        ca = ChangeAttribution(attribution_type="management_explanation")
        assert ca.attribution_type == "management_explanation"

    def test_defaults(self):
        ca = ChangeAttribution(attribution_type="tariff_competition")
        assert ca.description == ""
        assert ca.confidence == "medium"
        assert ca.evidence == []
        assert ca.source == ""


class TestSegmentAnalysis:
    def test_minimal_instantiation(self):
        sa = SegmentAnalysis(segment_name="Mobile")
        assert sa.segment_name == "Mobile"

    def test_defaults(self):
        sa = SegmentAnalysis(segment_name="Fixed Broadband")
        assert sa.segment_id == ""
        assert sa.key_metrics == {}
        assert sa.changes == []
        assert sa.trend_data == {}
        assert sa.competitor_comparison == {}
        assert sa.attributions == []
        assert sa.health_status == "stable"
        assert sa.key_message == ""
        assert sa.action_required == ""


class TestNetworkAnalysis:
    def test_defaults(self):
        na = NetworkAnalysis()
        assert na.technology_mix == {}
        assert na.controlled_vs_resale == {}
        assert na.coverage == {}
        assert na.quality_scores == {}
        assert na.homepass_vs_connect == {}
        assert na.evolution_strategy == {}
        assert na.investment_direction == ""
        assert na.vs_competitors == ""
        assert na.consumer_impact == ""
        assert na.b2b_impact == ""
        assert na.cost_impact == ""


class TestExposurePoint:
    def test_minimal_instantiation(self):
        ep = ExposurePoint(trigger_action="1&1 network migration")
        assert ep.trigger_action == "1&1 network migration"

    def test_defaults(self):
        ep = ExposurePoint(trigger_action="test")
        assert ep.side_effect == ""
        assert ep.attack_vector == ""
        assert ep.severity == "medium"
        assert ep.evidence == []


class TestBMCCanvas:
    def test_defaults(self):
        bmc = BMCCanvas()
        assert bmc.key_partners == []
        assert bmc.key_activities == []
        assert bmc.key_resources == []
        assert bmc.value_propositions == []
        assert bmc.customer_relationships == []
        assert bmc.channels == []
        assert bmc.customer_segments == []
        assert bmc.cost_structure == []
        assert bmc.revenue_streams == []

    def test_nine_building_blocks(self):
        """BMC Canvas should have exactly 9 building blocks."""
        bmc = BMCCanvas()
        block_fields = [
            "key_partners", "key_activities", "key_resources",
            "value_propositions", "customer_relationships", "channels",
            "customer_segments", "cost_structure", "revenue_streams",
        ]
        for f in block_fields:
            assert hasattr(bmc, f), f"BMCCanvas missing field: {f}"
        assert len(block_fields) == 9


class TestSelfInsight:
    def test_defaults(self):
        si = SelfInsight()
        assert si.financial_health == {}
        assert si.revenue_breakdown == {}
        assert si.market_positions == {}
        assert si.share_trends == {}
        assert si.segment_analyses == []
        assert isinstance(si.network, NetworkAnalysis)
        assert si.customer_perception == {}
        assert si.leadership_changes == []
        assert isinstance(si.bmc, BMCCanvas)
        assert si.org_culture == ""
        assert si.talent_assessment == {}
        assert si.performance_gap == ""
        assert si.opportunity_gap == ""
        assert si.strategic_review == ""
        assert si.strengths == []
        assert si.weaknesses == []
        assert si.exposure_points == []
        assert si.health_rating == "stable"

    def test_has_key_message(self):
        si = SelfInsight()
        assert hasattr(si, "key_message")
        assert si.key_message == ""


# =====================================================================
# SWOT Model Tests
# =====================================================================

class TestSWOTAnalysis:
    def test_defaults(self):
        swot = SWOTAnalysis()
        assert swot.strengths == []
        assert swot.weaknesses == []
        assert swot.opportunities == []
        assert swot.threats == []
        assert swot.so_strategies == []
        assert swot.wo_strategies == []
        assert swot.st_strategies == []
        assert swot.wt_strategies == []

    def test_has_key_message(self):
        swot = SWOTAnalysis()
        assert hasattr(swot, "key_message")
        assert swot.key_message == ""

    def test_four_quadrants(self):
        swot = SWOTAnalysis(
            so_strategies=["Invest in 5G"],
            wo_strategies=["Partner for fiber"],
            st_strategies=["Lock-in enterprise contracts"],
            wt_strategies=["Exit unprofitable segments"],
        )
        assert len(swot.so_strategies) == 1
        assert len(swot.wo_strategies) == 1
        assert len(swot.st_strategies) == 1
        assert len(swot.wt_strategies) == 1

    def test_list_independence(self):
        s1 = SWOTAnalysis()
        s2 = SWOTAnalysis()
        s1.strengths.append("strong brand")
        assert s2.strengths == []


# =====================================================================
# Opportunity Model Tests
# =====================================================================

class TestSPANPosition:
    def test_minimal_instantiation(self):
        sp = SPANPosition(opportunity_name="5G Enterprise")
        assert sp.opportunity_name == "5G Enterprise"

    def test_defaults(self):
        sp = SPANPosition(opportunity_name="FWA")
        assert sp.market_size_score == 0.0
        assert sp.market_growth_score == 0.0
        assert sp.profit_potential_score == 0.0
        assert sp.strategic_value_score == 0.0
        assert sp.market_attractiveness == 0.0
        assert sp.market_share_score == 0.0
        assert sp.product_fit_score == 0.0
        assert sp.brand_channel_score == 0.0
        assert sp.tech_capability_score == 0.0
        assert sp.competitive_position == 0.0
        assert sp.quadrant == ""
        assert sp.recommended_strategy == ""
        assert sp.bubble_size == 1.0


class TestOpportunityItem:
    def test_minimal_instantiation(self):
        oi = OpportunityItem(name="5G Private Networks")
        assert oi.name == "5G Private Networks"

    def test_defaults(self):
        oi = OpportunityItem(name="IoT")
        assert oi.description == ""
        assert oi.derived_from == []
        assert oi.addressable_market == "N/A"
        assert oi.addressable_market_source == ""
        assert oi.our_capability == ""
        assert oi.competition_intensity == ""
        assert oi.time_window == ""
        assert oi.priority == "P1"
        assert oi.priority_rationale == ""

    def test_addressable_market_default_is_na(self):
        """Addressable market should default to N/A, never fabricate."""
        oi = OpportunityItem(name="Test")
        assert oi.addressable_market == "N/A"


class TestOpportunityInsight:
    def test_defaults(self):
        oi = OpportunityInsight()
        assert oi.span_positions == []
        assert oi.grow_invest == []
        assert oi.acquire_skills == []
        assert oi.harvest == []
        assert oi.avoid_exit == []
        assert oi.window_opportunities == []
        assert oi.opportunities == []

    def test_has_key_message(self):
        oi = OpportunityInsight()
        assert hasattr(oi, "key_message")
        assert oi.key_message == ""


# =====================================================================
# Feedback Model Tests
# =====================================================================

class TestUserFeedback:
    def test_minimal_instantiation(self):
        fb = UserFeedback(look_category="trends")
        assert fb.look_category == "trends"

    def test_defaults(self):
        fb = UserFeedback(look_category="competition")
        assert fb.finding_ref == ""
        assert fb.feedback_type == "confirmed"
        assert fb.original_value is None
        assert fb.user_comment == ""
        assert fb.user_value is None
        assert fb.analysis_job_id == 0
        assert fb.operator_id == ""
        assert fb.period == ""
        assert isinstance(fb.created_at, datetime)

    def test_to_dict(self):
        fb = UserFeedback(
            look_category="trends",
            finding_ref="pest_eco",
            analysis_job_id=5,
            operator_id="vf_de",
            period="CQ4_2025",
        )
        d = fb.to_dict()
        assert d["look_category"] == "trends"
        assert d["analysis_job_id"] == 5
        assert isinstance(d["created_at"], str)

    def test_feedback_types(self):
        assert "confirmed" in FEEDBACK_TYPES
        assert "disputed" in FEEDBACK_TYPES
        assert "modified" in FEEDBACK_TYPES
        assert "supplemented" in FEEDBACK_TYPES
        assert len(FEEDBACK_TYPES) == 4

    def test_all_categories(self):
        categories = ["trends", "market", "competition", "self", "swot", "opportunity"]
        for cat in categories:
            fb = UserFeedback(look_category=cat)
            assert fb.look_category == cat

    def test_created_at_auto_set(self):
        before = datetime.now()
        fb = UserFeedback(look_category="trends")
        after = datetime.now()
        assert before <= fb.created_at <= after


# =====================================================================
# key_message Field Tests (Cross-cutting)
# =====================================================================

class TestKeyMessageField:
    """Every major insight model must have a key_message field."""

    def test_trend_analysis_has_key_message(self):
        assert hasattr(TrendAnalysis(), "key_message")

    def test_market_customer_insight_has_key_message(self):
        assert hasattr(MarketCustomerInsight(), "key_message")

    def test_competition_insight_has_key_message(self):
        assert hasattr(CompetitionInsight(), "key_message")

    def test_self_insight_has_key_message(self):
        assert hasattr(SelfInsight(), "key_message")

    def test_swot_analysis_has_key_message(self):
        assert hasattr(SWOTAnalysis(), "key_message")

    def test_opportunity_insight_has_key_message(self):
        assert hasattr(OpportunityInsight(), "key_message")

    def test_all_default_to_empty_string(self):
        models = [
            TrendAnalysis(),
            MarketCustomerInsight(),
            CompetitionInsight(),
            SelfInsight(),
            SWOTAnalysis(),
            OpportunityInsight(),
        ]
        for m in models:
            assert m.key_message == "", f"{type(m).__name__}.key_message should default to empty string"


# =====================================================================
# Import Tests (via __init__.py)
# =====================================================================

class TestModuleImports:
    """Test that all models are importable from src.models."""

    def test_import_provenance(self):
        from src.models import SourceType, Confidence, FreshnessStatus
        from src.models import SourceReference, TrackedValue, ProvenanceStore

    def test_import_trend(self):
        from src.models import PESTFactor, PESTAnalysis, TrendAnalysis

    def test_import_market(self):
        from src.models import MarketChange, CustomerSegment, APPEALSAssessment, MarketCustomerInsight

    def test_import_competition(self):
        from src.models import CompetitorImplication, PorterForce, CompetitorDeepDive, CompetitionInsight

    def test_import_self(self):
        from src.models import (
            SegmentChange, ChangeAttribution, SegmentAnalysis,
            NetworkAnalysis, ExposurePoint, BMCCanvas, SelfInsight,
        )

    def test_import_swot(self):
        from src.models import SWOTAnalysis

    def test_import_opportunity(self):
        from src.models import SPANPosition, OpportunityItem, OpportunityInsight

    def test_import_feedback(self):
        from src.models import UserFeedback

    def test_all_exports(self):
        import src.models
        assert len(src.models.__all__) >= 24


# =====================================================================
# Integration Tests
# =====================================================================

class TestIntegration:
    """Test that models compose together correctly."""

    def test_full_analysis_pipeline(self):
        """Simulate building a complete analysis from all models."""
        # Create provenance store
        store = ProvenanceStore()
        src = SourceReference(
            source_type=SourceType.FINANCIAL_REPORT_PDF,
            document_name="Vodafone DE Annual Report 2024",
            publisher="Vodafone Group",
            confidence=Confidence.HIGH,
        )
        store.register_source(src)

        # Track a value
        rev = store.track(
            value=11200,
            field_name="total_revenue",
            operator="Vodafone DE",
            period="FY2024",
            source=src,
            unit="EUR million",
        )
        assert rev.confidence == Confidence.HIGH

        # Build trend analysis
        trend = TrendAnalysis(
            industry_market_size="EUR 60B",
            industry_lifecycle_stage="mature",
            key_message="Mature market with 5G growth opportunity",
        )

        # Build market insight
        market = MarketCustomerInsight(
            market_snapshot={"total_revenue": 60000},
            key_message="Price competition intensifying",
        )

        # Build competition insight
        dt_dive = CompetitorDeepDive(
            operator="Deutsche Telekom",
            financial_health={"revenue": 25000, "ebitda_margin": 0.40},
            strengths=["Largest fiber footprint"],
        )
        competition = CompetitionInsight(
            competitor_analyses={"dt": dt_dive},
            key_message="DT dominates; VF needs differentiation",
        )

        # Build self insight
        mobile_seg = SegmentAnalysis(
            segment_name="Mobile",
            segment_id="mobile",
            health_status="stable",
        )
        self_insight = SelfInsight(
            segment_analyses=[mobile_seg],
            key_message="Network investment is critical",
        )

        # Build SWOT
        swot = SWOTAnalysis(
            strengths=["Strong cable network"],
            weaknesses=["Low fiber penetration"],
            opportunities=["5G FWA"],
            threats=["DT fiber rollout"],
            so_strategies=["Leverage cable for converged offers"],
            key_message="Must invest in fiber to remain competitive",
        )

        # Build opportunities
        span = SPANPosition(
            opportunity_name="5G Enterprise",
            market_attractiveness=7.5,
            competitive_position=5.0,
            quadrant="acquire_skills",
        )
        opportunities = OpportunityInsight(
            span_positions=[span],
            acquire_skills=["5G Enterprise"],
            key_message="Focus on B2B 5G private networks",
        )

        # Verify everything works together
        assert trend.key_message != ""
        assert market.key_message != ""
        assert competition.key_message != ""
        assert self_insight.key_message != ""
        assert swot.key_message != ""
        assert opportunities.key_message != ""
        assert store.quality_report()["total_data_points"] == 1

    def test_tracked_value_with_derivation(self):
        """Test that derived values can reference their inputs."""
        store = ProvenanceStore()
        mobile = store.track(value=5000, field_name="mobile_revenue", unit="EUR M")
        fixed = store.track(value=4000, field_name="fixed_revenue", unit="EUR M")
        b2b = store.track(value=2200, field_name="b2b_revenue", unit="EUR M")

        total = TrackedValue(
            value=11200,
            field_name="total_revenue",
            derived_from=[mobile, fixed, b2b],
            derivation_formula="mobile + fixed + b2b",
            unit="EUR M",
        )
        assert total.value == 11200
        assert len(total.derived_from) == 3
        assert "mobile + fixed + b2b" in total.explain()
