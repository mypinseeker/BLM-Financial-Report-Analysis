"""Seed the database with Germany telecom market data from legacy files.

Reads hardcoded data from the legacy analysis files and inserts them
into the SQLite database using proper fiscal period alignment.

The legacy files use Vodafone's fiscal quarter labels (Q4 FY24 through Q3 FY26)
as array indices for ALL operators. For Vodafone these are actual fiscal periods;
for DT/O2/1&1 (calendar-year operators) the same indices map to the same
calendar quarters because the data was collected at the same time.

Calendar quarter mapping of the 8 data positions:
  Index 0: Q4 FY24 = CQ1_2024  (Jan-Mar 2024)
  Index 1: Q1 FY25 = CQ2_2024  (Apr-Jun 2024)
  Index 2: Q2 FY25 = CQ3_2024  (Jul-Sep 2024)
  Index 3: Q3 FY25 = CQ4_2024  (Oct-Dec 2024)
  Index 4: Q4 FY25 = CQ1_2025  (Jan-Mar 2025)
  Index 5: Q1 FY26 = CQ2_2025  (Apr-Jun 2025)
  Index 6: Q2 FY26 = CQ3_2025  (Jul-Sep 2025)
  Index 7: Q3 FY26 = CQ4_2025  (Oct-Dec 2025)
"""

import sys
from pathlib import Path

# Add project root to path for imports
_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.database.db import TelecomDatabase
from src.database.operator_directory import OPERATOR_DIRECTORY
from src.database.period_utils import get_converter
from src.database.seed_internet_data import seed_internet_data


# ============================================================================
# Vodafone fiscal quarter labels used as index keys in legacy data
# ============================================================================
VODAFONE_QUARTERS_8Q = [
    "Q4 FY24", "Q1 FY25", "Q2 FY25", "Q3 FY25",
    "Q4 FY25", "Q1 FY26", "Q2 FY26", "Q3 FY26",
]

# Calendar-year equivalent quarters for DT/O2/1&1
CALENDAR_QUARTERS_8Q = [
    "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024",
    "Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025",
]

# Mapping from legacy operator display names to our operator IDs
LEGACY_NAME_TO_ID = {
    "Vodafone Germany": "vodafone_germany",
    "Deutsche Telekom": "deutsche_telekom",
    "Deutsche Telekom Germany": "deutsche_telekom",
    "Telefónica O2 Germany": "telefonica_o2",
    "Telefonica O2 Germany": "telefonica_o2",
    "1&1 AG": "one_and_one",
}


def _get_period_for_operator(operator_id: str, quarter_index: int) -> str:
    """Get the operator-specific period string for a given quarter index."""
    if operator_id == "vodafone_germany":
        return VODAFONE_QUARTERS_8Q[quarter_index]
    else:
        return CALENDAR_QUARTERS_8Q[quarter_index]


def seed_operators(db: TelecomDatabase):
    """Register all 4 Germany market operators."""
    for op_id, info in OPERATOR_DIRECTORY.items():
        if info["market"] == "germany":
            db.upsert_operator(op_id, **info)
    print(f"  Registered {len([k for k, v in OPERATOR_DIRECTORY.items() if v['market'] == 'germany'])} operators")


