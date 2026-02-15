"""Seed the database with Malta telecom market data.

3-player market: GO plc (#1, incumbent), Melita (#2, cable), Epic (#3, NJJ/Monaco Telecom).
Currency: EUR. All revenue figures in EUR millions per quarter.

Data sources:
  - GO plc Annual Report 2024 (Malta Stock Exchange filings)
  - Melita — EQT-owned; limited public financials
  - Epic Malta — Monaco Telecom subsidiary; limited public data
  - MCA (Malta Communications Authority) market reports
  - Malta National Statistics Office / IMF
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

MARKET_ID = "malta"
OPERATORS = ["epic_mt", "go_mt", "melita_mt"]


def get_seed_data():
    return {
        "financials": {
            # Epic Malta — Monaco Telecom / NJJ subsidiary
            # Smallest operator in Malta; limited public data
            # Estimated revenue ~EUR 35-40M based on ~15% market share
            "epic_mt": {
                "total_revenue": [8, 8, 9, 9, 9, 9, 10, 10],
                "service_revenue": [7, 7, 8, 8, 8, 8, 9, 9],
                "service_revenue_growth_pct": [3.0, 3.5, 4.0, 4.5, 12.5, 14.3, 12.5, 12.5],
                "mobile_service_revenue": [5, 5, 6, 6, 6, 6, 7, 7],
                "mobile_service_growth_pct": [2.0, 2.5, 3.0, 3.5, 20.0, 20.0, 16.7, 16.7],
                "fixed_service_revenue": [1, 1, 1, 1, 1, 1, 1, 1],
                "fixed_service_growth_pct": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                "b2b_revenue": [1, 1, 1, 1, 1, 1, 1, 1],
                "ebitda": [2, 2, 3, 3, 3, 3, 3, 3],
                "ebitda_margin_pct": [25.0, 25.0, 33.3, 33.3, 33.3, 33.3, 30.0, 30.0],
                "ebitda_growth_pct": [0.0, 0.0, 50.0, 50.0, 50.0, 50.0, 0.0, 0.0],
                "capex": [2, 2, 2, 2, 2, 2, 3, 3],
                "capex_to_revenue_pct": [25.0, 25.0, 22.2, 22.2, 22.2, 22.2, 30.0, 30.0],
                "employees": [180, 182, 184, 186, 188, 190, 192, 195],
                "_source": "Epic Malta (Monaco Telecom subsidiary); private company; estimates based on market share",
            },
            # GO plc — Malta's incumbent, listed on Malta Stock Exchange
            # FY2024: Revenue EUR 244.9M (+3.8%), EBITDA EUR 55.4M (down from EUR 60.3M)
            # 34.8% mobile share, 46.8% broadband share; 500K+ customers
            "go_mt": {
                "total_revenue": [57, 58, 59, 60, 59, 60, 62, 64],
                "service_revenue": [52, 53, 54, 55, 54, 55, 57, 59],
                "service_revenue_growth_pct": [2.0, 2.5, 3.0, 3.5, 3.8, 3.8, 5.6, 7.3],
                "mobile_service_revenue": [15, 15, 16, 16, 16, 16, 17, 17],
                "mobile_service_growth_pct": [2.0, 2.5, 3.0, 3.5, 6.7, 6.7, 6.3, 6.3],
                "fixed_service_revenue": [30, 31, 31, 32, 31, 32, 33, 34],
                "fixed_service_growth_pct": [1.5, 2.0, 2.5, 3.0, 3.3, 3.2, 6.5, 6.3],
                "b2b_revenue": [7, 7, 7, 7, 7, 7, 7, 8],
                "ebitda": [14, 15, 15, 16, 13, 13, 14, 15],
                "ebitda_margin_pct": [24.6, 25.9, 25.4, 26.7, 22.0, 21.7, 22.6, 23.4],
                "ebitda_growth_pct": [3.0, 4.0, 3.0, 5.0, -7.1, -13.3, -6.7, -6.3],
                "capex": [10, 11, 11, 12, 11, 12, 12, 13],
                "capex_to_revenue_pct": [17.5, 19.0, 18.6, 20.0, 18.6, 20.0, 19.4, 20.3],
                "employees": [1480, 1490, 1500, 1510, 1500, 1500, 1510, 1520],
                "_source": "GO plc FY2024 (Malta Stock Exchange); revenue EUR 244.9M (+3.8%), EBITDA EUR 55.4M; incl Cablenet Cyprus subsidiary",
            },
            # Melita — EQT PE-owned, cable + mobile operator
            # Private company; limited public financials
            # Estimated revenue ~EUR 100-110M based on ~35% market share
            "melita_mt": {
                "total_revenue": [24, 25, 25, 26, 25, 26, 26, 27],
                "service_revenue": [22, 23, 23, 24, 23, 24, 24, 25],
                "service_revenue_growth_pct": [2.0, 2.5, 2.5, 3.0, 4.5, 4.3, 4.3, 4.2],
                "mobile_service_revenue": [8, 8, 8, 9, 8, 9, 9, 9],
                "mobile_service_growth_pct": [2.0, 2.5, 3.0, 3.5, 0.0, 12.5, 12.5, 0.0],
                "fixed_service_revenue": [12, 13, 13, 13, 13, 13, 13, 14],
                "fixed_service_growth_pct": [2.0, 2.5, 2.0, 2.5, 8.3, 0.0, 0.0, 7.7],
                "b2b_revenue": [2, 2, 2, 2, 2, 2, 2, 2],
                "ebitda": [9, 10, 10, 10, 10, 10, 10, 11],
                "ebitda_margin_pct": [37.5, 40.0, 40.0, 38.5, 40.0, 38.5, 38.5, 40.7],
                "ebitda_growth_pct": [3.0, 5.0, 5.0, 3.0, 11.1, 0.0, 0.0, 10.0],
                "capex": [5, 5, 6, 6, 6, 6, 6, 6],
                "capex_to_revenue_pct": [20.8, 20.0, 24.0, 23.1, 24.0, 23.1, 23.1, 22.2],
                "employees": [500, 505, 510, 515, 520, 525, 530, 535],
                "_source": "Melita (EQT-owned); private company; estimates based on cable + mobile market position",
            },
        },
        "subscribers": {
            "epic_mt": {
                "mobile_total_k": [72, 73, 74, 75, 76, 77, 78, 80],
                "mobile_postpaid_k": [45, 46, 47, 48, 49, 50, 51, 52],
                "mobile_prepaid_k": [27, 27, 27, 27, 27, 27, 27, 28],
                "mobile_net_adds_k": [1, 1, 1, 1, 1, 1, 1, 2],
                "mobile_churn_pct": [1.8, 1.8, 1.7, 1.7, 1.7, 1.6, 1.6, 1.5],
                "mobile_arpu": [22.0, 22.2, 22.5, 22.8, 23.0, 23.3, 23.5, 23.8],
                "broadband_total_k": [8, 8, 9, 9, 10, 10, 11, 11],
                "broadband_fiber_k": [8, 8, 9, 9, 10, 10, 11, 11],
                "broadband_net_adds_k": [0, 0, 1, 0, 1, 0, 1, 0],
                "tv_total_k": [0, 0, 0, 0, 0, 0, 0, 0],
                "b2b_customers_k": [2, 2, 2, 2, 2, 2, 2, 2],
                "_source": "Epic Malta; estimated ~15% mobile share; no owned fixed network",
            },
            "go_mt": {
                "mobile_total_k": [170, 172, 174, 176, 178, 180, 183, 186],
                "mobile_postpaid_k": [110, 112, 114, 116, 118, 120, 123, 126],
                "mobile_prepaid_k": [60, 60, 60, 60, 60, 60, 60, 60],
                "mobile_net_adds_k": [2, 2, 2, 2, 2, 2, 3, 3],
                "mobile_churn_pct": [1.2, 1.2, 1.1, 1.1, 1.1, 1.0, 1.0, 1.0],
                "mobile_arpu": [28.0, 28.3, 28.5, 28.8, 29.0, 29.3, 29.5, 29.8],
                "broadband_total_k": [88, 89, 90, 91, 92, 93, 94, 95],
                "broadband_fiber_k": [50, 52, 54, 56, 58, 60, 62, 65],
                "broadband_net_adds_k": [1, 1, 1, 1, 1, 1, 1, 1],
                "tv_total_k": [55, 55, 55, 55, 55, 56, 56, 56],
                "b2b_customers_k": [8, 8, 8, 8, 8, 9, 9, 9],
                "_source": "GO plc FY2024; 34.8% mobile, 46.8% broadband market share; 500K+ total customers",
            },
            "melita_mt": {
                "mobile_total_k": [135, 136, 137, 138, 139, 140, 141, 142],
                "mobile_postpaid_k": [85, 86, 87, 88, 89, 90, 91, 92],
                "mobile_prepaid_k": [50, 50, 50, 50, 50, 50, 50, 50],
                "mobile_net_adds_k": [1, 1, 1, 1, 1, 1, 1, 1],
                "mobile_churn_pct": [1.3, 1.3, 1.2, 1.2, 1.2, 1.2, 1.1, 1.1],
                "mobile_arpu": [20.0, 20.3, 20.5, 20.8, 21.0, 21.3, 21.5, 21.8],
                "broadband_total_k": [62, 63, 63, 64, 64, 65, 65, 66],
                "broadband_fiber_k": [10, 12, 14, 16, 18, 20, 22, 24],
                "broadband_net_adds_k": [0, 1, 0, 1, 0, 1, 0, 1],
                "tv_total_k": [55, 55, 55, 55, 56, 56, 56, 57],
                "b2b_customers_k": [5, 5, 5, 5, 5, 5, 5, 6],
                "_source": "Melita; cable + mobile operator; EQT PE-owned; estimated ~28% mobile share",
            },
        },
        "macro": {
            "gdp_growth_pct": 5.0,
            "inflation_pct": 3.0,
            "unemployment_pct": 3.5,
            "telecom_market_size_eur_b": 0.25,
            "telecom_growth_pct": 3.5,
            "five_g_adoption_pct": 12.0,
            "fiber_penetration_pct": 45.0,
            "regulatory_environment": "MCA (Malta Communications Authority) regulation; EU framework. 5G deployed by all three operators. GO wholesale access mandated. iGaming regulation drives enterprise demand.",
            "digital_strategy": "Dense geography enables efficient network deployment. Malta as EU iGaming hub. 3M+ tourists for 540K pop. Growing fintech and digital services. Smart city initiatives.",
            "source_url": "MCA / Malta National Statistics Office / IMF",
        },
        "network": {
            "epic_mt": {
                "five_g_coverage_pct": 50,
                "four_g_coverage_pct": 90,
                "fiber_homepass_k": 0,
                "technology_mix": {"mobile_vendor": "Huawei", "spectrum_mhz": 120, "fixed_access": "GO wholesale"},
            },
            "go_mt": {
                "five_g_coverage_pct": 65,
                "four_g_coverage_pct": 99,
                "fiber_homepass_k": 200,
                "technology_mix": {"mobile_vendor": "Nokia", "spectrum_mhz": 180, "fiber_technology": "GPON", "fixed_incumbent": True},
            },
            "melita_mt": {
                "five_g_coverage_pct": 55,
                "four_g_coverage_pct": 95,
                "fiber_homepass_k": 50,
                "technology_mix": {"mobile_vendor": "Mixed", "spectrum_mhz": 140, "cable_docsis": "3.1", "cable_homepass_k": 180},
            },
        },
        "executives": {
            "epic_mt": [
                {"name": "Paul Fenech", "title": "CEO", "start_date": "2021-01-01", "background": "Monaco Telecom appointee; leading Epic Malta market growth"},
            ],
            "go_mt": [
                {"name": "Nikhil Patil", "title": "CEO", "start_date": "2019-01-01", "background": "Led GO plc through fiber expansion and Cablenet Cyprus acquisition"},
            ],
            "melita_mt": [
                {"name": "Harald Roesch", "title": "CEO", "start_date": "2019-01-01", "background": "EQT appointee; managing cable-to-fiber transition and convergent strategy"},
            ],
        },
        "competitive_scores": {
            "epic_mt": {
                "Network Coverage": 68, "Network Quality": 75, "Brand Strength": 55,
                "Price Competitiveness": 80, "Customer Service": 68, "Digital Experience": 78,
                "Enterprise Solutions": 40, "Innovation": 75, "Distribution": 55,
            },
            "go_mt": {
                "Network Coverage": 95, "Network Quality": 82, "Brand Strength": 90,
                "Price Competitiveness": 60, "Customer Service": 78, "Digital Experience": 72,
                "Enterprise Solutions": 88, "Innovation": 70, "Distribution": 90,
            },
            "melita_mt": {
                "Network Coverage": 82, "Network Quality": 80, "Brand Strength": 78,
                "Price Competitiveness": 72, "Customer Service": 75, "Digital Experience": 70,
                "Enterprise Solutions": 65, "Innovation": 72, "Distribution": 78,
            },
        },
        "intelligence_events": [
            {
                "operator_id": "go_mt",
                "event_date": "2024-12-01",
                "category": "investment",
                "title": "GO plc achieves record revenue EUR 244.9M in FY2024",
                "description": "GO plc consolidated revenue grew 3.8% to record EUR 244.9M. Mobile market share 34.8%, broadband 46.8%. EBITDA fell to EUR 55.4M from EUR 60.3M due to increased investment. Gained 10,000+ new mobile customers.",
                "impact_type": "positive",
                "severity": "high",
            },
            {
                "operator_id": "go_mt",
                "event_date": "2025-03-01",
                "category": "investment",
                "title": "GO plc FTTH fiber rollout accelerating across Malta",
                "description": "GO plc investing in nationwide FTTH fiber replacement of legacy copper network. Key to maintaining broadband leadership (46.8% share) against Melita cable and emerging competitors.",
                "impact_type": "positive",
                "severity": "medium",
            },
            {
                "operator_id": "melita_mt",
                "event_date": "2024-06-01",
                "category": "competitive",
                "title": "Melita accelerates DOCSIS 3.1 rollout and selective FTTH",
                "description": "Melita upgrading HFC cable network to DOCSIS 3.1 for multi-Gbps speeds. Selective FTTH in new developments. EQT ownership driving investment efficiency.",
                "impact_type": "positive",
                "severity": "medium",
            },
        ],
        "earnings_highlights": {
            "epic_mt": [
                {"segment": "Mobile", "highlight_type": "guidance", "content": "Epic Malta growing mobile subscriber base as third operator. NJJ/Monaco Telecom investment commitment. 5G network expanding. Competitive pricing challenging GO and Melita.", "speaker": "CEO"},
            ],
            "go_mt": [
                {"segment": "Overall", "highlight_type": "guidance", "content": "FY2024 record revenue EUR 244.9M (+3.8%). Mobile share 34.8%, broadband 46.8%. EBITDA EUR 55.4M (down from EUR 60.3M due to investment). 500K+ customers. 10K+ mobile net adds.", "speaker": "CEO"},
                {"segment": "Strategy", "highlight_type": "outlook", "content": "FTTH fiber expansion across Malta replacing legacy copper. Cablenet Cyprus subsidiary contributing to group. Enterprise ICT growth. Listed on Malta Stock Exchange with solid dividend.", "speaker": "CFO"},
            ],
            "melita_mt": [
                {"segment": "Overall", "highlight_type": "guidance", "content": "Melita maintains strong #2 position in Malta with cable + mobile convergence. EQT PE ownership since 2019. DOCSIS 3.1 upgrade enabling multi-Gbps broadband speeds. Strong TV subscriber base.", "speaker": "CEO"},
            ],
        },
    }


def seed_all(db_path: str = "data/telecom.db"):
    from src.database.seed_latam_helper import seed_all_for_market
    import src.database.seed_malta as mod
    return seed_all_for_market(mod, db_path)


if __name__ == "__main__":
    seed_all()
