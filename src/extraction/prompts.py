"""Extraction prompts for Gemini AI — 6 prompt functions for report discovery and 5 data tables.

Each function returns (system_instruction, user_prompt).
All prompts enforce:
- Amounts in millions of local currency
- Subscriber counts in thousands (_k suffix)
- Null for unavailable fields
- Confidence 0.0-1.0 per record
- JSON field names exactly match database column names
"""


def get_discovery_prompt(
    operator_name: str, ir_url: str, report_period: str = ""
) -> tuple[str, str]:
    """Prompt for discovering the latest earnings report PDF via Google Search."""
    system_instruction = (
        "You are a financial research assistant specialized in finding direct PDF "
        "download links for telecom operator earnings reports. "
        "You MUST return a direct link to a .pdf file, NOT an HTML page. "
        "Return ONLY a JSON object."
    )
    period_hint = f" Focus on the {report_period} period." if report_period else ""
    user_prompt = f"""Find the DIRECT PDF download URL for the most recent quarterly earnings report for: {operator_name}
Investor Relations page: {ir_url}{period_hint}

IMPORTANT RULES:
1. The pdf_url MUST be a direct link to a PDF file (typically ending in .pdf)
2. Do NOT return an HTML page URL — it must be a downloadable PDF
3. Search for "earnings release PDF", "quarterly report PDF", "results PDF" on the company's IR site
4. For Millicom/Tigo, look at: https://www.millicom.com/investors/reports-and-presentations/
5. Common PDF URL patterns: /files/*.pdf, /media/*.pdf, /documents/*.pdf, /wp-content/*.pdf

Return a JSON object with these exact fields:
{{
    "pdf_url": "DIRECT URL to the PDF file (must be a real .pdf download link, NOT an HTML page)",
    "report_title": "title of the report (e.g., 'Q4 2025 Earnings Release')",
    "report_period": "period in CQ format like 'CQ4_2025' or 'CQ3_2025'",
    "ir_page_url": "URL of the investor relations page where the PDF link was found",
    "confidence": 0.0 to 1.0
}}

If you absolutely cannot find a direct PDF link, set confidence to 0.2 and explain in report_title.
NEVER return an HTML page URL as pdf_url."""
    return system_instruction, user_prompt


def get_financial_prompt(
    operator_id: str,
    operator_name: str,
    currency: str,
    target_quarter: str,
    n_quarters: int = 4,
) -> tuple[str, str]:
    """Prompt for extracting financial_quarterly data from a report PDF."""
    system_instruction = (
        "You are a financial data extraction expert. Extract structured quarterly "
        "financial data from telecom operator earnings reports. "
        "Be precise with numbers. All monetary values must be in MILLIONS of local currency. "
        "Return ONLY a JSON array of quarterly records."
    )
    user_prompt = f"""Extract quarterly financial data for {operator_name} (ID: {operator_id}).
Currency: {currency} (all amounts in MILLIONS of {currency}).
Target: up to {n_quarters} most recent quarters, ideally including {target_quarter}.

Extract a JSON array where each element has these exact fields:
[
  {{
    "operator_id": "{operator_id}",
    "period": "e.g. Q4 2025 or FY Q3",
    "calendar_quarter": "CQn_YYYY format (e.g. CQ4_2025)",
    "period_start": "YYYY-MM-DD (first day of quarter)",
    "period_end": "YYYY-MM-DD (last day of quarter)",
    "report_date": "YYYY-MM-DD (publication date if known, else null)",
    "report_status": "published",
    "total_revenue": null or number (millions {currency}),
    "service_revenue": null or number,
    "service_revenue_growth_pct": null or number,
    "mobile_service_revenue": null or number,
    "mobile_service_growth_pct": null or number,
    "fixed_service_revenue": null or number,
    "fixed_service_growth_pct": null or number,
    "b2b_revenue": null or number,
    "b2b_growth_pct": null or number,
    "tv_revenue": null or number,
    "wholesale_revenue": null or number,
    "other_revenue": null or number,
    "ebitda": null or number,
    "ebitda_margin_pct": null or number,
    "ebitda_growth_pct": null or number,
    "net_income": null or number,
    "capex": null or number,
    "capex_to_revenue_pct": null or number,
    "opex": null or number,
    "opex_to_revenue_pct": null or number,
    "employees": null or integer,
    "confidence": 0.0 to 1.0
  }}
]

Calendar quarter mapping:
- CQ1 = Jan-Mar (period_start: YYYY-01-01, period_end: YYYY-03-31)
- CQ2 = Apr-Jun (period_start: YYYY-04-01, period_end: YYYY-06-30)
- CQ3 = Jul-Sep (period_start: YYYY-07-01, period_end: YYYY-09-30)
- CQ4 = Oct-Dec (period_start: YYYY-10-01, period_end: YYYY-12-31)

Rules:
- Set fields to null if data is not available in the report
- Growth percentages should be year-over-year
- EBITDA margin = EBITDA / total_revenue * 100
- Confidence reflects how clearly the data was stated in the report"""
    return system_instruction, user_prompt


