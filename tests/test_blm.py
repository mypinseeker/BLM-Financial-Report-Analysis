"""Tests for BLM Strategic Analysis module.

Tests cover:
- Telecom data generation
- Five Looks (五看) analysis
- Three Decisions (三定) strategy
- Report generation
- CLI commands
"""

import json
import tempfile
from pathlib import Path

import pandas as pd
import pytest
from click.testing import CliRunner

from src.blm.telecom_data import (
    GLOBAL_OPERATORS,
    BUSINESS_SEGMENTS,
    COMPETITIVE_DIMENSIONS,
    OperatorProfile,
    MarketContext,
    TelecomDataGenerator,
    generate_sample_data,
)
from src.blm.five_looks import InsightResult, FiveLooksAnalyzer
from src.blm.three_decisions import (
    StrategyItem,
    StrategyResult,
    ThreeDecisionsEngine,
    generate_blm_strategy,
)
from src.blm.report_generator import BLMReportGenerator
from src.blm.cli import blm_cli


# =============================================================================
# Telecom Data Tests
# =============================================================================

class TestTelecomData:
    """Tests for telecom data models and generator."""

    def test_global_operators_registry(self):
        """Test that global operators registry contains expected entries."""
        assert len(GLOBAL_OPERATORS) >= 20
        assert "China Mobile" in GLOBAL_OPERATORS
        assert "Vodafone" in GLOBAL_OPERATORS
        assert "MTN" in GLOBAL_OPERATORS
        assert "AT&T" in GLOBAL_OPERATORS

    def test_global_operators_structure(self):
        """Test that operator entries have required fields."""
        for name, info in GLOBAL_OPERATORS.items():
            assert "country" in info
            assert "region" in info
            assert "type" in info

    def test_business_segments(self):
        """Test that business segments are defined."""
        assert len(BUSINESS_SEGMENTS) >= 5
        assert "Mobile Services" in BUSINESS_SEGMENTS
        assert "Enterprise/B2B" in BUSINESS_SEGMENTS

    def test_competitive_dimensions(self):
        """Test that competitive dimensions are defined."""
        assert len(COMPETITIVE_DIMENSIONS) >= 8
        assert "Network Coverage" in COMPETITIVE_DIMENSIONS
        assert "Brand Strength" in COMPETITIVE_DIMENSIONS

    def test_operator_profile_from_registry(self):
        """Test creating OperatorProfile from registry."""
        profile = OperatorProfile.from_registry("China Mobile")
        assert profile.name == "China Mobile"
        assert profile.country == "China"
        assert profile.region == "APAC"

    def test_operator_profile_unknown(self):
        """Test error for unknown operator."""
        with pytest.raises(ValueError, match="Unknown operator"):
            OperatorProfile.from_registry("Unknown Operator")

    def test_market_context(self):
        """Test MarketContext dataclass."""
        ctx = MarketContext(
            countries=["China"],
            analysis_period="2023Q1-2024Q4",
            target_operator="China Mobile",
            competitors=["China Telecom", "China Unicom"],
        )
        assert ctx.target_operator == "China Mobile"
        assert len(ctx.competitors) == 2

    def test_telecom_data_generator(self):
        """Test TelecomDataGenerator produces expected data."""
        generator = TelecomDataGenerator(seed=42)
        data = generator.generate_dataset(
            ["China Mobile", "China Telecom"],
            n_quarters=4,
        )

        assert "market" in data
        assert "financial" in data
        assert "competitive" in data
        assert "macro" in data
        assert "segments" in data
        assert "customer" in data

    def test_generated_market_data(self):
        """Test market data structure."""
        generator = TelecomDataGenerator(seed=42)
        data = generator.generate_dataset(["Vodafone", "MTN"], n_quarters=4)

        market_df = data["market"]
        assert not market_df.empty
        assert "quarter" in market_df.columns
        assert "operator" in market_df.columns
        assert "subscribers_million" in market_df.columns
        assert "market_share_pct" in market_df.columns
        assert "5g_users_pct" in market_df.columns

    def test_generated_financial_data(self):
        """Test financial data structure."""
        generator = TelecomDataGenerator(seed=42)
        data = generator.generate_dataset(["AT&T", "Verizon"], n_quarters=4)

        fin_df = data["financial"]
        assert not fin_df.empty
        assert "revenue_billion_usd" in fin_df.columns
        assert "profit_margin_pct" in fin_df.columns
        assert "arpu_usd" in fin_df.columns

    def test_generated_competitive_data(self):
        """Test competitive data structure."""
        generator = TelecomDataGenerator(seed=42)
        data = generator.generate_dataset(["Orange", "Telefonica"], n_quarters=4)

        comp_df = data["competitive"]
        assert not comp_df.empty
        assert "dimension" in comp_df.columns
        assert "score" in comp_df.columns
        # Should have scores for all dimensions
        dims = comp_df["dimension"].unique()
        assert len(dims) == len(COMPETITIVE_DIMENSIONS)

    def test_generate_sample_data_convenience(self):
        """Test generate_sample_data convenience function."""
        data = generate_sample_data()
        assert len(data) == 6  # All data types
        # Default is China Big 3
        operators = data["market"]["operator"].unique()
        assert "China Mobile" in operators

    def test_generate_sample_data_custom_operators(self):
        """Test generate_sample_data with custom operators."""
        data = generate_sample_data(
            operators=["Vodafone", "MTN"],
            n_quarters=4,
            seed=123,
        )
        operators = data["market"]["operator"].unique()
        assert len(operators) == 2
        assert "Vodafone" in operators
        assert "MTN" in operators

    def test_data_reproducibility(self):
        """Test that same seed produces same data."""
        data1 = generate_sample_data(seed=42)
        data2 = generate_sample_data(seed=42)

        pd.testing.assert_frame_equal(data1["market"], data2["market"])


