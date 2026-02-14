"""Seed the database with Netherlands telecom market data.

3-player market: KPN (incumbent), VodafoneZiggo (cable JV), Odido (mobile challenger).
Currency: EUR. All revenue figures in EUR millions per quarter.

Data sources:
  - KPN Annual Report 2024/2025, quarterly press releases
  - VodafoneZiggo/Liberty Global quarterly reports (SEC filings)
  - Odido FY2024 results (Telecompaper), IPO prospectus data
  - ACM Telecom Monitor Q4 2024 / Q1 2025
  - EU Digital Decade 2025 Netherlands report
  - CBS Netherlands population/GDP statistics
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "netherlands"
OPERATORS = ["odido_nl", "kpn_nl", "vodafoneziggo_nl"]


def get_seed_data():
    return {
        "financials": {
            # Odido (formerly T-Mobile NL) — mobile-centric challenger, PE-owned
            # FY2024: Revenue EUR 2,300M (+1.6%), EBITDA EUR 881M (+2.9%), margin 38.1%
            # ~8M customers total, broadband crossed 1M in Q1 2025
            "odido_nl": {
                "total_revenue": [560, 568, 575, 582, 585, 592, 598, 605],
                "service_revenue": [520, 528, 535, 542, 545, 552, 558, 565],
                "service_revenue_growth_pct": [1.2, 1.5, 1.8, 2.0, 4.5, 4.2, 4.3, 4.0],
                "mobile_service_revenue": [385, 390, 395, 400, 400, 405, 410, 415],
                "mobile_service_growth_pct": [1.5, 1.8, 2.0, 2.2, 3.9, 3.8, 3.8, 3.8],
                "fixed_service_revenue": [95, 98, 100, 102, 105, 108, 110, 112],
                "fixed_service_growth_pct": [8.0, 9.0, 10.0, 10.5, 10.5, 10.2, 10.0, 9.8],
                "b2b_revenue": [40, 40, 40, 40, 40, 39, 40, 38],
                "ebitda": [213, 218, 222, 228, 225, 230, 235, 240],
                "ebitda_margin_pct": [38.0, 38.4, 38.6, 39.2, 38.5, 38.9, 39.3, 39.7],
                "ebitda_growth_pct": [2.0, 2.5, 3.0, 3.5, 5.6, 5.5, 5.9, 5.3],
                "capex": [105, 108, 110, 112, 112, 115, 118, 120],
                "capex_to_revenue_pct": [18.8, 19.0, 19.1, 19.2, 19.1, 19.4, 19.7, 19.8],
                "employees": [2100, 2100, 2100, 2100, 2200, 2200, 2200, 2200],
                "_source": "Odido FY2024 results (Telecompaper); quarterly split estimated from annual",
            },
            # KPN — incumbent, converged, public company
            # FY2024: Revenue ~EUR 5,600M, Service revenue EUR 5,215M, EBITDA AL EUR 2,508M
            # FY2025: Service revenue +2.7%, EBITDA AL EUR 2,636M (+5.1%)
            # Q1 2024 EBITDA EUR 605M (+3.6%), Q2 2025 EBITDA EUR 670M (+6.4%)
            "kpn_nl": {
                "total_revenue": [1370, 1395, 1405, 1430, 1395, 1425, 1435, 1465],
                "service_revenue": [1275, 1300, 1310, 1330, 1305, 1340, 1345, 1370],
                "service_revenue_growth_pct": [2.0, 2.3, 2.5, 2.7, 2.4, 3.1, 2.7, 3.0],
                "mobile_service_revenue": [400, 408, 412, 418, 412, 422, 425, 435],
                "mobile_service_growth_pct": [1.5, 2.0, 2.3, 2.8, 3.0, 3.4, 3.2, 4.1],
                "fixed_service_revenue": [575, 582, 588, 595, 585, 598, 602, 610],
                "fixed_service_growth_pct": [0.5, 0.8, 1.0, 1.2, 1.7, 2.7, 2.4, 2.5],
                "b2b_revenue": [380, 388, 392, 400, 390, 400, 405, 415],
                "ebitda": [605, 640, 630, 633, 640, 670, 660, 666],
                "ebitda_margin_pct": [44.2, 45.9, 44.8, 44.3, 45.9, 47.0, 46.0, 45.4],
                "ebitda_growth_pct": [3.6, 5.6, 2.3, 2.0, 5.8, 4.7, 4.8, 5.2],
                "capex": [305, 320, 315, 315, 310, 320, 315, 305],
                "capex_to_revenue_pct": [22.3, 22.9, 22.4, 22.0, 22.2, 22.5, 22.0, 20.8],
                "employees": [10100, 10200, 10300, 10333, 10400, 10500, 10500, 10600],
                "_source": "KPN N.V. Annual Report 2024, Q1-Q4 2024/2025 quarterly reports",
            },
            # VodafoneZiggo — cable + mobile JV (Liberty Global / Vodafone Group)
            # FY2024: Revenue EUR 4,100M (+1.5%), EBITDA EUR 1,880M (+3.1%)
            # Q1 2024: Rev EUR 1,026M, EBITDA EUR 478M
            # Q3 2024: Rev EUR 1,029M; Q4 2024: Rev ~EUR 1,010M (-2.5%)
            # Q3 2025: Rev EUR 990M (-3.9%), EBITDA EUR 447M
            # ~7,000 employees, cutting 400 in 2025
            "vodafoneziggo_nl": {
                "total_revenue": [1026, 1035, 1029, 1010, 1005, 998, 990, 985],
                "service_revenue": [890, 898, 895, 880, 878, 872, 868, 865],
                "service_revenue_growth_pct": [1.5, 1.8, 1.2, 0.5, -1.3, -2.9, -3.0, -1.7],
                "mobile_service_revenue": [280, 285, 288, 285, 284, 282, 280, 278],
                "mobile_service_growth_pct": [3.4, 3.2, 2.6, 1.8, 1.4, -1.1, -2.8, -2.5],
                "fixed_service_revenue": [480, 483, 478, 468, 467, 464, 462, 460],
                "fixed_service_growth_pct": [-0.8, -0.4, -0.8, -2.0, -2.7, -3.9, -3.3, -1.7],
                "b2b_revenue": [130, 130, 129, 127, 127, 126, 126, 127],
                "ebitda": [478, 482, 480, 440, 445, 440, 447, 440],
                "ebitda_margin_pct": [46.6, 46.6, 46.6, 43.6, 44.3, 44.1, 45.2, 44.7],
                "ebitda_growth_pct": [3.2, 3.5, 3.0, 1.0, -6.9, -8.7, -6.9, 0.0],
                "capex": [210, 218, 212, 210, 215, 210, 208, 205],
                "capex_to_revenue_pct": [20.5, 21.1, 20.6, 20.8, 21.4, 21.0, 21.0, 20.8],
                "employees": [7000, 7000, 7000, 7000, 6800, 6700, 6600, 6600],
                "_source": "VodafoneZiggo quarterly reports (Liberty Global SEC filings)",
            },
        },
        "subscribers": {
            "odido_nl": {
                "mobile_total_k": [6900, 6950, 7050, 7150, 7250, 7350, 7450, 7550],
                "mobile_postpaid_k": [5200, 5250, 5330, 5400, 5480, 5560, 5640, 5720],
                "mobile_prepaid_k": [1700, 1700, 1720, 1750, 1770, 1790, 1810, 1830],
                "mobile_net_adds_k": [30, 50, 100, 100, 100, 100, 100, 100],
                "mobile_churn_pct": [1.3, 1.3, 1.2, 1.2, 1.2, 1.1, 1.1, 1.1],
                "mobile_arpu": [14.5, 14.6, 14.7, 14.8, 14.8, 14.9, 15.0, 15.1],
                "broadband_total_k": [850, 880, 910, 940, 1000, 1040, 1080, 1120],
                "broadband_fiber_k": [200, 220, 240, 260, 300, 330, 360, 390],
                "broadband_net_adds_k": [25, 30, 30, 30, 60, 40, 40, 40],
                "tv_total_k": [0, 0, 0, 0, 0, 0, 0, 0],
                "b2b_customers_k": [85, 86, 87, 88, 89, 90, 91, 92],
                "_source": "Odido / T-Mobile NL; broadband crossed 1M in Q1 2025",
            },
            "kpn_nl": {
                # Consumer postpaid: ~3.8M→4.05M, net adds +30K/q (confirmed Q1 2024, Q3 2025)
                # Consumer broadband: 2.78M→2.9M, fiber 1.75M→2.23M
                # Total mobile incl wholesale: 11.4M but consumer postpaid only here
                "mobile_total_k": [3800, 3830, 3877, 3900, 3930, 3970, 4010, 4050],
                "mobile_postpaid_k": [3800, 3830, 3877, 3900, 3930, 3970, 4010, 4050],
                "mobile_prepaid_k": [0, 0, 0, 0, 0, 0, 0, 0],
                "mobile_net_adds_k": [30, 30, 47, 23, 30, 40, 40, 40],
                "mobile_churn_pct": [1.1, 1.1, 1.0, 1.0, 1.0, 0.9, 0.9, 0.9],
                "mobile_arpu": [17.0, 17.0, 17.0, 17.0, 16.5, 16.0, 16.2, 16.5],
                "broadband_total_k": [2780, 2830, 2836, 2846, 2860, 2875, 2886, 2900],
                "broadband_fiber_k": [1750, 1810, 1880, 1950, 2020, 2090, 2160, 2230],
                "broadband_net_adds_k": [13, 50, 6, 10, 14, 15, 11, 14],
                "tv_total_k": [1500, 1495, 1490, 1485, 1480, 1475, 1470, 1465],
                "b2b_customers_k": [384, 384, 384, 384, 384, 384, 384, 384],
                "_source": "KPN N.V. quarterly KPI reports; fiber homepass 5.05M→5.58M",
            },
            "vodafoneziggo_nl": {
                # Mobile postpaid: 5.27M→5.375M; broadband: 3.2M→2.99M (declining -115K/yr)
                # Video: 3.4M end-2024, declining; FMC: 1.5M households
                "mobile_total_k": [5600, 5600, 5600, 5600, 5620, 5640, 5660, 5680],
                "mobile_postpaid_k": [5270, 5280, 5290, 5300, 5320, 5340, 5357, 5375],
                "mobile_prepaid_k": [330, 320, 310, 300, 300, 300, 303, 305],
                "mobile_net_adds_k": [22, 5, 12, 1, 20, 20, 17, 18],
                "mobile_churn_pct": [1.2, 1.2, 1.1, 1.1, 1.1, 1.1, 1.0, 1.0],
                "mobile_arpu": [14.0, 14.2, 14.4, 14.3, 14.1, 14.0, 13.9, 14.0],
                "broadband_total_k": [3200, 3170, 3145, 3085, 3055, 3028, 3010, 2990],
                "broadband_fiber_k": [50, 55, 60, 65, 70, 75, 80, 85],
                "broadband_net_adds_k": [-27, -30, -25, -30, -30, -27, -18, -20],
                "tv_total_k": [3500, 3480, 3460, 3400, 3380, 3360, 3340, 3320],
                "b2b_customers_k": [110, 111, 112, 113, 114, 115, 116, 117],
                "_source": "VodafoneZiggo quarterly reports; broadband declining -115K/yr in 2024",
            },
        },
        "macro": {
            "gdp_growth_pct": 1.5,
            "inflation_pct": 2.3,
            "unemployment_pct": 3.7,
            "telecom_market_size_eur_b": 12.0,
            "telecom_growth_pct": 3.0,
            "five_g_adoption_pct": 48.0,
            "fiber_penetration_pct": 77.7,
            "regulatory_environment": "ACM pro-competition regulation; joint SMP finding for KPN+VodafoneZiggo in wholesale fixed access; 3.5 GHz auction completed Jul 2024 (EUR 174.4M, 100 MHz each to KPN/Odido/VZ); 2G/3G sunset research published Dec 2024",
            "digital_strategy": "Dutch Gigabit Strategy: 100% gigabit coverage by 2030; all populated areas 5G; 98.3% VHCN coverage already achieved (above EU avg 78.8%); majority of households now using fiber (ACM Q1 2025)",
            "source_url": "ACM Telecom Monitor 2024-2025 / CBS / EU Digital Decade 2025 Netherlands report",
        },
        "network": {
            "odido_nl": {
                "five_g_coverage_pct": 99,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 0,
                "technology_mix": {"mobile_vendor": "Ericsson", "spectrum_mhz": 400, "core_vendor": "Nokia", "5g_sa_status": "Deploying"},
            },
            "kpn_nl": {
                "five_g_coverage_pct": 99,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 5580,
                "technology_mix": {"mobile_vendor": "Nokia", "spectrum_mhz": 420, "core_vendor": "Nokia", "fiber_technology": "GPON/XGS-PON"},
            },
            "vodafoneziggo_nl": {
                "five_g_coverage_pct": 98,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 200,
                "technology_mix": {"mobile_vendor": "Ericsson/Nokia", "spectrum_mhz": 380, "core_vendor": "Ericsson", "cable_docsis": "3.1", "cable_homepass_k": 7000},
            },
        },
        "executives": {
            "odido_nl": [
                {"name": "Soren Abildgaard", "title": "CEO", "start_date": "2023-09-01", "background": "Led T-Mobile NL rebrand to Odido; ex-TDC Denmark; PE-backed transformation leader"},
                {"name": "Gero Niemeyer", "title": "CFO", "start_date": "2023-01-01", "background": "Finance executive; managing PE-backed capital structure"},
            ],
            "kpn_nl": [
                {"name": "Joost Farwerck", "title": "CEO", "start_date": "2019-12-01", "background": "KPN veteran; led fiber acceleration strategy; reappointed 2024"},
                {"name": "Chris Figee", "title": "CFO", "start_date": "2021-04-01", "background": "Ex-Aegon; driving financial efficiency and shareholder returns"},
            ],
            "vodafoneziggo_nl": [
                {"name": "Stephen van Rooyen", "title": "CEO", "start_date": "2024-09-01", "background": "Ex-Sky UK CEO; replaced Jeroen Hoencamp; Ritchy Drost served as interim CEO May-Sep 2024"},
                {"name": "Ritchy Drost", "title": "CFO", "start_date": "2020-01-01", "background": "Also served as interim CEO May-Sep 2024; managing JV financial structure"},
            ],
        },
        "competitive_scores": {
            "odido_nl": {
                "Network Coverage": 88, "Network Quality": 88, "Brand Strength": 65,
                "Price Competitiveness": 78, "Customer Service": 72, "Digital Experience": 85,
                "Enterprise Solutions": 55, "Innovation": 82, "Distribution": 72,
            },
            "kpn_nl": {
                "Network Coverage": 92, "Network Quality": 85, "Brand Strength": 90,
                "Price Competitiveness": 62, "Customer Service": 80, "Digital Experience": 78,
                "Enterprise Solutions": 92, "Innovation": 78, "Distribution": 88,
            },
            "vodafoneziggo_nl": {
                "Network Coverage": 90, "Network Quality": 78, "Brand Strength": 82,
                "Price Competitiveness": 72, "Customer Service": 68, "Digital Experience": 72,
                "Enterprise Solutions": 75, "Innovation": 70, "Distribution": 85,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "odido_nl",
                "event_date": "2023-09-04",
                "category": "competitive",
                "title": "T-Mobile Netherlands rebrands to Odido",
                "description": "Complete rebrand from T-Mobile to Odido, marking independence from Deutsche Telekom. New brand emphasizes Dutch identity and digital-first approach. Includes sub-brands Tele2, Simpel, Ben.",
                "impact_type": "neutral",
                "severity": "high",
            },
            {
                "operator_id": None,
                "event_date": "2024-07-01",
                "category": "regulatory",
                "title": "3.5 GHz spectrum auction completes — EUR 174.4M total",
                "description": "KPN, Odido, and VodafoneZiggo each acquire 100 MHz in the 3.5 GHz band. Total raised EUR 174.4M. Licenses valid until 2040. Enables 5G SA deployment.",
                "impact_type": "neutral",
                "severity": "high",
            },
            {
                "operator_id": "vodafoneziggo_nl",
                "event_date": "2024-09-01",
                "category": "competitive",
                "title": "Stephen van Rooyen appointed VodafoneZiggo CEO",
                "description": "Ex-Sky UK CEO replaces Jeroen Hoencamp. CFO Ritchy Drost served as interim CEO May-Sep 2024. New leadership amid broadband subscriber losses.",
                "impact_type": "neutral",
                "severity": "medium",
            },
            {
                "operator_id": "kpn_nl",
                "event_date": "2025-03-01",
                "category": "investment",
                "title": "KPN fiber homepass exceeds 5.5M — majority of NL now on fiber",
                "description": "KPN + Glaspoort JV reach 5.58M fiber homepass by Q3 2025. ACM Telecom Monitor confirms majority of Dutch households using fiber for first time (Q1 2025).",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "vodafoneziggo_nl",
                "event_date": "2025-05-06",
                "category": "competitive",
                "title": "VodafoneZiggo cuts 400 jobs due to disappointing revenue",
                "description": "VodafoneZiggo announces 400 position cuts citing disappointing turnover results and broadband subscriber losses. Revenue declining -3.9% YoY by Q3 2025.",
                "impact_type": "negative",
                "severity": "high",
            },
            {
                "operator_id": "odido_nl",
                "event_date": "2026-01-13",
                "category": "competitive",
                "title": "Odido postpones EUR 1B Amsterdam IPO",
                "description": "Apax/Warburg Pincus planned EUR 1.1B IPO at ~EUR 7B valuation postponed due to muted investor response and market volatility. No firm timeline for revival.",
                "impact_type": "negative",
                "severity": "high",
            },
        ],
        "earnings_highlights": {
            "odido_nl": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "FY2024 revenue EUR 2.3B (+1.6%), EBITDA EUR 881M (+2.9%, margin 38.1%). Mobile service revenue growing above market rate driven by 5G upsell and postpaid migration.", "speaker": "CEO"},
                {"segment": "Broadband", "highlight_type": "outlook", "content": "Broadband customer base crossed 1 million in Q1 2025 via FWA and wholesale fiber. Growing fixed revenue stream diversifying mobile-centric business.", "speaker": "CFO"},
            ],
            "kpn_nl": [
                {"segment": "Fiber", "highlight_type": "guidance", "content": "FY2025 EBITDA EUR 2,636M (+5.1% YoY). Fiber homepass 5.58M by Q3 2025, targeting 85% of NL. Customer migration from copper accelerating with 85%+ take-up in fiber areas.", "speaker": "CEO"},
                {"segment": "Overall", "highlight_type": "outlook", "content": "FY2025 service revenue +2.7% YoY. FCF EUR 952M. Confident in mid-single-digit EBITDA growth through convergence, fiber ramp, and cost efficiency.", "speaker": "CFO"},
            ],
            "vodafoneziggo_nl": [
                {"segment": "Convergence", "highlight_type": "guidance", "content": "FY2024 revenue EUR 4.1B stable. FMC penetration 48% of broadband base. DOCSIS 3.1 delivering 2 Gbps to cable footprint.", "speaker": "CEO"},
                {"segment": "Broadband", "highlight_type": "explanation", "content": "Lost 115,000 broadband customers during 2024 due to competitive fiber pricing environment. Cutting 400 jobs in 2025 to manage cost base.", "speaker": "CFO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_netherlands as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
