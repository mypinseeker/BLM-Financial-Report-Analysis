"""Look 3: Competition Analysis - Porter's Five Forces + Competitor Deep Dives.

Analyzes competitive dynamics in a telecom market using Porter's Five Forces
framework and individual competitor deep dives. All data is sourced from the
TelecomDatabase; nothing is fabricated.

Usage:
    from src.database.db import TelecomDatabase
    from src.blm.look_at_competition import analyze_competition

    db = TelecomDatabase("data/telecom.db")
    db.init()
    result = analyze_competition(db, market="germany", target_operator="vodafone_germany")
"""

from __future__ import annotations

from typing import Optional

from src.database.db import TelecomDatabase
from src.database.period_utils import PeriodConverter
from src.models.competition import (
    CompetitionInsight,
    CompetitorDeepDive,
    CompetitorImplication,
    PorterForce,
)


# ============================================================================
# Public API
# ============================================================================


def analyze_competition(
    db: TelecomDatabase,
    market: str,
    target_operator: str,
    target_period: str = None,
    n_quarters: int = 8,
    provenance=None,
) -> CompetitionInsight:
    """Run the complete Look 3: Competition analysis.

    Args:
        db: Initialized TelecomDatabase instance.
        market: Market identifier (e.g., "germany").
        target_operator: Operator ID of the company being analyzed.
        target_period: Calendar quarter to focus on (e.g., "CQ4_2025").
                       Defaults to the latest available quarter.
        n_quarters: Number of quarters for time-series analysis.
        provenance: Optional provenance tracker (reserved for future use).

    Returns:
        CompetitionInsight with five forces, competitor deep dives,
        comparison table, and key message.
    """
    # Resolve the target period
    if target_period is None:
        target_period = _resolve_latest_period(db, market, n_quarters)

    # Gather operators in the market
    all_operators = db.get_operators_in_market(market)
    if not all_operators:
        return _empty_insight("No operators found in this market.")

    # Identify competitors (everyone except the target)
    competitor_ops = [
        op for op in all_operators if op["operator_id"] != target_operator
    ]

    # Gather market comparison snapshot for target period
    market_snapshot = db.get_market_comparison(market, target_period)

    # Gather competitive scores
    comp_scores = db.get_competitive_scores(market, target_period)
    scores_by_operator = _group_scores_by_operator(comp_scores)

    # Gather intelligence events (use large window to capture available data)
    intel_events = _safe_intelligence_events(db, market=market, days_back=730)

    # Build Porter's Five Forces
    five_forces = _build_five_forces(
        db, market, target_operator, target_period,
        n_quarters, all_operators, market_snapshot,
        scores_by_operator, intel_events,
    )

    # Build competitor deep dives
    competitor_analyses = {}
    for comp_op in competitor_ops:
        comp_id = comp_op["operator_id"]
        deep_dive = _build_competitor_deep_dive(
            db, comp_id, comp_op, target_operator,
            target_period, n_quarters,
            scores_by_operator.get(comp_id, {}),
            intel_events,
        )
        competitor_analyses[comp_id] = deep_dive

    # Build comparison table (includes target operator)
    comparison_table = _build_comparison_table(
        db, all_operators, target_period, n_quarters, scores_by_operator,
    )

    # Determine overall competition intensity
    overall_intensity = _assess_overall_intensity(five_forces, market_snapshot)

    # Build competitive landscape narrative
    landscape = _build_landscape_narrative(
        all_operators, market_snapshot, five_forces, overall_intensity,
    )

    # Build key message
    key_message = _build_key_message(
        market, target_operator, all_operators, market_snapshot,
        five_forces, overall_intensity,
    )

    return CompetitionInsight(
        five_forces=five_forces,
        overall_competition_intensity=overall_intensity,
        competitor_analyses=competitor_analyses,
        comparison_table=comparison_table,
        competitive_landscape=landscape,
        key_message=key_message,
    )


# ============================================================================
# Five Forces Construction
# ============================================================================


def _build_five_forces(
    db, market, target_operator, target_period, n_quarters,
    all_operators, market_snapshot, scores_by_operator, intel_events,
):
    """Build all 5 PorterForce objects."""
    return {
        "existing_competitors": _force_existing_competitors(
            db, market, target_operator, target_period,
            n_quarters, all_operators, market_snapshot,
            scores_by_operator,
        ),
        "new_entrants": _force_new_entrants(
            all_operators, intel_events, market_snapshot,
        ),
        "substitutes": _force_substitutes(intel_events),
        "supplier_power": _force_supplier_power(intel_events),
        "buyer_power": _force_buyer_power(
            db, market, target_period, n_quarters,
            all_operators, market_snapshot, intel_events,
        ),
    }


