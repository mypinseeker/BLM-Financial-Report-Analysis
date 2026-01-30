"""Tests for data loading and preprocessing module."""

import os
import tempfile

import pandas as pd
import pytest

from src.data.loader import DataLoader, FinancialDataPreprocessor


@pytest.fixture
def sample_csv(tmp_path):
    """Create a sample CSV file for testing."""
    csv_path = tmp_path / "test_data.csv"
    df = pd.DataFrame({
        "Category": ["Wildlife", "Forestry", "Mining"],
        "Amount": ["$1,234.56", "$2,345.67", "$3,456.78"],
        "Budget": ["$1,000.00", "$2,500.00", "$3,000.00"],
        "Date": ["2023-01-15", "2023-06-20", "2023-12-01"],
    })
    df.to_csv(csv_path, index=False)
    return str(csv_path)


@pytest.fixture
def sample_excel(tmp_path):
    """Create a sample Excel file for testing."""
    xlsx_path = tmp_path / "test_data.xlsx"
    df = pd.DataFrame({
        "Program": ["Fire Mgmt", "Range Mgmt"],
        "Spending": [500000, 750000],
        "Fiscal Year": [2023, 2023],
    })
    df.to_excel(xlsx_path, index=False, engine="openpyxl")
    return str(xlsx_path)


class TestDataLoader:
    def test_load_csv(self, sample_csv):
        loader = DataLoader()
        df = loader.load(sample_csv)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        # Columns should be standardized to snake_case
        assert "category" in df.columns
        assert "amount" in df.columns

    def test_load_excel(self, sample_excel):
        loader = DataLoader()
        df = loader.load(sample_excel)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "program" in df.columns

    def test_load_nonexistent_file(self):
        loader = DataLoader()
        with pytest.raises(FileNotFoundError):
            loader.load("/nonexistent/file.csv")

    def test_load_unsupported_format(self, tmp_path):
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("hello")
        loader = DataLoader()
        with pytest.raises(ValueError, match="Unsupported file format"):
            loader.load(str(txt_file))

    def test_standardize_columns(self):
        df = pd.DataFrame({"Column Name": [1], "Another-Col!": [2], "  Spaces  ": [3]})
        result = DataLoader._standardize_columns(df)
        assert "column_name" in result.columns
        assert "anothercol" in result.columns
        assert "spaces" in result.columns


class TestFinancialDataPreprocessor:
    def test_preprocess_cleans_strings(self):
        df = pd.DataFrame({"name": ["  Alice  ", "  Bob  ", None]})
        preprocessor = FinancialDataPreprocessor()
        result = preprocessor.preprocess(df)
        assert result["name"].iloc[0] == "Alice"
        assert result["name"].iloc[1] == "Bob"

    def test_preprocess_parses_currency(self):
        df = pd.DataFrame({"amount": ["$1,234.56", "$2,345.67", "($100.00)"]})
        preprocessor = FinancialDataPreprocessor()
        result = preprocessor.preprocess(df)
        assert result["amount"].iloc[0] == pytest.approx(1234.56)
        assert result["amount"].iloc[1] == pytest.approx(2345.67)
        assert result["amount"].iloc[2] == pytest.approx(-100.00)

    def test_preprocess_drops_empty(self):
        df = pd.DataFrame({
            "a": [1, None, 3],
            "b": [None, None, None],
            "c": [4, 5, 6],
        })
        preprocessor = FinancialDataPreprocessor()
        result = preprocessor.preprocess(df)
        assert "b" not in result.columns  # all-null column dropped

    def test_preprocess_parses_dates(self):
        df = pd.DataFrame({"date": ["2023-01-15", "2023-06-20"]})
        preprocessor = FinancialDataPreprocessor()
        result = preprocessor.preprocess(df)
        assert pd.api.types.is_datetime64_any_dtype(result["date"])
