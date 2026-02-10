"""Look 2: Market/Customer Analysis ($APPEALS Framework).

Analyzes market dynamics, customer segmentation, and competitive positioning
using the $APPEALS framework. This module implements the second look in the
BLM Five Looks methodology.

Input: TelecomDatabase with financial, subscriber, competitive scores data.
Output: MarketCustomerInsight dataclass.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

# Ensure project root is importable
_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.models.market import (
    MarketChange,
    CustomerSegment,
    APPEALSAssessment,
    MarketCustomerInsight,
)
from src.models.market_config import MarketConfig
from src.database.period_utils import PeriodConverter


# ============================================================================
# $APPEALS dimension mapping from competitive_scores dimension names
# ============================================================================

# Maps APPEALS dimension codes to (display_name, competitive_scores_dimensions, priority)
APPEALS_DIMENSION_MAP = {
    "$": {
        "name": "Price",
        "score_dimensions": ["Pricing Competitiveness"],
        "priority": "critical",
    },
    "A1": {
        "name": "Availability",
        "score_dimensions": ["Network Coverage"],
        "priority": "critical",
    },
    "P1": {
        "name": "Packaging",
        "score_dimensions": ["Product Innovation"],
        "priority": "important",
    },
    "P2": {
        "name": "Performance",
        "score_dimensions": ["Network Quality", "5G Deployment"],
        "priority": "critical",
    },
    "E": {
        "name": "Ease of Use",
        "score_dimensions": ["Customer Service", "Digital Services"],
        "priority": "important",
    },
    "A2": {
        "name": "Assurances",
        "score_dimensions": ["Enterprise Solutions"],
        "priority": "important",
    },
    "L": {
        "name": "Lifecycle Cost",
        "score_dimensions": ["Pricing Competitiveness"],
        "priority": "important",
    },
    "S": {
        "name": "Social/Brand",
        "score_dimensions": ["Brand Strength", "Sustainability"],
        "priority": "nice_to_have",
    },
}

# Customer segment definitions for German telecom market
GERMAN_TELECOM_SEGMENTS = [
    {
        "segment_name": "Consumer High-End",
        "segment_type": "consumer",
        "unmet_needs": [
            "Premium 5G standalone experiences",
            "Ultra-low latency gaming and VR",
        ],
        "pain_points": [
            "Network congestion in urban areas",
            "Limited premium content bundles",
        ],
        "purchase_decision_factors": [
            "Network quality",
            "5G coverage",
            "Brand prestige",
            "Premium device availability",
        ],
    },
    {
        "segment_name": "Consumer Mainstream",
        "segment_type": "consumer",
        "unmet_needs": [
            "Better value convergent bundles",
            "Transparent pricing without hidden fees",
        ],
        "pain_points": [
            "Complex tariff structures",
            "Long contract lock-in periods",
        ],
        "purchase_decision_factors": [
            "Price-performance ratio",
            "Network reliability",
            "Bundle offers",
            "Contract flexibility",
        ],
    },
    {
        "segment_name": "Consumer Price-Sensitive",
        "segment_type": "consumer",
        "unmet_needs": [
            "Affordable unlimited data plans",
            "No-contract flexibility",
        ],
        "pain_points": [
            "Data caps at low price points",
            "Poor customer service at budget brands",
        ],
        "purchase_decision_factors": [
            "Monthly cost",
            "Data allowance",
            "No-contract options",
        ],
    },
    {
        "segment_name": "Consumer Youth",
        "segment_type": "consumer",
        "unmet_needs": [
            "Social media and streaming-optimized plans",
            "eSIM and digital-first experience",
        ],
        "pain_points": [
            "Expensive data top-ups",
            "Outdated app experiences",
        ],
        "purchase_decision_factors": [
            "Data volume",
            "App experience",
            "Social media bundles",
            "Price",
        ],
    },
    {
        "segment_name": "Enterprise Large",
        "segment_type": "enterprise",
        "unmet_needs": [
            "End-to-end managed SD-WAN",
            "Private 5G network solutions",
            "Multi-cloud connectivity",
        ],
        "pain_points": [
            "Complex multi-vendor management",
            "Slow provisioning times",
            "Lack of integrated security",
        ],
        "purchase_decision_factors": [
            "SLA guarantees",
            "Global coverage",
            "Security certifications",
            "Total cost of ownership",
            "Dedicated account management",
        ],
    },
    {
        "segment_name": "Enterprise SME",
        "segment_type": "enterprise",
        "unmet_needs": [
            "Simple all-in-one business connectivity",
            "Affordable cloud and collaboration tools",
        ],
        "pain_points": [
            "IT resource constraints",
            "Complex B2B pricing",
            "Poor onboarding experience",
        ],
        "purchase_decision_factors": [
            "Simplicity",
            "Price",
            "Bundled IT services",
            "Local support",
        ],
    },
    {
        "segment_name": "Wholesale MVNO",
        "segment_type": "wholesale",
        "unmet_needs": [
            "Flexible wholesale pricing models",
            "Access to 5G network capabilities",
        ],
        "pain_points": [
            "Limited network differentiation",
            "Dependency on host MNO roadmap",
        ],
        "purchase_decision_factors": [
            "Wholesale rate",
            "Network quality access",
            "API availability",
            "Contract flexibility",
        ],
    },
]


def _safe_pct_change(new_val, old_val):
    """Calculate percentage change, returning None if inputs are invalid."""
    if new_val is None or old_val is None or old_val == 0:
        return None
    return round((new_val - old_val) / abs(old_val) * 100, 2)


def _safe_get(d: dict, key: str, default=None):
    """Safely get value from dict, treating None as missing."""
    val = d.get(key)
    return val if val is not None else default


def _determine_latest_quarter(db, market: str, target_period: str = None) -> str:
    """Determine the latest calendar quarter with data.

    If target_period is provided, use it. Otherwise, find the latest
    quarter that has financial data for operators in the market.
    """
    if target_period:
        return target_period

    # Query for the latest quarter with financial data
    sql = """
        SELECT f.calendar_quarter
        FROM financial_quarterly f
        JOIN operators o ON o.operator_id = f.operator_id
        WHERE o.market = ? AND o.is_active = 1
        ORDER BY f.period_start DESC
        LIMIT 1
    """
    row = db.conn.execute(sql, [market]).fetchone()
    if row:
        return dict(row)["calendar_quarter"]

    # Fallback: generate from current date
    converter = PeriodConverter()
    timeline = converter.generate_timeline(n_quarters=1)
    return timeline[0]


def _get_previous_quarter(calendar_quarter: str) -> str:
    """Get the previous calendar quarter string. CQ1_2025 -> CQ4_2024."""
    import re
    match = re.match(r'CQ(\d)_(\d{4})', calendar_quarter)
    if not match:
        return calendar_quarter
    q = int(match.group(1))
    y = int(match.group(2))
    if q == 1:
        return f"CQ4_{y - 1}"
    return f"CQ{q - 1}_{y}"


def _get_yoy_quarter(calendar_quarter: str) -> str:
    """Get the year-over-year comparison quarter. CQ4_2025 -> CQ4_2024."""
    import re
    match = re.match(r'CQ(\d)_(\d{4})', calendar_quarter)
    if not match:
        return calendar_quarter
    q = int(match.group(1))
    y = int(match.group(2))
    return f"CQ{q}_{y - 1}"


# ============================================================================
# Market Snapshot
# ============================================================================

def _build_market_snapshot(db, market: str, latest_cq: str,
                           provenance=None, market_config: MarketConfig = None) -> dict:
    """Build the market snapshot dict with totals and per-operator shares."""
    comparison = db.get_market_comparison(market, latest_cq)

    if not comparison:
        return {
            "calendar_quarter": latest_cq,
            "total_revenue": "N/A",
            "total_subscribers": "N/A",
            "market_shares": {},
            "penetration_rates": {},
            "operator_count": 0,
        }

    total_revenue = 0.0
    total_mobile_subs = 0.0
    total_broadband_subs = 0.0
    market_shares = {}
    operator_revenues = {}

    for row in comparison:
        op_id = row["operator_id"]
        rev = _safe_get(row, "total_revenue", 0)
        mobile_k = _safe_get(row, "mobile_total_k", 0)
        bb_k = _safe_get(row, "broadband_total_k", 0)

        total_revenue += rev
        total_mobile_subs += mobile_k
        total_broadband_subs += bb_k
        operator_revenues[op_id] = rev

    # Compute market shares
    for op_id, rev in operator_revenues.items():
        if total_revenue > 0:
            market_shares[op_id] = round(rev / total_revenue * 100, 1)
        else:
            market_shares[op_id] = 0

    # Compute penetration rates using market population
    population_k = market_config.population_k if market_config else 84000
    penetration_rates = {
        "mobile_penetration_pct": round(
            total_mobile_subs / population_k * 100, 1
        ) if total_mobile_subs > 0 else "N/A",
        "broadband_penetration_pct": round(
            total_broadband_subs / population_k * 100, 1
        ) if total_broadband_subs > 0 else "N/A",
    }

    snapshot = {
        "calendar_quarter": latest_cq,
        "total_revenue": round(total_revenue, 1),
        "total_mobile_subscribers_k": round(total_mobile_subs, 1),
        "total_broadband_subscribers_k": round(total_broadband_subs, 1),
        "market_shares": market_shares,
        "penetration_rates": penetration_rates,
        "operator_count": len(comparison),
    }

    if provenance:
        provenance.track(
            value=round(total_revenue, 1),
            field_name="market_total_revenue",
            period=latest_cq,
            unit="EUR millions",
        )

    return snapshot


# ============================================================================
# Market Changes Detection
# ============================================================================

def _detect_market_changes(db, market: str, target_operator: str,
                            latest_cq: str, n_quarters: int,
                            provenance=None) -> list[MarketChange]:
    """Detect significant market changes by comparing quarters."""
    changes = []

    prev_cq = _get_previous_quarter(latest_cq)
    yoy_cq = _get_yoy_quarter(latest_cq)

    # Get current and previous quarter data for all operators
    current_data = db.get_market_comparison(market, latest_cq)
    prev_data = db.get_market_comparison(market, prev_cq)
    yoy_data = db.get_market_comparison(market, yoy_cq)

    if not current_data:
        return changes

    # Build lookup dicts
    prev_lookup = {row["operator_id"]: row for row in prev_data} if prev_data else {}
    yoy_lookup = {row["operator_id"]: row for row in yoy_data} if yoy_data else {}

    for row in current_data:
        op_id = row["operator_id"]
        display_name = row.get("display_name", op_id)

        # --- Revenue change analysis ---
        prev_row = prev_lookup.get(op_id, {})
        yoy_row = yoy_lookup.get(op_id, {})

        current_rev = _safe_get(row, "total_revenue")
        prev_rev = _safe_get(prev_row, "total_revenue")
        yoy_rev = _safe_get(yoy_row, "total_revenue")

        # QoQ revenue change
        qoq_rev_change = _safe_pct_change(current_rev, prev_rev)
        if qoq_rev_change is not None and abs(qoq_rev_change) > 5:
            direction = "increase" if qoq_rev_change > 0 else "decline"
            is_target = (op_id == target_operator)
            if is_target:
                impact = "opportunity" if qoq_rev_change > 0 else "threat"
            else:
                # Competitor growing fast is a threat; competitor declining may be opportunity
                impact = "threat" if qoq_rev_change > 0 else "opportunity"

            changes.append(MarketChange(
                change_type="pricing",
                description=(
                    f"{display_name} revenue {direction} {abs(qoq_rev_change):.1f}% QoQ "
                    f"(EUR {current_rev:.0f}M vs {prev_rev:.0f}M)"
                ),
                source="peer_driven",
                time_horizon="short_term",
                impact_type=impact,
                impact_description=(
                    f"Significant revenue {direction} signals "
                    f"{'positive momentum' if qoq_rev_change > 0 else 'market pressure'}"
                ),
                severity="high" if abs(qoq_rev_change) > 10 else "medium",
                evidence=[f"QoQ revenue change: {qoq_rev_change:+.1f}%"],
            ))

        # YoY revenue change
        yoy_rev_change = _safe_pct_change(current_rev, yoy_rev)
        if yoy_rev_change is not None and abs(yoy_rev_change) > 5:
            direction = "growth" if yoy_rev_change > 0 else "decline"
            is_target = (op_id == target_operator)
            if is_target:
                impact = "opportunity" if yoy_rev_change > 0 else "threat"
            else:
                impact = "threat" if yoy_rev_change > 0 else "opportunity"

            changes.append(MarketChange(
                change_type="pricing",
                description=(
                    f"{display_name} revenue {direction} {abs(yoy_rev_change):.1f}% YoY"
                ),
                source="peer_driven",
                time_horizon="medium_term",
                impact_type=impact,
                impact_description=(
                    f"Year-over-year {direction} indicates "
                    f"{'sustained growth trajectory' if yoy_rev_change > 0 else 'structural challenge'}"
                ),
                severity="high" if abs(yoy_rev_change) > 10 else "medium",
                evidence=[f"YoY revenue change: {yoy_rev_change:+.1f}%"],
            ))

        # --- Subscriber change analysis ---
        current_mobile = _safe_get(row, "mobile_total_k")
        prev_mobile = _safe_get(prev_row, "mobile_total_k")

        qoq_sub_change = _safe_pct_change(current_mobile, prev_mobile)
        if qoq_sub_change is not None and abs(qoq_sub_change) > 10:
            direction = "gain" if qoq_sub_change > 0 else "loss"
            is_target = (op_id == target_operator)
            if is_target:
                impact = "opportunity" if qoq_sub_change > 0 else "threat"
            else:
                impact = "threat" if qoq_sub_change > 0 else "opportunity"

            changes.append(MarketChange(
                change_type="technology",
                description=(
                    f"{display_name} mobile subscriber {direction} "
                    f"{abs(qoq_sub_change):.1f}% QoQ"
                ),
                source="peer_driven",
                time_horizon="short_term",
                impact_type=impact,
                impact_description=(
                    f"Subscriber {direction} indicates "
                    f"{'market share gain' if qoq_sub_change > 0 else 'churn pressure'}"
                ),
                severity="high" if abs(qoq_sub_change) > 20 else "medium",
                evidence=[f"QoQ subscriber change: {qoq_sub_change:+.1f}%"],
            ))

        # --- ARPU / pricing shifts ---
        current_arpu = _safe_get(row, "mobile_arpu")
        prev_arpu = _safe_get(prev_row, "mobile_arpu")

        arpu_change = _safe_pct_change(current_arpu, prev_arpu)
        if arpu_change is not None and abs(arpu_change) > 5:
            direction = "increase" if arpu_change > 0 else "decrease"
            is_target = (op_id == target_operator)
            # ARPU increase by a competitor could signal value migration
            if is_target:
                impact = "opportunity" if arpu_change > 0 else "threat"
            else:
                impact = "both"

            changes.append(MarketChange(
                change_type="pricing",
                description=(
                    f"{display_name} mobile ARPU {direction} "
                    f"{abs(arpu_change):.1f}% QoQ (EUR {current_arpu:.1f})"
                ),
                source="peer_driven",
                time_horizon="short_term",
                impact_type=impact,
                impact_description=(
                    f"ARPU {direction} signals "
                    f"{'value-led growth' if arpu_change > 0 else 'pricing pressure'}"
                ),
                severity="medium",
                evidence=[f"ARPU change: {arpu_change:+.1f}%"],
            ))

        # --- EBITDA margin shifts ---
        current_margin = _safe_get(row, "ebitda_margin_pct")
        prev_margin = _safe_get(prev_row, "ebitda_margin_pct")

        if current_margin is not None and prev_margin is not None:
            margin_delta = current_margin - prev_margin
            if abs(margin_delta) > 2:  # >2pp shift is significant
                direction = "improvement" if margin_delta > 0 else "compression"
                is_target = (op_id == target_operator)
                if is_target:
                    impact = "opportunity" if margin_delta > 0 else "threat"
                else:
                    impact = "threat" if margin_delta > 0 else "opportunity"

                changes.append(MarketChange(
                    change_type="pricing",
                    description=(
                        f"{display_name} EBITDA margin {direction}: "
                        f"{current_margin:.1f}% vs {prev_margin:.1f}% ({margin_delta:+.1f}pp)"
                    ),
                    source="peer_driven",
                    time_horizon="medium_term",
                    impact_type=impact,
                    impact_description=(
                        f"Margin {direction} indicates "
                        f"{'operational efficiency gains' if margin_delta > 0 else 'cost pressure or investment phase'}"
                    ),
                    severity="medium",
                    evidence=[f"Margin change: {margin_delta:+.1f}pp"],
                ))

    # --- Intelligence events ---
    try:
        events = db.get_intelligence_events(market=market, days_back=365)
        for evt in events:
            category = evt.get("category", "")
            impact_type_raw = evt.get("impact_type", "neutral")

            # Map event impact to opportunity/threat for target
            if impact_type_raw == "positive":
                impact = "opportunity"
            elif impact_type_raw == "negative":
                impact = "threat"
            else:
                impact = "both"

            # If event is about a competitor, flip the impact
            evt_operator = evt.get("operator_id")
            if evt_operator and evt_operator != target_operator:
                if impact == "opportunity":
                    impact = "threat"
                elif impact == "threat":
                    impact = "opportunity"

            changes.append(MarketChange(
                change_type=_map_event_category(category),
                description=evt.get("title", "Unknown event"),
                source="external_player_driven" if category in (
                    "regulatory", "economic", "social", "technology"
                ) else "peer_driven",
                time_horizon="medium_term",
                impact_type=impact,
                impact_description=evt.get("description", ""),
                severity=evt.get("severity", "medium"),
                evidence=[evt.get("source_url", "")] if evt.get("source_url") else [],
            ))
    except Exception:
        # Intelligence events are optional; don't fail if unavailable
        pass

    return changes


def _map_event_category(category: str) -> str:
    """Map intelligence event category to MarketChange change_type."""
    mapping = {
        "regulatory": "pricing",
        "economic": "pricing",
        "technology": "technology",
        "competitive": "merger",
        "new_entrant": "new_entrant",
        "substitute": "ott",
        "ott": "ott",
        "social": "pricing",
    }
    return mapping.get(category, "technology")


# ============================================================================
# Customer Segmentation
# ============================================================================

def _build_customer_segments(db, market: str, target_operator: str,
                              latest_cq: str, provenance=None,
                              market_config: MarketConfig = None) -> list[CustomerSegment]:
    """Build customer segment analysis using subscriber data."""
    comparison = db.get_market_comparison(market, latest_cq)

    # Compute aggregate subscriber data for segment sizing
    total_mobile_k = 0
    total_postpaid_k = 0
    total_prepaid_k = 0
    total_bb_k = 0
    total_b2b_k = 0
    target_mobile_k = 0
    target_postpaid_k = 0
    target_bb_k = 0
    target_b2b_k = 0

    for row in comparison:
        mobile = _safe_get(row, "mobile_total_k", 0)
        postpaid = _safe_get(row, "mobile_postpaid_k", 0)
        prepaid = _safe_get(row, "mobile_postpaid_k", 0)
        actual_prepaid = mobile - postpaid if mobile > 0 and postpaid > 0 else 0
        bb = _safe_get(row, "broadband_total_k", 0)
        b2b = _safe_get(row, "b2b_customers_k", 0)

        total_mobile_k += mobile
        total_postpaid_k += postpaid
        total_prepaid_k += actual_prepaid
        total_bb_k += bb
        total_b2b_k += b2b

        if row["operator_id"] == target_operator:
            target_mobile_k = mobile
            target_postpaid_k = postpaid
            target_bb_k = bb
            target_b2b_k = b2b

    # Use market config segments if available, fall back to hardcoded German segments
    segment_defs = market_config.customer_segments if market_config else GERMAN_TELECOM_SEGMENTS

    segments = []
    for seg_def in segment_defs:
        seg = CustomerSegment(
            segment_name=seg_def["segment_name"],
            segment_type=seg_def["segment_type"],
            unmet_needs=seg_def.get("unmet_needs", []),
            pain_points=seg_def.get("pain_points", []),
            purchase_decision_factors=seg_def.get("purchase_decision_factors", []),
        )

        # Estimate segment sizes and shares based on available data
        if seg_def["segment_type"] == "consumer":
            _populate_consumer_segment(
                seg, seg_def["segment_name"],
                total_mobile_k, total_postpaid_k, total_prepaid_k,
                target_mobile_k, target_postpaid_k,
            )
        elif seg_def["segment_type"] == "enterprise":
            _populate_enterprise_segment(
                seg, seg_def["segment_name"],
                total_b2b_k, target_b2b_k,
            )
        elif seg_def["segment_type"] == "wholesale":
            _populate_wholesale_segment(seg, total_mobile_k)

        segments.append(seg)

    return segments


def _populate_consumer_segment(seg: CustomerSegment, name: str,
                                 total_mobile_k: float,
                                 total_postpaid_k: float,
                                 total_prepaid_k: float,
                                 target_mobile_k: float,
                                 target_postpaid_k: float):
    """Populate consumer segment with estimated data."""
    # Use postpaid/prepaid mix as proxy for segment distribution
    if total_mobile_k <= 0:
        seg.size_estimate = "N/A"
        seg.our_share = "N/A"
        return

    postpaid_ratio = total_postpaid_k / total_mobile_k if total_mobile_k > 0 else 0

    if name == "Consumer High-End":
        # Approx 15% of postpaid base
        est_size = total_postpaid_k * 0.15
        seg.size_estimate = f"~{est_size / 1000:.1f}M subscribers"
        seg.growth_trend = "growing"
        if target_postpaid_k > 0:
            seg.our_share = f"~{target_postpaid_k / total_postpaid_k * 100:.0f}% of postpaid"
        seg.competitor_gaps = [
            "DT dominates with Magenta brand premium positioning",
            "Opportunity in 5G-exclusive premium bundles",
        ]
        seg.opportunity = (
            "Premium 5G and converged services for high-ARPU customers"
        )

    elif name == "Consumer Mainstream":
        est_size = total_postpaid_k * 0.55
        seg.size_estimate = f"~{est_size / 1000:.1f}M subscribers"
        seg.growth_trend = "stable"
        if target_postpaid_k > 0:
            seg.our_share = f"~{target_postpaid_k / total_postpaid_k * 100:.0f}% of postpaid"
        seg.competitor_gaps = [
            "O2 aggressive on price but weaker on network quality",
            "1&1 limited by network build-out",
        ]
        seg.opportunity = (
            "Value-for-money bundles combining mobile + broadband"
        )

    elif name == "Consumer Price-Sensitive":
        est_size = total_prepaid_k * 0.7  # 70% of prepaid market
        seg.size_estimate = f"~{est_size / 1000:.1f}M subscribers"
        seg.growth_trend = "shrinking"
        target_prepaid = target_mobile_k - target_postpaid_k
        if total_prepaid_k > 0 and target_prepaid > 0:
            seg.our_share = f"~{target_prepaid / total_prepaid_k * 100:.0f}% of prepaid"
        seg.competitor_gaps = [
            "1&1 and O2 sub-brands dominate this space",
        ]
        seg.opportunity = (
            "Selective prepaid-to-postpaid migration campaigns"
        )

    elif name == "Consumer Youth":
        est_size = total_mobile_k * 0.12  # ~12% of total
        seg.size_estimate = f"~{est_size / 1000:.1f}M subscribers"
        seg.growth_trend = "growing"
        if target_mobile_k > 0 and total_mobile_k > 0:
            seg.our_share = f"~{target_mobile_k / total_mobile_k * 100:.0f}% overall"
        seg.competitor_gaps = [
            "Lack of digital-native sub-brands across operators",
        ]
        seg.opportunity = (
            "Digital-first sub-brand or youth-targeted bundles"
        )


def _populate_enterprise_segment(seg: CustomerSegment, name: str,
                                   total_b2b_k: float,
                                   target_b2b_k: float):
    """Populate enterprise segment with estimated data."""
    if name == "Enterprise Large":
        seg.size_estimate = (
            f"~{total_b2b_k * 0.05:.0f}K customers (top 5%)"
            if total_b2b_k > 0 else "N/A"
        )
        seg.growth_trend = "growing"
        if target_b2b_k > 0 and total_b2b_k > 0:
            seg.our_share = f"~{target_b2b_k / total_b2b_k * 100:.0f}% of B2B base"
        seg.competitor_gaps = [
            "DT dominates with T-Systems for large enterprise ICT",
            "Opportunity in cloud and security managed services",
        ]
        seg.opportunity = (
            "Managed connectivity + cloud services for digital transformation"
        )

    elif name == "Enterprise SME":
        seg.size_estimate = (
            f"~{total_b2b_k * 0.95:.0f}K customers"
            if total_b2b_k > 0 else "N/A"
        )
        seg.growth_trend = "stable"
        if target_b2b_k > 0 and total_b2b_k > 0:
            seg.our_share = f"~{target_b2b_k / total_b2b_k * 100:.0f}% of B2B base"
        seg.competitor_gaps = [
            "Most operators lack simplified SME bundles",
        ]
        seg.opportunity = (
            "Simple all-in-one business packages with digital tools"
        )


def _populate_wholesale_segment(seg: CustomerSegment, total_mobile_k: float):
    """Populate wholesale segment with estimated data."""
    # MVNOs typically carry 10-15% of total mobile subscribers in Germany
    mvno_est = total_mobile_k * 0.12 if total_mobile_k > 0 else 0
    seg.size_estimate = f"~{mvno_est / 1000:.1f}M MVNO subscribers" if mvno_est > 0 else "N/A"
    seg.growth_trend = "stable"
    seg.our_share = "N/A"  # Wholesale share depends on specific MVNO contracts
    seg.competitor_gaps = [
        "Host MNO network quality is key differentiator for MVNO partners",
    ]
    seg.opportunity = (
        "Expand wholesale partnerships with 5G API access"
    )


# ============================================================================
# $APPEALS Assessment
# ============================================================================

def _build_appeals_assessment(db, market: str, target_operator: str,
                                latest_cq: str,
                                provenance=None) -> list[APPEALSAssessment]:
    """Build $APPEALS assessment using competitive_scores data."""
    scores_raw = db.get_competitive_scores(market, latest_cq)

    if not scores_raw:
        # Return empty assessments with N/A when no data
        return _build_empty_appeals()

    # Build per-operator score lookup: {operator_id: {dimension: score}}
    operator_scores = {}
    for row in scores_raw:
        op_id = row["operator_id"]
        dim = row["dimension"]
        score = row["score"]
        if op_id not in operator_scores:
            operator_scores[op_id] = {}
        operator_scores[op_id][dim] = score

    assessments = []
    for dim_code, dim_info in APPEALS_DIMENSION_MAP.items():
        # Compute target score (average of mapped competitive score dimensions)
        our_raw_scores = []
        for sd in dim_info["score_dimensions"]:
            val = operator_scores.get(target_operator, {}).get(sd)
            if val is not None:
                our_raw_scores.append(val)

        # Convert 0-100 scale to 1-5 scale
        our_avg_100 = sum(our_raw_scores) / len(our_raw_scores) if our_raw_scores else 0
        our_score_5 = round(our_avg_100 / 20, 1)  # 100/20 = 5.0

        # Compute competitor scores
        competitor_scores = {}
        for op_id, op_dims in operator_scores.items():
            if op_id == target_operator:
                continue
            comp_raw = []
            for sd in dim_info["score_dimensions"]:
                val = op_dims.get(sd)
                if val is not None:
                    comp_raw.append(val)
            if comp_raw:
                comp_avg = sum(comp_raw) / len(comp_raw)
                competitor_scores[op_id] = round(comp_avg / 20, 1)

        # Gap analysis
        gap_analysis = _compute_gap_analysis(
            dim_code, dim_info["name"], our_score_5, competitor_scores
        )

        assessments.append(APPEALSAssessment(
            dimension=dim_code,
            dimension_name=dim_info["name"],
            our_score=our_score_5,
            competitor_scores=competitor_scores,
            customer_priority=dim_info["priority"],
            gap_analysis=gap_analysis,
        ))

        if provenance:
            provenance.track(
                value=our_score_5,
                field_name=f"appeals_{dim_code}_score",
                operator=target_operator,
                period=latest_cq,
            )

    return assessments


def _build_empty_appeals() -> list[APPEALSAssessment]:
    """Build APPEALS list with all 8 dimensions but no scores."""
    return [
        APPEALSAssessment(
            dimension=dim_code,
            dimension_name=dim_info["name"],
            our_score=0.0,
            competitor_scores={},
            customer_priority=dim_info["priority"],
            gap_analysis="No competitive score data available",
        )
        for dim_code, dim_info in APPEALS_DIMENSION_MAP.items()
    ]


def _compute_gap_analysis(dim_code: str, dim_name: str,
                            our_score: float,
                            competitor_scores: dict) -> str:
    """Generate a gap analysis string for a given APPEALS dimension."""
    if not competitor_scores:
        return f"No competitor data available for {dim_name}"

    max_comp = max(competitor_scores.values())
    min_comp = min(competitor_scores.values())
    avg_comp = sum(competitor_scores.values()) / len(competitor_scores)

    leader = max(competitor_scores, key=competitor_scores.get)

    if our_score >= max_comp:
        return f"Market leader in {dim_name} (score {our_score}/5.0)"
    elif our_score >= avg_comp:
        gap = max_comp - our_score
        return (
            f"Above average in {dim_name} but {gap:.1f} points behind "
            f"leader ({leader}: {max_comp}/5.0)"
        )
    else:
        gap = avg_comp - our_score
        return (
            f"Below market average in {dim_name} by {gap:.1f} points. "
            f"Leader: {leader} ({max_comp}/5.0)"
        )


# ============================================================================
# Market Outlook & Key Message
# ============================================================================

def _determine_market_outlook(snapshot: dict, changes: list[MarketChange],
                                target_operator: str) -> str:
    """Determine overall market outlook: favorable, challenging, or mixed."""
    if not changes:
        return "mixed"

    opportunity_count = sum(
        1 for c in changes if c.impact_type == "opportunity"
    )
    threat_count = sum(
        1 for c in changes if c.impact_type == "threat"
    )
    both_count = sum(
        1 for c in changes if c.impact_type == "both"
    )

    total = opportunity_count + threat_count + both_count
    if total == 0:
        return "mixed"

    opp_ratio = (opportunity_count + both_count * 0.5) / total

    if opp_ratio >= 0.6:
        return "favorable"
    elif opp_ratio <= 0.3:
        return "challenging"
    return "mixed"


def _generate_key_message(snapshot: dict, changes: list[MarketChange],
                            segments: list[CustomerSegment],
                            appeals: list[APPEALSAssessment],
                            target_operator: str,
                            market_outlook: str) -> str:
    """Generate a concise key message summarizing the market analysis."""
    # Count opportunities and threats
    opportunities = [c for c in changes if c.impact_type == "opportunity"]
    threats = [c for c in changes if c.impact_type == "threat"]

    total_rev = snapshot.get("total_revenue", "N/A")
    market_shares = snapshot.get("market_shares", {})
    our_share = market_shares.get(target_operator, "N/A")

    # Find APPEALS strengths and weaknesses
    strengths = [a for a in appeals if a.our_score >= 4.0]
    weaknesses = [a for a in appeals if 0 < a.our_score < 3.0]

    parts = []

    if total_rev != "N/A":
        parts.append(
            f"German telecom market totals EUR {total_rev}M in quarterly revenue"
        )

    if our_share != "N/A":
        parts.append(
            f"{target_operator} holds {our_share}% market share"
        )

    if strengths:
        strength_names = [s.dimension_name for s in strengths[:2]]
        parts.append(f"competitive strengths in {', '.join(strength_names)}")

    if weaknesses:
        weak_names = [w.dimension_name for w in weaknesses[:2]]
        parts.append(f"gaps in {', '.join(weak_names)}")

    outlook_desc = {
        "favorable": "Market outlook is favorable with more opportunities than threats",
        "challenging": "Market faces significant competitive headwinds",
        "mixed": "Market presents a balanced mix of opportunities and challenges",
    }
    parts.append(outlook_desc.get(market_outlook, ""))

    return "; ".join(p for p in parts if p) + "."


def _determine_value_migration(changes: list[MarketChange],
                                 appeals: list[APPEALSAssessment]) -> str:
    """Determine customer value migration trend."""
    pricing_changes = [c for c in changes if c.change_type == "pricing"]
    if not pricing_changes:
        return "Limited data to assess value migration trends"

    arpu_increases = sum(
        1 for c in pricing_changes if "increase" in c.description.lower()
        or "growth" in c.description.lower()
    )
    arpu_decreases = sum(
        1 for c in pricing_changes if "decline" in c.description.lower()
        or "decrease" in c.description.lower()
    )

    if arpu_increases > arpu_decreases:
        return (
            "Value migration trending upward: customers willing to pay more "
            "for premium connectivity and convergent bundles. "
            "Focus on upselling and cross-selling opportunities."
        )
    elif arpu_decreases > arpu_increases:
        return (
            "Value migration trending downward: price competition intensifying. "
            "Defend high-value customers and optimize cost base."
        )
    return (
        "Value migration is mixed: some segments trending up while "
        "price-sensitive segments face pressure. "
        "Differentiated strategy by segment recommended."
    )


# ============================================================================
# Main Entry Point
# ============================================================================

def analyze_market_customer(
    db,
    market: str,
    target_operator: str,
    target_period: str = None,
    n_quarters: int = 8,
    provenance=None,
    market_config: MarketConfig = None,
) -> MarketCustomerInsight:
    """Perform Look 2: Market/Customer analysis.

    Analyzes market dynamics, detects changes, segments customers,
    and evaluates competitive positioning using the $APPEALS framework.

    Args:
        db: TelecomDatabase instance (must be initialized)
        market: Market identifier (e.g., "germany")
        target_operator: Operator ID to analyze (e.g., "vodafone_germany")
        target_period: Calendar quarter to analyze (e.g., "CQ4_2025").
                       If None, uses the latest available quarter.
        n_quarters: Number of quarters for trend analysis (default 8)
        provenance: Optional ProvenanceStore for data tracking

    Returns:
        MarketCustomerInsight with complete market/customer analysis
    """
    # Determine the latest quarter to analyze
    latest_cq = _determine_latest_quarter(db, market, target_period)

    # 1. Build market snapshot
    snapshot = _build_market_snapshot(db, market, latest_cq, provenance, market_config)

    # 2. Detect market changes
    changes = _detect_market_changes(
        db, market, target_operator, latest_cq, n_quarters, provenance
    )

    # 3. Separate opportunities and threats
    opportunities = [c for c in changes if c.impact_type == "opportunity"]
    threats = [c for c in changes if c.impact_type == "threat"]

    # 4. Build customer segments
    segments = _build_customer_segments(
        db, market, target_operator, latest_cq, provenance, market_config
    )

    # 5. Build $APPEALS assessment
    appeals = _build_appeals_assessment(
        db, market, target_operator, latest_cq, provenance
    )

    # 6. Determine market outlook
    market_outlook = _determine_market_outlook(snapshot, changes, target_operator)

    # 7. Customer value migration
    value_migration = _determine_value_migration(changes, appeals)

    # 8. Generate key message
    key_message = _generate_key_message(
        snapshot, changes, segments, appeals, target_operator, market_outlook
    )

    return MarketCustomerInsight(
        market_snapshot=snapshot,
        changes=changes,
        opportunities=opportunities,
        threats=threats,
        customer_segments=segments,
        appeals_assessment=appeals,
        customer_value_migration=value_migration,
        market_outlook=market_outlook,
        key_message=key_message,
    )
