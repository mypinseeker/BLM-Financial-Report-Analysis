"""Seed the database with Colombia telecom market data.

Colombia is Millicom's largest market by revenue (Tigo-UNE).
As of Q4 2025: 4-player market — Claro (leader), Movistar/Coltel, Tigo-UNE, WOM.
Currency: COP (Colombian Peso). Millicom reports in USD.

CRITICAL TIMELINE CORRECTIONS (verified Feb 2026):
  - Q4 2025 (Oct-Dec 2025): Market was STILL 4 players. Both Millicom acquisitions
    had NOT yet closed. Tigo-UNE was still a 50% JV with EPM.
  - Jan 27, 2026: Millicom wins EPM's 50% share of Tigo-UNE at auction (~$571M / COP 2.1T).
  - Feb 5-6, 2026: Millicom closes tender offer for Telefónica's 67.5% stake in
    Coltel (Movistar Colombia) for $214.4M. Market becomes 3-player.
  - ~Apr 2026 (expected): Phase 2 — Colombian government's 32.5% Coltel stake (~$200M).

WOM STATUS: Rescued from bankruptcy by SUR Holdings (US/UK investors) in 2025.
  First positive EBITDA in Q1 2025 (COP 60B). ~7M subscribers.

Exchange rate: Q4 2025 average ~3,780-3,800 COP/USD.

Data sources: Millicom Q4 2025 earnings (2026-02-26), América Móvil Q4 2025 earnings,
CRC Colombia Q2 2025 Data Flash, ANE spectrum registry, WOM/SUR Holdings filings.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "colombia"
# During Q4 2025: 4 operators still active. Coltel acquisition closes Feb 2026.
OPERATORS = ["tigo_colombia", "claro_co", "movistar_co", "wom_co"]


def get_seed_data():
    return {
        "financials": {
            # ── Tigo-UNE Colombia (Millicom 50% JV with EPM during Q4 2025) ──
            # VERIFIED: Millicom Q4 2025 Earnings Release (2026-02-26)
            # Millicom reports FULL-YEAR 2025 only for Colombia segment:
            #   - FY 2025 Service Revenue: $389M (+6.9% YoY)
            #   - FY 2025 Adjusted EBITDA: $174M (+24.6% YoY)
            #   - FY 2025 EBITDA Margin: 44.1% (record high)
            # NOTE: Millicom does NOT disclose quarterly Colombia segment revenue.
            # NOTE: Q4 2025 is PRE-Coltel, PRE-EPM buyout (Tigo UNE only).
            "tigo_colombia": {
                # FY 2025 figures — quarterly breakdown NOT disclosed
                "fy_2025_service_revenue_usd_m": 389,
                "fy_2025_service_revenue_growth_pct": 6.9,
                "fy_2025_ebitda_usd_m": 174,
                "fy_2025_ebitda_growth_pct": 24.6,
                "fy_2025_ebitda_margin_pct": 44.1,
                # Quarterly time series: NOT disclosed at country level
                "total_revenue": [None, None, None, None, None, None, None, None],
                "ebitda": [None, None, None, None, None, None, None, None],
                # mobile_service_revenue: not disclosed separately
                # fixed_service_revenue: not disclosed separately
                # capex: not disclosed at country level
                # employees: not disclosed at country level
                "_source": "Millicom Q4 2025 Earnings Release (2026-02-26) — Colombia segment",
                "_source_url": "https://www.globenewswire.com/news-release/2026/02/26/3245346/0/en/Millicom-Tigo-Q4-2025-Earnings-Release.html",
                "_alt_source": "TeleSemana 2026-02-26",
                "_alt_source_url": "https://www.telesemana.com/blog/2026/02/26/millicom-cerro-2025-con-ingresos-estables/",
            },
            # ── Claro Colombia (América Móvil) Q4 2025 ──
            # VERIFIED: América Móvil Q4 2025 Earnings Call (Feb 2026)
            #   - Q4 Revenue: COP 4.3T (~$1.13B at ~3,800 COP/USD)
            #   - Service revenue growth: +5.4% YoY
            #   - Mobile service revenue growth: +7.6% YoY
            #   - Postpaid revenue growth: +7.8% YoY
            #   - Fixed-line service revenue growth: +2.2% YoY
            #   - Broadband revenue growth: +16.1% YoY
            #   - EBITDA growth: +4.1% reported / +6.3% organic
            #   - EBITDA margin: 41.0% (+2.2pp LTM)
            # NOTE: AMX reports in COP. Q4 2025 revenue COP 4.3T = COP 4,300B.
            "claro_co": {
                "q4_2025_revenue_cop_b": 4300,
                "q4_2025_revenue_usd_m_approx": 1132,  # derived at ~3,800 COP/USD
                "service_revenue_growth_pct_q4": 5.4,
                "mobile_service_revenue_growth_pct_q4": 7.6,
                "postpaid_revenue_growth_pct_q4": 7.8,
                "fixed_service_revenue_growth_pct_q4": 2.2,
                "broadband_revenue_growth_pct_q4": 16.1,
                "ebitda_growth_pct_q4_reported": 4.1,
                "ebitda_growth_pct_q4_organic": 6.3,
                "ebitda_margin_pct": 41.0,
                "ebitda_margin_improvement_pp_ltm": 2.2,
                # Quarterly time series: NOT disclosed for Colombia specifically
                "total_revenue": [None, None, None, None, None, None, None, 4300],
                "ebitda": [None, None, None, None, None, None, None, None],
                # capex: not disclosed at country level
                # employees: not disclosed at country level
                "_source": "América Móvil Q4 2025 Earnings Call (Feb 2026)",
                "_source_url": "https://www.americamovil.com/investors/reports-and-filings/quarterly-results/default.aspx",
                "_alt_source": "AMX Q4 2025 Earnings Call Transcript — Insider Monkey",
                "_alt_source_url": "https://www.insidermonkey.com/blog/america-movil-s-a-b-de-c-v-nyseamx-q4-2025-earnings-call-transcript-1694480/",
            },
            # ── Movistar Colombia / Coltel (Telefónica → Millicom) ──
            # STATUS: Telefónica sold 67.5% stake to Millicom, closed Feb 6, 2026.
            # Q4 2025 financials NOT published by Telefónica (sale in progress).
            "movistar_co": {
                "total_revenue": [None, None, None, None, None, None, None, None],
                "ebitda": [None, None, None, None, None, None, None, None],
                "_status": "acquired_by_millicom",
                "_acquisition_price_usd_m": 214.4,
                "_acquisition_stake_pct": 67.5,
                "_acquisition_closing_date": "2026-02-06",
                "_source": "Millicom Coltel Tender Offer PR (2026-02-05)",
                "_source_url": "https://www.globenewswire.com/news-release/2026/02/05/3233403/0/en/Millicom-Tigo-Concludes-Tender-Offer-Coltel.html",
                "_note": "Telefónica did not publish Colombia-specific Q4 2025 financials",
            },
            # ── WOM Colombia ──
            # STATUS: Rescued from bankruptcy by SUR Holdings (US/UK) in 2025.
            # Only verified data: Q1 2025 EBITDA = COP 60B (first positive ever).
            # Q4 2025 financials NOT publicly available.
            "wom_co": {
                "total_revenue": [None, None, None, None, None, None, None, None],
                "ebitda": [None, None, None, None, None, None, None, None],
                "q1_2025_ebitda_cop_b": 60,  # First positive EBITDA ever
                "q1_2024_ebitda_cop_b": -82,  # Prior year comparison
                "_status": "acquired_by_sur_holdings",
                "_sur_planned_investment_usd_m": 100,
                "_sur_invested_so_far_usd_m": 40,
                "_source": "SUR Holdings acquisition filings, América Economía, Developing Telecoms",
                "_source_url": "https://www.americaeconomia.com/en/node/290161",
                "_note": "WOM does not publish quarterly earnings publicly",
            },
        },
        "subscribers": {
            # ── Tigo-UNE Colombia (Q4 2025, PRE-Coltel) ──
            # VERIFIED: Millicom Q4 2025 Earnings Release
            "tigo_colombia": {
                "mobile_postpaid_k": 4400,  # 4.4M (+9.6% YoY)
                "mobile_postpaid_growth_pct": 9.6,
                "home_subscribers_k": 1676,  # 1,676K (+10.2% YoY)
                "home_subscribers_growth_pct": 10.2,
                "cell_sites": 10500,
                "mobile_market_share_pct": 20,  # ~20% pre-Coltel
                # mobile_total, prepaid, ARPU: NOT disclosed by Millicom at country level
                # broadband breakdown (cable/fiber): NOT disclosed
                "_source": "Millicom Q4 2025 Earnings Release (2026-02-26)",
                "_source_url": "https://www.globenewswire.com/news-release/2026/02/26/3245346/0/en/Millicom-Tigo-Q4-2025-Earnings-Release.html",
            },
            # ── Claro Colombia (Q4 2025) ──
            # VERIFIED: América Móvil Q4 2025 Earnings Call
            "claro_co": {
                "wireless_clients_k": 42700,  # 42.7M (+4.2% YoY) — includes IoT/M2M
                "wireless_growth_pct": 4.2,
                "q4_postpaid_net_adds_k": 276,
                "q4_prepaid_net_adds_k": 224,
                "q4_broadband_net_adds_k": 49,
                "q4_fixed_disconnections_k": -42,  # landline + PayTV
                # postpaid/prepaid stock breakdown: NOT disclosed at Colombia level
                # ARPU: NOT disclosed at Colombia level
                "_note": "42.7M 'wireless clients' includes IoT/M2M SIMs per AMX convention",
                "_source": "América Móvil Q4 2025 Earnings Call",
                "_source_url": "https://www.insidermonkey.com/blog/america-movil-s-a-b-de-c-v-nyseamx-q4-2025-earnings-call-transcript-1694480/",
            },
            # ── Movistar/Coltel (pre-acquisition, CRC data) ──
            "movistar_co": {
                "mobile_lines_k": 21000,  # ~21M as of Sep 2025 (CRC)
                "mobile_market_share_pct": 25,
                "broadband_market_share_pct": 17,
                "paytv_market_share_pct": 9,
                "_source": "CRC Colombia via El Colombiano / multiple sources (Sep 2025)",
                "_source_url": "https://www.elcolombiano.com/negocios/mercado-movil-colombia-millicom-compra-movistar-segundo-operador-claro-JB33239743",
                "_note": "Pre-acquisition figures. Exact subscriber stock not published in Telefónica Q4 2025.",
            },
            # ── WOM Colombia ──
            "wom_co": {
                "mobile_subscribers_k_approx": 7000,  # ~7M
                "mobile_market_share_pct": 7,
                # postpaid/prepaid breakdown: NOT disclosed
                # ARPU: NOT disclosed
                "_source": "Multiple sources — América Economía, Developing Telecoms, DCD",
                "_source_url": "https://developingtelecoms.com/telecom-business/operator-news/18805-wom-colombia-looks-forward.html",
            },
            # ── Market-level CRC data (Q2 2025 — latest available) ──
            "_market_totals": {
                "data_as_of": "Q2 2025",
                "total_mobile_lines_k": 102500,  # 102.5M (+2.8% YoY)
                "mobile_growth_pct": 2.8,
                "mobile_internet_revenue_cop_t": 2.9,  # COP 2.9T (+10.9% YoY)
                "mobile_internet_revenue_growth_pct": 10.9,
                "five_g_connections_k": 6030,  # 6.03M (12.4% of mobile internet)
                "five_g_pct_of_mobile_internet": 12.4,
                "five_g_growth_pct": 185.5,
                "mno_subscriber_growth_pct": 3.2,
                "mvno_subscriber_growth_pct": -14.1,
                "bundled_plans_k": 38000,  # 38M lines (84.8% of revenue lines)
                "bundled_plans_pct_of_revenue_lines": 84.8,
                "_market_shares_crc_sep_2025": {
                    "claro": {"mobile_lines_k": 42100, "share_pct": 44.0},
                    "movistar": {"mobile_lines_k": 21000, "share_pct": 25.0},
                    "tigo": {"mobile_lines_k": 15100, "share_pct": 18.0},
                    "wom": {"mobile_lines_k": 6400, "share_pct": 6.7},
                    "mvnos_other": {"share_pct": 6.3},
                },
                "_source": "CRC Data Flash 2025-012 (Q2 2025, published Sep 2025) + CRC press release",
                "_source_url": "https://www.postdata.gov.co/dataflash/data-flash-2025-012-servicios-moviles",
                "_alt_source_url": "https://www.crcom.gov.co/es/noticias/comunicado-prensa/conectividad-movil-en-colombia-5g-sigue-creciendo",
                "_note": "CRC Q3/Q4 2025 data NOT yet published as of Feb 2026",
            },
        },
        "macro": {
            "gdp_growth_pct": 1.8,
            "inflation_pct": 5.5,
            "unemployment_pct": 10.2,
            "population_m": 52,
            "currency": "COP",
            "exchange_rate_q4_2025": 3790,  # ~3,780-3,800 COP/USD
            "five_g_connections_k": 6030,  # CRC Q2 2025
            "regulatory_environment": "CRC pro-competition; spectrum caps; MVNOs encouraged; asymmetric regulation on Claro",
            "digital_strategy": "Colombia Digital 2030; broadband universalization; 5G roadmap announced",
            "_source": "DANE / MinTIC / CRC Colombia / IMF",
        },
        # ── Network infrastructure with detailed spectrum_bands ──
        # Q4 2025: Tigo-UNE has 145 MHz (Coltel NOT yet acquired)
        # Post-Feb 2026: Tigo will have 265 MHz (after Coltel closes)
        "network": {
            # ── Tigo-UNE Colombia: 145 MHz (Q4 2025, pre-Coltel) ──
            # Bands: 700 (B28), 1900 (B2), AWS (B4), 2500 (B41 TDD)
            "tigo_colombia": {
                "five_g_coverage_pct": 12,
                "four_g_coverage_pct": 92,
                "fiber_homepass_k": 4500,  # Tigo-UNE alone (pre-Coltel)
                "cable_homepass_k": 5200,
                "cell_sites": 10500,
                "technology_mix": {
                    "mobile_vendor": "Nokia",
                    "core_vendor": "Nokia",
                    "spectrum_mhz": 145,  # Q4 2025 PRE-Coltel
                    "notes": "Q4 2025 pre-Coltel. Post-Feb 2026 combined = 265 MHz.",
                    "spectrum_bands": [
                        # 700 MHz — Band 28 FDD (APT)
                        {"band": "700 MHz", "band_id": "B28", "duplex": "FDD",
                         "paired_mhz": 10, "total_mhz": 20,
                         "ul": "703–713 MHz", "dl": "758–768 MHz",
                         "use": "4G/5G coverage", "origin": "Tigo-UNE"},
                        # 1900 MHz — Band 2 PCS FDD
                        {"band": "1900 MHz", "band_id": "B2", "duplex": "FDD",
                         "paired_mhz": 12.5, "total_mhz": 25,
                         "ul": "1862.5–1875 MHz", "dl": "1942.5–1955 MHz",
                         "use": "3G/4G capacity", "origin": "Tigo-UNE"},
                        # AWS — Band 4 FDD
                        {"band": "AWS", "band_id": "B4", "duplex": "FDD",
                         "paired_mhz": 20, "total_mhz": 40,
                         "ul": "1710–1730 MHz", "dl": "2110–2130 MHz",
                         "use": "4G capacity", "origin": "Tigo-UNE"},
                        # 2500 MHz — Band 41 TDD
                        {"band": "2500 MHz", "band_id": "B41", "duplex": "TDD",
                         "total_mhz": 60,
                         "range": "2530–2590 MHz",
                         "use": "4G high-capacity", "origin": "Tigo-UNE"},
                    ],
                    # Post-acquisition spectrum (after Feb 2026 Coltel closing):
                    "_post_coltel_spectrum_bands": [
                        {"band": "700 MHz", "band_id": "B28", "duplex": "FDD",
                         "paired_mhz": 10, "total_mhz": 20,
                         "ul": "723–733 MHz", "dl": "778–788 MHz",
                         "use": "4G/5G coverage", "origin": "ex-Coltel"},
                        {"band": "850 MHz", "band_id": "B5", "duplex": "FDD",
                         "paired_mhz": 5, "total_mhz": 10,
                         "ul": "829–834 MHz", "dl": "874–879 MHz",
                         "use": "4G rural coverage", "origin": "ex-Coltel"},
                        {"band": "1900 MHz", "band_id": "B2", "duplex": "FDD",
                         "paired_mhz": 25, "total_mhz": 50,
                         "ul": "1850–1875 MHz", "dl": "1930–1955 MHz",
                         "use": "3G/4G capacity", "origin": "ex-Coltel"},
                        {"band": "AWS", "band_id": "B4", "duplex": "FDD",
                         "paired_mhz": 20, "total_mhz": 40,
                         "ul": "1730–1750 MHz", "dl": "2130–2150 MHz",
                         "use": "4G capacity", "origin": "ex-Coltel"},
                    ],
                    "_post_coltel_total_mhz": 265,
                },
                "_source": "ANE Colombia spectrum registry, Millicom Q4 2025 Earnings",
            },
            # ── Claro Colombia: 200 MHz ──
            "claro_co": {
                "five_g_coverage_pct": 10,
                "four_g_coverage_pct": 90,
                "fiber_homepass_k": 8000,
                "cable_homepass_k": 3000,
                "technology_mix": {
                    "mobile_vendor": "Ericsson",
                    "core_vendor": "Ericsson",
                    "spectrum_mhz": 200,
                    "spectrum_bands": [
                        {"band": "700 MHz", "band_id": "B28", "duplex": "FDD",
                         "paired_mhz": 10, "total_mhz": 20,
                         "ul": "713–723 MHz", "dl": "768–778 MHz",
                         "use": "4G/5G coverage"},
                        {"band": "850 MHz", "band_id": "B5", "duplex": "FDD",
                         "paired_mhz": 15, "total_mhz": 30,
                         "ul": "824–839 MHz", "dl": "869–884 MHz",
                         "use": "3G/4G rural coverage"},
                        {"band": "1900 MHz", "band_id": "B2", "duplex": "FDD",
                         "paired_mhz": 25, "total_mhz": 50,
                         "ul": "1875–1900 MHz", "dl": "1955–1980 MHz",
                         "use": "3G/4G capacity"},
                        {"band": "AWS", "band_id": "B4", "duplex": "FDD",
                         "paired_mhz": 20, "total_mhz": 40,
                         "ul": "1750–1770 MHz", "dl": "2150–2170 MHz",
                         "use": "4G capacity"},
                        {"band": "2500 MHz", "band_id": "B7", "duplex": "FDD",
                         "paired_mhz": 30, "total_mhz": 60,
                         "ul": "2500–2530 MHz", "dl": "2620–2650 MHz",
                         "use": "4G high-capacity"},
                    ],
                },
                "_source": "ANE Colombia spectrum registry",
            },
            # ── Movistar/Coltel: 120 MHz (Q4 2025, pre-transfer to Tigo) ──
            "movistar_co": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 85,
                "fiber_homepass_k": 3500,
                "technology_mix": {
                    "mobile_vendor": "Ericsson/Huawei",
                    "spectrum_mhz": 120,  # Still held during Q4 2025
                    "status": "pending_transfer",
                    "transfer_to": "tigo_colombia",
                    "transfer_date": "2026-02-06",
                    "spectrum_bands": [
                        {"band": "700 MHz", "band_id": "B28", "duplex": "FDD",
                         "paired_mhz": 10, "total_mhz": 20,
                         "ul": "723–733 MHz", "dl": "778–788 MHz",
                         "use": "4G coverage"},
                        {"band": "850 MHz", "band_id": "B5", "duplex": "FDD",
                         "paired_mhz": 5, "total_mhz": 10,
                         "ul": "829–834 MHz", "dl": "874–879 MHz",
                         "use": "4G rural"},
                        {"band": "1900 MHz", "band_id": "B2", "duplex": "FDD",
                         "paired_mhz": 25, "total_mhz": 50,
                         "ul": "1850–1875 MHz", "dl": "1930–1955 MHz",
                         "use": "3G/4G capacity"},
                        {"band": "AWS", "band_id": "B4", "duplex": "FDD",
                         "paired_mhz": 20, "total_mhz": 40,
                         "ul": "1730–1750 MHz", "dl": "2130–2150 MHz",
                         "use": "4G capacity"},
                    ],
                },
                "_source": "ANE Colombia spectrum registry",
                "_note": "Spectrum will transfer to Tigo upon Coltel acquisition completion (Feb 2026)",
            },
            # ── WOM Colombia: 60 MHz ──
            "wom_co": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 50,
                "technology_mix": {
                    "mobile_vendor": "Samsung/Nokia",
                    "spectrum_mhz": 60,
                    "spectrum_bands": [
                        {"band": "700 MHz", "band_id": "B28", "duplex": "FDD",
                         "paired_mhz": 5, "total_mhz": 10,
                         "ul": "733–738 MHz", "dl": "788–793 MHz",
                         "use": "4G coverage"},
                        {"band": "AWS", "band_id": "B4", "duplex": "FDD",
                         "paired_mhz": 15, "total_mhz": 30,
                         "ul": "1770–1785 MHz", "dl": "2170–2185 MHz",
                         "use": "4G capacity"},
                        {"band": "1900 MHz", "band_id": "B2", "duplex": "FDD",
                         "paired_mhz": 10, "total_mhz": 20,
                         "ul": "1900–1910 MHz", "dl": "1980–1990 MHz",
                         "use": "3G/4G capacity"},
                    ],
                },
                "_source": "ANE Colombia spectrum registry",
            },
        },
        "executives": {
            "tigo_colombia": [
                {"name": "Marcelo Cataldo", "title": "CEO", "start_date": "2021-01-01",
                 "background": "Former Millicom EVP, ex-Telefonica executive"},
            ],
            "claro_co": [
                {"name": "Carlos Zenteno", "title": "CEO", "start_date": "2019-01-01",
                 "background": "América Móvil regional leadership"},
            ],
            "movistar_co": [
                {"name": "Fabián Hernández", "title": "CEO", "start_date": "2020-01-01",
                 "background": "Telefonica Group veteran (pre-acquisition)"},
            ],
            "wom_co": [
                {"name": "Chris Bannister", "title": "CEO", "start_date": "2022-01-01",
                 "background": "International telco executive, ex-Digicel; SUR Holdings era"},
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
                "event_date": "2026-01-27",
                "category": "m_and_a",
                "title": "Millicom wins EPM's 50% share of Tigo-UNE at auction (~$571M)",
                "description": (
                    "Millicom wins the auction for EPM's remaining 50% stake in "
                    "Tigo-UNE for approximately COP 2.1 trillion (~$571M). This gives "
                    "Millicom 100% ownership of Tigo Colombia operations."
                ),
                "impact_type": "positive",
                "severity": "critical",
                "_source": "Millicom Q4 2025 Earnings Release",
                "_source_url": "https://www.globenewswire.com/news-release/2026/02/26/3245346/0/en/Millicom-Tigo-Q4-2025-Earnings-Release.html",
            },
            {
                "operator_id": "tigo_colombia",
                "event_date": "2026-02-06",
                "category": "m_and_a",
                "title": "Millicom closes acquisition of Telefónica's 67.5% stake in Coltel for $214.4M",
                "description": (
                    "Millicom completes tender offer for Telefónica's controlling stake "
                    "in Colombia Telecomunicaciones (Coltel / Movistar Colombia). "
                    "Combined entity will hold 265 MHz spectrum, ~36-41M mobile lines, "
                    "~43% mobile market share. Phase 2 (government's 32.5%) expected ~Apr 2026."
                ),
                "impact_type": "positive",
                "severity": "critical",
                "_source": "Millicom Coltel Tender Offer PR (2026-02-05)",
                "_source_url": "https://www.globenewswire.com/news-release/2026/02/05/3233403/0/en/Millicom-Tigo-Concludes-Tender-Offer-Coltel.html",
            },
            {
                "operator_id": "wom_co",
                "event_date": "2025-06-01",
                "category": "m_and_a",
                "title": "SUR Holdings (US/UK) acquires WOM Colombia from bankruptcy",
                "description": (
                    "SUR Holdings consortium rescues WOM Colombia, planning $100M "
                    "investment. WOM achieves first positive EBITDA (COP 60B) in Q1 2025. "
                    "Government grants 3-year grace period on spectrum payments."
                ),
                "impact_type": "neutral",
                "severity": "high",
                "_source": "América Economía, Developing Telecoms",
                "_source_url": "https://www.americaeconomia.com/en/node/290161",
            },
            {
                "operator_id": None,
                "event_date": "2025-09-01",
                "category": "regulatory",
                "title": "CRC publishes Q2 2025 mobile data: 102.5M lines, 6.03M 5G connections",
                "description": (
                    "CRC Data Flash 2025-012 shows 102.5M total mobile lines (+2.8% YoY), "
                    "6.03M 5G connections (12.4% of mobile internet, +185.5% YoY). "
                    "Mobile internet revenue COP 2.9T (+10.9%)."
                ),
                "impact_type": "neutral",
                "severity": "medium",
                "_source": "CRC Data Flash 2025-012",
                "_source_url": "https://www.postdata.gov.co/dataflash/data-flash-2025-012-servicios-moviles",
            },
        ],
        "earnings_highlights": {
            "tigo_colombia": [
                {"segment": "Overall", "highlight_type": "guidance",
                 "content": "Colombia FY 2025: record EBITDA margin of 44.1%, service revenue +6.9%. "
                            "Coltel acquisition (closed Feb 2026) to create combined #2 operator.",
                 "speaker": "Millicom Q4 2025 Earnings",
                 "_source_url": "https://www.globenewswire.com/news-release/2026/02/26/3245346/0/en/Millicom-Tigo-Q4-2025-Earnings-Release.html"},
            ],
            "claro_co": [
                {"segment": "Colombia", "highlight_type": "guidance",
                 "content": "Colombia Q4 2025: service revenue +5.4%, mobile +7.6%, broadband +16.1%. "
                            "EBITDA margin 41.0% (+2.2pp LTM). Wireless clients 42.7M (+4.2%).",
                 "speaker": "AMX Q4 2025 Earnings Call",
                 "_source_url": "https://www.insidermonkey.com/blog/america-movil-s-a-b-de-c-v-nyseamx-q4-2025-earnings-call-transcript-1694480/"},
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
