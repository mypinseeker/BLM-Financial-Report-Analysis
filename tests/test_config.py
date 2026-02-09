"""Tests for configuration loader."""

import pytest

from src.config import Config, DEFAULT_CONFIG


class TestConfig:
    def test_default_config_loads(self):
        config = Config()
        assert config.analysis["anomaly_threshold"] == 2.0
        assert config.analysis["trend_frequency"] == "YE"

    def test_config_properties(self):
        config = Config()
        assert "raw_dir" in config.data
        assert "default_format" in config.reports
        assert "style" in config.visualization

    def test_get_nested_value(self):
        config = Config()
        val = config.get("analysis", "anomaly_threshold")
        assert val == 2.0

    def test_get_missing_key_returns_default(self):
        config = Config()
        val = config.get("nonexistent", "key", default="fallback")
        assert val == "fallback"

    def test_custom_config_file(self, tmp_path):
        custom = tmp_path / "custom.yaml"
        custom.write_text(
            "analysis:\n  anomaly_threshold: 3.5\n  trend_frequency: ME\n"
        )
        config = Config(config_path=str(custom))
        assert config.analysis["anomaly_threshold"] == 3.5
        assert config.analysis["trend_frequency"] == "ME"
        # Other defaults preserved
        assert config.analysis["default_amount_col"] == "amount"

    def test_nonexistent_config_uses_defaults(self, tmp_path):
        config = Config(config_path=str(tmp_path / "missing.yaml"))
        assert config.analysis["anomaly_threshold"] == DEFAULT_CONFIG["analysis"]["anomaly_threshold"]
