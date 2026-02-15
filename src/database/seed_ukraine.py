"""Seed the database with Ukraine telecom market data.

3-player mobile market: Kyivstar (#1, VEON), Vodafone Ukraine (#2, NEQSOL), lifecell (#3, NJJ/DVL Group).
Currency: UAH. All revenue figures in UAH billions per quarter.
Note: Active wartime market since Feb 2022. All data in context of conflict conditions.

Data sources:
  - lifecell FY2023 results (TAdviser, ITC.ua); FY2024 estimated
  - Kyivstar FY2024 (VEON/Interfax); Kyivstar NASDAQ listing Q1 2025
  - Vodafone Ukraine FY2024 (Interfax)
  - NCEC (regulator) spectrum auction Nov 2024
  - World Bank Ukraine GDP data / IMF
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "ukraine"
OPERATORS = ["lifecell_ua", "kyivstar_ua", "vodafone_ua"]


def get_seed_data():
    return {
        "financials": {
            # lifecell (DVL Group / NJJ) — Target operator
            # FY2023: Revenue UAH 11.7B (+24.4%), EBITDA UAH 6.81B, profit UAH 2.57B
            # FY2024: Estimated ~UAH 14.0B based on ~20% growth trajectory
            # NJJ acquired Sep 2024 for $524M; merging with Datagroup-Volia
            # Note: Revenue in UAH billions; arrays store UAH millions for consistency
            "lifecell_ua": {
                "total_revenue": [2600, 2750, 2900, 3050, 3200, 3400, 3600, 3800],
                "service_revenue": [2500, 2650, 2800, 2950, 3100, 3300, 3500, 3700],
                "service_revenue_growth_pct": [20.0, 22.0, 24.0, 25.0, 23.1, 23.6, 24.1, 24.6],
                "mobile_service_revenue": [2200, 2330, 2460, 2590, 2700, 2870, 3040, 3210],
                "mobile_service_growth_pct": [18.0, 20.0, 22.0, 24.0, 22.7, 23.2, 23.6, 23.9],
                "fixed_service_revenue": [200, 220, 240, 260, 300, 330, 360, 390],
                "fixed_service_growth_pct": [40.0, 42.0, 44.0, 46.0, 50.0, 50.0, 50.0, 50.0],
                "b2b_revenue": [100, 100, 100, 100, 100, 100, 100, 100],
                "ebitda": [1520, 1610, 1700, 1790, 1850, 1960, 2070, 2120],
                "ebitda_margin_pct": [58.5, 58.5, 58.6, 58.7, 57.8, 57.6, 57.5, 55.8],
                "ebitda_growth_pct": [20.0, 22.0, 24.0, 25.0, 21.7, 21.7, 21.8, 18.4],
                "capex": [420, 450, 480, 510, 600, 650, 700, 750],
                "capex_to_revenue_pct": [16.2, 16.4, 16.6, 16.7, 18.8, 19.1, 19.4, 19.7],
                "employees": [1400, 1420, 1440, 1500, 4800, 4900, 5000, 5100],
                "_source": "lifecell FY2023 (ITC.ua/TAdviser); FY2024 estimated; Q3-Q4 2024 incl Datagroup-Volia post-acquisition",
            },
            # Kyivstar — VEON subsidiary, Ukraine's largest operator
            # FY2024: Revenue UAH 37.27B (+11%), EBITDA ~UAH 21.4B, margin 56.1%
            # Capex UAH 10.22B (+60.7%); post-cyberattack rebuild
            # ~24M mobile subs, 1.1M broadband
            "kyivstar_ua": {
                "total_revenue": [7800, 8600, 9200, 9600, 8700, 9200, 9600, 9770],
                "service_revenue": [7500, 8300, 8900, 9300, 8400, 8900, 9300, 9470],
                "service_revenue_growth_pct": [15.0, 18.0, 20.0, 22.0, -14.1, 7.0, 10.9, 11.8],
                "mobile_service_revenue": [6800, 7500, 8050, 8400, 7600, 8050, 8400, 8570],
                "mobile_service_growth_pct": [14.0, 17.0, 19.0, 21.0, -15.0, 7.3, 11.2, 12.0],
                "fixed_service_revenue": [500, 560, 620, 680, 600, 650, 700, 700],
                "fixed_service_growth_pct": [25.0, 28.0, 30.0, 32.0, 20.0, 16.1, 12.9, 2.9],
                "b2b_revenue": [200, 240, 230, 220, 200, 200, 200, 200],
                "ebitda": [4800, 5200, 5500, 5700, 4800, 5200, 5500, 5900],
                "ebitda_margin_pct": [61.5, 60.5, 59.8, 59.4, 55.2, 56.5, 57.3, 60.4],
                "ebitda_growth_pct": [18.0, 20.0, 22.0, 24.0, -20.0, 0.0, 0.0, 3.5],
                "capex": [1500, 1600, 1700, 1800, 2300, 2500, 2700, 2720],
                "capex_to_revenue_pct": [19.2, 18.6, 18.5, 18.8, 26.4, 27.2, 28.1, 27.8],
                "employees": [4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000],
                "_source": "VEON/Kyivstar FY2024 (Interfax); Q1 2024 down 14.1% due to cyberattack loyalty measures",
            },
            # Vodafone Ukraine — NEQSOL Holding (Azerbaijan)
            # FY2024: Revenue UAH 24.44B, service revenue +12.9%
            # OIBDA UAH 12.22B (-3.6%), margin ~50%
            # 15.8M mobile subs; growing GPON fiber (100K+ subs)
            "vodafone_ua": {
                "total_revenue": [5200, 5500, 5700, 5800, 5800, 6100, 6200, 6340],
                "service_revenue": [4900, 5200, 5400, 5500, 5500, 5800, 5900, 6040],
                "service_revenue_growth_pct": [10.0, 12.0, 13.0, 14.0, 12.2, 11.5, 9.3, 9.8],
                "mobile_service_revenue": [4300, 4550, 4720, 4810, 4500, 4740, 4830, 4900],
                "mobile_service_growth_pct": [9.0, 11.0, 12.0, 13.0, 4.7, 4.2, 2.3, 1.9],
                "fixed_service_revenue": [180, 200, 210, 220, 230, 250, 270, 290],
                "fixed_service_growth_pct": [30.0, 35.0, 38.0, 40.0, 27.8, 25.0, 28.6, 31.8],
                "b2b_revenue": [420, 450, 470, 470, 470, 510, 500, 550],
                "ebitda": [3050, 3200, 3300, 3350, 3000, 3100, 3050, 3070],
                "ebitda_margin_pct": [58.7, 58.2, 57.9, 57.8, 51.7, 50.8, 49.2, 48.4],
                "ebitda_growth_pct": [15.0, 14.0, 13.0, 12.0, -1.6, -3.1, -7.6, -8.4],
                "capex": [1200, 1300, 1350, 1400, 1450, 1500, 1550, 1600],
                "capex_to_revenue_pct": [23.1, 23.6, 23.7, 24.1, 25.0, 24.6, 25.0, 25.2],
                "employees": [4400, 4400, 4500, 4500, 4500, 4500, 4500, 4500],
                "_source": "Vodafone Ukraine FY2024 (Interfax); OIBDA UAH 12.22B; GPON 100K+ subs",
            },
        },
        "subscribers": {
            "lifecell_ua": {
                "mobile_total_k": [9500, 9600, 9700, 9900, 9900, 9950, 10000, 10000],
                "mobile_postpaid_k": [2500, 2550, 2600, 2650, 2700, 2750, 2800, 2850],
                "mobile_prepaid_k": [7000, 7050, 7100, 7250, 7200, 7200, 7200, 7150],
                "mobile_net_adds_k": [50, 100, 100, 200, 0, 50, 50, 0],
                "mobile_churn_pct": [2.5, 2.4, 2.3, 2.2, 2.2, 2.1, 2.1, 2.0],
                "mobile_arpu": [98, 102, 106, 111, 115, 120, 125, 130],
                "broadband_total_k": [3800, 3850, 3900, 3950, 3950, 3960, 3970, 4000],
                "broadband_fiber_k": [1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850],
                "broadband_net_adds_k": [20, 50, 50, 50, 0, 10, 10, 30],
                "tv_total_k": [1200, 1210, 1220, 1230, 1230, 1235, 1240, 1250],
                "b2b_customers_k": [50, 51, 52, 53, 80, 82, 84, 86],
                "_source": "lifecell FY2023: 9.9M mobile; Datagroup-Volia ~4M HH broadband; B2B jumps post-acquisition",
            },
            "kyivstar_ua": {
                "mobile_total_k": [23500, 23700, 23900, 24000, 24000, 24100, 24200, 24300],
                "mobile_postpaid_k": [6000, 6100, 6200, 6300, 6400, 6500, 6600, 6700],
                "mobile_prepaid_k": [17500, 17600, 17700, 17700, 17600, 17600, 17600, 17600],
                "mobile_net_adds_k": [100, 200, 200, 100, 0, 100, 100, 100],
                "mobile_churn_pct": [2.0, 1.8, 1.7, 1.7, 2.5, 2.0, 1.8, 1.7],
                "mobile_arpu": [105, 110, 115, 120, 118, 123, 130, 136],
                "broadband_total_k": [900, 930, 960, 1000, 1020, 1050, 1080, 1100],
                "broadband_fiber_k": [400, 430, 460, 500, 530, 560, 590, 620],
                "broadband_net_adds_k": [20, 30, 30, 40, 20, 30, 30, 20],
                "tv_total_k": [0, 0, 0, 0, 0, 0, 0, 0],
                "b2b_customers_k": [100, 102, 104, 106, 108, 110, 112, 114],
                "_source": "Kyivstar FY2024 (VEON); ~24M mobile, 1.1M broadband; Q4 2024 ARPU UAH 136",
            },
            "vodafone_ua": {
                "mobile_total_k": [15700, 15750, 15800, 15900, 15900, 15850, 15800, 15800],
                "mobile_postpaid_k": [4200, 4250, 4300, 4350, 4400, 4450, 4500, 4550],
                "mobile_prepaid_k": [11500, 11500, 11500, 11550, 11500, 11400, 11300, 11250],
                "mobile_net_adds_k": [30, 50, 50, 100, 0, -50, -50, 0],
                "mobile_churn_pct": [2.2, 2.1, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
                "mobile_arpu": [100, 104, 108, 112, 114, 117, 120, 118],
                "broadband_total_k": [30, 40, 50, 60, 70, 80, 90, 100],
                "broadband_fiber_k": [30, 40, 50, 60, 70, 80, 90, 100],
                "broadband_net_adds_k": [5, 10, 10, 10, 10, 10, 10, 10],
                "tv_total_k": [0, 0, 0, 0, 0, 0, 0, 0],
                "b2b_customers_k": [60, 62, 64, 66, 68, 70, 72, 74],
                "_source": "Vodafone Ukraine FY2024; 15.8M mobile (-0.7%); GPON 100K+ subs; ARPU UAH 118.4",
            },
        },
        "macro": {
            "gdp_growth_pct": 5.3,
            "inflation_pct": 12.0,
            "unemployment_pct": 15.0,
            "telecom_market_size_eur_b": 1.8,
            "telecom_growth_pct": 12.0,
            "five_g_adoption_pct": 0.0,
            "fiber_penetration_pct": 50.0,
            "regulatory_environment": "NCEC regulation. Active armed conflict since Feb 2022. Martial law. EU candidate status (Jun 2022). 5G spectrum allocated Nov 2024 but commercial launch pending military clearance. Spectrum auction raised UAH 2.895B.",
            "digital_strategy": "Recovery and resilience focus. Population ~37M in government-controlled territory (pre-war 44M). GDP $190.7B (2024). UAH/USD avg 40.18 (2024). International aid supporting economic stability. Diia digital government platform.",
            "source_url": "World Bank / IMF / NCEC / CES",
        },
        "network": {
            "lifecell_ua": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 85,
                "fiber_homepass_k": 4000,
                "technology_mix": {"mobile_vendor": "Mixed", "spectrum_mhz": 110, "fixed_network": "Datagroup-Volia fiber/cable ~4M HH", "base_stations_on_fiber": 350},
            },
            "kyivstar_ua": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 96,
                "fiber_homepass_k": 2000,
                "technology_mix": {"mobile_vendor": "Ericsson", "spectrum_mhz": 202, "base_stations": 66000, "own_fiber_km": 44000},
            },
            "vodafone_ua": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 90,
                "fiber_homepass_k": 1300,
                "technology_mix": {"mobile_vendor": "Huawei/Ericsson", "spectrum_mhz": 145, "gpon_homepass_k": 1300, "sites_destroyed_pct": 10},
            },
        },
        "executives": {
            "lifecell_ua": [
                {"name": "Mykhailo Shelemba", "title": "CEO (DVL Group)", "start_date": "2024-09-01", "background": "CEO of merged DVL Group; previously CEO of Datagroup; 5% shareholder in NJJ acquisition"},
            ],
            "kyivstar_ua": [
                {"name": "Oleksandr Komarov", "title": "CEO", "start_date": "2023-01-01", "background": "VEON appointee; managing post-cyberattack recovery and NASDAQ listing process"},
            ],
            "vodafone_ua": [
                {"name": "Olga Ustinova", "title": "CEO", "start_date": "2022-01-01", "background": "NEQSOL Holding appointee; managing wartime operations and GPON fiber expansion"},
            ],
        },
        "competitive_scores": {
            "lifecell_ua": {
                "Network Coverage": 65, "Network Quality": 68, "Brand Strength": 55,
                "Price Competitiveness": 82, "Customer Service": 65, "Digital Experience": 70,
                "Enterprise Solutions": 75, "Innovation": 78, "Distribution": 60,
            },
            "kyivstar_ua": {
                "Network Coverage": 95, "Network Quality": 85, "Brand Strength": 90,
                "Price Competitiveness": 65, "Customer Service": 80, "Digital Experience": 82,
                "Enterprise Solutions": 85, "Innovation": 80, "Distribution": 92,
            },
            "vodafone_ua": {
                "Network Coverage": 82, "Network Quality": 78, "Brand Strength": 80,
                "Price Competitiveness": 72, "Customer Service": 72, "Digital Experience": 75,
                "Enterprise Solutions": 70, "Innovation": 72, "Distribution": 78,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "lifecell_ua",
                "event_date": "2024-09-10",
                "category": "investment",
                "title": "NJJ Holding completes $524M acquisition of lifecell + Datagroup-Volia",
                "description": "Xavier Niel's NJJ Holding (85%), Horizon Capital (10%), and Mykhailo Shelemba (5%) completed acquisition of lifecell mobile + Datagroup-Volia fixed broadband. Largest FDI in Ukraine since full-scale Russian invasion. Creates converged operator with 10M mobile + 4M broadband HH.",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "lifecell_ua",
                "event_date": "2024-10-15",
                "category": "investment",
                "title": "EBRD/IFC $435M financing for DVL Group network modernization",
                "description": "IFC $217.5M + EBRD $217.5M loan package for network modernization. Plans: 10,000+ km fiber, 1,000+ new 4G/5G base stations, tower upgrades, cybersecurity. 350 base stations already connected to Datagroup fiber backbone.",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "kyivstar_ua",
                "event_date": "2023-12-12",
                "category": "competitive",
                "title": "Kyivstar suffers largest telecom cyberattack in European history",
                "description": "Russia-linked attack destroyed Kyivstar's core network systems. 24.3M mobile + 1.1M broadband subscribers affected; network down 3+ days. Revenue impact: ~UAH 3.6B ($95M) in 2024 from customer loyalty measures. Recovery investment: $90M.",
                "impact_type": "negative",
                "severity": "high",
            },
            {
                "operator_id": None,
                "event_date": "2024-11-19",
                "category": "regulatory",
                "title": "NCEC spectrum auction — UAH 2.895B for 2100/2300/2600 MHz bands",
                "description": "All three operators acquired new spectrum. Kyivstar: UAH 1.43B (2100+2300 MHz, total 202 MHz). Vodafone: 2100+2600 MHz. lifecell: 2100 MHz. 15-year licenses; technology-neutral (can be used for 5G). Mandate: 1,500 new base stations in 2 years.",
                "impact_type": "neutral",
                "severity": "high",
            },
            {
                "operator_id": None,
                "event_date": "2024-12-01",
                "category": "regulatory",
                "title": "War infrastructure damage: 4,300+ base stations destroyed since 2022",
                "description": "Total telecom infrastructure damage: $1.2B as of Nov 2024. 4,300+ mobile base stations destroyed, 30,000+ km fiber damaged. 389 infrastructure incidents in 2024 alone. Estimated 10-year repair cost: $4.67B.",
                "impact_type": "negative",
                "severity": "high",
            },
            {
                "operator_id": "kyivstar_ua",
                "event_date": "2025-08-01",
                "category": "investment",
                "title": "Kyivstar lists on NASDAQ as KYIV — first Ukrainian company on US exchange",
                "description": "VEON spun off Kyivstar as independently listed entity on NASDAQ (ticker: KYIV). First Ukrainian company to list on US stock exchange. Capital raise via secondary offering.",
                "impact_type": "positive",
                "severity": "high",
            },
        ],
        "earnings_highlights": {
            "lifecell_ua": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "FY2023 revenue UAH 11.7B (+24.4%), EBITDA UAH 6.81B (margin 58.2%), net profit UAH 2.57B. Mobile subs 9.9M (3-month active). ARPU UAH 110.9 (+21.2% YoY). FY2024 estimated ~UAH 14B.", "speaker": "CEO"},
                {"segment": "Convergence", "highlight_type": "outlook", "content": "NJJ acquisition completed Sep 2024 for $524M. Merging with Datagroup-Volia (#1 fixed ISP, 4M HH). EBRD/IFC $435M financing secured. Plans: 10,000+ km fiber, 1,000+ new base stations. Creating Ukraine's first converged telco.", "speaker": "CEO"},
            ],
            "kyivstar_ua": [
                {"segment": "Overall", "highlight_type": "guidance", "content": "FY2024 revenue UAH 37.27B (+11%). EBITDA margin 56.1%. Capex UAH 10.22B (+60.7%) — post-cyberattack rebuild. 24M mobile subs, 1.1M broadband, 6.1M multiplay customers (+50.2%).", "speaker": "CEO"},
                {"segment": "Digital", "highlight_type": "outlook", "content": "10.6M digital MAU (+29.6%). Q4 ARPU UAH 136 (+34.5% YoY). Spectrum holdings expanded to 202 MHz (largest among Ukrainian operators). NASDAQ listing planned as KYIV.", "speaker": "CFO"},
            ],
            "vodafone_ua": [
                {"segment": "Revenue", "highlight_type": "guidance", "content": "FY2024 total revenue UAH 24.44B. Mobile revenue UAH 18.97B (+12.5%). Fixed-line UAH 936M (+48.8%) driven by GPON fiber expansion. OIBDA UAH 12.22B (margin ~50%).", "speaker": "CEO"},
                {"segment": "Network", "highlight_type": "outlook", "content": "GPON fiber covering 1.3M HH across 14 regions; 100K+ subscribers (14x growth). Spectrum acquired at Nov 2024 auction (2100+2600 MHz). 15.8M mobile subs. ARPU UAH 118.4 (+10%).", "speaker": "CFO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_ukraine as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
