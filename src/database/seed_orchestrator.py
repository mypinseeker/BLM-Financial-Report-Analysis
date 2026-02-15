"""Seed orchestrator — seeds all 17 markets into a single SQLite DB.

Used by cli_group_local.py and cli_push_all.py to prepare a complete
local database with Germany, Chile, 10 LATAM Millicom markets,
Netherlands, Belgium, France, Italy, and Poland.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.database.db import TelecomDatabase
from src.database.seed_latam_helper import seed_market

# All 17 markets in the system
ALL_MARKETS = [
    "germany", "chile",
    "guatemala", "colombia", "honduras", "paraguay", "bolivia",
    "el_salvador", "panama", "nicaragua", "ecuador", "uruguay",
    "netherlands", "belgium", "france", "italy", "poland",
]

# European markets with shared get_seed_data() pattern
EUROPE_MARKETS = ["netherlands", "belgium", "france", "italy", "poland"]

# 10 LATAM markets with shared seed_market() pattern
LATAM_MARKETS = [
    "guatemala", "colombia", "honduras", "paraguay", "bolivia",
    "el_salvador", "panama", "nicaragua", "ecuador", "uruguay",
]

# Tigo operator for each LATAM market (used for group analysis)
TIGO_OPERATORS = [
    ("tigo_guatemala", "guatemala"),
    ("tigo_colombia", "colombia"),
    ("tigo_honduras", "honduras"),
    ("tigo_paraguay", "paraguay"),
    ("tigo_bolivia", "bolivia"),
    ("tigo_el_salvador", "el_salvador"),
    ("tigo_panama", "panama"),
    ("tigo_nicaragua", "nicaragua"),
    ("tigo_ecuador", "ecuador"),
    ("tigo_uruguay", "uruguay"),
]


def seed_all_markets(db_path: str = ":memory:") -> TelecomDatabase:
    """Seed all 17 markets into a single SQLite database.

    Args:
        db_path: Path to SQLite database. Use ":memory:" for in-memory.

    Returns:
        Initialized TelecomDatabase with all market data.
    """
    db = TelecomDatabase(db_path)
    db.init()

    # Apply v3 schema (operator_groups, group_subsidiaries, analysis_jobs)
    _apply_v3_schema(db)

    # 1. Seed Germany (uses its own seed_all pattern)
    print("\n[1/18] Seeding Germany...")
    from src.database.seed_germany import seed_all as seed_germany
    # seed_germany creates its own db, but we can call the individual steps
    # Instead, we re-use the db by calling the step functions directly
    _seed_germany_into(db)

    # 2. Seed Chile (uses its own seed_all pattern)
    print("\n[2/18] Seeding Chile...")
    _seed_chile_into(db)

    # 3-12. Seed 10 LATAM markets via shared helper
    for i, market_id in enumerate(LATAM_MARKETS, 3):
        print(f"\n[{i}/18] Seeding {market_id}...")
        _seed_latam_market(db, market_id)

    # 13. Seed Millicom group structure
    print("\n[13/18] Seeding Millicom group structure...")
    from src.database.seed_millicom import seed_all_millicom
    seed_all_millicom(db)

    # 14-18. Seed European markets (Netherlands, Belgium, France, Italy, Poland)
    for i, market_id in enumerate(EUROPE_MARKETS, 14):
        print(f"\n[{i}/18] Seeding {market_id}...")
        _seed_europe_market(db, market_id)

    print(f"\n{'='*60}")
    print(f"  All 17 markets seeded successfully")
    print(f"{'='*60}")

    return db


def _apply_v3_schema(db: TelecomDatabase):
    """Apply schema v3 extensions (operator_groups, group_subsidiaries, etc.)."""
    schema_v3 = Path(__file__).parent / "supabase_schema_v3.sql"
    if not schema_v3.exists():
        return
    sql = schema_v3.read_text()
    for statement in sql.split(";"):
        # Strip comment-only lines from the statement
        code_lines = [
            line for line in statement.split("\n")
            if line.strip() and not line.strip().startswith("--")
        ]
        stmt = "\n".join(code_lines).strip()
        if not stmt:
            continue
        try:
            db.conn.execute(stmt)
        except Exception:
            pass

    # Also create market_configs table (defined in supabase_schema.sql for Postgres,
    # but needed in SQLite for seed_millicom)
    db.conn.execute("""
        CREATE TABLE IF NOT EXISTS market_configs (
            market_id TEXT PRIMARY KEY,
            market_name TEXT NOT NULL,
            country TEXT NOT NULL,
            currency TEXT NOT NULL DEFAULT 'EUR',
            currency_symbol TEXT DEFAULT '€',
            regulatory_body TEXT,
            population_k REAL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.conn.commit()


def _seed_germany_into(db: TelecomDatabase):
    """Seed Germany data into an existing db (without creating a new one)."""
    from src.database import seed_germany as sg
    sg.seed_operators(db)
    sg.seed_financial_data(db)
    sg.seed_subscriber_data(db)
    sg.seed_competitive_scores(db)
    sg.seed_macro_data(db)
    sg.seed_network_data(db)
    sg.seed_executives(db)
    try:
        from src.database.seed_internet_data import seed_internet_data
        seed_internet_data(db)
    except Exception:
        pass
    try:
        from src.database.seed_tariffs import seed_tariffs
        seed_tariffs(db)
    except Exception:
        pass
    print("Germany seed complete!")


def _seed_chile_into(db: TelecomDatabase):
    """Seed Chile data into an existing db (without creating a new one)."""
    from src.database import seed_chile as sc
    sc.seed_operators(db)
    sc.seed_financial_data(db)
    sc.seed_subscriber_data(db)
    sc.seed_competitive_scores(db)
    sc.seed_macro_data(db)
    sc.seed_network_data(db)
    sc.seed_executives(db)
    try:
        from src.database.seed_tariffs_chile import seed_tariffs_chile
        seed_tariffs_chile(db)
    except Exception:
        pass
    print("Chile seed complete!")


def _seed_latam_market(db: TelecomDatabase, market_id: str):
    """Seed a single LATAM market using the shared helper."""
    import importlib
    mod = importlib.import_module(f"src.database.seed_{market_id}")
    data = mod.get_seed_data()
    seed_market(
        db=db,
        market_id=mod.MARKET_ID,
        operators=mod.OPERATORS,
        **data,
    )


def _seed_europe_market(db: TelecomDatabase, market_id: str):
    """Seed a European market using the shared helper (same pattern as LATAM)."""
    import importlib
    mod = importlib.import_module(f"src.database.seed_{market_id}")
    data = mod.get_seed_data()
    seed_market(
        db=db,
        market_id=mod.MARKET_ID,
        operators=mod.OPERATORS,
        **data,
    )
