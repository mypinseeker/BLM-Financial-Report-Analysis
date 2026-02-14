"""Seed the database with Panama telecom market data.

Panama is a dollarized (USD) market with high GDP per capita for LATAM.
3-player market: Claro (leader), Tigo, Digicel.
Currency: USD. All revenue figures in USD millions.

Data sources: Millicom Q4 2025 earnings, ASEP Panama regulator data, America Movil IR.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "panama"
OPERATORS = ["tigo_panama", "claro_pa", "digicel_pa"]


def get_seed_data():
    return {
        "financials": {
            "tigo_panama": {
                "total_revenue": [140, 143, 146, 149, 152, 155, 158, 161],
                "service_revenue": [132, 135, 138, 141, 144, 147, 150, 153],
                "service_revenue_growth_pct": [5.0, 5.3, 5.5, 5.8, 8.6, 8.9, 8.7, 8.5],
                "mobile_service_revenue": [88, 90, 92, 94, 96, 98, 100, 102],
                "mobile_service_growth_pct": [4.0, 4.3, 4.5, 4.8, 9.1, 8.9, 8.7, 8.5],
                "fixed_service_revenue": [36, 37, 38, 39, 40, 41, 42, 43],
                "fixed_service_growth_pct": [8.0, 8.3, 8.5, 8.8, 11.1, 10.8, 10.5, 10.3],
                "b2b_revenue": [8, 8, 8, 8, 8, 8, 8, 8],
                "ebitda": [60, 61, 63, 64, 66, 67, 68, 70],
                "ebitda_margin_pct": [42.9, 42.7, 43.2, 43.0, 43.4, 43.2, 43.0, 43.5],
                "ebitda_growth_pct": [4.5, 4.8, 6.8, 4.8, 10.0, 9.8, 7.9, 9.4],
                "capex": [22, 23, 23, 24, 24, 25, 25, 26],
                "capex_to_revenue_pct": [15.7, 16.1, 15.8, 16.1, 15.8, 16.1, 15.8, 16.1],
                "employees": [1100, 1100, 1120, 1120, 1140, 1140, 1160, 1160],
                "_source": "Millicom Q4 2025 Earnings Report",
            },
            "claro_pa": {
                "total_revenue": [200, 203, 206, 209, 212, 215, 218, 221],
                "service_revenue": [188, 191, 194, 197, 200, 203, 206, 209],
                "service_revenue_growth_pct": [3.5, 3.8, 4.0, 4.2, 6.0, 6.3, 6.2, 6.1],
                "mobile_service_revenue": [140, 142, 144, 146, 148, 150, 152, 154],
                "fixed_service_revenue": [40, 41, 42, 43, 44, 45, 46, 47],
                "b2b_revenue": [8, 8, 8, 8, 8, 8, 8, 8],
                "ebitda": [76, 77, 78, 80, 81, 82, 83, 85],
                "ebitda_margin_pct": [38.0, 37.9, 37.9, 38.3, 38.2, 38.1, 38.1, 38.5],
                "capex": [34, 35, 35, 36, 36, 37, 37, 38],
                "capex_to_revenue_pct": [17.0, 17.2, 17.0, 17.2, 17.0, 17.2, 17.0, 17.2],
                "employees": [1800, 1800, 1800, 1850, 1850, 1850, 1900, 1900],
                "_source": "America Movil Q4 2025 Earnings",
            },
            "digicel_pa": {
                "total_revenue": [60, 59, 58, 57, 56, 55, 54, 53],
                "service_revenue": [56, 55, 54, 53, 52, 51, 50, 49],
                "service_revenue_growth_pct": [-3.5, -3.8, -4.0, -4.2, -6.7, -7.3, -7.4, -7.5],
                "mobile_service_revenue": [52, 51, 50, 49, 48, 47, 46, 45],
                "ebitda": [14, 13, 13, 12, 12, 11, 11, 10],
                "ebitda_margin_pct": [23.3, 22.0, 22.4, 21.1, 21.4, 20.0, 20.4, 18.9],
                "capex": [6, 5, 5, 5, 5, 4, 4, 4],
                "employees": [600, 590, 580, 570, 560, 550, 540, 530],
                "_source": "Digicel Group FY2025 Results",
            },
        },
        "subscribers": {
            "tigo_panama": {
                "mobile_total_k": [2100, 2130, 2160, 2190, 2220, 2250, 2280, 2310],
                "mobile_postpaid_k": [525, 535, 540, 550, 555, 565, 570, 580],
                "mobile_prepaid_k": [1575, 1595, 1620, 1640, 1665, 1685, 1710, 1730],
                "mobile_net_adds_k": [22, 30, 30, 30, 30, 30, 30, 30],
                "mobile_churn_pct": [2.5, 2.4, 2.4, 2.3, 2.3, 2.2, 2.2, 2.1],
                "mobile_arpu": [4.2, 4.2, 4.3, 4.3, 4.3, 4.4, 4.4, 4.4],
                "broadband_total_k": [180, 186, 192, 198, 204, 210, 216, 222],
                "broadband_cable_k": [140, 143, 146, 149, 152, 155, 158, 161],
                "broadband_fiber_k": [25, 28, 31, 34, 37, 40, 43, 46],
                "broadband_net_adds_k": [5, 6, 6, 6, 6, 6, 6, 6],
                "tv_total_k": [140, 143, 146, 149, 152, 155, 158, 161],
                "b2b_customers_k": [10, 10, 11, 11, 11, 12, 12, 12],
                "_source": "Millicom Q4 2025 Earnings Report",
            },
            "claro_pa": {
                "mobile_total_k": [2500, 2520, 2540, 2560, 2580, 2600, 2620, 2640],
                "mobile_postpaid_k": [750, 760, 765, 770, 775, 780, 785, 790],
                "mobile_prepaid_k": [1750, 1760, 1775, 1790, 1805, 1820, 1835, 1850],
                "mobile_net_adds_k": [15, 20, 20, 20, 20, 20, 20, 20],
                "mobile_churn_pct": [2.2, 2.2, 2.1, 2.1, 2.0, 2.0, 2.0, 1.9],
                "mobile_arpu": [5.6, 5.6, 5.7, 5.7, 5.7, 5.8, 5.8, 5.8],
                "broadband_total_k": [220, 224, 228, 232, 236, 240, 244, 248],
                "broadband_fiber_k": [60, 64, 68, 72, 76, 80, 84, 88],
                "tv_total_k": [120, 122, 124, 126, 128, 130, 132, 134],
                "_source": "America Movil Q4 2025 Earnings",
            },
            "digicel_pa": {
                "mobile_total_k": [900, 892, 884, 876, 868, 860, 852, 844],
                "mobile_postpaid_k": [90, 89, 88, 88, 87, 86, 85, 84],
                "mobile_prepaid_k": [810, 803, 796, 788, 781, 774, 767, 760],
                "mobile_net_adds_k": [-6, -8, -8, -8, -8, -8, -8, -8],
                "mobile_churn_pct": [4.0, 4.1, 4.2, 4.2, 4.3, 4.3, 4.4, 4.4],
                "mobile_arpu": [5.8, 5.7, 5.7, 5.6, 5.5, 5.5, 5.4, 5.3],
                "_source": "Digicel Group FY2025 Results",
            },
        },
        "macro": {
            "gdp_growth_pct": 5.0,
            "inflation_pct": 2.0,
            "unemployment_pct": 7.5,
            "telecom_market_size_eur_b": 1.1,
            "telecom_growth_pct": 5.0,
            "five_g_adoption_pct": 0.0,
            "fiber_penetration_pct": 8.0,
            "regulatory_environment": "ASEP regulatory framework; dollarized economy; Canal Zone drives enterprise demand",
            "digital_strategy": "Panama Hub Digital; connectivity for logistics corridor; data center growth",
            "source_url": "ASEP Panama / MEF / ITU 2025",
        },
        "network": {
            "tigo_panama": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 82,
                "fiber_homepass_k": 250,
                "cable_homepass_k": 450,
                "technology_mix": {"mobile_vendor": "Ericsson", "spectrum_mhz": 100, "core_vendor": "Ericsson"},
            },
            "claro_pa": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 85,
                "fiber_homepass_k": 400,
                "technology_mix": {"mobile_vendor": "Ericsson/Nokia", "spectrum_mhz": 120},
            },
            "digicel_pa": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 42,
                "technology_mix": {"mobile_vendor": "Huawei", "spectrum_mhz": 50},
            },
        },
        "executives": {
            "tigo_panama": [
                {"name": "Pedro Hernandez", "title": "CEO", "start_date": "2021-01-01", "background": "Millicom Central America leadership"},
            ],
            "claro_pa": [
                {"name": "Eduardo Castaneda", "title": "CEO", "start_date": "2019-06-01", "background": "America Movil regional executive"},
            ],
            "digicel_pa": [
                {"name": "Luis Bermudez", "title": "CEO", "start_date": "2022-01-01", "background": "Digicel Group management"},
            ],
        },
        "competitive_scores": {
            "tigo_panama": {
                "Network Coverage": 80, "Network Quality": 78, "Brand Strength": 75,
                "Price Competitiveness": 72, "Customer Service": 70, "Digital Experience": 70,
                "Enterprise Solutions": 60, "Innovation": 65, "Distribution": 78,
            },
            "claro_pa": {
                "Network Coverage": 85, "Network Quality": 82, "Brand Strength": 82,
                "Price Competitiveness": 65, "Customer Service": 72, "Digital Experience": 72,
                "Enterprise Solutions": 70, "Innovation": 68, "Distribution": 85,
            },
            "digicel_pa": {
                "Network Coverage": 42, "Network Quality": 40, "Brand Strength": 42,
                "Price Competitiveness": 72, "Customer Service": 40, "Digital Experience": 35,
                "Enterprise Solutions": 22, "Innovation": 32, "Distribution": 48,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "tigo_panama",
                "event_date": "2025-10-01",
                "category": "technology",
                "title": "Tigo Panama expands fiber broadband to Panama City suburbs",
                "description": "FTTH deployment reaching 250K homes in Greater Panama City",
                "impact_type": "positive",
                "severity": "medium",
            },
        ],
        "earnings_highlights": {
            "tigo_panama": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "Panama mobile growth driven by data monetization in high-ARPU market", "speaker": "CEO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_panama as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
