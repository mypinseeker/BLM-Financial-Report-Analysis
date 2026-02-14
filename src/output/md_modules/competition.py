"""Module 03: Competition — Porter + Deep Dives renderer.

Produces the Competition section containing:
1. Market Structure Overview
2. Five Forces Analysis
3. Competitor Deep Dives
4. Cross-Operator Comparison Dashboard
5. Competitive Dynamics
6. Competitive Risk Register
"""
from __future__ import annotations

from ..md_utils import (
    section_header, section_divider, md_table,
    bold, bullet_list, fmt_smart_value, fmt_currency, fmt_pct,
    safe_get, safe_list, safe_dict,
    operator_display_name,
    collect_operator_ids, replace_operator_ids,
    empty_section_notice,
    filter_findings_by_feedback,
)


def render_competition(result, diagnosis, config, feedback=None) -> str:
    """Render Module 03: Competition Analysis."""
    comp = result.competition
    if comp is None:
        return empty_section_notice("Competition")

    parts = []
    op_map = collect_operator_ids(result)
    target_name = operator_display_name(result.target_operator)
    period = result.analysis_period or ""

    # Module title
    parts.append(f"# Competition Analysis — Porter's Five Forces + Deep Dives ({period})")
    parts.append("")
    parts.append(f"**Protagonist**: {target_name}")
    parts.append(f"**Framework**: Porter's Five Forces + Individual Competitor Profiles")
    parts.append("")
    parts.append("---")

    # 1. Market Structure
    parts.append(_render_market_structure(comp, diagnosis))

    # 2. Five Forces (with feedback filtering)
    parts.append(_render_five_forces(comp, feedback=feedback))

    # 3. Competitor Deep Dives (with feedback filtering)
    parts.append(_render_deep_dives(comp, result.target_operator, config, op_map,
                                     feedback=feedback))

    # 4. Comparison Dashboard
    parts.append(_render_comparison_dashboard(comp, config))

    # 5. Competitive Dynamics
    parts.append(_render_dynamics(comp, diagnosis, op_map))

    # 6. Risk Register
    parts.append(_render_risk_register(comp, result.target_operator))

    return "\n\n".join(p for p in parts if p)


# ---------------------------------------------------------------------------
# Sub-renderers
# ---------------------------------------------------------------------------

