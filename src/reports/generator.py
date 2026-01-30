"""Report generation module for BLM financial analysis.

Generates HTML and text reports from analysis results.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from jinja2 import Template

from src.analysis.financial import AnalysisResult


HTML_REPORT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f5f5f5; color: #333; line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header {
            background: linear-gradient(135deg, #1a5276, #2e86c1);
            color: white; padding: 30px; border-radius: 8px; margin-bottom: 20px;
        }
        header h1 { font-size: 24px; margin-bottom: 5px; }
        header p { opacity: 0.8; font-size: 14px; }
        .section {
            background: white; border-radius: 8px; padding: 25px;
            margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .section h2 {
            font-size: 18px; color: #1a5276; margin-bottom: 15px;
            padding-bottom: 10px; border-bottom: 2px solid #eee;
        }
        .summary-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px; margin-bottom: 15px;
        }
        .summary-card {
            background: #f8f9fa; padding: 15px; border-radius: 6px;
            border-left: 4px solid #2e86c1;
        }
        .summary-card .label { font-size: 12px; text-transform: uppercase; color: #666; }
        .summary-card .value { font-size: 20px; font-weight: bold; color: #1a5276; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; }
        th {
            background: #1a5276; color: white; padding: 10px 12px;
            text-align: left; font-weight: 600;
        }
        td { padding: 8px 12px; border-bottom: 1px solid #eee; }
        tr:hover { background: #f8f9fa; }
        .chart-container { text-align: center; margin: 15px 0; }
        .chart-container img { max-width: 100%; border-radius: 6px; }
        footer { text-align: center; color: #888; font-size: 12px; padding: 20px; }
        .positive { color: #27ae60; }
        .negative { color: #e74c3c; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ title }}</h1>
            <p>Generated: {{ generated_at }} | Period: {{ period }}</p>
        </header>

        {% for section in sections %}
        <div class="section">
            <h2>{{ section.title }}</h2>

            {% if section.summary %}
            <div class="summary-grid">
                {% for key, value in section.summary.items() %}
                <div class="summary-card">
                    <div class="label">{{ key | replace("_", " ") }}</div>
                    <div class="value">{{ value }}</div>
                </div>
                {% endfor %}
            </div>
            {% endif %}

            {% if section.chart_path %}
            <div class="chart-container">
                <img src="{{ section.chart_path }}" alt="{{ section.title }}">
            </div>
            {% endif %}

            {% if section.table_html %}
            {{ section.table_html }}
            {% endif %}
        </div>
        {% endfor %}

        <footer>
            BLM Financial Report Analysis Tool v{{ version }}
        </footer>
    </div>
</body>
</html>"""


class ReportGenerator:
    """Generate financial analysis reports in various formats."""

    def __init__(self, output_dir: Optional[str] = None):
        if output_dir is None:
            output_dir = str(Path(__file__).resolve().parent.parent.parent / "data" / "output")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_html_report(
        self,
        results: list[AnalysisResult],
        title: str = "BLM Financial Analysis Report",
        period: str = "",
        chart_paths: Optional[dict[str, str]] = None,
        filename: str = "report.html",
    ) -> str:
        """Generate an HTML report from analysis results.

        Args:
            results: List of AnalysisResult objects.
            title: Report title.
            period: Reporting period description.
            chart_paths: Dict mapping result names to chart image paths.
            filename: Output filename.

        Returns:
            Path to the generated report.
        """
        chart_paths = chart_paths or {}

        sections = []
        for result in results:
            section = {
                "title": result.name.replace("_", " ").title(),
                "summary": self._format_summary(result.summary),
                "chart_path": chart_paths.get(result.name, ""),
                "table_html": self._df_to_html(result.details) if not result.details.empty else "",
            }
            sections.append(section)

        template = Template(HTML_REPORT_TEMPLATE)
        html = template.render(
            title=title,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            period=period or "All Available Data",
            sections=sections,
            version="0.1.0",
        )

        output_path = self.output_dir / filename
        output_path.write_text(html, encoding="utf-8")
        return str(output_path)

    def generate_text_report(
        self,
        results: list[AnalysisResult],
        title: str = "BLM Financial Analysis Report",
        filename: str = "report.txt",
    ) -> str:
        """Generate a plain text report from analysis results.

        Args:
            results: List of AnalysisResult objects.
            title: Report title.
            filename: Output filename.

        Returns:
            Path to the generated report.
        """
        lines = [
            "=" * 70,
            title.center(70),
            "=" * 70,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]

        for result in results:
            lines.append("-" * 70)
            lines.append(f"  {result.name.replace('_', ' ').upper()}")
            lines.append("-" * 70)
            lines.append("")

            # Summary
            lines.append("  Summary:")
            for key, value in result.summary.items():
                formatted_key = key.replace("_", " ").title()
                lines.append(f"    {formatted_key}: {self._format_value(value)}")
            lines.append("")

            # Details table
            if not result.details.empty:
                lines.append("  Details:")
                table_str = result.details.to_string(index=False)
                for line in table_str.split("\n"):
                    lines.append(f"    {line}")
                lines.append("")

        lines.append("=" * 70)
        lines.append("End of Report".center(70))
        lines.append("=" * 70)

        output_path = self.output_dir / filename
        output_path.write_text("\n".join(lines), encoding="utf-8")
        return str(output_path)

    def generate_json_report(
        self,
        results: list[AnalysisResult],
        title: str = "BLM Financial Analysis Report",
        filename: str = "report.json",
    ) -> str:
        """Generate a JSON report from analysis results.

        Args:
            results: List of AnalysisResult objects.
            title: Report title.
            filename: Output filename.

        Returns:
            Path to the generated report.
        """
        report_data = {
            "title": title,
            "generated_at": datetime.now().isoformat(),
            "results": [r.to_dict() for r in results],
        }

        output_path = self.output_dir / filename
        output_path.write_text(
            json.dumps(report_data, indent=2, default=str),
            encoding="utf-8",
        )
        return str(output_path)

    @staticmethod
    def _format_summary(summary: dict) -> dict:
        """Format summary values for display.

        Uses the key name to determine formatting (e.g., keys containing
        'pct' or 'rate' are formatted as percentages).
        """
        formatted = {}
        for key, value in summary.items():
            formatted[key] = ReportGenerator._format_value(value, key)
        return formatted

    @staticmethod
    def _format_value(value, key: str = "") -> str:
        """Format a single value for display.

        Args:
            value: The value to format.
            key: The associated key name, used to determine format
                 (e.g., keys with 'pct' or 'rate' are percentages).
        """
        if isinstance(value, float):
            key_lower = key.lower()
            is_pct = "pct" in key_lower or "rate" in key_lower or "percentage" in key_lower
            if is_pct:
                return f"{value:.1f}%"
            if abs(value) >= 1_000_000:
                return f"${value:,.0f}"
            return f"{value:,.2f}"
        return str(value)

    @staticmethod
    def _df_to_html(df: pd.DataFrame, max_rows: int = 50) -> str:
        """Convert DataFrame to styled HTML table."""
        display_df = df.head(max_rows) if len(df) > max_rows else df
        html = display_df.to_html(index=False, classes="data-table", border=0)
        if len(df) > max_rows:
            html += f"<p><em>Showing {max_rows} of {len(df)} rows</em></p>"
        return html
