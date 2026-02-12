"""Module 05: Opportunities — SPAN Matrix renderer.

Produces the Opportunities section containing:
1. SPAN Matrix Overview
2. Grow/Invest Opportunities
3. Acquire Skills Opportunities
4. Harvest / Avoid Items
5. Portfolio Prioritization
6. Financial Impact Assessment
7. Strategic Recommendations
"""
from __future__ import annotations

from ..md_utils import (
    section_header, section_divider, md_table,
    bold, bullet_list, fmt_pct,
    safe_get, safe_list, safe_dict,
    operator_display_name,
    empty_section_notice,
)


def render_opportunities(result, diagnosis, config) -> str:
    """Render Module 05: Opportunities (SPAN Matrix) Analysis."""
    opp = result.opportunities
    if opp is None:
        return empty_section_notice("Opportunities (SPAN)")

    parts = []
    target_name = operator_display_name(result.target_operator)
    period = result.analysis_period or ""

    # Module title
    parts.append(f"# Opportunities Analysis — SPAN Matrix ({period})")
    parts.append("")
    parts.append(f"**Protagonist**: {target_name}")
    parts.append(f"**Framework**: SPAN (Strategy Positioning and Action Navigation) Matrix")
    parts.append("")
    parts.append("---")

    # 1. SPAN Matrix Overview
    parts.append(_render_span_overview(opp))

    # 2. Grow/Invest
    parts.append(_render_quadrant_detail(opp, "grow_invest", "Grow/Invest",
                                          "Execute aggressively — highest priority"))

    # 3. Acquire Skills
    parts.append(_render_quadrant_detail(opp, "acquire_skills", "Acquire Skills",
                                          "Build capability before competing"))

    # 4. Harvest / Avoid
    parts.append(_render_harvest_avoid(opp))

    # 5. Priority Ranking
    parts.append(_render_priority_ranking(opp))

    # 6. Financial Impact
    parts.append(_render_financial_impact(opp, diagnosis))

    # 7. Strategic Recommendations
    parts.append(_render_recommendations(opp, diagnosis))

    return "\n\n".join(p for p in parts if p)


# ---------------------------------------------------------------------------
# Sub-renderers
# ---------------------------------------------------------------------------

def _render_span_overview(opp) -> str:
    positions = safe_list(opp, "span_positions")
    gi = safe_list(opp, "grow_invest")
    ask = safe_list(opp, "acquire_skills")
    harvest = safe_list(opp, "harvest")
    avoid = safe_list(opp, "avoid_exit")

    lines = [section_header("1. SPAN Matrix Overview", 2), ""]

    # Quadrant distribution
    total = len(gi) + len(ask) + len(harvest) + len(avoid)
    if total == 0:
        total = len(positions)

    def pct(n):
        return f"{n / total * 100:.0f}%" if total > 0 else "—"

    dist_rows = [
        ["Grow/Invest", str(len(gi)), pct(len(gi)),
         "Execute aggressively — highest priority"],
        ["Acquire Skills", str(len(ask)), pct(len(ask)),
         "Build capabilities before competing"],
        ["Harvest", str(len(harvest)), pct(len(harvest)),
         "Extract value from declining positions"],
        ["Avoid/Exit", str(len(avoid)), pct(len(avoid)),
         "Do not invest — exit if possible"],
    ]

    lines.append(md_table(["Quadrant", "Count", "Share", "Action"], dist_rows))

    # SPAN positions table (detailed)
    if positions:
        lines.append("")
        lines.append(section_header("SPAN Position Details", 3))
        lines.append("")

        pos_rows = []
        for p in positions:
            name = safe_get(p, "opportunity_name", "")
            ma = safe_get(p, "market_attractiveness", 0)
            cp = safe_get(p, "competitive_position", 0)
            quad = safe_get(p, "quadrant", "").replace("_", " ").title()
            strategy = safe_get(p, "recommended_strategy", "")

            ma_str = f"{float(ma):.1f}" if ma else "—"
            cp_str = f"{float(cp):.1f}" if cp else "—"

            pos_rows.append([name, ma_str, cp_str, quad, strategy[:50]])

        lines.append(md_table(
            ["Opportunity", "Mkt Attractiveness", "Comp Position", "Quadrant", "Strategy"],
            pos_rows
        ))

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_quadrant_detail(opp, attr: str, title: str, description: str) -> str:
    items = safe_list(opp, attr)
    if not items:
        return ""

    lines = [section_header(f"2. {title} Opportunities", 2)]
    lines.append(f"*{description}*")
    lines.append("")

    # Match items with detailed opportunity records
    opportunities = safe_list(opp, "opportunities")
    opp_map = {}
    for o in opportunities:
        name = safe_get(o, "name", "")
        if name:
            opp_map[name.lower()] = o

    for i, item in enumerate(items, 1):
        lines.append(f"### {i}. {item}")
        lines.append("")

        # Try to find detailed record
        detail = opp_map.get(item.lower())
        if detail:
            desc = safe_get(detail, "description", "")
            if desc:
                lines.append(desc)
                lines.append("")

            detail_rows = []
            am = safe_get(detail, "addressable_market", "")
            if am and am != "N/A":
                detail_rows.append(["Addressable market", str(am)])
            cap = safe_get(detail, "our_capability", "")
            if cap:
                detail_rows.append(["Our capability", cap])
            comp_int = safe_get(detail, "competition_intensity", "")
            if comp_int:
                detail_rows.append(["Competition intensity", comp_int])
            tw = safe_get(detail, "time_window", "")
            if tw:
                detail_rows.append(["Time window", tw])
            pr = safe_get(detail, "priority", "")
            if pr:
                detail_rows.append(["Priority", bold(pr)])
            rat = safe_get(detail, "priority_rationale", "")
            if rat:
                detail_rows.append(["Rationale", rat])

            if detail_rows:
                lines.append(md_table(["Aspect", "Detail"], detail_rows))
                lines.append("")

            derived = safe_list(detail, "derived_from")
            if derived:
                lines.append(f"*Derived from: {', '.join(derived)}*")
                lines.append("")

    lines.append("---")

    return "\n".join(lines)


