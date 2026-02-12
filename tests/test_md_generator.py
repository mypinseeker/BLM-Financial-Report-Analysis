"""Tests for the BLM MD Strategic Insight Report generator.

Validates:
- md_utils formatting functions
- StrategicDiagnosisComputer rule-based logic
- BLMMdGenerator end-to-end report generation
- Module renderers produce valid Markdown
"""
from __future__ import annotations

import os
import tempfile
import pytest

from src.output.md_utils import (
    md_table, md_kv_table, fmt_currency, fmt_pct, fmt_subs,
    fmt_number, section_header, section_divider, operator_display_name,
    market_display_name, safe_get, safe_list, safe_dict,
    bullet_list, numbered_list, code_block, blockquote,
    empty_section_notice, truncate,
)
from src.output.strategic_diagnosis import (
    StrategicDiagnosisComputer, StrategicDiagnosis, _to_float, _name_match,
)
from src.output.md_generator import BLMMdGenerator


# -----------------------------------------------------------------------
# Fixtures — minimal FiveLooksResult mock
# -----------------------------------------------------------------------

class MockPEST:
    def __init__(self):
        self.political_factors = [MockFactor("Regulation", "opportunity", "high")]
        self.economic_factors = [MockFactor("GDP Growth", "threat", "medium")]
        self.society_factors = [MockFactor("5G Adoption", "opportunity", "high")]
        self.technology_factors = [MockFactor("Fiber Buildout", "both", "high")]
        self.overall_weather = "mixed"
        self.weather_explanation = "Net favorable with two risks"
        self.policy_opportunities = ["Spectrum extension", "Subsidies"]
        self.policy_threats = ["Coverage obligations"]
        self.tech_addressable_market = ""
        self.key_message = "Cautiously favorable macro environment"


class MockFactor:
    def __init__(self, name, impact, severity):
        self.factor_name = name
        self.dimension = "P"
        self.dimension_name = "Political"
        self.current_status = f"{name} status"
        self.trend = "stable"
        self.trend_direction = "stable"
        self.industry_impact = f"{name} industry impact"
        self.company_impact = f"{name} company impact"
        self.impact_type = impact
        self.severity = severity
        self.time_horizon = "medium_term"
        self.predictability = "uncertain"
        self.evidence = [f"Evidence for {name}"]
        self.data_source = ""


class MockTrends:
    def __init__(self):
        self.pest = MockPEST()
        self.industry_market_size = "€12.3B/quarter"
        self.industry_growth_rate = "+0.3%"
        self.industry_profit_trend = "Stable"
        self.industry_concentration = "CR4 = 100%"
        self.industry_lifecycle_stage = "mature"
        self.new_business_models = ["FWA", "Network-as-a-Service"]
        self.technology_revolution = ["5G SA", "Fiber"]
        self.key_success_factors = ["Retention", "FMC", "B2B pivot"]
        self.value_transfer_trends = ["Voice → Data", "Linear TV → Streaming"]
        self.key_message = "Mature market with two existential technology risks"


class MockAPPEALS:
    def __init__(self, dim, dim_name, our, comp):
        self.dimension = dim
        self.dimension_name = dim_name
        self.our_score = our
        self.competitor_scores = comp
        self.customer_priority = "important"
        self.gap_analysis = f"Gap in {dim_name}"


class MockMarketCustomer:
    def __init__(self):
        self.market_snapshot = {"total_revenue": "€12.3B", "operators": 4}
        self.changes = []
        self.opportunities = []
        self.threats = []
        self.customer_segments = []
        self.appeals_assessment = [
            MockAPPEALS("$", "Price", 3.6, {"dt_germany": 4.2, "o2_germany": 3.8}),
            MockAPPEALS("P1", "Performance", 3.8, {"dt_germany": 4.7, "o2_germany": 3.5}),
        ]
        self.customer_value_migration = "Value migrating from consumer to B2B"
        self.market_outlook = "mixed"
        self.key_message = "Squeezed middle confirmed in customer perception"


class MockPorterForce:
    def __init__(self, name, level):
        self.force_name = name
        self.force_level = level
        self.key_factors = [{"name": f"{name} driver", "description": "desc", "impact": "high", "trend": "stable"}]
        self.implications = [f"Implication for {name}"]


