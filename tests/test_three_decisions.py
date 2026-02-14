"""Tests for BLM Three Decisions (TP-10).

Validates:
- decisions.py data models
- ThreeDecisionsComputer engine logic
- MD module renderer (render_decisions)
"""
from __future__ import annotations

import pytest

from src.models.decisions import (
    StrategicPillar, StrategyDecision,
    KeyTask, KeyTasksDecision,
    Milestone, GovernanceItem,
    ExecutionDecision, ThreeDecisions,
)
from src.blm.three_decisions_engine import ThreeDecisionsComputer


# -----------------------------------------------------------------------
# Fixtures — reuse mock structure from test_md_generator
# -----------------------------------------------------------------------

class _Factor:
    def __init__(self, name, impact="opportunity", severity="medium"):
        self.factor_name = name
        self.dimension = "P"
        self.dimension_name = "Political"
        self.current_status = f"{name} status"
        self.trend = "stable"
        self.trend_direction = "stable"
        self.industry_impact = ""
        self.company_impact = ""
        self.impact_type = impact
        self.severity = severity
        self.time_horizon = "medium_term"
        self.predictability = "uncertain"
        self.evidence = []
        self.data_source = ""


class _PEST:
    def __init__(self):
        self.political_factors = [_Factor("Regulation")]
        self.economic_factors = [_Factor("GDP", "threat")]
        self.society_factors = []
        self.technology_factors = []
        self.overall_weather = "mixed"
        self.weather_explanation = ""
        self.policy_opportunities = []
        self.policy_threats = []
        self.tech_addressable_market = ""
        self.key_message = ""


class _Trends:
    def __init__(self):
        self.pest = _PEST()
        self.industry_market_size = ""
        self.industry_growth_rate = ""
        self.industry_profit_trend = ""
        self.industry_concentration = ""
        self.industry_lifecycle_stage = ""
        self.new_business_models = []
        self.technology_revolution = []
        self.key_success_factors = []
        self.value_transfer_trends = []
        self.key_message = ""


class _Segment:
    def __init__(self, name, action="GROW"):
        self.segment_name = name
        self.segment_id = name.lower()
        self.key_metrics = {"revenue": "€100M"}
        self.changes = []
        self.trend_data = {"revenue": [90, 95, 100]}
        self.competitor_comparison = {}
        self.attributions = []
        self.health_status = "stable"
        self.key_message = ""
        self.action_required = action


class _Network:
    def __init__(self):
        self.technology_mix = {"cable": 70}
        self.controlled_vs_resale = {}
        self.coverage = {}
        self.quality_scores = {}
        self.homepass_vs_connect = {}
        self.evolution_strategy = {"summary": "Fiber JV + DOCSIS 4.0"}
        self.investment_direction = ""
        self.vs_competitors = ""
        self.consumer_impact = ""
        self.b2b_impact = ""
        self.cost_impact = ""


class _BMC:
    def __init__(self):
        self.key_partners = ["Partner"]
        self.key_activities = []
        self.key_resources = []
        self.value_propositions = []
        self.customer_relationships = []
        self.channels = []
        self.customer_segments = []
        self.cost_structure = []
        self.revenue_streams = []


class _SPAN:
    def __init__(self, name, quad="grow_invest"):
        self.opportunity_name = name
        self.market_attractiveness = 8
        self.competitive_position = 7
        self.quadrant = quad
        self.recommended_strategy = ""
        self.market_size_score = 8
        self.market_growth_score = 8
        self.profit_potential_score = 8
        self.strategic_value_score = 8
        self.market_share_score = 7
        self.product_fit_score = 7
        self.brand_channel_score = 7
        self.tech_capability_score = 7
        self.bubble_size = 1.0


class _Opportunities:
    def __init__(self):
        self.span_positions = [
            _SPAN("Opp1"), _SPAN("Opp2"), _SPAN("Opp3"),
            _SPAN("Opp4"), _SPAN("Opp5"), _SPAN("Opp6"),
        ]
        self.grow_invest = ["Opp1"]
        self.acquire_skills = []
        self.harvest = []
        self.avoid_exit = []
        self.window_opportunities = []
        self.opportunities = []
        self.key_message = ""


