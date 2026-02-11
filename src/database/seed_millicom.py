"""Seed the database with Millicom (Tigo) group data.

Registers:
  - Millicom as an operator group
  - 9 LATAM market operators (Tigo subsidiaries + competitors)
  - Group-subsidiary relationships

This script works with both Supabase (via REST) and SQLite (via TelecomDatabase).
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.database.operator_directory import (
    OPERATOR_DIRECTORY,
    OPERATOR_GROUPS,
    get_operators_for_group,
    get_operators_for_market,
)

# ============================================================================
# Millicom subsidiary definitions with ownership details
# ============================================================================

MILLICOM_SUBSIDIARIES = [
    {
        "operator_id": "tigo_guatemala",
        "market": "guatemala",
        "ownership_pct": 100.0,
        "ownership_type": "direct",
        "local_brand": "Tigo Guatemala",
        "is_active": True,
    },
    {
        "operator_id": "tigo_honduras",
        "market": "honduras",
        "ownership_pct": 100.0,
        "ownership_type": "direct",
        "local_brand": "Tigo Honduras",
        "is_active": True,
    },
    {
        "operator_id": "tigo_el_salvador",
        "market": "el_salvador",
        "ownership_pct": 100.0,
        "ownership_type": "direct",
        "local_brand": "Tigo El Salvador",
        "is_active": True,
    },
    {
        "operator_id": "tigo_colombia",
        "market": "colombia",
        "ownership_pct": 50.0,
        "ownership_type": "joint_venture",
        "local_brand": "Tigo-UNE Colombia",
        "is_active": True,
    },
    {
        "operator_id": "tigo_panama",
        "market": "panama",
        "ownership_pct": 100.0,
        "ownership_type": "direct",
        "local_brand": "Tigo Panama",
        "is_active": True,
    },
    {
        "operator_id": "tigo_bolivia",
        "market": "bolivia",
        "ownership_pct": 100.0,
        "ownership_type": "direct",
        "local_brand": "Tigo Bolivia",
        "is_active": True,
    },
    {
        "operator_id": "tigo_paraguay",
        "market": "paraguay",
        "ownership_pct": 100.0,
        "ownership_type": "direct",
        "local_brand": "Tigo Paraguay",
        "is_active": True,
    },
    {
        "operator_id": "tigo_nicaragua",
        "market": "nicaragua",
        "ownership_pct": 100.0,
        "ownership_type": "direct",
        "local_brand": "Tigo Nicaragua",
        "is_active": True,
    },
    {
        "operator_id": "tigo_chile",
        "market": "chile",
        "ownership_pct": 100.0,
        "ownership_type": "direct",
        "local_brand": "Tigo Chile",
        "is_active": True,
    },
]

# Markets where Tigo operates and their competitors
LATAM_MARKETS = [
    "guatemala", "honduras", "el_salvador", "colombia",
    "panama", "bolivia", "paraguay", "nicaragua", "chile",
]


def seed_millicom_group(db):
    """Register Millicom as an operator group.

    Args:
        db: TelecomDatabase instance (SQLite)
    """
    group = OPERATOR_GROUPS["millicom"]
    db.execute(
        """INSERT OR REPLACE INTO operator_groups
           (group_id, group_name, brand_name, headquarters, ir_url,
            stock_ticker, markets_count, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            group["group_id"],
            group["group_name"],
            group["brand_name"],
            group["headquarters"],
            group["ir_url"],
            group["stock_ticker"],
            group["markets_count"],
            group.get("notes", ""),
        ),
    )
    print(f"  Registered group: {group['group_name']}")


def seed_latam_operators(db):
    """Register all LATAM operators (Tigo subsidiaries + competitors)."""
    count = 0
    for market in LATAM_MARKETS:
        for op_id in get_operators_for_market(market):
            info = OPERATOR_DIRECTORY[op_id]
            db.upsert_operator(op_id, **info)
            count += 1

    print(f"  Registered {count} LATAM operators across {len(LATAM_MARKETS)} markets")


def seed_subsidiaries(db):
    """Register Millicom group-subsidiary relationships."""
    count = 0
    for sub in MILLICOM_SUBSIDIARIES:
        db.execute(
            """INSERT OR REPLACE INTO group_subsidiaries
               (group_id, operator_id, market, ownership_pct,
                ownership_type, local_brand, is_active)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                "millicom",
                sub["operator_id"],
                sub["market"],
                sub["ownership_pct"],
                sub["ownership_type"],
                sub["local_brand"],
                sub["is_active"],
            ),
        )
        count += 1

    print(f"  Registered {count} Millicom subsidiaries")


def seed_market_configs_to_db(db):
    """Register market_configs rows for all 9 LATAM markets."""
    from src.models.market_configs import MARKET_REGISTRY

    count = 0
    for market_id in LATAM_MARKETS:
        config = MARKET_REGISTRY.get(market_id)
        if not config:
            print(f"  WARNING: No MarketConfig for '{market_id}'")
            continue

        db.execute(
            """INSERT OR REPLACE INTO market_configs
               (market_id, market_name, country, currency, regulatory_body)
               VALUES (?, ?, ?, ?, ?)""",
            (
                config.market_id,
                config.market_name,
                config.country,
                config.currency,
                config.regulatory_body,
            ),
        )
        count += 1

    print(f"  Registered {count} LATAM market configs")


def seed_all_millicom(db):
    """Run complete Millicom seed process.

    Args:
        db: TelecomDatabase instance
    """
    print("Seeding Millicom (Tigo) group data...")

    print("\nStep 1/4: Registering Millicom group...")
    seed_millicom_group(db)

    print("Step 2/4: Registering LATAM operators...")
    seed_latam_operators(db)

    print("Step 3/4: Registering subsidiaries...")
    seed_subsidiaries(db)

    print("Step 4/4: Registering market configs...")
    seed_market_configs_to_db(db)

    print("\nMillicom seed complete!")


if __name__ == "__main__":
    from src.database.db import TelecomDatabase
    import argparse

    parser = argparse.ArgumentParser(description="Seed Millicom group data")
    parser.add_argument(
        "--db-path", default="data/telecom.db",
        help="Path to SQLite database (default: data/telecom.db)",
    )
    args = parser.parse_args()

    db = TelecomDatabase(args.db_path)
    db.init()

    # Ensure v3 schema tables exist
    schema_v3 = Path(__file__).parent / "supabase_schema_v3.sql"
    if schema_v3.exists():
        print("Applying schema v3...")
        sql = schema_v3.read_text()
        for statement in sql.split(";"):
            stmt = statement.strip()
            if stmt and not stmt.startswith("--"):
                try:
                    db.execute(stmt)
                except Exception as e:
                    # Ignore "duplicate column" etc.
                    if "duplicate" not in str(e).lower():
                        print(f"  Note: {e}")

    seed_all_millicom(db)
