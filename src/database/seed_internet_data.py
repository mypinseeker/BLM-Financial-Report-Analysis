"""Seed the database with internet-sourced data for Germany telecom market.

Data collected from public sources on 2026-02-09, covering:
1. Regulatory insights (BNetzA, EU digital strategy)
2. Earnings call Q&A highlights (Vodafone Q3 FY26, O2, 1&1)
3. Media/industry reports (M&A, network strategy, market dynamics)

Each entry includes source_url for traceability.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.database.db import TelecomDatabase


def seed_source_registry(db: TelecomDatabase):
    """Register all data sources used in this seed."""
    sources = [
        {
            "source_id": "vod_q3fy26_trading_update",
            "source_type": "earnings_report",
            "url": "https://reports.investors.vodafone.com/view/412789358/",
            "document_name": "Vodafone Q3 FY26 Trading Update",
            "publisher": "Vodafone Group Plc",
            "publication_date": "2026-02-05",
        },
        {
            "source_id": "vod_q3fy26_earnings_call",
            "source_type": "earnings_call",
            "url": "https://fintool.com/app/research/companies/VOD/earnings/Q3%202026",
            "document_name": "Vodafone Q3 FY26 Earnings Call Q&A",
            "publisher": "Vodafone Group Plc",
            "publication_date": "2026-02-05",
        },
        {
            "source_id": "bnetza_spectrum_2025",
            "source_type": "regulator",
            "url": "https://www.bundesnetzagentur.de/SharedDocs/Pressemitteilungen/EN/2025/20250324_frequenzen.html",
            "document_name": "BNetzA Spectrum Extension Decision",
            "publisher": "Bundesnetzagentur",
            "publication_date": "2025-03-24",
        },
        {
            "source_id": "bnetza_spectrum_decision_pdf",
            "source_type": "regulator",
            "url": "https://www.bundesnetzagentur.de/SharedDocs/Downloads/EN/Areas/Telecommunications/Companies/TelecomRegulation/FrequencyManagement/ElectronicCommunicationsServices/Decision2025.pdf",
            "document_name": "BNetzA Decision on Spectrum Extension (Full Text)",
            "publisher": "Bundesnetzagentur",
            "publication_date": "2025-03-24",
        },
        {
            "source_id": "eu_digital_germany",
            "source_type": "regulator",
            "url": "https://digital-strategy.ec.europa.eu/en/policies/digital-connectivity-germany",
            "document_name": "Digital Connectivity in Germany",
            "publisher": "European Commission",
            "publication_date": "2025-01-23",
        },
        {
            "source_id": "vod_altice_fibreco",
            "source_type": "press_release",
            "url": "https://www.vodafone.com/news/newsroom/corporate-and-financial/vodafone-altice-create-joint-venture-deploy-fibre-to-the-home-germany",
            "document_name": "Vodafone and Altice FibreCo JV Announcement",
            "publisher": "Vodafone Group Plc",
            "publication_date": "2025-07-15",
        },
        {
            "source_id": "vod_skaylink_acquisition",
            "source_type": "press_release",
            "url": "https://www.vodafone.com/news/corporate-and-financial/vodafone-to-acquire-skaylink",
            "document_name": "Vodafone to Acquire Skaylink",
            "publisher": "Vodafone Group Plc",
            "publication_date": "2025-10-30",
        },
        {
            "source_id": "vod_skaylink_completion",
            "source_type": "press_release",
            "url": "https://www.vodafone.com/news/newsroom/corporate-and-financial/vodafone-completes-the-acquisition-of-skaylink",
            "document_name": "Vodafone Completes Skaylink Acquisition",
            "publisher": "Vodafone Group Plc",
            "publication_date": "2025-12-16",
        },
        {
            "source_id": "o2_q1_2025",
            "source_type": "earnings_report",
            "url": "https://www.telefonica.de/news/press-releases-telefonica-germany/2025/05/quarterly-results-customer-growth-strengthens-o2-telefonicas-operating-performance-in-the-first-quarter-2025.html",
            "document_name": "O2 Telefonica Germany Q1 2025 Results",
            "publisher": "Telefonica Deutschland",
            "publication_date": "2025-05-08",
        },
        {
            "source_id": "o2_q2_2025",
            "source_type": "earnings_report",
            "url": "https://www.telefonica.de/news/press-releases-telefonica-germany/2025/07/quarterly-results-customer-growth-across-segments-confirms-o2-telefonicas-course-in-the-second-quarter.html",
            "document_name": "O2 Telefonica Germany Q2 2025 Results",
            "publisher": "Telefonica Deutschland",
            "publication_date": "2025-07-24",
        },
        {
            "source_id": "one_one_q3_2025",
            "source_type": "earnings_report",
            "url": "https://imagepool.1und1.ag/v2/download/berichte/2025-1u1AG-Q3_EN.pdf",
            "document_name": "1&1 AG Interim Statement Q3 2025",
            "publisher": "1&1 AG",
            "publication_date": "2025-11-12",
        },
        {
            "source_id": "one_one_openran_migration",
            "source_type": "news",
            "url": "https://www.lightreading.com/finance/germany-s-1-1-migrates-all-mobile-customers-to-open-ran-5g-network",
            "document_name": "1&1 Migrates All Customers to Open RAN 5G Network",
            "publisher": "Light Reading",
            "publication_date": "2025-12-20",
        },
        {
            "source_id": "dt_q3_2025",
            "source_type": "earnings_report",
            "url": "https://www.telekom.com/en/investor-relations/publications/financial-results/financial-results-2025",
            "document_name": "Deutsche Telekom Q3 2025 Financial Results",
            "publisher": "Deutsche Telekom AG",
            "publication_date": "2025-11-13",
        },
        {
            "source_id": "vatm_market_2025",
            "source_type": "analyst",
            "url": "https://www.vatm.de/wp-content/uploads/2025/06/VATM-Market-Analysis-Germany-2025.pdf",
            "document_name": "26th Telecommunications Market Analysis Germany 2025",
            "publisher": "VATM",
            "publication_date": "2025-06-15",
        },
        {
            "source_id": "vod_mdu_impact",
            "source_type": "news",
            "url": "https://www.broadbandtvnews.com/2024/05/14/vodafones-german-recovery-hit-by-end-to-mdu-tv-switch/",
            "document_name": "Vodafone German Recovery Hit by MDU TV Switching",
            "publisher": "Broadband TV News",
            "publication_date": "2024-05-14",
        },
        {
            "source_id": "vod_cable_restructure",
            "source_type": "news",
            "url": "https://www.broadbandtvnews.com/2025/09/01/vodafone-restructures-tv-frequencies-across-germany-to-boost-cable-performance/",
            "document_name": "Vodafone Restructures TV Frequencies Across Germany",
            "publisher": "Broadband TV News",
            "publication_date": "2025-09-01",
        },
        {
            "source_id": "birdbird_spectrum_analysis",
            "source_type": "analyst",
            "url": "https://www.twobirds.com/en/insights/2025/german-bundesnetzagentur-provides-decision-to-extend-mobile-spectrum-subject-to-conditions",
            "document_name": "BNetzA Spectrum Extension Legal Analysis",
            "publisher": "Bird & Bird LLP",
            "publication_date": "2025-04-02",
        },
        {
            "source_id": "dt_targets_vodafone_fiber",
            "source_type": "news",
            "url": "https://www.telcotitans.com/deutsche-telekomwatch/germany-dt-targets-vodafone-as-it-reboots-fibre-tactics/9904.article",
            "document_name": "DT Targets Vodafone as It Reboots Fibre Tactics",
            "publisher": "TelcoTitans",
            "publication_date": "2025-08-15",
        },
    ]

    count = 0
    for src in sources:
        sql = """
            INSERT INTO source_registry (source_id, source_type, url, document_name, publisher, publication_date)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_id) DO UPDATE SET
                source_type = excluded.source_type,
                url = excluded.url,
                document_name = excluded.document_name,
                publisher = excluded.publisher,
                publication_date = excluded.publication_date
        """
        db.conn.execute(sql, (
            src["source_id"], src["source_type"], src["url"],
            src["document_name"], src["publisher"], src["publication_date"],
        ))
        count += 1

    db.conn.commit()
    print(f"  Registered {count} data sources")


def seed_intelligence_events(db: TelecomDatabase):
    """Insert intelligence events from internet research."""
    events = [
        # ── Regulatory / BNetzA ──
        {
            "operator_id": None,
            "market": "germany",
            "event_date": "2025-03-24",
            "category": "regulatory",
            "title": "BNetzA extends 800/1800/2600 MHz spectrum by 5 years",
            "description": (
                "BNetzA decided to extend 800MHz, 1800MHz, and 2600MHz spectrum usage rights by 5 years (originally expiring end of 2025). "
                "Conditions: 99.5% national area coverage ≥50Mbps by 2030; 99% of households in sparsely populated municipalities ≥100Mbps by 2029. "
                "All three operators must negotiate spectrum sharing with MVNOs/service providers. "
                "Special requirement: all three must provide 800MHz 2×5MHz shared access to 1&1; O2 must continue leasing 2600MHz 2×10MHz to 1&1. "
                "Re-auction expected in 2029."
            ),
            "impact_type": "positive",
            "severity": "high",
            "source_url": "https://www.bundesnetzagentur.de/SharedDocs/Pressemitteilungen/EN/2025/20250324_frequenzen.html",
            "notes": "Positive for DT/VF/O2 (avoids auction costs); negative for 1&1 (no direct spectrum extension) but gains shared access rights",
        },
        {
            "operator_id": None,
            "market": "germany",
            "event_date": "2025-01-23",
            "category": "regulatory",
            "title": "German government launches €1.2B Gigabit Funding Programme 2025",
            "description": (
                "German Federal Ministry for Digital and Transport launches the 2025 Gigabit Funding Programme, allocating €1.2B for fiber infrastructure. "
                "Targets: 50% household FTTH/FTTB coverage by 2025, 100% fiber coverage by 2030. "
                "Fiber connections grew over 20% YoY."
            ),
            "impact_type": "positive",
            "severity": "high",
            "source_url": "https://digital-strategy.ec.europa.eu/en/policies/digital-connectivity-germany",
            "notes": "Positive for all operators; Vodafone can access subsidies through Altice FibreCo JV",
        },
        {
            "operator_id": None,
            "market": "germany",
            "event_date": "2024-07-01",
            "category": "regulatory",
            "title": "Nebenkostenprivileg (MDU cable TV bundling) abolished",
            "description": (
                "From July 1, 2024, landlords can no longer include cable TV fees in ancillary costs (Nebenkostenprivileg abolished). "
                "Vodafone most affected: originally 8.5M MDU subscribers, retention rate ~50% (~4M retained). "
                "Fixed-line service revenue declined 5.9% in H1 FY25. By Q3 FY26, fixed-line decline narrowed to -1.1%, headwind easing."
            ),
            "impact_type": "negative",
            "severity": "high",
            "source_url": "https://www.broadbandtvnews.com/2024/05/14/vodafones-german-recovery-hit-by-end-to-mdu-tv-switch/",
            "notes": "Vodafone-specific risk (critical severity); minimal impact on DT/O2. Q3 FY26 base effect starting to fade",
        },
        # ── Vodafone Strategic Events ──
        {
            "operator_id": "vodafone_germany",
            "market": "germany",
            "event_date": "2025-12-16",
            "category": "competitive",
            "title": "Vodafone completes Skaylink acquisition for €175M",
            "description": (
                "Vodafone completed the acquisition of Skaylink (€175M, EV/EBITDA 7.0x), "
                "gaining 500+ cloud and security specialists. Skaylink specializes in AWS/Azure deployment, migration, and AI solutions. "
                "New B2B head Hagen Rickmann targets: €1B additional enterprise revenue over 5 years. "
                "This is a key step in Vodafone Business's transformation from connectivity to digital services."
            ),
            "impact_type": "positive",
            "severity": "high",
            "source_url": "https://www.vodafone.com/news/newsroom/corporate-and-financial/vodafone-completes-the-acquisition-of-skaylink",
            "notes": "EV/EBITDA 7.0x, reasonable valuation. Key to watch: integration speed and cross-selling effectiveness",
        },
        {
            "operator_id": "vodafone_germany",
            "market": "germany",
            "event_date": "2025-07-15",
            "category": "technology",
            "title": "Vodafone-Altice FibreCo JV: FTTH to 7M homes in 6 years",
            "description": (
                "Vodafone and Altice formed FibreCo JV to deploy FTTH to 7M homes over 6 years. "
                "80% upgrading within Vodafone's existing cable footprint, 20% greenfield expansion. "
                "Simultaneously advancing cable upgrades: node splitting + DOCSIS 3.1 high-split (3Gbps) → DOCSIS 4.0 (10Gbps). "
                "This is Vodafone's core strategic move in transitioning from cable to fiber."
            ),
            "impact_type": "positive",
            "severity": "high",
            "source_url": "https://www.vodafone.com/news/newsroom/corporate-and-financial/vodafone-altice-create-joint-venture-deploy-fibre-to-the-home-germany",
            "notes": "Addresses Vodafone's core problem of low fiber self-sufficiency. Key risks: execution speed and capital requirements",
        },
        {
            "operator_id": "vodafone_germany",
            "market": "germany",
            "event_date": "2025-09-01",
            "category": "technology",
            "title": "Vodafone restructures cable TV frequencies nationwide",
            "description": (
                "Vodafone begins nationwide cable network frequency restructuring, creating unified spectrum and releasing broadband capacity. "
                "Technical upgrade covers 400+ cities and 8.6M TV connections, expected completion mid-2026. "
                "Goal: free up spectrum resources for faster broadband speeds."
            ),
            "impact_type": "positive",
            "severity": "medium",
            "source_url": "https://www.broadbandtvnews.com/2025/09/01/vodafone-restructures-tv-frequencies-across-germany-to-boost-cable-performance/",
            "notes": "Frequency restructuring is a prerequisite for cable upgrades, paving the way for DOCSIS 4.0",
        },
        {
            "operator_id": "vodafone_germany",
            "market": "germany",
            "event_date": "2026-02-05",
            "category": "competitive",
            "title": "Vodafone completes 1&1 customer migration: 12M users on network",
            "description": (
                "Vodafone successfully completed the 1&1 customer migration; 12M 1&1 customers now on Vodafone's nationwide 5G network. "
                "This is one of the largest customer migrations in European telecom history. "
                "Wholesale revenue contribution expected to reach full run-rate by Q4 FY26. "
                "Network test results continue to improve; migration did not affect network quality."
            ),
            "impact_type": "positive",
            "severity": "high",
            "source_url": "https://reports.investors.vodafone.com/view/412789358/",
            "notes": "Wholesale revenue is the most certain growth driver for FY26, but long-term 1&1 self-built network will divert traffic",
        },
        # ── 1&1 Events ──
        {
            "operator_id": "one_and_one",
            "market": "germany",
            "event_date": "2025-12-31",
            "category": "new_entrant",
            "title": "1&1 completes OpenRAN migration, reaches 25% own network coverage",
            "description": (
                "All 1&1 mobile subscribers have migrated to its own OpenRAN 5G network (first in Europe). "
                "Approximately 1,500 own base stations operational, ~4,500 under construction. "
                "Achieved the 25% population coverage regulatory deadline target. "
                "Q3 2025 mobile net adds +40K (H1 roughly flat due to migration impact). "
                "9-month CAPEX €228.7M primarily for network build-out."
            ),
            "impact_type": "neutral",
            "severity": "high",
            "source_url": "https://www.lightreading.com/finance/germany-s-1-1-migrates-all-mobile-customers-to-open-ran-5g-network",
            "notes": "For Vodafone: short-term positive (wholesale revenue), long-term threat (traffic will gradually decrease). OpenRAN pioneer status worth monitoring",
        },
        # ── Deutsche Telekom Events ──
        {
            "operator_id": "deutsche_telekom",
            "market": "germany",
            "event_date": "2025-11-13",
            "category": "competitive",
            "title": "Deutsche Telekom Q3 2025: revenue +1.5%, net profit +14.3%",
            "description": (
                "DT Q3 2025 group revenue €28.935B (+1.5% YoY), EBITDAaL margin 38.2%. "
                "Net profit grew 14.3% to €2.67B. YTD free cash flow +6.8% to €16.1B. "
                "Germany Q4 outlook: EBITDA growth >2%, benefiting from cost savings and easing wage/energy pressure. "
                "Q4 2025 full results scheduled for February 26, 2026."
            ),
            "impact_type": "negative",
            "severity": "medium",
            "source_url": "https://www.telekom.com/en/investor-relations/publications/financial-results/financial-results-2025",
            "notes": "Negative for Vodafone: DT continues to widen its lead. DT's scale advantages and operational discipline set the benchmark",
        },
        {
            "operator_id": "deutsche_telekom",
            "market": "germany",
            "event_date": "2025-08-15",
            "category": "competitive",
            "title": "DT reboots fibre tactics, targets Vodafone cable footprint",
            "description": (
                "DT adjusts its fiber strategy, actively deploying FTTH in Vodafone cable coverage areas, "
                "directly competing with Vodafone's cable+fiber hybrid network. "
                "This is DT's offensive strategy leveraging fiber first-mover advantage to capture Vodafone fixed-line customers."
            ),
            "impact_type": "negative",
            "severity": "high",
            "source_url": "https://www.telcotitans.com/deutsche-telekomwatch/germany-dt-targets-vodafone-as-it-reboots-fibre-tactics/9904.article",
            "notes": "Serious threat to Vodafone: cable customers may be attracted by DT's pure fiber proposition",
        },
        # ── O2 / Telefónica Events ──
        {
            "operator_id": "telefonica_o2",
            "market": "germany",
            "event_date": "2025-07-24",
            "category": "competitive",
            "title": "O2 Germany Q2 2025: revenue -2.4% but IoT +47%, users growing",
            "description": (
                "O2 Q2 2025 total revenue declined 2.4% (mobile service revenue -3.4%), "
                "but subscriber growth was strong: Q2 contract customers +184K. "
                "IoT connections grew 47% YoY (Q2 net adds 177K), the biggest highlight. "
                "5G coverage at 98%, leading the industry. EBITDA margin stable at ~30.6%."
            ),
            "impact_type": "neutral",
            "severity": "medium",
            "source_url": "https://www.telefonica.de/news/press-releases-telefonica-germany/2025/07/quarterly-results-customer-growth-across-segments-confirms-o2-telefonicas-course-in-the-second-quarter.html",
            "notes": "O2 excels in IoT and subscriber growth but revenue under pressure. 5G 98% coverage creates network competitive pressure on Vodafone",
        },
        # ── Market-level Events ──
        {
            "operator_id": None,
            "market": "germany",
            "event_date": "2025-06-15",
            "category": "economic",
            "title": "German telecom market reaches $86B, CAGR 5.53% to 2030",
            "description": (
                "VATM 26th market analysis report: German telecom market 2025 size $86B (~€79B annually), "
                "projected to reach $112.6B by 2030, CAGR 5.53%. "
                "Market has 150+ service providers, highly competitive. Industry-average ARPU declining ~4%. "
                "Mobile data service revenue CAGR 9.5%, 5G plans are the main growth engine. "
                "Fiber connections grew over 20%, 97% household broadband coverage."
            ),
            "impact_type": "neutral",
            "severity": "medium",
            "source_url": "https://www.vatm.de/wp-content/uploads/2025/06/VATM-Market-Analysis-Germany-2025.pdf",
            "notes": "Market growth driven primarily by data/5G/fiber; traditional voice/SMS continues to shrink",
        },
    ]

    count = 0
    for event in events:
        db.upsert_intelligence(event)
        count += 1

    print(f"  Inserted {count} intelligence events")


def seed_earnings_call_highlights(db: TelecomDatabase):
    """Insert earnings call Q&A highlights."""
    highlights = [
        # ── Vodafone Q3 FY26 Earnings Call (2026-02-05) ──
        {
            "segment": "germany",
            "highlight_type": "guidance",
            "content": (
                "Germany EBITDA: H2 performing better than H1, but FY26 will not return to positive growth. "
                "Key tailwinds: (1) MDU YoY base effect starting to fade from Q3; "
                "(2) 1&1 wholesale revenue reaching full run-rate by Q4; "
                "(3) MVNO base effects. "
                "Positive EBITDA growth not expected until FY27."
            ),
            "speaker": "Management",
            "source_url": "https://fintool.com/app/research/companies/VOD/earnings/Q3%202026",
            "notes": "Top analyst concern. Investors have reservations about Germany's recovery pace",
        },
        {
            "segment": "germany_broadband",
            "highlight_type": "explanation",
            "content": (
                "Broadband pricing strategy: another price increase in January 2026, adopting a 'more-for-more' approach. "
                "Fixed-line consumer revenue has stabilized. New customer broadband ARPU at a 3-year high (+21% YoY). "
                "Q4 volume trends expected to be similar, but the value equation is working. "
                "Retail pricing actions between March and October 2025 are supporting the ARPU trend."
            ),
            "speaker": "Management",
            "source_url": "https://reports.investors.vodafone.com/view/412789358/",
            "notes": "'Value management' strategy proving effective on the broadband side — a core positive signal",
        },
        {
            "segment": "germany_mobile",
            "highlight_type": "explanation",
            "content": (
                "Mobile service revenue grew 2.8% in Q3 (Q2: 3.8%), growth decelerating. "
                "Reason: wholesale revenue growth partially offset by ARPU pressure and service provider payment timing. "
                "Post-1&1 migration, network test results continue to improve — 12M user migration is one of Europe's largest ever. "
                "Consumer contract customer net adds 42,000 (Q2 only +1,000), consumer momentum improving."
            ),
            "speaker": "Management",
            "source_url": "https://reports.investors.vodafone.com/view/412789358/",
            "notes": "Mobile ARPU pressure is a concern. Consumer contract net adds recovery is a positive signal",
        },
        {
            "segment": "germany_b2b",
            "highlight_type": "explanation",
            "content": (
                "Vodafone Business Germany service revenue declined 1.8% in Q3 (Q2: -1.6%), widening decline. "
                "Reason: ARPU pressure on mobile contract renewals + core connectivity business under sustained pressure. "
                "Highlight: strong digital services demand. Skaylink acquisition (completed December 2025) "
                "expected to accelerate growth in cloud, security, and managed services. "
                "New B2B head Hagen Rickmann's 5-year €1B growth target is a key strategic commitment."
            ),
            "speaker": "Management",
            "source_url": "https://reports.investors.vodafone.com/view/412789358/",
            "notes": "B2B is a strategic priority but still declining short-term; Skaylink is the inflection point",
        },
        {
            "segment": "group",
            "highlight_type": "guidance",
            "content": (
                "Group FY26 guidance reaffirmed at upper end: EBITDAaL €11.3-11.6B, free cash flow €2.4-2.6B. "
                "YTD EBITDAaL grew 5.3% to €8.5B, in line with expectations. "
                "Group service revenue grew 5.4% in Q3. "
                "November 2025: FY26 dividend per share increased 2.5%, reflecting medium-term free cash flow growth confidence."
            ),
            "speaker": "Management",
            "source_url": "https://www.stocktitan.net/sec-filings/VOD/6-k-vodafone-group-public-ltd-co-current-report-foreign-issuer-17b0d1c9489d.html",
            "notes": "Group level healthy; Germany is the slowest-improving market",
        },
    ]

    count = 0
    for h in highlights:
        db.upsert_earnings_highlight("vodafone_germany", "CQ4_2025", h)
        count += 1

    print(f"  Inserted {count} earnings call highlights")


def seed_updated_macro(db: TelecomDatabase):
    """Update macro environment data with internet-sourced details.

    Reads existing data first to avoid overwriting fields we don't update.
    """
    # Read existing macro data for CQ4_2025
    row = db.conn.execute(
        "SELECT * FROM macro_environment WHERE country = ? AND calendar_quarter = ?",
        ("Germany", "CQ4_2025"),
    ).fetchone()

    existing = dict(row) if row else {}

    # Merge: only update fields we have new data for
    macro_update = {
        "gdp_growth_pct": existing.get("gdp_growth_pct"),
        "inflation_pct": existing.get("inflation_pct"),
        "unemployment_pct": existing.get("unemployment_pct"),
        "five_g_adoption_pct": existing.get("five_g_adoption_pct"),
        "fiber_penetration_pct": existing.get("fiber_penetration_pct"),
        "energy_cost_index": existing.get("energy_cost_index"),
        "consumer_confidence_index": existing.get("consumer_confidence_index"),
        # New/updated fields from internet research
        "telecom_market_size_eur_b": 79.0,  # $86B ≈ €79B (annual)
        "telecom_growth_pct": 5.53,  # CAGR 2025-2030
        "regulatory_environment": (
            "BNetzA: 800/1800/2600MHz spectrum extended 5 years (March 2025 decision); "
            "Coverage obligation: 99.5% area ≥50Mbps by 2030; "
            "€1.2B Gigabit Funding Programme (Jan 2025); "
            "Nebenkostenprivileg abolished July 2024 (MDU TV regulation change); "
            "Fiber targets: 50% FTTH by 2025, 100% by 2030"
        ),
        "digital_strategy": (
            "Gigabit Strategy: FTTH/FTTB 50% by 2025, 100% by 2030; "
            "€1.2B Gigabit Funding Programme 2025; "
            "Fiber connections +20% YoY; "
            "5G coverage obligation: 99.5% area by 2030"
        ),
        "source_url": "https://www.bundesnetzagentur.de/SharedDocs/Pressemitteilungen/EN/2025/20250324_frequenzen.html",
        "notes": (
            "Sources: BNetzA spectrum decision (2025-03-24), "
            "EU Digital Connectivity Germany, "
            "VATM Market Analysis 2025"
        ),
    }

    db.upsert_macro("Germany", "CQ4_2025", macro_update)
    print(f"  Updated macro environment for CQ4_2025 with internet data")


def seed_internet_data(db: TelecomDatabase):
    """Run the complete internet data seed process."""
    print("\n=== Seeding Internet-Sourced Data ===")

    print("Step 1/4: Registering data sources...")
    seed_source_registry(db)

    print("Step 2/4: Inserting intelligence events (regulatory/media/strategic)...")
    seed_intelligence_events(db)

    print("Step 3/4: Inserting earnings call Q&A highlights...")
    seed_earnings_call_highlights(db)

    print("Step 4/4: Updating macro environment data...")
    seed_updated_macro(db)

    print("=== Internet data seed complete! ===\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Seed internet-sourced data")
    parser.add_argument(
        "--db-path", default="data/telecom.db",
        help="Path to SQLite database (default: data/telecom.db)",
    )
    args = parser.parse_args()

    db = TelecomDatabase(args.db_path)
    db.init()
    seed_internet_data(db)
    db.close()
