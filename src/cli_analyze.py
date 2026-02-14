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

    # Market readiness audit
    python3 -m src.cli_analyze audit --market chile --reference germany --period CQ4_2025
    python3 -m src.cli_analyze audit --market chile --period CQ4_2025  # absolute thresholds
    python3 -m src.cli_analyze audit --market chile --reference germany --output-json /tmp/audit.json
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


def cmd_audit(args):
    """Run a market readiness audit."""
    from pathlib import Path
    from src.web.services.market_audit import MarketAuditService

    svc = _get_service()

    # Validate target market has operators
    target_ops = svc.get_operators_in_market(args.market)
    if not target_ops:
        print(f"ERROR: No operators found for market '{args.market}'")
        sys.exit(1)

    # Interactive target operator selection
    print(f"\nOperators in {args.market}:")
    for i, op in enumerate(target_ops, 1):
        print(f"  {i}. {op.get('display_name', op['operator_id'])} ({op['operator_id']})")

    if len(target_ops) == 1:
        target_operator = target_ops[0]["operator_id"]
        print(f"  -> Auto-selected: {target_operator}")
    else:
        choice = input(f"Select target operator [1-{len(target_ops)}]: ").strip()
        try:
            idx = int(choice) - 1
            if idx < 0 or idx >= len(target_ops):
                raise ValueError()
            target_operator = target_ops[idx]["operator_id"]
        except (ValueError, IndexError):
            print("ERROR: Invalid selection")
            sys.exit(1)

    # Reference market operator selection (if provided)
    ref_operator = ""
    if args.reference:
        ref_ops = svc.get_operators_in_market(args.reference)
        if not ref_ops:
            print(f"ERROR: No operators found for reference market '{args.reference}'")
            sys.exit(1)

        print(f"\nOperators in {args.reference}:")
        for i, op in enumerate(ref_ops, 1):
            print(f"  {i}. {op.get('display_name', op['operator_id'])} ({op['operator_id']})")

        if len(ref_ops) == 1:
            ref_operator = ref_ops[0]["operator_id"]
            print(f"  -> Auto-selected: {ref_operator}")
        else:
            choice = input(f"Select reference operator [1-{len(ref_ops)}]: ").strip()
            try:
                idx = int(choice) - 1
                if idx < 0 or idx >= len(ref_ops):
                    raise ValueError()
                ref_operator = ref_ops[idx]["operator_id"]
            except (ValueError, IndexError):
                print("ERROR: Invalid selection")
                sys.exit(1)

    # Run audit
    audit_svc = MarketAuditService(svc)
    report = audit_svc.run_audit(
        target_market=args.market,
        target_operator=target_operator,
        reference=args.reference or "",
        ref_operator=ref_operator,
        period=args.period,
        n_quarters=args.n_quarters,
    )
    print(audit_svc.format_console_report(report))

    if args.output_json:
        out_path = Path(args.output_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(report.to_dict(), indent=2, default=str),
            encoding="utf-8",
        )
        print(f"\nJSON report saved to: {args.output_json}")

    return 0


def cmd_feedback(args):
    """Manage user feedback records."""
    from src.database.db import TelecomDatabase
    from src.models.feedback import FEEDBACK_TYPES

    db = TelecomDatabase("data/telecom.db")
    db.init()

    action = args.action

    if action == "add":
        if not args.job_id or not args.operator or not args.look or not args.finding:
            print("ERROR: --job-id, --operator, --look, and --finding are required for 'add'")
            return 1
        if args.type and args.type not in FEEDBACK_TYPES:
            print(f"ERROR: --type must be one of {FEEDBACK_TYPES}")
            return 1
        data = {
            "analysis_job_id": args.job_id,
            "operator_id": args.operator,
            "period": args.period or "",
            "look_category": args.look,
            "finding_ref": args.finding,
            "feedback_type": args.type or "confirmed",
            "user_comment": args.comment or "",
            "original_value": args.value,
            "user_value": args.value,
        }
        db.upsert_feedback(data)
        print(f"Feedback upserted: job={args.job_id} op={args.operator} "
              f"look={args.look} finding={args.finding} type={args.type or 'confirmed'}")
        return 0

    elif action == "list":
        rows = db.get_feedback(
            analysis_job_id=args.job_id,
            operator_id=args.operator,
            look_category=args.look,
        )
        if not rows:
            print("No feedback records found.")
            return 0
        print(f"{'ID':>5}  {'Job':>5}  {'Operator':15}  {'Look':14}  {'Finding':20}  {'Type':12}  {'Comment'}")
        print("-" * 100)
        for r in rows:
            print(f"{r.get('id', ''):>5}  {r.get('analysis_job_id', ''):>5}  "
                  f"{r.get('operator_id', ''):15}  {r.get('look_category', ''):14}  "
                  f"{r.get('finding_ref', ''):20}  {r.get('feedback_type', ''):12}  "
                  f"{r.get('user_comment', '')}")
        print(f"\n{len(rows)} record(s)")
        return 0

    elif action == "export":
        rows = db.get_feedback(
            analysis_job_id=args.job_id,
            operator_id=args.operator,
            look_category=args.look,
        )
        print(json.dumps(rows, indent=2, default=str))
        return 0

    elif action == "clear":
        if not args.job_id or not args.operator:
            print("ERROR: --job-id and --operator are required for 'clear'")
            return 1
        count = db.clear_feedback(args.job_id, args.operator)
        print(f"Cleared {count} feedback record(s) for job={args.job_id} op={args.operator}")
        return 0

    else:
        print(f"Unknown action: {action}. Use add/list/export/clear.")
        return 1


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

    # audit
    p_audit = sub.add_parser("audit", help="Market readiness audit")
    p_audit.add_argument("--market", required=True, help="Target market ID (e.g., chile)")
    p_audit.add_argument("--reference", default=None, help="Reference market ID (e.g., germany). Omit for absolute thresholds.")
    p_audit.add_argument("--period", default="CQ4_2025", help="Analysis period (default: CQ4_2025)")
    p_audit.add_argument("--n-quarters", type=int, default=8, help="Historical range in quarters (default: 8)")
    p_audit.add_argument("--output-json", default=None, help="Path to save JSON report")

    # feedback
    p_feedback = sub.add_parser("feedback", help="Manage user feedback")
    p_feedback.add_argument("action", choices=["add", "list", "export", "clear"],
                            help="Action: add/list/export/clear")
    p_feedback.add_argument("--job-id", type=int, default=None, help="Analysis job ID")
    p_feedback.add_argument("--operator", default=None, help="Operator ID")
    p_feedback.add_argument("--look", default=None, help="Look category (trends/market/competition/self/swot/opportunity)")
    p_feedback.add_argument("--finding", default=None, help="Finding reference")
    p_feedback.add_argument("--type", default=None, help="Feedback type (confirmed/disputed/modified/supplemented)")
    p_feedback.add_argument("--comment", default=None, help="User comment")
    p_feedback.add_argument("--value", default=None, help="User value (override)")
    p_feedback.add_argument("--period", default=None, help="Analysis period (e.g., CQ4_2025)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "single": cmd_single,
        "group": cmd_group,
        "list": cmd_list,
        "status": cmd_status,
        "audit": cmd_audit,
        "feedback": cmd_feedback,
    }

    exit_code = commands[args.command](args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
