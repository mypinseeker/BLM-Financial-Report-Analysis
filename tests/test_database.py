"""Tests for TelecomDatabase and seed data integrity."""

import sys
from datetime import date
from pathlib import Path

import pytest

# Ensure project root is on path
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.database.db import TelecomDatabase
from src.database.period_utils import get_converter


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def db():
    """Create an in-memory database with schema initialized."""
    database = TelecomDatabase(":memory:")
    database.init()
    yield database
    database.close()


@pytest.fixture
def seeded_db():
    """Create an in-memory database with Germany seed data."""
    from src.database.seed_germany import seed_all
    database = seed_all(":memory:")
    yield database
    database.close()


# ============================================================================
# Schema Creation
# ============================================================================

class TestSchemaCreation:

    def test_all_tables_created(self, db):
        """Verify all 14 tables are created."""
        cursor = db.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in cursor.fetchall()]

        expected_tables = [
            "competitive_scores",
            "data_provenance",
            "earnings_call_highlights",
            "executives",
            "financial_quarterly",
            "intelligence_events",
            "macro_environment",
            "network_infrastructure",
            "operators",
            "source_registry",
            "subscriber_quarterly",
            "tariffs",
            "user_feedback",
        ]

        for table in expected_tables:
            assert table in tables, f"Table '{table}' not found"

    def test_indexes_created(self, db):
        """Verify indexes are created."""
        cursor = db.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'"
        )
        indexes = [row[0] for row in cursor.fetchall()]
        assert len(indexes) >= 7  # At least 7 custom indexes


# ============================================================================
# Operator CRUD
# ============================================================================

class TestOperatorCRUD:

    def test_upsert_and_query_operator(self, db):
        """Insert operator and retrieve it."""
        db.upsert_operator(
            "test_op",
            display_name="Test Operator",
            country="Germany",
            market="germany",
            operator_type="challenger",
        )

        ops = db.get_operators_in_market("germany")
        assert len(ops) == 1
        assert ops[0]["operator_id"] == "test_op"
        assert ops[0]["display_name"] == "Test Operator"
        assert ops[0]["country"] == "Germany"

    def test_upsert_operator_update(self, db):
        """Upsert should update existing operator."""
        db.upsert_operator("op1", display_name="V1", country="DE", market="de")
        db.upsert_operator("op1", display_name="V2", country="DE", market="de")

        ops = db.get_operators_in_market("de")
        assert len(ops) == 1
        assert ops[0]["display_name"] == "V2"


# ============================================================================
# Financial Data
# ============================================================================

class TestFinancialData:

    def test_upsert_and_query_financial(self, db):
        """Insert financial data and retrieve via timeseries."""
        db.upsert_operator("vodafone_germany", display_name="VF", country="DE", market="germany")

        # Insert a single quarter
        db.upsert_financial("vodafone_germany", "Q3 FY26", {
            "total_revenue": 3092,
            "service_revenue": 2726,
            "ebitda": 1120,
            "ebitda_margin_pct": 36.2,
        })

        # Query
        data = db.get_financial_timeseries(
            "vodafone_germany", n_quarters=8, end_cq="CQ4_2025"
        )
        assert len(data) == 1
        assert data[0]["calendar_quarter"] == "CQ4_2025"
        assert data[0]["total_revenue"] == 3092
        assert data[0]["ebitda_margin_pct"] == 36.2

    def test_financial_auto_converts_period(self, db):
        """Financial upsert auto-converts Vodafone fiscal period to CQ."""
        db.upsert_operator("vodafone_germany", display_name="VF", country="DE", market="germany")
        db.upsert_financial("vodafone_germany", "Q1 FY26", {
            "total_revenue": 3090,
        })

        data = db.get_financial_timeseries(
            "vodafone_germany", n_quarters=4, end_cq="CQ2_2025"
        )
        assert len(data) == 1
        assert data[0]["calendar_quarter"] == "CQ2_2025"

    def test_financial_upsert_updates_existing(self, db):
        """Second upsert for same CQ updates the record."""
        db.upsert_operator("vodafone_germany", display_name="VF", country="DE", market="germany")
        db.upsert_financial("vodafone_germany", "Q3 FY26", {"total_revenue": 3000})
        db.upsert_financial("vodafone_germany", "Q3 FY26", {"total_revenue": 3092})

        data = db.get_financial_timeseries(
            "vodafone_germany", n_quarters=8, end_cq="CQ4_2025"
        )
        assert len(data) == 1
        assert data[0]["total_revenue"] == 3092

    def test_calendar_year_financial(self, db):
        """DT uses calendar year periods."""
        db.upsert_operator("deutsche_telekom", display_name="DT", country="DE", market="germany")
        db.upsert_financial("deutsche_telekom", "Q4 2025", {
            "total_revenue": 6200,
        })

        data = db.get_financial_timeseries(
            "deutsche_telekom", n_quarters=4, end_cq="CQ4_2025"
        )
        assert len(data) == 1
        assert data[0]["calendar_quarter"] == "CQ4_2025"


