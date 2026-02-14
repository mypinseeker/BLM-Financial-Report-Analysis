"""Operator directory with fiscal year configuration and metadata.

This module contains the canonical registry of telecom operators,
their fiscal year configurations, earnings calendars, and operator groups.
"""

# ============================================================================
# Operator Groups — multinational parent companies
# ============================================================================

OPERATOR_GROUPS = {
    "millicom": {
        "group_id": "millicom",
        "group_name": "Millicom International Cellular S.A.",
        "brand_name": "Tigo",
        "headquarters": "Luxembourg",
        "ir_url": "https://www.millicom.com/investors/",
        "stock_ticker": "TIGO (NASDAQ)",
        "markets_count": 11,
        "notes": "Leading provider of mobile and cable services in Latin America",
    },
    "vodafone_group": {
        "group_id": "vodafone_group",
        "group_name": "Vodafone Group Plc",
        "brand_name": "Vodafone",
        "headquarters": "London, UK",
        "ir_url": "https://www.vodafone.com/investors",
        "stock_ticker": "VOD (LSE/NASDAQ)",
        "markets_count": 15,
    },
    "telefonica_group": {
        "group_id": "telefonica_group",
        "group_name": "Telefonica S.A.",
        "brand_name": "Movistar",
        "headquarters": "Madrid, Spain",
        "ir_url": "https://www.telefonica.com/en/shareholders-investors/",
        "stock_ticker": "TEF (BME/NYSE)",
        "markets_count": 12,
    },
    "america_movil": {
        "group_id": "america_movil",
        "group_name": "America Movil S.A.B. de C.V.",
        "brand_name": "Claro",
        "headquarters": "Mexico City, Mexico",
        "ir_url": "https://www.americamovil.com/English/investors/",
        "stock_ticker": "AMX (BMV/NYSE)",
        "markets_count": 25,
    },
}

