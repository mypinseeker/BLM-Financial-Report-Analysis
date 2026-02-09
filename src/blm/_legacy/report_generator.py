"""BLM Strategic Analysis Report Generator.

Generates strategic analysis reports in HTML, text, and JSON formats
based on Five Looks (五看) and Three Decisions (三定) analysis results.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from jinja2 import Template

from src.blm._legacy.five_looks import InsightResult
from src.blm._legacy.three_decisions import StrategyResult


BLM_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
            background: #f0f2f5; color: #333; line-height: 1.7;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 30px; }
        header {
            background: linear-gradient(135deg, #1a365d, #2c5282, #3182ce);
            color: white; padding: 40px; border-radius: 12px; margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        header h1 { font-size: 32px; margin-bottom: 10px; }
        header .subtitle { opacity: 0.9; font-size: 18px; margin-bottom: 5px; }
        header .meta { opacity: 0.7; font-size: 14px; }

        .section-group { margin-bottom: 40px; }
        .section-group-title {
            font-size: 22px; color: #1a365d; margin-bottom: 20px;
            padding-bottom: 10px; border-bottom: 3px solid #3182ce;
            display: flex; align-items: center; gap: 10px;
        }
        .section-group-title .icon { font-size: 28px; }

        .section {
            background: white; border-radius: 10px; padding: 25px;
            margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid #3182ce;
        }
        .section h3 {
            font-size: 18px; color: #2d3748; margin-bottom: 15px;
            display: flex; align-items: center; gap: 8px;
        }
        .section h3 .badge {
            font-size: 12px; padding: 2px 8px; border-radius: 4px;
            background: #e2e8f0; color: #4a5568;
        }

        .findings-list { list-style: none; padding: 0; }
        .findings-list li {
            padding: 8px 0 8px 24px; border-bottom: 1px solid #f0f0f0;
            position: relative;
        }
        .findings-list li:before {
            content: "●"; position: absolute; left: 0; color: #3182ce;
        }
        .findings-list li:last-child { border-bottom: none; }

        .metrics-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px; margin: 15px 0;
        }
        .metric-card {
            background: linear-gradient(135deg, #f7fafc, #edf2f7);
            padding: 15px; border-radius: 8px; text-align: center;
        }
        .metric-card .label { font-size: 12px; color: #718096; text-transform: uppercase; }
        .metric-card .value { font-size: 24px; font-weight: bold; color: #2d3748; }

        .recommendations {
            background: #fffaf0; border-left: 4px solid #ed8936;
            padding: 15px 20px; margin-top: 15px; border-radius: 0 8px 8px 0;
        }
        .recommendations h4 { color: #c05621; margin-bottom: 10px; font-size: 14px; }
        .recommendations ul { margin: 0; padding-left: 20px; }
        .recommendations li { color: #744210; padding: 3px 0; }

        .strategy-item {
            background: #f7fafc; padding: 15px; margin: 10px 0; border-radius: 8px;
            border-left: 4px solid #48bb78;
        }
        .strategy-item.p0 { border-left-color: #e53e3e; }
        .strategy-item.p1 { border-left-color: #ed8936; }
        .strategy-item.p2 { border-left-color: #48bb78; }
        .strategy-item .name {
            font-weight: bold; color: #2d3748; margin-bottom: 5px;
            display: flex; align-items: center; gap: 8px;
        }
        .strategy-item .priority {
            font-size: 11px; padding: 2px 6px; border-radius: 3px;
            font-weight: bold;
        }
        .strategy-item .priority.p0 { background: #fed7d7; color: #c53030; }
        .strategy-item .priority.p1 { background: #feebc8; color: #c05621; }
        .strategy-item .priority.p2 { background: #c6f6d5; color: #276749; }
        .strategy-item .desc { color: #4a5568; font-size: 14px; }
        .strategy-item .kpis { font-size: 12px; color: #718096; margin-top: 8px; }

        table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 14px; }
        th { background: #2d3748; color: white; padding: 12px; text-align: left; }
        td { padding: 10px 12px; border-bottom: 1px solid #e2e8f0; }
        tr:hover { background: #f7fafc; }

        .summary-box {
            background: #ebf8ff; border: 1px solid #90cdf4; border-radius: 8px;
            padding: 20px; margin: 15px 0; white-space: pre-wrap; font-size: 14px;
            line-height: 1.8;
        }

        footer {
            text-align: center; color: #a0aec0; font-size: 12px; padding: 30px;
            border-top: 1px solid #e2e8f0; margin-top: 40px;
        }

        .positive { color: #38a169; }
        .negative { color: #e53e3e; }
        .warning { color: #dd6b20; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ title }}</h1>
            <div class="subtitle">{{ target_operator }} 战略分析报告</div>
            <div class="meta">
                生成时间: {{ generated_at }} |
                竞争对手: {{ competitors | join(", ") or "N/A" }}
            </div>
        </header>

        <!-- Five Looks Section -->
        <div class="section-group">
            <div class="section-group-title">
                <span class="icon">🔍</span>
                五看分析 (Five Looks Analysis)
            </div>

            {% for look_key, look in five_looks.items() %}
            <div class="section">
                <h3>
                    {{ look.title }}
                    <span class="badge">{{ look.category }}</span>
                </h3>

                {% if look.metrics %}
                <div class="metrics-grid">
                    {% for key, value in look.metrics.items() %}
                    <div class="metric-card">
                        <div class="label">{{ key | replace("_", " ") }}</div>
                        <div class="value">{{ value }}</div>
                    </div>
                    {% endfor %}
                </div>
                {% endif %}

                <ul class="findings-list">
                    {% for finding in look.findings %}
                    <li>{{ finding }}</li>
                    {% endfor %}
                </ul>

                {% if look.recommendations %}
                <div class="recommendations">
                    <h4>💡 建议</h4>
                    <ul>
                        {% for rec in look.recommendations %}
                        <li>{{ rec }}</li>
                        {% endfor %}
                    </ul>
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>

        <!-- Three Decisions Section -->
        <div class="section-group">
            <div class="section-group-title">
                <span class="icon">🎯</span>
                三定策略 (Three Decisions Strategy)
            </div>

            {% for decision_key, decision in three_decisions.items() %}
            <div class="section">
                <h3>{{ decision.title }}</h3>

                <div class="summary-box">{{ decision.summary }}</div>

                {% for item in decision.strategy_items %}
                <div class="strategy-item {{ item.priority | lower }}">
                    <div class="name">
                        {{ item.name }}
                        <span class="priority {{ item.priority | lower }}">{{ item.priority }}</span>
                        {% if item.timeline %}<span class="badge">{{ item.timeline }}</span>{% endif %}
                    </div>
                    <div class="desc">{{ item.description }}</div>
                    {% if item.kpis %}
                    <div class="kpis">KPI: {{ item.kpis | join(" | ") }}</div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
            {% endfor %}
        </div>

        <footer>
            BLM Strategic Analysis Tool | Business Leadership Model (业务领先模型)
        </footer>
    </div>
</body>
</html>"""


