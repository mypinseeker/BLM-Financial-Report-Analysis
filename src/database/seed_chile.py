"""Seed the database with Chile telecom market data.

Reads hardcoded data from the legacy Chile analysis file and inserts them
into the SQLite database using calendar quarter alignment.

All Chile operators use calendar year (fiscal_year_start_month = 1),
so the period labels map directly: "Q1 2024" → CQ1_2024, etc.

Calendar quarter mapping of the 8 data positions:
  Index 0: Q1 2024 = CQ1_2024  (Jan-Mar 2024)
  Index 1: Q2 2024 = CQ2_2024  (Apr-Jun 2024)
  Index 2: Q3 2024 = CQ3_2024  (Jul-Sep 2024)
  Index 3: Q4 2024 = CQ4_2024  (Oct-Dec 2024)
  Index 4: Q1 2025 = CQ1_2025  (Jan-Mar 2025)
  Index 5: Q2 2025 = CQ2_2025  (Apr-Jun 2025)
  Index 6: Q3 2025 = CQ3_2025  (Jul-Sep 2025)
  Index 7: Q4 2025 = CQ4_2025  (Oct-Dec 2025)
"""

import sys
from pathlib import Path

# Add project root to path for imports
_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.database.db import TelecomDatabase
from src.database.operator_directory import OPERATOR_DIRECTORY


# ============================================================================
# Calendar quarter labels — all Chile operators use calendar year
# ============================================================================
CALENDAR_QUARTERS_8Q = [
    "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024",
    "Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025",
]

# Mapping from legacy operator display names to operator IDs
LEGACY_NAME_TO_ID = {
    "Entel Chile": "entel_cl",
    "Movistar Chile": "movistar_cl",
    "Claro Chile": "claro_cl",
    "WOM Chile": "wom_cl",
}


def seed_operators(db: TelecomDatabase):
    """Register all Chile market operators (excluding tigo_chile — no historical data)."""
    count = 0
    for op_id, info in OPERATOR_DIRECTORY.items():
        if info["market"] == "chile" and op_id != "tigo_chile":
            db.upsert_operator(op_id, **info)
            count += 1
    print(f"  Registered {count} Chile operators")


def seed_financial_data(db: TelecomDatabase):
    """Insert 8 quarters of financial data from REVENUE, PROFITABILITY, INVESTMENT dicts."""
    from src.blm._legacy.chile_market_comprehensive_data import (
        REVENUE_DATA_8Q,
        PROFITABILITY_DATA_8Q,
        INVESTMENT_DATA_8Q,
    )

    count = 0
    for legacy_name, rev_data in REVENUE_DATA_8Q.items():
        op_id = LEGACY_NAME_TO_ID.get(legacy_name)
        if not op_id:
            print(f"  WARNING: Unknown operator '{legacy_name}', skipping")
            continue

        prof_data = PROFITABILITY_DATA_8Q.get(legacy_name, {})
        inv_data = INVESTMENT_DATA_8Q.get(legacy_name, {})

        for i in range(8):
            period = CALENDAR_QUARTERS_8Q[i]

            # Employees are in thousands in legacy data, convert to headcount
            employees_k = inv_data.get("employees_k", [None] * 8)[i]
            employees = int(employees_k * 1000) if employees_k is not None else None

            financial = {
                # Revenue (CLP millions)
                "total_revenue": rev_data.get("total_revenue", [None] * 8)[i],
                "service_revenue": rev_data.get("service_revenue", [None] * 8)[i],
                "service_revenue_growth_pct": rev_data.get("service_revenue_growth_pct", [None] * 8)[i],
                "mobile_service_revenue": rev_data.get("mobile_service_revenue", [None] * 8)[i],
                "mobile_service_growth_pct": rev_data.get("mobile_service_growth_pct", [None] * 8)[i],
                "fixed_service_revenue": rev_data.get("fixed_service_revenue", [None] * 8)[i],
                "fixed_service_growth_pct": rev_data.get("fixed_service_growth_pct", [None] * 8)[i],
                "b2b_revenue": rev_data.get("b2b_revenue", [None] * 8)[i],
                "b2b_growth_pct": rev_data.get("b2b_growth_pct", [None] * 8)[i],
                # Profitability
                "ebitda": prof_data.get("ebitda", [None] * 8)[i],
                "ebitda_margin_pct": prof_data.get("ebitda_margin_pct", [None] * 8)[i],
                "ebitda_growth_pct": prof_data.get("ebitda_growth_pct", [None] * 8)[i],
                "net_income": prof_data.get("net_income", [None] * 8)[i],
                # Investment
                "capex": inv_data.get("capex", [None] * 8)[i],
                "capex_to_revenue_pct": inv_data.get("capex_to_revenue_pct", [None] * 8)[i],
                "opex": inv_data.get("opex", [None] * 8)[i],
                "opex_to_revenue_pct": inv_data.get("opex_to_revenue_pct", [None] * 8)[i],
                "employees": employees,
                # Source
                "source_url": rev_data.get("_source", ""),
            }

            db.upsert_financial(op_id, period, financial)
            count += 1

    print(f"  Inserted {count} financial quarterly records")


