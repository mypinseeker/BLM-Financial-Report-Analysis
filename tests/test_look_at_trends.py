"""Tests for Look 1: Trends (PEST Framework) analysis module.

Tests cover:
  - Full analysis with seeded Germany data
  - Empty database graceful handling
  - PEST dimension population
  - Industry metrics computation
  - Key message generation
  - Factor field validation
  - Trend direction validation
"""

import pytest

from src.database.db import TelecomDatabase
from src.database.seed_germany import seed_all
from src.models.trend import PESTFactor, PESTAnalysis, TrendAnalysis
from src.models.provenance import ProvenanceStore
from src.blm.look_at_trends import analyze_trends


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def seeded_db():
    """In-memory database seeded with Germany telecom market data."""
    database = seed_all(":memory:")
    yield database
    database.close()


@pytest.fixture
def empty_db():
    """In-memory database with schema but no data."""
    database = TelecomDatabase(":memory:")
    database.init()
    yield database
    database.close()


# ---------------------------------------------------------------------------
# Core integration test
# ---------------------------------------------------------------------------

class TestAnalyzeTrendsWithSeedData:
    """Test analyze_trends with fully seeded Germany market data."""

    def test_returns_trend_analysis(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert isinstance(result, TrendAnalysis)

    def test_pest_is_populated(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert isinstance(result.pest, PESTAnalysis)

    def test_all_four_pest_dimensions_have_factors(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert len(result.pest.political_factors) > 0, "Political factors should not be empty"
        assert len(result.pest.economic_factors) > 0, "Economic factors should not be empty"
        assert len(result.pest.society_factors) > 0, "Society factors should not be empty"
        assert len(result.pest.technology_factors) > 0, "Technology factors should not be empty"

    def test_provenance_tracking(self, seeded_db):
        prov = ProvenanceStore()
        analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
            provenance=prov,
        )
        # Should have tracked some data points
        all_values = prov.get_values()
        assert len(all_values) > 0, "Provenance should contain tracked values"

    def test_with_target_period(self, seeded_db):
        """Test with explicit target_period parameter."""
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
            target_period="CQ4_2025",
        )
        assert isinstance(result, TrendAnalysis)
        assert result.key_message != ""

    def test_with_different_operator(self, seeded_db):
        """Test with a different target operator in the same market."""
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="deutsche_telekom",
        )
        assert isinstance(result, TrendAnalysis)
        assert len(result.pest.political_factors) > 0


# ---------------------------------------------------------------------------
# Empty database handling
# ---------------------------------------------------------------------------