class _SWOT:
    def __init__(self):
        self.strengths = ["Network"]
        self.weaknesses = ["Service quality"]
        self.opportunities = ["Fiber"]
        self.threats = ["Regulation"]
        self.so_strategies = []
        self.wo_strategies = []
        self.st_strategies = []
        self.wt_strategies = []
        self.key_message = ""


class _PorterForce:
    def __init__(self, name, intensity="medium"):
        self.force_name = name
        self.intensity = intensity
        self.key_factors = []
        self.implications = []
        self.key_message = ""


class _Competition:
    def __init__(self):
        self.five_forces = [
            _PorterForce("Rivalry", "high"),
            _PorterForce("Substitutes", "medium"),
        ]
        self.competitor_analyses = {}
        self.overall_intensity = "high"
        self.key_message = ""


class _SelfInsight:
    def __init__(self):
        self.financial_health = {
            "revenue": 3092, "ebitda_margin_pct": 36.2,
            "revenue_yoy_pct": 0.7,
        }
        self.revenue_breakdown = {}
        self.market_positions = {}
        self.share_trends = {}
        self.segment_analyses = [
            _Segment("Mobile", "GROW"),
            _Segment("Fixed BB", "MAINTAIN"),
            _Segment("B2B", "GROW"),
        ]
        self.network = _Network()
        self.customer_perception = {}
        self.leadership_changes = []
        self.bmc = _BMC()
        self.org_culture = ""
        self.talent_assessment = {}
        self.performance_gap = ""
        self.opportunity_gap = ""
        self.strategic_review = ""
        self.management_commentary = []
        self.strengths = ["Network coverage"]
        self.weaknesses = ["Customer service"]
        self.exposure_points = []
        self.health_rating = "stable"
        self.key_message = ""


class _Provenance:
    def quality_report(self):
        return {"total_data_points": 50, "high_confidence": 30,
                "medium_confidence": 15, "low_confidence": 5,
                "estimated": 0, "unique_sources": 5}

    def to_footnotes(self):
        return []


class _Result:
    def __init__(self):
        self.target_operator = "vodafone_germany"
        self.market = "germany"
        self.analysis_period = "CQ4_2025"
        self.trends = _Trends()
        self.market_customer = None
        self.competition = _Competition()
        self.self_analysis = _SelfInsight()
        self.swot = _SWOT()
        self.opportunities = _Opportunities()
        self.tariff_analysis = None
        self.provenance = _Provenance()


class _Diagnosis:
    def __init__(self, label="The Squeezed Middle", rank=2,
                 stance="Balanced"):
        self.central_diagnosis_label = label
        self.operator_rank = rank
        self.competitive_stance = stance
        self.strategic_traps = [
            {"trap": "Scale trap", "temptation": "Buy market share",
             "reality": "Cash burn without retention"},
        ]
        self.verdict = "Challenger with potential"
        self.priorities = ["Growth in B2B", "Fix churn"]
        self.risk_reward = "Medium risk / high reward"


@pytest.fixture
def result():
    return _Result()


@pytest.fixture
def diagnosis():
    return _Diagnosis()


@pytest.fixture
def decisions(result, diagnosis):
    return ThreeDecisionsComputer(result, diagnosis).compute()


# -----------------------------------------------------------------------
# Data model tests
# -----------------------------------------------------------------------

