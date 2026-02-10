"""Chart generation engine for BLM PPT reports.

Migrated from src/blm/ppt_charts.py with refactoring:
- Uses PPTStyle for all coloring (brand color for protagonist, gray for competitors)
- Adds 6 new chart types: SPAN bubble, Porter five forces, SWOT matrix,
  APPEALS radar, BMC canvas, PEST dashboard

All charts are saved as PNG images that can be embedded in PowerPoint slides.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Optional

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects
import numpy as np

from src.output.ppt_styles import PPTStyle, DEFAULT_STYLE, OPERATOR_BRAND_COLORS


def _rgb_to_hex(rgb_tuple: tuple) -> str:
    """Convert (R, G, B) tuple to '#RRGGBB' hex string."""
    return f'#{rgb_tuple[0]:02X}{rgb_tuple[1]:02X}{rgb_tuple[2]:02X}'


def _rgb_to_mpl(rgb_tuple: tuple) -> tuple:
    """Convert (R, G, B) 0-255 tuple to matplotlib 0-1 tuple."""
    return (rgb_tuple[0] / 255.0, rgb_tuple[1] / 255.0, rgb_tuple[2] / 255.0)


class BLMChartGenerator:
    """Generate charts for BLM PPT presentations.

    All coloring is driven by the PPTStyle: brand color for protagonist,
    gray for competitors, semantic colors for positive/negative.
    """

    def __init__(
        self,
        style: Optional[PPTStyle] = None,
        output_dir: Optional[str] = None,
        dpi: int = 150,
    ):
        if style is None:
            style = DEFAULT_STYLE
        self.style = style
        self.dpi = dpi

        if output_dir:
            self.output_dir = Path(output_dir)
            self.output_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.output_dir = Path(tempfile.mkdtemp())

        self._setup_fonts()

    def _setup_fonts(self):
        """Configure matplotlib font fallback with CJK support."""
        import matplotlib.font_manager as fm
        try:
            fm._load_fontmanager(try_read_cache=False)
        except Exception:
            pass

        chinese_fonts = [
            'WenQuanYi Zen Hei', 'WenQuanYi Micro Hei',
            'Noto Sans CJK SC', 'SimHei', 'Microsoft YaHei',
            'PingFang SC', 'Hiragino Sans GB',
        ]
        available = {f.name for f in fm.fontManager.ttflist}
        selected = next((f for f in chinese_fonts if f in available), None)

        if selected:
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.sans-serif'] = [selected, 'DejaVu Sans', 'Arial']
        else:
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
        plt.rcParams['axes.unicode_minus'] = False

    # --- Color helpers ---

    @property
    def _primary_hex(self) -> str:
        return _rgb_to_hex(self.style.primary_color)

    @property
    def _dark_hex(self) -> str:
        return _rgb_to_hex(self.style.text_color)

    @property
    def _gray_hex(self) -> str:
        return _rgb_to_hex(self.style.light_text_color)

    @property
    def _light_gray_hex(self) -> str:
        return '#E5E5E5'

    @property
    def _positive_hex(self) -> str:
        return _rgb_to_hex(self.style.positive_color)

    @property
    def _negative_hex(self) -> str:
        return _rgb_to_hex(self.style.negative_color)

    @property
    def _warning_hex(self) -> str:
        return _rgb_to_hex(self.style.warning_color)

    def _palette_hex(self, index: int) -> str:
        palette = self.style.chart_palette
        return _rgb_to_hex(palette[index % len(palette)])

    def _brand_color(self, name: str, fallback_idx: int) -> str:
        """Look up operator brand color; fall back to a varied palette index."""
        brand = OPERATOR_BRAND_COLORS.get(name)
        if brand:
            return _rgb_to_hex(brand)
        # Use a varied palette that avoids near-black
        varied = [
            '#4682B4',  # Steel Blue
            '#2E8B57',  # Sea Green
            '#D2691E',  # Chocolate
            '#6A5ACD',  # Slate Blue
            '#20B2AA',  # Light Sea Green
        ]
        return varied[fallback_idx % len(varied)]

    def _color_for_operator(self, operator: str, target: str, idx: int) -> str:
        """Brand color for protagonist, operator brand color for known operators."""
        if operator == target:
            return self._primary_hex
        return self._brand_color(operator, idx)

    def _save_fig(self, fig, filename: str) -> str:
        output_path = self.output_dir / filename
        fig.savefig(output_path, dpi=self.dpi, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close(fig)
        return str(output_path)

    def _style_axes(self, ax):
        """Apply consistent axis styling."""
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(self._light_gray_hex)
        ax.spines['bottom'].set_color(self._light_gray_hex)
        ax.tick_params(colors=self._dark_hex)

    # =========================================================================
    # Migrated chart types (from src/blm/ppt_charts.py)
    # =========================================================================

    def create_bar_chart(
        self,
        categories: list[str],
        values: list[float],
        target_category: str = "",
        title: str = "",
        y_label: str = "",
        filename: str = "bar_chart.png",
    ) -> str:
        """Vertical bar chart with target highlighting."""
        fig, ax = plt.subplots(figsize=(10, 6))
        x_pos = np.arange(len(categories))
        colors = [self._primary_hex if c == target_category
                  else self._brand_color(c, i)
                  for i, c in enumerate(categories)]

        bars = ax.bar(x_pos, values, color=colors, width=0.6, edgecolor='white', linewidth=1)
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(values) * 0.01,
                    f'{val:.1f}', ha='center', va='bottom',
                    fontsize=11, fontweight='bold', color=self._dark_hex)

        ax.set_xticks(x_pos)
        ax.set_xticklabels(categories, fontsize=11, rotation=15, ha='right')
        ax.set_ylabel(y_label, fontsize=12, color=self._dark_hex)
        ax.set_title(title, fontsize=16, fontweight='bold', color=self._dark_hex, pad=15)
        ax.set_ylim(0, max(values) * 1.2 if values else 1)
        ax.yaxis.grid(True, linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)
        self._style_axes(ax)
        plt.tight_layout()
        return self._save_fig(fig, filename)

    def create_horizontal_bar_chart(
        self,
        categories: list[str],
        values: list[float],
        target_category: str = "",
        title: str = "",
        x_label: str = "",
        filename: str = "hbar_chart.png",
        value_suffix: str = "",
    ) -> str:
        """Horizontal bar chart (e.g., market share)."""
        fig, ax = plt.subplots(figsize=(10, 5))

        sorted_data = sorted(zip(categories, values), key=lambda x: x[1], reverse=True)
        cats = [x[0] for x in sorted_data]
        vals = [x[1] for x in sorted_data]

        colors = [self._primary_hex if c == target_category else self._gray_hex for c in cats]
        y_pos = np.arange(len(cats))
        bars = ax.barh(y_pos, vals, color=colors, height=0.6)

        for i, (bar, val) in enumerate(zip(bars, vals)):
            text_color = self._primary_hex if cats[i] == target_category else self._dark_hex
            ax.text(bar.get_width() + max(vals) * 0.01, bar.get_y() + bar.get_height() / 2,
                    f'{val:.1f}{value_suffix}', va='center', fontsize=11,
                    fontweight='bold', color=text_color)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(cats, fontsize=12)
        ax.set_xlabel(x_label, fontsize=12, color=self._dark_hex)
        ax.set_title(title, fontsize=16, fontweight='bold', color=self._dark_hex, pad=15)
        ax.set_xlim(0, max(vals) * 1.2 if vals else 1)
        ax.invert_yaxis()
        self._style_axes(ax)
        plt.tight_layout()
        return self._save_fig(fig, filename)

    def create_radar_chart(
        self,
        dimensions: list[str],
        scores: dict[str, list[float]],
        target_operator: str = "",
        title: str = "",
        filename: str = "radar_chart.png",
    ) -> str:
        """Radar/spider chart for multi-dimensional comparison."""
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

        num_dims = len(dimensions)
        angles = np.linspace(0, 2 * np.pi, num_dims, endpoint=False).tolist()
        angles += angles[:1]

        for i, (operator, operator_scores) in enumerate(scores.items()):
            vals = operator_scores + operator_scores[:1]
            if operator == target_operator:
                color = self._primary_hex
                linewidth, alpha = 3, 0.3
            else:
                color = self._color_for_operator(operator, target_operator, i)
                linewidth, alpha = 2, 0.1
            ax.plot(angles, vals, 'o-', linewidth=linewidth, label=operator, color=color)
            ax.fill(angles, vals, alpha=alpha, color=color)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(dimensions, fontsize=10)
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=8, color=self._gray_hex)
        ax.set_title(title, fontsize=16, fontweight='bold', color=self._dark_hex, pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=10)
        plt.tight_layout()
        return self._save_fig(fig, filename)

    def create_multi_line_trend(
        self,
        x_labels: list[str],
        data_series: dict[str, list[float]],
        title: str = "",
        y_label: str = "",
        target_operator: str = "",
        filename: str = "trend_chart.png",
        y_format: str = "number",
    ) -> str:
        """Multi-line trend chart for quarterly comparison."""
        fig, ax = plt.subplots(figsize=(12, 5))
        x = np.arange(len(x_labels))

        for i, (operator, values) in enumerate(data_series.items()):
            if operator == target_operator:
                color = self._primary_hex
                linewidth, marker, ms, zorder = 3, 'o', 8, 10
            else:
                color = self._color_for_operator(operator, target_operator, i)
                linewidth, marker, ms, zorder = 2, 's', 5, 5

            valid_x = [j for j, v in enumerate(values) if v is not None]
            valid_y = [v for v in values if v is not None]
            ax.plot(valid_x, valid_y, color=color, linewidth=linewidth,
                    marker=marker, markersize=ms, label=operator, zorder=zorder)

        ax.set_xticks(x)
        ax.set_xticklabels(x_labels, fontsize=10)
        ax.set_ylabel(y_label, fontsize=11, color=self._dark_hex)

        if y_format == "percent":
            ax.yaxis.set_major_formatter(plt.FuncFormatter(
                lambda v, _: f'{v:+.1f}%' if v != 0 else '0%'))
        elif y_format == "millions":
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.1f}M'))

        ax.set_title(title, fontsize=14, fontweight='bold', color=self._dark_hex, pad=15)
        ax.grid(True, axis='y', alpha=0.3)
        self._style_axes(ax)
        ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=9)
        plt.tight_layout()
        return self._save_fig(fig, filename)

    def create_stacked_bar(
        self,
        x_labels: list[str],
        segments: dict[str, list[float]],
        title: str = "",
        y_label: str = "",
        filename: str = "stacked_bar.png",
    ) -> str:
        """Stacked bar chart for segment breakdown over time."""
        fig, ax = plt.subplots(figsize=(12, 5))
        x = np.arange(len(x_labels))
        width = 0.6

        bottom = np.zeros(len(x_labels))
        for i, (segment, values) in enumerate(segments.items()):
            ax.bar(x, values, width, bottom=bottom, label=segment,
                   color=self._palette_hex(i), edgecolor='white', linewidth=0.5)
            bottom += np.array(values)

        ax.set_xticks(x)
        ax.set_xticklabels(x_labels, fontsize=10)
        ax.set_ylabel(y_label, fontsize=11, color=self._dark_hex)
        ax.set_title(title, fontsize=14, fontweight='bold', color=self._dark_hex, pad=15)
        ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=9)
        self._style_axes(ax)
        plt.tight_layout()
        return self._save_fig(fig, filename)

    def create_kpi_table_chart(
        self,
        metrics: list[str],
        data: dict[str, list],
        target_operator: str = "",
        title: str = "",
        filename: str = "kpi_table.png",
    ) -> str:
        """Styled table as image for KPI comparison."""
        operators = list(data.keys())
        num_rows = len(metrics)

        fig, ax = plt.subplots(figsize=(12, 0.6 * num_rows + 2))
        ax.axis('off')

        cell_text = [[data[op][i] for op in operators] for i in range(num_rows)]

        col_colors = [self._primary_hex if op == target_operator
                      else self._brand_color(op, i)
                      for i, op in enumerate(operators)]
        table = ax.table(
            cellText=cell_text, rowLabels=metrics, colLabels=operators,
            cellLoc='center', loc='center',
            colColours=col_colors, rowColours=[self._light_gray_hex] * num_rows,
        )
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1.2, 1.8)

        for j in range(len(operators)):
            table[(0, j)].set_text_props(color='white', fontweight='bold')

        target_idx = operators.index(target_operator) if target_operator in operators else -1
        if target_idx >= 0:
            for i in range(num_rows):
                table[(i + 1, target_idx)].set_facecolor('#FFF0F0')

        ax.set_title(title, fontsize=16, fontweight='bold', color=self._dark_hex, pad=20)
        plt.tight_layout()
        return self._save_fig(fig, filename)

    def create_donut_gauges(
        self,
        labels: list[str],
        values: list[float],
        target_label: str = "",
        title: str = "",
        filename: str = "donut_gauges.png",
    ) -> str:
        """Donut gauge chart (e.g., 5G coverage)."""
        n = max(len(labels), 1)
        fig, axes = plt.subplots(1, n, figsize=(4 * n, 4))
        if n == 1:
            axes = [axes]

        for i, (ax, label, val) in enumerate(zip(axes, labels, values)):
            color = self._primary_hex if label == target_label else self._brand_color(label, i)
            sizes = [val, 100 - val]
            ax.pie(sizes, colors=[color, self._light_gray_hex], startangle=90,
                   wedgeprops=dict(width=0.3))
            ax.text(0, 0, f'{val:.0f}%', ha='center', va='center',
                    fontsize=24, fontweight='bold', color=color)
            ax.set_title(label, fontsize=12, fontweight='bold', color=self._dark_hex)

        fig.suptitle(title, fontsize=16, fontweight='bold', color=self._dark_hex, y=1.02)
        plt.tight_layout()
        return self._save_fig(fig, filename)

    def create_gap_analysis_chart(
        self,
        dimensions: list[str],
        target_scores: list[float],
        leader_scores: list[float],
        target_name: str = "",
        leader_name: str = "",
        title: str = "",
        filename: str = "gap_analysis.png",
    ) -> str:
        """Gap analysis chart showing difference from leader."""
        fig, ax = plt.subplots(figsize=(12, 6))
        y_pos = np.arange(len(dimensions))
        gaps = [t - l for t, l in zip(target_scores, leader_scores)]

        colors = [self._negative_hex if g < 0 else self._positive_hex for g in gaps]
        bars = ax.barh(y_pos, gaps, color=colors, height=0.6)

        ax.axvline(x=0, color=self._dark_hex, linewidth=1)
        for bar, gap in zip(bars, gaps):
            x_pos = bar.get_width() + (1 if gap >= 0 else -1)
            ax.text(x_pos, bar.get_y() + bar.get_height() / 2,
                    f'{gap:+.1f}', va='center', ha='left' if gap >= 0 else 'right',
                    fontsize=11, fontweight='bold', color=self._dark_hex)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(dimensions, fontsize=11)
        ax.set_xlabel(f'Gap ({target_name} vs {leader_name})', fontsize=12, color=self._dark_hex)
        ax.set_title(title, fontsize=16, fontweight='bold', color=self._dark_hex, pad=15)
        ax.invert_yaxis()

        ax.legend(
            handles=[mpatches.Patch(color=self._negative_hex, label='Behind'),
                     mpatches.Patch(color=self._positive_hex, label='Ahead')],
            loc='lower right', fontsize=10)
        self._style_axes(ax)
        plt.tight_layout()
        return self._save_fig(fig, filename)

    def create_heatmap(
        self,
        row_labels: list[str],
        col_labels: list[str],
        matrix: list[list[float]],
        title: str = "",
        value_fmt: str = ".1f",
        filename: str = "heatmap.png",
    ) -> str:
        """Heatmap chart (e.g., user flow between operators)."""
        data = np.array(matrix)
        fig, ax = plt.subplots(figsize=(max(8, len(col_labels) * 2), max(5, len(row_labels) * 1.2)))

        cmap = plt.cm.Reds
        im = ax.imshow(data, cmap=cmap, aspect='auto')

        ax.set_xticks(np.arange(len(col_labels)))
        ax.set_yticks(np.arange(len(row_labels)))
        ax.set_xticklabels(col_labels, fontsize=10)
        ax.set_yticklabels(row_labels, fontsize=10)

        max_val = data.max() if data.size > 0 else 1
        for i in range(len(row_labels)):
            for j in range(len(col_labels)):
                val = data[i, j]
                if val > 0:
                    text_color = 'white' if val > max_val * 0.5 else 'black'
                    ax.text(j, i, f'{val:{value_fmt}}', ha='center', va='center',
                            color=text_color, fontsize=10)

        ax.set_title(title, fontsize=14, fontweight='bold', color=self._dark_hex, pad=15)
        plt.colorbar(im, ax=ax, shrink=0.8)
        plt.tight_layout()
        return self._save_fig(fig, filename)

    def create_segment_comparison(
        self,
        x_labels: list[str],
        operator_values: dict[str, list[float]],
        target_operator: str = "",
        title: str = "",
        y_label: str = "",
        filename: str = "segment_comparison.png",
    ) -> str:
        """Grouped bar chart comparing operators across periods."""
        n = len(operator_values)
        # Scale figure width based on data density
        fig_w = max(14, len(x_labels) * n * 0.8 + 4)
        fig, ax = plt.subplots(figsize=(fig_w, 6))
        x = np.arange(len(x_labels))
        width = 0.85 / max(n, 1)

        for i, (operator, values) in enumerate(operator_values.items()):
            offset = (i - n / 2 + 0.5) * width
            color = self._color_for_operator(operator, target_operator, i)
            bars = ax.bar(x + offset, values, width, label=operator, color=color,
                          edgecolor='white', linewidth=0.5)
            # Add value labels on bars
            for bar, val in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(max(v) for v in operator_values.values()) * 0.01,
                        f'{val:.0f}' if val == int(val) else f'{val:.1f}',
                        ha='center', va='bottom', fontsize=8, color=self._dark_hex)

        ax.set_xticks(x)
        ax.set_xticklabels(x_labels, fontsize=12, fontweight='bold')
        ax.set_ylabel(y_label, fontsize=11, color=self._dark_hex)
        ax.set_title(title, fontsize=14, fontweight='bold', color=self._dark_hex, pad=15)
        ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
        ax.set_ylim(0, max(max(v) for v in operator_values.values()) * 1.15)
        ax.grid(True, axis='y', alpha=0.3)
        self._style_axes(ax)
        plt.tight_layout()
        return self._save_fig(fig, filename)

    def create_priority_chart(
        self,
        items: list[str],
        priorities: list[str],
        title: str = "",
        filename: str = "priority_chart.png",
    ) -> str:
        """Strategy priority chart with P0/P1/P2 badges."""
        priority_colors = {
            'P0': self._primary_hex,
            'P1': self._warning_hex,
            'P2': self._positive_hex,
        }
        fig, ax = plt.subplots(figsize=(12, len(items) * 0.8 + 1))
        ax.axis('off')

        for y, (item, priority) in enumerate(zip(items, priorities)):
            color = priority_colors.get(priority, self._gray_hex)
            badge = mpatches.FancyBboxPatch(
                (0.02, y - 0.15), 0.08, 0.3,
                boxstyle="round,pad=0.01", facecolor=color, edgecolor='none')
            ax.add_patch(badge)
            ax.text(0.06, y, priority, ha='center', va='center',
                    fontsize=11, fontweight='bold', color='white')
            ax.text(0.12, y, item, ha='left', va='center',
                    fontsize=12, color=self._dark_hex)
            ax.axhline(y=y - 0.35, xmin=0.02, xmax=0.98,
                       color=self._light_gray_hex, linewidth=0.5)

        ax.set_xlim(0, 1)
        ax.set_ylim(-0.5, len(items) - 0.5)
        ax.set_title(title, fontsize=16, fontweight='bold', color=self._dark_hex,
                     loc='left', x=0.02, pad=15)
        plt.tight_layout()
        return self._save_fig(fig, filename)

    def create_timeline_chart(
        self,
        milestones: list[dict],
        title: str = "",
        filename: str = "timeline.png",
    ) -> str:
        """Timeline chart for execution plan.

        milestones: list of dicts with 'date', 'name', 'priority' keys.
        """
        priority_colors = {
            'P0': self._primary_hex,
            'P1': self._warning_hex,
            'P2': self._positive_hex,
        }
        fig, ax = plt.subplots(figsize=(14, 4))
        ax.axhline(y=0.5, color=self._dark_hex, linewidth=2, zorder=1)

        n = len(milestones)
        for i, ms in enumerate(milestones):
            x = i / (n - 1) if n > 1 else 0.5
            color = priority_colors.get(ms.get('priority', 'P1'), self._gray_hex)
            ax.scatter(x, 0.5, s=200, c=color, zorder=2, edgecolors='white', linewidths=2)
            ax.text(x, 0.7, ms.get('date', ''), ha='center', va='bottom',
                    fontsize=10, color=self._gray_hex)
            ax.text(x, 0.3, ms.get('name', ''), ha='center', va='top',
                    fontsize=10, color=self._dark_hex, fontweight='bold')

        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title(title, fontsize=16, fontweight='bold', color=self._dark_hex, pad=15)
        plt.tight_layout()
        return self._save_fig(fig, filename)

    # =========================================================================
    # New chart types
    # =========================================================================

    def create_span_bubble_chart(
        self,
        positions: list,
        title: str = "SPAN Matrix",
        filename: str = "span_bubble.png",
    ) -> str:
        """SPAN matrix bubble chart.

        positions: list of SPANPosition objects (or dicts with competitive_position,
                   market_attractiveness, bubble_size, opportunity_name, quadrant).
        X = competitive_position (0-10), Y = market_attractiveness (0-10).
        """
        fig, ax = plt.subplots(figsize=(12, 9))

        # Draw quadrant backgrounds
        ax.axhline(y=5, color=self._light_gray_hex, linewidth=1, linestyle='--')
        ax.axvline(x=5, color=self._light_gray_hex, linewidth=1, linestyle='--')

        # Quadrant labels (watermark style)
        quadrant_labels = [
            (2.5, 7.5, "Acquire/Build\nSkills", '#E8F4FD'),
            (7.5, 7.5, "Grow/\nInvest", '#E8F8E8'),
            (2.5, 2.5, "Avoid/\nExit", '#FDE8E8'),
            (7.5, 2.5, "Harvest/\nDivest", '#FFF8E1'),
        ]
        for qx, qy, qlabel, qcolor in quadrant_labels:
            ax.fill_between([qx - 2.5, qx + 2.5], qy - 2.5, qy + 2.5,
                            alpha=0.3, color=qcolor, zorder=0)
            ax.text(qx, qy, qlabel, ha='center', va='center', fontsize=12,
                    color=self._gray_hex, fontstyle='italic', alpha=0.5)

        # Plot bubbles
        quadrant_colors = {
            'grow_invest': self._positive_hex,
            'acquire_skills': '#4682B4',  # Steel Blue
            'harvest': self._warning_hex,
            'avoid_exit': self._negative_hex,
        }

        # Collect all positions for label staggering
        label_data = []
        for pos in positions:
            if hasattr(pos, 'competitive_position'):
                x = pos.competitive_position
                y = pos.market_attractiveness
                size = max(pos.bubble_size, 0.1) * 300
                name = pos.opportunity_name
                quadrant = pos.quadrant
            else:
                x = pos.get('competitive_position', 5)
                y = pos.get('market_attractiveness', 5)
                size = max(pos.get('bubble_size', 1), 0.1) * 300
                name = pos.get('opportunity_name', '')
                quadrant = pos.get('quadrant', '')

            color = quadrant_colors.get(quadrant, self._primary_hex)
            ax.scatter(x, y, s=size, c=color, alpha=0.7, edgecolors='white',
                       linewidths=2, zorder=5)
            label_data.append((x, y, name))

        # Stagger label offsets to reduce overlap
        label_data.sort(key=lambda p: (round(p[1], 1), p[0]))
        used_positions: list[tuple[float, float]] = []
        for x, y, name in label_data:
            # Try multiple offsets to find non-overlapping position
            best_ox, best_oy = 0, 14
            for ox, oy in [(0, 14), (0, -18), (15, 8), (-15, 8),
                           (18, -8), (-18, -8), (0, 22), (0, -26)]:
                candidate = (x + ox * 0.05, y + oy * 0.05)
                overlap = any(abs(candidate[0] - px) < 0.4 and abs(candidate[1] - py) < 0.3
                              for px, py in used_positions)
                if not overlap:
                    best_ox, best_oy = ox, oy
                    break
            used_positions.append((x + best_ox * 0.05, y + best_oy * 0.05))
            ax.annotate(name, (x, y), textcoords="offset points",
                        xytext=(best_ox, best_oy), ha='center', fontsize=7,
                        color=self._dark_hex,
                        arrowprops=dict(arrowstyle='-', color='#AAAAAA',
                                        lw=0.5) if abs(best_ox) > 10 or abs(best_oy) > 18 else None)

        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_xlabel('Competitive Position →', fontsize=12, color=self._dark_hex)
        ax.set_ylabel('Market Attractiveness →', fontsize=12, color=self._dark_hex)
        ax.set_title(title, fontsize=16, fontweight='bold', color=self._dark_hex, pad=15)
        ax.grid(True, alpha=0.2)
        plt.tight_layout()
        return self._save_fig(fig, filename)

    def create_porter_five_forces(
        self,
        forces: dict,
        title: str = "Porter's Five Forces",
        filename: str = "porter_five_forces.png",
    ) -> str:
        """Pentagon/radar chart for Porter's Five Forces.

        forces: dict of {force_name: PorterForce} or {force_name: force_level_str}.
        force_level mapped to score: high=3, medium=2, low=1.
        """
        force_labels = [
            'Existing Competitors',
            'New Entrants',
            'Substitutes',
            'Supplier Power',
            'Buyer Power',
        ]
        force_keys = [
            'existing_competitors', 'new_entrants', 'substitutes',
            'supplier_power', 'buyer_power',
        ]

        level_map = {'high': 3, 'medium': 2, 'low': 1}
        scores = []
        for key in force_keys:
            force = forces.get(key)
            if force is None:
                scores.append(0)
            elif hasattr(force, 'force_level'):
                scores.append(level_map.get(force.force_level, 2))
            elif isinstance(force, str):
                scores.append(level_map.get(force, 2))
            else:
                scores.append(level_map.get(str(force), 2))

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        num = len(force_labels)
        angles = np.linspace(0, 2 * np.pi, num, endpoint=False).tolist()
        angles += angles[:1]
        scores_plot = scores + scores[:1]

        ax.plot(angles, scores_plot, 'o-', linewidth=2.5, color=self._primary_hex, markersize=10)
        ax.fill(angles, scores_plot, alpha=0.25, color=self._primary_hex)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(force_labels, fontsize=11, fontweight='bold')
        ax.set_ylim(0, 3.5)
        ax.set_yticks([1, 2, 3])
        ax.set_yticklabels(['Low', 'Medium', 'High'], fontsize=9, color=self._gray_hex)
        ax.set_title(title, fontsize=16, fontweight='bold', color=self._dark_hex, pad=25)
        plt.tight_layout()
        return self._save_fig(fig, filename)

    def create_swot_matrix(
        self,
        swot,
        title: str = "SWOT Analysis",
        filename: str = "swot_matrix.png",
    ) -> str:
        """2x2 SWOT grid. swot: SWOTAnalysis object or dict with S/W/O/T lists."""
        if hasattr(swot, 'strengths'):
            s = swot.strengths
            w = swot.weaknesses
            o = swot.opportunities
            t = swot.threats
        else:
            s = swot.get('strengths', [])
            w = swot.get('weaknesses', [])
            o = swot.get('opportunities', [])
            t = swot.get('threats', [])

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        quadrants = [
            (axes[0, 0], 'Strengths (S)', s, '#4CAF50', '#E8F5E9'),
            (axes[0, 1], 'Weaknesses (W)', w, '#F44336', '#FFEBEE'),
            (axes[1, 0], 'Opportunities (O)', o, '#2196F3', '#E3F2FD'),
            (axes[1, 1], 'Threats (T)', t, '#FF9800', '#FFF3E0'),
        ]

        for ax, label, items, color, bg_color in quadrants:
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_facecolor(bg_color)
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_color(color)
                spine.set_linewidth(2)

            # Header
            ax.fill_between([0, 1], 0.85, 1.0, color=color, alpha=0.9)
            ax.text(0.5, 0.925, label, ha='center', va='center', fontsize=14,
                    fontweight='bold', color='white')

            # Items
            max_items = min(len(items), 6)
            for i, item in enumerate(items[:max_items]):
                y = 0.78 - i * 0.12
                text = item if len(item) <= 50 else item[:47] + '...'
                ax.text(0.05, y, f'• {text}', ha='left', va='top',
                        fontsize=9, color=self._dark_hex, wrap=True)

        fig.suptitle(title, fontsize=18, fontweight='bold', color=self._dark_hex, y=0.98)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        return self._save_fig(fig, filename)

    def create_appeals_radar(
        self,
        assessments: list,
        target_operator: str = "",
        title: str = "$APPEALS Assessment",
        filename: str = "appeals_radar.png",
    ) -> str:
        """8-axis radar chart for $APPEALS assessment.

        assessments: list of APPEALSAssessment objects.
        Multi-operator overlay with brand color for protagonist.
        """
        if not assessments:
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.text(0.5, 0.5, 'No APPEALS data', ha='center', va='center', fontsize=14)
            ax.axis('off')
            return self._save_fig(fig, filename)

        dimensions = [a.dimension_name if hasattr(a, 'dimension_name') else str(a)
                      for a in assessments]
        our_scores = [a.our_score if hasattr(a, 'our_score') else 0 for a in assessments]

        # Collect all competitors across assessments
        all_competitors = set()
        for a in assessments:
            if hasattr(a, 'competitor_scores') and a.competitor_scores:
                all_competitors.update(a.competitor_scores.keys())

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        num = len(dimensions)
        angles = np.linspace(0, 2 * np.pi, num, endpoint=False).tolist()
        angles += angles[:1]

        # Plot protagonist
        vals = our_scores + our_scores[:1]
        ax.plot(angles, vals, 'o-', linewidth=3, label=target_operator or 'Us',
                color=self._primary_hex, markersize=8)
        ax.fill(angles, vals, alpha=0.25, color=self._primary_hex)

        # Plot competitors
        for ci, comp in enumerate(sorted(all_competitors)):
            comp_scores = []
            for a in assessments:
                scores_dict = a.competitor_scores if hasattr(a, 'competitor_scores') else {}
                comp_scores.append(scores_dict.get(comp, 0))
            comp_vals = comp_scores + comp_scores[:1]
            color = self._color_for_operator(comp, target_operator, ci)
            ax.plot(angles, comp_vals, 's-', linewidth=1.5, label=comp,
                    color=color, markersize=5, alpha=0.7)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(dimensions, fontsize=10, fontweight='bold')
        ax.set_ylim(0, 5.5)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=8, color=self._gray_hex)
        ax.set_title(title, fontsize=16, fontweight='bold', color=self._dark_hex, pad=25)
        ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.0), fontsize=9)
        plt.tight_layout()
        return self._save_fig(fig, filename)

    def create_bmc_canvas(
        self,
        bmc,
        title: str = "Business Model Canvas",
        filename: str = "bmc_canvas.png",
    ) -> str:
        """9-box Business Model Canvas layout.

        bmc: BMCCanvas object or dict with 9 keys.
        """
        if hasattr(bmc, 'key_partners'):
            blocks = {
                'Key Partners': bmc.key_partners,
                'Key Activities': bmc.key_activities,
                'Key Resources': bmc.key_resources,
                'Value Propositions': bmc.value_propositions,
                'Customer Relationships': bmc.customer_relationships,
                'Channels': bmc.channels,
                'Customer Segments': bmc.customer_segments,
                'Cost Structure': bmc.cost_structure,
                'Revenue Streams': bmc.revenue_streams,
            }
        else:
            blocks = bmc

        fig = plt.figure(figsize=(16, 10))

        # BMC layout: 5 cols x 4 rows conceptually
        # Row 0-1: KP | KA | VP | CR | CS
        #          KP | KR | VP | CH | CS
        # Row 2-3: Cost Structure       | Revenue Streams
        positions = [
            ('Key Partners', 0, 0, 1, 2),
            ('Key Activities', 1, 0, 1, 1),
            ('Key Resources', 1, 1, 1, 1),
            ('Value Propositions', 2, 0, 1, 2),
            ('Customer Relationships', 3, 0, 1, 1),
            ('Channels', 3, 1, 1, 1),
            ('Customer Segments', 4, 0, 1, 2),
            ('Cost Structure', 0, 2, 2.5, 1),
            ('Revenue Streams', 2.5, 2, 2.5, 1),
        ]

        block_colors = {
            'Key Partners': '#E3F2FD',
            'Key Activities': '#F3E5F5',
            'Key Resources': '#FFF3E0',
            'Value Propositions': '#E8F5E9',
            'Customer Relationships': '#FCE4EC',
            'Channels': '#E0F7FA',
            'Customer Segments': '#FFF9C4',
            'Cost Structure': '#EFEBE9',
            'Revenue Streams': '#F1F8E9',
        }

        for name, col, row, w, h in positions:
            items = blocks.get(name, [])
            ax = fig.add_axes([col / 5.0 + 0.01, 1.0 - (row + h) / 3.0 + 0.01,
                               w / 5.0 - 0.02, h / 3.0 - 0.02])
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_facecolor(block_colors.get(name, '#F5F5F5'))
            ax.set_xticks([])
            ax.set_yticks([])

            # Header
            ax.text(0.05, 0.92, name, fontsize=9, fontweight='bold',
                    color=self._primary_hex, va='top')

            # Items
            max_items = min(len(items), 4)
            for i, item in enumerate(items[:max_items]):
                text = item if len(item) <= 35 else item[:32] + '...'
                ax.text(0.05, 0.75 - i * 0.18, f'• {text}', fontsize=7,
                        color=self._dark_hex, va='top')

        fig.suptitle(title, fontsize=16, fontweight='bold', color=self._dark_hex, y=0.99)
        return self._save_fig(fig, filename)

    def create_pest_dashboard(
        self,
        pest,
        title: str = "PEST Analysis Dashboard",
        filename: str = "pest_dashboard.png",
    ) -> str:
        """4-quadrant PEST dashboard with color-coded factors.

        pest: PESTAnalysis object or dict with P/E/S/T factor lists.
        """
        if hasattr(pest, 'political_factors'):
            quadrants_data = [
                ('Political', pest.political_factors, '#1565C0', '#E3F2FD'),
                ('Economic', pest.economic_factors, '#2E7D32', '#E8F5E9'),
                ('Society', pest.society_factors, '#E65100', '#FFF3E0'),
                ('Technology', pest.technology_factors, '#6A1B9A', '#F3E5F5'),
            ]
        else:
            quadrants_data = [
                ('Political', pest.get('political_factors', []), '#1565C0', '#E3F2FD'),
                ('Economic', pest.get('economic_factors', []), '#2E7D32', '#E8F5E9'),
                ('Society', pest.get('society_factors', []), '#E65100', '#FFF3E0'),
                ('Technology', pest.get('technology_factors', []), '#6A1B9A', '#F3E5F5'),
            ]

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        impact_icons = {
            'opportunity': '▲',
            'threat': '▼',
            'neutral': '●',
            'both': '◆',
        }

        for ax, (dim_name, factors, color, bg) in zip(axes.flat, quadrants_data):
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_facecolor(bg)
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_color(color)
                spine.set_linewidth(2)

            # Header
            ax.fill_between([0, 1], 0.88, 1.0, color=color, alpha=0.9)
            ax.text(0.5, 0.94, dim_name, ha='center', va='center', fontsize=14,
                    fontweight='bold', color='white')

            # Factors
            max_factors = min(len(factors), 5)
            for i, factor in enumerate(factors[:max_factors]):
                y = 0.82 - i * 0.15
                if hasattr(factor, 'factor_name'):
                    name = factor.factor_name
                    impact = getattr(factor, 'impact_type', 'neutral')
                    severity = getattr(factor, 'severity', 'medium')
                elif isinstance(factor, dict):
                    name = factor.get('factor_name', str(factor))
                    impact = factor.get('impact_type', 'neutral')
                    severity = factor.get('severity', 'medium')
                else:
                    name = str(factor)
                    impact = 'neutral'
                    severity = 'medium'

                icon = impact_icons.get(impact, '●')
                severity_colors = {'high': '#C62828', 'medium': '#F57F17', 'low': '#2E7D32'}
                sev_color = severity_colors.get(severity, self._gray_hex)

                text = name if len(name) <= 45 else name[:42] + '...'
                ax.text(0.05, y, f'{icon} {text}', ha='left', va='top',
                        fontsize=9, color=self._dark_hex)

        fig.suptitle(title, fontsize=18, fontweight='bold', color=self._dark_hex, y=0.98)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        return self._save_fig(fig, filename)