def _force_existing_competitors(
    db, market, target_operator, target_period,
    n_quarters, all_operators, market_snapshot,
    scores_by_operator,
):
    """Assess the force of existing competitors.

    Evaluates: number of comparable players, revenue distribution,
    growth rate disparity, market share concentration, and margin pressure.
    """
    factors = []
    implications = []

    # Count active players
    num_players = len(all_operators)
    factors.append({
        "name": "Number of competitors",
        "description": f"{num_players} active operators in the market",
        "impact": "high" if num_players >= 4 else "medium",
        "trend": "stable",
    })

    # Revenue concentration
    revenues = []
    for row in market_snapshot:
        rev = row.get("total_revenue")
        if rev is not None:
            revenues.append((row.get("operator_id", ""), rev))

    if revenues:
        revenues.sort(key=lambda x: x[1], reverse=True)
        total_rev = sum(r for _, r in revenues)
        if total_rev > 0:
            top_share = revenues[0][1] / total_rev * 100
            factors.append({
                "name": "Market concentration",
                "description": (
                    f"Top operator holds {top_share:.0f}% of market revenue "
                    f"(total: {total_rev:.0f}M EUR)"
                ),
                "impact": "high" if top_share > 40 else "medium",
                "trend": "stable",
            })
            implications.append(
                f"Market is {'concentrated' if top_share > 40 else 'fragmented'} "
                f"with top player at {top_share:.0f}% revenue share."
            )

    # Growth rate disparity
    growth_rates = []
    for row in market_snapshot:
        gr = row.get("service_revenue_growth_pct")
        op_id = row.get("operator_id", "")
        if gr is not None:
            growth_rates.append((op_id, gr))

    if growth_rates:
        max_gr = max(gr for _, gr in growth_rates)
        min_gr = min(gr for _, gr in growth_rates)
        disparity = max_gr - min_gr
        factors.append({
            "name": "Growth rate disparity",
            "description": (
                f"Service revenue growth ranges from {min_gr:+.1f}% to "
                f"{max_gr:+.1f}% (spread: {disparity:.1f}pp)"
            ),
            "impact": "high" if disparity > 5 else "medium",
            "trend": "increasing" if disparity > 5 else "stable",
        })

    # Margin pressure
    margins = []
    for row in market_snapshot:
        m = row.get("ebitda_margin_pct")
        op_id = row.get("operator_id", "")
        if m is not None:
            margins.append((op_id, m))

    if margins:
        avg_margin = sum(m for _, m in margins) / len(margins)
        factors.append({
            "name": "Margin pressure",
            "description": f"Average EBITDA margin: {avg_margin:.1f}%",
            "impact": "medium",
            "trend": "stable",
        })

    # Determine force level
    high_count = sum(1 for f in factors if f.get("impact") == "high")
    if high_count >= 2 or num_players >= 4:
        force_level = "high"
    elif high_count >= 1:
        force_level = "medium"
    else:
        force_level = "low"

    if not factors:
        force_level = "medium"
        factors.append({
            "name": "Competition assessment",
            "description": "Insufficient data for detailed assessment",
            "impact": "medium",
            "trend": "unknown",
        })

    return PorterForce(
        force_name="existing_competitors",
        force_level=force_level,
        key_factors=factors,
        implications=implications,
    )


def _force_new_entrants(all_operators, intel_events, market_snapshot):
    """Assess the threat of new entrants.

    Looks for new_entrant type operators and intelligence events about
    potential market entry.
    """
    factors = []
    implications = []

    # Check for new_entrant type operators already in the market
    new_entrants = [
        op for op in all_operators
        if op.get("operator_type") == "new_entrant"
    ]

    if new_entrants:
        for ne in new_entrants:
            factors.append({
                "name": f"Active new entrant: {ne.get('display_name', ne['operator_id'])}",
                "description": (
                    f"{ne.get('display_name', ne['operator_id'])} is currently "
                    f"building/expanding its network presence"
                ),
                "impact": "medium",
                "trend": "increasing",
            })
            implications.append(
                f"{ne.get('display_name', ne['operator_id'])} entering the market "
                f"may increase competitive pressure on pricing and coverage."
            )

    # Check intelligence events for new entrant signals
    new_entrant_events = [
        e for e in intel_events
        if e.get("category") in ("new_entrant", "market_entry")
    ]
    for event in new_entrant_events:
        factors.append({
            "name": event.get("title", "New entrant signal"),
            "description": event.get("description", ""),
            "impact": event.get("severity", "medium"),
            "trend": "increasing",
        })

    # Entry barriers (always relevant for telecom)
    factors.append({
        "name": "Entry barriers",
        "description": (
            "High barriers: spectrum licensing, massive capex for network build, "
            "regulatory approvals, established brand loyalty"
        ),
        "impact": "high",
        "trend": "stable",
    })
    implications.append(
        "High entry barriers (spectrum, capex, regulation) limit new competitors, "
        "but determined entrants with deep pockets can still disrupt."
    )

    # Determine force level
    if new_entrants or new_entrant_events:
        force_level = "medium"
    else:
        force_level = "low"

    return PorterForce(
        force_name="new_entrants",
        force_level=force_level,
        key_factors=factors,
        implications=implications,
    )


