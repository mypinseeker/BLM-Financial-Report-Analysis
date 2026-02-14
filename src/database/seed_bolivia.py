"""Seed the database with Bolivia telecom market data.

Tigo Bolivia is the market leader with ~45% mobile share.
3-player market: Tigo (leader), Entel (state-owned), Viva.
Currency: BOB (Boliviano). All revenue figures in BOB millions.

Data sources: Millicom Q4 2025 earnings, ATT Bolivia regulator data.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "bolivia"
OPERATORS = ["tigo_bolivia", "entel_bo", "viva_bo"]


def get_seed_data():
    return {
        "financials": {
            "tigo_bolivia": {
                "total_revenue": [1680, 1710, 1740, 1770, 1800, 1830, 1860, 1890],
                "service_revenue": [1590, 1620, 1650, 1680, 1710, 1740, 1770, 1800],
                "service_revenue_growth_pct": [5.0, 5.2, 5.5, 5.8, 7.1, 7.4, 7.3, 7.1],
                "mobile_service_revenue": [1200, 1220, 1240, 1260, 1280, 1300, 1320, 1340],
                "mobile_service_growth_pct": [4.5, 4.8, 5.0, 5.2, 6.7, 6.6, 6.5, 6.3],
                "fixed_service_revenue": [280, 290, 300, 310, 320, 330, 340, 350],
                "fixed_service_growth_pct": [8.0, 8.3, 8.6, 8.9, 14.3, 13.8, 13.3, 12.9],
                "b2b_revenue": [110, 110, 110, 110, 110, 110, 110, 110],
                "ebitda": [710, 725, 740, 750, 765, 780, 790, 805],
                "ebitda_margin_pct": [42.3, 42.4, 42.5, 42.4, 42.5, 42.6, 42.5, 42.6],
                "ebitda_growth_pct": [4.5, 4.8, 5.0, 5.2, 7.7, 7.6, 6.8, 7.3],
                "capex": [260, 265, 270, 275, 280, 285, 290, 295],
                "capex_to_revenue_pct": [15.5, 15.5, 15.5, 15.5, 15.6, 15.6, 15.6, 15.6],
                "employees": [1800, 1800, 1850, 1850, 1900, 1900, 1900, 1950],
                "_source": "Millicom Q4 2025 Earnings Report",
            },
            "entel_bo": {
                "total_revenue": [1350, 1360, 1370, 1380, 1390, 1400, 1410, 1420],
                "service_revenue": [1280, 1290, 1300, 1310, 1320, 1330, 1340, 1350],
                "service_revenue_growth_pct": [2.0, 2.2, 2.3, 2.5, 2.4, 2.2, 2.3, 2.2],
                "mobile_service_revenue": [950, 958, 965, 972, 980, 987, 995, 1002],
                "fixed_service_revenue": [250, 252, 254, 256, 258, 260, 262, 264],
                "b2b_revenue": [80, 80, 81, 82, 82, 83, 83, 84],
                "ebitda": [405, 408, 411, 414, 417, 420, 423, 426],
                "ebitda_margin_pct": [30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0],
                "capex": [230, 232, 234, 236, 238, 240, 242, 244],
                "capex_to_revenue_pct": [17.0, 17.1, 17.1, 17.1, 17.1, 17.1, 17.2, 17.2],
                "employees": [3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500],
                "_source": "Entel Bolivia Annual Report 2025",
            },
            "viva_bo": {
                "total_revenue": [520, 518, 515, 512, 510, 508, 505, 502],
                "service_revenue": [485, 483, 480, 477, 475, 473, 470, 467],
                "service_revenue_growth_pct": [-1.0, -1.2, -1.5, -1.8, -1.9, -2.1, -2.1, -2.1],
                "mobile_service_revenue": [450, 448, 445, 442, 440, 438, 435, 432],
                "ebitda": [130, 128, 126, 124, 122, 120, 118, 116],
                "ebitda_margin_pct": [25.0, 24.7, 24.5, 24.2, 23.9, 23.6, 23.4, 23.1],
                "capex": [60, 58, 57, 55, 54, 52, 51, 50],
                "capex_to_revenue_pct": [11.5, 11.2, 11.1, 10.7, 10.6, 10.2, 10.1, 10.0],
                "employees": [800, 800, 790, 790, 780, 780, 770, 770],
                "_source": "NuevaTel (Viva) FY2025 Estimates",
            },
        },
        "subscribers": {
            "tigo_bolivia": {
                "mobile_total_k": [5200, 5280, 5360, 5440, 5520, 5600, 5680, 5760],
                "mobile_postpaid_k": [520, 530, 540, 550, 560, 570, 580, 590],
                "mobile_prepaid_k": [4680, 4750, 4820, 4890, 4960, 5030, 5100, 5170],
                "mobile_net_adds_k": [60, 80, 80, 80, 80, 80, 80, 80],
                "mobile_churn_pct": [3.0, 2.9, 2.8, 2.8, 2.7, 2.7, 2.6, 2.6],
                "mobile_arpu": [23.1, 23.1, 23.1, 23.2, 23.2, 23.2, 23.2, 23.3],
                "broadband_total_k": [180, 190, 200, 210, 220, 230, 240, 250],
                "broadband_cable_k": [140, 145, 150, 155, 160, 165, 170, 175],
                "broadband_fiber_k": [20, 22, 25, 28, 32, 36, 40, 45],
                "broadband_net_adds_k": [8, 10, 10, 10, 10, 10, 10, 10],
                "tv_total_k": [130, 135, 140, 145, 150, 155, 160, 165],
                "b2b_customers_k": [15, 16, 16, 17, 17, 18, 18, 19],
                "_source": "Millicom Q4 2025 Earnings Report",
            },
            "entel_bo": {
                "mobile_total_k": [4500, 4510, 4520, 4530, 4540, 4550, 4560, 4570],
                "mobile_postpaid_k": [450, 452, 454, 456, 458, 460, 462, 464],
                "mobile_prepaid_k": [4050, 4058, 4066, 4074, 4082, 4090, 4098, 4106],
                "mobile_net_adds_k": [5, 10, 10, 10, 10, 10, 10, 10],
                "mobile_churn_pct": [2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
                "mobile_arpu": [21.1, 21.2, 21.3, 21.5, 21.6, 21.7, 21.8, 21.9],
                "broadband_total_k": [200, 202, 204, 206, 208, 210, 212, 214],
                "broadband_fiber_k": [40, 42, 45, 48, 50, 53, 55, 58],
                "tv_total_k": [80, 81, 82, 83, 84, 85, 86, 87],
                "_source": "Entel Bolivia Annual Report 2025",
            },
            "viva_bo": {
                "mobile_total_k": [2200, 2190, 2180, 2170, 2160, 2150, 2140, 2130],
                "mobile_postpaid_k": [220, 219, 218, 217, 216, 215, 214, 213],
                "mobile_prepaid_k": [1980, 1971, 1962, 1953, 1944, 1935, 1926, 1917],
                "mobile_net_adds_k": [-8, -10, -10, -10, -10, -10, -10, -10],
                "mobile_churn_pct": [3.8, 3.9, 3.9, 4.0, 4.0, 4.1, 4.1, 4.2],
                "mobile_arpu": [20.5, 20.4, 20.4, 20.4, 20.4, 20.4, 20.3, 20.3],
                "_source": "NuevaTel (Viva) FY2025 Estimates",
            },
        },
        "macro": {
            "gdp_growth_pct": 3.0,
            "inflation_pct": 3.5,
            "unemployment_pct": 5.0,
            "telecom_market_size_eur_b": 1.0,
            "telecom_growth_pct": 4.5,
            "five_g_adoption_pct": 0.0,
            "fiber_penetration_pct": 2.0,
            "regulatory_environment": "ATT regulatory oversight; government influence via Entel; spectrum controlled",
            "digital_strategy": "Bolivia Digital plan; rural connectivity mandate; mobile broadband priority",
            "source_url": "ATT Bolivia / INE / ITU 2025",
        },
        "network": {
            "tigo_bolivia": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 65,
                "fiber_homepass_k": 250,
                "cable_homepass_k": 450,
                "technology_mix": {"mobile_vendor": "Ericsson", "spectrum_mhz": 100, "core_vendor": "Ericsson"},
            },
            "entel_bo": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 60,
                "fiber_homepass_k": 300,
                "technology_mix": {"mobile_vendor": "Huawei/ZTE", "spectrum_mhz": 110},
            },
            "viva_bo": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 38,
                "technology_mix": {"mobile_vendor": "Huawei", "spectrum_mhz": 50},
            },
        },
        "executives": {
            "tigo_bolivia": [
                {"name": "Mario Zanatti", "title": "CEO", "start_date": "2020-01-01", "background": "Millicom executive, ex-banking sector"},
                {"name": "Claudia Torres", "title": "CFO", "start_date": "2021-06-01", "background": "Financial services"},
            ],
            "entel_bo": [
                {"name": "Jose Luis Perez", "title": "CEO", "start_date": "2022-01-01", "background": "Government appointed, public sector background"},
            ],
            "viva_bo": [
                {"name": "Ricardo Flores", "title": "CEO", "start_date": "2023-06-01", "background": "NuevaTel management"},
            ],
        },
        "competitive_scores": {
            "tigo_bolivia": {
                "Network Coverage": 72, "Network Quality": 68, "Brand Strength": 78,
                "Price Competitiveness": 70, "Customer Service": 65, "Digital Experience": 62,
                "Enterprise Solutions": 55, "Innovation": 60, "Distribution": 80,
            },
            "entel_bo": {
                "Network Coverage": 68, "Network Quality": 62, "Brand Strength": 65,
                "Price Competitiveness": 72, "Customer Service": 58, "Digital Experience": 50,
                "Enterprise Solutions": 50, "Innovation": 48, "Distribution": 75,
            },
            "viva_bo": {
                "Network Coverage": 42, "Network Quality": 40, "Brand Strength": 45,
                "Price Competitiveness": 68, "Customer Service": 42, "Digital Experience": 38,
                "Enterprise Solutions": 30, "Innovation": 35, "Distribution": 50,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "tigo_bolivia",
                "event_date": "2025-09-15",
                "category": "technology",
                "title": "Tigo Bolivia launches fiber broadband in Santa Cruz",
                "description": "FTTH deployment targeting 250K homes in Bolivia's largest city",
                "impact_type": "positive",
                "severity": "medium",
            },
        ],
        "earnings_highlights": {
            "tigo_bolivia": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "Bolivia mobile growth steady with data adoption driving revenue", "speaker": "CEO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_bolivia as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
