"""Fiscal period alignment utilities.

Converts between operator-specific fiscal periods and standardized calendar quarters.
Key insight: Vodafone FY starts April, so Q3 FY26 = Oct-Dec 2025 = CQ4_2025.
             DT/O2/1&1 use calendar year, so Q4 2025 = CQ4_2025.
"""

from dataclasses import dataclass
from datetime import date, timedelta
import re
from typing import Optional


@dataclass
class PeriodInfo:
    """Represents a fiscal period with both operator and calendar quarter views."""
    operator_period: str       # "Q3 FY26" or "Q4 2025"
    calendar_quarter: str      # "CQ4_2025"
    period_start: date         # 2025-10-01
    period_end: date           # 2025-12-31
    fiscal_year: str           # "FY26" or "2025"
    fiscal_quarter: int        # 3 or 4
    calendar_year: int         # 2025
    calendar_q: int            # 4


class PeriodConverter:
    """Converts between operator fiscal periods and calendar quarters.

    Args:
        fiscal_year_start_month: Month when fiscal year starts (1=Jan, 4=Apr)
        fiscal_year_label: "FY" for Vodafone, "" for calendar-year operators
        quarter_naming: "fiscal" or "calendar"
    """

    def __init__(self, fiscal_year_start_month: int = 1,
                 fiscal_year_label: str = "",
                 quarter_naming: str = "calendar"):
        self.fy_start_month = fiscal_year_start_month
        self.fy_label = fiscal_year_label
        self.quarter_naming = quarter_naming

    def to_calendar_quarter(self, operator_period: str) -> PeriodInfo:
        """Convert operator period string to PeriodInfo.

        Examples:
            "Q3 FY26" (Vodafone) -> CQ4_2025
            "Q4 2025" (DT) -> CQ4_2025
            "Q1 FY26" (Vodafone) -> CQ2_2025
            "Q4 FY26" (Vodafone) -> CQ1_2026
        """
        fq, year_str = self._parse_period(operator_period)

        if self.fy_start_month == 1:
            # Calendar year operator (DT, O2, 1&1)
            cy = int(year_str)
            cq = fq
        else:
            # Fiscal year operator (e.g., Vodafone starts April)
            fy = int(re.sub(r'[^0-9]', '', year_str))
            if fy < 100:
                fy += 2000

            # Calculate calendar month for start of this fiscal quarter
            month_offset = (fq - 1) * 3
            start_month = ((self.fy_start_month - 1 + month_offset) % 12) + 1

            # Calculate calendar year
            if start_month >= self.fy_start_month:
                cy = fy - 1  # Still in previous calendar year
            else:
                cy = fy  # Crossed into the FY-labeled year

            cq = (start_month - 1) // 3 + 1

        period_start = date(cy, (cq - 1) * 3 + 1, 1)
        if cq == 4:
            period_end = date(cy, 12, 31)
        else:
            # Last day of the quarter's final month
            next_quarter_start = date(cy, cq * 3 + 1, 1)
            period_end = next_quarter_start - timedelta(days=1)

        return PeriodInfo(
            operator_period=operator_period,
            calendar_quarter=f"CQ{cq}_{cy}",
            period_start=period_start,
            period_end=period_end,
            fiscal_year=year_str,
            fiscal_quarter=fq,
            calendar_year=cy,
            calendar_q=cq,
        )

    def from_calendar_quarter(self, cq_str: str) -> str:
        """Convert calendar quarter back to operator period string.

        "CQ4_2025" -> "Q3 FY26" (Vodafone) or "Q4 2025" (DT)
        """
        match = re.match(r'CQ(\d)_(\d{4})', cq_str)
        if not match:
            raise ValueError(f"Invalid calendar quarter format: {cq_str}")

        cq = int(match.group(1))
        cy = int(match.group(2))

        if self.fy_start_month == 1:
            return f"Q{cq} {cy}"

        # Fiscal year operator
        start_month = (cq - 1) * 3 + 1
        months_into_fy = (start_month - self.fy_start_month) % 12
        fq = months_into_fy // 3 + 1

        if start_month >= self.fy_start_month:
            fy = cy + 1
        else:
            fy = cy

        fy_short = fy % 100
        return f"Q{fq} {self.fy_label}{fy_short}"

    def generate_timeline(self, n_quarters: int = 8,
                          end_cq: Optional[str] = None) -> list:
        """Generate a list of calendar quarters.

        Returns list of "CQn_YYYY" strings, oldest first.
        """
        if end_cq:
            match = re.match(r'CQ(\d)_(\d{4})', end_cq)
            if not match:
                raise ValueError(f"Invalid calendar quarter format: {end_cq}")
            end_q = int(match.group(1))
            end_y = int(match.group(2))
        else:
            today = date.today()
            end_q = (today.month - 1) // 3 + 1
            end_y = today.year

        quarters = []
        q, y = end_q, end_y
        for _ in range(n_quarters):
            quarters.append(f"CQ{q}_{y}")
            q -= 1
            if q == 0:
                q = 4
                y -= 1

        return list(reversed(quarters))

    def _parse_period(self, period_str: str) -> tuple:
        """Parse period string into (quarter_number, year_string).

        Supports: "Q3 FY26", "Q4 2025", "Q1 FY2026"
        """
        period_str = period_str.strip()

        match = re.match(r'Q(\d)\s+(.+)', period_str)
        if match:
            return int(match.group(1)), match.group(2).strip()

        raise ValueError(f"Cannot parse period: {period_str}")


# Pre-built converters for known operators
CONVERTERS = {
    "vodafone_germany": PeriodConverter(
        fiscal_year_start_month=4,
        fiscal_year_label="FY",
        quarter_naming="fiscal",
    ),
    "deutsche_telekom": PeriodConverter(
        fiscal_year_start_month=1,
        fiscal_year_label="",
        quarter_naming="calendar",
    ),
    "telefonica_o2": PeriodConverter(
        fiscal_year_start_month=1,
        fiscal_year_label="",
        quarter_naming="calendar",
    ),
    "one_and_one": PeriodConverter(
        fiscal_year_start_month=1,
        fiscal_year_label="",
        quarter_naming="calendar",
    ),
}


def get_converter(operator_id: str) -> PeriodConverter:
    """Get the period converter for an operator.

    Falls back to calendar-year converter if operator is not registered.
    """
    if operator_id in CONVERTERS:
        return CONVERTERS[operator_id]
    # Default: calendar year
    return PeriodConverter()
