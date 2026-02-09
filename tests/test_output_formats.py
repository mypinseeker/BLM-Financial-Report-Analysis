"""Tests for JSON, TXT, and HTML output formats."""

import json
import tempfile
from pathlib import Path

import pytest

from src.output.json_exporter import BLMJsonExporter
from src.output.txt_formatter import BLMTxtFormatter
from src.output.html_generator import BLMHtmlGenerator
from src.output.ppt_styles import VODAFONE_STYLE
from src.blm.engine import FiveLooksResult
from src.models.provenance import ProvenanceStore, SourceReference, SourceType, Confidence
from src.models.trend import TrendAnalysis, PESTAnalysis, PESTFactor
from src.models.market import (
    MarketCustomerInsight, MarketChange, CustomerSegment, APPEALSAssessment
)
from src.models.competition import (
    CompetitionInsight, PorterForce, CompetitorDeepDive
)
from src.models.self_analysis import (
    SelfInsight, SegmentAnalysis, NetworkAnalysis, BMCCanvas, ExposurePoint
)
from src.models.swot import SWOTAnalysis
from src.models.opportunity import (
    OpportunityInsight, SPANPosition, OpportunityItem
)


# =============================================================================
# Shared fixtures
# =============================================================================

@pytest.fixture
def tmp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def mock_result():
    """Complete FiveLooksResult with realistic test data."""
    prov = ProvenanceStore()
    src = SourceReference(
        source_type=SourceType.FINANCIAL_REPORT_PDF,
        document_name="Q3 FY26 Results",
        publisher="Vodafone Group",
        confidence=Confidence.HIGH,
    )
    prov.register_source(src)
    prov.track(12.1, "revenue", operator="vodafone", source=src, unit="EUR B")
    prov.track(32, "ebitda_margin", operator="vodafone", source=src, unit="%")

    return FiveLooksResult(
        target_operator="vodafone_germany",
        market="germany",
        analysis_period="CQ4_2025",
        trends=TrendAnalysis(
            pest=PESTAnalysis(
                political_factors=[
                    PESTFactor(dimension="P", dimension_name="Political",
                               factor_name="Gigabit Strategy",
                               impact_type="opportunity", severity="high"),
                ],
                economic_factors=[
                    PESTFactor(dimension="E", dimension_name="Economic",
                               factor_name="GDP Growth",
                               impact_type="neutral"),
                ],
                society_factors=[],
                technology_factors=[
                    PESTFactor(dimension="T", dimension_name="Technology",
                               factor_name="5G Rollout",
                               impact_type="opportunity"),
                ],
                key_message="Favorable environment",
            ),
            industry_market_size="EUR 60B",
            industry_growth_rate="2.5%",
            industry_lifecycle_stage="mature",
            key_success_factors=["Network quality", "Convergence"],
            key_message="Mature market with 5G opportunity",
        ),
        market_customer=MarketCustomerInsight(
            market_snapshot={"total_revenue": "EUR 55B", "total_subscribers": "130M"},
            changes=[
                MarketChange(change_type="pricing",
                             description="Price war in postpaid",
                             impact_type="threat"),
            ],
            customer_segments=[
                CustomerSegment(segment_name="Value-Conscious",
                                growth_trend="growing", size_estimate="40%"),
            ],
            appeals_assessment=[
                APPEALSAssessment(dimension="$", dimension_name="Price",
                                  our_score=3.5,
                                  competitor_scores={"dt": 3.0}),
                APPEALSAssessment(dimension="P2", dimension_name="Performance",
                                  our_score=4.2,
                                  competitor_scores={"dt": 4.8}),
            ],
            key_message="Market favors convergence",
        ),
        competition=CompetitionInsight(
            five_forces={
                "existing_competitors": PorterForce(
                    force_name="existing_competitors", force_level="high"),
                "new_entrants": PorterForce(
                    force_name="new_entrants", force_level="medium"),
                "substitutes": PorterForce(
                    force_name="substitutes", force_level="low"),
                "supplier_power": PorterForce(
                    force_name="supplier_power", force_level="medium"),
                "buyer_power": PorterForce(
                    force_name="buyer_power", force_level="high"),
            },
            competitor_analyses={
                "deutsche_telekom": CompetitorDeepDive(
                    operator="deutsche_telekom",
                    strengths=["Network leader"],
                    weaknesses=["Premium pricing"]),
            },
            comparison_table={"Revenue": {"vodafone": "12B", "dt": "25B"}},
            key_message="High competition; DT leads",
        ),
        self_analysis=SelfInsight(
            financial_health={"revenue": "EUR 12B"},
            segment_analyses=[
                SegmentAnalysis(segment_name="Mobile", segment_id="mobile",
                                health_status="stable"),
            ],
            strengths=["Cable network", "5G spectrum"],
            weaknesses=["Limited fiber"],
            exposure_points=[
                ExposurePoint(trigger_action="1&1 migration",
                              side_effect="Load surge"),
            ],
            health_rating="stable",
            key_message="Stable with fiber gap",
        ),
        swot=SWOTAnalysis(
            strengths=["Cable infra", "5G"],
            weaknesses=["Fiber gap"],
            opportunities=["5G enterprise", "FWA"],
            threats=["1&1 launch", "Price war"],
            so_strategies=["5G enterprise push"],
            wo_strategies=["Fiber partnerships"],
            st_strategies=["Convergence bundles"],
            wt_strategies=["Selective retreat"],
            key_message="Cable+5G strengths, address fiber",
        ),
        opportunities=OpportunityInsight(
            span_positions=[
                SPANPosition(opportunity_name="5G Enterprise",
                             market_attractiveness=8.5,
                             competitive_position=7.0,
                             bubble_size=3.0, quadrant="grow_invest"),
                SPANPosition(opportunity_name="IoT",
                             market_attractiveness=6.0,
                             competitive_position=4.0,
                             bubble_size=1.5, quadrant="acquire_skills"),
            ],
            grow_invest=["5G Enterprise"],
            acquire_skills=["IoT"],
            opportunities=[
                OpportunityItem(name="5G Enterprise", priority="P0",
                                description="B2B 5G", addressable_market="EUR 2B",
                                time_window="immediate"),
                OpportunityItem(name="IoT", priority="P1",
                                description="Industrial IoT"),
            ],
            key_message="5G enterprise is the primary growth engine",
        ),
        provenance=prov,
    )


