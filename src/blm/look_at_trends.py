"""Look 1: Trends -- PEST Framework Analysis.

Analyses the macro environment (Political, Economic, Society, Technology)
and industry environment to identify trends, opportunities, and threats
for a target operator in a given market.

Usage:
    from src.blm.look_at_trends import analyze_trends

    result = analyze_trends(
        db=db,
        market="germany",
        target_operator="vodafone_germany",
    )
"""

from __future__ import annotations

from typing import Optional

from src.database.db import TelecomDatabase
from src.database.period_utils import PeriodConverter
from src.models.trend import PESTFactor, PESTAnalysis, TrendAnalysis


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_trends(
    db,
    market: str,
    target_operator: str,
    target_period: str = None,
    n_quarters: int = 8,
    provenance=None,
    market_config=None,
) -> TrendAnalysis:
    """Run the complete Look 1: Trends analysis.

    Args:
        db: TelecomDatabase instance (already initialized).
        market: Market identifier, e.g. "germany".
        target_operator: Operator ID, e.g. "vodafone_germany".
        target_period: Optional end calendar quarter, e.g. "CQ4_2025".
        n_quarters: Number of quarters of historical data to analyse.
        provenance: Optional ProvenanceStore for data-point tracking.

    Returns:
        A fully populated TrendAnalysis dataclass.
    """
    # Resolve country from market / operator directory
    country = _resolve_country(db, market)

    # ------------------------------------------------------------------
    # 1. Gather raw data from the database
    # ------------------------------------------------------------------
    macro_data = db.get_macro_data(country, n_quarters=n_quarters, end_cq=target_period)
    intelligence_events = _get_intelligence_safe(db, market)
    operators = db.get_operators_in_market(market)
    market_ts = db.get_market_timeseries(market, n_quarters=n_quarters, end_cq=target_period)

    # ------------------------------------------------------------------
    # 2. Build PEST factors
    # ------------------------------------------------------------------
    political_factors = _build_political_factors(macro_data, intelligence_events, target_operator, provenance)
    economic_factors = _build_economic_factors(macro_data, target_operator, provenance)
    society_factors = _build_society_factors(macro_data, intelligence_events, target_operator, provenance)
    technology_factors = _build_technology_factors(macro_data, intelligence_events, target_operator, provenance)

    # ------------------------------------------------------------------
    # 3. Build cross-cutting PEST summaries
    # ------------------------------------------------------------------
    policy_opportunities = _extract_policy_opportunities(political_factors)
    policy_threats = _extract_policy_threats(political_factors)
    tech_addressable = _summarise_tech_market(technology_factors)
    weather, weather_explanation = _assess_weather(
        political_factors, economic_factors, society_factors, technology_factors
    )

    pest = PESTAnalysis(
        political_factors=political_factors,
        economic_factors=economic_factors,
        society_factors=society_factors,
        technology_factors=technology_factors,
        overall_weather=weather,
        weather_explanation=weather_explanation,
        policy_opportunities=policy_opportunities,
        policy_threats=policy_threats,
        tech_addressable_market=tech_addressable,
        key_message=_pest_key_message(weather, political_factors, economic_factors,
                                      society_factors, technology_factors),
    )

    # ------------------------------------------------------------------
    # 4. Industry environment analysis
    # ------------------------------------------------------------------
    ind = _analyse_industry(market_ts, operators, n_quarters, provenance, market_config)

    # ------------------------------------------------------------------
    # 5. Assemble the top-level key message
    # ------------------------------------------------------------------
    key_message = _build_key_message(pest, ind, market)

    return TrendAnalysis(
        pest=pest,
        industry_market_size=ind["market_size"],
        industry_growth_rate=ind["growth_rate"],
        industry_profit_trend=ind["profit_trend"],
        industry_concentration=ind["concentration"],
        industry_lifecycle_stage=ind["lifecycle_stage"],
        new_business_models=ind["new_business_models"],
        technology_revolution=ind["technology_revolution"],
        key_success_factors=ind["key_success_factors"],
        value_transfer_trends=ind["value_transfer_trends"],
        key_message=key_message,
    )


# ---------------------------------------------------------------------------
# Country resolution
# ---------------------------------------------------------------------------

def _resolve_country(db, market: str) -> str:
    """Resolve the country name for a given market identifier."""
    operators = db.get_operators_in_market(market)
    if operators:
        return operators[0].get("country", market.title())
    return market.title()


# ---------------------------------------------------------------------------
# Safe intelligence event retrieval
# ---------------------------------------------------------------------------