def _render_harvest_avoid(opp) -> str:
    harvest = safe_list(opp, "harvest")
    avoid = safe_list(opp, "avoid_exit")

    if not harvest and not avoid:
        return ""

    lines = [section_header("4. Harvest & Avoid/Exit", 2), ""]

    if harvest:
        lines.append(section_header("Harvest", 3))
        lines.append("*Extract remaining value — do not invest for growth*")
        lines.append("")
        for item in harvest:
            lines.append(f"- {item}")
        lines.append("")

    if avoid:
        lines.append(section_header("Avoid/Exit", 3))
        lines.append("*No viable path — exit or do not enter*")
        lines.append("")
        for item in avoid:
            lines.append(f"- {item}")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_priority_ranking(opp) -> str:
    opportunities = safe_list(opp, "opportunities")
    if not opportunities:
        return ""

    lines = [section_header("5. Portfolio Prioritization", 2), ""]

    # Group by priority
    p0 = [o for o in opportunities if safe_get(o, "priority") == "P0"]
    p1 = [o for o in opportunities if safe_get(o, "priority") == "P1"]
    p2 = [o for o in opportunities if safe_get(o, "priority") == "P2"]
    other = [o for o in opportunities if safe_get(o, "priority") not in ("P0", "P1", "P2")]

    for label, items, desc in [
        ("P0 — Must Do (Existential)", p0, "Failure to execute threatens survival or core business"),
        ("P1 — Should Do (Strategic)", p1, "High-impact strategic initiatives"),
        ("P2 — Could Do (Opportunistic)", p2, "Worthwhile if resources allow"),
    ]:
        if not items:
            continue
        lines.append(section_header(label, 3))
        lines.append(f"*{desc}*")
        lines.append("")

        rows = []
        for o in items:
            name = safe_get(o, "name", "")
            market = safe_get(o, "addressable_market", "N/A")
            window = safe_get(o, "time_window", "")
            capability = safe_get(o, "our_capability", "")
            rows.append([name, str(market), window, capability])

        lines.append(md_table(
            ["Opportunity", "Addressable Market", "Time Window", "Capability"],
            rows
        ))
        lines.append("")

    # Window opportunities
    windows = safe_list(opp, "window_opportunities")
    if windows:
        lines.append(section_header("Time-Sensitive Windows", 3))
        lines.append("")
        for w in windows:
            lines.append(f"- {w}")
        lines.append("")

    lines.append("---")

    return "\n".join(lines)


def _render_financial_impact(opp, diagnosis) -> str:
    opportunities = safe_list(opp, "opportunities")
    if not opportunities:
        return ""

    lines = [section_header("6. Financial Impact Assessment", 2), ""]

    # Build financial summary from available data
    rows = []
    for o in opportunities[:10]:
        name = safe_get(o, "name", "")
        market = safe_get(o, "addressable_market", "N/A")
        priority = safe_get(o, "priority", "")
        rows.append([name, priority, str(market)])

    if rows:
        lines.append(md_table(["Opportunity", "Priority", "Addressable Market"], rows))
        lines.append("")

    # Risk/reward reference
    if diagnosis.bull_case:
        lines.append(f"**Bull case (full execution)**: {diagnosis.bull_case.get('revenue_impact', '')}")
    if diagnosis.bear_case:
        lines.append(f"**Bear case (no execution)**: {diagnosis.bear_case.get('revenue_impact', '')}")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_recommendations(opp, diagnosis) -> str:
    km = safe_get(opp, "key_message", "")

    lines = [section_header("7. Strategic Recommendations", 2), ""]

    if km:
        lines.append(f"**Key message**: {km}")
        lines.append("")

    # Derive recommendations from priorities
    priorities = diagnosis.priorities
    if priorities:
        lines.append(section_header("Immediate Actions (Next Quarter)", 3))
        lines.append("")
        immediate = [p for p in priorities if
                     p.get("time_window", "").lower() in ("immediate", "now", "")][:3]
        if not immediate:
            immediate = priorities[:2]
        for p in immediate:
            lines.append(f"- **{p.get('name', '')}**: {p.get('description', p.get('how', ''))[:100]}")
        lines.append("")

        medium = [p for p in priorities if
                  any(x in p.get("time_window", "").lower() for x in ("1-2", "2-3", "medium"))]
        if medium:
            lines.append(section_header("Medium-Term Initiatives (1-3 Years)", 3))
            lines.append("")
            for p in medium[:3]:
                lines.append(f"- **{p.get('name', '')}**: {p.get('description', p.get('how', ''))[:100]}")
            lines.append("")

        long_term = [p for p in priorities if
                     any(x in p.get("time_window", "").lower() for x in ("3-5", "long"))]
        if long_term:
            lines.append(section_header("Long-Term Transformation (3-5 Years)", 3))
            lines.append("")
            for p in long_term[:3]:
                lines.append(f"- **{p.get('name', '')}**: {p.get('description', p.get('how', ''))[:100]}")
            lines.append("")

    lines.append(f"**Net assessment**: {diagnosis.opportunities_net_assessment}")
    lines.append("")
    lines.append("---")

    return "\n".join(lines)
