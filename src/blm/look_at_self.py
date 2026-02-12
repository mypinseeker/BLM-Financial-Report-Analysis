"""Look 4: Self Analysis (BMC + Capability Assessment).

Analyzes the target operator's financial health, segment performance,
network infrastructure, business model, and competitive position.
Uses the BLM methodology's "Look at Self" framework with BMC canvas
and capability assessment.
"""

from __future__ import annotations

from typing import Optional

from src.database.db import TelecomDatabase
from src.models.market_config import MarketConfig
from src.models.self_analysis import (
    BMCCanvas,
    ChangeAttribution,
    ExposurePoint,
    NetworkAnalysis,
    SegmentAnalysis,
    SegmentChange,
    SelfInsight,
)


# ============================================================================
# Revenue formatting
# ============================================================================


def _fmt_rev(val_m: float, currency: str = "") -> str:
    """Format a revenue value in millions to a human-readable string."""
    prefix = f"{currency} " if currency else ""
    if val_m >= 1_000_000:
        return f"{prefix}{val_m / 1_000_000:.2f}T"
    elif val_m >= 10_000:
        return f"{prefix}{val_m / 1_000:.1f}B"
    elif val_m >= 1_000:
        return f"{prefix}{val_m:,.0f}M"
    else:
        return f"{prefix}{val_m:,.1f}M"


# ============================================================================
# Constants
# ============================================================================

# Segment definitions: (segment_name, segment_id)
SEGMENT_DEFINITIONS = [
    ("Mobile", "mobile"),
    ("Fixed Broadband", "fixed"),
    ("B2B", "b2b"),
    ("TV/Convergence", "tv"),
    ("Wholesale", "wholesale"),
]

VALID_HEALTH_STATUSES = {"strong", "stable", "weakening", "critical"}
VALID_HEALTH_RATINGS = {"healthy", "stable", "concerning", "critical"}


# ============================================================================
# Helper Functions
# ============================================================================

def _safe_pct_change(current, previous):
    """Compute percentage change, returning 0.0 if inputs are invalid."""
    if current is None or previous is None:
        return 0.0
    if previous == 0:
        return 0.0
    return round(((current - previous) / abs(previous)) * 100, 2)


def _safe_get(data: dict, key: str, default=None):
    """Safely get a value from a dict, returning default if None or missing."""
    val = data.get(key, default)
    return val if val is not None else default


def _determine_direction(change_pct: float, threshold: float = 1.0) -> str:
    """Determine direction from a percentage change value."""
    if change_pct > threshold:
        return "improving"
    elif change_pct < -threshold:
        return "declining"
    return "stable"


def _determine_significance(change_pct: float) -> str:
    """Determine significance from an absolute change percentage."""
    abs_change = abs(change_pct)
    if abs_change >= 5.0:
        return "significant"
    elif abs_change >= 2.0:
        return "moderate"
    return "minor"


def _get_latest_cq(financial_data: list) -> Optional[str]:
    """Get the latest calendar quarter from a financial timeseries."""
    if not financial_data:
        return None
    return financial_data[-1].get("calendar_quarter")


def _get_yoy_quarter(data_list: list, current_index: int) -> Optional[dict]:
    """Get the year-over-year quarter (4 quarters back) if available."""
    yoy_index = current_index - 4
    if 0 <= yoy_index < len(data_list):
        return data_list[yoy_index]
    return None


# ============================================================================
# Financial Health
# ============================================================================

def _analyze_financial_health(financial_data: list) -> dict:
    """Analyze overall financial health from time series data.

    Returns a dict with revenue, ebitda, margin, capex, and growth metrics.
    """
    if not financial_data:
        return {}

    latest = financial_data[-1]
    prev = financial_data[-2] if len(financial_data) >= 2 else {}
    yoy = financial_data[-5] if len(financial_data) >= 5 else {}

    total_revenue = _safe_get(latest, "total_revenue")
    prev_revenue = _safe_get(prev, "total_revenue")
    yoy_revenue = _safe_get(yoy, "total_revenue")

    ebitda = _safe_get(latest, "ebitda")
    prev_ebitda = _safe_get(prev, "ebitda")

    health = {
        # Current period metrics
        "total_revenue": total_revenue,
        "service_revenue": _safe_get(latest, "service_revenue"),
        "ebitda": ebitda,
        "ebitda_margin_pct": _safe_get(latest, "ebitda_margin_pct"),
        "net_income": _safe_get(latest, "net_income"),
        "capex": _safe_get(latest, "capex"),
        "capex_to_revenue_pct": _safe_get(latest, "capex_to_revenue_pct"),
        "opex": _safe_get(latest, "opex"),
        "employees": _safe_get(latest, "employees"),
        # Growth rates
        "revenue_qoq_pct": _safe_pct_change(total_revenue, prev_revenue),
        "revenue_yoy_pct": _safe_pct_change(total_revenue, yoy_revenue),
        "ebitda_qoq_pct": _safe_pct_change(ebitda, prev_ebitda),
        "ebitda_growth_pct": _safe_get(latest, "ebitda_growth_pct"),
        "service_revenue_growth_pct": _safe_get(latest, "service_revenue_growth_pct"),
        # Trend indicators
        "revenue_trend": [],
        "ebitda_trend": [],
        "margin_trend": [],
    }

    # Build trend arrays for visualization
    for q in financial_data:
        health["revenue_trend"].append(_safe_get(q, "total_revenue"))
        health["ebitda_trend"].append(_safe_get(q, "ebitda"))
        health["margin_trend"].append(_safe_get(q, "ebitda_margin_pct"))

    # Determine overall health assessment
    rev_growing = (health["revenue_qoq_pct"] > 0) or (health["revenue_yoy_pct"] > 0)
    margin_ok = (health.get("ebitda_margin_pct") or 0) >= 30
    health["revenue_growing"] = rev_growing
    health["margin_healthy"] = margin_ok

    return health


# ============================================================================
# Revenue Breakdown
# ============================================================================

def _compute_revenue_breakdown(latest_financial: dict) -> dict:
    """Compute revenue breakdown by segment from latest financial data."""
    if not latest_financial:
        return {}

    total = _safe_get(latest_financial, "total_revenue", 0)
    if total == 0:
        return {}

    segments = {
        "mobile_service_revenue": _safe_get(latest_financial, "mobile_service_revenue"),
        "fixed_service_revenue": _safe_get(latest_financial, "fixed_service_revenue"),
        "b2b_revenue": _safe_get(latest_financial, "b2b_revenue"),
        "tv_revenue": _safe_get(latest_financial, "tv_revenue"),
        "wholesale_revenue": _safe_get(latest_financial, "wholesale_revenue"),
    }

    breakdown = {}
    for key, value in segments.items():
        if value is not None:
            share = round((value / total) * 100, 1) if total > 0 else 0
            breakdown[key] = {
                "value": value,
                "share_pct": share,
            }

    # Calculate other/unclassified revenue
    classified_total = sum(v for v in segments.values() if v is not None)
    other = total - classified_total
    if other > 0:
        breakdown["other_revenue"] = {
            "value": round(other, 1),
            "share_pct": round((other / total) * 100, 1) if total > 0 else 0,
        }

    breakdown["total_revenue"] = total
    return breakdown


# ============================================================================
# Market Positions
# ============================================================================

def _analyze_market_positions(
    db: TelecomDatabase,
    market: str,
    target_operator: str,
    latest_cq: str,
) -> dict:
    """Compute target operator's market position relative to competitors."""
    if not latest_cq:
        return {}

    try:
        comparison = db.get_market_comparison(market, latest_cq)
    except Exception:
        return {}

    if not comparison:
        return {}

    positions = {
        "calendar_quarter": latest_cq,
        "operators_count": len(comparison),
    }

    # Find target operator's data and rank
    target_data = None
    for row in comparison:
        if row.get("operator_id") == target_operator:
            target_data = row
            break

    if not target_data:
        return positions

    # Revenue rank (comparison is already sorted by total_revenue DESC)
    revenue_rank = 1
    for row in comparison:
        if row.get("operator_id") == target_operator:
            break
        if _safe_get(row, "total_revenue") is not None:
            revenue_rank += 1

    positions["revenue_rank"] = revenue_rank
    positions["total_revenue"] = _safe_get(target_data, "total_revenue")

    # Compute revenue market share
    total_market_revenue = sum(
        _safe_get(r, "total_revenue", 0) for r in comparison
        if _safe_get(r, "total_revenue") is not None
    )
    if total_market_revenue > 0 and positions.get("total_revenue") is not None:
        positions["revenue_market_share_pct"] = round(
            (positions["total_revenue"] / total_market_revenue) * 100, 1
        )

    # Mobile subscriber rank
    mobile_subs = [
        (r["operator_id"], _safe_get(r, "mobile_total_k", 0))
        for r in comparison
        if _safe_get(r, "mobile_total_k") is not None
    ]
    mobile_subs.sort(key=lambda x: x[1], reverse=True)
    for i, (op_id, _) in enumerate(mobile_subs, 1):
        if op_id == target_operator:
            positions["subscriber_rank"] = i
            break

    # Mobile subscriber share
    total_mobile = sum(s for _, s in mobile_subs)
    target_mobile = _safe_get(target_data, "mobile_total_k")
    if total_mobile > 0 and target_mobile is not None:
        positions["mobile_subscriber_share_pct"] = round(
            (target_mobile / total_mobile) * 100, 1
        )

    # Broadband subscriber share
    bb_subs = [
        (r["operator_id"], _safe_get(r, "broadband_total_k", 0))
        for r in comparison
        if _safe_get(r, "broadband_total_k") is not None
    ]
    total_bb = sum(s for _, s in bb_subs)
    target_bb = _safe_get(target_data, "broadband_total_k")
    if total_bb > 0 and target_bb is not None:
        positions["broadband_subscriber_share_pct"] = round(
            (target_bb / total_bb) * 100, 1
        )

    # Include competitor revenue info for reference
    positions["competitors"] = {}
    for row in comparison:
        if row.get("operator_id") != target_operator:
            positions["competitors"][row["operator_id"]] = {
                "display_name": row.get("display_name"),
                "total_revenue": _safe_get(row, "total_revenue"),
                "mobile_total_k": _safe_get(row, "mobile_total_k"),
                "broadband_total_k": _safe_get(row, "broadband_total_k"),
            }

    return positions


# ============================================================================
# Segment Analysis
# ============================================================================

