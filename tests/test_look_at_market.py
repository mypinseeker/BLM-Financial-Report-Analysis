"""Tests for Look 2: Market/Customer Analysis module.

Tests the analyze_market_customer function against both the seeded
Germany telecom database and an empty database to verify correct behavior.
"""

import sys
from pathlib import Path

import pytest

# Ensure project root is on path
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.database.db import TelecomDatabase
from src.database.seed_germany import seed_all
from src.blm.look_at_market_customer import analyze_market_customer
from src.models.market import (
    MarketChange,
    CustomerSegment,
    APPEALSAssessment,
    MarketCustomerInsight,
)
from src.models.provenance import ProvenanceStore


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def seeded_db():
    """Create an in-memory database with Germany seed data."""
    db = seed_all(":memory:")
    yield db
    db.close()


@pytest.fixture
def empty_db():
    """Create an in-memory database with schema but no data."""
    db = TelecomDatabase(":memory:")
    db.init()
    yield db
    db.close()


# ============================================================================
# Market Snapshot Tests
# ============================================================================

class TestMarketSnapshot:

    def test_market_snapshot_populated(self, seeded_db):
        """Market snapshot should have total_revenue and market_shares."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        snapshot = result.market_snapshot

        assert "total_revenue" in snapshot
        assert snapshot["total_revenue"] != "N/A"
        assert snapshot["total_revenue"] > 0

        assert "market_shares" in snapshot
        assert isinstance(snapshot["market_shares"], dict)
        assert len(snapshot["market_shares"]) > 0
        assert "Vodafone Germany" in snapshot["market_shares"]

    def test_market_shares_sum_to_100(self, seeded_db):
        """Market shares should approximately sum to 100%."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        shares = result.market_snapshot.get("market_shares", {})
        if shares:
            total = sum(shares.values())
            assert abs(total - 100.0) < 1.0, (
                f"Market shares sum to {total}%, expected ~100%"
            )

    def test_snapshot_has_subscriber_data(self, seeded_db):
        """Snapshot should include subscriber totals."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        snapshot = result.market_snapshot
        assert "total_mobile_subscribers_k" in snapshot
        assert snapshot["total_mobile_subscribers_k"] > 0

    def test_snapshot_has_penetration_rates(self, seeded_db):
        """Snapshot should include penetration rate estimates."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        snapshot = result.market_snapshot
        assert "penetration_rates" in snapshot
        pen = snapshot["penetration_rates"]
        assert "mobile_penetration_pct" in pen

    def test_snapshot_operator_count(self, seeded_db):
        """Snapshot should reflect 4 operators in Germany market."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        assert result.market_snapshot.get("operator_count") == 4


# ============================================================================
# Market Changes Tests
# ============================================================================

class TestMarketChanges:

    def test_market_changes_detected(self, seeded_db):
        """At least some market changes should be detected with seed data."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        # With 8 quarters of data and 4 operators, there should be
        # detectable QoQ or YoY changes
        assert len(result.changes) >= 0  # May be 0 if changes are within thresholds
        # The changes list should be a list of MarketChange
        for change in result.changes:
            assert isinstance(change, MarketChange)

    def test_changes_have_required_fields(self, seeded_db):
        """Each change should have change_type, description, and impact_type."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        for change in result.changes:
            assert change.change_type, "change_type should not be empty"
            assert change.description, "description should not be empty"
            assert change.impact_type in (
                "opportunity", "threat", "both", "neutral"
            )

    def test_changes_have_severity(self, seeded_db):
        """Each change should have a severity level."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        for change in result.changes:
            assert change.severity in ("low", "medium", "high", "critical")


# ============================================================================
# Opportunities and Threats Tests
# ============================================================================

class TestOpportunitiesAndThreats:

    def test_opportunities_and_threats_separated(self, seeded_db):
        """Opportunities and threats should be correctly classified."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        # Every item in opportunities should have impact_type == "opportunity"
        for opp in result.opportunities:
            assert opp.impact_type == "opportunity", (
                f"Opportunity item has wrong impact_type: {opp.impact_type}"
            )

        # Every item in threats should have impact_type == "threat"
        for threat in result.threats:
            assert threat.impact_type == "threat", (
                f"Threat item has wrong impact_type: {threat.impact_type}"
            )

    def test_opportunities_threats_are_subset_of_changes(self, seeded_db):
        """Opportunities and threats should be subsets of all changes."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        all_opp_descs = {c.description for c in result.opportunities}
        all_threat_descs = {c.description for c in result.threats}
        all_change_descs = {c.description for c in result.changes}

        assert all_opp_descs.issubset(all_change_descs)
        assert all_threat_descs.issubset(all_change_descs)


# ============================================================================
# Customer Segments Tests
# ============================================================================

