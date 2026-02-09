"""HTML report generator for BLM Five Looks analysis results.

Produces a self-contained HTML file with embedded CSS, brand color variables
from PPTStyle, collapsible sections, and provenance tooltips.

Usage:
    from src.output.ppt_styles import get_style
    gen = BLMHtmlGenerator(get_style("vodafone"))
    path = gen.generate(result, "output/report.html")
"""

from __future__ import annotations

import html
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.output.ppt_styles import PPTStyle, DEFAULT_STYLE


def _rgb_css(rgb: tuple) -> str:
    """Convert (R, G, B) tuple to CSS rgb() string."""
    return f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"


def _esc(text) -> str:
    """HTML-escape text."""
    return html.escape(str(text)) if text else ""


class BLMHtmlGenerator:
    """Generate a self-contained HTML report from FiveLooksResult."""

    def __init__(self, style: Optional[PPTStyle] = None):
        self.style = style or DEFAULT_STYLE

    def generate(
        self,
        result,
        output_path: Optional[str] = None,
        include_charts: bool = False,
    ) -> str:
        """Generate the HTML report.

        Args:
            result: FiveLooksResult
            output_path: File path (returns HTML string if None)
            include_charts: Whether to embed chart images (requires BLMChartGenerator)

        Returns:
            Path to file or HTML string
        """
        html_content = self._build_html(result)

        if output_path:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(html_content, encoding='utf-8')
            return str(output_path)
        return html_content

    def _build_html(self, result) -> str:
        """Build the complete HTML document."""
        css = self._build_css()
        body = self._build_body(result)
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BLM Five Looks Analysis - {_esc(result.target_operator)}</title>
<style>{css}</style>
</head>
<body>
{body}
<script>
document.querySelectorAll('.section-toggle').forEach(btn => {{
    btn.addEventListener('click', () => {{
        const content = btn.nextElementSibling;
        content.style.display = content.style.display === 'none' ? 'block' : 'none';
        btn.textContent = btn.textContent.includes('+') ?
            btn.textContent.replace('+', '-') : btn.textContent.replace('-', '+');
    }});
}});
</script>
</body>
</html>"""

    def _build_css(self) -> str:
        primary = _rgb_css(self.style.primary_color)
        secondary = _rgb_css(self.style.secondary_color)
        text_color = _rgb_css(self.style.text_color)
        light_text = _rgb_css(self.style.light_text_color)
        positive = _rgb_css(self.style.positive_color)
        negative = _rgb_css(self.style.negative_color)
        warning = _rgb_css(self.style.warning_color)

        return f"""
:root {{
    --primary: {primary};
    --secondary: {secondary};
    --text: {text_color};
    --light-text: {light_text};
    --positive: {positive};
    --negative: {negative};
    --warning: {warning};
    --bg: #ffffff;
    --card-bg: #f8f9fa;
    --border: #e0e0e0;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: var(--text);
    background: var(--bg);
    line-height: 1.6;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}}
