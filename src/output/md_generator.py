"""BLM Strategic Insight Report — Markdown Generator (Orchestrator).

Transforms a FiveLooksResult into a comprehensive ~2,500-3,000 line
Markdown strategic analysis report matching the BLM benchmark structure.

Usage:
    from src.output.md_generator import BLMMdGenerator
    gen = BLMMdGenerator()
    md_text = gen.generate(result)                # returns string
    gen.generate(result, "report.md")             # writes to file
"""
from __future__ import annotations

import datetime
from pathlib import Path
from typing import Optional

from .md_utils import (
    section_header, section_divider, module_comment, blockquote,
    md_table, operator_display_name, market_display_name,
    safe_get,
)
from .strategic_diagnosis import StrategicDiagnosisComputer, StrategicDiagnosis


class BLMMdGenerator:
    """Orchestrates generation of a complete BLM Strategic Insight MD report."""

    def __init__(self, market_config=None):
        """Initialize the MD generator.

        Args:
            market_config: Optional MarketConfig. Auto-resolved from result.market
                           if omitted.
        """
        self._config = market_config

    def generate(self, result, output_path: str | None = None) -> str:
        """Generate the complete MD report.

        Args:
            result: FiveLooksResult from the analysis engine.
            output_path: If provided, write the report to this file path.

        Returns:
            The complete Markdown string (always). If output_path is given,
            also writes to file and returns the file path.
        """
        # 1. Resolve MarketConfig
        config = self._resolve_config(result)

        # 2. Compute strategic diagnosis
        computer = StrategicDiagnosisComputer(result, config)
        diagnosis = computer.compute()

        # 3. Build document
        sections = []
        sections.append(self._build_document_header(result, config))
        sections.append(self._build_toc(result))

        # 4. Render 8 modules
        from .md_modules import (
            render_executive_summary,
            render_trends,
            render_market_customer,
            render_tariff,
            render_competition,
            render_self_analysis,
            render_swot,
            render_opportunities,
            render_decisions,
        )

        module_renderers = [
            ("ES", "Executive Summary", render_executive_summary),
            ("01", "Look 1: Trends — PEST Analysis", render_trends),
            ("02", "Look 2: Market & Customer — $APPEALS", render_market_customer),
            ("02a", "Tariff Deep Analysis", render_tariff),
            ("03", "Look 3: Competition — Porter + Deep Dives", render_competition),
            ("04", "Look 4: Self — BMC + Capability", render_self_analysis),
            ("SW", "SWOT Synthesis", render_swot),
            ("05", "Look 5: Opportunities — SPAN Matrix", render_opportunities),
            ("06", "Three Decisions — Strategy & Execution", render_decisions),
        ]

        for mod_id, mod_title, renderer in module_renderers:
            sections.append(module_comment(mod_id, mod_title))
            try:
                content = renderer(result, diagnosis, config)
                if content:
                    sections.append(content)
            except Exception as e:
                sections.append(f"\n*Module {mod_id} ({mod_title}) generation failed: {e}*\n")

        # 5. Provenance footer
        sections.append(self._build_provenance_footer(result, config))

        # 6. Assemble
        md_content = "\n\n".join(s for s in sections if s)

        # 7. Write file or return string
        if output_path:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(md_content, encoding="utf-8")
            return md_content

        return md_content

    # ------------------------------------------------------------------
    # Document header
    # ------------------------------------------------------------------

    def _build_document_header(self, result, config) -> str:
        target_name = operator_display_name(result.target_operator)
        market_name = market_display_name(result.market) if result.market else "Market"
        period = result.analysis_period or "Unknown Period"
        now = datetime.datetime.now().strftime("%Y-%m-%d")

        lines = [
            f"# {target_name} — BLM Strategic Assessment: Complete Analysis",
            "",
            f"> **Period**: {period}",
            f"> **Framework**: Business Leadership Model (BLM) — Five Looks + SWOT + SPAN",
            f"> **Protagonist**: {target_name}",
            f"> **Market**: {market_name}",
            f"> **Generated**: {now}",
        ]

        # Add market structure if available from config
        if config:
            pop = safe_get(config, "population_k")
            if pop:
                lines.append(f"> **Population**: {pop/1000:.1f}M")

        lines.append("")
        lines.append("---")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Table of contents
    # ------------------------------------------------------------------

    def _build_toc(self, result) -> str:
        lines = [
            section_header("Document Structure", 2),
            "",
            "This document consolidates all deep analysis modules from the BLM "
            "strategic assessment into a single reference. It can be used as:",
            "- **Human reference**: Complete strategic analysis in one place",
            "- **AI agent input**: Feed this document to an AI agent to generate "
            "updated presentations, summaries, or derivative analyses",
            "",
        ]

        modules = [
            ("ES", "Executive Summary", "executive-summary"),
            ("01", "Look 1: Trends — PEST Analysis", "trends-pest-analysis"),
            ("02", "Look 2: Market & Customer — $APPEALS", "market-customer-appeals"),
            ("02a", "Tariff Deep Analysis", "tariff-deep-analysis"),
            ("03", "Look 3: Competition — Porter + Deep Dives", "competition-porter"),
            ("04", "Look 4: Self — BMC + Capability", "self-analysis-bmc"),
            ("SW", "SWOT Synthesis", "swot-synthesis"),
            ("05", "Look 5: Opportunities — SPAN Matrix", "opportunities-span-matrix"),
            ("06", "Three Decisions — Strategy & Execution", "three-decisions-strategy-execution"),
        ]

        rows = []
        for mod_id, mod_name, anchor in modules:
            # Skip tariff if no data
            if mod_id == "02a" and result.tariff_analysis is None:
                continue
            rows.append([mod_id, mod_name, f"[Link](#{anchor})"])

        lines.append(md_table(["#", "Module", "Section"], rows))
        lines.append("")
        lines.append("---")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Provenance footer
    # ------------------------------------------------------------------

    def _build_provenance_footer(self, result, config) -> str:
        lines = [
            "",
            "---",
            "",
        ]

        prov = result.provenance if hasattr(result, 'provenance') and result.provenance else None
        if prov:
            report = prov.quality_report()
            total = report.get("total_data_points", 0)
            high = report.get("high_confidence", 0)
            medium = report.get("medium_confidence", 0)
            low = report.get("low_confidence", 0) + report.get("estimated", 0)
            sources = report.get("unique_sources", 0)

            lines.append(section_header("Data Provenance", 2))
            lines.append("")
            lines.append(md_table(
                ["Metric", "Value"],
                [
                    ["Total data points", str(total)],
                    ["High confidence", str(high)],
                    ["Medium confidence", str(medium)],
                    ["Low/Estimated", str(low)],
                    ["Unique sources", str(sources)],
                ]
            ))

            footnotes = prov.to_footnotes()
            if footnotes:
                # Deduplicate sources
                unique_sources = list(dict.fromkeys(footnotes))
                lines.append("")
                lines.append("### Sources")
                lines.append("")
                for fn in unique_sources[:15]:
                    lines.append(f"- {fn}")

        lines.append("")
        lines.append("---")
        lines.append("")

        now = datetime.datetime.now().strftime("%Y-%m-%d")
        target_name = operator_display_name(result.target_operator)
        period = result.analysis_period or ""

        lines.append(f"*Generated: {now} | {target_name} BLM Strategic Assessment ({period})*")
        lines.append(f"*Framework: Business Leadership Model — Five Looks + SWOT + SPAN*")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Config resolution
    # ------------------------------------------------------------------

    def _resolve_config(self, result):
        """Resolve MarketConfig from explicit config, result.market, or None."""
        if self._config is not None:
            return self._config

        market_id = result.market if hasattr(result, "market") else None
        if not market_id:
            return None

        try:
            from src.models.market_configs import get_market_config
            return get_market_config(market_id)
        except Exception:
            return None
