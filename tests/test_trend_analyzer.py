"""Tests for src.blm.trend_analyzer — multi-quarter trend analysis library.

~50 test functions across 13 test classes covering all pure functions,
edge cases, and the orchestrator.
"""
import math
import pytest

from src.blm.trend_analyzer import (
    TrendMetrics,
    _clean_series,
    compute_cagr,
    compute_momentum_score,
    compute_volatility,
    compute_trend_slope,
    compute_acceleration,
    classify_momentum_phase,
    compute_sequential_growth,
    compute_yoy_growth,
    detect_seasonality,
    compute_trend_metrics,
)


# ============================================================================
# TestCleanSeries
# ============================================================================

class TestCleanSeries:
    def test_strips_none(self):
        assert _clean_series([1, None, 3, None, 5]) == [1.0, 3.0, 5.0]

    def test_empty_input(self):
        assert _clean_series([]) == []

    def test_mixed_types(self):
        result = _clean_series([10, "20", None, 30.5, "bad", 40])
        assert result == [10.0, 20.0, 30.5, 40.0]


# ============================================================================
# TestComputeCAGR
# ============================================================================

class TestComputeCAGR:
    def test_steady_growth(self):
        # 8 quarters: 100 → 110, roughly 10% total growth over 7Q transitions
        vals = [100, 101, 103, 105, 106, 107, 108, 110]
        cagr = compute_cagr(vals)
        assert cagr is not None
        # 10% over ~7 quarters → annualized ~5.8%
        assert 4.0 < cagr < 8.0

    def test_decline(self):
        vals = [100, 98, 96, 94, 92, 90]
        cagr = compute_cagr(vals)
        assert cagr is not None
        assert cagr < 0

    def test_single_value(self):
        assert compute_cagr([100]) is None

    def test_zeros_start(self):
        # Start at 0 → cannot compute
        assert compute_cagr([0, 10, 20, 30]) is None

    def test_with_nones(self):
        vals = [100, None, 110, None, 120]
        cagr = compute_cagr(vals)
        assert cagr is not None
        assert cagr > 0  # 100 → 120

    def test_negative_start(self):
        # Negative start → return None
        assert compute_cagr([-100, -90, -80]) is None


# ============================================================================
# TestComputeMomentumScore
# ============================================================================

class TestComputeMomentumScore:
    def test_accelerating(self):
        # Recent half grows faster than earlier
        vals = [100, 101, 102, 103, 105, 108, 112, 118]
        score = compute_momentum_score(vals)
        assert score is not None
        assert score > 60

    def test_decelerating(self):
        # Earlier half grows faster than recent
        vals = [100, 108, 116, 125, 126, 127, 128, 129]
        score = compute_momentum_score(vals)
        assert score is not None
        assert score < 40

    def test_neutral(self):
        # Roughly equal growth both halves
        vals = [100, 105, 110, 115, 120, 125, 130, 135]
        score = compute_momentum_score(vals)
        assert score is not None
        assert 35 < score < 65

    def test_insufficient_data(self):
        assert compute_momentum_score([100, 110]) is None


# ============================================================================
# TestComputeVolatility
# ============================================================================

class TestComputeVolatility:
    def test_constant(self):
        vals = [100, 100, 100, 100]
        vol = compute_volatility(vals)
        assert vol is not None
        assert vol == 0.0

    def test_high_oscillation(self):
        vals = [100, 50, 100, 50, 100, 50]
        vol = compute_volatility(vals)
        assert vol is not None
        assert vol > 0.3

    def test_zeros(self):
        # All zeros → mean=0, cannot compute
        assert compute_volatility([0, 0, 0, 0]) is None

    def test_single_value(self):
        assert compute_volatility([100]) is None


# ============================================================================
# TestComputeTrendSlope
# ============================================================================

class TestComputeTrendSlope:
    def test_linear_growth(self):
        # Perfect linear: 100, 110, 120, 130 → slope = 10 per quarter
        vals = [100, 110, 120, 130]
        slope = compute_trend_slope(vals)
        assert slope is not None
        assert abs(slope - 10.0) < 0.01

    def test_flat(self):
        vals = [50, 50, 50, 50]
        slope = compute_trend_slope(vals)
        assert slope is not None
        assert abs(slope) < 0.01

    def test_noisy_positive(self):
        vals = [100, 105, 102, 108, 103, 112]
        slope = compute_trend_slope(vals)
        assert slope is not None
        assert slope > 0

    def test_insufficient_data(self):
        assert compute_trend_slope([100]) is None


# ============================================================================
# TestComputeAcceleration
# ============================================================================

class TestComputeAcceleration:
    def test_positive_acceleration(self):
        # Earlier: flat (100,100,100,100), Recent: growing (100,110,120,130)
        vals = [100, 100, 100, 100, 100, 110, 120, 130]
        accel = compute_acceleration(vals)
        assert accel is not None
        assert accel > 0

    def test_negative_acceleration(self):
        # Earlier: growing fast, Recent: flat
        vals = [100, 110, 120, 130, 130, 130, 130, 130]
        accel = compute_acceleration(vals)
        assert accel is not None
        assert accel < 0

    def test_insufficient_data(self):
        assert compute_acceleration([100, 110]) is None


# ============================================================================
# TestClassifyPhase
# ============================================================================