def _make_segment_change(
    metric: str,
    current_value,
    previous_value,
    yoy_value=None,
) -> SegmentChange:
    """Create a SegmentChange with computed QoQ/YoY metrics."""
    qoq = _safe_pct_change(current_value, previous_value)
    yoy = _safe_pct_change(current_value, yoy_value)

    return SegmentChange(
        metric=metric,
        current_value=current_value,
        previous_value=previous_value,
        yoy_value=yoy_value,
        change_qoq=qoq,
        change_yoy=yoy,
        direction=_determine_direction(qoq),
        significance=_determine_significance(qoq),
    )


def _analyze_mobile_segment(
    financial_data: list,
    subscriber_data: list,
    comparison: list,
    target_operator: str,
) -> SegmentAnalysis:
    """Analyze Mobile segment."""
    latest_fin = financial_data[-1] if financial_data else {}
    prev_fin = financial_data[-2] if len(financial_data) >= 2 else {}
    yoy_fin = financial_data[-5] if len(financial_data) >= 5 else {}

    latest_sub = subscriber_data[-1] if subscriber_data else {}
    prev_sub = subscriber_data[-2] if len(subscriber_data) >= 2 else {}
    yoy_sub = subscriber_data[-5] if len(subscriber_data) >= 5 else {}

    key_metrics = {
        "mobile_service_revenue": _safe_get(latest_fin, "mobile_service_revenue"),
        "mobile_service_growth_pct": _safe_get(latest_fin, "mobile_service_growth_pct"),
        "mobile_total_k": _safe_get(latest_sub, "mobile_total_k"),
        "mobile_postpaid_k": _safe_get(latest_sub, "mobile_postpaid_k"),
        "mobile_prepaid_k": _safe_get(latest_sub, "mobile_prepaid_k"),
        "mobile_net_adds_k": _safe_get(latest_sub, "mobile_net_adds_k"),
        "mobile_churn_pct": _safe_get(latest_sub, "mobile_churn_pct"),
        "mobile_arpu": _safe_get(latest_sub, "mobile_arpu"),
        "iot_connections_k": _safe_get(latest_sub, "iot_connections_k"),
    }

    changes = [
        _make_segment_change(
            "revenue",
            _safe_get(latest_fin, "mobile_service_revenue"),
            _safe_get(prev_fin, "mobile_service_revenue"),
            _safe_get(yoy_fin, "mobile_service_revenue"),
        ),
        _make_segment_change(
            "subscribers",
            _safe_get(latest_sub, "mobile_total_k"),
            _safe_get(prev_sub, "mobile_total_k"),
            _safe_get(yoy_sub, "mobile_total_k"),
        ),
        _make_segment_change(
            "arpu",
            _safe_get(latest_sub, "mobile_arpu"),
            _safe_get(prev_sub, "mobile_arpu"),
            _safe_get(yoy_sub, "mobile_arpu"),
        ),
    ]

    # Build trend data
    trend_data = {
        "revenue": [_safe_get(f, "mobile_service_revenue") for f in financial_data],
        "subscribers": [_safe_get(s, "mobile_total_k") for s in subscriber_data],
        "arpu": [_safe_get(s, "mobile_arpu") for s in subscriber_data],
        "churn": [_safe_get(s, "mobile_churn_pct") for s in subscriber_data],
    }

    # Competitor comparison
    comp = {}
    for row in comparison:
        if row.get("operator_id") != target_operator:
            comp[row.get("display_name", row.get("operator_id", "unknown"))] = {
                "mobile_service_revenue": _safe_get(row, "mobile_service_revenue"),
                "mobile_total_k": _safe_get(row, "mobile_total_k"),
                "mobile_arpu": _safe_get(row, "mobile_arpu"),
                "mobile_churn_pct": _safe_get(row, "mobile_churn_pct"),
            }

    # Determine health
    rev_change = changes[0].change_qoq if changes else 0
    sub_change = changes[1].change_qoq if len(changes) > 1 else 0
    health = _classify_segment_health(rev_change, sub_change)

    # Key message
    rev_val = key_metrics.get("mobile_service_revenue")
    growth_pct = key_metrics.get("mobile_service_growth_pct")
    msg_parts = []
    if rev_val is not None:
        msg_parts.append(f"Mobile service revenue at {_fmt_rev(rev_val)}")
    if growth_pct is not None:
        direction = "up" if growth_pct > 0 else "down"
        msg_parts.append(f"{direction} {abs(growth_pct):.1f}% YoY")
    arpu = key_metrics.get("mobile_arpu")
    if arpu is not None:
        msg_parts.append(f"ARPU {arpu}")
    key_message = "; ".join(msg_parts) if msg_parts else "Insufficient data for mobile segment assessment"

    return SegmentAnalysis(
        segment_name="Mobile",
        segment_id="mobile",
        key_metrics=key_metrics,
        changes=changes,
        trend_data=trend_data,
        competitor_comparison=comp,
        health_status=health,
        key_message=key_message,
    )


def _analyze_fixed_segment(
    financial_data: list,
    subscriber_data: list,
    comparison: list,
    target_operator: str,
) -> SegmentAnalysis:
    """Analyze Fixed Broadband segment."""
    latest_fin = financial_data[-1] if financial_data else {}
    prev_fin = financial_data[-2] if len(financial_data) >= 2 else {}
    yoy_fin = financial_data[-5] if len(financial_data) >= 5 else {}

    latest_sub = subscriber_data[-1] if subscriber_data else {}
    prev_sub = subscriber_data[-2] if len(subscriber_data) >= 2 else {}
    yoy_sub = subscriber_data[-5] if len(subscriber_data) >= 5 else {}

    key_metrics = {
        "fixed_service_revenue": _safe_get(latest_fin, "fixed_service_revenue"),
        "fixed_service_growth_pct": _safe_get(latest_fin, "fixed_service_growth_pct"),
        "broadband_total_k": _safe_get(latest_sub, "broadband_total_k"),
        "broadband_net_adds_k": _safe_get(latest_sub, "broadband_net_adds_k"),
        "broadband_cable_k": _safe_get(latest_sub, "broadband_cable_k"),
        "broadband_fiber_k": _safe_get(latest_sub, "broadband_fiber_k"),
        "broadband_dsl_k": _safe_get(latest_sub, "broadband_dsl_k"),
        "broadband_arpu": _safe_get(latest_sub, "broadband_arpu"),
    }

    changes = [
        _make_segment_change(
            "revenue",
            _safe_get(latest_fin, "fixed_service_revenue"),
            _safe_get(prev_fin, "fixed_service_revenue"),
            _safe_get(yoy_fin, "fixed_service_revenue"),
        ),
        _make_segment_change(
            "subscribers",
            _safe_get(latest_sub, "broadband_total_k"),
            _safe_get(prev_sub, "broadband_total_k"),
            _safe_get(yoy_sub, "broadband_total_k"),
        ),
        _make_segment_change(
            "arpu",
            _safe_get(latest_sub, "broadband_arpu"),
            _safe_get(prev_sub, "broadband_arpu"),
            _safe_get(yoy_sub, "broadband_arpu"),
        ),
    ]

    trend_data = {
        "revenue": [_safe_get(f, "fixed_service_revenue") for f in financial_data],
        "subscribers": [_safe_get(s, "broadband_total_k") for s in subscriber_data],
        "arpu": [_safe_get(s, "broadband_arpu") for s in subscriber_data],
        "fiber": [_safe_get(s, "broadband_fiber_k") for s in subscriber_data],
        "cable": [_safe_get(s, "broadband_cable_k") for s in subscriber_data],
    }

    comp = {}
    for row in comparison:
        if row.get("operator_id") != target_operator:
            comp[row.get("display_name", row.get("operator_id", "unknown"))] = {
                "fixed_service_revenue": _safe_get(row, "fixed_service_revenue"),
                "broadband_total_k": _safe_get(row, "broadband_total_k"),
                "broadband_fiber_k": _safe_get(row, "broadband_fiber_k"),
            }

    rev_change = changes[0].change_qoq if changes else 0
    sub_change = changes[1].change_qoq if len(changes) > 1 else 0
    health = _classify_segment_health(rev_change, sub_change)

    rev_val = key_metrics.get("fixed_service_revenue")
    growth_pct = key_metrics.get("fixed_service_growth_pct")
    fiber_k = key_metrics.get("broadband_fiber_k")
    msg_parts = []
    if rev_val is not None:
        msg_parts.append(f"Fixed service revenue {_fmt_rev(rev_val)}")
    if growth_pct is not None:
        msg_parts.append(f"growth {growth_pct:+.1f}% YoY")
    if fiber_k is not None:
        msg_parts.append(f"Fiber subs {fiber_k:.0f}K")
    key_message = "; ".join(msg_parts) if msg_parts else "Insufficient data for fixed broadband assessment"

    return SegmentAnalysis(
        segment_name="Fixed Broadband",
        segment_id="fixed",
        key_metrics=key_metrics,
        changes=changes,
        trend_data=trend_data,
        competitor_comparison=comp,
        health_status=health,
        key_message=key_message,
    )


