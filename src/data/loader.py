"""Data loading and parsing module for BLM financial reports.

Supports loading financial data from CSV, Excel, and PDF formats.
"""

import os
from pathlib import Path
from typing import Optional

import pandas as pd

def _import_pdfplumber():
    try:
        import pdfplumber
        return pdfplumber
    except ImportError:
        return None
    except Exception:
        return None


def _import_tabula():
    try:
        import tabula
        return tabula
    except ImportError:
        return None
    except Exception:
        return None


class DataLoader:
    """Load and parse BLM financial report data from various file formats."""

    SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".pdf"}

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
        self.data_dir = Path(data_dir).resolve()

    def load(self, filepath: str) -> pd.DataFrame:
        """Load a financial report file and return a DataFrame.

        Args:
            filepath: Path to the file. If relative, resolved against data_dir.

        Returns:
            pandas DataFrame with the loaded data.

        Raises:
            ValueError: If file format is not supported.
            FileNotFoundError: If file does not exist.
        """
        path = Path(filepath)
        if not path.is_absolute():
            path = self.data_dir / path
        path = path.resolve()

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        ext = path.suffix.lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file format: {ext}. "
                f"Supported formats: {', '.join(sorted(self.SUPPORTED_EXTENSIONS))}"
            )

        loader_map = {
            ".csv": self._load_csv,
            ".xlsx": self._load_excel,
            ".xls": self._load_excel,
            ".pdf": self._load_pdf,
        }
        return loader_map[ext](path)

    def load_directory(self, directory: Optional[str] = None, pattern: str = "*") -> dict[str, pd.DataFrame]:
        """Load all supported files from a directory.

        Args:
            directory: Directory path. Defaults to data_dir.
            pattern: Glob pattern to filter files.

        Returns:
            Dict mapping filenames to DataFrames.
        """
        target_dir = Path(directory) if directory else self.data_dir
        results = {}
        for ext in self.SUPPORTED_EXTENSIONS:
            for filepath in target_dir.glob(f"{pattern}{ext}"):
                try:
                    results[filepath.name] = self.load(str(filepath))
                except Exception as e:
                    print(f"Warning: Failed to load {filepath.name}: {e}")
        return results

    def _load_csv(self, path: Path) -> pd.DataFrame:
        """Load a CSV file."""
        df = pd.read_csv(path)
        return self._standardize_columns(df)

    def _load_excel(self, path: Path) -> pd.DataFrame:
        """Load an Excel file."""
        df = pd.read_excel(path, engine="openpyxl")
        return self._standardize_columns(df)

    def _load_pdf(self, path: Path) -> pd.DataFrame:
        """Extract tabular data from a PDF file."""
        _pdfplumber = _import_pdfplumber()
        if _pdfplumber is not None:
            return self._load_pdf_pdfplumber(path, _pdfplumber)
        _tabula = _import_tabula()
        if _tabula is not None:
            return self._load_pdf_tabula(path, _tabula)
        raise ImportError(
            "PDF parsing requires either 'pdfplumber' or 'tabula-py'. "
            "Install one of them: pip install pdfplumber"
        )

    def _load_pdf_pdfplumber(self, path: Path, _pdfplumber) -> pd.DataFrame:
        """Extract tables from PDF using pdfplumber."""
        all_tables = []
        with _pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    if table and len(table) > 1:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        all_tables.append(df)
        if not all_tables:
            raise ValueError(f"No tables found in PDF: {path}")
        combined = pd.concat(all_tables, ignore_index=True)
        return self._standardize_columns(combined)

    def _load_pdf_tabula(self, path: Path, _tabula) -> pd.DataFrame:
        """Extract tables from PDF using tabula."""
        dfs = _tabula.read_pdf(str(path), pages="all", multiple_tables=True)
        if not dfs:
            raise ValueError(f"No tables found in PDF: {path}")
        combined = pd.concat(dfs, ignore_index=True)
        return self._standardize_columns(combined)

    @staticmethod
    def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names to snake_case."""
        df.columns = (
            df.columns.str.strip()
            .str.lower()
            .str.replace(r"[^\w\s]", "", regex=True)
            .str.replace(r"\s+", "_", regex=True)
        )
        return df


class FinancialDataPreprocessor:
    """Preprocess and clean BLM financial data."""

    CURRENCY_COLUMNS_PATTERNS = [
        "amount", "budget", "revenue", "expense", "cost",
        "funding", "allocation", "expenditure", "income",
        "total", "balance", "payment", "fee", "grant",
    ]

    DATE_COLUMN_PATTERNS = [
        "date", "period", "year", "quarter", "month",
        "fiscal_year", "fy",
    ]

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply standard preprocessing to financial data.

        - Remove fully empty rows/columns
        - Parse currency columns to numeric
        - Parse date columns
        - Strip whitespace from string columns
        """
        df = df.dropna(how="all").dropna(axis=1, how="all")
        df = self._clean_string_columns(df)
        df = self._parse_currency_columns(df)
        df = self._parse_date_columns(df)
        return df.reset_index(drop=True)

    def _clean_string_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Strip whitespace from string columns."""
        for col in df.select_dtypes(include=["object", "string"]).columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace({"nan": None, "None": None, "": None})
        return df

    def _parse_currency_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert currency-formatted strings to numeric values."""
        for col in df.columns:
            if any(pattern in col for pattern in self.CURRENCY_COLUMNS_PATTERNS):
                df[col] = self._parse_currency_series(df[col])
        return df

    @staticmethod
    def _parse_currency_series(series: pd.Series) -> pd.Series:
        """Parse a series of currency strings to numeric."""
        cleaned = (
            series.astype(str)
            .str.replace(r"[\$,\s]", "", regex=True)
            .str.replace(r"\(([^)]+)\)", r"-\1", regex=True)  # (100) -> -100
        )
        return pd.to_numeric(cleaned, errors="coerce")

    def _parse_date_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Attempt to parse date-like columns.

        Skips columns that are already numeric (e.g., fiscal_year=2019)
        to avoid misinterpreting integers as timestamps.
        """
        for col in df.columns:
            if any(pattern in col for pattern in self.DATE_COLUMN_PATTERNS):
                if pd.api.types.is_numeric_dtype(df[col]):
                    continue
                try:
                    df[col] = pd.to_datetime(df[col], errors="coerce")
                except (ValueError, TypeError):
                    pass
        return df