.header {{
    background: var(--primary);
    color: white;
    padding: 40px 30px;
    border-radius: 8px;
    margin-bottom: 30px;
}}
.header h1 {{ font-size: 28px; margin-bottom: 8px; }}
.header .meta {{ font-size: 14px; opacity: 0.9; }}
.section {{
    margin-bottom: 24px;
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
}}
.section-toggle {{
    display: block;
    width: 100%;
    padding: 16px 20px;
    background: var(--card-bg);
    border: none;
    font-size: 18px;
    font-weight: bold;
    color: var(--text);
    cursor: pointer;
    text-align: left;
    border-bottom: 3px solid var(--primary);
}}
.section-toggle:hover {{ background: #f0f0f0; }}
.section-content {{
    padding: 20px;
}}
.metric-cards {{
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin: 16px 0;
}}
.metric-card {{
    background: var(--card-bg);
    border-radius: 8px;
    padding: 16px;
    min-width: 180px;
    flex: 1;
}}
.metric-card .label {{ font-size: 12px; color: var(--light-text); }}
.metric-card .value {{ font-size: 24px; font-weight: bold; color: var(--primary); }}
.key-message {{
    background: var(--primary);
    color: white;
    padding: 12px 20px;
    border-radius: 6px;
    margin-top: 16px;
    font-weight: bold;
    font-size: 14px;
}}
.tracked {{
    border-bottom: 1px dotted var(--light-text);
    cursor: help;
    position: relative;
}}
.tracked:hover::after {{
    content: attr(data-source);
    position: absolute;
    bottom: 100%;
    left: 0;
    background: #333;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    white-space: nowrap;
    z-index: 10;
}}
ul {{ margin: 8px 0 8px 24px; }}
li {{ margin-bottom: 4px; }}
h3 {{ color: var(--primary); margin: 16px 0 8px; }}
.swot-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin: 16px 0;
}}
.swot-cell {{
    padding: 16px;
    border-radius: 8px;
    min-height: 120px;
}}
.swot-cell h4 {{ margin-bottom: 8px; color: white; }}
.swot-s {{ background: #4CAF50; color: white; }}
.swot-w {{ background: #F44336; color: white; }}
.swot-o {{ background: #2196F3; color: white; }}
.swot-t {{ background: #FF9800; color: white; }}
.priority-badge {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    color: white;
    font-size: 12px;
    font-weight: bold;
}}
.p0 {{ background: var(--primary); }}
.p1 {{ background: var(--warning); }}
.p2 {{ background: var(--positive); }}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
}}
th, td {{
    padding: 8px 12px;
    text-align: left;
    border-bottom: 1px solid var(--border);
}}
th {{ background: var(--card-bg); font-weight: bold; }}
.footer {{
    text-align: center;
    padding: 20px;
    color: var(--light-text);
    font-size: 12px;
    border-top: 1px solid var(--border);
    margin-top: 40px;
}}
@media (max-width: 768px) {{
    .metric-cards {{ flex-direction: column; }}
    .swot-grid {{ grid-template-columns: 1fr; }}
}}
"""

    def _build_body(self, result) -> str:
        """Build all HTML body sections."""
        parts = []
        parts.append(self._build_header(result))
        parts.append(self._build_exec_summary(result))
        parts.append(self._build_trends_section(result.trends))
        parts.append(self._build_market_section(result.market_customer))
        parts.append(self._build_competition_section(result.competition))
        parts.append(self._build_self_section(result.self_analysis))
        parts.append(self._build_swot_section(result.swot))
        parts.append(self._build_opportunities_section(result.opportunities))
        parts.append(self._build_provenance_section(result.provenance))
        parts.append(self._build_footer())
        return "\n".join(parts)

    def _build_header(self, result) -> str:
        return f"""<div class="header">
<h1>BLM Five Looks Strategic Analysis</h1>
<div class="meta">
    Target: {_esc(result.target_operator)} |
    Market: {_esc(result.market)} |
    Period: {_esc(result.analysis_period)} |
    Generated: {datetime.now().strftime('%Y-%m-%d')}
</div>
</div>"""

    def _build_exec_summary(self, result) -> str:
        items = [
            ("Trends", _get_km(result.trends)),
            ("Market/Customer", _get_km(result.market_customer)),
            ("Competition", _get_km(result.competition)),
            ("Self", _get_km(result.self_analysis)),
            ("SWOT", _get_km(result.swot)),
            ("Opportunities", _get_km(result.opportunities)),
        ]
        rows = ""
        for label, msg in items:
            rows += f"<tr><td><strong>{_esc(label)}</strong></td><td>{_esc(msg) or 'Pending'}</td></tr>\n"

        return f"""<div class="section">
<button class="section-toggle">[-] Executive Summary</button>
<div class="section-content">
<table>{rows}</table>
</div></div>"""

    def _build_trends_section(self, trends) -> str:
        if trends is None:
            return self._empty_section("01 Trends (PEST)")

        content = ""
        pest = getattr(trends, 'pest', None)
        if pest:
            for dim_name, factors in [
                ("Political", getattr(pest, 'political_factors', [])),
                ("Economic", getattr(pest, 'economic_factors', [])),
                ("Society", getattr(pest, 'society_factors', [])),
                ("Technology", getattr(pest, 'technology_factors', [])),
            ]:
                if factors:
                    content += f"<h3>{_esc(dim_name)}</h3><ul>"
                    for f in factors[:5]:
                        name = f.factor_name if hasattr(f, 'factor_name') else str(f)
                        impact = getattr(f, 'impact_type', 'neutral')
                        icon = {"opportunity": "\u25B2", "threat": "\u25BC",
                                "both": "\u25C6"}.get(impact, "\u25CF")
                        content += f"<li>{icon} {_esc(name)}</li>"
                    content += "</ul>"

        # Industry environment
        env_items = []
        for attr, label in [
            ('industry_market_size', 'Market Size'),
            ('industry_growth_rate', 'Growth Rate'),
            ('industry_lifecycle_stage', 'Lifecycle'),
        ]:
            val = getattr(trends, attr, '')
            if val:
                env_items.append(f"{label}: {val}")
        if env_items:
            content += "<h3>Industry Environment</h3><ul>"
            content += "".join(f"<li>{_esc(i)}</li>" for i in env_items)
            content += "</ul>"

        km = getattr(trends, 'key_message', '')
        return self._wrap_section("01 Trends (PEST)", content, km)

    def _build_market_section(self, mci) -> str:
        if mci is None:
            return self._empty_section("02 Market/Customer ($APPEALS)")

        content = ""
        # Snapshot
        snapshot = mci.market_snapshot or {}
        if snapshot:
            cards = ""
            for k, v in list(snapshot.items())[:4]:
                label = k.replace('_', ' ').title()
                cards += f'<div class="metric-card"><div class="label">{_esc(label)}</div><div class="value">{_esc(str(v))}</div></div>'
            content += f'<div class="metric-cards">{cards}</div>'

        # Changes
        changes = mci.changes or []
        if changes:
            content += "<h3>Market Changes</h3><ul>"
            for c in changes[:6]:
                desc = c.description if hasattr(c, 'description') else str(c)
                content += f"<li>{_esc(desc)}</li>"
            content += "</ul>"

        # APPEALS
        appeals = mci.appeals_assessment or []
        if appeals:
            content += "<h3>$APPEALS Assessment</h3><table><tr><th>Dimension</th><th>Our Score</th><th>Priority</th></tr>"
            for a in appeals:
                dim = a.dimension_name if hasattr(a, 'dimension_name') else str(a)
                score = getattr(a, 'our_score', 0)
                priority = getattr(a, 'customer_priority', '')
                content += f"<tr><td>{_esc(dim)}</td><td>{score:.1f}/5</td><td>{_esc(priority)}</td></tr>"
            content += "</table>"

        km = getattr(mci, 'key_message', '')
        return self._wrap_section("02 Market/Customer ($APPEALS)", content, km)

    def _build_competition_section(self, comp) -> str:
        if comp is None:
            return self._empty_section("03 Competition (Porter)")

        content = ""
        # Five forces
        forces = comp.five_forces if hasattr(comp, 'five_forces') else {}
        if forces:
            content += "<h3>Five Forces</h3><table><tr><th>Force</th><th>Level</th></tr>"
            for name, force in forces.items():
                level = force.force_level if hasattr(force, 'force_level') else str(force)
                content += f"<tr><td>{_esc(name)}</td><td>{_esc(level)}</td></tr>"
            content += "</table>"

        # Competitor analyses
        analyses = comp.competitor_analyses if hasattr(comp, 'competitor_analyses') else {}
        for op_id, dd in list(analyses.items())[:3]:
            content += f"<h3>{_esc(op_id)}</h3>"
            strengths = getattr(dd, 'strengths', [])
            weaknesses = getattr(dd, 'weaknesses', [])
            if strengths:
                content += "<strong>Strengths:</strong><ul>"
                content += "".join(f"<li>{_esc(s)}</li>" for s in strengths[:4])
                content += "</ul>"
            if weaknesses:
                content += "<strong>Weaknesses:</strong><ul>"
                content += "".join(f"<li>{_esc(w)}</li>" for w in weaknesses[:4])
                content += "</ul>"

        km = getattr(comp, 'key_message', '')
        return self._wrap_section("03 Competition (Porter)", content, km)

    def _build_self_section(self, self_analysis) -> str:
        if self_analysis is None:
            return self._empty_section("04 Self (BMC + Capability)")

        content = ""
        rating = getattr(self_analysis, 'health_rating', '')
        if rating:
            content += f'<h3>Health Rating: <span style="color: var(--primary)">{_esc(rating.upper())}</span></h3>'

        # Financial health
        fh = self_analysis.financial_health or {}
        if fh:
            cards = ""
            for k, v in list(fh.items())[:4]:
                label = k.replace('_', ' ').title()
                cards += f'<div class="metric-card"><div class="label">{_esc(label)}</div><div class="value">{_esc(str(v))}</div></div>'
            content += f'<div class="metric-cards">{cards}</div>'

        # Segments
        segments = self_analysis.segment_analyses or []
        if segments:
            content += "<h3>Business Segments</h3><table><tr><th>Segment</th><th>Health</th></tr>"
            for seg in segments[:4]:
                content += f"<tr><td>{_esc(seg.segment_name)}</td><td>{_esc(getattr(seg, 'health_status', ''))}</td></tr>"
            content += "</table>"

        # Strengths/Weaknesses
        for label, items, css in [
            ("Strengths", getattr(self_analysis, 'strengths', []), "positive"),
            ("Weaknesses", getattr(self_analysis, 'weaknesses', []), "negative"),
        ]:
            if items:
                content += f'<h3 style="color: var(--{css})">{label}</h3><ul>'
                content += "".join(f"<li>{_esc(i)}</li>" for i in items[:5])
                content += "</ul>"

        km = getattr(self_analysis, 'key_message', '')
        return self._wrap_section("04 Self (BMC + Capability)", content, km)

    def _build_swot_section(self, swot) -> str:
        if swot is None:
            return self._empty_section("SWOT Synthesis")

        grid = '<div class="swot-grid">'
        for css_class, label, items in [
            ("swot-s", "Strengths", getattr(swot, 'strengths', [])),
            ("swot-w", "Weaknesses", getattr(swot, 'weaknesses', [])),
            ("swot-o", "Opportunities", getattr(swot, 'opportunities', [])),
            ("swot-t", "Threats", getattr(swot, 'threats', [])),
        ]:
            grid += f'<div class="swot-cell {css_class}"><h4>{label}</h4><ul>'
            grid += "".join(f"<li>{_esc(i)}</li>" for i in items[:5])
            grid += "</ul></div>"
        grid += "</div>"

        # Strategies
        strategies = ""
        for label, items in [
            ("SO Strategies", getattr(swot, 'so_strategies', [])),
            ("WO Strategies", getattr(swot, 'wo_strategies', [])),
            ("ST Strategies", getattr(swot, 'st_strategies', [])),
            ("WT Strategies", getattr(swot, 'wt_strategies', [])),
        ]:
            if items:
                strategies += f"<h3>{label}</h3><ul>"
                strategies += "".join(f"<li>{_esc(i)}</li>" for i in items[:3])
                strategies += "</ul>"

        km = getattr(swot, 'key_message', '')
        return self._wrap_section("SWOT Synthesis", grid + strategies, km)

    def _build_opportunities_section(self, opp) -> str:
        if opp is None:
            return self._empty_section("05 Opportunities (SPAN)")

        content = ""
        # SPAN positions
        positions = getattr(opp, 'span_positions', [])
        if positions:
            content += "<h3>SPAN Matrix Positions</h3>"
            content += "<table><tr><th>Opportunity</th><th>Attractiveness</th><th>Position</th><th>Quadrant</th></tr>"
            for p in positions[:8]:
                name = p.opportunity_name if hasattr(p, 'opportunity_name') else str(p)
                ma = getattr(p, 'market_attractiveness', 0)
                cp = getattr(p, 'competitive_position', 0)
                q = getattr(p, 'quadrant', '')
                content += f"<tr><td>{_esc(name)}</td><td>{ma:.1f}</td><td>{cp:.1f}</td><td>{_esc(q)}</td></tr>"
            content += "</table>"

        # Opportunities list
        opps = getattr(opp, 'opportunities', [])
        if opps:
            content += "<h3>Prioritized Opportunities</h3>"
            for o in opps[:6]:
                name = o.name if hasattr(o, 'name') else str(o)
                priority = getattr(o, 'priority', 'P1')
                desc = getattr(o, 'description', '')
                market = getattr(o, 'addressable_market', 'N/A')
                badge_class = priority.lower()
                content += f'<div style="margin: 8px 0; padding: 12px; background: var(--card-bg); border-radius: 6px;">'
                content += f'<span class="priority-badge {badge_class}">{_esc(priority)}</span> '
                content += f'<strong>{_esc(name)}</strong> (Market: {_esc(market)})'
                if desc:
                    content += f'<br><small>{_esc(desc)}</small>'
                content += '</div>'

        km = getattr(opp, 'key_message', '')
        return self._wrap_section("05 Opportunities (SPAN)", content, km)

    def _build_provenance_section(self, prov) -> str:
        if prov is None:
            return self._empty_section("Data Provenance")

        report = prov.quality_report()
        cards = ""
        for label, key in [
            ("Total Points", "total_data_points"),
            ("High Confidence", "high_confidence"),
            ("Medium", "medium_confidence"),
            ("Sources", "unique_sources"),
        ]:
            val = report.get(key, 0)
            cards += f'<div class="metric-card"><div class="label">{label}</div><div class="value">{val}</div></div>'

        content = f'<div class="metric-cards">{cards}</div>'

        footnotes = prov.to_footnotes()
        if footnotes:
            content += "<h3>Source Citations</h3><ul>"
            content += "".join(f"<li>{_esc(fn)}</li>" for fn in footnotes[:15])
            content += "</ul>"

        return self._wrap_section("Data Provenance", content, "")

    def _build_footer(self) -> str:
        return f'<div class="footer">Generated by BLM Analysis Engine | {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>'

    # --- Helpers ---

    def _wrap_section(self, title: str, content: str, key_message: str) -> str:
        km_html = ""
        if key_message:
            km_html = f'<div class="key-message">Key Message: {_esc(key_message)}</div>'
        return f"""<div class="section">
<button class="section-toggle">[-] {_esc(title)}</button>
<div class="section-content">
{content}
{km_html}
</div></div>"""

    def _empty_section(self, title: str) -> str:
        return self._wrap_section(title, "<p>No data available for this section.</p>", "")


def _get_km(obj) -> str:
    if obj is None:
        return ""
    return getattr(obj, 'key_message', '') or ""
