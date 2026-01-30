# BLM Financial Report Analysis

A Python tool for analyzing Bureau of Land Management (BLM) financial reports. Provides budget variance analysis, trend detection, anomaly identification, category breakdowns, and automated report generation with visualizations.

## Features

- **Data Loading**: Import financial data from CSV, Excel, and PDF formats
- **Data Preprocessing**: Automatic currency parsing, date handling, and data cleaning
- **Financial Analysis**:
  - Summary statistics (overall and grouped)
  - Budget vs. actual variance analysis
  - Time-series trend analysis with linear regression
  - Anomaly detection using z-score method
  - Category-level breakdown with percentage allocation
- **Visualization**: Auto-generated charts including bar charts, line plots, pie charts, scatter plots, and heatmaps
- **Report Generation**: HTML, plain text, and JSON output formats
- **CLI Interface**: Command-line tool for quick analysis

## Project Structure

```
BLM-Financial-Report-Analysis/
├── src/
│   ├── __init__.py
│   ├── main.py                  # CLI entry point
│   ├── data/
│   │   ├── loader.py            # Data loading & preprocessing
│   │   └── sample.py            # Sample data generation
│   ├── analysis/
│   │   └── financial.py         # Core financial analysis
│   ├── visualization/
│   │   └── charts.py            # Chart generation
│   └── reports/
│       └── generator.py         # Report generation (HTML/Text/JSON)
├── tests/
│   ├── test_loader.py
│   ├── test_analysis.py
│   ├── test_reports.py
│   └── test_sample.py
├── data/
│   ├── raw/                     # Input data files
│   ├── processed/               # Cleaned intermediate data
│   └── output/                  # Generated reports and charts
├── config/
│   └── default.yaml             # Default configuration
├── requirements.txt
├── setup.py
└── README.md
```

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd BLM-Financial-Report-Analysis

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Usage

### Generate Sample Data

```bash
python -m src.main generate-sample --output data/raw/sample_blm_data.csv
```

### Run Full Analysis

```bash
python -m src.main analyze data/raw/sample_blm_data.csv --format all
```

### Print Summary Statistics

```bash
python -m src.main summary data/raw/sample_blm_data.csv --amount-col amount --group-col category
```

### Python API

```python
from src.data.loader import DataLoader, FinancialDataPreprocessor
from src.analysis.financial import BudgetAnalyzer
from src.visualization.charts import FinancialChartGenerator
from src.reports.generator import ReportGenerator

# Load and preprocess data
loader = DataLoader()
preprocessor = FinancialDataPreprocessor()
df = loader.load("data/raw/report.csv")
df = preprocessor.preprocess(df)

# Analyze
analyzer = BudgetAnalyzer(df)
summary = analyzer.summary_statistics(amount_col="amount", group_col="category")
variance = analyzer.budget_variance(budget_col="budget", actual_col="actual")
trends = analyzer.trend_analysis(amount_col="amount", date_col="date")
anomalies = analyzer.detect_anomalies(amount_col="amount")

# Generate report
report_gen = ReportGenerator()
report_gen.generate_html_report([summary, variance, trends, anomalies])
```

## Running Tests

```bash
pytest tests/ -v
```

## Configuration

Edit `config/default.yaml` to customize default column names, analysis parameters, and output settings.

## Requirements

- Python 3.9+
- pandas, numpy, matplotlib, seaborn, openpyxl, pdfplumber, jinja2, click, pyyaml
