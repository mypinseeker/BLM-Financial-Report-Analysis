"""TXT formatter for BLM Five Looks analysis results.

Produces a terminal-readable plain text report using box-drawing characters
and structured sections. Each section ends with a key message line.

Usage:
    formatter = BLMTxtFormatter()
    text = formatter.format(result)
"""

from __future__ import annotations

from typing import Optional


# Box-drawing characters
BOX_H = "\u2500"   # ─
BOX_V = "\u2502"   # │
BOX_TL = "\u250C"  # ┌
BOX_TR = "\u2510"  # ┐
BOX_BL = "\u2514"  # └
BOX_BR = "\u2518"  # ┘
BOX_T = "\u252C"   # ┬
BOX_B = "\u2534"   # ┴
ARROW = "\u2192"    # →


class BLMTxtFormatter:
    """Format FiveLooksResult as plain text for terminal display."""

    def __init__(self, width: int = 80):
        self.width = width

    def format(self, result) -> str:
        """Format the complete analysis result.

        Args:
            result: FiveLooksResult from the analysis engine

        Returns:
            Formatted plain text string
        """
        sections = []
        sections.append(self._format_header(result))
        sections.append(self._format_trends(result.trends))
        sections.append(self._format_market_customer(result.market_customer))
        sections.append(self._format_competition(result.competition))
        sections.append(self._format_self(result.self_analysis))
        sections.append(self._format_swot(result.swot))
        sections.append(self._format_opportunities(result.opportunities))
        sections.append(self._format_provenance(result.provenance))
        return "\n".join(sections)

    # --- Section formatters ---

    def _format_header(self, result) -> str:
        lines = []
        lines.append(self._box_line())
        lines.append(self._center("BLM Five Looks Strategic Analysis"))
        lines.append(self._center(f"Target: {result.target_operator}"))
        lines.append(self._center(f"Market: {result.market} | Period: {result.analysis_period}"))
        lines.append(self._box_line())
        return "\n".join(lines)

    def _format_trends(self, trends) -> str:
        lines = []
        lines.append(self._section_header("01 TRENDS (PEST Framework)"))
        if trends is None:
            lines.append("  No trend analysis available.")
            return "\n".join(lines)

        pest = getattr(trends, 'pest', None)
        if pest:
            for dim_name, factors in [
                ("Political", getattr(pest, 'political_factors', [])),
                ("Economic", getattr(pest, 'economic_factors', [])),
                ("Society", getattr(pest, 'society_factors', [])),
                ("Technology", getattr(pest, 'technology_factors', [])),
            ]:
                if factors:
                    lines.append(f"  [{dim_name}]")
                    for f in factors[:4]:
                        name = f.factor_name if hasattr(f, 'factor_name') else str(f)
                        impact = getattr(f, 'impact_type', 'neutral')
                        icon = self._impact_icon(impact)
                        lines.append(f"    {icon} {name}")

        if trends.industry_lifecycle_stage:
            lines.append(f"  Industry Lifecycle: {trends.industry_lifecycle_stage}")
        if trends.industry_growth_rate:
            lines.append(f"  Growth Rate: {trends.industry_growth_rate}")

        lines.append(self._key_message(getattr(trends, 'key_message', '')))
        return "\n".join(lines)

    def _format_market_customer(self, mci) -> str:
        lines = []
        lines.append(self._section_header("02 MARKET/CUSTOMER ($APPEALS)"))
        if mci is None:
            lines.append("  No market analysis available.")
            return "\n".join(lines)

        # Snapshot
        snapshot = mci.market_snapshot or {}
        if snapshot:
            lines.append("  [Market Snapshot]")
            for k, v in list(snapshot.items())[:5]:
                lines.append(f"    {k}: {v}")

        # Changes
        changes = mci.changes or []
        if changes:
            lines.append("  [Market Changes]")
            for c in changes[:5]:
                desc = c.description if hasattr(c, 'description') else str(c)
                impact = getattr(c, 'impact_type', 'neutral')
                lines.append(f"    {self._impact_icon(impact)} {desc}")

        # Segments
        segs = mci.customer_segments or []
        if segs:
            lines.append("  [Customer Segments]")
            for s in segs[:4]:
                name = s.segment_name if hasattr(s, 'segment_name') else str(s)
                trend = getattr(s, 'growth_trend', '')
                lines.append(f"    {name} ({trend})")

        # APPEALS
        appeals = mci.appeals_assessment or []
        if appeals:
            lines.append("  [$APPEALS Scores]")
            for a in appeals:
                dim = a.dimension_name if hasattr(a, 'dimension_name') else str(a)
                score = getattr(a, 'our_score', 0)
                bar = self._score_bar(score, 5)
                lines.append(f"    {dim:20s} {bar} {score:.1f}/5")

        lines.append(self._key_message(getattr(mci, 'key_message', '')))
        return "\n".join(lines)

    def _format_competition(self, comp) -> str:
        lines = []
        lines.append(self._section_header("03 COMPETITION (Porter's Five Forces)"))
        if comp is None:
            lines.append("  No competition analysis available.")
            return "\n".join(lines)

        # Five forces
        forces = comp.five_forces if hasattr(comp, 'five_forces') else {}
        if forces:
            lines.append("  [Five Forces]")
            for name, force in forces.items():
                level = force.force_level if hasattr(force, 'force_level') else str(force)
                indicator = {"high": "!!!", "medium": "!!", "low": "!"}.get(level, "?")
                lines.append(f"    {name:25s} [{indicator}] {level}")

        intensity = getattr(comp, 'overall_competition_intensity', '')
        if intensity:
            lines.append(f"  Overall Intensity: {intensity.upper()}")

        # Competitor analyses
        analyses = comp.competitor_analyses if hasattr(comp, 'competitor_analyses') else {}
        for op_id, dd in list(analyses.items())[:3]:
            lines.append(f"  [{op_id}]")
            strengths = getattr(dd, 'strengths', [])
            weaknesses = getattr(dd, 'weaknesses', [])
            if strengths:
                lines.append(f"    Strengths: {', '.join(strengths[:3])}")
            if weaknesses:
                lines.append(f"    Weaknesses: {', '.join(weaknesses[:3])}")

        lines.append(self._key_message(getattr(comp, 'key_message', '')))
        return "\n".join(lines)

    def _format_self(self, self_analysis) -> str:
        lines = []
        lines.append(self._section_header("04 SELF (BMC + Capability)"))
        if self_analysis is None:
            lines.append("  No self analysis available.")
            return "\n".join(lines)

        # Health rating
        rating = getattr(self_analysis, 'health_rating', '')
        if rating:
            lines.append(f"  Health Rating: {rating.upper()}")

        # Financial health
        fh = self_analysis.financial_health or {}
        if fh:
            lines.append("  [Financial Health]")
            for k, v in list(fh.items())[:5]:
                lines.append(f"    {k}: {v}")

        # Segments
        segments = self_analysis.segment_analyses or []
        if segments:
            lines.append("  [Business Segments]")
            for seg in segments[:4]:
                name = seg.segment_name
                health = getattr(seg, 'health_status', '')
                lines.append(f"    {name:20s} [{health}]")

        # Strengths/Weaknesses
        strengths = getattr(self_analysis, 'strengths', [])
        weaknesses = getattr(self_analysis, 'weaknesses', [])
        if strengths:
            lines.append("  [Strengths]")
            for s in strengths[:5]:
                lines.append(f"    + {s}")
        if weaknesses:
            lines.append("  [Weaknesses]")
            for w in weaknesses[:5]:
                lines.append(f"    - {w}")

        lines.append(self._key_message(getattr(self_analysis, 'key_message', '')))
        return "\n".join(lines)

    def _format_swot(self, swot) -> str:
        lines = []
        lines.append(self._section_header("SWOT SYNTHESIS"))
        if swot is None:
            lines.append("  No SWOT analysis available.")
            return "\n".join(lines)

        quadrants = [
            ("Strengths", getattr(swot, 'strengths', []), "+"),
            ("Weaknesses", getattr(swot, 'weaknesses', []), "-"),
            ("Opportunities", getattr(swot, 'opportunities', []), "^"),
            ("Threats", getattr(swot, 'threats', []), "v"),
        ]
        for label, items, icon in quadrants:
            lines.append(f"  [{label}]")
            for item in items[:5]:
                lines.append(f"    {icon} {item}")

        # Strategies
        strategy_quadrants = [
            ("SO Strategies", getattr(swot, 'so_strategies', [])),
            ("WO Strategies", getattr(swot, 'wo_strategies', [])),
            ("ST Strategies", getattr(swot, 'st_strategies', [])),
            ("WT Strategies", getattr(swot, 'wt_strategies', [])),
        ]
        for label, items in strategy_quadrants:
            if items:
                lines.append(f"  [{label}]")
                for item in items[:3]:
                    lines.append(f"    {ARROW} {item}")

        lines.append(self._key_message(getattr(swot, 'key_message', '')))
        return "\n".join(lines)

    def _format_opportunities(self, opp) -> str:
        lines = []
        lines.append(self._section_header("05 OPPORTUNITIES (SPAN Matrix)"))
        if opp is None:
            lines.append("  No opportunity analysis available.")
            return "\n".join(lines)

        # SPAN positions
        positions = getattr(opp, 'span_positions', [])
        if positions:
            lines.append("  [SPAN Positions]")
            lines.append(f"    {'Name':25s} {'Attractiveness':>14s} {'Position':>10s} {'Quadrant':>15s}")
            lines.append(f"    {BOX_H * 70}")
            for p in positions[:8]:
                name = p.opportunity_name if hasattr(p, 'opportunity_name') else str(p)
                ma = getattr(p, 'market_attractiveness', 0)
                cp = getattr(p, 'competitive_position', 0)
                q = getattr(p, 'quadrant', '')
                lines.append(f"    {name:25s} {ma:>14.1f} {cp:>10.1f} {q:>15s}")

        # Grouped quadrants
        for q_label, q_attr in [
            ("Grow/Invest", "grow_invest"),
            ("Acquire Skills", "acquire_skills"),
            ("Harvest", "harvest"),
            ("Avoid/Exit", "avoid_exit"),
        ]:
            items = getattr(opp, q_attr, [])
            if items:
                lines.append(f"  [{q_label}]")
                for item in items[:4]:
                    lines.append(f"    {ARROW} {item}")

        # Priority list
        opps = getattr(opp, 'opportunities', [])
        if opps:
            lines.append("  [Priority Ranking]")
            for o in opps[:6]:
                name = o.name if hasattr(o, 'name') else str(o)
                priority = getattr(o, 'priority', 'P1')
                market = getattr(o, 'addressable_market', 'N/A')
                lines.append(f"    [{priority}] {name} (Market: {market})")

        lines.append(self._key_message(getattr(opp, 'key_message', '')))
        return "\n".join(lines)

    def _format_provenance(self, prov) -> str:
        lines = []
        lines.append(self._section_header("DATA PROVENANCE"))
        if prov is None:
            lines.append("  No provenance data.")
            return "\n".join(lines)

        report = prov.quality_report()
        lines.append(f"  Total data points: {report.get('total_data_points', 0)}")
        lines.append(f"  High confidence: {report.get('high_confidence', 0)}")
        lines.append(f"  Medium confidence: {report.get('medium_confidence', 0)}")
        lines.append(f"  Low/Estimated: {report.get('low_confidence', 0) + report.get('estimated', 0)}")
        lines.append(f"  Unique sources: {report.get('unique_sources', 0)}")

        footnotes = prov.to_footnotes()
        if footnotes:
            lines.append("")
            lines.append("  [Sources]")
            for fn in footnotes[:10]:
                lines.append(f"    {fn}")

        lines.append(self._box_line())
        return "\n".join(lines)

    # --- Utility methods ---

    def _section_header(self, title: str) -> str:
        return f"\n{BOX_TL}{BOX_H * (self.width - 2)}{BOX_TR}\n{BOX_V} {title}{' ' * (self.width - len(title) - 4)}{BOX_V}\n{BOX_BL}{BOX_H * (self.width - 2)}{BOX_BR}"

    def _box_line(self) -> str:
        return BOX_H * self.width

    def _center(self, text: str) -> str:
        return text.center(self.width)

    def _key_message(self, msg: str) -> str:
        if not msg:
            return ""
        return f"\n  {ARROW} Key Message: {msg}"

    def _impact_icon(self, impact: str) -> str:
        icons = {
            'opportunity': '\u25B2',  # ▲
            'threat': '\u25BC',        # ▼
            'neutral': '\u25CF',       # ●
            'both': '\u25C6',          # ◆
        }
        return icons.get(impact, '\u25CF')

    def _score_bar(self, score: float, max_score: float) -> str:
        """Create a text-based progress bar."""
        filled = int(score / max_score * 10)
        return f"[{'#' * filled}{'.' * (10 - filled)}]"
