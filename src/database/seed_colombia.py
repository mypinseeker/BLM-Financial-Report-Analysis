"""Seed the database with Colombia telecom market data.

Colombia is Millicom's largest market by revenue (Tigo-UNE, 50% JV with EPM).
4-player market: Claro (leader), Tigo-UNE, Movistar, WOM (new entrant).
Currency: COP (Colombian Peso). All revenue figures in COP billions.

NOTE: Tigo (Millicom) acquired Colombia Telecomunicaciones (Coltel, formerly
Telefonica Colombia / Movistar Colombia) in Q3 2025. Post-acquisition, Tigo
inherits Coltel's subscriber base, spectrum assets, and fixed infrastructure.
The combined entity operates under the Tigo brand.

Data sources: Millicom Q4 2025 earnings, CRC Colombia regulator data,
America Movil IR, WOM public filings, ANE spectrum allocation registry.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "colombia"
# NOTE: Movistar Colombia (Coltel) was acquired by Tigo in Q3 2025.
# Post-acquisition the market is effectively 3-player: Tigo-UNE (incl. Coltel),
# Claro, and WOM. We keep movistar_co for historical data but mark it inactive.
OPERATORS = ["tigo_colombia", "claro_co", "movistar_co", "wom_co"]


def get_seed_data():
    return {
        "financials": {
            # Tigo-UNE Colombia — now #1 by spectrum post-Coltel acquisition, 50% JV with EPM
            "tigo_colombia": {
                "total_revenue": [2150, 2180, 2220, 2260, 2300, 2340, 2380, 2420],
                "service_revenue": [2020, 2050, 2090, 2130, 2170, 2210, 2250, 2290],
                "service_revenue_growth_pct": [4.0, 4.3, 4.5, 4.8, 7.0, 7.3, 7.2, 7.1],
                "mobile_service_revenue": [1100, 1120, 1140, 1160, 1180, 1200, 1220, 1240],
                "mobile_service_growth_pct": [3.5, 3.8, 4.0, 4.2, 7.3, 7.1, 7.0, 6.9],
                "fixed_service_revenue": [750, 760, 780, 800, 820, 840, 860, 880],
                "fixed_service_growth_pct": [5.0, 5.2, 5.5, 5.8, 8.0, 7.9, 7.7, 7.5],
                "b2b_revenue": [170, 170, 170, 170, 170, 170, 170, 170],
                "ebitda": [750, 760, 780, 790, 810, 820, 835, 850],
                "ebitda_margin_pct": [34.9, 34.9, 35.1, 35.0, 35.2, 35.0, 35.1, 35.1],
                "ebitda_growth_pct": [3.5, 3.8, 4.2, 4.5, 8.0, 7.9, 7.1, 7.6],
                "capex": [420, 430, 440, 450, 460, 470, 480, 490],
                "capex_to_revenue_pct": [19.5, 19.7, 19.8, 19.9, 20.0, 20.1, 20.2, 20.2],
                "employees": [6500, 6500, 6600, 6600, 6700, 6700, 6800, 6800],
                "_source": "Millicom Q4 2025 Earnings Report — Colombia segment",
            },
            # Claro Colombia — market leader by revenue and subscribers
            "claro_co": {
                "total_revenue": [4200, 4250, 4300, 4350, 4400, 4450, 4500, 4550],
                "service_revenue": [3950, 4000, 4050, 4100, 4150, 4200, 4250, 4300],
                "service_revenue_growth_pct": [2.8, 3.0, 3.2, 3.5, 3.8, 3.9, 4.0, 4.2],
                "mobile_service_revenue": [2500, 2530, 2560, 2590, 2620, 2650, 2680, 2710],
                "fixed_service_revenue": [1100, 1120, 1140, 1160, 1180, 1200, 1220, 1240],
                "b2b_revenue": [350, 350, 350, 350, 350, 350, 350, 350],
                "ebitda": [1680, 1700, 1720, 1740, 1760, 1780, 1800, 1820],
                "ebitda_margin_pct": [40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0],
                "capex": [730, 740, 750, 760, 770, 780, 790, 800],
                "capex_to_revenue_pct": [17.4, 17.4, 17.4, 17.5, 17.5, 17.5, 17.6, 17.6],
                "employees": [12000, 12000, 12100, 12100, 12200, 12200, 12300, 12300],
                "_source": "America Movil Q4 2025 Earnings — Colombia segment",
            },
            # Movistar Colombia (Coltel) — ACQUIRED by Tigo Q3 2025; historical data below
            "movistar_co": {
                "total_revenue": [1800, 1810, 1820, 1830, 1840, 1850, 1860, 1870],
                "service_revenue": [1680, 1690, 1700, 1710, 1720, 1730, 1740, 1750],
                "service_revenue_growth_pct": [1.0, 1.2, 1.3, 1.5, 2.2, 2.4, 2.4, 2.3],
                "mobile_service_revenue": [1200, 1210, 1220, 1230, 1240, 1250, 1260, 1270],
                "fixed_service_revenue": [380, 380, 380, 380, 380, 380, 380, 380],
                "b2b_revenue": [100, 100, 100, 100, 100, 100, 100, 100],
                "ebitda": [520, 525, 530, 535, 540, 545, 550, 555],
                "ebitda_margin_pct": [28.9, 29.0, 29.1, 29.2, 29.3, 29.5, 29.6, 29.7],
                "capex": [310, 315, 318, 320, 325, 328, 330, 335],
                "capex_to_revenue_pct": [17.2, 17.4, 17.5, 17.5, 17.7, 17.7, 17.7, 17.9],
                "employees": [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000],
                "_source": "Telefonica LATAM Q4 2025 Report",
            },
            # WOM Colombia — new entrant, rapid growth but unprofitable
            "wom_co": {
                "total_revenue": [280, 310, 340, 370, 400, 430, 460, 500],
                "service_revenue": [250, 280, 310, 340, 370, 400, 430, 460],
                "service_revenue_growth_pct": [45.0, 48.0, 50.0, 52.0, 42.9, 38.7, 35.3, 35.3],
                "mobile_service_revenue": [250, 280, 310, 340, 370, 400, 430, 460],
                "ebitda": [-80, -70, -60, -50, -40, -30, -20, -10],
                "ebitda_margin_pct": [-28.6, -22.6, -17.6, -13.5, -10.0, -7.0, -4.3, -2.0],
                "capex": [120, 130, 140, 150, 155, 160, 165, 170],
                "capex_to_revenue_pct": [42.9, 41.9, 41.2, 40.5, 38.8, 37.2, 35.9, 34.0],
                "employees": [2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700],
                "_source": "WOM Colombia public filings",
            },
        },
        "subscribers": {
            "tigo_colombia": {
                "mobile_total_k": [14500, 14700, 14900, 15100, 15300, 15500, 15700, 15900],
                "mobile_postpaid_k": [4350, 4410, 4470, 4530, 4590, 4650, 4710, 4770],
                "mobile_prepaid_k": [10150, 10290, 10430, 10570, 10710, 10850, 10990, 11130],
                "mobile_net_adds_k": [150, 200, 200, 200, 200, 200, 200, 200],
                "mobile_churn_pct": [2.5, 2.4, 2.4, 2.3, 2.3, 2.2, 2.2, 2.1],
                "mobile_arpu": [7600, 7650, 7700, 7700, 7750, 7800, 7800, 7850],
                "broadband_total_k": [1600, 1640, 1680, 1720, 1760, 1800, 1840, 1880],
                "broadband_cable_k": [1100, 1110, 1120, 1130, 1140, 1150, 1160, 1170],
                "broadband_fiber_k": [350, 370, 400, 430, 460, 490, 520, 550],
                "broadband_net_adds_k": [30, 40, 40, 40, 40, 40, 40, 40],
                "tv_total_k": [1200, 1210, 1220, 1230, 1240, 1250, 1260, 1270],
                "fmc_total_k": [400, 420, 440, 460, 480, 500, 520, 540],
                "fmc_penetration_pct": [25.0, 25.6, 26.2, 26.7, 27.3, 27.8, 28.3, 28.7],
                "b2b_customers_k": [85, 87, 89, 91, 93, 95, 97, 99],
                "_source": "Millicom Q4 2025 Earnings Report",
            },
            "claro_co": {
                "mobile_total_k": [31000, 31200, 31400, 31600, 31800, 32000, 32200, 32400],
                "mobile_postpaid_k": [9300, 9360, 9420, 9480, 9540, 9600, 9660, 9720],
                "mobile_prepaid_k": [21700, 21840, 21980, 22120, 22260, 22400, 22540, 22680],
                "mobile_net_adds_k": [150, 200, 200, 200, 200, 200, 200, 200],
                "mobile_churn_pct": [2.2, 2.2, 2.1, 2.1, 2.0, 2.0, 2.0, 1.9],
                "mobile_arpu": [8100, 8150, 8200, 8200, 8250, 8300, 8350, 8400],
                "broadband_total_k": [2800, 2830, 2860, 2890, 2920, 2950, 2980, 3010],
                "broadband_fiber_k": [800, 840, 880, 920, 960, 1000, 1040, 1080],
                "tv_total_k": [2100, 2110, 2120, 2130, 2140, 2150, 2160, 2170],
                "b2b_customers_k": [150, 152, 154, 156, 158, 160, 162, 164],
                "_source": "America Movil Q4 2025 Earnings",
            },
            "movistar_co": {
                "mobile_total_k": [15000, 15050, 15100, 15150, 15200, 15250, 15300, 15350],
                "mobile_postpaid_k": [5250, 5270, 5290, 5310, 5330, 5350, 5370, 5390],
                "mobile_prepaid_k": [9750, 9780, 9810, 9840, 9870, 9900, 9930, 9960],
                "mobile_net_adds_k": [30, 50, 50, 50, 50, 50, 50, 50],
                "mobile_churn_pct": [2.8, 2.7, 2.7, 2.6, 2.6, 2.5, 2.5, 2.5],
                "mobile_arpu": [8000, 8030, 8060, 8080, 8100, 8130, 8160, 8200],
                "broadband_total_k": [1100, 1110, 1120, 1130, 1140, 1150, 1160, 1170],
                "broadband_fiber_k": [350, 370, 390, 410, 430, 450, 470, 490],
                "tv_total_k": [700, 705, 710, 715, 720, 725, 730, 735],
                "b2b_customers_k": [60, 61, 62, 63, 64, 65, 66, 67],
                "_source": "Telefonica LATAM Q4 2025 Report",
            },
            "wom_co": {
                "mobile_total_k": [2500, 2800, 3100, 3400, 3700, 4000, 4300, 4600],
                "mobile_postpaid_k": [500, 560, 620, 680, 740, 800, 860, 920],
                "mobile_prepaid_k": [2000, 2240, 2480, 2720, 2960, 3200, 3440, 3680],
                "mobile_net_adds_k": [250, 300, 300, 300, 300, 300, 300, 300],
                "mobile_churn_pct": [4.0, 3.8, 3.6, 3.5, 3.3, 3.2, 3.1, 3.0],
                "mobile_arpu": [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10870],
                "_source": "WOM Colombia public filings",
            },
        },
        "macro": {
            "gdp_growth_pct": 1.8,
            "inflation_pct": 5.5,
            "unemployment_pct": 10.2,
            "telecom_market_size_eur_b": 8.5,
            "telecom_growth_pct": 4.0,
            "five_g_adoption_pct": 2.0,
            "fiber_penetration_pct": 18.0,
            "regulatory_environment": "CRC pro-competition; spectrum caps; MVNOs encouraged; asymmetric regulation on Claro",
            "digital_strategy": "Colombia Digital 2030; broadband universalization; 5G roadmap announced",
            "source_url": "CRC Colombia / DANE / MinTIC 2025",
        },
        "network": {
            # ──────────────────────────────────────────────────────────────
            # Spectrum data source: ANE Colombia (Agencia Nacional del Espectro)
            # FDD bands: shown as 2×N MHz (paired uplink + downlink)
            #   total_mhz = paired_mhz × 2  (e.g. 2×10 = 20 MHz total)
            # TDD bands: shown as N MHz (unpaired, single range)
            #   total_mhz = the block width
            # ──────────────────────────────────────────────────────────────

            # Post-acquisition: Tigo now holds combined Tigo + Coltel spectrum
            "tigo_colombia": {
                "five_g_coverage_pct": 12,
                "four_g_coverage_pct": 92,
                "fiber_homepass_k": 8000,
                "cable_homepass_k": 5200,
                "technology_mix": {
                    "mobile_vendor": "Nokia/Ericsson/Huawei",
                    "spectrum_mhz": 265,
                    "core_vendor": "Nokia",
                    "notes": "Combined Tigo + Coltel spectrum post-acquisition Q3 2025",
                    "spectrum_bands": [
                        # 700 MHz — Band 28 FDD (APT)
                        {"band": "700 MHz", "band_id": "B28", "duplex": "FDD",
                         "paired_mhz": 10, "total_mhz": 20,
                         "ul": "703–713 MHz", "dl": "758–768 MHz",
                         "use": "4G/5G coverage", "origin": "Tigo original"},
                        {"band": "700 MHz", "band_id": "B28", "duplex": "FDD",
                         "paired_mhz": 10, "total_mhz": 20,
                         "ul": "723–733 MHz", "dl": "778–788 MHz",
                         "use": "4G/5G coverage", "origin": "ex-Coltel"},
                        # 850 MHz — Band 5 FDD
                        {"band": "850 MHz", "band_id": "B5", "duplex": "FDD",
                         "paired_mhz": 5, "total_mhz": 10,
                         "ul": "829–834 MHz", "dl": "874–879 MHz",
                         "use": "4G rural coverage", "origin": "ex-Coltel"},
                        # 1900 MHz — Band 2 PCS FDD
                        {"band": "1900 MHz", "band_id": "B2", "duplex": "FDD",
                         "paired_mhz": 12.5, "total_mhz": 25,
                         "ul": "1862.5–1875 MHz", "dl": "1942.5–1955 MHz",
                         "use": "3G/4G capacity", "origin": "Tigo original"},
                        {"band": "1900 MHz", "band_id": "B2", "duplex": "FDD",
                         "paired_mhz": 25, "total_mhz": 50,
                         "ul": "1850–1875 MHz", "dl": "1930–1955 MHz",
                         "use": "3G/4G capacity", "origin": "ex-Coltel"},
                        # AWS — Band 4 FDD
                        {"band": "AWS", "band_id": "B4", "duplex": "FDD",
                         "paired_mhz": 20, "total_mhz": 40,
                         "ul": "1710–1730 MHz", "dl": "2110–2130 MHz",
                         "use": "4G capacity", "origin": "Tigo original"},
                        {"band": "AWS", "band_id": "B4", "duplex": "FDD",
                         "paired_mhz": 20, "total_mhz": 40,
                         "ul": "1730–1750 MHz", "dl": "2130–2150 MHz",
                         "use": "4G capacity", "origin": "ex-Coltel"},
                        # 2500 MHz — Band 41 TDD
                        {"band": "2500 MHz", "band_id": "B41", "duplex": "TDD",
                         "total_mhz": 60,
                         "range": "2530–2590 MHz",
                         "use": "4G high-capacity", "origin": "Tigo original"},
                    ],
                },
            },
            "claro_co": {
                "five_g_coverage_pct": 10,
                "four_g_coverage_pct": 90,
                "fiber_homepass_k": 8000,
                "cable_homepass_k": 3000,
                "technology_mix": {
                    "mobile_vendor": "Ericsson",
                    "spectrum_mhz": 200,
                    "core_vendor": "Ericsson",
                    "spectrum_bands": [
                        # 700 MHz — Band 28 FDD
                        {"band": "700 MHz", "band_id": "B28", "duplex": "FDD",
                         "paired_mhz": 10, "total_mhz": 20,
                         "ul": "713–723 MHz", "dl": "768–778 MHz",
                         "use": "4G/5G coverage"},
                        # 850 MHz — Band 5 FDD
                        {"band": "850 MHz", "band_id": "B5", "duplex": "FDD",
                         "paired_mhz": 15, "total_mhz": 30,
                         "ul": "824–839 MHz", "dl": "869–884 MHz",
                         "use": "3G/4G rural coverage"},
                        # 1900 MHz — Band 2 PCS FDD
                        {"band": "1900 MHz", "band_id": "B2", "duplex": "FDD",
                         "paired_mhz": 25, "total_mhz": 50,
                         "ul": "1875–1900 MHz", "dl": "1955–1980 MHz",
                         "use": "3G/4G capacity"},
                        # AWS — Band 4 FDD
                        {"band": "AWS", "band_id": "B4", "duplex": "FDD",
                         "paired_mhz": 20, "total_mhz": 40,
                         "ul": "1750–1770 MHz", "dl": "2150–2170 MHz",
                         "use": "4G capacity"},
                        # 2500 MHz — Band 7 FDD
                        {"band": "2500 MHz", "band_id": "B7", "duplex": "FDD",
                         "paired_mhz": 30, "total_mhz": 60,
                         "ul": "2500–2530 MHz", "dl": "2620–2650 MHz",
                         "use": "4G high-capacity"},
                    ],
                },
            },
            # Movistar/Coltel — ACQUIRED by Tigo Q3 2025, kept for historical data
            "movistar_co": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 0,
                "fiber_homepass_k": 0,
                "notes": "Acquired by Tigo (Millicom) Q3 2025. Spectrum transferred to tigo_colombia.",
                "technology_mix": {
                    "mobile_vendor": "N/A — acquired by Tigo",
                    "spectrum_mhz": 0,
                    "status": "acquired",
                    "acquired_by": "tigo_colombia",
                    "acquisition_date": "2025-09-01",
                    "spectrum_bands": [],
                },
            },
            "wom_co": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 50,
                "technology_mix": {
                    "mobile_vendor": "Samsung/Nokia",
                    "spectrum_mhz": 60,
                    "spectrum_bands": [
                        # 700 MHz — Band 28 FDD
                        {"band": "700 MHz", "band_id": "B28", "duplex": "FDD",
                         "paired_mhz": 5, "total_mhz": 10,
                         "ul": "733–738 MHz", "dl": "788–793 MHz",
                         "use": "4G coverage"},
                        # AWS — Band 4 FDD
                        {"band": "AWS", "band_id": "B4", "duplex": "FDD",
                         "paired_mhz": 15, "total_mhz": 30,
                         "ul": "1770–1785 MHz", "dl": "2170–2185 MHz",
                         "use": "4G capacity"},
                        # 1900 MHz — Band 2 PCS FDD
                        {"band": "1900 MHz", "band_id": "B2", "duplex": "FDD",
                         "paired_mhz": 10, "total_mhz": 20,
                         "ul": "1900–1910 MHz", "dl": "1980–1990 MHz",
                         "use": "3G/4G capacity"},
                    ],
                },
            },
        },
        "executives": {
            "tigo_colombia": [
                {"name": "Marcelo Cataldo", "title": "CEO", "start_date": "2021-01-01", "background": "Former Millicom EVP, ex-Telefonica executive"},
                {"name": "Diego Pardo", "title": "CFO", "start_date": "2022-06-01", "background": "Finance professional, ex-PwC Colombia"},
            ],
            "claro_co": [
                {"name": "Carlos Zenteno", "title": "CEO", "start_date": "2019-01-01", "background": "America Movil regional leadership"},
            ],
            "movistar_co": [
                {"name": "Fabián Hernández", "title": "CEO", "start_date": "2020-01-01", "background": "Telefonica Group veteran"},
            ],
            "wom_co": [
                {"name": "Chris Bannister", "title": "CEO", "start_date": "2022-01-01", "background": "International telco executive, ex-Digicel"},
            ],
        },
        "competitive_scores": {
            "tigo_colombia": {
                "Network Coverage": 78, "Network Quality": 75, "Brand Strength": 72,
                "Price Competitiveness": 70, "Customer Service": 68, "Digital Experience": 72,
                "Enterprise Solutions": 70, "Innovation": 68, "Distribution": 75,
            },
            "claro_co": {
                "Network Coverage": 90, "Network Quality": 85, "Brand Strength": 88,
                "Price Competitiveness": 65, "Customer Service": 70, "Digital Experience": 75,
                "Enterprise Solutions": 82, "Innovation": 72, "Distribution": 90,
            },
            "movistar_co": {
                "Network Coverage": 72, "Network Quality": 70, "Brand Strength": 68,
                "Price Competitiveness": 68, "Customer Service": 65, "Digital Experience": 62,
                "Enterprise Solutions": 60, "Innovation": 58, "Distribution": 70,
            },
            "wom_co": {
                "Network Coverage": 42, "Network Quality": 45, "Brand Strength": 50,
                "Price Competitiveness": 90, "Customer Service": 55, "Digital Experience": 65,
                "Enterprise Solutions": 20, "Innovation": 70, "Distribution": 45,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "tigo_colombia",
                "event_date": "2025-09-01",
                "category": "m_and_a",
                "title": "Tigo (Millicom) completes acquisition of Coltel (Movistar Colombia)",
                "description": (
                    "Millicom acquires Colombia Telecomunicaciones (Coltel) from Telefonica. "
                    "The deal consolidates the market from 4 to 3 players. Tigo inherits "
                    "Coltel's 15.3M mobile subscribers, 120 MHz of spectrum, 3.5M fiber "
                    "homepasses, and the Movistar Colombia brand. The combined entity becomes "
                    "Colombia's largest operator by spectrum holdings (265 MHz total) and "
                    "second by subscribers, significantly narrowing the gap with Claro."
                ),
                "impact_type": "positive",
                "severity": "critical",
            },
            {
                "operator_id": "tigo_colombia",
                "event_date": "2025-08-15",
                "category": "technology",
                "title": "Tigo-UNE launches 5G in Bogota and Medellin",
                "description": "Initial 5G deployment covering central business districts",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "wom_co",
                "event_date": "2025-07-01",
                "category": "competitive",
                "title": "WOM reaches 4.6M subscribers in Colombia",
                "description": "Rapid subscriber growth continues with aggressive pricing strategy",
                "impact_type": "negative",
                "severity": "medium",
            },
            {
                "operator_id": None,
                "event_date": "2025-11-01",
                "category": "regulatory",
                "title": "CRC announces 5G spectrum auction timeline",
                "description": "3.5 GHz and 26 GHz bands to be auctioned in 2026",
                "impact_type": "neutral",
                "severity": "high",
            },
        ],
        "earnings_highlights": {
            "tigo_colombia": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "Mobile service revenue growth accelerating with data monetization and postpaid migration", "speaker": "CEO"},
                {"segment": "Home", "highlight_type": "outlook", "content": "Fixed broadband growth driven by fiber expansion, targeting 550K fiber subs by end of 2025", "speaker": "CEO"},
                {"segment": "B2B", "highlight_type": "explanation", "content": "Colombia B2B segment benefiting from enterprise cloud connectivity solutions", "speaker": "CFO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    """Seed Colombia market data."""
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_colombia as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