def _get_intelligence_safe(db, market: str) -> list:
    """Retrieve intelligence events, deduplicated by title."""
    try:
        raw = db.get_intelligence_events(market=market, days_back=730)
        # Deduplicate by title (database may contain duplicate inserts)
        seen = set()
        unique = []
        for evt in raw:
            title = evt.get("title", "")
            if title not in seen:
                seen.add(title)
                unique.append(evt)
        return unique
    except Exception:
        return []


# ---------------------------------------------------------------------------
# PEST: Political factors
# ---------------------------------------------------------------------------

def _build_political_factors(
    macro_data: list,
    events: list,
    target_operator: str,
    provenance,
) -> list[PESTFactor]:
    factors = []

    # -- Regulatory environment from macro data --
    reg_texts = [
        m.get("regulatory_environment")
        for m in macro_data
        if m.get("regulatory_environment")
    ]
    if reg_texts:
        latest_reg = reg_texts[-1]
        trend_dir = _infer_trend_from_texts(reg_texts)
        factors.append(PESTFactor(
            dimension="P",
            dimension_name="Political",
            factor_name="Regulatory Environment",
            current_status=latest_reg,
            trend=f"Regulatory stance: {latest_reg}",
            trend_direction=trend_dir,
            industry_impact="Regulatory framework shapes competitive dynamics and investment requirements",
            company_impact=f"Compliance requirements and spectrum policies directly affect {target_operator}",
            impact_type="both",
            severity="high",
            time_horizon="medium_term",
            predictability="predictable",
            evidence=[f"Macro data: {latest_reg}"],
            data_source="macro_environment",
        ))
        _track(provenance, latest_reg, "regulatory_environment", target_operator)

    # -- Digital strategy from macro data --
    digital_texts = [
        m.get("digital_strategy")
        for m in macro_data
        if m.get("digital_strategy")
    ]
    if digital_texts:
        latest_ds = digital_texts[-1]
        factors.append(PESTFactor(
            dimension="P",
            dimension_name="Political",
            factor_name="National Digital Strategy",
            current_status=latest_ds,
            trend="Government fiber and 5G coverage targets driving infrastructure investment",
            trend_direction="improving",
            industry_impact="Policy targets create both mandate and subsidy opportunities for network operators",
            company_impact=f"Fiber/5G coverage mandates may require {target_operator} investment but also enable subsidy access",
            impact_type="opportunity",
            severity="high",
            time_horizon="medium_term",
            predictability="predictable",
            evidence=[f"Digital strategy: {latest_ds}"],
            data_source="macro_environment",
        ))

    # -- Political events from intelligence --
    political_events = [e for e in events if e.get("category") in ("regulatory", "political")]
    for ev in political_events[:3]:
        factors.append(_event_to_pest_factor(ev, "P", "Political", target_operator))

    # Ensure at least one factor
    if not factors:
        factors.append(PESTFactor(
            dimension="P",
            dimension_name="Political",
            factor_name="Regulatory Environment",
            current_status="No data available",
            trend="N/A",
            trend_direction="uncertain",
            industry_impact="N/A",
            company_impact="N/A",
            impact_type="neutral",
            severity="low",
            time_horizon="medium_term",
            predictability="uncertain",
            evidence=[],
            data_source="N/A",
        ))

    return factors


# ---------------------------------------------------------------------------
# PEST: Economic factors
# ---------------------------------------------------------------------------

