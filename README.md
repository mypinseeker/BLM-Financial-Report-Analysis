# BLM Strategic Analysis Skill

A comprehensive Python framework for telecom operator strategic analysis using the **Business Leadership Model (业务领先模型 / BLM)**. Supports global operators with Five Looks (五看) analysis and Three Decisions (三定) strategy generation.

## Overview

This tool implements the BLM strategic framework commonly used in telecom industry strategic planning:

**Five Looks (五看) Analysis:**
1. 看市场 (Look at Market) - Market size, growth, segments, trends
2. 看自己 (Look at Self) - Self assessment, capabilities, performance
3. 看对手 (Look at Competitors) - Competitive positioning, benchmarking
4. 看宏观 (Look at Macro) - Macro environment, regulations, technology trends
5. 看机会 (Look at Opportunities) - Gap analysis, opportunities, threats

**Three Decisions (三定) Strategy:**
1. 定策略 (Set Strategy) - Strategic direction, differentiation, positioning
2. 定重点工作 (Set Key Tasks) - Critical tasks, key initiatives
3. 定执行 (Set Execution) - Action plans, milestones, KPIs

## Supported Operators

The framework supports 24+ global telecom operators across all regions:

| Region | Operators |
|--------|-----------|
| **APAC** | China Mobile, China Telecom, China Unicom, NTT Docomo, SoftBank, SK Telecom, Singtel, Telstra, Reliance Jio, Bharti Airtel |
| **Europe** | Vodafone, Deutsche Telekom, Orange, Telefonica, BT Group |
| **Americas** | AT&T, Verizon, T-Mobile US, America Movil |
| **Africa/MEA** | MTN, Airtel Africa, Etisalat, STC |

Custom operators can be easily added to the registry.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/BLM-Financial-Report-Analysis.git
cd BLM-Financial-Report-Analysis

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Quick Start

### Python API

```python
from src.blm import generate_blm_strategy, generate_sample_data

# Generate sample data for operators
data = generate_sample_data(
    operators=["Vodafone", "MTN", "Orange"],
    n_quarters=8,
)

# Run full BLM analysis
results = generate_blm_strategy(
    data,
    target_operator="Vodafone",
    competitors=["MTN", "Orange"],
)

# Access Five Looks insights
market_insight = results["five_looks"]["market"]
print(f"Market findings: {market_insight.findings}")
print(f"Market metrics: {market_insight.metrics}")

# Access Three Decisions strategy
strategy = results["three_decisions"]["strategy"]
print(f"Strategy summary: {strategy.summary}")
for item in strategy.items:
    print(f"  [{item.priority}] {item.name}: {item.description}")
```

### CLI Commands

```bash
# List all supported operators
python -m src.main blm list-operators

# Run full BLM analysis for an operator
python -m src.main blm analyze \
    --target "China Mobile" \
    --competitors "China Telecom,China Unicom" \
    --format all

# Compare multiple operators
python -m src.main blm compare \
    --operators "Vodafone,MTN,Orange,Telefonica"

# Run Five Looks analysis only
python -m src.main blm five-looks \
    --target "AT&T" \
    --competitors "Verizon,T-Mobile US" \
    --look all

# Run Three Decisions strategy only
python -m src.main blm three-decisions \
    --target "Deutsche Telekom" \
    --decision strategy

# Generate sample data
python -m src.main blm generate-data \
    --operators "Reliance Jio,Bharti Airtel" \
    --quarters 12 \
    --output data/raw/india_operators.json
```

## Project Structure

```
BLM-Financial-Report-Analysis/
├── src/
│   ├── blm/                        # BLM Strategic Analysis Module
│   │   ├── __init__.py             # Module exports
│   │   ├── telecom_data.py         # Telecom data models & generator
│   │   ├── five_looks.py           # Five Looks analysis engine
│   │   ├── three_decisions.py      # Three Decisions strategy engine
│   │   ├── report_generator.py     # BLM report generation
│   │   └── cli.py                  # BLM CLI commands
│   ├── data/                       # Data utilities
│   │   ├── loader.py               # Data loading & preprocessing
│   │   ├── export.py               # Data export utilities
│   │   └── sample.py               # Sample data generation
│   ├── analysis/
│   │   └── financial.py            # Financial analysis utilities
│   ├── visualization/
│   │   └── charts.py               # Chart generation
│   ├── reports/
│   │   └── generator.py            # General report generation
│   ├── config.py                   # Configuration management
│   └── main.py                     # CLI entry point
├── tests/
│   ├── test_blm.py                 # BLM module tests (45 tests)
│   ├── test_analysis.py
│   ├── test_loader.py
│   └── ...
├── data/
│   ├── raw/                        # Input data files
│   └── output/                     # Generated reports and charts
├── config/
│   └── default.yaml                # Default configuration
├── requirements.txt
└── README.md
```

## API Reference

### Core Classes

#### `FiveLooksAnalyzer`