def seed_financial_data(db: TelecomDatabase):
    """Insert 8 quarters of financial data from legacy REVENUE, PROFITABILITY, INVESTMENT data."""
    # Import legacy data inline to avoid import errors if legacy code has dependencies
    from src.blm._legacy.germany_market_comprehensive_data import (
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

        # Get profitability and investment data for same operator
        prof_data = PROFITABILITY_DATA_8Q.get(legacy_name, {})
        inv_data = INVESTMENT_DATA_8Q.get(legacy_name, {})

        for i in range(8):
            period = _get_period_for_operator(op_id, i)

            # Employees are in thousands in legacy data, convert to count
            employees_k = inv_data.get("employees_k", [None]*8)[i]
            employees = int(employees_k * 1000) if employees_k is not None else None

            financial = {
                # Revenue (EUR millions)
                "total_revenue": rev_data.get("total_revenue", [None]*8)[i],
                "service_revenue": rev_data.get("service_revenue", [None]*8)[i],
                "service_revenue_growth_pct": rev_data.get("service_revenue_growth_pct", [None]*8)[i],
                "mobile_service_revenue": rev_data.get("mobile_service_revenue", [None]*8)[i],
                "mobile_service_growth_pct": rev_data.get("mobile_service_growth_pct", [None]*8)[i],
                "fixed_service_revenue": rev_data.get("fixed_service_revenue", [None]*8)[i],
                "fixed_service_growth_pct": rev_data.get("fixed_service_growth_pct", [None]*8)[i],
                "b2b_revenue": rev_data.get("b2b_revenue", [None]*8)[i],
                "b2b_growth_pct": rev_data.get("b2b_growth_pct", [None]*8)[i],
                "tv_revenue": rev_data.get("tv_revenue", [None]*8)[i],
                "wholesale_revenue": rev_data.get("wholesale_revenue", [None]*8)[i],
                # Profitability
                "ebitda": prof_data.get("ebitda", [None]*8)[i],
                "ebitda_margin_pct": prof_data.get("ebitda_margin_pct", [None]*8)[i],
                "ebitda_growth_pct": prof_data.get("ebitda_growth_pct", [None]*8)[i],
                "net_income": prof_data.get("net_income", [None]*8)[i],
                # Investment
                "capex": inv_data.get("capex", [None]*8)[i],
                "capex_to_revenue_pct": inv_data.get("capex_to_revenue_pct", [None]*8)[i],
                "opex": inv_data.get("opex", [None]*8)[i],
                "opex_to_revenue_pct": inv_data.get("opex_to_revenue_pct", [None]*8)[i],
                "employees": employees,
                # Source
                "source_url": rev_data.get("_source", ""),
            }

            db.upsert_financial(op_id, period, financial)
            count += 1

    print(f"  Inserted {count} financial quarterly records")


def seed_subscriber_data(db: TelecomDatabase):
    """Insert 8 quarters of subscriber data from legacy MOBILE, FIXED, TV/FMC, B2B data."""
    from src.blm._legacy.germany_market_comprehensive_data import (
        MOBILE_BUSINESS_DATA_8Q,
        FIXED_BROADBAND_DATA_8Q,
        TV_FMC_DATA_8Q,
        B2B_BUSINESS_DATA_8Q,
    )

    count = 0
    for legacy_name, mob_data in MOBILE_BUSINESS_DATA_8Q.items():
        op_id = LEGACY_NAME_TO_ID.get(legacy_name)
        if not op_id:
            print(f"  WARNING: Unknown operator '{legacy_name}', skipping")
            continue

        # Get fixed, TV/FMC, B2B data
        fix_data = FIXED_BROADBAND_DATA_8Q.get(legacy_name, {})
        tv_data = TV_FMC_DATA_8Q.get(legacy_name, {})
        b2b_data = B2B_BUSINESS_DATA_8Q.get(legacy_name, {})

        for i in range(8):
            period = _get_period_for_operator(op_id, i)

            # Mobile data - convert from millions to thousands
            total_mobile_m = mob_data.get("total_mobile_subs_m", [None]*8)[i]
            postpaid_m = mob_data.get("postpaid_subs_m", [None]*8)[i]
            prepaid_m = mob_data.get("prepaid_subs_m", [None]*8)[i]
            iot_m = mob_data.get("iot_connections_m", [None]*8)[i]

            # Fixed broadband - convert from millions to thousands
            bb_total_m = fix_data.get("broadband_subs_m", [None]*8)[i]
            fiber_m = fix_data.get("fiber_ftth_subs_m", [None]*8)[i]
            cable_m = fix_data.get("cable_docsis_subs_m", [None]*8)[i]
            dsl_m = fix_data.get("dsl_copper_subs_m", [None]*8)[i]

            # TV/FMC - convert from millions to thousands
            tv_m = tv_data.get("tv_subs_m", [None]*8)[i]
            fmc_m = tv_data.get("fmc_subs_m", [None]*8)[i]

            subscriber = {
                # Mobile (in thousands)
                "mobile_total_k": total_mobile_m * 1000 if total_mobile_m is not None else None,
                "mobile_postpaid_k": postpaid_m * 1000 if postpaid_m is not None else None,
                "mobile_prepaid_k": prepaid_m * 1000 if prepaid_m is not None else None,
                "mobile_net_adds_k": mob_data.get("net_adds_k", [None]*8)[i],
                "mobile_churn_pct": mob_data.get("monthly_churn_pct", [None]*8)[i],
                "mobile_arpu": mob_data.get("mobile_arpu_eur", [None]*8)[i],
                # IoT (in thousands)
                "iot_connections_k": iot_m * 1000 if iot_m is not None else None,
                # Broadband (in thousands)
                "broadband_total_k": bb_total_m * 1000 if bb_total_m is not None else None,
                "broadband_net_adds_k": fix_data.get("net_adds_k", [None]*8)[i],
                "broadband_cable_k": cable_m * 1000 if cable_m is not None else None,
                "broadband_fiber_k": fiber_m * 1000 if fiber_m is not None else None,
                "broadband_dsl_k": dsl_m * 1000 if dsl_m is not None else None,
                "broadband_arpu": fix_data.get("broadband_arpu_eur", [None]*8)[i],
                # TV (in thousands)
                "tv_total_k": tv_m * 1000 if tv_m is not None else None,
                "tv_net_adds_k": tv_data.get("tv_net_adds_k", [None]*8)[i],
                # FMC (in thousands)
                "fmc_total_k": fmc_m * 1000 if fmc_m is not None else None,
                "fmc_penetration_pct": tv_data.get("fmc_penetration_pct", [None]*8)[i],
                # B2B
                "b2b_customers_k": b2b_data.get("b2b_customers_k", [None]*8)[i],
                # Source
                "source_url": mob_data.get("_source", ""),
            }

            db.upsert_subscriber(op_id, period, subscriber)
            count += 1

    print(f"  Inserted {count} subscriber quarterly records")


def seed_competitive_scores(db: TelecomDatabase):
    """Insert competitive scores from legacy COMPETITIVE_SCORES_Q3_FY26."""
    from src.blm._legacy.germany_telecom_analysis import COMPETITIVE_SCORES_Q3_FY26

    # These scores are for Q3 FY26 = CQ4_2025
    calendar_quarter = "CQ4_2025"
    count = 0

    for legacy_name, scores in COMPETITIVE_SCORES_Q3_FY26.items():
        op_id = LEGACY_NAME_TO_ID.get(legacy_name)
        if not op_id:
            print(f"  WARNING: Unknown operator '{legacy_name}', skipping")
            continue

        db.upsert_competitive_scores(op_id, calendar_quarter, scores)
        count += len(scores)

    print(f"  Inserted {count} competitive score records")


def seed_macro_data(db: TelecomDatabase):
    """Insert macro environment data from legacy MACRO_DATA_GERMANY_2025.

    The legacy data is a single snapshot; we store it under the latest
    available quarter CQ4_2025.
    """
    from src.blm._legacy.germany_telecom_analysis import MACRO_DATA_GERMANY_2025
    from src.blm._legacy.germany_market_comprehensive_data import MARKET_SUMMARY_8Q

    # Insert market-level macro data for CQ4_2025
    macro = {
        "gdp_growth_pct": MACRO_DATA_GERMANY_2025.get("gdp_growth_pct"),
        "inflation_pct": MACRO_DATA_GERMANY_2025.get("inflation_pct"),
        "regulatory_environment": MACRO_DATA_GERMANY_2025.get("regulatory_environment"),
        "five_g_adoption_pct": MARKET_SUMMARY_8Q.get("5g_adoption_pct", [None]*8)[7],
        "fiber_penetration_pct": MARKET_SUMMARY_8Q.get("fiber_penetration_pct", [None]*8)[7],
        "digital_strategy": (
            f"Fiber target 2025: {MACRO_DATA_GERMANY_2025.get('fiber_target_2025_pct', '')}%, "
            f"2030: {MACRO_DATA_GERMANY_2025.get('fiber_target_2030_pct', '')}%"
        ),
        "source_url": MARKET_SUMMARY_8Q.get("_source", ""),
    }

    db.upsert_macro("Germany", "CQ4_2025", macro)

    # Also insert macro data for earlier quarters using market summary
    for i in range(7):  # First 7 quarters
        converter = get_converter("vodafone_germany")
        pi = converter.to_calendar_quarter(VODAFONE_QUARTERS_8Q[i])
        cq = pi.calendar_quarter

        macro_q = {
            "gdp_growth_pct": MACRO_DATA_GERMANY_2025.get("gdp_growth_pct"),
            "inflation_pct": MACRO_DATA_GERMANY_2025.get("inflation_pct"),
            "five_g_adoption_pct": MARKET_SUMMARY_8Q.get("5g_adoption_pct", [None]*8)[i],
            "fiber_penetration_pct": MARKET_SUMMARY_8Q.get("fiber_penetration_pct", [None]*8)[i],
            "regulatory_environment": MACRO_DATA_GERMANY_2025.get("regulatory_environment"),
            "source_url": MARKET_SUMMARY_8Q.get("_source", ""),
        }
        db.upsert_macro("Germany", cq, macro_q)

    print(f"  Inserted 8 macro environment records")


def seed_network_data(db: TelecomDatabase):
    """Insert network infrastructure data from legacy NETWORK_INFRASTRUCTURE.

    The legacy data is a single snapshot (not quarterly), so we store it
    under CQ4_2025 (the latest quarter).
    """
    from src.blm._legacy.germany_market_comprehensive_data import NETWORK_INFRASTRUCTURE

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


def seed_executives(db: TelecomDatabase):
    """Insert executive data from legacy EXECUTIVE_CHANGES."""
    from src.blm._legacy.germany_market_comprehensive_data import EXECUTIVE_CHANGES

    count = 0
    for legacy_name, exec_data in EXECUTIVE_CHANGES.items():
        op_id = LEGACY_NAME_TO_ID.get(legacy_name)
        if not op_id:
            print(f"  WARNING: Unknown operator '{legacy_name}', skipping")
            continue

        # Insert C-level executives
        for role in ["ceo", "cfo", "cto"]:
            if role in exec_data:
                info = exec_data[role]
                db.upsert_executive(op_id, {
                    "name": info.get("name"),
                    "title": role.upper(),
                    "start_date": info.get("since"),
                    "is_current": 1,
                    "background": info.get("background"),
                })
                count += 1

    print(f"  Inserted {count} executive records")


def seed_all(db_path: str = "data/telecom.db"):
    """Run complete seed process.

    Args:
        db_path: Path to SQLite database. Use ":memory:" for testing.

    Returns:
        The initialized TelecomDatabase instance.
    """
    print(f"Seeding database: {db_path}")
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

    # Also seed executives
    print("Bonus: Inserting executive data...")
    seed_executives(db)

    # Seed internet-sourced data (regulatory, earnings call Q&A, media)
    print("\nStep 7/8: Seeding internet-sourced data...")
    seed_internet_data(db)

    # Seed tariff data
    print("Step 8/8: Inserting tariff data...")
    from src.database.seed_tariffs import seed_tariffs
    seed_tariffs(db)

    print("Seed complete!")
    return db


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Seed Germany telecom database")
    parser.add_argument(
        "--db-path", default="data/telecom.db",
        help="Path to SQLite database (default: data/telecom.db)"
    )
    args = parser.parse_args()

    seed_all(args.db_path)
