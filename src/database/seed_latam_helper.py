"""Shared seeding helper for LATAM market data.

Each market seed file defines DATA dicts and calls this helper to do the DB work.
Avoids duplicating the same upsert-loop logic across 11 market seed files.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.database.db import TelecomDatabase
from src.database.operator_directory import OPERATOR_DIRECTORY


# Calendar quarter labels — all LATAM Millicom operators use calendar year
CALENDAR_QUARTERS_8Q = [
    "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024",
    "Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025",
]


def seed_market(
    db: TelecomDatabase,
    market_id: str,
    operators: list[str],
    financials: dict[str, dict],
    subscribers: dict[str, dict],
    macro: dict,
    network: dict[str, dict],
    executives: dict[str, list[dict]],
    competitive_scores: dict[str, dict[str, float]],
    intelligence_events: list[dict] | None = None,
    earnings_highlights: dict[str, list[dict]] | None = None,
):
    """Seed all data for a single LATAM market.

    Args:
        db: Initialized TelecomDatabase instance
        market_id: Market identifier (e.g. "guatemala")
        operators: List of operator_ids to register from OPERATOR_DIRECTORY
        financials: operator_id → {field: [8 quarterly values]}
        subscribers: operator_id → {field: [8 quarterly values]}
        macro: {field: value} for macro_environment (single snapshot at CQ4_2025)
        network: operator_id → {field: value} for network_infrastructure (CQ4_2025)
        executives: operator_id → [{name, title, start_date, background}]
        competitive_scores: operator_id → {dimension: score}
        intelligence_events: [{operator_id, market, event_date, category, title, ...}]
        earnings_highlights: operator_id → [{segment, highlight_type, content, speaker}]
    """
    country = OPERATOR_DIRECTORY[operators[0]]["country"]
    print(f"\nSeeding {market_id} market data...")

    # Step 1: Register operators
    count = 0
    for op_id in operators:
        if op_id in OPERATOR_DIRECTORY:
            db.upsert_operator(op_id, **OPERATOR_DIRECTORY[op_id])
            count += 1
    print(f"  Step 1/7: Registered {count} operators")

    # Step 2: Financial data (8 quarters per operator)
    count = 0
    for op_id, fin_data in financials.items():
        for i in range(8):
            period = CALENDAR_QUARTERS_8Q[i]
            financial = {}
            for field_name, values in fin_data.items():
                if field_name.startswith("_"):
                    continue
                if isinstance(values, list) and len(values) >= 8:
                    financial[field_name] = values[i]
                else:
                    financial[field_name] = values
            financial.setdefault("source_url", fin_data.get("_source", ""))
            db.upsert_financial(op_id, period, financial)
            count += 1
    print(f"  Step 2/7: Inserted {count} financial quarterly records")

    # Step 3: Subscriber data (8 quarters per operator)
    count = 0
    for op_id, sub_data in subscribers.items():
        for i in range(8):
            period = CALENDAR_QUARTERS_8Q[i]
            subscriber = {}
            for field_name, values in sub_data.items():
                if field_name.startswith("_"):
                    continue
                if isinstance(values, list) and len(values) >= 8:
                    subscriber[field_name] = values[i]
                else:
                    subscriber[field_name] = values
            subscriber.setdefault("source_url", sub_data.get("_source", ""))
            db.upsert_subscriber(op_id, period, subscriber)
            count += 1
    print(f"  Step 3/7: Inserted {count} subscriber quarterly records")

    # Step 4: Competitive scores (CQ4_2025)
    count = 0
    for op_id, scores in competitive_scores.items():
        db.upsert_competitive_scores(op_id, "CQ4_2025", scores)
        count += len(scores)
    print(f"  Step 4/7: Inserted {count} competitive score records")

    # Step 5: Macro environment (8 quarters, same snapshot data)
    for i in range(8):
        period = CALENDAR_QUARTERS_8Q[i]
        from src.database.period_utils import PeriodConverter
        converter = PeriodConverter()
        pi = converter.to_calendar_quarter(period)
        db.upsert_macro(country, pi.calendar_quarter, macro)
    print(f"  Step 5/7: Inserted 8 macro environment records")

    # Step 6: Network infrastructure (CQ4_2025 snapshot)
    count = 0
    for op_id, net_data in network.items():
        db.upsert_network(op_id, "CQ4_2025", net_data)
        count += 1
    print(f"  Step 6/7: Inserted {count} network infrastructure records")

    # Step 7: Executives
    count = 0
    for op_id, exec_list in executives.items():
        for exec_data in exec_list:
            db.upsert_executive(op_id, exec_data)
            count += 1
    print(f"  Step 7/7: Inserted {count} executive records")

    # Optional: Intelligence events
    if intelligence_events:
        count = 0
        for event in intelligence_events:
            event.setdefault("market", market_id)
            db.upsert_intelligence(event)
            count += 1
        print(f"  Bonus: Inserted {count} intelligence events")

    # Optional: Earnings highlights
    if earnings_highlights:
        count = 0
        for op_id, highlights in earnings_highlights.items():
            for hl in highlights:
                db.upsert_earnings_highlight(op_id, "CQ4_2025", hl)
                count += 1
        print(f"  Bonus: Inserted {count} earnings highlights")

    print(f"{market_id} seed complete!")


def seed_all_for_market(market_module, db_path: str = "data/telecom.db"):
    """Convenience wrapper: init DB, call market module's get_seed_data(), seed.

    Each market seed module must define:
        MARKET_ID: str
        OPERATORS: list[str]
        get_seed_data() -> dict with keys matching seed_market() params

    Args:
        market_module: The imported market seed module
        db_path: Path to SQLite database
    Returns:
        TelecomDatabase instance
    """
    db = TelecomDatabase(db_path)
    db.init()

    data = market_module.get_seed_data()
    seed_market(
        db=db,
        market_id=market_module.MARKET_ID,
        operators=market_module.OPERATORS,
        **data,
    )
    return db
