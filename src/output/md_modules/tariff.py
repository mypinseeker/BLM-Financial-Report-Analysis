"""Module 02a: Tariff Deep Analysis renderer.

Only rendered if result.tariff_analysis is not None.

Produces the Tariff section containing:
1. Tariff Overview
2. Mobile Pricing Comparison
3. Value Analysis (cost-per-unit)
4. Price Evolution / Historical Trends
5. Fixed Broadband / FMC / TV Comparisons
6. Strategic Implications
"""
from __future__ import annotations

from ..md_utils import (
    section_header, section_divider, md_table,
    bold, bullet_list, fmt_pct, fmt_currency,
    safe_get, safe_list, safe_dict,
    operator_display_name,
    empty_section_notice,
)


def render_tariff(result, diagnosis, config) -> str:
    """Render Module 02a: Tariff Deep Analysis."""
    tariff = result.tariff_analysis
    if tariff is None:
        return ""  # Skip silently if no tariff data

    if not isinstance(tariff, dict):
        return empty_section_notice("Tariff")

    parts = []
    target_name = operator_display_name(result.target_operator)
    period = result.analysis_period or ""

    # Module title
    parts.append(f"# Tariff Deep Analysis ({period})")
    parts.append("")

    # Summary stats
    record_count = tariff.get("total_records") or tariff.get("record_count", "")
    if record_count:
        parts.append(f"**Data basis**: {record_count} tariff records analyzed")
    parts.append("")
    parts.append("---")

    # 1. Overview
    parts.append(_render_overview(tariff, target_name, config))

    # 2. Mobile Pricing
    parts.append(_render_mobile_pricing(tariff, target_name, config))

    # 3. Value Analysis
    parts.append(_render_value_analysis(tariff, target_name))

    # 4. Price Evolution
    parts.append(_render_price_evolution(tariff))

    # 5. Fixed/FMC/TV
    parts.append(_render_fixed_comparisons(tariff, target_name, config))

    # 6. Strategic Implications
    parts.append(_render_strategic_implications(tariff, diagnosis))

    return "\n\n".join(p for p in parts if p)


# ---------------------------------------------------------------------------
# Sub-renderers
# ---------------------------------------------------------------------------

def _render_overview(tariff: dict, target_name: str, config) -> str:
    summary = tariff.get("summary") or tariff.get("overview", "")
    if not summary and not tariff.get("key_findings"):
        return ""

    lines = [section_header("1. Tariff Landscape Overview", 2), ""]

    if summary:
        lines.append(summary)
        lines.append("")

    findings = tariff.get("key_findings") or []
    if findings:
        for f in findings:
            if isinstance(f, str):
                lines.append(f"- {f}")
            elif isinstance(f, dict):
                lines.append(f"- **{f.get('finding', '')}**: {f.get('impact', '')}")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_mobile_pricing(tariff: dict, target_name: str, config) -> str:
    mobile = tariff.get("mobile_pricing") or tariff.get("mobile_comparison") or tariff.get("mobile", {})
    if not mobile:
        # Try flat structure
        operators = tariff.get("operators") or tariff.get("operator_comparison") or {}
        if operators:
            return _render_operator_comparison(operators, target_name, "Mobile", config)
        return ""

    lines = [section_header("2. Mobile Pricing Comparison", 2), ""]

    if isinstance(mobile, list):
        # List of tariff records
        rows = []
        for m in mobile[:15]:
            if isinstance(m, dict):
                rows.append([
                    m.get("operator", ""),
                    m.get("plan_name", m.get("name", "")),
                    str(m.get("price", "")),
                    str(m.get("data", m.get("data_gb", ""))),
                    str(m.get("cost_per_gb", m.get("price_per_gb", ""))),
                ])
        if rows:
            lines.append(md_table(
                ["Operator", "Plan", "Price", "Data", "€/GB"],
                rows
            ))
    elif isinstance(mobile, dict):
        _render_dict_section(mobile, lines)

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_operator_comparison(operators: dict, target_name: str,
                                 segment: str, config) -> str:
    if not operators:
        return ""

    lines = [section_header(f"2. {segment} Pricing Comparison", 2), ""]

    # Operators dict: {operator_id: {tier: price, ...}} or similar
    if isinstance(operators, dict):
        all_tiers = set()
        for op_data in operators.values():
            if isinstance(op_data, dict):
                all_tiers.update(op_data.keys())
        tiers = sorted(all_tiers)

        if tiers:
            headers = ["Operator"] + [str(t).replace("_", " ").title() for t in tiers]
            rows = []
            for op_id, op_data in operators.items():
                row = [operator_display_name(op_id)]
                for tier in tiers:
                    val = op_data.get(tier, "—") if isinstance(op_data, dict) else "—"
                    row.append(str(val))
                rows.append(row)
            lines.append(md_table(headers, rows))

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_value_analysis(tariff: dict, target_name: str) -> str:
    value = tariff.get("value_analysis") or tariff.get("cost_per_unit") or {}
    if not value:
        return ""

    lines = [section_header("3. Value Analysis (Cost per Unit)", 2), ""]
    _render_dict_section(value, lines)
    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_price_evolution(tariff: dict) -> str:
    evolution = tariff.get("price_evolution") or tariff.get("historical_trends") or {}
    if not evolution:
        return ""

    lines = [section_header("4. Price Evolution", 2), ""]

    if isinstance(evolution, dict):
        _render_dict_section(evolution, lines)
    elif isinstance(evolution, list):
        for item in evolution:
            if isinstance(item, str):
                lines.append(f"- {item}")
            elif isinstance(item, dict):
                period = item.get("period", "")
                change = item.get("change", item.get("description", ""))
                lines.append(f"- **{period}**: {change}")

    lines.append("")
    lines.append("---")

    return "\n".join(lines)