def _analyze_b2b_segment(
    financial_data: list,
    subscriber_data: list,
    comparison: list,
    target_operator: str,
) -> SegmentAnalysis:
    """Analyze B2B / Enterprise segment."""
    latest_fin = financial_data[-1] if financial_data else {}
    prev_fin = financial_data[-2] if len(financial_data) >= 2 else {}
    yoy_fin = financial_data[-5] if len(financial_data) >= 5 else {}

    latest_sub = subscriber_data[-1] if subscriber_data else {}
    prev_sub = subscriber_data[-2] if len(subscriber_data) >= 2 else {}
    yoy_sub = subscriber_data[-5] if len(subscriber_data) >= 5 else {}

    total_revenue = _safe_get(latest_fin, "total_revenue", 0)
    b2b_rev = _safe_get(latest_fin, "b2b_revenue")
    b2b_share = round((b2b_rev / total_revenue) * 100, 1) if (b2b_rev and total_revenue) else None

    key_metrics = {
        "b2b_revenue": b2b_rev,
        "b2b_growth_pct": _safe_get(latest_fin, "b2b_growth_pct"),
        "b2b_customers_k": _safe_get(latest_sub, "b2b_customers_k"),
        "b2b_share_of_revenue_pct": b2b_share,
    }

    changes = [
        _make_segment_change(
            "revenue",
            b2b_rev,
            _safe_get(prev_fin, "b2b_revenue"),
            _safe_get(yoy_fin, "b2b_revenue"),
        ),
        _make_segment_change(
            "customers",
            _safe_get(latest_sub, "b2b_customers_k"),
            _safe_get(prev_sub, "b2b_customers_k"),
            _safe_get(yoy_sub, "b2b_customers_k"),
        ),
    ]

    trend_data = {
        "revenue": [_safe_get(f, "b2b_revenue") for f in financial_data],
        "customers": [_safe_get(s, "b2b_customers_k") for s in subscriber_data],
    }

    comp = {}
    for row in comparison:
        if row.get("operator_id") != target_operator:
            comp[row.get("display_name", row.get("operator_id", "unknown"))] = {
                "b2b_revenue": _safe_get(row, "b2b_revenue"),
                "b2b_growth_pct": _safe_get(row, "b2b_growth_pct"),
                "b2b_customers_k": _safe_get(row, "b2b_customers_k"),
            }

    rev_change = changes[0].change_qoq if changes else 0
    health = _classify_segment_health(rev_change, 0)

    msg_parts = []
    if b2b_rev is not None:
        msg_parts.append(f"B2B revenue {_fmt_rev(b2b_rev)}")
    growth = key_metrics.get("b2b_growth_pct")
    if growth is not None:
        msg_parts.append(f"growth {growth:+.1f}% YoY")
    if b2b_share is not None:
        msg_parts.append(f"{b2b_share}% of total revenue")
    key_message = "; ".join(msg_parts) if msg_parts else "Insufficient data for B2B assessment"

    return SegmentAnalysis(
        segment_name="B2B",
        segment_id="b2b",
        key_metrics=key_metrics,
        changes=changes,
        trend_data=trend_data,
        competitor_comparison=comp,
        health_status=health,
        key_message=key_message,
    )


def _analyze_tv_segment(
    financial_data: list,
    subscriber_data: list,
    comparison: list,
    target_operator: str,
) -> SegmentAnalysis:
    """Analyze TV / Convergence segment."""
    latest_fin = financial_data[-1] if financial_data else {}
    prev_fin = financial_data[-2] if len(financial_data) >= 2 else {}
    yoy_fin = financial_data[-5] if len(financial_data) >= 5 else {}

    latest_sub = subscriber_data[-1] if subscriber_data else {}
    prev_sub = subscriber_data[-2] if len(subscriber_data) >= 2 else {}
    yoy_sub = subscriber_data[-5] if len(subscriber_data) >= 5 else {}

    key_metrics = {
        "tv_revenue": _safe_get(latest_fin, "tv_revenue"),
        "tv_total_k": _safe_get(latest_sub, "tv_total_k"),
        "tv_net_adds_k": _safe_get(latest_sub, "tv_net_adds_k"),
        "fmc_total_k": _safe_get(latest_sub, "fmc_total_k"),
        "fmc_penetration_pct": _safe_get(latest_sub, "fmc_penetration_pct"),
    }

    changes = [
        _make_segment_change(
            "revenue",
            _safe_get(latest_fin, "tv_revenue"),
            _safe_get(prev_fin, "tv_revenue"),
            _safe_get(yoy_fin, "tv_revenue"),
        ),
        _make_segment_change(
            "subscribers",
            _safe_get(latest_sub, "tv_total_k"),
            _safe_get(prev_sub, "tv_total_k"),
            _safe_get(yoy_sub, "tv_total_k"),
        ),
        _make_segment_change(
            "fmc_subscribers",
            _safe_get(latest_sub, "fmc_total_k"),
            _safe_get(prev_sub, "fmc_total_k"),
            _safe_get(yoy_sub, "fmc_total_k"),
        ),
    ]

    trend_data = {
        "revenue": [_safe_get(f, "tv_revenue") for f in financial_data],
        "tv_subscribers": [_safe_get(s, "tv_total_k") for s in subscriber_data],
        "fmc_subscribers": [_safe_get(s, "fmc_total_k") for s in subscriber_data],
        "fmc_penetration": [_safe_get(s, "fmc_penetration_pct") for s in subscriber_data],
    }

    comp = {}
    for row in comparison:
        if row.get("operator_id") != target_operator:
            comp[row.get("display_name", row.get("operator_id", "unknown"))] = {
                "tv_total_k": _safe_get(row, "tv_total_k"),
                "fmc_total_k": _safe_get(row, "fmc_total_k"),
                "fmc_penetration_pct": _safe_get(row, "fmc_penetration_pct"),
            }

    rev_change = changes[0].change_qoq if changes else 0
    sub_change = changes[1].change_qoq if len(changes) > 1 else 0
    health = _classify_segment_health(rev_change, sub_change)

    tv_k = key_metrics.get("tv_total_k")
    fmc_k = key_metrics.get("fmc_total_k")
    fmc_pct = key_metrics.get("fmc_penetration_pct")
    msg_parts = []
    if tv_k is not None:
        msg_parts.append(f"TV subscribers {tv_k:.0f}K")
    if fmc_k is not None:
        msg_parts.append(f"FMC {fmc_k:.0f}K")
    if fmc_pct is not None:
        msg_parts.append(f"FMC penetration {fmc_pct:.1f}%")
    key_message = "; ".join(msg_parts) if msg_parts else "Insufficient data for TV/convergence assessment"

    return SegmentAnalysis(
        segment_name="TV/Convergence",
        segment_id="tv",
        key_metrics=key_metrics,
        changes=changes,
        trend_data=trend_data,
        competitor_comparison=comp,
        health_status=health,
        key_message=key_message,
    )


def _analyze_wholesale_segment(
    financial_data: list,
    subscriber_data: list,
    comparison: list,
    target_operator: str,
) -> SegmentAnalysis:
    """Analyze Wholesale segment."""
    latest_fin = financial_data[-1] if financial_data else {}
    prev_fin = financial_data[-2] if len(financial_data) >= 2 else {}
    yoy_fin = financial_data[-5] if len(financial_data) >= 5 else {}

    total_revenue = _safe_get(latest_fin, "total_revenue", 0)
    ws_rev = _safe_get(latest_fin, "wholesale_revenue")
    ws_share = round((ws_rev / total_revenue) * 100, 1) if (ws_rev and total_revenue) else None

    key_metrics = {
        "wholesale_revenue": ws_rev,
        "wholesale_share_of_revenue_pct": ws_share,
    }

    changes = [
        _make_segment_change(
            "revenue",
            ws_rev,
            _safe_get(prev_fin, "wholesale_revenue"),
            _safe_get(yoy_fin, "wholesale_revenue"),
        ),
    ]

    trend_data = {
        "revenue": [_safe_get(f, "wholesale_revenue") for f in financial_data],
    }

    rev_change = changes[0].change_qoq if changes else 0
    health = _classify_segment_health(rev_change, 0)

    msg_parts = []
    if ws_rev is not None:
        msg_parts.append(f"Wholesale revenue {_fmt_rev(ws_rev)}")
    if ws_share is not None:
        msg_parts.append(f"{ws_share}% of total")
    key_message = "; ".join(msg_parts) if msg_parts else "Insufficient data for wholesale assessment"

    return SegmentAnalysis(
        segment_name="Wholesale",
        segment_id="wholesale",
        key_metrics=key_metrics,
        changes=changes,
        trend_data=trend_data,
        competitor_comparison={},
        health_status=health,
        key_message=key_message,
    )


def _classify_segment_health(rev_change: float, sub_change: float) -> str:
    """Classify segment health status based on revenue and subscriber trends."""
    if rev_change > 2 and sub_change >= 0:
        return "strong"
    elif rev_change < -3 or sub_change < -3:
        if rev_change < -5 or sub_change < -5:
            return "critical"
        return "weakening"
    return "stable"


# ============================================================================
# Network Analysis
# ============================================================================

def _analyze_network(
    db: TelecomDatabase,
    market: str,
    target_operator: str,
    financial_data: list,
    subscriber_data: list,
    management_commentary: list,
    intelligence_events: list,
    latest_cq: str,
    market_config: MarketConfig = None,
) -> NetworkAnalysis:
    """Analyze network infrastructure for the target operator."""
    try:
        net_data = db.get_network_data(target_operator)
    except Exception:
        net_data = {}

    if not net_data:
        return NetworkAnalysis()

    technology_mix = net_data.get("technology_mix", {}) or {}
    quality_scores = net_data.get("quality_scores", {}) or {}

    coverage = {}
    if net_data.get("five_g_coverage_pct") is not None:
        coverage["5g"] = net_data["five_g_coverage_pct"]
    if net_data.get("four_g_coverage_pct") is not None:
        coverage["4g"] = net_data["four_g_coverage_pct"]

    # Determine investment direction from capex trends
    investment_direction = "stable"
    if financial_data and len(financial_data) >= 2:
        latest_capex = _safe_get(financial_data[-1], "capex")
        prev_capex = _safe_get(financial_data[-2], "capex")
        if latest_capex is not None and prev_capex is not None:
            capex_change = _safe_pct_change(latest_capex, prev_capex)
            if capex_change > 3:
                investment_direction = "increasing"
            elif capex_change < -3:
                investment_direction = "decreasing"

    # --- Enhanced homepass_vs_connect (#1) ---
    homepass_vs_connect = _build_homepass_vs_connect(net_data, subscriber_data)

    # --- vs_competitors (#4) ---
    vs_competitors = _build_vs_competitors(db, market, target_operator, latest_cq, net_data)

    # --- cost_impact (#7) ---
    cost_impact = _build_cost_impact(financial_data, net_data, market_config, target_operator)

    # --- controlled_vs_resale (#2) ---
    controlled_vs_resale = _build_controlled_vs_resale(net_data, market_config, target_operator)

    # --- evolution_strategy (#3) ---
    evolution_strategy = _build_evolution_strategy(
        technology_mix, net_data, intelligence_events, market_config, target_operator,
    )

    # --- consumer_impact (#5) ---
    consumer_impact = _build_consumer_impact(
        coverage, net_data, subscriber_data, quality_scores, market_config, target_operator,
    )

    # --- b2b_impact (#6) ---
    b2b_impact = _build_b2b_impact(
        technology_mix, subscriber_data, financial_data, market_config, target_operator,
    )

    return NetworkAnalysis(
        technology_mix=technology_mix,
        controlled_vs_resale=controlled_vs_resale,
        coverage=coverage,
        quality_scores=quality_scores,
        homepass_vs_connect=homepass_vs_connect,
        evolution_strategy=evolution_strategy,
        investment_direction=investment_direction,
        vs_competitors=vs_competitors,
        consumer_impact=consumer_impact,
        b2b_impact=b2b_impact,
        cost_impact=cost_impact,
    )


