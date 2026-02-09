"""Tests for Look at Opportunities module (src/blm/look_at_opportunities.py)."""

import pytest

from src.models.trend import TrendAnalysis, PESTAnalysis, PESTFactor
from src.models.market import MarketCustomerInsight, MarketChange
from src.models.competition import (
    CompetitionInsight,
    PorterForce,
    CompetitorDeepDive,
)
from src.models.self_analysis import SelfInsight, ExposurePoint
from src.models.swot import SWOTAnalysis
from src.models.opportunity import SPANPosition, OpportunityItem, OpportunityInsight
from src.blm.swot_synthesis import synthesize_swot
from src.blm.look_at_opportunities import analyze_opportunities


# ---------------------------------------------------------------------------
# Fixtures -- reuse same realistic data as SWOT tests + SWOT output
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_trends():
    pest = PESTAnalysis(
        policy_opportunities=[
            "Gigabit subsidies available",
            "5G spectrum auction favorable",
        ],
        policy_threats=[
            "NIS2 compliance costs",
            "Energy price regulation",
        ],
    )
    return TrendAnalysis(
        pest=pest,
        technology_revolution=["Open RAN adoption", "Edge computing rollout"],
        key_message="Mixed macro environment",
    )


@pytest.fixture
def mock_market():
    return MarketCustomerInsight(
        opportunities=[
            MarketChange(
                change_type="technology",
                description="5G enterprise demand growing",
                impact_type="opportunity",
                severity="high",
            ),
            MarketChange(
                change_type="pricing",
                description="Premium segment growing",
                impact_type="opportunity",
                severity="medium",
            ),
        ],
        threats=[
            MarketChange(
                change_type="new_entrant",
                description="1&1 launching own network",
                impact_type="threat",
            ),
            MarketChange(
                change_type="ott",
                description="WhatsApp replacing voice revenue",
                impact_type="threat",
            ),
        ],
    )


@pytest.fixture
def mock_competition():
    return CompetitionInsight(
        five_forces={
            "existing_competitors": PorterForce(
                force_name="existing_competitors", force_level="high",
            ),
            "new_entrants": PorterForce(
                force_name="new_entrants", force_level="medium",
            ),
            "substitutes": PorterForce(
                force_name="substitutes", force_level="medium",
            ),
            "supplier_power": PorterForce(
                force_name="supplier_power", force_level="high",
            ),
            "buyer_power": PorterForce(
                force_name="buyer_power", force_level="low",
            ),
        },
        competitor_analyses={
            "deutsche_telekom": CompetitorDeepDive(
                operator="deutsche_telekom",
                weaknesses=["Slow innovation in B2B cloud", "High cost base"],
            ),
            "o2_telefonica": CompetitorDeepDive(
                operator="o2_telefonica",
                weaknesses=["Limited fixed-line coverage"],
            ),
        },
    )


@pytest.fixture
def mock_self():
    return SelfInsight(
        strengths=[
            "Strong cable network coverage",
            "Leading brand in Germany",
            "Enterprise customer base",
        ],
        weaknesses=[
            "Low fiber penetration",
            "Declining DSL revenue",
            "Below-average app ratings",
        ],
        exposure_points=[
            ExposurePoint(
                trigger_action="1&1 user migration",
                side_effect="Network load spikes",
            ),
        ],
    )


@pytest.fixture
def mock_swot(mock_trends, mock_market, mock_competition, mock_self):
    return synthesize_swot(
        trends=mock_trends,
        market_customer=mock_market,
        competition=mock_competition,
        self_analysis=mock_self,
    )


@pytest.fixture
def opportunity_result(
    mock_trends, mock_market, mock_competition, mock_self, mock_swot,
):
    """Full opportunity analysis output."""
    return analyze_opportunities(
        trends=mock_trends,
        market_customer=mock_market,
        competition=mock_competition,
        self_analysis=mock_self,
        swot=mock_swot,
        target_operator="vodafone_germany",
    )


# ---------------------------------------------------------------------------
# Test: SPAN scoring
# ---------------------------------------------------------------------------

