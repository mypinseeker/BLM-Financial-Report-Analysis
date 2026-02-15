"""Seed the database with Italy telecom market data.

4-player market: TIM (incumbent, post-NetCo sale), Vodafone Italia+Fastweb (Swisscom, merging),
WindTre (CK Hutchison), Iliad Italia (disruptor since 2018).
Currency: EUR. All revenue figures in EUR millions per quarter.

Data sources:
  - Iliad Group FY 2024 results (Italy segment)
  - TIM quarterly reports 2024-2025
  - Vodafone Group quarterly reports (Italy segment pre-sale)
  - Swisscom reports (post Vodafone Italia acquisition Jan 2025)
  - CK Hutchison annual reports (WindTre)
  - AGCOM Osservatorio delle comunicazioni

Note: TIM sold NetCo to KKR (completed July 2024) — now asset-light services company.
Vodafone Italia acquired by Swisscom (completed Jan 2025) — merging with Fastweb.
Italian mobile ARPUs among lowest in Western Europe.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "italy"
OPERATORS = ["iliad_it", "tim_it", "vodafone_it", "windtre_it"]


def get_seed_data():
    return {
        "financials": {
            # Iliad Italia — disruptive challenger since May 2018
            # FY2024: Revenue EUR 1,145M (+8% YoY), EBITDAaL EUR 308M (+24.5%)
            # EBITDAaL margin 26.9% (+3.5pp). Now profitable and cash-flow positive.
            # 11.64M mobile + 349K fiber = 11.99M total subs (end-2024)
            # Quarterly split estimated from annual; Q4 typically strongest
            "iliad_it": {
                "total_revenue": [275, 280, 288, 302, 295, 305, 312, 325],
                "service_revenue": [260, 265, 273, 287, 280, 290, 297, 310],
                "service_revenue_growth_pct": [8.5, 8.2, 7.8, 7.5, 7.3, 8.9, 8.3, 7.6],
                "mobile_service_revenue": [248, 252, 258, 270, 262, 270, 275, 288],
                "mobile_service_growth_pct": [7.5, 7.0, 6.5, 6.0, 5.6, 7.1, 6.6, 6.7],
                "fixed_service_revenue": [12, 13, 15, 17, 18, 20, 22, 25],
                "fixed_service_growth_pct": [80.0, 85.0, 90.0, 95.0, 50.0, 53.8, 46.7, 47.1],
                "b2b_revenue": [5, 6, 6, 7, 8, 9, 10, 12],
                "ebitda": [68, 72, 78, 90, 82, 88, 95, 108],
                "ebitda_margin_pct": [24.7, 25.7, 27.1, 29.8, 27.8, 28.9, 30.4, 33.2],
                "ebitda_growth_pct": [22.0, 24.0, 25.0, 27.0, 20.6, 22.2, 21.8, 20.0],
                "capex": [70, 72, 73, 75, 68, 70, 72, 75],
                "capex_to_revenue_pct": [25.5, 25.7, 25.3, 24.8, 23.1, 23.0, 23.1, 23.1],
                "employees": [3200, 3200, 3300, 3300, 3400, 3400, 3500, 3500],
                "_source": "Iliad Group FY 2024 results (Italy segment); quarterly split estimated",
            },
            # TIM (Telecom Italia) — incumbent, post-NetCo sale to KKR (July 2024)
            # Pre-NetCo: TIM Group Italy FY2023 revenue ~EUR 14.4B
            # Post-NetCo (ServCo only): FY2024 ProForma revenue ~EUR 10.4B (-2% organic)
            # TIM domestic: Q3 2024 revenue EUR 3.3B; EBITDA margin ~38%
            # Post-NetCo TIM is asset-light; now pays wholesale to FiberCop
            "tim_it": {
                "total_revenue": [2650, 2620, 2600, 2530, 2580, 2560, 2540, 2500],
                "service_revenue": [2350, 2330, 2310, 2250, 2300, 2280, 2260, 2230],
                "service_revenue_growth_pct": [-2.0, -2.5, -3.0, -3.5, -1.9, -2.1, -2.2, -0.9],
                "mobile_service_revenue": [800, 790, 785, 775, 780, 775, 770, 765],
                "mobile_service_growth_pct": [-4.0, -4.5, -4.0, -3.5, -2.5, -1.9, -1.9, -1.3],
                "fixed_service_revenue": [1100, 1090, 1080, 1070, 1075, 1065, 1055, 1050],
                "fixed_service_growth_pct": [-1.0, -1.5, -2.0, -2.5, -2.3, -2.3, -2.3, -1.9],
                "b2b_revenue": [550, 555, 560, 565, 570, 575, 580, 585],
                "ebitda": [1000, 990, 985, 955, 980, 975, 968, 950],
                "ebitda_margin_pct": [37.7, 37.8, 37.9, 37.7, 38.0, 38.1, 38.1, 38.0],
                "ebitda_growth_pct": [-2.5, -3.0, -2.0, -4.0, -2.0, -1.5, -1.7, -0.5],
                "capex": [350, 340, 335, 375, 340, 330, 325, 355],
                "capex_to_revenue_pct": [13.2, 13.0, 12.9, 14.8, 13.2, 12.9, 12.8, 14.2],
                "employees": [42000, 41500, 41000, 40500, 40000, 39500, 39000, 38500],
                "_source": "TIM quarterly reports 2024-2025; post-NetCo ProForma from TIM Industrial Plan; headcount declining",
            },
            # Vodafone Italia (+ Fastweb post-Swisscom merger Jan 2025)
            # Pre-merger: Vodafone Italia FY2024 (Vodafone FY ending Mar): ~EUR 4.5B
            # Fastweb FY2024: ~EUR 2.6B
            # Post-merger (Jan 2025): combined ~EUR 7B annual run-rate
            # Q1-Q4 2024 = Vodafone Italia standalone, Q1-Q4 2025 = Vodafone Italia + Fastweb
            "vodafone_it": {
                "total_revenue": [1120, 1110, 1105, 1100, 1740, 1750, 1755, 1760],
                "service_revenue": [970, 960, 955, 950, 1540, 1550, 1555, 1560],
                "service_revenue_growth_pct": [-3.0, -3.5, -3.0, -2.5, 58.8, 61.5, 62.8, 64.2],
                "mobile_service_revenue": [580, 575, 570, 565, 585, 590, 592, 595],
                "mobile_service_growth_pct": [-4.0, -4.5, -4.0, -3.5, 0.9, 2.6, 3.9, 5.3],
                "fixed_service_revenue": [250, 248, 245, 242, 790, 795, 798, 800],
                "fixed_service_growth_pct": [0.5, 0.0, -0.5, -1.0, 216.0, 220.6, 225.7, 230.6],
                "b2b_revenue": [190, 188, 185, 183, 310, 315, 318, 320],
                "ebitda": [380, 375, 370, 365, 620, 635, 640, 650],
                "ebitda_margin_pct": [33.9, 33.8, 33.5, 33.2, 35.6, 36.3, 36.5, 36.9],
                "ebitda_growth_pct": [-4.0, -4.5, -3.5, -3.0, 63.2, 69.3, 73.0, 78.1],
                "capex": [220, 215, 218, 297, 310, 305, 308, 370],
                "capex_to_revenue_pct": [19.6, 19.4, 19.7, 27.0, 17.8, 17.4, 17.5, 21.0],
                "employees": [6000, 6000, 6000, 6000, 14500, 14500, 14300, 14300],
                "_source": "Vodafone Group FY2024 (Italy segment); Fastweb/Swisscom reports; post-merger from Jan 2025 combined",
            },
            # WindTre — CK Hutchison, Wind+Tre merged operator
            # FY2024: Revenue ~EUR 4.8B (estimated), EBITDA ~EUR 1.7B (~35% margin)
            # CK Hutchison reviewing European asset sales
            # VERY Mobile sub-brand for value segment
            "windtre_it": {
                "total_revenue": [1210, 1200, 1195, 1190, 1185, 1180, 1175, 1170],
                "service_revenue": [1080, 1070, 1065, 1060, 1058, 1052, 1048, 1042],
                "service_revenue_growth_pct": [-1.5, -2.0, -2.5, -2.0, -1.8, -1.7, -1.6, -1.5],
                "mobile_service_revenue": [760, 755, 750, 745, 740, 735, 730, 725],
                "mobile_service_growth_pct": [-2.0, -2.5, -3.0, -2.5, -2.6, -2.6, -2.7, -2.7],
                "fixed_service_revenue": [180, 178, 177, 175, 178, 180, 181, 183],
                "fixed_service_growth_pct": [1.0, 0.5, 0.0, -0.5, -1.1, 1.1, 2.3, 4.6],
                "b2b_revenue": [140, 137, 138, 140, 140, 137, 137, 134],
                "ebitda": [425, 420, 418, 437, 420, 415, 412, 430],
                "ebitda_margin_pct": [35.1, 35.0, 35.0, 36.7, 35.4, 35.2, 35.1, 36.8],
                "ebitda_growth_pct": [-1.0, -1.5, -1.5, -0.5, -1.2, -1.2, -1.4, -1.6],
                "capex": [210, 205, 208, 227, 200, 198, 200, 220],
                "capex_to_revenue_pct": [17.4, 17.1, 17.4, 19.1, 16.9, 16.8, 17.0, 18.8],
                "employees": [7500, 7500, 7400, 7400, 7300, 7300, 7200, 7200],
                "_source": "CK Hutchison annual report 2024 (Europe telecom segment); WindTre estimated from AGCOM data",
            },
        },
        "subscribers": {
            # Iliad Italia — launched May 2018, rapid growth
            # FY2024: 11.64M mobile, 349K fiber (11.99M total)
            # Leader in net adds for 7 consecutive years
            # ~14.6% mobile market share
            "iliad_it": {
                "mobile_total_k": [11000, 11150, 11350, 11640, 11750, 11900, 12050, 12200],
                "mobile_postpaid_k": [10800, 10950, 11150, 11440, 11550, 11700, 11850, 12000],
                "mobile_prepaid_k": [200, 200, 200, 200, 200, 200, 200, 200],
                "mobile_net_adds_k": [200, 150, 200, 290, 110, 150, 150, 150],
                "mobile_churn_pct": [1.8, 1.7, 1.7, 1.6, 1.6, 1.5, 1.5, 1.5],
                "mobile_arpu": [10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9],
                "broadband_total_k": [200, 240, 290, 349, 390, 440, 495, 550],
                "broadband_fiber_k": [200, 240, 290, 349, 390, 440, 495, 550],
                "broadband_net_adds_k": [30, 40, 50, 59, 41, 50, 55, 55],
                "b2b_customers_k": [15, 18, 20, 23, 26, 30, 34, 38],
                "_source": "Iliad Group FY 2024 results; Italy KPI from quarterly reports",
            },
            # TIM — incumbent, largest base, declining
            # FY2024: ~30M mobile (including M2M), ~9M fixed broadband
            # Mobile market share ~23.5%
            "tim_it": {
                "mobile_total_k": [30500, 30300, 30100, 29800, 29600, 29400, 29200, 29000],
                "mobile_postpaid_k": [20500, 20400, 20300, 20100, 20000, 19900, 19800, 19700],
                "mobile_prepaid_k": [10000, 9900, 9800, 9700, 9600, 9500, 9400, 9300],
                "mobile_net_adds_k": [-200, -200, -200, -300, -200, -200, -200, -200],
                "mobile_churn_pct": [2.0, 2.0, 2.1, 2.1, 2.0, 2.0, 2.0, 2.0],
                "mobile_arpu": [11.5, 11.4, 11.3, 11.2, 11.3, 11.4, 11.5, 11.5],
                "broadband_total_k": [9200, 9180, 9150, 9100, 9080, 9060, 9040, 9020],
                "broadband_fiber_k": [5000, 5100, 5200, 5300, 5400, 5500, 5600, 5700],
                "broadband_net_adds_k": [-20, -20, -30, -50, -20, -20, -20, -20],
                "tv_total_k": [4200, 4180, 4150, 4120, 4100, 4080, 4060, 4040],
                "b2b_customers_k": [350, 352, 354, 356, 358, 360, 362, 364],
                "_source": "TIM quarterly reports; subscriber counts estimated from market share data",
            },
            # Vodafone Italia (+ Fastweb from Jan 2025)
            # Pre-merger: ~18M mobile, ~2.8M fixed (Fastweb ~2.7M broadband)
            # Post-merger: ~18M mobile, ~5.5M fixed combined
            "vodafone_it": {
                "mobile_total_k": [18200, 18100, 18000, 17900, 17850, 17800, 17750, 17700],
                "mobile_postpaid_k": [13200, 13150, 13100, 13050, 13020, 13000, 12980, 12960],
                "mobile_prepaid_k": [5000, 4950, 4900, 4850, 4830, 4800, 4770, 4740],
                "mobile_net_adds_k": [-100, -100, -100, -100, -50, -50, -50, -50],
                "mobile_churn_pct": [2.2, 2.2, 2.3, 2.3, 2.0, 2.0, 1.9, 1.9],
                "mobile_arpu": [12.0, 11.9, 11.8, 11.7, 12.0, 12.1, 12.2, 12.3],
                "broadband_total_k": [2800, 2810, 2820, 2830, 5530, 5550, 5570, 5590],
                "broadband_fiber_k": [2200, 2250, 2300, 2350, 4800, 4850, 4900, 4950],
                "broadband_net_adds_k": [10, 10, 10, 10, 2700, 20, 20, 20],
                "tv_total_k": [500, 510, 520, 530, 540, 550, 560, 570],
                "b2b_customers_k": [120, 122, 124, 126, 230, 232, 234, 236],
                "_source": "Vodafone Group/Swisscom reports; Fastweb consolidated from Q1 2025 (+2.7M broadband)",
            },
            # WindTre — CK Hutchison, largest mobile base
            # ~24% mobile market share, declining slightly
            # VERY Mobile sub-brand ~5M+ subs
            "windtre_it": {
                "mobile_total_k": [19500, 19400, 19300, 19200, 19100, 19000, 18900, 18800],
                "mobile_postpaid_k": [13000, 12950, 12900, 12850, 12800, 12750, 12700, 12650],
                "mobile_prepaid_k": [6500, 6450, 6400, 6350, 6300, 6250, 6200, 6150],
                "mobile_net_adds_k": [-100, -100, -100, -100, -100, -100, -100, -100],
                "mobile_churn_pct": [2.5, 2.5, 2.6, 2.5, 2.4, 2.4, 2.3, 2.3],
                "mobile_arpu": [11.0, 10.9, 10.8, 10.7, 10.8, 10.8, 10.9, 10.9],
                "broadband_total_k": [1200, 1210, 1220, 1230, 1240, 1250, 1260, 1270],
                "broadband_fiber_k": [600, 620, 640, 660, 680, 700, 720, 740],
                "broadband_net_adds_k": [5, 10, 10, 10, 10, 10, 10, 10],
                "b2b_customers_k": [80, 81, 82, 83, 84, 85, 86, 87],
                "_source": "CK Hutchison reports; AGCOM market data; VERY Mobile included in totals",
            },
        },
        "macro": {
            "gdp_growth_pct": 0.7,
            "inflation_pct": 2.0,
            "unemployment_pct": 6.8,
            "telecom_market_size_eur_b": 28.5,
            "telecom_growth_pct": -0.5,
            "five_g_adoption_pct": 25.0,
            "fiber_penetration_pct": 52.0,
            "regulatory_environment": "AGCOM promoting infrastructure competition and wholesale access; 5G spectrum auction 2018 raised EUR 6.5B (highest per capita in EU, burdened operators); TIM NetCo sale to KKR (EUR 18.8B, July 2024) created FiberCop wholesale fiber platform; Vodafone Italia sold to Swisscom (Jan 2025) merged with Fastweb; CK Hutchison exploring WindTre sale; Italian government involved via CDP stake in TIM",
            "digital_strategy": "PNRR (Recovery Plan): EUR 6.7B for digital infrastructure; VHCN target 100% by 2026 (EU Digital Decade); Open Fiber deploying FTTH in white/grey areas; FiberCop targeting 76% FTTH coverage; BUL (Ultra-broadband) plan for rural areas; 5G target all urban areas by 2025",
            "source_url": "AGCOM Osservatorio 2024 / ISTAT / European Commission 2025",
        },
        "network": {
            "iliad_it": {
                "five_g_coverage_pct": 40,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 0,
                "technology_mix": {"mobile_vendor": "Nokia", "spectrum_mhz": 280, "core_vendor": "Nokia", "5g_sa_status": "NSA deploying", "own_sites": 6800, "roaming_partner": "WindTre"},
            },
            "tim_it": {
                "five_g_coverage_pct": 75,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 0,
                "technology_mix": {"mobile_vendor": "Ericsson/Nokia", "spectrum_mhz": 380, "core_vendor": "Ericsson", "notes": "Fixed network sold to FiberCop/KKR; now wholesale customer"},
            },
            "vodafone_it": {
                "five_g_coverage_pct": 55,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 2500,
                "technology_mix": {"mobile_vendor": "Ericsson", "spectrum_mhz": 300, "core_vendor": "Ericsson", "notes": "Fastweb fiber 2.5M FTTH homepass integrated post-merger"},
            },
            "windtre_it": {
                "five_g_coverage_pct": 50,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 0,
                "technology_mix": {"mobile_vendor": "ZTE/Ericsson", "spectrum_mhz": 320, "core_vendor": "ZTE", "notes": "No owned fixed; wholesale fiber via Open Fiber/FiberCop"},
            },
        },
        "executives": {
            "iliad_it": [
                {"name": "Benedetto Levi", "title": "CEO, Iliad Italia", "start_date": "2018-01-01", "background": "Led Italy launch in 2018; grew subscriber base from 0 to 11.6M in 6 years; responsible for fixed broadband expansion"},
            ],
            "tim_it": [
                {"name": "Pietro Labriola", "title": "CEO, TIM Group", "start_date": "2022-01-01", "background": "Led NetCo sale to KKR; transforming TIM from infrastructure-heavy to asset-light services company"},
                {"name": "Adrian Calaza", "title": "CFO, TIM Group", "start_date": "2022-06-01", "background": "Managing financial restructuring post-NetCo sale; debt reduction focus"},
            ],
            "vodafone_it": [
                {"name": "Aldo Bisio", "title": "CEO, Vodafone Italia", "start_date": "2014-01-01", "background": "Long-serving CEO; managing Swisscom acquisition transition and Fastweb integration"},
            ],
            "windtre_it": [
                {"name": "Jeffrey Hedberg", "title": "CEO, WindTre", "start_date": "2016-01-01", "background": "Led Wind-Tre merger integration; managing through CK Hutchison strategic review"},
            ],
        },
        "competitive_scores": {
            "iliad_it": {
                "Network Coverage": 75, "Network Quality": 72, "Brand Strength": 80,
                "Price Competitiveness": 95, "Customer Service": 75, "Digital Experience": 88,
                "Enterprise Solutions": 25, "Innovation": 85, "Distribution": 65,
            },
            "tim_it": {
                "Network Coverage": 92, "Network Quality": 88, "Brand Strength": 82,
                "Price Competitiveness": 55, "Customer Service": 70, "Digital Experience": 72,
                "Enterprise Solutions": 90, "Innovation": 70, "Distribution": 88,
            },
            "vodafone_it": {
                "Network Coverage": 88, "Network Quality": 85, "Brand Strength": 78,
                "Price Competitiveness": 60, "Customer Service": 72, "Digital Experience": 75,
                "Enterprise Solutions": 75, "Innovation": 72, "Distribution": 80,
            },
            "windtre_it": {
                "Network Coverage": 85, "Network Quality": 80, "Brand Strength": 68,
                "Price Competitiveness": 78, "Customer Service": 65, "Digital Experience": 70,
                "Enterprise Solutions": 55, "Innovation": 62, "Distribution": 82,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "tim_it",
                "event_date": "2024-07-01",
                "category": "competitive",
                "title": "TIM completes EUR 18.8B NetCo sale to KKR",
                "description": "TIM sells fixed network infrastructure (FiberCop) to KKR for EUR 18.8B. TIM becomes asset-light services company. FiberCop becomes wholesale fiber platform for all Italian operators.",
                "impact_type": "neutral",
                "severity": "high",
            },
            {
                "operator_id": "vodafone_it",
                "event_date": "2025-01-01",
                "category": "competitive",
                "title": "Swisscom completes Vodafone Italia acquisition — merges with Fastweb",
                "description": "Swisscom acquires Vodafone Italia for EUR 8B. Immediate merger with Fastweb creates Italy's #2 converged operator with 18M mobile + 5.5M fixed broadband customers.",
                "impact_type": "neutral",
                "severity": "high",
            },
            {
                "operator_id": "iliad_it",
                "event_date": "2024-06-01",
                "category": "commercial",
                "title": "Iliad Italia crosses 11M mobile subscribers",
                "description": "Iliad Italia reaches 11M+ mobile subscribers. Leader in net adds for 7th consecutive year. Fixed broadband growing with 349K fiber subscribers via wholesale.",
                "impact_type": "positive",
                "severity": "medium",
            },
            {
                "operator_id": "windtre_it",
                "event_date": "2025-03-01",
                "category": "competitive",
                "title": "CK Hutchison explores sale of European telecom assets including WindTre",
                "description": "CK Hutchison Group confirms strategic review of European telecom operations. WindTre (Italy), Three UK, Three Ireland potentially for sale. Creates market uncertainty.",
                "impact_type": "negative",
                "severity": "high",
            },
            {
                "operator_id": None,
                "event_date": "2025-01-15",
                "category": "regulatory",
                "title": "AGCOM launches review of post-NetCo wholesale fiber pricing",
                "description": "AGCOM initiates market review following TIM NetCo sale to KKR. FiberCop wholesale pricing to be regulated to ensure fair access for all operators including Iliad.",
                "impact_type": "neutral",
                "severity": "medium",
            },
        ],
        "earnings_highlights": {
            "iliad_it": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "FY2024: Revenue EUR 1,145M (+8%), EBITDAaL EUR 308M (+24.5%, margin 26.9%). Leader in net adds 7 consecutive years. 11.64M mobile subs. Mobile-first, expanding into fixed.", "speaker": "CEO"},
                {"segment": "Fixed", "highlight_type": "outlook", "content": "Fixed broadband 349K fiber subscribers at end-2024 via Open Fiber and FiberCop wholesale. Targeting 1M+ fiber subs by 2026. Iliad Box launched with Iliad Group Freebox technology.", "speaker": "CEO"},
            ],
            "tim_it": [
                {"segment": "ServCo", "highlight_type": "guidance", "content": "Post-NetCo TIM: asset-light services company. Revenue declining ~2% but EBITDA margin improving post-restructuring. TIM Enterprise (cloud, IoT, security) is key growth driver. Sparkle international wholesale.", "speaker": "CEO"},
                {"segment": "Enterprise", "highlight_type": "outlook", "content": "TIM Enterprise growing +3-4% driven by cloud (Google partnership), cybersecurity, and IoT. Government/public sector contracts. Offsetting consumer decline.", "speaker": "CEO"},
            ],
            "vodafone_it": [
                {"segment": "Group", "highlight_type": "guidance", "content": "Post-Swisscom acquisition: Vodafone Italia merged with Fastweb creating Italy's strongest converged platform. Combined revenue ~EUR 7B. Synergy target EUR 600M+ over 3-4 years.", "speaker": "CEO"},
                {"segment": "Integration", "highlight_type": "outlook", "content": "Fastweb fiber (2.5M FTTH homepass) + Vodafone mobile (18M subs). Network integration underway. Brand strategy: dual brand initially, potentially unified later.", "speaker": "CEO"},
            ],
            "windtre_it": [
                {"segment": "Group", "highlight_type": "guidance", "content": "WindTre FY2024: revenue ~EUR 4.8B, EBITDA ~EUR 1.7B. Mobile subs declining moderately. VERY Mobile sub-brand competitive in value segment. CK Hutchison strategic review ongoing.", "speaker": "CEO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_italy as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
