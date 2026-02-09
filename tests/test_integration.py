"""End-to-end integration tests exercising the full analysis pipeline."""

import os
from pathlib import Path

import pandas as pd
import pytest

from src.data.sample import generate_sample_data
from src.data.loader import DataLoader, FinancialDataPreprocessor
from src.data.export import DataExporter
from src.analysis.financial import BudgetAnalyzer
from src.visualization.charts import FinancialChartGenerator
from src.reports.generator import ReportGenerator


@pytest.fixture
def sample_csv(tmp_path):
    """Generate sample data and write to CSV."""
    df = generate_sample_data(n_records=100, seed=99)
    csv_path = tmp_path / "blm_test_data.csv"
    df.to_csv(csv_path, index=False)
    return str(csv_path)


@pytest.fixture
def output_dir(tmp_path):
    out = tmp_path / "output"
    out.mkdir()
    return str(out)


class TestFullPipeline:
    """Test the complete data → analysis → report pipeline."""

    def test_load_analyze_report(self, sample_csv, output_dir):
        # 1. Load
        loader = DataLoader()
        df = loader.load(sample_csv)
        assert len(df) == 100

        # 2. Preprocess
        preprocessor = FinancialDataPreprocessor()
        df = preprocessor.preprocess(df)
        assert "amount" in df.columns

        # 3. Analyze
        analyzer = BudgetAnalyzer(df)
        results = [
            analyzer.summary_statistics(amount_col="amount", group_col="category"),
            analyzer.budget_variance(budget_col="budget", actual_col="actual", category_col="category"),
            analyzer.detect_anomalies(amount_col="amount"),
            analyzer.category_breakdown(amount_col="amount", category_col="category"),
            analyzer.year_over_year(amount_col="amount", year_col="fiscal_year"),
            analyzer.state_comparison(amount_col="amount", state_col="state"),
        ]
        assert len(results) == 6
        for r in results:
            assert r.name
            assert r.summary

        # 4. Generate reports
        report_gen = ReportGenerator(output_dir=output_dir)
        html_path = report_gen.generate_html_report(results)
        text_path = report_gen.generate_text_report(results)
        json_path = report_gen.generate_json_report(results)

        assert Path(html_path).exists()
        assert Path(text_path).exists()
        assert Path(json_path).exists()

        html_content = Path(html_path).read_text()
        assert "Summary Statistics" in html_content
        assert "Year Over Year" in html_content
        assert "State Comparison" in html_content

    def test_export_pipeline(self, sample_csv, output_dir):
        loader = DataLoader()
        df = loader.load(sample_csv)
        preprocessor = FinancialDataPreprocessor()
        df = preprocessor.preprocess(df)

        # Export processed data
        exporter = DataExporter(output_dir=output_dir)
        csv_path = exporter.export_dataframe(df, "processed_data", fmt="csv")
        assert Path(csv_path).exists()

        # Export analysis results
        analyzer = BudgetAnalyzer(df)
        results = [
            analyzer.summary_statistics(amount_col="amount"),
            analyzer.category_breakdown(amount_col="amount", category_col="category"),
        ]
        paths = exporter.export_results(results, prefix="test", fmt="csv")
        assert len(paths) == 2
        for p in paths:
            assert Path(p).exists()

        # Export summary
        summary_path = exporter.export_summary(results, filename="test_summary")
        assert Path(summary_path).exists()
        summary_df = pd.read_csv(summary_path)
        assert "analysis" in summary_df.columns
        assert "metric" in summary_df.columns

    def test_chart_generation(self, sample_csv, output_dir):
        loader = DataLoader()
        df = loader.load(sample_csv)
        preprocessor = FinancialDataPreprocessor()
        df = preprocessor.preprocess(df)

        analyzer = BudgetAnalyzer(df)
        chart_gen = FinancialChartGenerator(output_dir=output_dir)

        # Category pie chart
        breakdown = analyzer.category_breakdown(amount_col="amount", category_col="category")
        pie_path = chart_gen.category_pie_chart(breakdown.details)
        assert Path(pie_path).exists()

        # Top N bar chart
        bar_path = chart_gen.top_n_bar_chart(breakdown.details, n=5)
        assert Path(bar_path).exists()

        # Budget variance chart
        variance = analyzer.budget_variance(
            budget_col="budget", actual_col="actual", category_col="category"
        )
        var_path = chart_gen.budget_variance_chart(variance.details)
        assert Path(var_path).exists()