# ============================================================================
# Subscriber Data
# ============================================================================

class TestSubscriberData:

    def test_upsert_and_query_subscriber(self, db):
        """Insert subscriber data and retrieve."""
        db.upsert_operator("vodafone_germany", display_name="VF", country="DE", market="germany")
        db.upsert_subscriber("vodafone_germany", "Q3 FY26", {
            "mobile_total_k": 32500,
            "broadband_total_k": 9940,
            "mobile_arpu": 12.8,
        })

        data = db.get_subscriber_timeseries(
            "vodafone_germany", n_quarters=8, end_cq="CQ4_2025"
        )
        assert len(data) == 1
        assert data[0]["mobile_total_k"] == 32500
        assert data[0]["broadband_total_k"] == 9940
        assert data[0]["mobile_arpu"] == 12.8


# ============================================================================
# Market Comparison
# ============================================================================

class TestMarketComparison:

    def test_market_comparison_returns_all_operators(self, db):
        """Market comparison joins financial + subscriber data."""
        # Register operators
        db.upsert_operator("op1", display_name="Op1", country="DE", market="germany")
        db.upsert_operator("op2", display_name="Op2", country="DE", market="germany")

        # Insert financial data for same CQ
        db.upsert_financial("op1", "Q4 2025", {"total_revenue": 6000})
        db.upsert_financial("op2", "Q4 2025", {"total_revenue": 3000})

        # Insert subscriber data
        db.upsert_subscriber("op1", "Q4 2025", {"mobile_total_k": 50000})
        db.upsert_subscriber("op2", "Q4 2025", {"mobile_total_k": 30000})

        result = db.get_market_comparison("germany", "CQ4_2025")
        assert len(result) == 2
        # Should be ordered by total_revenue DESC
        assert result[0]["operator_id"] == "op1"
        assert result[0]["total_revenue"] == 6000
        assert result[0]["mobile_total_k"] == 50000
        assert result[1]["operator_id"] == "op2"

    def test_market_comparison_aligned_data(self, db):
        """Operators in different CQs should not cross-contaminate."""
        db.upsert_operator("op1", display_name="Op1", country="DE", market="germany")

        db.upsert_financial("op1", "Q3 2025", {"total_revenue": 5000})
        db.upsert_financial("op1", "Q4 2025", {"total_revenue": 6000})

        # Query for Q4 only
        result = db.get_market_comparison("germany", "CQ4_2025")
        assert len(result) == 1
        assert result[0]["total_revenue"] == 6000


# ============================================================================
# Network, Competitive Scores, Macro
# ============================================================================

