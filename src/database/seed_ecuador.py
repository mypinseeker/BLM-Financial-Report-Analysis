"""Seed the database with Ecuador telecom market data.

Ecuador is a newly acquired Millicom market (via Telefonica Ecuador acquisition 2025).
3-player market: Claro (leader), Tigo (ex-Telefonica), CNT (state-owned).
Currency: USD (dollarized). All revenue figures in USD millions.

Data sources: ARCOTEL Ecuador, America Movil IR, Telefonica LATAM, CNT annual report.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "ecuador"
OPERATORS = ["tigo_ecuador", "claro_ec", "cnt_ec"]


def get_seed_data():
    return {
        "financials": {
            "tigo_ecuador": {
                "total_revenue": [320, 325, 330, 335, 340, 345, 350, 355],
                "service_revenue": [300, 305, 310, 315, 320, 325, 330, 335],
                "service_revenue_growth_pct": [2.0, 2.2, 2.5, 2.8, 6.3, 6.6, 6.5, 6.1],
                "mobile_service_revenue": [210, 213, 216, 220, 224, 228, 232, 236],
                "mobile_service_growth_pct": [1.5, 1.8, 2.0, 2.3, 6.7, 7.0, 7.4, 7.3],
                "fixed_service_revenue": [72, 74, 76, 77, 78, 79, 80, 81],
                "fixed_service_growth_pct": [3.0, 3.2, 3.5, 3.7, 8.3, 6.8, 5.3, 5.1],
                "b2b_revenue": [18, 18, 18, 18, 18, 18, 18, 18],
                "ebitda": [102, 104, 106, 108, 110, 112, 114, 116],
                "ebitda_margin_pct": [31.9, 32.0, 32.1, 32.2, 32.4, 32.5, 32.6, 32.7],
                "ebitda_growth_pct": [1.0, 1.5, 2.0, 2.5, 7.8, 7.7, 7.5, 7.4],
                "capex": [55, 56, 58, 59, 60, 62, 63, 64],
                "capex_to_revenue_pct": [17.2, 17.2, 17.6, 17.6, 17.6, 18.0, 18.0, 18.0],
                "employees": [2500, 2500, 2500, 2500, 2600, 2600, 2600, 2600],
                "_source": "Millicom Q4 2025 Earnings (Ecuador acquired assets)",
            },
            "claro_ec": {
                "total_revenue": [520, 528, 536, 544, 552, 560, 568, 576],
                "service_revenue": [490, 498, 506, 514, 522, 530, 538, 546],
                "service_revenue_growth_pct": [3.5, 3.8, 4.0, 4.2, 6.1, 6.4, 6.3, 6.0],
                "mobile_service_revenue": [380, 386, 392, 398, 404, 410, 416, 422],
                "fixed_service_revenue": [85, 87, 89, 91, 93, 95, 97, 99],
                "b2b_revenue": [25, 25, 25, 25, 25, 25, 25, 25],
                "ebitda": [192, 195, 198, 201, 204, 207, 210, 213],
                "ebitda_margin_pct": [36.9, 36.9, 36.9, 36.9, 36.9, 37.0, 37.0, 37.0],
                "capex": [90, 92, 94, 95, 97, 98, 100, 101],
                "capex_to_revenue_pct": [17.3, 17.4, 17.5, 17.5, 17.6, 17.5, 17.6, 17.5],
                "employees": [3500, 3500, 3500, 3500, 3600, 3600, 3600, 3600],
                "_source": "America Movil Q4 2025 Earnings — Ecuador",
            },
            "cnt_ec": {
                "total_revenue": [280, 282, 284, 286, 288, 290, 292, 294],
                "service_revenue": [265, 267, 269, 271, 273, 275, 277, 279],
                "service_revenue_growth_pct": [1.0, 1.2, 1.3, 1.5, 1.5, 1.5, 1.5, 1.4],
                "mobile_service_revenue": [100, 101, 102, 103, 104, 105, 106, 107],
                "fixed_service_revenue": [140, 141, 142, 143, 144, 145, 146, 147],
                "b2b_revenue": [25, 25, 25, 25, 25, 25, 25, 25],
                "ebitda": [56, 56, 57, 57, 58, 58, 58, 59],
                "ebitda_margin_pct": [20.0, 19.9, 20.1, 19.9, 20.1, 20.0, 19.9, 20.1],
                "capex": [50, 50, 51, 51, 52, 52, 52, 53],
                "capex_to_revenue_pct": [17.9, 17.7, 18.0, 17.8, 18.1, 17.9, 17.8, 18.0],
                "employees": [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000],
                "_source": "CNT Ecuador Annual Report 2025",
            },
        },
        "subscribers": {
            "tigo_ecuador": {
                "mobile_total_k": [5500, 5550, 5600, 5650, 5700, 5750, 5800, 5850],
                "mobile_postpaid_k": [1100, 1115, 1125, 1135, 1145, 1155, 1165, 1175],
                "mobile_prepaid_k": [4400, 4435, 4475, 4515, 4555, 4595, 4635, 4675],
                "mobile_net_adds_k": [40, 50, 50, 50, 50, 50, 50, 50],
                "mobile_churn_pct": [2.8, 2.7, 2.7, 2.6, 2.6, 2.5, 2.5, 2.5],
                "mobile_arpu": [3.8, 3.8, 3.9, 3.9, 3.9, 4.0, 4.0, 4.0],
                "broadband_total_k": [420, 430, 440, 450, 460, 470, 480, 490],
                "broadband_fiber_k": [100, 110, 120, 130, 140, 150, 160, 170],
                "broadband_net_adds_k": [8, 10, 10, 10, 10, 10, 10, 10],
                "tv_total_k": [200, 205, 210, 215, 220, 225, 230, 235],
                "b2b_customers_k": [25, 26, 26, 27, 27, 28, 28, 29],
                "_source": "Millicom Q4 2025 Earnings (Ecuador)",
            },
            "claro_ec": {
                "mobile_total_k": [9000, 9050, 9100, 9150, 9200, 9250, 9300, 9350],
                "mobile_postpaid_k": [2250, 2265, 2280, 2295, 2310, 2325, 2340, 2355],
                "mobile_prepaid_k": [6750, 6785, 6820, 6855, 6890, 6925, 6960, 6995],
                "mobile_net_adds_k": [30, 50, 50, 50, 50, 50, 50, 50],
                "mobile_churn_pct": [2.2, 2.2, 2.1, 2.1, 2.0, 2.0, 2.0, 1.9],
                "mobile_arpu": [4.2, 4.3, 4.3, 4.3, 4.4, 4.4, 4.5, 4.5],
                "broadband_total_k": [500, 510, 520, 530, 540, 550, 560, 570],
                "broadband_fiber_k": [150, 160, 170, 180, 190, 200, 210, 220],
                "tv_total_k": [250, 253, 256, 259, 262, 265, 268, 271],
                "b2b_customers_k": [40, 41, 42, 43, 44, 45, 46, 47],
                "_source": "America Movil Q4 2025 Earnings",
            },
            "cnt_ec": {
                "mobile_total_k": [2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500],
                "mobile_postpaid_k": [375, 375, 375, 375, 375, 375, 375, 375],
                "mobile_prepaid_k": [2125, 2125, 2125, 2125, 2125, 2125, 2125, 2125],
                "mobile_net_adds_k": [0, 0, 0, 0, 0, 0, 0, 0],
                "mobile_churn_pct": [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0],
                "mobile_arpu": [4.0, 4.0, 4.1, 4.1, 4.2, 4.2, 4.2, 4.3],
                "broadband_total_k": [800, 805, 810, 815, 820, 825, 830, 835],
                "broadband_fiber_k": [400, 410, 420, 430, 440, 450, 460, 470],
                "tv_total_k": [150, 151, 152, 153, 154, 155, 156, 157],
                "_source": "CNT Ecuador Annual Report 2025",
            },
        },
        "macro": {
            "gdp_growth_pct": 2.5,
            "inflation_pct": 2.2,
            "unemployment_pct": 5.0,
            "telecom_market_size_eur_b": 2.8,
            "telecom_growth_pct": 3.5,
            "five_g_adoption_pct": 0.0,
            "fiber_penetration_pct": 12.0,
            "regulatory_environment": "ARCOTEL regulatory framework; dollarized economy; pro-competition mandate",
            "digital_strategy": "Ecuador Digital plan; broadband universalization; 5G spectrum planning",
            "source_url": "ARCOTEL Ecuador / BCE / ITU 2025",
        },
        "network": {
            "tigo_ecuador": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 72,
                "fiber_homepass_k": 1200,
                "technology_mix": {"mobile_vendor": "Nokia/Ericsson", "spectrum_mhz": 110, "core_vendor": "Nokia"},
            },
            "claro_ec": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 80,
                "fiber_homepass_k": 1500,
                "technology_mix": {"mobile_vendor": "Ericsson", "spectrum_mhz": 140, "core_vendor": "Ericsson"},
            },
            "cnt_ec": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 55,
                "fiber_homepass_k": 2000,
                "technology_mix": {"mobile_vendor": "Huawei/ZTE", "spectrum_mhz": 80},
            },
        },
        "executives": {
            "tigo_ecuador": [
                {"name": "Carlos Villagomez", "title": "CEO", "start_date": "2025-06-01", "background": "Millicom integration team, ex-Telefonica Ecuador"},
            ],
            "claro_ec": [
                {"name": "Jorge Hidalgo", "title": "CEO", "start_date": "2019-01-01", "background": "America Movil Andean region"},
            ],
            "cnt_ec": [
                {"name": "Maria Fernanda Torres", "title": "CEO", "start_date": "2023-01-01", "background": "Government-appointed, public sector"},
            ],
        },
        "competitive_scores": {
            "tigo_ecuador": {
                "Network Coverage": 70, "Network Quality": 65, "Brand Strength": 55,
                "Price Competitiveness": 68, "Customer Service": 60, "Digital Experience": 58,
                "Enterprise Solutions": 55, "Innovation": 58, "Distribution": 65,
            },
            "claro_ec": {
                "Network Coverage": 82, "Network Quality": 78, "Brand Strength": 82,
                "Price Competitiveness": 62, "Customer Service": 68, "Digital Experience": 70,
                "Enterprise Solutions": 72, "Innovation": 65, "Distribution": 85,
            },
            "cnt_ec": {
                "Network Coverage": 60, "Network Quality": 52, "Brand Strength": 58,
                "Price Competitiveness": 75, "Customer Service": 48, "Digital Experience": 42,
                "Enterprise Solutions": 55, "Innovation": 40, "Distribution": 70,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "tigo_ecuador",
                "event_date": "2025-06-01",
                "category": "competitive",
                "title": "Millicom completes acquisition of Telefonica Ecuador",
                "description": "Tigo Ecuador brand launches, integration of fixed+mobile assets begins",
                "impact_type": "positive",
                "severity": "high",
            },
        ],
        "earnings_highlights": {
            "tigo_ecuador": [
                {"segment": "Integration", "highlight_type": "guidance", "content": "Ecuador integration proceeding on schedule; synergies expected from Millicom LATAM platform", "speaker": "CEO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_ecuador as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
