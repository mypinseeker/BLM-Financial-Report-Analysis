"""Module 01: Trends — PEST Deep Analysis renderer.

Produces the Trends/PEST section containing:
1. Industry Landscape Snapshot
2. PEST Weather Summary
3. Political/Economic/Social/Technology Factors (detailed)
4. Value Transfer & Emerging Models
5. Impact Matrix & Net Assessment
"""
from __future__ import annotations

from ..md_utils import (
    section_header, section_divider, md_table, md_kv_table,
    bold, bullet_list, code_block,
    safe_get, safe_list, safe_dict,
    operator_display_name, market_display_name,
    empty_section_notice,
)


def render_trends(result, diagnosis, config) -> str:
    """Render Module 01: Trends/PEST Analysis."""
    trends = result.trends
    if trends is None:
        return empty_section_notice("Trends/PEST")

    parts = []
    market_name = market_display_name(result.market) if result.market else "Market"
    period = result.analysis_period or ""
    target_op = result.target_operator or ""

    # Module title
    parts.append(f"# {market_name.split()[0]} Telecom Macro Trends — PEST Deep Analysis ({period})")
    parts.append("")
    parts.append(f"**Data basis**: PEST framework | {_count_factors(trends)} macro factors | "
                 f"{period} market data | Regulatory/event intelligence | Industry lifecycle assessment")
    parts.append("")
    parts.append("---")

    # 1. Industry Landscape
    parts.append(_render_landscape(trends, config))

    # 2. PEST Weather Summary
    parts.append(_render_pest_weather(trends))

    # 3-6. Detailed PEST factors
    parts.append(_render_pest_details(trends, target_op))

    # 7. Value Transfer
    parts.append(_render_value_transfer(trends))

    # 8. Impact Matrix
    parts.append(_render_impact_matrix(trends, diagnosis, target_op))

    return "\n\n".join(p for p in parts if p)


# ---------------------------------------------------------------------------
# Sub-renderers
# ---------------------------------------------------------------------------