def _force_substitutes(intel_events):
    """Assess the threat of substitutes.

    OTT services replacing traditional telecom revenues, Wi-Fi replacing
    cellular, cloud replacing enterprise ICT, etc.
    """
    factors = []
    implications = []

    # Standard telecom substitute threats (always present)
    standard_substitutes = [
        {
            "name": "OTT messaging replaces SMS/voice",
            "description": (
                "WhatsApp, Signal, Teams replacing traditional voice/SMS revenue. "
                "OTT messaging penetration continues to grow."
            ),
            "impact": "high",
            "trend": "increasing",
        },
        {
            "name": "Streaming replaces linear TV/IPTV",
            "description": (
                "Netflix, Disney+, YouTube Premium substituting traditional "
                "TV/cable TV subscriptions."
            ),
            "impact": "medium",
            "trend": "increasing",
        },
        {
            "name": "Wi-Fi offload reduces cellular dependency",
            "description": (
                "Public and private Wi-Fi networks reduce reliance on "
                "mobile data, especially in urban areas."
            ),
            "impact": "low",
            "trend": "stable",
        },
        {
            "name": "Cloud services substitute enterprise ICT",
            "description": (
                "AWS, Azure, GCP offering direct enterprise connectivity, "
                "reducing operator B2B ICT revenue opportunity."
            ),
            "impact": "medium",
            "trend": "increasing",
        },
    ]
    factors.extend(standard_substitutes)

    implications.append(
        "OTT services continue to erode traditional voice/SMS revenue; "
        "operators must pivot toward data, connectivity, and digital services."
    )
    implications.append(
        "Streaming substitution pressures TV/IPTV bundling strategies; "
        "operators should focus on aggregation and super-bundling."
    )

    # Add intelligence-based substitute events
    substitute_events = [
        e for e in intel_events
        if e.get("category") in ("substitute", "ott", "disruptive_technology")
    ]
    for event in substitute_events:
        factors.append({
            "name": event.get("title", "Substitute threat"),
            "description": event.get("description", ""),
            "impact": event.get("severity", "medium"),
            "trend": "increasing",
        })

    # Force level: substitutes are always a significant threat in telecom
    high_count = sum(1 for f in factors if f.get("impact") == "high")
    force_level = "high" if high_count >= 1 else "medium"

    return PorterForce(
        force_name="substitutes",
        force_level=force_level,
        key_factors=factors,
        implications=implications,
    )


def _force_supplier_power(intel_events):
    """Assess supplier bargaining power.

    Equipment vendors (Huawei/Ericsson/Nokia) form an oligopoly.
    Spectrum is controlled by government. Tower companies are concentrated.
    """
    factors = [
        {
            "name": "Network equipment vendor concentration",
            "description": (
                "Oligopoly of 3 major vendors (Huawei, Ericsson, Nokia). "
                "Limited alternatives increase supplier leverage on pricing "
                "and technology roadmaps."
            ),
            "impact": "high",
            "trend": "stable",
        },
        {
            "name": "Semiconductor supply chain",
            "description": (
                "Chip supply constraints can create bottlenecks for both "
                "network equipment and consumer devices."
            ),
            "impact": "medium",
            "trend": "stable",
        },
        {
            "name": "Tower infrastructure",
            "description": (
                "Independent tower companies (e.g., Vantage Towers, GD Towers) "
                "have pricing power for site rentals and co-location."
            ),
            "impact": "medium",
            "trend": "increasing",
        },
        {
            "name": "Fiber infrastructure suppliers",
            "description": (
                "Fiber cable and deployment contractors influence capex "
                "for FTTH rollout programs."
            ),
            "impact": "medium",
            "trend": "stable",
        },
    ]

    implications = [
        "Vendor oligopoly limits negotiation leverage; multi-vendor strategies "
        "and Open RAN initiatives can help diversify supply.",
        "Tower company independence increases site rental costs; operators "
        "should evaluate infrastructure-sharing arrangements.",
    ]

    # Check intelligence events for supplier-related signals
    supplier_events = [
        e for e in intel_events
        if e.get("category") in ("supplier", "supply_chain", "vendor")
    ]
    for event in supplier_events:
        factors.append({
            "name": event.get("title", "Supplier event"),
            "description": event.get("description", ""),
            "impact": event.get("severity", "medium"),
            "trend": "stable",
        })

    # Force level: supplier power is generally medium-high in telecom
    high_count = sum(1 for f in factors if f.get("impact") == "high")
    force_level = "high" if high_count >= 2 else "medium"

    return PorterForce(
        force_name="supplier_power",
        force_level=force_level,
        key_factors=factors,
        implications=implications,
    )