# =============================================================================
# Five Looks Tests
# =============================================================================

class TestFiveLooks:
    """Tests for Five Looks (五看) analysis."""

    @pytest.fixture
    def sample_data(self):
        """Generate sample data for testing."""
        return generate_sample_data(
            operators=["China Mobile", "China Telecom", "China Unicom"],
            n_quarters=8,
        )

    @pytest.fixture
    def analyzer(self, sample_data):
        """Create analyzer instance."""
        return FiveLooksAnalyzer(
            sample_data,
            target_operator="China Mobile",
            competitors=["China Telecom", "China Unicom"],
        )

    def test_insight_result_dataclass(self):
        """Test InsightResult dataclass."""
        result = InsightResult(
            category="market",
            title="Market Insight",
            findings=["Finding 1", "Finding 2"],
            metrics={"key": 100},
            data=pd.DataFrame(),
            recommendations=["Rec 1"],
        )
        assert result.category == "market"
        assert len(result.findings) == 2

    def test_look_at_market(self, analyzer):
        """Test market analysis (看市场)."""
        result = analyzer.look_at_market()

        assert result.category == "market"
        assert "市场" in result.title
        assert len(result.findings) > 0
        assert "total_subscribers_million" in result.metrics
        assert "5g_penetration_pct" in result.metrics
        assert len(result.recommendations) > 0

    def test_look_at_self(self, analyzer):
        """Test self analysis (看自己)."""
        result = analyzer.look_at_self()

        assert result.category == "self"
        assert len(result.findings) > 0
        assert "market_share_pct" in result.metrics or "revenue_billion_usd" in result.metrics
        assert len(result.recommendations) > 0

    def test_look_at_competitors(self, analyzer):
        """Test competitor analysis (看对手)."""
        result = analyzer.look_at_competitors()

        assert result.category == "competitor"
        assert len(result.findings) > 0
        # Should have data for each competitor
        assert not result.data.empty

    def test_look_at_competitors_no_competitors(self, sample_data):
        """Test competitor analysis with no competitors specified."""
        analyzer = FiveLooksAnalyzer(sample_data, "China Mobile", competitors=[])
        result = analyzer.look_at_competitors()

        assert "未指定" in result.findings[0] or len(result.findings) == 1

    def test_look_at_macro(self, analyzer):
        """Test macro environment analysis (看宏观)."""
        result = analyzer.look_at_macro()

        assert result.category == "macro"
        assert len(result.findings) > 0
        assert "avg_gdp_growth_pct" in result.metrics or "avg_5g_coverage_pct" in result.metrics

    def test_look_at_opportunities(self, analyzer):
        """Test opportunity analysis (看机会)."""
        result = analyzer.look_at_opportunities()

        assert result.category == "opportunity"
        assert len(result.findings) > 0
        assert "opportunities_count" in result.metrics

    def test_run_full_analysis(self, analyzer):
        """Test full Five Looks analysis."""
        results = analyzer.run_full_analysis()

        assert len(results) == 5
        assert "market" in results
        assert "self" in results
        assert "competitor" in results
        assert "macro" in results
        assert "opportunity" in results

        for key, result in results.items():
            assert isinstance(result, InsightResult)


