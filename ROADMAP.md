# ROADMAP.md — BLM Five Looks Analysis Engine

## Current Status (2026-02-14)

Engine v1.0.0 complete. Thirteen enhancement task packages (TP-1 through TP-13) delivered,
adding Supabase cloud pipeline, AI extraction, multi-market analysis, engine quality
improvements, market readiness audit, data gap remediation, MD strategic reports, Three
Decisions (BLM Phase 2), full Millicom group rollout, group cross-market report, Supabase
bulk push, data provenance persistence, and Draft→Final feedback loop.

```
M0  Project Infrastructure     ████████████████████  DONE
M1  Data Layer                 ████████████████████  DONE
M2  Five Looks Engine          ████████████████████  DONE
M3  Output Layer               ████████████████████  DONE
M4  Integration & Testing      ████████████████████  DONE
M5  Global Market Adaptation   ████████████████████  DONE  (9decb30)
M6  Deep Analysis Pipeline     ████████████████████  DONE  (v1.0.0)
TP-1  Cloud Pipeline + Wizard  ████████████████████  DONE  (2026-02-10)
TP-2  AI Data Extraction       ████████████████████  DONE  (2026-02-10)
TP-3  Analysis Execution       ████████████████████  DONE  (2026-02-11)
TP-4  Engine Quality (18 items)████████████████████  DONE  (2026-02-11)
TP-5  Market Readiness Audit   ████████████████████  DONE  (2026-02-12)
TP-6  Fill Data Gaps (10 flds) ████████████████████  DONE  (2026-02-12)
TP-7  MD Strategic Reports     ████████████████████  DONE  (2026-02-12)
TP-8  Chile MD + Housekeeping  ████████████████████  DONE  (2026-02-13)
TP-9  Tech Debt Cleanup        ████████████████████  DONE  (2026-02-13)
TP-10 Three Decisions (Phase 2)████████████████████  DONE  (2026-02-13)
TP-11 Millicom 11-Country Roll ████████████████████  DONE  (2026-02-14)
TP-12 Group Report + Push + Prov████████████████████  DONE  (2026-02-14)
TP-13 Draft→Final Feedback Loop ████████████████████  DONE  (2026-02-14)
TP-14 Real Data Ingestion CLI   ████████████████████  DONE  (2026-02-14)
```

### Latest Reports: CQ4_2025
- **12 markets analyzed**: Germany, Chile, Guatemala, Colombia, Honduras, Paraguay, Bolivia, El Salvador, Panama, Nicaragua, Ecuador, Uruguay
- **38 operators** across all markets, **304 financial quarterly** + **subscriber quarterly** records
- **Output formats**: JSON, TXT, HTML, PPTX, MD (Five Looks + Three Decisions) + Final mode (PPTX/MD with feedback)
- **Group report**: 10-market Millicom cross-market summary (JSON + TXT) with subscriber data
- **Feedback loop**: Web UI for reviewing findings → persist feedback → regenerate final reports
- **Audit scores**: Germany 97/A, Chile 92/A
- **Tests**: 800 passing (as of TP-13)

---

## Task Package History

### TP-1: Cloud Pipeline + Object Selection Wizard (2026-02-10)
- FastAPI + Jinja2 web app, Supabase (PostgreSQL) backend
- Object selection wizard for multi-market analysis
- Routers: markets, operators, outputs, cloud, groups, analyze, data_extract, audit, pages
- 40 total API routes, Vercel deployment via `api/index.py`

### TP-2: AI Data Extraction Pipeline (2026-02-10)
- GeminiService (httpx REST, no SDK), ExtractionService, 6 extraction prompts
- 7 API endpoints: `/api/extract/{discover,download,run,{id},approve,reject,list}`
- Review UI: `/review` + `/review/{job_id}` (editable tables, confidence colors)
- SupabaseDataService: extraction CRUD, 5-table upsert, provenance tracking
- extraction_jobs table SQL