def _force_buyer_power(
    db, market, target_period, n_quarters,
    all_operators, market_snapshot, intel_events,
):
    """Assess buyer bargaining power.

    Evaluates churn rates (high churn = high buyer power), postpaid/prepaid mix,
    enterprise customer concentration, and switching costs.
    """
    factors = []
    implications = []

    # Assess from churn rates
    churn_data = []
    for row in market_snapshot:
        churn = row.get("mobile_churn_pct")
        op_id = row.get("operator_id", "")
        if churn is not None:
            churn_data.append((op_id, churn))

    if churn_data:
        avg_churn = sum(c for _, c in churn_data) / len(churn_data)
        max_churn_op, max_churn = max(churn_data, key=lambda x: x[1])
        factors.append({
            "name": "Consumer churn rates",
            "description": (
                f"Average mobile churn: {avg_churn:.2f}%/month. "
                f"Highest: {max_churn:.2f}% indicating {'high' if avg_churn > 1.5 else 'moderate'} "
                f"willingness to switch."
            ),
            "impact": "high" if avg_churn > 1.5 else "medium",
            "trend": "stable",
        })

    # Postpaid/prepaid mix (higher postpaid = lower buyer power due to contracts)
    postpaid_ratios = []
    for row in market_snapshot:
        total = row.get("mobile_total_k")
        postpaid = row.get("mobile_postpaid_k")
        if total and postpaid and total > 0:
            ratio = postpaid / total * 100
            postpaid_ratios.append((row.get("operator_id", ""), ratio))

    if postpaid_ratios:
        avg_ratio = sum(r for _, r in postpaid_ratios) / len(postpaid_ratios)
        factors.append({
            "name": "Postpaid contract mix",
            "description": (
                f"Average postpaid ratio: {avg_ratio:.0f}%. "
                f"{'High' if avg_ratio > 70 else 'Moderate'} contract lock-in "
                f"{'reduces' if avg_ratio > 70 else 'moderately constrains'} buyer mobility."
            ),
            "impact": "low" if avg_ratio > 70 else "medium",
            "trend": "stable",
        })

    # Individual consumer power is low, but collective switching matters
    factors.append({
        "name": "Individual consumer bargaining power",
        "description": (
            "Individual consumers have low bargaining power, but low "
            "switching costs (number portability, short contracts) mean "
            "they vote with their feet."
        ),
        "impact": "medium",
        "trend": "increasing",
    })

    # Enterprise customer power
    b2b_data = []
    for row in market_snapshot:
        b2b = row.get("b2b_customers_k")
        if b2b is not None:
            b2b_data.append(b2b)

    if b2b_data:
        factors.append({
            "name": "Enterprise customer concentration",
            "description": (
                "Large enterprise customers have significant bargaining power "
                "through multi-vendor strategies and competitive tenders."
            ),
            "impact": "high",
            "trend": "stable",
        })
        implications.append(
            "Enterprise customers can leverage multi-vendor strategies; "
            "differentiation through service quality and SLAs is critical."
        )

    # Regulatory influence on buyer power
    factors.append({
        "name": "Regulatory protection for buyers",
        "description": (
            "EU regulations support number portability, contract transparency, "
            "and maximum contract lengths, enhancing consumer switching ability."
        ),
        "impact": "medium",
        "trend": "increasing",
    })

    implications.append(
        "Low switching costs and regulatory support for portability mean "
        "operators must compete on value, not lock-in."
    )

    # Determine force level
    high_count = sum(1 for f in factors if f.get("impact") == "high")
    if high_count >= 2:
        force_level = "high"
    elif high_count >= 1:
        force_level = "medium"
    else:
        force_level = "low"

    return PorterForce(
        force_name="buyer_power",
        force_level=force_level,
        key_factors=factors,
        implications=implications,
    )


# ============================================================================
# Competitor Deep Dive
# ============================================================================


