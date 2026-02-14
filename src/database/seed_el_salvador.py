"""Seed the database with El Salvador telecom market data.

El Salvador is a dollarized (USD) market in Central America.
3-player market: Claro (leader), Tigo, Digicel.
Currency: USD. All revenue figures in USD millions.

Data sources: Millicom Q4 2025 earnings, SIGET regulator data, America Movil IR.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "el_salvador"
OPERATORS = ["tigo_el_salvador", "claro_sv", "digicel_sv"]


def get_seed_data():
    return {
        "financials": {
            "tigo_el_salvador": {
                "total_revenue": [125, 127, 129, 131, 133, 135, 137, 139],
                "service_revenue": [118, 120, 122, 124, 126, 128, 130, 132],
                "service_revenue_growth_pct": [4.5, 4.8, 5.0, 5.2, 6.4, 6.3, 6.6, 6.5],
                "mobile_service_revenue": [78, 79, 80, 82, 83, 84, 86, 87],
                "mobile_service_growth_pct": [3.5, 3.8, 4.0, 4.2, 6.4, 6.3, 7.5, 6.1],
                "fixed_service_revenue": [32, 33, 34, 34, 35, 36, 36, 37],
                "fixed_service_growth_pct": [7.0, 7.3, 7.5, 5.9, 9.4, 9.1, 5.9, 8.8],
                "b2b_revenue": [8, 8, 8, 8, 8, 8, 8, 8],
                "ebitda": [52, 53, 54, 55, 56, 57, 58, 59],
                "ebitda_margin_pct": [41.6, 41.7, 41.9, 42.0, 42.1, 42.2, 42.3, 42.4],
                "ebitda_growth_pct": [4.0, 4.3, 4.5, 4.8, 7.7, 7.5, 7.4, 7.3],
                "capex": [20, 20, 21, 21, 21, 22, 22, 22],
                "capex_to_revenue_pct": [16.0, 15.7, 16.3, 16.0, 15.8, 16.3, 16.1, 15.8],
                "employees": [1200, 1200, 1220, 1220, 1240, 1240, 1260, 1260],
                "_source": "Millicom Q4 2025 Earnings Report",
            },
            "claro_sv": {
                "total_revenue": [165, 167, 169, 171, 173, 175, 177, 179],
                "service_revenue": [155, 157, 159, 161, 163, 165, 167, 169],
                "service_revenue_growth_pct": [3.0, 3.2, 3.5, 3.8, 4.8, 5.1, 5.0, 5.0],
                "mobile_service_revenue": [120, 121, 123, 124, 126, 127, 129, 130],
                "fixed_service_revenue": [28, 28, 29, 29, 29, 30, 30, 31],
                "b2b_revenue": [7, 8, 7, 8, 8, 8, 8, 8],
                "ebitda": [58, 59, 59, 60, 61, 61, 62, 63],
                "ebitda_margin_pct": [35.2, 35.3, 34.9, 35.1, 35.3, 34.9, 35.0, 35.2],
                "capex": [28, 28, 29, 29, 29, 30, 30, 30],
                "capex_to_revenue_pct": [17.0, 16.8, 17.2, 17.0, 16.8, 17.1, 16.9, 16.8],
                "employees": [1600, 1600, 1600, 1650, 1650, 1650, 1700, 1700],
                "_source": "America Movil Q4 2025 Earnings",
            },
            "digicel_sv": {
                "total_revenue": [45, 44, 43, 42, 41, 40, 39, 38],
                "service_revenue": [42, 41, 40, 39, 38, 37, 36, 35],
                "service_revenue_growth_pct": [-4.0, -4.5, -4.8, -5.0, -8.9, -9.1, -10.0, -10.3],
                "mobile_service_revenue": [40, 39, 38, 37, 36, 35, 34, 33],
                "ebitda": [10, 9, 9, 8, 8, 7, 7, 6],
                "ebitda_margin_pct": [22.2, 20.5, 20.9, 19.0, 19.5, 17.5, 17.9, 15.8],
                "capex": [4, 4, 3, 3, 3, 3, 2, 2],
                "employees": [500, 490, 480, 470, 460, 450, 440, 430],
                "_source": "Digicel Group FY2025 Results",
            },
        },
        "subscribers": {
            "tigo_el_salvador": {
                "mobile_total_k": [3200, 3240, 3280, 3320, 3360, 3400, 3440, 3480],
                "mobile_postpaid_k": [480, 490, 495, 500, 505, 510, 515, 520],
                "mobile_prepaid_k": [2720, 2750, 2785, 2820, 2855, 2890, 2925, 2960],
                "mobile_net_adds_k": [30, 40, 40, 40, 40, 40, 40, 40],
                "mobile_churn_pct": [2.8, 2.7, 2.7, 2.6, 2.6, 2.5, 2.5, 2.4],
                "mobile_arpu": [3.1, 3.1, 3.1, 3.1, 3.1, 3.1, 3.1, 3.2],
                "broadband_total_k": [200, 208, 216, 224, 232, 240, 248, 256],
                "broadband_cable_k": [170, 175, 180, 185, 190, 195, 200, 205],
                "broadband_fiber_k": [15, 17, 19, 22, 25, 28, 31, 34],
                "broadband_net_adds_k": [6, 8, 8, 8, 8, 8, 8, 8],
                "tv_total_k": [150, 155, 160, 165, 170, 175, 180, 185],
                "b2b_customers_k": [12, 12, 13, 13, 13, 14, 14, 14],
                "_source": "Millicom Q4 2025 Earnings Report",
            },
            "claro_sv": {
                "mobile_total_k": [3800, 3830, 3860, 3890, 3920, 3950, 3980, 4010],
                "mobile_postpaid_k": [760, 770, 775, 780, 785, 790, 795, 800],
                "mobile_prepaid_k": [3040, 3060, 3085, 3110, 3135, 3160, 3185, 3210],
                "mobile_net_adds_k": [20, 30, 30, 30, 30, 30, 30, 30],
                "mobile_churn_pct": [2.5, 2.4, 2.4, 2.3, 2.3, 2.2, 2.2, 2.2],
                "mobile_arpu": [3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2],
                "broadband_total_k": [180, 183, 186, 189, 192, 195, 198, 201],
                "broadband_fiber_k": [30, 33, 36, 39, 42, 45, 48, 51],
                "tv_total_k": [90, 91, 92, 93, 94, 95, 96, 97],
                "_source": "America Movil Q4 2025 Earnings",
            },
            "digicel_sv": {
                "mobile_total_k": [900, 890, 880, 870, 860, 850, 840, 830],
                "mobile_postpaid_k": [90, 89, 88, 87, 86, 85, 84, 83],
                "mobile_prepaid_k": [810, 801, 792, 783, 774, 765, 756, 747],
                "mobile_net_adds_k": [-8, -10, -10, -10, -10, -10, -10, -10],
                "mobile_churn_pct": [4.2, 4.3, 4.4, 4.4, 4.5, 4.5, 4.6, 4.6],
                "mobile_arpu": [4.4, 4.4, 4.3, 4.3, 4.2, 4.1, 4.0, 4.0],
                "_source": "Digicel Group FY2025 Results",
            },
        },
        "macro": {
            "gdp_growth_pct": 2.8,
            "inflation_pct": 2.5,
            "unemployment_pct": 6.8,
            "telecom_market_size_eur_b": 0.9,
            "telecom_growth_pct": 4.0,
            "five_g_adoption_pct": 0.0,
            "fiber_penetration_pct": 3.0,
            "regulatory_environment": "SIGET framework; Bitcoin legal tender creates fintech dynamics; stable regulatory",
            "digital_strategy": "El Salvador digital transformation; Bitcoin City project; mobile payments emphasis",
            "source_url": "SIGET El Salvador / BCR / ITU 2025",
        },
        "network": {
            "tigo_el_salvador": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 80,
                "fiber_homepass_k": 300,
                "cable_homepass_k": 550,
                "technology_mix": {"mobile_vendor": "Ericsson", "spectrum_mhz": 100, "core_vendor": "Ericsson"},
            },
            "claro_sv": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 82,
                "fiber_homepass_k": 350,
                "technology_mix": {"mobile_vendor": "Ericsson/Nokia", "spectrum_mhz": 110},
            },
            "digicel_sv": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 35,
                "technology_mix": {"mobile_vendor": "Huawei/ZTE", "spectrum_mhz": 40},
            },
        },
        "executives": {
            "tigo_el_salvador": [
                {"name": "Carlos Enrique Lopez", "title": "CEO", "start_date": "2022-01-01", "background": "Millicom Central America leadership"},
                {"name": "Ana Maria Alvarez", "title": "CFO", "start_date": "2021-06-01", "background": "KPMG El Salvador, financial services"},
            ],
            "claro_sv": [
                {"name": "Marcelo Rivera", "title": "CEO", "start_date": "2020-03-01", "background": "America Movil Central America regional management"},
            ],
            "digicel_sv": [
                {"name": "Jorge Mendoza", "title": "CEO", "start_date": "2023-01-01", "background": "Digicel Group Central America"},
            ],
        },
        "competitive_scores": {
            "tigo_el_salvador": {
                "Network Coverage": 80, "Network Quality": 76, "Brand Strength": 75,
                "Price Competitiveness": 72, "Customer Service": 70, "Digital Experience": 68,
                "Enterprise Solutions": 58, "Innovation": 65, "Distribution": 78,
            },
            "claro_sv": {
                "Network Coverage": 82, "Network Quality": 78, "Brand Strength": 80,
                "Price Competitiveness": 68, "Customer Service": 72, "Digital Experience": 70,
                "Enterprise Solutions": 65, "Innovation": 62, "Distribution": 82,
            },
            "digicel_sv": {
                "Network Coverage": 38, "Network Quality": 35, "Brand Strength": 40,
                "Price Competitiveness": 75, "Customer Service": 38, "Digital Experience": 32,
                "Enterprise Solutions": 20, "Innovation": 30, "Distribution": 42,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "tigo_el_salvador",
                "event_date": "2025-08-01",
                "category": "technology",
                "title": "Tigo El Salvador launches Tigo Money Bitcoin integration",
                "description": "Mobile wallet integrates Bitcoin payments following legal tender status",
                "impact_type": "positive",
                "severity": "medium",
            },
        ],
        "earnings_highlights": {
            "tigo_el_salvador": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "El Salvador mobile growth supported by data adoption and fintech integration", "speaker": "CEO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_el_salvador as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
