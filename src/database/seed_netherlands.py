"""Seed the database with Netherlands telecom market data.

3-player market: KPN (incumbent), VodafoneZiggo (cable JV), Odido (mobile challenger).
Currency: EUR. All revenue figures in EUR millions per quarter.

Data sources: KPN IR, VodafoneZiggo results, Odido/T-Mobile NL reports, ACM, CBS.
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
            # Odido (formerly T-Mobile NL) — mobile-centric challenger
            # Revenue ~EUR 2.0-2.1B/year, ~500-530M/quarter
            "odido_nl": {
                "total_revenue": [498, 502, 508, 512, 516, 520, 525, 530],
                "service_revenue": [445, 449, 454, 458, 462, 466, 471, 476],
                "service_revenue_growth_pct": [2.8, 3.0, 3.2, 3.1, 3.6, 3.6, 3.3, 3.5],
                "mobile_service_revenue": [385, 389, 394, 398, 402, 406, 411, 416],
                "mobile_service_growth_pct": [3.0, 3.2, 3.4, 3.3, 4.4, 4.4, 4.3, 4.5],
                "fixed_service_revenue": [42, 42, 42, 42, 42, 42, 42, 42],
                "fixed_service_growth_pct": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                "b2b_revenue": [18, 18, 18, 18, 18, 18, 18, 18],
                "ebitda": [179, 181, 183, 185, 188, 190, 193, 195],
                "ebitda_margin_pct": [35.9, 36.1, 36.0, 36.1, 36.4, 36.5, 36.8, 36.8],
                "ebitda_growth_pct": [3.5, 3.8, 4.0, 3.8, 5.0, 5.0, 5.5, 5.4],
                "capex": [85, 86, 88, 89, 90, 92, 93, 94],
                "capex_to_revenue_pct": [17.1, 17.1, 17.3, 17.4, 17.4, 17.7, 17.7, 17.7],
                "employees": [3200, 3200, 3200, 3200, 3100, 3100, 3100, 3100],
                "_source": "Odido Group / T-Mobile NL FY2024-2025 Results",
            },
            # KPN — incumbent market leader, converged player
            # Revenue ~EUR 5.4B/year, ~1,340-1,370M/quarter
            "kpn_nl": {
                "total_revenue": [1328, 1335, 1340, 1345, 1350, 1358, 1365, 1372],
                "service_revenue": [1195, 1202, 1206, 1211, 1218, 1225, 1230, 1237],
                "service_revenue_growth_pct": [2.2, 2.4, 2.5, 2.6, 1.9, 1.9, 2.0, 2.1],
                "mobile_service_revenue": [420, 424, 428, 432, 436, 440, 444, 448],
                "mobile_service_growth_pct": [1.5, 1.8, 2.0, 2.2, 3.8, 3.8, 3.7, 3.7],
                "fixed_service_revenue": [610, 612, 612, 612, 614, 616, 616, 618],
                "fixed_service_growth_pct": [-0.5, -0.3, -0.2, 0.0, 0.7, 0.7, 0.7, 1.0],
                "b2b_revenue": [165, 166, 166, 167, 168, 169, 170, 171],
                "ebitda": [585, 590, 594, 598, 603, 608, 613, 618],
                "ebitda_margin_pct": [44.1, 44.2, 44.3, 44.5, 44.7, 44.8, 44.9, 45.0],
                "ebitda_growth_pct": [2.0, 2.2, 2.5, 2.8, 3.1, 3.1, 3.2, 3.3],
                "capex": [285, 288, 290, 292, 295, 298, 300, 302],
                "capex_to_revenue_pct": [21.5, 21.6, 21.6, 21.7, 21.9, 21.9, 22.0, 22.0],
                "employees": [10200, 10100, 10000, 9900, 9800, 9700, 9600, 9500],
                "_source": "KPN N.V. FY2024-2025 Quarterly Reports",
            },
            # VodafoneZiggo — cable + mobile JV
            # Revenue ~EUR 4.0B/year, ~990-1,010M/quarter
            "vodafoneziggo_nl": {
                "total_revenue": [988, 992, 996, 1000, 1002, 1005, 1008, 1010],
                "service_revenue": [920, 924, 928, 932, 935, 938, 941, 944],
                "service_revenue_growth_pct": [0.5, 0.8, 1.0, 1.2, 1.4, 1.5, 1.4, 1.3],
                "mobile_service_revenue": [340, 343, 346, 349, 352, 355, 358, 361],
                "mobile_service_growth_pct": [1.0, 1.2, 1.5, 1.8, 3.5, 3.5, 3.5, 3.4],
                "fixed_service_revenue": [510, 511, 512, 513, 513, 513, 513, 513],
                "fixed_service_growth_pct": [-0.8, -0.6, -0.4, -0.2, 0.6, 0.4, 0.2, 0.0],
                "b2b_revenue": [70, 70, 70, 70, 70, 70, 70, 70],
                "ebitda": [425, 428, 431, 434, 437, 440, 443, 446],
                "ebitda_margin_pct": [43.0, 43.1, 43.3, 43.4, 43.6, 43.8, 43.9, 44.2],
                "ebitda_growth_pct": [0.8, 1.0, 1.2, 1.5, 2.8, 2.8, 2.8, 2.8],
                "capex": [205, 208, 210, 212, 215, 218, 220, 222],
                "capex_to_revenue_pct": [20.7, 21.0, 21.1, 21.2, 21.5, 21.7, 21.8, 22.0],
                "employees": [7500, 7400, 7300, 7200, 7100, 7000, 6900, 6800],
                "_source": "VodafoneZiggo Group FY2024-2025 Results",
            },
        },
        "subscribers": {
            "odido_nl": {
                "mobile_total_k": [6800, 6850, 6900, 6950, 7000, 7050, 7100, 7150],
                "mobile_postpaid_k": [5100, 5140, 5180, 5220, 5260, 5300, 5340, 5380],
                "mobile_prepaid_k": [1700, 1710, 1720, 1730, 1740, 1750, 1760, 1770],
                "mobile_net_adds_k": [40, 50, 50, 50, 50, 50, 50, 50],
                "mobile_churn_pct": [1.4, 1.3, 1.3, 1.2, 1.2, 1.2, 1.1, 1.1],
                "mobile_arpu": [14.2, 14.3, 14.4, 14.5, 14.6, 14.7, 14.8, 14.9],
                "broadband_total_k": [280, 290, 300, 310, 320, 330, 340, 350],
                "broadband_fiber_k": [0, 0, 0, 0, 0, 0, 0, 0],
                "tv_total_k": [0, 0, 0, 0, 0, 0, 0, 0],
                "b2b_customers_k": [85, 86, 87, 88, 89, 90, 91, 92],
                "_source": "Odido / T-Mobile NL Quarterly KPIs",
            },
            "kpn_nl": {
                "mobile_total_k": [6500, 6520, 6540, 6560, 6580, 6600, 6620, 6640],
                "mobile_postpaid_k": [5200, 5215, 5230, 5245, 5260, 5275, 5290, 5305],
                "mobile_prepaid_k": [1300, 1305, 1310, 1315, 1320, 1325, 1330, 1335],
                "mobile_net_adds_k": [15, 20, 20, 20, 20, 20, 20, 20],
                "mobile_churn_pct": [1.1, 1.1, 1.0, 1.0, 1.0, 1.0, 0.9, 0.9],
                "mobile_arpu": [15.8, 15.9, 16.0, 16.1, 16.2, 16.3, 16.4, 16.5],
                "broadband_total_k": [2980, 2995, 3010, 3025, 3040, 3055, 3070, 3085],
                "broadband_fiber_k": [1500, 1560, 1620, 1680, 1740, 1800, 1860, 1920],
                "broadband_net_adds_k": [12, 15, 15, 15, 15, 15, 15, 15],
                "tv_total_k": [1750, 1745, 1740, 1735, 1730, 1725, 1720, 1715],
                "b2b_customers_k": [180, 182, 184, 186, 188, 190, 192, 194],
                "_source": "KPN N.V. Quarterly KPI Report",
            },
            "vodafoneziggo_nl": {
                "mobile_total_k": [5200, 5210, 5220, 5230, 5240, 5250, 5260, 5270],
                "mobile_postpaid_k": [3900, 3910, 3920, 3930, 3940, 3950, 3960, 3970],
                "mobile_prepaid_k": [1300, 1300, 1300, 1300, 1300, 1300, 1300, 1300],
                "mobile_net_adds_k": [5, 10, 10, 10, 10, 10, 10, 10],
                "mobile_churn_pct": [1.3, 1.3, 1.2, 1.2, 1.2, 1.1, 1.1, 1.1],
                "mobile_arpu": [13.5, 13.6, 13.7, 13.8, 13.9, 14.0, 14.1, 14.2],
                "broadband_total_k": [3400, 3395, 3390, 3385, 3380, 3375, 3370, 3365],
                "broadband_fiber_k": [50, 60, 70, 80, 90, 100, 110, 120],
                "broadband_net_adds_k": [-2, -5, -5, -5, -5, -5, -5, -5],
                "tv_total_k": [3100, 3085, 3070, 3055, 3040, 3025, 3010, 2995],
                "b2b_customers_k": [110, 111, 112, 113, 114, 115, 116, 117],
                "_source": "VodafoneZiggo Group Results",
            },
        },
        "macro": {
            "gdp_growth_pct": 1.8,
            "inflation_pct": 2.5,
            "unemployment_pct": 3.6,
            "telecom_market_size_eur_b": 9.5,
            "telecom_growth_pct": 1.5,
            "five_g_adoption_pct": 28.0,
            "fiber_penetration_pct": 38.0,
            "regulatory_environment": "ACM pro-competition regulation; wholesale access mandates; 5G spectrum fully allocated; Gigabit coverage target by 2030",
            "digital_strategy": "Dutch Gigabit Strategy 2030; full fiber/cable gigabit coverage target; 5G standalone deployment mandates; Digital Government strategy",
            "source_url": "ACM / CBS / European Commission Digital Economy 2025",
        },
        "network": {
            "odido_nl": {
                "five_g_coverage_pct": 85,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 0,
                "technology_mix": {"mobile_vendor": "Ericsson", "spectrum_mhz": 310, "core_vendor": "Ericsson"},
            },
            "kpn_nl": {
                "five_g_coverage_pct": 78,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 4200,
                "technology_mix": {"mobile_vendor": "Nokia", "spectrum_mhz": 290, "core_vendor": "Nokia"},
            },
            "vodafoneziggo_nl": {
                "five_g_coverage_pct": 72,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 120,
                "technology_mix": {"mobile_vendor": "Ericsson/Samsung", "spectrum_mhz": 270, "core_vendor": "Ericsson", "cable_docsis": "3.1"},
            },
        },
        "executives": {
            "odido_nl": [
                {"name": "Soren Abildgaard", "title": "CEO", "start_date": "2023-09-01", "background": "Led T-Mobile NL rebrand to Odido; ex-TDC Denmark; PE-backed transformation leader"},
            ],
            "kpn_nl": [
                {"name": "Joost Farwerck", "title": "CEO", "start_date": "2019-07-01", "background": "KPN veteran; led fiber acceleration strategy; COO before CEO appointment"},
            ],
            "vodafoneziggo_nl": [
                {"name": "Jeroen Hoencamp", "title": "CEO", "start_date": "2017-01-01", "background": "Ex-Vodafone UK CEO; led Vodafone-Ziggo JV integration; cable-mobile convergence expert"},
            ],
        },
        "competitive_scores": {
            "odido_nl": {
                "Network Coverage": 88, "Network Quality": 90, "Brand Strength": 68,
                "Price Competitiveness": 78, "Customer Service": 72, "Digital Experience": 82,
                "Enterprise Solutions": 62, "Innovation": 80, "Distribution": 75,
            },
            "kpn_nl": {
                "Network Coverage": 92, "Network Quality": 88, "Brand Strength": 90,
                "Price Competitiveness": 62, "Customer Service": 80, "Digital Experience": 78,
                "Enterprise Solutions": 92, "Innovation": 75, "Distribution": 88,
            },
            "vodafoneziggo_nl": {
                "Network Coverage": 90, "Network Quality": 82, "Brand Strength": 78,
                "Price Competitiveness": 72, "Customer Service": 70, "Digital Experience": 72,
                "Enterprise Solutions": 72, "Innovation": 68, "Distribution": 82,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "odido_nl",
                "event_date": "2023-09-04",
                "category": "competitive",
                "title": "T-Mobile Netherlands rebrands to Odido",
                "description": "Complete rebrand from T-Mobile to Odido, marking independence from Deutsche Telekom. New brand emphasizes Dutch identity and digital-first approach.",
                "impact_type": "neutral",
                "severity": "high",
            },
            {
                "operator_id": "odido_nl",
                "event_date": "2024-03-15",
                "category": "competitive",
                "title": "Apax Partners and Warburg Pincus complete Odido acquisition",
                "description": "Private equity consortium acquires Odido from Deutsche Telekom. Transaction valued at ~EUR 5.1B. Focus on growth and operational efficiency.",
                "impact_type": "neutral",
                "severity": "high",
            },
            {
                "operator_id": "kpn_nl",
                "event_date": "2024-06-01",
                "category": "investment",
                "title": "KPN accelerates fiber rollout, targeting 80% FTTH by 2027",
                "description": "KPN increases fiber investment, targeting 6M+ homepass. Glaspoort JV contributing 1M+ additional homepass via open access model.",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "vodafoneziggo_nl",
                "event_date": "2024-09-01",
                "category": "regulatory",
                "title": "ACM investigates VodafoneZiggo pricing practices",
                "description": "ACM launches market investigation into cable broadband pricing and bundling practices. Potential impact on convergent strategy.",
                "impact_type": "negative",
                "severity": "medium",
            },
            {
                "operator_id": "odido_nl",
                "event_date": "2025-01-15",
                "category": "investment",
                "title": "Odido launches 5G standalone network commercially",
                "description": "First operator in Netherlands to launch 5G SA, enabling network slicing and ultra-low latency services for enterprise customers.",
                "impact_type": "positive",
                "severity": "high",
            },
        ],
        "earnings_highlights": {
            "odido_nl": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "Odido mobile service revenue growing above market rate driven by 5G upsell and postpaid migration. Brand awareness recovery on track post-rebrand.", "speaker": "CEO"},
                {"segment": "Enterprise", "highlight_type": "outlook", "content": "IoT and private 5G opportunities accelerating. Pipeline of enterprise deals growing significantly.", "speaker": "CFO"},
            ],
            "kpn_nl": [
                {"segment": "Fiber", "highlight_type": "guidance", "content": "Fiber rollout progressing well; 4.2M homepass reached. Customer migration from copper accelerating with 85%+ take-up in fiber areas.", "speaker": "CEO"},
                {"segment": "Overall", "highlight_type": "outlook", "content": "Confident in delivering mid-single-digit EBITDA growth through convergence, fiber ramp, and continued cost efficiency.", "speaker": "CFO"},
            ],
            "vodafoneziggo_nl": [
                {"segment": "Convergence", "highlight_type": "guidance", "content": "Fixed-mobile convergence driving lower churn in our base. DOCSIS 3.1 upgrade delivering gigabit speeds to 95% of cable footprint.", "speaker": "CEO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_netherlands as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
