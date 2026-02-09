"""Visualization module for BLM financial report analysis.

Generates charts and plots for financial data using matplotlib and seaborn.
"""

from pathlib import Path
from typing import Optional

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server/CLI use
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd


class FinancialChartGenerator:
    """Generate financial charts and visualizations."""

    DEFAULT_FIGSIZE = (12, 6)
    DEFAULT_STYLE = "seaborn-v0_8-whitegrid"
    COLOR_PALETTE = "viridis"

    def __init__(self, output_dir: Optional[str] = None, style: Optional[str] = None):
        if output_dir is None:
            output_dir = str(Path(__file__).resolve().parent.parent.parent / "data" / "output")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.style = style or self.DEFAULT_STYLE

    def _setup_plot(self, figsize=None, title: str = ""):
        """Set up a new figure with consistent styling."""
        try:
            plt.style.use(self.style)
        except OSError:
            plt.style.use("ggplot")
        fig, ax = plt.subplots(figsize=figsize or self.DEFAULT_FIGSIZE)
        if title:
            ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
        return fig, ax

    def _save_and_close(self, fig, filename: str) -> str:
        """Save figure and return the output path."""
        output_path = self.output_dir / filename
        fig.tight_layout()
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return str(output_path)

    def budget_variance_chart(
        self,
        df: pd.DataFrame,
        category_col: str = "category",
        budget_col: str = "total_budget",
        actual_col: str = "total_actual",
        filename: str = "budget_variance.png",
    ) -> str:
        """Generate a grouped bar chart comparing budget vs actual.

        Returns:
            Path to the saved chart image.
        """
        fig, ax = self._setup_plot(title="Budget vs Actual Expenditure")

        x = range(len(df))
        width = 0.35
        ax.bar([i - width / 2 for i in x], df[budget_col], width, label="Budget", color="#2196F3")
        ax.bar([i + width / 2 for i in x], df[actual_col], width, label="Actual", color="#FF9800")

        ax.set_xticks(list(x))
        ax.set_xticklabels(df[category_col], rotation=45, ha="right")
        ax.set_ylabel("Amount ($)")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        ax.legend()

        return self._save_and_close(fig, filename)

    def trend_chart(
        self,
        df: pd.DataFrame,
        date_col: str = "date",
        amount_col: str = "total",
        filename: str = "trend_analysis.png",
    ) -> str:
        """Generate a line chart showing financial trends over time.

        Returns:
            Path to the saved chart image.
        """
        fig, ax = self._setup_plot(title="Financial Trend Over Time")

        ax.plot(df[date_col], df[amount_col], marker="o", linewidth=2, color="#4CAF50")
        ax.fill_between(df[date_col], df[amount_col], alpha=0.15, color="#4CAF50")

        ax.set_xlabel("Period")
        ax.set_ylabel("Amount ($)")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        plt.xticks(rotation=45, ha="right")

        return self._save_and_close(fig, filename)

    def category_pie_chart(
        self,
        df: pd.DataFrame,
        category_col: str = "category",
        amount_col: str = "total",
        filename: str = "category_breakdown.png",
    ) -> str:
        """Generate a pie chart showing category distribution.

        Returns:
            Path to the saved chart image.
        """
        fig, ax = self._setup_plot(figsize=(10, 8), title="Expenditure by Category")

        # Show top categories, group rest as "Other"
        max_slices = 8
        if len(df) > max_slices:
            top = df.nlargest(max_slices - 1, amount_col)
            other_total = df[~df.index.isin(top.index)][amount_col].sum()
            other_row = pd.DataFrame({category_col: ["Other"], amount_col: [other_total]})
            plot_df = pd.concat([top, other_row], ignore_index=True)
        else:
            plot_df = df

        colors = sns.color_palette(self.COLOR_PALETTE, len(plot_df))
        wedges, texts, autotexts = ax.pie(
            plot_df[amount_col],
            labels=plot_df[category_col],
            autopct="%1.1f%%",
            colors=colors,
            startangle=90,
        )
        for autotext in autotexts:
            autotext.set_fontsize(9)

        return self._save_and_close(fig, filename)

    def anomaly_scatter(
        self,
        df: pd.DataFrame,
        amount_col: str = "amount",
        z_score_col: str = "z_score",
        filename: str = "anomalies.png",
    ) -> str:
        """Generate a scatter plot highlighting anomalous data points.

        Returns:
            Path to the saved chart image.
        """
        fig, ax = self._setup_plot(title="Anomaly Detection - Financial Entries")

        is_anomaly = df.get("is_anomaly", pd.Series([False] * len(df)))
        normal = df[~is_anomaly]
        anomalies = df[is_anomaly]

        ax.scatter(
            normal.index, normal[amount_col],
            c="#4CAF50", alpha=0.6, label="Normal", s=30,
        )
        ax.scatter(
            anomalies.index, anomalies[amount_col],
            c="#F44336", alpha=0.8, label="Anomaly", s=80, marker="x",
        )

        ax.set_xlabel("Record Index")
        ax.set_ylabel("Amount ($)")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        ax.legend()

        return self._save_and_close(fig, filename)

    def top_n_bar_chart(
        self,
        df: pd.DataFrame,
        category_col: str = "category",
        amount_col: str = "total",
        n: int = 10,
        filename: str = "top_categories.png",
    ) -> str:
        """Generate a horizontal bar chart of top N categories by amount.

        Returns:
            Path to the saved chart image.
        """
        top = df.nlargest(n, amount_col)
        fig, ax = self._setup_plot(title=f"Top {n} Categories by Amount")

        colors = sns.color_palette(self.COLOR_PALETTE, len(top))
        bars = ax.barh(top[category_col], top[amount_col], color=colors)
        ax.invert_yaxis()
        ax.set_xlabel("Amount ($)")
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))

        return self._save_and_close(fig, filename)

    def heatmap(
        self,
        df: pd.DataFrame,
        index_col: str = "category",
        columns_col: str = "fiscal_year",
        values_col: str = "amount",
        filename: str = "heatmap.png",
    ) -> str:
        """Generate a heatmap of financial data across two dimensions.

        Returns:
            Path to the saved chart image.
        """
        pivot = df.pivot_table(
            index=index_col, columns=columns_col,
            values=values_col, aggfunc="sum", fill_value=0,
        )
        fig, ax = self._setup_plot(
            figsize=(max(12, len(pivot.columns) * 1.5), max(6, len(pivot) * 0.5)),
            title="Financial Heatmap",
        )

        sns.heatmap(
            pivot, annot=True, fmt=",.0f", cmap="YlOrRd",
            ax=ax, linewidths=0.5,
        )
        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)

        return self._save_and_close(fig, filename)
