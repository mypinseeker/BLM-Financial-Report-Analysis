"""CLI commands for BLM Strategic Analysis.

Provides command-line interface for running BLM (Business Leadership Model)
strategic analysis on telecom operators.

Usage:
    blm-analyze blm analyze --target "China Mobile" --competitors "China Telecom,China Unicom"
    blm-analyze blm compare --operators "Vodafone,MTN,Orange"
    blm-analyze blm generate-data --operators "AT&T,Verizon,T-Mobile US" --output data.json
"""

import json
import sys
from pathlib import Path
from typing import Optional

import click
import pandas as pd

from src.blm.telecom_data import (
    GLOBAL_OPERATORS,
    TelecomDataGenerator,
    generate_sample_data,
)
from src.blm.five_looks import FiveLooksAnalyzer
from src.blm.three_decisions import ThreeDecisionsEngine, generate_blm_strategy
from src.blm.report_generator import BLMReportGenerator


@click.group(name="blm")
def blm_cli():
    """BLM (Business Leadership Model) Strategic Analysis.

    Perform telecom operator strategic analysis using the BLM framework:
    - Five Looks (五看): Market, Self, Competitors, Macro, Opportunities
    - Three Decisions (三定): Strategy, Key Tasks, Execution
    """
    pass


@blm_cli.command("list-operators")
def list_operators():
    """List all supported global telecom operators."""
    click.echo("\n" + "=" * 60)
    click.echo("  Supported Global Telecom Operators")
    click.echo("=" * 60 + "\n")

    # Group by region
    by_region = {}
    for name, info in GLOBAL_OPERATORS.items():
        region = info["region"]
        if region not in by_region:
            by_region[region] = []
        by_region[region].append((name, info["country"], info["type"]))

    for region in sorted(by_region.keys()):
        click.echo(f"  [{region}]")
        for name, country, op_type in sorted(by_region[region]):
            click.echo(f"    • {name} ({country}) - {op_type}")
        click.echo()

    click.echo(f"Total: {len(GLOBAL_OPERATORS)} operators")


