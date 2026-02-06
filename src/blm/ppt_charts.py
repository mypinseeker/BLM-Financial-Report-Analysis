"""Chart generation utilities for BLM PPT.

Creates charts as images that can be embedded in PowerPoint presentations.
Uses matplotlib for chart generation.
"""

import io
from pathlib import Path
from typing import Optional
import tempfile

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Huawei color scheme
HUAWEI_RED = '#C7000B'
HUAWEI_DARK = '#333333'
HUAWEI_GRAY = '#666666'
HUAWEI_LIGHT_GRAY = '#E5E5E5'

# Color palette for multiple series
CHART_COLORS = [
    '#C7000B',  # Huawei Red (primary)
    '#2E5A8B',  # Blue
    '#4A9D4A',  # Green
    '#F5A623',  # Orange
    '#9B59B6',  # Purple
    '#3498DB',  # Light Blue
]


class PPTChartGenerator:
    """Generate charts for PPT presentations."""

    def __init__(self, output_dir: Optional[str] = None, dpi: int = 150):
        """Initialize chart generator.

        Args:
            output_dir: Directory to save chart images
            dpi: Resolution for chart images
        """
        if output_dir:
            self.output_dir = Path(output_dir)
            self.output_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.output_dir = Path(tempfile.mkdtemp())
        self.dpi = dpi

        # Set matplotlib style with CJK font support
        self._setup_chinese_fonts()

    def _setup_chinese_fonts(self):
        """Configure matplotlib to use Chinese fonts properly."""
        import matplotlib.font_manager as fm

        # Clear font cache to pick up newly installed fonts
        fm._load_fontmanager(try_read_cache=False)

        # Priority list of Chinese fonts
        chinese_fonts = [
            'WenQuanYi Zen Hei',      # Available on this system
            'WenQuanYi Micro Hei',    # Open source CJK font
            'Noto Sans CJK SC',       # Google Noto fonts
            'SimHei',                 # Windows Chinese font
            'Microsoft YaHei',        # Windows Chinese font
            'PingFang SC',            # macOS Chinese font
            'Hiragino Sans GB',       # macOS Chinese font
            'Arial Unicode MS',       # Unicode font
        ]

        # Find available Chinese font
        available_fonts = [f.name for f in fm.fontManager.ttflist]
        selected_font = None

        for font in chinese_fonts:
            if font in available_fonts:
                selected_font = font
                break

        if selected_font:
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.sans-serif'] = [selected_font, 'DejaVu Sans', 'Arial']
        else:
            # Fallback: try to use any available font
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

        plt.rcParams['axes.unicode_minus'] = False

    def create_market_share_bar_chart(
        self,
        operators: list[str],
        market_shares: list[float],
        target_operator: str,
        title: str = "市场份额对比",
        filename: str = "market_share.png",
    ) -> str:
        """Create horizontal bar chart for market share comparison.

        Args:
            operators: List of operator names
            market_shares: List of market share percentages
            target_operator: Name of target operator (highlighted)
            title: Chart title
            filename: Output filename

        Returns:
            Path to generated chart image
        """
        fig, ax = plt.subplots(figsize=(10, 5))

        # Sort by market share
        sorted_data = sorted(zip(operators, market_shares), key=lambda x: x[1], reverse=True)
        operators = [x[0] for x in sorted_data]
        market_shares = [x[1] for x in sorted_data]

        # Create colors (highlight target)
        colors = []
        for op in operators:
            if op == target_operator:
                colors.append(HUAWEI_RED)
            else:
                colors.append(HUAWEI_GRAY)

        y_pos = np.arange(len(operators))
        bars = ax.barh(y_pos, market_shares, color=colors, height=0.6)

        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, market_shares)):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                   f'{value:.1f}%', va='center', fontsize=11, fontweight='bold',
                   color=HUAWEI_RED if operators[i] == target_operator else HUAWEI_DARK)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(operators, fontsize=12)
        ax.set_xlabel('市场份额 (%)', fontsize=12, color=HUAWEI_DARK)
        ax.set_title(title, fontsize=16, fontweight='bold', color=HUAWEI_DARK, pad=15)
        ax.set_xlim(0, max(market_shares) * 1.2)
        ax.invert_yaxis()

        # Style
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(HUAWEI_LIGHT_GRAY)
        ax.spines['bottom'].set_color(HUAWEI_LIGHT_GRAY)
        ax.tick_params(colors=HUAWEI_DARK)

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        return str(output_path)

    def create_revenue_comparison_chart(
        self,
        operators: list[str],
        revenues: list[float],
        target_operator: str,
        title: str = "收入规模对比 (€B)",
        filename: str = "revenue_comparison.png",
    ) -> str:
        """Create vertical bar chart for revenue comparison.

        Args:
            operators: List of operator names
            revenues: List of revenue values (in billions)
            target_operator: Name of target operator
            title: Chart title
            filename: Output filename

        Returns:
            Path to generated chart image
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        x_pos = np.arange(len(operators))
        colors = [HUAWEI_RED if op == target_operator else '#5B9BD5' for op in operators]

        bars = ax.bar(x_pos, revenues, color=colors, width=0.6, edgecolor='white', linewidth=1)

        # Add value labels on top
        for bar, value in zip(bars, revenues):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                   f'€{value:.1f}B', ha='center', va='bottom',
                   fontsize=12, fontweight='bold', color=HUAWEI_DARK)

        ax.set_xticks(x_pos)
        ax.set_xticklabels(operators, fontsize=11, rotation=15, ha='right')
        ax.set_ylabel('收入 (€ Billion)', fontsize=12, color=HUAWEI_DARK)
        ax.set_title(title, fontsize=16, fontweight='bold', color=HUAWEI_DARK, pad=15)
        ax.set_ylim(0, max(revenues) * 1.2)

        # Grid
        ax.yaxis.grid(True, linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)

        # Style
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(HUAWEI_LIGHT_GRAY)
        ax.spines['bottom'].set_color(HUAWEI_LIGHT_GRAY)

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        return str(output_path)

    def create_competitive_radar_chart(
        self,
        dimensions: list[str],
        scores: dict[str, list[float]],
        target_operator: str,
        title: str = "竞争力雷达图",
        filename: str = "competitive_radar.png",
    ) -> str:
        """Create radar/spider chart for competitive analysis.

        Args:
            dimensions: List of competitive dimensions
            scores: Dict mapping operator names to list of scores
            target_operator: Name of target operator
            title: Chart title
            filename: Output filename

        Returns:
            Path to generated chart image
        """
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

        # Number of dimensions
        num_dims = len(dimensions)
        angles = np.linspace(0, 2 * np.pi, num_dims, endpoint=False).tolist()
        angles += angles[:1]  # Complete the loop

        # Plot each operator
        color_idx = 0
        for operator, operator_scores in scores.items():
            values = operator_scores + operator_scores[:1]  # Complete the loop

            if operator == target_operator:
                color = HUAWEI_RED
                linewidth = 3
                alpha = 0.3
            else:
                color = CHART_COLORS[color_idx % len(CHART_COLORS)]
                if color == HUAWEI_RED:
                    color_idx += 1
                    color = CHART_COLORS[color_idx % len(CHART_COLORS)]
                linewidth = 2
                alpha = 0.1
                color_idx += 1

            ax.plot(angles, values, 'o-', linewidth=linewidth, label=operator, color=color)
            ax.fill(angles, values, alpha=alpha, color=color)

        # Set dimension labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(dimensions, fontsize=10)

        # Set radial limits
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=8, color=HUAWEI_GRAY)

        ax.set_title(title, fontsize=16, fontweight='bold', color=HUAWEI_DARK, pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=10)

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        return str(output_path)

    def create_kpi_comparison_table_chart(
        self,
        metrics: list[str],
        data: dict[str, list],
        target_operator: str,
        title: str = "关键指标对比",
        filename: str = "kpi_comparison.png",
    ) -> str:
        """Create a styled table as an image for KPI comparison.

        Args:
            metrics: List of metric names (rows)
            data: Dict mapping operator names to list of values
            target_operator: Name of target operator
            title: Chart title
            filename: Output filename

        Returns:
            Path to generated chart image
        """
        operators = list(data.keys())
        num_rows = len(metrics)
        num_cols = len(operators)

        fig, ax = plt.subplots(figsize=(12, 0.6 * num_rows + 2))
        ax.axis('off')

        # Create table data
        cell_text = []
        for i, metric in enumerate(metrics):
            row = [data[op][i] for op in operators]
            cell_text.append(row)

        # Create table
        table = ax.table(
            cellText=cell_text,
            rowLabels=metrics,
            colLabels=operators,
            cellLoc='center',
            loc='center',
            colColours=[HUAWEI_RED if op == target_operator else '#5B9BD5' for op in operators],
            rowColours=[HUAWEI_LIGHT_GRAY] * num_rows,
        )

        # Style table
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1.2, 1.8)

        # Color header text white
        for j, op in enumerate(operators):
            cell = table[(0, j)]
            cell.set_text_props(color='white', fontweight='bold')

        # Highlight target operator column
        target_idx = operators.index(target_operator) if target_operator in operators else -1
        if target_idx >= 0:
            for i in range(num_rows):
                cell = table[(i + 1, target_idx)]
                cell.set_facecolor('#FFF0F0')

        ax.set_title(title, fontsize=16, fontweight='bold', color=HUAWEI_DARK, pad=20)

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        return str(output_path)

    def create_5g_coverage_comparison(
        self,
        operators: list[str],
        coverage_pct: list[float],
        target_operator: str,
        title: str = "5G 网络覆盖率对比",
        filename: str = "5g_coverage.png",
    ) -> str:
        """Create gauge/progress style chart for 5G coverage comparison.

        Args:
            operators: List of operator names
            coverage_pct: List of coverage percentages
            target_operator: Name of target operator
            title: Chart title
            filename: Output filename

        Returns:
            Path to generated chart image
        """
        fig, axes = plt.subplots(1, len(operators), figsize=(4 * len(operators), 4))
        if len(operators) == 1:
            axes = [axes]

        for ax, operator, coverage in zip(axes, operators, coverage_pct):
            # Create donut chart
            colors = [HUAWEI_RED if operator == target_operator else '#5B9BD5',
                     HUAWEI_LIGHT_GRAY]
            sizes = [coverage, 100 - coverage]

            wedges, _ = ax.pie(sizes, colors=colors, startangle=90,
                              wedgeprops=dict(width=0.3))

            # Add center text
            ax.text(0, 0, f'{coverage:.0f}%', ha='center', va='center',
                   fontsize=24, fontweight='bold',
                   color=HUAWEI_RED if operator == target_operator else HUAWEI_DARK)

            ax.set_title(operator, fontsize=12, fontweight='bold', color=HUAWEI_DARK)

        fig.suptitle(title, fontsize=16, fontweight='bold', color=HUAWEI_DARK, y=1.02)

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        return str(output_path)

    def create_financial_metrics_chart(
        self,
        operators: list[str],
        metrics_data: dict[str, dict],
        target_operator: str,
        title: str = "财务指标对比",
        filename: str = "financial_metrics.png",
    ) -> str:
        """Create multi-metric grouped bar chart.

        Args:
            operators: List of operator names
            metrics_data: Dict with structure {metric_name: {operator: value}}
            target_operator: Name of target operator
            title: Chart title
            filename: Output filename

        Returns:
            Path to generated chart image
        """
        metrics = list(metrics_data.keys())
        x = np.arange(len(metrics))
        width = 0.8 / len(operators)

        fig, ax = plt.subplots(figsize=(12, 6))

        for i, operator in enumerate(operators):
            values = [metrics_data[m].get(operator, 0) for m in metrics]
            offset = (i - len(operators)/2 + 0.5) * width

            color = HUAWEI_RED if operator == target_operator else CHART_COLORS[(i+1) % len(CHART_COLORS)]
            bars = ax.bar(x + offset, values, width * 0.9, label=operator, color=color)

            # Add value labels
            for bar, val in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                       f'{val:.1f}', ha='center', va='bottom', fontsize=9,
                       color=HUAWEI_DARK, fontweight='bold')

        ax.set_ylabel('Value', fontsize=12, color=HUAWEI_DARK)
        ax.set_title(title, fontsize=16, fontweight='bold', color=HUAWEI_DARK, pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(metrics, fontsize=11)
        ax.legend(loc='upper right', fontsize=10)

        # Grid
        ax.yaxis.grid(True, linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)

        # Style
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        return str(output_path)

    def create_gap_analysis_chart(
        self,
        dimensions: list[str],
        target_scores: list[float],
        leader_scores: list[float],
        target_name: str,
        leader_name: str,
        title: str = "差距分析",
        filename: str = "gap_analysis.png",
    ) -> str:
        """Create gap analysis chart showing difference from leader.

        Args:
            dimensions: List of dimension names
            target_scores: Scores for target operator
            leader_scores: Scores for market leader
            target_name: Name of target operator
            leader_name: Name of market leader
            title: Chart title
            filename: Output filename

        Returns:
            Path to generated chart image
        """
        fig, ax = plt.subplots(figsize=(12, 6))

        y_pos = np.arange(len(dimensions))
        gaps = [t - l for t, l in zip(target_scores, leader_scores)]

        # Color bars based on positive/negative gap
        colors = [HUAWEI_RED if g < 0 else '#4CAF50' for g in gaps]

        bars = ax.barh(y_pos, gaps, color=colors, height=0.6)

        # Add reference line at 0
        ax.axvline(x=0, color=HUAWEI_DARK, linewidth=1)

        # Add value labels
        for bar, gap in zip(bars, gaps):
            x_pos = bar.get_width() + (1 if gap >= 0 else -1)
            ax.text(x_pos, bar.get_y() + bar.get_height()/2,
                   f'{gap:+.1f}', va='center', ha='left' if gap >= 0 else 'right',
                   fontsize=11, fontweight='bold', color=HUAWEI_DARK)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(dimensions, fontsize=11)
        ax.set_xlabel(f'差距 ({target_name} vs {leader_name})', fontsize=12, color=HUAWEI_DARK)
        ax.set_title(title, fontsize=16, fontweight='bold', color=HUAWEI_DARK, pad=15)
        ax.invert_yaxis()

        # Legend
        red_patch = mpatches.Patch(color=HUAWEI_RED, label='落后')
        green_patch = mpatches.Patch(color='#4CAF50', label='领先')
        ax.legend(handles=[red_patch, green_patch], loc='lower right', fontsize=10)

        # Style
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(HUAWEI_LIGHT_GRAY)

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        return str(output_path)

    def create_strategy_priority_chart(
        self,
        strategies: list[str],
        priorities: list[str],
        title: str = "战略优先级矩阵",
        filename: str = "strategy_priority.png",
    ) -> str:
        """Create visual priority chart for strategies.

        Args:
            strategies: List of strategy names
            priorities: List of priority levels (P0, P1, P2)
            title: Chart title
            filename: Output filename

        Returns:
            Path to generated chart image
        """
        fig, ax = plt.subplots(figsize=(12, len(strategies) * 0.8 + 1))
        ax.axis('off')

        priority_colors = {
            'P0': HUAWEI_RED,
            'P1': '#F5A623',
            'P2': '#4CAF50',
        }

        y_positions = range(len(strategies) - 1, -1, -1)

        for y, (strategy, priority) in enumerate(zip(strategies, priorities)):
            # Priority badge
            color = priority_colors.get(priority, HUAWEI_GRAY)
            badge = mpatches.FancyBboxPatch(
                (0.02, y - 0.15), 0.08, 0.3,
                boxstyle="round,pad=0.01",
                facecolor=color, edgecolor='none'
            )
            ax.add_patch(badge)
            ax.text(0.06, y, priority, ha='center', va='center',
                   fontsize=11, fontweight='bold', color='white')

            # Strategy text
            ax.text(0.12, y, strategy, ha='left', va='center',
                   fontsize=12, color=HUAWEI_DARK)

            # Underline
            ax.axhline(y=y - 0.35, xmin=0.02, xmax=0.98,
                      color=HUAWEI_LIGHT_GRAY, linewidth=0.5)

        ax.set_xlim(0, 1)
        ax.set_ylim(-0.5, len(strategies) - 0.5)
        ax.set_title(title, fontsize=16, fontweight='bold', color=HUAWEI_DARK,
                    loc='left', x=0.02, pad=15)

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        return str(output_path)

    def create_timeline_chart(
        self,
        milestones: list[dict],
        title: str = "执行时间线",
        filename: str = "timeline.png",
    ) -> str:
        """Create timeline chart for execution plan.

        Args:
            milestones: List of dicts with 'date', 'name', 'priority' keys
            title: Chart title
            filename: Output filename

        Returns:
            Path to generated chart image
        """
        fig, ax = plt.subplots(figsize=(14, 4))

        # Timeline base
        ax.axhline(y=0.5, color=HUAWEI_DARK, linewidth=2, zorder=1)

        priority_colors = {
            'P0': HUAWEI_RED,
            'P1': '#F5A623',
            'P2': '#4CAF50',
        }

        for i, milestone in enumerate(milestones):
            x = i / (len(milestones) - 1) if len(milestones) > 1 else 0.5
            color = priority_colors.get(milestone.get('priority', 'P1'), HUAWEI_GRAY)

            # Marker
            ax.scatter(x, 0.5, s=200, c=color, zorder=2, edgecolors='white', linewidths=2)

            # Date label (above)
            ax.text(x, 0.7, milestone.get('date', ''),
                   ha='center', va='bottom', fontsize=10, color=HUAWEI_GRAY)

            # Name label (below)
            ax.text(x, 0.3, milestone.get('name', ''),
                   ha='center', va='top', fontsize=10, color=HUAWEI_DARK,
                   fontweight='bold', wrap=True)

        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title(title, fontsize=16, fontweight='bold', color=HUAWEI_DARK, pad=15)

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        return str(output_path)

    def create_multi_line_trend_chart(
        self,
        quarters: list[str],
        data_series: dict[str, list[float]],
        title: str,
        y_label: str = "",
        target_operator: str = None,
        filename: str = "trend_chart.png",
        show_legend: bool = True,
        y_format: str = "number",  # "number", "percent", "millions"
    ) -> str:
        """Create multi-line trend chart for quarterly comparison.

        Args:
            quarters: List of quarter labels (e.g., ["Q1 FY25", "Q2 FY25", ...])
            data_series: Dict of {operator_name: [values...]}
            title: Chart title
            y_label: Y-axis label
            target_operator: Name of target operator (highlighted)
            filename: Output filename
            show_legend: Whether to show legend
            y_format: Format for y-axis values

        Returns:
            Path to generated chart image
        """
        fig, ax = plt.subplots(figsize=(12, 5))

        x = np.arange(len(quarters))

        for i, (operator, values) in enumerate(data_series.items()):
            # Highlight target operator
            if operator == target_operator:
                color = HUAWEI_RED
                linewidth = 3
                marker = 'o'
                markersize = 8
                zorder = 10
            else:
                color = CHART_COLORS[i % len(CHART_COLORS)]
                linewidth = 2
                marker = 's'
                markersize = 5
                zorder = 5

            # Handle None/missing values
            valid_x = []
            valid_y = []
            for j, v in enumerate(values):
                if v is not None:
                    valid_x.append(j)
                    valid_y.append(v)

            ax.plot(valid_x, valid_y, color=color, linewidth=linewidth,
                   marker=marker, markersize=markersize, label=operator, zorder=zorder)

        ax.set_xticks(x)
        ax.set_xticklabels(quarters, fontsize=10)
        ax.set_ylabel(y_label, fontsize=11, color=HUAWEI_DARK)

        # Format y-axis
        if y_format == "percent":
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:+.1f}%' if v != 0 else '0%'))
        elif y_format == "millions":
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.1f}M'))

        ax.set_title(title, fontsize=14, fontweight='bold', color=HUAWEI_DARK, pad=15)
        ax.grid(True, axis='y', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        if show_legend:
            ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=9)

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        return str(output_path)

    def create_stacked_bar_trend_chart(
        self,
        quarters: list[str],
        segments: dict[str, list[float]],
        title: str,
        y_label: str = "",
        filename: str = "stacked_trend.png",
        colors: list[str] = None,
    ) -> str:
        """Create stacked bar chart for segment breakdown over time.

        Args:
            quarters: List of quarter labels
            segments: Dict of {segment_name: [values...]}
            title: Chart title
            y_label: Y-axis label
            filename: Output filename
            colors: Custom colors for segments

        Returns:
            Path to generated chart image
        """
        fig, ax = plt.subplots(figsize=(12, 5))

        x = np.arange(len(quarters))
        width = 0.6

        if colors is None:
            colors = CHART_COLORS

        bottom = np.zeros(len(quarters))
        for i, (segment, values) in enumerate(segments.items()):
            ax.bar(x, values, width, bottom=bottom, label=segment,
                  color=colors[i % len(colors)], edgecolor='white', linewidth=0.5)
            bottom += np.array(values)

        ax.set_xticks(x)
        ax.set_xticklabels(quarters, fontsize=10)
        ax.set_ylabel(y_label, fontsize=11, color=HUAWEI_DARK)
        ax.set_title(title, fontsize=14, fontweight='bold', color=HUAWEI_DARK, pad=15)

        ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=9)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        return str(output_path)

    def create_user_flow_sankey_simple(
        self,
        flow_data: dict[str, int],
        operators: list[str],
        title: str = "User Flow Analysis",
        filename: str = "user_flow.png",
    ) -> str:
        """Create simplified user flow visualization.

        Args:
            flow_data: Dict with flow keys like "from_vodafone_to_dt": value
            operators: List of operator names
            title: Chart title
            filename: Output filename

        Returns:
            Path to generated chart image
        """
        fig, ax = plt.subplots(figsize=(12, 6))

        # Create a matrix visualization
        n = len(operators)
        matrix = np.zeros((n, n))

        op_map = {
            "vodafone": 0, "dt": 1, "o2": 2, "1and1": 3,
            "Vodafone Germany": 0, "Deutsche Telekom": 1,
            "Telefónica O2 Germany": 2, "1&1 AG": 3
        }

        for key, value in flow_data.items():
            parts = key.replace("from_", "").split("_to_")
            if len(parts) == 2:
                src = op_map.get(parts[0], -1)
                dst = op_map.get(parts[1], -1)
                if src >= 0 and dst >= 0:
                    matrix[src, dst] = value

        # Plot as heatmap
        cmap = plt.cm.Reds
        im = ax.imshow(matrix, cmap=cmap, aspect='auto')

        ax.set_xticks(np.arange(n))
        ax.set_yticks(np.arange(n))
        short_names = ["Vodafone", "DT", "O2", "1&1"]
        ax.set_xticklabels(short_names, fontsize=10)
        ax.set_yticklabels(short_names, fontsize=10)

        ax.set_xlabel("To", fontsize=11, color=HUAWEI_DARK)
        ax.set_ylabel("From", fontsize=11, color=HUAWEI_DARK)

        # Add values in cells
        for i in range(n):
            for j in range(n):
                if i != j and matrix[i, j] > 0:
                    text_color = 'white' if matrix[i, j] > matrix.max() * 0.5 else 'black'
                    ax.text(j, i, f'{int(matrix[i, j])}K',
                           ha='center', va='center', color=text_color, fontsize=10)

        ax.set_title(title, fontsize=14, fontweight='bold', color=HUAWEI_DARK, pad=15)

        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Users (K)', fontsize=10)

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        return str(output_path)

    def create_segment_comparison_chart(
        self,
        quarters: list[str],
        operators_data: dict[str, dict[str, list[float]]],
        segment: str,
        title: str,
        y_label: str = "",
        target_operator: str = None,
        filename: str = "segment_comparison.png",
    ) -> str:
        """Create grouped bar chart comparing segment performance across operators.

        Args:
            quarters: List of quarter labels
            operators_data: Dict of {operator: {metric: [values...]}}
            segment: Segment key to compare (e.g., "mobile_service_revenue")
            title: Chart title
            y_label: Y-axis label
            target_operator: Target operator to highlight
            filename: Output filename

        Returns:
            Path to generated chart image
        """
        fig, ax = plt.subplots(figsize=(14, 5))

        x = np.arange(len(quarters))
        n_operators = len(operators_data)
        width = 0.8 / n_operators

        for i, (operator, data) in enumerate(operators_data.items()):
            values = data.get(segment, [0] * len(quarters))
            offset = (i - n_operators / 2 + 0.5) * width

            if operator == target_operator:
                color = HUAWEI_RED
                edgecolor = 'darkred'
            else:
                color = CHART_COLORS[i % len(CHART_COLORS)]
                edgecolor = 'none'

            bars = ax.bar(x + offset, values, width, label=operator,
                         color=color, edgecolor=edgecolor, linewidth=1.5)

        ax.set_xticks(x)
        ax.set_xticklabels(quarters, fontsize=10)
        ax.set_ylabel(y_label, fontsize=11, color=HUAWEI_DARK)
        ax.set_title(title, fontsize=14, fontweight='bold', color=HUAWEI_DARK, pad=15)

        ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=9)
        ax.grid(True, axis='y', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        return str(output_path)
