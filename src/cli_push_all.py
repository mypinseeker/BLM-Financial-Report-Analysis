"""CLI to seed all 12 markets locally and push to Supabase.

Seeds into a temp SQLite DB via seed_orchestrator, then pushes each market
to Supabase using BLMCloudSync.

Usage:
    python3 -m src.cli_push_all                     # seed + push all 12 markets
    python3 -m src.cli_push_all --markets guatemala  # push single market
    python3 -m src.cli_push_all --dry-run            # seed only, verify counts
    python3 -m src.cli_push_all --status             # check Supabase row counts
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))


def main():
    parser = argparse.ArgumentParser(
        description="BLM Supabase Push — Seed locally and push to cloud"
    )
    parser.add_argument(
        "--markets", default="",
        help="Comma-separated market IDs (default: all 12)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Seed locally only, print counts without pushing to Supabase",
    )
    parser.add_argument(
        "--status", action="store_true",
        help="Show current Supabase row counts and exit",
    )
    args = parser.parse_args()

    # Status mode: just show Supabase counts
    if args.status:
        return cmd_status()

    from src.database.seed_orchestrator import seed_all_markets, ALL_MARKETS

    # Determine markets
    if args.markets:
        markets = [m.strip() for m in args.markets.split(",")]
        invalid = [m for m in markets if m not in ALL_MARKETS]
        if invalid:
            print(f"ERROR: Unknown markets: {invalid}")
            print(f"Valid: {ALL_MARKETS}")
            return 1
    else:
        markets = ALL_MARKETS

    print("=" * 60)
    print("  BLM Supabase Push")
    print(f"  Markets: {len(markets)}")
    print(f"  Mode:    {'DRY RUN (no push)' if args.dry_run else 'PUSH TO SUPABASE'}")
    print("=" * 60)

    # 1. Seed all markets into temp SQLite
    print("\nPhase 1: Seeding all markets into local SQLite...")
    tmp_dir = tempfile.mkdtemp(prefix="blm_push_")
    db_path = str(Path(tmp_dir) / "push_all.db")
    db = seed_all_markets(db_path)

    # 2. Print local counts
    print("\nLocal database counts:")
    local_counts = _print_local_counts(db)

    if args.dry_run:
        print("\n[DRY RUN] No data pushed to Supabase.")
        db.close()
        return 0

    # 3. Push to Supabase
    print("\nPhase 2: Pushing to Supabase...")
    from src.database.supabase_sync import BLMCloudSync

    syncer = BLMCloudSync(local_db=db)
    total_rows = 0
    total_errors = 0

    for market in markets:
        print(f"\n--- Pushing {market} ---")
        report = syncer.push_all(market)
        rows = sum(report.tables.values())
        total_rows += rows
        total_errors += len(report.errors)
        if report.errors:
            print(f"  Errors: {report.errors}")

    # 4. Push group-level tables (operator_groups, group_subsidiaries)
    print("\n--- Pushing group tables ---")
    for table in ("operator_groups", "group_subsidiaries"):
        try:
            n = syncer.push_table(table)
            print(f"  {table}: {n} rows pushed")
            total_rows += n
        except Exception as e:
            print(f"  {table}: ERROR — {e}")
            total_errors += 1

    # 5. Summary
    print(f"\n{'='*60}")
    print(f"  Push Complete")
    print(f"  Total rows pushed: {total_rows}")
    print(f"  Errors: {total_errors}")
    print(f"{'='*60}")

    db.close()

    # 6. Show Supabase status
    print("\nVerifying Supabase counts...")
    cmd_status()

    return 0 if total_errors == 0 else 1


def cmd_status() -> int:
    """Show current Supabase row counts."""
    try:
        from src.database.supabase_sync import BLMCloudSync
        syncer = BLMCloudSync()
        print(syncer.status())
        return 0
    except Exception as e:
        print(f"ERROR: Cannot connect to Supabase — {e}")
        print("Set SUPABASE_URL and SUPABASE_SERVICE_KEY in src/database/.env")
        return 1


def _print_local_counts(db) -> dict:
    """Print row counts for all tables in local SQLite DB."""
    counts = {}
    tables = [
        "operators", "financial_quarterly", "subscriber_quarterly",
        "competitive_scores", "macro_environment", "network_infrastructure",
        "executives", "intelligence_events", "earnings_call_highlights",
        "tariffs", "operator_groups", "group_subsidiaries",
    ]
    for table in tables:
        try:
            n = db.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            counts[table] = n
            print(f"  {table}: {n}")
        except Exception:
            pass

    total = sum(counts.values())
    print(f"  ---")
    print(f"  Total: {total}")
    return counts


if __name__ == "__main__":
    sys.exit(main())