def get_subscriber_prompt(
    operator_id: str,
    operator_name: str,
    target_quarter: str,
    n_quarters: int = 4,
) -> tuple[str, str]:
    """Prompt for extracting subscriber_quarterly data."""
    system_instruction = (
        "You are a telecom data extraction expert. Extract subscriber/customer "
        "metrics from quarterly earnings reports. All subscriber counts must be "
        "in THOUSANDS (the _k suffix means thousands). "
        "Return ONLY a JSON array."
    )
    user_prompt = f"""Extract quarterly subscriber data for {operator_name} (ID: {operator_id}).
All subscriber/customer counts in THOUSANDS.
Target: up to {n_quarters} most recent quarters, ideally including {target_quarter}.

Extract a JSON array where each element has these exact fields:
[
  {{
    "operator_id": "{operator_id}",
    "period": "e.g. Q4 2025",
    "calendar_quarter": "CQn_YYYY format",
    "period_start": "YYYY-MM-DD",
    "period_end": "YYYY-MM-DD",
    "report_status": "published",
    "mobile_total_k": null or number (thousands),
    "mobile_postpaid_k": null or number,
    "mobile_prepaid_k": null or number,
    "mobile_net_adds_k": null or number (can be negative),
    "mobile_churn_pct": null or number,
    "mobile_arpu": null or number (local currency, NOT thousands),
    "iot_connections_k": null or number,
    "broadband_total_k": null or number,
    "broadband_net_adds_k": null or number,
    "broadband_cable_k": null or number,
    "broadband_fiber_k": null or number,
    "broadband_dsl_k": null or number,
    "broadband_fwa_k": null or number,
    "broadband_arpu": null or number (local currency),
    "tv_total_k": null or number,
    "tv_net_adds_k": null or number,
    "fmc_total_k": null or number,
    "fmc_penetration_pct": null or number,
    "b2b_customers_k": null or number,
    "confidence": 0.0 to 1.0
  }}
]

Rules:
- ARPU values are in local currency per month per subscriber, NOT in thousands
- Net adds can be negative (net losses)
- Churn is monthly churn percentage
- Set to null if not reported"""
    return system_instruction, user_prompt


def get_tariff_prompt(
    operator_id: str,
    operator_name: str,
    currency: str,
    snapshot_period: str = "",
) -> tuple[str, str]:
    """Prompt for extracting tariff/plan data."""
    system_instruction = (
        "You are a telecom pricing analyst. Extract current tariff plans and "
        "pricing information from operator reports, websites, or publications. "
        "Return ONLY a JSON array of plan records."
    )
    period_hint = snapshot_period or "H1_2026"
    user_prompt = f"""Extract current tariff/pricing plans for {operator_name} (ID: {operator_id}).
Currency: {currency}.
Snapshot period: {period_hint}

Extract a JSON array where each element has these exact fields:
[
  {{
    "operator_id": "{operator_id}",
    "plan_name": "name of the plan",
    "plan_type": "one of: mobile_postpaid / mobile_prepaid / fixed_dsl / fixed_cable / fixed_fiber / tv / fmc_bundle",
    "plan_tier": "one of: xs / s / m / l / xl / unlimited",
    "monthly_price": number ({currency}),
    "data_allowance": "e.g. '50GB', 'Unlimited', '10GB/day'",
    "speed_mbps": null or number,
    "contract_months": null or integer,
    "includes_5g": true/false,
    "technology": "e.g. '4G LTE', '5G', 'Fiber', 'Cable'",
    "effective_date": "YYYY-MM-DD or null",
    "snapshot_period": "{period_hint}",
    "confidence": 0.0 to 1.0
  }}
]

Rules:
- Include all major consumer plans (postpaid, prepaid, broadband, bundles)
- Monthly price in local currency
- Speed in Mbps (download speed)
- Set to null if info not available"""
    return system_instruction, user_prompt


