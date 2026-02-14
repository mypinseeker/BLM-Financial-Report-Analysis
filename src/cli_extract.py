"""CLI for batch data extraction from consolidated earnings PDFs.

Usage:
    # Extract all 11 Tigo operators from Millicom consolidated PDF
    python3 -m src.cli_extract millicom --pdf-url URL --period CQ4_2025

    # Extract one operator (PDF or search fallback)
    python3 -m src.cli_extract single --operator tigo_guatemala --period CQ4_2025

    # Review extracted JSON before committing
    python3 -m src.cli_extract review --operator tigo_guatemala
    python3 -m src.cli_extract review --all

    # Commit reviewed JSON to SQLite
    python3 -m src.cli_extract commit --operator tigo_guatemala
    python3 -m src.cli_extract commit --all

    # Show extraction progress
    python3 -m src.cli_extract status
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

from src.database.operator_directory import (
    OPERATOR_DIRECTORY,
    get_non_group_operators,
    get_operators_for_group,
)

EXTRACTION_DIR = Path("data/extraction")

# Table types extractable from a consolidated PDF
PDF_TABLE_TYPES = ["financial", "subscriber", "network"]

# Table types that use search (no PDF needed)
SEARCH_TABLE_TYPES = ["macro"]


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _save_json(path: Path, data: list[dict], source_url: str = "") -> None:
    """Write extraction results as JSON with provenance metadata."""
    now = datetime.utcnow().isoformat() + "Z"
    for row in data:
        row["_extraction_method"] = "gemini_pdf" if source_url else "gemini_search"
        row["_source_url"] = source_url
        row["_extracted_at"] = now
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def _parse_filename(stem: str) -> tuple[str, str]:
    """Parse extraction filename stem into (entity_id, table_type).

    Examples:
        'tigo_guatemala_financial' -> ('tigo_guatemala', 'financial')
        'el_salvador_macro'        -> ('el_salvador', 'macro')
        'claro_gt_financial'       -> ('claro_gt', 'financial')
    """
    all_types = PDF_TABLE_TYPES + SEARCH_TABLE_TYPES + ["tariff"]
    for ttype in all_types:
        suffix = f"_{ttype}"
        if stem.endswith(suffix):
            entity = stem[: -len(suffix)]
            return entity, ttype
    raise ValueError(f"Cannot parse table type from filename: {stem}")


def _strip_provenance(rows: list[dict]) -> list[dict]:
    """Remove _-prefixed metadata fields before DB write."""
    return [
        {k: v for k, v in row.items() if not k.startswith("_")}
        for row in rows
    ]


def _ensure_operators(db) -> int:
    """Register all Latin America operators in the database. Returns count."""
    count = 0
    for op_id, info in OPERATOR_DIRECTORY.items():
        if info.get("region") == "Latin America":
            db.upsert_operator(op_id, **info)
            count += 1
    return count


def _upsert_rows(db, entity_id: str, table_type: str, rows: list[dict]) -> int:
    """Dispatch rows to the correct db.upsert_*() method. Returns count."""
    count = 0
    for row in rows:
        if table_type == "financial":
            period = row.get("period") or row.get("calendar_quarter", "")
            db.upsert_financial(entity_id, period, row)
        elif table_type == "subscriber":
            period = row.get("period") or row.get("calendar_quarter", "")
            db.upsert_subscriber(entity_id, period, row)
        elif table_type == "network":
            cq = row.get("calendar_quarter", "")
            db.upsert_network(entity_id, cq, row)
        elif table_type == "macro":
            country = row.get("country", entity_id)
            cq = row.get("calendar_quarter", "")
            db.upsert_macro(country, cq, row)
        elif table_type == "tariff":
            plan_name = row.get("plan_name", "")
            plan_type = row.get("plan_type", "")
            snapshot = row.get("snapshot_period", "")
            db.upsert_tariff(entity_id, plan_name, plan_type, snapshot, row)
        else:
            raise ValueError(f"Unknown table type: {table_type}")
        count += 1
    return count


def _get_extraction_service():
    """Create ExtractionService with Gemini configured from env."""
    import os
    from src.web.services.gemini_service import GeminiService
    from src.web.services.extraction_service import ExtractionService

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable not set")
        sys.exit(1)
    gemini = GeminiService(api_key=api_key)
    return ExtractionService(gemini=gemini)


def _get_db(db_path: str = "data/telecom.db"):
    """Create and init TelecomDatabase."""
    from src.database.db import TelecomDatabase
    db = TelecomDatabase(db_path)
    db.init()
    return db


# ------------------------------------------------------------------
# Subcommands
# ------------------------------------------------------------------

async def _extract_operator(
    ext, operator_id: str, period: str, file_uri: str = "",
    force: bool = False, source_url: str = "",
) -> dict[str, int]:
    """Extract all table types for one operator. Returns {type: row_count}."""
    op_info = OPERATOR_DIRECTORY.get(operator_id)
    if not op_info:
        print(f"  WARNING: Unknown operator {operator_id}, skipping")
        return {}

    results = {}
    table_types = PDF_TABLE_TYPES if file_uri else PDF_TABLE_TYPES + SEARCH_TABLE_TYPES

    for ttype in table_types:
        out_path = EXTRACTION_DIR / f"{operator_id}_{ttype}.json"
        if out_path.exists() and not force:
            existing = json.loads(out_path.read_text())
            print(f"  {operator_id}/{ttype}: {len(existing)} rows (cached)")
            results[ttype] = len(existing)
            continue

        print(f"  {operator_id}/{ttype}: extracting...", end="", flush=True)
        try:
            rows = await ext.extract_table(
                file_uri or "search", ttype, operator_id, period
            )
            _save_json(out_path, rows, source_url=source_url if file_uri else "")
            print(f" {len(rows)} rows")
            results[ttype] = len(rows)
        except Exception as e:
            print(f" ERROR: {e}")
            results[ttype] = 0

        await asyncio.sleep(1.0 if file_uri else 1.5)

    return results


async def _extract_macro(ext, country: str, period: str, force: bool = False) -> int:
    """Extract macro data for a country via search."""
    # Use country name (lowered, spaces→underscores) as filename entity
    entity = country.lower().replace(" ", "_")
    out_path = EXTRACTION_DIR / f"{entity}_macro.json"
    if out_path.exists() and not force:
        existing = json.loads(out_path.read_text())
        print(f"  {country}/macro: {len(existing)} rows (cached)")
        return len(existing)

    # Find any operator in this country to get correct op_info for the prompt
    op_id = next(
        (oid for oid, info in OPERATOR_DIRECTORY.items() if info["country"] == country),
        None,
    )
    if not op_id:
        print(f"  WARNING: No operator found for country {country}")
        return 0

    print(f"  {country}/macro: extracting...", end="", flush=True)
    try:
        rows = await ext.extract_table("search", "macro", op_id, period)
        _save_json(out_path, rows)
        print(f" {len(rows)} rows")
        return len(rows)
    except Exception as e:
        print(f" ERROR: {e}")
        return 0


def cmd_millicom(args):
    """Extract all 11 Tigo operators from a Millicom consolidated PDF."""
    ext = _get_extraction_service()
    pdf_url = args.pdf_url
    period = args.period
    force = args.force

    operators = get_operators_for_group("millicom")
    print(f"Millicom batch extraction: {len(operators)} operators, period={period}")

    async def run():
        # Step 1: Upload PDF
        print(f"\nUploading PDF: {pdf_url}")
        file_uri = await ext.download_and_upload(pdf_url, "millicom_earnings")
        print(f"  file_uri: {file_uri}")

        # Step 2: Extract each Tigo operator from the PDF
        total = {}
        for op_id in operators:
            print(f"\n--- {op_id} ---")
            result = await _extract_operator(
                ext, op_id, period, file_uri=file_uri,
                force=force, source_url=pdf_url,
            )
            total[op_id] = result

        # Step 3: Extract macro data for each unique country (via search)
        countries = sorted(set(
            OPERATOR_DIRECTORY[op_id]["country"]
            for op_id in operators
            if op_id in OPERATOR_DIRECTORY
        ))
        print(f"\n--- Macro data for {len(countries)} countries ---")
        for country in countries:
            await _extract_macro(ext, country, period, force=force)
            await asyncio.sleep(1.5)

        # Step 4: Optionally extract competitors
        if args.include_competitors:
            print("\n--- Competitor extraction ---")
            markets = sorted(set(
                OPERATOR_DIRECTORY[op_id]["market"]
                for op_id in operators
                if op_id in OPERATOR_DIRECTORY
            ))
            for market in markets:
                comp_ids = get_non_group_operators(market, "millicom")
                for comp_id in comp_ids:
                    print(f"\n--- {comp_id} (competitor) ---")
                    await _extract_operator(
                        ext, comp_id, period, file_uri="search",
                        force=force,
                    )

        # Summary
        print("\n=== Summary ===")
        total_rows = 0
        for op_id, types in total.items():
            rows = sum(types.values())
            total_rows += rows
            print(f"  {op_id}: {rows} rows")
        print(f"  TOTAL: {total_rows} rows")

        if args.approve:
            print("\n--- Auto-committing to SQLite ---")
            _do_commit(operator=None, all_ops=True, db_path=args.db)

    asyncio.run(run())


def cmd_single(args):
    """Extract data for a single operator."""
    ext = _get_extraction_service()
    operator_id = args.operator
    period = args.period

    if operator_id not in OPERATOR_DIRECTORY:
        print(f"ERROR: Unknown operator: {operator_id}")
        sys.exit(1)

    async def run():
        file_uri = ""
        source_url = ""
        if args.pdf_url:
            print(f"Uploading PDF: {args.pdf_url}")
            file_uri = await ext.download_and_upload(args.pdf_url, "earnings_report")
            source_url = args.pdf_url
            print(f"  file_uri: {file_uri}")

        print(f"\n--- {operator_id} ---")
        result = await _extract_operator(
            ext, operator_id, period, file_uri=file_uri,
            force=args.force, source_url=source_url,
        )

        # Also extract macro for the operator's country
        country = OPERATOR_DIRECTORY[operator_id]["country"]
        print(f"\n--- {country} macro ---")
        await _extract_macro(ext, country, period, force=args.force)

        total = sum(result.values())
        print(f"\nDone: {total} rows extracted for {operator_id}")

    asyncio.run(run())


def cmd_review(args):
    """Print extracted JSON for review."""
    if not EXTRACTION_DIR.exists():
        print("No extraction data found. Run 'millicom' or 'single' first.")
        return

    files = sorted(EXTRACTION_DIR.glob("*.json"))
    if not files:
        print("No extraction JSON files found.")
        return

    # Filter by operator if specified
    if args.operator:
        files = [f for f in files if f.stem.startswith(args.operator)]
        if not files:
            print(f"No extraction files found for operator: {args.operator}")
            return

    for f in files:
        entity, ttype = _parse_filename(f.stem)
        data = json.loads(f.read_text())
        print(f"\n{'='*60}")
        print(f"  {entity} / {ttype} — {len(data)} rows")
        print(f"  File: {f}")
        print(f"{'='*60}")
        for i, row in enumerate(data):
            # Show key fields only
            clean = {k: v for k, v in row.items() if not k.startswith("_") and v is not None}
            print(f"  [{i}] {json.dumps(clean, indent=4, ensure_ascii=False)}")


def _do_commit(operator: str | None, all_ops: bool, db_path: str = "data/telecom.db"):
    """Shared commit logic for cmd_commit and auto-approve."""
    if not EXTRACTION_DIR.exists():
        print("No extraction data found.")
        return

    files = sorted(EXTRACTION_DIR.glob("*.json"))
    if not files:
        print("No extraction JSON files found.")
        return

    if operator:
        files = [f for f in files if f.stem.startswith(operator)]
    elif not all_ops:
        print("ERROR: Specify --operator or --all")
        sys.exit(1)

    db = _get_db(db_path)
    reg_count = _ensure_operators(db)
    print(f"Registered {reg_count} LATAM operators")

    total = 0
    for f in files:
        entity, ttype = _parse_filename(f.stem)
        data = json.loads(f.read_text())
        clean_rows = _strip_provenance(data)

        try:
            count = _upsert_rows(db, entity, ttype, clean_rows)
            print(f"  {f.stem}: {count} rows committed")
            total += count
        except Exception as e:
            print(f"  {f.stem}: ERROR — {e}")

    db.close()
    print(f"\nTotal: {total} rows committed to {db_path}")


def cmd_commit(args):
    """Write reviewed JSON to SQLite."""
    _do_commit(args.operator, args.all, db_path=args.db)


def cmd_status(args):
    """Show extraction progress."""
    if not EXTRACTION_DIR.exists():
        print("No extraction data directory found.")
        return

    files = sorted(EXTRACTION_DIR.glob("*.json"))
    if not files:
        print("No extraction files found.")
        return

    # Group by entity
    entities: dict[str, dict] = {}
    for f in files:
        entity, ttype = _parse_filename(f.stem)
        data = json.loads(f.read_text())
        if entity not in entities:
            entities[entity] = {}
        entities[entity][ttype] = {
            "rows": len(data),
            "extracted_at": data[0].get("_extracted_at", "?") if data else "?",
        }

    print(f"Extraction status: {len(files)} files, {len(entities)} entities\n")
    for entity in sorted(entities.keys()):
        types = entities[entity]
        parts = []
        for ttype, info in sorted(types.items()):
            parts.append(f"{ttype}={info['rows']}")
        print(f"  {entity}: {', '.join(parts)}")

    # Show which Tigo operators are missing
    tigo_ops = get_operators_for_group("millicom")
    missing = [op for op in tigo_ops if op not in entities]
    if missing:
        print(f"\nMissing Tigo operators: {', '.join(missing)}")


# ------------------------------------------------------------------
# Argument parser
# ------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="cli_extract",
        description="Batch data extraction from consolidated earnings PDFs",
    )
    parser.add_argument(
        "--db", default="data/telecom.db",
        help="Path to SQLite database (default: data/telecom.db)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # millicom
    p_mill = sub.add_parser("millicom", help="Extract all Tigo ops from Millicom PDF")
    p_mill.add_argument("--pdf-url", required=True, help="URL of Millicom consolidated PDF")
    p_mill.add_argument("--period", default="CQ4_2025", help="Target quarter")
    p_mill.add_argument("--force", action="store_true", help="Re-extract even if cached")
    p_mill.add_argument("--approve", action="store_true", help="Auto-commit after extraction")
    p_mill.add_argument("--include-competitors", action="store_true", help="Also extract competitors via search")
    p_mill.set_defaults(func=cmd_millicom)

    # single
    p_single = sub.add_parser("single", help="Extract one operator")
    p_single.add_argument("--operator", required=True, help="Operator ID")
    p_single.add_argument("--pdf-url", default="", help="PDF URL (omit for search mode)")
    p_single.add_argument("--period", default="CQ4_2025", help="Target quarter")
    p_single.add_argument("--force", action="store_true", help="Re-extract even if cached")
    p_single.set_defaults(func=cmd_single)

    # review
    p_review = sub.add_parser("review", help="Review extracted JSON")
    p_review.add_argument("--operator", default="", help="Filter by operator ID")
    p_review.add_argument("--all", action="store_true", help="Show all")
    p_review.set_defaults(func=cmd_review)

    # commit
    p_commit = sub.add_parser("commit", help="Commit JSON to SQLite")
    p_commit.add_argument("--operator", default="", help="Commit one operator")
    p_commit.add_argument("--all", action="store_true", help="Commit all")
    p_commit.set_defaults(func=cmd_commit)

    # status
    p_status = sub.add_parser("status", help="Show extraction progress")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
