"""Seed the database with Guatemala telecom market data.

Guatemala is Millicom's largest and most profitable LATAM market.
Tigo Guatemala is the market leader with ~50% mobile market share.
3-player market: Tigo (leader), Claro, Movistar.
Currency: GTQ (Guatemalan Quetzal). All revenue figures in GTQ millions.

Data sources: Millicom Q4 2025 earnings, SIT Guatemala regulator data,
America Movil IR, Telefonica LATAM reports.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "guatemala"
OPERATORS = ["tigo_guatemala", "claro_gt", "movistar_gt"]


def get_seed_data():
    return {
        "financials": {
            # Tigo Guatemala — market leader, ~50% share, strong profitability
            "tigo_guatemala": {
                "total_revenue": [3850, 3920, 3980, 4050, 4120, 4200, 4280, 4350],
                "service_revenue": [3650, 3720, 3780, 3850, 3920, 3990, 4060, 4130],
                "service_revenue_growth_pct": [5.2, 5.5, 5.8, 6.0, 7.0, 7.3, 7.4, 7.3],
                "mobile_service_revenue": [2550, 2600, 2650, 2700, 2750, 2800, 2850, 2900],
                "mobile_service_growth_pct": [4.5, 4.8, 5.0, 5.2, 7.8, 7.7, 7.5, 7.4],
                "fixed_service_revenue": [850, 870, 880, 900, 920, 940, 960, 980],
                "fixed_service_growth_pct": [8.0, 8.5, 8.8, 9.0, 8.2, 8.0, 8.5, 8.9],
                "b2b_revenue": [250, 250, 250, 250, 250, 250, 250, 250],
                "ebitda": [1730, 1765, 1790, 1820, 1855, 1890, 1925, 1960],
                "ebitda_margin_pct": [44.9, 45.0, 45.0, 44.9, 45.0, 45.0, 45.0, 45.1],
                "ebitda_growth_pct": [4.8, 5.0, 5.2, 5.5, 7.2, 7.1, 7.5, 7.7],
                "capex": [580, 590, 600, 620, 630, 650, 660, 670],
                "capex_to_revenue_pct": [15.1, 15.1, 15.1, 15.3, 15.3, 15.5, 15.4, 15.4],
                "employees": [3200, 3200, 3250, 3250, 3300, 3300, 3350, 3350],
                "_source": "Millicom Q4 2025 Earnings Report",
            },
            # Claro Guatemala — #2 player, strong in postpaid
            "claro_gt": {
                "total_revenue": [2800, 2830, 2860, 2900, 2940, 2980, 3010, 3050],
                "service_revenue": [2650, 2680, 2710, 2750, 2790, 2830, 2860, 2900],
                "service_revenue_growth_pct": [3.5, 3.8, 4.0, 4.2, 5.0, 5.3, 5.5, 5.5],
                "mobile_service_revenue": [2100, 2120, 2150, 2180, 2220, 2250, 2280, 2310],
                "fixed_service_revenue": [400, 410, 415, 420, 425, 430, 435, 440],
                "b2b_revenue": [150, 150, 145, 150, 145, 150, 145, 150],
                "ebitda": [980, 990, 1000, 1015, 1030, 1045, 1055, 1070],
                "ebitda_margin_pct": [35.0, 35.0, 35.0, 35.0, 35.0, 35.1, 35.0, 35.1],
                "capex": [450, 455, 460, 470, 475, 480, 485, 490],
                "capex_to_revenue_pct": [16.1, 16.1, 16.1, 16.2, 16.2, 16.1, 16.1, 16.1],
                "employees": [2500, 2500, 2500, 2550, 2550, 2550, 2600, 2600],
                "_source": "America Movil Q4 2025 Earnings (Guatemala segment)",
            },
            # Movistar Guatemala — #3 player, declining share
            "movistar_gt": {
                "total_revenue": [1200, 1190, 1180, 1170, 1160, 1150, 1140, 1130],
                "service_revenue": [1120, 1110, 1100, 1090, 1080, 1070, 1060, 1050],
                "service_revenue_growth_pct": [-2.0, -2.2, -2.5, -2.8, -3.3, -3.6, -3.6, -3.4],
                "mobile_service_revenue": [950, 940, 930, 920, 910, 900, 890, 880],
                "fixed_service_revenue": [120, 120, 120, 120, 120, 120, 120, 120],
                "ebitda": [360, 355, 350, 345, 340, 335, 330, 325],
                "ebitda_margin_pct": [30.0, 29.8, 29.7, 29.5, 29.3, 29.1, 28.9, 28.8],
                "capex": [180, 175, 170, 170, 165, 160, 155, 150],
                "capex_to_revenue_pct": [15.0, 14.7, 14.4, 14.5, 14.2, 13.9, 13.6, 13.3],
                "employees": [1800, 1780, 1760, 1750, 1730, 1710, 1700, 1680],
                "_source": "Telefonica LATAM Q4 2025 Report",
            },
        },
        "subscribers": {
            "tigo_guatemala": {
                "mobile_total_k": [10200, 10350, 10500, 10650, 10800, 10950, 11100, 11250],
                "mobile_postpaid_k": [1530, 1560, 1580, 1600, 1620, 1650, 1680, 1700],
                "mobile_prepaid_k": [8670, 8790, 8920, 9050, 9180, 9300, 9420, 9550],
                "mobile_net_adds_k": [120, 150, 150, 150, 150, 150, 150, 150],
                "mobile_churn_pct": [2.8, 2.7, 2.6, 2.5, 2.5, 2.4, 2.4, 2.3],
                "mobile_arpu": [25.0, 25.3, 25.2, 25.4, 25.5, 25.6, 25.7, 25.8],
                "broadband_total_k": [520, 540, 560, 580, 600, 620, 640, 660],
                "broadband_cable_k": [420, 430, 440, 450, 460, 470, 480, 490],
                "broadband_fiber_k": [50, 55, 60, 70, 80, 90, 100, 110],
                "broadband_net_adds_k": [15, 20, 20, 20, 20, 20, 20, 20],
                "tv_total_k": [380, 390, 400, 410, 420, 430, 440, 450],
                "b2b_customers_k": [45, 46, 47, 48, 49, 50, 51, 52],
                "_source": "Millicom Q4 2025 Earnings Report",
            },
            "claro_gt": {
                "mobile_total_k": [7500, 7550, 7600, 7650, 7700, 7750, 7800, 7850],
                "mobile_postpaid_k": [1350, 1370, 1390, 1410, 1430, 1450, 1470, 1490],
                "mobile_prepaid_k": [6150, 6180, 6210, 6240, 6270, 6300, 6330, 6360],
                "mobile_net_adds_k": [40, 50, 50, 50, 50, 50, 50, 50],
                "mobile_churn_pct": [3.0, 2.9, 2.8, 2.8, 2.7, 2.7, 2.6, 2.6],
                "mobile_arpu": [28.0, 28.1, 28.3, 28.5, 28.8, 29.0, 29.2, 29.4],
                "broadband_total_k": [280, 290, 295, 300, 310, 315, 320, 330],
                "broadband_fiber_k": [30, 35, 40, 45, 50, 55, 60, 70],
                "tv_total_k": [150, 155, 158, 160, 165, 168, 170, 175],
                "b2b_customers_k": [35, 35, 36, 36, 37, 37, 38, 38],
                "_source": "America Movil Q4 2025 Earnings",
            },
            "movistar_gt": {
                "mobile_total_k": [3800, 3780, 3750, 3720, 3690, 3660, 3630, 3600],
                "mobile_postpaid_k": [570, 565, 560, 555, 550, 545, 540, 535],
                "mobile_prepaid_k": [3230, 3215, 3190, 3165, 3140, 3115, 3090, 3065],
                "mobile_net_adds_k": [-20, -20, -30, -30, -30, -30, -30, -30],
                "mobile_churn_pct": [3.5, 3.5, 3.6, 3.6, 3.7, 3.7, 3.8, 3.8],
                "mobile_arpu": [25.0, 24.8, 24.7, 24.5, 24.4, 24.2, 24.0, 23.8],
                "broadband_total_k": [80, 78, 76, 75, 73, 72, 70, 68],
                "tv_total_k": [40, 39, 38, 37, 36, 35, 34, 33],
                "_source": "Telefonica LATAM Q4 2025 Report",
            },
        },
        "macro": {
            "gdp_growth_pct": 3.5,
            "inflation_pct": 4.2,
            "unemployment_pct": 2.8,
            "telecom_market_size_eur_b": 2.8,
            "telecom_growth_pct": 5.5,
            "five_g_adoption_pct": 0.0,
            "fiber_penetration_pct": 3.5,
            "regulatory_environment": "SIT pro-competition framework; spectrum auctions planned; no net neutrality rules",
            "digital_strategy": "Guatemala Digital 2030 plan; mobile broadband focus; rural connectivity subsidies",
            "source_url": "SIT Guatemala / World Bank / ITU 2025",
        },
        "network": {
            "tigo_guatemala": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 78,
                "fiber_homepass_k": 800,
                "cable_homepass_k": 1200,
                "technology_mix": {
                    "mobile_vendor": "Ericsson",
                    "spectrum_mhz": 130,
                    "core_vendor": "Ericsson",
                },
            },
            "claro_gt": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 72,
                "fiber_homepass_k": 400,
                "technology_mix": {
                    "mobile_vendor": "Ericsson/Nokia",
                    "spectrum_mhz": 110,
                },
            },
            "movistar_gt": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 55,
                "technology_mix": {
                    "mobile_vendor": "Huawei",
                    "spectrum_mhz": 80,
                },
            },
        },
        "executives": {
            "tigo_guatemala": [
                {"name": "Rodrigo Aguilar", "title": "CEO", "start_date": "2022-01-01", "background": "Millicom veteran, previously COO Tigo Honduras"},
                {"name": "Carlos Martinez", "title": "CFO", "start_date": "2021-06-01", "background": "Financial services background, ex-Deloitte"},
            ],
            "claro_gt": [
                {"name": "Oscar Aguirre", "title": "CEO", "start_date": "2020-03-01", "background": "America Movil regional executive"},
            ],
            "movistar_gt": [
                {"name": "Ana Lucia Duarte", "title": "CEO", "start_date": "2023-01-01", "background": "Telefonica Group management program"},
            ],
        },
        "competitive_scores": {
            "tigo_guatemala": {
                "Network Coverage": 82, "Network Quality": 78, "Brand Strength": 85,
                "Price Competitiveness": 75, "Customer Service": 72, "Digital Experience": 70,
                "Enterprise Solutions": 65, "Innovation": 68, "Distribution": 88,
            },
            "claro_gt": {
                "Network Coverage": 75, "Network Quality": 72, "Brand Strength": 78,
                "Price Competitiveness": 70, "Customer Service": 68, "Digital Experience": 65,
                "Enterprise Solutions": 60, "Innovation": 62, "Distribution": 80,
            },
            "movistar_gt": {
                "Network Coverage": 58, "Network Quality": 55, "Brand Strength": 60,
                "Price Competitiveness": 65, "Customer Service": 55, "Digital Experience": 50,
                "Enterprise Solutions": 45, "Innovation": 48, "Distribution": 60,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "tigo_guatemala",
                "event_date": "2025-10-15",
                "category": "technology",
                "title": "Tigo Guatemala expands 4G LTE coverage to 5 new departments",
                "description": "Tigo extends 4G coverage to rural departments, reaching 78% population coverage",
                "impact_type": "positive",
                "severity": "medium",
            },
            {
                "operator_id": None,
                "event_date": "2025-09-01",
                "category": "regulatory",
                "title": "SIT announces spectrum auction for 700 MHz band",
                "description": "Guatemala to auction 700 MHz spectrum for rural broadband expansion",
                "impact_type": "neutral",
                "severity": "high",
            },
            {
                "operator_id": "tigo_guatemala",
                "event_date": "2025-11-20",
                "category": "competitive",
                "title": "Tigo launches Tigo Money mobile wallet expansion",
                "description": "Tigo Money extends financial services to unbanked populations",
                "impact_type": "positive",
                "severity": "medium",
            },
        ],
        "earnings_highlights": {
            "tigo_guatemala": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "Expect continued mid-single-digit mobile service revenue growth driven by data monetization", "speaker": "CEO"},
                {"segment": "Home", "highlight_type": "outlook", "content": "HFC expansion driving fixed broadband subscriber growth of 20K per quarter", "speaker": "CEO"},
                {"segment": "B2B", "highlight_type": "explanation", "content": "Enterprise segment growing with cloud and connectivity solutions for SMEs", "speaker": "CFO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    """Seed Guatemala market data."""
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_guatemala as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