### TP-3: Analysis Execution + Report Generation (2026-02-11)
- AnalysisRunnerService: Pull-to-SQLite → BLMAnalysisEngine → 5 output formats → Supabase upload
- GroupSummaryGenerator: cross-market comparison (revenue, subs, competitive position)
- CLI: `python3 -m src.cli_analyze {single,group,list,status,audit}`
- Web: `POST /api/analyze/{id}/execute` + auto-trigger via BackgroundTasks
- analyze.html: download links, re-execute button, phase-labeled progress

### TP-4: Engine Quality Improvements (2026-02-11) — 18 items, 4 sprints
- **Sprint 1** (8 quick wins): Chile data population, segment fields, scale auto-detect
- **Sprint 2** (6 items): Relative scoring, revenue B/T format, fuzzy dedup (intel, Five Forces, SWOT, mgmt commentary)
- **Sprint 3** (4 items): SPAN matrix overhaul (real scores, 4 quadrants), provenance wiring, SWOT opportunity filter, PEST company_impact
- **Backlog** (3 items): `_fmt_rev()` revenue formatting (M/B/T), competitor deep-dive enrichment (growth_strategy, problems, product_portfolio, business_model, ma_activity)
- Commits: `17bbdd3` → `67aafdc` → `aea9252` → `e01e514`

### TP-5: Market Readiness Audit (2026-02-12)
- MarketAuditService: 3-layer audit (Data/Analysis/Provenance), scored/graded reports
- CLI: `python3 -m src.cli_analyze audit --market X --reference Y --period CQ4_2025`
- API: `GET /api/audit/{market}?operator=X&reference=Y&ref_operator=Z`
- Scoring: 0.35×data + 0.45×analysis + 0.20×provenance → A/B/C/D/F grade
- Commits: `a8183be`, `dd0338a` (audit fix)

### TP-6: Fill Data Gaps (2026-02-12) — 10 fields
- **NetworkAnalysis** (7 fields): homepass_vs_connect (enhanced with penetration), controlled_vs_resale, evolution_strategy, vs_competitors, consumer_impact, b2b_impact, cost_impact
- **SegmentAnalysis** (2 fields): attributions (per segment from earnings+intel+changes), action_required (URGENT/MONITOR/SUSTAIN/GROW/MAINTAIN)
- **SelfInsight** (1 field): org_culture (leadership stability + strategic orientation + config)
- New MarketConfig field: `operator_network_enrichments` (Germany 4 ops, Chile 5 ops)
- Commit: `cdce1e5`

### TP-7: BLM Strategic Insight Report Generation — MD (2026-02-12)
- BLMMdGenerator: orchestrator + 8 module renderers + StrategicDiagnosisComputer
- Architecture: `md_generator.py` → `strategic_diagnosis.py` + `md_utils.py` + `md_modules/{8 files}`
- StrategicDiagnosis: rule-based (no AI), produces central_diagnosis_label, verdict, priorities, traps, risk/reward, KPI dashboard
- Labels: "The Squeezed Middle", "The Distant Second", "The Competitive Challenger", etc.
- Modules: ES(exec summary), 01(trends/PEST), 02(market/$APPEALS), 02a(tariff), 03(competition/Porter), 04(self/BMC), SW(SWOT), 05(opportunities/SPAN)
- Integrated into analysis_runner as 5th output format (JSON/TXT/HTML/PPT/MD)
- Germany: 2,206 lines / 98KB, Chile: 1,968 lines / ~75KB
- 671 tests pass (62 new + 609 existing), zero regressions
- **Polishing Sprint 1** (`bcb0121`): 9 fixes — raw dicts, revenue formatting, priority labels, duplicate net_assessment, SO/WO labels, P0 tiering, source dedup
- **Polishing Sprint 2** (`216a24d`): 10 fixes — period "unknown", SPAN tiering, PEST dedup, headline numbers, segment metrics, TV casing, escape routes, operator_id→display name
- Commits: `6450b76` → `bcb0121` → `216a24d` → `b5c5b8c`