def seed_subscriber_data(db: TelecomDatabase):
    """Insert 8 quarters of subscriber data from MOBILE, FIXED, TV/FMC dicts."""
    from src.blm._legacy.chile_market_comprehensive_data import (
        MOBILE_BUSINESS_DATA_8Q,
        FIXED_BROADBAND_DATA_8Q,
        TV_FMC_DATA_8Q,
    )

    count = 0
    for legacy_name, mob_data in MOBILE_BUSINESS_DATA_8Q.items():
        op_id = LEGACY_NAME_TO_ID.get(legacy_name)
        if not op_id:
            print(f"  WARNING: Unknown operator '{legacy_name}', skipping")
            continue

        fix_data = FIXED_BROADBAND_DATA_8Q.get(legacy_name, {})
        tv_data = TV_FMC_DATA_8Q.get(legacy_name, {})

        for i in range(8):
            period = CALENDAR_QUARTERS_8Q[i]

            # Mobile — convert from millions to thousands
            total_mobile_m = mob_data.get("total_mobile_subs_m", [None] * 8)[i]
            postpaid_m = mob_data.get("postpaid_subs_m", [None] * 8)[i]
            prepaid_m = mob_data.get("prepaid_subs_m", [None] * 8)[i]

            # Fixed broadband — convert from millions to thousands
            bb_total_m = fix_data.get("broadband_subs_m", [None] * 8)[i]
            fiber_m = fix_data.get("fiber_ftth_subs_m", [None] * 8)[i]
            cable_m = fix_data.get("cable_docsis_subs_m", [None] * 8)[i]
            dsl_m = fix_data.get("dsl_copper_subs_m", [None] * 8)[i]

            # TV/FMC — convert from millions to thousands
            tv_m = tv_data.get("tv_subs_m", [None] * 8)[i]
            fmc_m = tv_data.get("fmc_subs_m", [None] * 8)[i]

            subscriber = {
                # Mobile (in thousands)
                "mobile_total_k": total_mobile_m * 1000 if total_mobile_m is not None else None,
                "mobile_postpaid_k": postpaid_m * 1000 if postpaid_m is not None else None,
                "mobile_prepaid_k": prepaid_m * 1000 if prepaid_m is not None else None,
                "mobile_net_adds_k": mob_data.get("net_adds_k", [None] * 8)[i],
                "mobile_churn_pct": mob_data.get("monthly_churn_pct", [None] * 8)[i],
                "mobile_arpu": mob_data.get("mobile_arpu_clp", [None] * 8)[i],
                # Broadband (in thousands)
                "broadband_total_k": bb_total_m * 1000 if bb_total_m is not None else None,
                "broadband_net_adds_k": fix_data.get("net_adds_k", [None] * 8)[i],
                "broadband_cable_k": cable_m * 1000 if cable_m is not None else None,
                "broadband_fiber_k": fiber_m * 1000 if fiber_m is not None else None,
                "broadband_dsl_k": dsl_m * 1000 if dsl_m is not None else None,
                "broadband_arpu": fix_data.get("broadband_arpu_clp", [None] * 8)[i],
                # TV (in thousands)
                "tv_total_k": tv_m * 1000 if tv_m is not None else None,
                "tv_net_adds_k": tv_data.get("tv_net_adds_k", [None] * 8)[i],
                # FMC (in thousands)
                "fmc_total_k": fmc_m * 1000 if fmc_m is not None else None,
                "fmc_penetration_pct": tv_data.get("fmc_penetration_pct", [None] * 8)[i],
                # Source
                "source_url": mob_data.get("_source", ""),
            }

            db.upsert_subscriber(op_id, period, subscriber)
            count += 1

    print(f"  Inserted {count} subscriber quarterly records")


def seed_competitive_scores(db: TelecomDatabase):
    """Insert competitive scores for CQ4_2025."""
    from src.blm._legacy.chile_market_comprehensive_data import COMPETITIVE_SCORES

    calendar_quarter = "CQ4_2025"
    count = 0

    for legacy_name, scores in COMPETITIVE_SCORES.items():
        op_id = LEGACY_NAME_TO_ID.get(legacy_name)
        if not op_id:
            print(f"  WARNING: Unknown operator '{legacy_name}', skipping")
            continue

        db.upsert_competitive_scores(op_id, calendar_quarter, scores)
        count += len(scores)

    print(f"  Inserted {count} competitive score records")