def _build_competitor_deep_dive(
    db, comp_id, comp_op, target_operator,
    target_period, n_quarters, comp_scores, intel_events,
):
    """Build a CompetitorDeepDive for a single competitor."""

    display_name = comp_op.get("display_name", comp_id)

    # Financial health
    financial_health = _assess_financial_health(
        db, comp_id, target_period, n_quarters,
    )

    # Subscriber health
    subscriber_health = _assess_subscriber_health(
        db, comp_id, target_period, n_quarters,
    )

    # Network status
    network_status = _assess_network_status(db, comp_id, target_period)

    # Strengths and weaknesses from competitive scores
    strengths, weaknesses = _derive_strengths_weaknesses(comp_scores, display_name)

    # Likely future actions (inferred from trends)
    likely_future_actions = _infer_future_actions(
        financial_health, subscriber_health, network_status,
        comp_op, comp_scores, display_name,
    )

    # Implications for the target operator
    implications = _derive_implications(
        target_operator, comp_id, display_name,
        financial_health, subscriber_health, network_status,
        strengths, weaknesses, likely_future_actions,
    )

    return CompetitorDeepDive(
        operator=display_name,
        financial_health=financial_health,
        subscriber_health=subscriber_health,
        network_status=network_status,
        strengths=strengths,
        weaknesses=weaknesses,
        likely_future_actions=likely_future_actions,
        implications=implications,
    )


def _assess_financial_health(db, operator_id, target_period, n_quarters):
    """Build financial health summary from time-series data."""
    ts = db.get_financial_timeseries(operator_id, n_quarters=n_quarters,
                                     end_cq=target_period)

    if not ts:
        return {"status": "no_data"}

    latest = ts[-1]
    health = {
        "status": "data_available",
        "latest_quarter": latest.get("calendar_quarter", ""),
        "revenue": latest.get("total_revenue"),
        "service_revenue": latest.get("service_revenue"),
        "service_revenue_growth_pct": latest.get("service_revenue_growth_pct"),
        "ebitda": latest.get("ebitda"),
        "ebitda_margin_pct": latest.get("ebitda_margin_pct"),
        "ebitda_growth_pct": latest.get("ebitda_growth_pct"),
        "capex": latest.get("capex"),
        "capex_to_revenue_pct": latest.get("capex_to_revenue_pct"),
    }

    # Calculate revenue trend over the time series
    revs = [r.get("total_revenue") for r in ts if r.get("total_revenue") is not None]
    if len(revs) >= 2:
        if revs[-1] > revs[0]:
            health["revenue_trend"] = "growing"
        elif revs[-1] < revs[0]:
            health["revenue_trend"] = "declining"
        else:
            health["revenue_trend"] = "flat"

    # EBITDA margin trend
    margins = [
        r.get("ebitda_margin_pct") for r in ts
        if r.get("ebitda_margin_pct") is not None
    ]
    if len(margins) >= 2:
        if margins[-1] > margins[0]:
            health["margin_trend"] = "improving"
        elif margins[-1] < margins[0]:
            health["margin_trend"] = "declining"
        else:
            health["margin_trend"] = "stable"

    health["quarters_analyzed"] = len(ts)
    return health


def _assess_subscriber_health(db, operator_id, target_period, n_quarters):
    """Build subscriber health summary from time-series data."""
    ts = db.get_subscriber_timeseries(operator_id, n_quarters=n_quarters,
                                       end_cq=target_period)

    if not ts:
        return {"status": "no_data"}

    latest = ts[-1]
    health = {
        "status": "data_available",
        "latest_quarter": latest.get("calendar_quarter", ""),
        "mobile_total_k": latest.get("mobile_total_k"),
        "mobile_postpaid_k": latest.get("mobile_postpaid_k"),
        "mobile_net_adds_k": latest.get("mobile_net_adds_k"),
        "mobile_churn_pct": latest.get("mobile_churn_pct"),
        "mobile_arpu": latest.get("mobile_arpu"),
        "broadband_total_k": latest.get("broadband_total_k"),
        "broadband_net_adds_k": latest.get("broadband_net_adds_k"),
        "tv_total_k": latest.get("tv_total_k"),
    }

    # Mobile subscriber trend
    mob_totals = [
        r.get("mobile_total_k") for r in ts
        if r.get("mobile_total_k") is not None
    ]
    if len(mob_totals) >= 2:
        if mob_totals[-1] > mob_totals[0]:
            health["mobile_trend"] = "growing"
        elif mob_totals[-1] < mob_totals[0]:
            health["mobile_trend"] = "declining"
        else:
            health["mobile_trend"] = "flat"

    # Broadband subscriber trend
    bb_totals = [
        r.get("broadband_total_k") for r in ts
        if r.get("broadband_total_k") is not None
    ]
    if len(bb_totals) >= 2:
        if bb_totals[-1] > bb_totals[0]:
            health["broadband_trend"] = "growing"
        elif bb_totals[-1] < bb_totals[0]:
            health["broadband_trend"] = "declining"
        else:
            health["broadband_trend"] = "flat"

    # ARPU trend
    arpus = [
        r.get("mobile_arpu") for r in ts
        if r.get("mobile_arpu") is not None
    ]
    if len(arpus) >= 2:
        if arpus[-1] > arpus[0]:
            health["arpu_trend"] = "growing"
        elif arpus[-1] < arpus[0]:
            health["arpu_trend"] = "declining"
        else:
            health["arpu_trend"] = "flat"

    health["quarters_analyzed"] = len(ts)
    return health