def _build_homepass_vs_connect(net_data: dict, subscriber_data: list) -> dict:
    """Enhanced homepass vs connect with penetration ratios (#1)."""
    hvc = {}
    fiber_homepass = net_data.get("fiber_homepass_k")
    cable_homepass = net_data.get("cable_homepass_k")
    if fiber_homepass is not None:
        hvc["fiber_homepass_k"] = fiber_homepass
    if cable_homepass is not None:
        hvc["cable_homepass_k"] = cable_homepass

    # Connected subscribers from network_infrastructure or subscriber_quarterly
    latest_sub = subscriber_data[-1] if subscriber_data else {}
    fiber_connected = net_data.get("fiber_connected_k") or _safe_get(latest_sub, "broadband_fiber_k")
    cable_connected = _safe_get(latest_sub, "broadband_cable_k")

    if fiber_connected is not None:
        hvc["fiber_connected_k"] = fiber_connected
    if cable_connected is not None:
        hvc["cable_connected_k"] = cable_connected

    # Penetration ratios
    if fiber_homepass and fiber_connected:
        hvc["fiber_penetration_pct"] = round((fiber_connected / fiber_homepass) * 100, 1)
    if cable_homepass and cable_connected:
        hvc["cable_penetration_pct"] = round((cable_connected / cable_homepass) * 100, 1)

    return hvc


def _build_vs_competitors(
    db: TelecomDatabase, market: str, target_operator: str,
    latest_cq: str, net_data: dict,
) -> str:
    """Compare network metrics vs competitors (#4)."""
    if not latest_cq:
        return ""

    # Get network data for all operators in market
    try:
        operators = db.get_operators_in_market(market)
    except Exception:
        return ""

    target_5g = net_data.get("five_g_coverage_pct")
    target_fiber_hp = net_data.get("fiber_homepass_k")

    comparisons = []
    for op in operators:
        op_id = op.get("operator_id")
        if op_id == target_operator:
            continue
        try:
            op_net = db.get_network_data(op_id)
        except Exception:
            continue
        if not op_net:
            continue

        display = op.get("display_name", op_id)

        # 5G coverage comparison
        op_5g = op_net.get("five_g_coverage_pct")
        if target_5g is not None and op_5g is not None:
            gap = target_5g - op_5g
            if abs(gap) > 3:
                direction = "ahead of" if gap > 0 else "behind"
                comparisons.append(f"5G: {direction} {display} by {abs(gap):.0f}pp")

        # Fiber homepass comparison
        op_fiber_hp = op_net.get("fiber_homepass_k")
        if target_fiber_hp is not None and op_fiber_hp is not None and op_fiber_hp > 0:
            ratio = target_fiber_hp / op_fiber_hp
            if ratio > 1.5:
                comparisons.append(f"Fiber: {ratio:.1f}x more homepass than {display}")
            elif ratio < 0.67:
                comparisons.append(f"Fiber: {1/ratio:.1f}x less homepass than {display}")

    # Cap at 4 comparisons
    return "; ".join(comparisons[:4])


def _build_cost_impact(
    financial_data: list, net_data: dict,
    market_config: MarketConfig = None, target_operator: str = "",
) -> str:
    """Build cost impact assessment (#7)."""
    parts = []

    if financial_data:
        latest_fin = financial_data[-1]
        capex_ratio = _safe_get(latest_fin, "capex_to_revenue_pct")
        if capex_ratio is not None:
            if capex_ratio > 20:
                parts.append(f"High capex intensity ({capex_ratio:.1f}%)")
            elif capex_ratio > 15:
                parts.append(f"Moderate capex intensity ({capex_ratio:.1f}%)")
            else:
                parts.append(f"Capex-light model ({capex_ratio:.1f}%)")

        total_rev = _safe_get(latest_fin, "total_revenue")
        opex = _safe_get(latest_fin, "opex")
        if total_rev and opex and total_rev > 0:
            opex_ratio = (opex / total_rev) * 100
            if opex_ratio > 75:
                parts.append(f"OPEX-heavy ({opex_ratio:.0f}% of revenue)")
            elif opex_ratio < 60:
                parts.append(f"Lean operating model ({opex_ratio:.0f}% of revenue)")

        # Investment direction
        if len(financial_data) >= 2:
            latest_capex = _safe_get(latest_fin, "capex")
            prev_capex = _safe_get(financial_data[-2], "capex")
            if latest_capex is not None and prev_capex is not None:
                capex_change = _safe_pct_change(latest_capex, prev_capex)
                if capex_change > 5:
                    parts.append(f"Capex increasing ({capex_change:+.1f}% QoQ)")
                elif capex_change < -5:
                    parts.append(f"Capex decreasing ({capex_change:+.1f}% QoQ)")

    # Dual-network signal
    has_fiber = (net_data.get("fiber_homepass_k") or 0) > 0
    has_cable = (net_data.get("cable_homepass_k") or 0) > 0
    if has_fiber and has_cable:
        parts.append("Dual fixed-network cost (fiber + cable)")

    # Config overlay
    if market_config and target_operator in market_config.operator_network_enrichments:
        enrichment = market_config.operator_network_enrichments[target_operator].get("cost_impact")
        if enrichment and not parts:
            return enrichment

    return "; ".join(parts) if parts else ""


def _build_controlled_vs_resale(
    net_data: dict, market_config: MarketConfig = None, target_operator: str = "",
) -> dict:
    """Infer controlled vs resale infrastructure split (#2)."""
    result = {}

    # Data-driven: infer from infrastructure presence
    own_infra = []
    if net_data.get("cable_homepass_k"):
        own_infra.append("cable")
    if net_data.get("fiber_homepass_k"):
        own_infra.append("fiber")
    if net_data.get("five_g_coverage_pct") or net_data.get("four_g_coverage_pct"):
        own_infra.append("mobile")

    if own_infra:
        result["own_infrastructure"] = own_infra

    # Config overlay
    if market_config and target_operator in market_config.operator_network_enrichments:
        enrichment = market_config.operator_network_enrichments[target_operator].get("controlled_vs_resale")
        if enrichment:
            result["summary"] = enrichment

    return result


def _build_evolution_strategy(
    technology_mix: dict, net_data: dict,
    intelligence_events: list,
    market_config: MarketConfig = None, target_operator: str = "",
) -> dict:
    """Build network evolution strategy (#3)."""
    result = {}

    # Data-driven signals
    signals = []
    sa_status = technology_mix.get("5g_sa_status") or technology_mix.get("five_g_sa_status")
    if sa_status:
        signals.append(f"5G SA: {sa_status}")

    fiber_hp = net_data.get("fiber_homepass_k") or 0
    cable_hp = net_data.get("cable_homepass_k") or 0
    if fiber_hp > 0 and cable_hp > 0:
        ratio = fiber_hp / (fiber_hp + cable_hp)
        if ratio > 0.7:
            signals.append("Fiber-dominant fixed footprint")
        elif ratio < 0.3:
            signals.append("Cable-dominant, fiber transition underway")
        else:
            signals.append("Mixed fiber/cable footprint")
    elif fiber_hp > 0:
        signals.append("Fiber-only fixed footprint")
    elif cable_hp > 0:
        signals.append("Cable-only fixed footprint")

    docsis_pct = technology_mix.get("docsis_31_pct")
    if docsis_pct is not None:
        signals.append(f"DOCSIS 3.1 at {docsis_pct}%")

    if signals:
        result["data_signals"] = signals

    # Recent tech intelligence events
    tech_events = [
        e for e in intelligence_events
        if (e.get("category") or "").lower() == "technology"
    ][:3]
    if tech_events:
        result["recent_tech_initiatives"] = [
            e.get("title") or e.get("description", "")
            for e in tech_events
        ]

    # Config overlay
    if market_config and target_operator in market_config.operator_network_enrichments:
        enrichment = market_config.operator_network_enrichments[target_operator].get("evolution_strategy")
        if enrichment:
            result["summary"] = enrichment

    return result


def _build_consumer_impact(
    coverage: dict, net_data: dict, subscriber_data: list,
    quality_scores: dict,
    market_config: MarketConfig = None, target_operator: str = "",
) -> str:
    """Build consumer impact assessment (#5)."""
    parts = []

    # Coverage statement
    five_g_cov = coverage.get("5g")
    if five_g_cov is not None:
        if five_g_cov >= 90:
            parts.append(f"Strong 5G coverage ({five_g_cov}%)")
        elif five_g_cov >= 70:
            parts.append(f"Expanding 5G coverage ({five_g_cov}%)")
        else:
            parts.append(f"Early 5G coverage ({five_g_cov}%)")

    # Broadband mix
    latest_sub = subscriber_data[-1] if subscriber_data else {}
    fiber_k = _safe_get(latest_sub, "broadband_fiber_k") or 0
    cable_k = _safe_get(latest_sub, "broadband_cable_k") or 0
    dsl_k = _safe_get(latest_sub, "broadband_dsl_k") or 0
    total_bb = fiber_k + cable_k + dsl_k
    if total_bb > 0:
        if fiber_k / total_bb > 0.5:
            parts.append("Fiber-dominant broadband mix")
        elif cable_k / total_bb > 0.5:
            parts.append("Cable-dominant broadband mix")
        elif dsl_k / total_bb > 0.3:
            parts.append("DSL-heavy broadband mix — speed perception risk")

    # Quality scores
    if quality_scores:
        top_score_key = max(quality_scores, key=quality_scores.get) if quality_scores else None
        if top_score_key:
            parts.append(f"Network quality: {top_score_key} {quality_scores[top_score_key]}")

    # Config overlay
    if market_config and target_operator in market_config.operator_network_enrichments:
        enrichment = market_config.operator_network_enrichments[target_operator].get("consumer_impact")
        if enrichment and not parts:
            return enrichment

    return "; ".join(parts) if parts else ""


