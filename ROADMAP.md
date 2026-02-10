# ROADMAP.md — BLM Five Looks Analysis Engine

## Current Status (2026-02-10)

All milestones **COMPLETE**. Project archived as **v1.0.0**.

```
M0  Project Infrastructure     ████████████████████  DONE
M1  Data Layer                 ████████████████████  DONE
M2  Five Looks Engine          ████████████████████  DONE
M3  Output Layer               ████████████████████  DONE
M4  Integration & Testing      ████████████████████  DONE
M5  Global Market Adaptation   ████████████████████  DONE  (9decb30)
M6  Deep Analysis Pipeline     ████████████████████  DONE  (v1.0.0)
```

### Latest Output: v1.0.0 Deep Analysis
- **PPT**: `data/output/blm_vodafone_germany_deep_analysis.pptx` — 48 slides, 34 charts
- **PDF**: `data/output/blm_vodafone_germany_full_analysis_cq4_2025.pdf` — 85 pages, A4
- **MD**: `data/output/blm_vodafone_germany_full_analysis_cq4_2025.md` — 2,887 lines
- **Tag**: `v1.0.0` on `main`

---

## Version History

| Version | Commit | Slides | Charts | Key Changes |
|---------|--------|--------|--------|-------------|
| V1 | (legacy) | 22 | ~6 | Legacy generator, Chinese text |
| V2 | `bacd9bc` | 39 | 16 | New engine, all English, KPI formatting |
| V3 | `75b8351` | 41 | 21 | Gap analysis, revenue comparison, 5 new charts |
| V4 | `006dac0` | 41 | 21 | MarketConfig global adaptation, 466 tariff records, data-driven BMC/exposures |
| V5 | `483fe36` | 46 | — | Tariff analysis slides integrated |
| **v1.0.0** | `e1dfe66` | **48** | **34** | **Deep analysis PPT from 8 MDs, brand colors, PDF/MD consolidation** |

---

## M5: Global Market Adaptation (DONE — `9decb30`)

### What was delivered
- **MarketConfig system** — `src/models/market_config.py` dataclass + registry in `src/models/market_configs/`
- **Germany config** — 7 customer segments, 4 operator BMC enrichments, 4 operator exposure profiles, PEST context, competitive landscape notes (all migrated from hardcoded data)
- **Tariff data pipeline** — schema with `snapshot_period` + historical UNIQUE constraint, `upsert_tariff()` / `get_tariffs()` / `get_tariff_comparison()` in db.py
- **466 German tariff records** — 4 operators × 7 half-year snapshots (H1_2023–H1_2026) × 7 plan types (mobile postpaid/prepaid, fixed DSL/cable/fiber, TV, FMC bundle)
- **Engine refactored** — `look_at_market_customer.py` and `look_at_self.py` read from MarketConfig instead of hardcoded data; fallback preserved for backward compatibility
- **32 new tests** — 15 tariff data + 17 market config, all passing

### Adding a new market (zero engine code changes)
```python
# 1. Create src/models/market_configs/uk.py → UK_CONFIG
# 2. Create src/database/seed_uk.py → operators + tariffs
# 3. Register in src/models/market_configs/__init__.py
# Then:
engine = BLMAnalysisEngine(db, target_operator='vodafone_uk', market='uk', ...)
result = engine.run_five_looks()  # uses UK config automatically
```

---

## M6: Deep Analysis Pipeline (DONE — v1.0.0)

### What was delivered
- **8 deep analysis markdown modules** — ~2,700 lines of strategic analysis covering all BLM Five Looks
- **Deep PPT generator** — `generate_deep_ppt.py` generates 48 slides with 34 charts directly from MD content
- **MD parsing library** — `md_parser.py` + `deep_data_extractor.py` for structured data extraction
- **Operator brand colors** — OPERATOR_BRAND_COLORS registry in `ppt_styles.py`, used across all multi-operator charts
- **Calendar quarter normalization** — CQ1'24–CQ4'25 absolute labels replacing sequential Q1–Q8
- **Consolidated outputs** — full analysis MD (2,887 lines), chaptered PDF (85 pages), final PPT (48 slides)
- **16 chart types utilized** — all including SPAN bubble, Porter's Five Forces, SWOT matrix, $APPEALS radar

### Key commits
```
e1dfe66 Add PDF version of full analysis (85 pages, A4, chaptered)
59e3c43 Add consolidated full analysis document (8 modules, ~2,800 lines)
2885d1b Improve PPT visual quality: brand colors, SPAN layout, text sizing
411f617 Replace Q1-Q8 sequential labels with calendar quarters (CQ1'24–CQ4'25)
9495773 Add deep analysis PPT generator — 48 slides, 34 charts from 8 MD files
1036a7d Add Executive Summary — BLM Strategic Assessment capstone
```

---

## Next Phase: Data Enrichment & Quality

### P0 — Data Gaps (Impact: Analysis Quality)