@blm_cli.command("analyze")
@click.option(
    "--target", "-t", required=True,
    help="Target operator to analyze (e.g., 'China Mobile', 'Vodafone')."
)
@click.option(
    "--competitors", "-c", default="",
    help="Comma-separated list of competitor operators."
)
@click.option(
    "--data-file", "-d", default=None, type=click.Path(exists=True),
    help="Path to existing data file (JSON). If not provided, generates sample data."
)
@click.option(
    "--output-dir", "-o", default=None,
    help="Output directory for reports."
)
@click.option(
    "--format", "-f", "report_format",
    type=click.Choice(["html", "text", "json", "all"]),
    default="html",
    help="Report output format."
)
@click.option(
    "--quarters", "-q", default=8, type=int,
    help="Number of quarters of data to generate (if no data file)."
)
def analyze(target, competitors, data_file, output_dir, report_format, quarters):
    """Run full BLM strategic analysis on a telecom operator.

    Performs Five Looks (五看) analysis and Three Decisions (三定) strategy
    generation for the specified operator.

    Examples:
        blm-analyze blm analyze -t "China Mobile" -c "China Telecom,China Unicom"
        blm-analyze blm analyze -t "Vodafone" -c "Orange,Deutsche Telekom" -f all
    """
    click.echo(f"\n{'=' * 60}")
    click.echo(f"  BLM Strategic Analysis: {target}")
    click.echo(f"{'=' * 60}\n")

    # Parse competitors
    competitor_list = [c.strip() for c in competitors.split(",") if c.strip()]

    # Validate operators
    all_operators = [target] + competitor_list
    for op in all_operators:
        if op not in GLOBAL_OPERATORS:
            click.echo(f"Warning: '{op}' not in registry. Using default profile.", err=True)

    # Load or generate data
    if data_file:
        click.echo(f"Loading data from: {data_file}")
        data = _load_data_file(data_file)
    else:
        click.echo(f"Generating sample data for: {', '.join(all_operators)}")
        generator = TelecomDataGenerator(seed=42)
        data = generator.generate_dataset(all_operators, n_quarters=quarters)

    click.echo(f"Data loaded: {sum(len(df) for df in data.values())} total records\n")

    # Run Five Looks analysis
    click.echo("Running Five Looks (五看) analysis...")
    analyzer = FiveLooksAnalyzer(data, target, competitor_list)
    five_looks = analyzer.run_full_analysis()

    for key, result in five_looks.items():
        click.echo(f"  ✓ {result.title}")

    click.echo()

    # Run Three Decisions strategy
    click.echo("Running Three Decisions (三定) strategy...")
    strategy_engine = ThreeDecisionsEngine(five_looks, target)
    three_decisions = strategy_engine.run_full_strategy()

    for key, result in three_decisions.items():
        click.echo(f"  ✓ {result.title}")

    click.echo()

    # Generate reports
    click.echo("Generating reports...")
    report_gen = BLMReportGenerator(output_dir=output_dir)

    if report_format in ("html", "all"):
        path = report_gen.generate_html_report(
            five_looks, three_decisions, target, competitor_list,
            filename=f"blm_{_sanitize_name(target)}_report.html",
        )
        click.echo(f"  HTML report: {path}")

    if report_format in ("text", "all"):
        path = report_gen.generate_text_report(
            five_looks, three_decisions, target, competitor_list,
            filename=f"blm_{_sanitize_name(target)}_report.txt",
        )
        click.echo(f"  Text report: {path}")

    if report_format in ("json", "all"):
        path = report_gen.generate_json_report(
            five_looks, three_decisions, target, competitor_list,
            filename=f"blm_{_sanitize_name(target)}_report.json",
        )
        click.echo(f"  JSON report: {path}")

    # Print executive summary
    click.echo("\n" + "=" * 60)
    click.echo("  Executive Summary")
    click.echo("=" * 60 + "\n")
    summary = report_gen.generate_executive_summary(five_looks, three_decisions, target)
    click.echo(summary)

    click.echo("\n\nAnalysis complete.")


@blm_cli.command("compare")
@click.option(
    "--operators", "-o", required=True,
    help="Comma-separated list of operators to compare."
)
@click.option(
    "--output-dir", default=None,
    help="Output directory for reports."
)
@click.option(
    "--quarters", "-q", default=8, type=int,
    help="Number of quarters of data to generate."
)
def compare(operators, output_dir, quarters):
    """Compare multiple telecom operators side-by-side.

    Generates a comparison report showing key metrics and competitive
    positioning across all specified operators.

    Example:
        blm-analyze blm compare -o "Vodafone,MTN,Orange,Telefonica"
    """
    operator_list = [op.strip() for op in operators.split(",") if op.strip()]

    if len(operator_list) < 2:
        click.echo("Error: At least 2 operators required for comparison.", err=True)
        sys.exit(1)

    click.echo(f"\n{'=' * 60}")
    click.echo(f"  Multi-Operator Comparison")
    click.echo(f"{'=' * 60}\n")
    click.echo(f"Operators: {', '.join(operator_list)}\n")

    # Generate data
    click.echo("Generating data...")
    generator = TelecomDataGenerator(seed=42)
    data = generator.generate_dataset(operator_list, n_quarters=quarters)

    # Get latest quarter metrics for comparison
    market_df = data["market"]
    fin_df = data["financial"]
    comp_df = data["competitive"]

    latest_q = market_df["quarter"].max()

    click.echo("\n" + "-" * 60)
    click.echo("  Market Position Comparison")
    click.echo("-" * 60)

    comparison_data = []
    for op in operator_list:
        op_market = market_df[(market_df["quarter"] == latest_q) & (market_df["operator"] == op)]
        op_fin = fin_df[(fin_df["quarter"] == fin_df["quarter"].max()) & (fin_df["operator"] == op)]
        op_comp = comp_df[(comp_df["quarter"] == comp_df["quarter"].max()) & (comp_df["operator"] == op)]

        row = {
            "Operator": op,
            "Market Share (%)": op_market["market_share_pct"].iloc[0] if not op_market.empty else "N/A",
            "Revenue ($B)": op_fin["revenue_billion_usd"].iloc[0] if not op_fin.empty else "N/A",
            "Profit Margin (%)": op_fin["profit_margin_pct"].iloc[0] if not op_fin.empty else "N/A",
            "5G Users (%)": op_market["5g_users_pct"].iloc[0] if not op_market.empty else "N/A",
            "Avg Score": round(op_comp["score"].mean(), 1) if not op_comp.empty else "N/A",
        }
        comparison_data.append(row)

    comparison_df = pd.DataFrame(comparison_data)
    click.echo(comparison_df.to_string(index=False))

    # Competitive dimensions comparison
    click.echo("\n" + "-" * 60)
    click.echo("  Competitive Dimensions")
    click.echo("-" * 60)

    pivot = comp_df[comp_df["quarter"] == latest_q].pivot(
        index="dimension", columns="operator", values="score"
    )
    click.echo(pivot.to_string())

    # Export comparison
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        comparison_df.to_csv(output_path / "operator_comparison.csv", index=False)
        pivot.to_csv(output_path / "competitive_dimensions.csv")
        click.echo(f"\nExported to: {output_path}")

    click.echo("\nComparison complete.")


