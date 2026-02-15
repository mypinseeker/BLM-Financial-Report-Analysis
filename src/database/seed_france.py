"""Seed the database with France telecom market data.

4-player market: Orange (incumbent), SFR/Altice (cable+mobile), Free/Iliad (disruptor), Bouygues Telecom (challenger).
Currency: EUR. All revenue figures in EUR millions per quarter.

Data sources:
  - Iliad Group Q1/H1/FY 2024 press releases, FY 2024 results
  - Orange Group FY 2024 results, Q4 2024 press release
  - Altice France Q4 FY 2024 and Q1-Q3 2025 press releases
  - Bouygues Telecom FY 2024 results
  - ARCEP Observatoire des marches Q4 2024
  - Iliad H1 2025 results (TelecomLead)

Note: Free France and Orange France dominate; SFR in decline under Altice restructuring.
Q1-Q4 2025 figures for Free/Orange/Bouygues estimated from H1 2025 guidance and trends.
SFR 2025 quarterly data from Altice France Q1/Q2/Q3 2025 press releases.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "france"
OPERATORS = ["free_fr", "orange_fr", "sfr_fr", "bouygues_telecom_fr"]


def get_seed_data():
    return {
        "financials": {
            # Free/Iliad France — disruptive challenger, Xavier Niel
            # FY2024: France revenue EUR 6,530M (+8.2%), EBITDAaL EUR 2,600M (39.9% margin)
            # Q1 2024: EUR 1,586M (+10.0%), Q2 2024: EUR 1,611M (+9.1%)
            # H1 2024: EUR 3,197M (+9.6%), FY 2024: EUR 6,530M
            # H1 2024 France EBITDAaL: EUR 1,235M (+11.3%)
            # H1 2024 France Capex: EUR 631M
            # FY2025: Group revenue EUR 10.5B+, France growth moderating to ~5-6%
            "free_fr": {
                "total_revenue": [1586, 1611, 1630, 1703, 1665, 1690, 1715, 1740],
                "service_revenue": [1480, 1505, 1525, 1600, 1558, 1585, 1608, 1635],
                "service_revenue_growth_pct": [10.0, 9.1, 8.4, 6.5, 5.0, 5.2, 5.4, 2.2],
                "mobile_service_revenue": [612, 625, 635, 658, 648, 660, 670, 680],
                "mobile_service_growth_pct": [4.3, 4.5, 4.2, 4.0, 5.9, 5.6, 5.5, 3.3],
                "fixed_service_revenue": [868, 880, 890, 972, 910, 925, 938, 955],
                "fixed_service_growth_pct": [9.4, 9.8, 9.5, 8.0, 4.8, 5.1, 5.4, -1.7],
                "b2b_revenue": [45, 48, 50, 52, 55, 58, 60, 62],
                "ebitda": [595, 640, 650, 715, 650, 680, 700, 730],
                "ebitda_margin_pct": [37.5, 39.7, 39.9, 42.0, 39.0, 40.2, 40.8, 42.0],
                "ebitda_growth_pct": [11.3, 11.5, 8.5, 5.5, 9.2, 6.3, 7.7, 2.1],
                "capex": [310, 321, 325, 344, 310, 318, 320, 340],
                "capex_to_revenue_pct": [19.5, 19.9, 19.9, 20.2, 18.6, 18.8, 18.7, 19.5],
                "employees": [10000, 10000, 10100, 10100, 10200, 10200, 10300, 10300],
                "_source": "Iliad Group Q1/H1/FY 2024 press releases; 2025 estimated from H1 2025 guidance",
            },
            # Orange France — incumbent, state-linked
            # FY2024: France revenue EUR 17,798M (+0.4%), EBITDAaL EUR 6,393M (+0.5%)
            # eCAPEX EUR 3,101M (+2.1%). Q4 2024: EUR 4,567M (-0.6%)
            # Note: Orange France revenue includes all divisions (consumer, enterprise, wholesale, carrier)
            # For quarterly split: FY2024 EUR 17,798M; assume seasonal ~25% Q1-Q3, ~26% Q4
            "orange_fr": {
                "total_revenue": [4380, 4430, 4421, 4567, 4395, 4445, 4435, 4580],
                "service_revenue": [3960, 4010, 4000, 4130, 3980, 4025, 4015, 4155],
                "service_revenue_growth_pct": [0.5, 0.8, 0.2, -0.2, 0.3, 0.3, 0.4, 0.2],
                "mobile_service_revenue": [1120, 1140, 1135, 1175, 1130, 1150, 1148, 1190],
                "mobile_service_growth_pct": [0.5, 1.0, 0.5, -0.5, 0.9, 0.9, 1.1, 1.3],
                "fixed_service_revenue": [1650, 1670, 1665, 1720, 1660, 1680, 1675, 1730],
                "fixed_service_growth_pct": [0.8, 1.2, 0.5, -0.3, 0.6, 0.6, 0.6, 0.6],
                "b2b_revenue": [1190, 1200, 1200, 1235, 1190, 1195, 1192, 1235],
                "ebitda": [1550, 1620, 1610, 1613, 1560, 1630, 1620, 1625],
                "ebitda_margin_pct": [35.4, 36.6, 36.4, 35.3, 35.5, 36.7, 36.5, 35.5],
                "ebitda_growth_pct": [0.5, 0.8, 0.3, 0.1, 0.6, 0.6, 0.6, 0.7],
                "capex": [750, 790, 780, 781, 740, 770, 760, 770],
                "capex_to_revenue_pct": [17.1, 17.8, 17.6, 17.1, 16.8, 17.3, 17.1, 16.8],
                "employees": [68000, 68000, 68000, 68000, 67500, 67500, 67000, 67000],
                "_source": "Orange Group FY 2024 results, Q3/Q4 2024 press releases; 2025 from Lead the Future guidance",
            },
            # SFR / Altice France — cable+mobile, financial distress
            # FY2024: Revenue ~EUR 10,300M, EBITDA EUR 3,351M (~32.5%), Capex EUR 1,999M
            # 2025 accelerating decline: Q1 EUR 2,382M (-6.2%), Q2 ~EUR 2,350M, Q3 ~EUR 2,320M
            # 9M 2025: EUR 7,050M (-7.6%), EBITDA EUR 2,324M (-10.3%)
            # Losing ~500K mobile subs per quarter in 2025
            "sfr_fr": {
                "total_revenue": [2610, 2590, 2560, 2540, 2382, 2350, 2320, 2300],
                "service_revenue": [2250, 2240, 2220, 2200, 2060, 2040, 2015, 2000],
                "service_revenue_growth_pct": [-0.9, -0.2, -1.5, -1.2, -8.7, -8.9, -9.2, -9.1],
                "mobile_service_revenue": [900, 895, 885, 880, 825, 815, 808, 800],
                "mobile_service_growth_pct": [-1.5, -1.0, -2.0, -2.5, -8.3, -8.9, -8.7, -9.1],
                "fixed_service_revenue": [1050, 1045, 1040, 1030, 960, 955, 945, 940],
                "fixed_service_growth_pct": [-0.5, 0.5, -1.0, -0.5, -8.6, -8.6, -9.1, -8.7],
                "b2b_revenue": [300, 300, 295, 290, 275, 270, 262, 260],
                "ebitda": [782, 770, 810, 989, 678, 801, 764, 750],
                "ebitda_margin_pct": [30.0, 29.7, 31.6, 38.9, 28.5, 34.1, 32.9, 32.6],
                "ebitda_growth_pct": [-6.5, -7.5, -5.0, -3.0, -13.3, 4.0, -5.7, -24.2],
                "capex": [490, 510, 505, 494, 440, 450, 445, 440],
                "capex_to_revenue_pct": [18.8, 19.7, 19.7, 19.4, 18.5, 19.1, 19.2, 19.1],
                "employees": [15000, 15000, 14800, 14800, 14500, 14500, 14200, 14200],
                "_source": "Altice France Q4 FY 2024, Q1/Q2/Q3 2025 press releases (PDF)",
            },
            # Bouygues Telecom — part of Bouygues Group
            # FY2024: Billed sales EUR 6,200M (+5%), Total sales EUR 7,820M (+1%)
            # EBITDAaL EUR 2,037M (+EUR 68M), Capex EUR 1,541M (excl. freq)
            # La Poste Mobile consolidated from Nov 2024 (2.4M customers)
            # Quarterly: assume ~25% per Q for even distribution
            "bouygues_telecom_fr": {
                "total_revenue": [1920, 1940, 1950, 2010, 1960, 1985, 1990, 2050],
                "service_revenue": [1520, 1540, 1555, 1585, 1555, 1578, 1585, 1615],
                "service_revenue_growth_pct": [5.0, 5.2, 4.8, 5.0, 2.3, 2.5, 1.9, 1.9],
                "mobile_service_revenue": [680, 690, 695, 705, 700, 710, 715, 725],
                "mobile_service_growth_pct": [3.0, 3.5, 3.2, 3.8, 2.9, 2.9, 2.9, 2.8],
                "fixed_service_revenue": [640, 650, 660, 680, 660, 670, 675, 690],
                "fixed_service_growth_pct": [6.0, 6.5, 6.2, 6.0, 3.1, 3.1, 2.3, 1.5],
                "b2b_revenue": [200, 200, 200, 200, 195, 198, 195, 200],
                "ebitda": [485, 510, 510, 532, 500, 525, 520, 540],
                "ebitda_margin_pct": [25.3, 26.3, 26.2, 26.5, 25.5, 26.4, 26.1, 26.3],
                "ebitda_growth_pct": [3.5, 3.0, 3.5, 3.8, 3.1, 2.9, 2.0, 1.5],
                "capex": [375, 390, 385, 391, 365, 378, 372, 380],
                "capex_to_revenue_pct": [19.5, 20.1, 19.7, 19.5, 18.6, 19.0, 18.7, 18.5],
                "employees": [9300, 9400, 9500, 9500, 9600, 9600, 9700, 9700],
                "_source": "Bouygues Group FY 2024 results; 2025 estimated from guidance (+low single-digit growth)",
            },
        },
        "subscribers": {
            # Free France — from Iliad quarterly KPI reports
            # End-2023: 14,832K mobile, 7,414K fixed
            # Q1 2024: 15,217K mobile, 7,499K fixed (5,748K FTTH)
            # Q2 2024: 15,337K mobile, 7,539K fixed (5,937K FTTH)
            # FY 2024: 15,500K mobile (+668K net adds), 7,600K fixed (6,400K FTTH, 81.7% take-up)
            # Mobile ARPU: EUR 12.3/month, Fixed ARPU: EUR 37.0/month
            "free_fr": {
                "mobile_total_k": [15217, 15337, 15420, 15500, 15580, 15660, 15740, 15820],
                "mobile_postpaid_k": [11345, 11530, 11700, 12050, 12200, 12350, 12500, 12650],
                "mobile_prepaid_k": [3872, 3807, 3720, 3450, 3380, 3310, 3240, 3170],
                "mobile_net_adds_k": [385, 120, 83, 80, 80, 80, 80, 80],
                "mobile_churn_pct": [1.5, 1.4, 1.4, 1.4, 1.4, 1.3, 1.3, 1.3],
                "mobile_arpu": [12.2, 12.3, 12.3, 12.4, 12.5, 12.5, 12.6, 12.6],
                "broadband_total_k": [7499, 7539, 7570, 7600, 7635, 7670, 7700, 7730],
                "broadband_fiber_k": [5748, 5937, 6100, 6400, 6550, 6700, 6850, 7000],
                "broadband_net_adds_k": [85, 40, 31, 30, 35, 35, 30, 30],
                "tv_total_k": [6800, 6850, 6900, 6950, 7000, 7030, 7060, 7090],
                "b2b_customers_k": [50, 52, 55, 58, 62, 66, 70, 75],
                "_source": "Iliad Q1/H1/FY 2024 press releases; ARPU billed to subscribers",
            },
            # Orange France — estimated from group-level reports
            # Convergent customers: 9.1M (Q4 2024, +1.0% YoY), ARPO EUR 78.0/month
            # Fiber France: ~10M milestone (end-2024), households connectable: 40.3M
            # Q4 2024: mobile net adds +118K, fixed broadband +10K, fiber +292K
            "orange_fr": {
                "mobile_total_k": [22200, 22350, 22450, 22550, 22600, 22700, 22800, 22900],
                "mobile_postpaid_k": [19600, 19750, 19850, 19950, 20050, 20150, 20250, 20350],
                "mobile_prepaid_k": [2600, 2600, 2600, 2600, 2550, 2550, 2550, 2550],
                "mobile_net_adds_k": [50, 150, 100, 118, 50, 100, 100, 100],
                "mobile_churn_pct": [1.2, 1.1, 1.1, 1.1, 1.2, 1.1, 1.1, 1.1],
                "mobile_arpu": [20.5, 20.8, 20.6, 20.4, 20.6, 20.8, 20.7, 20.5],
                "broadband_total_k": [11200, 11250, 11350, 11500, 11530, 11580, 11650, 11720],
                "broadband_fiber_k": [9200, 9500, 9750, 10000, 10200, 10400, 10600, 10800],
                "broadband_net_adds_k": [30, 50, 100, 10, 30, 50, 70, 70],
                "tv_total_k": [8500, 8550, 8600, 8650, 8700, 8730, 8760, 8790],
                "b2b_customers_k": [400, 405, 410, 415, 420, 425, 430, 435],
                "_source": "Orange Group FY 2024 results; France subscriber counts estimated from convergent/fiber metrics",
            },
            # SFR / Altice France — subscriber decline accelerating
            # FY2024: ~20.5M mobile (estimated), losing ~500K/Q in 2025
            # Fixed broadband ~6.5-7M, Fiber ~4.5-5M
            # 5G coverage: 84%, 11,951 municipalities (Q1 2025)
            "sfr_fr": {
                "mobile_total_k": [21000, 20800, 20600, 20500, 20000, 19500, 19100, 18700],
                "mobile_postpaid_k": [16500, 16400, 16300, 16200, 15800, 15400, 15100, 14800],
                "mobile_prepaid_k": [4500, 4400, 4300, 4300, 4200, 4100, 4000, 3900],
                "mobile_net_adds_k": [-100, -200, -200, -100, -500, -500, -400, -400],
                "mobile_churn_pct": [2.2, 2.3, 2.4, 2.3, 2.8, 2.9, 2.8, 2.8],
                "mobile_arpu": [17.5, 17.3, 17.0, 16.8, 16.5, 16.2, 16.0, 15.8],
                "broadband_total_k": [6800, 6780, 6750, 6700, 6600, 6500, 6400, 6300],
                "broadband_fiber_k": [4500, 4600, 4700, 4800, 4850, 4900, 4930, 4960],
                "broadband_net_adds_k": [-20, -20, -30, -50, -100, -100, -100, -100],
                "tv_total_k": [5500, 5450, 5400, 5350, 5250, 5150, 5050, 4950],
                "b2b_customers_k": [200, 198, 196, 195, 190, 188, 185, 182],
                "_source": "Altice France Q4 2024 / Q1 2025 press releases; Mobile Europe SFR subscriber losses article",
            },
            # Bouygues Telecom — steady growth, La Poste consolidation
            # FY2024: 18.3M mobile plan (incl. 2.4M La Poste, +339K organic)
            # Fixed: 5.2M (+263K), FTTH: 4.2M (+615K in FY24)
            # FTTH premises marketed: 38M, 81% of fixed base
            # Mobile ABPU EUR 19.1/month (excl. La Poste), La Poste ABPU EUR 11.0
            # Fixed ABPU EUR 33.4/month (+EUR 2.0 YoY)
            "bouygues_telecom_fr": {
                "mobile_total_k": [15600, 15750, 15900, 18300, 18400, 18500, 18600, 18700],
                "mobile_postpaid_k": [14800, 14950, 15100, 17400, 17500, 17600, 17700, 17800],
                "mobile_prepaid_k": [800, 800, 800, 900, 900, 900, 900, 900],
                "mobile_net_adds_k": [80, 150, 150, 2400, 100, 100, 100, 100],
                "mobile_churn_pct": [1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.2, 1.2],
                "mobile_arpu": [19.5, 19.3, 19.2, 19.1, 19.0, 19.1, 19.2, 19.3],
                "broadband_total_k": [4937, 4980, 5080, 5200, 5260, 5320, 5380, 5440],
                "broadband_fiber_k": [3585, 3750, 3990, 4200, 4350, 4500, 4650, 4800],
                "broadband_net_adds_k": [50, 43, 100, 120, 60, 60, 60, 60],
                "tv_total_k": [3800, 3850, 3900, 3950, 4000, 4040, 4080, 4120],
                "b2b_customers_k": [150, 153, 156, 160, 163, 166, 169, 172],
                "_source": "Bouygues FY 2024 results; La Poste consolidated Q4 2024 (+2.4M mobile subs)",
            },
        },
        "macro": {
            "gdp_growth_pct": 1.1,
            "inflation_pct": 2.3,
            "unemployment_pct": 7.3,
            "telecom_market_size_eur_b": 38.1,
            "telecom_growth_pct": 1.2,
            "five_g_adoption_pct": 29.0,
            "fiber_penetration_pct": 75.0,
            "regulatory_environment": "ARCEP pro-competition regulation; fiber co-investment framework; copper retirement mandate by 2030; 5G deployment obligations (8,000 sites by end-2024); ARCEP deregulated wholesale central access Oct 2024 citing effective competition; active MVNO segment (~15% mobile market); 4-player market structure maintained since 2012",
            "digital_strategy": "EU Digital Decade: 100% 5G coverage by 2030; France Tres Haut Debit fiber plan >90% coverage achieved by end-2024 (40.3M premises connectable); near-universal fiber by 2025; copper retirement by 2030; public broadband subsidies for rural areas via RIP networks",
            "source_url": "ARCEP Observatoire Q4 2024 / INSEE / European Commission 2025",
        },
        "network": {
            "free_fr": {
                "five_g_coverage_pct": 94,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 37000,
                "technology_mix": {"mobile_vendor": "Nokia", "spectrum_mhz": 310, "core_vendor": "Nokia", "5g_sa_status": "5G SA launched Sep 2024", "fiber_technology": "GPON/XGS-PON"},
            },
            "orange_fr": {
                "five_g_coverage_pct": 93,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 40300,
                "technology_mix": {"mobile_vendor": "Ericsson/Nokia", "spectrum_mhz": 380, "core_vendor": "Ericsson", "5g_sa_status": "SA deploying", "fiber_technology": "GPON/XGS-PON/10G-PON"},
            },
            "sfr_fr": {
                "five_g_coverage_pct": 84,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 30000,
                "technology_mix": {"mobile_vendor": "Nokia", "spectrum_mhz": 290, "core_vendor": "Nokia", "cable_docsis": "3.1", "cable_homepass_k": 22000},
            },
            "bouygues_telecom_fr": {
                "five_g_coverage_pct": 82,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 38000,
                "technology_mix": {"mobile_vendor": "Huawei/Nokia", "spectrum_mhz": 280, "core_vendor": "Nokia", "fiber_technology": "GPON co-investment"},
            },
        },
        "executives": {
            "free_fr": [
                {"name": "Thomas Reynaud", "title": "CEO, Iliad Group", "start_date": "2018-05-01", "background": "Iliad Group CEO since 2018; also Chairman of the Board at Tele2 since May 2024; driving international expansion and AI investment"},
                {"name": "Nicolas Thomas", "title": "CEO, Free (France OpCo)", "start_date": "2023-01-01", "background": "Leads French operations; product and commercial strategy; Freebox innovation cycles"},
                {"name": "Thomas Robin", "title": "CFO, Free (France OpCo)", "start_date": "2023-01-01", "background": "Finance and investor relations for French operations"},
            ],
            "orange_fr": [
                {"name": "Christel Heydemann", "title": "CEO, Orange Group", "start_date": "2022-04-01", "background": "Former Schneider Electric EVP; first female CEO of Orange; driving Lead the Future transformation plan"},
                {"name": "Laurent Martinez", "title": "CFO, Orange Group", "start_date": "2023-01-01", "background": "Orange Group CFO; managing capex discipline and shareholder returns"},
            ],
            "sfr_fr": [
                {"name": "Mathieu Cocq", "title": "CEO, SFR", "start_date": "2024-08-01", "background": "Succeeded Gregory Rabuel; managing SFR through Altice financial restructuring"},
                {"name": "Arthur Dreyfuss", "title": "CEO, Altice France", "start_date": "2021-01-01", "background": "Also CEO of Altice Media; overseeing Altice France debt restructuring and potential asset sales"},
            ],
            "bouygues_telecom_fr": [
                {"name": "Benoit Torloting", "title": "CEO, Bouygues Telecom", "start_date": "2022-01-01", "background": "Bouygues Group veteran; driving convergence and La Poste Mobile integration"},
                {"name": "Christian Lecoq", "title": "Deputy MD Finance", "start_date": "2020-01-01", "background": "Finance and strategy for Bouygues Telecom"},
            ],
        },
        "competitive_scores": {
            "free_fr": {
                "Network Coverage": 88, "Network Quality": 85, "Brand Strength": 82,
                "Price Competitiveness": 95, "Customer Service": 70, "Digital Experience": 90,
                "Enterprise Solutions": 35, "Innovation": 92, "Distribution": 72,
            },
            "orange_fr": {
                "Network Coverage": 95, "Network Quality": 92, "Brand Strength": 90,
                "Price Competitiveness": 55, "Customer Service": 80, "Digital Experience": 82,
                "Enterprise Solutions": 95, "Innovation": 85, "Distribution": 92,
            },
            "sfr_fr": {
                "Network Coverage": 82, "Network Quality": 72, "Brand Strength": 60,
                "Price Competitiveness": 75, "Customer Service": 55, "Digital Experience": 68,
                "Enterprise Solutions": 65, "Innovation": 60, "Distribution": 72,
            },
            "bouygues_telecom_fr": {
                "Network Coverage": 85, "Network Quality": 86, "Brand Strength": 78,
                "Price Competitiveness": 78, "Customer Service": 88, "Digital Experience": 80,
                "Enterprise Solutions": 55, "Innovation": 75, "Distribution": 80,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "free_fr",
                "event_date": "2024-01-15",
                "category": "commercial",
                "title": "Free launches Freebox Ultra with WiFi 7 — first in Europe",
                "description": "Freebox Ultra launched with WiFi 7, 8Gbps symmetric fiber, integrated NAS, 4K HDR player. EUR 49.99/month. First major European ISP with WiFi 7.",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "free_fr",
                "event_date": "2024-09-15",
                "category": "technology",
                "title": "Free launches 5G Standalone nationwide",
                "description": "Free becomes first French operator to deploy 5G Standalone nationwide. 94.2% population coverage. 6,000 new 5G sites deployed in 2024.",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "sfr_fr",
                "event_date": "2025-02-15",
                "category": "competitive",
                "title": "Altice France restructures EUR 24B debt — creditors take 45% stake",
                "description": "Patrick Drahi negotiates debt reduction from EUR 24B to EUR 15.5B. Cedes 45% ownership stake to creditors. SFR revenue and EBITDA in accelerating decline.",
                "impact_type": "negative",
                "severity": "high",
            },
            {
                "operator_id": None,
                "event_date": "2025-10-14",
                "category": "competitive",
                "title": "Orange, Bouygues, Free bid EUR 17B for SFR assets — rejected",
                "description": "Consortium of Orange (27%), Bouygues (43%), Free (30%) submits EUR 17B non-binding offer for most of Altice France's SFR assets. Altice immediately rejects. Talks continue with due diligence starting Jan 2026.",
                "impact_type": "neutral",
                "severity": "high",
            },
            {
                "operator_id": "bouygues_telecom_fr",
                "event_date": "2024-11-01",
                "category": "competitive",
                "title": "Bouygues acquires SFR's 49% stake in La Poste Mobile",
                "description": "Bouygues Telecom acquires SFR's 49% stake in La Poste Mobile. 2.4M customers consolidated. Migration to Bouygues network planned 2025-2027.",
                "impact_type": "positive",
                "severity": "medium",
            },
            {
                "operator_id": "free_fr",
                "event_date": "2025-06-01",
                "category": "investment",
                "title": "Iliad announces EUR 3B AI investment — Scaleway, OpCore, Kyutai",
                "description": "Iliad Group announces EUR 3B investment plan in AI infrastructure. Scaleway cloud GPU clusters, OpCore data centers, Kyutai AI research lab. Positions Free as tech platform beyond telecom.",
                "impact_type": "positive",
                "severity": "medium",
            },
        ],
        "earnings_highlights": {
            "free_fr": [
                {"segment": "Group", "highlight_type": "guidance", "content": "FY2024: France revenue EUR 6,530M (+8.2%), EBITDAaL EUR 2,600M (39.9% margin). Iliad Group crossed EUR 10B revenue milestone. Europe's 5th largest telco by subscribers (50.5M). 2025 OpFCF target EUR 2.0B.", "speaker": "CEO"},
                {"segment": "Mobile", "highlight_type": "explanation", "content": "Mobile subs 15.5M (+668K net adds in 2024). 5G SA launched nationwide Sep 2024. Mobile ARPU EUR 12.3 (+1.8% YoY). Convergent discount driving improved retention but slight ARPU dilution.", "speaker": "CEO"},
                {"segment": "Fixed", "highlight_type": "outlook", "content": "Freebox subs 7.6M. Fiber take-up 81.7% (6.4M FTTH active). Fixed ARPU EUR 37.0 (+4.5% YoY). Freebox Ultra driving ARPU uplift. 37M+ premises connectable across group.", "speaker": "CFO"},
            ],
            "orange_fr": [
                {"segment": "France", "highlight_type": "guidance", "content": "FY2024 France revenue EUR 17,798M (+0.4%), EBITDAaL EUR 6,393M (+0.5%). Fiber milestone: 10M customers in France. Convergent customers 9.1M, ARPO EUR 78/month (+4% YoY). 2025 organic cash flow target raised to EUR 3.6B+.", "speaker": "CEO"},
                {"segment": "Fixed", "highlight_type": "explanation", "content": "40.3M premises connectable (>90% of French households). Copper retirement accelerating. Fiber net adds strong: +292K in Q4 2024 alone.", "speaker": "CTO"},
            ],
            "sfr_fr": [
                {"segment": "Group", "highlight_type": "guidance", "content": "FY2024 EBITDA EUR 3,351M, Capex EUR 1,999M, OpFCF EUR 1,351M. Debt restructured from EUR 24B to EUR 15.5B (Feb 2025). 9M 2025: revenue -7.6%, EBITDA -10.3%. Subscriber losses accelerating.", "speaker": "CEO"},
                {"segment": "Commercial", "highlight_type": "outlook", "content": "Losing ~500K mobile subs per quarter in 2025. 5G coverage 84% (11,951 municipalities). RED by SFR competing on price but unable to stem churn. Joint SFR acquisition bid by Orange/Bouygues/Free rejected but talks ongoing.", "speaker": "CEO"},
            ],
            "bouygues_telecom_fr": [
                {"segment": "Group", "highlight_type": "guidance", "content": "FY2024 billed sales EUR 6,200M (+5%), EBITDAaL EUR 2,037M. La Poste Mobile consolidated Nov 2024 (+2.4M customers). FTTH 4.2M subscribers (81% of fixed base). Mobile ABPU EUR 19.1.", "speaker": "CEO"},
                {"segment": "Fixed", "highlight_type": "outlook", "content": "FTTH net adds +615K in 2024 (207K in Q4). 38M premises marketed. Fixed ABPU EUR 33.4 (+EUR 2.0 YoY). Continuing fiber-led growth strategy.", "speaker": "CFO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_france as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