def seed_macro_data(db: TelecomDatabase):
    """Insert macro environment data for Chile across all 8 quarters."""
    from src.blm._legacy.chile_market_comprehensive_data import (
        MACRO_DATA_CHILE_2025,
        MARKET_SUMMARY_8Q,
    )
    from src.database.period_utils import get_converter

    converter = get_converter("entel_cl")

    # Insert for all 8 quarters
    for i in range(8):
        pi = converter.to_calendar_quarter(CALENDAR_QUARTERS_8Q[i])
        cq = pi.calendar_quarter

        macro = {
            "gdp_growth_pct": MACRO_DATA_CHILE_2025.get("gdp_growth_pct"),
            "inflation_pct": MACRO_DATA_CHILE_2025.get("inflation_pct"),
            "regulatory_environment": MACRO_DATA_CHILE_2025.get("regulatory_environment"),
            "five_g_adoption_pct": MARKET_SUMMARY_8Q.get("5g_adoption_pct", [None] * 8)[i],
            "fiber_penetration_pct": MARKET_SUMMARY_8Q.get("fiber_penetration_pct", [None] * 8)[i],
            "source_url": MARKET_SUMMARY_8Q.get("_source", ""),
        }

        # Add extra detail for the latest quarter
        if i == 7:
            macro["digital_strategy"] = (
                f"5G adoption: {MARKET_SUMMARY_8Q.get('5g_adoption_pct', [None] * 8)[7]}%, "
                f"Fiber penetration: {MARKET_SUMMARY_8Q.get('fiber_penetration_pct', [None] * 8)[7]}%, "
                f"Mobile penetration: {MACRO_DATA_CHILE_2025.get('mobile_penetration_pct', '')}%"
            )

        db.upsert_macro("Chile", cq, macro)

    print(f"  Inserted 8 macro environment records")


def seed_network_data(db: TelecomDatabase):
    """Insert network infrastructure data — single snapshot at CQ4_2025."""
    from src.blm._legacy.chile_market_comprehensive_data import NETWORK_INFRASTRUCTURE

    calendar_quarter = "CQ4_2025"
    count = 0

    for legacy_name, net_data in NETWORK_INFRASTRUCTURE.items():
        op_id = LEGACY_NAME_TO_ID.get(legacy_name)
        if not op_id:
            print(f"  WARNING: Unknown operator '{legacy_name}', skipping")
            continue

        mobile = net_data.get("mobile_network", {})
        fixed = net_data.get("fixed_network", {})

        network = {
            "five_g_coverage_pct": mobile.get("5g_population_coverage_pct"),
            "four_g_coverage_pct": mobile.get("4g_population_coverage_pct"),
            "fiber_homepass_k": (
                fixed.get("fiber_homes_passed_m", 0) * 1000
                if fixed.get("fiber_homes_passed_m") is not None else None
            ),
            "cable_homepass_k": (
                fixed.get("cable_homes_passed_m", 0) * 1000
                if fixed.get("cable_homes_passed_m") is not None else None
            ),
            "cable_docsis31_pct": fixed.get("docsis_31_coverage_pct"),
            "technology_mix": {
                "mobile_vendor": mobile.get("technology"),
                "5g_sa_status": mobile.get("5g_sa_status"),
                "spectrum_mhz": mobile.get("spectrum_holdings_mhz"),
                "5g_base_stations": mobile.get("5g_base_stations"),
                "core_vendor": net_data.get("core_network", {}).get("vendor"),
                "virtualization_pct": net_data.get("core_network", {}).get("virtualization_pct"),
                "edge_nodes": net_data.get("core_network", {}).get("edge_nodes"),
            },
            "source_url": net_data.get("_source", ""),
        }

        db.upsert_network(op_id, calendar_quarter, network)
        count += 1

    print(f"  Inserted {count} network infrastructure records")


def seed_all(db_path: str = "data/telecom.db"):
    """Run complete Chile seed process.

    Args:
        db_path: Path to SQLite database. Use ":memory:" for testing.

    Returns:
        The initialized TelecomDatabase instance.
    """
    print(f"Seeding Chile market data: {db_path}")
    db = TelecomDatabase(db_path)
    db.init()

    print("Step 1/6: Registering operators...")
    seed_operators(db)

    print("Step 2/6: Inserting financial data (8 quarters x 4 operators)...")
    seed_financial_data(db)

    print("Step 3/6: Inserting subscriber data (8 quarters x 4 operators)...")
    seed_subscriber_data(db)

    print("Step 4/6: Inserting competitive scores...")
    seed_competitive_scores(db)

    print("Step 5/6: Inserting macro environment data...")
    seed_macro_data(db)

    print("Step 6/6: Inserting network infrastructure data...")
    seed_network_data(db)

    # Seed tariff data
    print("Bonus: Inserting tariff data...")
    from src.database.seed_tariffs_chile import seed_tariffs_chile
    seed_tariffs_chile(db)

    print("Chile seed complete!")
    return db


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Seed Chile telecom database")
    parser.add_argument(
        "--db-path", default="data/telecom.db",
        help="Path to SQLite database (default: data/telecom.db)",
    )
    args = parser.parse_args()

    seed_all(args.db_path)
