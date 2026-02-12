"""Module ES: Executive Summary renderer for BLM Strategic Insight Report.

Produces the executive summary section (~350 lines) containing:
1. One-Line Verdict
2. Situation at a Glance
3. Key Findings by BLM Look
4. Central Diagnosis
5. Top 5 Strategic Priorities
6. What NOT to Do
7. Timeline & Sequencing
8. Risk/Reward Summary
9. Success Metrics Dashboard
"""
from __future__ import annotations

from ..md_utils import (
    section_header, section_divider, md_table, md_kv_table,
    blockquote, bold, code_block, bullet_list,
    operator_display_name, market_display_name,
    safe_get, safe_list, safe_dict, fmt_currency, fmt_pct,
    empty_section_notice,
)


def render_executive_summary(result, diagnosis, config) -> str:
    """Render the Executive Summary module."""
    parts = []

    target_name = operator_display_name(result.target_operator)
    market_name = market_display_name(result.market) if result.market else "Market"
    period = result.analysis_period or ""

    # Module title
    parts.append(f"# Executive Summary — {target_name} BLM Strategic Assessment")
    parts.append("")
    parts.append(f"**Period**: {period}")
    parts.append(f"**Framework**: Business Leadership Model (BLM) — Five Looks + SWOT + Opportunities")
    parts.append(f"**Protagonist**: {target_name}")
    parts.append(f"**Market**: {market_name}")
    parts.append("")
    parts.append("---")

    # 1. One-Line Verdict
    parts.append(_render_verdict(diagnosis))

    # 2. Situation at a Glance
    parts.append(_render_situation(result, diagnosis, config))

    # 3. Key Findings by BLM Look
    parts.append(_render_key_findings(result, diagnosis))

    # 4. Central Diagnosis
    parts.append(_render_central_diagnosis(result, diagnosis, config))

    # 5. Strategic Priorities
    parts.append(_render_priorities(diagnosis))

    # 6. What NOT to Do
    parts.append(_render_traps(diagnosis))

    # 7. Timeline & Sequencing
    parts.append(_render_timeline(result, diagnosis))

    # 8. Risk/Reward Summary
    parts.append(_render_risk_reward(diagnosis, config))

    # 9. Success Metrics Dashboard
    parts.append(_render_dashboard(diagnosis))

    return "\n\n".join(p for p in parts if p)


# ---------------------------------------------------------------------------
# Sub-renderers
# ---------------------------------------------------------------------------

def _render_verdict(diagnosis) -> str:
    verdict = diagnosis.one_line_verdict
    if not verdict:
        return ""
    lines = [
        section_header("The One-Line Verdict", 2),
        "",
        f"**{verdict}**",
        "",
        "---",
    ]
    return "\n".join(lines)


