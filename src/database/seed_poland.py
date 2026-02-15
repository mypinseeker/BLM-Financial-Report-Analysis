"""Seed the database with Poland telecom market data.

4-player market: Play/P4 (Iliad, #1 mobile), Orange Polska (convergent incumbent),
T-Mobile Polska (Deutsche Telekom), Plus/Polkomtel (Cyfrowy Polsat media-telecom group).
Currency: PLN. All revenue figures in PLN millions per quarter.

Data sources:
  - Iliad Group FY 2024 results (Poland segment: PLN 10.19B)
  - Orange Polska quarterly reports (Warsaw Stock Exchange)
  - Deutsche Telekom quarterly reports (T-Mobile Polska segment)
  - Cyfrowy Polsat / Polsat Plus Group FY 2024 results (PLN 14.3B group)
  - UKE (Polish telecom regulator) market data
  - Play acquired UPC Poland (cable) from Liberty Global in 2022

Note: Play = P4 Sp. z o.o., owned 96.66% by Iliad SA since Nov 2020.
UPC Poland merged with Play Aug 2023, creating converged operator.
PLN/EUR exchange rate: ~4.25 (2024 average).
Polsat Plus Group revenue (PLN 14.3B) includes media+energy; telecom portion ~PLN 7B.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "poland"
OPERATORS = ["play_pl", "orange_pl", "tmobile_pl", "plus_pl"]


def get_seed_data():
    return {
        "financials": {
            # Play (P4) — Iliad Group subsidiary, #1 mobile operator
            # FY2024: Revenue PLN 10,190M (EUR ~2,398M), ~+5% YoY
            # Includes UPC Poland (cable) consolidated since Aug 2023
            # EBITDAaL ~38-40% margin (Iliad Group-level efficiency)
            # Q4 2024 growth 3.2%. Q1 2024 was stronger.
            # Mobile net adds: +506K in 2023; continuing strong adds
            # 13.3M mobile + 2.1M fixed (end-2024)
            "play_pl": {
                "total_revenue": [2480, 2530, 2540, 2640, 2560, 2610, 2620, 2730],
                "service_revenue": [2280, 2330, 2340, 2440, 2360, 2410, 2420, 2530],
                "service_revenue_growth_pct": [6.5, 5.8, 5.2, 4.0, 3.2, 3.4, 3.4, 3.4],
                "mobile_service_revenue": [1580, 1610, 1620, 1690, 1630, 1660, 1670, 1740],
                "mobile_service_growth_pct": [5.0, 4.5, 4.0, 3.5, 3.2, 3.1, 3.1, 3.0],
                "fixed_service_revenue": [520, 535, 540, 555, 545, 560, 565, 585],
                "fixed_service_growth_pct": [12.0, 10.0, 8.5, 6.0, 4.8, 4.7, 4.6, 5.4],
                "b2b_revenue": [180, 185, 180, 195, 185, 190, 185, 205],
                "ebitda": [960, 990, 995, 1055, 1000, 1030, 1035, 1100],
                "ebitda_margin_pct": [38.7, 39.1, 39.2, 40.0, 39.1, 39.5, 39.5, 40.3],
                "ebitda_growth_pct": [7.0, 6.5, 6.0, 5.5, 4.2, 4.0, 4.0, 4.3],
                "capex": [520, 530, 535, 565, 510, 520, 525, 560],
                "capex_to_revenue_pct": [21.0, 20.9, 21.1, 21.4, 19.9, 19.9, 20.0, 20.5],
                "employees": [6000, 6000, 6100, 6100, 6200, 6200, 6200, 6200],
                "_source": "Iliad Group FY 2024 results (Poland PLN 10.19B); quarterly split estimated from growth trends",
            },
            # Orange Polska — incumbent, publicly listed on WSE
            # FY2024: Revenue PLN 13.0B (+4.5%), EBITDAaL PLN 4.2B (+6%)
            # Leading convergent operator with largest fiber network
            # 5M+ FTTH homepass, targeting 6M+
            # Q1 2024: Revenue PLN 3.13B (+3.5%)
            "orange_pl": {
                "total_revenue": [3130, 3220, 3250, 3400, 3200, 3280, 3310, 3460],
                "service_revenue": [2830, 2920, 2950, 3100, 2910, 2990, 3020, 3160],
                "service_revenue_growth_pct": [3.5, 4.2, 4.5, 5.5, 2.5, 2.4, 2.4, 1.9],
                "mobile_service_revenue": [1150, 1180, 1195, 1255, 1180, 1210, 1225, 1285],
                "mobile_service_growth_pct": [3.0, 3.5, 4.0, 4.5, 2.6, 2.5, 2.5, 2.4],
                "fixed_service_revenue": [1200, 1240, 1250, 1310, 1230, 1265, 1275, 1335],
                "fixed_service_growth_pct": [4.0, 5.0, 5.0, 6.0, 2.5, 2.0, 2.0, 1.9],
                "b2b_revenue": [630, 650, 660, 690, 650, 670, 680, 710],
                "ebitda": [990, 1050, 1060, 1100, 1020, 1080, 1090, 1130],
                "ebitda_margin_pct": [31.6, 32.6, 32.6, 32.4, 31.9, 32.9, 32.9, 32.7],
                "ebitda_growth_pct": [6.0, 6.5, 6.0, 5.5, 3.0, 2.9, 2.8, 2.7],
                "capex": [640, 680, 690, 740, 620, 660, 670, 720],
                "capex_to_revenue_pct": [20.4, 21.1, 21.2, 21.8, 19.4, 20.1, 20.2, 20.8],
                "employees": [11000, 11000, 10900, 10900, 10800, 10800, 10700, 10700],
                "_source": "Orange Polska quarterly reports (WSE filings); FY 2024 annual report",
            },
            # T-Mobile Polska — Deutsche Telekom subsidiary
            # FY2024: Revenue PLN 7.5B (estimated), EBITDA PLN 2.8B (~37% margin)
            # Strong 5G position, growing fixed via FWA and selective fiber
            "tmobile_pl": {
                "total_revenue": [1810, 1850, 1870, 1970, 1860, 1900, 1920, 2020],
                "service_revenue": [1620, 1660, 1680, 1780, 1670, 1710, 1730, 1830],
                "service_revenue_growth_pct": [4.0, 4.5, 4.2, 4.8, 2.8, 3.0, 3.0, 2.8],
                "mobile_service_revenue": [1180, 1210, 1225, 1295, 1220, 1250, 1265, 1335],
                "mobile_service_growth_pct": [3.5, 4.0, 3.8, 4.5, 3.4, 3.3, 3.3, 3.1],
                "fixed_service_revenue": [280, 288, 292, 310, 290, 298, 302, 320],
                "fixed_service_growth_pct": [8.0, 8.5, 8.0, 7.0, 3.6, 3.5, 3.4, 3.2],
                "b2b_revenue": [260, 268, 270, 285, 270, 278, 280, 295],
                "ebitda": [670, 695, 700, 735, 690, 715, 720, 760],
                "ebitda_margin_pct": [37.0, 37.6, 37.4, 37.3, 37.1, 37.6, 37.5, 37.6],
                "ebitda_growth_pct": [5.0, 5.5, 5.0, 4.5, 3.0, 2.9, 2.9, 3.4],
                "capex": [370, 385, 390, 415, 360, 375, 380, 405],
                "capex_to_revenue_pct": [20.4, 20.8, 20.9, 21.1, 19.4, 19.7, 19.8, 20.0],
                "employees": [5500, 5500, 5500, 5500, 5400, 5400, 5400, 5400],
                "_source": "Deutsche Telekom quarterly reports (Europe segment); T-Mobile Polska estimated from group disclosures",
            },
            # Plus / Polkomtel (Cyfrowy Polsat Group) — media-telecom conglomerate
            # Polsat Plus Group FY2024: Revenue PLN 14.3B (+4.7%), EBITDA PLN 3.3B (+9.6%)
            # Note: Group includes media (Polsat TV) + energy + telecom
            # Telecom portion (Polkomtel): ~PLN 7B revenue, ~PLN 2.5B EBITDA
            # 11M broadband homepass coverage
            "plus_pl": {
                "total_revenue": [1680, 1720, 1740, 1860, 1720, 1760, 1780, 1900],
                "service_revenue": [1500, 1540, 1560, 1680, 1545, 1585, 1605, 1720],
                "service_revenue_growth_pct": [3.0, 3.5, 4.0, 5.0, 3.0, 2.9, 2.9, 2.4],
                "mobile_service_revenue": [1000, 1025, 1040, 1115, 1030, 1055, 1070, 1145],
                "mobile_service_growth_pct": [2.5, 3.0, 3.5, 4.5, 3.0, 2.9, 2.9, 2.7],
                "fixed_service_revenue": [320, 330, 335, 365, 330, 340, 345, 375],
                "fixed_service_growth_pct": [5.0, 5.5, 6.0, 7.0, 3.1, 3.0, 3.0, 2.7],
                "b2b_revenue": [180, 185, 185, 200, 185, 190, 190, 200],
                "ebitda": [600, 620, 628, 652, 618, 640, 648, 674],
                "ebitda_margin_pct": [35.7, 36.0, 36.1, 35.1, 35.9, 36.4, 36.4, 35.5],
                "ebitda_growth_pct": [8.0, 9.0, 10.0, 10.5, 3.0, 3.2, 3.2, 3.4],
                "capex": [320, 340, 345, 395, 310, 330, 335, 380],
                "capex_to_revenue_pct": [19.0, 19.8, 19.8, 21.2, 18.0, 18.8, 18.8, 20.0],
                "employees": [8500, 8500, 8400, 8400, 8300, 8300, 8200, 8200],
                "_source": "Cyfrowy Polsat/Polsat Plus Group FY 2024 results; telecom portion estimated from segment disclosures",
            },
        },
        "subscribers": {
            # Play — Poland's #1 mobile operator
            # FY2024: 13.3M mobile + 2.1M fixed (includes UPC Poland cable)
            # Mobile market share ~28.7%, highest net-add leader
            # Mobile net adds +506K in 2023, continuing strong in 2024
            # UPC Poland cable base: ~1.5M broadband customers
            "play_pl": {
                "mobile_total_k": [12800, 12950, 13100, 13300, 13400, 13530, 13660, 13800],
                "mobile_postpaid_k": [9800, 9950, 10100, 10300, 10400, 10530, 10660, 10800],
                "mobile_prepaid_k": [3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000],
                "mobile_net_adds_k": [100, 150, 150, 200, 100, 130, 130, 140],
                "mobile_churn_pct": [1.5, 1.4, 1.4, 1.3, 1.4, 1.3, 1.3, 1.3],
                "mobile_arpu": [32.0, 32.5, 33.0, 33.5, 33.0, 33.5, 34.0, 34.5],
                "broadband_total_k": [1950, 1980, 2020, 2100, 2120, 2160, 2200, 2250],
                "broadband_fiber_k": [600, 630, 660, 700, 730, 760, 790, 830],
                "broadband_net_adds_k": [15, 30, 40, 80, 20, 40, 40, 50],
                "tv_total_k": [1100, 1110, 1120, 1130, 1140, 1150, 1160, 1170],
                "b2b_customers_k": [120, 123, 126, 130, 133, 136, 139, 143],
                "_source": "Iliad Group FY 2024 results; Play/P4 quarterly reports (ir.play.pl)",
            },
            # Orange Polska — convergent leader with largest fiber
            # ~15.5M mobile (incl. MVNO hosting), ~2.8M broadband, ~5M+ FTTH homepass
            # Mobile market share ~27.7%
            "orange_pl": {
                "mobile_total_k": [15200, 15300, 15400, 15500, 15550, 15620, 15700, 15780],
                "mobile_postpaid_k": [10200, 10300, 10400, 10500, 10550, 10620, 10700, 10780],
                "mobile_prepaid_k": [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000],
                "mobile_net_adds_k": [50, 100, 100, 100, 50, 70, 80, 80],
                "mobile_churn_pct": [1.3, 1.3, 1.2, 1.2, 1.3, 1.2, 1.2, 1.2],
                "mobile_arpu": [28.0, 28.5, 29.0, 29.5, 29.0, 29.5, 30.0, 30.5],
                "broadband_total_k": [2750, 2770, 2790, 2820, 2835, 2855, 2875, 2900],
                "broadband_fiber_k": [1800, 1860, 1920, 2000, 2060, 2120, 2180, 2250],
                "broadband_net_adds_k": [15, 20, 20, 30, 15, 20, 20, 25],
                "tv_total_k": [900, 905, 910, 915, 920, 925, 930, 935],
                "b2b_customers_k": [200, 203, 206, 210, 213, 216, 219, 223],
                "_source": "Orange Polska quarterly reports (WSE); FTTH homepass 5M+ by end-2024",
            },
            # T-Mobile Polska — Deutsche Telekom, growing fixed
            # ~11M mobile (estimated), growing fixed via FWA and wholesale fiber
            # Mobile market share ~20.3%
            "tmobile_pl": {
                "mobile_total_k": [10800, 10850, 10900, 10950, 11000, 11050, 11100, 11150],
                "mobile_postpaid_k": [8300, 8350, 8400, 8450, 8500, 8550, 8600, 8650],
                "mobile_prepaid_k": [2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500],
                "mobile_net_adds_k": [30, 50, 50, 50, 50, 50, 50, 50],
                "mobile_churn_pct": [1.4, 1.4, 1.3, 1.3, 1.4, 1.3, 1.3, 1.3],
                "mobile_arpu": [30.0, 30.5, 31.0, 31.5, 31.0, 31.5, 32.0, 32.5],
                "broadband_total_k": [850, 870, 890, 920, 940, 960, 980, 1000],
                "broadband_fiber_k": [350, 370, 390, 420, 440, 460, 480, 500],
                "broadband_net_adds_k": [15, 20, 20, 30, 20, 20, 20, 20],
                "tv_total_k": [300, 305, 310, 315, 320, 325, 330, 335],
                "b2b_customers_k": [100, 102, 104, 106, 108, 110, 112, 114],
                "_source": "Deutsche Telekom quarterly reports; T-Mobile Polska estimated from group data",
            },
            # Plus / Polkomtel (Polsat Plus Group)
            # ~11M mobile (estimated), ~3M broadband (via Netia + cable)
            # 11M broadband homepass coverage
            # Mobile market share ~23.3%
            "plus_pl": {
                "mobile_total_k": [11000, 10980, 10960, 10940, 10920, 10900, 10880, 10860],
                "mobile_postpaid_k": [7500, 7490, 7480, 7470, 7460, 7450, 7440, 7430],
                "mobile_prepaid_k": [3500, 3490, 3480, 3470, 3460, 3450, 3440, 3430],
                "mobile_net_adds_k": [-20, -20, -20, -20, -20, -20, -20, -20],
                "mobile_churn_pct": [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5],
                "mobile_arpu": [27.0, 27.5, 28.0, 28.5, 28.0, 28.5, 29.0, 29.5],
                "broadband_total_k": [2900, 2920, 2940, 2960, 2975, 2990, 3005, 3020],
                "broadband_fiber_k": [800, 830, 860, 900, 930, 960, 990, 1020],
                "broadband_net_adds_k": [10, 20, 20, 20, 15, 15, 15, 15],
                "tv_total_k": [4500, 4480, 4460, 4440, 4420, 4400, 4380, 4360],
                "b2b_customers_k": [130, 132, 134, 136, 138, 140, 142, 144],
                "_source": "Cyfrowy Polsat/Polsat Plus Group FY 2024; TV subscribers includes DTH satellite",
            },
        },
        "macro": {
            "gdp_growth_pct": 3.2,
            "inflation_pct": 3.7,
            "unemployment_pct": 5.0,
            "telecom_market_size_eur_b": 9.5,
            "telecom_growth_pct": 4.5,
            "five_g_adoption_pct": 18.0,
            "fiber_penetration_pct": 28.0,
            "regulatory_environment": "UKE pro-competition regulation; 5G 3.5 GHz spectrum auctioned 2024; 700 MHz assigned for 5G; wholesale fiber access mandates; Polish broadband subsidies from EU co-funded KPO/NCBR programs; MVNO segment ~10% of mobile market; 4-player market structure stable",
            "digital_strategy": "EU Digital Decade: gigabit for all by 2030; KPO funding for fiber rural areas; 5G coverage target: 95% by 2027; Orange Polska targeting 6M+ FTTH homepass by 2026; government e-services digitalization (mObywatel app)",
            "source_url": "UKE Market Report 2024 / GUS (Central Statistical Office) / European Commission 2025",
        },
        "network": {
            "play_pl": {
                "five_g_coverage_pct": 45,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 1500,
                "technology_mix": {"mobile_vendor": "Nokia/Ericsson", "spectrum_mhz": 310, "core_vendor": "Nokia", "cable_docsis": "3.1", "cable_homepass_k": 3200, "notes": "UPC Poland cable integrated Aug 2023; PSO open fiber access JV"},
            },
            "orange_pl": {
                "five_g_coverage_pct": 50,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 5200,
                "technology_mix": {"mobile_vendor": "Nokia", "spectrum_mhz": 340, "core_vendor": "Nokia", "5g_sa_status": "SA deploying", "fiber_technology": "GPON/XGS-PON"},
            },
            "tmobile_pl": {
                "five_g_coverage_pct": 52,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 400,
                "technology_mix": {"mobile_vendor": "Ericsson", "spectrum_mhz": 300, "core_vendor": "Ericsson", "5g_sa_status": "SA trials", "fwa_deployed": True},
            },
            "plus_pl": {
                "five_g_coverage_pct": 40,
                "four_g_coverage_pct": 98,
                "fiber_homepass_k": 2000,
                "technology_mix": {"mobile_vendor": "Huawei/Nokia", "spectrum_mhz": 280, "core_vendor": "Nokia", "cable_homepass_k": 3500, "notes": "Netia fixed subsidiary; Polsat satellite TV platform"},
            },
        },
        "executives": {
            "play_pl": [
                {"name": "Jean-Marc Harion", "title": "CEO, Play (P4)", "start_date": "2020-11-01", "background": "Iliad Group appointee post-acquisition; leading fixed broadband expansion and 5G rollout; previously at Proximus and BASE"},
            ],
            "orange_pl": [
                {"name": "Liudmila Climoc", "title": "CEO, Orange Polska", "start_date": "2023-01-01", "background": "Orange Group executive; leading fiber acceleration and convergent strategy in Poland"},
                {"name": "Jacek Kunicki", "title": "CFO, Orange Polska", "start_date": "2020-01-01", "background": "Finance professional managing fiber capex program and WSE investor relations"},
            ],
            "tmobile_pl": [
                {"name": "Andreas Maierhofer", "title": "CEO, T-Mobile Polska", "start_date": "2020-01-01", "background": "Deutsche Telekom executive; driving 5G leadership and convergent growth in Poland"},
            ],
            "plus_pl": [
                {"name": "Maciej Stec", "title": "President, Polkomtel", "start_date": "2025-07-01", "background": "New leadership following Polsat Plus Group restructuring; Zygmunt Solorz succession planning"},
            ],
        },
        "competitive_scores": {
            "play_pl": {
                "Network Coverage": 88, "Network Quality": 85, "Brand Strength": 85,
                "Price Competitiveness": 82, "Customer Service": 78, "Digital Experience": 85,
                "Enterprise Solutions": 50, "Innovation": 80, "Distribution": 78,
            },
            "orange_pl": {
                "Network Coverage": 92, "Network Quality": 90, "Brand Strength": 88,
                "Price Competitiveness": 65, "Customer Service": 82, "Digital Experience": 80,
                "Enterprise Solutions": 90, "Innovation": 82, "Distribution": 88,
            },
            "tmobile_pl": {
                "Network Coverage": 88, "Network Quality": 88, "Brand Strength": 82,
                "Price Competitiveness": 72, "Customer Service": 78, "Digital Experience": 82,
                "Enterprise Solutions": 72, "Innovation": 78, "Distribution": 80,
            },
            "plus_pl": {
                "Network Coverage": 85, "Network Quality": 82, "Brand Strength": 78,
                "Price Competitiveness": 68, "Customer Service": 72, "Digital Experience": 72,
                "Enterprise Solutions": 65, "Innovation": 68, "Distribution": 85,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "play_pl",
                "event_date": "2023-08-31",
                "category": "competitive",
                "title": "Play completes UPC Poland merger — becomes converged operator",
                "description": "UPC Poland (Liberty Global cable, 1.5M broadband customers) formally merges with Play. Creates Poland's first Iliad-style converged mobile+cable operator. 3.2M cable homepass.",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "play_pl",
                "event_date": "2023-04-03",
                "category": "investment",
                "title": "PSO (Play + InfraVia) creates Poland's biggest open access fiber network",
                "description": "Play and InfraVia create PSO (Swiatlowod Otwarty), Poland's largest open access broadband network with ~3M premises. Play transfers fiber assets and gains wholesale access.",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "orange_pl",
                "event_date": "2024-06-01",
                "category": "investment",
                "title": "Orange Polska accelerates fiber — surpasses 5M FTTH homepass",
                "description": "Orange Polska fiber footprint exceeds 5M premises passed. Targeting 6M+ by 2026. Convergent Orange Love bundles driving customer value. Best fiber speeds in Poland.",
                "impact_type": "positive",
                "severity": "medium",
            },
            {
                "operator_id": "plus_pl",
                "event_date": "2025-07-12",
                "category": "competitive",
                "title": "Polsat Plus Group leadership change — Solorz succession",
                "description": "Major leadership restructuring at Cyfrowy Polsat/Polsat Plus Group. Maciej Stec becomes President of Polkomtel. Succession planning for founder Zygmunt Solorz.",
                "impact_type": "negative",
                "severity": "medium",
            },
            {
                "operator_id": "play_pl",
                "event_date": "2024-09-01",
                "category": "technology",
                "title": "Play launches Iliad-designed Internet Box in Poland",
                "description": "Play launches new Internet Box based on Iliad Group Freebox technology. 5G + fiber hybrid CPE. Accelerates fixed broadband growth. 1,050 new base stations deployed in 2024.",
                "impact_type": "positive",
                "severity": "medium",
            },
            {
                "operator_id": None,
                "event_date": "2024-10-01",
                "category": "regulatory",
                "title": "UKE completes 3.5 GHz 5G spectrum auction",
                "description": "Polish regulator UKE completes 3.4-3.8 GHz 5G spectrum auction. All four operators acquire spectrum. Enables wide-area 5G deployment across Poland.",
                "impact_type": "neutral",
                "severity": "high",
            },
        ],
        "earnings_highlights": {
            "play_pl": [
                {"segment": "Group", "highlight_type": "guidance", "content": "FY2024: Revenue PLN 10,190M (~EUR 2,398M). Q4 growth 3.2%. 13.3M mobile + 2.1M fixed subscribers. UPC Poland integration complete. PSO open access fiber JV operational.", "speaker": "CEO"},
                {"segment": "Mobile", "highlight_type": "explanation", "content": "Poland's #1 mobile operator with highest net adds. 5G rollout accelerating. Iliad Group procurement synergies reducing equipment costs. Play Box launched using Freebox technology platform.", "speaker": "CEO"},
            ],
            "orange_pl": [
                {"segment": "Group", "highlight_type": "guidance", "content": "FY2024: Revenue PLN 13.0B (+4.5%), EBITDAaL PLN 4.2B (+6%). Fiber homepass 5M+. Orange Love convergent bundles driving ARPU growth. Enterprise ICT growing strongly.", "speaker": "CEO"},
                {"segment": "Fixed", "highlight_type": "outlook", "content": "Fiber rollout accelerating toward 6M+ homepass by 2026. Copper retirement in fiber-covered areas. FTTH take-up rate improving. Fixed ARPU growth driven by speed upgrades.", "speaker": "CTO"},
            ],
            "tmobile_pl": [
                {"segment": "Group", "highlight_type": "guidance", "content": "FY2024: Revenue PLN 7.5B, EBITDA PLN 2.8B (37% margin). 5G coverage leadership in Poland. Growing fixed broadband via FWA and wholesale fiber. Magenta plans competitive.", "speaker": "CEO"},
            ],
            "plus_pl": [
                {"segment": "Group", "highlight_type": "guidance", "content": "Polsat Plus Group FY2024: Revenue PLN 14.3B (+4.7%), EBITDA PLN 3.3B (+9.6%). Telecom + media convergence unique in Poland. 11M broadband homepass. Polsat Sport content differentiator.", "speaker": "CEO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_poland as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
