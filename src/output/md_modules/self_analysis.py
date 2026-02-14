"""Module 04: Self Analysis — BMC + Capability renderer.

Produces the Self Analysis section containing:
1. Financial Health Dashboard
2. Revenue Breakdown & Segments
3. Segment Deep Dives
4. Network Assessment
5. Business Model Canvas (BMC)
6. Strengths, Weaknesses & Exposure Points
7. Management Outlook
8. Strategic Diagnosis Summary
"""
from __future__ import annotations

from ..md_utils import (
    section_header, section_divider, md_table, md_kv_table,
    bold, bullet_list, code_block,
    fmt_currency, fmt_pct, fmt_subs, fmt_smart_value,
    safe_get, safe_list, safe_dict,
    operator_display_name,
    empty_section_notice,
    filter_findings_by_feedback,
)


def render_self_analysis(result, diagnosis, config, feedback=None) -> str:
    """Render Module 04: Self Analysis."""
    sa = result.self_analysis
    if sa is None:
        return empty_section_notice("Self Analysis")

    parts = []
    target_name = operator_display_name(result.target_operator)
    period = result.analysis_period or ""

    # Module title
    parts.append(f"# Self Analysis — {target_name} ({period})")
    parts.append("")
    parts.append(f"**Framework**: Business Model Canvas (BMC) + Capability Assessment")
    parts.append(f"**Health rating**: {bold(safe_get(sa, 'health_rating', 'stable').title())}")
    parts.append("")
    parts.append("---")

    # 1. Financial Health
    parts.append(_render_financial_health(sa, config))

    # 2. Revenue Breakdown
    parts.append(_render_revenue_breakdown(sa, config))

    # 3. Segment Deep Dives (with feedback filtering)
    parts.append(_render_segments(sa, config, feedback=feedback))

    # 4. Network Assessment
    parts.append(_render_network(sa))

    # 5. BMC
    parts.append(_render_bmc(sa))

    # 6. Strengths/Weaknesses/Exposures (with feedback filtering)
    parts.append(_render_strengths_weaknesses(sa, result.target_operator,
                                               feedback=feedback))

    # 7. Management Outlook
    parts.append(_render_management(sa))

    # 8. Diagnosis Summary
    parts.append(_render_diagnosis_summary(sa, diagnosis))

    return "\n\n".join(p for p in parts if p)


# ---------------------------------------------------------------------------
# Sub-renderers
# ---------------------------------------------------------------------------

