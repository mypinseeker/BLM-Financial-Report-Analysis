"""Tests for SWOT Synthesis module (src/blm/swot_synthesis.py)."""

import pytest

from src.models.trend import TrendAnalysis, PESTAnalysis, PESTFactor
from src.models.market import MarketCustomerInsight, MarketChange
from src.models.competition import CompetitionInsight, PorterForce
from src.models.self_analysis import SelfInsight, ExposurePoint
from src.models.swot import SWOTAnalysis
from src.blm.swot_synthesis import synthesize_swot


# ---------------------------------------------------------------------------
# Fixtures with realistic German telecom data
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
    return TrendAnalysis(pest=pest, key_message="Mixed macro environment")


@pytest.fixture
def mock_market():
    return MarketCustomerInsight(
        opportunities=[
            MarketChange(
                change_type="technology",
                description="5G enterprise demand growing",
                impact_type="opportunity",
            ),
            MarketChange(
                change_type="pricing",
                description="Premium segment growing",
                impact_type="opportunity",
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
def swot_result(mock_trends, mock_market, mock_competition, mock_self):
    """Convenience fixture providing the synthesized SWOT."""
    return synthesize_swot(
        trends=mock_trends,
        market_customer=mock_market,
        competition=mock_competition,
        self_analysis=mock_self,
    )


# ---------------------------------------------------------------------------
# Test: Strengths extraction
# ---------------------------------------------------------------------------

class TestSWOTStrengths:

    def test_swot_extracts_strengths(self, swot_result, mock_self):
        """S list must match self_analysis.strengths exactly."""
        assert swot_result.strengths == mock_self.strengths

    def test_strengths_count(self, swot_result):
        assert len(swot_result.strengths) == 3


# ---------------------------------------------------------------------------
# Test: Weaknesses extraction (includes exposure points)
# ---------------------------------------------------------------------------

class TestSWOTWeaknesses:

    def test_swot_extracts_weaknesses_with_exposures(self, swot_result, mock_self):
        """W must include weaknesses AND exposure point side_effects."""
        for w in mock_self.weaknesses:
            assert w in swot_result.weaknesses
        # Exposure point side_effect should also appear
        assert "Network load spikes" in swot_result.weaknesses

    def test_weakness_count(self, swot_result):
        # 3 weaknesses + 1 exposure point side_effect
        assert len(swot_result.weaknesses) == 4


# ---------------------------------------------------------------------------
# Test: Opportunities extraction
# ---------------------------------------------------------------------------

class TestSWOTOpportunities:

    def test_swot_extracts_opportunities(self, swot_result):
        """O must include both policy opportunities and market opportunities."""
        descs = swot_result.opportunities
        assert "Gigabit subsidies available" in descs
        assert "5G spectrum auction favorable" in descs
        assert "5G enterprise demand growing" in descs
        assert "Premium segment growing" in descs

    def test_opportunity_count(self, swot_result):
        # 2 policy + 2 market
        assert len(swot_result.opportunities) == 4


# ---------------------------------------------------------------------------
# Test: Threats extraction
# ---------------------------------------------------------------------------

class TestSWOTThreats:

    def test_swot_extracts_threats(self, swot_result):
        """T must include trend threats, market threats, and high-force competition pressures."""
        descs = swot_result.threats
        # Trend-derived threats
        assert "NIS2 compliance costs" in descs
        assert "Energy price regulation" in descs
        # Market-derived threats
        assert "1&1 launching own network" in descs
        assert "WhatsApp replacing voice revenue" in descs
        # Competition-derived (only "high" forces qualify)
        assert "High existing competitors pressure" in descs
        assert "High supplier power pressure" in descs

    def test_medium_force_not_in_threats(self, swot_result):
        """Forces at medium or low level should NOT appear in threats."""
        descs = swot_result.threats
        assert "High new entrants pressure" not in descs
        assert "High substitutes pressure" not in descs
        assert "High buyer power pressure" not in descs

    def test_threat_count(self, swot_result):
        # 2 trend + 2 market + 2 competition (high only)
        assert len(swot_result.threats) == 6


# ---------------------------------------------------------------------------
# Test: Strategy generation
# ---------------------------------------------------------------------------

class TestSWOTStrategies:

    def test_so_strategies_generated(self, swot_result):
        """so_strategies must be non-empty (2-4 items)."""
        assert len(swot_result.so_strategies) >= 2
        assert len(swot_result.so_strategies) <= 4

    def test_wo_strategies_generated(self, swot_result):
        """wo_strategies must be non-empty (2-4 items)."""
        assert len(swot_result.wo_strategies) >= 2
        assert len(swot_result.wo_strategies) <= 4

    def test_st_strategies_generated(self, swot_result):
        """st_strategies must be non-empty (2-4 items)."""
        assert len(swot_result.st_strategies) >= 2
        assert len(swot_result.st_strategies) <= 4

    def test_wt_strategies_generated(self, swot_result):
        """wt_strategies must be non-empty (2-4 items)."""
        assert len(swot_result.wt_strategies) >= 2
        assert len(swot_result.wt_strategies) <= 4

    def test_so_strategies_reference_strengths_and_opportunities(self, swot_result):
        """Each SO strategy should reference a strength and an opportunity."""
        for strat in swot_result.so_strategies:
            assert "Leverage" in strat or "capture" in strat

    def test_wt_strategies_reference_weaknesses_and_threats(self, swot_result):
        """Each WT strategy should reference a weakness and a threat."""
        for strat in swot_result.wt_strategies:
            assert "Mitigate" in strat or "defend" in strat


# ---------------------------------------------------------------------------
# Test: Key message
# ---------------------------------------------------------------------------

class TestSWOTKeyMessage:

    def test_key_message_not_empty(self, swot_result):
        assert swot_result.key_message
        assert len(swot_result.key_message) > 10

    def test_key_message_contains_counts(self, swot_result):
        assert "3 strengths" in swot_result.key_message
        assert "4 weaknesses" in swot_result.key_message
        assert "4 opportunities" in swot_result.key_message
        assert "6 threats" in swot_result.key_message


# ---------------------------------------------------------------------------
# Test: Empty / None inputs
# ---------------------------------------------------------------------------

class TestSWOTEmptyInputs:

    def test_empty_inputs(self):
        """All empty inputs should return a valid SWOTAnalysis with empty lists."""
        result = synthesize_swot(
            trends=TrendAnalysis(),
            market_customer=MarketCustomerInsight(),
            competition=CompetitionInsight(),
            self_analysis=SelfInsight(),
        )
        assert isinstance(result, SWOTAnalysis)
        assert result.strengths == []
        assert result.weaknesses == []
        assert result.opportunities == []
        assert result.threats == []
        assert result.so_strategies == []
        assert result.wo_strategies == []
        assert result.st_strategies == []
        assert result.wt_strategies == []
        assert result.key_message  # Should still have a message

    def test_none_inputs(self):
        """None inputs should not raise, returns valid SWOTAnalysis."""
        result = synthesize_swot(
            trends=None,
            market_customer=None,
            competition=None,
            self_analysis=None,
        )
        assert isinstance(result, SWOTAnalysis)
        assert result.strengths == []
        assert result.weaknesses == []

    def test_partial_inputs(self, mock_self):
        """Only self_analysis provided; should still produce S, W, and strategies."""
        result = synthesize_swot(
            trends=None,
            market_customer=None,
            competition=None,
            self_analysis=mock_self,
        )
        assert len(result.strengths) == 3
        assert len(result.weaknesses) == 4  # 3 + 1 exposure
        assert result.opportunities == []
        # No opportunities -> no SO or WO strategies
        assert result.so_strategies == []
        assert result.wo_strategies == []


# ---------------------------------------------------------------------------
# Test: Return type
# ---------------------------------------------------------------------------

class TestSWOTReturnType:

    def test_returns_swot_analysis(self, swot_result):
        assert isinstance(swot_result, SWOTAnalysis)

    def test_provenance_tracking(
        self, mock_trends, mock_market, mock_competition, mock_self,
    ):
        """When provenance is supplied, swot_total_items is tracked."""
        from src.models.provenance import ProvenanceStore
        prov = ProvenanceStore()
        synthesize_swot(
            trends=mock_trends,
            market_customer=mock_market,
            competition=mock_competition,
            self_analysis=mock_self,
            provenance=prov,
        )
        tracked = prov.get_values(field_name="swot_total_items")
        assert len(tracked) == 1
        assert tracked[0].value > 0