class MockCompetitorDeepDive:
    def __init__(self, op):
        self.operator = op
        self.financial_health = {"revenue": 6200, "ebitda_margin": 42.1}
        self.subscriber_health = {"mobile_subs": 52200}
        self.network_status = {"5g_coverage": "97%"}
        self.product_portfolio = ["Mobile", "Fixed", "TV"]
        self.new_product_pipeline = []
        self.growth_strategy = "Premium strategy"
        self.supply_chain_status = ""
        self.ecosystem_partners = []
        self.core_control_points = ["Fiber network"]
        self.business_model = "Integrated operator"
        self.org_structure = ""
        self.incentive_system = ""
        self.talent_culture = ""
        self.ma_activity = []
        self.strengths = ["Market leader", "Brand strength"]
        self.weaknesses = ["Slow innovation"]
        self.problems = []
        self.likely_future_actions = ["Fiber expansion"]
        self.implications = []


class MockCompetition:
    def __init__(self):
        self.five_forces = {
            "existing_competitors": MockPorterForce("existing_competitors", "high"),
            "new_entrants": MockPorterForce("new_entrants", "medium"),
        }
        self.overall_competition_intensity = "high"
        self.competitor_analyses = {
            "dt_germany": MockCompetitorDeepDive("dt_germany"),
        }
        self.comparison_table = {
            "revenue": {"dt_germany": 6200, "vodafone_germany": 3092, "o2_germany": 2000},
            "revenue_share": {"dt_germany": 50.3, "vodafone_germany": 25.1, "o2_germany": 16.2},
        }
        self.competitive_landscape = "4-operator oligopoly dominated by DT"
        self.key_message = "DT unassailable #1; VF squeezed between premium and value"


class MockSegment:
    def __init__(self, name, health):
        self.segment_name = name
        self.segment_id = name.lower()
        self.key_metrics = {"revenue": "€800M/q"}
        self.changes = []
        self.trend_data = {}
        self.competitor_comparison = {}
        self.attributions = []
        self.health_status = health
        self.key_message = f"{name} segment message"
        self.action_required = ""


class MockNetwork:
    def __init__(self):
        self.technology_mix = {"cable": 70, "fiber": 5}
        self.controlled_vs_resale = {}
        self.coverage = {"5g": "92%"}
        self.quality_scores = {}
        self.homepass_vs_connect = {}
        self.evolution_strategy = {}
        self.investment_direction = "Fiber JV + DOCSIS 4.0"
        self.vs_competitors = ""
        self.consumer_impact = ""
        self.b2b_impact = ""
        self.cost_impact = ""


class MockBMC:
    def __init__(self):
        self.key_partners = ["Altice", "Ericsson"]
        self.key_activities = ["Network ops", "Customer service"]
        self.key_resources = ["Cable network", "Spectrum"]
        self.value_propositions = ["Convergence", "B2B solutions"]
        self.customer_relationships = ["Retail stores", "Online"]
        self.channels = ["Retail", "Online", "B2B direct"]
        self.customer_segments = ["Consumer", "Enterprise"]
        self.cost_structure = ["Network", "Content", "Staff"]
        self.revenue_streams = ["Mobile", "Fixed", "B2B", "Wholesale"]


class MockSelfInsight:
    def __init__(self):
        self.financial_health = {
            "revenue": 3092, "ebitda_margin": 36.2,
            "revenue_growth_yoy": 0.7, "churn": 1.05,
        }
        self.revenue_breakdown = {"mobile": 1200, "fixed": 795, "b2b": 520, "wholesale": 380}
        self.market_positions = {}
        self.share_trends = {}
        self.segment_analyses = [
            MockSegment("Mobile", "stable"),
            MockSegment("Fixed Broadband", "weakening"),
            MockSegment("B2B", "strong"),
        ]
        self.network = MockNetwork()
        self.customer_perception = {"summary": "Below market average"}
        self.leadership_changes = [
            {"name": "Philippe Rogge", "title": "CEO", "is_current": True, "tenure_years": 2},
        ]
        self.bmc = MockBMC()
        self.org_culture = "Transformation-focused"
        self.talent_assessment = {}
        self.performance_gap = "Revenue growth lags DT"
        self.opportunity_gap = "Fiber and B2B underexploited"
        self.strategic_review = "Managed optimization, not growth"
        self.management_commentary = [
            {"speaker": "CEO", "quote": "MDU base effect fades from Q3", "topic": "TV"},
        ]
        self.strengths = ["Cable network (24M homes)", "TV market leader", "B2B growth"]
        self.weaknesses = ["Customer service (70 score)", "Pricing perception", "Wholesale dependency"]
        self.exposure_points = []
        self.health_rating = "stable"
        self.key_message = "Stable but diverging trajectories"


