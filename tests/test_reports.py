"""Tests for report generation module."""

import json
from pathlib import Path

import pandas as pd
import pytest

from src.analysis.financial import AnalysisResult
from src.reports.generator import ReportGenerator


@pytest.fixture
def sample_results():
    """Create sample analysis results for testing."""
    return [
        AnalysisResult(
            name="summary_statistics",
            summary={"total": 10000.0, "mean": 2000.0, "count": 5},
            details=pd.DataFrame({
                "metric": ["count", "total", "mean"],
                "value": [5, 10000.0, 2000.0],
            }),
        ),
        AnalysisResult(
            name="budget_variance",
            summary={
                "total_budget": 10200.0,
                "total_actual": 10000.0,
                "total_variance": -200.0,
            },
            details=pd.DataFrame({
                "category": ["Wildlife", "Forestry"],
                "total_budget": [2600, 4400],
                "total_actual": [2500, 4500],
            }),
        ),
    ]


@pytest.fixture
def report_gen(tmp_path):
    return ReportGenerator(output_dir=str(tmp_path))


class TestReportGenerator:
    def test_generate_html_report(self, report_gen, sample_results):
        path = report_gen.generate_html_report(sample_results)
        assert Path(path).exists()
        content = Path(path).read_text()
        assert "BLM Financial Analysis Report" in content
        assert "Summary Statistics" in content

    def test_generate_text_report(self, report_gen, sample_results):
        path = report_gen.generate_text_report(sample_results)
        assert Path(path).exists()
        content = Path(path).read_text()
        assert "SUMMARY STATISTICS" in content
        assert "BUDGET VARIANCE" in content

    def test_generate_json_report(self, report_gen, sample_results):
        path = report_gen.generate_json_report(sample_results)
        assert Path(path).exists()
        data = json.loads(Path(path).read_text())
        assert data["title"] == "BLM Financial Analysis Report"
        assert len(data["results"]) == 2

    def test_html_report_custom_title(self, report_gen, sample_results):
        path = report_gen.generate_html_report(
            sample_results, title="Custom Report Title"
        )
        content = Path(path).read_text()
        assert "Custom Report Title" in content

    def test_empty_results(self, report_gen):
        path = report_gen.generate_html_report([])
        assert Path(path).exists()
