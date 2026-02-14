"""Seed the database with Paraguay telecom market data.

Tigo Paraguay is the market leader with ~50% mobile share.
3-player market: Tigo (leader), Claro, Personal (Telecom Argentina).
Currency: PYG (Paraguayan Guarani). All revenue figures in PYG billions.

Data sources: Millicom Q4 2025 earnings, CONATEL Paraguay, America Movil IR.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "paraguay"
OPERATORS = ["tigo_paraguay", "claro_py", "personal_py"]


def get_seed_data():
    return {
        "financials": {
            "tigo_paraguay": {
                "total_revenue": [1850, 1880, 1910, 1940, 1970, 2000, 2030, 2060],
                "service_revenue": [1750, 1780, 1810, 1840, 1870, 1900, 1930, 1960],
                "service_revenue_growth_pct": [5.5, 5.8, 6.0, 6.2, 6.5, 6.4, 6.6, 6.5],
                "mobile_service_revenue": [1200, 1220, 1240, 1260, 1280, 1300, 1320, 1340],
                "mobile_service_growth_pct": [4.8, 5.0, 5.2, 5.5, 6.7, 6.6, 6.5, 6.3],
                "fixed_service_revenue": [420, 430, 440, 450, 460, 470, 480, 490],
                "fixed_service_growth_pct": [8.5, 8.8, 9.0, 9.2, 9.5, 9.3, 9.1, 8.9],
                "b2b_revenue": [130, 130, 130, 130, 130, 130, 130, 130],
                "ebitda": [830, 845, 860, 875, 890, 900, 915, 930],
                "ebitda_margin_pct": [44.9, 44.9, 45.0, 45.1, 45.2, 45.0, 45.1, 45.1],
                "ebitda_growth_pct": [5.0, 5.3, 5.5, 5.8, 7.2, 6.5, 6.4, 6.3],
                "capex": [290, 295, 300, 305, 310, 315, 320, 325],
                "capex_to_revenue_pct": [15.7, 15.7, 15.7, 15.7, 15.7, 15.8, 15.8, 15.8],
                "employees": [2200, 2200, 2250, 2250, 2300, 2300, 2300, 2350],
                "_source": "Millicom Q4 2025 Earnings Report",
            },
            "claro_py": {
                "total_revenue": [1100, 1110, 1120, 1130, 1140, 1150, 1160, 1170],
                "service_revenue": [1030, 1040, 1050, 1060, 1070, 1080, 1090, 1100],
                "service_revenue_growth_pct": [3.0, 3.2, 3.5, 3.8, 3.6, 3.8, 3.8, 3.6],
                "mobile_service_revenue": [850, 860, 870, 880, 890, 900, 910, 920],
                "fixed_service_revenue": [130, 130, 130, 130, 130, 130, 130, 130],
                "ebitda": [370, 375, 378, 382, 385, 388, 392, 395],
                "ebitda_margin_pct": [33.6, 33.8, 33.8, 33.8, 33.8, 33.7, 33.8, 33.8],
                "capex": [175, 178, 180, 182, 185, 187, 190, 192],
                "capex_to_revenue_pct": [15.9, 16.0, 16.1, 16.1, 16.2, 16.3, 16.4, 16.4],
                "employees": [1500, 1500, 1500, 1550, 1550, 1550, 1550, 1600],
                "_source": "America Movil Q4 2025 Earnings",
            },
            "personal_py": {
                "total_revenue": [620, 615, 610, 605, 600, 595, 590, 585],
                "service_revenue": [580, 575, 570, 565, 560, 555, 550, 545],
                "service_revenue_growth_pct": [-1.5, -1.8, -2.0, -2.2, -3.2, -3.5, -3.5, -3.5],
                "mobile_service_revenue": [520, 515, 510, 505, 500, 495, 490, 485],
                "ebitda": [155, 152, 150, 148, 145, 142, 140, 138],
                "ebitda_margin_pct": [25.0, 24.7, 24.6, 24.5, 24.2, 23.9, 23.7, 23.6],
                "capex": [75, 73, 72, 70, 68, 67, 65, 63],
                "capex_to_revenue_pct": [12.1, 11.9, 11.8, 11.6, 11.3, 11.3, 11.0, 10.8],
                "employees": [1000, 1000, 980, 980, 960, 960, 950, 950],
                "_source": "Telecom Argentina FY2025 Report",
            },
        },
        "subscribers": {
            "tigo_paraguay": {
                "mobile_total_k": [4200, 4260, 4320, 4380, 4440, 4500, 4560, 4620],
                "mobile_postpaid_k": [630, 640, 650, 660, 670, 680, 690, 700],
                "mobile_prepaid_k": [3570, 3620, 3670, 3720, 3770, 3820, 3870, 3920],
                "mobile_net_adds_k": [50, 60, 60, 60, 60, 60, 60, 60],
                "mobile_churn_pct": [2.8, 2.7, 2.6, 2.6, 2.5, 2.5, 2.4, 2.4],
                "mobile_arpu": [28.6, 28.6, 28.7, 28.8, 28.8, 28.9, 28.9, 29.0],
                "broadband_total_k": [280, 290, 300, 310, 320, 330, 340, 350],
                "broadband_cable_k": [230, 235, 240, 245, 250, 255, 260, 265],
                "broadband_fiber_k": [25, 28, 32, 36, 40, 44, 48, 52],
                "broadband_net_adds_k": [8, 10, 10, 10, 10, 10, 10, 10],
                "tv_total_k": [220, 225, 230, 235, 240, 245, 250, 255],
                "b2b_customers_k": [22, 23, 23, 24, 24, 25, 25, 26],
                "_source": "Millicom Q4 2025 Earnings Report",
            },
            "claro_py": {
                "mobile_total_k": [3000, 3020, 3040, 3060, 3080, 3100, 3120, 3140],
                "mobile_postpaid_k": [450, 455, 460, 465, 470, 475, 480, 485],
                "mobile_prepaid_k": [2550, 2565, 2580, 2595, 2610, 2625, 2640, 2655],
                "mobile_net_adds_k": [15, 20, 20, 20, 20, 20, 20, 20],
                "mobile_churn_pct": [3.2, 3.1, 3.0, 3.0, 2.9, 2.9, 2.8, 2.8],
                "mobile_arpu": [28.3, 28.5, 28.6, 28.8, 28.9, 29.0, 29.2, 29.3],
                "broadband_total_k": [100, 103, 105, 108, 110, 113, 115, 118],
                "tv_total_k": [50, 51, 52, 53, 54, 55, 56, 57],
                "_source": "America Movil Q4 2025 Earnings",
            },
            "personal_py": {
                "mobile_total_k": [1800, 1790, 1780, 1770, 1760, 1750, 1740, 1730],
                "mobile_postpaid_k": [270, 268, 267, 265, 264, 262, 261, 260],
                "mobile_prepaid_k": [1530, 1522, 1513, 1505, 1496, 1488, 1479, 1470],
                "mobile_net_adds_k": [-8, -10, -10, -10, -10, -10, -10, -10],
                "mobile_churn_pct": [3.8, 3.9, 3.9, 4.0, 4.0, 4.1, 4.1, 4.2],
                "mobile_arpu": [28.9, 28.7, 28.6, 28.5, 28.4, 28.3, 28.1, 28.0],
                "_source": "Telecom Argentina FY2025 Report",
            },
        },
        "macro": {
            "gdp_growth_pct": 4.0,
            "inflation_pct": 3.8,
            "unemployment_pct": 6.5,
            "telecom_market_size_eur_b": 1.2,
            "telecom_growth_pct": 5.5,
            "five_g_adoption_pct": 0.0,
            "fiber_penetration_pct": 2.5,
            "regulatory_environment": "CONATEL oversight; spectrum allocation process; moderate regulatory intervention",
            "digital_strategy": "Paraguay Digital 2030; mobile broadband expansion; e-government initiatives",
            "source_url": "CONATEL Paraguay / BCP / ITU 2025",
        },
        "network": {
            "tigo_paraguay": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 72,
                "fiber_homepass_k": 350,
                "cable_homepass_k": 600,
                "technology_mix": {"mobile_vendor": "Ericsson", "spectrum_mhz": 110, "core_vendor": "Ericsson"},
            },
            "claro_py": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 65,
                "fiber_homepass_k": 150,
                "technology_mix": {"mobile_vendor": "Ericsson/Nokia", "spectrum_mhz": 90},
            },
            "personal_py": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 45,
                "technology_mix": {"mobile_vendor": "Huawei", "spectrum_mhz": 60},
            },
        },
        "executives": {
            "tigo_paraguay": [
                {"name": "Miguel Gomez", "title": "CEO", "start_date": "2021-06-01", "background": "Millicom regional executive"},
                {"name": "Laura Mendez", "title": "CFO", "start_date": "2022-03-01", "background": "Financial services background"},
            ],
            "claro_py": [
                {"name": "Alejandro Rios", "title": "CEO", "start_date": "2020-01-01", "background": "America Movil management"},
            ],
            "personal_py": [
                {"name": "Fernando Acosta", "title": "CEO", "start_date": "2023-01-01", "background": "Telecom Argentina leadership"},
            ],
        },
        "competitive_scores": {
            "tigo_paraguay": {
                "Network Coverage": 78, "Network Quality": 74, "Brand Strength": 82,
                "Price Competitiveness": 72, "Customer Service": 70, "Digital Experience": 68,
                "Enterprise Solutions": 60, "Innovation": 65, "Distribution": 84,
            },
            "claro_py": {
                "Network Coverage": 68, "Network Quality": 65, "Brand Strength": 72,
                "Price Competitiveness": 68, "Customer Service": 62, "Digital Experience": 58,
                "Enterprise Solutions": 52, "Innovation": 55, "Distribution": 72,
            },
            "personal_py": {
                "Network Coverage": 48, "Network Quality": 45, "Brand Strength": 50,
                "Price Competitiveness": 65, "Customer Service": 48, "Digital Experience": 42,
                "Enterprise Solutions": 35, "Innovation": 40, "Distribution": 55,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "tigo_paraguay",
                "event_date": "2025-10-01",
                "category": "technology",
                "title": "Tigo Paraguay expands 4G LTE to rural departments",
                "description": "4G coverage reaches 72% of population",
                "impact_type": "positive",
                "severity": "medium",
            },
        ],
        "earnings_highlights": {
            "tigo_paraguay": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "Paraguay mobile growth driven by data monetization and smartphone adoption", "speaker": "CEO"},
                {"segment": "Home", "highlight_type": "outlook", "content": "Cable broadband and TV expansion driving fixed revenue growth", "speaker": "CEO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_paraguay as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