def _assess_network_status(db, operator_id, target_period):
    """Get network infrastructure status."""
    net = db.get_network_data(operator_id, calendar_quarter=target_period)

    if not net:
        # Try without quarter restriction (get latest)
        net = db.get_network_data(operator_id)

    if not net:
        return {"status": "no_data"}

    return {
        "status": "data_available",
        "five_g_coverage_pct": net.get("five_g_coverage_pct"),
        "four_g_coverage_pct": net.get("four_g_coverage_pct"),
        "fiber_homepass_k": net.get("fiber_homepass_k"),
        "cable_homepass_k": net.get("cable_homepass_k"),
        "cable_docsis31_pct": net.get("cable_docsis31_pct"),
        "technology_mix": net.get("technology_mix"),
    }


def _derive_strengths_weaknesses(comp_scores, display_name):
    """Derive strengths and weaknesses from competitive scores.

    Dimensions with score > 70 are strengths; < 40 are weaknesses.
    """
    strengths = []
    weaknesses = []

    for dimension, score in sorted(comp_scores.items()):
        if score > 70:
            strengths.append(f"{dimension}: {score}/100")
        elif score < 40:
            weaknesses.append(f"{dimension}: {score}/100")

    return strengths, weaknesses


def _infer_future_actions(
    financial_health, subscriber_health, network_status,
    comp_op, comp_scores, display_name,
):
    """Infer likely future actions from observable trends.

    This implements the "three do's" principle: predict future behavior,
    don't just observe the past.
    """
    actions = []
    op_type = comp_op.get("operator_type", "")

    # Revenue growth + high capex => aggressive expansion
    rev_trend = financial_health.get("revenue_trend")
    capex_ratio = financial_health.get("capex_to_revenue_pct")
    if rev_trend == "growing" and capex_ratio is not None and capex_ratio > 15:
        actions.append(
            f"{display_name} is likely to continue aggressive network expansion "
            f"(capex/revenue at {capex_ratio:.0f}% with growing revenue)."
        )

    # Declining revenue => cost optimization or pivot
    if rev_trend == "declining":
        actions.append(
            f"{display_name} may pursue cost optimization or strategic pivot "
            f"given declining revenue trend."
        )

    # Strong subscriber growth => market share grab
    mob_trend = subscriber_health.get("mobile_trend")
    if mob_trend == "growing":
        actions.append(
            f"{display_name} is likely to continue market share expansion "
            f"in mobile, leveraging positive subscriber momentum."
        )

    # Broadband decline => focus shift
    bb_trend = subscriber_health.get("broadband_trend")
    if bb_trend == "declining":
        actions.append(
            f"{display_name} may accelerate fiber migration or FWA push "
            f"to counter broadband subscriber losses."
        )

    # High 5G coverage => monetization push
    five_g = network_status.get("five_g_coverage_pct")
    if five_g is not None and five_g > 85:
        actions.append(
            f"{display_name} with {five_g:.0f}% 5G coverage is positioned to "
            f"push 5G monetization through premium tiers and B2B use cases."
        )

    # New entrant pattern
    if op_type == "new_entrant":
        actions.append(
            f"{display_name} as a new entrant will likely focus on "
            f"network buildout, aggressive pricing, and customer acquisition."
        )

    # Low network scores => investment needed
    net_cov = comp_scores.get("Network Coverage", 0)
    if net_cov > 0 and net_cov < 50:
        actions.append(
            f"{display_name} will need significant network investment "
            f"(coverage score: {net_cov}/100)."
        )

    # If no specific actions could be inferred
    if not actions:
        actions.append(
            f"Insufficient trend data to predict {display_name}'s future actions."
        )

    return actions


