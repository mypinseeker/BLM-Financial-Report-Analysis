"""Tests for the visualization/charts module."""

from pathlib import Path

import pandas as pd
import pytest

from src.visualization.charts import FinancialChartGenerator


@pytest.fixture
def chart_gen(tmp_path):
    return FinancialChartGenerator(output_dir=str(tmp_path))


@pytest.fixture
def category_data():
    return pd.DataFrame({
        "category": ["Wildlife", "Forestry", "Mining", "Fire", "Energy"],
        "total": [5000, 4000, 3000, 2000, 1000],
    })


@pytest.fixture
def trend_data():
    return pd.DataFrame({
        "date": pd.to_datetime(["2020-12-31", "2021-12-31", "2022-12-31", "2023-12-31"]),
        "total": [10000, 12000, 11000, 15000],
    })


@pytest.fixture
def variance_data():
    return pd.DataFrame({
        "category": ["Wildlife", "Forestry", "Mining"],
        "total_budget": [5000, 4000, 3000],
        "total_actual": [4500, 4500, 2800],
    })


@pytest.fixture
def anomaly_data():
    return pd.DataFrame({
        "amount": [100, 110, 105, 95, 1000, 98, 102],
        "z_score": [0.1, 0.3, 0.2, -0.1, 5.0, -0.05, 0.15],
        "is_anomaly": [False, False, False, False, True, False, False],
    })


class TestFinancialChartGenerator:
    def test_category_pie_chart(self, chart_gen, category_data):
        path = chart_gen.category_pie_chart(category_data)
        assert Path(path).exists()
        assert path.endswith(".png")

    def test_category_pie_chart_many_categories(self, chart_gen):
        data = pd.DataFrame({
            "category": [f"Cat_{i}" for i in range(15)],
            "total": list(range(1500, 0, -100)),
        })
        path = chart_gen.category_pie_chart(data)
        assert Path(path).exists()

    def test_trend_chart(self, chart_gen, trend_data):
        path = chart_gen.trend_chart(trend_data)
        assert Path(path).exists()
        assert path.endswith(".png")

    def test_budget_variance_chart(self, chart_gen, variance_data):
        path = chart_gen.budget_variance_chart(variance_data)
        assert Path(path).exists()
        assert path.endswith(".png")

    def test_anomaly_scatter(self, chart_gen, anomaly_data):
        path = chart_gen.anomaly_scatter(anomaly_data)
        assert Path(path).exists()
        assert path.endswith(".png")

    def test_top_n_bar_chart(self, chart_gen, category_data):
        path = chart_gen.top_n_bar_chart(category_data, n=3)
        assert Path(path).exists()
        assert path.endswith(".png")

    def test_heatmap(self, chart_gen):
        data = pd.DataFrame({
            "category": ["A", "A", "B", "B"],
            "fiscal_year": [2022, 2023, 2022, 2023],
            "amount": [100, 150, 200, 180],
        })
        path = chart_gen.heatmap(data)
        assert Path(path).exists()
        assert path.endswith(".png")

    def test_custom_filename(self, chart_gen, category_data):
        path = chart_gen.category_pie_chart(category_data, filename="custom_chart.png")
        assert Path(path).name == "custom_chart.png"
        assert Path(path).exists()
