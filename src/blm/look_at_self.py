"""Look 4: Self Analysis (BMC + Capability Assessment).

Analyzes the target operator's financial health, segment performance,
network infrastructure, business model, and competitive position.
Uses the BLM methodology's "Look at Self" framework with BMC canvas
and capability assessment.
"""

from __future__ import annotations

from typing import Optional

from src.database.db import TelecomDatabase
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
        msg_parts.append(f"Mobile service revenue at EUR {rev_val}M")
    if growth_pct is not None:
        direction = "up" if growth_pct > 0 else "down"
        msg_parts.append(f"{direction} {abs(growth_pct):.1f}% YoY")
    arpu = key_metrics.get("mobile_arpu")
    if arpu is not None:
        msg_parts.append(f"ARPU EUR {arpu}")
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
        msg_parts.append(f"Fixed service revenue EUR {rev_val}M")
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
        msg_parts.append(f"B2B revenue EUR {b2b_rev}M")
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
        msg_parts.append(f"Wholesale revenue EUR {ws_rev}M")
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
    target_operator: str,
    financial_data: list,
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

    # Compute homepass vs connect if data available
    homepass_vs_connect = {}
    fiber_homepass = net_data.get("fiber_homepass_k")
    cable_homepass = net_data.get("cable_homepass_k")
    if fiber_homepass is not None:
        homepass_vs_connect["fiber_homepass_k"] = fiber_homepass
    if cable_homepass is not None:
        homepass_vs_connect["cable_homepass_k"] = cable_homepass

    return NetworkAnalysis(
        technology_mix=technology_mix,
        coverage=coverage,
        quality_scores=quality_scores,
        investment_direction=investment_direction,
        homepass_vs_connect=homepass_vs_connect,
    )


# ============================================================================
# BMC Canvas
# ============================================================================

def _build_bmc_canvas(target_operator: str) -> BMCCanvas:
    """Build a Business Model Canvas for the target operator.

    Currently provides Vodafone Germany-specific values.
    Can be extended for other operators.
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

    # Operator-specific adjustments
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
) -> list:
    """Identify strategic exposure points for the target operator."""
    exposures = []

    if target_operator == "vodafone_germany":
        # 1&1 migration impact
        exposures.append(ExposurePoint(
            trigger_action="1&1 building own mobile network and migrating users off Vodafone wholesale",
            side_effect="Loss of wholesale revenue as 1&1 users migrate to own network",
            attack_vector="1&1 positions as independent operator with competitive pricing",
            severity="high",
            evidence=["1&1 new entrant in Germany market", "Building Open RAN network"],
        ))

        # Cable technology dependency
        fiber_k = None
        cable_k = None
        if subscriber_data:
            latest_sub = subscriber_data[-1]
            fiber_k = _safe_get(latest_sub, "broadband_fiber_k")
            cable_k = _safe_get(latest_sub, "broadband_cable_k")

        if cable_k is not None and fiber_k is not None:
            if cable_k > fiber_k * 5:
                exposures.append(ExposurePoint(
                    trigger_action="Heavy reliance on cable (DOCSIS) technology while market shifts to fiber",
                    side_effect="Technology perception gap as competitors lead fiber deployment",
                    attack_vector="DT markets fiber superiority; cable seen as legacy",
                    severity="high",
                    evidence=[
                        f"Cable subs {cable_k:.0f}K vs Fiber subs {fiber_k:.0f}K",
                        "DT aggressively deploying FTTH",
                    ],
                ))

        # Low fiber penetration compared to DT
        competitors = market_positions.get("competitors", {})
        dt_data = competitors.get("deutsche_telekom", {})
        dt_bb = dt_data.get("broadband_total_k")
        if dt_bb and fiber_k is not None and fiber_k < 500:
            exposures.append(ExposurePoint(
                trigger_action="Low fiber penetration compared to Deutsche Telekom",
                side_effect="Competitive disadvantage in future-proof broadband",
                attack_vector="Customers migrating to FTTH offerings from DT",
                severity="medium",
                evidence=[f"Fiber subscribers only {fiber_k:.0f}K"],
            ))

    else:
        # Generic exposure analysis for other operators
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

    # If no specific exposures found, add a generic one based on market dynamics
    if not exposures:
        exposures.append(ExposurePoint(
            trigger_action="Intensifying market competition in Germany telecom",
            side_effect="Pressure on margins and market share",
            attack_vector="Price competition from challengers",
            severity="medium",
            evidence=["4-player market with new entrant 1&1"],
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
            # Compute market average per dimension
            dim_scores = {}
            for row in all_scores:
                dim = row.get("dimension")
                score = row.get("score")
                if dim and score is not None:
                    if dim not in dim_scores:
                        dim_scores[dim] = {"total": 0, "count": 0, "target": None}
                    dim_scores[dim]["total"] += score
                    dim_scores[dim]["count"] += 1
                    if row.get("operator_id") == target_operator:
                        dim_scores[dim]["target"] = score

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
            if margin >= 35:
                strengths.append(f"Strong EBITDA margin at {margin:.1f}%")
            elif margin < 25:
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
    if rev_rank is not None:
        if rev_rank <= 2:
            strengths.append(f"Top {rev_rank} in revenue market ranking")
        elif rev_rank >= 3:
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
        strengths.append("Established market presence in Germany")
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
) -> str:
    """Synthesize a key message summarizing the self-analysis."""
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
            parts.append(f"revenue EUR {total_rev}M")
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
# Main Entry Point
# ============================================================================

def analyze_self(
    db: TelecomDatabase,
    market: str,
    target_operator: str,
    target_period: str = None,
    n_quarters: int = 8,
    provenance=None,
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
    # 6. Network analysis
    # ------------------------------------------------------------------
    network = _analyze_network(db, target_operator, financial_data)

    # ------------------------------------------------------------------
    # 7. BMC Canvas
    # ------------------------------------------------------------------
    bmc = _build_bmc_canvas(target_operator)

    # ------------------------------------------------------------------
    # 8. Exposure points
    # ------------------------------------------------------------------
    net_data_raw = {}
    try:
        net_data_raw = db.get_network_data(target_operator)
    except Exception:
        pass
    exposure_points = _identify_exposure_points(
        target_operator, financial_data, subscriber_data, net_data_raw, market_positions
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
    # 12. Assemble SelfInsight
    # ------------------------------------------------------------------
    return SelfInsight(
        financial_health=financial_health,
        revenue_breakdown=revenue_breakdown,
        market_positions=market_positions,
        share_trends=share_trends,
        segment_analyses=segment_analyses,
        network=network,
        bmc=bmc,
        exposure_points=exposure_points,
        strengths=strengths,
        weaknesses=weaknesses,
        health_rating=health_rating,
        key_message=key_message,
    )