def _render_situation(result, diagnosis, config) -> str:
    lines = [section_header("1. Situation at a Glance", 2)]

    # 1.1 Market Context
    lines.append("")
    lines.append(section_header("1.1 Market Context", 3))
    lines.append("")

    trends = result.trends
    mci = result.market_customer

    market_rows = []
    if trends:
        ms = safe_get(trends, "industry_market_size", "")
        gr = safe_get(trends, "industry_growth_rate", "")
        conc = safe_get(trends, "industry_concentration", "")
        lifecycle = safe_get(trends, "industry_lifecycle_stage", "")

        if ms:
            market_rows.append(["Market size", str(ms), "Market scale indicator"])
        if gr:
            market_rows.append(["Market growth", str(gr), _growth_implication(gr)])
        if conc:
            market_rows.append(["Concentration", str(conc), "Market structure"])
        if lifecycle:
            market_rows.append(["Lifecycle stage", lifecycle.title(), _lifecycle_implication(lifecycle)])

    if config:
        pop = safe_get(config, "population_k")
        if pop:
            market_rows.append(["Population", f"{pop/1000:.1f}M", ""])
        reg = safe_get(config, "regulatory_body", "")
        if reg:
            market_rows.append(["Regulator", reg, ""])

    if diagnosis.market_structure:
        market_rows.append(["Structure", diagnosis.market_structure, ""])

    if market_rows:
        lines.append(md_table(["Metric", "Value", "Implication"], market_rows))
    else:
        lines.append("*Market context data not available.*")

    # 1.2 Operator Position
    lines.append("")
    lines.append(section_header("1.2 Operator Position", 3))
    lines.append("")

    sa = result.self_analysis
    fh = safe_dict(sa, "financial_health") if sa else {}
    position_rows = []

    for metric, keys in [
        ("Revenue", ["revenue", "total_revenue", "quarterly_revenue"]),
        ("EBITDA margin", ["ebitda_margin", "margin"]),
        ("Mobile subs", ["mobile_subscribers", "mobile_subs"]),
        ("BB subs", ["broadband_subscribers", "bb_subs", "fixed_broadband_subs"]),
        ("TV subs", ["tv_subscribers", "tv_subs"]),
        ("Monthly churn", ["churn", "monthly_churn"]),
    ]:
        val = None
        for k in keys:
            val = fh.get(k)
            if val is not None:
                break
        if val is not None:
            rank_str = ""
            # Try to find rank from comparison table
            comp = result.competition
            if comp:
                ct = safe_dict(comp, "comparison_table")
                for k in keys:
                    if k in ct:
                        rank_str = _compute_metric_rank(ct[k], result.target_operator, val)
                        break
            position_rows.append([metric, str(val), rank_str, ""])

    if position_rows:
        lines.append(md_table(["Metric", "Value", "Rank", "Assessment"], position_rows))
    else:
        lines.append("*Operator position data not available.*")

    # 1.3 Headline Numbers (code block)
    lines.append("")
    lines.append(section_header("1.3 The Headline Numbers", 3))
    lines.append("")

    headline_lines = []
    for metric, keys, suffix in [
        ("Revenue", ["revenue", "total_revenue", "quarterly_revenue"], "/q"),
        ("EBITDA", ["ebitda", "ebitda_value"], "/q"),
        ("Mobile", ["mobile_net_adds", "net_adds_mobile"], "/q net adds"),
        ("Broadband", ["bb_net_adds", "net_adds_bb", "broadband_net_adds"], "/q net adds"),
        ("B2B", ["b2b_revenue", "enterprise_revenue"], "/q"),
    ]:
        val = None
        for k in keys:
            val = fh.get(k)
            if val is not None:
                break
        if val is not None:
            growth_keys = [f"{k}_growth" for k in keys] + [f"{k}_yoy" for k in keys]
            growth = None
            for gk in growth_keys:
                growth = fh.get(gk)
                if growth is not None:
                    break
            growth_str = f"  ({fmt_pct(growth)})" if growth is not None else ""
            headline_lines.append(f"{metric:14s} {str(val):>12s}{suffix}{growth_str}")

    if headline_lines:
        lines.append(code_block("\n".join(headline_lines)))

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_key_findings(result, diagnosis) -> str:
    lines = [section_header("2. Key Findings by BLM Look", 2)]

    looks = [
        ("Look 1: Trends (PEST)", diagnosis.trends_net_assessment, result.trends),
        ("Look 2: Market & Customer ($APPEALS)", diagnosis.market_net_assessment, result.market_customer),
        ("Look 3: Competition", diagnosis.competition_net_assessment, result.competition),
        ("Look 4: Self-Analysis", diagnosis.self_net_assessment, result.self_analysis),
        ("Tariff Analysis", diagnosis.tariff_net_assessment, result.tariff_analysis),
        ("SWOT Synthesis", diagnosis.swot_net_assessment, result.swot),
        ("Look 5: Opportunities (SPAN)", diagnosis.opportunities_net_assessment, result.opportunities),
    ]

    for title, net_assessment, data in looks:
        if data is None:
            continue

        lines.append("")
        lines.append(section_header(title, 3))
        lines.append("")
        lines.append(f"**Net assessment: {net_assessment}**")
        lines.append("")

        # Extract findings from the module data
        findings = _extract_findings(title, data)
        if findings:
            lines.append(md_table(["Finding", "Impact"], findings))
        lines.append("")

    lines.append("---")

    return "\n".join(lines)