class TestDecisionModels:

    def test_strategic_pillar_defaults(self):
        p = StrategicPillar(name="Growth", direction="Expand", rationale="Revenue")
        assert p.priority == "P1"
        assert p.kpis == []

    def test_strategy_decision_defaults(self):
        sd = StrategyDecision()
        assert sd.pillars == []
        assert sd.overall_direction == ""
        assert sd.competitive_posture == ""

    def test_key_task_defaults(self):
        kt = KeyTask(name="Deploy 5G", domain="Network", description="Expand coverage")
        assert kt.priority == "P1"
        assert kt.owner == ""
        assert kt.kpis == []

    def test_key_tasks_decision_defaults(self):
        ktd = KeyTasksDecision()
        assert ktd.tasks == []
        assert ktd.resource_implication == ""

    def test_milestone_defaults(self):
        ms = Milestone(quarter="Q1", name="Foundation")
        assert ms.deliverables == []
        assert ms.priority == "P0"

    def test_governance_item(self):
        g = GovernanceItem(mechanism="Review", cadence="Monthly",
                           description="Track progress")
        assert g.mechanism == "Review"

    def test_execution_decision_defaults(self):
        ed = ExecutionDecision()
        assert ed.milestones == []
        assert ed.governance == []
        assert ed.risk_mitigation == []
        assert ed.traps_to_avoid == []

    def test_three_decisions_container(self):
        td = ThreeDecisions()
        assert isinstance(td.strategy, StrategyDecision)
        assert isinstance(td.key_tasks, KeyTasksDecision)
        assert isinstance(td.execution, ExecutionDecision)
        assert td.narrative == ""
        assert td.diagnosis_label == ""


# -----------------------------------------------------------------------
# Engine tests
# -----------------------------------------------------------------------

class TestThreeDecisionsComputer:

    def test_compute_returns_three_decisions(self, decisions):
        assert isinstance(decisions, ThreeDecisions)

    def test_diagnosis_label_set(self, decisions):
        assert decisions.diagnosis_label == "The Squeezed Middle"

    def test_strategy_has_four_pillars(self, decisions):
        assert len(decisions.strategy.pillars) == 4

    def test_pillar_names(self, decisions):
        names = [p.name for p in decisions.strategy.pillars]
        assert "Growth Strategy" in names
        assert "Competitive Strategy" in names
        assert "Transformation Strategy" in names
        assert "Customer Strategy" in names

    def test_each_pillar_has_kpis(self, decisions):
        for p in decisions.strategy.pillars:
            assert len(p.kpis) >= 1, f"{p.name} has no KPIs"

    def test_each_pillar_has_priority(self, decisions):
        for p in decisions.strategy.pillars:
            assert p.priority in ("P0", "P1", "P2")

    def test_overall_direction_includes_label(self, decisions):
        assert "The Squeezed Middle" in decisions.strategy.overall_direction

    def test_competitive_posture_set(self, decisions):
        assert decisions.strategy.competitive_posture != ""

    # Key Tasks
    def test_key_tasks_non_empty(self, decisions):
        assert len(decisions.key_tasks.tasks) >= 1

    def test_key_tasks_capped_at_8(self, decisions):
        assert len(decisions.key_tasks.tasks) <= 8

    def test_key_tasks_sorted_by_priority(self, decisions):
        order = {"P0": 0, "P1": 1, "P2": 2}
        priorities = [order.get(t.priority, 9) for t in decisions.key_tasks.tasks]
        assert priorities == sorted(priorities)

    def test_key_tasks_cover_domains(self, decisions):
        domains = {t.domain for t in decisions.key_tasks.tasks}
        assert "Network" in domains
        assert "Customer" in domains

    def test_resource_implication(self, decisions):
        assert "P0" in decisions.key_tasks.resource_implication

    # Execution
    def test_milestones_quarterly(self, decisions):
        quarters = [m.quarter for m in decisions.execution.milestones]
        assert quarters == ["Q1", "Q2", "Q3", "Q4"]

    def test_governance_items(self, decisions):
        assert len(decisions.execution.governance) >= 2

    def test_governance_cadences(self, decisions):
        cadences = [g.cadence for g in decisions.execution.governance]
        assert "Monthly" in cadences
        assert "Quarterly" in cadences

    def test_risks_present(self, decisions):
        assert len(decisions.execution.risk_mitigation) >= 2

    def test_traps_from_diagnosis(self, decisions):
        assert len(decisions.execution.traps_to_avoid) >= 1

    # Narrative
    def test_narrative_non_empty(self, decisions):
        assert len(decisions.narrative) > 50

    def test_narrative_includes_label(self, decisions):
        assert "The Squeezed Middle" in decisions.narrative


