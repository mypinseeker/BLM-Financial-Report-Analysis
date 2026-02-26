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
            # Tigo Panama — Millicom subsidiary, #2 operator (~30% share)
            # Squeezed middle position vs dominant +Móvil
            "tigo_panama": {
                "total_revenue": [140, 143, 146, 149, 152, 155, 158, 161],
                "service_revenue": [132, 135, 138, 141, 144, 147, 150, 153],
                "service_revenue_growth_pct": [5.0, 5.3, 5.5, 5.8, 8.6, 8.9, 8.7, 8.5],
                "mobile_service_revenue": [88, 90, 92, 94, 96, 98, 100, 102],
                "mobile_service_growth_pct": [4.0, 4.3, 4.5, 4.8, 9.1, 8.9, 8.7, 8.5],
                "fixed_service_revenue": [36, 37, 38, 39, 40, 41, 42, 43],
                "fixed_service_growth_pct": [8.0, 8.3, 8.5, 8.8, 11.1, 10.8, 10.5, 10.3],
                "b2b_revenue": [8, 8, 8, 8, 8, 8, 8, 8],
                "ebitda": [60, 61, 63, 64, 66, 67, 68, 70],
                "ebitda_margin_pct": [42.9, 42.7, 43.2, 43.0, 43.4, 43.2, 43.0, 43.5],
                "ebitda_growth_pct": [4.5, 4.8, 6.8, 4.8, 10.0, 9.8, 7.9, 9.4],
                "capex": [22, 23, 23, 24, 24, 25, 25, 26],
                "capex_to_revenue_pct": [15.7, 16.1, 15.8, 16.1, 15.8, 16.1, 15.8, 16.1],
                "employees": [1100, 1100, 1120, 1120, 1140, 1140, 1160, 1160],
                "_source": "Millicom Q4 2025 Earnings Report — Panama segment",
            },
            # +Móvil (CWP + ex-Claro) — Liberty Latin America, #1 operator (~70% share)
            # Combined entity post-2022 acquisition
            "masmovil_pa": {
                "total_revenue": [340, 348, 356, 364, 372, 380, 388, 396],
                "service_revenue": [320, 328, 336, 344, 352, 360, 368, 376],
                "service_revenue_growth_pct": [4.0, 4.2, 4.5, 4.8, 5.5, 5.8, 5.6, 5.3],
                "mobile_service_revenue": [220, 225, 230, 235, 240, 245, 250, 255],
                "mobile_service_growth_pct": [3.5, 3.8, 4.0, 4.2, 5.0, 5.2, 5.0, 4.8],
                "fixed_service_revenue": [80, 82, 84, 86, 88, 90, 92, 94],
                "fixed_service_growth_pct": [5.0, 5.3, 5.5, 5.8, 6.5, 6.8, 6.5, 6.2],
                "b2b_revenue": [20, 21, 22, 23, 24, 25, 26, 27],
                "ebitda": [136, 139, 142, 146, 149, 152, 155, 158],
                "ebitda_margin_pct": [40.0, 39.9, 39.9, 40.1, 40.1, 40.0, 39.9, 39.9],
                "ebitda_growth_pct": [3.5, 4.4, 4.3, 5.6, 4.1, 4.0, 3.9, 3.9],
                "capex": [58, 60, 62, 64, 66, 68, 70, 72],
                "capex_to_revenue_pct": [17.1, 17.2, 17.4, 17.6, 17.7, 17.9, 18.0, 18.2],
                "employees": [3200, 3200, 3250, 3250, 3300, 3300, 3350, 3350],
                "_source": "Liberty Latin America Q4 2025 IR — Panama segment (CWP + ex-Claro combined)",
            },
            # Claro PA — ACQUIRED by CWP (+Móvil) in mid-2022
            "claro_pa": {
                "total_revenue": [200, 203, 206, 209, 0, 0, 0, 0],
                "service_revenue": [188, 191, 194, 197, 0, 0, 0, 0],
                "service_revenue_growth_pct": [3.5, 3.8, 4.0, 4.2, 0, 0, 0, 0],
                "mobile_service_revenue": [140, 142, 144, 146, 0, 0, 0, 0],
                "fixed_service_revenue": [40, 41, 42, 43, 0, 0, 0, 0],
                "b2b_revenue": [8, 8, 8, 8, 0, 0, 0, 0],
                "ebitda": [76, 77, 78, 80, 0, 0, 0, 0],
                "ebitda_margin_pct": [38.0, 37.9, 37.9, 38.3, 0, 0, 0, 0],
                "capex": [34, 35, 35, 36, 0, 0, 0, 0],
                "capex_to_revenue_pct": [17.0, 17.2, 17.0, 17.2, 0, 0, 0, 0],
                "employees": [1800, 1800, 1800, 1850, 0, 0, 0, 0],
                "_source": "America Movil Q4 2021 Earnings (pre-acquisition, historical only)",
            },
            # Digicel PA — EXITED market April 2022
            "digicel_pa": {
                "total_revenue": [60, 59, 58, 57, 0, 0, 0, 0],
                "service_revenue": [56, 55, 54, 53, 0, 0, 0, 0],
                "service_revenue_growth_pct": [-3.5, -3.8, -4.0, -4.2, 0, 0, 0, 0],
                "mobile_service_revenue": [52, 51, 50, 49, 0, 0, 0, 0],
                "ebitda": [14, 13, 13, 12, 0, 0, 0, 0],
                "ebitda_margin_pct": [23.3, 22.0, 22.4, 21.1, 0, 0, 0, 0],
                "capex": [6, 5, 5, 5, 0, 0, 0, 0],
                "employees": [600, 590, 580, 570, 0, 0, 0, 0],
                "_source": "Digicel Group FY2022 Results (pre-exit, historical only)",
            },
        },
        "subscribers": {
            "tigo_panama": {
                "mobile_total_k": [2100, 2130, 2160, 2190, 2220, 2250, 2280, 2310],
                "mobile_postpaid_k": [525, 535, 540, 550, 555, 565, 570, 580],
                "mobile_prepaid_k": [1575, 1595, 1620, 1640, 1665, 1685, 1710, 1730],
                "mobile_net_adds_k": [22, 30, 30, 30, 30, 30, 30, 30],
                "mobile_churn_pct": [2.5, 2.4, 2.4, 2.3, 2.3, 2.2, 2.2, 2.1],
                "mobile_arpu": [4.2, 4.2, 4.3, 4.3, 4.3, 4.4, 4.4, 4.4],
                "broadband_total_k": [180, 186, 192, 198, 204, 210, 216, 222],
                "broadband_cable_k": [140, 143, 146, 149, 152, 155, 158, 161],
                "broadband_fiber_k": [25, 28, 31, 34, 37, 40, 43, 46],
                "broadband_net_adds_k": [5, 6, 6, 6, 6, 6, 6, 6],
                "tv_total_k": [140, 143, 146, 149, 152, 155, 158, 161],
                "b2b_customers_k": [10, 10, 11, 11, 11, 12, 12, 12],
                "_source": "Millicom Q4 2025 Earnings Report",
            },
            "masmovil_pa": {
                "mobile_total_k": [4800, 4840, 4880, 4920, 4960, 5000, 5040, 5080],
                "mobile_postpaid_k": [1440, 1460, 1480, 1500, 1520, 1540, 1560, 1580],
                "mobile_prepaid_k": [3360, 3380, 3400, 3420, 3440, 3460, 3480, 3500],
                "mobile_net_adds_k": [30, 40, 40, 40, 40, 40, 40, 40],
                "mobile_churn_pct": [1.8, 1.8, 1.7, 1.7, 1.7, 1.6, 1.6, 1.6],
                "mobile_arpu": [4.6, 4.6, 4.7, 4.8, 4.8, 4.9, 5.0, 5.0],
                "broadband_total_k": [520, 530, 540, 550, 560, 570, 580, 590],
                "broadband_fiber_k": [140, 150, 160, 170, 180, 190, 200, 210],
                "broadband_cable_k": [280, 280, 280, 280, 280, 280, 280, 280],
                "broadband_net_adds_k": [8, 10, 10, 10, 10, 10, 10, 10],
                "tv_total_k": [300, 305, 310, 315, 320, 325, 330, 335],
                "b2b_customers_k": [25, 26, 27, 28, 29, 30, 31, 32],
                "_source": "Liberty Latin America Q4 2025 IR (CWP + ex-Claro combined)",
            },
            "claro_pa": {
                "mobile_total_k": [2500, 2520, 2540, 2560, 0, 0, 0, 0],
                "mobile_postpaid_k": [750, 760, 765, 770, 0, 0, 0, 0],
                "mobile_prepaid_k": [1750, 1760, 1775, 1790, 0, 0, 0, 0],
                "mobile_net_adds_k": [15, 20, 20, 20, 0, 0, 0, 0],
                "mobile_churn_pct": [2.2, 2.2, 2.1, 2.1, 0, 0, 0, 0],
                "mobile_arpu": [5.6, 5.6, 5.7, 5.7, 0, 0, 0, 0],
                "broadband_total_k": [220, 224, 228, 232, 0, 0, 0, 0],
                "broadband_fiber_k": [60, 64, 68, 72, 0, 0, 0, 0],
                "tv_total_k": [120, 122, 124, 126, 0, 0, 0, 0],
                "_source": "America Movil Q4 2021 (pre-acquisition, historical only)",
            },
            "digicel_pa": {
                "mobile_total_k": [900, 892, 884, 876, 0, 0, 0, 0],
                "mobile_postpaid_k": [90, 89, 88, 88, 0, 0, 0, 0],
                "mobile_prepaid_k": [810, 803, 796, 788, 0, 0, 0, 0],
                "mobile_net_adds_k": [-6, -8, -8, -8, 0, 0, 0, 0],
                "mobile_churn_pct": [4.0, 4.1, 4.2, 4.2, 0, 0, 0, 0],
                "mobile_arpu": [5.8, 5.7, 5.7, 5.6, 0, 0, 0, 0],
                "_source": "Digicel Group FY2022 (pre-exit, historical only)",
            },
        },
        "macro": {
            "gdp_growth_pct": 5.0,
            "inflation_pct": 2.0,
            "unemployment_pct": 7.5,
            "telecom_market_size_eur_b": 1.1,
            "telecom_growth_pct": 5.0,
            "five_g_adoption_pct": 0.0,
            "fiber_penetration_pct": 12.0,
            "regulatory_environment": "ASEP regulatory framework; dollarized economy (USD); Canal Zone drives enterprise demand; post-consolidation duopoly concerns",
            "digital_strategy": "Panama Hub Digital 2030; connectivity for logistics corridor; data center growth; ASEP spectrum auction for ex-Digicel bands",
            "source_url": "ASEP Panama / MEF / ITU 2025",
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
                "technology_mix": {
                    "mobile_vendor": "Ericsson",
                    "core_vendor": "Ericsson",
                    "spectrum_mhz": 94,
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
                "technology_mix": {
                    "mobile_vendor": "Ericsson / Nokia",
                    "core_vendor": "Nokia",
                    "spectrum_mhz": 136,
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
                "technology_mix": {
                    "mobile_vendor": "Ericsson/Nokia",
                    "spectrum_mhz": 0,
                    "spectrum_bands": [],
                    "status": "acquired",
                    "note": "Merged into +Móvil (CWP) in mid-2022. All spectrum transferred.",
                },
            },
            # ── Digicel PA — EXITED market April 2022 ──
            "digicel_pa": {
                "five_g_coverage_pct": 0,
                "four_g_coverage_pct": 0,
                "technology_mix": {
                    "mobile_vendor": "Huawei",
                    "spectrum_mhz": 0,
                    "spectrum_bands": [],
                    "status": "exited",
                    "note": "Exited Panama April 2022. Spectrum (700+1900 MHz) returned to ASEP for re-tender.",
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
            "tigo_panama": {
                "Network Coverage": 80, "Network Quality": 78, "Brand Strength": 75,
                "Price Competitiveness": 78, "Customer Service": 70, "Digital Experience": 70,
                "Enterprise Solutions": 60, "Innovation": 65, "Distribution": 78,
            },
            "masmovil_pa": {
                "Network Coverage": 92, "Network Quality": 88, "Brand Strength": 90,
                "Price Competitiveness": 60, "Customer Service": 75, "Digital Experience": 80,
                "Enterprise Solutions": 85, "Innovation": 78, "Distribution": 92,
            },
            "claro_pa": {
                "Network Coverage": 0, "Network Quality": 0, "Brand Strength": 0,
                "Price Competitiveness": 0, "Customer Service": 0, "Digital Experience": 0,
                "Enterprise Solutions": 0, "Innovation": 0, "Distribution": 0,
            },
            "digicel_pa": {
                "Network Coverage": 0, "Network Quality": 0, "Brand Strength": 0,
                "Price Competitiveness": 0, "Customer Service": 0, "Digital Experience": 0,
                "Enterprise Solutions": 0, "Innovation": 0, "Distribution": 0,
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
