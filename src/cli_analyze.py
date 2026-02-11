"""CLI entry point for BLM analysis execution.

Usage:
    # Single market
    python3 -m src.cli_analyze single --market germany --operator vodafone_germany --period CQ4_2025

    # Group analysis
    python3 -m src.cli_analyze group --group-id millicom --period CQ4_2025

    # List jobs
    python3 -m src.cli_analyze list

    # Check job status
    python3 -m src.cli_analyze status --job-id 42
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime


def _get_service():
    """Create a SupabaseDataService from environment variables."""
    from src.web.services.supabase_data import SupabaseDataService
    from supabase import create_client

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        # Try loading from src/database/.env
        from dotenv import load_dotenv
        from pathlib import Path
        env_path = Path(__file__).parent / "database" / ".env"
        load_dotenv(env_path)
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")

    if not url or not key:
        print("ERROR: Missing SUPABASE_URL or SUPABASE_SERVICE_KEY")
        print("Set them as env vars or in src/database/.env")
        sys.exit(1)

    client = create_client(url, key)
    return SupabaseDataService(client)


def cmd_single(args):
    """Run a single-market analysis."""
    svc = _get_service()
    from src.web.services.analysis_runner import AnalysisRunnerService

    # Validate operator exists
    op = svc.get_operator(args.operator)
    if not op:
        print(f"ERROR: Operator '{args.operator}' not found in Supabase")
        sys.exit(1)

    print(f"{'=' * 60}")
    print(f"  BLM Single Market Analysis")
    print(f"  Market:   {args.market}")
    print(f"  Operator: {args.operator}")
    print(f"  Period:   {args.period}")
    print(f"  Quarters: {args.n_quarters}")
    print(f"{'=' * 60}")

    # Create analysis job
    job_data = {
        "job_type": "single_market",
        "market": args.market,
        "target_operator": args.operator,
        "analysis_period": args.period,
        "n_quarters": args.n_quarters,
        "status": "pending",
        "progress": json.dumps({args.market: "pending"}),
        "config": json.dumps({}),
    }
    job = svc.create_analysis_job(job_data)
    job_id = job.get("id")
    print(f"\nJob #{job_id} created. Starting execution...\n")

    # Run synchronously
    runner = AnalysisRunnerService(svc)
    result = runner.run_single(job_id)

    print(f"\n{'=' * 60}")
    print(f"  Result: {result['status'].upper()}")
    if result.get("output_count"):
        print(f"  Outputs: {result['output_count']} files generated and uploaded")
    if result.get("error"):
        print(f"  Error: {result['error']}")
    print(f"{'=' * 60}")

    return 0 if result["status"] == "completed" else 1


def cmd_group(args):
    """Run a group analysis across multiple markets."""
    svc = _get_service()
    from src.web.services.analysis_runner import AnalysisRunnerService

    # Validate group exists
    group = svc.get_operator_group(args.group_id)
    if not group:
        print(f"ERROR: Group '{args.group_id}' not found in Supabase")
        sys.exit(1)

    # Get subsidiaries to determine markets
    subs = svc.get_group_subsidiaries(args.group_id)
    all_markets = [s["market"] for s in subs]

    # Filter to selected markets if specified
    if args.markets:
        markets = [m.strip() for m in args.markets.split(",")]
    else:
        markets = all_markets

    print(f"{'=' * 60}")
    print(f"  BLM Group Analysis: {group.get('group_name', args.group_id)}")
    print(f"  Markets: {', '.join(markets)} ({len(markets)} total)")
    print(f"  Period:  {args.period}")
    print(f"{'=' * 60}")

    # Create analysis job
    progress = {m: "pending" for m in markets}
    job_data = {
        "job_type": "group_analysis",
        "group_id": args.group_id,
        "analysis_period": args.period,
        "n_quarters": args.n_quarters,
        "status": "pending",
        "progress": json.dumps(progress),
        "config": json.dumps({"selected_markets": markets}),
    }
    job = svc.create_analysis_job(job_data)
    job_id = job.get("id")
    print(f"\nJob #{job_id} created. Starting execution...\n")

    # Run synchronously
    runner = AnalysisRunnerService(svc)
    result = runner.run_group(job_id)

    print(f"\n{'=' * 60}")
    print(f"  Result: {result['status'].upper()}")
    if result.get("markets"):
        for m, s in result["markets"].items():
            icon = "OK" if s == "completed" else "FAIL"
            print(f"    [{icon}] {m}: {s}")
    if result.get("output_count"):
        print(f"  Total outputs: {result['output_count']} files")
    print(f"{'=' * 60}")

    return 0 if result["status"] == "completed" else 1


def cmd_list(args):
    """List analysis jobs."""
    svc = _get_service()
    jobs = svc.get_analysis_jobs(status=args.status)

    if not jobs:
        print("No analysis jobs found.")
        return 0

    print(f"{'ID':>5}  {'Type':15}  {'Status':10}  {'Market/Group':20}  {'Period':10}  {'Created'}")
    print("-" * 90)
    for j in jobs:
        job_type = j.get("job_type", "")
        status = j.get("status", "")
        market = j.get("market") or j.get("group_id") or ""
        period = j.get("analysis_period", "")
        created = j.get("created_at", "")[:19]
        print(f"{j.get('id', ''):>5}  {job_type:15}  {status:10}  {market:20}  {period:10}  {created}")

    return 0


def cmd_status(args):
    """Check a specific job's status and progress."""
    svc = _get_service()
    job = svc.get_analysis_job(args.job_id)

    if not job:
        print(f"Job #{args.job_id} not found.")
        return 1

    print(f"Job #{job.get('id')}")
    print(f"  Type:     {job.get('job_type')}")
    print(f"  Status:   {job.get('status')}")
    print(f"  Market:   {job.get('market') or job.get('group_id')}")
    print(f"  Operator: {job.get('target_operator', 'N/A')}")
    print(f"  Period:   {job.get('analysis_period')}")
    print(f"  Created:  {job.get('created_at')}")
    print(f"  Started:  {job.get('started_at', 'N/A')}")
    print(f"  Completed:{job.get('completed_at', 'N/A')}")

    # Parse progress
    progress_str = job.get("progress", "{}")
    if isinstance(progress_str, str):
        try:
            progress = json.loads(progress_str)
        except json.JSONDecodeError:
            progress = {}
    else:
        progress = progress_str or {}

    if progress:
        print(f"  Progress:")
        for market, status in progress.items():
            icon = "OK" if status == "completed" else (
                "..." if status.startswith("running") else
                "!!" if status == "failed" else "--"
            )
            print(f"    [{icon}] {market}: {status}")

    if job.get("error_message"):
        print(f"  Error: {job['error_message']}")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="BLM Analysis CLI — Execute analysis jobs"
    )
    sub = parser.add_subparsers(dest="command", help="Command")

    # single
    p_single = sub.add_parser("single", help="Run single-market analysis")
    p_single.add_argument("--market", required=True, help="Market ID (e.g., germany)")
    p_single.add_argument("--operator", required=True, help="Operator ID (e.g., vodafone_germany)")
    p_single.add_argument("--period", default="CQ4_2025", help="Analysis period (default: CQ4_2025)")
    p_single.add_argument("--n-quarters", type=int, default=8, help="Historical range in quarters (default: 8)")

    # group
    p_group = sub.add_parser("group", help="Run group analysis across markets")
    p_group.add_argument("--group-id", required=True, help="Operator group ID (e.g., millicom)")
    p_group.add_argument("--period", default="CQ4_2025", help="Analysis period")
    p_group.add_argument("--n-quarters", type=int, default=8, help="Historical range")
    p_group.add_argument("--markets", default="", help="Comma-separated market IDs (default: all)")

    # list
    p_list = sub.add_parser("list", help="List analysis jobs")
    p_list.add_argument("--status", default=None, help="Filter by status (pending/running/completed/failed)")

    # status
    p_status = sub.add_parser("status", help="Check a job's status")
    p_status.add_argument("--job-id", type=int, required=True, help="Job ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "single": cmd_single,
        "group": cmd_group,
        "list": cmd_list,
        "status": cmd_status,
    }

    exit_code = commands[args.command](args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