class BLMReportGenerator:
    """Generate BLM strategic analysis reports."""

    def __init__(self, output_dir: Optional[str] = None):
        if output_dir is None:
            output_dir = str(Path(__file__).resolve().parent.parent.parent / "data" / "output")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_html_report(
        self,
        five_looks: dict[str, InsightResult],
        three_decisions: dict[str, StrategyResult],
        target_operator: str,
        competitors: list[str] = None,
        title: str = "BLM 战略分析报告",
        filename: str = "blm_strategy_report.html",
    ) -> str:
        """Generate an HTML strategic analysis report.

        Args:
            five_looks: Dict of Five Looks analysis results.
            three_decisions: Dict of Three Decisions strategy results.
            target_operator: The operator being analyzed.
            competitors: List of competitor names.
            title: Report title.
            filename: Output filename.

        Returns:
            Path to the generated report.
        """
        # Convert InsightResult and StrategyResult to dicts for template
        five_looks_data = {}
        for key, result in five_looks.items():
            five_looks_data[key] = {
                "category": result.category,
                "title": result.title,
                "findings": result.findings,
                "metrics": result.metrics,
                "recommendations": result.recommendations,
            }

        three_decisions_data = {}
        for key, result in three_decisions.items():
            three_decisions_data[key] = {
                "decision_type": result.decision_type,
                "title": result.title,
                "summary": result.summary,
                "strategy_items": [
                    {
                        "name": item.name,
                        "description": item.description,
                        "priority": item.priority,
                        "category": item.category,
                        "timeline": item.timeline,
                        "kpis": item.kpis,
                    }
                    for item in result.items
                ],
                "metrics": result.metrics,
            }

        template = Template(BLM_HTML_TEMPLATE)
        html = template.render(
            title=title,
            target_operator=target_operator,
            competitors=competitors or [],
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            five_looks=five_looks_data,
            three_decisions=three_decisions_data,
        )

        output_path = self.output_dir / filename
        output_path.write_text(html, encoding="utf-8")
        return str(output_path)

    def generate_text_report(
        self,
        five_looks: dict[str, InsightResult],
        three_decisions: dict[str, StrategyResult],
        target_operator: str,
        competitors: list[str] = None,
        title: str = "BLM Strategic Analysis Report",
        filename: str = "blm_strategy_report.txt",
    ) -> str:
        """Generate a plain text strategic analysis report.

        Args:
            five_looks: Dict of Five Looks analysis results.
            three_decisions: Dict of Three Decisions strategy results.
            target_operator: The operator being analyzed.
            competitors: List of competitor names.
            title: Report title.
            filename: Output filename.

        Returns:
            Path to the generated report.
        """
        lines = [
            "=" * 80,
            title.center(80),
            f"{target_operator} 战略分析报告".center(80),
            "=" * 80,
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"竞争对手: {', '.join(competitors) if competitors else 'N/A'}",
            "",
            "",
        ]

        # Five Looks Section
        lines.append("=" * 80)
        lines.append("  五看分析 (FIVE LOOKS ANALYSIS)")
        lines.append("=" * 80)
        lines.append("")

        for key, result in five_looks.items():
            lines.append("-" * 80)
            lines.append(f"  {result.title}")
            lines.append("-" * 80)
            lines.append("")

            # Metrics
            if result.metrics:
                lines.append("  [关键指标]")
                for mkey, mval in result.metrics.items():
                    lines.append(f"    • {mkey.replace('_', ' ')}: {mval}")
                lines.append("")

            # Findings
            lines.append("  [洞察发现]")
            for finding in result.findings:
                lines.append(f"    • {finding}")
            lines.append("")

            # Recommendations
            if result.recommendations:
                lines.append("  [行动建议]")
                for rec in result.recommendations:
                    lines.append(f"    → {rec}")
                lines.append("")

            lines.append("")

        # Three Decisions Section
        lines.append("=" * 80)
        lines.append("  三定策略 (THREE DECISIONS STRATEGY)")
        lines.append("=" * 80)
        lines.append("")

        for key, result in three_decisions.items():
            lines.append("-" * 80)
            lines.append(f"  {result.title}")
            lines.append("-" * 80)
            lines.append("")

            # Summary
            lines.append("  [策略概要]")
            for line in result.summary.split("\n"):
                lines.append(f"    {line}")
            lines.append("")

            # Strategy items
            lines.append("  [具体举措]")
            for item in result.items:
                lines.append(f"    [{item.priority}] {item.name}")
                lines.append(f"         {item.description}")
                if item.kpis:
                    lines.append(f"         KPI: {', '.join(item.kpis)}")
                lines.append("")

            lines.append("")

        lines.append("=" * 80)
        lines.append("End of Report".center(80))
        lines.append("=" * 80)

        output_path = self.output_dir / filename
        output_path.write_text("\n".join(lines), encoding="utf-8")
        return str(output_path)

    def generate_json_report(
        self,
        five_looks: dict[str, InsightResult],
        three_decisions: dict[str, StrategyResult],
        target_operator: str,
        competitors: list[str] = None,
        title: str = "BLM Strategic Analysis Report",
        filename: str = "blm_strategy_report.json",
    ) -> str:
        """Generate a JSON strategic analysis report.

        Args:
            five_looks: Dict of Five Looks analysis results.
            three_decisions: Dict of Three Decisions strategy results.
            target_operator: The operator being analyzed.
            competitors: List of competitor names.
            title: Report title.
            filename: Output filename.

        Returns:
            Path to the generated report.
        """
        # Convert to serializable format
        five_looks_data = {}
        for key, result in five_looks.items():
            five_looks_data[key] = {
                "category": result.category,
                "title": result.title,
                "findings": result.findings,
                "metrics": result.metrics,
                "recommendations": result.recommendations,
                "data": result.data.to_dict(orient="records") if not result.data.empty else [],
            }

        three_decisions_data = {}
        for key, result in three_decisions.items():
            three_decisions_data[key] = {
                "decision_type": result.decision_type,
                "title": result.title,
                "summary": result.summary,
                "items": [
                    {
                        "name": item.name,
                        "description": item.description,
                        "priority": item.priority,
                        "category": item.category,
                        "timeline": item.timeline,
                        "owner": item.owner,
                        "kpis": item.kpis,
                    }
                    for item in result.items
                ],
                "metrics": result.metrics,
            }

        report_data = {
            "title": title,
            "target_operator": target_operator,
            "competitors": competitors or [],
            "generated_at": datetime.now().isoformat(),
            "five_looks": five_looks_data,
            "three_decisions": three_decisions_data,
        }

        output_path = self.output_dir / filename
        output_path.write_text(
            json.dumps(report_data, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
        return str(output_path)

    def generate_executive_summary(
        self,
        five_looks: dict[str, InsightResult],
        three_decisions: dict[str, StrategyResult],
        target_operator: str,
    ) -> str:
        """Generate a brief executive summary text.

        Args:
            five_looks: Dict of Five Looks analysis results.
            three_decisions: Dict of Three Decisions strategy results.
            target_operator: The operator being analyzed.

        Returns:
            Executive summary text.
        """
        lines = [
            f"【{target_operator} 战略分析执行摘要】",
            "",
            "═══════════════════════════════════════",
            "一、市场态势",
            "═══════════════════════════════════════",
        ]

        # Market insight
        if "market" in five_looks:
            market = five_looks["market"]
            for finding in market.findings[:3]:
                lines.append(f"• {finding}")

        lines.extend([
            "",
            "═══════════════════════════════════════",
            "二、竞争格局",
            "═══════════════════════════════════════",
        ])

        # Self and competitor insights
        if "self" in five_looks:
            self_insight = five_looks["self"]
            for finding in self_insight.findings[:2]:
                lines.append(f"• {finding}")

        if "competitor" in five_looks:
            comp = five_looks["competitor"]
            for finding in comp.findings[:2]:
                lines.append(f"• {finding}")

        lines.extend([
            "",
            "═══════════════════════════════════════",
            "三、战略重点",
            "═══════════════════════════════════════",
        ])

        # Strategy highlights
        if "strategy" in three_decisions:
            strategy = three_decisions["strategy"]
            p0_items = [i for i in strategy.items if i.priority == "P0"]
            for item in p0_items[:2]:
                lines.append(f"【P0】{item.name}: {item.description}")

        lines.extend([
            "",
            "═══════════════════════════════════════",
            "四、关键举措",
            "═══════════════════════════════════════",
        ])

        # Key tasks
        if "key_tasks" in three_decisions:
            tasks = three_decisions["key_tasks"]
            p0_tasks = [i for i in tasks.items if i.priority == "P0"]
            for task in p0_tasks[:3]:
                lines.append(f"• {task.name}")

        return "\n".join(lines)
