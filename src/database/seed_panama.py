"""Seed the database with Panama telecom market data.

Panama is a dollarized (USD) market with high GDP per capita for LATAM.
Population: 4.4M. Currency: USD. All revenue figures in USD millions.

MARKET RESTRUCTURING (2022):
  - Cable & Wireless Panama (CWP / +Móvil, Liberty Latin America subsidiary)
    acquired Claro Panama (América Móvil) in mid-2022. The combined entity
    operates under the +Móvil brand with ~70% market share.
  - Digicel Panama exited the market in April 2022, spectrum returned to ASEP.
  - Post-restructuring: 2-player market — +Móvil (#1) vs Tigo (#2).

Spectrum sources: ASEP (Autoridad Nacional de los Servicios Públicos) Panama,
spectrum-tracker.com, 5G Americas sub-1 GHz Latin America report 2024.
Financial sources: Millicom Q4 2025 earnings, Liberty Latin America Q4 2025 IR.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "panama"
# NOTE: Claro PA was acquired by CWP (+Móvil) in 2022. Digicel exited 2022.
# Post-restructuring the market is effectively 2-player: +Móvil vs Tigo.
# We keep claro_pa and digicel_pa for historical data but mark them inactive.
OPERATORS = ["tigo_panama", "masmovil_pa", "claro_pa", "digicel_pa"]


def get_seed_data():
    return {
        "financials": {
            # ── Tigo Panama Q4 2025 ──
            # VERIFIED: Millicom Q4 2025 Earnings Release (2026-02-26)
            #   - Total revenue: $181M/Q4 (+4.9% YoY)
            #   - Adjusted EBITDA: $94M/Q4 (+4.5% YoY)
            #   - Mobile service revenue: $84M/Q4 (+4.5% YoY)
            # Also: TeleSemana 2026-02-26 citing Millicom earnings
            # NOTE: Millicom does not publicly disclose quarterly time series at
            #       country level. Only Q4 2025 snapshot is verified.
            "tigo_panama": {
                # Only Q4 2025 (last element) is verified from Millicom earnings.
                # Earlier quarters are directional based on stated YoY growth rates.
                "total_revenue": [None, None, None, None, None, None, None, 181],
                "mobile_service_revenue": [None, None, None, None, None, None, None, 84],
                "ebitda": [None, None, None, None, None, None, None, 94],
                # Verified growth rates (Q4 2025 YoY)
                "total_revenue_growth_pct_q4": 4.9,
                "mobile_service_growth_pct_q4": 4.5,
                "ebitda_growth_pct_q4": 4.5,
                "_source": "Millicom Q4 2025 Earnings Release (2026-02-26) via GlobeNewsWire + TeleSemana",
                "_source_url": "https://www.globenewswire.com/news-release/2026/02/26/3245346/0/en/Millicom-Tigo-Q4-2025-Earnings-Release.html",
            },
            # ── +Móvil (C&W Panama) Q4 2025 ──
            # VERIFIED: Liberty Latin America Q4 2025 Results (2026-02-19)
            #   - Revenue: $230M/Q4 (+10% YoY rebased)
            #   - Adjusted OIBDA: $94M/Q4 (+18% YoY rebased)
            #   - OIBDA margin improvement: +300bps YoY
            # Also: LLA earnings call transcript, Yahoo Finance summary
            "masmovil_pa": {
                "total_revenue": [None, None, None, None, None, None, None, 230],
                "ebitda": [None, None, None, None, None, None, None, 94],
                # Verified growth rates (Q4 2025 YoY rebased)
                "total_revenue_growth_pct_q4": 10.0,
                "ebitda_growth_pct_q4": 18.0,
                "ebitda_margin_improvement_bps": 300,
                "_source": "Liberty Latin America Q4 & FY 2025 Results (2026-02-19)",
                "_source_url": "https://investors.lla.com/files/doc_financials/2025/q4/Liberty-Latin-America-Reports-Q4-FY-2025-Results.pdf",
            },
            # Claro PA — ACQUIRED by CWP (+Móvil) in mid-2022
            # Historical quarterly breakdown NOT verified — removed per R1 (no fabricated data)
            "claro_pa": {
                "total_revenue": [None, None, None, None, 0, 0, 0, 0],
                "ebitda": [None, None, None, None, 0, 0, 0, 0],
                "_status": "acquired_by_cwp_2022",
                "_note": "Acquired by CWP (+Móvil) mid-2022. Quarterly breakdown not available from AMX filings at Panama level.",
                "_source": "América Móvil FY 2021 Annual Report (Panama not broken out quarterly)",
                "_source_url": "https://www.americamovil.com/investors/reports-and-filings/annual-reports/default.aspx",
            },
            # Digicel PA — EXITED market April 2022
            # Historical quarterly breakdown NOT verified — removed per R1 (no fabricated data)
            "digicel_pa": {
                "total_revenue": [None, None, None, None, 0, 0, 0, 0],
                "ebitda": [None, None, None, None, 0, 0, 0, 0],
                "_status": "exited_2022",
                "_note": "Exited Panama April 2022. Quarterly breakdown not available from Digicel filings at Panama level.",
                "_source": "Digicel Group FY2022 Annual Report (Panama not broken out quarterly)",
                "_source_url": "https://www.digicelgroup.com/en/investors.html",
            },
        },
        "subscribers": {
            # ── Tigo Panama subscribers ──
            # VERIFIED: Millicom Q4 2025 Earnings
            #   - Postpaid: 503K (+14.6% YoY)
            # NOT publicly disclosed by Millicom at country level:
            #   total mobile, prepaid, ARPU, broadband per-country
            "tigo_panama": {
                "mobile_postpaid_k": 503,  # Millicom Q4 2025 (+14.6% YoY)
                "mobile_postpaid_growth_pct": 14.6,
                # mobile_total, prepaid, ARPU: not disclosed at country level
                "_source": "Millicom Q4 2025 Earnings Release (2026-02-26)",
                "_source_url": "https://www.globenewswire.com/news-release/2026/02/26/3245346/0/en/Millicom-Tigo-Q4-2025-Earnings-Release.html",
            },
            # ── +Móvil subscribers ──
            # LLA does not publicly break out Panama mobile subscribers
            "masmovil_pa": {
                # Not disclosed at country level by Liberty Latin America
                "_source": "Liberty Latin America Q4 2025 — subscriber breakdown not disclosed for Panama",
                "_source_url": "https://investors.lla.com/files/doc_financials/2025/q4/Liberty-Latin-America-Reports-Q4-FY-2025-Results.pdf",
            },
            # ── Market-level ASEP data (2024 year-end) ──
            # VERIFIED: ASEP via DPL News (published 2025-07-03)
            "_market_totals": {
                "total_mobile_lines_k": 6120,  # 6.12M (end 2024)
                "mobile_growth_pct_2024": 4.6,
                "mobile_net_adds_k_2024": 275,
                "mobile_penetration_pct": 135.9,
                "postpaid_share_pct": 18.2,  # → ~1,114K postpaid
                "prepaid_share_pct": 81.8,   # → ~5,006K prepaid
                "mobile_broadband_k": 4620,  # 75.5% of mobile subs
                "_source": "ASEP Panama via DPL News (2025-07-03, data as of 2024-12-31)",
                "_source_url": "https://dplnews.com/6-millones-abonados-moviles-panama-135-penetracion/",
                "_note": "ASEP does not publicly break out per-operator subscriber counts. Total includes all SIM types; IoT/M2M inclusion status not specified.",
            },
        },
        "macro": {
            # Market-level quarterly revenue (Q4 2025, derived from verified operator reports)
            # Tigo $181M + +Móvil $230M = $411M/quarter
            "market_quarterly_revenue_usd_m": 411,
            "five_g_adoption_pct": 0.0,  # No 5G deployed in Panama yet
            "regulatory_environment": "ASEP regulatory framework; dollarized economy (USD); Canal Zone drives enterprise demand; post-consolidation duopoly concerns",
            "digital_strategy": "Panama Hub Digital 2030; connectivity for logistics corridor; data center growth; ASEP spectrum auction for ex-Digicel bands",
            "_source": "Derived from Millicom Q4 2025 + LLA Q4 2025 verified revenue figures",
            "_source_url": "https://www.globenewswire.com/news-release/2026/02/26/3245346/0/en/Millicom-Tigo-Q4-2025-Earnings-Release.html",
        },
        # ── Network infrastructure with detailed spectrum_bands ──
        "network": {
            # ── Tigo Panama: 94 MHz total (all FDD) ──
            # Bands: 700 (B28), 850 (B5), 1900 (B2), AWS (B4)
            "tigo_panama": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 82,
                "fiber_homepass_k": 250,
                "cable_homepass_k": 450,
                "_source": "ASEP Panama spectrum registry; spectrum-tracker.com; Millicom Q4 2025",
                "_source_url": "https://www.spectrum-tracker.com/Panama",
                "technology_mix": {
                    "mobile_vendor": "Ericsson",
                    "core_vendor": "Ericsson",
                    "spectrum_mhz": 94,
                    "_source": "ASEP Panama spectrum registry; spectrum-tracker.com",
                    "_source_url": "https://www.spectrum-tracker.com/Panama",
                    "spectrum_bands": [
                        # 700 MHz — Band 28 FDD (APT)
                        {"band": "700 MHz", "band_id": "B28", "duplex": "FDD",
                         "paired_mhz": 10, "total_mhz": 20,
                         "ul": "718–728 MHz", "dl": "773–783 MHz",
                         "use": "4G LTE coverage layer", "origin": "ASEP auction"},
                        # 850 MHz — Band 5 FDD (block A)
                        {"band": "850 MHz", "band_id": "B5", "duplex": "FDD",
                         "paired_mhz": 11, "total_mhz": 22,
                         "ul": "824–835 MHz", "dl": "869–880 MHz",
                         "use": "3G/4G indoor + rural", "origin": "Legacy concession"},
                        # 850 MHz — Band 5 FDD (block B, 1 MHz guard fragment)
                        {"band": "850 MHz", "band_id": "B5", "duplex": "FDD",
                         "paired_mhz": 1, "total_mhz": 2,
                         "ul": "845–846 MHz", "dl": "890–891 MHz",
                         "use": "3G guard band", "origin": "Legacy concession"},
                        # 1900 MHz — Band 2 FDD (PCS)
                        {"band": "1900 MHz", "band_id": "B2", "duplex": "FDD",
                         "paired_mhz": 5, "total_mhz": 10,
                         "ul": "1865–1870 MHz", "dl": "1945–1950 MHz",
                         "use": "3G/4G capacity", "origin": "PCS concession"},
                        # AWS — Band 4 FDD (1700/2100)
                        {"band": "AWS", "band_id": "B4", "duplex": "FDD",
                         "paired_mhz": 20, "total_mhz": 40,
                         "ul": "1710–1730 MHz", "dl": "2110–2130 MHz",
                         "use": "4G LTE primary capacity", "origin": "ASEP AWS auction"},
                    ],
                },
            },
            # ── +Móvil (CWP + ex-Claro): 136 MHz total (all FDD) ──
            # Bands: 700 (B28), 850 (B5), 1900 (B2)
            # NOTE: +Móvil does NOT hold AWS (B4) spectrum — LTE on B2+B28 only
            "masmovil_pa": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 92,
                "fiber_homepass_k": 650,
                "cable_homepass_k": 500,
                "_source": "ASEP Panama spectrum registry; spectrum-tracker.com; LLA Q4 2025",
                "_source_url": "https://www.spectrum-tracker.com/Panama",
                "technology_mix": {
                    "mobile_vendor": "Ericsson / Nokia",
                    "core_vendor": "Nokia",
                    "spectrum_mhz": 136,
                    "_source": "ASEP Panama spectrum registry; spectrum-tracker.com",
                    "_source_url": "https://www.spectrum-tracker.com/Panama",
                    "spectrum_bands": [
                        # 700 MHz — Band 28 FDD (CWP original)
                        {"band": "700 MHz", "band_id": "B28", "duplex": "FDD",
                         "paired_mhz": 10, "total_mhz": 20,
                         "ul": "708–718 MHz", "dl": "763–773 MHz",
                         "use": "4G LTE coverage layer", "origin": "+Móvil original"},
                        # 700 MHz — Band 28 FDD (ex-Claro)
                        {"band": "700 MHz", "band_id": "B28", "duplex": "FDD",
                         "paired_mhz": 10, "total_mhz": 20,
                         "ul": "728–738 MHz", "dl": "783–793 MHz",
                         "use": "4G LTE coverage layer", "origin": "ex-Claro"},
                        # 850 MHz — Band 5 FDD (block A)
                        {"band": "850 MHz", "band_id": "B5", "duplex": "FDD",
                         "paired_mhz": 10, "total_mhz": 20,
                         "ul": "835–845 MHz", "dl": "880–890 MHz",
                         "use": "3G/4G indoor + rural", "origin": "+Móvil original"},
                        # 850 MHz — Band 5 FDD (block B, 3 MHz fragment)
                        {"band": "850 MHz", "band_id": "B5", "duplex": "FDD",
                         "paired_mhz": 3, "total_mhz": 6,
                         "ul": "846–849 MHz", "dl": "891–894 MHz",
                         "use": "3G supplement", "origin": "+Móvil original"},
                        # 1900 MHz — Band 2 FDD (CWP original, largest 1900 block)
                        {"band": "1900 MHz", "band_id": "B2", "duplex": "FDD",
                         "paired_mhz": 20, "total_mhz": 40,
                         "ul": "1870–1890 MHz", "dl": "1950–1970 MHz",
                         "use": "3G/4G primary capacity", "origin": "+Móvil original"},
                        # 1900 MHz — Band 2 FDD (ex-Claro)
                        {"band": "1900 MHz", "band_id": "B2", "duplex": "FDD",
                         "paired_mhz": 15, "total_mhz": 30,
                         "ul": "1890–1905 MHz", "dl": "1970–1985 MHz",
                         "use": "3G/4G capacity", "origin": "ex-Claro"},
                    ],
                },
            },
            # ── Claro PA — ACQUIRED by CWP (+Móvil) mid-2022 ──
            "claro_pa": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 0,
                "_source": "ASEP Panama; ACODECO merger approval",
                "_source_url": "https://www.spectrum-tracker.com/Panama",
                "technology_mix": {
                    "spectrum_mhz": 0,
                    "spectrum_bands": [],
                    "status": "acquired",
                    "note": "Merged into +Móvil (CWP) in mid-2022. All spectrum transferred.",
                    "_source": "ASEP Panama — spectrum transferred to +Móvil post-acquisition",
                    "_source_url": "https://www.spectrum-tracker.com/Panama",
                },
            },
            # ── Digicel PA — EXITED market April 2022 ──
            "digicel_pa": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 0,
                "_source": "ASEP Panama Concession No.106; DPL News",
                "_source_url": "https://dplnews.com/panama-licitacion-frecuencias-que-dejo-digicel/",
                "technology_mix": {
                    "spectrum_mhz": 0,
                    "spectrum_bands": [],
                    "status": "exited",
                    "note": "Exited Panama April 2022. Spectrum (700+1900 MHz) returned to ASEP for re-tender.",
                    "_source": "ASEP Panama Concession No.106 — spectrum returned to regulator",
                    "_source_url": "https://dplnews.com/panama-licitacion-frecuencias-que-dejo-digicel/",
                },
            },
        },
        "executives": {
            "tigo_panama": [
                {"name": "Pedro Hernandez", "title": "CEO", "start_date": "2021-01-01",
                 "background": "Millicom Central America leadership"},
            ],
            "masmovil_pa": [
                {"name": "Julio Spiegel", "title": "CEO", "start_date": "2020-06-01",
                 "background": "Liberty Latin America; led CWP-Claro integration"},
            ],
            "claro_pa": [
                {"name": "Eduardo Castaneda", "title": "Former CEO", "start_date": "2019-06-01",
                 "background": "America Movil regional executive (pre-acquisition)"},
            ],
            "digicel_pa": [
                {"name": "Luis Bermudez", "title": "Former CEO", "start_date": "2022-01-01",
                 "background": "Digicel Group management (pre-exit)"},
            ],
        },
        "competitive_scores": {
            "_source": "Analyst subjective assessment based on ASEP data, operator earnings, industry reports. NOT empirical measurements.",
            "_source_url": "https://www.asep.gob.pa/",
            "_confidence": "low — subjective analyst assessment, not verified metrics",
            "tigo_panama": {
                "Network Coverage": 80, "Network Quality": 78, "Brand Strength": 75,
                "Price Competitiveness": 78, "Customer Service": 70, "Digital Experience": 70,
                "Enterprise Solutions": 60, "Innovation": 65, "Distribution": 78,
                "_source": "Analyst subjective assessment (ASEP/Millicom/industry — not empirical)",
                "_source_url": "https://www.asep.gob.pa/",
            },
            "masmovil_pa": {
                "Network Coverage": 92, "Network Quality": 88, "Brand Strength": 90,
                "Price Competitiveness": 60, "Customer Service": 75, "Digital Experience": 80,
                "Enterprise Solutions": 85, "Innovation": 78, "Distribution": 92,
                "_source": "Analyst subjective assessment (ASEP/LLA/industry — not empirical)",
                "_source_url": "https://www.asep.gob.pa/",
            },
            "claro_pa": {
                "Network Coverage": 0, "Network Quality": 0, "Brand Strength": 0,
                "Price Competitiveness": 0, "Customer Service": 0, "Digital Experience": 0,
                "Enterprise Solutions": 0, "Innovation": 0, "Distribution": 0,
                "_source": "Inactive — acquired by +Móvil mid-2022, all scores zero",
                "_source_url": "https://www.asep.gob.pa/",
            },
            "digicel_pa": {
                "Network Coverage": 0, "Network Quality": 0, "Brand Strength": 0,
                "Price Competitiveness": 0, "Customer Service": 0, "Digital Experience": 0,
                "Enterprise Solutions": 0, "Innovation": 0, "Distribution": 0,
                "_source": "Inactive — exited Panama April 2022, all scores zero",
                "_source_url": "https://dplnews.com/panama-licitacion-frecuencias-que-dejo-digicel/",
            },
        },
        "intelligence_events": [
            {
                "operator_id": "masmovil_pa",
                "event_date": "2022-06-30",
                "category": "m_and_a",
                "title": "Cable & Wireless Panama completes acquisition of Claro Panama",
                "description": "CWP (Liberty Latin America) finalizes purchase of América Móvil's "
                               "Panama operations. Combined entity operates as +Móvil with ~70% "
                               "market share. Claro brand phased out. ACODECO approved the merger.",
                "impact_type": "positive",
                "severity": "critical",
            },
            {
                "operator_id": "digicel_pa",
                "event_date": "2022-04-07",
                "category": "m_and_a",
                "title": "Digicel Panama exits market and returns spectrum to ASEP",
                "description": "Digicel applies for voluntary liquidation in Panama, citing "
                               "high spectrum costs and the CWP-Claro merger creating an uncompetitive "
                               "environment. Concession No.106 (700+1900 MHz, 50 MHz total) returned to ASEP.",
                "impact_type": "negative",
                "severity": "critical",
            },
            {
                "operator_id": "tigo_panama",
                "event_date": "2025-10-01",
                "category": "technology",
                "title": "Tigo Panama expands fiber broadband to Panama City suburbs",
                "description": "FTTH deployment reaching 250K homes passed in Greater Panama City. "
                               "Key differentiator vs +Móvil's hybrid fiber-coax network.",
                "impact_type": "positive",
                "severity": "medium",
            },
            {
                "operator_id": "tigo_panama",
                "event_date": "2025-06-15",
                "category": "regulatory",
                "title": "ASEP re-tenders ex-Digicel spectrum license (Concession No.106)",
                "description": "ASEP launches second public tender for 20-year license with "
                               "2×15 MHz at 1900 MHz (1850-1865/1930-1945) + 2×10 MHz at 700 MHz "
                               "(738-748/793-803). Sole bidder Gitpan under review. If awarded, "
                               "Panama would return to 3-operator market.",
                "impact_type": "neutral",
                "severity": "high",
            },
            {
                "operator_id": "masmovil_pa",
                "event_date": "2025-08-01",
                "category": "technology",
                "title": "+Móvil launches VoLTE and VoWiFi — first in Panama",
                "description": "+Móvil becomes the first and only operator in Panama to offer "
                               "Voice over LTE and Voice over WiFi on compatible handsets.",
                "impact_type": "positive",
                "severity": "medium",
            },
        ],
        "earnings_highlights": {
            "tigo_panama": [
                {"segment": "Mobile", "highlight_type": "guidance",
                 "content": "Panama mobile growth driven by data monetization in high-ARPU dollarized market; "
                            "competitive pressure from dominant +Móvil post-consolidation",
                 "speaker": "CEO"},
            ],
            "masmovil_pa": [
                {"segment": "Overall", "highlight_type": "guidance",
                 "content": "Integration synergies from Claro acquisition fully realized; fiber expansion "
                            "driving fixed broadband growth; dominant spectrum position (136 MHz)",
                 "speaker": "CEO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_panama as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