def _derive_implications(
    target_operator, comp_id, display_name,
    financial_health, subscriber_health, network_status,
    strengths, weaknesses, likely_future_actions,
):
    """Derive implications of this competitor's position for the target operator."""
    implications = []

    # Threat: competitor is growing where we might not be
    rev_trend = financial_health.get("revenue_trend")
    if rev_trend == "growing":
        implications.append(CompetitorImplication(
            implication_type="threat",
            description=(
                f"{display_name}'s growing revenue indicates competitive "
                f"pressure; they are capturing market value."
            ),
            evidence=[f"Revenue trend: {rev_trend}"],
            suggested_action="Monitor pricing and go-to-market strategies.",
        ))

    # Opportunity: competitor has weaknesses we can exploit
    if weaknesses:
        weak_dims = ", ".join(w.split(":")[0] for w in weaknesses[:3])
        implications.append(CompetitorImplication(
            implication_type="opportunity",
            description=(
                f"{display_name} is weak in: {weak_dims}. "
                f"Target can differentiate in these dimensions."
            ),
            evidence=weaknesses[:3],
            suggested_action=(
                f"Invest in {weak_dims} to capture customers dissatisfied "
                f"with {display_name}."
            ),
        ))

    # Learning: competitor's strengths we should study
    if strengths:
        strong_dims = ", ".join(s.split(":")[0] for s in strengths[:3])
        implications.append(CompetitorImplication(
            implication_type="learning",
            description=(
                f"{display_name} excels in: {strong_dims}. "
                f"Study their approach for best practices."
            ),
            evidence=strengths[:3],
            suggested_action=(
                f"Benchmark {display_name}'s practices in {strong_dims}."
            ),
        ))

    # Network gap analysis
    five_g_target_coverage = network_status.get("five_g_coverage_pct")
    if five_g_target_coverage is not None and five_g_target_coverage > 90:
        implications.append(CompetitorImplication(
            implication_type="threat",
            description=(
                f"{display_name} has {five_g_target_coverage:.0f}% 5G coverage, "
                f"creating potential network advantage."
            ),
            evidence=[f"5G coverage: {five_g_target_coverage:.0f}%"],
            suggested_action="Accelerate 5G deployment to close coverage gap.",
        ))

    return implications


# ============================================================================
# Comparison Table
# ============================================================================


def _build_comparison_table(
    db, all_operators, target_period, n_quarters, scores_by_operator,
):
    """Build cross-operator comparison table for key metrics.

    Returns dict of {metric_name: {operator_id: value}}.
    """
    table = {
        "revenue": {},
        "revenue_growth": {},
        "ebitda_margin": {},
        "subscribers": {},
        "arpu": {},
        "churn": {},
        "5g_coverage": {},
    }

    for op in all_operators:
        op_id = op["operator_id"]
        display = op.get("display_name", op_id)

        # Financial data
        fin_ts = db.get_financial_timeseries(op_id, n_quarters=1,
                                              end_cq=target_period)
        if fin_ts:
            latest_fin = fin_ts[-1]
            table["revenue"][op_id] = latest_fin.get("total_revenue")
            table["revenue_growth"][op_id] = latest_fin.get("service_revenue_growth_pct")
            table["ebitda_margin"][op_id] = latest_fin.get("ebitda_margin_pct")

        # Subscriber data
        sub_ts = db.get_subscriber_timeseries(op_id, n_quarters=1,
                                               end_cq=target_period)
        if sub_ts:
            latest_sub = sub_ts[-1]
            table["subscribers"][op_id] = latest_sub.get("mobile_total_k")
            table["arpu"][op_id] = latest_sub.get("mobile_arpu")
            table["churn"][op_id] = latest_sub.get("mobile_churn_pct")

        # Network data
        net = db.get_network_data(op_id, calendar_quarter=target_period)
        if not net:
            net = db.get_network_data(op_id)
        if net:
            table["5g_coverage"][op_id] = net.get("five_g_coverage_pct")

    return table


# ============================================================================
# Overall Assessment
# ============================================================================


def _assess_overall_intensity(five_forces, market_snapshot):
    """Determine overall competition intensity from five forces."""
    if not five_forces:
        return "medium"

    level_scores = {"high": 3, "medium": 2, "low": 1}
    total = 0
    count = 0

    for force_name, force in five_forces.items():
        level = force.force_level if isinstance(force, PorterForce) else "medium"
        total += level_scores.get(level, 2)
        count += 1

    if count == 0:
        return "medium"

    avg = total / count
    if avg >= 2.5:
        return "high"
    elif avg >= 1.5:
        return "medium"
    else:
        return "low"