class TestMiscellaneousData:

    def test_competitive_scores(self, db):
        """Insert and query competitive scores."""
        db.upsert_operator("op1", display_name="Op1", country="DE", market="germany")
        db.upsert_competitive_scores("op1", "CQ4_2025", {
            "Network Coverage": 80,
            "Brand Strength": 82,
        })

        scores = db.get_competitive_scores("germany", "CQ4_2025")
        assert len(scores) == 2
        dims = {s["dimension"]: s["score"] for s in scores}
        assert dims["Network Coverage"] == 80
        assert dims["Brand Strength"] == 82

    def test_network_data(self, db):
        """Insert and query network data."""
        db.upsert_operator("op1", display_name="Op1", country="DE", market="germany")
        db.upsert_network("op1", "CQ4_2025", {
            "five_g_coverage_pct": 90,
            "four_g_coverage_pct": 99.5,
            "technology_mix": {"vendor": "Ericsson"},
        })

        data = db.get_network_data("op1", "CQ4_2025")
        assert data["five_g_coverage_pct"] == 90
        assert data["technology_mix"]["vendor"] == "Ericsson"

    def test_network_data_latest(self, db):
        """get_network_data without CQ returns latest."""
        db.upsert_operator("op1", display_name="Op1", country="DE", market="germany")
        db.upsert_network("op1", "CQ3_2025", {"five_g_coverage_pct": 85})
        db.upsert_network("op1", "CQ4_2025", {"five_g_coverage_pct": 90})

        data = db.get_network_data("op1")
        assert data["five_g_coverage_pct"] == 90

    def test_macro_data(self, db):
        """Insert and query macro data."""
        db.upsert_macro("Germany", "CQ4_2025", {
            "gdp_growth_pct": 0.8,
            "inflation_pct": 2.1,
        })

        data = db.get_macro_data("Germany", n_quarters=4, end_cq="CQ4_2025")
        assert len(data) == 1
        assert data[0]["gdp_growth_pct"] == 0.8

    def test_executives(self, db):
        """Insert and query executive data."""
        db.upsert_operator("op1", display_name="Op1", country="DE", market="germany")
        db.upsert_executive("op1", {
            "name": "John Doe",
            "title": "CEO",
            "start_date": "2023-01-01",
            "is_current": 1,
        })

        execs = db.get_executives("op1")
        assert len(execs) == 1
        assert execs[0]["name"] == "John Doe"
        assert execs[0]["title"] == "CEO"

    def test_intelligence_events(self, db):
        """Insert and query intelligence events."""
        db.upsert_intelligence({
            "market": "germany",
            "event_date": date.today().isoformat(),
            "category": "regulatory",
            "title": "BNetzA ruling",
            "description": "New regulation",
            "severity": "high",
        })

        events = db.get_intelligence_events(market="germany")
        assert len(events) == 1
        assert events[0]["category"] == "regulatory"

    def test_earnings_highlights(self, db):
        """Insert and query earnings highlights."""
        db.upsert_operator("op1", display_name="Op1", country="DE", market="germany")
        db.upsert_earnings_highlight("op1", "CQ4_2025", {
            "segment": "mobile",
            "highlight_type": "guidance",
            "content": "Revenue expected to grow",
        })

        highlights = db.get_earnings_highlights("op1", "CQ4_2025")
        assert len(highlights) == 1
        assert highlights[0]["content"] == "Revenue expected to grow"


# ============================================================================
# Context Manager
# ============================================================================

class TestContextManager:

    def test_context_manager(self):
        """Database can be used as context manager."""
        with TelecomDatabase(":memory:") as db:
            db.upsert_operator("op1", display_name="Op1", country="DE", market="de")
            ops = db.get_operators_in_market("de")
            assert len(ops) == 1


# ============================================================================
# Seed Data Integrity
# ============================================================================