def _build_economic_factors(
    macro_data: list,
    target_operator: str,
    provenance,
) -> list[PESTFactor]:
    factors = []

    # -- GDP growth --
    gdp_values = [m.get("gdp_growth_pct") for m in macro_data if m.get("gdp_growth_pct") is not None]
    if gdp_values:
        latest_gdp = gdp_values[-1]
        trend_dir = _numeric_trend(gdp_values)
        status = f"GDP growth at {latest_gdp}%"
        if latest_gdp < 1.0:
            impact_type = "threat"
            industry_impact = "Slow GDP growth constrains consumer spending and enterprise IT budgets"
        elif latest_gdp < 2.0:
            impact_type = "neutral"
            industry_impact = "Moderate GDP growth supports steady telecom demand"
        else:
            impact_type = "opportunity"
            industry_impact = "Strong GDP growth boosts both consumer and enterprise spending"

        factors.append(PESTFactor(
            dimension="E",
            dimension_name="Economic",
            factor_name="GDP Growth",
            current_status=status,
            trend=f"GDP growth trend: {trend_dir} (latest {latest_gdp}%)",
            trend_direction=trend_dir,
            industry_impact=industry_impact,
            company_impact=f"{'Constrained' if latest_gdp < 1.0 else 'Supported'} revenue growth for {target_operator}",
            impact_type=impact_type,
            severity="medium" if 0.5 <= latest_gdp <= 2.0 else "high",
            time_horizon="short_term",
            predictability="predictable",
            evidence=[f"GDP growth: {latest_gdp}%"],
            data_source="macro_environment",
        ))
        _track(provenance, latest_gdp, "gdp_growth_pct", target_operator, unit="%")

    # -- Inflation --
    infl_values = [m.get("inflation_pct") for m in macro_data if m.get("inflation_pct") is not None]
    if infl_values:
        latest_infl = infl_values[-1]
        trend_dir = _numeric_trend(infl_values, lower_is_better=True)
        if latest_infl > 4.0:
            impact_type = "threat"
            severity = "high"
        elif latest_infl > 2.5:
            impact_type = "both"
            severity = "medium"
        else:
            impact_type = "neutral"
            severity = "low"

        factors.append(PESTFactor(
            dimension="E",
            dimension_name="Economic",
            factor_name="Inflation",
            current_status=f"Inflation at {latest_infl}%",
            trend=f"Inflation trend: {trend_dir} (latest {latest_infl}%)",
            trend_direction=trend_dir,
            industry_impact="Inflation affects both OPEX (energy, wages) and consumer willingness to pay",
            company_impact=f"{'OPEX pressure' if latest_infl > 3 else 'Manageable cost environment'} for {target_operator}",
            impact_type=impact_type,
            severity=severity,
            time_horizon="short_term",
            predictability="predictable",
            evidence=[f"Inflation: {latest_infl}%"],
            data_source="macro_environment",
        ))
        _track(provenance, latest_infl, "inflation_pct", target_operator, unit="%")

    # -- Unemployment --
    unemp_values = [m.get("unemployment_pct") for m in macro_data if m.get("unemployment_pct") is not None]
    if unemp_values:
        latest_unemp = unemp_values[-1]
        trend_dir = _numeric_trend(unemp_values, lower_is_better=True)
        factors.append(PESTFactor(
            dimension="E",
            dimension_name="Economic",
            factor_name="Unemployment",
            current_status=f"Unemployment at {latest_unemp}%",
            trend=f"Unemployment trend: {trend_dir}",
            trend_direction=trend_dir,
            industry_impact="Unemployment affects consumer spending power and enterprise IT budgets",
            company_impact=f"Consumer segment sensitivity for {target_operator}",
            impact_type="threat" if latest_unemp > 8 else "neutral",
            severity="medium",
            time_horizon="short_term",
            predictability="predictable",
            evidence=[f"Unemployment: {latest_unemp}%"],
            data_source="macro_environment",
        ))

    # -- Energy cost index --
    energy_values = [m.get("energy_cost_index") for m in macro_data if m.get("energy_cost_index") is not None]
    if energy_values:
        latest_energy = energy_values[-1]
        trend_dir = _numeric_trend(energy_values, lower_is_better=True)
        factors.append(PESTFactor(
            dimension="E",
            dimension_name="Economic",
            factor_name="Energy Costs",
            current_status=f"Energy cost index: {latest_energy}",
            trend=f"Energy cost trend: {trend_dir}",
            trend_direction=trend_dir,
            industry_impact="Telecom operators are major electricity consumers; energy costs directly impact OPEX",
            company_impact=f"Network energy costs are a significant OPEX line for {target_operator}",
            impact_type="threat" if trend_dir == "worsening" else "opportunity" if trend_dir == "improving" else "neutral",
            severity="medium",
            time_horizon="short_term",
            predictability="uncertain",
            evidence=[f"Energy cost index: {latest_energy}"],
            data_source="macro_environment",
        ))

    # -- Consumer confidence --
    conf_values = [m.get("consumer_confidence_index") for m in macro_data if m.get("consumer_confidence_index") is not None]
    if conf_values:
        latest_conf = conf_values[-1]
        trend_dir = _numeric_trend(conf_values)
        factors.append(PESTFactor(
            dimension="E",
            dimension_name="Economic",
            factor_name="Consumer Confidence",
            current_status=f"Consumer confidence index: {latest_conf}",
            trend=f"Consumer confidence trend: {trend_dir}",
            trend_direction=trend_dir,
            industry_impact="Consumer confidence drives willingness to spend on telecom and digital services",
            company_impact=f"Impacts ARPU growth and upsell potential for {target_operator}",
            impact_type="opportunity" if trend_dir == "improving" else "threat" if trend_dir == "worsening" else "neutral",
            severity="low",
            time_horizon="short_term",
            predictability="uncertain",
            evidence=[f"Consumer confidence: {latest_conf}"],
            data_source="macro_environment",
        ))

    # Ensure at least one factor
    if not factors:
        factors.append(PESTFactor(
            dimension="E",
            dimension_name="Economic",
            factor_name="Economic Environment",
            current_status="No economic data available",
            trend="N/A",
            trend_direction="uncertain",
            industry_impact="N/A",
            company_impact="N/A",
            impact_type="neutral",
            severity="low",
            time_horizon="medium_term",
            predictability="uncertain",
            evidence=[],
            data_source="N/A",
        ))

    return factors