class MockSWOT:
    def __init__(self):
        self.strengths = ["Cable network", "TV leadership", "B2B growth", "EBITDA margin", "Brand"]
        self.weaknesses = ["Customer service", "Pricing", "Wholesale risk"]
        self.opportunities = ["FibreCo JV", "Spectrum extension", "FMC growth", "Skaylink", "5G SA"]
        self.threats = ["DT fiber overbuild", "Nebenkostenprivileg", "Price pressure"]
        self.so_strategies = ["Leverage cable for FMC convergence moat", "B2B via Skaylink"]
        self.wo_strategies = ["Fix customer service to reduce churn"]
        self.st_strategies = ["DOCSIS 4.0 to counter DT fiber"]
        self.wt_strategies = ["Manage wholesale transition carefully"]
        self.key_message = "Offensive posture (SO-dominant)"


class MockSPAN:
    def __init__(self, name, ma, cp, quad):
        self.opportunity_name = name
        self.market_attractiveness = ma
        self.competitive_position = cp
        self.quadrant = quad
        self.recommended_strategy = f"Strategy for {name}"
        self.market_size_score = ma
        self.market_growth_score = ma
        self.profit_potential_score = ma
        self.strategic_value_score = ma
        self.market_share_score = cp
        self.product_fit_score = cp
        self.brand_channel_score = cp
        self.tech_capability_score = cp
        self.bubble_size = 1.0


class MockOpportunityItem:
    def __init__(self, name, priority, window):
        self.name = name
        self.description = f"Execute {name}"
        self.derived_from = ["SWOT", "SPAN"]
        self.addressable_market = "€500M"
        self.addressable_market_source = ""
        self.our_capability = "medium"
        self.competition_intensity = "high"
        self.time_window = window
        self.priority = priority
        self.priority_rationale = f"High impact {name}"


class MockOpportunities:
    def __init__(self):
        self.span_positions = [
            MockSPAN("FibreCo JV", 8.5, 7.0, "grow_invest"),
            MockSPAN("FMC Expansion", 7.5, 8.0, "grow_invest"),
            MockSPAN("Customer Service Fix", 6.0, 4.0, "acquire_skills"),
        ]
        self.grow_invest = ["FibreCo JV", "FMC Expansion"]
        self.acquire_skills = ["Customer Service Fix"]
        self.harvest = []
        self.avoid_exit = []
        self.window_opportunities = ["FibreCo JV — 3-5 year execution window"]
        self.opportunities = [
            MockOpportunityItem("Defend Fixed BB", "P0", "immediate"),
            MockOpportunityItem("FMC Penetration", "P0", "1-2 years"),
            MockOpportunityItem("Fix Customer Service", "P1", "1-2 years"),
            MockOpportunityItem("B2B via Skaylink", "P1", "1-2 years"),
            MockOpportunityItem("Wholesale Transition", "P1", "3-5 years"),
        ]
        self.key_message = "86% in Grow/Invest — favorable hand"


class MockProvenance:
    def quality_report(self):
        return {
            "total_data_points": 150,
            "high_confidence": 80,
            "medium_confidence": 50,
            "low_confidence": 15,
            "estimated": 5,
            "unique_sources": 12,
        }

    def to_footnotes(self):
        return ["[1] Vodafone Q3 FY26 earnings release", "[2] BNetzA market data"]


class MockFiveLooksResult:
    def __init__(self):
        self.target_operator = "vodafone_germany"
        self.market = "germany"
        self.analysis_period = "CQ4_2025"
        self.trends = MockTrends()
        self.market_customer = MockMarketCustomer()
        self.competition = MockCompetition()
        self.self_analysis = MockSelfInsight()
        self.swot = MockSWOT()
        self.opportunities = MockOpportunities()
        self.tariff_analysis = None  # No tariff data
        self.provenance = MockProvenance()


@pytest.fixture
def mock_result():
    return MockFiveLooksResult()


@pytest.fixture
def mock_result_with_tariff():
    r = MockFiveLooksResult()
    r.tariff_analysis = {
        "total_records": 466,
        "key_message": "Worst price-value in market; cable is pricing bright spot",
        "summary": "Comprehensive tariff comparison across 4 operators",
        "mobile_pricing": [
            {"operator": "Vodafone", "plan_name": "GigaMobil S", "price": "€25", "data": "15GB", "cost_per_gb": "€1.67"},
            {"operator": "DT", "plan_name": "MagentaMobil S", "price": "€40", "data": "20GB", "cost_per_gb": "€2.00"},
        ],
    }
    return r