def _build_b2b_impact(
    technology_mix: dict, subscriber_data: list, financial_data: list,
    market_config: MarketConfig = None, target_operator: str = "",
) -> str:
    """Build B2B/enterprise impact assessment (#6)."""
    parts = []

    # 5G SA status → network slicing
    sa_status = technology_mix.get("5g_sa_status") or technology_mix.get("five_g_sa_status")
    if sa_status:
        if "live" in str(sa_status).lower() or "commercial" in str(sa_status).lower():
            parts.append("5G SA live — network slicing capable")
        elif "trial" in str(sa_status).lower() or "pilot" in str(sa_status).lower():
            parts.append("5G SA in trial — slicing roadmap")

    # Edge nodes
    edge_nodes = technology_mix.get("edge_nodes")
    if edge_nodes:
        parts.append(f"Edge computing: {edge_nodes} nodes")

    # Core virtualization
    core_virt_pct = technology_mix.get("core_virtualization_pct")
    if core_virt_pct is not None:
        if core_virt_pct >= 80:
            parts.append(f"Highly virtualized core ({core_virt_pct}%) — SD-WAN/NFV ready")
        elif core_virt_pct >= 50:
            parts.append(f"Partially virtualized core ({core_virt_pct}%)")

    # IoT connections
    latest_sub = subscriber_data[-1] if subscriber_data else {}
    iot_k = _safe_get(latest_sub, "iot_connections_k")
    if iot_k is not None:
        parts.append(f"IoT connections: {iot_k:.0f}K")

    # B2B revenue share
    if financial_data:
        latest_fin = financial_data[-1]
        b2b_rev = _safe_get(latest_fin, "b2b_revenue")
        total_rev = _safe_get(latest_fin, "total_revenue")
        if b2b_rev and total_rev and total_rev > 0:
            share = (b2b_rev / total_rev) * 100
            parts.append(f"B2B revenue share: {share:.0f}%")

    # Config overlay
    if market_config and target_operator in market_config.operator_network_enrichments:
        enrichment = market_config.operator_network_enrichments[target_operator].get("b2b_impact")
        if enrichment and not parts:
            return enrichment

    return "; ".join(parts) if parts else ""


# ============================================================================
# Segment Action Required & Attributions
# ============================================================================

def _derive_action_required(health_status: str, changes: list) -> str:
    """Derive action_required string from health_status + changes (#8)."""
    if not changes:
        return ""

    # Count directions
    improving = sum(1 for c in changes if c.direction == "improving")
    declining = sum(1 for c in changes if c.direction == "declining")
    significant_decline = any(
        c.direction == "declining" and c.significance == "significant" for c in changes
    )

    if health_status == "critical" or significant_decline:
        return "URGENT: Significant decline detected — immediate intervention required"
    elif health_status == "weakening" or declining > improving:
        return "MONITOR: Negative trends emerging — close tracking and corrective action needed"
    elif health_status == "strong" and improving > 0:
        return "GROW: Strong momentum — invest to accelerate growth"
    elif health_status == "strong":
        return "SUSTAIN: Healthy position — maintain current strategy"
    elif improving > declining:
        return "GROW: Improving trajectory — consider incremental investment"
    else:
        return "MAINTAIN: Stable performance — optimize current operations"


def _derive_segment_attributions(
    segment_id: str,
    changes: list,
    earnings_highlights: list,
    intelligence_events: list,
) -> list:
    """Derive attributions for a segment from earnings + intelligence + changes (#11)."""
    attributions = []

    # Keyword mapping for segment matching
    segment_keywords = {
        "mobile": ["mobile", "wireless", "cellular", "5g", "prepaid", "postpaid"],
        "fixed": ["broadband", "fixed", "fiber", "cable", "dsl", "ftth", "internet"],
        "b2b": ["b2b", "enterprise", "business", "corporate", "ict", "cloud"],
        "tv": ["tv", "television", "video", "iptv", "convergence", "content", "streaming"],
        "wholesale": ["wholesale", "mvno", "resale", "interconnect"],
    }
    keywords = segment_keywords.get(segment_id, [])

    # 1. Match earnings_call_highlights by segment keywords
    for h in earnings_highlights:
        content = (h.get("content") or "").lower()
        segment_field = (h.get("segment") or "").lower()
        if segment_id in segment_field or any(kw in content for kw in keywords):
            attributions.append(ChangeAttribution(
                attribution_type="management_explanation",
                description=h.get("content", "")[:200],
                confidence="high",
                evidence=[f"Earnings call: {h.get('speaker', 'management')}"],
                source="earnings_call",
            ))
            if len(attributions) >= 5:
                return attributions

    # 2. Match intelligence_events by keywords
    for e in intelligence_events:
        title = (e.get("title") or "").lower()
        desc = (e.get("description") or "").lower()
        if any(kw in title or kw in desc for kw in keywords):
            attributions.append(ChangeAttribution(
                attribution_type="market_change",
                description=(e.get("title") or e.get("description", ""))[:200],
                confidence="medium",
                evidence=[f"Intelligence: {e.get('source', 'market data')}"],
                source="intelligence_event",
            ))
            if len(attributions) >= 5:
                return attributions

    # 3. Auto-generate from significant metric changes
    for c in changes:
        if c.significance in ("significant", "moderate") and c.current_value is not None:
            direction_word = "increased" if c.direction == "improving" else "decreased" if c.direction == "declining" else "changed"
            attributions.append(ChangeAttribution(
                attribution_type="product_change",
                description=f"{c.metric} {direction_word} {abs(c.change_qoq):.1f}% QoQ",
                confidence="high",
                evidence=[f"Metric data: {c.metric} = {c.current_value}"],
                source="metric_analysis",
            ))
            if len(attributions) >= 5:
                return attributions

    return attributions[:5]


# ============================================================================
# Org Culture
# ============================================================================

def _build_org_culture(
    db: TelecomDatabase,
    target_operator: str,
    management_commentary: list,
    intelligence_events: list,
    financial_health: dict,
    market_config: MarketConfig = None,
) -> str:
    """Build org_culture assessment (#10)."""
    parts = []

    # 1. Leadership stability from executives
    try:
        execs = db.get_executives(target_operator)
    except Exception:
        execs = []

    current_execs = [e for e in execs if e.get("is_current")]
    c_suite = [e for e in current_execs if any(
        t in (e.get("title") or "").upper() for t in ("CEO", "CFO", "CTO", "COO", "CMO")
    )]
    if c_suite:
        tenures = []
        for e in c_suite:
            start = e.get("start_date")
            if start:
                try:
                    from datetime import date
                    start_dt = date.fromisoformat(str(start)[:10])
                    tenures.append((date.today() - start_dt).days / 365.25)
                except Exception:
                    pass
        if tenures:
            avg_tenure = sum(tenures) / len(tenures)
            if avg_tenure >= 3:
                parts.append("Stable leadership team (avg tenure >3 years)")
            elif avg_tenure < 1.5:
                parts.append("Leadership in transition (avg tenure <1.5 years)")

    # 2. Strategic orientation from management guidance
    guidance_texts = [
        c["content"].lower() for c in management_commentary
        if c.get("type") == "guidance" and c.get("content")
    ]
    if guidance_texts:
        combined = " ".join(guidance_texts)
        growth_words = sum(1 for w in ["growth", "invest", "expand", "accelerate", "innovation"] if w in combined)
        efficiency_words = sum(1 for w in ["efficiency", "cost", "savings", "optimize", "restructur"] if w in combined)
        transform_words = sum(1 for w in ["transform", "digital", "agile", "moderniz"] if w in combined)

        if transform_words >= 2:
            parts.append("Transformation-oriented strategic posture")
        elif growth_words > efficiency_words:
            parts.append("Growth-oriented strategic posture")
        elif efficiency_words > growth_words:
            parts.append("Efficiency-focused strategic posture")

    # 3. Investment posture from capex ratio
    capex_ratio = financial_health.get("capex_to_revenue_pct")
    if capex_ratio is not None:
        if capex_ratio > 20:
            parts.append("High-investment posture")
        elif capex_ratio < 12:
            parts.append("Low-investment/harvesting posture")

    # 4. Strategic initiative count from intelligence
    strategic_events = [
        e for e in intelligence_events
        if (e.get("category") or "").lower() in ("strategy", "technology", "m_and_a", "partnership")
    ]
    if len(strategic_events) >= 5:
        parts.append(f"Active strategic agenda ({len(strategic_events)} recent initiatives)")
    elif len(strategic_events) >= 2:
        parts.append(f"Moderate strategic activity ({len(strategic_events)} recent initiatives)")

    # Config overlay
    if market_config and target_operator in market_config.operator_network_enrichments:
        enrichment = market_config.operator_network_enrichments[target_operator].get("org_culture")
        if enrichment and not parts:
            return enrichment
        elif enrichment:
            parts.append(enrichment)

    return "; ".join(parts) if parts else ""


# ============================================================================
# BMC Canvas
# ============================================================================

def _build_bmc_canvas(target_operator: str,
                       market_config: MarketConfig = None) -> BMCCanvas:
    """Build a Business Model Canvas for the target operator.

    Uses MarketConfig.operator_bmc_enrichments for operator-specific data.
    Falls back to hardcoded German data when no market_config is provided.
    """
    # Default BMC for a generic telecom operator
    bmc = BMCCanvas(
        key_partners=[
            "Network equipment vendors (Ericsson, Nokia)",
            "Content providers (Netflix, Disney+)",
            "Device manufacturers (Apple, Samsung)",
            "Tower companies (Vantage Towers)",
            "MVNO partners",
        ],
        key_activities=[
            "Network operations and maintenance",
            "Customer service and support",
            "Product development and bundling",
            "Network expansion and modernization",
            "B2B solution delivery",
        ],
        key_resources=[
            "Spectrum licenses",
            "Network infrastructure (mobile, cable, fiber)",
            "Brand and customer base",
            "IT/BSS systems",
            "Skilled workforce",
        ],
        value_propositions=[
            "Reliable mobile and fixed connectivity",
            "Converged bundles (mobile + broadband + TV)",
            "Enterprise digital transformation solutions",
            "Nationwide 5G coverage",
            "Cable broadband with high speeds",
        ],
        customer_relationships=[
            "Retail stores",
            "Online self-service (app, website)",
            "Call center support",
            "Dedicated enterprise account managers",
            "Partner/reseller channels",
        ],
        channels=[
            "Physical retail stores",
            "Online shop",
            "Wholesale/partner distribution",
            "Enterprise direct sales",
            "Telesales",
        ],
        customer_segments=[
            "Consumer mobile (postpaid and prepaid)",
            "Consumer broadband and TV",
            "Small and medium enterprises",
            "Large enterprises and public sector",
            "Wholesale (MVNO, ISP)",
        ],
        cost_structure=[
            "Network OPEX (maintenance, energy, leases)",
            "Spectrum acquisition costs",
            "Personnel costs",
            "Content and device subsidies",
            "IT and digital transformation",
        ],
        revenue_streams=[
            "Mobile service revenue (voice, data)",
            "Fixed broadband subscriptions",
            "TV and content subscriptions",
            "B2B/enterprise solutions",
            "Wholesale and MVNO fees",
            "Device sales and financing",
        ],
    )

    # Apply operator-specific enrichments from MarketConfig
    if market_config and target_operator in market_config.operator_bmc_enrichments:
        enrichments = market_config.operator_bmc_enrichments[target_operator]
        for field_name in ("key_partners", "key_activities", "key_resources",
                           "value_propositions"):
            extras = enrichments.get(field_name, [])
            getattr(bmc, field_name).extend(extras)
    else:
        # Legacy fallback for backward compatibility (no market_config)
        if target_operator == "vodafone_germany":
            bmc.key_resources.append("Cable network (largest in Germany)")
            bmc.value_propositions.append("GigaCable Max ultra-fast broadband")
        elif target_operator == "deutsche_telekom":
            bmc.key_partners.append("T-Mobile US (synergies)")
            bmc.key_resources.append("Largest fiber network in Germany")
            bmc.value_propositions.append("MagentaEINS convergence platform")
        elif target_operator == "telefonica_o2":
            bmc.value_propositions.append("Value-for-money positioning")
            bmc.key_partners.append("Drillisch/1&1 (national roaming)")
        elif target_operator == "one_and_one":
            bmc.key_activities.append("Network buildout (new entrant)")
            bmc.value_propositions.append("Disruptive pricing in mobile")

    return bmc