def _render_central_diagnosis(result, diagnosis, config) -> str:
    label = diagnosis.central_diagnosis_label
    if not label:
        return ""

    lines = [
        section_header(f'3. The "{label}" — Central Diagnosis', 2),
        "",
        diagnosis.central_diagnosis,
    ]

    # Dimension comparison table if competition data available
    comp = result.competition
    if comp:
        ct = safe_dict(comp, "comparison_table")
        if ct:
            lines.append("")
            # Build operator columns from comparison table
            operators = set()
            for metric_data in ct.values():
                if isinstance(metric_data, dict):
                    operators.update(metric_data.keys())
            operators = sorted(operators)

            if operators:
                headers = ["Dimension"] + [operator_display_name(op) for op in operators]
                rows = []
                for metric, values in ct.items():
                    if isinstance(values, dict):
                        row = [metric.replace("_", " ").title()]
                        for op in operators:
                            row.append(str(values.get(op, "—")))
                        rows.append(row)
                if rows:
                    lines.append(md_table(headers, rows[:10]))

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_priorities(diagnosis) -> str:
    priorities = diagnosis.priorities
    if not priorities:
        return ""

    lines = [section_header("4. Strategic Priorities — Consolidated", 2)]
    lines.append("")
    lines.append(f"Across all analyses, {len(priorities)} strategic priorities emerge consistently:")
    lines.append("")

    for i, p in enumerate(priorities, 1):
        name = p.get("name", "Unknown")
        priority_level = p.get("priority", "P1")
        urgency = {"P0": "EXISTENTIAL", "P1": "STRATEGIC", "P2": "IMPORTANT"}.get(priority_level, "")

        lines.append(section_header(f"Priority {i}: {name}" + (f" ({urgency})" if urgency else ""), 3))
        lines.append("")

        # Priority detail table
        detail_rows = []
        if p.get("metric"):
            detail_rows.append(["Addressable market", p["metric"]])
        if p.get("current"):
            detail_rows.append(["Current capability", p["current"]])
        if p.get("time_window"):
            detail_rows.append(["Time window", p["time_window"]])
        if p.get("how"):
            detail_rows.append(["Approach", p["how"]])

        if detail_rows:
            lines.append(md_table(["Aspect", "Detail"], detail_rows))
        elif p.get("description"):
            lines.append(p["description"])
        lines.append("")

    lines.append("---")

    return "\n".join(lines)