# =============================================================================
# Three Decisions Tests
# =============================================================================

class TestThreeDecisions:
    """Tests for Three Decisions (三定) strategy."""

    @pytest.fixture
    def five_looks_results(self):
        """Generate Five Looks results for testing."""
        data = generate_sample_data(
            operators=["Vodafone", "MTN", "Orange"],
            n_quarters=8,
        )
        analyzer = FiveLooksAnalyzer(data, "Vodafone", ["MTN", "Orange"])
        return analyzer.run_full_analysis()

    @pytest.fixture
    def engine(self, five_looks_results):
        """Create strategy engine instance."""
        return ThreeDecisionsEngine(five_looks_results, "Vodafone")

    def test_strategy_item_dataclass(self):
        """Test StrategyItem dataclass."""
        item = StrategyItem(
            name="Test Strategy",
            description="Description",
            priority="P0",
            category="growth",
            timeline="Q1-Q2",
            kpis=["KPI 1", "KPI 2"],
        )
        assert item.name == "Test Strategy"
        assert item.priority == "P0"
        assert len(item.kpis) == 2

    def test_strategy_result_dataclass(self):
        """Test StrategyResult dataclass."""
        result = StrategyResult(
            decision_type="strategy",
            title="Define Strategy",
            summary="Summary text",
            items=[],
            metrics={"count": 5},
        )
        assert result.decision_type == "strategy"
        assert result.title == "Define Strategy"

    def test_define_strategy(self, engine):
        """Test strategy definition (定策略)."""
        result = engine.define_strategy()

        assert result.decision_type == "strategy"
        assert len(result.items) >= 3
        assert result.summary
        assert "total_strategies" in result.metrics

        # Check priorities are valid
        for item in result.items:
            assert item.priority in ("P0", "P1", "P2")

    def test_define_key_tasks(self, engine):
        """Test key tasks definition (定重点工作)."""
        result = engine.define_key_tasks()

        assert result.decision_type == "key_tasks"
        assert len(result.items) >= 5
        assert result.summary
        assert "total_tasks" in result.metrics

    def test_define_execution(self, engine):
        """Test execution planning (定执行)."""
        result = engine.define_execution()

        assert result.decision_type == "execution"
        assert len(result.items) >= 5
        assert result.summary
        assert "total_milestones" in result.metrics
        assert "governance_items" in result.metrics

    def test_run_full_strategy(self, engine):
        """Test full Three Decisions strategy."""
        results = engine.run_full_strategy()

        assert len(results) == 3
        assert "strategy" in results
        assert "key_tasks" in results
        assert "execution" in results

        for key, result in results.items():
            assert isinstance(result, StrategyResult)

    def test_generate_blm_strategy_convenience(self):
        """Test generate_blm_strategy convenience function."""
        data = generate_sample_data(["AT&T", "Verizon"])
        results = generate_blm_strategy(
            data,
            target_operator="AT&T",
            competitors=["Verizon"],
        )

        assert "five_looks" in results
        assert "three_decisions" in results
        assert results["target_operator"] == "AT&T"
        assert "Verizon" in results["competitors"]


# =============================================================================
# Report Generator Tests
# =============================================================================

