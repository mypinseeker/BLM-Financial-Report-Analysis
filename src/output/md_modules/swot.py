"""Module SW: SWOT Synthesis renderer.

Produces the SWOT Synthesis section containing:
1. SWOT Overview (posture, counts, balance)
2. Strengths (detailed)
3. Weaknesses (detailed)
4. Opportunities (ranked, timed)
5. Threats (detailed with compound effects)
6. Strategy Matrix (SO/WO/ST/WT)
7. Strategic Synthesis
"""
from __future__ import annotations

from ..md_utils import (
    section_header, section_divider, md_table,
    bold, bullet_list,
    safe_get, safe_list,
    operator_display_name,
    empty_section_notice,
)


def render_swot(result, diagnosis, config) -> str:
    """Render Module SW: SWOT Synthesis."""
    swot = result.swot
    if swot is None:
        return empty_section_notice("SWOT")

    parts = []
    target_name = operator_display_name(result.target_operator)
    period = result.analysis_period or ""

    # Module title
    parts.append(f"# SWOT Synthesis — {target_name} ({period})")
    parts.append("")
    parts.append(f"**Competitive stance**: {bold(diagnosis.competitive_stance)}")
    parts.append("")
    parts.append("---")

    target_op = result.target_operator or ""

    # 1. Overview
    parts.append(_render_overview(swot, diagnosis))

    # 2-5. Individual quadrants
    parts.append(_render_strengths(swot))
    parts.append(_render_weaknesses(swot))
    parts.append(_render_opportunities(swot, target_op))
    parts.append(_render_threats(swot, target_op))

    # 6. Strategy Matrix
    parts.append(_render_strategy_matrix(swot, target_op))

    # 7. Strategic Synthesis
    parts.append(_render_synthesis(swot, diagnosis))

    return "\n\n".join(p for p in parts if p)


# ---------------------------------------------------------------------------
# Sub-renderers
# ---------------------------------------------------------------------------

def _render_overview(swot, diagnosis) -> str:
    s = safe_list(swot, "strengths")
    w = safe_list(swot, "weaknesses")
    o = safe_list(swot, "opportunities")
    t = safe_list(swot, "threats")

    lines = [section_header("1. SWOT Overview", 2), ""]

    # Count table
    rows = [
        [bold("Strengths"), str(len(s)), _top_items(s, 3)],
        [bold("Weaknesses"), str(len(w)), _top_items(w, 3)],
        [bold("Opportunities"), str(len(o)), _top_items(o, 3)],
        [bold("Threats"), str(len(t)), _top_items(t, 3)],
    ]
    lines.append(md_table(["Quadrant", "Count", "Key Items"], rows))

    # Balance assessment
    lines.append("")
    s_dom = "S > W" if len(s) >= len(w) else "W > S"
    o_dom = "O > T" if len(o) >= len(t) else "T > O"
    lines.append(f"**Balance**: {s_dom} and {o_dom}")
    lines.append(f"**Competitive stance**: {diagnosis.competitive_stance}")

    # Critical insight
    km = safe_get(swot, "key_message", "")
    if km:
        lines.append("")
        lines.append(f"**Critical insight**: {km}")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_strengths(swot) -> str:
    items = safe_list(swot, "strengths")
    if not items:
        return ""

    lines = [section_header("2. Strengths", 2), ""]

    for i, item in enumerate(items, 1):
        lines.append(f"{i}. {item}")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_weaknesses(swot) -> str:
    items = safe_list(swot, "weaknesses")
    if not items:
        return ""

    lines = [section_header("3. Weaknesses", 2), ""]

    for i, item in enumerate(items, 1):
        lines.append(f"{i}. {item}")

    # Interaction effects
    if len(items) >= 2:
        lines.append("")
        lines.append(section_header("Weakness Interactions", 3))
        lines.append("")
        lines.append(f"Note: Weaknesses often compound. For example, "
                     f"'{_short(items[0])}' may exacerbate "
                     f"'{_short(items[1])}', creating a negative feedback loop.")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_opportunities(swot, target_op: str = "") -> str:
    items = safe_list(swot, "opportunities")
    if not items:
        return ""

    target_display = operator_display_name(target_op) if target_op else ""
    lines = [section_header("4. Opportunities", 2), ""]

    for i, item in enumerate(items, 1):
        if target_op and target_op in item:
            item = item.replace(target_op, target_display)
        lines.append(f"{i}. {item}")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_threats(swot, target_op: str = "") -> str:
    items = safe_list(swot, "threats")
    if not items:
        return ""

    target_display = operator_display_name(target_op) if target_op else ""
    lines = [section_header("5. Threats", 2), ""]

    for i, item in enumerate(items, 1):
        if target_op and target_op in item:
            item = item.replace(target_op, target_display)
        lines.append(f"{i}. {item}")

    # Compound effects
    if len(items) >= 2:
        lines.append("")
        lines.append(section_header("Compound Threat Effects", 3))
        lines.append("")
        lines.append(f"Multiple threats occurring simultaneously amplify impact. "
                     f"If '{_short(items[0])}' coincides with "
                     f"'{_short(items[1])}', the combined pressure could "
                     f"force reactive rather than strategic responses.")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_strategy_matrix(swot, target_op: str = "") -> str:
    so = safe_list(swot, "so_strategies")
    wo = safe_list(swot, "wo_strategies")
    st = safe_list(swot, "st_strategies")
    wt = safe_list(swot, "wt_strategies")

    if not any([so, wo, st, wt]):
        return ""

    target_display = operator_display_name(target_op) if target_op else ""
    lines = [section_header("6. Strategy Matrix", 2), ""]

    quadrants = [
        ("SO Strategies (Strengths × Opportunities)", "Use strengths to capture opportunities",
         so, "Offensive"),
        ("WO Strategies (Weaknesses × Opportunities)", "Fix weaknesses to capture opportunities",
         wo, "Developmental"),
        ("ST Strategies (Strengths × Threats)", "Use strengths to counter threats",
         st, "Defensive"),
        ("WT Strategies (Weaknesses × Threats)", "Minimize weaknesses and avoid threats",
         wt, "Survival"),
    ]

    for title, description, items, posture in quadrants:
        if not items:
            continue

        lines.append(section_header(f"{title}", 3))
        lines.append(f"*{description}* — Posture: {posture}")
        lines.append("")

        for i, item in enumerate(items, 1):
            if target_op and target_op in item:
                item = item.replace(target_op, target_display)
            lines.append(f"{i}. {item}")
        lines.append("")

    lines.append("---")

    return "\n".join(lines)


def _render_synthesis(swot, diagnosis) -> str:
    lines = [section_header("7. Strategic Synthesis", 2), ""]

    km = safe_get(swot, "key_message", "")
    if km:
        lines.append(f"**Key message**: {km}")
        lines.append("")

    lines.append(f"**Competitive stance**: {diagnosis.competitive_stance}")
    lines.append("")

    # Reference central diagnosis
    if diagnosis.central_diagnosis_label:
        label = diagnosis.central_diagnosis_label
        lines.append(f"This SWOT analysis reinforces the **\"{label}\"** "
                     f"central diagnosis identified across all Five Looks.")
        lines.append("")

    lines.append(f"**Net assessment**: {diagnosis.swot_net_assessment}")
    lines.append("")
    lines.append("---")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _top_items(items: list, n: int) -> str:
    """Return first n items as comma-separated string."""
    if not items:
        return "—"
    display = items[:n]
    shortened = [_short(item) for item in display]
    return ", ".join(shortened)


def _short(text: str, max_len: int = 50) -> str:
    """Shorten text for display."""
    if not text:
        return ""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."
