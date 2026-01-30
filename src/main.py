"""CLI entry point for BLM Financial Report Analysis Tool.

Usage:
    blm-analyze analyze <file> [--output-dir DIR] [--format FORMAT]
    blm-analyze summary <file> [--amount-col COL] [--group-col COL]
    blm-analyze export <file> [--output-dir DIR] [--fmt FORMAT]
    blm-analyze generate-sample [--output FILE]
"""

import sys
from pathlib import Path

import click
import pandas as pd

from src.config import Config
from src.data.loader import DataLoader, FinancialDataPreprocessor
from src.data.export import DataExporter
from src.analysis.financial import BudgetAnalyzer
from src.visualization.charts import FinancialChartGenerator
from src.reports.generator import ReportGenerator


@click.group()
@click.version_option(version="0.1.0", prog_name="blm-analyze")
@click.option("--config", "config_path", default=None, type=click.Path(), help="Path to YAML config file.")
@click.pass_context
def cli(ctx, config_path):
    """BLM Financial Report Analysis Tool.

    Analyze Bureau of Land Management financial reports with
    budget variance analysis, trend detection, anomaly identification,
    and comprehensive report generation.
    """
    ctx.ensure_object(dict)
    ctx.obj["config"] = Config(config_path)


def _load_data(file: str) -> pd.DataFrame:
    """Load and preprocess a data file."""
    loader = DataLoader()
    preprocessor = FinancialDataPreprocessor()
    df = loader.load(file)
    return preprocessor.preprocess(df)


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--output-dir", "-o", default=None, help="Output directory for reports and charts.")
@click.option(
    "--format", "-f", "report_format",
    type=click.Choice(["html", "text", "json", "all"]),
    default="html",
    help="Report output format.",
)
@click.option("--amount-col", default="amount", help="Column name for monetary amounts.")
@click.option("--budget-col", default="budget", help="Column name for budget amounts.")
@click.option("--actual-col", default="actual", help="Column name for actual expenditures.")
@click.option("--category-col", default="category", help="Column name for categories.")
@click.option("--date-col", default="date", help="Column name for dates.")
@click.option("--year-col", default="fiscal_year", help="Column name for fiscal year.")
@click.option("--state-col", default="state", help="Column name for state/region.")
@click.pass_context
def analyze(ctx, file, output_dir, report_format, amount_col, budget_col,
            actual_col, category_col, date_col, year_col, state_col):
    """Run full financial analysis on a data file.

    Performs summary statistics, budget variance analysis, trend analysis,
    anomaly detection, category breakdown, year-over-year comparison,
    and state comparison. Generates charts and reports.
    """
    config = ctx.obj["config"]
    click.echo(f"Loading data from: {file}")

    try:
        df = _load_data(file)
    except Exception as e:
        click.echo(f"Error loading file: {e}", err=True)
        sys.exit(1)

    click.echo(f"Loaded {len(df)} records with {len(df.columns)} columns.")
    click.echo(f"Columns: {', '.join(df.columns)}")

    analyzer = BudgetAnalyzer(df)
    results = []

    # Summary statistics
    if amount_col in df.columns:
        click.echo("Running summary statistics...")
        result = analyzer.summary_statistics(amount_col=amount_col, group_col=category_col)
        results.append(result)

    # Budget variance
    if budget_col in df.columns and actual_col in df.columns:
        click.echo("Running budget variance analysis...")
        result = analyzer.budget_variance(
            budget_col=budget_col, actual_col=actual_col, category_col=category_col,
        )
        results.append(result)

    # Trend analysis
    if amount_col in df.columns and date_col in df.columns:
        click.echo("Running trend analysis...")
        freq = config.get("analysis", "trend_frequency", default="YE")
        result = analyzer.trend_analysis(amount_col=amount_col, date_col=date_col, freq=freq)
        results.append(result)

    # Anomaly detection
    if amount_col in df.columns:
        click.echo("Running anomaly detection...")
        threshold = config.get("analysis", "anomaly_threshold", default=2.0)
        result = analyzer.detect_anomalies(amount_col=amount_col, threshold=threshold)
        results.append(result)

    # Category breakdown
    if amount_col in df.columns and category_col in df.columns:
        click.echo("Running category breakdown...")
        result = analyzer.category_breakdown(amount_col=amount_col, category_col=category_col)
        results.append(result)

    # Year-over-year comparison
    if amount_col in df.columns and year_col in df.columns:
        click.echo("Running year-over-year analysis...")
        result = analyzer.year_over_year(
            amount_col=amount_col, year_col=year_col, category_col=category_col,
        )
        results.append(result)

    # State comparison
    if amount_col in df.columns and state_col in df.columns:
        click.echo("Running state comparison...")
        result = analyzer.state_comparison(amount_col=amount_col, state_col=state_col)
        results.append(result)

    if not results:
        click.echo("No analyses could be performed. Check column names.", err=True)
        sys.exit(1)

    # Generate charts
    click.echo("Generating charts...")
    chart_gen = FinancialChartGenerator(output_dir=output_dir)
    chart_paths = {}

    for result in results:
        try:
            if result.name == "budget_variance" and not result.details.empty:
                path = chart_gen.budget_variance_chart(result.details)
                chart_paths[result.name] = path
            elif result.name == "trend_analysis" and not result.details.empty:
                path = chart_gen.trend_chart(result.details, date_col=date_col)
                chart_paths[result.name] = path
            elif result.name == "category_breakdown" and not result.details.empty:
                path = chart_gen.category_pie_chart(result.details)
                chart_paths[result.name] = path
            elif result.name == "anomaly_detection" and not result.details.empty:
                path = chart_gen.anomaly_scatter(result.details)
                chart_paths[result.name] = path
            elif result.name == "state_comparison" and not result.details.empty:
                path = chart_gen.top_n_bar_chart(
                    result.details, category_col=state_col, amount_col="total",
                    filename="state_comparison.png",
                )
                chart_paths[result.name] = path
        except Exception as e:
            click.echo(f"Warning: Could not generate chart for {result.name}: {e}")

    # Generate reports
    click.echo("Generating reports...")
    report_gen = ReportGenerator(output_dir=output_dir)

    if report_format in ("html", "all"):
        path = report_gen.generate_html_report(results, chart_paths=chart_paths)
        click.echo(f"HTML report: {path}")

    if report_format in ("text", "all"):
        path = report_gen.generate_text_report(results)
        click.echo(f"Text report: {path}")

    if report_format in ("json", "all"):
        path = report_gen.generate_json_report(results)
        click.echo(f"JSON report: {path}")

    click.echo("Analysis complete.")


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--amount-col", default="amount", help="Column name for monetary amounts.")
@click.option("--group-col", default=None, help="Column name for grouping.")
@click.pass_context
def summary(ctx, file, amount_col, group_col):
    """Print summary statistics for a financial data file."""
    try:
        df = _load_data(file)
    except Exception as e:
        click.echo(f"Error loading file: {e}", err=True)
        sys.exit(1)

    analyzer = BudgetAnalyzer(df)
    result = analyzer.summary_statistics(amount_col=amount_col, group_col=group_col)

    click.echo(f"\n{'=' * 50}")
    click.echo(f"  Summary Statistics: {Path(file).name}")
    click.echo(f"{'=' * 50}")
    for key, value in result.summary.items():
        click.echo(f"  {key.replace('_', ' ').title()}: {value}")
    click.echo(f"\n{result.details.to_string(index=False)}")


