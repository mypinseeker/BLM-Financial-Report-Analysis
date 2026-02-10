# Changelog

All notable changes to the BLM Strategic Analysis project are documented in this file.

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
