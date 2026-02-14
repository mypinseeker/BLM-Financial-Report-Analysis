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

from src.blm.trend_analyzer import compute_trend_metrics
from src.database.db import TelecomDatabase
from src.database.period_utils import PeriodConverter
from src.models.competition import (
    CompetitionInsight,
    CompetitorDeepDive,
    CompetitorImplication,
    PorterForce,
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
# Dedup helpers
# ============================================================================


def _dedup_intel_events(events: list[dict]) -> list[dict]:
    """Remove near-duplicate intelligence events by title similarity.

    Two events are considered duplicates when their lowercased titles share
    ≥80% of words. The first occurrence is kept.
    """
    if not events:
        return events
    result = []
    seen_words: list[set[str]] = []
    for ev in events:
        title = ev.get("title", "")
        words = set(title.lower().split())
        if not words:
            result.append(ev)
            continue
        is_dup = False
        for sw in seen_words:
            if not sw:
                continue
            overlap = len(words & sw) / max(len(words), len(sw))
            if overlap >= 0.80:
                is_dup = True
                break
        if not is_dup:
            result.append(ev)
            seen_words.append(words)
    return result


def _dedup_factors(factors: list[dict]) -> list[dict]:
    """Remove duplicate key_factors by name (case-insensitive)."""
    seen: set[str] = set()
    result = []
    for f in factors:
        key = f.get("name", "").lower().strip()
        if key not in seen:
            seen.add(key)
            result.append(f)
    return result


# ============================================================================
# Public API
# ============================================================================


def analyze_competition(
    db: TelecomDatabase,
    market: str,
    target_operator: str,
    target_period: str = None,
    n_quarters: int = 8,
    market_config=None,
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
    intel_events = _dedup_intel_events(intel_events)

    # Build Porter's Five Forces
    five_forces = _build_five_forces(
        db, market, target_operator, target_period,
        n_quarters, all_operators, market_snapshot,
        scores_by_operator, intel_events,
        market_config=market_config,
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
            all_scores_by_operator=scores_by_operator,
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
    market_config=None,
):
    """Build all 5 PorterForce objects."""
    return {
        "existing_competitors": _force_existing_competitors(
            db, market, target_operator, target_period,
            n_quarters, all_operators, market_snapshot,
            scores_by_operator, market_config=market_config,
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
    scores_by_operator, market_config=None,
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
                    f"(total: {_fmt_rev(total_rev, market_config.currency if market_config else 'USD')})"
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
        key_factors=_dedup_factors(factors),
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
        key_factors=_dedup_factors(factors),
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
        key_factors=_dedup_factors(factors),
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
        key_factors=_dedup_factors(factors),
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
        key_factors=_dedup_factors(factors),
        implications=implications,
    )


# ============================================================================
# Competitor Deep Dive — Derived fields
# ============================================================================


def _derive_growth_strategy(financial_health: dict, subscriber_health: dict,
                            comp_scores: dict) -> str:
    """Infer growth strategy from financial and subscriber trends."""
    if financial_health.get("status") == "no_data":
        return ""

    parts = []
    rev_trend = financial_health.get("revenue_trend", "")
    margin_trend = financial_health.get("margin_trend", "")
    sub_trend = subscriber_health.get("mobile_trend", "") if subscriber_health.get("status") != "no_data" else ""

    # Revenue + margin pattern → strategy inference
    if rev_trend == "growing" and margin_trend == "improving":
        parts.append("Revenue-led profitable growth")
    elif rev_trend == "growing" and margin_trend == "declining":
        parts.append("Market share expansion (investing for growth)")
    elif rev_trend == "declining" and margin_trend == "improving":
        parts.append("Margin optimization / cost transformation")
    elif rev_trend == "declining":
        parts.append("Defensive cost restructuring")
    elif rev_trend == "growing":
        parts.append("Steady growth trajectory")

    # Subscriber pattern
    if sub_trend == "growing":
        parts.append("subscriber acquisition focus")
    elif sub_trend == "declining":
        parts.append("ARPU-led value strategy")

    # Competitive dimension hints
    high_scores = [d for d, s in comp_scores.items() if s and s >= 80]
    if "Enterprise Solutions" in high_scores or "enterprise_solutions" in [d.lower().replace(" ", "_") for d in high_scores]:
        parts.append("strong B2B/enterprise push")
    if "5G Deployment" in high_scores:
        parts.append("5G network leadership")

    return "; ".join(parts)


def _derive_ma_activity(intel_events: list, comp_id: str) -> list[str]:
    """Extract M&A events from intelligence events for a competitor."""
    ma_keywords = {"acqui", "merger", "joint venture", "jv ", "divest",
                   "sale of", "sells ", "buys ", "partnership", "stake"}
    results = []
    for ev in intel_events:
        if ev.get("operator_id") != comp_id:
            continue
        title = (ev.get("title") or "").lower()
        if any(kw in title for kw in ma_keywords):
            results.append(ev.get("title", ""))
    return results


def _derive_problems(weaknesses: list, financial_health: dict,
                     subscriber_health: dict) -> list[str]:
    """Derive key problems from weaknesses and declining metrics."""
    problems = []
    # Weaknesses are already diagnosed
    for w in weaknesses:
        dim = w.split(":")[0].strip() if ":" in w else w
        problems.append(f"Competitive gap in {dim}")

    # Financial stress signals
    if financial_health.get("revenue_trend") == "declining":
        problems.append("Revenue under pressure (declining trend)")
    if financial_health.get("margin_trend") == "declining":
        problems.append("Margin erosion")
    growth = financial_health.get("ebitda_growth_pct")
    if growth is not None and growth < -5:
        problems.append(f"EBITDA contraction ({growth:+.1f}%)")

    # Subscriber stress
    if subscriber_health.get("status") != "no_data":
        if subscriber_health.get("mobile_trend") == "declining":
            problems.append("Mobile subscriber losses")
        if subscriber_health.get("broadband_trend") == "declining":
            problems.append("Broadband subscriber losses")

    return problems


def _derive_product_portfolio(comp_scores: dict, subscriber_health: dict) -> list[str]:
    """Infer product portfolio areas from scores and subscriber data."""
    portfolio = []
    # All operators have mobile
    portfolio.append("Mobile (postpaid + prepaid)")

    # Check for broadband from subscriber data
    if subscriber_health.get("status") != "no_data":
        bb_total = subscriber_health.get("broadband_total_k")
        if bb_total and bb_total > 0:
            fiber_k = subscriber_health.get("broadband_fiber_k")
            if fiber_k and fiber_k > 0:
                portfolio.append("Fixed broadband (incl. fiber/FTTH)")
            else:
                portfolio.append("Fixed broadband")

        tv_k = subscriber_health.get("tv_total_k")
        if tv_k and tv_k > 0:
            portfolio.append("TV/Video")

    # From competitive dimensions
    if comp_scores.get("Enterprise Solutions") and comp_scores["Enterprise Solutions"] >= 60:
        portfolio.append("Enterprise/B2B solutions")
    if comp_scores.get("Digital Services") and comp_scores["Digital Services"] >= 60:
        portfolio.append("Digital services")

    return portfolio


def _derive_business_model(financial_health: dict, subscriber_health: dict) -> str:
    """Infer business model type from revenue and subscriber mix."""
    if financial_health.get("status") == "no_data":
        return ""

    rev = financial_health.get("revenue")
    service_rev = financial_health.get("service_revenue")

    parts = []
    # Check if mobile-dominant or convergent
    if subscriber_health.get("status") != "no_data":
        mobile_k = subscriber_health.get("mobile_total_k") or 0
        bb_k = subscriber_health.get("broadband_total_k") or 0
        if bb_k > 0 and mobile_k > 0:
            ratio = bb_k / mobile_k
            if ratio > 0.3:
                parts.append("Convergent (mobile + fixed)")
            else:
                parts.append("Mobile-centric with fixed complement")
        elif mobile_k > 0:
            parts.append("Mobile-only operator")

    # Service revenue ratio
    if rev and service_rev and rev > 0:
        svc_pct = (service_rev / rev) * 100
        if svc_pct >= 85:
            parts.append("service-revenue dominant")
        elif svc_pct >= 70:
            parts.append("balanced service + equipment revenue")

    margin = financial_health.get("ebitda_margin_pct")
    if margin:
        if margin >= 35:
            parts.append("high-margin profile")
        elif margin >= 25:
            parts.append("moderate-margin profile")
        else:
            parts.append("low-margin / scale-focused")

    return "; ".join(parts) if parts else ""


def _derive_new_product_pipeline(intel_events: list, comp_id: str,
                                  earnings_highlights: list) -> list[str]:
    """Extract new product pipeline items from intel events and earnings."""
    keywords = {"launch", "rollout", "upgrade", "new service", "new product",
                "new plan", "new tariff", "pilot", "beta", "deploy"}
    results = []
    seen = set()

    for ev in intel_events:
        if ev.get("operator_id") != comp_id:
            continue
        title = (ev.get("title") or "").lower()
        if any(kw in title for kw in keywords):
            item = ev.get("title", "")
            if item and item.lower() not in seen:
                seen.add(item.lower())
                results.append(item)

    for eh in earnings_highlights:
        content = (eh.get("content") or "").lower()
        if any(kw in content for kw in keywords):
            snippet = eh.get("content", "")[:120]
            if snippet and snippet.lower() not in seen:
                seen.add(snippet.lower())
                results.append(snippet)

    return results[:5]


def _derive_supply_chain_status(network_status: dict) -> str:
    """Synthesize supply chain status from network infrastructure data."""
    if network_status.get("status") == "no_data":
        return ""

    tech_mix = network_status.get("technology_mix")
    if not tech_mix or not isinstance(tech_mix, dict):
        return ""

    parts = []
    vendor = tech_mix.get("mobile_vendor")
    if vendor:
        parts.append(f"Primary vendor: {vendor}")
    virt_pct = tech_mix.get("virtualization_pct")
    if virt_pct is not None:
        parts.append(f"{virt_pct}% virtualized")
    sa_status = tech_mix.get("5g_sa_status")
    if sa_status:
        parts.append(f"5G SA: {sa_status}")
    core_vendor = tech_mix.get("core_vendor")
    if core_vendor:
        parts.append(f"Core: {core_vendor}")

    return "; ".join(parts)


def _derive_ecosystem_partners(intel_events: list, comp_id: str,
                                network_status: dict) -> list[str]:
    """Extract ecosystem partners from intel events and network vendor info."""
    keywords = {"partner", "alliance", "consortium", "joint venture",
                "jv ", "collaboration", "agreement with", "deal with"}
    results = []
    seen = set()

    for ev in intel_events:
        if ev.get("operator_id") != comp_id:
            continue
        title = (ev.get("title") or "").lower()
        if any(kw in title for kw in keywords):
            item = ev.get("title", "")
            if item and item.lower() not in seen:
                seen.add(item.lower())
                results.append(item)

    # Add network vendor as ecosystem partner
    if network_status.get("status") != "no_data":
        tech_mix = network_status.get("technology_mix")
        if tech_mix and isinstance(tech_mix, dict):
            vendor = tech_mix.get("mobile_vendor")
            if vendor and vendor.lower() not in seen:
                seen.add(vendor.lower())
                results.append(f"Network vendor: {vendor}")

    return results[:5]


def _derive_core_control_points(comp_scores: dict, network_status: dict,
                                 subscriber_health: dict) -> list[str]:
    """Derive core control points from competitive scores, infra, and scale."""
    results = []

    # Top competitive dimensions scoring ≥80
    for dim, score in sorted(comp_scores.items(), key=lambda x: x[1] or 0,
                             reverse=True):
        if score and score >= 80:
            results.append(f"Market leadership in {dim}")

    # Network infrastructure ownership
    if network_status.get("status") != "no_data":
        fiber_k = network_status.get("fiber_homepass_k")
        if fiber_k and fiber_k > 0:
            results.append(f"Own fiber infrastructure ({fiber_k:.0f}k homes)")
        cable_k = network_status.get("cable_homepass_k")
        if cable_k and cable_k > 0:
            results.append(f"Own cable infrastructure ({cable_k:.0f}k homes)")

    # Subscriber scale advantage
    if subscriber_health.get("status") != "no_data":
        mobile_k = subscriber_health.get("mobile_total_k")
        if mobile_k and mobile_k > 10000:
            results.append(f"Scale advantage ({mobile_k / 1000:.1f}m mobile subs)")

    return results[:5]


def _derive_org_structure(db, comp_id: str) -> str:
    """Build org structure summary from executive records."""
    executives = db.get_executives(comp_id)
    if not executives:
        return ""

    current = [e for e in executives if e.get("is_current")]
    if not current:
        return ""

    parts = []
    for exec_rec in current:
        title = exec_rec.get("title", "")
        name = exec_rec.get("name", "")
        bg = exec_rec.get("background", "")
        label = f"{title}: {name}"
        if bg:
            label += f" ({bg})"
        parts.append(label)

    return "; ".join(parts[:5])


def _derive_incentive_system(financial_health: dict, growth_strategy: str) -> str:
    """Infer incentive alignment from financial trajectory."""
    if financial_health.get("status") == "no_data":
        return ""

    margin_trend = financial_health.get("margin_trend", "")
    rev_trend = financial_health.get("revenue_trend", "")

    if margin_trend == "improving":
        return "Efficiency/profitability-focused incentive alignment"
    if rev_trend == "growing" and margin_trend != "declining":
        return "Growth-oriented with volume/revenue targets"
    if rev_trend == "declining":
        return "Restructuring mode — cost discipline focus"

    # Fallback from growth_strategy keywords
    gs = growth_strategy.lower()
    if "cost" in gs or "margin" in gs:
        return "Cost discipline and margin protection"
    if "growth" in gs or "acquisition" in gs:
        return "Growth and market share targets"

    return "Balanced efficiency and growth targets"


def _derive_talent_culture(db, comp_id: str, comp_scores: dict) -> str:
    """Infer talent/culture profile from executives and innovation scores."""
    executives = db.get_executives(comp_id)
    current = [e for e in executives if e.get("is_current")] if executives else []

    # Innovation and Digital scores for tech orientation
    innovation = comp_scores.get("Product Innovation") or 0
    digital = comp_scores.get("Digital Services") or 0
    avg_tech = (innovation + digital) / 2 if (innovation or digital) else 0

    if avg_tech >= 75:
        culture = "tech-forward"
    elif avg_tech >= 50:
        culture = "transitioning to digital"
    elif avg_tech > 0:
        culture = "traditional"
    else:
        culture = ""

    parts = []
    if current:
        parts.append(f"{len(current)} C-suite leaders")
    if culture:
        parts.append(f"{culture} culture")

    return "; ".join(parts)


# ============================================================================
# Competitor Deep Dive
# ============================================================================


def _build_competitor_deep_dive(
    db, comp_id, comp_op, target_operator,
    target_period, n_quarters, comp_scores, intel_events,
    all_scores_by_operator=None,
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

    # Strengths and weaknesses from competitive scores (relative to market)
    strengths, weaknesses = _derive_strengths_weaknesses(
        comp_scores, display_name, all_scores_by_operator,
    )

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

    # Derived skeleton fields
    growth_strategy = _derive_growth_strategy(
        financial_health, subscriber_health, comp_scores,
    )
    ma_activity = _derive_ma_activity(intel_events, comp_id)
    problems = _derive_problems(weaknesses, financial_health, subscriber_health)
    product_portfolio = _derive_product_portfolio(comp_scores, subscriber_health)
    business_model = _derive_business_model(financial_health, subscriber_health)

    # 7 newly populated fields
    earnings_highlights = db.get_earnings_highlights(comp_id, target_period)
    new_product_pipeline = _derive_new_product_pipeline(
        intel_events, comp_id, earnings_highlights,
    )
    supply_chain_status = _derive_supply_chain_status(network_status)
    ecosystem_partners = _derive_ecosystem_partners(
        intel_events, comp_id, network_status,
    )
    core_control_points = _derive_core_control_points(
        comp_scores, network_status, subscriber_health,
    )
    org_structure = _derive_org_structure(db, comp_id)
    incentive_system = _derive_incentive_system(financial_health, growth_strategy)
    talent_culture = _derive_talent_culture(db, comp_id, comp_scores)

    return CompetitorDeepDive(
        operator=display_name,
        financial_health=financial_health,
        subscriber_health=subscriber_health,
        network_status=network_status,
        strengths=strengths,
        weaknesses=weaknesses,
        likely_future_actions=likely_future_actions,
        implications=implications,
        growth_strategy=growth_strategy,
        ma_activity=ma_activity,
        problems=problems,
        product_portfolio=product_portfolio,
        business_model=business_model,
        new_product_pipeline=new_product_pipeline,
        supply_chain_status=supply_chain_status,
        ecosystem_partners=ecosystem_partners,
        core_control_points=core_control_points,
        org_structure=org_structure,
        incentive_system=incentive_system,
        talent_culture=talent_culture,
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

    # Compute rich trend metrics from revenue/margin arrays
    if len(revs) >= 2:
        health["revenue_metrics"] = compute_trend_metrics(revs).to_dict()
    if len(margins) >= 2:
        health["margin_metrics"] = compute_trend_metrics(margins).to_dict()

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
        "broadband_fiber_k": latest.get("broadband_fiber_k"),
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


def _derive_strengths_weaknesses(comp_scores, display_name,
                                  all_scores_by_operator=None):
    """Derive strengths and weaknesses from competitive scores.

    Uses **relative scoring**: compares the operator's score per dimension
    against the market average across all operators.
      - Score ≥ market_avg + 5  → strength  (label includes market avg)
      - Score ≤ market_avg − 5  → weakness  (label includes market avg)
    Falls back to absolute thresholds (>70 / <40) when no market-wide
    data is available.
    """
    strengths = []
    weaknesses = []

    # Build per-dimension market averages from all operators
    market_avgs: dict[str, float] = {}
    if all_scores_by_operator:
        dim_values: dict[str, list[float]] = {}
        for op_scores in all_scores_by_operator.values():
            for dim, val in op_scores.items():
                if val is not None:
                    dim_values.setdefault(dim, []).append(val)
        for dim, vals in dim_values.items():
            if vals:
                market_avgs[dim] = sum(vals) / len(vals)

    for dimension, score in sorted(comp_scores.items()):
        if score is None:
            continue
        avg = market_avgs.get(dimension)
        if avg is not None:
            label = f"{dimension}: score {score:.0f} (market avg {avg:.0f})"
            if score >= avg + 5:
                strengths.append(label)
            elif score <= avg - 5:
                weaknesses.append(label)
        else:
            # Fallback to absolute thresholds
            label = f"{dimension}: {score:.1f}/100"
            if score > 70:
                strengths.append(label)
            elif score < 40:
                weaknesses.append(label)

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

    # Low network scores => investment needed (scores already normalised to 0-100)
    net_cov = comp_scores.get("Network Coverage", 0)
    if net_cov > 0 and net_cov < 50:
        actions.append(
            f"{display_name} will need significant network investment "
            f"(coverage score: {net_cov:.0f}/100)."
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

        # Ensure every operator appears in every metric (even if None)
        for metric in table:
            table[metric].setdefault(op_id, None)

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
            f"{name} ({_fmt_rev(rev)})" for name, rev in revenues
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
    Normalises dimension names (snake_case → Title Case) and deduplicates.
    Auto-detects 0-10 vs 0-100 scale and normalises to 0-100.
    """
    raw = {}
    for row in comp_scores:
        op_id = row.get("operator_id", "")
        dim_raw = row.get("dimension", "")
        score = row.get("score", 0)
        if op_id not in raw:
            raw[op_id] = {}
        # Normalise dimension name: "brand_strength" → "Brand Strength"
        dim = dim_raw.replace("_", " ").title()
        # If duplicate after normalisation, keep the higher score
        if dim in raw[op_id]:
            raw[op_id][dim] = max(raw[op_id][dim], score)
        else:
            raw[op_id][dim] = score

    # Auto-detect scale: if max score across all operators <= 10, assume 0-10
    all_values = [
        s for op_scores in raw.values()
        for s in op_scores.values()
        if s is not None
    ]
    scale_factor = 10 if (all_values and max(all_values) <= 10) else 1

    if scale_factor != 1:
        for op_id in raw:
            for dim in raw[op_id]:
                if raw[op_id][dim] is not None:
                    raw[op_id][dim] = raw[op_id][dim] * scale_factor

    return raw


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