@pytest.fixture
def empty_result():
    """FiveLooksResult with all None sections."""
    return FiveLooksResult(
        target_operator="test_op",
        market="test",
        analysis_period="CQ1_2026",
    )


# =============================================================================
# JSON Exporter tests
# =============================================================================

class TestJsonExporter:
    def test_export_returns_valid_json(self, mock_result):
        exporter = BLMJsonExporter()
        json_str = exporter.export(mock_result)
        data = json.loads(json_str)
        assert isinstance(data, dict)

    def test_export_to_file(self, mock_result, tmp_dir):
        exporter = BLMJsonExporter()
        path = exporter.export(mock_result, f"{tmp_dir}/test.json")
        assert Path(path).exists()
        content = Path(path).read_text(encoding='utf-8')
        data = json.loads(content)
        assert "meta" in data

    def test_meta_section(self, mock_result):
        exporter = BLMJsonExporter()
        data = json.loads(exporter.export(mock_result))
        meta = data["meta"]
        assert meta["target_operator"] == "vodafone_germany"
        assert meta["market"] == "germany"
        assert meta["analysis_period"] == "CQ4_2025"
        assert "generated_at" in meta
        assert meta["format_version"] == "1.0"

    def test_five_looks_sections_present(self, mock_result):
        exporter = BLMJsonExporter()
        data = json.loads(exporter.export(mock_result))
        fl = data["five_looks"]
        assert "trends" in fl
        assert "market_customer" in fl
        assert "competition" in fl
        assert "self_analysis" in fl
        assert "swot" in fl
        assert "opportunities" in fl

    def test_data_quality_section(self, mock_result):
        exporter = BLMJsonExporter()
        data = json.loads(exporter.export(mock_result))
        assert "data_quality" in data
        dq = data["data_quality"]
        assert dq["total_data_points"] == 2
        assert dq["high_confidence"] == 2

    def test_provenance_section(self, mock_result):
        exporter = BLMJsonExporter()
        data = json.loads(exporter.export(mock_result))
        assert "provenance" in data
        prov = data["provenance"]
        assert prov["source_count"] == 1
        assert prov["value_count"] == 2

    def test_exclude_provenance(self, mock_result):
        exporter = BLMJsonExporter()
        data = json.loads(exporter.export(mock_result, include_provenance=False))
        assert "provenance" not in data
        assert "data_quality" not in data

    def test_datetime_serialization(self, mock_result):
        exporter = BLMJsonExporter()
        json_str = exporter.export(mock_result)
        # Should not raise - all datetimes should be ISO format
        data = json.loads(json_str)
        assert isinstance(data, dict)

    def test_enum_serialization(self, mock_result):
        exporter = BLMJsonExporter()
        json_str = exporter.export(mock_result)
        # SourceType and Confidence enums should be serialized as values
        assert '"financial_report_pdf"' in json_str or '"high"' in json_str

    def test_none_sections_handled(self, empty_result):
        exporter = BLMJsonExporter()
        json_str = exporter.export(empty_result)
        data = json.loads(json_str)
        fl = data["five_looks"]
        assert fl["trends"] is None
        assert fl["swot"] is None

    def test_trends_data_structure(self, mock_result):
        exporter = BLMJsonExporter()
        data = json.loads(exporter.export(mock_result))
        trends = data["five_looks"]["trends"]
        assert "pest" in trends
        assert "key_message" in trends
        assert trends["industry_market_size"] == "EUR 60B"

    def test_swot_data_structure(self, mock_result):
        exporter = BLMJsonExporter()
        data = json.loads(exporter.export(mock_result))
        swot = data["five_looks"]["swot"]
        assert isinstance(swot["strengths"], list)
        assert "Cable infra" in swot["strengths"]
        assert isinstance(swot["so_strategies"], list)

    def test_opportunities_data_structure(self, mock_result):
        exporter = BLMJsonExporter()
        data = json.loads(exporter.export(mock_result))
        opps = data["five_looks"]["opportunities"]
        assert isinstance(opps["span_positions"], list)
        pos = opps["span_positions"][0]
        assert pos["opportunity_name"] == "5G Enterprise"
        assert pos["market_attractiveness"] == 8.5