# ---------------------------------------------------------------------------
# PEST: Society factors
# ---------------------------------------------------------------------------

def _build_society_factors(
    macro_data: list,
    events: list,
    target_operator: str,
    provenance,
) -> list[PESTFactor]:
    factors = []

    # -- 5G adoption (proxy for digital adoption / society change) --
    adoption_values = [m.get("five_g_adoption_pct") for m in macro_data if m.get("five_g_adoption_pct") is not None]
    if adoption_values:
        latest_5g = adoption_values[-1]
        trend_dir = _numeric_trend(adoption_values)
        factors.append(PESTFactor(
            dimension="S",
            dimension_name="Society",
            factor_name="5G Adoption Rate",
            current_status=f"5G adoption at {latest_5g}% of mobile subscribers",
            trend=f"5G adoption trend: {trend_dir} ({adoption_values[0]}% -> {latest_5g}%)" if len(adoption_values) > 1 else f"5G adoption at {latest_5g}%",
            trend_direction=trend_dir,
            industry_impact="Growing 5G adoption validates network investment and enables new use cases",
            company_impact=f"5G adoption growth supports premium pricing and new service revenue for {target_operator}",
            impact_type="opportunity",
            severity="high",
            time_horizon="medium_term",
            predictability="predictable",
            evidence=[f"5G adoption: {latest_5g}%"],
            data_source="macro_environment",
        ))
        _track(provenance, latest_5g, "five_g_adoption_pct", target_operator, unit="%")

    # -- Fiber penetration (society infrastructure readiness) --
    fiber_values = [m.get("fiber_penetration_pct") for m in macro_data if m.get("fiber_penetration_pct") is not None]
    if fiber_values:
        latest_fiber = fiber_values[-1]
        trend_dir = _numeric_trend(fiber_values)
        factors.append(PESTFactor(
            dimension="S",
            dimension_name="Society",
            factor_name="Fiber Broadband Penetration",
            current_status=f"Fiber penetration at {latest_fiber}%",
            trend=f"Fiber penetration trend: {trend_dir} ({fiber_values[0]}% -> {latest_fiber}%)" if len(fiber_values) > 1 else f"Fiber at {latest_fiber}%",
            trend_direction=trend_dir,
            industry_impact="Growing fiber adoption accelerates fixed broadband technology transition from copper/cable",
            company_impact=f"Fiber migration presents both investment challenge and growth opportunity for {target_operator}",
            impact_type="both",
            severity="high",
            time_horizon="medium_term",
            predictability="predictable",
            evidence=[f"Fiber penetration: {latest_fiber}%"],
            data_source="macro_environment",
        ))
        _track(provenance, latest_fiber, "fiber_penetration_pct", target_operator, unit="%")

    # -- Social events from intelligence --
    social_events = [e for e in events if e.get("category") in ("social", "demographic", "society")]
    for ev in social_events[:2]:
        factors.append(_event_to_pest_factor(ev, "S", "Society", target_operator))

    # Ensure at least one factor
    if not factors:
        factors.append(PESTFactor(
            dimension="S",
            dimension_name="Society",
            factor_name="Digital Adoption",
            current_status="No society data available",
            trend="N/A",
            trend_direction="uncertain",
            industry_impact="N/A",
            company_impact="N/A",
            impact_type="neutral",
            severity="low",
            time_horizon="medium_term",
            predictability="uncertain",
            evidence=[],
            data_source="N/A",
        ))

    return factors


# ---------------------------------------------------------------------------
# PEST: Technology factors
# ---------------------------------------------------------------------------