### TP-8: Chile MD Regeneration + Comprehensive Housekeeping (2026-02-13)
- Chile MD report regenerated from 287 lines (old format) to 1,968 lines (new BLMMdGenerator)
- ROADMAP.md updated: added TP-7/TP-8 docs, fixed P1-4 status, test count, audit scores, output format count
- Confirmed P1-4 (seed data language) already complete (commit `9207312`)

### TP-9: Tech Debt Cleanup (2026-02-13) — 4 sprints
- **Sprint 1** (P2-2): Added 10 missing packages to requirements.txt (openpyxl, python-pptx, pandas, numpy, matplotlib, seaborn, click, pyyaml, pdfplumber, tabula-py)
- **Sprint 2** (P2-3): SPAN bubble size differentiation — replaced hardcoded 1.0 with MA×CP formula (range 0.3–3.0, 9 unique sizes)
- **Sprint 3** (P1-3): Integrated `create_stacked_bar` for Revenue Composition Trend slide; confirmed `create_timeline_chart` already used in deep PPT; deferred `create_heatmap` (needs churn data)
- **Sprint 4** (P2-1): Deleted 12 root-level legacy duplicate files (434KB dead code); `src/blm/` reduced to 9 core files

### TP-10: Three Decisions — BLM Phase 2 (2026-02-13)
- Data model: `src/models/decisions.py` — 7 dataclasses (StrategicPillar, StrategyDecision, KeyTask, KeyTasksDecision, Milestone, GovernanceItem, ExecutionDecision, ThreeDecisions)
- Engine: `src/blm/three_decisions_engine.py` — ThreeDecisionsComputer: rule-based, FiveLooksResult+Diagnosis → 3 decisions (Strategy 4 pillars, Key Tasks 8 max, Execution quarterly milestones)
- PPT: 4 new slides (divider + strategy + key tasks + execution)
- MD: `src/output/md_modules/decisions.py` — Module 06 renderer, wired into md_generator + TOC
- Tests: `tests/test_three_decisions.py` — 60 tests (models, engine, rank variants, edge cases, MD renderer)
- Total: 731 tests pass, zero regressions

### TP-11: Millicom Group Full Market Rollout — 11 Countries (2026-02-14)
- **Scope**: Seed data + enriched configs for all 11 Millicom/Tigo LATAM markets
- **New infrastructure**: `src/database/seed_latam_helper.py` — shared seeding logic for all markets
- **New markets added**: Ecuador (3 ops), Uruguay (3 ops) — operator_directory, market configs, seed data
- **Seed data created** (10 markets × ~200-400 lines each):
  - Guatemala (3 ops), Colombia (4 ops), Honduras (3 ops), Paraguay (3 ops), Bolivia (3 ops)
  - El Salvador (3 ops), Panama (3 ops), Nicaragua (2 ops), Ecuador (3 ops), Uruguay (3 ops)
- **Market configs enriched** (8 markets): Added operator_bmc_enrichments, operator_exposures, operator_network_enrichments to Guatemala, Colombia, Honduras, Paraguay, Bolivia, El Salvador, Panama, Nicaragua
- **Totals**: 12 markets, 38 operators, 304 financial records, 10 MD reports (1,775–2,074 lines), 10 PPT reports (1.5–1.7 MB each)
- **Bug fix**: PPT stacked bar chart None guard in `ppt_charts.py`
- **Files**: 13 new files (~3,500 lines), 10 modified files (~2,000 lines enrichments)

### TP-12: Group Report + Supabase Push + Provenance Persistence (2026-02-14)
- **Phase 1 — Group Report**: `seed_orchestrator.py` seeds all 12 markets into single SQLite; `cli_group_local.py` runs Five Looks for 11 Tigo operators, generates GroupSummary JSON+TXT
  - Group summary: revenue/subscriber/competitive comparison, common opportunities (47) and threats (7), key findings
  - CLI: `python3 -m src.cli_group_local [--markets X,Y] [--output-dir DIR] [--with-md]`