# =============================================================================
# TXT Formatter tests
# =============================================================================

class TestTxtFormatter:
    def test_format_returns_string(self, mock_result):
        fmt = BLMTxtFormatter()
        text = fmt.format(mock_result)
        assert isinstance(text, str)
        assert len(text) > 500

    def test_header_present(self, mock_result):
        fmt = BLMTxtFormatter()
        text = fmt.format(mock_result)
        assert "BLM Five Looks" in text
        assert "vodafone_germany" in text

    def test_all_sections_present(self, mock_result):
        fmt = BLMTxtFormatter()
        text = fmt.format(mock_result)
        assert "TRENDS" in text
        assert "MARKET" in text
        assert "COMPETITION" in text
        assert "SELF" in text
        assert "SWOT" in text
        assert "OPPORTUNITIES" in text
        assert "PROVENANCE" in text

    def test_key_messages_present(self, mock_result):
        fmt = BLMTxtFormatter()
        text = fmt.format(mock_result)
        assert "Key Message:" in text
        # Should have multiple key messages
        assert text.count("Key Message:") >= 5

    def test_provenance_footer(self, mock_result):
        fmt = BLMTxtFormatter()
        text = fmt.format(mock_result)
        assert "Total data points:" in text
        assert "Q3 FY26 Results" in text

    def test_pest_factors_shown(self, mock_result):
        fmt = BLMTxtFormatter()
        text = fmt.format(mock_result)
        assert "Political" in text
        assert "Gigabit Strategy" in text

    def test_five_forces_shown(self, mock_result):
        fmt = BLMTxtFormatter()
        text = fmt.format(mock_result)
        assert "existing_competitors" in text
        assert "high" in text.lower()

    def test_swot_items_shown(self, mock_result):
        fmt = BLMTxtFormatter()
        text = fmt.format(mock_result)
        assert "Cable infra" in text
        assert "Fiber gap" in text
        assert "5G enterprise" in text

    def test_span_positions_shown(self, mock_result):
        fmt = BLMTxtFormatter()
        text = fmt.format(mock_result)
        assert "5G Enterprise" in text
        assert "grow_invest" in text

    def test_custom_width(self, mock_result):
        fmt = BLMTxtFormatter(width=120)
        text = fmt.format(mock_result)
        assert isinstance(text, str)

    def test_empty_result(self, empty_result):
        fmt = BLMTxtFormatter()
        text = fmt.format(empty_result)
        assert "No trend analysis available" in text
        assert "No SWOT analysis available" in text

    def test_appeals_scores_shown(self, mock_result):
        fmt = BLMTxtFormatter()
        text = fmt.format(mock_result)
        assert "Price" in text
        assert "3.5" in text

    def test_opportunities_priority_shown(self, mock_result):
        fmt = BLMTxtFormatter()
        text = fmt.format(mock_result)
        assert "[P0]" in text
        assert "5G Enterprise" in text


