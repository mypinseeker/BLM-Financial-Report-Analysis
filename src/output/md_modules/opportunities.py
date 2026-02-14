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

import re

from ..md_utils import (
    section_header, section_divider, md_table,
    bold, bullet_list, fmt_pct,
    safe_get, safe_list, safe_dict,
    operator_display_name,
    collect_operator_ids, replace_operator_ids,
    empty_section_notice,
    filter_findings_by_feedback,
)


def _descriptive_label(name: str, detail: dict = None) -> str:
    """Convert generic SO-1/WO-1/ST-1/WT-1 labels into descriptive names.

    Also shortens verbose opportunity names for section headers.
    """
    # If it's a SWOT strategy ID, extract label from description
    if re.match(r'^(SO|WO|ST|WT)-\d+$', name):
        desc = safe_get(detail, "description", "") if detail else ""
        if not desc:
            return name
        # Extract key phrases from strategy description
        m = re.search(r"'([^':]+?)(?:: score|\s*')", desc)
        capability = m.group(1).strip() if m else ""
        m2 = re.search(r"(?:opportunity|threat) of '([^':]+?)(?:: |')", desc)
        target = m2.group(1).strip() if m2 else ""
        prefix_map = {"SO": "Leverage", "WO": "Address", "ST": "Defend", "WT": "Mitigate"}
        prefix = prefix_map.get(name.split("-")[0], "Act on")
        if capability and target:
            target_short = target[:40] + "..." if len(target) > 40 else target
            return f"{prefix} {capability} → {target_short}"
        if capability:
            return f"{prefix} {capability}"
        return desc[:60] + "..." if len(desc) > 60 else desc

    # Shorten overly verbose names
    if len(name) > 70:
        return name[:67] + "..."
    return name


def render_opportunities(result, diagnosis, config, feedback=None) -> str:
    """Render Module 05: Opportunities (SPAN Matrix) Analysis."""
    opp = result.opportunities
    if opp is None:
        return empty_section_notice("Opportunities (SPAN)")

    parts = []
    op_map = collect_operator_ids(result)
    target_op = result.target_operator or ""
    target_name = operator_display_name(target_op)
    period = result.analysis_period or ""

    # Module title
    parts.append(f"# Opportunities Analysis — SPAN Matrix ({period})")
    parts.append("")
    parts.append(f"**Protagonist**: {target_name}")
    parts.append(f"**Framework**: SPAN (Strategy Positioning and Action Navigation) Matrix")
    parts.append("")
    parts.append("---")

    # 1. SPAN Matrix Overview (with feedback filtering on span_positions)
    parts.append(_render_span_overview(opp, op_map, feedback=feedback))

    # 2. Grow/Invest
    parts.append(_render_quadrant_detail(opp, "grow_invest", "Grow/Invest",
                                          "Execute aggressively — highest priority", op_map))

    # 3. Acquire Skills
    parts.append(_render_quadrant_detail(opp, "acquire_skills", "Acquire Skills",
                                          "Build capability before competing", op_map))

    # 4. Harvest / Avoid
    parts.append(_render_harvest_avoid(opp, op_map))

    # 5. Priority Ranking
    parts.append(_render_priority_ranking(opp, op_map))

    # 6. Financial Impact
    parts.append(_render_financial_impact(opp, diagnosis, op_map))

    # 7. Strategic Recommendations
    parts.append(_render_recommendations(opp, diagnosis))

    return "\n\n".join(p for p in parts if p)


# ---------------------------------------------------------------------------
# Sub-renderers
# ---------------------------------------------------------------------------

def _render_span_overview(opp, op_map: dict[str, str] = None, feedback=None) -> str:
    positions = safe_list(opp, "span_positions")
    positions = filter_findings_by_feedback(positions, "span_", feedback)
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
            name = replace_operator_ids(name, op_map)
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


