"""Tests for sample data generation."""

import pandas as pd
import pytest

from src.data.sample import generate_sample_data, BLM_PROGRAMS, BLM_STATES


class TestGenerateSampleData:
    def test_returns_dataframe(self):
        df = generate_sample_data()
        assert isinstance(df, pd.DataFrame)

    def test_default_record_count(self):
        df = generate_sample_data()
        assert len(df) == 200

    def test_custom_record_count(self):
        df = generate_sample_data(n_records=50)
        assert len(df) == 50

    def test_required_columns(self):
        df = generate_sample_data()
        expected_cols = {
            "date", "fiscal_year", "state", "category",
            "program", "budget", "actual", "amount",
            "revenue", "description",
        }
        assert expected_cols.issubset(set(df.columns))

    def test_categories_are_valid(self):
        df = generate_sample_data()
        assert all(cat in BLM_PROGRAMS for cat in df["category"].unique())

    def test_states_are_valid(self):
        df = generate_sample_data()
        assert all(state in BLM_STATES for state in df["state"].unique())

    def test_reproducible_with_seed(self):
        df1 = generate_sample_data(seed=123)
        df2 = generate_sample_data(seed=123)
        pd.testing.assert_frame_equal(df1, df2)

    def test_budget_amounts_positive(self):
        df = generate_sample_data()
        assert (df["budget"] > 0).all()

    def test_fiscal_years_in_range(self):
        df = generate_sample_data(start_year=2020, end_year=2024)
        assert df["fiscal_year"].min() >= 2020
        assert df["fiscal_year"].max() <= 2024
