"""Seed the database with Honduras telecom market data.

Honduras is one of Millicom's strongest markets in Central America.
Tigo Honduras is a market leader with strong mobile and cable TV presence.
3-player market: Tigo (leader), Claro, Digicel (declining).
Currency: HNL (Honduran Lempira). All revenue figures in HNL millions.

Data sources: Millicom Q4 2025 earnings, CONATEL Honduras regulator data,
America Movil IR, Digicel Group reports.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "honduras"
OPERATORS = ["tigo_honduras", "claro_hn", "digicel_hn"]


def get_seed_data():
    return {
        "financials": {
            # Tigo Honduras — market leader, strong cable TV + broadband
            "tigo_honduras": {
                "total_revenue": [4200, 4280, 4360, 4440, 4520, 4600, 4680, 4760],
                "service_revenue": [3980, 4060, 4140, 4220, 4300, 4380, 4460, 4530],
                "service_revenue_growth_pct": [6.0, 6.3, 6.5, 6.8, 7.6, 7.5, 7.7, 7.3],
                "mobile_service_revenue": [2700, 2750, 2800, 2850, 2900, 2950, 3000, 3050],
                "mobile_service_growth_pct": [5.0, 5.3, 5.5, 5.8, 7.4, 7.3, 7.1, 7.0],
                "fixed_service_revenue": [1050, 1080, 1110, 1140, 1170, 1200, 1230, 1250],
                "fixed_service_growth_pct": [9.0, 9.3, 9.5, 9.8, 11.4, 11.1, 10.8, 9.6],
                "b2b_revenue": [230, 230, 230, 230, 230, 230, 230, 230],
                "ebitda": [1890, 1925, 1960, 2000, 2035, 2070, 2105, 2140],
                "ebitda_margin_pct": [45.0, 45.0, 45.0, 45.0, 45.0, 45.0, 45.0, 45.0],
                "ebitda_growth_pct": [5.5, 5.8, 6.0, 6.2, 7.7, 7.5, 7.4, 7.0],
                "capex": [630, 640, 655, 665, 680, 690, 700, 715],
                "capex_to_revenue_pct": [15.0, 14.9, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0],
                "employees": [2800, 2800, 2850, 2850, 2900, 2900, 2950, 2950],
                "_source": "Millicom Q4 2025 Earnings Report",
            },
            # Claro Honduras — #2 player
            "claro_hn": {
                "total_revenue": [2600, 2630, 2660, 2690, 2720, 2750, 2780, 2810],
                "service_revenue": [2450, 2480, 2510, 2540, 2570, 2600, 2630, 2660],
                "service_revenue_growth_pct": [3.0, 3.2, 3.5, 3.8, 4.5, 4.8, 4.8, 4.7],
                "mobile_service_revenue": [2050, 2070, 2100, 2130, 2160, 2190, 2220, 2250],
                "fixed_service_revenue": [280, 290, 295, 300, 300, 305, 305, 310],
                "b2b_revenue": [120, 120, 115, 110, 110, 105, 105, 100],
                "ebitda": [830, 840, 850, 860, 870, 880, 890, 900],
                "ebitda_margin_pct": [31.9, 31.9, 32.0, 32.0, 32.0, 32.0, 32.0, 32.0],
                "capex": [400, 405, 410, 415, 420, 425, 430, 435],
                "capex_to_revenue_pct": [15.4, 15.4, 15.4, 15.4, 15.4, 15.5, 15.5, 15.5],
                "employees": [2200, 2200, 2200, 2250, 2250, 2250, 2300, 2300],
                "_source": "America Movil Q4 2025 Earnings",
            },
            # Digicel Honduras — #3 player, struggling
            "digicel_hn": {
                "total_revenue": [800, 790, 780, 770, 760, 750, 740, 730],
                "service_revenue": [740, 730, 720, 710, 700, 690, 680, 670],
                "service_revenue_growth_pct": [-3.0, -3.2, -3.5, -3.8, -5.0, -5.1, -5.6, -5.6],
                "mobile_service_revenue": [680, 670, 660, 650, 640, 630, 620, 610],
                "ebitda": [200, 195, 190, 185, 180, 175, 170, 165],
                "ebitda_margin_pct": [25.0, 24.7, 24.4, 24.0, 23.7, 23.3, 23.0, 22.6],
                "capex": [90, 85, 80, 80, 75, 70, 70, 65],
                "capex_to_revenue_pct": [11.3, 10.8, 10.3, 10.4, 9.9, 9.3, 9.5, 8.9],
                "employees": [1200, 1180, 1160, 1140, 1120, 1100, 1080, 1060],
                "_source": "Digicel Group FY2025 Results",
            },
        },
        "subscribers": {
            "tigo_honduras": {
                "mobile_total_k": [5800, 5900, 6000, 6100, 6200, 6300, 6400, 6500],
                "mobile_postpaid_k": [870, 890, 900, 920, 940, 950, 960, 980],
                "mobile_prepaid_k": [4930, 5010, 5100, 5180, 5260, 5350, 5440, 5520],
                "mobile_net_adds_k": [80, 100, 100, 100, 100, 100, 100, 100],
                "mobile_churn_pct": [3.0, 2.9, 2.8, 2.8, 2.7, 2.7, 2.6, 2.6],
                "mobile_arpu": [46.6, 46.6, 46.7, 46.7, 46.8, 46.8, 46.9, 46.9],
                "broadband_total_k": [420, 435, 450, 465, 480, 495, 510, 525],
                "broadband_cable_k": [360, 370, 380, 390, 400, 410, 420, 430],
                "broadband_fiber_k": [30, 35, 40, 45, 50, 55, 60, 65],
                "broadband_net_adds_k": [12, 15, 15, 15, 15, 15, 15, 15],
                "tv_total_k": [350, 360, 370, 380, 390, 400, 410, 420],
                "b2b_customers_k": [30, 31, 32, 33, 34, 35, 36, 37],
                "_source": "Millicom Q4 2025 Earnings Report",
            },
            "claro_hn": {
                "mobile_total_k": [4200, 4230, 4260, 4290, 4320, 4350, 4380, 4410],
                "mobile_postpaid_k": [630, 640, 645, 650, 655, 660, 665, 670],
                "mobile_prepaid_k": [3570, 3590, 3615, 3640, 3665, 3690, 3715, 3740],
                "mobile_net_adds_k": [20, 30, 30, 30, 30, 30, 30, 30],
                "mobile_churn_pct": [3.2, 3.1, 3.0, 3.0, 2.9, 2.9, 2.8, 2.8],
                "mobile_arpu": [48.8, 48.9, 49.3, 49.7, 50.0, 50.3, 50.7, 51.0],
                "broadband_total_k": [180, 185, 190, 195, 200, 205, 210, 215],
                "broadband_fiber_k": [20, 22, 25, 28, 30, 33, 35, 38],
                "tv_total_k": [80, 82, 83, 85, 86, 88, 89, 90],
                "b2b_customers_k": [18, 18, 19, 19, 20, 20, 21, 21],
                "_source": "America Movil Q4 2025 Earnings",
            },
            "digicel_hn": {
                "mobile_total_k": [1800, 1780, 1760, 1740, 1720, 1700, 1680, 1660],
                "mobile_postpaid_k": [180, 178, 176, 174, 172, 170, 168, 166],
                "mobile_prepaid_k": [1620, 1602, 1584, 1566, 1548, 1530, 1512, 1494],
                "mobile_net_adds_k": [-15, -20, -20, -20, -20, -20, -20, -20],
                "mobile_churn_pct": [4.0, 4.1, 4.2, 4.2, 4.3, 4.3, 4.4, 4.4],
                "mobile_arpu": [37.8, 37.6, 37.5, 37.4, 37.2, 37.1, 36.9, 36.7],
                "_source": "Digicel Group FY2025 Results",
            },
        },
        "macro": {
            "gdp_growth_pct": 3.2,
            "inflation_pct": 5.8,
            "unemployment_pct": 8.5,
            "telecom_market_size_eur_b": 1.5,
            "telecom_growth_pct": 5.0,
            "five_g_adoption_pct": 0.0,
            "fiber_penetration_pct": 2.0,
            "regulatory_environment": "CONATEL oversight; spectrum allocation pending; limited net neutrality",
            "digital_strategy": "Honduras Digital agenda; rural connectivity focus; mobile broadband priority",
            "source_url": "CONATEL Honduras / BCH / ITU 2025",
        },
        "network": {
            "tigo_honduras": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 75,
                "fiber_homepass_k": 500,
                "cable_homepass_k": 900,
                "technology_mix": {
                    "mobile_vendor": "Ericsson",
                    "spectrum_mhz": 120,
                    "core_vendor": "Ericsson",
                },
            },
            "claro_hn": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 68,
                "fiber_homepass_k": 250,
                "technology_mix": {
                    "mobile_vendor": "Ericsson/Nokia",
                    "spectrum_mhz": 100,
                },
            },
            "digicel_hn": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 40,
                "technology_mix": {
                    "mobile_vendor": "Huawei/ZTE",
                    "spectrum_mhz": 50,
                },
            },
        },
        "executives": {
            "tigo_honduras": [
                {"name": "Juan Carlos Suazo", "title": "CEO", "start_date": "2021-03-01", "background": "Millicom LATAM leadership, previously VP Commercial"},
                {"name": "Patricia Reyes", "title": "CFO", "start_date": "2022-01-01", "background": "Financial services background"},
            ],
            "claro_hn": [
                {"name": "Roberto Sandoval", "title": "CEO", "start_date": "2020-06-01", "background": "America Movil Central America"},
            ],
            "digicel_hn": [
                {"name": "Mario Castillo", "title": "CEO", "start_date": "2023-01-01", "background": "Digicel Group regional management"},
            ],
        },
        "competitive_scores": {
            "tigo_honduras": {
                "Network Coverage": 80, "Network Quality": 76, "Brand Strength": 83,
                "Price Competitiveness": 72, "Customer Service": 70, "Digital Experience": 68,
                "Enterprise Solutions": 62, "Innovation": 65, "Distribution": 85,
            },
            "claro_hn": {
                "Network Coverage": 72, "Network Quality": 68, "Brand Strength": 75,
                "Price Competitiveness": 68, "Customer Service": 65, "Digital Experience": 60,
                "Enterprise Solutions": 55, "Innovation": 58, "Distribution": 75,
            },
            "digicel_hn": {
                "Network Coverage": 42, "Network Quality": 40, "Brand Strength": 45,
                "Price Competitiveness": 72, "Customer Service": 42, "Digital Experience": 38,
                "Enterprise Solutions": 25, "Innovation": 35, "Distribution": 50,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "tigo_honduras",
                "event_date": "2025-09-01",
                "category": "technology",
                "title": "Tigo Honduras expands HFC network to secondary cities",
                "description": "Cable broadband and TV expansion reaching 900K homes passed",
                "impact_type": "positive",
                "severity": "medium",
            },
            {
                "operator_id": "digicel_hn",
                "event_date": "2025-10-15",
                "category": "competitive",
                "title": "Digicel Honduras continues subscriber decline",
                "description": "Third consecutive quarter of subscriber losses, market exit rumors",
                "impact_type": "positive",
                "severity": "medium",
            },
        ],
        "earnings_highlights": {
            "tigo_honduras": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "Honduras mobile growth driven by data monetization and prepaid-to-postpaid migration", "speaker": "CEO"},
                {"segment": "Home", "highlight_type": "outlook", "content": "Cable TV and broadband remain key growth drivers, expanding to secondary cities", "speaker": "CEO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    """Seed Honduras market data."""
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_honduras as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
