# ROADMAP.md — BLM Five Looks Analysis Engine

## Current Status (2026-02-10)

All original milestones (M0-M4) are **COMPLETE**.

```
M0  Project Infrastructure     ████████████████████  DONE
M1  Data Layer                 ████████████████████  DONE
M2  Five Looks Engine          ████████████████████  DONE
M3  Output Layer               ████████████████████  DONE
M4  Integration & Testing      ████████████████████  DONE
```

### Latest Output: V3 Draft PPT
- **File**: `data/output/blm_vodafone_germany_q3fy26_v3_draft.pptx`
- **41 slides | 21 charts | 1.6 MB | 574 tests passing**
- **Commit**: `75b8351` on `main`

---

## Version History

| Version | Commit | Slides | Charts | Key Changes |
|---------|--------|--------|--------|-------------|
| V1 | (legacy) | 22 | ~6 | Legacy generator, Chinese text |
| V2 | `bacd9bc` | 39 | 16 | New engine, all English, KPI formatting |
| V3 | `75b8351` | 41 | 21 | Gap analysis, revenue comparison, 5 new charts |

---

## Next Phase: Data Enrichment & Quality

### P0 — Data Gaps (Impact: Analysis Quality)

| ID | Task | Impact | Files |
|----|------|--------|-------|
| P0-1 | **Fill tariffs table** — Add seed data, upsert/query methods; wire into $APPEALS Price scoring | $APPEALS Price dimension lacks real pricing data | `db.py`, `seed_germany.py`, `look_at_market_customer.py` |
| P0-2 | **Populate CompetitorDeepDive fields** — 12 fields never filled (product_portfolio, growth_strategy, business_model, org_structure, etc.) | Competitor slides show limited content | `competition.py`, `look_at_competition.py` |
| P0-3 | **Populate SelfInsight fields** — 6 fields empty (customer_perception, performance_gap, opportunity_gap, talent_assessment, leadership_changes, strategic_review) | Org & Talent slide sparse; gap analysis concepts missing | `self_analysis.py`, `look_at_self.py` |

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
| P2-5 | **Multi-market support** — Currently Germany-only; hardcoded in 4+ modules | Cannot analyze other markets | Multiple files |

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
| `create_radar_chart` | **Unused** | Could enhance competition comparison |
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
                    filename="blm_vodafone_germany_q3fy26_v3_draft.pptx")
```

## Test

```bash
python3 -m pytest tests/ --tb=short  # 574 passed, 2 openpyxl failures (unrelated)
```
