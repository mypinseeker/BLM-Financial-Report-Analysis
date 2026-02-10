"""Tests for tariff data: upsert, query, comparison, and seed integrity."""

import sys
from pathlib import Path

import pytest

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.database.db import TelecomDatabase


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def db():
    """Create an in-memory database with schema initialized."""
    database = TelecomDatabase(":memory:")
    database.init()
    # Register a test operator
    database.upsert_operator(
        "test_op", display_name="Test Op", country="DE", market="germany"
    )
    yield database
    database.close()


@pytest.fixture
def seeded_db():
    """Create an in-memory database with full Germany seed data."""
    from src.database.seed_germany import seed_all
    database = seed_all(":memory:")
    yield database
    database.close()


# ============================================================================
# Basic Upsert / Query
# ============================================================================

class TestUpsertTariff:

    def test_upsert_tariff_basic(self, db):
        """Basic insert and retrieve of a tariff."""
        db.upsert_tariff("test_op", "Plan A", "mobile_postpaid", "H1_2026", {
            "plan_tier": "m",
            "monthly_price": 30.0,
            "data_allowance": "20GB",
            "includes_5g": 1,
        })

        tariffs = db.get_tariffs(operator_id="test_op")
        assert len(tariffs) == 1
        assert tariffs[0]["plan_name"] == "Plan A"
        assert tariffs[0]["monthly_price"] == 30.0
        assert tariffs[0]["data_allowance"] == "20GB"
        assert tariffs[0]["includes_5g"] == 1
        assert tariffs[0]["snapshot_period"] == "H1_2026"

    def test_upsert_tariff_update(self, db):
        """Upserting same plan+type+snapshot updates the record."""
        db.upsert_tariff("test_op", "Plan A", "mobile_postpaid", "H1_2026", {
            "monthly_price": 30.0,
        })
        db.upsert_tariff("test_op", "Plan A", "mobile_postpaid", "H1_2026", {
            "monthly_price": 25.0,
        })

        tariffs = db.get_tariffs(operator_id="test_op")
        assert len(tariffs) == 1
        assert tariffs[0]["monthly_price"] == 25.0

    def test_upsert_tariff_historical(self, db):
        """Same plan in different snapshot periods creates separate records."""
        for period in ["H1_2023", "H2_2023", "H1_2024"]:
            db.upsert_tariff("test_op", "Plan A", "mobile_postpaid", period, {
                "monthly_price": 30.0,
            })

        tariffs = db.get_tariffs(operator_id="test_op")
        assert len(tariffs) == 3
        periods = {t["snapshot_period"] for t in tariffs}
        assert periods == {"H1_2023", "H2_2023", "H1_2024"}


# ============================================================================
# Query Filters
# ============================================================================

class TestGetTariffs:

    def test_get_tariffs_by_operator(self, db):
        """Filter tariffs by operator_id."""
        db.upsert_operator("op2", display_name="Op2", country="DE", market="germany")
        db.upsert_tariff("test_op", "Plan A", "mobile_postpaid", "H1_2026", {"monthly_price": 30})
        db.upsert_tariff("op2", "Plan B", "mobile_postpaid", "H1_2026", {"monthly_price": 40})

        tariffs = db.get_tariffs(operator_id="test_op")
        assert len(tariffs) == 1
        assert tariffs[0]["operator_id"] == "test_op"

    def test_get_tariffs_by_plan_type(self, db):
        """Filter tariffs by plan_type."""
        db.upsert_tariff("test_op", "Plan A", "mobile_postpaid", "H1_2026", {"monthly_price": 30})
        db.upsert_tariff("test_op", "Plan B", "fixed_dsl", "H1_2026", {"monthly_price": 35})

        tariffs = db.get_tariffs(plan_type="fixed_dsl")
        assert len(tariffs) == 1
        assert tariffs[0]["plan_type"] == "fixed_dsl"

    def test_get_tariffs_by_market(self, db):
        """Filter tariffs by market via operator join."""
        db.upsert_operator("uk_op", display_name="UK Op", country="UK", market="uk")
        db.upsert_tariff("test_op", "Plan A", "mobile_postpaid", "H1_2026", {"monthly_price": 30})
        db.upsert_tariff("uk_op", "Plan B", "mobile_postpaid", "H1_2026", {"monthly_price": 40})

        tariffs = db.get_tariffs(market="germany")
        assert len(tariffs) == 1
        assert tariffs[0]["market"] == "germany"


