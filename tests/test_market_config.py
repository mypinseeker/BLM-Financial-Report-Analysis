"""Tests for MarketConfig system and Germany configuration."""

import sys
from pathlib import Path

import pytest

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.models.market_config import MarketConfig
from src.models.market_configs import get_market_config, MARKET_REGISTRY


# ============================================================================
# Registry
# ============================================================================

class TestMarketRegistry:

    def test_germany_config_exists(self):
        """Germany config should be registered."""
        assert "germany" in MARKET_REGISTRY

    def test_get_market_config_germany(self):
        """get_market_config('germany') returns a MarketConfig."""
        cfg = get_market_config("germany")
        assert isinstance(cfg, MarketConfig)
        assert cfg.market_id == "germany"

    def test_get_market_config_unknown(self):
        """Unknown market should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown market"):
            get_market_config("narnia")

    def test_get_market_config_error_message(self):
        """Error message should list available markets."""
        with pytest.raises(ValueError, match="germany"):
            get_market_config("unknown_market")


# ============================================================================
# Germany Config
# ============================================================================

class TestGermanyConfig:

    @pytest.fixture
    def cfg(self):
        return get_market_config("germany")

    def test_market_identity(self, cfg):
        """Germany config should have correct identity fields."""
        assert cfg.market_name == "Germany"
        assert cfg.country == "Germany"
        assert cfg.currency == "EUR"
        assert cfg.currency_symbol == "€"
        assert cfg.regulatory_body == "BNetzA"
        assert cfg.population_k == 84000

    def test_customer_segments_count(self, cfg):
        """Germany should have 7 customer segments."""
        assert len(cfg.customer_segments) == 7

    def test_customer_segment_types(self, cfg):
        """Segments should cover consumer, enterprise, and wholesale."""
        segment_types = {s["segment_type"] for s in cfg.customer_segments}
        assert segment_types == {"consumer", "enterprise", "wholesale"}

    def test_customer_segment_names(self, cfg):
        """Segment names should match the original GERMAN_TELECOM_SEGMENTS."""
        names = [s["segment_name"] for s in cfg.customer_segments]
        assert "Consumer High-End" in names
        assert "Consumer Mainstream" in names
        assert "Enterprise Large" in names
        assert "Wholesale MVNO" in names

    def test_customer_segment_fields(self, cfg):
        """Each segment should have required fields."""
        for seg in cfg.customer_segments:
            assert "segment_name" in seg
            assert "segment_type" in seg
            assert "unmet_needs" in seg
            assert "pain_points" in seg
            assert "purchase_decision_factors" in seg

    def test_bmc_enrichments_all_operators(self, cfg):
        """All 4 German operators should have BMC enrichments."""
        expected_ops = {"vodafone_germany", "deutsche_telekom", "telefonica_o2", "one_and_one"}
        assert set(cfg.operator_bmc_enrichments.keys()) == expected_ops

    def test_bmc_enrichment_vodafone(self, cfg):
        """Vodafone BMC enrichment should include cable network."""
        vf = cfg.operator_bmc_enrichments["vodafone_germany"]
        assert any("Cable" in r for r in vf.get("key_resources", []))

    def test_bmc_enrichment_dt(self, cfg):
        """DT BMC enrichment should include fiber network."""
        dt = cfg.operator_bmc_enrichments["deutsche_telekom"]
        assert any("fiber" in r.lower() for r in dt.get("key_resources", []))

    def test_exposures_all_operators(self, cfg):
        """All 4 operators should have exposure data."""
        expected_ops = {"vodafone_germany", "deutsche_telekom", "telefonica_o2", "one_and_one"}
        assert set(cfg.operator_exposures.keys()) == expected_ops

    def test_exposure_fields(self, cfg):
        """Each exposure should have required fields."""
        for op_id, exposures in cfg.operator_exposures.items():
            assert len(exposures) >= 1, f"{op_id} has no exposures"
            for exp in exposures:
                assert "trigger_action" in exp
                assert "side_effect" in exp
                assert "attack_vector" in exp
                assert "severity" in exp

    def test_competitive_landscape_notes(self, cfg):
        """Competitive landscape should have notes."""
        assert len(cfg.competitive_landscape_notes) >= 3

    def test_pest_context(self, cfg):
        """PEST context should have all 4 dimensions."""
        assert "political" in cfg.pest_context
        assert "economic" in cfg.pest_context
        assert "social" in cfg.pest_context
        assert "technological" in cfg.pest_context
        for key, items in cfg.pest_context.items():
            assert len(items) >= 2, f"PEST '{key}' has fewer than 2 items"


# ============================================================================
# MarketConfig Required Fields
# ============================================================================

class TestMarketConfigRequiredFields:

    def test_all_required_fields_present(self):
        """MarketConfig should have all required fields."""
        cfg = get_market_config("germany")
        required = [
            "market_id", "market_name", "country", "currency",
            "currency_symbol", "regulatory_body", "population_k",
        ]
        for field_name in required:
            assert hasattr(cfg, field_name), f"Missing field: {field_name}"
            assert getattr(cfg, field_name) is not None, f"Field is None: {field_name}"
