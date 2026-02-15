"""Seed the database with Switzerland telecom market data.

3-player market: Swisscom (dominant incumbent), Sunrise (post-UPC merger), Salt (NJJ challenger).
Currency: CHF. All revenue figures in CHF millions per quarter.

Data sources:
  - Salt FY2024 Results (Matterhorn Telecom press releases)
  - Swisscom Annual Report 2024, quarterly reports
  - Sunrise FY2024 Results, quarterly reports (Liberty Global / SIX filings)
  - BAKOM / COMCOM regulatory data
  - Swiss Federal Statistical Office / IMF
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "switzerland"
OPERATORS = ["salt_ch", "swisscom_ch", "sunrise_ch"]


def get_seed_data():
    return {
        "financials": {
            # Salt Mobile SA — NJJ/Xavier Niel owned, private company
            # FY2024: Revenue CHF 973.2M (+4.4%), EBITDA CHF 586M, margin ~60%
            # FY2024: Capex CHF 223.6M, FCF CHF 375.8M (+27.3%)
            # ~1,150 employees; among highest EBITDA margins in Europe
            "salt_ch": {
                "total_revenue": [225, 230, 233, 237, 237, 246, 245, 245],
                "service_revenue": [210, 215, 218, 222, 222, 231, 230, 230],
                "service_revenue_growth_pct": [2.5, 3.0, 3.2, 3.5, 5.3, 7.4, 5.2, 3.4],
                "mobile_service_revenue": [175, 178, 180, 183, 180, 186, 184, 183],
                "mobile_service_growth_pct": [1.5, 2.0, 2.2, 2.5, 2.9, 4.5, 2.2, 0.0],
                "fixed_service_revenue": [25, 27, 28, 30, 32, 35, 37, 38],
                "fixed_service_growth_pct": [15.0, 17.0, 18.0, 20.0, 28.0, 29.6, 32.1, 26.7],
                "b2b_revenue": [10, 10, 10, 9, 10, 10, 9, 9],
                "ebitda": [138, 142, 144, 148, 144, 150, 148, 144],
                "ebitda_margin_pct": [61.3, 61.7, 61.8, 62.4, 60.8, 61.0, 60.4, 58.8],
                "ebitda_growth_pct": [1.0, 1.5, 1.8, 2.0, 4.3, 5.6, 2.8, -2.7],
                "capex": [52, 55, 56, 57, 56, 65, 59, 44],
                "capex_to_revenue_pct": [23.1, 23.9, 24.0, 24.1, 23.6, 26.4, 24.1, 18.0],
                "employees": [1100, 1100, 1120, 1130, 1130, 1140, 1150, 1150],
                "_source": "Salt FY2024 results (Matterhorn Telecom); Q2 2024 CHF 285.6M rev confirmed",
            },
            # Swisscom AG — 51% Swiss Confederation, listed (SIX: SCMN)
            # Switzerland segment FY2024: Revenue ~CHF 8,006M, EBITDA CHF 3,679M
            # Group FY2024: Revenue CHF 11,036M, EBITDA CHF 4,355M
            # Using Switzerland segment only for market comparison
            "swisscom_ch": {
                "total_revenue": [1993, 1995, 1978, 2040, 2050, 2065, 2055, 2080],
                "service_revenue": [1850, 1855, 1840, 1900, 1910, 1925, 1915, 1940],
                "service_revenue_growth_pct": [-1.5, -1.2, -1.8, -0.5, -2.1, -1.5, -1.3, -1.0],
                "mobile_service_revenue": [520, 525, 522, 535, 530, 540, 535, 545],
                "mobile_service_growth_pct": [-0.5, 0.0, -0.5, 0.5, 1.9, 2.9, 2.5, 1.9],
                "fixed_service_revenue": [880, 878, 870, 885, 878, 880, 875, 885],
                "fixed_service_growth_pct": [-2.5, -2.2, -2.8, -1.5, -0.2, 0.2, 0.6, 0.0],
                "b2b_revenue": [290, 295, 298, 308, 305, 312, 315, 320],
                "ebitda": [915, 930, 910, 924, 920, 940, 925, 935],
                "ebitda_margin_pct": [45.9, 46.6, 46.0, 45.3, 44.9, 45.5, 45.0, 45.0],
                "ebitda_growth_pct": [-3.5, -3.0, -4.5, -4.0, 0.5, 1.1, 1.6, 1.2],
                "capex": [420, 430, 425, 437, 440, 445, 440, 430],
                "capex_to_revenue_pct": [21.1, 21.6, 21.5, 21.4, 21.5, 21.5, 21.4, 20.7],
                "employees": [15905, 15905, 15905, 15905, 15800, 15800, 15800, 15800],
                "_source": "Swisscom Annual Report 2024 (Switzerland segment); Q1-Q3 2024 quarterly reports",
            },
            # Sunrise Communications AG — Spun off from Liberty Global Nov 2024
            # FY2024: Revenue CHF 3,018M (-0.6%), EBITDAaL CHF 1,029.9M (+0.7%)
            # Capex CHF 509.9M (-5.2%), FCF CHF 362.5M (+2.8%)
            # ~2,750 employees; synergies target CHF 325M from UPC merger
            "sunrise_ch": {
                "total_revenue": [753, 755, 749, 761, 747, 738, 749, 785],
                "service_revenue": [680, 682, 678, 690, 676, 668, 678, 710],
                "service_revenue_growth_pct": [-0.5, -0.3, -0.8, 0.0, -1.0, -2.1, 0.0, 2.9],
                "mobile_service_revenue": [235, 238, 240, 245, 240, 242, 245, 255],
                "mobile_service_growth_pct": [3.0, 3.5, 3.8, 4.0, 2.1, 1.7, 2.1, 4.1],
                "fixed_service_revenue": [330, 328, 322, 320, 318, 310, 315, 325],
                "fixed_service_growth_pct": [-3.0, -2.8, -3.5, -3.0, -3.6, -5.5, -2.2, 1.6],
                "b2b_revenue": [190, 195, 200, 210, 200, 205, 210, 215],
                "ebitda": [254, 260, 256, 260, 250, 255, 260, 265],
                "ebitda_margin_pct": [33.7, 34.4, 34.2, 34.2, 33.5, 34.6, 34.7, 33.8],
                "ebitda_growth_pct": [0.5, 1.0, 0.8, 1.2, -1.6, -1.9, 1.6, 1.9],
                "capex": [140, 138, 132, 128, 130, 128, 125, 127],
                "capex_to_revenue_pct": [18.6, 18.3, 17.6, 16.8, 17.4, 17.3, 16.7, 16.2],
                "employees": [2850, 2850, 2800, 2750, 2750, 2700, 2700, 2650],
                "_source": "Sunrise FY2024 results (SIX/Nasdaq filings); Q1-Q4 2024 quarterly data",
            },
        },
        "subscribers": {
            "salt_ch": {
                "mobile_total_k": [1900, 1920, 1940, 1960, 1980, 2000, 2020, 2050],
                "mobile_postpaid_k": [1580, 1600, 1620, 1640, 1660, 1680, 1700, 1720],
                "mobile_prepaid_k": [320, 320, 320, 320, 320, 320, 320, 330],
                "mobile_net_adds_k": [15, 20, 20, 20, 20, 20, 20, 30],
                "mobile_churn_pct": [1.5, 1.5, 1.4, 1.4, 1.4, 1.3, 1.3, 1.3],
                "mobile_arpu": [38.0, 38.5, 39.0, 39.5, 39.0, 39.5, 39.0, 38.5],
                "broadband_total_k": [190, 200, 210, 220, 230, 240, 250, 265],
                "broadband_fiber_k": [190, 200, 210, 220, 230, 240, 250, 265],
                "broadband_net_adds_k": [8, 10, 10, 10, 10, 10, 10, 15],
                "tv_total_k": [0, 0, 0, 0, 0, 0, 0, 0],
                "b2b_customers_k": [20, 20, 21, 21, 22, 22, 23, 23],
                "_source": "Salt FY2024; postpaid >1.7M, broadband passed 250K in Q4 2024",
            },
            "swisscom_ch": {
                "mobile_total_k": [6277, 6290, 6310, 6331, 6340, 6360, 6380, 6400],
                "mobile_postpaid_k": [5150, 5180, 5210, 5240, 5270, 5300, 5330, 5360],
                "mobile_prepaid_k": [1127, 1110, 1100, 1091, 1070, 1060, 1050, 1040],
                "mobile_net_adds_k": [5, 13, 20, 21, 9, 20, 20, 20],
                "mobile_churn_pct": [1.0, 1.0, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9],
                "mobile_arpu": [48.0, 48.0, 47.5, 47.0, 47.0, 46.5, 46.5, 46.0],
                "broadband_total_k": [2006, 2000, 1990, 1967, 1960, 1955, 1950, 1945],
                "broadband_fiber_k": [1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850],
                "broadband_net_adds_k": [-5, -6, -10, -23, -7, -5, -5, -5],
                "tv_total_k": [1537, 1530, 1520, 1493, 1485, 1480, 1475, 1470],
                "b2b_customers_k": [180, 181, 182, 183, 184, 185, 186, 187],
                "_source": "Swisscom 2024 Annual Report; mobile 6,331K end-2024, BB 1,967K, TV 1,493K",
            },
            "sunrise_ch": {
                "mobile_total_k": [2900, 2920, 2950, 2971, 3000, 3030, 3078, 3130],
                "mobile_postpaid_k": [2700, 2720, 2750, 2771, 2800, 2830, 2868, 2920],
                "mobile_prepaid_k": [200, 200, 200, 200, 200, 200, 210, 210],
                "mobile_net_adds_k": [20, 20, 30, 21, 29, 30, 48, 59],
                "mobile_churn_pct": [1.2, 1.2, 1.1, 1.1, 1.1, 1.1, 1.0, 1.0],
                "mobile_arpu": [28.0, 28.5, 28.5, 29.0, 27.5, 27.0, 27.5, 28.0],
                "broadband_total_k": [1265, 1275, 1285, 1289, 1295, 1300, 1305, 1320],
                "broadband_fiber_k": [150, 160, 170, 180, 190, 200, 210, 220],
                "broadband_net_adds_k": [5, 10, 10, 4, 6, 5, 5, 10],
                "tv_total_k": [1020, 1015, 1010, 1000, 998, 995, 993, 990],
                "b2b_customers_k": [50, 51, 52, 53, 54, 55, 56, 57],
                "_source": "Sunrise FY2024; mobile postpaid 3,130K, broadband 1,320K, FMC 57.1%",
            },
        },
        "macro": {
            "gdp_growth_pct": 1.3,
            "inflation_pct": 1.1,
            "unemployment_pct": 2.8,
            "telecom_market_size_eur_b": 12.5,
            "telecom_growth_pct": 1.0,
            "five_g_adoption_pct": 35.0,
            "fiber_penetration_pct": 55.0,
            "regulatory_environment": "COMCOM/BAKOM regulation; lighter touch than EU. Swisscom 51% state-owned. Switzerland not EU member; separate framework. Strong data protection (nDSG 2023). 5G spectrum allocated.",
            "digital_strategy": "Swisscom targeting near-universal fiber by 2030. All three MNOs have 5G. Among most expensive telecom markets in Europe. CHF/EUR ~0.95.",
            "source_url": "BAKOM / Swiss Federal Statistical Office / IMF",
        },
        "network": {
            "salt_ch": {
                "five_g_coverage_pct": 75,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 2500,
                "technology_mix": {"mobile_vendor": "Nokia/Ericsson", "spectrum_mhz": 280, "fiber_access": "Own-build + Swiss Fibre Net wholesale", "5g_band": "3500 MHz"},
            },
            "swisscom_ch": {
                "five_g_coverage_pct": 85,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 3500,
                "technology_mix": {"mobile_vendor": "Ericsson", "spectrum_mhz": 380, "fiber_technology": "GPON/XGS-PON", "5g_sa_status": "Deploying"},
            },
            "sunrise_ch": {
                "five_g_coverage_pct": 80,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 500,
                "technology_mix": {"mobile_vendor": "Huawei/Nokia", "spectrum_mhz": 340, "cable_docsis": "3.1", "cable_homepass_k": 2500},
            },
        },
        "executives": {
            "salt_ch": [
                {"name": "Max Nunziata", "title": "CEO", "start_date": "2024-01-01", "background": "Appointed ~2024; Iliad Group executive; overseeing Salt convergence strategy"},
                {"name": "Franck Bernard", "title": "CFO", "start_date": "2020-01-01", "background": "Finance executive managing Matterhorn Telecom/Salt debt structure"},
            ],
            "swisscom_ch": [
                {"name": "Christoph Aeschlimann", "title": "CEO", "start_date": "2022-06-01", "background": "Internal promotion; overseeing fiber expansion and Fastweb+Vodafone Italia integration"},
                {"name": "Eugen Stermetz", "title": "CFO", "start_date": "2021-01-01", "background": "Managing EUR 8B Vodafone Italia acquisition financing"},
            ],
            "sunrise_ch": [
                {"name": "Andre Krause", "title": "CEO", "start_date": "2020-01-01", "background": "Led Sunrise+UPC merger and Liberty Global spin-off. First CEO of independent Sunrise."},
                {"name": "Jany Fruytier", "title": "CFO", "start_date": "2023-01-01", "background": "Finance executive; managing post-spin-off capital structure"},
            ],
        },
        "competitive_scores": {
            "salt_ch": {
                "Network Coverage": 80, "Network Quality": 92, "Brand Strength": 65,
                "Price Competitiveness": 92, "Customer Service": 72, "Digital Experience": 85,
                "Enterprise Solutions": 45, "Innovation": 88, "Distribution": 65,
            },
            "swisscom_ch": {
                "Network Coverage": 98, "Network Quality": 95, "Brand Strength": 95,
                "Price Competitiveness": 45, "Customer Service": 85, "Digital Experience": 80,
                "Enterprise Solutions": 95, "Innovation": 78, "Distribution": 95,
            },
            "sunrise_ch": {
                "Network Coverage": 88, "Network Quality": 82, "Brand Strength": 78,
                "Price Competitiveness": 70, "Customer Service": 75, "Digital Experience": 75,
                "Enterprise Solutions": 72, "Innovation": 75, "Distribution": 82,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "swisscom_ch",
                "event_date": "2024-12-31",
                "category": "investment",
                "title": "Swisscom completes EUR 8B acquisition of Vodafone Italia",
                "description": "Swisscom completed acquisition of Vodafone Italia, merging with Fastweb to create 'Fastweb + Vodafone'. EUR ~600M annual synergies targeted. CHF 227M integration costs in 2024 EBITDA. Management bandwidth diverted to Italian integration.",
                "impact_type": "neutral",
                "severity": "high",
            },
            {
                "operator_id": "sunrise_ch",
                "event_date": "2024-11-08",
                "category": "competitive",
                "title": "Sunrise spun off from Liberty Global; listed on SIX and Nasdaq",
                "description": "Sunrise listed on SIX (SUNN) Nov 15 and Nasdaq (SNRE) Nov 13 2024. Opening market cap ~CHF 3.2B. First dividend CHF 3.33/share. Mike Fries (Liberty Global CEO) as Chairman. Now fully independent operator.",
                "impact_type": "neutral",
                "severity": "high",
            },
            {
                "operator_id": "salt_ch",
                "event_date": "2024-12-01",
                "category": "competitive",
                "title": "Salt Home broadband passes 250K subscribers",
                "description": "Salt broadband exceeded 250K subscribers in Q4 2024. Targeting nationwide Salt Home availability by 2025 via own-build fiber + Swisscom wholesale (layer 1 IRU). 10 Gbps symmetric residential fiber offered.",
                "impact_type": "positive",
                "severity": "medium",
            },
            {
                "operator_id": "salt_ch",
                "event_date": "2025-02-01",
                "category": "investment",
                "title": "Matterhorn Telecom refinancing — EUR 420M notes + EUR 430M TLB",
                "description": "Matterhorn Telecom issued EUR 420M 4.500% senior secured notes due 2030 plus EUR 430M Term Loan B3. Funds network investment, subscriber acquisition, and fiber expansion.",
                "impact_type": "neutral",
                "severity": "medium",
            },
            {
                "operator_id": "sunrise_ch",
                "event_date": "2026-01-15",
                "category": "competitive",
                "title": "Sunrise announces ~190 job cuts post-spin-off",
                "description": "Sunrise plans to cut up to 190 jobs (~7% of workforce) as part of post-spin-off restructuring to improve efficiency. Part of CHF 325M annual synergy target from UPC merger.",
                "impact_type": "negative",
                "severity": "medium",
            },
        ],
        "earnings_highlights": {
            "salt_ch": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "FY2024 revenue CHF 973.2M (+4.4%), operating EBITDA margin ~60%, among highest in Europe. Mobile postpaid base exceeds 1.7M. Salt Connect magazine network score 952/1000 ('outstanding').", "speaker": "CEO"},
                {"segment": "Broadband", "highlight_type": "outlook", "content": "Salt Home broadband passed 250K subscribers in Q4 2024. Fixed service revenue growing 25%+ YoY. FTTH accessible to ~2.5M households via own-build + wholesale; targeting 3M by end 2025.", "speaker": "CFO"},
            ],
            "swisscom_ch": [
                {"segment": "Switzerland", "highlight_type": "guidance", "content": "Switzerland segment revenue CHF 8,006M. EBITDA CHF 3,679M (-4.2% incl Vodafone Italia integration costs). FTTH coverage >50% of premises. Mobile lines 6.3M, broadband 1.97M.", "speaker": "CEO"},
                {"segment": "Group", "highlight_type": "outlook", "content": "Group revenue CHF 11,036M. Fastweb+Vodafone Italia integration progressing; EUR 600M annual synergy target. 2025 dividend CHF 26/share (up from CHF 22). Group capex guidance CHF 3.1-3.2B.", "speaker": "CFO"},
            ],
            "sunrise_ch": [
                {"segment": "Overall", "highlight_type": "guidance", "content": "FY2024 revenue CHF 3,018M. EBITDAaL CHF 1,030M. Mobile postpaid +159K net adds (+6.0%). FMC convergence rate 57.1%. Successfully completed SIX/Nasdaq dual listing.", "speaker": "CEO"},
                {"segment": "Residential", "highlight_type": "explanation", "content": "Residential revenue CHF 2,173M (-3.3%). B2B revenue CHF 830M (+6.9%). Capex/revenue improved to 16.9%. First dividend as independent company CHF 3.33/share (~CHF 240M total).", "speaker": "CFO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_switzerland as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