def _render_traps(diagnosis) -> str:
    traps = diagnosis.strategic_traps
    if not traps:
        return ""

    lines = [
        section_header("5. What NOT to Do", 2),
        "",
        "Equally important — strategic traps to avoid:",
        "",
    ]

    rows = []
    for t in traps:
        rows.append([
            f"**{t.get('trap', '')}**",
            t.get("temptation", ""),
            t.get("reality", ""),
        ])
    lines.append(md_table(["Trap", "Why It's Tempting", "Why It's Wrong"], rows))

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_timeline(result, diagnosis) -> str:
    priorities = diagnosis.priorities
    if not priorities:
        return ""

    period = result.analysis_period or "CQ4_2025"

    lines = [section_header("6. Timeline & Sequencing", 2), ""]

    # Build ASCII timeline from priorities
    immediate_items = []
    short_items = []
    medium_items = []
    long_items = []

    for p in priorities:
        name = p.get("name", "Unknown priority")
        window = p.get("time_window", "").lower()
        if "immediate" in window or "now" in window:
            immediate_items.append(name)
        elif "1-2" in window or "short" in window or "6" in window or "12" in window:
            short_items.append(name)
        elif "3-5" in window or "long" in window:
            long_items.append(name)
        else:
            medium_items.append(name)

    # If nothing was sorted, distribute evenly
    if not any([immediate_items, short_items, medium_items, long_items]):
        for i, p in enumerate(priorities):
            name = p.get("name", "Unknown")
            if i == 0:
                immediate_items.append(name)
            elif i <= 2:
                short_items.append(name)
            else:
                medium_items.append(name)

    timeline_parts = []
    if immediate_items:
        timeline_parts.append(f"**IMMEDIATE (Now)**")
        for item in immediate_items:
            timeline_parts.append(f"  - {item}")
        timeline_parts.append("")
    if short_items:
        timeline_parts.append(f"**SHORT-TERM (6-18 months)**")
        for item in short_items:
            timeline_parts.append(f"  - {item}")
        timeline_parts.append("")
    if medium_items:
        timeline_parts.append(f"**MEDIUM-TERM (2-3 years)**")
        for item in medium_items:
            timeline_parts.append(f"  - {item}")
        timeline_parts.append("")
    if long_items:
        timeline_parts.append(f"**LONG-TERM (3-5 years)**")
        for item in long_items:
            timeline_parts.append(f"  - {item}")

    lines.append("\n".join(timeline_parts))
    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_risk_reward(diagnosis, config) -> str:
    bull = diagnosis.bull_case
    bear = diagnosis.bear_case
    base = diagnosis.base_case

    if not bull and not bear:
        return ""

    lines = [section_header("7. Risk/Reward Summary", 2)]

    if bull:
        lines.append("")
        lines.append(section_header("7.1 If Executed Well (Bull Case)", 3))
        lines.append("")
        lines.append(f"**Scenario**: {bull.get('scenario', '')}")
        lines.append(f"**Revenue impact**: {bull.get('revenue_impact', '')}")
        lines.append(f"**Conditions**: {bull.get('conditions', '')}")

    if bear:
        lines.append("")
        lines.append(section_header("7.2 If Not Executed (Bear Case)", 3))
        lines.append("")
        lines.append(f"**Scenario**: {bear.get('scenario', '')}")
        lines.append(f"**Revenue impact**: {bear.get('revenue_impact', '')}")
        lines.append(f"**Conditions**: {bear.get('conditions', '')}")

    if base:
        lines.append("")
        lines.append(section_header("7.3 Base Case", 3))
        lines.append("")
        lines.append(f"**Scenario**: {base.get('scenario', '')}")
        lines.append(f"**Revenue impact**: {base.get('revenue_impact', '')}")

    # Net assessment table
    lines.append("")
    lines.append(section_header("7.4 Net Assessment", 3))
    lines.append("")
    rows = [
        ["Execute priorities", bull.get("revenue_impact", ""), "Investment required", "Positive net value"],
        ["Do nothing", bear.get("revenue_impact", ""), "€0", "Structural decline"],
    ]
    lines.append(md_table(["Scenario", "Revenue Delta", "Investment", "Net Value"], rows))
    lines.append("")

    lines.append("**The asymmetry is clear**: the downside of inaction exceeds the net cost of action.")
    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_dashboard(diagnosis) -> str:
    dashboard = diagnosis.kpi_dashboard
    if not dashboard:
        return ""

    lines = [section_header("8. Success Metrics Dashboard", 2), ""]

    rows = []
    for kpi in dashboard:
        rows.append([
            f"**{kpi.get('kpi', '')}**",
            kpi.get("current", ""),
            kpi.get("q2_target", ""),
            kpi.get("q4_target", ""),
            kpi.get("fy_target", ""),
        ])

    lines.append(md_table(
        ["KPI", "Current", "12-Month", "3-Year", "5-Year"],
        rows
    ))
    lines.append("")
    lines.append("---")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _extract_findings(title: str, data) -> list[list[str]]:
    """Extract key findings from a module's data for the ES summary table."""
    findings = []

    if data is None:
        return findings

    # Use key_message as the primary finding
    km = ""
    if isinstance(data, dict):
        km = data.get("key_message", "") or data.get("summary", "")
    else:
        km = safe_get(data, "key_message", "")

    if km:
        findings.append([km, ""])

    # Module-specific extraction
    if "Trends" in title:
        lifecycle = safe_get(data, "industry_lifecycle_stage", "")
        growth = safe_get(data, "industry_growth_rate", "")
        if lifecycle:
            findings.append([f"Industry lifecycle: {lifecycle}", ""])
        if growth:
            findings.append([f"Market growth: {growth}", _growth_implication(growth)])

        pest = safe_get(data, "pest")
        if pest:
            weather = safe_get(pest, "overall_weather", "mixed")
            findings.append([f"PEST weather: {weather}", safe_get(pest, "weather_explanation", "")])

    elif "Market" in title and "Customer" in title:
        outlook = safe_get(data, "market_outlook", "")
        if outlook:
            findings.append([f"Market outlook: {outlook}", ""])
        segments = safe_list(data, "customer_segments")
        if segments:
            findings.append([f"{len(segments)} customer segments identified", ""])

    elif "Competition" in title:
        intensity = safe_get(data, "overall_competition_intensity", "")
        if intensity:
            findings.append([f"Competition intensity: {intensity}", ""])
        n_comp = len(safe_dict(data, "competitor_analyses"))
        if n_comp:
            findings.append([f"{n_comp} competitor deep dives completed", ""])

    elif "Self" in title:
        health = safe_get(data, "health_rating", "")
        if health:
            findings.append([f"Health rating: {health}", ""])

    elif "SWOT" in title:
        s = len(safe_list(data, "strengths"))
        w = len(safe_list(data, "weaknesses"))
        o = len(safe_list(data, "opportunities"))
        t = len(safe_list(data, "threats"))
        findings.append([f"S:{s} W:{w} O:{o} T:{t}", f"Balance: {'S>W' if s > w else 'W>S'}, {'O>T' if o > t else 'T>O'}"])

    elif "Opportunities" in title:
        gi = len(safe_list(data, "grow_invest"))
        total = len(safe_list(data, "span_positions")) or gi
        if total:
            pct = gi / total * 100 if total else 0
            findings.append([f"{gi}/{total} ({pct:.0f}%) in Grow/Invest", "Favorable opportunity landscape"])

    return findings[:6]  # Max 6 findings per look