def get_macro_prompt(
    country: str, target_quarter: str, n_quarters: int = 4
) -> tuple[str, str]:
    """Prompt for extracting macro_environment data."""
    system_instruction = (
        "You are a macroeconomic analyst. Extract country-level economic and "
        "telecom market indicators. Use official statistics where available. "
        "Return ONLY a JSON array."
    )
    user_prompt = f"""Extract macroeconomic data for {country}.
Target: up to {n_quarters} most recent quarters, ideally including {target_quarter}.

Extract a JSON array where each element has these exact fields:
[
  {{
    "country": "{country}",
    "calendar_quarter": "CQn_YYYY format",
    "gdp_growth_pct": null or number (year-over-year %),
    "inflation_pct": null or number (annual %),
    "unemployment_pct": null or number (%),
    "telecom_market_size_eur_b": null or number (billions EUR),
    "telecom_growth_pct": null or number (%),
    "five_g_adoption_pct": null or number (% of mobile connections),
    "fiber_penetration_pct": null or number (% of broadband),
    "regulatory_environment": null or "brief description of current regulation",
    "digital_strategy": null or "government digital agenda summary",
    "energy_cost_index": null or number (index, 100=base),
    "consumer_confidence_index": null or number,
    "confidence": 0.0 to 1.0
  }}
]

Rules:
- Use most recent official statistics
- GDP growth and inflation are year-over-year percentages
- Telecom market size in billions EUR (convert if needed)
- Set to null if reliable data is not available"""
    return system_instruction, user_prompt


def get_network_prompt(
    operator_id: str,
    operator_name: str,
    target_quarter: str,
    n_quarters: int = 4,
) -> tuple[str, str]:
    """Prompt for extracting network_infrastructure data."""
    system_instruction = (
        "You are a telecom network analyst. Extract network infrastructure "
        "and coverage metrics from operator reports. All homepass/connected "
        "counts in THOUSANDS. Return ONLY a JSON array."
    )
    user_prompt = f"""Extract network infrastructure data for {operator_name} (ID: {operator_id}).
Target: up to {n_quarters} most recent quarters, ideally including {target_quarter}.

Extract a JSON array where each element has these exact fields:
[
  {{
    "operator_id": "{operator_id}",
    "calendar_quarter": "CQn_YYYY format",
    "five_g_coverage_pct": null or number (% population covered),
    "four_g_coverage_pct": null or number (%),
    "fiber_homepass_k": null or number (thousands of homes passed),
    "fiber_connected_k": null or number (thousands connected),
    "cable_homepass_k": null or number (thousands),
    "cable_docsis31_pct": null or number (% of cable network upgraded),
    "technology_mix": null or "JSON string describing tech portfolio",
    "quality_scores": null or "JSON string with NPS/quality metrics",
    "confidence": 0.0 to 1.0
  }}
]

Rules:
- All homepass/connected counts in THOUSANDS
- Coverage percentages are population coverage
- technology_mix and quality_scores should be JSON-formatted strings if available
- Set to null if not reported"""
    return system_instruction, user_prompt


# ------------------------------------------------------------------
# Lookup helper
# ------------------------------------------------------------------

TABLE_PROMPT_MAP = {
    "financial": get_financial_prompt,
    "subscriber": get_subscriber_prompt,
    "tariff": get_tariff_prompt,
    "macro": get_macro_prompt,
    "network": get_network_prompt,
}