def _render_financial_health(sa, config) -> str:
    fh = safe_dict(sa, "financial_health")
    if not fh:
        return ""

    lines = [section_header("1. Financial Health Dashboard", 2), ""]

    # Skip trend arrays and internal flags — those are rendered separately
    _SKIP_KEYS = {
        'revenue_trend', 'ebitda_trend', 'margin_trend',
        'revenue_growing', 'margin_healthy',
        'quarters_analyzed', 'status', 'latest_quarter',
    }

    rows = []
    for k, v in fh.items():
        if k in _SKIP_KEYS:
            continue
        if isinstance(v, (list, tuple)):
            continue  # skip trend arrays
        display_key = k.replace("_", " ").title()
        rows.append([display_key, fmt_smart_value(k, v, config)])

    lines.append(md_table(["KPI", "Value"], rows))

    # 8Q Revenue Trend if available
    segments = safe_list(sa, "segment_analyses")
    # Look for revenue trend data across segments
    trend_lines = []
    for seg in segments:
        trend = safe_dict(seg, "trend_data")
        rev_trend = trend.get("revenue") or trend.get("quarterly_revenue")
        if rev_trend and isinstance(rev_trend, (list, tuple)):
            name = safe_get(seg, "segment_name", "")
            vals = [str(v) for v in rev_trend]
            trend_lines.append(f"{name:15s} {' → '.join(vals[-4:])}")

    if trend_lines:
        lines.append("")
        lines.append(section_header("Revenue Trends (Recent Quarters)", 3))
        lines.append("")
        lines.append(code_block("\n".join(trend_lines)))

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_revenue_breakdown(sa, config) -> str:
    rb = safe_dict(sa, "revenue_breakdown")
    if not rb:
        return ""

    lines = [section_header("2. Revenue Breakdown", 2), ""]

    # Skip the 'total_revenue' entry if present — it's not a segment
    _SKIP_RB = {'total_revenue', 'quarterly_revenue', 'total'}

    # Extract numeric values (handling dict entries like {'value': 1520, 'share_pct': 49.2})
    def _extract_num(v):
        if isinstance(v, dict):
            return float(v.get('value', 0))
        if _is_number(v):
            return float(v)
        return 0.0

    segment_items = {k: v for k, v in rb.items() if k not in _SKIP_RB}
    total = sum(_extract_num(v) for v in segment_items.values())

    rows = []
    for segment, value in segment_items.items():
        display_name = _fix_metric_casing(segment.replace("_", " ").title())

        if isinstance(value, dict):
            # Dict with value and share_pct
            num = float(value.get('value', 0))
            share_pct = value.get('share_pct')
            val_str = fmt_currency(num, config)
            share = fmt_pct(share_pct, show_sign=False) if share_pct is not None else ""
        elif _is_number(value):
            num = float(value)
            val_str = fmt_currency(num, config)
            share = fmt_pct(num / total * 100, show_sign=False) if total > 0 else ""
        else:
            val_str = str(value)
            share = ""

        rows.append([display_name, val_str, share])

    # Add total row
    if total > 0:
        rows.append([bold("Total"), bold(fmt_currency(total, config)), bold("100.0%")])

    lines.append(md_table(["Segment", "Revenue", "Share"], rows))
    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_segments(sa, config, feedback=None) -> str:
    segments = safe_list(sa, "segment_analyses")
    segments = filter_findings_by_feedback(segments, "self_segment_", feedback)
    if not segments:
        return ""

    lines = [section_header("3. Business Segment Deep Dives", 2)]

    # Summary table
    lines.append("")
    summary_rows = []
    for seg in segments:
        name = safe_get(seg, "segment_name", "")
        health = safe_get(seg, "health_status", "stable")
        km = safe_get(seg, "key_metrics", {})
        rev = _find_revenue(km)
        rev_str = fmt_currency(rev, config) if rev is not None else "—"
        action = safe_get(seg, "action_required", "")
        summary_rows.append([name, rev_str, bold(health.title()), action[:60]])

    lines.append(md_table(["Segment", "Revenue", "Health", "Action Required"], summary_rows))

    # Individual segment deep dives
    for seg in segments:
        name = safe_get(seg, "segment_name", "Unknown")
        health = safe_get(seg, "health_status", "stable")
        km_dict = safe_dict(seg, "key_metrics")
        changes = safe_list(seg, "changes")
        attributions = safe_list(seg, "attributions")
        key_msg = safe_get(seg, "key_message", "")
        action = safe_get(seg, "action_required", "")

        lines.append("")
        lines.append(section_header(f"Segment: {name} [{health.title()}]", 3))
        lines.append("")

        # Key metrics
        if km_dict:
            metric_rows = []
            for k, v in km_dict.items():
                display_key = _fix_metric_casing(k.replace("_", " ").title())
                metric_rows.append([display_key, fmt_smart_value(k, v, config)])
            lines.append(md_table(["Metric", "Value"], metric_rows))
            lines.append("")

        # Changes
        if changes:
            lines.append(section_header("Changes", 4))
            lines.append("")
            change_rows = []
            for c in changes:
                metric = safe_get(c, "metric", "")
                current = safe_get(c, "current_value", "")
                prev = safe_get(c, "previous_value", "")
                direction = safe_get(c, "direction", "")
                significance = safe_get(c, "significance", "")
                change_rows.append([metric, str(current), str(prev), direction.title(), significance.title()])
            lines.append(md_table(["Metric", "Current", "Previous", "Direction", "Significance"], change_rows))
            lines.append("")

        # Attributions
        if attributions:
            lines.append(section_header("Why — Attribution Analysis", 4))
            lines.append("")
            for attr in attributions:
                attr_type = safe_get(attr, "attribution_type", "").replace("_", " ").title()
                desc = safe_get(attr, "description", "")
                confidence = safe_get(attr, "confidence", "")
                lines.append(f"- **{attr_type}** ({confidence}): {desc}")
            lines.append("")

        # Key message & action
        if key_msg:
            lines.append(f"**Key message**: {key_msg}")
        if action:
            lines.append(f"**Action required**: {action}")
        lines.append("")

    lines.append("---")

    return "\n".join(lines)