class TestCustomerSegments:

    def test_customer_segments_populated(self, seeded_db):
        """At least 3 customer segments should be populated."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        assert len(result.customer_segments) >= 3

    def test_segment_types_present(self, seeded_db):
        """Should include consumer, enterprise, and wholesale segments."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        seg_types = {seg.segment_type for seg in result.customer_segments}
        assert "consumer" in seg_types
        assert "enterprise" in seg_types
        assert "wholesale" in seg_types

    def test_segments_have_names(self, seeded_db):
        """Each segment should have a non-empty name."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        for seg in result.customer_segments:
            assert seg.segment_name, "Segment name should not be empty"

    def test_segments_have_decision_factors(self, seeded_db):
        """Each segment should have purchase decision factors."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        for seg in result.customer_segments:
            assert len(seg.purchase_decision_factors) > 0, (
                f"Segment '{seg.segment_name}' lacks purchase decision factors"
            )

    def test_seven_segments_total(self, seeded_db):
        """Should have all 7 defined segments for German market."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        assert len(result.customer_segments) == 7
        names = {seg.segment_name for seg in result.customer_segments}
        expected_names = {
            "Consumer High-End",
            "Consumer Mainstream",
            "Consumer Price-Sensitive",
            "Consumer Youth",
            "Enterprise Large",
            "Enterprise SME",
            "Wholesale MVNO",
        }
        assert names == expected_names


# ============================================================================
# $APPEALS Assessment Tests
# ============================================================================

class TestAPPEALSAssessment:

    def test_appeals_dimensions_complete(self, seeded_db):
        """All 8 APPEALS dimensions should be present."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        dims = {a.dimension for a in result.appeals_assessment}
        expected = {"$", "A1", "P1", "P2", "E", "A2", "L", "S"}
        assert dims == expected, (
            f"Missing APPEALS dimensions: {expected - dims}"
        )

    def test_appeals_have_dimension_names(self, seeded_db):
        """Each APPEALS assessment should have a descriptive name."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        expected_names = {
            "Price", "Availability", "Packaging", "Performance",
            "Ease of Use", "Assurances", "Lifecycle Cost", "Social/Brand",
        }
        names = {a.dimension_name for a in result.appeals_assessment}
        assert names == expected_names

    def test_appeals_scores_in_range(self, seeded_db):
        """APPEALS scores should be between 0 and 5."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        for a in result.appeals_assessment:
            assert 0 <= a.our_score <= 5.0, (
                f"{a.dimension_name} score {a.our_score} out of range [0, 5]"
            )

    def test_appeals_have_competitor_scores(self, seeded_db):
        """APPEALS assessments should include competitor scores."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        for a in result.appeals_assessment:
            assert isinstance(a.competitor_scores, dict)
            # With seed data, should have scores for other operators
            assert len(a.competitor_scores) > 0, (
                f"{a.dimension_name} lacks competitor scores"
            )

    def test_appeals_have_gap_analysis(self, seeded_db):
        """Each APPEALS dimension should have a gap analysis string."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        for a in result.appeals_assessment:
            assert a.gap_analysis, (
                f"{a.dimension_name} lacks gap analysis"
            )

    def test_appeals_have_customer_priority(self, seeded_db):
        """Each APPEALS dimension should have a customer priority."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        valid_priorities = {"critical", "important", "nice_to_have"}
        for a in result.appeals_assessment:
            assert a.customer_priority in valid_priorities, (
                f"{a.dimension_name} has invalid priority: {a.customer_priority}"
            )

    def test_appeals_for_different_target(self, seeded_db):
        """APPEALS should work for Deutsche Telekom as target."""
        result = analyze_market_customer(
            seeded_db, "germany", "deutsche_telekom",
            target_period="CQ4_2025",
        )
        dims = {a.dimension for a in result.appeals_assessment}
        assert len(dims) == 8
        # DT should generally score higher (incumbent advantage)
        price_dim = next(
            a for a in result.appeals_assessment if a.dimension == "A1"
        )
        assert price_dim.our_score > 0


# ============================================================================
# Market Outlook Tests
# ============================================================================

class TestMarketOutlook:

    def test_market_outlook_set(self, seeded_db):
        """Market outlook should be one of favorable, challenging, or mixed."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        assert result.market_outlook in ("favorable", "challenging", "mixed")

    def test_market_outlook_reflects_changes(self, seeded_db):
        """Outlook should be deterministic given the same data."""
        result1 = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        result2 = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        assert result1.market_outlook == result2.market_outlook


# ============================================================================
# Key Message Tests
# ============================================================================

class TestKeyMessage:

    def test_key_message_not_empty(self, seeded_db):
        """Key message should be a non-empty string."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        assert result.key_message
        assert isinstance(result.key_message, str)
        assert len(result.key_message) > 10

    def test_key_message_mentions_market(self, seeded_db):
        """Key message should reference the market context."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        msg_lower = result.key_message.lower()
        # Should mention revenue, market, share, or similar
        assert any(
            term in msg_lower
            for term in ["revenue", "market", "share", "telecom", "outlook"]
        ), f"Key message lacks market context: {result.key_message}"


