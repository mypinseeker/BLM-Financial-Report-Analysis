"""Data export module for saving processed data and analysis results."""

from pathlib import Path
from typing import Optional

import pandas as pd

from src.analysis.financial import AnalysisResult


class DataExporter:
    """Export processed data and analysis results to various formats."""

    def __init__(self, output_dir: Optional[str] = None):
        if output_dir is None:
            output_dir = str(
                Path(__file__).resolve().parent.parent.parent / "data" / "processed"
            )
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_dataframe(
        self,
        df: pd.DataFrame,
        filename: str,
        fmt: str = "csv",
    ) -> str:
        """Export a DataFrame to file.

        Args:
            df: DataFrame to export.
            filename: Output filename (without extension).
            fmt: Format - 'csv' or 'excel'.

        Returns:
            Path to the exported file.
        """
        if fmt == "csv":
            path = self.output_dir / f"{filename}.csv"
            df.to_csv(path, index=False)
        elif fmt == "excel":
            path = self.output_dir / f"{filename}.xlsx"
            df.to_excel(path, index=False, engine="openpyxl")
        else:
            raise ValueError(f"Unsupported export format: {fmt}. Use 'csv' or 'excel'.")
        return str(path)

    def export_results(
        self,
        results: list[AnalysisResult],
        prefix: str = "analysis",
        fmt: str = "csv",
    ) -> list[str]:
        """Export multiple analysis results to files.

        Args:
            results: List of AnalysisResult objects.
            prefix: Filename prefix for all exported files.
            fmt: Export format ('csv' or 'excel').

        Returns:
            List of paths to exported files.
        """
        paths = []
        for result in results:
            if result.details.empty:
                continue
            filename = f"{prefix}_{result.name}"
            path = self.export_dataframe(result.details, filename, fmt)
            paths.append(path)
        return paths

    def export_summary(
        self,
        results: list[AnalysisResult],
        filename: str = "analysis_summary",
        fmt: str = "csv",
    ) -> str:
        """Export summary data from all results as a single file.

        Args:
            results: List of AnalysisResult objects.
            filename: Output filename (without extension).
            fmt: Export format.

        Returns:
            Path to the exported file.
        """
        rows = []
        for result in results:
            for key, value in result.summary.items():
                rows.append({
                    "analysis": result.name,
                    "metric": key,
                    "value": value,
                })
        summary_df = pd.DataFrame(rows)
        return self.export_dataframe(summary_df, filename, fmt)
