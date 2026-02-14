"""Local group analysis CLI — bypasses Supabase entirely.

Seeds all 12 markets into a temp SQLite DB, runs Five Looks for each
Tigo operator, and generates a GroupSummary + optional per-market MD reports.

Usage:
    python3 -m src.cli_group_local                             # all 11 Tigo markets
    python3 -m src.cli_group_local --markets guatemala,honduras
    python3 -m src.cli_group_local --output-dir data/output/group
    python3 -m src.cli_group_local --with-md                   # also generate per-market MD
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))


def main():
    parser = argparse.ArgumentParser(
        description="BLM Local Group Analysis — Millicom/Tigo cross-market report"
    )
    parser.add_argument(
        "--markets", default="",
        help="Comma-separated market IDs (default: all 11 Tigo markets)",
    )
    parser.add_argument(
        "--output-dir", default="data/output/group",
        help="Output directory (default: data/output/group)",
    )
    parser.add_argument(
        "--period", default="CQ4_2025",
        help="Analysis period (default: CQ4_2025)",
    )
    parser.add_argument(
        "--n-quarters", type=int, default=8,
        help="Historical range in quarters (default: 8)",
    )
    parser.add_argument(
        "--with-md", action="store_true",
        help="Also generate per-market MD strategic reports",
    )
    args = parser.parse_args()

    from src.database.seed_orchestrator import seed_all_markets, TIGO_OPERATORS
    from src.database.operator_directory import OPERATOR_GROUPS

    # Determine which Tigo markets to analyze
    if args.markets:
        selected = [m.strip() for m in args.markets.split(",")]
        tigo_ops = [(op, mkt) for op, mkt in TIGO_OPERATORS if mkt in selected]
        if not tigo_ops:
            print(f"ERROR: No Tigo operators found for markets: {args.markets}")
            print(f"Available: {', '.join(m for _, m in TIGO_OPERATORS)}")
            sys.exit(1)
    else:
        tigo_ops = TIGO_OPERATORS

    print("=" * 60)
    print("  BLM Local Group Analysis — Millicom/Tigo")
    print(f"  Markets: {len(tigo_ops)}")
    print(f"  Period:  {args.period}")
    print(f"  Output:  {args.output_dir}")
    print("=" * 60)

    # 1. Seed all markets into temp SQLite
    print("\nPhase 1: Seeding all markets into local SQLite...")
    tmp_dir = tempfile.mkdtemp(prefix="blm_group_")
    db_path = str(Path(tmp_dir) / "group_analysis.db")
    db = seed_all_markets(db_path)

    # 2. Run Five Looks for each Tigo operator
    print("\nPhase 2: Running Five Looks analysis for each Tigo operator...")
    from src.blm.engine import BLMAnalysisEngine

    market_results = {}
    for operator_id, market_id in tigo_ops:
        print(f"\n  [{len(market_results)+1}/{len(tigo_ops)}] {operator_id} in {market_id}...")
        try:
            engine = BLMAnalysisEngine(
                db=db,
                target_operator=operator_id,
                market=market_id,
                target_period=args.period,
                n_quarters=args.n_quarters,
            )
            result = engine.run_five_looks()
            market_results[market_id] = result
            print(f"    OK — {result.analysis_period}")
        except Exception as e:
            print(f"    FAILED — {type(e).__name__}: {e}")

    if not market_results:
        print("\nERROR: No markets completed successfully")
        db.close()
        sys.exit(1)

    # 3. Generate group summary
    print(f"\nPhase 3: Generating group summary ({len(market_results)} markets)...")
    from src.web.services.group_summary import GroupSummaryGenerator

    group_info = OPERATOR_GROUPS.get("millicom", {})
    gen = GroupSummaryGenerator()
    summary = gen.generate(market_results, group_info)

    # 4. Write outputs
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # JSON
    json_name = f"blm_millicom_group_summary_{args.period.lower()}.json"
    json_path = output_dir / json_name
    json_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    print(f"  JSON: {json_path} ({json_path.stat().st_size / 1024:.1f} KB)")

    # TXT
    txt_name = f"blm_millicom_group_summary_{args.period.lower()}.txt"
    txt_path = output_dir / txt_name
    txt_content = _format_group_txt(summary, args.period)
    txt_path.write_text(txt_content, encoding="utf-8")
    print(f"  TXT: {txt_path} ({txt_path.stat().st_size / 1024:.1f} KB)")

    # 5. Optionally generate per-market MD reports
    if args.with_md:
        print("\nPhase 4: Generating per-market MD reports...")
        from src.output.md_generator import BLMMdGenerator
        md_gen = BLMMdGenerator()

        for market_id, result in market_results.items():
            try:
                md_content = md_gen.generate(result)
                md_name = f"blm_{result.target_operator}_analysis_{args.period.lower()}.md"
                md_path = output_dir / md_name
                md_path.write_text(md_content, encoding="utf-8")
                lines = md_content.count("\n") + 1
                print(f"    MD: {md_name} ({lines} lines, {md_path.stat().st_size / 1024:.0f} KB)")
            except Exception as e:
                print(f"    MD FAILED for {market_id}: {e}")

    # Summary
    print(f"\n{'='*60}")
    print(f"  Group Analysis Complete")
    print(f"  Markets analyzed:  {len(market_results)}/{len(tigo_ops)}")
    print(f"  Output directory:  {output_dir}")
    print(f"  Files generated:   {len(list(output_dir.glob('blm_millicom_*')))} group + "
          f"{len(list(output_dir.glob('blm_tigo_*')))} per-market")
    print(f"{'='*60}")

    # Key findings
    findings = summary.get("key_findings", [])
    if findings:
        print("\nKey Findings:")
        for f in findings:
            print(f"  -> {f}")

    db.close()
    return 0


def _format_group_txt(summary: dict, period: str) -> str:
    """Format group summary as plain text."""
    lines = []
    lines.append("=" * 80)
    lines.append(f"  BLM Group Analysis Summary: MILLICOM (Tigo)")
    lines.append(f"  Period: {period}")
    lines.append(f"  Markets: {summary.get('market_count', 0)}")
    lines.append("=" * 80)

    # Revenue comparison
    rev = summary.get("revenue_comparison", {})
    if rev:
        lines.append("\n[Revenue Comparison]")
        lines.append(f"  {'Market':<20s}  {'Revenue':>12s}  {'Growth':>8s}  {'EBITDA Margin':>14s}")
        lines.append(f"  {'-'*20}  {'-'*12}  {'-'*8}  {'-'*14}")
        for market, data in sorted(rev.items()):
            rev_val = data.get("total_revenue")
            rev_str = f"{rev_val:,.0f}" if rev_val else "N/A"
            growth = data.get("revenue_growth_pct")
            growth_str = f"{growth:+.1f}%" if growth else "N/A"
            margin = data.get("ebitda_margin_pct")
            margin_str = f"{margin:.1f}%" if margin else "N/A"
            lines.append(f"  {market:<20s}  {rev_str:>12s}  {growth_str:>8s}  {margin_str:>14s}")

    # Subscriber comparison
    subs = summary.get("subscriber_comparison", {})
    if subs:
        lines.append("\n[Subscriber Comparison]")
        lines.append(f"  {'Market':<20s}  {'Mobile (K)':>12s}  {'BB (K)':>10s}  {'ARPU':>8s}")
        lines.append(f"  {'-'*20}  {'-'*12}  {'-'*10}  {'-'*8}")
        for market, data in sorted(subs.items()):
            mobile = data.get("mobile_subs_k")
            mobile_str = f"{mobile:,.0f}" if mobile else "N/A"
            bb = data.get("broadband_subs_k")
            bb_str = f"{bb:,.0f}" if bb else "N/A"
            arpu = data.get("mobile_arpu")
            arpu_str = f"{arpu:.1f}" if arpu else "N/A"
            lines.append(f"  {market:<20s}  {mobile_str:>12s}  {bb_str:>10s}  {arpu_str:>8s}")

    # Competitive position
    comp = summary.get("competitive_position", {})
    if comp:
        lines.append("\n[Competitive Position]")
        for market, data in sorted(comp.items()):
            ranking = data.get("ranking", "N/A")
            intensity = data.get("intensity", "N/A")
            lines.append(f"  {market:<20s}  Rank: {ranking}  Intensity: {intensity}")

    # Common opportunities
    opps = summary.get("common_opportunities", [])
    if opps:
        lines.append("\n[Common Opportunities (2+ markets)]")
        for opp in opps[:10]:
            lines.append(f"  -> {opp}")

    # Common threats
    threats = summary.get("common_threats", [])
    if threats:
        lines.append("\n[Common Threats (2+ markets)]")
        for threat in threats[:10]:
            lines.append(f"  !! {threat}")

    # Key findings
    findings = summary.get("key_findings", [])
    if findings:
        lines.append("\n[Key Findings]")
        for finding in findings:
            lines.append(f"  * {finding}")

    # Health ratings
    health = summary.get("health_ratings", {})
    if health:
        lines.append("\n[Market Health Ratings]")
        for market, rating in sorted(health.items()):
            lines.append(f"  {market:<20s}  {rating}")

    lines.append("\n" + "=" * 80)
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