# ============================================================================
# Tariff Comparison
# ============================================================================

class TestTariffComparison:

    def test_get_tariff_comparison(self, db):
        """Cross-operator comparison for a plan type and period."""
        db.upsert_operator("op2", display_name="Op2", country="DE", market="germany")

        db.upsert_tariff("test_op", "Plan A", "mobile_postpaid", "H1_2026", {
            "plan_tier": "m", "monthly_price": 30,
        })
        db.upsert_tariff("op2", "Plan B", "mobile_postpaid", "H1_2026", {
            "plan_tier": "m", "monthly_price": 40,
        })

        comparison = db.get_tariff_comparison("germany", "mobile_postpaid", "H1_2026")
        assert len(comparison) == 2
        # Should be sorted by monthly_price ASC
        assert comparison[0]["monthly_price"] <= comparison[1]["monthly_price"]

    def test_tariff_comparison_filters_correctly(self, db):
        """Comparison only returns matching plan_type and snapshot_period."""
        db.upsert_tariff("test_op", "Plan A", "mobile_postpaid", "H1_2026", {"monthly_price": 30})
        db.upsert_tariff("test_op", "Plan B", "fixed_dsl", "H1_2026", {"monthly_price": 35})
        db.upsert_tariff("test_op", "Plan C", "mobile_postpaid", "H2_2025", {"monthly_price": 28})

        comparison = db.get_tariff_comparison("germany", "mobile_postpaid", "H1_2026")
        assert len(comparison) == 1
        assert comparison[0]["plan_name"] == "Plan A"


# ============================================================================
# Seed Data Integrity
# ============================================================================

class TestSeedTariffs:

    def test_seed_tariffs_count(self, seeded_db):
        """Seed data should produce at least 200 tariff records."""
        tariffs = seeded_db.get_tariffs()
        assert len(tariffs) >= 200, f"Only {len(tariffs)} tariffs, expected ≥200"

    def test_all_operators_have_tariffs(self, seeded_db):
        """All 4 German operators should have tariff data."""
        tariffs = seeded_db.get_tariffs()
        operators = {t["operator_id"] for t in tariffs}
        expected = {"vodafone_germany", "deutsche_telekom", "telefonica_o2", "one_and_one"}
        assert operators == expected

    def test_all_plan_types_covered(self, seeded_db):
        """All 7 plan types should be present."""
        tariffs = seeded_db.get_tariffs()
        plan_types = {t["plan_type"] for t in tariffs}
        expected = {
            "mobile_postpaid", "mobile_prepaid", "fixed_dsl",
            "fixed_cable", "fixed_fiber", "tv", "fmc_bundle",
        }
        assert plan_types == expected

    def test_historical_snapshots(self, seeded_db):
        """At least 5 different snapshot periods should exist."""
        tariffs = seeded_db.get_tariffs()
        snapshots = {t["snapshot_period"] for t in tariffs}
        assert len(snapshots) >= 5, f"Only {len(snapshots)} snapshot periods"

    def test_all_snapshots_present(self, seeded_db):
        """All 7 snapshot periods (H1_2023 through H1_2026) should exist."""
        tariffs = seeded_db.get_tariffs()
        snapshots = {t["snapshot_period"] for t in tariffs}
        expected = {"H1_2023", "H2_2023", "H1_2024", "H2_2024", "H1_2025", "H2_2025", "H1_2026"}
        assert snapshots == expected

    def test_vodafone_mobile_postpaid_h1_2026(self, seeded_db):
        """Verify specific Vodafone postpaid prices for H1_2026."""
        tariffs = seeded_db.get_tariffs(
            operator_id="vodafone_germany",
            plan_type="mobile_postpaid",
            snapshot_period="H1_2026",
        )
        assert len(tariffs) >= 4
        prices = {t["plan_tier"]: t["monthly_price"] for t in tariffs}
        assert prices["s"] == 25
        assert prices["m"] == 33
        assert prices["xl"] == 55

    def test_tariff_comparison_mobile_postpaid(self, seeded_db):
        """Cross-operator mobile postpaid comparison for H1_2026."""
        comparison = seeded_db.get_tariff_comparison(
            "germany", "mobile_postpaid", "H1_2026"
        )
        assert len(comparison) >= 12  # 4 operators × 3-4 tiers each
        operators = {c["operator_id"] for c in comparison}
        assert len(operators) == 4