# ============================================================================
# Operator Directory — all registered operators
# ============================================================================

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

    # ========================================================================
    # Guatemala
    # ========================================================================
    "tigo_guatemala": {
        "display_name": "Tigo Guatemala",
        "parent_company": "Millicom International Cellular",
        "country": "Guatemala",
        "region": "Latin America",
        "market": "guatemala",
        "operator_type": "incumbent",
        "group_id": "millicom",
        "ir_url": "https://www.millicom.com/investors/",
        "fiscal_year_start_month": 1,
        "fiscal_year_label": "",
        "quarter_naming": "calendar",
        "currency": "GTQ",
    },
    "claro_gt": {
        "display_name": "Claro Guatemala",
        "parent_company": "America Movil",
        "country": "Guatemala",
        "region": "Latin America",
        "market": "guatemala",
        "operator_type": "challenger",
        "group_id": "america_movil",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "GTQ",
    },
    "movistar_gt": {
        "display_name": "Movistar Guatemala",
        "parent_company": "Telefonica S.A.",
        "country": "Guatemala",
        "region": "Latin America",
        "market": "guatemala",
        "operator_type": "challenger",
        "group_id": "telefonica_group",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "GTQ",
    },

    # ========================================================================
    # Honduras
    # ========================================================================
    "tigo_honduras": {
        "display_name": "Tigo Honduras",
        "parent_company": "Millicom International Cellular",
        "country": "Honduras",
        "region": "Latin America",
        "market": "honduras",
        "operator_type": "incumbent",
        "group_id": "millicom",
        "ir_url": "https://www.millicom.com/investors/",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "HNL",
    },
    "claro_hn": {
        "display_name": "Claro Honduras",
        "parent_company": "America Movil",
        "country": "Honduras",
        "region": "Latin America",
        "market": "honduras",
        "operator_type": "challenger",
        "group_id": "america_movil",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "HNL",
    },
    "digicel_hn": {
        "display_name": "Digicel Honduras",
        "parent_company": "Digicel Group",
        "country": "Honduras",
        "region": "Latin America",
        "market": "honduras",
        "operator_type": "challenger",
        "fiscal_year_start_month": 4,
        "quarter_naming": "fiscal",
        "currency": "HNL",
    },

    # ========================================================================
    # El Salvador
    # ========================================================================
    "tigo_el_salvador": {
        "display_name": "Tigo El Salvador",
        "parent_company": "Millicom International Cellular",
        "country": "El Salvador",
        "region": "Latin America",
        "market": "el_salvador",
        "operator_type": "challenger",
        "group_id": "millicom",
        "ir_url": "https://www.millicom.com/investors/",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "USD",
    },
    "claro_sv": {
        "display_name": "Claro El Salvador",
        "parent_company": "America Movil",
        "country": "El Salvador",
        "region": "Latin America",
        "market": "el_salvador",
        "operator_type": "incumbent",
        "group_id": "america_movil",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "USD",
    },
    "digicel_sv": {
        "display_name": "Digicel El Salvador",
        "parent_company": "Digicel Group",
        "country": "El Salvador",
        "region": "Latin America",
        "market": "el_salvador",
        "operator_type": "challenger",
        "fiscal_year_start_month": 4,
        "quarter_naming": "fiscal",
        "currency": "USD",
    },

    # ========================================================================
    # Colombia
    # ========================================================================
    "tigo_colombia": {
        "display_name": "Tigo Colombia",
        "parent_company": "Millicom International Cellular",
        "country": "Colombia",
        "region": "Latin America",
        "market": "colombia",
        "operator_type": "challenger",
        "group_id": "millicom",
        "ir_url": "https://www.millicom.com/investors/",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "COP",
    },
    "claro_co": {
        "display_name": "Claro Colombia",
        "parent_company": "America Movil",
        "country": "Colombia",
        "region": "Latin America",
        "market": "colombia",
        "operator_type": "incumbent",
        "group_id": "america_movil",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "COP",
    },
    "movistar_co": {
        "display_name": "Movistar Colombia",
        "parent_company": "Telefonica S.A.",
        "country": "Colombia",
        "region": "Latin America",
        "market": "colombia",
        "operator_type": "challenger",
        "group_id": "telefonica_group",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "COP",
    },
    "wom_co": {
        "display_name": "WOM Colombia",
        "parent_company": "WOM S.A.",
        "country": "Colombia",
        "region": "Latin America",
        "market": "colombia",
        "operator_type": "new_entrant",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "COP",
    },

    # ========================================================================
    # Panama
    # ========================================================================
    "tigo_panama": {
        "display_name": "Tigo Panama",
        "parent_company": "Millicom International Cellular",
        "country": "Panama",
        "region": "Latin America",
        "market": "panama",
        "operator_type": "challenger",
        "group_id": "millicom",
        "ir_url": "https://www.millicom.com/investors/",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "USD",
    },
    "claro_pa": {
        "display_name": "Claro Panama",
        "parent_company": "America Movil",
        "country": "Panama",
        "region": "Latin America",
        "market": "panama",
        "operator_type": "incumbent",
        "group_id": "america_movil",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "USD",
    },
    "digicel_pa": {
        "display_name": "Digicel Panama",
        "parent_company": "Digicel Group",
        "country": "Panama",
        "region": "Latin America",
        "market": "panama",
        "operator_type": "challenger",
        "fiscal_year_start_month": 4,
        "quarter_naming": "fiscal",
        "currency": "USD",
    },

    # ========================================================================
    # Bolivia
    # ========================================================================
    "tigo_bolivia": {
        "display_name": "Tigo Bolivia",
        "parent_company": "Millicom International Cellular",
        "country": "Bolivia",
        "region": "Latin America",
        "market": "bolivia",
        "operator_type": "incumbent",
        "group_id": "millicom",
        "ir_url": "https://www.millicom.com/investors/",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "BOB",
    },
    "entel_bo": {
        "display_name": "Entel Bolivia",
        "parent_company": "Entel S.A. (State-owned)",
        "country": "Bolivia",
        "region": "Latin America",
        "market": "bolivia",
        "operator_type": "incumbent",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "BOB",
    },
    "viva_bo": {
        "display_name": "Viva Bolivia",
        "parent_company": "NuevaTel PCS",
        "country": "Bolivia",
        "region": "Latin America",
        "market": "bolivia",
        "operator_type": "challenger",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "BOB",
    },

    # ========================================================================
    # Paraguay
    # ========================================================================
    "tigo_paraguay": {
        "display_name": "Tigo Paraguay",
        "parent_company": "Millicom International Cellular",
        "country": "Paraguay",
        "region": "Latin America",
        "market": "paraguay",
        "operator_type": "incumbent",
        "group_id": "millicom",
        "ir_url": "https://www.millicom.com/investors/",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "PYG",
    },
    "claro_py": {
        "display_name": "Claro Paraguay",
        "parent_company": "America Movil",
        "country": "Paraguay",
        "region": "Latin America",
        "market": "paraguay",
        "operator_type": "challenger",
        "group_id": "america_movil",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "PYG",
    },
    "personal_py": {
        "display_name": "Personal Paraguay",
        "parent_company": "Telecom Argentina (Grupo Clarin)",
        "country": "Paraguay",
        "region": "Latin America",
        "market": "paraguay",
        "operator_type": "challenger",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "PYG",
    },

    # ========================================================================
    # Nicaragua
    # ========================================================================
    "tigo_nicaragua": {
        "display_name": "Tigo Nicaragua",
        "parent_company": "Millicom International Cellular",
        "country": "Nicaragua",
        "region": "Latin America",
        "market": "nicaragua",
        "operator_type": "incumbent",
        "group_id": "millicom",
        "ir_url": "https://www.millicom.com/investors/",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "NIO",
    },
    "claro_ni": {
        "display_name": "Claro Nicaragua",
        "parent_company": "America Movil",
        "country": "Nicaragua",
        "region": "Latin America",
        "market": "nicaragua",
        "operator_type": "challenger",
        "group_id": "america_movil",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "NIO",
    },

    # ========================================================================
    # Ecuador
    # ========================================================================
    "tigo_ecuador": {
        "display_name": "Tigo Ecuador",
        "parent_company": "Millicom International Cellular",
        "country": "Ecuador",
        "region": "Latin America",
        "market": "ecuador",
        "operator_type": "challenger",
        "group_id": "millicom",
        "ir_url": "https://www.millicom.com/investors/",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "USD",
        "notes": "Acquired 2025. Formerly Telefonica Ecuador.",
    },
    "claro_ec": {
        "display_name": "Claro Ecuador",
        "parent_company": "America Movil",
        "country": "Ecuador",
        "region": "Latin America",
        "market": "ecuador",
        "operator_type": "incumbent",
        "group_id": "america_movil",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "USD",
    },
    "cnt_ec": {
        "display_name": "CNT Ecuador",
        "parent_company": "Corporacion Nacional de Telecomunicaciones (State-owned)",
        "country": "Ecuador",
        "region": "Latin America",
        "market": "ecuador",
        "operator_type": "incumbent",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "USD",
    },

    # ========================================================================
    # Uruguay
    # ========================================================================
    "tigo_uruguay": {
        "display_name": "Tigo Uruguay",
        "parent_company": "Millicom International Cellular",
        "country": "Uruguay",
        "region": "Latin America",
        "market": "uruguay",
        "operator_type": "challenger",
        "group_id": "millicom",
        "ir_url": "https://www.millicom.com/investors/",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "UYU",
        "notes": "Acquired 2025. New market entry.",
    },
    "antel_uy": {
        "display_name": "Antel Uruguay",
        "parent_company": "Administracion Nacional de Telecomunicaciones (State-owned)",
        "country": "Uruguay",
        "region": "Latin America",
        "market": "uruguay",
        "operator_type": "incumbent",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "UYU",
    },
    "claro_uy": {
        "display_name": "Claro Uruguay",
        "parent_company": "America Movil",
        "country": "Uruguay",
        "region": "Latin America",
        "market": "uruguay",
        "operator_type": "challenger",
        "group_id": "america_movil",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "UYU",
    },

    # ========================================================================
    # Chile
    # ========================================================================
    "tigo_chile": {
        "display_name": "Tigo Chile",
        "parent_company": "Millicom International Cellular",
        "country": "Chile",
        "region": "Latin America",
        "market": "chile",
        "operator_type": "challenger",
        "group_id": "millicom",
        "ir_url": "https://www.millicom.com/investors/",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "CLP",
        "notes": "Acquired Telefonica Chile Feb 2026. No historical Tigo data.",
    },
    "entel_cl": {
        "display_name": "Entel Chile",
        "parent_company": "Entel S.A.",
        "country": "Chile",
        "region": "Latin America",
        "market": "chile",
        "operator_type": "incumbent",
        "ir_url": "https://investors.entel.cl/",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "CLP",
    },
    "wom_cl": {
        "display_name": "WOM Chile",
        "parent_company": "WOM S.A.",
        "country": "Chile",
        "region": "Latin America",
        "market": "chile",
        "operator_type": "challenger",
        "ir_url": "https://www.wom.cl/",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "CLP",
    },
    "claro_cl": {
        "display_name": "Claro Chile",
        "parent_company": "America Movil",
        "country": "Chile",
        "region": "Latin America",
        "market": "chile",
        "operator_type": "challenger",
        "group_id": "america_movil",
        "ir_url": "https://www.americamovil.com/English/investors/",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "CLP",
    },
    "movistar_cl": {
        "display_name": "Movistar Chile",
        "parent_company": "Telefonica S.A.",
        "country": "Chile",
        "region": "Latin America",
        "market": "chile",
        "operator_type": "incumbent",
        "group_id": "telefonica_group",
        "ir_url": "https://www.telefonica.com/en/shareholders-investors/",
        "fiscal_year_start_month": 1,
        "quarter_naming": "calendar",
        "currency": "CLP",
    },

    # ========================================================================
    # Netherlands
    # ========================================================================
    "odido_nl": {
        "display_name": "Odido",
        "parent_company": "Odido Group (Apax/Warburg Pincus)",
        "country": "Netherlands",
        "region": "Europe",
        "market": "netherlands",
        "operator_type": "challenger",
        "ir_url": "https://www.odido.nl/",
        "fiscal_year_start_month": 1,
        "fiscal_year_label": "",
        "quarter_naming": "calendar",
        "currency": "EUR",
        "notes": "Rebranded from T-Mobile Netherlands in Sep 2023. Sold by Deutsche Telekom to Apax/Warburg Pincus consortium.",
    },
    "kpn_nl": {
        "display_name": "KPN",
        "parent_company": "Koninklijke KPN N.V.",
        "country": "Netherlands",
        "region": "Europe",
        "market": "netherlands",
        "operator_type": "incumbent",
        "ir_url": "https://www.kpn.com/investor-relations.htm",
        "fiscal_year_start_month": 1,
        "fiscal_year_label": "",
        "quarter_naming": "calendar",
        "currency": "EUR",
    },
    "vodafoneziggo_nl": {
        "display_name": "VodafoneZiggo",
        "parent_company": "VodafoneZiggo Group (Vodafone/Liberty Global JV)",
        "country": "Netherlands",
        "region": "Europe",
        "market": "netherlands",
        "operator_type": "challenger",
        "group_id": "vodafone_group",
        "ir_url": "https://www.vodafoneziggo.nl/",
        "fiscal_year_start_month": 1,
        "fiscal_year_label": "",
        "quarter_naming": "calendar",
        "currency": "EUR",
    },

    # ========================================================================
    # Belgium
    # ========================================================================
    "proximus_be": {
        "display_name": "Proximus",
        "parent_company": "Proximus Group",
        "country": "Belgium",
        "region": "Europe",
        "market": "belgium",
        "operator_type": "incumbent",
        "ir_url": "https://www.proximus.com/investors",
        "fiscal_year_start_month": 1,
        "fiscal_year_label": "",
        "quarter_naming": "calendar",
        "currency": "EUR",
    },
    "orange_be": {
        "display_name": "Orange Belgium",
        "parent_company": "Orange S.A.",
        "country": "Belgium",
        "region": "Europe",
        "market": "belgium",
        "operator_type": "challenger",
        "ir_url": "https://corporate.orange.be/en/investors",
        "fiscal_year_start_month": 1,
        "fiscal_year_label": "",
        "quarter_naming": "calendar",
        "currency": "EUR",
    },
    "telenet_be": {
        "display_name": "Telenet",
        "parent_company": "Liberty Global (via Telenet Group)",
        "country": "Belgium",
        "region": "Europe",
        "market": "belgium",
        "operator_type": "challenger",
        "ir_url": "https://www2.telenet.be/en/investor-relations/",
        "fiscal_year_start_month": 1,
        "fiscal_year_label": "",
        "quarter_naming": "calendar",
        "currency": "EUR",
        "notes": "Cable operator, also owns BASE mobile brand. Acquired VOO (Wallonia cable) in 2023.",
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


def get_operators_for_group(group_id: str) -> list:
    """Get all operator IDs belonging to a given group."""
    return [
        op_id for op_id, info in OPERATOR_DIRECTORY.items()
        if info.get("group_id") == group_id
    ]


def get_group_info(group_id: str) -> dict:
    """Get group metadata by ID. Returns empty dict if not found."""
    return OPERATOR_GROUPS.get(group_id, {})


def get_all_markets() -> list[str]:
    """Get all unique market IDs."""
    return sorted(set(info["market"] for info in OPERATOR_DIRECTORY.values()))


def get_non_group_operators(market: str, group_id: str) -> list[str]:
    """Get operator IDs in a market that do NOT belong to a given group."""
    return [
        op_id for op_id, info in OPERATOR_DIRECTORY.items()
        if info["market"] == market and info.get("group_id") != group_id
    ]
