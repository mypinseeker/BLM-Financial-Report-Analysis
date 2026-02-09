"""BLM PPT Generator — transforms FiveLooksResult into a branded PowerPoint deck.

Generates 35-42 slides (Draft) or 20-25 (Final mode with user_decisions filter).
Every content slide ends with a Key Message bar at the bottom.

Usage:
    from src.output.ppt_styles import get_style
    from src.output.ppt_generator import BLMPPTGenerator

    style = get_style("vodafone")
    gen = BLMPPTGenerator(style=style, operator_id="vodafone_germany")
    ppt_path = gen.generate(five_looks_result, mode="draft")
"""

from __future__ import annotations

import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.shapes import MSO_SHAPE
    PPTX_AVAILABLE = True
except ImportError:
    PPTX_AVAILABLE = False

from src.output.ppt_styles import PPTStyle, get_style, DEFAULT_STYLE
from src.output.ppt_charts import BLMChartGenerator


@dataclass
class SlideSpec:
    """Specification for a slide in the deck."""
    slide_id: str
    title: str
    section: str = ""
    required: bool = True  # False = optional deep-dive slide


class BLMPPTGenerator:
    """Generate PowerPoint presentations from FiveLooksResult.

    Takes a FiveLooksResult and PPTStyle, produces a branded 16:9 deck
    with ~38 slides (Draft) or a filtered subset (Final).
    """

    # Slide dimensions: 16:9 widescreen
    SLIDE_WIDTH = 13.333
    SLIDE_HEIGHT = 7.5

    # Key message bar position
    KM_LEFT = 0.5
    KM_TOP = 6.3
    KM_WIDTH = 12.333
    KM_HEIGHT = 0.75

    def __init__(
        self,
        style: Optional[PPTStyle] = None,
        operator_id: str = "",
        output_dir: Optional[str] = None,
        chart_dpi: int = 150,
    ):
        if not PPTX_AVAILABLE:
            raise ImportError(
                "python-pptx is required for PPT generation. "
                "Install it with: pip install python-pptx"
            )
        self.style = style or DEFAULT_STYLE
        self.operator_id = operator_id
        self.output_dir = Path(output_dir) if output_dir else Path(
            tempfile.mkdtemp())
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self._chart_dir = Path(tempfile.mkdtemp())
        self.chart_gen = BLMChartGenerator(
            style=self.style, output_dir=str(self._chart_dir), dpi=chart_dpi)

        self.prs = None
        self.slide_num = 0
        self._slide_specs: list[SlideSpec] = []

    # =========================================================================
    # Public API
    # =========================================================================

    def generate(
        self,
        result,
        mode: str = "draft",
        user_decisions: Optional[dict] = None,
        filename: Optional[str] = None,
    ) -> str:
        """Generate the PPT deck.

        Args:
            result: FiveLooksResult from the analysis engine
            mode: "draft" (full ~38 slides) or "final" (filtered by user_decisions)
            user_decisions: dict mapping slide_id -> "keep"/"remove"/"merge"
            filename: Output filename (auto-generated if None)

        Returns:
            Path to generated .pptx file
        """
        self.prs = Presentation()
        self.prs.slide_width = Inches(self.SLIDE_WIDTH)
        self.prs.slide_height = Inches(self.SLIDE_HEIGHT)
        self.slide_num = 0
        self._slide_specs = []

        # Build all slides
        self._build_all_slides(result)

        # In final mode, remove slides the user declined
        if mode == "final" and user_decisions:
            self._apply_user_decisions(user_decisions)

        # Save
        if filename is None:
            safe_name = self._sanitize_name(result.target_operator)
            filename = f"blm_{safe_name}_{mode}.pptx"
        output_path = self.output_dir / filename
        self.prs.save(str(output_path))
        return str(output_path)

    # =========================================================================
    # Slide orchestration
    # =========================================================================

    def _build_all_slides(self, result):
        """Build the complete slide deck."""
        # S01 Cover
        self._add_cover_slide(result)
        # S02 TOC
        self._add_toc_slide(result)
        # S03 Data Quality
        self._add_data_quality_slide(result)
        # S04 Executive Summary
        self._add_executive_summary(result)

        # --- Look 1: Trends ---
        self._add_section_divider("01 看趋势", "Look at Trends — PEST Framework")
        self._add_pest_dashboard(result.trends)
        self._add_industry_environment(result.trends)
        self._add_trend_deep_dive(result.trends)

        # --- Look 2: Market/Customer ---
        self._add_section_divider("02 看市场/客户", "Look at Market/Customer — $APPEALS")
        self._add_market_change_panorama(result.market_customer)
        self._add_customer_segments(result.market_customer)
        self._add_appeals_assessment(result.market_customer)
        self._add_market_deep_dive(result.market_customer)

        # --- Look 3: Competition ---
        self._add_section_divider("03 看竞争", "Look at Competition — Porter's Five Forces")
        self._add_five_forces(result.competition)
        self._add_competitor_deep_dives(result.competition)
        self._add_competition_summary(result.competition)
        self._add_new_entrants(result.competition)

        # --- Look 4: Self ---
        self._add_section_divider("04 看自己", "Look at Self — BMC + Capability")
        self._add_health_check(result.self_analysis)
        self._add_segment_deep_dives(result.self_analysis)
        self._add_network_analysis(result.self_analysis)
        self._add_bmc_canvas(result.self_analysis)
        self._add_org_talent(result.self_analysis)
        self._add_strengths_weaknesses_exposure(result.self_analysis)

        # --- SWOT ---
        self._add_section_divider("SWOT 综合分析", "SWOT Synthesis")
        self._add_swot_matrix(result.swot)

        # --- Look 5: Opportunities ---
        self._add_section_divider("05 看机会", "Look at Opportunities — SPAN Matrix")
        self._add_span_bubble(result.opportunities)
        self._add_priority_table(result.opportunities)
        self._add_opportunity_deep_dive(result.opportunities)

        # --- Summary ---
        self._add_summary_slide(result)
        self._add_provenance_appendix(result)
        self._add_back_cover()

    def _apply_user_decisions(self, decisions: dict):
        """Remove slides that the user marked as 'remove' in Final mode."""
        indices_to_remove = []
        for i, spec in enumerate(self._slide_specs):
            action = decisions.get(spec.slide_id, "keep")
            if action == "remove":
                indices_to_remove.append(i)

        # Remove in reverse order to preserve indices
        for idx in reversed(indices_to_remove):
            xml_slides = self.prs.slides._sldIdLst
            slides_list = list(xml_slides)
            if idx < len(slides_list):
                xml_slides.remove(slides_list[idx])

    # =========================================================================
    # Utility methods
    # =========================================================================

    def _new_slide(self, slide_id: str = "", title: str = "",
                   section: str = "", required: bool = True):
        """Add a blank slide and register its spec."""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])  # Blank
        self.slide_num += 1
        spec = SlideSpec(
            slide_id=slide_id or f"S{self.slide_num:02d}",
            title=title, section=section, required=required)
        self._slide_specs.append(spec)
        return slide

    def _add_header(self, slide, title: str, subtitle: str = ""):
        """Standard slide header with accent bar."""
        # Top accent bar
        self._add_shape(slide, 0, 0, Inches(self.SLIDE_WIDTH), Inches(0.08),
                        self.style.primary_color)
        # Title
        self._add_text_box(slide, Inches(0.5), Inches(0.25), Inches(10), Inches(0.6),
                           title, font_size=self.style.subtitle_size,
                           font_color=self.style.text_color, bold=True)
        if subtitle:
            self._add_text_box(slide, Inches(0.5), Inches(0.85), Inches(10), Inches(0.35),
                               subtitle, font_size=12,
                               font_color=self.style.primary_color, bold=True)
        # Page number
        self._add_text_box(slide, Inches(12.3), Inches(7.0), Inches(0.8), Inches(0.35),
                           str(self.slide_num), font_size=10,
                           font_color=self.style.light_text_color, align="right")

    def _add_key_message_bar(self, slide, message: str):
        """Add Key Message bar at the bottom of a content slide."""
        if not message:
            return
        shape = self._add_shape(
            slide, Inches(self.KM_LEFT), Inches(self.KM_TOP),
            Inches(self.KM_WIDTH), Inches(self.KM_HEIGHT),
            self.style.key_message_bg)

        txBox = slide.shapes.add_textbox(
            Inches(self.KM_LEFT + 0.15), Inches(self.KM_TOP + 0.1),
            Inches(self.KM_WIDTH - 0.3), Inches(self.KM_HEIGHT - 0.2))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"Key Message: {message}"
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(*self.style.key_message_text)
        p.font.bold = True
        p.font.name = self.style.body_font
        p.alignment = PP_ALIGN.LEFT

    def _add_shape(self, slide, left, top, width, height, fill_color,
                   shape_type=None):
        """Add a colored shape."""
        if shape_type is None:
            shape_type = MSO_SHAPE.RECTANGLE
        shape = slide.shapes.add_shape(shape_type, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*fill_color)
        shape.line.fill.background()
        return shape

    def _add_text_box(self, slide, left, top, width, height, text: str,
                      font_size: int = 14, font_color: tuple = (0, 0, 0),
                      bold: bool = False, align: str = "left"):
        """Add a text box."""
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = str(text)
        p.font.size = Pt(font_size)
        p.font.color.rgb = RGBColor(*font_color)
        p.font.bold = bold
        p.font.name = self.style.body_font
        if align == "center":
            p.alignment = PP_ALIGN.CENTER
        elif align == "right":
            p.alignment = PP_ALIGN.RIGHT
        else:
            p.alignment = PP_ALIGN.LEFT
        return txBox

    def _add_bullet_list(self, slide, left, top, width, height,
                         items: list, font_size: int = 12,
                         font_color: tuple = None, max_items: int = 8):
        """Add a bulleted list text box."""
        if font_color is None:
            font_color = self.style.text_color
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True
        for i, item in enumerate(items[:max_items]):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = f"• {item}"
            p.font.size = Pt(font_size)
            p.font.color.rgb = RGBColor(*font_color)
            p.font.name = self.style.body_font
            p.space_after = Pt(4)
        return txBox

    def _add_image(self, slide, image_path: str, left, top, width, height=None):
        """Add an image to the slide."""
        if height:
            slide.shapes.add_picture(image_path, left, top, width, height)
        else:
            slide.shapes.add_picture(image_path, left, top, width)

    def _add_metric_cards(self, slide, metrics: list[tuple], top, left_start=0.5,
                          card_width=2.8, card_height=1.2, gap=0.2):
        """Add a row of metric cards (label, value, change_indicator)."""
        x = Inches(left_start)
        for label, value, change in metrics:
            self._add_shape(slide, x, Inches(top), Inches(card_width),
                            Inches(card_height), (245, 245, 245))
            self._add_text_box(slide, x + Inches(0.15), Inches(top + 0.1),
                               Inches(card_width - 0.3), Inches(0.35),
                               label, font_size=10,
                               font_color=self.style.light_text_color)
            self._add_text_box(slide, x + Inches(0.15), Inches(top + 0.45),
                               Inches(card_width - 0.3), Inches(0.4),
                               str(value), font_size=18,
                               font_color=self.style.primary_color, bold=True)
            if change:
                is_positive = str(change).startswith('+') or (
                    isinstance(change, (int, float)) and change > 0)
                change_color = self.style.positive_color if is_positive else self.style.negative_color
                self._add_text_box(slide, x + Inches(0.15), Inches(top + 0.85),
                                   Inches(card_width - 0.3), Inches(0.25),
                                   str(change), font_size=10,
                                   font_color=change_color)
            x += Inches(card_width + gap)

    def _sanitize_name(self, name: str) -> str:
        return name.lower().replace(" ", "_").replace("/", "_").replace("&", "and")

    # =========================================================================
    # S01: Cover Slide
    # =========================================================================

    def _add_cover_slide(self, result):
        slide = self._new_slide("cover", "Cover")

        # Brand header bar
        self._add_shape(slide, 0, 0, Inches(self.SLIDE_WIDTH), Inches(2.8),
                        self.style.primary_color)

        # Title
        title_text = f"{self.style.display_name} BLM Strategic Analysis"
        self._add_text_box(slide, Inches(0.5), Inches(0.5), Inches(9), Inches(1.2),
                           title_text, font_size=self.style.title_size,
                           font_color=(255, 255, 255), bold=True)

        # Subtitle
        self._add_text_box(slide, Inches(0.5), Inches(1.7), Inches(9), Inches(0.6),
                           "BLM (Business Leadership Model) Five Looks Analysis",
                           font_size=20, font_color=(255, 220, 220))

        # Info cards
        info_items = [
            ("Target Operator", result.target_operator.replace("_", " ").title()),
            ("Market", result.market.replace("_", " ").title()),
            ("Analysis Period", result.analysis_period),
            ("Report Date", datetime.now().strftime('%Y-%m-%d')),
        ]
        x = Inches(0.5)
        for label, value in info_items:
            self._add_shape(slide, x, Inches(3.5), Inches(2.9), Inches(1.3),
                            (245, 245, 245))
            self._add_text_box(slide, x + Inches(0.15), Inches(3.6),
                               Inches(2.6), Inches(0.3), label,
                               font_size=10, font_color=self.style.light_text_color)
            self._add_text_box(slide, x + Inches(0.15), Inches(3.9),
                               Inches(2.6), Inches(0.7), value,
                               font_size=16, font_color=self.style.primary_color,
                               bold=True)
            x += Inches(3.1)

        # Framework overview
        framework = (
            "01 Trends (PEST) | 02 Market/Customer ($APPEALS) | "
            "03 Competition (Porter) | 04 Self (BMC) | "
            "SWOT Synthesis | 05 Opportunities (SPAN)"
        )
        self._add_text_box(slide, Inches(0.5), Inches(5.3), Inches(12), Inches(0.6),
                           framework, font_size=12,
                           font_color=self.style.light_text_color)

    # =========================================================================
    # S02: Table of Contents
    # =========================================================================

    def _add_toc_slide(self, result):
        slide = self._new_slide("toc", "Table of Contents")
        self._add_header(slide, "Report Contents", "目录")

        sections = [
            ("01", "Executive Summary", "Key findings and recommendations"),
            ("02", "看趋势 Trends", "PEST Framework — macro environment"),
            ("03", "看市场 Market/Customer", "$APPEALS — market changes & needs"),
            ("04", "看竞争 Competition", "Porter's Five Forces — competitive landscape"),
            ("05", "看自己 Self", "BMC + Capability — internal assessment"),
            ("06", "SWOT Synthesis", "Strengths, Weaknesses, Opportunities, Threats"),
            ("07", "看机会 Opportunities", "SPAN Matrix — opportunity selection"),
            ("08", "Summary & Provenance", "Conclusions and data sources"),
        ]

        y = Inches(1.5)
        for num, title, desc in sections:
            self._add_shape(slide, Inches(0.8), y, Inches(0.5), Inches(0.5),
                            self.style.primary_color, MSO_SHAPE.OVAL)
            self._add_text_box(slide, Inches(0.8), y + Inches(0.08), Inches(0.5),
                               Inches(0.35), num, font_size=12,
                               font_color=(255, 255, 255), bold=True, align="center")
            self._add_text_box(slide, Inches(1.5), y + Inches(0.02), Inches(4),
                               Inches(0.3), title, font_size=14,
                               font_color=self.style.text_color, bold=True)
            self._add_text_box(slide, Inches(1.5), y + Inches(0.3), Inches(8),
                               Inches(0.3), desc, font_size=11,
                               font_color=self.style.light_text_color)
            y += Inches(0.7)

    # =========================================================================
    # S03: Data Quality
    # =========================================================================

    def _add_data_quality_slide(self, result):
        slide = self._new_slide("data_quality", "Data Quality")
        self._add_header(slide, "Data Quality Overview", "数据质量概览")

        prov = result.provenance
        report = prov.quality_report() if prov else {}

        total = report.get("total_data_points", 0)
        high = report.get("high_confidence", 0)
        medium = report.get("medium_confidence", 0)
        low = report.get("low_confidence", 0)
        estimated = report.get("estimated", 0)
        conflicts = report.get("with_conflicts", 0)
        sources = report.get("unique_sources", 0)

        metrics = [
            ("Total Data Points", str(total), ""),
            ("High Confidence", str(high), f"{high/max(total,1)*100:.0f}%"),
            ("Medium Confidence", str(medium), ""),
            ("Low/Estimated", str(low + estimated), ""),
        ]
        self._add_metric_cards(slide, metrics, top=1.5)

        # Additional info
        info_text = (
            f"Unique Sources: {sources}\n"
            f"Data Conflicts: {conflicts}\n"
            f"Coverage: {'Good' if high > total * 0.5 else 'Partial'}"
        )
        self._add_text_box(slide, Inches(0.5), Inches(3.2), Inches(5), Inches(2),
                           info_text, font_size=14,
                           font_color=self.style.text_color)

        km = f"{total} data points tracked, {high} high-confidence ({high/max(total,1)*100:.0f}%)"
        self._add_key_message_bar(slide, km)

    # =========================================================================
    # S04: Executive Summary
    # =========================================================================

    def _add_executive_summary(self, result):
        slide = self._new_slide("exec_summary", "Executive Summary")
        self._add_header(slide, "Executive Summary", "执行摘要")

        y = Inches(1.4)
        summaries = [
            ("Trends", _get_key_message(result.trends)),
            ("Market/Customer", _get_key_message(result.market_customer)),
            ("Competition", _get_key_message(result.competition)),
            ("Self Assessment", _get_key_message(result.self_analysis)),
            ("SWOT", _get_key_message(result.swot)),
            ("Opportunities", _get_key_message(result.opportunities)),
        ]

        for label, msg in summaries:
            # Label
            self._add_shape(slide, Inches(0.5), y, Inches(2.2), Inches(0.6),
                            (245, 245, 245))
            self._add_text_box(slide, Inches(0.6), y + Inches(0.1),
                               Inches(2), Inches(0.4), label,
                               font_size=12, font_color=self.style.primary_color,
                               bold=True)
            # Message
            self._add_text_box(slide, Inches(2.9), y + Inches(0.1),
                               Inches(9.5), Inches(0.5), msg or "Analysis pending",
                               font_size=11, font_color=self.style.text_color)
            y += Inches(0.7)

        self._add_key_message_bar(slide, "Five Looks analysis completed — see details in following sections")

    # =========================================================================
    # Section divider
    # =========================================================================

    def _add_section_divider(self, title: str, subtitle: str = ""):
        slide = self._new_slide(f"section_{self.slide_num}", title)

        self._add_shape(slide, 0, 0, Inches(self.SLIDE_WIDTH), Inches(self.SLIDE_HEIGHT),
                        self.style.primary_color)
        self._add_text_box(slide, Inches(1), Inches(2.5), Inches(11), Inches(1.5),
                           title, font_size=self.style.title_size,
                           font_color=(255, 255, 255), bold=True)
        if subtitle:
            self._add_text_box(slide, Inches(1), Inches(4.0), Inches(11), Inches(1),
                               subtitle, font_size=self.style.heading_size,
                               font_color=(255, 220, 220))

    # =========================================================================
    # Look 1: Trends
    # =========================================================================

    def _add_pest_dashboard(self, trends):
        if trends is None:
            return
        pest = trends.pest if hasattr(trends, 'pest') else None
        if pest is None:
            return

        slide = self._new_slide("pest_dashboard", "PEST Dashboard")
        self._add_header(slide, "PEST Analysis Dashboard", "宏观环境分析")

        chart_path = self.chart_gen.create_pest_dashboard(pest, filename="pest_dashboard.png")
        self._add_image(slide, chart_path, Inches(0.5), Inches(1.3),
                        Inches(12), Inches(4.8))

        km = getattr(pest, 'key_message', '') or "PEST analysis of macro environment factors"
        self._add_key_message_bar(slide, km)

    def _add_industry_environment(self, trends):
        if trends is None:
            return

        slide = self._new_slide("industry_env", "Industry Environment")
        self._add_header(slide, "Industry Environment", "行业环境")

        # Left column: key metrics
        items = []
        if trends.industry_market_size:
            items.append(f"Market Size: {trends.industry_market_size}")
        if trends.industry_growth_rate:
            items.append(f"Growth Rate: {trends.industry_growth_rate}")
        if trends.industry_profit_trend:
            items.append(f"Profit Trend: {trends.industry_profit_trend}")
        if trends.industry_concentration:
            items.append(f"Concentration: {trends.industry_concentration}")
        if trends.industry_lifecycle_stage:
            items.append(f"Lifecycle Stage: {trends.industry_lifecycle_stage}")
        if items:
            self._add_bullet_list(slide, Inches(0.5), Inches(1.4), Inches(5.5),
                                  Inches(2.5), items, font_size=13)

        # Right column
        right_items = []
        if trends.new_business_models:
            right_items.append("New Business Models:")
            right_items.extend(f"  {m}" for m in trends.new_business_models[:3])
        if trends.technology_revolution:
            right_items.append("Technology Revolution:")
            right_items.extend(f"  {t}" for t in trends.technology_revolution[:3])
        if right_items:
            self._add_bullet_list(slide, Inches(6.5), Inches(1.4), Inches(6),
                                  Inches(3), right_items, font_size=12)

        # Key success factors
        if trends.key_success_factors:
            self._add_text_box(slide, Inches(0.5), Inches(4.2), Inches(5), Inches(0.3),
                               "Key Success Factors:", font_size=13,
                               font_color=self.style.primary_color, bold=True)
            self._add_bullet_list(slide, Inches(0.5), Inches(4.5), Inches(12),
                                  Inches(1.5), trends.key_success_factors[:5],
                                  font_size=11)

        km = trends.key_message or "Industry environment analysis"
        self._add_key_message_bar(slide, km)

    def _add_trend_deep_dive(self, trends):
        if trends is None:
            return
        if not trends.value_transfer_trends:
            return

        slide = self._new_slide("trend_deep_dive", "Trend Deep Dive", required=False)
        self._add_header(slide, "Value Transfer Trends", "价值转移趋势")

        self._add_bullet_list(slide, Inches(0.5), Inches(1.4), Inches(12),
                              Inches(4.5), trends.value_transfer_trends[:8],
                              font_size=13)

        km = trends.key_message or "Value transfer trends in the industry"
        self._add_key_message_bar(slide, km)

    # =========================================================================
    # Look 2: Market/Customer
    # =========================================================================

    def _add_market_change_panorama(self, mci):
        if mci is None:
            return

        slide = self._new_slide("market_changes", "Market Changes")
        self._add_header(slide, "Market Change Panorama", "市场变化全景")

        # Snapshot metrics
        snapshot = mci.market_snapshot or {}
        if snapshot:
            metrics = []
            # Try matching keys with fallbacks for different naming conventions
            key_map = [
                ('total_revenue', 'Total Revenue'),
                ('total_mobile_subscribers_k', 'Mobile Subs (K)'),
                ('total_broadband_subscribers_k', 'Broadband Subs (K)'),
                ('operator_count', 'Operators'),
            ]
            for key, label in key_map:
                if key in snapshot:
                    v = snapshot[key]
                    if isinstance(v, dict):
                        v = ", ".join(f"{sk}: {sv}" for sk, sv in v.items())
                    metrics.append((label, str(v), ""))
            if metrics:
                self._add_metric_cards(slide, metrics[:4], top=1.4)

        # Changes
        changes = mci.changes or []
        if changes:
            y = Inches(3.0)
            self._add_text_box(slide, Inches(0.5), y, Inches(5), Inches(0.3),
                               "Market Changes:", font_size=13,
                               font_color=self.style.primary_color, bold=True)
            items = []
            for c in changes[:6]:
                desc = c.description if hasattr(c, 'description') else str(c)
                items.append(desc)
            self._add_bullet_list(slide, Inches(0.5), y + Inches(0.3), Inches(12),
                                  Inches(2.5), items, font_size=11)

        km = mci.key_message or "Market dynamics overview"
        self._add_key_message_bar(slide, km)

    def _add_customer_segments(self, mci):
        if mci is None:
            return
        if not mci.customer_segments:
            return

        slide = self._new_slide("customer_segments", "Customer Segments")
        self._add_header(slide, "Customer Segments", "客户细分")

        y = Inches(1.4)
        for seg in mci.customer_segments[:4]:
            self._add_shape(slide, Inches(0.5), y, Inches(12), Inches(1.0),
                            (248, 248, 248))
            name = seg.segment_name if hasattr(seg, 'segment_name') else str(seg)
            self._add_text_box(slide, Inches(0.7), y + Inches(0.05), Inches(3),
                               Inches(0.3), name, font_size=13,
                               font_color=self.style.primary_color, bold=True)
            details = []
            if hasattr(seg, 'size_estimate') and seg.size_estimate:
                details.append(f"Size: {seg.size_estimate}")
            if hasattr(seg, 'growth_trend'):
                details.append(f"Trend: {seg.growth_trend}")
            if hasattr(seg, 'our_share') and seg.our_share:
                details.append(f"Our Share: {seg.our_share}")
            detail_text = " | ".join(details)
            self._add_text_box(slide, Inches(0.7), y + Inches(0.35), Inches(11),
                               Inches(0.25), detail_text, font_size=11,
                               font_color=self.style.text_color)
            if hasattr(seg, 'unmet_needs') and seg.unmet_needs:
                needs_text = "Unmet Needs: " + ", ".join(seg.unmet_needs[:3])
                self._add_text_box(slide, Inches(0.7), y + Inches(0.6), Inches(11),
                                   Inches(0.3), needs_text, font_size=10,
                                   font_color=self.style.light_text_color)
            y += Inches(1.15)

        km = mci.key_message or "Customer segmentation analysis"
        self._add_key_message_bar(slide, km)

    def _add_appeals_assessment(self, mci):
        if mci is None:
            return
        if not mci.appeals_assessment:
            return

        slide = self._new_slide("appeals", "$APPEALS Assessment")
        self._add_header(slide, "$APPEALS Assessment", "客户需求评估")

        chart_path = self.chart_gen.create_appeals_radar(
            mci.appeals_assessment,
            target_operator=self.operator_id,
            filename="appeals_radar.png")
        self._add_image(slide, chart_path, Inches(0.5), Inches(1.3),
                        Inches(11.5), Inches(4.8))

        km = mci.key_message or "$APPEALS customer needs assessment"
        self._add_key_message_bar(slide, km)

    def _add_market_deep_dive(self, mci):
        if mci is None:
            return
        if not mci.customer_value_migration:
            return

        slide = self._new_slide("market_deep_dive", "Market Deep Dive", required=False)
        self._add_header(slide, "Customer Value Migration", "客户价值迁移")

        self._add_text_box(slide, Inches(0.5), Inches(1.4), Inches(12), Inches(3),
                           mci.customer_value_migration, font_size=13,
                           font_color=self.style.text_color)

        opps = mci.opportunities or []
        threats = mci.threats or []
        if opps:
            self._add_text_box(slide, Inches(0.5), Inches(3.5), Inches(5.5), Inches(0.3),
                               "Opportunities:", font_size=12,
                               font_color=self.style.positive_color, bold=True)
            self._add_bullet_list(slide, Inches(0.5), Inches(3.8), Inches(5.5),
                                  Inches(2), [o.description for o in opps[:4]
                                              if hasattr(o, 'description')],
                                  font_size=10)
        if threats:
            self._add_text_box(slide, Inches(6.5), Inches(3.5), Inches(5.5), Inches(0.3),
                               "Threats:", font_size=12,
                               font_color=self.style.negative_color, bold=True)
            self._add_bullet_list(slide, Inches(6.5), Inches(3.8), Inches(5.5),
                                  Inches(2), [t.description for t in threats[:4]
                                              if hasattr(t, 'description')],
                                  font_size=10)

        km = mci.key_message or "Market deep dive analysis"
        self._add_key_message_bar(slide, km)

    # =========================================================================
    # Look 3: Competition
    # =========================================================================

    def _add_five_forces(self, comp):
        if comp is None:
            return

        slide = self._new_slide("five_forces", "Porter's Five Forces")
        self._add_header(slide, "Porter's Five Forces", "波特五力分析")

        forces = comp.five_forces if hasattr(comp, 'five_forces') else {}
        if forces:
            chart_path = self.chart_gen.create_porter_five_forces(
                forces, filename="porter_forces.png")
            self._add_image(slide, chart_path, Inches(3), Inches(1.2),
                            Inches(7), Inches(5))

        # Overall intensity label
        intensity = getattr(comp, 'overall_competition_intensity', 'medium')
        self._add_text_box(slide, Inches(0.5), Inches(1.5), Inches(2.5), Inches(0.4),
                           f"Overall Intensity: {intensity.upper()}",
                           font_size=13, font_color=self.style.primary_color, bold=True)

        km = comp.key_message or "Competitive forces analysis"
        self._add_key_message_bar(slide, km)

    def _add_competitor_deep_dives(self, comp):
        if comp is None:
            return
        analyses = comp.competitor_analyses if hasattr(comp, 'competitor_analyses') else {}
        for operator_id, deep_dive in list(analyses.items())[:3]:
            slide = self._new_slide(f"competitor_{operator_id}", f"Competitor: {operator_id}")
            self._add_header(slide, f"Competitor Analysis: {operator_id.replace('_', ' ').title()}",
                             "竞争对手分析")

            y = Inches(1.4)
            # Financial health
            fh = deep_dive.financial_health if hasattr(deep_dive, 'financial_health') else {}
            if fh:
                metrics = [(k.replace('_', ' ').title(), str(v), "")
                           for k, v in list(fh.items())[:4]]
                self._add_metric_cards(slide, metrics, top=1.4)
                y = Inches(2.8)

            # Strengths / Weaknesses
            cols = [
                ("Strengths", getattr(deep_dive, 'strengths', []), self.style.positive_color),
                ("Weaknesses", getattr(deep_dive, 'weaknesses', []), self.style.negative_color),
            ]
            x = Inches(0.5)
            for col_title, items, color in cols:
                self._add_text_box(slide, x, y, Inches(5.5), Inches(0.3),
                                   col_title, font_size=13, font_color=color, bold=True)
                self._add_bullet_list(slide, x, y + Inches(0.3), Inches(5.5),
                                      Inches(2.5), items[:5], font_size=11)
                x += Inches(6)

            # Growth strategy
            strategy = getattr(deep_dive, 'growth_strategy', '')
            if strategy:
                self._add_text_box(slide, Inches(0.5), Inches(5.5), Inches(12), Inches(0.5),
                                   f"Strategy: {strategy}", font_size=11,
                                   font_color=self.style.text_color)

            self._add_key_message_bar(slide, f"Competitor analysis: {operator_id}")

    def _add_competition_summary(self, comp):
        if comp is None:
            return

        slide = self._new_slide("competition_summary", "Competition Summary")
        self._add_header(slide, "Competitive Landscape Summary", "竞争格局总结")

        # Comparison table
        table = comp.comparison_table if hasattr(comp, 'comparison_table') else {}
        if table:
            metrics = list(table.keys())[:6]
            operators = set()
            for m in metrics:
                operators.update(table[m].keys())
            operators = sorted(operators)[:5]

            data = {op: [str(table[m].get(op, 'N/A')) for m in metrics]
                    for op in operators}
            if data:
                chart_path = self.chart_gen.create_kpi_table_chart(
                    metrics, data, target_operator=self.operator_id,
                    title="Competitive Comparison", filename="comp_table.png")
                self._add_image(slide, chart_path, Inches(0.5), Inches(1.3),
                                Inches(12), Inches(4.5))

        landscape = getattr(comp, 'competitive_landscape', '')
        if landscape and not table:
            self._add_text_box(slide, Inches(0.5), Inches(1.4), Inches(12),
                               Inches(4), landscape, font_size=13,
                               font_color=self.style.text_color)

        km = comp.key_message or "Competitive landscape overview"
        self._add_key_message_bar(slide, km)

    def _add_new_entrants(self, comp):
        if comp is None:
            return
        forces = comp.five_forces if hasattr(comp, 'five_forces') else {}
        ne_force = forces.get('new_entrants')
        if ne_force is None:
            return
        if not (hasattr(ne_force, 'key_factors') and ne_force.key_factors):
            return

        slide = self._new_slide("new_entrants", "New Entrants", required=False)
        self._add_header(slide, "New Entrants Threat", "新进入者威胁")

        items = []
        for factor in ne_force.key_factors[:6]:
            if isinstance(factor, dict):
                items.append(f"{factor.get('name', '')}: {factor.get('description', '')}")
            else:
                items.append(str(factor))
        self._add_bullet_list(slide, Inches(0.5), Inches(1.4), Inches(12),
                              Inches(4), items, font_size=13)

        level = getattr(ne_force, 'force_level', 'medium')
        km = f"New entrants threat level: {level}"
        self._add_key_message_bar(slide, km)

    # =========================================================================
    # Look 4: Self
    # =========================================================================

    def _add_health_check(self, self_analysis):
        if self_analysis is None:
            return

        slide = self._new_slide("health_check", "Health Check")
        self._add_header(slide, "Operating Health Check", "经营体检")

        # Financial health metrics
        fh = self_analysis.financial_health or {}
        if fh:
            metrics = [(k.replace('_', ' ').title(), str(v), "")
                       for k, v in list(fh.items())[:4]]
            self._add_metric_cards(slide, metrics, top=1.4)

        # Health rating
        rating = getattr(self_analysis, 'health_rating', 'stable')
        rating_colors = {
            'healthy': self.style.positive_color,
            'stable': self.style.warning_color,
            'concerning': self.style.negative_color,
            'critical': (200, 0, 0),
        }
        self._add_text_box(slide, Inches(0.5), Inches(3.0), Inches(3), Inches(0.4),
                           f"Health Rating: {rating.upper()}",
                           font_size=14, font_color=rating_colors.get(rating, self.style.text_color),
                           bold=True)

        # Revenue breakdown
        rb = self_analysis.revenue_breakdown or {}
        if rb:
            items = []
            for k, v in list(rb.items())[:6]:
                if isinstance(v, dict):
                    val = v.get('value', '')
                    share = v.get('share_pct', '')
                    items.append(f"{k.replace('_', ' ').title()}: €{val:,.0f}M ({share}%)" if val else f"{k}: {v}")
                else:
                    items.append(f"{k.replace('_', ' ').title()}: {v}")
            self._add_text_box(slide, Inches(0.5), Inches(3.6), Inches(5), Inches(0.3),
                               "Revenue Breakdown:", font_size=12,
                               font_color=self.style.primary_color, bold=True)
            self._add_bullet_list(slide, Inches(0.5), Inches(3.9), Inches(5),
                                  Inches(2), items, font_size=11)

        # Market positions
        mp = self_analysis.market_positions or {}
        if mp:
            pos_items = [f"{k}: {v}" for k, v in list(mp.items())[:6]]
            self._add_text_box(slide, Inches(6.5), Inches(3.6), Inches(5.5), Inches(0.3),
                               "Market Positions:", font_size=12,
                               font_color=self.style.primary_color, bold=True)
            self._add_bullet_list(slide, Inches(6.5), Inches(3.9), Inches(5.5),
                                  Inches(2), pos_items, font_size=11)

        km = self_analysis.key_message or "Operating health check summary"
        self._add_key_message_bar(slide, km)

    def _add_segment_deep_dives(self, self_analysis):
        if self_analysis is None:
            return
        segments = self_analysis.segment_analyses or []
        for seg in segments[:4]:
            slide = self._new_slide(
                f"segment_{seg.segment_id}" if hasattr(seg, 'segment_id') else f"segment_{self.slide_num}",
                f"Segment: {seg.segment_name}")
            self._add_header(slide, f"Segment Analysis: {seg.segment_name}",
                             "细分业务分析")

            y = Inches(1.4)
            # Key metrics
            km_data = seg.key_metrics if hasattr(seg, 'key_metrics') else {}
            if km_data:
                metrics = [(k.replace('_', ' ').title(), str(v), "")
                           for k, v in list(km_data.items())[:4]]
                self._add_metric_cards(slide, metrics, top=1.4)
                y = Inches(2.8)

            # Health status
            health = getattr(seg, 'health_status', 'stable')
            self._add_text_box(slide, Inches(0.5), y, Inches(3), Inches(0.3),
                               f"Health: {health.upper()}", font_size=12,
                               font_color=self.style.primary_color, bold=True)

            # Changes
            changes = getattr(seg, 'changes', [])
            if changes:
                change_items = []
                for c in changes[:5]:
                    if hasattr(c, 'metric'):
                        direction = getattr(c, 'direction', '')
                        change_items.append(f"{c.metric}: {direction}")
                    else:
                        change_items.append(str(c))
                self._add_bullet_list(slide, Inches(0.5), y + Inches(0.4),
                                      Inches(5.5), Inches(2), change_items, font_size=11)

            # Attributions
            attributions = getattr(seg, 'attributions', [])
            if attributions:
                self._add_text_box(slide, Inches(6.5), y, Inches(5.5), Inches(0.3),
                                   "Root Causes:", font_size=12,
                                   font_color=self.style.primary_color, bold=True)
                attr_items = [a.description for a in attributions[:4]
                              if hasattr(a, 'description')]
                self._add_bullet_list(slide, Inches(6.5), y + Inches(0.4),
                                      Inches(5.5), Inches(2), attr_items, font_size=11)

            seg_km = getattr(seg, 'key_message', '') or f"{seg.segment_name} segment analysis"
            self._add_key_message_bar(slide, seg_km)

    def _add_network_analysis(self, self_analysis):
        if self_analysis is None:
            return
        network = getattr(self_analysis, 'network', None)
        if network is None:
            return

        slide = self._new_slide("network", "Network Analysis")
        self._add_header(slide, "Network Analysis", "网络分析")

        y = Inches(1.4)
        # Coverage gauges
        coverage = network.coverage or {}
        if coverage:
            labels = list(coverage.keys())[:4]
            values = [float(coverage[k]) for k in labels]
            chart_path = self.chart_gen.create_donut_gauges(
                labels, values, title="Network Coverage", filename="coverage_gauges.png")
            self._add_image(slide, chart_path, Inches(0.5), Inches(1.3),
                            Inches(12), Inches(2.5))
            y = Inches(4.0)

        # Tech mix
        tech = network.technology_mix or {}
        if tech:
            items = []
            for k, v in tech.items():
                label = k.replace('_', ' ').title()
                if isinstance(v, dict):
                    formatted = ", ".join(f"{sk}: {sv}" for sk, sv in v.items())
                    items.append(f"{label}: {formatted}")
                elif isinstance(v, (int, float)) and 'pct' in k:
                    items.append(f"{label}: {v}%")
                else:
                    items.append(f"{label}: {v}")
            self._add_text_box(slide, Inches(0.5), y, Inches(3), Inches(0.3),
                               "Technology Mix:", font_size=12,
                               font_color=self.style.primary_color, bold=True)
            self._add_bullet_list(slide, Inches(0.5), y + Inches(0.3), Inches(5),
                                  Inches(1.5), items, font_size=11)

        # Investment direction
        inv = network.investment_direction or ''
        if inv:
            self._add_text_box(slide, Inches(6.5), y, Inches(5.5), Inches(2),
                               f"Investment Direction: {inv}", font_size=12,
                               font_color=self.style.text_color)

        km = "Network infrastructure and coverage assessment"
        self._add_key_message_bar(slide, km)

    def _add_bmc_canvas(self, self_analysis):
        if self_analysis is None:
            return
        bmc = getattr(self_analysis, 'bmc', None)
        if bmc is None:
            return

        slide = self._new_slide("bmc", "Business Model Canvas")
        self._add_header(slide, "Business Model Canvas", "商业模式画布")

        chart_path = self.chart_gen.create_bmc_canvas(bmc, filename="bmc_canvas.png")
        self._add_image(slide, chart_path, Inches(0.3), Inches(1.2),
                        Inches(12.5), Inches(4.9))

        km = "Business model canvas overview"
        self._add_key_message_bar(slide, km)

    def _add_org_talent(self, self_analysis):
        if self_analysis is None:
            return

        slide = self._new_slide("org_talent", "Organization & Talent")
        self._add_header(slide, "Organization & Talent", "组织与人才")

        y = Inches(1.4)
        # Org culture
        culture = getattr(self_analysis, 'org_culture', '')
        if culture:
            self._add_text_box(slide, Inches(0.5), y, Inches(5.5), Inches(0.3),
                               "Organization Culture:", font_size=12,
                               font_color=self.style.primary_color, bold=True)
            self._add_text_box(slide, Inches(0.5), y + Inches(0.35), Inches(5.5),
                               Inches(1.5), culture, font_size=11,
                               font_color=self.style.text_color)

        # Talent assessment
        talent = self_analysis.talent_assessment or {}
        if talent:
            items = [f"{k}: {v}" for k, v in talent.items()]
            self._add_text_box(slide, Inches(6.5), y, Inches(5.5), Inches(0.3),
                               "Talent Assessment:", font_size=12,
                               font_color=self.style.primary_color, bold=True)
            self._add_bullet_list(slide, Inches(6.5), y + Inches(0.35), Inches(5.5),
                                  Inches(2), items, font_size=11)

        # Leadership changes
        changes = self_analysis.leadership_changes or []
        if changes:
            self._add_text_box(slide, Inches(0.5), Inches(4.0), Inches(12), Inches(0.3),
                               "Leadership Changes:", font_size=12,
                               font_color=self.style.primary_color, bold=True)
            items = [str(c) if not isinstance(c, dict) else
                     f"{c.get('name', '')}: {c.get('role', '')} ({c.get('date', '')})"
                     for c in changes[:4]]
            self._add_bullet_list(slide, Inches(0.5), Inches(4.3), Inches(12),
                                  Inches(1.5), items, font_size=11)

        km = "Organization and talent assessment"
        self._add_key_message_bar(slide, km)

    def _add_strengths_weaknesses_exposure(self, self_analysis):
        if self_analysis is None:
            return

        slide = self._new_slide("sw_exposure", "Strengths/Weaknesses/Exposure")
        self._add_header(slide, "Strengths, Weaknesses & Exposure Points",
                         "优势/劣势/风险暴露点")

        # Three columns
        cols = [
            ("Strengths", getattr(self_analysis, 'strengths', []),
             self.style.positive_color, Inches(0.5)),
            ("Weaknesses", getattr(self_analysis, 'weaknesses', []),
             self.style.negative_color, Inches(4.5)),
            ("Exposure Points", [], self.style.warning_color, Inches(8.5)),
        ]
        # Build exposure items
        exposure = getattr(self_analysis, 'exposure_points', [])
        exposure_items = []
        for ep in exposure[:5]:
            if hasattr(ep, 'trigger_action'):
                exposure_items.append(f"{ep.trigger_action}: {ep.side_effect}")
            else:
                exposure_items.append(str(ep))
        cols[2] = ("Exposure Points", exposure_items, self.style.warning_color, Inches(8.5))

        for title, items, color, x in cols:
            self._add_text_box(slide, x, Inches(1.4), Inches(3.8), Inches(0.3),
                               title, font_size=13, font_color=color, bold=True)
            self._add_bullet_list(slide, x, Inches(1.8), Inches(3.8), Inches(4),
                                  items[:6], font_size=11)

        km = self_analysis.key_message or "Self-assessment summary"
        self._add_key_message_bar(slide, km)

    # =========================================================================
    # SWOT Synthesis
    # =========================================================================

    def _add_swot_matrix(self, swot):
        if swot is None:
            return

        slide = self._new_slide("swot", "SWOT Matrix")
        self._add_header(slide, "SWOT Analysis", "SWOT 综合分析")

        chart_path = self.chart_gen.create_swot_matrix(swot, filename="swot_matrix.png")
        self._add_image(slide, chart_path, Inches(0.5), Inches(1.2),
                        Inches(7.5), Inches(4.9))

        # Strategy quadrants on the right
        strategies = [
            ("SO", getattr(swot, 'so_strategies', []), self.style.positive_color),
            ("WO", getattr(swot, 'wo_strategies', []), (70, 130, 180)),
            ("ST", getattr(swot, 'st_strategies', []), self.style.warning_color),
            ("WT", getattr(swot, 'wt_strategies', []), self.style.negative_color),
        ]
        y = Inches(1.4)
        for label, items, color in strategies:
            self._add_text_box(slide, Inches(8.5), y, Inches(1), Inches(0.25),
                               f"{label}:", font_size=10, font_color=color, bold=True)
            if items:
                text = items[0] if len(items[0]) <= 60 else items[0][:57] + "..."
                self._add_text_box(slide, Inches(9.3), y, Inches(3.5), Inches(0.6),
                                   text, font_size=9, font_color=self.style.text_color)
            y += Inches(0.7)

        km = swot.key_message or "SWOT synthesis and strategic implications"
        self._add_key_message_bar(slide, km)

    # =========================================================================
    # Look 5: Opportunities
    # =========================================================================

    def _add_span_bubble(self, opp):
        if opp is None:
            return

        slide = self._new_slide("span_bubble", "SPAN Matrix")
        self._add_header(slide, "SPAN Matrix — Opportunity Positioning", "机会定位矩阵")

        positions = opp.span_positions if hasattr(opp, 'span_positions') else []
        if positions:
            chart_path = self.chart_gen.create_span_bubble_chart(
                positions, filename="span_bubble.png")
            self._add_image(slide, chart_path, Inches(0.5), Inches(1.2),
                            Inches(11.5), Inches(4.8))
        else:
            self._add_text_box(slide, Inches(2), Inches(3), Inches(9), Inches(1),
                               "No SPAN positions available",
                               font_size=14, font_color=self.style.light_text_color,
                               align="center")

        km = opp.key_message or "Opportunity positioning on SPAN matrix"
        self._add_key_message_bar(slide, km)

    def _add_priority_table(self, opp):
        if opp is None:
            return
        opportunities = getattr(opp, 'opportunities', [])
        if not opportunities:
            return

        slide = self._new_slide("priority_table", "Opportunity Priorities")
        self._add_header(slide, "Opportunity Priority Ranking", "机会优先级排序")

        items = [o.name if hasattr(o, 'name') else str(o) for o in opportunities[:8]]
        priorities = [getattr(o, 'priority', 'P1') for o in opportunities[:8]]

        chart_path = self.chart_gen.create_priority_chart(
            items, priorities, title="", filename="priority_table.png")
        self._add_image(slide, chart_path, Inches(0.5), Inches(1.3),
                        Inches(12), Inches(4.5))

        km = opp.key_message or "Prioritized opportunities"
        self._add_key_message_bar(slide, km)

    def _add_opportunity_deep_dive(self, opp):
        if opp is None:
            return
        opportunities = getattr(opp, 'opportunities', [])
        if not opportunities:
            return

        slide = self._new_slide("opp_deep_dive", "Opportunity Details", required=False)
        self._add_header(slide, "Opportunity Details", "机会详情")

        y = Inches(1.4)
        for item in opportunities[:4]:
            name = item.name if hasattr(item, 'name') else str(item)
            desc = getattr(item, 'description', '')
            priority = getattr(item, 'priority', 'P1')
            market = getattr(item, 'addressable_market', 'N/A')
            window = getattr(item, 'time_window', '')

            self._add_shape(slide, Inches(0.5), y, Inches(12), Inches(1.0),
                            (248, 248, 248))
            # Priority badge
            p_colors = {'P0': self.style.primary_color,
                        'P1': self.style.warning_color,
                        'P2': self.style.positive_color}
            self._add_shape(slide, Inches(0.6), y + Inches(0.1), Inches(0.5), Inches(0.35),
                            p_colors.get(priority, self.style.neutral_color))
            self._add_text_box(slide, Inches(0.6), y + Inches(0.12), Inches(0.5),
                               Inches(0.3), priority, font_size=10,
                               font_color=(255, 255, 255), bold=True, align="center")

            self._add_text_box(slide, Inches(1.3), y + Inches(0.05), Inches(5),
                               Inches(0.3), name, font_size=13,
                               font_color=self.style.primary_color, bold=True)
            detail = f"Market: {market} | Window: {window}"
            self._add_text_box(slide, Inches(1.3), y + Inches(0.35), Inches(10),
                               Inches(0.25), detail, font_size=10,
                               font_color=self.style.light_text_color)
            if desc:
                self._add_text_box(slide, Inches(1.3), y + Inches(0.6), Inches(10),
                                   Inches(0.35), desc, font_size=10,
                                   font_color=self.style.text_color)
            y += Inches(1.15)

        km = opp.key_message or "Detailed opportunity analysis"
        self._add_key_message_bar(slide, km)

    # =========================================================================
    # Summary slides
    # =========================================================================

    def _add_summary_slide(self, result):
        slide = self._new_slide("summary", "Summary")
        self._add_header(slide, "Analysis Summary", "分析总结")

        sections = [
            ("01 Trends", _get_key_message(result.trends)),
            ("02 Market", _get_key_message(result.market_customer)),
            ("03 Competition", _get_key_message(result.competition)),
            ("04 Self", _get_key_message(result.self_analysis)),
            ("SWOT", _get_key_message(result.swot)),
            ("05 Opportunities", _get_key_message(result.opportunities)),
        ]

        y = Inches(1.4)
        for label, msg in sections:
            self._add_shape(slide, Inches(0.5), y, Inches(0.08), Inches(0.6),
                            self.style.primary_color)
            self._add_text_box(slide, Inches(0.8), y + Inches(0.02), Inches(2.2),
                               Inches(0.3), label, font_size=12,
                               font_color=self.style.primary_color, bold=True)
            self._add_text_box(slide, Inches(3.2), y + Inches(0.02), Inches(9.5),
                               Inches(0.55), msg or "—", font_size=11,
                               font_color=self.style.text_color)
            y += Inches(0.7)

        self._add_key_message_bar(slide, "Complete Five Looks analysis — see opportunity priorities for next steps")

    def _add_provenance_appendix(self, result):
        slide = self._new_slide("provenance", "Provenance Appendix")
        self._add_header(slide, "Data Provenance", "数据溯源")

        prov = result.provenance
        footnotes = prov.to_footnotes() if prov else []
        if footnotes:
            self._add_bullet_list(slide, Inches(0.5), Inches(1.4), Inches(12),
                                  Inches(4.5), footnotes[:15], font_size=10)
        else:
            self._add_text_box(slide, Inches(0.5), Inches(2), Inches(12), Inches(1),
                               "No provenance data recorded for this analysis",
                               font_size=13, font_color=self.style.light_text_color)

        self._add_key_message_bar(slide, "All data points are traceable to original sources")

    def _add_back_cover(self):
        slide = self._new_slide("back_cover", "Back Cover")
        self._add_shape(slide, 0, 0, Inches(self.SLIDE_WIDTH), Inches(self.SLIDE_HEIGHT),
                        self.style.primary_color)
        self._add_text_box(slide, Inches(2), Inches(2.5), Inches(9), Inches(1.5),
                           "Thank You", font_size=48,
                           font_color=(255, 255, 255), bold=True, align="center")
        self._add_text_box(slide, Inches(2), Inches(4.0), Inches(9), Inches(1),
                           "BLM Five Looks Strategic Analysis",
                           font_size=20, font_color=(255, 220, 220), align="center")


# =============================================================================
# Helpers
# =============================================================================

def _get_key_message(obj) -> str:
    """Safely extract key_message from a data model object."""
    if obj is None:
        return ""
    return getattr(obj, 'key_message', '') or ""