class TestBLMReportGenerator:
    """Tests for BLM report generation."""

    @pytest.fixture
    def analysis_results(self):
        """Generate analysis results for testing."""
        data = generate_sample_data(["China Mobile", "China Telecom"])
        return generate_blm_strategy(data, "China Mobile", ["China Telecom"])

    @pytest.fixture
    def report_gen(self, tmp_path):
        """Create report generator with temp output dir."""
        return BLMReportGenerator(output_dir=str(tmp_path))

    def test_generate_html_report(self, report_gen, analysis_results, tmp_path):
        """Test HTML report generation."""
        path = report_gen.generate_html_report(
            five_looks=analysis_results["five_looks"],
            three_decisions=analysis_results["three_decisions"],
            target_operator="China Mobile",
            competitors=["China Telecom"],
        )

        assert Path(path).exists()
        content = Path(path).read_text(encoding="utf-8")
        assert "China Mobile" in content
        assert "五看分析" in content or "Five Looks" in content
        assert "三定" in content or "Three Decisions" in content

    def test_generate_text_report(self, report_gen, analysis_results, tmp_path):
        """Test text report generation."""
        path = report_gen.generate_text_report(
            five_looks=analysis_results["five_looks"],
            three_decisions=analysis_results["three_decisions"],
            target_operator="China Mobile",
            competitors=["China Telecom"],
        )

        assert Path(path).exists()
        content = Path(path).read_text(encoding="utf-8")
        assert "China Mobile" in content
        assert "FIVE LOOKS" in content or "五看" in content

    def test_generate_json_report(self, report_gen, analysis_results, tmp_path):
        """Test JSON report generation."""
        path = report_gen.generate_json_report(
            five_looks=analysis_results["five_looks"],
            three_decisions=analysis_results["three_decisions"],
            target_operator="China Mobile",
            competitors=["China Telecom"],
        )

        assert Path(path).exists()
        content = Path(path).read_text(encoding="utf-8")
        data = json.loads(content)

        assert data["target_operator"] == "China Mobile"
        assert "five_looks" in data
        assert "three_decisions" in data
        assert "market" in data["five_looks"]
        assert "strategy" in data["three_decisions"]

    def test_generate_executive_summary(self, report_gen, analysis_results):
        """Test executive summary generation."""
        summary = report_gen.generate_executive_summary(
            five_looks=analysis_results["five_looks"],
            three_decisions=analysis_results["three_decisions"],
            target_operator="China Mobile",
        )

        assert "China Mobile" in summary
        assert len(summary) > 100


# =============================================================================
# CLI Tests
# =============================================================================

class TestBLMCLI:
    """Tests for BLM CLI commands."""

    @pytest.fixture
    def runner(self):
        """Create CLI test runner."""
        return CliRunner()

    def test_list_operators(self, runner):
        """Test list-operators command."""
        result = runner.invoke(blm_cli, ["list-operators"])
        assert result.exit_code == 0
        assert "China Mobile" in result.output
        assert "Vodafone" in result.output

    def test_analyze_basic(self, runner, tmp_path):
        """Test analyze command."""
        result = runner.invoke(blm_cli, [
            "analyze",
            "-t", "China Mobile",
            "-c", "China Telecom",
            "-o", str(tmp_path),
            "-f", "text",
            "-q", "4",
        ])

        assert result.exit_code == 0
        assert "BLM Strategic Analysis" in result.output
        assert "Five Looks" in result.output
        assert "Three Decisions" in result.output

    def test_analyze_all_formats(self, runner, tmp_path):
        """Test analyze command with all formats."""
        result = runner.invoke(blm_cli, [
            "analyze",
            "-t", "Vodafone",
            "-c", "MTN",
            "-o", str(tmp_path),
            "-f", "all",
            "-q", "4",
        ])

        assert result.exit_code == 0
        assert "HTML report" in result.output
        assert "Text report" in result.output
        assert "JSON report" in result.output

    def test_compare(self, runner, tmp_path):
        """Test compare command."""
        result = runner.invoke(blm_cli, [
            "compare",
            "-o", "Vodafone,MTN,Orange",
            "--output-dir", str(tmp_path),
            "-q", "4",
        ])

        assert result.exit_code == 0
        assert "Multi-Operator Comparison" in result.output
        assert "Market Position" in result.output

    def test_generate_data(self, runner, tmp_path):
        """Test generate-data command."""
        output_file = tmp_path / "test_data.json"
        result = runner.invoke(blm_cli, [
            "generate-data",
            "-o", "AT&T,Verizon",
            "-q", "4",
            "--output", str(output_file),
        ])

        assert result.exit_code == 0
        assert output_file.exists()

        data = json.loads(output_file.read_text())
        assert "market" in data
        assert "_meta" in data

    def test_five_looks_command(self, runner):
        """Test five-looks command."""
        result = runner.invoke(blm_cli, [
            "five-looks",
            "-t", "MTN",
            "-c", "Airtel Africa",
            "-l", "market",
        ])

        assert result.exit_code == 0
        assert "Five Looks Analysis" in result.output
        assert "市场" in result.output or "Market" in result.output

    def test_five_looks_all(self, runner):
        """Test five-looks command with all looks."""
        result = runner.invoke(blm_cli, [
            "five-looks",
            "-t", "Orange",
            "-l", "all",
        ])

        assert result.exit_code == 0
        # Should have all 5 looks
        assert "market" in result.output.lower() or "市场" in result.output

    def test_three_decisions_command(self, runner):
        """Test three-decisions command."""
        result = runner.invoke(blm_cli, [
            "three-decisions",
            "-t", "Telefonica",
            "-d", "strategy",
        ])

        assert result.exit_code == 0
        assert "Three Decisions Strategy" in result.output

    def test_three_decisions_all(self, runner):
        """Test three-decisions command with all decisions."""
        result = runner.invoke(blm_cli, [
            "three-decisions",
            "-t", "Deutsche Telekom",
            "-d", "all",
        ])

        assert result.exit_code == 0
        assert "Strategy" in result.output or "策略" in result.output