def _render_network(sa) -> str:
    network = safe_get(sa, "network")
    if network is None:
        return ""

    tech = safe_dict(network, "technology_mix")
    coverage = safe_dict(network, "coverage")
    quality = safe_dict(network, "quality_scores")
    controlled = safe_dict(network, "controlled_vs_resale")
    homepass = safe_dict(network, "homepass_vs_connect")
    evolution = safe_dict(network, "evolution_strategy")
    investment = safe_get(network, "investment_direction", "")
    vs_comp = safe_get(network, "vs_competitors", "")
    consumer = safe_get(network, "consumer_impact", "")
    b2b = safe_get(network, "b2b_impact", "")
    cost = safe_get(network, "cost_impact", "")

    has_data = any([tech, coverage, quality, controlled, homepass, evolution,
                    investment, vs_comp, consumer, b2b, cost])
    if not has_data:
        return ""

    lines = [section_header("4. Network Assessment", 2), ""]

    if tech:
        lines.append(section_header("Technology Mix", 3))
        lines.append("")
        rows = []
        for k, v in tech.items():
            display_k = k.replace("_", " ").title()
            # Unpack nested dicts (e.g. spectrum_mhz: {700: 20, 1800: 50})
            if isinstance(v, dict):
                display_v = "; ".join(f"{sk}: {sv}" for sk, sv in v.items())
            elif isinstance(v, list):
                display_v = ", ".join(str(x) for x in v)
            else:
                display_v = str(v)
            rows.append([display_k, display_v])
        lines.append(md_table(["Technology", "Detail"], rows))
        lines.append("")

    if coverage:
        lines.append(section_header("Coverage", 3))
        lines.append("")
        rows = [[k.replace("_", " ").upper(), f"{v}%"] for k, v in coverage.items()]
        lines.append(md_table(["Technology", "Coverage"], rows))
        lines.append("")

    if quality:
        lines.append(section_header("Quality Scores", 3))
        lines.append("")
        rows = [[k.replace("_", " ").title(), str(v)] for k, v in quality.items()]
        lines.append(md_table(["Test", "Score"], rows))
        lines.append("")

    if controlled:
        lines.append(section_header("Controlled vs. Resale", 3))
        lines.append("")
        rows = []
        for k, v in controlled.items():
            display_k = k.replace("_", " ").title()
            if isinstance(v, list):
                display_v = ", ".join(str(x) for x in v)
            else:
                display_v = str(v)
            rows.append([display_k, display_v])
        lines.append(md_table(["Type", "Detail"], rows))
        lines.append("")

    if homepass:
        lines.append(section_header("Homepass vs. Connect", 3))
        lines.append("")
        rows = []
        for k, v in homepass.items():
            display_k = k.replace("_", " ").title()
            display_v = fmt_smart_value(k, v, None)
            rows.append([display_k, display_v])
        lines.append(md_table(["Metric", "Value"], rows))
        lines.append("")

    if evolution:
        lines.append(section_header("Evolution Strategy", 3))
        lines.append("")
        for k, v in evolution.items():
            display_v = ", ".join(str(x) for x in v) if isinstance(v, list) else str(v)
            lines.append(f"- **{k.replace('_', ' ').title()}**: {display_v}")
        lines.append("")

    # Impact assessments
    for label, value in [
        ("Investment direction", investment),
        ("Vs. competitors", vs_comp),
        ("Consumer impact", consumer),
        ("B2B impact", b2b),
        ("Cost impact", cost),
    ]:
        if value:
            lines.append(f"**{label}**: {value}")
            lines.append("")

    lines.append("---")

    return "\n".join(lines)


