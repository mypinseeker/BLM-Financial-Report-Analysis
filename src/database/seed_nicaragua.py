"""Seed the database with Nicaragua telecom market data.

Nicaragua is Millicom's smallest LATAM market.
2-player market: Tigo (leader ~55% share), Claro.
Currency: NIO (Nicaraguan Cordoba). All revenue figures in NIO millions.

Data sources: Millicom Q4 2025 earnings, TELCOR Nicaragua, America Movil IR.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "nicaragua"
OPERATORS = ["tigo_nicaragua", "claro_ni"]


def get_seed_data():
    return {
        "financials": {
            "tigo_nicaragua": {
                "total_revenue": [2200, 2230, 2260, 2290, 2320, 2350, 2380, 2410],
                "service_revenue": [2080, 2110, 2140, 2170, 2200, 2230, 2260, 2290],
                "service_revenue_growth_pct": [4.5, 4.8, 5.0, 5.2, 5.5, 5.7, 5.6, 5.5],
                "mobile_service_revenue": [1700, 1720, 1740, 1760, 1780, 1800, 1820, 1840],
                "mobile_service_growth_pct": [4.0, 4.2, 4.5, 4.8, 4.7, 4.7, 4.6, 4.4],
                "fixed_service_revenue": [280, 290, 300, 310, 320, 330, 340, 350],
                "fixed_service_growth_pct": [8.0, 8.3, 8.6, 8.8, 14.3, 13.8, 13.3, 12.9],
                "b2b_revenue": [100, 100, 100, 100, 100, 100, 100, 100],
                "ebitda": [990, 1005, 1020, 1030, 1045, 1060, 1070, 1085],
                "ebitda_margin_pct": [45.0, 45.1, 45.1, 45.0, 45.0, 45.1, 45.0, 45.0],
                "ebitda_growth_pct": [4.0, 4.3, 4.5, 4.8, 5.6, 5.5, 4.9, 5.3],
                "capex": [330, 335, 340, 345, 350, 355, 360, 365],
                "capex_to_revenue_pct": [15.0, 15.0, 15.0, 15.1, 15.1, 15.1, 15.1, 15.1],
                "employees": [1500, 1500, 1520, 1520, 1540, 1540, 1560, 1560],
                "_source": "Millicom Q4 2025 Earnings Report",
            },
            "claro_ni": {
                "total_revenue": [1650, 1660, 1670, 1680, 1690, 1700, 1710, 1720],
                "service_revenue": [1550, 1560, 1570, 1580, 1590, 1600, 1610, 1620],
                "service_revenue_growth_pct": [2.5, 2.7, 2.8, 3.0, 2.6, 2.6, 2.5, 2.5],
                "mobile_service_revenue": [1350, 1358, 1366, 1374, 1382, 1390, 1398, 1406],
                "fixed_service_revenue": [150, 152, 154, 156, 158, 160, 162, 164],
                "ebitda": [510, 513, 517, 520, 523, 527, 530, 533],
                "ebitda_margin_pct": [30.9, 30.9, 31.0, 31.0, 30.9, 31.0, 31.0, 31.0],
                "capex": [265, 267, 269, 271, 273, 275, 277, 279],
                "capex_to_revenue_pct": [16.1, 16.1, 16.1, 16.1, 16.2, 16.2, 16.2, 16.2],
                "employees": [1400, 1400, 1400, 1400, 1420, 1420, 1420, 1420],
                "_source": "America Movil Q4 2025 Earnings",
            },
        },
        "subscribers": {
            "tigo_nicaragua": {
                "mobile_total_k": [3800, 3850, 3900, 3950, 4000, 4050, 4100, 4150],
                "mobile_postpaid_k": [380, 385, 390, 395, 400, 405, 410, 415],
                "mobile_prepaid_k": [3420, 3465, 3510, 3555, 3600, 3645, 3690, 3735],
                "mobile_net_adds_k": [40, 50, 50, 50, 50, 50, 50, 50],
                "mobile_churn_pct": [3.0, 2.9, 2.9, 2.8, 2.8, 2.7, 2.7, 2.6],
                "mobile_arpu": [44.7, 44.7, 44.6, 44.6, 44.5, 44.4, 44.4, 44.3],
                "broadband_total_k": [130, 135, 140, 145, 150, 155, 160, 165],
                "broadband_cable_k": [110, 113, 116, 119, 122, 125, 128, 131],
                "broadband_fiber_k": [8, 10, 12, 14, 16, 18, 20, 22],
                "broadband_net_adds_k": [4, 5, 5, 5, 5, 5, 5, 5],
                "tv_total_k": [90, 93, 96, 99, 102, 105, 108, 111],
                "b2b_customers_k": [10, 10, 11, 11, 11, 12, 12, 12],
                "_source": "Millicom Q4 2025 Earnings Report",
            },
            "claro_ni": {
                "mobile_total_k": [2800, 2810, 2820, 2830, 2840, 2850, 2860, 2870],
                "mobile_postpaid_k": [280, 282, 284, 286, 288, 290, 292, 294],
                "mobile_prepaid_k": [2520, 2528, 2536, 2544, 2552, 2560, 2568, 2576],
                "mobile_net_adds_k": [5, 10, 10, 10, 10, 10, 10, 10],
                "mobile_churn_pct": [3.2, 3.1, 3.0, 3.0, 2.9, 2.9, 2.8, 2.8],
                "mobile_arpu": [48.2, 48.3, 48.4, 48.5, 48.7, 48.8, 48.9, 49.0],
                "broadband_total_k": [60, 62, 64, 66, 68, 70, 72, 74],
                "tv_total_k": [25, 26, 27, 28, 29, 30, 31, 32],
                "_source": "America Movil Q4 2025 Earnings",
            },
        },
        "macro": {
            "gdp_growth_pct": 3.5,
            "inflation_pct": 6.0,
            "unemployment_pct": 5.5,
            "telecom_market_size_eur_b": 0.6,
            "telecom_growth_pct": 4.0,
            "five_g_adoption_pct": 0.0,
            "fiber_penetration_pct": 1.5,
            "regulatory_environment": "TELCOR oversight; political constraints on foreign investment; limited regulatory independence",
            "digital_strategy": "Limited government digital plan; mobile broadband as primary internet access",
            "source_url": "TELCOR Nicaragua / BCN / ITU 2025",
        },
        "network": {
            "tigo_nicaragua": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 60,
                "fiber_homepass_k": 120,
                "cable_homepass_k": 350,
                "technology_mix": {"mobile_vendor": "Ericsson", "spectrum_mhz": 90, "core_vendor": "Ericsson"},
            },
            "claro_ni": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 52,
                "fiber_homepass_k": 80,
                "technology_mix": {"mobile_vendor": "Ericsson/Nokia", "spectrum_mhz": 80},
            },
        },
        "executives": {
            "tigo_nicaragua": [
                {"name": "Ernesto Chamorro", "title": "CEO", "start_date": "2021-01-01", "background": "Millicom Central America"},
            ],
            "claro_ni": [
                {"name": "Rafael Solano", "title": "CEO", "start_date": "2020-06-01", "background": "America Movil regional management"},
            ],
        },
        "competitive_scores": {
            "tigo_nicaragua": {
                "Network Coverage": 68, "Network Quality": 62, "Brand Strength": 75,
                "Price Competitiveness": 70, "Customer Service": 62, "Digital Experience": 55,
                "Enterprise Solutions": 45, "Innovation": 55, "Distribution": 78,
            },
            "claro_ni": {
                "Network Coverage": 58, "Network Quality": 55, "Brand Strength": 65,
                "Price Competitiveness": 65, "Customer Service": 55, "Digital Experience": 48,
                "Enterprise Solutions": 40, "Innovation": 45, "Distribution": 68,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "tigo_nicaragua",
                "event_date": "2025-08-15",
                "category": "technology",
                "title": "Tigo Nicaragua expands 4G to Pacific coast cities",
                "description": "4G LTE coverage expansion reaching 60% population coverage",
                "impact_type": "positive",
                "severity": "medium",
            },
        ],
        "earnings_highlights": {
            "tigo_nicaragua": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "Nicaragua remains stable with steady mobile growth despite political challenges", "speaker": "CEO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_nicaragua as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
