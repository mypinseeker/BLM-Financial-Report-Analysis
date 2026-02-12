# BLM Analysis Engine — Improvement To-Do List

> Generated: 2026-02-11 | Source: QA comparison of Germany vs Chile reports
> Total issues: 24 (2 P0, 7 P1, 11 P2, 4 P3)

---

## P0 — Critical (Must Fix Before New Market Onboarding)

### TP-4A: Fix customer segment cross-contamination [QA-06]
- **File**: `src/blm/look_at_market_customer.py` — `_build_customer_segments()`
- **Problem**: Chile report contains hardcoded Germany competitor references ("O2 aggressive on price", "1&1 limited by network build-out") in competitor_gaps fields
- **Root Cause**: Customer segments loaded from `market_configs.customer_segments` table — if segments were initially copied from Germany template without updating competitor names, the engine passes them through unchanged
- **Fix**: Either (a) clean market_configs data in Supabase, or (b) engine should auto-replace competitor_gaps with operators from the current market, or (c) validate at ingestion that referenced operators exist in the target market
- **Effort**: S (2h)

### TP-4B: Make SPAN matrix produce meaningful differentiation [QA-14, QA-15]
- **File**: `src/blm/look_at_opportunities.py`
- **Problem**: All opportunities receive identical attractiveness/position scores (5.0-5.6). Every opportunity lands in grow_invest quadrant. Harvest and avoid_exit are always empty. The SPAN matrix provides zero prioritization value.
- **Root Cause**: Sub-scores (market_size, profit_potential, market_share, brand_channel, tech_capability) all default to 5.0. Only strategic_value (6-8) and market_growth (5-7) have any variance.
- **Fix**: (a) Feed real market data into attractiveness scoring (market size → actual revenue, growth → actual YoY%); (b) Feed real competitive_scores into position scoring (brand → actual brand score, tech → actual 5G/network score); (c) Use thresholds to place opportunities across all 4 quadrants; (d) SWOT strategies with weak capability match should go to acquire_skills; those addressing declining segments go to harvest
- **Effort**: L (8h)

---

## P1 — High Priority

### TP-4C: Fill Claro Chile competitive_scores in Supabase [QA-01]
- **Problem**: Claro Chile has 0 competitive dimension scores in the DB (after scale normalization, still empty). Movistar has scores but only 1 passes the strength threshold.
- **Fix**: Seed competitive_scores for claro_cl (all dimensions: 5G Deployment, Brand Strength, Network Coverage, Customer Service, etc.) matching the 10 standard dimensions used by Germany operators.
- **Effort**: S (1h)

### TP-4D: Engine should derive competitor weaknesses, not just strengths [QA-04]
- **File**: `src/blm/look_at_competition.py` — `_derive_strengths_weaknesses()`
- **Problem**: No competitor in either market has weaknesses populated. The threshold `< 40` on a 0-100 scale is too strict — even weak operators score 50-60, above the weakness threshold.
- **Fix**: Use relative scoring: if an operator's dimension score is >15 points below market average, flag as weakness. Or use a tertile approach: bottom-third of market = weakness.
- **Effort**: M (3h)

### TP-4E: Fix key_message truncation [QA-08]
- **Files**: `src/blm/look_at_self.py` — `_synthesize_key_message()`, any other key_message builders
- **Problem**: Both Chile and Germany self_analysis.key_message are truncated at ~300 characters mid-sentence ("...reaffirms FY2026 guidanc", "...预计FY27才能真正实现E")
- **Root Cause**: Likely a field length limit in the output model or a string truncation in the key message builder
- **Fix**: Either increase the limit or ensure the message is truncated at a sentence boundary with "..." ellipsis
- **Effort**: S (1h)

### TP-4F: Fix Chile revenue unit inconsistency [QA-10]
- **File**: `src/blm/look_at_trends.py` — `_analyse_industry()`
- **Problem**: Chile industry_market_size says "CLP 1391.0B" but total_revenue is 1,391,000.0M. Germany correctly shows "EUR 12.3B" from total_revenue 12,327.0M. The Trends module divides total_revenue by 1000 to get billions, but Chile revenue is stored in millions of CLP (1,391,000M) → division gives 1391.0B which is wrong — should be 1.391T.
- **Root Cause**: Chile revenue is in CLP millions (large number), Germany revenue in EUR millions (smaller number). The engine assumes all revenue numbers are similar scale.
- **Fix**: Use market_config to define revenue display rules. If the number exceeds 1000B, format as T (trillions). Better: add a `revenue_unit` field to MarketConfig.
- **Effort**: M (3h)

### TP-4G: Deduplicate near-identical intelligence events [QA-13, QA-23]
- **Problem**: "Claro Chile announces $300M..." and "Claro Chile invests $300M..." are the same event with different wording, creating duplicate SWOT threats. Similarly for Movistar FTTH event.
- **Fix**: (a) Clean the duplicate events in Supabase; (b) Add fuzzy dedup in the engine (title similarity > 80% → keep only the latest); (c) Add UNIQUE constraint or similarity check in seed scripts
- **Effort**: M (3h)