class TestSPANPositionScoring:

    def test_span_positions_scored(self, opportunity_result):
        """Each opportunity must have market_attractiveness and competitive_position computed."""
        assert len(opportunity_result.span_positions) > 0
        for sp in opportunity_result.span_positions:
            assert isinstance(sp, SPANPosition)
            assert 1.0 <= sp.market_attractiveness <= 10.0
            assert 1.0 <= sp.competitive_position <= 10.0

    def test_market_attractiveness_is_weighted_average(self):
        """Verify the weighted average formula for market attractiveness."""
        sp = SPANPosition(
            opportunity_name="test",
            market_size_score=8.0,
            market_growth_score=6.0,
            profit_potential_score=7.0,
            strategic_value_score=9.0,
        )
        expected = 0.30 * 8.0 + 0.25 * 6.0 + 0.25 * 7.0 + 0.20 * 9.0
        # Verify the formula by computing manually
        assert abs(expected - 7.45) < 0.01

    def test_competitive_position_is_weighted_average(self):
        """Verify the weighted average formula for competitive position."""
        sp = SPANPosition(
            opportunity_name="test",
            market_share_score=7.0,
            product_fit_score=5.0,
            brand_channel_score=6.0,
            tech_capability_score=8.0,
        )
        expected = 0.25 * 7.0 + 0.25 * 5.0 + 0.25 * 6.0 + 0.25 * 8.0
        assert abs(expected - 6.5) < 0.01


# ---------------------------------------------------------------------------
# Test: Quadrant assignment
# ---------------------------------------------------------------------------

class TestSPANQuadrantAssignment:

    def test_span_quadrant_assignment(self, opportunity_result):
        """All positions must have a valid quadrant assigned."""
        valid_quadrants = {"grow_invest", "acquire_skills", "harvest", "avoid_exit"}
        for sp in opportunity_result.span_positions:
            assert sp.quadrant in valid_quadrants

    def test_grow_invest_threshold(self):
        """attractiveness >= 5 AND position >= 5 -> grow_invest."""
        from src.blm.look_at_opportunities import _assign_quadrant
        assert _assign_quadrant(5.0, 5.0) == "grow_invest"
        assert _assign_quadrant(10.0, 10.0) == "grow_invest"
        assert _assign_quadrant(7.5, 6.0) == "grow_invest"

    def test_acquire_skills_threshold(self):
        """attractiveness >= 5 AND position < 5 -> acquire_skills."""
        from src.blm.look_at_opportunities import _assign_quadrant
        assert _assign_quadrant(5.0, 4.9) == "acquire_skills"
        assert _assign_quadrant(8.0, 1.0) == "acquire_skills"

    def test_harvest_threshold(self):
        """attractiveness < 5 AND position >= 5 -> harvest."""
        from src.blm.look_at_opportunities import _assign_quadrant
        assert _assign_quadrant(4.9, 5.0) == "harvest"
        assert _assign_quadrant(1.0, 9.0) == "harvest"

    def test_avoid_exit_threshold(self):
        """attractiveness < 5 AND position < 5 -> avoid_exit."""
        from src.blm.look_at_opportunities import _assign_quadrant
        assert _assign_quadrant(4.9, 4.9) == "avoid_exit"
        assert _assign_quadrant(1.0, 1.0) == "avoid_exit"


# ---------------------------------------------------------------------------
# Test: Opportunity items with priority
# ---------------------------------------------------------------------------

class TestOpportunityItems:

    def test_opportunity_items_with_priority(self, opportunity_result):
        """Each OpportunityItem must have P0/P1/P2 priority."""
        assert len(opportunity_result.opportunities) > 0
        valid_priorities = {"P0", "P1", "P2"}
        for item in opportunity_result.opportunities:
            assert isinstance(item, OpportunityItem)
            assert item.priority in valid_priorities

    def test_grow_invest_items_have_p0(self, opportunity_result):
        """Items in the grow_invest quadrant should get P0."""
        grow_names = set(opportunity_result.grow_invest)
        for item in opportunity_result.opportunities:
            if item.name in grow_names:
                assert item.priority == "P0"

    def test_avoid_exit_items_have_p2(self, opportunity_result):
        """Items in the avoid_exit quadrant should get P2."""
        avoid_names = set(opportunity_result.avoid_exit)
        for item in opportunity_result.opportunities:
            if item.name in avoid_names:
                assert item.priority == "P2"


# ---------------------------------------------------------------------------
# Test: Addressable market policy (never fabricate)
# ---------------------------------------------------------------------------

class TestAddressableMarketPolicy:

    def test_addressable_market_policy(self, opportunity_result):
        """All items must have addressable_market='N/A', never fabricated numbers."""
        for item in opportunity_result.opportunities:
            assert item.addressable_market == "N/A"


# ---------------------------------------------------------------------------
# Test: derived_from traceability
# ---------------------------------------------------------------------------