def _build_technology_factors(
    macro_data: list,
    events: list,
    target_operator: str,
    provenance,
) -> list[PESTFactor]:
    factors = []

    # -- 5G network status (from latest macro or telecom growth) --
    growth_values = [m.get("telecom_growth_pct") for m in macro_data if m.get("telecom_growth_pct") is not None]
    adoption_values = [m.get("five_g_adoption_pct") for m in macro_data if m.get("five_g_adoption_pct") is not None]

    if adoption_values:
        latest_5g = adoption_values[-1]
        if latest_5g >= 50:
            stage = "mass adoption"
            trend_dir = "improving"
        elif latest_5g >= 30:
            stage = "acceleration"
            trend_dir = "improving"
        elif latest_5g >= 10:
            stage = "early adoption"
            trend_dir = "improving"
        else:
            stage = "early deployment"
            trend_dir = "stable"

        factors.append(PESTFactor(
            dimension="T",
            dimension_name="Technology",
            factor_name="5G Network Evolution",
            current_status=f"5G in {stage} phase ({latest_5g}% adoption)",
            trend=f"5G transitioning from coverage race to monetization phase",
            trend_direction=trend_dir,
            industry_impact="5G enables network slicing, enterprise services, and FWA -- new revenue streams",
            company_impact=f"5G network capabilities are key competitive differentiator for {target_operator}",
            impact_type="opportunity",
            severity="high",
            time_horizon="medium_term",
            predictability="predictable",
            evidence=[f"5G adoption: {latest_5g}%"],
            data_source="macro_environment",
        ))

    # -- Fiber technology evolution --
    fiber_values = [m.get("fiber_penetration_pct") for m in macro_data if m.get("fiber_penetration_pct") is not None]
    if fiber_values:
        latest_fiber = fiber_values[-1]
        factors.append(PESTFactor(
            dimension="T",
            dimension_name="Technology",
            factor_name="Fiber/FTTH Deployment",
            current_status=f"Fiber penetration at {latest_fiber}%, indicating ongoing network modernization",
            trend="Fiber deployment accelerating as DSL/copper nears end of life",
            trend_direction="improving",
            industry_impact="Fiber replaces copper/cable as the fixed broadband standard, requiring massive CAPEX",
            company_impact=f"Fiber strategy (build vs buy vs partner) is a critical decision for {target_operator}",
            impact_type="both",
            severity="high",
            time_horizon="long_term",
            predictability="predictable",
            evidence=[f"Fiber penetration: {latest_fiber}%"],
            data_source="macro_environment",
        ))

    # -- Technology events from intelligence --
    tech_events = [e for e in events if e.get("category") in ("technology", "tech", "network")]
    for ev in tech_events[:3]:
        factors.append(_event_to_pest_factor(ev, "T", "Technology", target_operator))

    # Ensure at least one factor
    if not factors:
        factors.append(PESTFactor(
            dimension="T",
            dimension_name="Technology",
            factor_name="Technology Environment",
            current_status="No technology data available",
            trend="N/A",
            trend_direction="uncertain",
            industry_impact="N/A",
            company_impact="N/A",
            impact_type="neutral",
            severity="low",
            time_horizon="medium_term",
            predictability="uncertain",
            evidence=[],
            data_source="N/A",
        ))

    return factors


# ---------------------------------------------------------------------------
# Industry environment analysis
# ---------------------------------------------------------------------------

