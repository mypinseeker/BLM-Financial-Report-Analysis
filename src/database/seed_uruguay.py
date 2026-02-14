"""Seed the database with Uruguay telecom market data.

Uruguay is a newly entered Millicom market (acquisition 2025).
3-player mobile market: Antel (state-owned dominant), Claro (#2), Tigo (new entrant).
Antel has monopoly on fixed broadband with 100% FTTH coverage.
Currency: UYU (Uruguayan Peso). All revenue figures in UYU millions.

Data sources: URSEC Uruguay, Antel annual report, America Movil IR.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "uruguay"
OPERATORS = ["tigo_uruguay", "antel_uy", "claro_uy"]


def get_seed_data():
    return {
        "financials": {
            "tigo_uruguay": {
                "total_revenue": [1800, 1830, 1860, 1890, 1920, 1950, 1980, 2010],
                "service_revenue": [1700, 1730, 1760, 1790, 1820, 1850, 1880, 1910],
                "service_revenue_growth_pct": [3.0, 3.2, 3.5, 3.8, 6.7, 6.9, 6.8, 6.4],
                "mobile_service_revenue": [1600, 1625, 1650, 1675, 1700, 1725, 1750, 1775],
                "mobile_service_growth_pct": [2.8, 3.0, 3.2, 3.5, 6.3, 6.2, 6.1, 6.0],
                "fixed_service_revenue": [50, 55, 60, 65, 70, 75, 80, 85],
                "fixed_service_growth_pct": [10.0, 10.0, 9.1, 8.3, 40.0, 36.4, 33.3, 30.8],
                "b2b_revenue": [50, 50, 50, 50, 50, 50, 50, 50],
                "ebitda": [540, 549, 558, 567, 576, 585, 594, 603],
                "ebitda_margin_pct": [30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0],
                "ebitda_growth_pct": [2.5, 2.8, 3.0, 3.2, 6.7, 6.5, 6.4, 6.1],
                "capex": [340, 345, 350, 358, 365, 370, 378, 385],
                "capex_to_revenue_pct": [18.9, 18.9, 18.8, 18.9, 19.0, 19.0, 19.1, 19.2],
                "employees": [800, 800, 820, 820, 850, 850, 880, 880],
                "_source": "Millicom Q4 2025 Earnings (Uruguay new market)",
            },
            "antel_uy": {
                "total_revenue": [8500, 8580, 8660, 8740, 8820, 8900, 8980, 9060],
                "service_revenue": [8100, 8180, 8260, 8340, 8420, 8500, 8580, 8660],
                "service_revenue_growth_pct": [3.0, 3.2, 3.3, 3.5, 3.7, 3.9, 3.9, 3.8],
                "mobile_service_revenue": [3800, 3840, 3880, 3920, 3960, 4000, 4040, 4080],
                "fixed_service_revenue": [3500, 3530, 3560, 3590, 3620, 3650, 3680, 3710],
                "b2b_revenue": [800, 810, 820, 830, 840, 850, 860, 870],
                "ebitda": [3400, 3432, 3464, 3496, 3528, 3560, 3592, 3624],
                "ebitda_margin_pct": [40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0],
                "capex": [1450, 1465, 1480, 1495, 1510, 1525, 1540, 1555],
                "capex_to_revenue_pct": [17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.1, 17.2],
                "employees": [6500, 6500, 6500, 6500, 6500, 6500, 6500, 6500],
                "_source": "Antel Uruguay Annual Report 2025",
            },
            "claro_uy": {
                "total_revenue": [2800, 2828, 2856, 2884, 2912, 2940, 2968, 2996],
                "service_revenue": [2650, 2678, 2706, 2734, 2762, 2790, 2818, 2846],
                "service_revenue_growth_pct": [2.5, 2.8, 3.0, 3.2, 4.0, 4.2, 4.1, 4.0],
                "mobile_service_revenue": [2500, 2525, 2550, 2575, 2600, 2625, 2650, 2675],
                "b2b_revenue": [100, 103, 106, 109, 112, 115, 118, 121],
                "ebitda": [840, 849, 857, 865, 874, 882, 890, 899],
                "ebitda_margin_pct": [30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0],
                "capex": [430, 434, 439, 443, 447, 452, 456, 460],
                "capex_to_revenue_pct": [15.4, 15.4, 15.4, 15.4, 15.4, 15.4, 15.4, 15.4],
                "employees": [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500],
                "_source": "America Movil Q4 2025 Earnings — Uruguay",
            },
        },
        "subscribers": {
            "tigo_uruguay": {
                "mobile_total_k": [700, 720, 740, 760, 780, 800, 820, 840],
                "mobile_postpaid_k": [280, 290, 300, 310, 320, 330, 340, 350],
                "mobile_prepaid_k": [420, 430, 440, 450, 460, 470, 480, 490],
                "mobile_net_adds_k": [15, 20, 20, 20, 20, 20, 20, 20],
                "mobile_churn_pct": [2.5, 2.4, 2.4, 2.3, 2.3, 2.2, 2.2, 2.1],
                "mobile_arpu": [228.6, 226.4, 223.6, 220.4, 217.9, 215.6, 213.4, 211.3],
                "b2b_customers_k": [5, 5, 6, 6, 6, 7, 7, 7],
                "_source": "Millicom Q4 2025 Earnings (Uruguay)",
            },
            "antel_uy": {
                "mobile_total_k": [2800, 2810, 2820, 2830, 2840, 2850, 2860, 2870],
                "mobile_postpaid_k": [1680, 1690, 1695, 1700, 1705, 1710, 1715, 1720],
                "mobile_prepaid_k": [1120, 1120, 1125, 1130, 1135, 1140, 1145, 1150],
                "mobile_net_adds_k": [5, 10, 10, 10, 10, 10, 10, 10],
                "mobile_churn_pct": [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5],
                "mobile_arpu": [135.7, 136.7, 137.6, 138.5, 139.4, 140.4, 141.3, 142.2],
                "broadband_total_k": [900, 905, 910, 915, 920, 925, 930, 935],
                "broadband_fiber_k": [880, 885, 890, 895, 900, 905, 910, 915],
                "broadband_net_adds_k": [3, 5, 5, 5, 5, 5, 5, 5],
                "tv_total_k": [350, 352, 354, 356, 358, 360, 362, 364],
                "fmc_total_k": [500, 505, 510, 515, 520, 525, 530, 535],
                "fmc_penetration_pct": [55.6, 55.8, 56.0, 56.3, 56.5, 56.8, 57.0, 57.2],
                "b2b_customers_k": [35, 35, 36, 36, 37, 37, 38, 38],
                "_source": "Antel Uruguay Annual Report 2025",
            },
            "claro_uy": {
                "mobile_total_k": [1600, 1610, 1620, 1630, 1640, 1650, 1660, 1670],
                "mobile_postpaid_k": [640, 644, 648, 652, 656, 660, 664, 668],
                "mobile_prepaid_k": [960, 966, 972, 978, 984, 990, 996, 1002],
                "mobile_net_adds_k": [5, 10, 10, 10, 10, 10, 10, 10],
                "mobile_churn_pct": [2.0, 2.0, 1.9, 1.9, 1.9, 1.8, 1.8, 1.8],
                "mobile_arpu": [156.3, 156.8, 157.4, 157.9, 158.5, 159.1, 159.6, 160.2],
                "b2b_customers_k": [15, 15, 16, 16, 16, 17, 17, 17],
                "_source": "America Movil Q4 2025 Earnings — Uruguay",
            },
        },
        "macro": {
            "gdp_growth_pct": 3.0,
            "inflation_pct": 7.0,
            "unemployment_pct": 8.0,
            "telecom_market_size_eur_b": 1.4,
            "telecom_growth_pct": 3.5,
            "five_g_adoption_pct": 5.0,
            "fiber_penetration_pct": 65.0,
            "regulatory_environment": "URSEC framework; Antel state monopoly on fixed; competitive mobile market",
            "digital_strategy": "Plan Ceibal digital education; 100% fiber nationwide; 5G deployment underway via Antel",
            "source_url": "URSEC Uruguay / BCU / ITU 2025",
        },
        "network": {
            "tigo_uruguay": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 70,
                "technology_mix": {"mobile_vendor": "Nokia", "spectrum_mhz": 80, "core_vendor": "Nokia"},
            },
            "antel_uy": {
                "five_g_coverage_pct": 25,
                "four_g_coverage_pct": 95,
                "fiber_homepass_k": 1200,
                "fiber_connected_k": 915,
                "technology_mix": {"mobile_vendor": "Nokia/Huawei", "spectrum_mhz": 200, "core_vendor": "Nokia", "5g_sa_status": "Deploying"},
            },
            "claro_uy": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 82,
                "technology_mix": {"mobile_vendor": "Ericsson", "spectrum_mhz": 100},
            },
        },
        "executives": {
            "tigo_uruguay": [
                {"name": "Martin Gonzalez", "title": "CEO", "start_date": "2025-03-01", "background": "Millicom new market launch team"},
            ],
            "antel_uy": [
                {"name": "Gabriel Gurmen", "title": "CEO", "start_date": "2021-01-01", "background": "Government-appointed, telecom engineering background"},
            ],
            "claro_uy": [
                {"name": "Fernando Perez", "title": "CEO", "start_date": "2020-01-01", "background": "America Movil Southern Cone management"},
            ],
        },
        "competitive_scores": {
            "tigo_uruguay": {
                "Network Coverage": 62, "Network Quality": 58, "Brand Strength": 45,
                "Price Competitiveness": 72, "Customer Service": 55, "Digital Experience": 55,
                "Enterprise Solutions": 35, "Innovation": 50, "Distribution": 55,
            },
            "antel_uy": {
                "Network Coverage": 95, "Network Quality": 92, "Brand Strength": 90,
                "Price Competitiveness": 60, "Customer Service": 72, "Digital Experience": 75,
                "Enterprise Solutions": 82, "Innovation": 78, "Distribution": 90,
            },
            "claro_uy": {
                "Network Coverage": 78, "Network Quality": 72, "Brand Strength": 70,
                "Price Competitiveness": 68, "Customer Service": 65, "Digital Experience": 62,
                "Enterprise Solutions": 52, "Innovation": 55, "Distribution": 72,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "tigo_uruguay",
                "event_date": "2025-03-01",
                "category": "competitive",
                "title": "Millicom enters Uruguay market via acquisition",
                "description": "Tigo Uruguay brand launches, targeting mobile market as third operator",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "antel_uy",
                "event_date": "2025-06-01",
                "category": "technology",
                "title": "Antel deploys 5G in Montevideo and coastal cities",
                "description": "5G SA coverage reaches 25% of population, first in Uruguay",
                "impact_type": "positive",
                "severity": "high",
            },
        ],
        "earnings_highlights": {
            "tigo_uruguay": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "Uruguay entry progressing; mobile subscriber acquisition ahead of plan despite Antel dominance", "speaker": "CEO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_uruguay as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
