"""BLMCloudSync — bidirectional sync between local SQLite and Supabase.

Usage:
    python3 -m src.database.supabase_sync init
    python3 -m src.database.supabase_sync push --market germany
    python3 -m src.database.supabase_sync pull --market germany
    python3 -m src.database.supabase_sync sync --market germany
    python3 -m src.database.supabase_sync push-outputs --market germany --operator vodafone_germany --period CQ4_2025
    python3 -m src.database.supabase_sync status
"""

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

from src.database.db import TelecomDatabase
from src.database.supabase_client import BLMSupabaseClient
from src.models.market_config import MarketConfig
from src.models.market_configs import get_market_config

# Storage bucket name
BUCKET = "blm-outputs"

# Tables with their conflict columns and market filter column
TABLE_CONFIG = {
    "operators": {
        "conflict": "operator_id",
        "market_col": "market",
    },
    "financial_quarterly": {
        "conflict": "operator_id,calendar_quarter",
        "market_col": "_operator",  # needs join via operator
    },
    "subscriber_quarterly": {
        "conflict": "operator_id,calendar_quarter",
        "market_col": "_operator",
    },
    "network_infrastructure": {
        "conflict": "operator_id,calendar_quarter",
        "market_col": "_operator",
    },
    "tariffs": {
        "conflict": "operator_id,plan_name,plan_type,snapshot_period",
        "market_col": "_operator",
    },
    "competitive_scores": {
        "conflict": "operator_id,calendar_quarter,dimension",
        "market_col": "_operator",
    },
    "intelligence_events": {
        "conflict": None,  # no unique constraint, use id
        "market_col": "market",
    },
    "executives": {
        "conflict": "operator_id,name,title",
        "market_col": "_operator",
    },
    "macro_environment": {
        "conflict": "country,calendar_quarter",
        "market_col": "country",
    },
    "earnings_call_highlights": {
        "conflict": None,  # no unique constraint
        "market_col": "_operator",
    },
    "source_registry": {
        "conflict": "source_id",
        "market_col": None,  # no market filter
    },
    "data_provenance": {
        "conflict": None,
        "market_col": None,
    },
    "operator_groups": {
        "conflict": "group_id",
        "market_col": None,
    },
    "group_subsidiaries": {
        "conflict": "group_id,operator_id",
        "market_col": "market",
    },
}

# MD outputs and their module names
MD_MODULES = {
    "executive_summary": "executive_summary_cq{period_suffix}.md",
    "trends": "trends_deep_analysis_cq{period_suffix}.md",
    "market_customer": "market_customer_deep_analysis_cq{period_suffix}.md",
    "competition": "competition_deep_analysis_cq{period_suffix}.md",
    "self_analysis": "self_analysis_deep_cq{period_suffix}.md",
    "swot": "swot_deep_analysis_cq{period_suffix}.md",
    "opportunities": "opportunities_deep_analysis_cq{period_suffix}.md",
    "tariff": "tariff_deep_analysis_h1_{year_next}.md",
}


@dataclass
class SyncReport:
    """Report of a sync operation."""
    direction: str  # "push" / "pull" / "sync"
    market: str
    tables: dict = field(default_factory=dict)  # table_name → row_count
    files: dict = field(default_factory=dict)   # file_name → size_bytes
    errors: list = field(default_factory=list)
    started_at: str = ""
    finished_at: str = ""

    def summary(self) -> str:
        lines = [f"=== Sync Report ({self.direction}) — {self.market} ==="]
        lines.append(f"  Started:  {self.started_at}")
        lines.append(f"  Finished: {self.finished_at}")
        total_rows = sum(self.tables.values())
        lines.append(f"  Tables: {len(self.tables)}, Total rows: {total_rows}")
        for t, n in sorted(self.tables.items()):
            lines.append(f"    {t}: {n} rows")
        if self.files:
            lines.append(f"  Files: {len(self.files)}")
            for f, s in sorted(self.files.items()):
                size_kb = s / 1024 if s else 0
                lines.append(f"    {f}: {size_kb:.1f} KB")
        if self.errors:
            lines.append(f"  Errors: {len(self.errors)}")
            for e in self.errors:
                lines.append(f"    !! {e}")
        return "\n".join(lines)


