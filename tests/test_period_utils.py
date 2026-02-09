"""Tests for fiscal period alignment utilities."""

import sys
from datetime import date
from pathlib import Path

import pytest

# Ensure project root is on path
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.database.period_utils import (
    PeriodConverter,
    PeriodInfo,
    get_converter,
    CONVERTERS,
)


# ============================================================================
# Vodafone Converter (FY starts April)
# ============================================================================

class TestVodafonePeriodConverter:
    """Test Vodafone's fiscal period conversion (FY starts April)."""

    @pytest.fixture
    def converter(self):
        return PeriodConverter(
            fiscal_year_start_month=4,
            fiscal_year_label="FY",
            quarter_naming="fiscal",
        )

    def test_q3_fy26_to_cq4_2025(self, converter):
        """Q3 FY26 = Oct-Dec 2025 = CQ4_2025"""
        pi = converter.to_calendar_quarter("Q3 FY26")
        assert pi.calendar_quarter == "CQ4_2025"
        assert pi.period_start == date(2025, 10, 1)
        assert pi.period_end == date(2025, 12, 31)
        assert pi.calendar_year == 2025
        assert pi.calendar_q == 4
        assert pi.fiscal_quarter == 3
        assert pi.fiscal_year == "FY26"

    def test_q1_fy26_to_cq2_2025(self, converter):
        """Q1 FY26 = Apr-Jun 2025 = CQ2_2025"""
        pi = converter.to_calendar_quarter("Q1 FY26")
        assert pi.calendar_quarter == "CQ2_2025"
        assert pi.period_start == date(2025, 4, 1)
        assert pi.period_end == date(2025, 6, 30)
        assert pi.calendar_year == 2025
        assert pi.calendar_q == 2

    def test_q4_fy26_to_cq1_2026(self, converter):
        """Q4 FY26 = Jan-Mar 2026 = CQ1_2026"""
        pi = converter.to_calendar_quarter("Q4 FY26")
        assert pi.calendar_quarter == "CQ1_2026"
        assert pi.period_start == date(2026, 1, 1)
        assert pi.period_end == date(2026, 3, 31)
        assert pi.calendar_year == 2026
        assert pi.calendar_q == 1

    def test_q2_fy25_to_cq3_2024(self, converter):
        """Q2 FY25 = Jul-Sep 2024 = CQ3_2024"""
        pi = converter.to_calendar_quarter("Q2 FY25")
        assert pi.calendar_quarter == "CQ3_2024"
        assert pi.period_start == date(2024, 7, 1)
        assert pi.period_end == date(2024, 9, 30)
        assert pi.calendar_year == 2024
        assert pi.calendar_q == 3

    def test_q4_fy24_to_cq1_2024(self, converter):
        """Q4 FY24 = Jan-Mar 2024 = CQ1_2024"""
        pi = converter.to_calendar_quarter("Q4 FY24")
        assert pi.calendar_quarter == "CQ1_2024"
        assert pi.period_start == date(2024, 1, 1)
        assert pi.period_end == date(2024, 3, 31)

    def test_q2_fy26_to_cq3_2025(self, converter):
        """Q2 FY26 = Jul-Sep 2025 = CQ3_2025"""
        pi = converter.to_calendar_quarter("Q2 FY26")
        assert pi.calendar_quarter == "CQ3_2025"
        assert pi.period_start == date(2025, 7, 1)
        assert pi.period_end == date(2025, 9, 30)

    def test_from_cq4_2025_to_q3_fy26(self, converter):
        """CQ4_2025 -> Q3 FY26"""
        result = converter.from_calendar_quarter("CQ4_2025")
        assert result == "Q3 FY26"

    def test_from_cq2_2025_to_q1_fy26(self, converter):
        """CQ2_2025 -> Q1 FY26"""
        result = converter.from_calendar_quarter("CQ2_2025")
        assert result == "Q1 FY26"

    def test_from_cq1_2026_to_q4_fy26(self, converter):
        """CQ1_2026 -> Q4 FY26"""
        result = converter.from_calendar_quarter("CQ1_2026")
        assert result == "Q4 FY26"

    def test_round_trip_q3_fy26(self, converter):
        """Round-trip: Q3 FY26 -> CQ4_2025 -> Q3 FY26"""
        pi = converter.to_calendar_quarter("Q3 FY26")
        result = converter.from_calendar_quarter(pi.calendar_quarter)
        assert result == "Q3 FY26"

    def test_round_trip_q1_fy26(self, converter):
        """Round-trip: Q1 FY26 -> CQ2_2025 -> Q1 FY26"""
        pi = converter.to_calendar_quarter("Q1 FY26")
        result = converter.from_calendar_quarter(pi.calendar_quarter)
        assert result == "Q1 FY26"

    def test_round_trip_q4_fy26(self, converter):
        """Round-trip: Q4 FY26 -> CQ1_2026 -> Q4 FY26"""
        pi = converter.to_calendar_quarter("Q4 FY26")
        result = converter.from_calendar_quarter(pi.calendar_quarter)
        assert result == "Q4 FY26"

    def test_round_trip_all_quarters_fy25(self, converter):
        """Round-trip all four quarters of FY25."""
        for q in range(1, 5):
            period = f"Q{q} FY25"
            pi = converter.to_calendar_quarter(period)
            result = converter.from_calendar_quarter(pi.calendar_quarter)
            assert result == period, f"Failed for {period} -> {pi.calendar_quarter} -> {result}"

    def test_full_year_fy2026_long_format(self, converter):
        """Support FY2026 (four-digit year)."""
        pi = converter.to_calendar_quarter("Q1 FY2026")
        assert pi.calendar_quarter == "CQ2_2025"