# ============================================================================
# Exposure Points
# ============================================================================

def _identify_exposure_points(
    target_operator: str,
    financial_data: list,
    subscriber_data: list,
    network_data: dict,
    market_positions: dict,
    market_config: MarketConfig = None,
) -> list:
    """Identify strategic exposure points for the target operator.

    Uses MarketConfig.operator_exposures when available, falls back to
    data-driven analysis and legacy hardcoded logic.
    """
    exposures = []

    # 1. Use MarketConfig exposures if available
    if market_config and target_operator in market_config.operator_exposures:
        for exp_data in market_config.operator_exposures[target_operator]:
            exposures.append(ExposurePoint(
                trigger_action=exp_data["trigger_action"],
                side_effect=exp_data["side_effect"],
                attack_vector=exp_data["attack_vector"],
                severity=exp_data.get("severity", "medium"),
                evidence=exp_data.get("evidence", []),
            ))
    else:
        # Legacy fallback: hardcoded Vodafone-specific or generic analysis
        if target_operator == "vodafone_germany":
            exposures.append(ExposurePoint(
                trigger_action="1&1 building own mobile network and migrating users off Vodafone wholesale",
                side_effect="Loss of wholesale revenue as 1&1 users migrate to own network",
                attack_vector="1&1 positions as independent operator with competitive pricing",
                severity="high",
                evidence=["1&1 new entrant in Germany market", "Building Open RAN network"],
            ))

    # 2. Data-driven exposure detection (always runs)
    if financial_data and len(financial_data) >= 2:
        latest_fin = financial_data[-1]
        prev_fin = financial_data[-2]
        rev_change = _safe_pct_change(
            _safe_get(latest_fin, "total_revenue"),
            _safe_get(prev_fin, "total_revenue"),
        )
        if rev_change < -2:
            exposures.append(ExposurePoint(
                trigger_action="Declining revenue trend",
                side_effect="Weakening competitive position",
                attack_vector="Competitors gaining share during revenue decline",
                severity="medium",
                evidence=[f"Revenue declined {rev_change:.1f}% QoQ"],
            ))

    # 3. Only add generic exposure if no specific ones and revenue is declining
    if not exposures and financial_data and len(financial_data) >= 2:
        latest_fin = financial_data[-1]
        prev_fin = financial_data[-2]
        rev_change = _safe_pct_change(
            _safe_get(latest_fin, "total_revenue"),
            _safe_get(prev_fin, "total_revenue"),
        )
        if rev_change is not None and rev_change < 0:
            exposures.append(ExposurePoint(
                trigger_action="Intensifying market competition",
                side_effect="Pressure on margins and market share",
                attack_vector="Price competition from challengers",
                severity="medium",
                evidence=["Competitive telecom market dynamics"],
            ))

    return exposures


# ============================================================================
# Strengths & Weaknesses
# ============================================================================

def _derive_strengths_weaknesses(
    db: TelecomDatabase,
    market: str,
    target_operator: str,
    latest_cq: str,
    financial_health: dict,
    market_positions: dict,
    network: NetworkAnalysis,
) -> tuple:
    """Derive strengths and weaknesses from competitive scores and operational data.

    Returns (strengths_list, weaknesses_list).
    """
    strengths = []
    weaknesses = []

    # 1. Analyze competitive scores
    if latest_cq:
        try:
            all_scores = db.get_competitive_scores(market, latest_cq)
        except Exception:
            all_scores = []

        if all_scores:
            # Auto-detect score scale: if max score <= 10, data is on 1-10 scale
            all_vals = [r.get("score") for r in all_scores if r.get("score") is not None]
            scale_factor = 10 if (all_vals and max(all_vals) <= 10) else 1

            # Compute market average per dimension (normalize case to avoid dupes)
            dim_scores = {}
            for row in all_scores:
                dim_raw = row.get("dimension", "")
                dim = dim_raw.replace("_", " ").title()  # normalize: pricing_competitiveness → Pricing Competitiveness
                score = row.get("score")
                if dim and score is not None:
                    score_norm = score * scale_factor
                    if dim not in dim_scores:
                        dim_scores[dim] = {"total": 0, "count": 0, "target": None}
                    dim_scores[dim]["total"] += score_norm
                    dim_scores[dim]["count"] += 1
                    if row.get("operator_id") == target_operator:
                        dim_scores[dim]["target"] = score_norm

            for dim, info in dim_scores.items():
                if info["target"] is not None and info["count"] > 0:
                    avg = info["total"] / info["count"]
                    if info["target"] > avg + 3:
                        strengths.append(f"{dim}: score {info['target']:.0f} (market avg {avg:.0f})")
                    elif info["target"] < avg - 3:
                        weaknesses.append(f"{dim}: score {info['target']:.0f} (market avg {avg:.0f})")

    # 2. Financial health indicators
    if financial_health:
        margin = financial_health.get("ebitda_margin_pct")
        if margin is not None:
            if margin >= 28:
                strengths.append(f"Strong EBITDA margin at {margin:.1f}%")
            elif margin < 20:
                weaknesses.append(f"Below-average EBITDA margin at {margin:.1f}%")

        rev_growing = financial_health.get("revenue_growing", False)
        if rev_growing:
            strengths.append("Revenue on growth trajectory")
        else:
            yoy = financial_health.get("revenue_yoy_pct", 0)
            if yoy < -1:
                weaknesses.append(f"Revenue declining {yoy:.1f}% YoY")

    # 3. Market position
    rev_rank = market_positions.get("revenue_rank")
    rev_share = market_positions.get("revenue_market_share_pct")
    if rev_share is not None and rev_share > 30:
        strengths.append(f"Dominant market share at {rev_share:.1f}%")
    if rev_rank is not None:
        if rev_rank <= 2:
            strengths.append(f"Top {rev_rank} in revenue market ranking")
        elif rev_rank >= 4:
            weaknesses.append(f"Ranked #{rev_rank} in revenue among competitors")

    # 4. Network strength
    coverage_5g = network.coverage.get("5g")
    if coverage_5g is not None:
        if coverage_5g >= 90:
            strengths.append(f"Extensive 5G coverage at {coverage_5g}%")
        elif coverage_5g < 70:
            weaknesses.append(f"5G coverage gap at only {coverage_5g}%")

    # Ensure at least one item in each list
    if not strengths:
        strengths.append(f"Established market presence")
    if not weaknesses:
        weaknesses.append("No critical weaknesses identified from available data")

    return strengths, weaknesses


# ============================================================================
# Overall Health Rating
# ============================================================================

def _determine_health_rating(
    financial_health: dict,
    segment_analyses: list,
    market_positions: dict,
) -> str:
    """Determine the overall health rating for the operator."""
    score = 0
    factors = 0

    # Revenue trajectory
    if financial_health:
        rev_yoy = financial_health.get("revenue_yoy_pct", 0)
        if rev_yoy > 2:
            score += 2
        elif rev_yoy > 0:
            score += 1
        elif rev_yoy > -2:
            score += 0
        else:
            score -= 1
        factors += 1

        margin = financial_health.get("ebitda_margin_pct", 0)
        if margin is not None and margin >= 35:
            score += 2
        elif margin is not None and margin >= 28:
            score += 1
        else:
            score -= 1
        factors += 1

    # Segment health
    if segment_analyses:
        for seg in segment_analyses:
            if seg.health_status == "strong":
                score += 1
            elif seg.health_status == "weakening":
                score -= 1
            elif seg.health_status == "critical":
                score -= 2
            factors += 1

    # Market position
    rev_rank = market_positions.get("revenue_rank")
    if rev_rank is not None:
        if rev_rank <= 2:
            score += 1
        factors += 1

    if factors == 0:
        return "stable"

    avg_score = score / factors
    if avg_score >= 1.0:
        return "healthy"
    elif avg_score >= 0:
        return "stable"
    elif avg_score >= -0.5:
        return "concerning"
    else:
        return "critical"


# ============================================================================
# Key Message Synthesis
# ============================================================================

def _synthesize_key_message(
    target_operator: str,
    health_rating: str,
    financial_health: dict,
    market_positions: dict,
    strengths: list,
    weaknesses: list,
    market_config=None,
) -> str:
    """Synthesize a key message summarizing the self-analysis."""
    currency = market_config.currency if market_config else "USD"
    parts = []

    # Operator identity
    rev_rank = market_positions.get("revenue_rank")
    ops_count = market_positions.get("operators_count")
    if rev_rank and ops_count:
        parts.append(f"Ranked #{rev_rank} of {ops_count} operators in market")

    # Financial trajectory
    if financial_health:
        total_rev = financial_health.get("total_revenue")
        margin = financial_health.get("ebitda_margin_pct")
        if total_rev:
            parts.append(f"revenue {_fmt_rev(total_rev, currency)}")
        if margin:
            parts.append(f"EBITDA margin {margin:.1f}%")

    # Health assessment
    health_labels = {
        "healthy": "overall healthy operations",
        "stable": "stable but facing challenges",
        "concerning": "concerning trends requiring attention",
        "critical": "critical issues demanding immediate action",
    }
    parts.append(health_labels.get(health_rating, "assessment pending"))

    # Top strength and weakness
    if strengths:
        parts.append(f"key strength: {strengths[0].split(':')[0] if ':' in strengths[0] else strengths[0]}")
    if weaknesses:
        parts.append(f"key challenge: {weaknesses[0].split(':')[0] if ':' in weaknesses[0] else weaknesses[0]}")

    return "; ".join(parts)