@pytest.fixture
def empty_result():
    r = MockFiveLooksResult()
    r.trends = None
    r.market_customer = None
    r.competition = None
    r.self_analysis = None
    r.swot = None
    r.opportunities = None
    r.tariff_analysis = None
    r.provenance = None
    return r


# -----------------------------------------------------------------------
# md_utils tests
# -----------------------------------------------------------------------

class TestMdUtils:
    def test_md_table_basic(self):
        result = md_table(["A", "B"], [["1", "2"], ["3", "4"]])
        assert "| A | B |" in result
        assert "| 1 | 2 |" in result
        assert ":---" in result

    def test_md_table_alignment(self):
        result = md_table(["Name", "Value"], [["a", "1"]], align=["l", "r"])
        assert ":---" in result
        assert "---:" in result

    def test_md_table_empty_headers(self):
        assert md_table([], []) == ""

    def test_md_kv_table(self):
        result = md_kv_table({"Key1": "Val1", "Key2": "Val2"})
        assert "| Item | Detail |" in result
        assert "| Key1 | Val1 |" in result

    def test_fmt_currency_with_none(self):
        assert fmt_currency(None) == "N/A"

    def test_fmt_currency_basic(self):
        result = fmt_currency(3092)
        assert "3,092" in result

    def test_fmt_pct_positive(self):
        assert fmt_pct(8.9) == "+8.9%"

    def test_fmt_pct_negative(self):
        assert fmt_pct(-3.4) == "-3.4%"

    def test_fmt_pct_none(self):
        assert fmt_pct(None) == "N/A"

    def test_fmt_subs(self):
        assert fmt_subs(32500) == "32,500K"
        assert fmt_subs(None) == "N/A"

    def test_section_header(self):
        assert section_header("Test", 2) == "## Test"
        assert section_header("Test", 3) == "### Test"

    def test_operator_display_name(self):
        assert "Vodafone" in operator_display_name("vodafone_germany")
        assert "Deutsche Telekom" in operator_display_name("dt_germany")
        assert "1&1" in operator_display_name("1and1_germany")

    def test_market_display_name(self):
        assert "German" in market_display_name("germany")
        assert "Chilean" in market_display_name("chile")

    def test_safe_get_basic(self):
        class Obj:
            x = 42
        assert safe_get(Obj(), "x") == 42
        assert safe_get(None, "x", "default") == "default"

    def test_safe_get_dotted(self):
        class Inner:
            y = 10
        class Outer:
            inner = Inner()
        assert safe_get(Outer(), "inner.y") == 10

    def test_safe_get_dict(self):
        d = {"a": {"b": 5}}
        assert safe_get(d, "a.b") == 5

    def test_bullet_list(self):
        result = bullet_list(["one", "two"])
        assert "- one" in result
        assert "- two" in result

    def test_code_block(self):
        result = code_block("hello", "python")
        assert "```python" in result
        assert "hello" in result

    def test_truncate(self):
        assert truncate("short") == "short"
        assert truncate("a" * 200, 50).endswith("...")

    def test_empty_section_notice(self):
        result = empty_section_notice("Test")
        assert "Insufficient data" in result


# -----------------------------------------------------------------------
# Strategic Diagnosis tests
# -----------------------------------------------------------------------