def _build_landscape_narrative(
    all_operators, market_snapshot, five_forces, overall_intensity,
):
    """Build a textual description of the competitive landscape."""
    parts = []

    num_ops = len(all_operators)
    op_names = [op.get("display_name", op["operator_id"]) for op in all_operators]

    parts.append(
        f"The market comprises {num_ops} active operators: "
        f"{', '.join(op_names)}."
    )
    parts.append(
        f"Overall competition intensity is assessed as {overall_intensity}."
    )

    # Revenue ranking
    revenues = []
    for row in market_snapshot:
        rev = row.get("total_revenue")
        name = row.get("display_name", row.get("operator_id", ""))
        if rev is not None:
            revenues.append((name, rev))

    if revenues:
        revenues.sort(key=lambda x: x[1], reverse=True)
        ranking = ", ".join(
            f"{name} ({rev:.0f}M)" for name, rev in revenues
        )
        parts.append(f"Revenue ranking: {ranking}.")

    # Five forces summary
    force_summaries = []
    for fname, force in five_forces.items():
        if isinstance(force, PorterForce):
            pretty_name = fname.replace("_", " ").title()
            force_summaries.append(f"{pretty_name}: {force.force_level}")
    if force_summaries:
        parts.append("Five Forces: " + "; ".join(force_summaries) + ".")

    return " ".join(parts)


def _build_key_message(
    market, target_operator, all_operators, market_snapshot,
    five_forces, overall_intensity,
):
    """Build the key message for the competition analysis slide."""
    if not all_operators:
        return "No competitive data available for this market."

    parts = []
    num_ops = len(all_operators)

    # Find the market leader by revenue
    leader = None
    leader_rev = 0
    target_rev = 0
    for row in market_snapshot:
        rev = row.get("total_revenue")
        if rev is not None:
            if rev > leader_rev:
                leader = row.get("display_name", row.get("operator_id", ""))
                leader_rev = rev
            if row.get("operator_id") == target_operator:
                target_rev = rev

    if leader and leader_rev > 0 and target_rev > 0:
        market_total = sum(
            r.get("total_revenue", 0) for r in market_snapshot
            if r.get("total_revenue") is not None
        )
        if market_total > 0:
            leader_share = leader_rev / market_total * 100
            target_share = target_rev / market_total * 100
            parts.append(
                f"In a {num_ops}-player market with {overall_intensity} competition intensity, "
                f"{leader} leads with {leader_share:.0f}% revenue share."
            )
            if target_operator != leader:
                parts.append(
                    f"Target operator holds {target_share:.0f}% share."
                )

    # Highlight the strongest force
    strongest = None
    strongest_score = 0
    level_scores = {"high": 3, "medium": 2, "low": 1}
    for fname, force in five_forces.items():
        if isinstance(force, PorterForce):
            score = level_scores.get(force.force_level, 2)
            if score > strongest_score:
                strongest = fname
                strongest_score = score

    if strongest:
        pretty = strongest.replace("_", " ").title()
        parts.append(f"Strongest competitive force: {pretty}.")

    if not parts:
        return (
            f"Competitive landscape analysis for {market} market "
            f"with {num_ops} operators."
        )

    return " ".join(parts)


# ============================================================================
# Helpers
# ============================================================================


def _resolve_latest_period(db, market, n_quarters):
    """Find the latest calendar quarter with data in the market."""
    converter = PeriodConverter()
    timeline = converter.generate_timeline(n_quarters=n_quarters)

    # Check from newest to oldest
    for cq in reversed(timeline):
        rows = db.get_market_comparison(market, cq)
        has_data = any(
            r.get("total_revenue") is not None for r in rows
        )
        if has_data:
            return cq

    # Fallback to the latest generated quarter
    return timeline[-1] if timeline else "CQ4_2025"


def _group_scores_by_operator(comp_scores):
    """Group competitive score records by operator_id.

    Returns {operator_id: {dimension: score}}.
    """
    result = {}
    for row in comp_scores:
        op_id = row.get("operator_id", "")
        dim = row.get("dimension", "")
        score = row.get("score", 0)
        if op_id not in result:
            result[op_id] = {}
        result[op_id][dim] = score
    return result


def _safe_intelligence_events(db, market=None, days_back=730):
    """Safely retrieve intelligence events, returning empty list on failure."""
    try:
        return db.get_intelligence_events(market=market, days_back=days_back)
    except Exception:
        return []


def _empty_insight(message):
    """Return a valid but empty CompetitionInsight."""
    return CompetitionInsight(
        five_forces={
            "existing_competitors": PorterForce(
                force_name="existing_competitors", force_level="medium",
            ),
            "new_entrants": PorterForce(
                force_name="new_entrants", force_level="low",
            ),
            "substitutes": PorterForce(
                force_name="substitutes", force_level="medium",
            ),
            "supplier_power": PorterForce(
                force_name="supplier_power", force_level="medium",
            ),
            "buyer_power": PorterForce(
                force_name="buyer_power", force_level="medium",
            ),
        },
        overall_competition_intensity="medium",
        competitor_analyses={},
        comparison_table={},
        competitive_landscape="",
        key_message=message,
    )