class TestSeedDataIntegrity:

    def test_seed_creates_4_operators(self, seeded_db):
        """Seed should register 4 Germany operators."""
        ops = seeded_db.get_operators_in_market("germany")
        assert len(ops) == 4

        op_ids = {op["operator_id"] for op in ops}
        assert op_ids == {
            "vodafone_germany", "deutsche_telekom",
            "telefonica_o2", "one_and_one"
        }

    def test_seed_creates_8_quarters_financial(self, seeded_db):
        """Each operator should have 8 quarters of financial data."""
        for op_id in ["vodafone_germany", "deutsche_telekom", "telefonica_o2", "one_and_one"]:
            data = seeded_db.get_financial_timeseries(
                op_id, n_quarters=8, end_cq="CQ4_2025"
            )
            assert len(data) == 8, f"{op_id} has {len(data)} quarters, expected 8"

    def test_seed_creates_8_quarters_subscriber(self, seeded_db):
        """Each operator should have 8 quarters of subscriber data."""
        for op_id in ["vodafone_germany", "deutsche_telekom", "telefonica_o2", "one_and_one"]:
            data = seeded_db.get_subscriber_timeseries(
                op_id, n_quarters=8, end_cq="CQ4_2025"
            )
            assert len(data) == 8, f"{op_id} has {len(data)} subscriber quarters, expected 8"

    def test_seed_financial_data_values(self, seeded_db):
        """Verify specific financial data values from seed."""
        # Vodafone Q3 FY26 (CQ4_2025) revenue should be 3092 EUR M
        data = seeded_db.get_financial_timeseries(
            "vodafone_germany", n_quarters=1, end_cq="CQ4_2025"
        )
        assert len(data) == 1
        assert data[0]["total_revenue"] == 3092
        assert data[0]["service_revenue"] == 2726
        assert data[0]["ebitda"] == 1120
        assert data[0]["ebitda_margin_pct"] == 36.2

    def test_seed_dt_financial_values(self, seeded_db):
        """Verify DT financial values for latest quarter."""
        data = seeded_db.get_financial_timeseries(
            "deutsche_telekom", n_quarters=1, end_cq="CQ4_2025"
        )
        assert len(data) == 1
        assert data[0]["total_revenue"] == 6200
        assert data[0]["ebitda"] == 2610
        assert data[0]["ebitda_margin_pct"] == 42.1

    def test_seed_subscriber_values(self, seeded_db):
        """Verify subscriber counts from seed."""
        data = seeded_db.get_subscriber_timeseries(
            "vodafone_germany", n_quarters=1, end_cq="CQ4_2025"
        )
        assert len(data) == 1
        # total_mobile_subs_m was 32.5 -> 32500k
        assert data[0]["mobile_total_k"] == 32500
        # broadband_subs_m was 9.94 -> 9940k
        assert data[0]["broadband_total_k"] == 9940

    def test_seed_competitive_scores(self, seeded_db):
        """Verify competitive scores were seeded."""
        scores = seeded_db.get_competitive_scores("germany", "CQ4_2025")
        assert len(scores) > 0

        # Check Vodafone Network Coverage score
        vf_scores = [s for s in scores if s["operator_id"] == "vodafone_germany"]
        nc_score = [s for s in vf_scores if s["dimension"] == "Network Coverage"]
        assert len(nc_score) == 1
        assert nc_score[0]["score"] == 80

    def test_seed_macro_data(self, seeded_db):
        """Verify macro data was seeded."""
        data = seeded_db.get_macro_data("Germany", n_quarters=8, end_cq="CQ4_2025")
        assert len(data) == 8

        # Check latest quarter
        latest = data[-1]
        assert latest["gdp_growth_pct"] == 0.8
        assert latest["five_g_adoption_pct"] == 56

    def test_seed_network_data(self, seeded_db):
        """Verify network infrastructure data was seeded."""
        vf_net = seeded_db.get_network_data("vodafone_germany", "CQ4_2025")
        assert vf_net["five_g_coverage_pct"] == 92

        dt_net = seeded_db.get_network_data("deutsche_telekom", "CQ4_2025")
        assert dt_net["five_g_coverage_pct"] == 97

    def test_seed_market_comparison(self, seeded_db):
        """Market comparison should return all 4 operators for CQ4_2025."""
        comparison = seeded_db.get_market_comparison("germany", "CQ4_2025")
        assert len(comparison) == 4

        # DT should be first (highest revenue)
        assert comparison[0]["operator_id"] == "deutsche_telekom"

    def test_seed_calendar_quarter_alignment(self, seeded_db):
        """Verify that Vodafone and DT data aligns on calendar quarters."""
        vf = seeded_db.get_financial_timeseries(
            "vodafone_germany", n_quarters=8, end_cq="CQ4_2025"
        )
        dt = seeded_db.get_financial_timeseries(
            "deutsche_telekom", n_quarters=8, end_cq="CQ4_2025"
        )

        vf_cqs = [row["calendar_quarter"] for row in vf]
        dt_cqs = [row["calendar_quarter"] for row in dt]

        assert vf_cqs == dt_cqs, "Vodafone and DT calendar quarters should match"
        assert vf_cqs == [
            "CQ1_2024", "CQ2_2024", "CQ3_2024", "CQ4_2024",
            "CQ1_2025", "CQ2_2025", "CQ3_2025", "CQ4_2025",
        ]

    def test_seed_vodafone_period_labels(self, seeded_db):
        """Verify Vodafone data retains operator period labels."""
        data = seeded_db.get_financial_timeseries(
            "vodafone_germany", n_quarters=8, end_cq="CQ4_2025"
        )

        periods = [row["period"] for row in data]
        expected = [
            "Q4 FY24", "Q1 FY25", "Q2 FY25", "Q3 FY25",
            "Q4 FY25", "Q1 FY26", "Q2 FY26", "Q3 FY26",
        ]
        assert periods == expected

    def test_seed_executives(self, seeded_db):
        """Verify executive data was seeded."""
        execs = seeded_db.get_executives("vodafone_germany")
        assert len(execs) >= 3  # CEO, CFO, CTO

        names = {e["name"] for e in execs}
        assert "Marcel de Groot" in names

    def test_market_timeseries(self, seeded_db):
        """Market timeseries returns data for all operators across quarters."""
        data = seeded_db.get_market_timeseries(
            "germany", n_quarters=8, end_cq="CQ4_2025"
        )
        # 4 operators * 8 quarters = 32 rows
        assert len(data) == 32