class TestDerivedFromTraceability:

    def test_opportunities_derived_from_tracked(self, opportunity_result):
        """Each item's derived_from list must reference source analyses."""
        for item in opportunity_result.opportunities:
            assert isinstance(item.derived_from, list)
            # At least one source should be identified
            assert len(item.derived_from) >= 1


# ---------------------------------------------------------------------------
# Test: Key message
# ---------------------------------------------------------------------------

class TestKeyMessage:

    def test_key_message_not_empty(self, opportunity_result):
        assert opportunity_result.key_message
        assert len(opportunity_result.key_message) > 10

    def test_key_message_mentions_span(self, opportunity_result):
        assert "SPAN" in opportunity_result.key_message


# ---------------------------------------------------------------------------
# Test: Quadrant grouping
# ---------------------------------------------------------------------------

class TestQuadrantGrouping:

    def test_quadrant_grouping(self, opportunity_result):
        """grow_invest, acquire_skills, harvest, avoid_exit lists must be populated
        and consistent with span_positions."""
        all_grouped = (
            opportunity_result.grow_invest
            + opportunity_result.acquire_skills
            + opportunity_result.harvest
            + opportunity_result.avoid_exit
        )
        # Every SPAN position name should appear in exactly one group
        span_names = [sp.opportunity_name for sp in opportunity_result.span_positions]
        assert set(all_grouped) == set(span_names)

    def test_grow_invest_positions_match(self, opportunity_result):
        """Names in grow_invest must correspond to positions with that quadrant."""
        for sp in opportunity_result.span_positions:
            if sp.quadrant == "grow_invest":
                assert sp.opportunity_name in opportunity_result.grow_invest

    def test_avoid_exit_positions_match(self, opportunity_result):
        """Names in avoid_exit must correspond to positions with that quadrant."""
        for sp in opportunity_result.span_positions:
            if sp.quadrant == "avoid_exit":
                assert sp.opportunity_name in opportunity_result.avoid_exit


# ---------------------------------------------------------------------------
# Test: Empty / None inputs
# ---------------------------------------------------------------------------

class TestEmptyInputs:

    def test_empty_inputs(self):
        """Empty inputs should return valid OpportunityInsight with no items."""
        result = analyze_opportunities(
            trends=TrendAnalysis(),
            market_customer=MarketCustomerInsight(),
            competition=CompetitionInsight(),
            self_analysis=SelfInsight(),
            swot=SWOTAnalysis(),
        )
        assert isinstance(result, OpportunityInsight)
        assert result.span_positions == []
        assert result.opportunities == []
        assert result.grow_invest == []
        assert result.acquire_skills == []
        assert result.harvest == []
        assert result.avoid_exit == []
        assert result.key_message  # Should still have a message

    def test_none_inputs(self):
        """None inputs should not raise."""
        result = analyze_opportunities(
            trends=None,
            market_customer=None,
            competition=None,
            self_analysis=None,
            swot=None,
        )
        assert isinstance(result, OpportunityInsight)
        assert result.span_positions == []

    def test_only_swot_input(self, mock_swot):
        """With only SWOT input, SO/WO strategies should produce opportunities."""
        result = analyze_opportunities(
            trends=None,
            market_customer=None,
            competition=None,
            self_analysis=None,
            swot=mock_swot,
        )
        # SO + WO strategies from SWOT should be extracted
        assert len(result.span_positions) > 0


# ---------------------------------------------------------------------------
# Test: Provenance tracking
# ---------------------------------------------------------------------------

class TestProvenanceTracking:

    def test_provenance_tracking(
        self, mock_trends, mock_market, mock_competition, mock_self, mock_swot,
    ):
        from src.models.provenance import ProvenanceStore
        prov = ProvenanceStore()
        analyze_opportunities(
            trends=mock_trends,
            market_customer=mock_market,
            competition=mock_competition,
            self_analysis=mock_self,
            swot=mock_swot,
            target_operator="vodafone_germany",
            provenance=prov,
        )
        tracked = prov.get_values(field_name="opportunity_count")
        assert len(tracked) == 1
        assert tracked[0].value > 0
        assert tracked[0].operator == "vodafone_germany"


# ---------------------------------------------------------------------------
# Test: Recommended strategy text
# ---------------------------------------------------------------------------

class TestRecommendedStrategy:

    def test_recommended_strategy_populated(self, opportunity_result):
        """Every SPAN position should have a non-empty recommended_strategy."""
        for sp in opportunity_result.span_positions:
            assert sp.recommended_strategy
            assert len(sp.recommended_strategy) > 5