def _analyse_industry(
    market_ts: list,
    operators: list,
    n_quarters: int,
    provenance,
    market_config=None,
) -> dict:
    """Compute industry-level metrics from the market time series."""
    result = {
        "market_size": "",
        "growth_rate": "",
        "profit_trend": "",
        "concentration": "",
        "lifecycle_stage": "",
        "new_business_models": [],
        "technology_revolution": [],
        "key_success_factors": [],
        "value_transfer_trends": [],
    }

    if not market_ts:
        result["market_size"] = "N/A"
        result["growth_rate"] = "N/A"
        result["profit_trend"] = "N/A"
        result["concentration"] = "N/A"
        result["lifecycle_stage"] = "N/A"
        return result

    # Group data by calendar quarter
    by_quarter = {}
    for row in market_ts:
        cq = row.get("calendar_quarter", "")
        if cq not in by_quarter:
            by_quarter[cq] = []
        by_quarter[cq].append(row)

    sorted_quarters = sorted(by_quarter.keys())

    # -- Market size (latest quarter, sum of total_revenue) --
    if sorted_quarters:
        latest_q = sorted_quarters[-1]
        latest_rows = by_quarter[latest_q]
        total_rev = sum(r.get("total_revenue") or 0 for r in latest_rows)
        if total_rev > 0:
            currency = market_config.currency if market_config else "USD"
            rev_b = total_rev / 1000
            if rev_b >= 1000:
                result["market_size"] = f"{currency} {rev_b / 1000:.1f}T (quarterly, {latest_q})"
            else:
                result["market_size"] = f"{currency} {rev_b:.1f}B (quarterly, {latest_q})"
            _track_prov(provenance, total_rev, "industry_market_size", unit=f"{currency} M")
        else:
            result["market_size"] = "N/A"

    # -- Market growth rate (YoY) --
    if len(sorted_quarters) >= 5:
        # Compare latest quarter to same quarter one year ago (4 quarters back)
        latest_q = sorted_quarters[-1]
        yoy_q = sorted_quarters[-5] if len(sorted_quarters) >= 5 else sorted_quarters[0]
        rev_latest = sum(r.get("total_revenue") or 0 for r in by_quarter[latest_q])
        rev_yoy = sum(r.get("total_revenue") or 0 for r in by_quarter[yoy_q])
        if rev_yoy > 0 and rev_latest > 0:
            growth = (rev_latest - rev_yoy) / rev_yoy * 100
            result["growth_rate"] = f"{growth:+.1f}% YoY ({yoy_q} -> {latest_q})"
            _track_prov(provenance, growth, "industry_growth_rate", unit="%")

            # Lifecycle stage based on growth rate
            if growth > 10:
                result["lifecycle_stage"] = "growth"
            elif growth > 2:
                result["lifecycle_stage"] = "late_growth"
            elif growth > -1:
                result["lifecycle_stage"] = "mature"
            else:
                result["lifecycle_stage"] = "decline"
    elif len(sorted_quarters) >= 2:
        # Fallback: QoQ growth
        latest_q = sorted_quarters[-1]
        prev_q = sorted_quarters[-2]
        rev_latest = sum(r.get("total_revenue") or 0 for r in by_quarter[latest_q])
        rev_prev = sum(r.get("total_revenue") or 0 for r in by_quarter[prev_q])
        if rev_prev > 0 and rev_latest > 0:
            growth = (rev_latest - rev_prev) / rev_prev * 100
            result["growth_rate"] = f"{growth:+.1f}% QoQ ({prev_q} -> {latest_q})"
            if growth > 3:
                result["lifecycle_stage"] = "growth"
            elif growth > 0.5:
                result["lifecycle_stage"] = "mature"
            elif growth > -0.5:
                result["lifecycle_stage"] = "mature"
            else:
                result["lifecycle_stage"] = "decline"

    # -- Profit trend (EBITDA margin across quarters) --
    margin_by_q = {}
    for cq in sorted_quarters:
        rows = by_quarter[cq]
        total_ebitda = sum(r.get("ebitda") or 0 for r in rows)
        total_rev = sum(r.get("total_revenue") or 0 for r in rows)
        if total_rev > 0:
            margin_by_q[cq] = total_ebitda / total_rev * 100

    if len(margin_by_q) >= 2:
        margins = list(margin_by_q.values())
        if margins[-1] > margins[0] + 1:
            result["profit_trend"] = f"Improving (industry EBITDA margin {margins[-1]:.1f}%, up from {margins[0]:.1f}%)"
        elif margins[-1] < margins[0] - 1:
            result["profit_trend"] = f"Declining (industry EBITDA margin {margins[-1]:.1f}%, down from {margins[0]:.1f}%)"
        else:
            result["profit_trend"] = f"Stable (industry EBITDA margin ~{margins[-1]:.1f}%)"
    elif len(margin_by_q) == 1:
        m = list(margin_by_q.values())[0]
        result["profit_trend"] = f"Current industry EBITDA margin: {m:.1f}%"

    # -- Market concentration (CR4 in latest quarter) --
    if sorted_quarters:
        latest_q = sorted_quarters[-1]
        latest_rows = by_quarter[latest_q]
        revenues = sorted(
            [(r.get("total_revenue") or 0) for r in latest_rows],
            reverse=True,
        )
        total = sum(revenues)
        if total > 0:
            top4 = sum(revenues[:4])
            cr4 = top4 / total * 100
            result["concentration"] = f"CR4 = {cr4:.0f}%"

            # Individual shares
            shares = []
            for r in sorted(latest_rows, key=lambda x: x.get("total_revenue") or 0, reverse=True):
                name = r.get("display_name", r.get("operator_id", ""))
                rev = r.get("total_revenue") or 0
                if rev > 0:
                    share = rev / total * 100
                    shares.append(f"{name}: {share:.1f}%")
            if shares:
                result["concentration"] += " (" + ", ".join(shares[:4]) + ")"
            _track_prov(provenance, cr4, "industry_concentration", unit="%")

    # -- Standard industry insights for telecom --
    result["new_business_models"] = [
        "FWA (Fixed Wireless Access) as fiber alternative",
        "Network-as-a-Service for enterprise verticals",
        "Wholesale/MVNO partnerships for coverage monetization",
    ]
    result["technology_revolution"] = [
        "5G SA enabling network slicing and enterprise services",
        "AI/ML for network optimization and customer experience",
        "Open RAN for vendor diversification and cost reduction",
    ]
    result["key_success_factors"] = [
        "Network quality and coverage breadth",
        "Convergent (FMC) bundling strategy",
        "B2B/ICT capabilities for enterprise growth",
        "Operational efficiency (OPEX/revenue ratio)",
    ]
    result["value_transfer_trends"] = [
        "Value shifting from voice/SMS to data and digital services",
        "B2B/ICT growing faster than consumer segment",
        "Fiber displacing copper and cable broadband",
    ]

    return result


# ---------------------------------------------------------------------------
# PEST summary helpers
# ---------------------------------------------------------------------------

