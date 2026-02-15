"""Seed the database with Ireland telecom market data.

3-player mobile market: Three Ireland (#1 mobile), Vodafone Ireland (#2), eir (#3 mobile, #1 fixed).
Currency: EUR. All revenue figures in EUR millions per quarter.

Data sources:
  - eir FY2024 results (RTE, eir Investor Relations)
  - Three Ireland FY2024 (Irish Times, CK Hutchison Annual Results)
  - Vodafone Ireland FY24 (Irish Times, Vodafone Group quarterly reports)
  - ComReg Quarterly Key Data Report Q4 2024
  - CSO Ireland population/GDP statistics
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "ireland"
OPERATORS = ["eir_ie", "three_ie", "vodafone_ie"]


def get_seed_data():
    return {
        "financials": {
            # eir — NJJ/Xavier Niel >70% ownership, Ireland's fixed-line incumbent
            # FY2024: Revenue EUR 1,326M (+2%), EBITDA EUR 614M (+4%), margin ~46.3%
            # ~3,170 employees; EUR 1.7B invested 2018-2024
            "eir_ie": {
                "total_revenue": [318, 322, 325, 330, 322, 327, 332, 345],
                "service_revenue": [295, 299, 302, 307, 300, 305, 310, 322],
                "service_revenue_growth_pct": [1.5, 1.8, 2.0, 2.2, 1.3, 1.9, 2.6, 4.9],
                "mobile_service_revenue": [85, 87, 88, 90, 88, 90, 92, 96],
                "mobile_service_growth_pct": [4.0, 4.5, 5.0, 5.5, 3.5, 3.4, 4.5, 6.7],
                "fixed_service_revenue": [165, 167, 168, 170, 168, 170, 172, 178],
                "fixed_service_growth_pct": [0.5, 0.8, 1.0, 1.2, 1.8, 1.8, 2.4, 4.7],
                "b2b_revenue": [45, 45, 46, 47, 44, 45, 46, 48],
                "ebitda": [145, 148, 150, 152, 148, 152, 155, 159],
                "ebitda_margin_pct": [45.6, 46.0, 46.2, 46.1, 46.0, 46.5, 46.7, 46.1],
                "ebitda_growth_pct": [2.0, 2.5, 3.0, 3.5, 2.1, 2.7, 3.3, 4.6],
                "capex": [68, 70, 72, 73, 70, 72, 74, 76],
                "capex_to_revenue_pct": [21.4, 21.7, 22.2, 22.1, 21.7, 22.0, 22.3, 22.0],
                "employees": [3100, 3120, 3140, 3170, 3170, 3170, 3170, 3170],
                "_source": "eir FY2024 results (RTE/eir IR); quarterly split estimated from annual",
            },
            # Three Ireland — CK Hutchison subsidiary, Ireland's #1 mobile operator
            # FY2024: Revenue EUR 630.4M (+2.5%), Operating profit EUR 36M (+50%)
            # Net loss EUR 31.2M (improving); EBITDA ~EUR 165M (CK Hutchison report)
            # ~1,200 employees (down from 1,353 in 2023)
            "three_ie": {
                "total_revenue": [153, 155, 157, 157, 155, 157, 159, 159],
                "service_revenue": [140, 142, 144, 144, 143, 145, 147, 147],
                "service_revenue_growth_pct": [1.5, 2.0, 2.5, 2.8, 1.3, 1.9, 2.1, 2.1],
                "mobile_service_revenue": [135, 137, 139, 139, 138, 140, 142, 142],
                "mobile_service_growth_pct": [1.5, 2.0, 2.5, 2.8, 2.2, 2.2, 2.2, 2.2],
                "fixed_service_revenue": [5, 5, 5, 5, 5, 5, 5, 5],
                "fixed_service_growth_pct": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                "b2b_revenue": [20, 20, 21, 21, 20, 20, 21, 21],
                "ebitda": [38, 40, 42, 40, 40, 42, 43, 42],
                "ebitda_margin_pct": [24.8, 25.8, 26.8, 25.5, 25.8, 26.8, 27.0, 26.4],
                "ebitda_growth_pct": [3.0, 5.3, 7.7, 5.3, 5.3, 5.0, 2.4, 5.0],
                "capex": [25, 26, 27, 27, 26, 27, 28, 28],
                "capex_to_revenue_pct": [16.3, 16.8, 17.2, 17.2, 16.8, 17.2, 17.6, 17.6],
                "employees": [1353, 1330, 1300, 1280, 1250, 1230, 1210, 1199],
                "_source": "Three Ireland FY2024 (Irish Times); CK Hutchison 2024 results; EBITDA ~HK$1,290M",
            },
            # Vodafone Ireland — Vodafone Group subsidiary
            # FY (Apr-Mar): Revenue EUR 1,000M (+2.8%), Adj EBITDA EUR 164M
            # Aligned to calendar year estimates below
            # ~979 employees
            "vodafone_ie": {
                "total_revenue": [245, 248, 250, 252, 252, 255, 258, 260],
                "service_revenue": [215, 218, 220, 222, 222, 225, 228, 230],
                "service_revenue_growth_pct": [1.5, 2.0, 2.5, 2.8, 2.9, 3.2, 3.6, 3.6],
                "mobile_service_revenue": [142, 144, 146, 148, 148, 150, 152, 154],
                "mobile_service_growth_pct": [1.5, 2.0, 2.5, 2.8, 4.2, 4.2, 4.1, 4.1],
                "fixed_service_revenue": [48, 49, 50, 50, 50, 51, 52, 52],
                "fixed_service_growth_pct": [2.0, 2.0, 2.0, 2.0, 4.2, 4.1, 4.0, 4.0],
                "b2b_revenue": [25, 25, 24, 24, 24, 24, 24, 24],
                "ebitda": [38, 40, 42, 42, 42, 44, 44, 45],
                "ebitda_margin_pct": [15.5, 16.1, 16.8, 16.7, 16.7, 17.3, 17.1, 17.3],
                "ebitda_growth_pct": [5.0, 8.1, 12.0, 10.5, 10.5, 10.0, 4.8, 7.1],
                "capex": [28, 30, 30, 32, 30, 32, 32, 34],
                "capex_to_revenue_pct": [11.4, 12.1, 12.0, 12.7, 11.9, 12.5, 12.4, 13.1],
                "employees": [960, 965, 970, 979, 980, 985, 985, 990],
                "_source": "Vodafone Ireland FY24 (year end Mar 2024); calendar year estimates; Telecompaper Q3 FY26",
            },
        },
        "subscribers": {
            "eir_ie": {
                "mobile_total_k": [1380, 1400, 1420, 1424, 1440, 1460, 1480, 1509],
                "mobile_postpaid_k": [1080, 1100, 1120, 1101, 1130, 1150, 1175, 1203],
                "mobile_prepaid_k": [300, 300, 300, 323, 310, 310, 305, 306],
                "mobile_net_adds_k": [15, 20, 20, 4, 16, 20, 20, 29],
                "mobile_churn_pct": [1.3, 1.2, 1.2, 1.2, 1.2, 1.1, 1.1, 1.1],
                "mobile_arpu": [24.0, 24.5, 25.0, 25.0, 25.0, 25.5, 25.5, 26.0],
                "broadband_total_k": [460, 462, 465, 468, 470, 472, 475, 473],
                "broadband_fiber_k": [420, 425, 430, 435, 440, 445, 450, 455],
                "broadband_net_adds_k": [2, 2, 3, 3, 2, 2, 3, -2],
                "tv_total_k": [98, 100, 102, 104, 106, 108, 110, 112],
                "b2b_customers_k": [35, 35, 36, 36, 37, 37, 38, 38],
                "_source": "eir FY2024: mobile 1,509K (+6%), BB 886K fiber connections (94% on fiber), TV 112K (+11%)",
            },
            "three_ie": {
                # Three reports ~48% mobile share incl M2M/MBB; retail mobile ~28.6%
                # Estimated retail mobile subs ~2,400K
                "mobile_total_k": [2300, 2320, 2340, 2360, 2370, 2380, 2390, 2400],
                "mobile_postpaid_k": [1350, 1360, 1380, 1400, 1410, 1420, 1430, 1440],
                "mobile_prepaid_k": [950, 960, 960, 960, 960, 960, 960, 960],
                "mobile_net_adds_k": [10, 20, 20, 20, 10, 10, 10, 10],
                "mobile_churn_pct": [1.5, 1.5, 1.4, 1.4, 1.4, 1.3, 1.3, 1.3],
                "mobile_arpu": [17.0, 17.5, 17.5, 18.0, 17.5, 18.0, 18.0, 18.5],
                "broadband_total_k": [50, 52, 55, 58, 60, 62, 65, 68],
                "broadband_fiber_k": [50, 52, 55, 58, 60, 62, 65, 68],
                "broadband_net_adds_k": [2, 2, 3, 3, 2, 2, 3, 3],
                "tv_total_k": [0, 0, 0, 0, 0, 0, 0, 0],
                "b2b_customers_k": [25, 25, 26, 26, 27, 27, 28, 28],
                "_source": "Three Ireland; ComReg Q4 2024 data; 5G sites: 1,497 in 2024",
            },
            "vodafone_ie": {
                "mobile_total_k": [2050, 2060, 2080, 2100, 2100, 2110, 2120, 2130],
                "mobile_postpaid_k": [1360, 1370, 1390, 1400, 1400, 1410, 1420, 1436],
                "mobile_prepaid_k": [690, 690, 690, 700, 700, 700, 700, 694],
                "mobile_net_adds_k": [5, 10, 20, 20, 0, 10, 10, 10],
                "mobile_churn_pct": [1.3, 1.3, 1.2, 1.2, 1.2, 1.2, 1.1, 1.1],
                "mobile_arpu": [25.0, 25.5, 26.0, 26.0, 26.0, 26.5, 26.5, 27.0],
                "broadband_total_k": [330, 333, 336, 340, 342, 344, 346, 346],
                "broadband_fiber_k": [100, 110, 120, 130, 140, 150, 160, 170],
                "broadband_net_adds_k": [2, 3, 3, 4, 2, 2, 2, 0],
                "tv_total_k": [150, 148, 146, 145, 143, 141, 140, 138],
                "b2b_customers_k": [40, 40, 41, 41, 42, 42, 43, 43],
                "_source": "Vodafone Ireland; ComReg Q4 2024; 2,130K total mobile (Q3 FY26); 20.7% BB share",
            },
        },
        "macro": {
            "gdp_growth_pct": 2.6,
            "inflation_pct": 1.0,
            "unemployment_pct": 4.2,
            "telecom_market_size_eur_b": 5.0,
            "telecom_growth_pct": 2.5,
            "five_g_adoption_pct": 25.0,
            "fiber_penetration_pct": 51.0,
            "regulatory_environment": "ComReg pro-competition; MBSA2 spectrum auction Dec 2022 (EUR 448M total). Wholesale access mandated on eir. 5G deployed by all three MNOs. National Broadband Plan (EUR 2.7B) via NBI.",
            "digital_strategy": "NBP targeting 100% broadband by 2027. FTTP 74% premises availability (Q4 2024). Gigabit 85% availability. Ireland as EU tech hub (Apple, Google, Meta HQs). Population 5.4M (CSO Apr 2024).",
            "source_url": "ComReg Q4 2024 / CSO Ireland / EU Digital Decade",
        },
        "network": {
            "eir_ie": {
                "five_g_coverage_pct": 74,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 2200,
                "technology_mix": {"mobile_vendor": "Nokia", "spectrum_mhz": 350, "fiber_technology": "GPON/XGS-PON", "ftth_premises_k": 1300},
            },
            "three_ie": {
                "five_g_coverage_pct": 90,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 0,
                "technology_mix": {"mobile_vendor": "Ericsson", "spectrum_mhz": 350, "5g_sites": 1497, "5g_sa_status": "Deployed"},
            },
            "vodafone_ie": {
                "five_g_coverage_pct": 65,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 620,
                "technology_mix": {"mobile_vendor": "Ericsson/Nokia", "spectrum_mhz": 360, "siro_jv_homepass_k": 620, "3g_shutdown": "Nov 2024"},
            },
        },
        "executives": {
            "eir_ie": [
                {"name": "Oliver Loomes", "title": "CEO", "start_date": "2022-02-01", "background": "Ex-Vodafone Ireland CEO; now leading eir under NJJ ownership; FTTH expansion strategy"},
                {"name": "Stephen Tighe", "title": "CFO", "start_date": "2020-01-01", "background": "Finance executive; managing NJJ ownership transition and capex investment"},
            ],
            "three_ie": [
                {"name": "Elaine Carey", "title": "CEO", "start_date": "2024-04-01", "background": "Replaced Robert Finnegan Q2 2024; new leadership under CK Hutchison review"},
            ],
            "vodafone_ie": [
                {"name": "Sabrina Casalta", "title": "CEO", "start_date": "2025-05-01", "background": "Replaced Amanda Nelson (2022-2025); Vodafone Group appointment"},
            ],
        },
        "competitive_scores": {
            "eir_ie": {
                "Network Coverage": 95, "Network Quality": 82, "Brand Strength": 82,
                "Price Competitiveness": 68, "Customer Service": 70, "Digital Experience": 72,
                "Enterprise Solutions": 85, "Innovation": 75, "Distribution": 88,
            },
            "three_ie": {
                "Network Coverage": 90, "Network Quality": 88, "Brand Strength": 80,
                "Price Competitiveness": 85, "Customer Service": 65, "Digital Experience": 72,
                "Enterprise Solutions": 55, "Innovation": 78, "Distribution": 80,
            },
            "vodafone_ie": {
                "Network Coverage": 85, "Network Quality": 82, "Brand Strength": 85,
                "Price Competitiveness": 68, "Customer Service": 78, "Digital Experience": 78,
                "Enterprise Solutions": 82, "Innovation": 72, "Distribution": 82,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "eir_ie",
                "event_date": "2024-10-04",
                "category": "investment",
                "title": "Xavier Niel consolidates eir ownership to >70%",
                "description": "NJJ acquired Davidson Kempner's 8.9% stake in three tranches (Sep 2024-Feb 2025). NJJ now controls >70% of eir. Niel: 'It will never be for sale until the day I die.' Anchorage Capital retains ~19.4%.",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "three_ie",
                "event_date": "2026-01-20",
                "category": "competitive",
                "title": "Liberty Global in talks to acquire Three Ireland for EUR 1.5B",
                "description": "CK Hutchison in advanced discussions to sell Three Ireland to Liberty Global (Virgin Media Ireland parent) for up to EUR 1.5B. Would create converged fixed-mobile operator.",
                "impact_type": "neutral",
                "severity": "high",
            },
            {
                "operator_id": "three_ie",
                "event_date": "2024-04-01",
                "category": "competitive",
                "title": "Three Ireland CEO transition — Elaine Carey replaces Robert Finnegan",
                "description": "Elaine Carey appointed CEO of Three Ireland, replacing Robert Finnegan who moved to deputy chairman at CK Hutchison Telecoms Group. Near-complete executive team refresh.",
                "impact_type": "neutral",
                "severity": "medium",
            },
            {
                "operator_id": "eir_ie",
                "event_date": "2024-12-01",
                "category": "investment",
                "title": "eir FTTH passes 1.3M premises — targeting 1.9M by 2026",
                "description": "eir FTTH premises passed grew 17% YoY to 1.3M. Combined FTTH/FTTC covers 2.2M premises (95% of Ireland). InfraVia JV financing FTTH expansion to 1.9M by 2026.",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "vodafone_ie",
                "event_date": "2024-11-01",
                "category": "investment",
                "title": "Vodafone Ireland completes 3G network shutdown",
                "description": "Vodafone Ireland completed 3G network phase-out in November 2024, freeing spectrum for 4G/5G refarming. SIRO JV (50/50 with ESB) now live in all 26 counties, 620K premises passed.",
                "impact_type": "positive",
                "severity": "medium",
            },
            {
                "operator_id": None,
                "event_date": "2024-12-01",
                "category": "regulatory",
                "title": "NBP exceeds 2024 target — 300K+ premises passed by NBI",
                "description": "National Broadband Ireland surpassed 300K premises passed target. On track for 420K+ by end 2025. EUR 2.7B state-funded rural broadband program targeting 100% coverage by end 2026.",
                "impact_type": "neutral",
                "severity": "medium",
            },
        ],
        "earnings_highlights": {
            "eir_ie": [
                {"segment": "Overall", "highlight_type": "guidance", "content": "FY2024 revenue EUR 1,326M (+2%), EBITDA EUR 614M (+4%), margin 46.3%. Mobile subs 1,509K (+6% YoY). Fiber BB connections 886K (94% on fiber). NJJ ownership consolidated to >70%.", "speaker": "CEO"},
                {"segment": "Infrastructure", "highlight_type": "outlook", "content": "EUR 1.7B invested since 2018. FTTH passing 1.3M premises (+17% YoY), targeting 1.9M by 2026 via InfraVia JV. Combined FTTH/FTTC 2.2M premises (95% of Ireland). TV +11% to 112K.", "speaker": "CFO"},
            ],
            "three_ie": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "FY2024 revenue EUR 630.4M (+2.5%). Operating profit EUR 36M (+50%). Net loss narrowed to EUR 31.2M. 5G sites upgraded to 1,497 in 2024. ~48% mobile share (incl M2M/MBB).", "speaker": "CEO"},
                {"segment": "Strategic", "highlight_type": "outlook", "content": "CK Hutchison reviewing European telecom portfolio; Liberty Global in talks for EUR 1.5B acquisition. New CEO Elaine Carey; almost entire executive team refreshed in 2024. Employees reduced to 1,199.", "speaker": "CFO"},
            ],
            "vodafone_ie": [
                {"segment": "Overall", "highlight_type": "guidance", "content": "FY (Mar 2024) revenue EUR 1,000M (+2.8%). EBITDA EUR 164M. Pretax loss narrowed 83% to EUR 4.8M. Q3 FY26 service revenue EUR 222M quarterly. New CEO Sabrina Casalta from May 2025.", "speaker": "CEO"},
                {"segment": "Network", "highlight_type": "outlook", "content": "3G shutdown completed Nov 2024. SIRO fiber JV live in all 26 counties, 620K premises. Spectrum: EUR 146M invested in MBSA2 auction (most of three operators). 5G expanding.", "speaker": "CFO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_ireland as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