def _render_landscape(trends, config) -> str:
    lines = [section_header("1. Industry Landscape Snapshot", 2)]

    # 1.1 Market Fundamentals
    lines.append("")
    lines.append(section_header("1.1 Market Fundamentals", 3))
    lines.append("")

    rows = []
    ms = safe_get(trends, "industry_market_size", "")
    if ms:
        rows.append(["Market size", bold(str(ms)), "Market scale"])
    gr = safe_get(trends, "industry_growth_rate", "")
    if gr:
        rows.append(["YoY growth", bold(str(gr)), _growth_assessment(gr)])
    pt = safe_get(trends, "industry_profit_trend", "")
    if pt:
        rows.append(["Profit trend", str(pt), ""])
    conc = safe_get(trends, "industry_concentration", "")
    if conc:
        rows.append(["Concentration", bold(str(conc)), "Market structure"])
    lc = safe_get(trends, "industry_lifecycle_stage", "")
    if lc:
        rows.append(["Lifecycle stage", bold(lc.title()), _lifecycle_explanation(lc)])

    if rows:
        lines.append(md_table(["Metric", "Value", "Assessment"], rows))
    else:
        lines.append("*Industry landscape data not available.*")

    # Key insight
    if lc:
        lines.append("")
        lines.append(f"**Key insight**: The market is in the **{lc}** phase. "
                     f"{_lifecycle_explanation(lc)}")

    # 1.2 Revenue Distribution (from comparison table)
    lines.append("")
    lines.append(section_header("1.2 Industry Lifecycle — Implications", 3))
    lines.append("")

    ksf = safe_list(trends, "key_success_factors")
    if ksf:
        lines.append(f"Being in the **{lc or 'current'}** phase means:")
        for f in ksf:
            lines.append(f"- {f}")
    elif lc:
        implications = _lifecycle_implications(lc)
        for imp in implications:
            lines.append(f"- {imp}")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_pest_weather(trends) -> str:
    pest = safe_get(trends, "pest")
    if pest is None:
        return ""

    lines = [section_header("2. PEST Analysis — Full Assessment", 2)]
    lines.append("")
    lines.append(section_header("2.1 Overall PEST Weather", 3))
    lines.append("")

    # Summary table per dimension
    dimensions = [
        ("Political", safe_list(pest, "political_factors")),
        ("Economic", safe_list(pest, "economic_factors")),
        ("Social", safe_list(pest, "society_factors")),
        ("Technology", safe_list(pest, "technology_factors")),
    ]

    rows = []
    total_factors = 0
    total_opps = 0
    total_threats = 0

    for dim_name, factors in dimensions:
        n = len(factors)
        opps = sum(1 for f in factors if safe_get(f, "impact_type") in ("opportunity", "both"))
        threats = sum(1 for f in factors if safe_get(f, "impact_type") in ("threat", "both"))
        total_factors += n
        total_opps += opps
        total_threats += threats

        net = _net_assessment(opps, threats)
        rows.append([bold(dim_name), str(n), str(opps), str(threats), net])

    rows.append([
        bold("Total"), bold(str(total_factors)), bold(str(total_opps)),
        bold(str(total_threats)),
        bold(f"Net {'favorable' if total_opps > total_threats else 'challenging'} "
             f"({total_opps} opps vs {total_threats} threats)")
    ])

    lines.append(md_table(
        ["Dimension", "# Factors", "Opportunities", "Threats", "Net Assessment"],
        rows
    ))

    weather = safe_get(pest, "overall_weather", "mixed")
    explanation = safe_get(pest, "weather_explanation", "")
    if explanation:
        lines.append("")
        lines.append(f"**Overall weather**: {weather.title()} — {explanation}")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_pest_details(trends, target_op: str = "") -> str:
    pest = safe_get(trends, "pest")
    if pest is None:
        return ""

    target_display = operator_display_name(target_op) if target_op else "the operator"

    sections = []
    section_num = 3
    dimension_map = [
        ("Political", "political_factors", "Regulatory & Policy"),
        ("Economic", "economic_factors", "Macro Headwinds"),
        ("Social", "society_factors", "Consumer Behavior Shifts"),
        ("Technology", "technology_factors", "The Transformation Agenda"),
    ]

    for dim_name, attr, subtitle in dimension_map:
        factors = safe_list(pest, attr)
        if not factors:
            section_num += 1
            continue

        lines = [section_header(f"{section_num}. {dim_name} Factors — {subtitle}", 2)]
        section_num += 1

        for i, factor in enumerate(factors, 1):
            fname = safe_get(factor, "factor_name", f"Factor {i}")
            lines.append("")
            lines.append(section_header(f"{section_num - 1}.{i} {fname}", 3))
            lines.append("")

            # Factor detail table
            detail_rows = []
            severity = safe_get(factor, "severity", "")
            if severity:
                detail_rows.append(["Severity", bold(severity.title())])
            trend_dir = safe_get(factor, "trend_direction", "")
            if trend_dir:
                detail_rows.append(["Trend", trend_dir.title()])
            impact_type = safe_get(factor, "impact_type", "")
            if impact_type:
                detail_rows.append(["Impact type", impact_type.title()])
            time_h = safe_get(factor, "time_horizon", "")
            if time_h:
                detail_rows.append(["Time horizon", time_h.replace("_", " ").title()])

            if detail_rows:
                lines.append(md_table(["Factor", "Detail"], detail_rows))

            # Status and impact descriptions
            status = safe_get(factor, "current_status", "")
            if status:
                lines.append("")
                lines.append(f"**Current status**: {status}")

            industry_impact = safe_get(factor, "industry_impact", "")
            # Skip industry_impact if identical to current_status (dedup)
            if industry_impact and industry_impact != status:
                lines.append("")
                lines.append(f"**Industry impact**: {industry_impact}")

            company_impact = safe_get(factor, "company_impact", "")
            if company_impact:
                # Replace raw operator_id with display name
                if target_op:
                    company_impact = company_impact.replace(target_op, target_display)
                lines.append("")
                lines.append(f"**Company impact**: {company_impact}")

            # Evidence
            evidence = safe_list(factor, "evidence")
            if evidence:
                lines.append("")
                for e in evidence[:3]:
                    lines.append(f"- {e}")

        lines.append("")
        lines.append("---")
        sections.append("\n".join(lines))

    return "\n\n".join(sections)