def _extract_policy_opportunities(factors: list[PESTFactor]) -> list[str]:
    return [
        f.factor_name + ": " + (f.company_impact or f.industry_impact)
        for f in factors
        if f.impact_type in ("opportunity", "both")
    ]


def _extract_policy_threats(factors: list[PESTFactor]) -> list[str]:
    return [
        f.factor_name + ": " + (f.company_impact or f.industry_impact)
        for f in factors
        if f.impact_type in ("threat", "both")
    ]


def _summarise_tech_market(factors: list[PESTFactor]) -> str:
    opp_factors = [f for f in factors if f.impact_type in ("opportunity", "both")]
    if opp_factors:
        return "; ".join(f.factor_name for f in opp_factors)
    return "N/A"


def _assess_weather(
    political: list[PESTFactor],
    economic: list[PESTFactor],
    society: list[PESTFactor],
    technology: list[PESTFactor],
) -> tuple[str, str]:
    """Assess overall 'weather' from PEST factors."""
    all_factors = political + economic + society + technology
    if not all_factors:
        return "mixed", "Insufficient data to assess macro environment"

    opp_count = sum(1 for f in all_factors if f.impact_type in ("opportunity", "both"))
    threat_count = sum(1 for f in all_factors if f.impact_type in ("threat", "both"))
    high_threat_count = sum(1 for f in all_factors if f.impact_type == "threat" and f.severity == "high")
    total = len(all_factors)

    opp_ratio = opp_count / total if total > 0 else 0
    threat_ratio = threat_count / total if total > 0 else 0

    if high_threat_count >= 3:
        weather = "stormy"
        explanation = f"Multiple high-severity threats ({high_threat_count}) dominate the macro environment"
    elif opp_ratio > 0.6:
        weather = "sunny"
        explanation = f"Mostly favorable: {opp_count}/{total} factors present opportunities"
    elif threat_ratio > 0.5:
        weather = "cloudy"
        explanation = f"Challenging environment: {threat_count}/{total} factors pose threats"
    else:
        weather = "mixed"
        explanation = f"Mixed outlook: {opp_count} opportunities vs {threat_count} threats out of {total} factors"

    return weather, explanation


def _pest_key_message(
    weather: str,
    political: list[PESTFactor],
    economic: list[PESTFactor],
    society: list[PESTFactor],
    technology: list[PESTFactor],
) -> str:
    """Generate a one-line summary for the PEST analysis."""
    all_factors = political + economic + society + technology
    if not all_factors:
        return "Insufficient data for PEST analysis"

    high_opps = [f for f in all_factors if f.impact_type in ("opportunity", "both") and f.severity == "high"]
    high_threats = [f for f in all_factors if f.impact_type in ("threat", "both") and f.severity == "high"]

    parts = []
    weather_map = {
        "sunny": "Favorable",
        "mixed": "Mixed",
        "cloudy": "Challenging",
        "stormy": "Hostile",
    }
    parts.append(f"Macro environment: {weather_map.get(weather, weather)}.")

    if high_opps:
        opp_names = ", ".join(f.factor_name for f in high_opps[:2])
        parts.append(f"Key opportunities: {opp_names}.")
    if high_threats:
        threat_names = ", ".join(f.factor_name for f in high_threats[:2])
        parts.append(f"Key risks: {threat_names}.")

    return " ".join(parts)


# ---------------------------------------------------------------------------
# Top-level key message
# ---------------------------------------------------------------------------

