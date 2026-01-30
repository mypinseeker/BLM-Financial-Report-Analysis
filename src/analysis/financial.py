"""Core financial analysis module for BLM reports.

Provides budget analysis, trend detection, anomaly identification,
and comparative analysis across fiscal periods.
"""

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd


@dataclass
class AnalysisResult:
    """Container for analysis results."""

    name: str
    summary: dict
    details: pd.DataFrame
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "summary": self.summary,
            "details": self.details.to_dict(orient="records"),
            "metadata": self.metadata,
        }


class BudgetAnalyzer:
    """Analyze BLM budget allocations and expenditures."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def summary_statistics(
        self,
        amount_col: str = "amount",
        group_col: Optional[str] = None,
    ) -> AnalysisResult:
        """Compute summary statistics for financial amounts.

        Args:
            amount_col: Column containing monetary amounts.
            group_col: Optional column to group by (e.g., department, category).

        Returns:
            AnalysisResult with summary stats.
        """
        if amount_col not in self.df.columns:
            raise ValueError(f"Column '{amount_col}' not found in data.")

        if group_col and group_col in self.df.columns:
            grouped = self.df.groupby(group_col)[amount_col]
            details = grouped.agg(["count", "sum", "mean", "median", "std", "min", "max"])
            details = details.reset_index()
            summary = {
                "total": float(self.df[amount_col].sum()),
                "groups": int(details.shape[0]),
                "largest_group": details.loc[details["sum"].idxmax(), group_col],
                "smallest_group": details.loc[details["sum"].idxmin(), group_col],
            }
        else:
            series = self.df[amount_col].dropna()
            details = pd.DataFrame(
                {
                    "metric": ["count", "total", "mean", "median", "std", "min", "max"],
                    "value": [
                        series.count(),
                        series.sum(),
                        series.mean(),
                        series.median(),
                        series.std(),
                        series.min(),
                        series.max(),
                    ],
                }
            )
            summary = {
                "total": float(series.sum()),
                "mean": float(series.mean()),
                "count": int(series.count()),
            }

        return AnalysisResult(
            name="summary_statistics",
            summary=summary,
            details=details,
        )

    def budget_variance(
        self,
        budget_col: str = "budget",
        actual_col: str = "actual",
        category_col: Optional[str] = None,
    ) -> AnalysisResult:
        """Calculate budget vs actual variance.

        Args:
            budget_col: Column with budgeted amounts.
            actual_col: Column with actual expenditures.
            category_col: Optional grouping column.

        Returns:
            AnalysisResult with variance analysis.
        """
        for col in [budget_col, actual_col]:
            if col not in self.df.columns:
                raise ValueError(f"Column '{col}' not found in data.")

        df = self.df.copy()
        df["variance"] = df[actual_col] - df[budget_col]
        df["variance_pct"] = (df["variance"] / df[budget_col].replace(0, np.nan)) * 100

        if category_col and category_col in df.columns:
            details = (
                df.groupby(category_col)
                .agg(
                    total_budget=(budget_col, "sum"),
                    total_actual=(actual_col, "sum"),
                    total_variance=("variance", "sum"),
                    avg_variance_pct=("variance_pct", "mean"),
                )
                .reset_index()
            )
        else:
            details = df[[budget_col, actual_col, "variance", "variance_pct"]]

        over_budget = df[df["variance"] > 0]
        under_budget = df[df["variance"] < 0]

        summary = {
            "total_budget": float(df[budget_col].sum()),
            "total_actual": float(df[actual_col].sum()),
            "total_variance": float(df["variance"].sum()),
            "overall_variance_pct": float(
                (df[actual_col].sum() - df[budget_col].sum())
                / df[budget_col].sum()
                * 100
            )
            if df[budget_col].sum() != 0
            else 0.0,
            "items_over_budget": int(len(over_budget)),
            "items_under_budget": int(len(under_budget)),
        }

        return AnalysisResult(
            name="budget_variance",
            summary=summary,
            details=details,
        )

    def trend_analysis(
        self,
        amount_col: str = "amount",
        date_col: str = "date",
        freq: str = "YE",
    ) -> AnalysisResult:
        """Analyze financial trends over time.

        Args:
            amount_col: Column with monetary amounts.
            date_col: Column with dates/periods.
            freq: Frequency for aggregation ('YE', 'QE', 'ME').

        Returns:
            AnalysisResult with trend data.
        """
        for col in [amount_col, date_col]:
            if col not in self.df.columns:
                raise ValueError(f"Column '{col}' not found in data.")

        df = self.df.copy()
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.dropna(subset=[date_col, amount_col])

        df = df.set_index(date_col)
        trend = df[amount_col].resample(freq).agg(["sum", "mean", "count"])
        trend = trend.reset_index()
        trend.columns = [date_col, "total", "average", "count"]

        # Calculate period-over-period change
        trend["change"] = trend["total"].diff()
        trend["change_pct"] = trend["total"].pct_change() * 100

        # Linear trend
        if len(trend) > 1:
            x = np.arange(len(trend))
            coeffs = np.polyfit(x, trend["total"].values, 1)
            trend_direction = "increasing" if coeffs[0] > 0 else "decreasing"
            slope = float(coeffs[0])
        else:
            trend_direction = "insufficient_data"
            slope = 0.0

        summary = {
            "periods": int(len(trend)),
            "trend_direction": trend_direction,
            "slope_per_period": slope,
            "total_growth_pct": float(
                (trend["total"].iloc[-1] - trend["total"].iloc[0])
                / trend["total"].iloc[0]
                * 100
            )
            if len(trend) > 1 and trend["total"].iloc[0] != 0
            else 0.0,
        }

        return AnalysisResult(
            name="trend_analysis",
            summary=summary,
            details=trend,
        )

    def detect_anomalies(
        self,
        amount_col: str = "amount",
        threshold: float = 2.0,
    ) -> AnalysisResult:
        """Detect anomalous financial entries using z-score method.

        Args:
            amount_col: Column to check for anomalies.
            threshold: Z-score threshold for anomaly detection.

        Returns:
            AnalysisResult with flagged anomalies.
        """
        if amount_col not in self.df.columns:
            raise ValueError(f"Column '{amount_col}' not found in data.")

        df = self.df.copy()
        series = df[amount_col].dropna()

        mean = series.mean()
        std = series.std()

        if std == 0 or np.isnan(std):
            return AnalysisResult(
                name="anomaly_detection",
                summary={"anomalies_found": 0, "message": "No variance in data"},
                details=pd.DataFrame(),
            )

        df["z_score"] = (df[amount_col] - mean) / std
        df["is_anomaly"] = df["z_score"].abs() > threshold

        anomalies = df[df["is_anomaly"]].copy()

        summary = {
            "total_records": int(len(df)),
            "anomalies_found": int(len(anomalies)),
            "anomaly_rate": float(len(anomalies) / len(df) * 100) if len(df) > 0 else 0.0,
            "threshold": threshold,
            "mean": float(mean),
            "std": float(std),
        }

        return AnalysisResult(
            name="anomaly_detection",
            summary=summary,
            details=anomalies,
        )

    def category_breakdown(
        self,
        amount_col: str = "amount",
        category_col: str = "category",
    ) -> AnalysisResult:
        """Break down financial data by category.

        Args:
            amount_col: Column with monetary amounts.
            category_col: Column with categories.

        Returns:
            AnalysisResult with category breakdown.
        """
        for col in [amount_col, category_col]:
            if col not in self.df.columns:
                raise ValueError(f"Column '{col}' not found in data.")

        breakdown = (
            self.df.groupby(category_col)[amount_col]
            .agg(["sum", "mean", "count"])
            .reset_index()
        )
        breakdown.columns = [category_col, "total", "average", "count"]

        total = breakdown["total"].sum()
        breakdown["percentage"] = (breakdown["total"] / total * 100) if total != 0 else 0
        breakdown = breakdown.sort_values("total", ascending=False)

        summary = {
            "total_categories": int(len(breakdown)),
            "total_amount": float(total),
            "top_category": breakdown.iloc[0][category_col] if len(breakdown) > 0 else None,
            "top_category_pct": float(breakdown.iloc[0]["percentage"]) if len(breakdown) > 0 else 0.0,
        }

        return AnalysisResult(
            name="category_breakdown",
            summary=summary,
            details=breakdown,
        )

    def year_over_year(
        self,
        amount_col: str = "amount",
        year_col: str = "fiscal_year",
        category_col: Optional[str] = None,
    ) -> AnalysisResult:
        """Compare financial metrics year-over-year.

        Args:
            amount_col: Column with monetary amounts.
            year_col: Column with fiscal year values.
            category_col: Optional column to group by category within each year.

        Returns:
            AnalysisResult with year-over-year comparison.
        """
        for col in [amount_col, year_col]:
            if col not in self.df.columns:
                raise ValueError(f"Column '{col}' not found in data.")

        df = self.df.copy()

        if category_col and category_col in df.columns:
            yearly = (
                df.groupby([year_col, category_col])[amount_col]
                .sum()
                .reset_index()
            )
            pivot = yearly.pivot_table(
                index=category_col, columns=year_col,
                values=amount_col, fill_value=0,
            )
            years = sorted(pivot.columns)
            yoy_details = pd.DataFrame({category_col: pivot.index})
            for i in range(1, len(years)):
                prev, curr = years[i - 1], years[i]
                col_name = f"{prev}_to_{curr}_change_pct"
                prev_vals = pivot[prev].replace(0, np.nan)
                yoy_details[f"{prev}"] = pivot[prev].values
                yoy_details[f"{curr}"] = pivot[curr].values
                yoy_details[col_name] = (
                    (pivot[curr] - pivot[prev]) / prev_vals * 100
                ).values
            details = yoy_details.reset_index(drop=True)
        else:
            yearly = (
                df.groupby(year_col)[amount_col]
                .agg(["sum", "mean", "count"])
                .reset_index()
            )
            yearly.columns = [year_col, "total", "average", "count"]
            yearly = yearly.sort_values(year_col)
            yearly["yoy_change"] = yearly["total"].diff()
            yearly["yoy_change_pct"] = yearly["total"].pct_change() * 100
            details = yearly

        # Ensure year column is numeric for sorting/display
        if pd.api.types.is_datetime64_any_dtype(df[year_col]):
            df[year_col] = df[year_col].dt.year

        years_list = sorted(df[year_col].unique())
        first_year_total = float(
            df[df[year_col] == years_list[0]][amount_col].sum()
        )
        last_year_total = float(
            df[df[year_col] == years_list[-1]][amount_col].sum()
        )

        summary = {
            "years_covered": len(years_list),
            "first_year": int(years_list[0]),
            "last_year": int(years_list[-1]),
            "first_year_total": first_year_total,
            "last_year_total": last_year_total,
            "cumulative_change_pct": float(
                (last_year_total - first_year_total) / first_year_total * 100
            )
            if first_year_total != 0
            else 0.0,
        }

        return AnalysisResult(
            name="year_over_year",
            summary=summary,
            details=details,
        )

    def state_comparison(
        self,
        amount_col: str = "amount",
        state_col: str = "state",
    ) -> AnalysisResult:
        """Compare financial data across states/regions.

        Args:
            amount_col: Column with monetary amounts.
            state_col: Column with state/region names.

        Returns:
            AnalysisResult with state comparison.
        """
        for col in [amount_col, state_col]:
            if col not in self.df.columns:
                raise ValueError(f"Column '{col}' not found in data.")

        details = (
            self.df.groupby(state_col)[amount_col]
            .agg(["sum", "mean", "count", "std"])
            .reset_index()
        )
        details.columns = [state_col, "total", "average", "count", "std_dev"]
        overall_total = details["total"].sum()
        details["percentage"] = (
            (details["total"] / overall_total * 100) if overall_total != 0 else 0
        )
        details = details.sort_values("total", ascending=False)

        summary = {
            "total_states": int(len(details)),
            "total_amount": float(overall_total),
            "highest_state": details.iloc[0][state_col] if len(details) > 0 else None,
            "highest_amount": float(details.iloc[0]["total"]) if len(details) > 0 else 0.0,
            "lowest_state": details.iloc[-1][state_col] if len(details) > 0 else None,
            "lowest_amount": float(details.iloc[-1]["total"]) if len(details) > 0 else 0.0,
        }

        return AnalysisResult(
            name="state_comparison",
            summary=summary,
            details=details,
        )
