"""Tests for financial analysis module."""

import numpy as np
import pandas as pd
import pytest

from src.analysis.financial import BudgetAnalyzer, AnalysisResult


@pytest.fixture
def sample_financial_data():
    """Create sample financial data for testing."""
    return pd.DataFrame({
        "category": ["Wildlife", "Forestry", "Mining", "Wildlife", "Forestry"],
        "amount": [1000.0, 2000.0, 3000.0, 1500.0, 2500.0],
        "budget": [1200.0, 1800.0, 3200.0, 1400.0, 2600.0],
        "actual": [1000.0, 2000.0, 3000.0, 1500.0, 2500.0],
        "date": pd.to_datetime(["2021-01-01", "2022-01-01", "2023-01-01", "2024-01-01", "2025-01-01"]),
    })


@pytest.fixture
def analyzer(sample_financial_data):
    return BudgetAnalyzer(sample_financial_data)


class TestAnalysisResult:
    def test_to_dict(self):
        result = AnalysisResult(
            name="test",
            summary={"key": "value"},
            details=pd.DataFrame({"a": [1, 2]}),
        )
        d = result.to_dict()
        assert d["name"] == "test"
        assert d["summary"] == {"key": "value"}
        assert len(d["details"]) == 2


class TestBudgetAnalyzer:
    def test_summary_statistics_basic(self, analyzer):
        result = analyzer.summary_statistics(amount_col="amount")
        assert result.name == "summary_statistics"
        assert result.summary["total"] == 10000.0
        assert result.summary["count"] == 5

    def test_summary_statistics_grouped(self, analyzer):
        result = analyzer.summary_statistics(amount_col="amount", group_col="category")
        assert result.summary["groups"] == 3
        assert "largest_group" in result.summary

    def test_summary_statistics_missing_column(self, analyzer):
        with pytest.raises(ValueError, match="not found"):
            analyzer.summary_statistics(amount_col="nonexistent")

    def test_budget_variance(self, analyzer):
        result = analyzer.budget_variance(budget_col="budget", actual_col="actual")
        assert result.name == "budget_variance"
        assert "total_budget" in result.summary
        assert "total_actual" in result.summary
        assert "total_variance" in result.summary
        assert "items_over_budget" in result.summary

    def test_budget_variance_with_category(self, analyzer):
        result = analyzer.budget_variance(
            budget_col="budget", actual_col="actual", category_col="category"
        )
        assert not result.details.empty

    def test_budget_variance_missing_column(self, analyzer):
        with pytest.raises(ValueError, match="not found"):
            analyzer.budget_variance(budget_col="nonexistent")

    def test_trend_analysis(self, analyzer):
        result = analyzer.trend_analysis(amount_col="amount", date_col="date", freq="YE")
        assert result.name == "trend_analysis"
        assert "trend_direction" in result.summary
        assert result.summary["periods"] > 0

    def test_detect_anomalies(self, analyzer):
        result = analyzer.detect_anomalies(amount_col="amount")
        assert result.name == "anomaly_detection"
        assert "anomalies_found" in result.summary
        assert "total_records" in result.summary

    def test_detect_anomalies_with_outlier(self):
        data = pd.DataFrame({"amount": [100, 100, 100, 100, 100, 10000]})
        analyzer = BudgetAnalyzer(data)
        result = analyzer.detect_anomalies(amount_col="amount", threshold=2.0)
        assert result.summary["anomalies_found"] >= 1

    def test_detect_anomalies_no_variance(self):
        data = pd.DataFrame({"amount": [100, 100, 100]})
        analyzer = BudgetAnalyzer(data)
        result = analyzer.detect_anomalies(amount_col="amount")
        assert result.summary["anomalies_found"] == 0

    def test_category_breakdown(self, analyzer):
        result = analyzer.category_breakdown(amount_col="amount", category_col="category")
        assert result.name == "category_breakdown"
        assert result.summary["total_categories"] == 3
        assert "percentage" in result.details.columns

    def test_category_breakdown_missing_column(self, analyzer):
        with pytest.raises(ValueError, match="not found"):
            analyzer.category_breakdown(amount_col="amount", category_col="nonexistent")