```python
from src.blm import FiveLooksAnalyzer, generate_sample_data

data = generate_sample_data(["China Mobile", "China Telecom"])
analyzer = FiveLooksAnalyzer(
    data=data,
    target_operator="China Mobile",
    competitors=["China Telecom"],
)

# Run individual looks
market = analyzer.look_at_market()      # 看市场
self_insight = analyzer.look_at_self()  # 看自己
competitor = analyzer.look_at_competitors()  # 看对手
macro = analyzer.look_at_macro()        # 看宏观
opportunity = analyzer.look_at_opportunities()  # 看机会

# Run all at once
results = analyzer.run_full_analysis()
```

#### `ThreeDecisionsEngine`

```python
from src.blm import ThreeDecisionsEngine

engine = ThreeDecisionsEngine(
    five_looks_results=analyzer.run_full_analysis(),
    target_operator="China Mobile",
)

# Generate individual decisions
strategy = engine.define_strategy()      # 定策略
key_tasks = engine.define_key_tasks()    # 定重点工作
execution = engine.define_execution()    # 定执行

# Run all at once
decisions = engine.run_full_strategy()
```

#### `BLMReportGenerator`

```python
from src.blm import BLMReportGenerator

report_gen = BLMReportGenerator(output_dir="data/output")

# Generate HTML report
html_path = report_gen.generate_html_report(
    five_looks=results["five_looks"],
    three_decisions=results["three_decisions"],
    target_operator="Vodafone",
    competitors=["MTN", "Orange"],
)

# Generate text report
text_path = report_gen.generate_text_report(...)

# Generate JSON report
json_path = report_gen.generate_json_report(...)

# Get executive summary
summary = report_gen.generate_executive_summary(...)
```

### Data Models

#### `InsightResult` (Five Looks output)

```python
@dataclass
class InsightResult:
    category: str       # "market", "self", "competitor", "macro", "opportunity"
    title: str          # e.g., "市场洞察 (Look at Market)"
    findings: list[str] # Key findings
    metrics: dict       # Quantitative metrics
    data: pd.DataFrame  # Underlying data
    recommendations: list[str]  # Action recommendations
```

#### `StrategyResult` (Three Decisions output)

```python
@dataclass
class StrategyItem:
    name: str           # Strategy/task name
    description: str    # Description
    priority: str       # "P0", "P1", "P2"
    category: str       # Category
    timeline: str       # e.g., "Q1-Q4"
    kpis: list[str]     # Key performance indicators

@dataclass
class StrategyResult:
    decision_type: str  # "strategy", "key_tasks", "execution"
    title: str
    summary: str
    items: list[StrategyItem]
    metrics: dict
```

## Example Output

### Five Looks Analysis Sample

```
════════════════════════════════════════════════════════════════
  市场洞察 (Look at Market)
════════════════════════════════════════════════════════════════

  [关键指标]
    • total_subscribers_million: 1700.0
    • 5g_penetration_pct: 45.2
    • market_growth_pct: 8.5
    • avg_churn_pct: 1.45

  [洞察发现]
    • 市场总用户规模: 1700M
    • 5G用户渗透率: 45.2%
    • 市场平均流失率: 1.45%
    • 分析期间市场增长: 8.5%
    • 增长最快细分市场: Cloud & IT (25.3% YoY)

  [行动建议]
    → 持续关注5G用户迁移速度和价值提升
    → 重点发展数字化转型等新兴业务板块
    → 优化存量用户经营，降低流失率
```

### Three Decisions Strategy Sample

```
════════════════════════════════════════════════════════════════
  定策略 (Define Strategy)
════════════════════════════════════════════════════════════════

  [策略概要]
    China Mobile 战略规划:
    1. 【增长战略】巩固领先地位，通过差异化服务和生态建设维持份额
    2. 【竞争战略】持续强化网络覆盖核心优势，扩大领先差距
    3. 【数字化转型战略】加速5G网络建设和用户迁移
    4. 【客户经营战略】深化客户价值经营，提升用户ARPU

  [具体举措]
    [P0] 增长战略
         巩固领先地位，通过差异化服务和生态建设维持份额
         KPI: 市场份额保持>40%, 新业务收入占比>15%

    [P0] 竞争战略
         持续强化核心优势，扩大领先差距，同时补齐短板
         KPI: 核心优势维度保持领先10分以上, 短板维度缩小差距5分
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run BLM module tests only
pytest tests/test_blm.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Adding Custom Operators

```python
from src.blm.telecom_data import GLOBAL_OPERATORS, OperatorProfile

# Add to registry
GLOBAL_OPERATORS["MyTelco"] = {
    "country": "MyCountry",
    "region": "MyRegion",
    "type": "challenger",
}

# Or create profile directly
profile = OperatorProfile(
    name="MyTelco",
    country="MyCountry",
    region="MyRegion",
    operator_type="challenger",
    market_position=2,
)
```

## Configuration

Edit `config/default.yaml` to customize analysis parameters:

```yaml
analysis:
  trend_frequency: "QE"  # Quarterly
  anomaly_threshold: 2.0

output:
  default_format: "html"
  charts_enabled: true
```

## Requirements

- Python 3.9+
- pandas, numpy, matplotlib, seaborn
- jinja2, click, pyyaml
- openpyxl (for Excel support)
- pdfplumber (for PDF support)

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Submit a pull request

---

*BLM (Business Leadership Model) is a strategic planning framework. This tool is designed for educational and business analysis purposes.*
