"""Tests for the CLI interface."""

from pathlib import Path

import pandas as pd
import pytest
from click.testing import CliRunner

from src.data.sample import generate_sample_data
from src.main import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def sample_csv(tmp_path):
    """Generate a sample CSV file for testing."""
    df = generate_sample_data(n_records=50, seed=42)
    path = tmp_path / "test_data.csv"
    df.to_csv(path, index=False)
    return str(path)


class TestCLIHelp:
    def test_main_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "BLM Financial Report Analysis Tool" in result.output

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_analyze_help(self, runner):
        result = runner.invoke(cli, ["analyze", "--help"])
        assert result.exit_code == 0
        assert "--year-col" in result.output
        assert "--state-col" in result.output

    def test_export_help(self, runner):
        result = runner.invoke(cli, ["export", "--help"])
        assert result.exit_code == 0
        assert "--fmt" in result.output

    def test_generate_sample_help(self, runner):
        result = runner.invoke(cli, ["generate-sample", "--help"])
        assert result.exit_code == 0
        assert "--records" in result.output


class TestAnalyzeCommand:
    def test_analyze_html(self, runner, sample_csv, tmp_path):
        output_dir = str(tmp_path / "output")
        result = runner.invoke(cli, [
            "analyze", sample_csv,
            "--output-dir", output_dir,
            "--format", "html",
        ])
        assert result.exit_code == 0
        assert "Analysis complete." in result.output
        assert "Running summary statistics..." in result.output
        assert "Running year-over-year analysis..." in result.output
        assert "Running state comparison..." in result.output
        assert Path(output_dir, "report.html").exists()

    def test_analyze_all_formats(self, runner, sample_csv, tmp_path):
        output_dir = str(tmp_path / "output")
        result = runner.invoke(cli, [
            "analyze", sample_csv,
            "--output-dir", output_dir,
            "--format", "all",
        ])
        assert result.exit_code == 0
        assert Path(output_dir, "report.html").exists()
        assert Path(output_dir, "report.txt").exists()
        assert Path(output_dir, "report.json").exists()

    def test_analyze_json(self, runner, sample_csv, tmp_path):
        output_dir = str(tmp_path / "output")
        result = runner.invoke(cli, [
            "analyze", sample_csv,
            "--output-dir", output_dir,
            "--format", "json",
        ])
        assert result.exit_code == 0
        assert "JSON report:" in result.output

    def test_analyze_nonexistent_file(self, runner):
        result = runner.invoke(cli, ["analyze", "/nonexistent/file.csv"])
        assert result.exit_code != 0

    def test_analyze_with_config(self, runner, sample_csv, tmp_path):
        config_path = tmp_path / "test_config.yaml"
        config_path.write_text(
            "analysis:\n  anomaly_threshold: 3.0\n  trend_frequency: YE\n"
        )
        output_dir = str(tmp_path / "output")
        result = runner.invoke(cli, [
            "--config", str(config_path),
            "analyze", sample_csv,
            "--output-dir", output_dir,
        ])
        assert result.exit_code == 0
        assert "Analysis complete." in result.output


class TestSummaryCommand:
    def test_summary_basic(self, runner, sample_csv):
        result = runner.invoke(cli, ["summary", sample_csv])
        assert result.exit_code == 0
        assert "Summary Statistics" in result.output

    def test_summary_with_group(self, runner, sample_csv):
        result = runner.invoke(cli, [
            "summary", sample_csv,
            "--group-col", "category",
        ])
        assert result.exit_code == 0
        assert "Summary Statistics" in result.output


class TestExportCommand:
    def test_export_csv(self, runner, sample_csv, tmp_path):
        output_dir = str(tmp_path / "export_out")
        result = runner.invoke(cli, [
            "export", sample_csv,
            "--output-dir", output_dir,
            "--fmt", "csv",
        ])
        assert result.exit_code == 0
        assert "Export complete." in result.output
        assert "Processed data:" in result.output
        assert Path(output_dir, "processed_data.csv").exists()

    def test_export_excel(self, runner, sample_csv, tmp_path):
        output_dir = str(tmp_path / "export_out")
        result = runner.invoke(cli, [
            "export", sample_csv,
            "--output-dir", output_dir,
            "--fmt", "excel",
        ])
        assert result.exit_code == 0
        assert "Export complete." in result.output


class TestGenerateSampleCommand:
    def test_generate_sample(self, runner, tmp_path):
        output_path = str(tmp_path / "generated.csv")
        result = runner.invoke(cli, [
            "generate-sample",
            "--output", output_path,
        ])
        assert result.exit_code == 0
        assert "200 records" in result.output
        assert Path(output_path).exists()

    def test_generate_sample_custom_count(self, runner, tmp_path):
        output_path = str(tmp_path / "generated.csv")
        result = runner.invoke(cli, [
            "generate-sample",
            "--output", output_path,
            "--records", "50",
        ])
        assert result.exit_code == 0
        assert "50 records" in result.output
        df = pd.read_csv(output_path)
        assert len(df) == 50