# =============================================================================
# Integration Tests
# =============================================================================

class TestBLMIntegration:
    """Integration tests for full BLM analysis workflow."""

    def test_full_workflow_china_operators(self):
        """Test complete workflow for China operators."""
        # Generate data
        data = generate_sample_data(
            operators=["China Mobile", "China Telecom", "China Unicom"],
            n_quarters=8,
            seed=42,
        )

        # Run analysis
        results = generate_blm_strategy(
            data,
            target_operator="China Mobile",
            competitors=["China Telecom", "China Unicom"],
        )

        # Verify Five Looks
        five_looks = results["five_looks"]
        assert all(key in five_looks for key in ["market", "self", "competitor", "macro", "opportunity"])

        # Verify Three Decisions
        three_decisions = results["three_decisions"]
        assert all(key in three_decisions for key in ["strategy", "key_tasks", "execution"])

        # Verify strategies have valid priorities
        for decision_key, decision in three_decisions.items():
            for item in decision.items:
                assert item.priority in ("P0", "P1", "P2")

    def test_full_workflow_global_operators(self):
        """Test workflow with global operators from different regions."""
        operators = ["Vodafone", "MTN", "Orange", "Telefonica"]
        data = generate_sample_data(operators=operators, n_quarters=4)

        for target in operators:
            competitors = [op for op in operators if op != target]
            results = generate_blm_strategy(data, target, competitors)

            assert results["target_operator"] == target
            assert len(results["five_looks"]) == 5
            assert len(results["three_decisions"]) == 3

    def test_report_generation_workflow(self, tmp_path):
        """Test complete report generation workflow."""
        data = generate_sample_data(["AT&T", "Verizon", "T-Mobile US"])
        results = generate_blm_strategy(data, "AT&T", ["Verizon", "T-Mobile US"])

        report_gen = BLMReportGenerator(output_dir=str(tmp_path))

        # Generate all report formats
        html_path = report_gen.generate_html_report(
            results["five_looks"], results["three_decisions"], "AT&T", ["Verizon", "T-Mobile US"],
        )
        text_path = report_gen.generate_text_report(
            results["five_looks"], results["three_decisions"], "AT&T", ["Verizon", "T-Mobile US"],
        )
        json_path = report_gen.generate_json_report(
            results["five_looks"], results["three_decisions"], "AT&T", ["Verizon", "T-Mobile US"],
        )

        # Verify all reports exist
        assert Path(html_path).exists()
        assert Path(text_path).exists()
        assert Path(json_path).exists()

        # Verify JSON is valid and contains expected structure
        json_data = json.loads(Path(json_path).read_text())
        assert json_data["target_operator"] == "AT&T"
        assert len(json_data["five_looks"]) == 5
        assert len(json_data["three_decisions"]) == 3