@cli.command("export")
@click.argument("file", type=click.Path(exists=True))
@click.option("--output-dir", "-o", default=None, help="Output directory for exported data.")
@click.option(
    "--fmt", type=click.Choice(["csv", "excel"]),
    default="csv", help="Export format.",
)
@click.option("--amount-col", default="amount", help="Column name for monetary amounts.")
@click.option("--category-col", default="category", help="Column name for categories.")
@click.option("--year-col", default="fiscal_year", help="Column name for fiscal year.")
@click.option("--state-col", default="state", help="Column name for state/region.")
@click.pass_context
def export(ctx, file, output_dir, fmt, amount_col, category_col, year_col, state_col):
    """Export processed data and analysis results.

    Loads the file, runs all applicable analyses, and exports results.
    """
    click.echo(f"Loading data from: {file}")

    try:
        df = _load_data(file)
    except Exception as e:
        click.echo(f"Error loading file: {e}", err=True)
        sys.exit(1)

    exporter = DataExporter(output_dir=output_dir)

    # Export processed data
    path = exporter.export_dataframe(df, "processed_data", fmt=fmt)
    click.echo(f"Processed data: {path}")

    # Run analyses and export results
    analyzer = BudgetAnalyzer(df)
    results = []

    if amount_col in df.columns:
        results.append(analyzer.summary_statistics(amount_col=amount_col))

    if amount_col in df.columns and category_col in df.columns:
        results.append(analyzer.category_breakdown(amount_col=amount_col, category_col=category_col))

    if amount_col in df.columns and year_col in df.columns:
        results.append(analyzer.year_over_year(amount_col=amount_col, year_col=year_col))

    if amount_col in df.columns and state_col in df.columns:
        results.append(analyzer.state_comparison(amount_col=amount_col, state_col=state_col))

    if results:
        paths = exporter.export_results(results, prefix="analysis", fmt=fmt)
        for p in paths:
            click.echo(f"Exported: {p}")

        summary_path = exporter.export_summary(results, filename="analysis_summary")
        click.echo(f"Summary: {summary_path}")

    click.echo("Export complete.")


@cli.command("generate-sample")
@click.option("--output", "-o", default="data/raw/sample_blm_data.csv", help="Output file path.")
@click.option("--records", "-n", default=200, type=int, help="Number of records to generate.")
def generate_sample(output, records):
    """Generate sample BLM financial data for testing."""
    from src.data.sample import generate_sample_data

    df = generate_sample_data(n_records=records)
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    click.echo(f"Sample data written to: {output_path} ({len(df)} records)")


if __name__ == "__main__":
    cli()
