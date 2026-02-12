"""Shared Markdown formatting helpers for BLM strategic report generation.

Provides table builders, currency/percentage formatters, section helpers,
and safe attribute accessors used across all module renderers.
"""
from __future__ import annotations

from typing import Any, Optional


# ---------------------------------------------------------------------------
# Table builders
# ---------------------------------------------------------------------------

def md_table(headers: list[str], rows: list[list[str]],
             align: list[str] | None = None) -> str:
    """Build a Markdown table with optional column alignment.

    Args:
        headers: Column header strings.
        rows: List of rows, each a list of cell strings.
        align: Per-column alignment: "l" (left), "r" (right), "c" (center).
               Defaults to all left-aligned.

    Returns:
        Formatted Markdown table string.
    """
    if not headers:
        return ""
    ncols = len(headers)
    if align is None:
        align = ["l"] * ncols
    # Pad align list
    while len(align) < ncols:
        align.append("l")

    sep_map = {"l": ":---", "r": "---:", "c": ":---:"}
    sep = [sep_map.get(a, ":---") for a in align]

    lines = []
    lines.append("| " + " | ".join(str(h) for h in headers) + " |")
    lines.append("| " + " | ".join(sep) + " |")
    for row in rows:
        # Pad row to match headers
        cells = list(row) + [""] * (ncols - len(row))
        lines.append("| " + " | ".join(str(c) for c in cells[:ncols]) + " |")
    return "\n".join(lines)


def md_kv_table(data: dict | list[tuple], header_key: str = "Item",
                header_val: str = "Detail") -> str:
    """Build a 2-column key-value Markdown table."""
    if isinstance(data, dict):
        items = list(data.items())
    else:
        items = list(data)
    if not items:
        return ""
    rows = [[str(k), str(v)] for k, v in items]
    return md_table([header_key, header_val], rows)


# ---------------------------------------------------------------------------
# Number formatters
# ---------------------------------------------------------------------------

def fmt_currency(value, config=None, suffix: str = "M",
                 show_sign: bool = False) -> str:
    """Format a currency value with symbol and suffix.

    Examples:
        fmt_currency(3092, config)  -> "€3,092M"
        fmt_currency(245000, config) -> "CLP 245,000M"
    """
    if value is None:
        return "N/A"
    try:
        num = float(value)
    except (TypeError, ValueError):
        return str(value)
    symbol = ""
    if config is not None:
        symbol = getattr(config, "currency_symbol", "")
        if not symbol:
            symbol = getattr(config, "currency", "")
            if symbol:
                symbol = symbol + " "
    sign = ""
    if show_sign and num > 0:
        sign = "+"
    elif show_sign and num < 0:
        sign = "-"
        num = abs(num)
    formatted = f"{num:,.0f}" if num == int(num) else f"{num:,.1f}"
    return f"{sign}{symbol}{formatted}{suffix}"


def fmt_pct(value, show_sign: bool = True, decimals: int = 1) -> str:
    """Format a percentage value.

    Examples:
        fmt_pct(8.9)   -> "+8.9%"
        fmt_pct(-3.4)  -> "-3.4%"
        fmt_pct(None)  -> "N/A"
    """
    if value is None:
        return "N/A"
    try:
        num = float(value)
    except (TypeError, ValueError):
        return str(value)
    sign = "+" if show_sign and num > 0 else ""
    return f"{sign}{num:.{decimals}f}%"


def fmt_subs(value_k) -> str:
    """Format subscriber count (in thousands).

    Examples:
        fmt_subs(32500) -> "32,500K"
        fmt_subs(None)  -> "N/A"
    """
    if value_k is None:
        return "N/A"
    try:
        num = float(value_k)
    except (TypeError, ValueError):
        return str(value_k)
    if abs(num) >= 1000:
        return f"{num:,.0f}K"
    return f"{num:.0f}K"