# ============================================================================
# SelfInsight Field Builders
# ============================================================================

_TITLE_PRIORITY = {"CEO": 0, "CFO": 1, "CTO": 2, "COO": 3, "CMO": 4}


def _title_sort_key(title: str) -> int:
    """Sort executives by C-suite importance, others last."""
    upper = title.upper()
    for key, rank in _TITLE_PRIORITY.items():
        if key in upper:
            return rank
    return 99


def _build_leadership_changes(db: TelecomDatabase, target_operator: str) -> list[dict]:
    """Build leadership_changes from executive data."""
    try:
        execs = db.get_executives(target_operator)
    except Exception:
        return []
    result = []
    for ex in execs:
        title = ex.get("title", "")
        tenure_years = None
        start = ex.get("start_date")
        if start:
            try:
                from datetime import date
                start_dt = date.fromisoformat(str(start)[:10])
                tenure_years = round((date.today() - start_dt).days / 365.25, 1)
            except Exception:
                pass
        result.append({
            "name": ex.get("name", ""),
            "title": title,
            "is_current": bool(ex.get("is_current", True)),
            "start_date": start or "",
            "background": ex.get("background", ""),
            "tenure_years": tenure_years,
        })
    result.sort(key=lambda e: _title_sort_key(e["title"]))
    return result


def _build_talent_assessment(leadership: list[dict], target_scores: dict) -> dict:
    """Assess talent quality from leadership roster + competitive capability scores."""
    current = [e for e in leadership if e.get("is_current")]
    c_suite = [e for e in current if any(
        t in (e.get("title") or "").upper() for t in ("CEO", "CFO", "CTO", "COO", "CMO")
    )]
    tenures = [e["tenure_years"] for e in current if e.get("tenure_years") is not None]
    avg_tenure = round(sum(tenures) / len(tenures), 1) if tenures else None

    key_leaders = [f"{e['name']} ({e['title']})" for e in c_suite[:5]]

    # Capability alignment from competitive scores
    capability_dims = ["Customer Service", "Enterprise Solutions", "Digital Services"]
    alignment_parts = []
    for dim in capability_dims:
        score = target_scores.get(dim)
        if score is not None:
            level = "strong" if score >= 70 else "adequate" if score >= 50 else "developing"
            alignment_parts.append(f"{dim}: {level}")

    # Overall assessment
    if avg_tenure is not None and avg_tenure >= 3 and len(c_suite) >= 3:
        assessment = "Stable, experienced leadership team"
    elif avg_tenure is not None and avg_tenure < 1.5:
        assessment = "Leadership team in transition — several recent appointments"
    elif len(c_suite) >= 2:
        assessment = "Adequate leadership coverage"
    else:
        assessment = "Limited executive visibility from available data"

    return {
        "c_suite_count": len(c_suite),
        "avg_tenure_years": avg_tenure,
        "key_leaders": key_leaders,
        "capability_alignment": alignment_parts,
        "assessment": assessment,
    }


def _build_customer_perception(
    target_scores: dict, all_op_scores: dict, market: str,
) -> dict:
    """Assess customer perception from 3 perception-related competitive dimensions."""
    focus_dims = ["Customer Service", "Brand Strength", "Pricing Competitiveness"]
    breakdown = {}
    verdicts = []

    for dim in focus_dims:
        t_score = target_scores.get(dim)
        if t_score is None:
            continue
        # Market average (all operators for this dim)
        others = [scores.get(dim) for op, scores in all_op_scores.items() if scores.get(dim) is not None]
        if not others:
            continue
        mkt_avg = sum(others) / len(others)
        gap = t_score - mkt_avg
        if gap > 3:
            verdict = "above average"
        elif gap < -3:
            verdict = "below average"
        else:
            verdict = "at average"
        verdicts.append(verdict)
        breakdown[dim] = {
            "score": round(t_score, 1),
            "market_avg": round(mkt_avg, 1),
            "gap_pp": round(gap, 1),
            "verdict": verdict,
        }

    # Overall
    if verdicts:
        above = verdicts.count("above average")
        below = verdicts.count("below average")
        if above > below:
            overall = "positive"
        elif below > above:
            overall = "negative"
        else:
            overall = "mixed"
    else:
        overall = "insufficient data"

    # Summary narrative
    parts = []
    for dim, info in breakdown.items():
        sign = "+" if info["gap_pp"] >= 0 else ""
        parts.append(f"{dim} {sign}{info['gap_pp']:.0f}pp vs market")
    summary = "; ".join(parts) if parts else "No perception data available"

    return {
        "breakdown": breakdown,
        "overall_verdict": overall,
        "summary": summary,
    }


def _build_performance_gap(
    target_scores: dict,
    all_op_scores: dict,
    market_comparison: list,
    financial_health: dict,
) -> str:
    """Identify top performance gaps vs market leader."""
    gaps = []

    # Leader = first entry in market_comparison (sorted by revenue DESC)
    leader = market_comparison[0] if market_comparison else {}
    leader_id = leader.get("operator_id", "")

    # EBITDA margin gap
    target_margin = financial_health.get("ebitda_margin_pct")
    leader_margin = leader.get("ebitda_margin_pct")
    if target_margin is not None and leader_margin is not None and leader_id:
        margin_gap = target_margin - leader_margin
        if abs(margin_gap) > 0.5:
            gaps.append(
                f"EBITDA margin gap: {margin_gap:+.1f}pp vs leader "
                f"({leader.get('display_name', leader_id)} at {leader_margin:.1f}%)"
            )

    # Revenue share gap
    total_rev_all = sum(
        c.get("total_revenue", 0) or 0 for c in market_comparison
    )
    if total_rev_all > 0:
        target_comp = next(
            (c for c in market_comparison if c.get("operator_id") == financial_health.get("operator_id")),
            None,
        )
        # Find target by checking all entries
        if target_comp is None and market_comparison:
            target_rev = financial_health.get("total_revenue")
            if target_rev:
                target_comp = next(
                    (c for c in market_comparison if abs((c.get("total_revenue") or 0) - target_rev) < 1),
                    None,
                )
        leader_share = ((leader.get("total_revenue") or 0) / total_rev_all) * 100
        if target_comp:
            target_share = ((target_comp.get("total_revenue") or 0) / total_rev_all) * 100
            share_gap = target_share - leader_share
            if abs(share_gap) > 0.5:
                gaps.append(f"Revenue share gap: {share_gap:+.1f}pp vs leader ({leader_share:.1f}%)")

    # Weakest competitive score gaps vs leader
    leader_scores = all_op_scores.get(leader_id, {})
    score_gaps = []
    for dim, t_val in target_scores.items():
        l_val = leader_scores.get(dim)
        if t_val is not None and l_val is not None:
            score_gaps.append((dim, t_val - l_val))
    score_gaps.sort(key=lambda x: x[1])
    for dim, gap in score_gaps[:2]:
        if gap < -2:
            gaps.append(f"{dim}: {gap:+.0f}pp vs leader")

    if not gaps:
        return "No significant performance gaps identified from available data"
    return "Top performance gaps: " + "; ".join(gaps[:3])


def _build_opportunity_gap(
    segment_analyses: list,
    network: NetworkAnalysis,
    market_comparison: list,
    financial_health: dict,
) -> str:
    """Identify top opportunity gaps from segment health, network, and B2B."""
    opps = []

    # 1. Segment recovery opportunities
    for seg in segment_analyses:
        if seg.health_status in ("weakening", "critical"):
            opps.append(f"{seg.segment_name} segment recovery (currently {seg.health_status})")

    # 2. FTTH migration upside
    fiber_hp = network.homepass_vs_connect.get("fiber_homepass_k") or 0
    cable_hp = network.homepass_vs_connect.get("cable_homepass_k") or 0
    if cable_hp > 0 and fiber_hp > 0:
        ratio = fiber_hp / (fiber_hp + cable_hp)
        if ratio < 0.5:
            opps.append(f"FTTH migration upside (fiber only {ratio*100:.0f}% of homepass footprint)")
    elif cable_hp > 0 and fiber_hp == 0:
        opps.append("FTTH migration upside (no fiber homepass footprint yet)")

    # 3. B2B revenue gap vs leader
    if market_comparison:
        leader = market_comparison[0]
        leader_b2b = leader.get("b2b_revenue") or 0
        # Find target
        target_rev = financial_health.get("total_revenue")
        target_comp = None
        if target_rev:
            target_comp = next(
                (c for c in market_comparison if abs((c.get("total_revenue") or 0) - target_rev) < 1),
                None,
            )
        if target_comp:
            target_b2b = target_comp.get("b2b_revenue") or 0
            if leader_b2b > 0 and target_b2b < leader_b2b * 0.8:
                gap_pct = ((leader_b2b - target_b2b) / leader_b2b) * 100
                opps.append(f"B2B revenue gap ({gap_pct:.0f}% below market leader)")

    if not opps:
        return "No significant opportunity gaps identified from available data"
    return "Top opportunity gaps: " + "; ".join(opps[:3])


def _build_strategic_review(
    management_commentary: list,
    financial_health: dict,
    strengths: list,
    weaknesses: list,
    health_rating: str,
    share_trends: dict,
) -> str:
    """Synthesize strategic review from management guidance + financial trajectory."""
    parts = []

    # 1. Management guidance
    guidance = [c for c in management_commentary if c.get("type") == "guidance"]
    if guidance:
        stmt = guidance[0]["content"]
        if len(stmt) > 200:
            cut = stmt[:200]
            last_period = cut.rfind(".")
            stmt = cut[:last_period + 1] if last_period > 80 else cut.rstrip() + "..."
        parts.append(f"Management outlook: {stmt}")

    # 2. Financial trajectory
    rev_trend = "growing" if financial_health.get("revenue_growing") else "flat/declining"
    margin = financial_health.get("ebitda_margin_pct")
    if margin is not None:
        margin_qual = "strong" if margin >= 35 else "healthy" if margin >= 28 else "under pressure"
        parts.append(f"Revenue trajectory {rev_trend}, margins {margin_qual} ({margin:.1f}%)")
    elif financial_health:
        parts.append(f"Revenue trajectory {rev_trend}")

    # 3. Execution assessment from strengths/weaknesses balance
    s_count = len(strengths)
    w_count = len(weaknesses)
    if s_count > w_count + 1:
        parts.append("Execution momentum positive — strengths outweigh weaknesses")
    elif w_count > s_count + 1:
        parts.append("Execution under pressure — weaknesses outnumber strengths")
    else:
        parts.append("Execution balanced — strengths and weaknesses roughly even")

    # 4. Key risks (from top weakness)
    if weaknesses:
        parts.append(f"Primary risk: {weaknesses[0]}")

    # Fallback when no management commentary
    if not guidance:
        health_desc = {
            "healthy": "Overall healthy position",
            "stable": "Stable operations with room for improvement",
            "concerning": "Concerning trends requiring strategic attention",
            "critical": "Critical position requiring urgent intervention",
        }
        parts.insert(0, health_desc.get(health_rating, "Assessment based on available data"))

    return ". ".join(parts)