# =============================================================================
# HTML Generator tests
# =============================================================================

class TestHtmlGenerator:
    def test_generate_returns_html_string(self, mock_result):
        gen = BLMHtmlGenerator(VODAFONE_STYLE)
        html = gen.generate(mock_result)
        assert isinstance(html, str)
        assert html.startswith("<!DOCTYPE html>")

    def test_generate_to_file(self, mock_result, tmp_dir):
        gen = BLMHtmlGenerator(VODAFONE_STYLE)
        path = gen.generate(mock_result, f"{tmp_dir}/test.html")
        assert Path(path).exists()
        content = Path(path).read_text(encoding='utf-8')
        assert "<!DOCTYPE html>" in content

    def test_brand_colors_in_css(self, mock_result):
        gen = BLMHtmlGenerator(VODAFONE_STYLE)
        html = gen.generate(mock_result)
        # Vodafone red = (230, 0, 0)
        assert "rgb(230, 0, 0)" in html

    def test_all_sections_present(self, mock_result):
        gen = BLMHtmlGenerator(VODAFONE_STYLE)
        html = gen.generate(mock_result)
        assert "Trends" in html
        assert "Market" in html
        assert "Competition" in html
        assert "Self" in html
        assert "SWOT" in html
        assert "Opportunities" in html
        assert "Provenance" in html

    def test_key_messages_present(self, mock_result):
        gen = BLMHtmlGenerator(VODAFONE_STYLE)
        html = gen.generate(mock_result)
        assert "key-message" in html
        assert "Key Message:" in html

    def test_provenance_section(self, mock_result):
        gen = BLMHtmlGenerator(VODAFONE_STYLE)
        html = gen.generate(mock_result)
        assert "Q3 FY26 Results" in html
        assert "Total Points" in html

    def test_swot_grid(self, mock_result):
        gen = BLMHtmlGenerator(VODAFONE_STYLE)
        html = gen.generate(mock_result)
        assert "swot-grid" in html
        assert "swot-s" in html
        assert "swot-w" in html
        assert "swot-o" in html
        assert "swot-t" in html

    def test_priority_badges(self, mock_result):
        gen = BLMHtmlGenerator(VODAFONE_STYLE)
        html = gen.generate(mock_result)
        assert "priority-badge" in html
        assert "P0" in html

    def test_metric_cards(self, mock_result):
        gen = BLMHtmlGenerator(VODAFONE_STYLE)
        html = gen.generate(mock_result)
        assert "metric-card" in html

    def test_collapsible_sections(self, mock_result):
        gen = BLMHtmlGenerator(VODAFONE_STYLE)
        html = gen.generate(mock_result)
        assert "section-toggle" in html
        assert "section-content" in html

    def test_responsive_css(self, mock_result):
        gen = BLMHtmlGenerator(VODAFONE_STYLE)
        html = gen.generate(mock_result)
        assert "@media" in html

    def test_empty_result(self, empty_result):
        gen = BLMHtmlGenerator()
        html = gen.generate(empty_result)
        assert "No data available" in html

    def test_html_escaping(self):
        """Ensure XSS protection - HTML entities are escaped."""
        prov = ProvenanceStore()
        result = FiveLooksResult(
            target_operator="<script>alert('xss')</script>",
            market="test",
            analysis_period="CQ1_2026",
        )
        gen = BLMHtmlGenerator()
        html = gen.generate(result)
        assert "<script>alert" not in html
        assert "&lt;script&gt;" in html

    def test_appeals_table(self, mock_result):
        gen = BLMHtmlGenerator(VODAFONE_STYLE)
        html = gen.generate(mock_result)
        assert "APPEALS" in html
        assert "Price" in html
        assert "3.5" in html

    def test_five_forces_table(self, mock_result):
        gen = BLMHtmlGenerator(VODAFONE_STYLE)
        html = gen.generate(mock_result)
        assert "Five Forces" in html
        assert "existing_competitors" in html

    def test_span_positions_table(self, mock_result):
        gen = BLMHtmlGenerator(VODAFONE_STYLE)
        html = gen.generate(mock_result)
        assert "SPAN" in html
        assert "5G Enterprise" in html
        assert "8.5" in html

    def test_default_style(self, mock_result):
        gen = BLMHtmlGenerator()
        html = gen.generate(mock_result)
        assert isinstance(html, str)
        assert "<!DOCTYPE html>" in html