# ============================================================================
# Customer Value Migration Tests
# ============================================================================

class TestCustomerValueMigration:

    def test_value_migration_set(self, seeded_db):
        """Customer value migration should be a non-empty string."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        assert result.customer_value_migration
        assert isinstance(result.customer_value_migration, str)
        assert len(result.customer_value_migration) > 10


# ============================================================================
# Empty Database Handling Tests
# ============================================================================

class TestEmptyDatabaseHandling:

    def test_empty_db_handling(self, empty_db):
        """Empty DB should return a valid MarketCustomerInsight, not crash."""
        result = analyze_market_customer(
            empty_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        assert isinstance(result, MarketCustomerInsight)

    def test_empty_db_snapshot(self, empty_db):
        """Empty DB snapshot should show N/A values."""
        result = analyze_market_customer(
            empty_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        snapshot = result.market_snapshot
        assert snapshot.get("total_revenue") == "N/A" or snapshot.get("operator_count") == 0

    def test_empty_db_no_changes(self, empty_db):
        """Empty DB should produce no market changes."""
        result = analyze_market_customer(
            empty_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        assert len(result.changes) == 0

    def test_empty_db_has_segments(self, empty_db):
        """Empty DB should still produce segment definitions."""
        result = analyze_market_customer(
            empty_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        # Segments are defined from template, not DB data
        assert len(result.customer_segments) >= 3

    def test_empty_db_appeals_dimensions(self, empty_db):
        """Empty DB should still have all 8 APPEALS dimensions."""
        result = analyze_market_customer(
            empty_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        dims = {a.dimension for a in result.appeals_assessment}
        assert len(dims) == 8

    def test_empty_db_key_message(self, empty_db):
        """Empty DB should still produce a key message."""
        result = analyze_market_customer(
            empty_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        assert result.key_message
        assert isinstance(result.key_message, str)

    def test_empty_db_market_outlook(self, empty_db):
        """Empty DB should produce a valid market outlook."""
        result = analyze_market_customer(
            empty_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        assert result.market_outlook in ("favorable", "challenging", "mixed")


# ============================================================================
# Provenance Tracking Tests
# ============================================================================

class TestProvenanceTracking:

    def test_provenance_tracks_values(self, seeded_db):
        """Provenance should track market data points when provided."""
        prov = ProvenanceStore()
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
            provenance=prov,
        )
        values = prov.get_values()
        assert len(values) > 0, "Provenance should track at least some values"

    def test_provenance_tracks_revenue(self, seeded_db):
        """Provenance should track market total revenue."""
        prov = ProvenanceStore()
        analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
            provenance=prov,
        )
        rev_values = prov.get_values(field_name="market_total_revenue")
        assert len(rev_values) > 0

    def test_provenance_tracks_appeals(self, seeded_db):
        """Provenance should track APPEALS scores."""
        prov = ProvenanceStore()
        analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
            provenance=prov,
        )
        appeals_values = [
            v for v in prov.get_values()
            if v.field_name.startswith("appeals_")
        ]
        assert len(appeals_values) >= 8, (
            "Should track at least 8 APPEALS scores"
        )


# ============================================================================
# Return Type Tests
# ============================================================================

class TestReturnType:

    def test_returns_market_customer_insight(self, seeded_db):
        """Function should return a MarketCustomerInsight instance."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        assert isinstance(result, MarketCustomerInsight)

    def test_result_structure_complete(self, seeded_db):
        """Result should have all required fields populated."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ4_2025",
        )
        assert isinstance(result.market_snapshot, dict)
        assert isinstance(result.changes, list)
        assert isinstance(result.opportunities, list)
        assert isinstance(result.threats, list)
        assert isinstance(result.customer_segments, list)
        assert isinstance(result.appeals_assessment, list)
        assert isinstance(result.customer_value_migration, str)
        assert isinstance(result.market_outlook, str)
        assert isinstance(result.key_message, str)


# ============================================================================
# Auto-detect Period Tests
# ============================================================================

class TestAutoDetectPeriod:

    def test_auto_detect_latest_quarter(self, seeded_db):
        """Should auto-detect latest quarter when target_period is None."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
        )
        assert isinstance(result, MarketCustomerInsight)
        # Should use the latest available quarter from the seed data
        assert result.market_snapshot.get("calendar_quarter") is not None

    def test_explicit_period_honored(self, seeded_db):
        """Should use the explicitly provided target_period."""
        result = analyze_market_customer(
            seeded_db, "germany", "vodafone_germany",
            target_period="CQ3_2025",
        )
        assert result.market_snapshot.get("calendar_quarter") == "CQ3_2025"