def _render_market_structure(comp, diagnosis) -> str:
    lines = [section_header("1. Market Structure Overview", 2), ""]

    n_competitors = len(safe_dict(comp, "competitor_analyses"))
    intensity = safe_get(comp, "overall_competition_intensity", "medium")
    landscape = safe_get(comp, "competitive_landscape", "")

    rows = [
        ["Number of operators", str(n_competitors + 1)],
        ["Market structure", diagnosis.market_structure],
        ["Competition intensity", bold(intensity.title())],
    ]

    if diagnosis.operator_position_label:
        rows.append(["Target position", diagnosis.operator_position_label])

    lines.append(md_table(["Metric", "Value"], rows))

    if landscape:
        lines.append("")
        lines.append(landscape)

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_five_forces(comp, feedback=None) -> str:
    forces = safe_dict(comp, "five_forces")
    # Filter forces via feedback: porter_{force_id} refs
    if feedback and forces:
        fb_map = {fb.get("finding_ref", ""): fb for fb in feedback}
        filtered = {}
        for force_id, force in forces.items():
            ref = f"porter_{force_id}"
            fb = fb_map.get(ref)
            if fb and fb.get("feedback_type") == "disputed":
                continue  # Remove this force
            filtered[force_id] = force
        forces = filtered
    if not forces:
        return ""

    lines = [section_header("2. Five Forces Analysis", 2), ""]

    # Summary table
    force_display = {
        "existing_competitors": "Existing Competitors",
        "new_entrants": "Threat of New Entrants",
        "substitutes": "Threat of Substitutes",
        "supplier_power": "Supplier Bargaining Power",
        "buyer_power": "Buyer Bargaining Power",
    }

    rows = []
    for force_id, force in forces.items():
        name = force_display.get(force_id, safe_get(force, "force_name", force_id).replace("_", " ").title())
        level = safe_get(force, "force_level", "medium")
        level_icon = {"high": "High", "medium": "Medium", "low": "Low"}.get(level, level.title())

        # Collect key drivers
        key_factors = safe_list(force, "key_factors")
        drivers = []
        for kf in key_factors[:3]:
            if isinstance(kf, dict):
                drivers.append(kf.get("name", kf.get("description", "")))
            elif isinstance(kf, str):
                drivers.append(kf)
        driver_str = "; ".join(drivers) if drivers else ""

        rows.append([name, bold(level_icon), driver_str])

    lines.append(md_table(["Force", "Level", "Key Drivers"], rows))

    # Detailed analysis per force
    for force_id, force in forces.items():
        name = force_display.get(force_id, safe_get(force, "force_name", force_id).replace("_", " ").title())
        key_factors = safe_list(force, "key_factors")
        implications = safe_list(force, "implications")

        if not key_factors and not implications:
            continue

        lines.append("")
        lines.append(section_header(name, 3))

        if key_factors:
            lines.append("")
            factor_rows = []
            for kf in key_factors:
                if isinstance(kf, dict):
                    factor_rows.append([
                        kf.get("name", ""),
                        kf.get("description", ""),
                        kf.get("impact", ""),
                        kf.get("trend", ""),
                    ])
            if factor_rows:
                lines.append(md_table(["Factor", "Description", "Impact", "Trend"], factor_rows))

        if implications:
            lines.append("")
            lines.append("**Implications**:")
            for imp in implications:
                lines.append(f"- {imp}")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_deep_dives(comp, target_operator: str, config=None,
                       op_map: dict[str, str] = None, feedback=None) -> str:
    analyses = safe_dict(comp, "competitor_analyses")
    # Filter competitor deep dives via feedback: competitor_{op_id} refs
    if feedback and analyses:
        fb_map = {fb.get("finding_ref", ""): fb for fb in feedback}
        filtered = {}
        for op_id, dd in analyses.items():
            ref = f"competitor_{op_id}"
            fb = fb_map.get(ref)
            if fb and fb.get("feedback_type") == "disputed":
                continue
            filtered[op_id] = dd
        analyses = filtered
    if not analyses:
        return ""

    lines = [section_header("3. Competitor Deep Dives", 2)]

    for op_id, dd in analyses.items():
        op_name = operator_display_name(op_id)
        lines.append("")
        lines.append(section_header(f"{op_name}", 3))
        lines.append("")

        # Financial profile — skip trend arrays and internal flags
        fh = safe_dict(dd, "financial_health")
        sh = safe_dict(dd, "subscriber_health")
        _SKIP_KEYS = {
            'revenue_trend', 'ebitda_trend', 'margin_trend',
            'revenue_growing', 'margin_healthy',
            'quarters_analyzed', 'status', 'latest_quarter',
        }

        if fh or sh:
            lines.append(section_header("Financial & Subscriber Profile", 4))
            lines.append("")
            profile_rows = []
            for k, v in fh.items():
                if k in _SKIP_KEYS or isinstance(v, (list, tuple)):
                    continue
                profile_rows.append([k.replace("_", " ").title(), fmt_smart_value(k, v, config)])
            for k, v in sh.items():
                if k in _SKIP_KEYS or isinstance(v, (list, tuple)):
                    continue
                profile_rows.append([k.replace("_", " ").title(), fmt_smart_value(k, v, config)])
            if profile_rows:
                lines.append(md_table(["Metric", "Value"], profile_rows))
            lines.append("")

        # Momentum Indicators (from trend_analyzer enrichment)
        _momentum_rows = []
        for m_label, m_key in [("Revenue", "revenue_metrics"), ("Margin", "margin_metrics")]:
            tm = fh.get(m_key) if fh else None
            if not isinstance(tm, dict) or not tm:
                continue
            cagr = tm.get("cagr_pct")
            phase = tm.get("momentum_phase", "")
            score = tm.get("momentum_score")
            _momentum_rows.append([
                m_label,
                f"{cagr:+.1f}%" if cagr is not None else "—",
                _format_phase(phase),
                f"{score:.0f}/100" if score is not None else "—",
            ])
        if _momentum_rows:
            lines.append(section_header("Momentum Indicators", 4))
            lines.append("")
            lines.append(md_table(
                ["Metric", "CAGR", "Phase", "Momentum Score"],
                _momentum_rows,
            ))
            lines.append("")

        # Strategy
        strategy = safe_get(dd, "growth_strategy", "")
        if strategy:
            lines.append(f"**Growth strategy**: {strategy}")
            lines.append("")

        # Business model
        biz_model = safe_get(dd, "business_model", "")
        if biz_model:
            lines.append(f"**Business model**: {biz_model}")
            lines.append("")

        # Network status
        network = safe_dict(dd, "network_status")
        if network:
            lines.append(section_header("Network Status", 4))
            lines.append("")
            for k, v in network.items():
                display_v = fmt_smart_value(k, v, config)
                lines.append(f"- **{k.replace('_', ' ').title()}**: {display_v}")
            lines.append("")

        # Product portfolio
        products = safe_list(dd, "product_portfolio")
        if products:
            lines.append(f"**Product portfolio**: {'; '.join(products[:5])}")
            lines.append("")

        # Pipeline
        pipeline = safe_list(dd, "new_product_pipeline")
        if pipeline:
            lines.append(f"**Product pipeline**: {'; '.join(pipeline[:5])}")
            lines.append("")

        # Control points
        ctrl = safe_list(dd, "core_control_points")
        if ctrl:
            lines.append(f"**Core control points**: {'; '.join(ctrl[:5])}")
            lines.append("")

        # Ecosystem
        eco = safe_list(dd, "ecosystem_partners")
        if eco:
            lines.append(f"**Ecosystem partners**: {'; '.join(eco[:5])}")
            lines.append("")

        # M&A
        ma = safe_list(dd, "ma_activity")
        if ma:
            lines.append(f"**M&A activity**: {'; '.join(ma[:3])}")
            lines.append("")

        # Org / culture
        org = safe_get(dd, "org_structure", "")
        if org:
            lines.append(f"**Organization**: {org}")
            lines.append("")

        # Problems
        problems = safe_list(dd, "problems")
        if problems:
            lines.append("**Key problems**:")
            for p in problems[:5]:
                lines.append(f"- {p}")
            lines.append("")

        # Strengths & weaknesses
        strengths = safe_list(dd, "strengths")
        weaknesses = safe_list(dd, "weaknesses")

        if strengths or weaknesses:
            lines.append(section_header("Strengths & Weaknesses", 4))
            lines.append("")
            sw_rows = []
            max_items = max(len(strengths), len(weaknesses))
            for i in range(min(max_items, 5)):
                s = strengths[i] if i < len(strengths) else ""
                w = weaknesses[i] if i < len(weaknesses) else ""
                sw_rows.append([s, w])
            lines.append(md_table(["Strengths", "Weaknesses"], sw_rows))
            lines.append("")

        # Implications for target
        implications = safe_list(dd, "implications")
        if implications:
            lines.append(section_header(f"Implications for {operator_display_name(target_operator)}", 4))
            lines.append("")
            for imp in implications:
                imp_type = safe_get(imp, "implication_type", "").title()
                desc = replace_operator_ids(safe_get(imp, "description", ""), op_map)
                action = replace_operator_ids(safe_get(imp, "suggested_action", ""), op_map)
                if desc:
                    prefix = f"**{imp_type}**: " if imp_type else ""
                    lines.append(f"- {prefix}{desc}")
                    if action:
                        lines.append(f"  - *Action*: {action}")
            lines.append("")

        # Future actions
        future = safe_list(dd, "likely_future_actions")
        if future:
            lines.append("**Likely future actions**:")
            for f in future[:5]:
                lines.append(f"- {replace_operator_ids(f, op_map)}")
            lines.append("")

    lines.append("---")

    return "\n".join(lines)