- **Phase 2 — Supabase Push**: `cli_push_all.py` seeds locally then pushes all 12 markets to Supabase via BLMCloudSync
  - Added `operator_groups` + `group_subsidiaries` to TABLE_CONFIG in `supabase_sync.py`
  - Fixed country capitalization bug: `market.capitalize()` → operator directory lookup (fixes "el_salvador" → "El Salvador")
  - CLI: `python3 -m src.cli_push_all [--markets X] [--dry-run] [--status]`
  - Local totals: 39 operators, 304 financial, 304 subscriber, 350 competitive scores, 706 tariffs, 1 group, 11 subsidiaries
- **Phase 3 — Provenance Persistence**: `ProvenanceStore.save_to_db()` / `load_from_db()` for audit trail across runs
  - Added `analysis_job_id`, `operator_id`, `period`, `value_text`, `unit` columns to `data_provenance` table
  - Wired into `analysis_runner._run_engine()` — auto-saves provenance after each engine run
  - 10 new tests: empty store, sources, tracked values, roundtrip, quality report, job isolation, idempotent, engine integration
- **Bug fix**: `seed_millicom.py` `db.execute()` → `db.conn.execute()` (TelecomDatabase API mismatch)
- **Bug fix**: Subscriber comparison nulls — `_compare_subscribers()` now falls back to `segment_analyses[].key_metrics` for mobile/BB/ARPU data (`d5de0db`)
- **Bug fix**: Removed phantom `tigo_chile` from TIGO_OPERATORS (Millicom doesn't operate in Chile; no seed data existed) — group report now 10 markets (`55d3e4f`)
- **Tests**: 741 passed (731 existing + 10 new), zero regressions

### TP-13: Theme A — Close the Draft→Final Loop (2026-02-14)
- **Goal**: Wire feedback end-to-end — Web UI for reviewing findings → persist feedback → regenerate reports in final mode
- **Phase 1 — Foundation**: `FindingExtractor` walks JSON output, extracts findings from all 6 look categories; `feedback_to_ppt_decisions()` maps all-disputed slides to removal; `feedback_to_key_message_overrides()` extracts modified key messages; `filter_findings_by_feedback()` in md_utils.py handles disputed/modified/supplemented/confirmed
- **Phase 2 — Generators**: MD generator gains `mode`/`feedback` params; 6 module renderers (trends, market, competition, self, SWOT, opportunities) accept `feedback` kwarg and filter findings; PPT generator gains `key_message_overrides` param with `_apply_key_message_overrides()` method
- **Phase 3 — Web Layer**: Feedback router with 3 endpoints (`GET /findings`, `POST /save`, `POST /finalize`); `feedback.html` template (6-tab finding review UI with type/comment/value per finding); feedback page route; `generate_final_outputs()` added to AnalysisRunnerService
- **Data flow**: Completed analysis JSON → FindingExtractor → Tabbed feedback UI → user_feedback table → Final PPT (slide removal + key_message overrides) + Final MD (finding-level filtering)
- **New files**: `finding_extractor.py`, `feedback.py` (router), `feedback.html`, `test_finding_extractor.py`, `test_md_final_mode.py`
- **Modified files**: `md_generator.py`, `md_utils.py`, `ppt_generator.py`, `analysis_runner.py`, `app.py`, `pages.py`, `base.html`, 6 md_modules
- **Tests**: 800 passed (33 new + 767 existing), zero regressions
- **Routes**: 46 total (was 40)

### TP-14: Theme B — Real Data Ingestion for LATAM Markets (2026-02-14)
- **Goal**: CLI tool to batch-extract real financial/subscriber/network data from Millicom's consolidated PDF for all 11 Tigo operators
- **Phase 1 — Prompt Enhancement**: Added `country` parameter to `get_financial_prompt`, `get_subscriber_prompt`, `get_network_prompt` for multi-country PDF context (CONSOLIDATED filter instruction)
- **Phase 2 — Batch CLI**: `src/cli_extract.py` with 5 subcommands:
  - `millicom --pdf-url URL --period CQ4_2025` — extract all 11 Tigo ops from one PDF
  - `single --operator OP [--pdf-url URL]` — extract one operator (PDF or search)
  - `review --operator OP / --all` — print extracted JSON for review
  - `commit --operator OP / --all` — write reviewed JSON to SQLite
  - `status` — show extraction progress
- **Design**: Resumable (JSON checkpoint per operator×table), rate-limited, provenance-tagged, local-first (SQLite)
- **Phase 3 — Wiring**: Threaded `country` kwarg through `ExtractionService.extract_table()`; added `get_non_group_operators()` to operator_directory
- **Data flow**: PDF URL → Gemini upload → per-operator extraction → `data/extraction/{op_id}_{type}.json` → review → SQLite commit
- **New files**: `src/cli_extract.py` (~250 lines), `tests/test_cli_extract.py` (~120 lines)
- **Modified files**: `src/extraction/prompts.py` (+30), `src/web/services/extraction_service.py` (+3), `src/database/operator_directory.py` (+10)

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

---

## Remaining Backlog

### P0 — Data Gaps (Impact: Analysis Quality)

| ID | Task | Status |
|----|------|--------|
| P0-1 | ~~Fill tariffs table~~ | **DONE** `9decb30` |
| P0-2 | ~~Populate CompetitorDeepDive fields~~ — growth_strategy, problems, product_portfolio, business_model, ma_activity | **DONE** TP-4 Backlog `e01e514` |
| P0-3 | ~~Populate SelfInsight 6 fields~~ — customer_perception, performance_gap, opportunity_gap, talent_assessment, leadership_changes, strategic_review | **DONE** TP-4 Sprint 3 `aea9252` |

### P1 — Output Quality

| ID | Task | Impact | Status |
|----|------|--------|--------|
| P1-1 | ~~Persist data_provenance~~ — ProvenanceStore save_to_db/load_from_db + wired into analysis_runner | ~~No audit trail across runs~~ | **DONE** TP-12 |
| P1-2 | ~~Fill NetworkAnalysis 7 fields~~ | ~~Network slide lacks strategic depth~~ | **DONE** TP-6 `cdce1e5` |
| P1-3 | ~~Use remaining chart types~~ — stacked_bar integrated, timeline already used, heatmap deferred | ~~Chart gap~~ | **DONE** TP-9 |
| P1-4 | ~~Clean seed data language~~ — intelligence_events translated to English | ~~Mixed language outputs~~ | **DONE** `9207312` |
| P1-5 | ~~Implement user_feedback persistence~~ — upsert_feedback/get_feedback/clear_feedback + CLI `feedback` subcommand | ~~Draft→Final loop lacks persistence~~ | **DONE** P1-5 |
| P1-6 | ~~Wire Draft→Final loop end-to-end~~ — Web UI, feedback filtering in MD/PPT generators, final report generation | ~~No way to review findings or produce final reports~~ | **DONE** TP-13 |

### P2 — Tech Debt

| ID | Task | Impact | Status |
|----|------|--------|--------|
| P2-1 | ~~Remove 12 legacy file duplicates~~ — deleted root-level dead code (434KB) | ~~Maintainability risk~~ | **DONE** TP-9 |
| P2-2 | ~~Add missing dependencies to requirements.txt~~ — added 10 packages | ~~Deploy failures~~ | **DONE** TP-9 |
| P2-3 | ~~Differentiate SPAN bubble sizes~~ — MA×CP formula, range 0.3–3.0 | ~~No visual hierarchy~~ | **DONE** TP-9 |
| P2-4 | ~~Add "Three Decisions" slides~~ — Strategy/Key Tasks/Execution (BLM Phase 2) | ~~BLM framework incomplete~~ | **DONE** TP-10 |
| P2-5 | ~~Multi-market support~~ | **DONE** `9decb30` |

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
| `create_stacked_bar` | Used | Revenue Composition Trend (TP-9) |
| `create_heatmap` | **Deferred** | Needs user churn data enrichment |
| `create_timeline_chart` | Used | Opportunity Sequencing (deep PPT, M6) |

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
python3 -m pytest tests/ --tb=short  # 800 passed
```