class TestAnalyzeTrendsEmptyDB:
    """Test that analyze_trends handles an empty database gracefully."""

    def test_returns_valid_trend_analysis(self, empty_db):
        result = analyze_trends(
            db=empty_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert isinstance(result, TrendAnalysis)

    def test_pest_has_placeholder_factors(self, empty_db):
        result = analyze_trends(
            db=empty_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        # Each dimension should have at least one placeholder factor
        assert len(result.pest.political_factors) >= 1
        assert len(result.pest.economic_factors) >= 1
        assert len(result.pest.society_factors) >= 1
        assert len(result.pest.technology_factors) >= 1

    def test_industry_metrics_na(self, empty_db):
        result = analyze_trends(
            db=empty_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert result.industry_market_size == "N/A"
        assert result.industry_growth_rate == "N/A"

    def test_key_message_not_empty(self, empty_db):
        result = analyze_trends(
            db=empty_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert result.key_message != ""
        assert len(result.key_message) > 5


# ---------------------------------------------------------------------------
# PEST dimension detail tests
# ---------------------------------------------------------------------------

class TestPESTDimensionsPopulated:
    """Test that each PEST dimension is properly populated with seed data."""

    def test_political_has_regulatory_factor(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        factor_names = [f.factor_name for f in result.pest.political_factors]
        assert any("Regulatory" in name or "Digital" in name for name in factor_names), \
            f"Expected regulatory/digital factor, got: {factor_names}"

    def test_economic_has_gdp_factor(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        factor_names = [f.factor_name for f in result.pest.economic_factors]
        assert any("GDP" in name for name in factor_names), \
            f"Expected GDP factor, got: {factor_names}"

    def test_economic_has_inflation_factor(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        factor_names = [f.factor_name for f in result.pest.economic_factors]
        assert any("Inflation" in name for name in factor_names), \
            f"Expected inflation factor, got: {factor_names}"

    def test_society_has_adoption_factor(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        factor_names = [f.factor_name for f in result.pest.society_factors]
        assert any("5G" in name or "Fiber" in name or "Adoption" in name for name in factor_names), \
            f"Expected adoption/fiber factor, got: {factor_names}"

    def test_technology_has_5g_factor(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        factor_names = [f.factor_name for f in result.pest.technology_factors]
        assert any("5G" in name or "Fiber" in name for name in factor_names), \
            f"Expected 5G/Fiber technology factor, got: {factor_names}"

    def test_all_factors_have_correct_dimension(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        for f in result.pest.political_factors:
            assert f.dimension == "P"
        for f in result.pest.economic_factors:
            assert f.dimension == "E"
        for f in result.pest.society_factors:
            assert f.dimension == "S"
        for f in result.pest.technology_factors:
            assert f.dimension == "T"


# ---------------------------------------------------------------------------
# Industry metrics tests
# ---------------------------------------------------------------------------

class TestIndustryMetricsComputed:
    """Test that industry-level metrics are computed from seed data."""

    def test_market_size_computed(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
            target_period="CQ4_2025",
        )
        assert result.industry_market_size != ""
        assert result.industry_market_size != "N/A"
        assert "EUR" in result.industry_market_size

    def test_growth_rate_computed(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
            target_period="CQ4_2025",
        )
        assert result.industry_growth_rate != ""
        assert result.industry_growth_rate != "N/A"
        assert "%" in result.industry_growth_rate

    def test_concentration_computed(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
            target_period="CQ4_2025",
        )
        assert result.industry_concentration != ""
        assert result.industry_concentration != "N/A"
        assert "CR4" in result.industry_concentration

    def test_lifecycle_stage_determined(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
            target_period="CQ4_2025",
        )
        assert result.industry_lifecycle_stage in ("growth", "late_growth", "mature", "decline")

    def test_profit_trend_computed(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
            target_period="CQ4_2025",
        )
        assert result.industry_profit_trend != ""
        assert result.industry_profit_trend != "N/A"

    def test_key_success_factors_populated(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert len(result.key_success_factors) > 0

    def test_new_business_models_populated(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert len(result.new_business_models) > 0

    def test_value_transfer_trends_populated(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert len(result.value_transfer_trends) > 0


# ---------------------------------------------------------------------------
# Key message tests
# ---------------------------------------------------------------------------

class TestKeyMessageNotEmpty:
    """Test that key_message is always non-empty."""

    def test_key_message_with_seed_data(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert result.key_message != ""
        assert len(result.key_message) > 10

    def test_key_message_with_empty_db(self, empty_db):
        result = analyze_trends(
            db=empty_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert result.key_message != ""

    def test_pest_key_message_with_seed_data(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert result.pest.key_message != ""


# ---------------------------------------------------------------------------
# Factor field validation
# ---------------------------------------------------------------------------

class TestPESTFactorsHaveRequiredFields:
    """Test that each PESTFactor has all required fields populated."""

    def test_factors_have_dimension(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        all_factors = (
            result.pest.political_factors
            + result.pest.economic_factors
            + result.pest.society_factors
            + result.pest.technology_factors
        )
        for f in all_factors:
            assert f.dimension in ("P", "E", "S", "T"), f"Invalid dimension: {f.dimension}"

    def test_factors_have_factor_name(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        all_factors = (
            result.pest.political_factors
            + result.pest.economic_factors
            + result.pest.society_factors
            + result.pest.technology_factors
        )
        for f in all_factors:
            assert f.factor_name != "", f"Factor name should not be empty"
            assert len(f.factor_name) > 0

    def test_factors_have_impact_type(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        valid_types = {"opportunity", "threat", "neutral", "both"}
        all_factors = (
            result.pest.political_factors
            + result.pest.economic_factors
            + result.pest.society_factors
            + result.pest.technology_factors
        )
        for f in all_factors:
            assert f.impact_type in valid_types, \
                f"Invalid impact_type '{f.impact_type}' for factor '{f.factor_name}'"

    def test_factors_have_severity(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        valid_severities = {"high", "medium", "low"}
        all_factors = (
            result.pest.political_factors
            + result.pest.economic_factors
            + result.pest.society_factors
            + result.pest.technology_factors
        )
        for f in all_factors:
            assert f.severity in valid_severities, \
                f"Invalid severity '{f.severity}' for factor '{f.factor_name}'"

    def test_factors_have_dimension_name(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        valid_names = {"Political", "Economic", "Society", "Technology"}
        all_factors = (
            result.pest.political_factors
            + result.pest.economic_factors
            + result.pest.society_factors
            + result.pest.technology_factors
        )
        for f in all_factors:
            assert f.dimension_name in valid_names, \
                f"Invalid dimension_name '{f.dimension_name}'"


# ---------------------------------------------------------------------------
# Trend direction validation
# ---------------------------------------------------------------------------

class TestTrendDirectionValid:
    """Test that trend_direction values are valid."""

    VALID_DIRECTIONS = {"improving", "worsening", "stable", "uncertain"}

    def test_all_factors_have_valid_direction(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        all_factors = (
            result.pest.political_factors
            + result.pest.economic_factors
            + result.pest.society_factors
            + result.pest.technology_factors
        )
        for f in all_factors:
            assert f.trend_direction in self.VALID_DIRECTIONS, \
                f"Invalid trend_direction '{f.trend_direction}' for factor '{f.factor_name}'"

    def test_empty_db_factors_have_valid_direction(self, empty_db):
        result = analyze_trends(
            db=empty_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        all_factors = (
            result.pest.political_factors
            + result.pest.economic_factors
            + result.pest.society_factors
            + result.pest.technology_factors
        )
        for f in all_factors:
            assert f.trend_direction in self.VALID_DIRECTIONS, \
                f"Invalid trend_direction '{f.trend_direction}' for factor '{f.factor_name}'"


# ---------------------------------------------------------------------------
# Weather assessment tests
# ---------------------------------------------------------------------------

class TestWeatherAssessment:
    """Test the overall weather assessment logic."""

    def test_weather_is_valid(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        valid_weather = {"sunny", "cloudy", "stormy", "mixed"}
        assert result.pest.overall_weather in valid_weather, \
            f"Invalid weather: {result.pest.overall_weather}"

    def test_weather_explanation_not_empty(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert result.pest.weather_explanation != ""

    def test_weather_with_empty_db(self, empty_db):
        result = analyze_trends(
            db=empty_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert result.pest.overall_weather in {"sunny", "cloudy", "stormy", "mixed"}


# ---------------------------------------------------------------------------
# Cross-cutting PEST output tests
# ---------------------------------------------------------------------------

class TestPESTCrossCuttingOutputs:
    """Test PEST cross-cutting summary outputs."""

    def test_policy_opportunities_populated(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert isinstance(result.pest.policy_opportunities, list)
        # With seed data we expect some opportunities from regulatory/digital strategy
        assert len(result.pest.policy_opportunities) > 0

    def test_policy_threats_populated(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert isinstance(result.pest.policy_threats, list)

    def test_tech_addressable_market(self, seeded_db):
        result = analyze_trends(
            db=seeded_db,
            market="germany",
            target_operator="vodafone_germany",
        )
        assert result.pest.tech_addressable_market != ""