class TestStrategicDiagnosis:
    def test_compute_basic(self, mock_result):
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        assert isinstance(diag, StrategicDiagnosis)
        assert diag.one_line_verdict != ""
        assert diag.central_diagnosis_label != ""
        assert diag.competitive_stance != ""

    def test_operator_rank(self, mock_result):
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        assert diag.operator_rank == 2  # VF is #2 by revenue

    def test_market_structure(self, mock_result):
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        assert "operator" in diag.market_structure.lower()

    def test_competitive_stance_so_dominant(self, mock_result):
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        assert "Offensive" in diag.competitive_stance  # S(5) > W(3), O(5) > T(3)

    def test_diagnosis_label_squeezed_middle(self, mock_result):
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        # VF: 25.1% share, DT: 50.3% → gap = 25.2pp, 0 APPEALS wins → Squeezed Middle
        assert "Squeezed" in diag.central_diagnosis_label

    def test_priorities_populated(self, mock_result):
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        assert len(diag.priorities) > 0
        assert len(diag.priorities) <= 5

    def test_strategic_traps(self, mock_result):
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        assert len(diag.strategic_traps) > 0
        trap_names = [t["trap"] for t in diag.strategic_traps]
        assert any("price" in t.lower() for t in trap_names)

    def test_risk_reward_scenarios(self, mock_result):
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        assert diag.bull_case
        assert diag.bear_case
        assert diag.base_case

    def test_kpi_dashboard(self, mock_result):
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        assert len(diag.kpi_dashboard) > 0
        kpi_names = [k["kpi"] for k in diag.kpi_dashboard]
        assert any("revenue" in k.lower() or "margin" in k.lower() for k in kpi_names)

    def test_verdict_contains_operator(self, mock_result):
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        assert "Vodafone" in diag.one_line_verdict

    def test_net_assessments_populated(self, mock_result):
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        assert diag.trends_net_assessment != ""
        assert diag.market_net_assessment != ""
        assert diag.competition_net_assessment != ""
        assert diag.self_net_assessment != ""
        assert diag.swot_net_assessment != ""
        assert diag.opportunities_net_assessment != ""

    def test_empty_result_diagnosis(self, empty_result):
        computer = StrategicDiagnosisComputer(empty_result)
        diag = computer.compute()
        # Should not crash; returns defaults
        assert isinstance(diag, StrategicDiagnosis)
        assert diag.operator_rank == 0


class TestHelpers:
    def test_to_float_basic(self):
        assert _to_float(42) == 42.0
        assert _to_float("3.5") == 3.5
        assert _to_float(None) == 0.0

    def test_to_float_formatted(self):
        assert _to_float("3,092M") == 3092.0
        assert _to_float("€6,200M") == 6200.0
        assert _to_float("+8.5%") == 8.5

    def test_name_match(self):
        assert _name_match("vodafone_germany", "vodafone_germany")
        assert _name_match("vodafone germany", "vodafone_germany")
        assert not _name_match("dt_germany", "vodafone_germany")
        assert not _name_match("", "vodafone_germany")


# -----------------------------------------------------------------------
# BLMMdGenerator tests
# -----------------------------------------------------------------------

class TestBLMMdGenerator:
    def test_generate_returns_string(self, mock_result):
        gen = BLMMdGenerator()
        md = gen.generate(mock_result)
        assert isinstance(md, str)
        assert len(md) > 500

    def test_generate_has_module_headers(self, mock_result):
        gen = BLMMdGenerator()
        md = gen.generate(mock_result)
        # Check for key module sections
        assert "Executive Summary" in md
        assert "Trends" in md or "PEST" in md
        assert "Market" in md or "Customer" in md
        assert "Competition" in md
        assert "Self Analysis" in md or "Self" in md
        assert "SWOT" in md
        assert "Opportunities" in md or "SPAN" in md

    def test_generate_has_verdict(self, mock_result):
        gen = BLMMdGenerator()
        md = gen.generate(mock_result)
        assert "One-Line Verdict" in md
        assert "Vodafone" in md

    def test_generate_has_central_diagnosis(self, mock_result):
        gen = BLMMdGenerator()
        md = gen.generate(mock_result)
        assert "Central Diagnosis" in md

    def test_generate_has_priorities(self, mock_result):
        gen = BLMMdGenerator()
        md = gen.generate(mock_result)
        assert "Strategic Priorities" in md

    def test_generate_has_provenance(self, mock_result):
        gen = BLMMdGenerator()
        md = gen.generate(mock_result)
        assert "Provenance" in md
        assert "150" in md  # total data points

    def test_generate_writes_file(self, mock_result):
        gen = BLMMdGenerator()
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            path = f.name
        try:
            md = gen.generate(mock_result, output_path=path)
            assert os.path.exists(path)
            content = open(path, encoding="utf-8").read()
            assert "Executive Summary" in content
            assert len(content) > 500
        finally:
            os.unlink(path)

    def test_generate_empty_result(self, empty_result):
        gen = BLMMdGenerator()
        md = gen.generate(empty_result)
        assert isinstance(md, str)
        # Should have at least the document header
        assert "BLM Strategic Assessment" in md

    def test_generate_with_tariff(self, mock_result_with_tariff):
        gen = BLMMdGenerator()
        md = gen.generate(mock_result_with_tariff)
        assert "Tariff" in md
        assert "GigaMobil" in md or "466" in md

    def test_no_tariff_skips_module(self, mock_result):
        gen = BLMMdGenerator()
        md = gen.generate(mock_result)
        # Tariff module comment should exist but content should be empty/missing
        # since tariff_analysis is None
        assert "02a" in md  # Module comment is always added

    def test_toc_present(self, mock_result):
        gen = BLMMdGenerator()
        md = gen.generate(mock_result)
        assert "Document Structure" in md

    def test_line_count_reasonable(self, mock_result):
        gen = BLMMdGenerator()
        md = gen.generate(mock_result)
        lines = md.split("\n")
        # Mock data produces fewer lines than real data, but should be substantial
        assert len(lines) > 200

    def test_markdown_tables_well_formed(self, mock_result):
        gen = BLMMdGenerator()
        md = gen.generate(mock_result)
        # Check that tables have header separators
        lines = md.split("\n")
        table_seps = [l for l in lines if "| :---" in l or "| ---" in l]
        assert len(table_seps) > 5  # Multiple tables

    def test_five_forces_rendered(self, mock_result):
        gen = BLMMdGenerator()
        md = gen.generate(mock_result)
        assert "Five Forces" in md
        assert "existing" in md.lower() or "new entrants" in md.lower()

    def test_swot_quadrants_rendered(self, mock_result):
        gen = BLMMdGenerator()
        md = gen.generate(mock_result)
        assert "Strengths" in md
        assert "Weaknesses" in md
        assert "Opportunities" in md
        assert "Threats" in md

    def test_span_positions_rendered(self, mock_result):
        gen = BLMMdGenerator()
        md = gen.generate(mock_result)
        assert "FibreCo JV" in md
        assert "FMC" in md

    def test_appeals_rendered(self, mock_result):
        gen = BLMMdGenerator()
        md = gen.generate(mock_result)
        assert "APPEALS" in md or "Price" in md
        assert "Performance" in md


