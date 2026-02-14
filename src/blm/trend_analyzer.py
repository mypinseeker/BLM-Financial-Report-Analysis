"""Multi-Quarter Trend Analyzer — pure-function library.

Computes CAGR, momentum scores, volatility, trend slope, acceleration,
seasonality, and phase classification from quarterly time-series data.

Design constraints:
  - No numpy/scipy — stdlib `math` only
  - All functions handle empty, single-value, all-zeros, and None-filled arrays
  - Pure functions — no side effects, no DB access
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class TrendMetrics:
    """Rich metrics computed from a quarterly time-series."""
    cagr_pct: Optional[float] = None
    momentum_score: Optional[float] = None
    momentum_phase: str = "flat"
    volatility: Optional[float] = None
    trend_slope: Optional[float] = None
    acceleration: Optional[float] = None
    sequential_growth: list[float] = field(default_factory=list)
    yoy_growth: list[float] = field(default_factory=list)
    latest_qoq_pct: Optional[float] = None
    latest_yoy_pct: Optional[float] = None
    seasonality_detected: bool = False
    seasonality_pattern: Optional[str] = None

    def to_dict(self) -> dict:
        """Serialise to a plain dict, rounding floats to 2 dp."""
        d = asdict(self)
        for k, v in d.items():
            if isinstance(v, float):
                d[k] = round(v, 2)
            elif isinstance(v, list):
                d[k] = [round(x, 2) if isinstance(x, float) else x for x in v]
        return d


# ============================================================================
# Internal helpers
# ============================================================================

def _clean_series(values: list) -> list[float]:
    """Strip None / non-numeric values, returning a list of floats."""
    out: list[float] = []
    for v in values:
        if v is None:
            continue
        try:
            out.append(float(v))
        except (TypeError, ValueError):
            continue
    return out


def _mean(vals: list[float]) -> float:
    """Simple arithmetic mean. Caller must ensure vals is non-empty."""
    return sum(vals) / len(vals)


def _std_dev(vals: list[float], mean_val: float) -> float:
    """Population standard deviation."""
    if len(vals) < 2:
        return 0.0
    variance = sum((v - mean_val) ** 2 for v in vals) / len(vals)
    return math.sqrt(variance)


# ============================================================================
# Individual metric functions
# ============================================================================

def compute_cagr(values: list) -> Optional[float]:
    """Annualized compound growth rate from quarterly data.

    Formula: ((end / start) ^ (4 / n_periods) - 1) × 100
    where n_periods = len(clean) - 1 (number of quarter transitions).
    """
    clean = _clean_series(values)
    if len(clean) < 2:
        return None
    start, end = clean[0], clean[-1]
    if start <= 0 or end <= 0:
        return None
    n_periods = len(clean) - 1
    if n_periods == 0:
        return None
    ratio = end / start
    annualised = ratio ** (4.0 / n_periods) - 1
    return annualised * 100


def compute_momentum_score(values: list) -> Optional[float]:
    """0–100 score comparing recent-half vs earlier-half growth rates.

    > 60 → accelerating, < 40 → decelerating, 40–60 → neutral.
    """
    clean = _clean_series(values)
    if len(clean) < 4:
        return None
    mid = len(clean) // 2
    earlier = clean[:mid]
    recent = clean[mid:]

    def _half_growth(half: list[float]) -> float:
        if len(half) < 2 or half[0] == 0:
            return 0.0
        return ((half[-1] / half[0]) - 1) * 100

    eg = _half_growth(earlier)
    rg = _half_growth(recent)

    # Map growth differential to 0–100 score
    diff = rg - eg
    # Scale: diff of +10pp → score 80, diff of -10pp → score 20
    score = 50 + diff * 3
    return max(0.0, min(100.0, score))


def compute_volatility(values: list) -> Optional[float]:
    """Coefficient of variation (std_dev / |mean|). Lower = more stable."""
    clean = _clean_series(values)
    if len(clean) < 2:
        return None
    m = _mean(clean)
    if m == 0:
        return None
    sd = _std_dev(clean, m)
    return sd / abs(m)


def compute_trend_slope(values: list) -> Optional[float]:
    """Linear least-squares slope (units per quarter).

    Uses simple OLS: slope = Σ(xi - x̄)(yi - ȳ) / Σ(xi - x̄)²
    """
    clean = _clean_series(values)
    if len(clean) < 2:
        return None
    n = len(clean)
    x_vals = list(range(n))
    x_mean = _mean(x_vals)
    y_mean = _mean(clean)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_vals, clean))
    denominator = sum((x - x_mean) ** 2 for x in x_vals)
    if denominator == 0:
        return 0.0
    return numerator / denominator


def compute_acceleration(values: list) -> Optional[float]:
    """Change in slope: recent_half_slope - earlier_half_slope."""
    clean = _clean_series(values)
    if len(clean) < 4:
        return None
    mid = len(clean) // 2
    earlier_slope = compute_trend_slope(clean[:mid])
    recent_slope = compute_trend_slope(clean[mid:])
    if earlier_slope is None or recent_slope is None:
        return None
    return recent_slope - earlier_slope


def classify_momentum_phase(
    slope: Optional[float],
    acceleration: Optional[float],
    latest_qoq: Optional[float],
) -> str:
    """Classify into one of 6 momentum phases.

    Phases:
      - accelerating_growth: slope > 0 AND acceleration > 0
      - decelerating_growth: slope > 0 AND acceleration <= 0
      - stabilizing: |slope| small AND |acceleration| small
      - accelerating_decline: slope < 0 AND acceleration < 0
      - recovery: slope < 0 AND acceleration > 0 (or latest_qoq > 0)
      - flat: everything else
    """
    if slope is None:
        return "flat"

    # Thresholds for "small"
    slope_thresh = 0.5
    accel_thresh = 0.3

    if abs(slope) < slope_thresh and (acceleration is None or abs(acceleration) < accel_thresh):
        return "stabilizing" if latest_qoq is not None and abs(latest_qoq) < 2.0 else "flat"

    if slope > 0:
        if acceleration is not None and acceleration > accel_thresh:
            return "accelerating_growth"
        return "decelerating_growth"
    else:  # slope < 0
        if acceleration is not None and acceleration > accel_thresh:
            return "recovery"
        if latest_qoq is not None and latest_qoq > 1.0:
            return "recovery"
        if acceleration is not None and acceleration < -accel_thresh:
            return "accelerating_decline"
        return "decelerating_growth"


def compute_sequential_growth(values: list) -> list[float]:
    """QoQ percentage changes: (v[i] - v[i-1]) / |v[i-1]| × 100."""
    clean = _clean_series(values)
    growth: list[float] = []
    for i in range(1, len(clean)):
        if clean[i - 1] == 0:
            growth.append(0.0)
        else:
            growth.append(((clean[i] - clean[i - 1]) / abs(clean[i - 1])) * 100)
    return growth


def compute_yoy_growth(values: list) -> list[float]:
    """YoY percentage changes (4 quarters back): (v[i] - v[i-4]) / |v[i-4]| × 100."""
    clean = _clean_series(values)
    growth: list[float] = []
    for i in range(4, len(clean)):
        if clean[i - 4] == 0:
            growth.append(0.0)
        else:
            growth.append(((clean[i] - clean[i - 4]) / abs(clean[i - 4])) * 100)
    return growth


def detect_seasonality(values: list) -> tuple[bool, Optional[str]]:
    """Detect quarterly seasonality via positional grouping.

    Groups values by quarter position (0, 1, 2, 3), checks if any position
    deviates from the overall mean by more than 1σ.
    """
    clean = _clean_series(values)
    if len(clean) < 8:
        return False, None

    overall_mean = _mean(clean)
    if overall_mean == 0:
        return False, None
    overall_sd = _std_dev(clean, overall_mean)
    if overall_sd == 0:
        return False, None

    # Group by quarter position
    groups: dict[int, list[float]] = {0: [], 1: [], 2: [], 3: []}
    for i, v in enumerate(clean):
        groups[i % 4].append(v)

    # Check if any quarter position's mean deviates by > 1σ
    quarter_labels = ["Q1", "Q2", "Q3", "Q4"]
    deviating = []
    for q in range(4):
        if not groups[q]:
            continue
        q_mean = _mean(groups[q])
        if abs(q_mean - overall_mean) > overall_sd:
            direction = "high" if q_mean > overall_mean else "low"
            deviating.append(f"{quarter_labels[q]}={direction}")

    if deviating:
        return True, "; ".join(deviating)
    return False, None


# ============================================================================
# Orchestrator
# ============================================================================

def compute_trend_metrics(values: list) -> TrendMetrics:
    """Compute all trend metrics from a quarterly time-series.

    This is the main entry point. Calls all individual metric functions
    and assembles a TrendMetrics dataclass.
    """
    clean = _clean_series(values)
    if len(clean) < 2:
        return TrendMetrics()

    cagr = compute_cagr(clean)
    momentum = compute_momentum_score(clean)
    volatility = compute_volatility(clean)
    slope = compute_trend_slope(clean)
    accel = compute_acceleration(clean)
    seq_growth = compute_sequential_growth(clean)
    yoy = compute_yoy_growth(clean)
    seasonality, pattern = detect_seasonality(clean)

    latest_qoq = seq_growth[-1] if seq_growth else None
    latest_yoy = yoy[-1] if yoy else None

    phase = classify_momentum_phase(slope, accel, latest_qoq)

    return TrendMetrics(
        cagr_pct=cagr,
        momentum_score=momentum,
        momentum_phase=phase,
        volatility=volatility,
        trend_slope=slope,
        acceleration=accel,
        sequential_growth=seq_growth,
        yoy_growth=yoy,
        latest_qoq_pct=latest_qoq,
        latest_yoy_pct=latest_yoy,
        seasonality_detected=seasonality,
        seasonality_pattern=pattern,
    )