def _render_quadrant_detail(opp, attr: str, title: str, description: str,
                            op_map: dict[str, str] = None) -> str:
    items = safe_list(opp, attr)
    if not items:
        return ""

    # Section number depends on quadrant
    section_num = {"grow_invest": 2, "acquire_skills": 3}.get(attr, 2)
    lines = [section_header(f"{section_num}. {title} Opportunities", 2)]
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
        # Try to find detailed record
        detail = opp_map.get(item.lower())
        display_name = replace_operator_ids(_descriptive_label(item, detail), op_map)
        lines.append(f"### {i}. {display_name}")
        lines.append("")
        if detail:
            desc = safe_get(detail, "description", "")
            if desc:
                desc = replace_operator_ids(desc, op_map)
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
                derived_str = replace_operator_ids(', '.join(derived), op_map)
                lines.append(f"*Derived from: {derived_str}*")
                lines.append("")

    lines.append("---")

    return "\n".join(lines)


def _render_harvest_avoid(opp, op_map: dict[str, str] = None) -> str:
    harvest = safe_list(opp, "harvest")
    avoid = safe_list(opp, "avoid_exit")

    if not harvest and not avoid:
        return ""

    lines = [section_header("4. Harvest & Avoid/Exit", 2), ""]

    # Build opp_map for label lookup
    opportunities = safe_list(opp, "opportunities")
    opp_map = {safe_get(o, "name", "").lower(): o for o in opportunities}

    if harvest:
        lines.append(section_header("Harvest", 3))
        lines.append("*Extract remaining value — do not invest for growth*")
        lines.append("")
        for item in harvest:
            detail = opp_map.get(item.lower())
            label = replace_operator_ids(_descriptive_label(item, detail), op_map)
            lines.append(f"- {label}")
        lines.append("")

    if avoid:
        lines.append(section_header("Avoid/Exit", 3))
        lines.append("*No viable path — exit or do not enter*")
        lines.append("")
        for item in avoid:
            detail = opp_map.get(item.lower())
            label = replace_operator_ids(_descriptive_label(item, detail), op_map)
            lines.append(f"- {label}")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_priority_ranking(opp, op_map: dict[str, str] = None) -> str:
    opportunities = safe_list(opp, "opportunities")
    if not opportunities:
        return ""

    lines = [section_header("5. Portfolio Prioritization", 2), ""]

    # Apply smart tiering based on quadrant rather than trusting engine P0/P1/P2
    # Grow/invest → P0 (top 5) then P1; Acquire skills → P1; Harvest → P2; Avoid → P2
    gi_names = set(x.lower() for x in safe_list(opp, "grow_invest"))
    ask_names = set(x.lower() for x in safe_list(opp, "acquire_skills"))

    p0, p1, p2 = [], [], []
    for o in opportunities:
        name_lower = safe_get(o, "name", "").lower()
        if name_lower in gi_names:
            if len(p0) < 5:
                p0.append(o)
            else:
                p1.append(o)
        elif name_lower in ask_names:
            p1.append(o)
        else:
            p2.append(o)

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
            display = replace_operator_ids(_descriptive_label(name, o), op_map)
            market = safe_get(o, "addressable_market", "N/A")
            window = safe_get(o, "time_window", "")
            capability = safe_get(o, "our_capability", "")
            rows.append([display, str(market), window, capability])

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


def _render_financial_impact(opp, diagnosis, op_map: dict[str, str] = None) -> str:
    opportunities = safe_list(opp, "opportunities")
    if not opportunities:
        return ""

    lines = [section_header("6. Financial Impact Assessment", 2), ""]

    # Build financial summary from available data
    gi_names = set(x.lower() for x in safe_list(opp, "grow_invest"))
    rows = []
    for i, o in enumerate(opportunities[:10]):
        name = safe_get(o, "name", "")
        display = replace_operator_ids(_descriptive_label(name, o), op_map)
        market = safe_get(o, "addressable_market", "N/A")
        # Smart priority based on quadrant position
        if name.lower() in gi_names:
            priority = "P0" if i < 5 else "P1"
        else:
            priority = safe_get(o, "priority", "P2")
        rows.append([display, priority, str(market)])

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