### TP-4H: Wire provenance aggregation [QA-17]
- **File**: `src/blm/engine.py` or provenance module
- **Problem**: Provenance section shows 0 sources and 0 high-confidence data points despite dozens of evidence URLs in the report. The provenance system is disconnected from actual data flow.
- **Fix**: Aggregate all source_urls from intelligence_events, earnings_call_highlights, and data_provenance table into the report's provenance section. Count distinct sources. Mark data points with sources as medium/high confidence.
- **Effort**: M (4h)

---

## P2 — Medium Priority

### TP-4I: Seed Tigo Chile competitive_scores [QA-02]
- Even though Tigo is transitioning to MVNO, it should have some scores (at least for brand, pricing)
- **Effort**: XS (30min)

### TP-4J: Populate empty customer segment fields [QA-07]
- Chile "Consumer Postpaid Premium" has empty size_estimate, our_share, opportunity
- Either populate from market_configs or remove skeleton fields
- **Effort**: S (1h)

### TP-4K: Format large revenue numbers for readability [QA-09]
- "CLP 1391000.0M" → "CLP 1.39T" or "CLP 1,391B"
- Apply number formatting based on magnitude
- **Effort**: S (1h)

### TP-4L: Deduplicate SWOT strengths [QA-11]
- Chile has 16 strengths with overlaps (Product Innovation vs Innovation, Customer Service vs Customer Experience)
- Apply same dimension normalization from competitive_scores to SWOT items
- **Effort**: S (2h)

### TP-4M: Filter SWOT opportunities — separate news from strategy [QA-12]
- "Chile GDP growth 2.8%" is macro context, not a strategic opportunity
- Add classification: only include events with strategic action potential
- **Effort**: M (3h)

### TP-4N: Replace PEST company_impact placeholder [QA-24]
- "Potential impact on entel_cl" is a useless placeholder
- Generate meaningful company-specific impact based on event content and operator position
- **Effort**: M (3h)

### TP-4O: Fix SPAN opportunity name truncation [QA-16]
- Names cut at ~60 chars. Increase limit or use intelligent truncation at word boundary
- **Effort**: XS (30min)

### TP-4P: Fix Five Forces key_factor duplication [QA-05]
- Germany new_entrants has "1&1 completes OpenRAN migration" tripled
- Dedup key_factors before adding to PorterForce
- **Effort**: S (1h)

### TP-4Q: Fix Germany management_commentary triplication [QA-21]
- Each earnings highlight appears 3x in the self_analysis output
- Dedup by (segment, content) before outputting
- **Effort**: S (1h)

### TP-4R: Populate competitor deep-dive skeleton fields [QA-22]
- All competitors have empty product_portfolio, growth_strategy, ecosystem_partners, etc.
- Either populate from intelligence_events or remove unused fields to avoid JSON bloat
- **Effort**: L (8h) if populating, XS if removing

### TP-4S: Fix Trends key_message double period [QA-25]
- "...Fiber Broadband Penetration.. Industry is"
- **Effort**: XS (15min)

---

## P3 — Low Priority

### TP-4T: Use display_name in market_shares [QA-18]
- market_shares keys should be "Entel Chile" not "entel_cl"
- **Effort**: XS (30min)

### TP-4U: Include marginal operators in comparison_table [QA-19]
- Tigo Chile excluded from comparison despite being in market
- Show all operators even with 0% share
- **Effort**: XS (30min)

---

## Summary by Effort

| Effort | Count | Items |
|--------|-------|-------|
| XS (≤30min) | 5 | TP-4I, TP-4O, TP-4S, TP-4T, TP-4U |
| S (1-2h) | 6 | TP-4A, TP-4C, TP-4E, TP-4J, TP-4K, TP-4P, TP-4Q |
| M (3-4h) | 5 | TP-4D, TP-4F, TP-4G, TP-4H, TP-4M, TP-4N |
| L (8h+) | 2 | TP-4B, TP-4R |

**Recommended Sprint Plan:**
1. **Sprint 1 (Quick Wins)**: TP-4A, TP-4C, TP-4E, TP-4I, TP-4O, TP-4S, TP-4T, TP-4U — fix cross-contamination, fill data gaps, cosmetic fixes
2. **Sprint 2 (Engine Quality)**: TP-4D, TP-4F, TP-4G, TP-4L, TP-4P, TP-4Q — scoring logic, dedup, formatting
3. **Sprint 3 (Strategic Value)**: TP-4B, TP-4H, TP-4M, TP-4N — SPAN matrix overhaul, provenance wiring, SWOT quality
4. **Backlog**: TP-4J, TP-4K, TP-4R — nice-to-have data enrichment
