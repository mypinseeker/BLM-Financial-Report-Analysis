"""Configuration loader for BLM Financial Report Analysis."""

from pathlib import Path
from typing import Any, Optional

import yaml


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "default.yaml"

DEFAULT_CONFIG = {
    "data": {
        "raw_dir": "data/raw",
        "processed_dir": "data/processed",
        "output_dir": "data/output",
    },
    "analysis": {
        "default_amount_col": "amount",
        "default_budget_col": "budget",
        "default_actual_col": "actual",
        "default_category_col": "category",
        "default_date_col": "date",
        "anomaly_threshold": 2.0,
        "trend_frequency": "YE",
    },
    "reports": {
        "default_format": "html",
        "title": "BLM Financial Analysis Report",
        "max_table_rows": 50,
    },
    "visualization": {
        "style": "seaborn-v0_8-whitegrid",
        "figsize": [12, 6],
        "dpi": 150,
        "color_palette": "viridis",
    },
}


class Config:
    """Application configuration loaded from YAML file with defaults."""

    def __init__(self, config_path: Optional[str] = None):
        self._data = dict(DEFAULT_CONFIG)
        path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
        if path.exists():
            with open(path, "r") as f:
                user_config = yaml.safe_load(f) or {}
            self._merge(self._data, user_config)

    @staticmethod
    def _merge(base: dict, override: dict) -> None:
        """Recursively merge override into base dict."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                Config._merge(base[key], value)
            else:
                base[key] = value

    def get(self, *keys: str, default: Any = None) -> Any:
        """Get a nested config value using dot-separated keys.

        Example:
            config.get("analysis", "anomaly_threshold")  # returns 2.0
        """
        current = self._data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current

    @property
    def data(self) -> dict:
        return self._data["data"]

    @property
    def analysis(self) -> dict:
        return self._data["analysis"]

    @property
    def reports(self) -> dict:
        return self._data["reports"]

    @property
    def visualization(self) -> dict:
        return self._data["visualization"]