def fmt_smart_value(key: str, value, config=None) -> str:
    """Intelligently format a value based on its key name and type.

    Handles dict unpacking, list compacting, currency/subscriber/pct formatting.
    """
    if value is None:
        return "N/A"

    # Unpack dict values like {'value': 1520.0, 'share_pct': 49.2}
    if isinstance(value, dict):
        if 'value' in value:
            inner = value['value']
            share = value.get('share_pct')
            formatted = fmt_smart_value(key, inner, config)
            if share is not None:
                return f"{formatted} ({share:.1f}%)"
            return formatted
        # Compact format for other dicts (spectrum, etc.)
        parts = []
        for k, v in value.items():
            dk = k.replace('_', ' ').title()
            parts.append(f"{dk}: {v}")
        return '; '.join(parts)

    # Unpack list values
    if isinstance(value, (list, tuple)):
        return ', '.join(str(x) for x in value)

    # Boolean
    if isinstance(value, bool):
        return "Yes" if value else "No"

    k_lower = key.lower()

    # Revenue/EBITDA/financial fields → currency (but not margins/ratios)
    _rev_tokens = ('revenue', 'ebitda', 'net_income', 'capex', 'opex')
    _exclude_rev = ('pct', 'growth', 'trend', 'growing', 'margin', 'share')
    if (any(rk in k_lower for rk in _rev_tokens)
            and not any(ex in k_lower for ex in _exclude_rev)):
        return fmt_currency(value, config)

    # Subscriber fields → K formatting
    _sub_tokens = ('subscriber', 'subs')
    if ('_k' in k_lower and 'pct' not in k_lower) or any(st in k_lower for st in _sub_tokens):
        return fmt_subs(value)

    # Percentage fields
    if '_pct' in k_lower:
        try:
            return fmt_pct(float(value), show_sign=False)
        except (TypeError, ValueError):
            return str(value)

    # Growth fields
    if 'growth' in k_lower:
        try:
            return fmt_pct(float(value), show_sign=True)
        except (TypeError, ValueError):
            return str(value)

    # ARPU
    if 'arpu' in k_lower:
        try:
            symbol = ""
            if config:
                symbol = getattr(config, 'currency_symbol', '')
            return f"{symbol}{float(value):.2f}"
        except (TypeError, ValueError):
            return str(value)

    # Churn / share / coverage / penetration — percentage-like fields
    _pct_tokens = ('churn', 'share', 'coverage', 'penetration', 'margin')
    if any(tok in k_lower for tok in _pct_tokens) and 'trend' not in k_lower:
        try:
            num = float(value)
            if abs(num) <= 100:  # Looks like a percentage
                return fmt_pct(num, show_sign=False)
        except (TypeError, ValueError):
            pass

    # Generic numeric with comma formatting
    try:
        num = float(value)
        if num == int(num) and abs(num) >= 100:
            return f"{int(num):,}"
        return str(value)
    except (TypeError, ValueError):
        return str(value)


def fmt_number(value, decimals: int = 0, show_sign: bool = False) -> str:
    """Format a generic number with thousands separators."""
    if value is None:
        return "N/A"
    try:
        num = float(value)
    except (TypeError, ValueError):
        return str(value)
    sign = "+" if show_sign and num > 0 else ""
    if decimals == 0:
        return f"{sign}{num:,.0f}"
    return f"{sign}{num:,.{decimals}f}"


# ---------------------------------------------------------------------------
# Section / layout helpers
# ---------------------------------------------------------------------------

def section_header(title: str, level: int = 2) -> str:
    """Return a Markdown heading."""
    prefix = "#" * level
    return f"{prefix} {title}"


def section_divider() -> str:
    """Return a horizontal rule."""
    return "\n---\n"


def module_comment(module_id: str, module_title: str,
                   source_hint: str = "") -> str:
    """Return an HTML comment block marking a module boundary."""
    lines = [
        "",
        f"<!-- {'=' * 60} -->",
        f"<!-- MODULE: {module_id} — {module_title} -->",
    ]
    if source_hint:
        lines.append(f"<!-- Source: {source_hint} -->")
    lines.append(f"<!-- {'=' * 60} -->")
    lines.append("")
    return "\n".join(lines)


def blockquote(text: str) -> str:
    """Wrap text in a Markdown blockquote."""
    if not text:
        return ""
    return "\n".join(f"> {line}" for line in text.split("\n"))


def bold(text: str) -> str:
    return f"**{text}**"


def code_block(text: str, lang: str = "") -> str:
    """Wrap text in a fenced code block."""
    return f"```{lang}\n{text}\n```"


# ---------------------------------------------------------------------------
# Display name helpers
# ---------------------------------------------------------------------------

def operator_display_name(operator_id: str) -> str:
    """Convert operator_id to display name.

    'vodafone_germany' -> 'Vodafone Germany'
    'telefonica_o2' -> 'Telefónica O2'
    'one_and_one' -> '1&1 AG'
    """
    if not operator_id:
        return "Unknown Operator"
    special = {
        # Germany
        "dt_germany": "Deutsche Telekom",
        "deutsche_telekom": "Deutsche Telekom",
        "o2_germany": "Telefónica O2",
        "telefonica_o2": "Telefónica O2",
        "telefonica_o2_germany": "Telefónica O2",
        "1and1_germany": "1&1 AG",
        "one_and_one": "1&1 AG",
        # Chile
        "entel_cl": "Entel",
        "entel": "Entel",
        "movistar_cl": "Movistar Chile",
        "claro_cl": "Claro Chile",
        "claro": "Claro Chile",
        "wom_cl": "WOM Chile",
        "wom": "WOM Chile",
        "tigo_cl": "Tigo Chile",
    }
    if operator_id in special:
        return special[operator_id]
    return operator_id.replace("_", " ").title()


