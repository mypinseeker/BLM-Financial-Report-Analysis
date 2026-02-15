# Changelog

All notable changes to the BLM Strategic Analysis project are documented in this file.

## [v3.0.0] — 2026-02-15

**21-Market Global Coverage — PDF Reports + NJJ Group Rollout**

### TP-20: NJJ Group BLM Reports (`ac6b4a6`)
- 5 new markets: Switzerland (Salt), Ireland (eir), Ukraine (lifecell), Cyprus (Epic), Malta (Epic)
- 5 market configs, 5 seed files, 15 new operators, 6 parent groups in operator directory
- Seed orchestrator expanded: 17 → 22 markets, 71 total operators
- Full Five Looks + SWOT + SPAN + Three Decisions per operator

### PDF Report Generation (`b1eff97`, `56f22fc`)
- All 21 markets now have PDF versions of MD strategic insight reports
- WeasyPrint-based conversion: A4 layout, styled tables, page headers/footers, page numbers
- Germany and Chile reports regenerated with standardized naming convention
- Every market now ships 4 files: JSON + MD + PDF + PPTX

### Market Coverage (21 markets total)
| Group | Markets |
|-------|---------|
| Flagship | Germany (Vodafone), Chile (Entel) |
| Millicom/Tigo (10) | Guatemala, Colombia, Honduras, Paraguay, Bolivia, El Salvador, Panama, Nicaragua, Ecuador, Uruguay |
| Iliad (3) | France (Free), Italy (Iliad), Poland (Play) |
| NJJ (5) | Switzerland (Salt), Ireland (eir), Ukraine (lifecell), Cyprus (Epic), Malta (Epic) |
| Other Europe (2) | Netherlands (Odido), Belgium (Proximus) |

---

## [v2.5.0] — 2026-02-15

**TP-18/19: European Market Expansion — Iliad + Benelux**

### TP-19: Iliad Group BLM Reports (`fbfa215`)
- France (Free/Iliad), Italy (Iliad Italia), Poland (Play/P4)
- 3 market configs with full BMC enrichments, PEST context, competitive landscape
- 3 seed files with IR-sourced financials, intelligence events, earnings highlights

### TP-18: Netherlands & Belgium (`5dded84`, `f630a98`)
- Netherlands (Odido vs KPN/VodafoneZiggo), Belgium (Proximus vs Orange/Telenet)
- IR-sourced financials replacing initial estimates

### TP-17: Interactive Web Dashboard (`628586f`)
- Report viewer page with per-market download links (JSON/MD/PPTX)
- Market audit page with interactive operator selection
- Dashboard redesign with market grid cards

---

## [v2.0.0] — 2026-02-14

**Multi-Quarter Trends, Feedback Loop, and 12-Market Group Reports**

### TP-15: Multi-Quarter Trend Analysis (`dea08ef`)
- `trend_analyzer.py`: CAGR, momentum score (0–100), volatility (CoV), trend slope (OLS), acceleration, seasonality detection
- Engine: financial health + 5 segments enriched in look_at_self, competitor revenue/margin metrics in look_at_competition
- MD: Momentum Dashboard in Exec Summary, Financial Trend Metrics in Self Analysis
- PPT: Health Check CAGR+phase annotation, new Momentum Dashboard slide

### TP-16: Market Share Trend Analysis (`33e789f`)
- Share evolution tracking across quarters for mobile, broadband, and TV segments

### TP-13: Draft→Final Feedback Loop (`9072f17`)
- FindingExtractor: walks JSON, extracts findings from all 6 look categories
- Web UI: tabbed feedback interface (6 tabs), per-finding type/comment/value
- MD generator: feedback-aware filtering (disputed/modified/supplemented/confirmed)
- PPT generator: key_message_overrides from user feedback
- analysis_runner: `generate_final_outputs()` method for post-feedback regeneration

### P1-5: User Feedback Persistence (`eb29f54`)
- UserFeedback model with analysis_job_id, operator_id, period
- SQLite + Supabase CRUD (upsert/query/clear)
- CLI: `python3 -m src.cli_analyze feedback {add,list,export,clear}`

### TP-14: Batch Data Ingestion CLI (`b1e4c87`)
- CLI for ingesting LATAM market data from consolidated PDF reports

### TP-12: Group Report + Supabase Push (`09306ff`)
- `seed_orchestrator.py` + `cli_group_local.py` — 11-market Millicom group summary
- `cli_push_all.py` — bulk seed+push to Supabase (1,958 rows, 12 tables)
- ProvenanceStore: `save_to_db()`/`load_from_db()` for provenance persistence

---

## [v1.5.0] — 2026-02-13

**Three Decisions, Millicom Rollout, and Tech Debt Cleanup**

### TP-10: Three Decisions — BLM Phase 2 (`0444344`)
- ThreeDecisionsComputer: rule-based, 3 decisions from FiveLooks + Diagnosis
- 7 dataclasses, 4 PPT slides, MD Module 06
- 731 tests pass

### TP-11: Millicom 11-Country Rollout (`71bca27`)
- `seed_latam_helper.py` shared seeder + 10 seed files
- 2 new configs (Ecuador, Uruguay) + 8 enriched configs
- 12 markets, 38 operators, 304 financial records, all produce MD+PPT

### TP-9: Tech Debt Cleanup (`ed5437e`)
- 4 sprints of code quality improvements

### TP-8: Chile MD Regeneration (`3ab0ad2`)
- Regenerated Chile report with latest engine improvements

---

## [v1.2.0] — 2026-02-12

**BLM Strategic Insight Report (MD) + Market Audit + Data Gaps**

