"""Seed the database with Cyprus telecom market data.

3-player mobile market: Cyta (#1, state-owned incumbent), Epic (#2, NJJ/Monaco Telecom), PrimeTel (#3).
Currency: EUR. All revenue figures in EUR millions per quarter.

Data sources:
  - Epic (Monaco Telecom) — limited public financials; estimates from market data
  - Cyta — semi-governmental; budget/revenue data from JFDI/Cyprus media
  - PrimeTel — private company; limited public data
  - OCECPR (regulator) market data
  - Mordor Intelligence Cyprus Telecom Market Report
  - Cyprus Statistical Service / IMF
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "cyprus"
OPERATORS = ["epic_cy", "cyta_cy", "primetel_cy"]


def get_seed_data():
    return {
        "financials": {
            # Epic (Cyprus) — Monaco Telecom / NJJ subsidiary
            # Private company; limited public financials
            # Estimated revenue ~EUR 120-130M based on ~35% of ~EUR 350M market
            # Estimated EBITDA ~EUR 45-50M based on comparable operator margins
            "epic_cy": {
                "total_revenue": [28, 29, 29, 30, 30, 31, 32, 33],
                "service_revenue": [26, 27, 27, 28, 28, 29, 30, 31],
                "service_revenue_growth_pct": [3.0, 3.5, 4.0, 4.5, 7.1, 6.9, 10.3, 10.7],
                "mobile_service_revenue": [20, 21, 21, 22, 22, 23, 23, 24],
                "mobile_service_growth_pct": [2.5, 3.0, 3.5, 4.0, 10.0, 9.5, 9.5, 9.1],
                "fixed_service_revenue": [4, 4, 4, 4, 4, 4, 5, 5],
                "fixed_service_growth_pct": [5.0, 6.0, 7.0, 8.0, 0.0, 0.0, 25.0, 25.0],
                "b2b_revenue": [2, 2, 2, 2, 2, 2, 2, 2],
                "ebitda": [10, 11, 11, 12, 12, 12, 13, 13],
                "ebitda_margin_pct": [35.7, 37.9, 37.9, 40.0, 40.0, 38.7, 40.6, 39.4],
                "ebitda_growth_pct": [5.0, 5.5, 6.0, 6.5, 20.0, 9.1, 18.2, 8.3],
                "capex": [6, 6, 7, 7, 7, 7, 8, 8],
                "capex_to_revenue_pct": [21.4, 20.7, 24.1, 23.3, 23.3, 22.6, 25.0, 24.2],
                "employees": [550, 555, 560, 565, 570, 575, 580, 585],
                "_source": "Epic Cyprus (Monaco Telecom subsidiary); limited public data; estimates based on market share and comparable margins",
            },
            # Cyta — semi-governmental, Cyprus's incumbent operator
            # Revenue ~EUR 412M (2024 budget); personnel EUR 148M
            # Estimated EBITDA ~EUR 80-90M
            "cyta_cy": {
                "total_revenue": [96, 98, 100, 102, 100, 102, 104, 106],
                "service_revenue": [90, 92, 94, 96, 94, 96, 98, 100],
                "service_revenue_growth_pct": [1.5, 2.0, 2.5, 3.0, 4.4, 4.3, 4.3, 4.2],
                "mobile_service_revenue": [38, 39, 40, 41, 40, 41, 42, 43],
                "mobile_service_growth_pct": [1.0, 1.5, 2.0, 2.5, 5.3, 5.1, 5.0, 4.9],
                "fixed_service_revenue": [42, 43, 44, 45, 44, 45, 46, 47],
                "fixed_service_growth_pct": [0.5, 1.0, 1.5, 2.0, 4.8, 4.7, 4.5, 4.4],
                "b2b_revenue": [10, 10, 10, 10, 10, 10, 10, 10],
                "ebitda": [18, 19, 20, 21, 20, 21, 22, 22],
                "ebitda_margin_pct": [18.8, 19.4, 20.0, 20.6, 20.0, 20.6, 21.2, 20.8],
                "ebitda_growth_pct": [2.0, 3.0, 4.0, 5.0, 11.1, 10.5, 10.0, 4.8],
                "capex": [22, 23, 24, 25, 25, 26, 27, 27],
                "capex_to_revenue_pct": [22.9, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 25.5],
                "employees": [1300, 1300, 1300, 1300, 1300, 1300, 1300, 1300],
                "_source": "Cyta semi-governmental; 2024 budget EUR 412M revenue / EUR 501M expenditure; EUR 148M personnel; EBITDA low due to state cost structure",
            },
            # PrimeTel — private company, smallest MNO
            # Estimated revenue ~EUR 50-60M based on ~13% market share
            "primetel_cy": {
                "total_revenue": [12, 12, 13, 13, 13, 13, 14, 14],
                "service_revenue": [11, 11, 12, 12, 12, 12, 13, 13],
                "service_revenue_growth_pct": [1.0, 1.5, 2.0, 2.5, 9.1, 9.1, 8.3, 8.3],
                "mobile_service_revenue": [5, 5, 5, 5, 5, 5, 6, 6],
                "mobile_service_growth_pct": [1.0, 1.5, 2.0, 2.5, 0.0, 0.0, 20.0, 20.0],
                "fixed_service_revenue": [5, 5, 6, 6, 6, 6, 6, 6],
                "fixed_service_growth_pct": [1.0, 1.5, 2.0, 2.5, 20.0, 20.0, 0.0, 0.0],
                "b2b_revenue": [1, 1, 1, 1, 1, 1, 1, 1],
                "ebitda": [3, 3, 3, 3, 3, 3, 4, 4],
                "ebitda_margin_pct": [25.0, 25.0, 23.1, 23.1, 23.1, 23.1, 28.6, 28.6],
                "ebitda_growth_pct": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 33.3, 33.3],
                "capex": [3, 3, 3, 3, 3, 3, 3, 3],
                "capex_to_revenue_pct": [25.0, 25.0, 23.1, 23.1, 23.1, 23.1, 21.4, 21.4],
                "employees": [350, 350, 355, 355, 360, 360, 365, 365],
                "_source": "PrimeTel private company; estimates based on ~13% mobile market share",
            },
        },
        "subscribers": {
            "epic_cy": {
                "mobile_total_k": [470, 475, 480, 485, 490, 495, 500, 505],
                "mobile_postpaid_k": [300, 305, 310, 315, 320, 325, 330, 335],
                "mobile_prepaid_k": [170, 170, 170, 170, 170, 170, 170, 170],
                "mobile_net_adds_k": [3, 5, 5, 5, 5, 5, 5, 5],
                "mobile_churn_pct": [1.5, 1.5, 1.4, 1.4, 1.4, 1.3, 1.3, 1.3],
                "mobile_arpu": [15.0, 15.2, 15.4, 15.6, 15.8, 16.0, 16.2, 16.5],
                "broadband_total_k": [40, 42, 44, 46, 48, 50, 52, 55],
                "broadband_fiber_k": [25, 27, 29, 31, 33, 35, 37, 40],
                "broadband_net_adds_k": [1, 2, 2, 2, 2, 2, 2, 3],
                "tv_total_k": [0, 0, 0, 0, 0, 0, 0, 0],
                "b2b_customers_k": [5, 5, 5, 5, 5, 6, 6, 6],
                "_source": "Epic Cyprus; ~35% mobile share of 1.43M total; FTTH growing via EIB financing",
            },
            "cyta_cy": {
                "mobile_total_k": [720, 725, 730, 735, 740, 745, 750, 755],
                "mobile_postpaid_k": [450, 455, 460, 465, 470, 475, 480, 485],
                "mobile_prepaid_k": [270, 270, 270, 270, 270, 270, 270, 270],
                "mobile_net_adds_k": [3, 5, 5, 5, 5, 5, 5, 5],
                "mobile_churn_pct": [1.0, 1.0, 1.0, 1.0, 1.0, 0.9, 0.9, 0.9],
                "mobile_arpu": [17.0, 17.2, 17.4, 17.6, 17.5, 17.7, 17.9, 18.0],
                "broadband_total_k": [180, 182, 184, 186, 188, 190, 192, 195],
                "broadband_fiber_k": [120, 125, 130, 135, 140, 145, 150, 155],
                "broadband_net_adds_k": [1, 2, 2, 2, 2, 2, 2, 3],
                "tv_total_k": [60, 60, 61, 61, 62, 62, 63, 63],
                "b2b_customers_k": [15, 15, 15, 16, 16, 16, 16, 17],
                "_source": "Cyta ~52% mobile share; Cytamobile-Vodafone brand; FTTP 77% coverage; national incumbent",
            },
            "primetel_cy": {
                "mobile_total_k": [175, 176, 177, 178, 179, 180, 181, 182],
                "mobile_postpaid_k": [100, 101, 102, 103, 104, 105, 106, 107],
                "mobile_prepaid_k": [75, 75, 75, 75, 75, 75, 75, 75],
                "mobile_net_adds_k": [0, 1, 1, 1, 1, 1, 1, 1],
                "mobile_churn_pct": [1.8, 1.8, 1.7, 1.7, 1.7, 1.6, 1.6, 1.6],
                "mobile_arpu": [12.0, 12.2, 12.4, 12.5, 12.5, 12.7, 12.9, 13.0],
                "broadband_total_k": [45, 46, 47, 48, 49, 50, 51, 52],
                "broadband_fiber_k": [20, 22, 24, 26, 28, 30, 32, 34],
                "broadband_net_adds_k": [0, 1, 1, 1, 1, 1, 1, 1],
                "tv_total_k": [30, 30, 31, 31, 32, 32, 33, 33],
                "b2b_customers_k": [3, 3, 3, 3, 3, 3, 3, 3],
                "_source": "PrimeTel ~13% mobile share; smallest MNO; broadband + TV competitor",
            },
        },
        "macro": {
            "gdp_growth_pct": 3.0,
            "inflation_pct": 2.5,
            "unemployment_pct": 6.5,
            "telecom_market_size_eur_b": 0.35,
            "telecom_growth_pct": 3.0,
            "five_g_adoption_pct": 15.0,
            "fiber_penetration_pct": 50.0,
            "regulatory_environment": "OCECPR regulation; EU Digital Single Market. Cyta 100% state-owned. 5G spectrum allocated; Epic launched Jul 2021. Cyprus division: Republic controls south.",
            "digital_strategy": "FTTP 77% premises coverage. 5G by Epic and Cyta. Tourism drives seasonal demand (4M+ visitors/yr). Growing financial services and shipping sectors. Population ~1.2M.",
            "source_url": "OCECPR / Cyprus Statistical Service / IMF / Mordor Intelligence",
        },
        "network": {
            "epic_cy": {
                "five_g_coverage_pct": 60,
                "four_g_coverage_pct": 95,
                "fiber_homepass_k": 120,
                "technology_mix": {"mobile_vendor": "Huawei", "spectrum_mhz": 200, "5g_launched": "Jul 2021", "fiber_status": "EIB EUR 19M FTTH financing"},
            },
            "cyta_cy": {
                "five_g_coverage_pct": 55,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 350,
                "technology_mix": {"mobile_vendor": "Nokia/Ericsson", "spectrum_mhz": 250, "fttp_coverage_pct": 77, "fixed_incumbent": True},
            },
            "primetel_cy": {
                "five_g_coverage_pct": 20,
                "four_g_coverage_pct": 85,
                "fiber_homepass_k": 80,
                "technology_mix": {"mobile_vendor": "Mixed", "spectrum_mhz": 100, "smallest_mno": True},
            },
        },
        "executives": {
            "epic_cy": [
                {"name": "Marios Kalochoritis", "title": "CEO", "start_date": "2020-01-01", "background": "Monaco Telecom appointee; leading Epic's 5G and fiber strategy in Cyprus"},
            ],
            "cyta_cy": [
                {"name": "Andreas Neocleous", "title": "CEO", "start_date": "2022-01-01", "background": "Leading Cyta digital transformation and FTTP rollout; managing state-owned efficiency challenges"},
            ],
            "primetel_cy": [
                {"name": "Panicos Papadopoulos", "title": "CEO", "start_date": "2018-01-01", "background": "Long-standing CEO of PrimeTel; managing competitive positioning as smallest MNO"},
            ],
        },
        "competitive_scores": {
            "epic_cy": {
                "Network Coverage": 78, "Network Quality": 90, "Brand Strength": 72,
                "Price Competitiveness": 82, "Customer Service": 72, "Digital Experience": 85,
                "Enterprise Solutions": 55, "Innovation": 88, "Distribution": 68,
            },
            "cyta_cy": {
                "Network Coverage": 98, "Network Quality": 80, "Brand Strength": 88,
                "Price Competitiveness": 55, "Customer Service": 68, "Digital Experience": 65,
                "Enterprise Solutions": 88, "Innovation": 62, "Distribution": 92,
            },
            "primetel_cy": {
                "Network Coverage": 70, "Network Quality": 72, "Brand Strength": 55,
                "Price Competitiveness": 78, "Customer Service": 70, "Digital Experience": 68,
                "Enterprise Solutions": 45, "Innovation": 60, "Distribution": 55,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "epic_cy",
                "event_date": "2021-07-09",
                "category": "investment",
                "title": "Epic launches 5G network in Cyprus — first commercial 5G",
                "description": "Epic officially launched Cyprus's first 5G network in July 2021 after winning spectrum in Dec 2020 auction. EIB provided EUR 19M financing for FTTH rollout. Targeting nationwide 5G coverage.",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "cyta_cy",
                "event_date": "2024-01-03",
                "category": "competitive",
                "title": "Cyta employees strike over proposed operational changes",
                "description": "Cyta workers escalated strike measures over proposed organizational changes including new employee categories and promotion system. Highlights challenges of operating state-owned telco with unionized workforce.",
                "impact_type": "negative",
                "severity": "medium",
            },
            {
                "operator_id": "cyta_cy",
                "event_date": "2025-01-01",
                "category": "investment",
                "title": "Cyta announces EUR 108M strategic investments for 2025",
                "description": "Cyta plans EUR 108M in strategic investments for 2025 focusing on FTTP expansion, 5G network deployment, and digital transformation. Significant capex for state-owned operator in small market.",
                "impact_type": "positive",
                "severity": "high",
            },
        ],
        "earnings_highlights": {
            "epic_cy": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "Epic is #1 mobile network in speed tests (Ookla). 5G pioneer since Jul 2021. Growing subscriber base challenging Cyta's dominance. NJJ/Monaco Telecom ownership providing investment commitment.", "speaker": "CEO"},
                {"segment": "Broadband", "highlight_type": "outlook", "content": "FTTH rollout funded by EIB EUR 19M. Growing broadband subscriber base. Mobile-first evolving toward convergence to compete with Cyta's fixed-mobile bundles.", "speaker": "CEO"},
            ],
            "cyta_cy": [
                {"segment": "Overall", "highlight_type": "guidance", "content": "2024 revenue target EUR 412M. FTTP coverage 77% of premises. Mobile market leader with ~52% share via Cytamobile-Vodafone brand. 1,300 employees. EUR 148M personnel costs.", "speaker": "CEO"},
                {"segment": "Investment", "highlight_type": "outlook", "content": "EUR 108M strategic investments planned for 2025. Focusing on fiber expansion, 5G deployment, and enterprise ICT growth. New employee promotion system implemented for modernization.", "speaker": "CFO"},
            ],
            "primetel_cy": [
                {"segment": "Overall", "highlight_type": "guidance", "content": "PrimeTel maintains ~13% mobile market share. Competing on broadband and TV bundles against larger Cyta and Epic. Value-oriented positioning in small Cyprus market.", "speaker": "CEO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_cyprus as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
