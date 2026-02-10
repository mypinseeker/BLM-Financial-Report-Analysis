"""Markdown parsing utilities for deep analysis MD files.

Extracts tables, bullet lists, metrics, and structured data
from the 8 deep analysis markdown documents.
"""

from __future__ import annotations

import re
from typing import Optional


def parse_md_table(text: str, header_pattern: str = "") -> list[dict]:
    """Parse a markdown table into a list of dicts.

    Args:
        text: Full markdown text or section containing the table.
        header_pattern: If given, find the table after this heading.

    Returns:
        List of dicts, one per row, keyed by column headers.
    """
    if header_pattern:
        match = re.search(
            rf'{re.escape(header_pattern)}.*?\n'
            r'(\|.+?\|(?:\n\|.+?\|)*)',
            text, re.DOTALL)
        if not match:
            return []
        table_text = match.group(1)
    else:
        table_text = text

    lines = [l.strip() for l in table_text.strip().split('\n')
             if l.strip().startswith('|')]
    if len(lines) < 3:
        return []

    def split_row(line: str) -> list[str]:
        cells = [c.strip() for c in line.strip('|').split('|')]
        return [c.strip('* ') for c in cells]

    headers = split_row(lines[0])
    # Skip separator line (lines[1])
    rows = []
    for line in lines[2:]:
        if re.match(r'^\|[\s\-:]+\|$', line):
            continue
        cells = split_row(line)
        if len(cells) >= len(headers):
            rows.append(dict(zip(headers, cells[:len(headers)])))
        elif cells:
            padded = cells + [''] * (len(headers) - len(cells))
            rows.append(dict(zip(headers, padded)))
    return rows


def parse_md_tables_all(text: str) -> list[list[dict]]:
    """Find and parse all markdown tables in text."""
    tables = []
    # Find table blocks: sequences of lines starting with |
    in_table = False
    current_lines = []
    for line in text.split('\n'):
        stripped = line.strip()
        if stripped.startswith('|'):
            in_table = True
            current_lines.append(stripped)
        else:
            if in_table and current_lines:
                table_text = '\n'.join(current_lines)
                parsed = parse_md_table(table_text)
                if parsed:
                    tables.append(parsed)
                current_lines = []
                in_table = False
    # Flush last table
    if current_lines:
        table_text = '\n'.join(current_lines)
        parsed = parse_md_table(table_text)
        if parsed:
            tables.append(parsed)
    return tables


def extract_section(text: str, heading: str, level: int = 2) -> str:
    """Extract the text of a section by its heading (## or ###).

    Returns everything from the heading to the next heading of same or higher level.
    """
    prefix = '#' * level
    pattern = rf'^{prefix}\s+{re.escape(heading)}\s*$'
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        # Try fuzzy match
        pattern = rf'^{prefix}\s+.*{re.escape(heading)}.*$'
        match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
        if not match:
            return ""
    start = match.end()
    # Find next heading of same or higher level
    next_heading = re.search(rf'^#{{{1},{level}}}\s+', text[start:], re.MULTILINE)
    if next_heading:
        end = start + next_heading.start()
    else:
        end = len(text)
    return text[start:end].strip()


def extract_bullet_items(text: str, max_items: int = 20) -> list[str]:
    """Extract bullet list items from text."""
    items = []
    for match in re.finditer(r'^[\s]*[-•*]\s+(.+)$', text, re.MULTILINE):
        item = match.group(1).strip()
        if item:
            items.append(item)
        if len(items) >= max_items:
            break
    return items


def extract_number(text: str, pattern: str) -> Optional[float]:
    """Extract a numeric value near a pattern.

    Handles formats like €12.3B, 36.2%, +0.7%, 3,092M, etc.
    """
    match = re.search(
        rf'{re.escape(pattern)}[:\s]*[€$]?\s*([+\-]?[\d,]+\.?\d*)\s*([%BMKbmk]?)',
        text, re.IGNORECASE)
    if not match:
        return None
    num_str = match.group(1).replace(',', '')
    try:
        value = float(num_str)
    except ValueError:
        return None
    suffix = match.group(2).upper()
    if suffix == 'B':
        value *= 1000
    return value


def extract_metric_value(text: str, metric_name: str) -> Optional[str]:
    """Extract the value cell from a table row matching metric_name."""
    pattern = rf'\|\s*\*?\*?{re.escape(metric_name)}\*?\*?\s*\|\s*\*?\*?([^|]+?)\*?\*?\s*\|'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip().strip('*')
    return None


def parse_number(s: str) -> Optional[float]:
    """Parse a string like '€3,092M', '36.2%', '+0.7%', '12.3B' to float."""
    if not s:
        return None
    cleaned = re.sub(r'[€$,\s]', '', s)
    cleaned = cleaned.strip('*')
    match = re.match(r'^([+\-]?\d+\.?\d*)\s*(%|[BMKbmk])?', cleaned)
    if not match:
        return None
    try:
        value = float(match.group(1))
    except ValueError:
        return None
    suffix = (match.group(2) or '').upper()
    if suffix == 'B':
        value *= 1000
    elif suffix == 'K':
        value /= 1000
    return value


def extract_code_block(text: str) -> str:
    """Extract the first fenced code block content."""
    match = re.search(r'```[^\n]*\n(.*?)```', text, re.DOTALL)
    return match.group(1).strip() if match else ""