# -----------------------------------------------------------------------
# Module renderer isolation tests
# -----------------------------------------------------------------------

class TestModuleRenderers:
    def test_executive_summary_module(self, mock_result):
        from src.output.md_modules.executive_summary import render_executive_summary
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        md = render_executive_summary(mock_result, diag, None)
        assert "Executive Summary" in md
        assert "Verdict" in md

    def test_trends_module(self, mock_result):
        from src.output.md_modules.trends import render_trends
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        md = render_trends(mock_result, diag, None)
        assert "PEST" in md
        assert "mature" in md.lower()

    def test_trends_module_none(self, empty_result):
        from src.output.md_modules.trends import render_trends
        diag = StrategicDiagnosis()
        md = render_trends(empty_result, diag, None)
        assert "Insufficient" in md

    def test_market_customer_module(self, mock_result):
        from src.output.md_modules.market_customer import render_market_customer
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        md = render_market_customer(mock_result, diag, None)
        assert "APPEALS" in md or "Market" in md

    def test_competition_module(self, mock_result):
        from src.output.md_modules.competition import render_competition
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        md = render_competition(mock_result, diag, None)
        assert "Competition" in md
        assert "Deutsche Telekom" in md

    def test_self_analysis_module(self, mock_result):
        from src.output.md_modules.self_analysis import render_self_analysis
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        md = render_self_analysis(mock_result, diag, None)
        assert "Self Analysis" in md
        assert "Vodafone" in md

    def test_swot_module(self, mock_result):
        from src.output.md_modules.swot import render_swot
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        md = render_swot(mock_result, diag, None)
        assert "SWOT" in md
        assert "SO Strategies" in md or "Strategy Matrix" in md

    def test_opportunities_module(self, mock_result):
        from src.output.md_modules.opportunities import render_opportunities
        computer = StrategicDiagnosisComputer(mock_result)
        diag = computer.compute()
        md = render_opportunities(mock_result, diag, None)
        assert "SPAN" in md or "Opportunities" in md

    def test_tariff_module_none(self, mock_result):
        from src.output.md_modules.tariff import render_tariff
        diag = StrategicDiagnosis()
        md = render_tariff(mock_result, diag, None)
        assert md == ""  # Silently skip when no tariff data

    def test_tariff_module_with_data(self, mock_result_with_tariff):
        from src.output.md_modules.tariff import render_tariff
        computer = StrategicDiagnosisComputer(mock_result_with_tariff)
        diag = computer.compute()
        md = render_tariff(mock_result_with_tariff, diag, None)
        assert "Tariff" in md
        assert "466" in md