def _render_fixed_comparisons(tariff: dict, target_name: str, config) -> str:
    sections = []

    for key, title in [
        ("fixed_broadband", "Fixed Broadband Pricing"),
        ("fmc_bundles", "FMC Bundle Pricing"),
        ("tv_comparison", "TV Pricing"),
        ("convergence", "Convergence Analysis"),
    ]:
        data = tariff.get(key, {})
        if not data:
            continue

        lines = [section_header(title, 3), ""]
        if isinstance(data, dict):
            _render_dict_section(data, lines)
        elif isinstance(data, list):
            rows = []
            for item in data[:10]:
                if isinstance(item, dict):
                    rows.append([str(v) for v in item.values()])
            if rows:
                headers = list(data[0].keys()) if data and isinstance(data[0], dict) else []
                if headers:
                    lines.append(md_table(headers, rows))
        elif isinstance(data, str):
            lines.append(data)
        sections.append("\n".join(lines))

    if not sections:
        return ""

    result = [section_header("5. Fixed & Convergence Pricing", 2), ""]
    result.append("\n\n".join(sections))
    result.append("")
    result.append("---")

    return "\n".join(result)


def _render_strategic_implications(tariff: dict, diagnosis) -> str:
    implications = tariff.get("strategic_implications") or tariff.get("implications") or []
    km = tariff.get("key_message") or tariff.get("summary", "")

    if not implications and not km:
        return ""

    lines = [section_header("6. Strategic Implications", 2), ""]

    if km:
        lines.append(f"**Key message**: {km}")
        lines.append("")

    if isinstance(implications, list):
        for imp in implications:
            if isinstance(imp, str):
                lines.append(f"- {imp}")
            elif isinstance(imp, dict):
                lines.append(f"- **{imp.get('implication', imp.get('title', ''))}**: "
                             f"{imp.get('detail', imp.get('description', ''))}")
    elif isinstance(implications, str):
        lines.append(implications)

    lines.append("")
    lines.append(f"**Net assessment**: {diagnosis.tariff_net_assessment}")
    lines.append("")
    lines.append("---")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _render_dict_section(data: dict, lines: list):
    """Render a dict as either a table or key-value pairs depending on structure."""
    if not data:
        return

    # Check if values are simple (table) or complex (nested)
    simple_items = []
    complex_items = []
    for k, v in data.items():
        if isinstance(v, (str, int, float, bool)):
            simple_items.append((k, v))
        else:
            complex_items.append((k, v))

    if simple_items:
        rows = [[k.replace("_", " ").title(), str(v)] for k, v in simple_items]
        lines.append(md_table(["Metric", "Value"], rows))

    for k, v in complex_items:
        title = k.replace("_", " ").title()
        lines.append("")
        lines.append(f"**{title}**:")
        if isinstance(v, list):
            for item in v[:8]:
                if isinstance(item, dict):
                    # Compact dict items
                    parts = [f"{dk}: {dv}" for dk, dv in item.items()]
                    lines.append(f"- {'; '.join(parts)}")
                else:
                    lines.append(f"- {item}")
        elif isinstance(v, dict):
            # Check for nested dicts with simple values
            has_nested = any(isinstance(sv, (dict, list)) for sv in v.values())
            if has_nested:
                # Flatten nested dicts for display
                for sk, sv in v.items():
                    if isinstance(sv, dict):
                        compact = "; ".join(f"{dk}: {dv}" for dk, dv in sv.items())
                        lines.append(f"  - **{sk.replace('_', ' ').title()}**: {compact}")
                    elif isinstance(sv, list):
                        lines.append(f"  - **{sk.replace('_', ' ').title()}**: {', '.join(str(x) for x in sv)}")
                    else:
                        lines.append(f"  - **{sk.replace('_', ' ').title()}**: {sv}")
            else:
                rows = [[sk.replace("_", " ").title(), str(sv)] for sk, sv in v.items()]
                lines.append(md_table(["Item", "Value"], rows))
        else:
            lines.append(str(v))
