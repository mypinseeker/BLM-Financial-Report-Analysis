# BLM Strategic Analysis — Vodafone Germany

A Python framework for telecom operator strategic analysis using the **Business Leadership Model (业务领先模型 / BLM)**. Implements the Five Looks (五看) analysis framework with automated PPT, PDF, and markdown output generation.

**Current Release: v1.0.0** — Vodafone Germany BLM Strategic Assessment (CQ4 2025)

## Key Outputs

| Output | File | Size |
|--------|------|------|
| **Deep Analysis PPT** | `data/output/blm_vodafone_germany_deep_analysis.pptx` | 48 slides, 34 charts |
| **Full Analysis PDF** | `data/output/blm_vodafone_germany_full_analysis_cq4_2025.pdf` | 85 pages, A4, chaptered |
| **Full Analysis MD** | `data/output/blm_vodafone_germany_full_analysis_cq4_2025.md` | 2,887 lines, 153 KB |

## Architecture

```
BLM-Financial-Report-Analysis/
├── src/
│   ├── blm/                          # BLM Analysis Engine
│   │   ├── engine.py                 # Main BLM engine orchestrator
│   │   ├── five_looks.py             # Five Looks analysis
│   │   ├── three_decisions.py        # Three Decisions strategy
│   │   ├── look_at_market_customer.py
│   │   ├── look_at_self.py
│   │   ├── look_at_competitors.py
│   │   ├── look_at_trends.py
│   │   └── look_at_opportunities.py
│   ├── models/                       # Data Models
│   │   ├── market_config.py          # MarketConfig dataclass
│   │   └── market_configs/           # Per-market configs (Germany, ...)
│   ├── database/                     # SQLite Data Layer
│   │   ├── db.py                     # TelecomDatabase (operators, tariffs, KPIs)
│   │   └── seed_*.py                 # Data seeding scripts
│   └── output/                       # Output Generation Layer
│       ├── generate_deep_ppt.py      # Deep analysis PPT (48 slides from 8 MDs)
│       ├── deep_data_extractor.py    # Structured data extraction from MD
│       ├── md_parser.py              # Markdown table/list/metric parsing
│       ├── ppt_generator.py          # Base PPT generator (from DB dataclass)
│       ├── ppt_charts.py             # 16 chart types (matplotlib → PNG)
│       └── ppt_styles.py             # Operator brand colors & styles
├── data/
│   ├── output/                       # Generated outputs
│   │   ├── *_deep_analysis.pptx      # Final PPT
│   │   ├── *_full_analysis_*.md      # Consolidated markdown
│   │   ├── *_full_analysis_*.pdf     # Chaptered PDF
│   │   └── *.md (×8)                # Individual analysis modules
│   └── telecom.db                    # SQLite database
├── tests/                            # 606+ tests
├── docs/design/                      # Design documents (10 specs)
├── CHANGELOG.md                      # Version history
└── ROADMAP.md                        # Development roadmap
```

## Deep Analysis Modules (8 files)

The deep analysis pipeline reads from 8 markdown modules covering the BLM Five Looks:

| # | Module | BLM Look | Key Content |
|---|--------|----------|-------------|
| 1 | Executive Summary | Capstone | Squeezed Middle diagnosis, KPI dashboard |
| 2 | Trends (PEST) | Look 1: 看宏观 | Political, Economic, Social, Technology |
| 3 | Market & Customer | Look 2: 看市场 | $APPEALS radar, 7 customer segments |
| 4 | Tariff Analysis | Look 2 深入 | 466 tariffs, EUR/GB ranking, price evolution |
| 5 | Competition | Look 3: 看对手 | Porter's Five Forces, competitor deep dives |
| 6 | Self Analysis | Look 4: 看自己 | 8-quarter trends (CQ1'24–CQ4'25), 9 sections |
| 7 | SWOT Synthesis | Cross-Look | SWOT matrix, SO/WO/ST/WT strategies |
| 8 | Opportunities | Look 5: 看机会 | SPAN matrix, 21 opportunities, priority roadmap |

## PPT Slide Structure (48 slides)

| Slides | Section | Charts |
|--------|---------|--------|
| 1–3 | Cover + TOC + Data Notes | — |
| 4–8 | Executive Summary | Revenue bar, KPI table, priority chart |
| 9–13 | Trends (PEST) | PEST dashboard, horizontal bars, trend lines |
| 14–18 | Market & Customer | $APPEALS radar, segment comparison, gap analysis |
| 19–23 | Tariff Analysis | Grouped bars, EUR/GB ranking, evolution table |
| 24–29 | Competition | Five Forces, competitor cards ×3, radar |
| 30–35 | Self Analysis | Trend lines, bar charts, donut gauges |
| 36–40 | SWOT Synthesis | SWOT matrix, strategy 2×2, gap chart |
| 41–45 | Opportunities | SPAN bubble, priority table, timeline |
| 46–48 | Risk/Benefit + KPI Dashboard + Back Cover | Comparison bars, KPI table |

## Quick Start

### Generate Deep Analysis PPT

```bash
# From project root
python3 -m src.output.generate_deep_ppt

# Output: data/output/blm_vodafone_germany_deep_analysis.pptx
```

### Run BLM Engine (DB-based)

```python
from src.database.db import TelecomDatabase
from src.blm.engine import BLMAnalysisEngine
from src.output.ppt_generator import BLMPPTGenerator
from src.output.ppt_styles import get_style

db = TelecomDatabase("data/telecom.db")
db.init()
engine = BLMAnalysisEngine(
    db, target_operator='vodafone_germany',
    market='germany', target_period='CQ4_2025'
)
result = engine.run_five_looks()

gen = BLMPPTGenerator(
    style=get_style("vodafone"),
    operator_id="vodafone_germany",
    output_dir="data/output",
    chart_dpi=150
)
path = gen.generate(result, mode="draft")
```

### Run Tests

```bash
python3 -m pytest tests/ --tb=short  # 606+ tests
```

## Chart Types (16 used)

Bar, horizontal bar, multi-line trend, grouped segment comparison, KPI table, donut gauges, priority chart, PEST dashboard, Porter's Five Forces, SWOT matrix, $APPEALS radar, radar chart, BMC canvas, SPAN bubble chart, gap analysis chart — all with operator brand colors (DT magenta, VF red, O2 blue, 1&1 navy).

## Adding a New Market

Zero engine code changes required:

```python
# 1. Create src/models/market_configs/uk.py → UK_CONFIG
# 2. Create src/database/seed_uk.py → operators + tariffs
# 3. Register in src/models/market_configs/__init__.py
engine = BLMAnalysisEngine(db, target_operator='vodafone_uk', market='uk')
```

## Requirements

- Python 3.9+
- python-pptx, matplotlib, pandas, numpy
- weasyprint, markdown (for PDF generation)
- SQLite (built-in)

## License

MIT License

---

*BLM (Business Leadership Model) is a strategic planning framework widely used in telecom industry strategic planning.*