def _render_comparison_dashboard(comp, config=None) -> str:
    ct = safe_dict(comp, "comparison_table")
    if not ct:
        return ""

    lines = [section_header("4. Cross-Operator Comparison Dashboard", 2), ""]

    # Collect all operators
    all_ops = set()
    for metric_data in ct.values():
        if isinstance(metric_data, dict):
            all_ops.update(metric_data.keys())
    all_ops = sorted(all_ops)

    if not all_ops:
        return ""

    headers = ["Metric"] + [operator_display_name(op) for op in all_ops]
    rows = []
    for metric, values in ct.items():
        if not isinstance(values, dict):
            continue
        display_metric = metric.replace("_", " ").title()
        row = [bold(display_metric)]
        for op in all_ops:
            val = values.get(op, "—")
            row.append(fmt_smart_value(metric, val, config))
        rows.append(row)

    if rows:
        lines.append(md_table(headers, rows))

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_dynamics(comp, diagnosis, op_map: dict[str, str] = None) -> str:
    landscape = safe_get(comp, "competitive_landscape", "")
    km = safe_get(comp, "key_message", "")

    if not landscape and not km:
        return ""

    lines = [section_header("5. Competitive Dynamics", 2), ""]

    if landscape:
        lines.append(replace_operator_ids(landscape, op_map))
        lines.append("")

    if km:
        lines.append(f"**Key message**: {replace_operator_ids(km, op_map)}")
        lines.append("")

    lines.append(f"**Net assessment**: {replace_operator_ids(diagnosis.competition_net_assessment, op_map)}")
    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_risk_register(comp, target_operator: str) -> str:
    """Build a risk register from competitor implications."""
    analyses = safe_dict(comp, "competitor_analyses")
    if not analyses:
        return ""

    risks = []
    for op_id, dd in analyses.items():
        op_name = operator_display_name(op_id)
        implications = safe_list(dd, "implications")
        for imp in implications:
            if safe_get(imp, "implication_type") == "threat":
                risks.append({
                    "source": op_name,
                    "risk": safe_get(imp, "description", ""),
                    "action": safe_get(imp, "suggested_action", ""),
                })

    if not risks:
        return ""

    lines = [section_header("6. Competitive Risk Register", 2), ""]

    rows = []
    for r in risks[:8]:
        rows.append([r["source"], r["risk"], r["action"]])

    lines.append(md_table(["Source", "Risk", "Suggested Action"], rows))
    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _format_phase(phase: str) -> str:
    """Convert momentum_phase code to a human-friendly label."""
    labels = {
        "accelerating_growth": "Accelerating Growth",
        "decelerating_growth": "Decelerating Growth",
        "stabilizing": "Stabilizing",
        "accelerating_decline": "Accelerating Decline",
        "recovery": "Recovery",
        "flat": "Flat",
    }
    return labels.get(phase, phase.replace("_", " ").title() if phase else "—")