class TestClassifyPhase:
    def test_accelerating_growth(self):
        assert classify_momentum_phase(5.0, 2.0, 3.0) == "accelerating_growth"

    def test_decelerating_growth(self):
        assert classify_momentum_phase(5.0, -1.0, 2.0) == "decelerating_growth"

    def test_stabilizing(self):
        assert classify_momentum_phase(0.1, 0.1, 0.5) == "stabilizing"

    def test_accelerating_decline(self):
        assert classify_momentum_phase(-5.0, -2.0, -3.0) == "accelerating_decline"

    def test_recovery(self):
        assert classify_momentum_phase(-3.0, 2.0, 1.5) == "recovery"

    def test_flat_no_data(self):
        assert classify_momentum_phase(None, None, None) == "flat"


# ============================================================================
# TestSequentialGrowth
# ============================================================================

class TestSequentialGrowth:
    def test_normal(self):
        vals = [100, 110, 121]
        result = compute_sequential_growth(vals)
        assert len(result) == 2
        assert abs(result[0] - 10.0) < 0.01
        assert abs(result[1] - 10.0) < 0.01

    def test_with_nones(self):
        vals = [100, None, 120]
        result = compute_sequential_growth(vals)
        # After cleaning: [100, 120], so one growth entry
        assert len(result) == 1
        assert abs(result[0] - 20.0) < 0.01

    def test_empty(self):
        assert compute_sequential_growth([]) == []


# ============================================================================
# TestYoYGrowth
# ============================================================================

class TestYoYGrowth:
    def test_normal_8q(self):
        vals = [100, 102, 104, 106, 110, 112, 114, 116]
        result = compute_yoy_growth(vals)
        assert len(result) == 4
        # Q5 vs Q1: (110-100)/100 = 10%
        assert abs(result[0] - 10.0) < 0.01

    def test_short_series(self):
        vals = [100, 110, 120]
        result = compute_yoy_growth(vals)
        assert result == []  # Need at least 5 values

    def test_with_nones(self):
        vals = [100, None, 104, None, 110, None, 114, None]
        result = compute_yoy_growth(vals)
        # After cleaning: [100, 104, 110, 114] → need >= 5 for YoY
        assert result == []


# ============================================================================
# TestSeasonality
# ============================================================================

class TestSeasonality:
    def test_detected(self):
        # Strong Q4 seasonality
        vals = [100, 100, 100, 150, 100, 100, 100, 150, 100, 100, 100, 150]
        detected, pattern = detect_seasonality(vals)
        assert detected is True
        assert pattern is not None
        assert "Q4" in pattern

    def test_not_detected(self):
        vals = [100, 101, 102, 103, 104, 105, 106, 107]
        detected, pattern = detect_seasonality(vals)
        assert detected is False
        assert pattern is None

    def test_short_series(self):
        vals = [100, 110, 120]
        detected, pattern = detect_seasonality(vals)
        assert detected is False


# ============================================================================
# TestComputeTrendMetrics (orchestrator)
# ============================================================================

class TestComputeTrendMetrics:
    def test_full_8q_series(self):
        vals = [100, 102, 105, 108, 110, 113, 117, 121]
        m = compute_trend_metrics(vals)
        assert m.cagr_pct is not None
        assert m.cagr_pct > 0
        assert m.momentum_score is not None
        assert m.momentum_phase in (
            "accelerating_growth", "decelerating_growth",
            "stabilizing", "accelerating_decline", "recovery", "flat",
        )
        assert m.volatility is not None
        assert m.trend_slope is not None
        assert m.trend_slope > 0
        assert len(m.sequential_growth) == 7
        assert m.latest_qoq_pct is not None

    def test_empty(self):
        m = compute_trend_metrics([])
        assert m.cagr_pct is None
        assert m.momentum_phase == "flat"
        assert m.sequential_growth == []

    def test_all_nones(self):
        m = compute_trend_metrics([None, None, None, None])
        assert m.cagr_pct is None
        assert m.trend_slope is None


# ============================================================================
# TestTrendMetricsToDict
# ============================================================================

class TestTrendMetricsToDict:
    def test_round_trip(self):
        vals = [100, 110, 120, 130, 140, 150, 160, 170]
        m = compute_trend_metrics(vals)
        d = m.to_dict()
        assert isinstance(d, dict)
        assert "cagr_pct" in d
        assert "momentum_phase" in d
        assert isinstance(d["sequential_growth"], list)

    def test_field_completeness(self):
        m = TrendMetrics()
        d = m.to_dict()
        expected_keys = {
            "cagr_pct", "momentum_score", "momentum_phase", "volatility",
            "trend_slope", "acceleration", "sequential_growth", "yoy_growth",
            "latest_qoq_pct", "latest_yoy_pct", "seasonality_detected",
            "seasonality_pattern",
        }
        assert set(d.keys()) == expected_keys


# ============================================================================
# TestEdgeCases
# ============================================================================

class TestEdgeCases:
    def test_all_same_values(self):
        vals = [100, 100, 100, 100, 100, 100, 100, 100]
        m = compute_trend_metrics(vals)
        assert m.volatility == 0.0
        assert m.trend_slope is not None
        assert abs(m.trend_slope) < 0.01
        assert m.cagr_pct is not None
        assert abs(m.cagr_pct) < 0.01

    def test_single_value(self):
        m = compute_trend_metrics([42])
        assert m.cagr_pct is None
        assert m.trend_slope is None
        assert m.momentum_phase == "flat"

    def test_alternating(self):
        vals = [100, 50, 100, 50, 100, 50, 100, 50]
        m = compute_trend_metrics(vals)
        assert m.volatility is not None
        assert m.volatility > 0.3  # high volatility
        # Slope should be near zero (no net trend)
        assert m.trend_slope is not None
        assert abs(m.trend_slope) < 5.0