# ============================================================================
# Main Entry Point
# ============================================================================

def analyze_self(
    db: TelecomDatabase,
    market: str,
    target_operator: str,
    target_period: str = None,
    n_quarters: int = 8,
    provenance=None,
    market_config: MarketConfig = None,
) -> SelfInsight:
    """Analyze the target operator's internal state and capabilities.

    This is Look 4 in the BLM Five Looks framework. It examines the
    target operator's financial health, segment performance, network
    infrastructure, business model, and competitive position.

    Args:
        db: TelecomDatabase instance (must be initialized).
        market: Market identifier (e.g., "germany").
        target_operator: Operator ID (e.g., "vodafone_germany").
        target_period: Optional end calendar quarter (e.g., "CQ4_2025").
            If None, uses the latest available.
        n_quarters: Number of quarters for timeseries (default 8).
        provenance: Optional provenance tracker (reserved for future use).

    Returns:
        SelfInsight dataclass with complete self-analysis results.
    """
    # ------------------------------------------------------------------
    # 1. Fetch time series data
    # ------------------------------------------------------------------
    end_cq = target_period or "CQ4_2025"

    try:
        financial_data = db.get_financial_timeseries(
            target_operator, n_quarters=n_quarters, end_cq=end_cq
        )
    except Exception:
        financial_data = []

    try:
        subscriber_data = db.get_subscriber_timeseries(
            target_operator, n_quarters=n_quarters, end_cq=end_cq
        )
    except Exception:
        subscriber_data = []

    latest_cq = _get_latest_cq(financial_data) or end_cq

    # Market comparison data
    try:
        comparison = db.get_market_comparison(market, latest_cq)
    except Exception:
        comparison = []

    # ------------------------------------------------------------------
    # 2. Financial health
    # ------------------------------------------------------------------
    financial_health = _analyze_financial_health(financial_data)

    # ------------------------------------------------------------------
    # 3. Revenue breakdown
    # ------------------------------------------------------------------
    latest_fin = financial_data[-1] if financial_data else {}
    revenue_breakdown = _compute_revenue_breakdown(latest_fin)

    # ------------------------------------------------------------------
    # 4. Market positions
    # ------------------------------------------------------------------
    market_positions = _analyze_market_positions(
        db, market, target_operator, latest_cq
    )

    # ------------------------------------------------------------------
    # 5. Segment analyses
    # ------------------------------------------------------------------
    segment_analyses = [
        _analyze_mobile_segment(financial_data, subscriber_data, comparison, target_operator),
        _analyze_fixed_segment(financial_data, subscriber_data, comparison, target_operator),
        _analyze_b2b_segment(financial_data, subscriber_data, comparison, target_operator),
        _analyze_tv_segment(financial_data, subscriber_data, comparison, target_operator),
        _analyze_wholesale_segment(financial_data, subscriber_data, comparison, target_operator),
    ]

    # ------------------------------------------------------------------
    # 5b. Management commentary from earnings calls (needed before network)
    # ------------------------------------------------------------------
    management_commentary = []
    ec_highlights = []
    try:
        ec_highlights = db.get_earnings_highlights(target_operator, latest_cq)
        seen_content: set[str] = set()
        for h in ec_highlights:
            content = h.get("content", "")
            content_key = content.strip().lower()
            if content_key in seen_content:
                continue
            seen_content.add(content_key)
            management_commentary.append({
                "segment": h.get("segment", "general"),
                "type": h.get("highlight_type", "explanation"),
                "content": content,
                "speaker": h.get("speaker", ""),
                "source_url": h.get("source_url", ""),
            })
    except Exception:
        pass

    # ------------------------------------------------------------------
    # 5c. Intelligence events (needed for network + attributions + org_culture)
    # ------------------------------------------------------------------
    intelligence_events = []
    try:
        intelligence_events = db.get_intelligence_events(
            market=market, operator_id=target_operator,
        )
    except Exception:
        pass

    # ------------------------------------------------------------------
    # 6. Network analysis (expanded with new fields)
    # ------------------------------------------------------------------
    network = _analyze_network(
        db, market, target_operator, financial_data, subscriber_data,
        management_commentary, intelligence_events, latest_cq, market_config,
    )

    # ------------------------------------------------------------------
    # 6b. Segment attributions + action_required
    # ------------------------------------------------------------------
    for seg in segment_analyses:
        seg.action_required = _derive_action_required(seg.health_status, seg.changes)
        seg.attributions = _derive_segment_attributions(
            seg.segment_id, seg.changes,
            ec_highlights,
            intelligence_events,
        )

    # ------------------------------------------------------------------
    # 7. BMC Canvas
    # ------------------------------------------------------------------
    bmc = _build_bmc_canvas(target_operator, market_config)

    # ------------------------------------------------------------------
    # 8. Exposure points
    # ------------------------------------------------------------------
    net_data_raw = {}
    try:
        net_data_raw = db.get_network_data(target_operator)
    except Exception:
        pass
    exposure_points = _identify_exposure_points(
        target_operator, financial_data, subscriber_data, net_data_raw, market_positions,
        market_config,
    )

    # ------------------------------------------------------------------
    # 9. Strengths & weaknesses
    # ------------------------------------------------------------------
    strengths, weaknesses = _derive_strengths_weaknesses(
        db, market, target_operator, latest_cq,
        financial_health, market_positions, network,
    )

    # ------------------------------------------------------------------
    # 10. Health rating & key message
    # ------------------------------------------------------------------
    health_rating = _determine_health_rating(
        financial_health, segment_analyses, market_positions
    )

    key_message = _synthesize_key_message(
        target_operator, health_rating,
        financial_health, market_positions,
        strengths, weaknesses,
        market_config=market_config,
    )

    # ------------------------------------------------------------------
    # 11. Share trends
    # ------------------------------------------------------------------
    share_trends = {}
    if market_positions.get("revenue_market_share_pct") is not None:
        share_trends["revenue_share_latest"] = market_positions["revenue_market_share_pct"]
    if market_positions.get("mobile_subscriber_share_pct") is not None:
        share_trends["mobile_share_latest"] = market_positions["mobile_subscriber_share_pct"]
    if market_positions.get("broadband_subscriber_share_pct") is not None:
        share_trends["broadband_share_latest"] = market_positions["broadband_subscriber_share_pct"]

    # ------------------------------------------------------------------
    # 12. Enrich key message with management commentary
    # ------------------------------------------------------------------
    if management_commentary:
        # Find guidance highlight to supplement key message
        guidance = [c for c in management_commentary if c["type"] == "guidance"]
        if guidance:
            outlook = guidance[0]['content']
            # Truncate at sentence boundary within 250 chars
            if len(outlook) > 250:
                cut = outlook[:250]
                # Try to cut at last period
                last_period = cut.rfind(".")
                if last_period > 100:
                    outlook = cut[:last_period + 1]
                else:
                    # Cut at last space to avoid mid-word truncation
                    last_space = cut.rfind(" ")
                    outlook = cut[:last_space] + "..." if last_space > 0 else cut + "..."
            key_message += f"; Management outlook: {outlook}"

    # ------------------------------------------------------------------
    # 12b. Populate 6 SelfInsight fields
    # ------------------------------------------------------------------
    # Restructure competitive scores into {operator_id: {dim: score}}
    all_op_scores: dict[str, dict[str, float]] = {}
    try:
        raw_scores = db.get_competitive_scores(market, latest_cq)
        all_vals = [r.get("score") for r in raw_scores if r.get("score") is not None]
        sf = 10 if (all_vals and max(all_vals) <= 10) else 1
        for row in raw_scores:
            op = row.get("operator_id", "")
            dim = row.get("dimension", "").replace("_", " ").title()
            score = row.get("score")
            if op and dim and score is not None:
                all_op_scores.setdefault(op, {})[dim] = score * sf
    except Exception:
        pass
    target_scores = all_op_scores.get(target_operator, {})

    leadership_changes = _build_leadership_changes(db, target_operator)
    talent_assessment = _build_talent_assessment(leadership_changes, target_scores)
    customer_perception = _build_customer_perception(target_scores, all_op_scores, market)
    performance_gap = _build_performance_gap(
        target_scores, all_op_scores, comparison, financial_health,
    )
    opportunity_gap = _build_opportunity_gap(
        segment_analyses, network, comparison, financial_health,
    )
    strategic_review = _build_strategic_review(
        management_commentary, financial_health,
        strengths, weaknesses, health_rating, share_trends,
    )

    # ------------------------------------------------------------------
    # 12c. Org culture (#10)
    # ------------------------------------------------------------------
    org_culture = _build_org_culture(
        db, target_operator, management_commentary,
        intelligence_events, financial_health, market_config,
    )

    # ------------------------------------------------------------------
    # 13. Assemble SelfInsight
    # ------------------------------------------------------------------
    return SelfInsight(
        financial_health=financial_health,
        revenue_breakdown=revenue_breakdown,
        market_positions=market_positions,
        share_trends=share_trends,
        segment_analyses=segment_analyses,
        network=network,
        customer_perception=customer_perception,
        leadership_changes=leadership_changes,
        talent_assessment=talent_assessment,
        bmc=bmc,
        org_culture=org_culture,
        exposure_points=exposure_points,
        strengths=strengths,
        weaknesses=weaknesses,
        management_commentary=management_commentary,
        performance_gap=performance_gap,
        opportunity_gap=opportunity_gap,
        strategic_review=strategic_review,
        health_rating=health_rating,
        key_message=key_message,
    )