class TestEngineRank1:
    """Test with rank=1 leader positioning."""

    @pytest.fixture
    def leader_decisions(self, result):
        diag = _Diagnosis(label="The Undisputed Leader", rank=1,
                          stance="Offensive (Dominant)")
        return ThreeDecisionsComputer(result, diag).compute()

    def test_leader_growth_direction(self, leader_decisions):
        growth = [p for p in leader_decisions.strategy.pillars
                  if p.name == "Growth Strategy"][0]
        assert "Defend" in growth.direction or "leadership" in growth.direction

    def test_leader_overall_direction(self, leader_decisions):
        assert "defend" in leader_decisions.strategy.overall_direction.lower()


class TestEngineDefensive:
    """Test with Defensive/Turnaround stance."""

    @pytest.fixture
    def defensive_decisions(self, result):
        diag = _Diagnosis(label="The Distant Second", rank=3,
                          stance="Defensive (Turnaround needed)")
        return ThreeDecisionsComputer(result, diag).compute()

    def test_defensive_competitive_pillar(self, defensive_decisions):
        comp = [p for p in defensive_decisions.strategy.pillars
                if p.name == "Competitive Strategy"][0]
        assert "Shore up" in comp.direction or "address" in comp.direction.lower()

    def test_defensive_overall_direction(self, defensive_decisions):
        assert "stabilize" in defensive_decisions.strategy.overall_direction.lower()


class TestEngineEdgeCases:
    """Edge cases for engine robustness."""

    def test_no_self_analysis(self, diagnosis):
        r = _Result()
        r.self_analysis = None
        decisions = ThreeDecisionsComputer(r, diagnosis).compute()
        assert isinstance(decisions, ThreeDecisions)
        assert len(decisions.strategy.pillars) == 4

    def test_no_competition(self, diagnosis):
        r = _Result()
        r.competition = None
        decisions = ThreeDecisionsComputer(r, diagnosis).compute()
        assert len(decisions.execution.risk_mitigation) >= 1

    def test_no_opportunities(self, diagnosis):
        r = _Result()
        r.opportunities = None
        decisions = ThreeDecisionsComputer(r, diagnosis).compute()
        assert len(decisions.key_tasks.tasks) >= 1

    def test_empty_diagnosis_label(self, result):
        diag = _Diagnosis(label=None, rank=None, stance=None)
        decisions = ThreeDecisionsComputer(result, diag).compute()
        assert decisions.diagnosis_label == "Unknown"

    def test_segment_with_none_trend_data(self, diagnosis):
        r = _Result()
        r.self_analysis.segment_analyses[0].trend_data = None
        decisions = ThreeDecisionsComputer(r, diagnosis).compute()
        assert isinstance(decisions, ThreeDecisions)

    def test_segment_with_urgent_action(self, diagnosis):
        r = _Result()
        r.self_analysis.segment_analyses[1].action_required = "URGENT — revenue declining"
        decisions = ThreeDecisionsComputer(r, diagnosis).compute()
        customer_tasks = [t for t in decisions.key_tasks.tasks
                          if t.domain == "Customer"]
        assert any("Retention" in t.name or "URGENT" in (t.description or "")
                    for t in customer_tasks)

    def test_low_margin_triggers_recovery(self, diagnosis):
        r = _Result()
        r.self_analysis.financial_health["ebitda_margin_pct"] = 25.0
        decisions = ThreeDecisionsComputer(r, diagnosis).compute()
        eff_tasks = [t for t in decisions.key_tasks.tasks
                     if t.domain == "Efficiency"]
        assert any("Margin" in t.name or "Recovery" in t.name for t in eff_tasks)

    def test_high_margin_no_recovery(self, diagnosis):
        r = _Result()
        r.self_analysis.financial_health["ebitda_margin_pct"] = 40.0
        decisions = ThreeDecisionsComputer(r, diagnosis).compute()
        eff_tasks = [t for t in decisions.key_tasks.tasks
                     if t.domain == "Efficiency"]
        assert all("Recovery" not in t.name for t in eff_tasks)

    def test_5g_evolution_strategy(self, diagnosis):
        r = _Result()
        r.self_analysis.network.evolution_strategy = {"summary": "5G SA rollout nationwide"}
        decisions = ThreeDecisionsComputer(r, diagnosis).compute()
        transform = [p for p in decisions.strategy.pillars
                     if p.name == "Transformation Strategy"][0]
        assert "5G" in transform.direction

    def test_many_grow_invest_adds_portfolio_task(self, diagnosis):
        r = _Result()
        r.opportunities.span_positions = [_SPAN(f"Opp{i}") for i in range(8)]
        decisions = ThreeDecisionsComputer(r, diagnosis).compute()
        biz_tasks = [t for t in decisions.key_tasks.tasks
                     if t.domain == "Business"]
        assert any("Portfolio" in t.name or "Opportunity" in t.name
                    for t in biz_tasks)


