"""Seed the database with Belgium telecom market data.

3-player market: Proximus (incumbent), Telenet (cable), Orange Belgium (mobile challenger).
Currency: EUR. All revenue figures in EUR millions per quarter.

Data sources: Proximus IR, Telenet/Liberty Global results, Orange Belgium reports, BIPT.
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
            # Proximus — Belgian incumbent, ~EUR 5.8-6.0B/year, ~1,440-1,510M/quarter
            # Strong convergent portfolio, fiber investment phase
            "proximus_be": {
                "total_revenue": [1440, 1455, 1468, 1475, 1482, 1490, 1500, 1510],
                "service_revenue": [1260, 1272, 1282, 1290, 1298, 1306, 1315, 1324],
                "service_revenue_growth_pct": [1.5, 1.8, 2.0, 2.2, 3.0, 2.7, 2.6, 2.6],
                "mobile_service_revenue": [380, 384, 388, 392, 396, 400, 404, 408],
                "mobile_service_growth_pct": [1.0, 1.2, 1.5, 1.8, 4.2, 4.2, 4.1, 4.1],
                "fixed_service_revenue": [680, 685, 690, 693, 696, 699, 703, 707],
                "fixed_service_growth_pct": [0.2, 0.4, 0.5, 0.7, 2.4, 2.0, 1.9, 2.0],
                "b2b_revenue": [200, 203, 204, 205, 206, 207, 208, 209],
                "ebitda": [490, 496, 502, 508, 514, 520, 527, 534],
                "ebitda_margin_pct": [34.0, 34.1, 34.2, 34.4, 34.7, 34.9, 35.1, 35.4],
                "ebitda_growth_pct": [1.0, 1.5, 1.8, 2.0, 4.9, 4.8, 5.0, 5.1],
                "capex": [360, 365, 370, 375, 378, 380, 382, 385],
                "capex_to_revenue_pct": [25.0, 25.1, 25.2, 25.4, 25.5, 25.5, 25.5, 25.5],
                "employees": [11300, 11200, 11100, 11000, 10900, 10800, 10700, 10600],
                "_source": "Proximus Group FY2024-2025 Quarterly Reports",
            },
            # Orange Belgium — mobile challenger, part of Orange Group
            # Revenue ~EUR 1.4-1.5B/year, ~355-380M/quarter
            "orange_be": {
                "total_revenue": [355, 358, 362, 365, 368, 372, 375, 380],
                "service_revenue": [312, 315, 318, 321, 324, 327, 330, 334],
                "service_revenue_growth_pct": [2.0, 2.2, 2.5, 2.8, 3.7, 3.8, 3.8, 4.0],
                "mobile_service_revenue": [258, 261, 264, 267, 270, 273, 276, 280],
                "mobile_service_growth_pct": [2.5, 2.8, 3.0, 3.2, 4.7, 4.6, 4.5, 4.9],
                "fixed_service_revenue": [38, 38, 38, 38, 38, 38, 38, 38],
                "fixed_service_growth_pct": [-1.0, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                "b2b_revenue": [16, 16, 16, 16, 16, 16, 16, 16],
                "ebitda": [100, 101, 103, 104, 106, 108, 110, 112],
                "ebitda_margin_pct": [28.2, 28.2, 28.5, 28.5, 28.8, 29.0, 29.3, 29.5],
                "ebitda_growth_pct": [1.5, 2.0, 2.5, 3.0, 6.0, 6.9, 6.8, 7.7],
                "capex": [72, 73, 74, 75, 76, 77, 78, 79],
                "capex_to_revenue_pct": [20.3, 20.4, 20.4, 20.5, 20.7, 20.7, 20.8, 20.8],
                "employees": [1600, 1600, 1600, 1600, 1550, 1550, 1550, 1550],
                "_source": "Orange Belgium FY2024-2025 Quarterly Reports",
            },
            # Telenet (Liberty Global) — cable operator, incl. BASE mobile
            # Revenue ~EUR 2.7-2.8B/year, ~678-700M/quarter
            "telenet_be": {
                "total_revenue": [678, 682, 685, 688, 690, 693, 696, 700],
                "service_revenue": [618, 622, 625, 628, 632, 636, 640, 644],
                "service_revenue_growth_pct": [0.5, 0.8, 1.0, 1.2, 2.3, 2.3, 2.4, 2.5],
                "mobile_service_revenue": [165, 167, 169, 171, 173, 175, 177, 180],
                "mobile_service_growth_pct": [1.5, 1.8, 2.0, 2.2, 4.8, 4.8, 4.7, 5.3],
                "fixed_service_revenue": [380, 381, 382, 383, 384, 385, 387, 388],
                "fixed_service_growth_pct": [-0.5, -0.3, 0.0, 0.3, 1.1, 1.0, 1.3, 1.3],
                "b2b_revenue": [73, 74, 74, 74, 75, 76, 76, 76],
                "ebitda": [330, 332, 334, 336, 338, 341, 344, 347],
                "ebitda_margin_pct": [48.7, 48.7, 48.8, 48.8, 49.0, 49.2, 49.4, 49.6],
                "ebitda_growth_pct": [0.3, 0.5, 0.8, 1.0, 2.4, 2.7, 3.0, 3.3],
                "capex": [165, 168, 170, 172, 174, 176, 178, 180],
                "capex_to_revenue_pct": [24.3, 24.6, 24.8, 25.0, 25.2, 25.4, 25.6, 25.7],
                "employees": [4200, 4200, 4200, 4200, 4100, 4100, 4100, 4100],
                "_source": "Telenet Group / Liberty Global FY2024-2025 Results",
            },
        },
        "subscribers": {
            "proximus_be": {
                "mobile_total_k": [4700, 4720, 4740, 4760, 4780, 4800, 4820, 4840],
                "mobile_postpaid_k": [3500, 3520, 3540, 3560, 3580, 3600, 3620, 3640],
                "mobile_prepaid_k": [1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200],
                "mobile_net_adds_k": [15, 20, 20, 20, 20, 20, 20, 20],
                "mobile_churn_pct": [1.2, 1.2, 1.1, 1.1, 1.1, 1.0, 1.0, 1.0],
                "mobile_arpu": [19.5, 19.6, 19.7, 19.8, 20.0, 20.1, 20.2, 20.3],
                "broadband_total_k": [2100, 2115, 2130, 2145, 2160, 2175, 2190, 2205],
                "broadband_fiber_k": [450, 500, 550, 600, 660, 720, 780, 840],
                "broadband_net_adds_k": [10, 15, 15, 15, 15, 15, 15, 15],
                "tv_total_k": [1650, 1645, 1640, 1635, 1630, 1625, 1620, 1615],
                "b2b_customers_k": [220, 222, 224, 226, 228, 230, 232, 234],
                "_source": "Proximus Group Quarterly KPI Report",
            },
            "orange_be": {
                "mobile_total_k": [3200, 3220, 3240, 3260, 3280, 3300, 3320, 3340],
                "mobile_postpaid_k": [2400, 2420, 2440, 2460, 2480, 2500, 2520, 2540],
                "mobile_prepaid_k": [800, 800, 800, 800, 800, 800, 800, 800],
                "mobile_net_adds_k": [15, 20, 20, 20, 20, 20, 20, 20],
                "mobile_churn_pct": [1.5, 1.5, 1.4, 1.4, 1.4, 1.3, 1.3, 1.3],
                "mobile_arpu": [17.8, 17.9, 18.0, 18.1, 18.2, 18.3, 18.4, 18.5],
                "broadband_total_k": [380, 382, 384, 386, 388, 390, 392, 394],
                "broadband_fiber_k": [0, 0, 0, 0, 0, 0, 0, 0],
                "tv_total_k": [120, 120, 120, 120, 120, 120, 120, 120],
                "b2b_customers_k": [45, 46, 47, 48, 49, 50, 51, 52],
                "_source": "Orange Belgium Quarterly KPIs",
            },
            "telenet_be": {
                "mobile_total_k": [3000, 3010, 3020, 3030, 3040, 3050, 3060, 3070],
                "mobile_postpaid_k": [2100, 2110, 2120, 2130, 2140, 2150, 2160, 2170],
                "mobile_prepaid_k": [900, 900, 900, 900, 900, 900, 900, 900],
                "mobile_net_adds_k": [5, 10, 10, 10, 10, 10, 10, 10],
                "mobile_churn_pct": [1.4, 1.4, 1.3, 1.3, 1.3, 1.2, 1.2, 1.2],
                "mobile_arpu": [16.5, 16.6, 16.7, 16.8, 16.9, 17.0, 17.1, 17.2],
                "broadband_total_k": [2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085],
                "broadband_fiber_k": [20, 25, 30, 35, 40, 45, 50, 55],
                "broadband_net_adds_k": [3, 5, 5, 5, 5, 5, 5, 5],
                "tv_total_k": [1850, 1845, 1840, 1835, 1830, 1825, 1820, 1815],
                "b2b_customers_k": [95, 96, 97, 98, 99, 100, 101, 102],
                "_source": "Telenet Group Quarterly KPI Report",
            },
        },
        "macro": {
            "gdp_growth_pct": 1.2,
            "inflation_pct": 2.8,
            "unemployment_pct": 5.5,
            "telecom_market_size_eur_b": 7.8,
            "telecom_growth_pct": 1.0,
            "five_g_adoption_pct": 22.0,
            "fiber_penetration_pct": 18.0,
            "regulatory_environment": "BIPT pro-competition regulation; wholesale access mandates; 5G spectrum allocated 2022; automatic wage indexation increases operator costs",
            "digital_strategy": "Belgian Gigabit Plan aligned with EU Digital Decade; fiber/cable gigabit coverage targets; 5G rollout obligations; Brussels EU hub connectivity investments",
            "source_url": "BIPT / NBB / European Commission Digital Economy 2025",
        },
        "network": {
            "proximus_be": {
                "five_g_coverage_pct": 78,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 2200,
                "technology_mix": {"mobile_vendor": "Nokia", "spectrum_mhz": 280, "core_vendor": "Nokia"},
            },
            "orange_be": {
                "five_g_coverage_pct": 55,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 50,
                "technology_mix": {"mobile_vendor": "Ericsson", "spectrum_mhz": 200, "core_vendor": "Ericsson"},
            },
            "telenet_be": {
                "five_g_coverage_pct": 60,
                "four_g_coverage_pct": 97,
                "fiber_homepass_k": 80,
                "technology_mix": {"mobile_vendor": "Nokia", "spectrum_mhz": 220, "core_vendor": "Nokia", "cable_docsis": "3.1"},
            },
        },
        "executives": {
            "proximus_be": [
                {"name": "Guillaume Boutin", "title": "CEO", "start_date": "2019-12-01", "background": "Former Orange executive; led Bold2025 digital transformation; driving fiber acceleration and Proximus NXT enterprise strategy"},
            ],
            "orange_be": [
                {"name": "Xavier Pichon", "title": "CEO", "start_date": "2021-01-01", "background": "Orange Group veteran; mobile-centric growth strategy; building convergent capabilities through selective infrastructure investment"},
            ],
            "telenet_be": [
                {"name": "John Porter", "title": "CEO", "start_date": "2013-08-01", "background": "Led VOO acquisition and national cable expansion; strong entertainment focus; Liberty Global board member; longest-serving major operator CEO in Belgium"},
            ],
        },
        "competitive_scores": {
            "proximus_be": {
                "Network Coverage": 92, "Network Quality": 88, "Brand Strength": 88,
                "Price Competitiveness": 58, "Customer Service": 78, "Digital Experience": 80,
                "Enterprise Solutions": 90, "Innovation": 78, "Distribution": 90,
            },
            "orange_be": {
                "Network Coverage": 80, "Network Quality": 82, "Brand Strength": 72,
                "Price Competitiveness": 80, "Customer Service": 72, "Digital Experience": 76,
                "Enterprise Solutions": 60, "Innovation": 75, "Distribution": 70,
            },
            "telenet_be": {
                "Network Coverage": 88, "Network Quality": 85, "Brand Strength": 82,
                "Price Competitiveness": 68, "Customer Service": 75, "Digital Experience": 74,
                "Enterprise Solutions": 68, "Innovation": 72, "Distribution": 82,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "proximus_be",
                "event_date": "2024-03-01",
                "category": "investment",
                "title": "Proximus accelerates FTTH, targeting 4.2M homepass by 2028",
                "description": "Proximus raises fiber rollout target from 3.8M to 4.2M homepass, partnering with Nokia for deployment. Bold2025 strategy enters acceleration phase.",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "proximus_be",
                "event_date": "2024-09-01",
                "category": "competitive",
                "title": "Proximus launches NXT enterprise cloud platform",
                "description": "Proximus NXT positions as integrated ICT/cloud provider for Belgian enterprise. Azure partnership deepened with local data centers.",
                "impact_type": "positive",
                "severity": "medium",
            },
            {
                "operator_id": "telenet_be",
                "event_date": "2023-06-15",
                "category": "competitive",
                "title": "Telenet completes VOO acquisition, creating national cable footprint",
                "description": "Telenet finalizes acquisition of Wallonia cable operator VOO, extending coverage from Flanders-only to nationwide. Integration program launched.",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "orange_be",
                "event_date": "2024-06-01",
                "category": "regulatory",
                "title": "Orange Belgium gains cable bitstream access for broadband",
                "description": "BIPT-mandated cable bitstream access enables Orange Belgium to offer broadband via regulated wholesale on Proximus and Telenet networks.",
                "impact_type": "positive",
                "severity": "medium",
            },
            {
                "operator_id": "telenet_be",
                "event_date": "2025-01-10",
                "category": "competitive",
                "title": "Liberty Global evaluates strategic options for Telenet stake",
                "description": "Liberty Global confirms strategic review of European cable assets including Telenet. Potential sale, merger, or IPO under consideration.",
                "impact_type": "negative",
                "severity": "high",
            },
        ],
        "earnings_highlights": {
            "proximus_be": [
                {"segment": "Consumer", "highlight_type": "guidance", "content": "Proximus Flex convergent bundles driving ARPU uplift. Fiber take-up exceeding 50% in newly connected areas within 12 months.", "speaker": "CEO"},
                {"segment": "Enterprise", "highlight_type": "outlook", "content": "Proximus NXT enterprise revenue growing double-digit. Cybersecurity and cloud managed services are fastest growing segments.", "speaker": "CFO"},
            ],
            "orange_be": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "Mobile service revenue accelerating driven by 5G upsell and postpaid migration. Orange Thank loyalty program reducing churn.", "speaker": "CEO"},
            ],
            "telenet_be": [
                {"segment": "Convergence", "highlight_type": "guidance", "content": "VOO integration progressing well; DOCSIS 3.1 upgrade complete across Wallonia. National cable platform now serves 4.9M homepass.", "speaker": "CEO"},
                {"segment": "Entertainment", "highlight_type": "outlook", "content": "Play Sports and entertainment bundle driving customer retention. Convergent customer base growing as BASE mobile integrates with Telenet fixed.", "speaker": "CEO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_belgium as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