class BLMCloudSync:
    """Bidirectional sync between local SQLite and Supabase cloud."""

    def __init__(self, local_db: TelecomDatabase = None,
                 cloud: BLMSupabaseClient = None):
        self.local = local_db or TelecomDatabase()
        self.cloud = cloud or BLMSupabaseClient()
        self._operator_cache: dict[str, list[str]] = {}

    def _ensure_local(self):
        if self.local.conn is None:
            self.local.init()

    def _get_market_operators(self, market: str) -> list[str]:
        """Get operator_ids for a market (cached)."""
        if market not in self._operator_cache:
            self._ensure_local()
            ops = self.local.get_operators_in_market(market)
            self._operator_cache[market] = [o["operator_id"] for o in ops]
        return self._operator_cache[market]

    def _read_local_table(self, table: str) -> list[dict]:
        """Read all rows from a local SQLite table."""
        self._ensure_local()
        rows = self.local.conn.execute(f"SELECT * FROM {table}").fetchall()
        return [dict(r) for r in rows]

    def _filter_by_market(self, rows: list[dict], table: str,
                          market: str) -> list[dict]:
        """Filter rows by market."""
        cfg = TABLE_CONFIG.get(table, {})
        market_col = cfg.get("market_col")
        if not market_col:
            return rows  # no filter possible

        if market_col == "_operator":
            op_ids = self._get_market_operators(market)
            return [r for r in rows if r.get("operator_id") in op_ids]
        elif market_col == "country":
            # Map market_id to country name via operator directory
            country = self._market_to_country(market)
            return [r for r in rows
                    if r.get("country", "").lower() == country.lower()]
        else:
            return [r for r in rows if r.get(market_col) == market]

    @staticmethod
    def _market_to_country(market: str) -> str:
        """Convert market_id to country display name via operator directory.

        Handles multi-word countries like 'el_salvador' → 'El Salvador'.
        """
        from src.database.operator_directory import OPERATOR_DIRECTORY
        for info in OPERATOR_DIRECTORY.values():
            if info.get("market") == market:
                return info["country"]
        # Fallback: title case with underscore → space
        return market.replace("_", " ").title()

    def _clean_row_for_push(self, row: dict, table: str) -> dict:
        """Clean a row dict for Supabase upsert (remove auto-id, convert types)."""
        cleaned = {}
        for k, v in row.items():
            # Skip SQLite auto-increment ids for tables with BIGSERIAL
            if k == "id" and table != "operators" and table != "source_registry":
                continue
            # Convert SQLite boolean ints to Python bools
            if k in ("is_active", "is_current", "includes_5g"):
                cleaned[k] = bool(v) if v is not None else None
            # Parse JSON strings from SQLite into dicts for JSONB columns
            elif k in ("technology_mix", "quality_scores") and isinstance(v, str):
                try:
                    cleaned[k] = json.loads(v)
                except (json.JSONDecodeError, TypeError):
                    cleaned[k] = v
            # Fix partial dates (YYYY-MM → YYYY-MM-01) for Postgres DATE columns
            elif k in ("start_date", "end_date", "effective_date") and isinstance(v, str):
                import re
                if re.match(r'^\d{4}-\d{2}$', v):
                    cleaned[k] = v + "-01"
                else:
                    cleaned[k] = v
            else:
                cleaned[k] = v
        return cleaned

    # =========================================================================
    # Push (local → cloud)
    # =========================================================================

    def push_table(self, table: str, market: str = None) -> int:
        """Push a single table from local SQLite to Supabase.

        Returns number of rows pushed.
        """
        rows = self._read_local_table(table)
        if market:
            rows = self._filter_by_market(rows, table, market)
        if not rows:
            return 0

        cleaned = [self._clean_row_for_push(r, table) for r in rows]
        cfg = TABLE_CONFIG.get(table, {})
        conflict = cfg.get("conflict")

        if conflict:
            return self.cloud.upsert(table, cleaned, on_conflict=conflict)
        else:
            # No conflict key — insert one by one, skip duplicates
            count = 0
            for row in cleaned:
                try:
                    self.cloud.client.table(table).insert(row).execute()
                    count += 1
                except Exception:
                    # Likely duplicate, skip
                    count += 1
            return count

    def push_market_config(self, market_id: str) -> None:
        """Push a MarketConfig to the cloud market_configs table."""
        config = get_market_config(market_id)
        row = {
            "market_id": config.market_id,
            "market_name": config.market_name,
            "country": config.country,
            "currency": config.currency,
            "currency_symbol": config.currency_symbol,
            "regulatory_body": config.regulatory_body,
            "population_k": config.population_k,
            "customer_segments": config.customer_segments,
            "operator_bmc_enrichments": config.operator_bmc_enrichments,
            "operator_exposures": config.operator_exposures,
            "pest_context": config.pest_context,
            "competitive_landscape_notes": config.competitive_landscape_notes,
            "updated_at": datetime.utcnow().isoformat(),
        }
        self.cloud.upsert("market_configs", [row], on_conflict="market_id")

    def push_all(self, market: str) -> SyncReport:
        """Push all tables for a market from local → cloud."""
        report = SyncReport(direction="push", market=market,
                            started_at=datetime.utcnow().isoformat())

        # Push operators first (foreign key dependency)
        ordered_tables = ["operators"] + [
            t for t in TABLE_CONFIG if t != "operators"
        ]

        for table in ordered_tables:
            try:
                n = self.push_table(table, market)
                report.tables[table] = n
                print(f"  ✓ {table}: {n} rows pushed")
            except Exception as e:
                report.errors.append(f"{table}: {e}")
                print(f"  ✗ {table}: {e}")

        # Push market config
        try:
            self.push_market_config(market)
            report.tables["market_configs"] = 1
            print(f"  ✓ market_configs: 1 row pushed")
        except Exception as e:
            report.errors.append(f"market_configs: {e}")
            print(f"  ✗ market_configs: {e}")

        report.finished_at = datetime.utcnow().isoformat()
        return report

    # =========================================================================
    # Push outputs (MD / PDF / PPT → cloud)
    # =========================================================================

    def push_outputs(self, market: str, operator: str,
                     period: str) -> SyncReport:
        """Push analysis output files to cloud.

        MD content → analysis_outputs.content_text
        PDF/PPT → Supabase Storage bucket + analysis_outputs.storage_path
        """
        report = SyncReport(direction="push-outputs", market=market,
                            started_at=datetime.utcnow().isoformat())
        output_dir = Path("data/output")

        # Ensure storage bucket exists
        try:
            self.cloud.ensure_bucket(BUCKET)
        except Exception as e:
            report.errors.append(f"bucket creation: {e}")

        # Parse period for file name matching
        # "CQ4_2025" → suffix "4_2025", year_next "2026"
        parts = period.replace("CQ", "").split("_")
        q_num, year = parts[0], parts[1]
        period_suffix = f"{q_num}_{year}"
        year_next = str(int(year) + 1)

        storage_prefix = f"{market}/{operator}/{period}"

        # 1. Push module MDs
        for module, pattern in MD_MODULES.items():
            fname = pattern.format(period_suffix=period_suffix,
                                   year_next=year_next)
            fpath = output_dir / fname
            if not fpath.exists():
                continue
            try:
                content = fpath.read_text(encoding="utf-8")
                row = {
                    "market_id": market,
                    "operator_id": operator,
                    "analysis_period": period,
                    "output_type": "module_md",
                    "module_name": module,
                    "file_name": fname,
                    "content_text": content,
                    "file_size_bytes": fpath.stat().st_size,
                    "updated_at": datetime.utcnow().isoformat(),
                }
                self.cloud.upsert("analysis_outputs", [row],
                                  on_conflict="market_id,operator_id,analysis_period,output_type,module_name")
                report.files[fname] = fpath.stat().st_size
                print(f"  ✓ MD: {fname} ({fpath.stat().st_size / 1024:.1f} KB)")
            except Exception as e:
                report.errors.append(f"MD {fname}: {e}")
                print(f"  ✗ MD {fname}: {e}")

        # 2. Push full merged MD
        full_md_name = f"blm_{operator}_full_analysis_{period.lower()}.md"
        full_md_path = output_dir / full_md_name
        if full_md_path.exists():
            try:
                content = full_md_path.read_text(encoding="utf-8")
                row = {
                    "market_id": market,
                    "operator_id": operator,
                    "analysis_period": period,
                    "output_type": "full_md",
                    "module_name": None,
                    "file_name": full_md_name,
                    "content_text": content,
                    "file_size_bytes": full_md_path.stat().st_size,
                    "updated_at": datetime.utcnow().isoformat(),
                }
                self.cloud.upsert("analysis_outputs", [row],
                                  on_conflict="market_id,operator_id,analysis_period,output_type,module_name")
                report.files[full_md_name] = full_md_path.stat().st_size
                print(f"  ✓ Full MD: {full_md_name} ({full_md_path.stat().st_size / 1024:.1f} KB)")
            except Exception as e:
                report.errors.append(f"Full MD: {e}")
                print(f"  ✗ Full MD: {e}")

        # 3. Push PDF to storage
        pdf_name = f"blm_{operator}_full_analysis_{period.lower()}.pdf"
        pdf_path = output_dir / pdf_name
        if pdf_path.exists():
            try:
                storage_path = f"{storage_prefix}/{pdf_name}"
                self.cloud.upload_file(
                    BUCKET, storage_path,
                    pdf_path.read_bytes(),
                    content_type="application/pdf"
                )
                row = {
                    "market_id": market,
                    "operator_id": operator,
                    "analysis_period": period,
                    "output_type": "pdf",
                    "module_name": None,
                    "file_name": pdf_name,
                    "storage_path": storage_path,
                    "file_size_bytes": pdf_path.stat().st_size,
                    "updated_at": datetime.utcnow().isoformat(),
                }
                self.cloud.upsert("analysis_outputs", [row],
                                  on_conflict="market_id,operator_id,analysis_period,output_type,module_name")
                report.files[pdf_name] = pdf_path.stat().st_size
                print(f"  ✓ PDF: {pdf_name} ({pdf_path.stat().st_size / 1024:.1f} KB)")
            except Exception as e:
                report.errors.append(f"PDF: {e}")
                print(f"  ✗ PDF: {e}")

        # 4. Push PPT to storage
        pptx_name = f"blm_{operator}_deep_analysis.pptx"
        pptx_path = output_dir / pptx_name
        if pptx_path.exists():
            try:
                storage_path = f"{storage_prefix}/{pptx_name}"
                self.cloud.upload_file(
                    BUCKET, storage_path,
                    pptx_path.read_bytes(),
                    content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
                row = {
                    "market_id": market,
                    "operator_id": operator,
                    "analysis_period": period,
                    "output_type": "pptx",
                    "module_name": None,
                    "file_name": pptx_name,
                    "storage_path": storage_path,
                    "file_size_bytes": pptx_path.stat().st_size,
                    "updated_at": datetime.utcnow().isoformat(),
                }
                self.cloud.upsert("analysis_outputs", [row],
                                  on_conflict="market_id,operator_id,analysis_period,output_type,module_name")
                report.files[pptx_name] = pptx_path.stat().st_size
                print(f"  ✓ PPT: {pptx_name} ({pptx_path.stat().st_size / 1024:.1f} KB)")
            except Exception as e:
                report.errors.append(f"PPT: {e}")
                print(f"  ✗ PPT: {e}")

        report.finished_at = datetime.utcnow().isoformat()
        return report

    # =========================================================================
    # Pull (cloud → local)
    # =========================================================================

    def pull_table(self, table: str, market: str = None) -> int:
        """Pull a table from cloud to local SQLite.

        Returns number of rows pulled.
        """
        self._ensure_local()
        cfg = TABLE_CONFIG.get(table, {})
        market_col = cfg.get("market_col")

        # Build filters
        filters = {}
        if market and market_col and market_col != "_operator":
            if market_col == "country":
                filters["country"] = self._market_to_country(market)
            else:
                filters[market_col] = market

        rows = self.cloud.select(table, filters if filters else None)

        # If market filter is by operator, filter in memory
        if market and market_col == "_operator":
            # First get operators for this market from cloud
            market_ops = self.cloud.select("operators", {"market": market})
            op_ids = {o["operator_id"] for o in market_ops}
            rows = [r for r in rows if r.get("operator_id") in op_ids]

        if not rows:
            return 0

        # Get column names from local schema
        cursor = self.local.conn.execute(f"PRAGMA table_info({table})")
        local_cols = {row[1] for row in cursor.fetchall()}

        count = 0
        for row in rows:
            # Filter to only columns that exist locally
            filtered = {k: v for k, v in row.items() if k in local_cols}

            # Convert JSONB back to JSON strings for SQLite
            for json_col in ("technology_mix", "quality_scores"):
                if json_col in filtered and isinstance(filtered[json_col], (dict, list)):
                    filtered[json_col] = json.dumps(filtered[json_col])

            # Convert bools back to ints for SQLite
            for bool_col in ("is_active", "is_current", "includes_5g"):
                if bool_col in filtered and isinstance(filtered[bool_col], bool):
                    filtered[bool_col] = 1 if filtered[bool_col] else 0

            # Skip the id column for tables with auto-increment
            if "id" in filtered and table not in ("operators", "source_registry"):
                del filtered["id"]

            columns = ", ".join(filtered.keys())
            placeholders = ", ".join(["?"] * len(filtered))

            conflict = cfg.get("conflict")
            if conflict:
                updates = ", ".join(
                    f"{k} = excluded.{k}" for k in filtered.keys()
                    if k not in conflict.split(",")
                )
                sql = f"""
                    INSERT INTO {table} ({columns})
                    VALUES ({placeholders})
                    ON CONFLICT({conflict}) DO UPDATE SET {updates}
                """
            else:
                sql = f"INSERT OR IGNORE INTO {table} ({columns}) VALUES ({placeholders})"

            self.local.conn.execute(sql, list(filtered.values()))
            count += 1

        self.local.conn.commit()
        return count

    def pull_market_config(self, market_id: str) -> MarketConfig:
        """Pull a MarketConfig from cloud and return it."""
        rows = self.cloud.select("market_configs", {"market_id": market_id})
        if not rows:
            raise ValueError(f"No market_config found for '{market_id}' in cloud")
        r = rows[0]
        return MarketConfig(
            market_id=r["market_id"],
            market_name=r["market_name"],
            country=r["country"],
            currency=r["currency"],
            currency_symbol=r.get("currency_symbol", "€"),
            regulatory_body=r.get("regulatory_body", ""),
            population_k=r.get("population_k", 0),
            customer_segments=r.get("customer_segments", []),
            operator_bmc_enrichments=r.get("operator_bmc_enrichments", {}),
            operator_exposures=r.get("operator_exposures", {}),
            pest_context=r.get("pest_context", {}),
            competitive_landscape_notes=r.get("competitive_landscape_notes", []),
        )

    def pull_all(self, market: str) -> SyncReport:
        """Pull all tables for a market from cloud → local."""
        report = SyncReport(direction="pull", market=market,
                            started_at=datetime.utcnow().isoformat())

        # Pull operators first
        ordered_tables = ["operators"] + [
            t for t in TABLE_CONFIG if t != "operators"
        ]

        for table in ordered_tables:
            try:
                n = self.pull_table(table, market)
                report.tables[table] = n
                print(f"  ✓ {table}: {n} rows pulled")
            except Exception as e:
                report.errors.append(f"{table}: {e}")
                print(f"  ✗ {table}: {e}")

        report.finished_at = datetime.utcnow().isoformat()
        return report

    # =========================================================================
    # Smart sync (bidirectional based on timestamps)
    # =========================================================================

    def sync(self, market: str) -> SyncReport:
        """Smart sync: push local changes, then pull cloud changes.

        Uses a simple strategy: push first (local wins for conflicts),
        then pull anything new from cloud.
        """
        report = SyncReport(direction="sync", market=market,
                            started_at=datetime.utcnow().isoformat())

        print("Phase 1: Push local → cloud")
        push_report = self.push_all(market)
        for t, n in push_report.tables.items():
            report.tables[f"push:{t}"] = n
        report.errors.extend(push_report.errors)

        print("\nPhase 2: Pull cloud → local")
        pull_report = self.pull_all(market)
        for t, n in pull_report.tables.items():
            report.tables[f"pull:{t}"] = n
        report.errors.extend(pull_report.errors)

        report.finished_at = datetime.utcnow().isoformat()
        return report

    # =========================================================================
    # Status
    # =========================================================================

    def status(self) -> str:
        """Show cloud status: row counts per table."""
        lines = ["=== Supabase Cloud Status ==="]
        all_tables = list(TABLE_CONFIG.keys()) + ["market_configs", "analysis_outputs"]
        total = 0
        for table in all_tables:
            try:
                n = self.cloud.count(table)
                lines.append(f"  {table}: {n} rows")
                total += n
            except Exception as e:
                lines.append(f"  {table}: ERROR ({e})")
        lines.append(f"  ---")
        lines.append(f"  Total: {total} rows")

        # Check storage bucket
        try:
            bucket = self.cloud.client.storage.get_bucket(BUCKET)
            lines.append(f"\n  Storage bucket '{BUCKET}': exists")
        except Exception:
            lines.append(f"\n  Storage bucket '{BUCKET}': not found")

        return "\n".join(lines)


# =============================================================================
# Schema initialization
# =============================================================================

def init_schema(cloud: BLMSupabaseClient):
    """Initialize Supabase tables by executing schema SQL.

    Since Supabase doesn't allow arbitrary SQL via the client library,
    this prints the SQL for manual execution in the Supabase SQL Editor,
    or uses postgrest-compatible table creation.
    """
    schema_path = Path(__file__).parent / "supabase_schema.sql"
    sql = schema_path.read_text(encoding="utf-8")

    print("=" * 60)
    print("SUPABASE SCHEMA INITIALIZATION")
    print("=" * 60)
    print()
    print("The Supabase Python client cannot execute DDL directly.")
    print("Please run the following SQL in the Supabase SQL Editor")
    print("(Dashboard → SQL Editor → New Query):")
    print()
    print("-" * 60)
    print(sql)
    print("-" * 60)
    print()

    # Also try to create the storage bucket
    try:
        cloud.ensure_bucket(BUCKET)
        print(f"✓ Storage bucket '{BUCKET}' created/verified")
    except Exception as e:
        print(f"✗ Storage bucket creation failed: {e}")
        print(f"  Create it manually: Dashboard → Storage → New Bucket → '{BUCKET}'")

    print()
    print("After running the SQL, verify with:")
    print("  python3 -m src.database.supabase_sync status")


# =============================================================================
# CLI entry point
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="BLM Cloud Sync — SQLite ↔ Supabase"
    )
    sub = parser.add_subparsers(dest="command", help="Command")

    # init
    sub.add_parser("init", help="Initialize Supabase schema (prints SQL)")

    # push
    p_push = sub.add_parser("push", help="Push local data → cloud")
    p_push.add_argument("--market", required=True, help="Market ID (e.g., germany)")

    # pull
    p_pull = sub.add_parser("pull", help="Pull cloud data → local")
    p_pull.add_argument("--market", required=True, help="Market ID")

    # sync
    p_sync = sub.add_parser("sync", help="Smart bidirectional sync")
    p_sync.add_argument("--market", required=True, help="Market ID")

    # push-outputs
    p_out = sub.add_parser("push-outputs", help="Push analysis output files → cloud")
    p_out.add_argument("--market", required=True, help="Market ID")
    p_out.add_argument("--operator", required=True, help="Operator ID")
    p_out.add_argument("--period", required=True, help="Analysis period (e.g., CQ4_2025)")

    # status
    sub.add_parser("status", help="Show cloud status")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "init":
        cloud = BLMSupabaseClient()
        init_schema(cloud)
        return

    if args.command == "status":
        syncer = BLMCloudSync()
        print(syncer.status())
        return

    # Commands that need both local and cloud
    db = TelecomDatabase()
    db.init()
    syncer = BLMCloudSync(local_db=db, cloud=BLMSupabaseClient())

    try:
        if args.command == "push":
            print(f"Pushing {args.market} data to cloud...")
            report = syncer.push_all(args.market)
            print()
            print(report.summary())

        elif args.command == "pull":
            print(f"Pulling {args.market} data from cloud...")
            report = syncer.pull_all(args.market)
            print()
            print(report.summary())

        elif args.command == "sync":
            print(f"Syncing {args.market}...")
            report = syncer.sync(args.market)
            print()
            print(report.summary())

        elif args.command == "push-outputs":
            print(f"Pushing outputs for {args.operator} ({args.period})...")
            report = syncer.push_outputs(args.market, args.operator, args.period)
            print()
            print(report.summary())

    finally:
        db.close()


if __name__ == "__main__":
    main()