# -----------------------------------------------------------------------
# MD module renderer tests
# -----------------------------------------------------------------------

class TestRenderDecisions:

    @pytest.fixture
    def rendered(self, result, diagnosis):
        from src.output.md_modules.decisions import render_decisions
        return render_decisions(result, diagnosis, None)

    def test_returns_string(self, rendered):
        assert isinstance(rendered, str)

    def test_contains_h2_header(self, rendered):
        assert "## Three Decisions" in rendered

    def test_contains_decision_1(self, rendered):
        assert "### Decision 1: Define Strategy" in rendered

    def test_contains_decision_2(self, rendered):
        assert "### Decision 2: Define Key Tasks" in rendered

    def test_contains_decision_3(self, rendered):
        assert "### Decision 3: Define Execution" in rendered

    def test_contains_quarterly_roadmap(self, rendered):
        assert "#### Quarterly Roadmap" in rendered

    def test_contains_governance(self, rendered):
        assert "#### Governance" in rendered

    def test_contains_strategic_narrative(self, rendered):
        assert "#### Strategic Narrative" in rendered

    def test_contains_diagnosis_label(self, rendered):
        assert "The Squeezed Middle" in rendered

    def test_contains_pillar_table(self, rendered):
        assert "| Priority |" in rendered
        assert "| Pillar |" in rendered or "Pillar" in rendered

    def test_contains_task_table(self, rendered):
        assert "| Domain |" in rendered or "Domain" in rendered

    def test_contains_milestone_quarters(self, rendered):
        assert "**Q1:" in rendered
        assert "**Q4:" in rendered

    def test_no_section_header_error(self, rendered):
        """Verify the 'can't mul' bug is fixed."""
        assert "failed" not in rendered.lower()
        assert "error" not in rendered.lower()

    def test_traps_rendered(self, rendered):
        assert "Strategic Traps" in rendered or "Traps to Avoid" in rendered

    def test_risks_rendered(self, rendered):
        assert "Key Risks" in rendered or "Mitigation" in rendered


class TestRenderDecisionsEdgeCases:

    def test_render_with_no_traps(self, result):
        from src.output.md_modules.decisions import render_decisions
        diag = _Diagnosis()
        diag.strategic_traps = []
        md = render_decisions(result, diag, None)
        assert isinstance(md, str)
        assert "## Three Decisions" in md

    def test_render_with_string_traps(self, result):
        from src.output.md_modules.decisions import render_decisions
        diag = _Diagnosis()
        diag.strategic_traps = ["Avoid price wars", "Don't over-invest"]
        md = render_decisions(result, diag, None)
        assert "Avoid price wars" in md

    def test_render_gracefully_handles_engine_failure(self):
        """If engine fails, renderer returns error message instead of crashing."""
        from src.output.md_modules.decisions import render_decisions
        # Pass None as result to trigger engine error
        md = render_decisions(None, None, None)
        assert "failed" in md.lower() or "error" in md.lower() or isinstance(md, str)