@blm_cli.command("generate-data")
@click.option(
    "--operators", "-o", default="China Mobile,China Telecom,China Unicom",
    help="Comma-separated list of operators."
)
@click.option(
    "--quarters", "-q", default=8, type=int,
    help="Number of quarters of data."
)
@click.option(
    "--output", default="data/raw/blm_sample_data.json",
    help="Output file path."
)
@click.option(
    "--seed", default=42, type=int,
    help="Random seed for reproducibility."
)
def generate_data(operators, quarters, output, seed):
    """Generate sample telecom operator data for BLM analysis.

    Creates realistic sample data for market metrics, financial performance,
    competitive positioning, macro environment, and customer metrics.

    Example:
        blm-analyze blm generate-data -o "AT&T,Verizon,T-Mobile US" -q 12
    """
    operator_list = [op.strip() for op in operators.split(",") if op.strip()]

    click.echo(f"\n{'=' * 60}")
    click.echo("  Generating BLM Sample Data")
    click.echo(f"{'=' * 60}\n")
    click.echo(f"Operators: {', '.join(operator_list)}")
    click.echo(f"Quarters: {quarters}")
    click.echo(f"Seed: {seed}\n")

    generator = TelecomDataGenerator(seed=seed)
    data = generator.generate_dataset(operator_list, n_quarters=quarters)

    # Convert to JSON-serializable format
    output_data = {
        key: df.to_dict(orient="records")
        for key, df in data.items()
    }
    output_data["_meta"] = {
        "operators": operator_list,
        "quarters": quarters,
        "seed": seed,
    }

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    click.echo(f"Data summary:")
    for key, df in data.items():
        click.echo(f"  • {key}: {len(df)} records")

    click.echo(f"\nSaved to: {output_path}")


