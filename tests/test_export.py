"""Tests for data export module."""

from pathlib import Path

import pandas as pd
import pytest

from src.analysis.financial import AnalysisResult
from src.data.export import DataExporter


@pytest.fixture
def exporter(tmp_path):
    return DataExporter(output_dir=str(tmp_path))


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "category": ["A", "B", "C"],
        "amount": [100, 200, 300],
    })


@pytest.fixture
def sample_results():
    return [
        AnalysisResult(
            name="test_analysis",
            summary={"total": 600, "count": 3},
            details=pd.DataFrame({"cat": ["A", "B"], "val": [100, 200]}),
        ),
        AnalysisResult(
            name="empty_analysis",
            summary={"total": 0},
            details=pd.DataFrame(),
        ),
    ]


class TestDataExporter:
    def test_export_csv(self, exporter, sample_df):
        path = exporter.export_dataframe(sample_df, "test_output", fmt="csv")
        assert Path(path).exists()
        loaded = pd.read_csv(path)
        assert len(loaded) == 3

    def test_export_excel(self, exporter, sample_df):
        path = exporter.export_dataframe(sample_df, "test_output", fmt="excel")
        assert Path(path).exists()
        assert path.endswith(".xlsx")

    def test_export_unsupported_format(self, exporter, sample_df):
        with pytest.raises(ValueError, match="Unsupported export format"):
            exporter.export_dataframe(sample_df, "test", fmt="parquet")

    def test_export_results(self, exporter, sample_results):
        paths = exporter.export_results(sample_results, prefix="res", fmt="csv")
        # Only non-empty results should be exported
        assert len(paths) == 1
        assert Path(paths[0]).exists()

    def test_export_summary(self, exporter, sample_results):
        path = exporter.export_summary(sample_results, filename="summary")
        assert Path(path).exists()
        df = pd.read_csv(path)
        assert "analysis" in df.columns
        assert "metric" in df.columns
        assert "value" in df.columns
        assert len(df) == 3  # total + count from first + total from second
