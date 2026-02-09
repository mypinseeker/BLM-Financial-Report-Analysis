"""Operator directory with fiscal year configuration and metadata.

This module contains the canonical registry of telecom operators,
their fiscal year configurations, and earnings calendars.
"""

OPERATOR_DIRECTORY = {
    "vodafone_germany": {
        "display_name": "Vodafone Germany",
        "parent_company": "Vodafone Group",
        "country": "Germany",
        "region": "Europe",
        "market": "germany",
        "operator_type": "challenger",
        "ir_url": "https://www.vodafone.com/investors",
        "fiscal_year_start_month": 4,
        "fiscal_year_label": "FY",
        "quarter_naming": "fiscal",
        "currency": "EUR",
    },
    "deutsche_telekom": {
        "display_name": "Deutsche Telekom",
        "parent_company": "Deutsche Telekom AG",
        "country": "Germany",
        "region": "Europe",
        "market": "germany",
        "operator_type": "incumbent",
        "ir_url": "https://www.telekom.com/en/investor-relations",
        "fiscal_year_start_month": 1,
        "fiscal_year_label": "",
        "quarter_naming": "calendar",
        "currency": "EUR",
    },
    "telefonica_o2": {
        "display_name": "Telefonica O2 Germany",
        "parent_company": "Telefonica SA",
        "country": "Germany",
        "region": "Europe",
        "market": "germany",
        "operator_type": "challenger",
        "ir_url": "https://www.telefonica.de/investor-relations.html",
        "fiscal_year_start_month": 1,
        "fiscal_year_label": "",
        "quarter_naming": "calendar",
        "currency": "EUR",
    },
    "one_and_one": {
        "display_name": "1&1 AG",
        "parent_company": "United Internet AG",
        "country": "Germany",
        "region": "Europe",
        "market": "germany",
        "operator_type": "new_entrant",
        "ir_url": "https://www.1und1.ag/investor-relations",
        "fiscal_year_start_month": 1,
        "fiscal_year_label": "",
        "quarter_naming": "calendar",
        "currency": "EUR",
    },
}

# Earnings release calendar
EARNINGS_CALENDAR = {
    "vodafone_germany": {
        "Q3 FY26": {"expected_date": "2026-02-05", "status": "published"},
        "Q2 FY26": {"expected_date": "2025-11-12", "status": "published"},
        "Q1 FY26": {"expected_date": "2025-07-25", "status": "published"},
        "Q4 FY25": {"expected_date": "2025-05-20", "status": "published"},
        "Q3 FY25": {"expected_date": "2025-01-28", "status": "published"},
        "Q2 FY25": {"expected_date": "2024-11-12", "status": "published"},
        "Q1 FY25": {"expected_date": "2024-07-23", "status": "published"},
        "Q4 FY24": {"expected_date": "2024-05-21", "status": "published"},
    },
    "deutsche_telekom": {
        "Q4 2025": {"expected_date": "2026-02-27", "status": "pending"},
        "Q3 2025": {"expected_date": "2025-11-14", "status": "published"},
        "Q2 2025": {"expected_date": "2025-08-08", "status": "published"},
        "Q1 2025": {"expected_date": "2025-05-15", "status": "published"},
        "Q4 2024": {"expected_date": "2025-02-27", "status": "published"},
        "Q3 2024": {"expected_date": "2024-11-14", "status": "published"},
        "Q2 2024": {"expected_date": "2024-08-08", "status": "published"},
        "Q1 2024": {"expected_date": "2024-05-16", "status": "published"},
    },
    "telefonica_o2": {
        "Q3 2025": {"expected_date": "2025-10-30", "status": "published"},
        "Q2 2025": {"expected_date": "2025-07-24", "status": "published"},
        "Q1 2025": {"expected_date": "2025-05-08", "status": "published"},
        "Q4 2024": {"expected_date": "2025-02-20", "status": "published"},
        "Q3 2024": {"expected_date": "2024-10-24", "status": "published"},
        "Q2 2024": {"expected_date": "2024-07-25", "status": "published"},
        "Q1 2024": {"expected_date": "2024-05-09", "status": "published"},
    },
    "one_and_one": {
        "Q3 2025": {"expected_date": "2025-11-13", "status": "published"},
        "Q2 2025": {"expected_date": "2025-08-14", "status": "published"},
        "Q1 2025": {"expected_date": "2025-05-15", "status": "published"},
        "Q4 2024": {"expected_date": "2025-03-27", "status": "published"},
        "Q3 2024": {"expected_date": "2024-11-14", "status": "published"},
        "Q2 2024": {"expected_date": "2024-08-08", "status": "published"},
        "Q1 2024": {"expected_date": "2024-05-16", "status": "published"},
    },
}


def get_operators_for_market(market: str) -> list:
    """Get all operator IDs for a given market."""
    return [
        op_id for op_id, info in OPERATOR_DIRECTORY.items()
        if info["market"] == market
    ]


def get_operator_info(operator_id: str) -> dict:
    """Get operator metadata by ID. Returns empty dict if not found."""
    return OPERATOR_DIRECTORY.get(operator_id, {})
