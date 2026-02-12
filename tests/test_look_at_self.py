"""Tests for Look 4: Self Analysis module."""

import sys
from pathlib import Path

import pytest

# Ensure project root is on path
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.database.db import TelecomDatabase
from src.database.seed_germany import seed_all
from src.blm.look_at_self import analyze_self
from src.models.self_analysis import (
    BMCCanvas,
    ExposurePoint,
    NetworkAnalysis,
    SegmentAnalysis,
    SelfInsight,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def seeded_db():
    """Create an in-memory database with Germany seed data."""
    database = seed_all(":memory:")
    yield database
    database.close()


@pytest.fixture
def empty_db():
    """Create an in-memory database with schema but no data."""
    db = TelecomDatabase(":memory:")
    db.init()
    yield db
    db.close()


@pytest.fixture
def result(seeded_db):
    """Run analyze_self on the seeded database for Vodafone Germany."""
    return analyze_self(
        db=seeded_db,
        market="germany",
        target_operator="vodafone_germany",
        target_period="CQ4_2025",
        n_quarters=8,
    )


# ============================================================================
# Financial Health
# ============================================================================

class TestFinancialHealth:

    def test_financial_health_populated(self, result):
        """Financial health dict should have revenue and ebitda fields."""
        fh = result.financial_health
        assert isinstance(fh, dict)
        assert len(fh) > 0
        assert "total_revenue" in fh
        assert "ebitda" in fh
        assert "ebitda_margin_pct" in fh
        assert fh["total_revenue"] is not None
        assert fh["ebitda"] is not None

    def test_financial_health_has_growth_metrics(self, result):
        """Financial health should include QoQ and YoY growth metrics."""
        fh = result.financial_health
        assert "revenue_qoq_pct" in fh
        assert "revenue_yoy_pct" in fh
        assert "ebitda_qoq_pct" in fh

    def test_financial_health_has_trend_arrays(self, result):
        """Financial health should include trend arrays for visualization."""
        fh = result.financial_health
        assert "revenue_trend" in fh
        assert isinstance(fh["revenue_trend"], list)
        assert len(fh["revenue_trend"]) == 8

    def test_financial_health_vodafone_values(self, result):
        """Verify known Vodafone Germany Q3 FY26 financial values."""
        fh = result.financial_health
        # Vodafone Q3 FY26 = CQ4_2025: revenue 3092, ebitda 1120
        assert fh["total_revenue"] == 3092
        assert fh["ebitda"] == 1120
        assert fh["ebitda_margin_pct"] == 36.2


# ============================================================================
# Revenue Breakdown
# ============================================================================

class TestRevenueBreakdown:

    def test_revenue_breakdown(self, result):
        """Revenue breakdown should have at least 3 segments."""
        rb = result.revenue_breakdown
        assert isinstance(rb, dict)
        # Exclude total_revenue from count
        segment_keys = [k for k in rb if k != "total_revenue"]
        assert len(segment_keys) >= 3

    def test_revenue_breakdown_has_shares(self, result):
        """Each segment in revenue breakdown should have share_pct."""
        rb = result.revenue_breakdown
        for key, value in rb.items():
            if key == "total_revenue":
                continue
            assert "share_pct" in value
            assert "value" in value

    def test_revenue_breakdown_total(self, result):
        """Revenue breakdown should include total_revenue."""
        rb = result.revenue_breakdown
        assert "total_revenue" in rb
        assert rb["total_revenue"] == 3092


# ============================================================================
# Segment Analyses
# ============================================================================

class TestSegmentAnalyses:

    def test_segment_analyses_count(self, result):
        """There should be at least 5 segment analyses."""
        assert len(result.segment_analyses) >= 5

    def test_segment_names(self, result):
        """All expected segments should be present."""
        names = {seg.segment_name for seg in result.segment_analyses}
        assert "Mobile" in names
        assert "Fixed Broadband" in names
        assert "B2B" in names
        assert "TV/Convergence" in names
        assert "Wholesale" in names

    def test_segment_key_metrics(self, result):
        """Each segment should have a key_metrics dict with content."""
        for seg in result.segment_analyses:
            assert isinstance(seg.key_metrics, dict), f"{seg.segment_name} missing key_metrics"
            assert len(seg.key_metrics) > 0, f"{seg.segment_name} key_metrics is empty"

    def test_segment_health_status(self, result):
        """Each segment should have a valid health_status."""
        valid_statuses = {"strong", "stable", "weakening", "critical"}
        for seg in result.segment_analyses:
            assert seg.health_status in valid_statuses, (
                f"{seg.segment_name} has invalid health_status: {seg.health_status}"
            )

    def test_segment_has_changes(self, result):
        """Each segment should have at least one SegmentChange."""
        for seg in result.segment_analyses:
            assert len(seg.changes) >= 1, f"{seg.segment_name} has no changes"

    def test_segment_has_trend_data(self, result):
        """Each segment should have trend_data dict."""
        for seg in result.segment_analyses:
            assert isinstance(seg.trend_data, dict), f"{seg.segment_name} missing trend_data"
            assert len(seg.trend_data) > 0, f"{seg.segment_name} trend_data empty"

    def test_segment_key_message_not_empty(self, result):
        """Each segment should have a non-empty key_message."""
        for seg in result.segment_analyses:
            assert seg.key_message, f"{seg.segment_name} has empty key_message"

    def test_mobile_segment_has_specific_metrics(self, result):
        """Mobile segment should have mobile-specific metrics."""
        mobile = [s for s in result.segment_analyses if s.segment_id == "mobile"][0]
        assert "mobile_service_revenue" in mobile.key_metrics
        assert "mobile_total_k" in mobile.key_metrics
        assert "mobile_arpu" in mobile.key_metrics

    def test_fixed_segment_has_broadband_metrics(self, result):
        """Fixed segment should have broadband-specific metrics."""
        fixed = [s for s in result.segment_analyses if s.segment_id == "fixed"][0]
        assert "broadband_total_k" in fixed.key_metrics
        assert "fixed_service_revenue" in fixed.key_metrics

    def test_b2b_segment_has_revenue(self, result):
        """B2B segment should have b2b_revenue in key_metrics."""
        b2b = [s for s in result.segment_analyses if s.segment_id == "b2b"][0]
        assert "b2b_revenue" in b2b.key_metrics


# ============================================================================
# Network Analysis
# ============================================================================

class TestNetworkAnalysis:

    def test_network_analysis_populated(self, result):
        """Network analysis should have technology_mix and coverage."""
        net = result.network
        assert isinstance(net, NetworkAnalysis)
        assert isinstance(net.technology_mix, dict)
        assert len(net.technology_mix) > 0
        assert isinstance(net.coverage, dict)
        assert len(net.coverage) > 0

    def test_network_coverage_values(self, result):
        """Network coverage should include 5G and 4G values."""
        cov = result.network.coverage
        assert "5g" in cov
        assert "4g" in cov
        # Vodafone Germany: 5G coverage 92%
        assert cov["5g"] == 92

    def test_network_investment_direction(self, result):
        """Network analysis should have an investment direction."""
        assert result.network.investment_direction in {
            "increasing", "decreasing", "stable"
        }


# ============================================================================
# BMC Canvas
# ============================================================================

class TestBMCCanvas:

    def test_bmc_canvas(self, result):
        """All 9 BMC sections should be non-empty."""
        bmc = result.bmc
        assert isinstance(bmc, BMCCanvas)
        assert len(bmc.key_partners) > 0, "key_partners empty"
        assert len(bmc.key_activities) > 0, "key_activities empty"
        assert len(bmc.key_resources) > 0, "key_resources empty"
        assert len(bmc.value_propositions) > 0, "value_propositions empty"
        assert len(bmc.customer_relationships) > 0, "customer_relationships empty"
        assert len(bmc.channels) > 0, "channels empty"
        assert len(bmc.customer_segments) > 0, "customer_segments empty"
        assert len(bmc.cost_structure) > 0, "cost_structure empty"
        assert len(bmc.revenue_streams) > 0, "revenue_streams empty"

    def test_bmc_vodafone_specific(self, result):
        """BMC should include Vodafone-specific elements."""
        bmc = result.bmc
        # Vodafone has cable network as key resource
        cable_found = any("cable" in r.lower() or "Cable" in r for r in bmc.key_resources)
        assert cable_found, "Vodafone BMC should mention cable network"


# ============================================================================
# Exposure Points
# ============================================================================

class TestExposurePoints:

    def test_exposure_points(self, result):
        """There should be at least 1 exposure point."""
        assert len(result.exposure_points) >= 1
        assert all(isinstance(ep, ExposurePoint) for ep in result.exposure_points)

    def test_exposure_points_have_content(self, result):
        """Each exposure point should have trigger_action and severity."""
        for ep in result.exposure_points:
            assert ep.trigger_action, "Exposure point missing trigger_action"
            assert ep.severity in {"high", "medium", "low"}, (
                f"Invalid severity: {ep.severity}"
            )

    def test_vodafone_has_1and1_exposure(self, result):
        """Vodafone should have an exposure point about 1&1 migration."""
        triggers = [ep.trigger_action.lower() for ep in result.exposure_points]
        assert any("1&1" in t or "1and1" in t for t in triggers), (
            "Vodafone should identify 1&1 as an exposure point"
        )


# ============================================================================
# Strengths & Weaknesses
# ============================================================================

class TestStrengthsWeaknesses:

    def test_strengths_weaknesses(self, result):
        """Both strengths and weaknesses lists should be non-empty."""
        assert len(result.strengths) > 0, "strengths list is empty"
        assert len(result.weaknesses) > 0, "weaknesses list is empty"

    def test_strengths_are_strings(self, result):
        """Each strength should be a non-empty string."""
        for s in result.strengths:
            assert isinstance(s, str)
            assert len(s) > 0

    def test_weaknesses_are_strings(self, result):
        """Each weakness should be a non-empty string."""
        for w in result.weaknesses:
            assert isinstance(w, str)
            assert len(w) > 0


# ============================================================================
# Health Rating
# ============================================================================

class TestHealthRating:

    def test_health_rating_valid(self, result):
        """Health rating should be one of the valid values."""
        valid = {"healthy", "stable", "concerning", "critical"}
        assert result.health_rating in valid, (
            f"Invalid health_rating: {result.health_rating}"
        )


# ============================================================================
# Key Message
# ============================================================================

class TestKeyMessage:

    def test_key_message_not_empty(self, result):
        """Key message should be a non-empty string."""
        assert isinstance(result.key_message, str)
        assert len(result.key_message) > 0

    def test_key_message_contains_relevant_info(self, result):
        """Key message should reference operator ranking or financials."""
        msg = result.key_message.lower()
        # Should mention at least one of: rank, revenue, margin, health
        assert any(term in msg for term in ["rank", "revenue", "margin", "healthy", "stable", "concerning"]), (
            f"Key message lacks relevant content: {result.key_message}"
        )


# ============================================================================
# Market Positions
# ============================================================================

class TestMarketPositions:

    def test_market_positions(self, result):
        """Market positions should be populated with ranking info."""
        mp = result.market_positions
        assert isinstance(mp, dict)
        assert len(mp) > 0
        assert "revenue_rank" in mp
        assert "operators_count" in mp
        assert mp["operators_count"] == 4

    def test_market_share(self, result):
        """Market positions should include revenue market share."""
        mp = result.market_positions
        assert "revenue_market_share_pct" in mp
        share = mp["revenue_market_share_pct"]
        assert 0 < share < 100

    def test_subscriber_share(self, result):
        """Market positions should include mobile subscriber share."""
        mp = result.market_positions
        assert "mobile_subscriber_share_pct" in mp
        share = mp["mobile_subscriber_share_pct"]
        assert 0 < share < 100

    def test_competitors_info(self, result):
        """Market positions should include competitor information."""
        mp = result.market_positions
        assert "competitors" in mp
        assert len(mp["competitors"]) >= 2  # DT, O2 at minimum


# ============================================================================
# Empty Database Handling
# ============================================================================

class TestEmptyDB:

    def test_empty_db_handling(self, empty_db):
        """Empty DB should return a valid SelfInsight with defaults."""
        # Register a dummy operator so the query runs
        empty_db.upsert_operator(
            "test_op",
            display_name="Test",
            country="DE",
            market="test_market",
        )

        result = analyze_self(
            db=empty_db,
            market="test_market",
            target_operator="test_op",
            target_period="CQ4_2025",
        )

        assert isinstance(result, SelfInsight)
        # Financial health should be empty dict (no data)
        assert isinstance(result.financial_health, dict)
        # Should still get BMC canvas
        assert isinstance(result.bmc, BMCCanvas)
        assert len(result.bmc.key_partners) > 0
        # Health rating should be valid
        assert result.health_rating in {"healthy", "stable", "concerning", "critical"}
        # Key message should not be empty
        assert len(result.key_message) > 0
        # Should still produce segment analyses (with empty metrics)
        assert len(result.segment_analyses) >= 5
        # Exposure points may be empty if no data-driven exposure detected
        assert isinstance(result.exposure_points, list)
        # Strengths and weaknesses should have fallback values
        assert len(result.strengths) > 0
        assert len(result.weaknesses) > 0

    def test_empty_db_no_crash_on_segments(self, empty_db):
        """Segment analyses should not crash with no data."""
        empty_db.upsert_operator(
            "test_op", display_name="Test", country="DE", market="test_market"
        )
        result = analyze_self(
            db=empty_db,
            market="test_market",
            target_operator="test_op",
        )
        for seg in result.segment_analyses:
            assert seg.health_status in {"strong", "stable", "weakening", "critical"}
            assert seg.key_message  # Should have fallback message


# ============================================================================
# Share Trends
# ============================================================================

class TestShareTrends:

    def test_share_trends_populated(self, result):
        """Share trends should include revenue and subscriber shares."""
        st = result.share_trends
        assert isinstance(st, dict)
        assert "revenue_share_latest" in st
        assert "mobile_share_latest" in st


# ============================================================================
# Integration: Deutsche Telekom as Target
# ============================================================================

class TestAlternateOperator:

    def test_dt_as_target(self, seeded_db):
        """analyze_self should work with Deutsche Telekom as target."""
        result = analyze_self(
            db=seeded_db,
            market="germany",
            target_operator="deutsche_telekom",
            target_period="CQ4_2025",
        )
        assert isinstance(result, SelfInsight)
        assert result.financial_health.get("total_revenue") == 6200
        assert result.health_rating in {"healthy", "stable", "concerning", "critical"}
        assert len(result.segment_analyses) >= 5
        assert result.key_message

    def test_o2_as_target(self, seeded_db):
        """analyze_self should work with Telefonica O2 as target."""
        result = analyze_self(
            db=seeded_db,
            market="germany",
            target_operator="telefonica_o2",
            target_period="CQ4_2025",
        )
        assert isinstance(result, SelfInsight)
        assert result.health_rating in {"healthy", "stable", "concerning", "critical"}
        assert len(result.segment_analyses) >= 5
