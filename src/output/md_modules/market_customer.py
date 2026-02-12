"""Module 02: Market & Customer ($APPEALS) renderer.

Produces the Market/Customer section containing:
1. Market Snapshot
2. Market Events & Competitive Intelligence
3. Customer Segmentation
4. $APPEALS Assessment
5. Customer Value Migration
6. Opportunities & Threats Summary
"""
from __future__ import annotations

from ..md_utils import (
    section_header, section_divider, md_table, md_kv_table,
    bold, bullet_list, fmt_pct,
    safe_get, safe_list, safe_dict,
    operator_display_name,
    empty_section_notice,
)


def render_market_customer(result, diagnosis, config) -> str:
    """Render Module 02: Market & Customer ($APPEALS) Analysis."""
    mci = result.market_customer
    if mci is None:
        return empty_section_notice("Market & Customer ($APPEALS)")

    parts = []
    target_name = operator_display_name(result.target_operator)
    period = result.analysis_period or ""

    # Module title
    parts.append(f"# Market & Customer Analysis — $APPEALS Framework ({period})")
    parts.append("")
    parts.append(f"**Protagonist**: {target_name}")
    parts.append(f"**Framework**: $APPEALS (Availability, Price, Performance, Ease of Use, "
                 f"Assurances, Lifecycle Cost, Social Responsibility)")
    parts.append("")
    parts.append("---")

    # 1. Market Snapshot
    parts.append(_render_market_snapshot(mci, config))

    # 2. Market Events
    parts.append(_render_market_events(mci))

    # 3. Customer Segmentation
    parts.append(_render_segments(mci, config))

    # 4. $APPEALS
    parts.append(_render_appeals(mci, result))

    # 5. Value Migration
    parts.append(_render_value_migration(mci))

    # 6. Opportunities & Threats
    parts.append(_render_opps_threats(mci, diagnosis))

    return "\n\n".join(p for p in parts if p)


# ---------------------------------------------------------------------------
# Sub-renderers
# ---------------------------------------------------------------------------