### TP-7: MD Strategic Report Generator (`6450b76`, `bcb0121`, `216a24d`)
- BLMMdGenerator orchestrator + 8 module renderers + StrategicDiagnosisComputer
- Rule-based diagnosis: "The Squeezed Middle", "The Distant Second", etc.
- Polishing Sprint 1: 9 fixes (raw dicts, revenue formatting, P0 tiering)
- Polishing Sprint 2: 10 fixes (SPAN tiering, PEST dedup, headline numbers)

### TP-6: Fill Data Gaps (`cdce1e5`)
- 10 new fields: homepass_vs_connect, controlled_vs_resale, evolution_strategy, vs_competitors, consumer/b2b/cost impact, attributions, action_required, org_culture
- `operator_network_enrichments` in MarketConfig

### TP-5: Market Readiness Audit (`a8183be`, `dd0338a`)
- MarketAuditService: 3-layer audit (Data/Analysis/Provenance), scored/graded A–F
- CLI + API endpoints
- Fix: AUDIT_TABLES column name mismatches + case-sensitive market filter

---

## [v1.1.0] — 2026-02-11

**Engine Quality + AI Data Extraction Pipeline**

### TP-4: Engine Quality Improvements (4 sprints)
- Sprint 1 (`17bbdd3`): 8 quick wins — Chile data, segment fields, scale auto-detect
- Sprint 2 (`67aafdc`): 6 items — relative scoring, revenue B/T format, fuzzy dedup
- Sprint 3 (`aea9252`): 4 items — SPAN matrix overhaul, provenance wiring, SWOT filter
- Backlog (`e01e514`): revenue formatting, competitor deep-dive enrichment

### TP-3: Analysis Execution + Report Generation (`aa236b0`)
- AnalysisRunnerService: Pull-to-SQLite → BLMAnalysisEngine → 5 output formats → Supabase upload
- GroupSummaryGenerator: cross-market comparison
- CLI: `python3 -m src.cli_analyze {single,group,list,status,audit}`

### TP-2: AI Data Extraction Pipeline (`3cf5c8b`)
- GeminiService (httpx REST), ExtractionService, 6 extraction prompts
- 7 API endpoints, Review UI, 5-table upsert with provenance

### TP-1: Object Selection Wizard (`9fac46a`)
- Multi-market data model, operator selection UI

---

## [v1.0.0] — 2026-02-10

**First production release — Vodafone Germany BLM Strategic Assessment (CQ4 2025)**

### Deep Analysis Output Layer
- New `generate_deep_ppt.py` — 48-slide deep analysis PPT directly from 8 MD modules
- New `deep_data_extractor.py` — structured data extraction from markdown analysis files
- New `md_parser.py` — markdown table/list/metric parsing utilities
- All 16 chart types utilized (radar, SPAN bubble, Porter's Five Forces, SWOT matrix, etc.)
- Operator brand color system — DT magenta, VF red, O2 blue, 1&1 navy

### 8 Deep Analysis Modules (~2,700 lines total)
- `executive_summary_cq4_2025.md` — capstone with Squeezed Middle diagnosis
- `trends_deep_analysis_cq4_2025.md` — PEST macro environment (8 sections)
- `market_customer_deep_analysis_cq4_2025.md` — $APPEALS + 7 segments
- `tariff_deep_analysis_h1_2026.md` — 466 tariff records, EUR/GB ranking
- `competition_deep_analysis_cq4_2025.md` — Porter's Five Forces + competitor deep dives
- `self_analysis_deep_cq4_2025.md` — 9 sections, 320+ lines, CQ trend data
- `swot_deep_analysis_cq4_2025.md` — SWOT synthesis + SO/WO/ST/WT strategies
- `opportunities_deep_analysis_cq4_2025.md` — SPAN matrix, 21 opportunities

### Consolidated Outputs
- `blm_vodafone_germany_full_analysis_cq4_2025.md` — all 8 modules merged (2,887 lines, 153 KB)
- `blm_vodafone_germany_full_analysis_cq4_2025.pdf` — professional PDF (85 pages, A4, chaptered)
- `blm_vodafone_germany_deep_analysis.pptx` — final PPT (48 slides, 34 charts, ~2.9 MB)

### Visual Quality Improvements
- Operator brand colors across all multi-operator charts
- SPAN bubble chart: 21 curated positions spanning full 3.5–9.0 range
- Improved bar chart sizing with value labels
- Text-heavy slides: increased font sizes (12–14pt from 10–11pt)

### Calendar Quarter Normalization
- Replaced sequential Q1–Q8 labels with absolute calendar quarters (CQ1'24–CQ4'25)
- Updated both MD source files and PPT chart x-axes

---

## [v0.5.0] — 2026-02-08

**V5 draft with tariff analysis integration**

- Tariff analysis slides integrated into PPT (4 new slides, 46 total)
- `tariff_deep_analysis_h1_2026.md` added as PPT input
- Commit: `483fe36`

## [v0.4.0] — 2026-02-07

**V4 with MarketConfig global adaptation engine**

- MarketConfig system — dataclass + registry for multi-market support
- Germany config: 7 segments, 4 operator BMC enrichments, PEST context
- Tariff data pipeline: 466 records (4 ops × 7 periods × 7 types)
- 32 new tests (15 tariff + 17 market config), 606 total passing
- Commit: `006dac0`

## [v0.3.0] — 2026-02-06

**V3 draft with enhanced charts**

- Gap analysis chart + revenue comparison added (5 new charts)
- 41 slides, 21 charts
- Commit: `75b8351`

## [v0.2.0] — 2026-02-05

**V2 full rewrite with BLM engine**

- New Five Looks analysis engine + Three Decisions framework
- All-English output, KPI formatting
- 39 slides, 16 charts
- Commit: `bacd9bc`

## [v0.1.0] — 2026-02-04

**V1 legacy generator**

- Initial PPT generator with Chinese text
- 22 slides, ~6 charts