def _growth_implication(growth_str: str) -> str:
    """Derive implication from growth rate string."""
    if not growth_str:
        return ""
    try:
        val = float(str(growth_str).replace("%", "").replace("+", "").strip())
        if val < 0:
            return "Market is contracting"
        elif val < 1:
            return "Near-zero growth — competitive zero-sum game"
        elif val < 3:
            return "Slow growth — share gains matter"
        else:
            return "Growing market — rising tide"
    except (ValueError, TypeError):
        return ""


def _lifecycle_implication(stage: str) -> str:
    """Derive implication from lifecycle stage."""
    implications = {
        "growth": "Expansion opportunities still available",
        "mature": "Competition shifts from acquisition to retention",
        "decline": "Structural contraction — defend and optimize",
        "introduction": "Market is forming — first-mover advantages",
    }
    return implications.get(stage.lower(), "")


def _compute_metric_rank(metric_data: dict, target: str, target_val) -> str:
    """Compute rank of target operator within metric data."""
    if not isinstance(metric_data, dict):
        return ""
    from ..md_utils import safe_get as _sg
    from ..strategic_diagnosis import _to_float, _name_match

    vals = []
    for op, v in metric_data.items():
        vals.append((op, _to_float(v)))

    # Add target if not in data
    target_found = any(_name_match(op, target) for op, _ in vals)
    if not target_found:
        vals.append((target, _to_float(target_val)))

    vals.sort(key=lambda x: x[1], reverse=True)

    for i, (op, _) in enumerate(vals):
        if op == target or _name_match(op, target):
            ordinal = {0: "#1", 1: "#2", 2: "#3", 3: "#4"}.get(i, f"#{i+1}")
            return ordinal

    return ""