# ============================================================================
# Calendar Year Converter (DT, O2, 1&1)
# ============================================================================

class TestCalendarYearConverter:
    """Test calendar year period conversion (DT, O2, 1&1)."""

    @pytest.fixture
    def converter(self):
        return PeriodConverter(
            fiscal_year_start_month=1,
            fiscal_year_label="",
            quarter_naming="calendar",
        )

    def test_q4_2025_to_cq4_2025(self, converter):
        """Q4 2025 -> CQ4_2025"""
        pi = converter.to_calendar_quarter("Q4 2025")
        assert pi.calendar_quarter == "CQ4_2025"
        assert pi.period_start == date(2025, 10, 1)
        assert pi.period_end == date(2025, 12, 31)

    def test_q1_2025_to_cq1_2025(self, converter):
        """Q1 2025 -> CQ1_2025"""
        pi = converter.to_calendar_quarter("Q1 2025")
        assert pi.calendar_quarter == "CQ1_2025"
        assert pi.period_start == date(2025, 1, 1)
        assert pi.period_end == date(2025, 3, 31)

    def test_q2_2024_to_cq2_2024(self, converter):
        """Q2 2024 -> CQ2_2024"""
        pi = converter.to_calendar_quarter("Q2 2024")
        assert pi.calendar_quarter == "CQ2_2024"
        assert pi.period_start == date(2024, 4, 1)
        assert pi.period_end == date(2024, 6, 30)

    def test_q3_2024_to_cq3_2024(self, converter):
        """Q3 2024 -> CQ3_2024"""
        pi = converter.to_calendar_quarter("Q3 2024")
        assert pi.calendar_quarter == "CQ3_2024"
        assert pi.period_start == date(2024, 7, 1)
        assert pi.period_end == date(2024, 9, 30)

    def test_from_cq4_2025_to_q4_2025(self, converter):
        """CQ4_2025 -> Q4 2025"""
        result = converter.from_calendar_quarter("CQ4_2025")
        assert result == "Q4 2025"

    def test_from_cq1_2025_to_q1_2025(self, converter):
        """CQ1_2025 -> Q1 2025"""
        result = converter.from_calendar_quarter("CQ1_2025")
        assert result == "Q1 2025"

    def test_round_trip_calendar(self, converter):
        """Round-trip all quarters of 2025."""
        for q in range(1, 5):
            period = f"Q{q} 2025"
            pi = converter.to_calendar_quarter(period)
            result = converter.from_calendar_quarter(pi.calendar_quarter)
            assert result == period


# ============================================================================
# Timeline Generation
# ============================================================================

