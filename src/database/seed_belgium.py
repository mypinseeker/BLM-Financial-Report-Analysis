"""Seed the database with Belgium telecom market data.

3-player market: Proximus (incumbent), Orange Belgium (post-VOO acquisition), Telenet (cable/Liberty Global).
Currency: EUR. All revenue figures in EUR millions per quarter.

Data sources:
  - Proximus quarterly press releases Q1 2024 — Q3 2025
  - Orange Belgium H1/FY 2024-2025 results (semi-annual reporting)
  - Telenet/Liberty Global quarterly reports (SEC filings)
  - BIPT market reports
  - EU Digital Decade 2025 Belgium report

Note: Proximus figures are DOMESTIC segment only (excl. BICS/Route Mobile).
Orange Belgium reports semi-annually; quarterly figures are estimated splits.
DIGI Belgium (4th operator, launched Dec 2024) not modeled as full operator
due to negligible market share (~78K mobile subs by Q3 2025).
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "belgium"
OPERATORS = ["proximus_be", "orange_be", "telenet_be"]


def get_seed_data():
    return {
        "financials": {
            # Proximus DOMESTIC segment — Belgian incumbent, state-owned 53.5%
            # FY2024 Domestic: Revenue EUR 4,826M, EBITDA EUR 1,682M, CapEx EUR 1,355M
            # Q1 2024: Domestic rev EUR 1,201M (+4.5%), EBITDA EUR 424M (+4.7%)
            # Q2 2024: Domestic rev EUR 1,200M (+4.6%), EBITDA EUR 437M (+5.1%)
            # Q3 2024: Domestic rev EUR 1,191M (+1.5%), EBITDA EUR 429M (+1.3%)
            # Q4 2024: Domestic rev EUR 1,234M (+3.2%), EBITDA EUR 392M (-0.1%)
            # Q1 2025: Domestic rev EUR 1,216M (+1.2%), EBITDA EUR 430M (+1.5%)
            # Q2 2025: Domestic EBITDA EUR 446M (+1.9%)
            # Q3 2025: Domestic EBITDA EUR 437M (+1.8%)
            "proximus_be": {
                "total_revenue": [1201, 1200, 1191, 1234, 1216, 1210, 1191, 1240],
                "service_revenue": [1050, 1060, 1055, 1085, 1070, 1075, 1065, 1095],
                "service_revenue_growth_pct": [4.5, 4.6, 1.5, 3.2, 1.2, 1.3, 1.0, 0.9],
                "mobile_service_revenue": [370, 375, 378, 385, 380, 383, 386, 392],
                "mobile_service_growth_pct": [3.0, 3.2, 2.5, 3.5, 2.7, 2.1, 2.1, 1.8],
                "fixed_service_revenue": [520, 525, 518, 535, 528, 530, 522, 540],
                "fixed_service_growth_pct": [1.5, 2.0, 0.5, 2.5, 1.5, 1.0, 0.8, 0.9],
                "b2b_revenue": [310, 312, 310, 318, 315, 313, 310, 320],
                "ebitda": [424, 437, 429, 392, 430, 446, 437, 400],
                "ebitda_margin_pct": [35.3, 36.4, 36.0, 31.8, 35.4, 36.9, 36.7, 32.3],
                "ebitda_growth_pct": [4.7, 5.1, 1.3, -0.1, 1.5, 1.9, 1.8, 2.0],
                "capex": [294, 291, 289, 481, 270, 272, 284, 474],
                "capex_to_revenue_pct": [24.5, 24.3, 24.3, 39.0, 22.2, 22.5, 23.8, 38.2],
                "employees": [12725, 12700, 12680, 12650, 12600, 12580, 12550, 12500],
                "_source": "Proximus quarterly press releases Q1 2024-Q3 2025; Q4 2025 estimated (guidance: broadly stable)",
            },
            # Orange Belgium — mobile challenger, acquired VOO cable June 2023
            # FY2024: Revenue EUR 1,993.7M, EBITDAaL EUR 544.3M (+10.1%), eCapex EUR 180.1M (H1)
            # FY2025: Revenue EUR 1,963.4M (-1.5%), EBITDAaL EUR 566.1M (+4.0%), eCapex EUR 375.9M
            # H1 2024: Revenue EUR 977.6M (+2.5%), EBITDAaL EUR 252.9M (+13.9%)
            # H1 2025: Revenue EUR 963M (-1.7%), EBITDAaL EUR 265M (+4.7%)
            # Note: quarterly figures estimated from semi-annual reports
            "orange_be": {
                "total_revenue": [483, 495, 498, 505, 478, 485, 497, 504],
                "service_revenue": [390, 404, 402, 410, 385, 400, 395, 397],
                "service_revenue_growth_pct": [2.5, 2.5, 2.0, 2.2, -1.3, -1.0, -1.7, -3.2],
                "mobile_service_revenue": [220, 226, 228, 232, 218, 224, 226, 230],
                "mobile_service_growth_pct": [3.0, 4.5, 3.5, 3.8, -0.9, -0.9, -0.9, -0.9],
                "fixed_service_revenue": [130, 136, 135, 138, 128, 135, 132, 135],
                "fixed_service_growth_pct": [4.5, 4.5, 3.0, 2.5, -1.5, -0.7, -2.2, -2.2],
                "b2b_revenue": [40, 42, 39, 40, 39, 41, 37, 32],
                "ebitda": [122, 131, 135, 140, 127, 138, 147, 154],
                "ebitda_margin_pct": [25.3, 26.5, 27.1, 27.7, 26.6, 28.5, 29.6, 30.6],
                "ebitda_growth_pct": [10.0, 17.8, 8.0, 6.0, 4.1, 5.3, 8.9, 10.0],
                "capex": [88, 92, 93, 95, 90, 94, 95, 97],
                "capex_to_revenue_pct": [18.2, 18.6, 18.7, 18.8, 18.8, 19.4, 19.1, 19.2],
                "employees": [1700, 1700, 1680, 1680, 1650, 1650, 1630, 1630],
                "_source": "Orange Belgium H1/FY 2024-2025 press releases; quarterly split estimated",
            },
            # Telenet (Liberty Global) — cable operator, incl. BASE mobile
            # FY2024: Revenue EUR 2,851.4M, Adjusted EBITDA EUR 1,357.4M, CapEx EUR 928.5M
            # Q3 2024: Revenue EUR 714.3M; Q4 2024: Revenue EUR 733.3M, EBITDA EUR 346.9M
            # Q2 2025: Revenue EUR 705.9M (Liberty Global Q2 2025 report)
            # Fixed ARPU: EUR 63.77/month (+2.9% YoY) Q4 2024
            "telenet_be": {
                "total_revenue": [695, 709, 714, 733, 700, 706, 710, 735],
                "service_revenue": [620, 635, 640, 660, 628, 634, 638, 662],
                "service_revenue_growth_pct": [0.5, 1.0, 1.5, 2.0, -0.4, -0.2, -0.3, 0.3],
                "mobile_service_revenue": [170, 175, 178, 182, 175, 178, 181, 185],
                "mobile_service_growth_pct": [2.0, 2.5, 3.0, 3.5, 2.9, 1.7, 1.7, 1.6],
                "fixed_service_revenue": [400, 408, 412, 425, 405, 410, 410, 425],
                "fixed_service_growth_pct": [-0.5, 0.5, 1.0, 2.9, 1.3, 0.5, -0.5, 0.0],
                "b2b_revenue": [50, 52, 50, 53, 48, 46, 47, 52],
                "ebitda": [335, 338, 337, 347, 330, 332, 330, 340],
                "ebitda_margin_pct": [48.2, 47.7, 47.2, 47.3, 47.1, 47.0, 46.5, 46.3],
                "ebitda_growth_pct": [0.5, 1.0, 0.8, 1.5, -1.5, -1.8, -2.1, -2.0],
                "capex": [155, 160, 166, 287, 155, 160, 165, 280],
                "capex_to_revenue_pct": [22.3, 22.6, 23.2, 39.2, 22.1, 22.7, 23.2, 38.1],
                "employees": [3200, 3200, 3150, 3150, 3100, 3100, 3050, 3050],
                "_source": "Telenet Q3/Q4 2024 SEC filings, Liberty Global Q2 2025 report",
            },
        },
        "subscribers": {
            # Proximus — confirmed from quarterly press releases
            # Postpaid: +122K net adds in FY2024; prepaid declining structurally
            # Broadband: 2.279M→2.35M; Fiber: 441K→720K active lines
            # TV: declining ~15K/q; FMC: 1.13M→1.22M (penetration ~50-52%)
            "proximus_be": {
                "mobile_total_k": [5514, 5527, 5556, 5586, 5540, 5570, 5600, 5630],
                "mobile_postpaid_k": [4994, 5018, 5065, 5095, 5088, 5127, 5172, 5210],
                "mobile_prepaid_k": [520, 509, 491, 491, 452, 443, 428, 420],
                "mobile_net_adds_k": [-7, 13, 29, 30, -46, 30, 30, 30],
                "mobile_churn_pct": [1.3, 1.2, 1.2, 1.2, 1.3, 1.2, 1.2, 1.2],
                "mobile_arpu": [19.5, 19.8, 19.6, 19.4, 19.3, 19.5, 19.5, 19.5],
                "broadband_total_k": [2279, 2291, 2300, 2313, 2318, 2326, 2338, 2350],
                "broadband_fiber_k": [441, 481, 519, 564, 607, 646, 684, 720],
                "broadband_net_adds_k": [12, 11, 9, 14, 5, 8, 12, 12],
                "tv_total_k": [1659, 1650, 1637, 1630, 1614, 1604, 1594, 1585],
                "b2b_customers_k": [220, 222, 224, 226, 228, 230, 232, 234],
                "_source": "Proximus quarterly KPI reports; fiber homepass 2.2M→2.49M",
            },
            # Orange Belgium — includes VOO cable customers from June 2023
            # FY2024: 3.5M mobile, 1M+ broadband
            # FY2025: Postpaid 3,553K (+2.5% YoY), Cable 1,039K (+1.8% YoY)
            # H1 2024: Postpaid +74K net adds, Cable +18K net adds
            "orange_be": {
                "mobile_total_k": [3350, 3430, 3450, 3500, 3480, 3520, 3540, 3553],
                "mobile_postpaid_k": [3250, 3393, 3420, 3467, 3450, 3500, 3520, 3553],
                "mobile_prepaid_k": [100, 97, 95, 93, 90, 87, 85, 82],
                "mobile_net_adds_k": [30, 44, 20, 17, -20, 20, 20, 13],
                "mobile_churn_pct": [1.8, 1.7, 1.7, 1.6, 1.7, 1.6, 1.6, 1.5],
                "mobile_arpu": [14.5, 14.8, 14.6, 14.9, 14.3, 14.5, 14.4, 14.6],
                "broadband_total_k": [986, 1004, 1015, 1034, 1030, 1034, 1037, 1039],
                "broadband_fiber_k": [20, 22, 25, 28, 30, 33, 36, 40],
                "broadband_net_adds_k": [6, 12, 11, 5, -4, 4, 3, 2],
                "tv_total_k": [780, 790, 795, 800, 798, 800, 802, 805],
                "b2b_customers_k": [45, 46, 47, 48, 49, 50, 51, 52],
                "_source": "Orange Belgium H1/FY reports; cable broadband incl. VOO subscribers",
            },
            # Telenet (incl. BASE mobile) — from SEC filings
            # Q4 2024: Internet 1,718.8K, Video 1,588.6K, Postpaid 2,675K, Prepaid 195.1K
            # FMC 861K (+12.2K in Q4); BASE FMC exceeded 25K target
            # Broadband returned to growth +3.2K net adds in Q4 2024
            # Fixed ARPU EUR 63.77/month (+2.9% YoY)
            "telenet_be": {
                "mobile_total_k": [2905, 2910, 2895, 2870, 2880, 2895, 2910, 2925],
                "mobile_postpaid_k": [2700, 2705, 2690, 2675, 2685, 2700, 2715, 2730],
                "mobile_prepaid_k": [205, 205, 205, 195, 195, 195, 195, 195],
                "mobile_net_adds_k": [5, 5, -15, -25, 10, 15, 15, 15],
                "mobile_churn_pct": [1.5, 1.5, 1.6, 1.6, 1.5, 1.5, 1.4, 1.4],
                "mobile_arpu": [16.0, 16.2, 16.1, 16.3, 16.5, 16.7, 16.8, 17.0],
                "broadband_total_k": [1712, 1715, 1716, 1719, 1722, 1726, 1730, 1735],
                "broadband_fiber_k": [12, 13, 13, 14, 16, 18, 20, 23],
                "broadband_net_adds_k": [-2, 3, 1, 3, 3, 4, 4, 5],
                "tv_total_k": [1600, 1598, 1594, 1589, 1585, 1582, 1578, 1575],
                "b2b_customers_k": [95, 96, 97, 98, 99, 100, 101, 102],
                "_source": "Telenet Q4 2024 SEC filing; Liberty Global quarterly reports",
            },
        },
        "macro": {
            "gdp_growth_pct": 1.2,
            "inflation_pct": 2.5,
            "unemployment_pct": 5.6,
            "telecom_market_size_eur_b": 8.2,
            "telecom_growth_pct": 1.5,
            "five_g_adoption_pct": 35.0,
            "fiber_penetration_pct": 30.7,
            "regulatory_environment": "BIPT pro-competition regulation; completed EUR 1.2B multi-band 5G spectrum auction (2022, 700/900/1800/2100/3600 MHz); 4th operator DIGI Belgium launched Dec 2024 (EUR 5/month 15GB mobile); wholesale fiber access obligations; automatic wage indexation impacts cost bases; Belgian state 53.5% ownership of Proximus",
            "digital_strategy": "EU Digital Decade: 100% 5G coverage by 2030, gigabit broadband for all; Belgium fiber target 50% coverage by 2025; Proximus targeting 95% fiber by 2032; federal broadband subsidies for Wallonia; smart city initiatives Brussels/Antwerp/Ghent",
            "source_url": "BIPT 2024-2025 Market Reports / NBB / Eurostat / EU Digital Decade 2025",
        },
        "network": {
            "proximus_be": {
                "five_g_coverage_pct": 75,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 2491,
                "technology_mix": {"mobile_vendor": "Nokia/Ericsson", "spectrum_mhz": 310, "core_vendor": "Nokia", "5g_sa_status": "Deploying SA", "fiber_technology": "GPON/XGS-PON"},
            },
            "orange_be": {
                "five_g_coverage_pct": 70,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 80,
                "technology_mix": {"mobile_vendor": "Ericsson/Nokia", "spectrum_mhz": 220, "core_vendor": "Ericsson", "cable_docsis": "3.1", "cable_homepass_k": 1500},
            },
            "telenet_be": {
                "five_g_coverage_pct": 72,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 50,
                "technology_mix": {"mobile_vendor": "Nokia", "spectrum_mhz": 200, "core_vendor": "Nokia", "cable_docsis": "3.1", "cable_homepass_k": 4900},
            },
        },
        "executives": {
            "proximus_be": [
                {"name": "Guillaume Boutin", "title": "CEO", "start_date": "2019-12-01", "background": "Former Orange Group executive; driving Bold2025 digital transformation and fiber acceleration"},
                {"name": "Mark Reid", "title": "CFO", "start_date": "2022-04-01", "background": "Ex-British Telecom CFO; managing fiber investment program and shareholder returns"},
                {"name": "Geert Standaert", "title": "CTO", "start_date": "2013-01-01", "background": "Long-tenured technology leader overseeing fiber and 5G rollout"},
            ],
            "orange_be": [
                {"name": "Xavier Pichon", "title": "CEO", "start_date": "2017-07-01", "background": "Orange Group veteran; led EUR 1.8B VOO acquisition and integration; building national convergent platform"},
            ],
            "telenet_be": [
                {"name": "John Porter", "title": "CEO", "start_date": "2013-08-01", "background": "Former Austar CEO (Australia); longest-serving major operator CEO in Belgium; Liberty Global board member"},
                {"name": "Erik Van den Enden", "title": "CFO", "start_date": "2019-01-01", "background": "Former Proximus executive; managing cable investment and JV financial structure"},
            ],
        },
        "competitive_scores": {
            "proximus_be": {
                "Network Coverage": 92, "Network Quality": 88, "Brand Strength": 90,
                "Price Competitiveness": 55, "Customer Service": 78, "Digital Experience": 82,
                "Enterprise Solutions": 92, "Innovation": 85, "Distribution": 88,
            },
            "orange_be": {
                "Network Coverage": 78, "Network Quality": 82, "Brand Strength": 75,
                "Price Competitiveness": 72, "Customer Service": 72, "Digital Experience": 76,
                "Enterprise Solutions": 65, "Innovation": 78, "Distribution": 70,
            },
            "telenet_be": {
                "Network Coverage": 85, "Network Quality": 85, "Brand Strength": 82,
                "Price Competitiveness": 65, "Customer Service": 75, "Digital Experience": 80,
                "Enterprise Solutions": 60, "Innovation": 75, "Distribution": 82,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "orange_be",
                "event_date": "2023-06-01",
                "category": "competitive",
                "title": "Orange Belgium completes EUR 1.8B VOO acquisition",
                "description": "Orange Belgium acquires 75% of VOO SA from Nethys, gaining 1.5M cable homes in Wallonia. Creates national convergent platform competing with Proximus fiber and Telenet cable.",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "proximus_be",
                "event_date": "2024-03-01",
                "category": "investment",
                "title": "Proximus accelerates FTTH — 2.2M homepass, targeting 4.2M by 2028",
                "description": "Proximus fiber footprint reaches 2,224K homes (37% coverage, 42% street coverage). Active fiber lines 564K. On track toward 4.2M by 2028, 95% by 2032.",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": None,
                "event_date": "2024-12-11",
                "category": "competitive",
                "title": "DIGI Belgium launches as disruptive 4th mobile operator",
                "description": "DIGI Belgium (Citymesh/DIGI JV) launches EUR 5/month for 15GB mobile, EUR 10/month for 500Mbps fiber. Initially MVNO on Proximus, building own 4G/5G network. Target: 2M households within 5 years.",
                "impact_type": "negative",
                "severity": "high",
            },
            {
                "operator_id": "telenet_be",
                "event_date": "2024-06-01",
                "category": "commercial",
                "title": "Telenet launches nationwide BASE FMC proposition",
                "description": "BASE fixed-mobile convergent offer launched nationally. Exceeded 25,000 subscription target by end of 2024. FMC growth +12.2K in Q4 2024, best since Q4 2022.",
                "impact_type": "positive",
                "severity": "medium",
            },
            {
                "operator_id": "telenet_be",
                "event_date": "2025-01-10",
                "category": "competitive",
                "title": "Liberty Global evaluates strategic options for Telenet stake",
                "description": "Liberty Global confirms strategic review of European cable assets including Telenet. Potential sale, merger, or IPO under consideration. Ownership uncertainty affects strategic planning.",
                "impact_type": "negative",
                "severity": "high",
            },
            {
                "operator_id": "proximus_be",
                "event_date": "2025-03-01",
                "category": "commercial",
                "title": "Proximus increases mobile data volumes — defensive response to DIGI",
                "description": "Mobile Smart expanded to 50GB (from 35GB), Mobile Maxi to 100GB (from 70GB). No price increase. Defensive move against DIGI Belgium pricing pressure.",
                "impact_type": "neutral",
                "severity": "medium",
            },
            {
                "operator_id": "telenet_be",
                "event_date": "2025-04-01",
                "category": "commercial",
                "title": "Telenet launches TADAAM unlimited mobile at EUR 25/month",
                "description": "TADAAM mobile services with unlimited data, 5G access, eSIM. Competitive response to DIGI Belgium entry targeting data-intensive users.",
                "impact_type": "positive",
                "severity": "medium",
            },
        ],
        "earnings_highlights": {
            "proximus_be": [
                {"segment": "Residential", "highlight_type": "guidance", "content": "FY2024 Domestic revenue EUR 4,826M, EBITDA EUR 1,682M. 2025 guidance: broadly stable. Fiber take-up exceeding 50% in newly connected areas within 12 months. Convergent customer base growing 5%+ annually.", "speaker": "CEO"},
                {"segment": "Mobile", "highlight_type": "explanation", "content": "Residential mobile postpaid +122K net adds in 2024. Prepaid declining structurally. Responding to DIGI Belgium entry with data volume upgrades without price increases.", "speaker": "CEO"},
                {"segment": "Enterprise", "highlight_type": "guidance", "content": "Proximus NXT cloud and cybersecurity services driving enterprise growth. Business mobile ARPU under pressure (-3.8% in Q4 2024).", "speaker": "CFO"},
            ],
            "orange_be": [
                {"segment": "Group", "highlight_type": "guidance", "content": "FY2024 EBITDAaL EUR 544M, exceeding EUR 535M guidance. FY2025 EBITDAaL EUR 566M (+4.0%). VOO synergies driving margin improvement. Mobile postpaid +4.5% YoY growth.", "speaker": "CEO"},
                {"segment": "Fixed", "highlight_type": "outlook", "content": "Cable customer base surpassed 1 million milestone in H1 2024. VOO legal integration completed Oct 2025. 95% gigabit coverage via HFC. National convergent platform operational.", "speaker": "CEO"},
            ],
            "telenet_be": [
                {"segment": "Fixed", "highlight_type": "guidance", "content": "FY2024 revenue EUR 2,851M, EBITDA EUR 1,357M. Broadband net adds returned to growth in 2024 after two years of declines. Fixed ARPU EUR 63.77/month (+2.9% YoY) driven by rate increase and fiber migration.", "speaker": "CEO"},
                {"segment": "Convergence", "highlight_type": "outlook", "content": "FMC growth best since Q4 2022 (+12.2K in Q4 2024). BASE nationwide FMC proposition gaining traction. Expecting low-single-digit EBITDAaL decline in 2025.", "speaker": "CFO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_belgium as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