| ID | Task | Impact | Status |
|----|------|--------|--------|
| P0-1 | ~~Fill tariffs table~~ — 466 tariff records (4 ops × 7 periods × 7 types), upsert/query/comparison methods | ~~$APPEALS Price dimension lacks real pricing data~~ | **DONE** `9decb30` |
| P0-2 | **Populate CompetitorDeepDive fields** — 12 fields never filled (product_portfolio, growth_strategy, business_model, org_structure, etc.) | Competitor slides show limited content | Open |
| P0-3 | **Populate SelfInsight fields** — 6 fields empty (customer_perception, performance_gap, opportunity_gap, talent_assessment, leadership_changes, strategic_review) | Org & Talent slide sparse; gap analysis concepts missing | Open |

### P1 — Output Quality

| ID | Task | Impact | Files |
|----|------|--------|-------|
| P1-1 | **Persist data_provenance** — ProvenanceStore only in-memory; add save_to_db/load_from_db | No audit trail across runs | `provenance.py`, `db.py` |
| P1-2 | **Fill NetworkAnalysis 7 fields** — controlled_vs_resale, homepass_vs_connect, evolution_strategy, vs_competitors, consumer_impact, b2b_impact, cost_impact | Network slide lacks strategic depth | `self_analysis.py`, `look_at_self.py` |
| P1-3 | **Use remaining 4 chart types** — radar_chart, stacked_bar, heatmap, timeline_chart | 4 of 18 chart types still unused | `ppt_generator.py`, `ppt_charts.py` |
| P1-4 | **Clean seed data language** — intelligence_events has mixed Chinese/English descriptions | JSON/HTML/TXT outputs show mixed language | `seed_internet_data.py` |
| P1-5 | **Implement user_feedback persistence** — Add upsert_feedback() + CLI command | Draft->Final loop lacks persistence | `feedback.py`, `db.py` |

### P2 — Tech Debt

| ID | Task | Impact | Files |
|----|------|--------|-------|
| P2-1 | **Remove 12 legacy file duplicates** — src/blm/ root vs src/blm/_legacy/ | Maintainability risk | 12 files in `src/blm/` |
| P2-2 | **Add openpyxl to requirements.txt** | 3 test failures | `requirements.txt` |
| P2-3 | **Differentiate SPAN bubble sizes** — addressable_market always "N/A", bubble_size always 2.0 | SPAN chart lacks visual hierarchy | `look_at_opportunities.py` |
| P2-4 | **Add "Three Decisions" slides** — Strategy/Key Tasks/Execution (BLM Phase 2) | BLM framework incomplete | New module needed |
| P2-5 | ~~Multi-market support~~ — MarketConfig registry + data-driven segments/BMC/exposures; new market = config + seed only | ~~Cannot analyze other markets~~ | **DONE** `9decb30` |

---

## Chart Usage Status (18 types)

| Chart Type | Status | Used In |
|------------|--------|---------|
| `create_bar_chart` | Used | Health Check, Segments, Customer Segments, Revenue Comp |
| `create_horizontal_bar_chart` | Used | Market Share, Revenue Comparison |
| `create_multi_line_trend` | Used | Revenue Trend |
| `create_kpi_table_chart` | Used | Competition Summary |
| `create_donut_gauges` | Used | Network Coverage |
| `create_priority_chart` | Used | Opportunity Priorities |
| `create_pest_dashboard` | Used | PEST Dashboard |
| `create_porter_five_forces` | Used | Porter's Five Forces |
| `create_swot_matrix` | Used | SWOT Analysis |
| `create_appeals_radar` | Used | $APPEALS Assessment |
| `create_bmc_canvas` | Used | Business Model Canvas |
| `create_span_bubble_chart` | Used | SPAN Matrix |
| `create_gap_analysis_chart` | Used | Gap Analysis (V3) |
| `create_segment_comparison` | Used | PEST Factor Distribution (V3) |
| `create_radar_chart` | Used | Competition radar (deep PPT) |
| `create_stacked_bar` | **Unused** | Could show revenue composition over time |
| `create_heatmap` | **Unused** | Could visualize operator-to-operator user flow |
| `create_timeline_chart` | **Unused** | Could show opportunity action timeline |

---

## Quick Start

```python
from src.database.db import TelecomDatabase
from src.blm.engine import BLMAnalysisEngine
from src.output.ppt_generator import BLMPPTGenerator
from src.output.ppt_styles import get_style

db = TelecomDatabase("data/telecom.db")
db.init()
engine = BLMAnalysisEngine(db, target_operator='vodafone_germany',
                           market='germany', target_period='CQ4_2025')
result = engine.run_five_looks()

gen = BLMPPTGenerator(style=get_style("vodafone"), operator_id="vodafone_germany",
                      output_dir="data/output", chart_dpi=150)
path = gen.generate(result, mode="draft",
                    filename="blm_vodafone_germany_q3fy26_v4_draft.pptx")
```

## Test

```bash
python3 -m pytest tests/ --tb=short  # 606 passed, 2 openpyxl failures (unrelated)
```