class TestTimelineGeneration:

    def test_generate_8_quarters(self):
        converter = PeriodConverter()
        timeline = converter.generate_timeline(
            n_quarters=8, end_cq="CQ4_2025"
        )
        assert len(timeline) == 8
        assert timeline[0] == "CQ1_2024"
        assert timeline[-1] == "CQ4_2025"
        # Verify sequential order
        expected = [
            "CQ1_2024", "CQ2_2024", "CQ3_2024", "CQ4_2024",
            "CQ1_2025", "CQ2_2025", "CQ3_2025", "CQ4_2025",
        ]
        assert timeline == expected

    def test_generate_4_quarters(self):
        converter = PeriodConverter()
        timeline = converter.generate_timeline(
            n_quarters=4, end_cq="CQ4_2025"
        )
        assert len(timeline) == 4
        assert timeline[0] == "CQ1_2025"
        assert timeline[-1] == "CQ4_2025"

    def test_generate_crosses_year_boundary(self):
        converter = PeriodConverter()
        timeline = converter.generate_timeline(
            n_quarters=3, end_cq="CQ1_2025"
        )
        assert timeline == ["CQ3_2024", "CQ4_2024", "CQ1_2025"]


# ============================================================================
# get_converter
# ============================================================================

class TestGetConverter:

    def test_vodafone_converter(self):
        conv = get_converter("vodafone_germany")
        assert conv.fy_start_month == 4
        assert conv.fy_label == "FY"
        assert conv.quarter_naming == "fiscal"

    def test_dt_converter(self):
        conv = get_converter("deutsche_telekom")
        assert conv.fy_start_month == 1
        assert conv.fy_label == ""
        assert conv.quarter_naming == "calendar"

    def test_o2_converter(self):
        conv = get_converter("telefonica_o2")
        assert conv.fy_start_month == 1

    def test_one_and_one_converter(self):
        conv = get_converter("one_and_one")
        assert conv.fy_start_month == 1

    def test_unknown_operator_returns_default(self):
        conv = get_converter("some_unknown_operator")
        assert conv.fy_start_month == 1
        assert conv.fy_label == ""


# ============================================================================
# Edge Cases
# ============================================================================

class TestEdgeCases:

    def test_invalid_period_raises(self):
        converter = PeriodConverter()
        with pytest.raises(ValueError):
            converter.to_calendar_quarter("invalid")

    def test_invalid_cq_format_raises(self):
        converter = PeriodConverter()
        with pytest.raises(ValueError):
            converter.from_calendar_quarter("Q4_2025")

    def test_period_end_dates_correct(self):
        """Verify period end dates are the last day of the quarter."""
        converter = PeriodConverter()
        # Q1: ends Mar 31
        pi = converter.to_calendar_quarter("Q1 2025")
        assert pi.period_end == date(2025, 3, 31)
        # Q2: ends Jun 30
        pi = converter.to_calendar_quarter("Q2 2025")
        assert pi.period_end == date(2025, 6, 30)
        # Q3: ends Sep 30
        pi = converter.to_calendar_quarter("Q3 2025")
        assert pi.period_end == date(2025, 9, 30)
        # Q4: ends Dec 31
        pi = converter.to_calendar_quarter("Q4 2025")
        assert pi.period_end == date(2025, 12, 31)

    def test_vodafone_8q_timeline_alignment(self):
        """Verify the 8-quarter timeline for Vodafone matches expected CQs."""
        converter = get_converter("vodafone_germany")
        vf_quarters = [
            "Q4 FY24", "Q1 FY25", "Q2 FY25", "Q3 FY25",
            "Q4 FY25", "Q1 FY26", "Q2 FY26", "Q3 FY26",
        ]
        expected_cqs = [
            "CQ1_2024", "CQ2_2024", "CQ3_2024", "CQ4_2024",
            "CQ1_2025", "CQ2_2025", "CQ3_2025", "CQ4_2025",
        ]
        for vf_q, expected_cq in zip(vf_quarters, expected_cqs):
            pi = converter.to_calendar_quarter(vf_q)
            assert pi.calendar_quarter == expected_cq, \
                f"{vf_q} -> {pi.calendar_quarter}, expected {expected_cq}"