def _build_key_message(pest: PESTAnalysis, ind: dict, market: str) -> str:
    """Build the overall TrendAnalysis key message."""
    parts = []

    if pest.key_message:
        # Strip trailing period to avoid double-period when joining
        parts.append(pest.key_message.rstrip("."))

    if ind.get("lifecycle_stage") and ind["lifecycle_stage"] != "N/A":
        stage_map = {
            "growth": "growing",
            "late_growth": "in late growth phase",
            "mature": "mature",
            "decline": "in decline",
        }
        stage_label = stage_map.get(ind["lifecycle_stage"], ind["lifecycle_stage"])
        lifecycle_part = f"Industry is {stage_label}."
        if ind.get("growth_rate") and ind["growth_rate"] != "N/A":
            lifecycle_part += f" ({ind['growth_rate']})"
        parts.append(lifecycle_part)

    if not parts:
        return f"Trend analysis for {market} market completed with available data"

    return " ".join(parts)


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _derive_company_impact(event: dict, dimension: str, target_operator: str) -> str:
    """Generate meaningful company-specific impact text from an event.

    Incorporates the event title/description to create contextual impact
    statements rather than generic templates.
    """
    title = event.get("title", "")
    impact = event.get("impact_type", "neutral")
    event_op = event.get("operator_id", "")

    # Shorten the event title for embedding in impact text
    short_title = title[:80].rstrip(".") if title else "this development"

    # If the event is about the target operator directly
    if event_op and event_op.replace("_", " ").lower() in target_operator.replace("_", " ").lower():
        if impact == "positive":
            return f"{short_title} strengthens {target_operator} competitive position and market presence"
        elif impact == "negative":
            return f"{short_title} increases operational pressure on {target_operator}"
        return f"{short_title} directly affects {target_operator} strategy"

    # If the event is about a competitor
    if event_op and event_op != target_operator:
        op_display = event_op.replace("_", " ").title()
        if impact == "positive":
            return f"{short_title}: {op_display} strengthening increases competitive pressure on {target_operator}"
        elif impact == "negative":
            return f"{short_title}: {op_display} setback may create market share opportunity for {target_operator}"
        return f"{short_title}: requires strategic response from {target_operator}"

    # Market-wide / regulatory events — combine template with event details
    dim_templates = {
        "P": {
            "positive": f"{short_title}: may create new market access or subsidy opportunities for {target_operator}",
            "negative": f"{short_title}: may increase compliance costs or restrict {target_operator} operations",
            "neutral": f"{short_title}: requires {target_operator} to monitor and adapt strategy",
        },
        "E": {
            "positive": f"{short_title}: supports consumer spending and {target_operator} revenue growth",
            "negative": f"{short_title}: may constrain {target_operator} revenue and increase cost pressure",
            "neutral": f"{short_title}: affects {target_operator} demand environment",
        },
        "S": {
            "positive": f"{short_title}: creates new service demand for {target_operator}",
            "negative": f"{short_title}: may erode {target_operator} traditional revenue streams",
            "neutral": f"{short_title}: affects {target_operator} customer base dynamics",
        },
        "T": {
            "positive": f"{short_title}: enables new services and efficiency gains for {target_operator}",
            "negative": f"{short_title}: may require significant {target_operator} investment to stay competitive",
            "neutral": f"{short_title}: requires {target_operator} to evaluate build vs buy vs partner",
        },
    }
    dim_map = dim_templates.get(dimension, dim_templates["T"])
    return dim_map.get(impact, dim_map["neutral"])


def _event_to_pest_factor(
    event: dict,
    dimension: str,
    dimension_name: str,
    target_operator: str,
) -> PESTFactor:
    """Convert an intelligence event into a PESTFactor."""
    impact = event.get("impact_type", "neutral")
    impact_map = {
        "positive": "opportunity",
        "negative": "threat",
        "neutral": "neutral",
    }
    return PESTFactor(
        dimension=dimension,
        dimension_name=dimension_name,
        factor_name=event.get("title", "Unknown Event"),
        current_status=event.get("description", ""),
        trend=event.get("description", ""),
        trend_direction="uncertain",
        industry_impact=event.get("description", ""),
        company_impact=_derive_company_impact(event, dimension, target_operator),
        impact_type=impact_map.get(impact, "neutral"),
        severity=event.get("severity", "medium"),
        time_horizon="short_term",
        predictability="uncertain",
        evidence=[event.get("source_url", "")] if event.get("source_url") else [],
        data_source="intelligence_events",
    )


def _numeric_trend(values: list, lower_is_better: bool = False) -> str:
    """Determine trend direction from a list of numeric values.

    Returns one of: 'improving', 'worsening', 'stable', 'uncertain'.
    """
    if not values or len(values) < 2:
        return "uncertain"

    first_half = values[: len(values) // 2]
    second_half = values[len(values) // 2:]

    avg_first = sum(first_half) / len(first_half)
    avg_second = sum(second_half) / len(second_half)

    diff = avg_second - avg_first
    threshold = abs(avg_first) * 0.05 if avg_first != 0 else 0.1

    if abs(diff) < threshold:
        return "stable"

    going_up = diff > 0
    if lower_is_better:
        return "worsening" if going_up else "improving"
    else:
        return "improving" if going_up else "worsening"


def _infer_trend_from_texts(texts: list) -> str:
    """Infer trend direction from a list of text descriptions.

    Simple heuristic: if texts are identical across quarters, it's stable.
    """
    if not texts:
        return "uncertain"
    unique = set(texts)
    if len(unique) == 1:
        return "stable"
    return "uncertain"


def _track(provenance, value, field_name, operator, period=None, unit=None):
    """Track a value in provenance store if available."""
    if provenance is not None:
        try:
            provenance.track(
                value=value,
                field_name=field_name,
                operator=operator,
                period=period,
                unit=unit,
            )
        except Exception:
            pass


def _track_prov(provenance, value, field_name, unit=None):
    """Track a computed value in provenance store."""
    if provenance is not None:
        try:
            provenance.track(value=value, field_name=field_name, unit=unit)
        except Exception:
            pass