def _render_market_snapshot(mci, config) -> str:
    snapshot = safe_dict(mci, "market_snapshot")
    if not snapshot:
        return ""

    lines = [section_header("1. Market Snapshot", 2), ""]

    rows = []
    for key, value in snapshot.items():
        display_key = key.replace("_", " ").title()
        rows.append([display_key, str(value)])

    lines.append(md_table(["Metric", "Value"], rows))

    outlook = safe_get(mci, "market_outlook", "")
    if outlook:
        lines.append("")
        lines.append(f"**Market outlook**: {outlook.title()}")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_market_events(mci) -> str:
    changes = safe_list(mci, "changes")
    if not changes:
        return ""

    lines = [section_header("2. Market Events & Competitive Intelligence", 2), ""]

    rows = []
    for c in changes:
        change_type = safe_get(c, "change_type", "").replace("_", " ").title()
        desc = safe_get(c, "description", "")
        impact = safe_get(c, "impact_type", "neutral").title()
        severity = safe_get(c, "severity", "medium").title()
        source = safe_get(c, "source", "").replace("_", " ").title()
        rows.append([change_type, desc, impact, severity, source])

    lines.append(md_table(
        ["Type", "Description", "Impact", "Severity", "Source"],
        rows
    ))

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_segments(mci, config) -> str:
    segments = safe_list(mci, "customer_segments")
    # Also try from config
    if not segments and config:
        config_segs = safe_list(config, "customer_segments")
        if config_segs:
            # Config segments are dicts, not CustomerSegment objects
            lines = [section_header("3. Customer Segmentation", 2), ""]
            rows = []
            for seg in config_segs:
                name = seg.get("segment_name", "") if isinstance(seg, dict) else safe_get(seg, "segment_name", "")
                seg_type = seg.get("segment_type", "") if isinstance(seg, dict) else safe_get(seg, "segment_type", "")
                rows.append([name, seg_type.title(), "", ""])
            lines.append(md_table(["Segment", "Type", "Size", "Growth"], rows))
            lines.append("")
            lines.append("---")
            return "\n".join(lines)

    if not segments:
        return ""

    lines = [section_header("3. Customer Segmentation", 2), ""]

    rows = []
    for seg in segments:
        name = safe_get(seg, "segment_name", "")
        seg_type = safe_get(seg, "segment_type", "").title()
        size = safe_get(seg, "size_estimate", "")
        growth = safe_get(seg, "growth_trend", "").title()
        share = safe_get(seg, "our_share", "")
        rows.append([name, seg_type, str(size), growth, str(share)])

    lines.append(md_table(["Segment", "Type", "Size", "Growth", "Our Share"], rows))

    # Segment deep dives
    for seg in segments:
        name = safe_get(seg, "segment_name", "")
        unmet = safe_list(seg, "unmet_needs")
        pain = safe_list(seg, "pain_points")
        decision = safe_list(seg, "purchase_decision_factors")
        gaps = safe_list(seg, "competitor_gaps")
        opp = safe_get(seg, "opportunity", "")

        if any([unmet, pain, decision, gaps, opp]):
            lines.append("")
            lines.append(section_header(f"Segment: {name}", 4))
            if unmet:
                lines.append(f"- **Unmet needs**: {'; '.join(unmet[:3])}")
            if pain:
                lines.append(f"- **Pain points**: {'; '.join(pain[:3])}")
            if decision:
                lines.append(f"- **Decision factors**: {'; '.join(decision[:3])}")
            if gaps:
                lines.append(f"- **Competitor gaps**: {'; '.join(gaps[:3])}")
            if opp:
                lines.append(f"- **Opportunity**: {opp}")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_appeals(mci, result) -> str:
    appeals = safe_list(mci, "appeals_assessment")
    if not appeals:
        return ""

    target = result.target_operator
    target_name = operator_display_name(target)

    lines = [section_header("4. $APPEALS Assessment", 2), ""]

    # Collect all operators that appear in competitor_scores
    all_ops = set()
    for a in appeals:
        comp_scores = safe_dict(a, "competitor_scores")
        all_ops.update(comp_scores.keys())
    all_ops = sorted(all_ops)

    # Build scoring table
    headers = ["Dimension", target_name]
    for op in all_ops:
        headers.append(operator_display_name(op))
    headers.append("Priority")

    rows = []
    for a in appeals:
        dim = safe_get(a, "dimension_name", safe_get(a, "dimension", ""))
        our_score = safe_get(a, "our_score", 0)
        priority = safe_get(a, "customer_priority", "")

        row = [dim, f"{our_score:.1f}"]
        comp_scores = safe_dict(a, "competitor_scores")
        for op in all_ops:
            score = comp_scores.get(op, "—")
            if isinstance(score, (int, float)):
                row.append(f"{score:.1f}")
            else:
                row.append(str(score))
        row.append(priority.title())
        rows.append(row)

    lines.append(md_table(headers, rows))

    # Gap analysis
    lines.append("")
    lines.append(section_header("Gap Analysis", 3))
    lines.append("")

    gap_rows = []
    for a in appeals:
        dim = safe_get(a, "dimension_name", safe_get(a, "dimension", ""))
        our_score = float(safe_get(a, "our_score", 0))
        gap = safe_get(a, "gap_analysis", "")
        comp_scores = safe_dict(a, "competitor_scores")
        max_comp = max((float(v) for v in comp_scores.values() if isinstance(v, (int, float))), default=0)
        delta = our_score - max_comp
        status = "Leading" if delta > 0 else ("Parity" if delta == 0 else "Lagging")
        gap_rows.append([dim, f"{our_score:.1f}", f"{max_comp:.1f}",
                         f"{delta:+.1f}", status, gap])

    lines.append(md_table(
        ["Dimension", f"{target_name}", "Leader", "Gap", "Status", "Analysis"],
        gap_rows
    ))

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_value_migration(mci) -> str:
    vm = safe_get(mci, "customer_value_migration", "")
    if not vm:
        return ""

    lines = [
        section_header("5. Customer Value Migration", 2),
        "",
        vm,
        "",
        "---",
    ]
    return "\n".join(lines)


def _render_opps_threats(mci, diagnosis) -> str:
    opps = safe_list(mci, "opportunities")
    threats = safe_list(mci, "threats")

    if not opps and not threats:
        return ""

    lines = [section_header("6. Opportunities & Threats Summary", 2), ""]

    if opps:
        lines.append(section_header("Opportunities", 3))
        lines.append("")
        rows = []
        for o in opps:
            desc = safe_get(o, "description", str(o) if isinstance(o, str) else "")
            impact = safe_get(o, "impact_description", "")
            severity = safe_get(o, "severity", "")
            rows.append([desc, impact, severity.title()])
        if rows:
            lines.append(md_table(["Opportunity", "Impact", "Severity"], rows))
        lines.append("")

    if threats:
        lines.append(section_header("Threats", 3))
        lines.append("")
        rows = []
        for t in threats:
            desc = safe_get(t, "description", str(t) if isinstance(t, str) else "")
            impact = safe_get(t, "impact_description", "")
            severity = safe_get(t, "severity", "")
            rows.append([desc, impact, severity.title()])
        if rows:
            lines.append(md_table(["Threat", "Impact", "Severity"], rows))

    # Key message
    km = safe_get(mci, "key_message", "")
    if km:
        lines.append("")
        lines.append(f"**Key message**: {km}")

    lines.append("")
    lines.append(f"**Net assessment**: {diagnosis.market_net_assessment}")
    lines.append("")
    lines.append("---")

    return "\n".join(lines)