@blm_cli.command("five-looks")
@click.option(
    "--target", "-t", required=True,
    help="Target operator to analyze."
)
@click.option(
    "--competitors", "-c", default="",
    help="Comma-separated list of competitor operators."
)
@click.option(
    "--look", "-l",
    type=click.Choice(["market", "self", "competitor", "macro", "opportunity", "all"]),
    default="all",
    help="Which look to perform."
)
def five_looks(target, competitors, look):
    """Run Five Looks (五看) analysis only.

    Available looks:
    - market: 看市场 - Market insight
    - self: 看自己 - Self assessment
    - competitor: 看对手 - Competitive analysis
    - macro: 看宏观 - Macro environment
    - opportunity: 看机会 - Opportunity identification

    Example:
        blm-analyze blm five-looks -t "MTN" -c "Airtel Africa" -l market
    """
    competitor_list = [c.strip() for c in competitors.split(",") if c.strip()]
    all_operators = [target] + competitor_list

    click.echo(f"\n{'=' * 60}")
    click.echo(f"  Five Looks Analysis: {target}")
    click.echo(f"{'=' * 60}\n")

    # Generate data
    data = generate_sample_data(all_operators)

    # Run analysis
    analyzer = FiveLooksAnalyzer(data, target, competitor_list)

    if look == "all":
        results = analyzer.run_full_analysis()
    else:
        look_method = {
            "market": analyzer.look_at_market,
            "self": analyzer.look_at_self,
            "competitor": analyzer.look_at_competitors,
            "macro": analyzer.look_at_macro,
            "opportunity": analyzer.look_at_opportunities,
        }
        results = {look: look_method[look]()}

    # Print results
    for key, result in results.items():
        click.echo("-" * 60)
        click.echo(f"  {result.title}")
        click.echo("-" * 60 + "\n")

        if result.metrics:
            click.echo("  [Metrics]")
            for mkey, mval in result.metrics.items():
                click.echo(f"    • {mkey}: {mval}")
            click.echo()

        click.echo("  [Findings]")
        for finding in result.findings:
            click.echo(f"    • {finding}")
        click.echo()

        if result.recommendations:
            click.echo("  [Recommendations]")
            for rec in result.recommendations:
                click.echo(f"    → {rec}")
            click.echo()


@blm_cli.command("three-decisions")
@click.option(
    "--target", "-t", required=True,
    help="Target operator to analyze."
)
@click.option(
    "--competitors", "-c", default="",
    help="Comma-separated list of competitor operators."
)
@click.option(
    "--decision", "-d",
    type=click.Choice(["strategy", "key_tasks", "execution", "all"]),
    default="all",
    help="Which decision to generate."
)
def three_decisions_cmd(target, competitors, decision):
    """Run Three Decisions (三定) strategy only.

    Available decisions:
    - strategy: 定策略 - Set Strategy
    - key_tasks: 定重点工作 - Set Key Tasks
    - execution: 定执行 - Set Execution

    Example:
        blm-analyze blm three-decisions -t "Orange" -d strategy
    """
    competitor_list = [c.strip() for c in competitors.split(",") if c.strip()]
    all_operators = [target] + competitor_list

    click.echo(f"\n{'=' * 60}")
    click.echo(f"  Three Decisions Strategy: {target}")
    click.echo(f"{'=' * 60}\n")

    # Generate data and run Five Looks first
    data = generate_sample_data(all_operators)
    analyzer = FiveLooksAnalyzer(data, target, competitor_list)
    five_looks_results = analyzer.run_full_analysis()

    # Run Three Decisions
    engine = ThreeDecisionsEngine(five_looks_results, target)

    if decision == "all":
        results = engine.run_full_strategy()
    else:
        decision_method = {
            "strategy": engine.define_strategy,
            "key_tasks": engine.define_key_tasks,
            "execution": engine.define_execution,
        }
        results = {decision: decision_method[decision]()}

    # Print results
    for key, result in results.items():
        click.echo("-" * 60)
        click.echo(f"  {result.title}")
        click.echo("-" * 60 + "\n")

        click.echo("  [Summary]")
        for line in result.summary.split("\n"):
            click.echo(f"    {line}")
        click.echo()

        click.echo("  [Items]")
        for item in result.items:
            priority_marker = {"P0": "!", "P1": "+", "P2": "-"}.get(item.priority, " ")
            click.echo(f"    [{priority_marker}] {item.name}")
            click.echo(f"        {item.description}")
            if item.kpis:
                click.echo(f"        KPI: {', '.join(item.kpis)}")
            click.echo()


def _load_data_file(filepath: str) -> dict[str, pd.DataFrame]:
    """Load data from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        raw = json.load(f)

    data = {}
    for key, records in raw.items():
        if key.startswith("_"):
            continue
        data[key] = pd.DataFrame(records)

    return data


def _sanitize_name(name: str) -> str:
    """Sanitize operator name for use in filenames."""
    return name.lower().replace(" ", "_").replace("/", "_")