def _render_bmc(sa) -> str:
    bmc = safe_get(sa, "bmc")
    if bmc is None:
        return ""

    blocks = [
        ("Key Partners", safe_list(bmc, "key_partners")),
        ("Key Activities", safe_list(bmc, "key_activities")),
        ("Key Resources", safe_list(bmc, "key_resources")),
        ("Value Propositions", safe_list(bmc, "value_propositions")),
        ("Customer Relationships", safe_list(bmc, "customer_relationships")),
        ("Channels", safe_list(bmc, "channels")),
        ("Customer Segments", safe_list(bmc, "customer_segments")),
        ("Cost Structure", safe_list(bmc, "cost_structure")),
        ("Revenue Streams", safe_list(bmc, "revenue_streams")),
    ]

    has_data = any(items for _, items in blocks)
    if not has_data:
        return ""

    lines = [section_header("5. Business Model Canvas", 2), ""]

    rows = []
    for block_name, items in blocks:
        if items:
            rows.append([bold(block_name), "; ".join(items[:4])])
        else:
            rows.append([block_name, "—"])

    lines.append(md_table(["BMC Block", "Components"], rows))
    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_strengths_weaknesses(sa, target_operator: str, feedback=None) -> str:
    strengths = safe_list(sa, "strengths")
    weaknesses = safe_list(sa, "weaknesses")
    exposures = safe_list(sa, "exposure_points")
    exposures = filter_findings_by_feedback(exposures, "exposure_", feedback)

    if not strengths and not weaknesses and not exposures:
        return ""

    target_name = operator_display_name(target_operator)
    lines = [section_header("6. Strengths, Weaknesses & Exposure Points", 2), ""]

    if strengths:
        lines.append(section_header("Strengths", 3))
        lines.append("")
        for s in strengths:
            lines.append(f"- {s}")
        lines.append("")

    if weaknesses:
        lines.append(section_header("Weaknesses", 3))
        lines.append("")
        for w in weaknesses:
            lines.append(f"- {w}")
        lines.append("")

    if exposures:
        lines.append(section_header("Exposure Points", 3))
        lines.append("")
        rows = []
        for ep in exposures:
            trigger = safe_get(ep, "trigger_action", "")
            side = safe_get(ep, "side_effect", "")
            attack = safe_get(ep, "attack_vector", "")
            severity = safe_get(ep, "severity", "medium")
            rows.append([trigger, side, attack, bold(severity.title())])
        lines.append(md_table(
            ["Trigger", "Side Effect", "Attack Vector", "Severity"],
            rows
        ))

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_management(sa) -> str:
    commentary = safe_list(sa, "management_commentary")
    leadership = safe_list(sa, "leadership_changes")
    org_culture = safe_get(sa, "org_culture", "")
    perf_gap = safe_get(sa, "performance_gap", "")
    opp_gap = safe_get(sa, "opportunity_gap", "")
    strat_review = safe_get(sa, "strategic_review", "")

    has_data = any([commentary, leadership, org_culture, perf_gap, opp_gap, strat_review])
    if not has_data:
        return ""

    lines = [section_header("7. Management & Organization", 2), ""]

    # Leadership
    if leadership:
        lines.append(section_header("Leadership Team", 3))
        lines.append("")
        current = [e for e in leadership if e.get("is_current")]
        if current:
            rows = []
            for e in current[:8]:
                name = e.get("name", "")
                title = e.get("title", "")
                tenure = e.get("tenure_years")
                tenure_str = f"{tenure:.0f} years" if tenure else "—"
                rows.append([name, title, tenure_str])
            lines.append(md_table(["Name", "Title", "Tenure"], rows))
        lines.append("")

    # Org culture
    if org_culture:
        lines.append(section_header("Organization & Culture", 3))
        lines.append("")
        lines.append(org_culture)
        lines.append("")

    # Management commentary
    if commentary:
        lines.append(section_header("Management Commentary (Earnings Calls)", 3))
        lines.append("")
        for c in commentary[:5]:
            if isinstance(c, dict):
                speaker = c.get("speaker", "Management")
                quote = c.get("quote", c.get("text", c.get("comment", "")))
                topic = c.get("topic", "")
                if quote:
                    prefix = f"**{speaker}**" + (f" on {topic}" if topic else "")
                    lines.append(f"- {prefix}: *\"{quote}\"*")
            elif isinstance(c, str):
                lines.append(f"- {c}")
        lines.append("")

    # Gaps & Review
    if perf_gap:
        lines.append(f"**Performance gap**: {perf_gap}")
    if opp_gap:
        lines.append(f"**Opportunity gap**: {opp_gap}")
    if strat_review:
        lines.append(f"**Strategic review**: {strat_review}")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_diagnosis_summary(sa, diagnosis) -> str:
    km = safe_get(sa, "key_message", "")

    lines = [section_header("8. Strategic Diagnosis Summary", 2), ""]

    if km:
        lines.append(f"**Key message**: {km}")
        lines.append("")

    lines.append(f"**Net assessment**: {diagnosis.self_net_assessment}")
    lines.append("")
    lines.append("---")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _find_revenue(km: dict):
    """Find the revenue value in a key_metrics dict, trying various key patterns."""
    for k, v in km.items():
        if 'revenue' in k.lower() and 'growth' not in k.lower() and 'share' not in k.lower():
            return v
    return None


def _is_number(val) -> bool:
    try:
        float(val)
        return True
    except (TypeError, ValueError):
        return False


def _fix_metric_casing(text: str) -> str:
    """Fix title-cased metric names: Tv→TV, Bb→BB, B2B, Fmc→FMC, Iot→IoT, 5G etc."""
    import re
    replacements = {
        "Tv ": "TV ", "Bb ": "BB ", "Fmc ": "FMC ", "Iot ": "IoT ",
        "5g ": "5G ", "4g ": "4G ", "Ftth ": "FTTH ", "Arpu": "ARPU",
        "Yoy": "YoY", "Pct": "%", "B2b": "B2B", " K": " (K)",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Fix trailing tokens
    if text.endswith(" Pct"):
        text = text[:-4] + " %"
    if text.endswith(" K"):
        text = text[:-2] + " (K)"
    return text