def _render_value_transfer(trends) -> str:
    vt = safe_list(trends, "value_transfer_trends")
    nbm = safe_list(trends, "new_business_models")
    tr = safe_list(trends, "technology_revolution")

    if not vt and not nbm and not tr:
        return ""

    lines = [section_header("Value Transfer & Emerging Models", 2)]

    if vt:
        lines.append("")
        lines.append(section_header("Value Migration Map", 3))
        lines.append("")
        for item in vt:
            lines.append(f"- {item}")

    if nbm:
        lines.append("")
        lines.append(section_header("New Business Models", 3))
        lines.append("")
        for item in nbm:
            lines.append(f"- {item}")

    if tr:
        lines.append("")
        lines.append(section_header("Technology Revolution", 3))
        lines.append("")
        for item in tr:
            lines.append(f"- {item}")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_impact_matrix(trends, diagnosis, target_op: str = "") -> str:
    target_display = operator_display_name(target_op) if target_op else "the operator"
    lines = [section_header("Impact Assessment & Net Assessment", 2)]
    lines.append("")

    km = safe_get(trends, "key_message", "")
    if km:
        if target_op:
            km = km.replace(target_op, target_display)
        lines.append(f"**Key message**: {km}")
        lines.append("")

    lines.append(f"**Net assessment**: {diagnosis.trends_net_assessment}")
    lines.append("")

    # Policy opportunities and threats
    pest = safe_get(trends, "pest")
    if pest:
        opps = safe_list(pest, "policy_opportunities")
        threats = safe_list(pest, "policy_threats")
        if opps:
            lines.append(section_header("Policy Opportunities", 3))
            lines.append("")
            for o in opps:
                if target_op:
                    o = o.replace(target_op, target_display)
                lines.append(f"- {o}")
            lines.append("")
        if threats:
            lines.append(section_header("Policy Threats", 3))
            lines.append("")
            for t in threats:
                if target_op:
                    t = t.replace(target_op, target_display)
                lines.append(f"- {t}")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _count_factors(trends) -> int:
    pest = safe_get(trends, "pest")
    if pest is None:
        return 0
    return (len(safe_list(pest, "political_factors")) +
            len(safe_list(pest, "economic_factors")) +
            len(safe_list(pest, "society_factors")) +
            len(safe_list(pest, "technology_factors")))


def _growth_assessment(growth_str) -> str:
    try:
        val = float(str(growth_str).replace("%", "").replace("+", "").strip())
        if val < 0:
            return "Contracting market"
        elif val < 1:
            return "Near-zero — barely above inflation"
        elif val < 3:
            return "Slow growth"
        else:
            return "Healthy growth"
    except (ValueError, TypeError):
        return ""


def _lifecycle_explanation(stage: str) -> str:
    explanations = {
        "growth": "Market expansion still driving overall revenue growth.",
        "mature": "Growth from market expansion is over; competition becomes zero-sum.",
        "decline": "Structural contraction underway; optimization and consolidation required.",
        "introduction": "Market is forming with first-mover opportunities.",
    }
    return explanations.get(stage.lower(), "")


def _lifecycle_implications(stage: str) -> list[str]:
    impls = {
        "mature": [
            "Volume growth is exhausted — high penetration rates across segments",
            "Competition shifts from acquisition to retention and upsell",
            "ARPU defense becomes more important than subscriber growth",
            "Convergence (FMC) and B2B/enterprise are remaining growth pockets",
            "Cost optimization and operational efficiency drive profitability",
            "Regulatory and technology shifts are the primary disruptors",
        ],
        "growth": [
            "Subscriber acquisition still the primary driver",
            "Network coverage expansion critical",
            "Market share battles define long-term positioning",
        ],
        "decline": [
            "Revenue optimization over growth",
            "Consolidation likely",
            "Cost efficiency becomes paramount",
        ],
    }
    return impls.get(stage.lower(), ["Industry dynamics apply"])


def _net_assessment(opps: int, threats: int) -> str:
    if opps > threats * 2:
        return "Strongly favorable"
    elif opps > threats:
        return "Favorable"
    elif opps == threats:
        return "Mixed"
    elif threats > opps * 2:
        return "Challenging"
    else:
        return "Slight headwind"