def collect_operator_ids(result) -> dict[str, str]:
    """Collect all known operator_ids from a FiveLooksResult.

    Returns:
        Dict mapping operator_id -> display name for all operators
        (target + competitors) found in the result.
    """
    ops: dict[str, str] = {}
    target = getattr(result, 'target_operator', '') or ''
    if target:
        ops[target] = operator_display_name(target)
    comp = getattr(result, 'competition', None)
    if comp:
        analyses = getattr(comp, 'competitor_analyses', None) or {}
        if isinstance(analyses, dict):
            for op_id in analyses:
                ops[op_id] = operator_display_name(op_id)
    return ops


def replace_operator_ids(text: str, op_map: dict[str, str]) -> str:
    """Replace all known operator_ids in text with their display names.

    Replaces longest IDs first to avoid partial matches.
    """
    if not text or not op_map:
        return text
    for op_id in sorted(op_map.keys(), key=len, reverse=True):
        if op_id in text:
            text = text.replace(op_id, op_map[op_id])
    return text


def market_display_name(market_id: str) -> str:
    """Convert market_id to display name."""
    if not market_id:
        return "Unknown Market"
    special = {
        "germany": "German Telecommunications",
        "chile": "Chilean Telecommunications",
        "guatemala": "Guatemalan Telecommunications",
        "honduras": "Honduran Telecommunications",
        "el_salvador": "Salvadoran Telecommunications",
        "colombia": "Colombian Telecommunications",
        "panama": "Panamanian Telecommunications",
        "bolivia": "Bolivian Telecommunications",
        "paraguay": "Paraguayan Telecommunications",
        "nicaragua": "Nicaraguan Telecommunications",
    }
    return special.get(market_id, f"{market_id.replace('_', ' ').title()} Telecommunications")


# ---------------------------------------------------------------------------
# ASCII Timeline
# ---------------------------------------------------------------------------

def ascii_timeline(phases: list[dict]) -> str:
    """Build a multi-line ASCII Gantt chart.

    Each phase dict: {name, label, items: [str], start_col, width}
    Where start_col/width are in "quarter" units (0-based).
    """
    if not phases:
        return ""
    lines = []
    # Header bar
    max_cols = max((p.get("start_col", 0) + p.get("width", 4)) for p in phases)
    quarter_labels = []
    for i in range(max_cols):
        quarter_labels.append(f"Q{(i % 4) + 1}")

    for phase in phases:
        name = phase.get("name", "")
        items = phase.get("items", [])
        start = phase.get("start_col", 0)
        width = phase.get("width", 4)

        lines.append(f"{name}")
        bar = " " * (start * 4) + "█" * (width * 4)
        lines.append(f"  {bar}")
        for item in items:
            lines.append(f"  ├─ {item}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Safe data access
# ---------------------------------------------------------------------------

def safe_get(obj, attr: str, default: Any = "") -> Any:
    """Safely get an attribute from a dataclass, dict, or nested path.

    Supports dotted paths: safe_get(obj, "pest.overall_weather", "mixed")
    """
    if obj is None:
        return default

    parts = attr.split(".")
    current = obj
    for part in parts:
        if current is None:
            return default
        if isinstance(current, dict):
            current = current.get(part, None)
        else:
            current = getattr(current, part, None)

    return current if current is not None else default


def safe_list(obj, attr: str) -> list:
    """Safely get a list attribute, always returns a list."""
    val = safe_get(obj, attr, [])
    if isinstance(val, list):
        return val
    return []


def safe_dict(obj, attr: str) -> dict:
    """Safely get a dict attribute, always returns a dict."""
    val = safe_get(obj, attr, {})
    if isinstance(val, dict):
        return val
    return {}


def items_or_empty(items: list | None, placeholder: str = "") -> list:
    """Return items list or a list with a single placeholder if empty."""
    if items:
        return items
    if placeholder:
        return [placeholder]
    return []


def truncate(text: str, max_len: int = 120) -> str:
    """Truncate text with ellipsis if too long."""
    if not text:
        return ""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


# ---------------------------------------------------------------------------
# Bullet / list helpers
# ---------------------------------------------------------------------------

def bullet_list(items: list[str], prefix: str = "- ") -> str:
    """Format items as a bulleted list."""
    if not items:
        return ""
    return "\n".join(f"{prefix}{item}" for item in items if item)


def numbered_list(items: list[str]) -> str:
    """Format items as a numbered list."""
    if not items:
        return ""
    return "\n".join(f"{i}. {item}" for i, item in enumerate(items, 1) if item)


def empty_section_notice(section_name: str) -> str:
    """Return a notice that a section has insufficient data."""
    return f"\n*Insufficient data for {section_name} analysis.*\n"
