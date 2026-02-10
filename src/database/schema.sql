-- BLM Financial Report Analysis - Database Schema
-- All tables use calendar_quarter TEXT NOT NULL for fiscal alignment
-- Format: "CQ4_2025" means Calendar Quarter 4 of 2025

CREATE TABLE IF NOT EXISTS operators (
    operator_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    parent_company TEXT,
    country TEXT NOT NULL,
    region TEXT,
    market TEXT NOT NULL,
    operator_type TEXT,  -- "incumbent" / "challenger" / "new_entrant"
    ir_url TEXT,
    fiscal_year_start_month INTEGER DEFAULT 1,
    fiscal_year_label TEXT DEFAULT '',
    quarter_naming TEXT DEFAULT 'calendar',
    currency TEXT DEFAULT 'EUR',
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS financial_quarterly (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    period TEXT NOT NULL,
    calendar_quarter TEXT NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    report_date DATE,
    report_status TEXT DEFAULT 'published',
    -- Revenue (EUR millions)
    total_revenue REAL,
    service_revenue REAL,
    service_revenue_growth_pct REAL,
    mobile_service_revenue REAL,
    mobile_service_growth_pct REAL,
    fixed_service_revenue REAL,
    fixed_service_growth_pct REAL,
    b2b_revenue REAL,
    b2b_growth_pct REAL,
    tv_revenue REAL,
    wholesale_revenue REAL,
    other_revenue REAL,
    -- Profitability
    ebitda REAL,
    ebitda_margin_pct REAL,
    ebitda_growth_pct REAL,
    net_income REAL,
    -- Investment
    capex REAL,
    capex_to_revenue_pct REAL,
    opex REAL,
    opex_to_revenue_pct REAL,
    employees INTEGER,
    -- Metadata
    source_url TEXT,
    notes TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(operator_id, calendar_quarter)
);

CREATE TABLE IF NOT EXISTS subscriber_quarterly (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    period TEXT NOT NULL,
    calendar_quarter TEXT NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    report_status TEXT DEFAULT 'published',
    -- Mobile
    mobile_total_k REAL,
    mobile_postpaid_k REAL,
    mobile_prepaid_k REAL,
    mobile_net_adds_k REAL,
    mobile_churn_pct REAL,
    mobile_arpu REAL,
    -- IoT
    iot_connections_k REAL,
    -- Fixed broadband
    broadband_total_k REAL,
    broadband_net_adds_k REAL,
    broadband_cable_k REAL,
    broadband_fiber_k REAL,
    broadband_dsl_k REAL,
    broadband_fwa_k REAL,
    broadband_arpu REAL,
    -- TV
    tv_total_k REAL,
    tv_net_adds_k REAL,
    -- Convergence
    fmc_total_k REAL,
    fmc_penetration_pct REAL,
    -- B2B
    b2b_customers_k REAL,
    -- Metadata
    source_url TEXT,
    notes TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(operator_id, calendar_quarter)
);

CREATE TABLE IF NOT EXISTS network_infrastructure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    calendar_quarter TEXT NOT NULL,
    five_g_coverage_pct REAL,
    four_g_coverage_pct REAL,
    fiber_homepass_k REAL,
    fiber_connected_k REAL,
    cable_homepass_k REAL,
    cable_docsis31_pct REAL,
    technology_mix TEXT,  -- JSON
    quality_scores TEXT,  -- JSON
    source_url TEXT,
    notes TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(operator_id, calendar_quarter)
);

CREATE TABLE IF NOT EXISTS tariffs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    plan_name TEXT NOT NULL,
    plan_type TEXT,        -- mobile_postpaid / mobile_prepaid / fixed_dsl / fixed_cable / fixed_fiber / tv / fmc_bundle
    plan_tier TEXT,        -- xs / s / m / l / xl / unlimited
    monthly_price REAL,
    data_allowance TEXT,
    speed_mbps REAL,
    contract_months INTEGER,
    includes_5g BOOLEAN DEFAULT 0,
    technology TEXT,
    effective_date DATE,
    snapshot_period TEXT,   -- H1_2023 / H2_2023 / ... / H1_2026
    source_url TEXT,
    notes TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(operator_id, plan_name, plan_type, snapshot_period)
);

CREATE TABLE IF NOT EXISTS competitive_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    calendar_quarter TEXT NOT NULL,
    dimension TEXT NOT NULL,
    score REAL NOT NULL CHECK(score >= 0 AND score <= 100),
    notes TEXT,
    source_url TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(operator_id, calendar_quarter, dimension)
);

CREATE TABLE IF NOT EXISTS intelligence_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id TEXT,
    market TEXT,
    event_date DATE NOT NULL,
    category TEXT NOT NULL,  -- regulatory/economic/social/technology/competitive/new_entrant/substitute/ott
    title TEXT NOT NULL,
    description TEXT,
    impact_type TEXT,  -- positive/negative/neutral
    severity TEXT,  -- low/medium/high/critical
    source_url TEXT,
    notes TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS executives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    name TEXT NOT NULL,
    title TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT 1,
    background TEXT,
    notes TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(operator_id, name, title)
);

CREATE TABLE IF NOT EXISTS macro_environment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT NOT NULL,
    calendar_quarter TEXT NOT NULL,
    gdp_growth_pct REAL,
    inflation_pct REAL,
    unemployment_pct REAL,
    telecom_market_size_eur_b REAL,
    telecom_growth_pct REAL,
    five_g_adoption_pct REAL,
    fiber_penetration_pct REAL,
    regulatory_environment TEXT,
    digital_strategy TEXT,
    energy_cost_index REAL,
    consumer_confidence_index REAL,
    source_url TEXT,
    notes TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(country, calendar_quarter)
);

CREATE TABLE IF NOT EXISTS earnings_call_highlights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    calendar_quarter TEXT NOT NULL,
    segment TEXT,
    highlight_type TEXT,  -- guidance/explanation/outlook
    content TEXT NOT NULL,
    speaker TEXT,
    source_url TEXT,
    notes TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS source_registry (
    source_id TEXT PRIMARY KEY,
    source_type TEXT,  -- "earnings_report" / "press_release" / "regulator" / "analyst"
    url TEXT,
    document_name TEXT,
    publisher TEXT,
    publication_date DATE,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS data_provenance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type TEXT NOT NULL,  -- "financial_quarterly" / "subscriber_quarterly" / etc.
    entity_id INTEGER NOT NULL,
    field_name TEXT NOT NULL,
    source_id TEXT REFERENCES source_registry(source_id),
    confidence REAL CHECK(confidence >= 0 AND confidence <= 1),
    extraction_method TEXT,  -- "manual" / "api" / "scrape" / "calculated"
    raw_text TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    look_category TEXT NOT NULL,  -- "trend" / "market" / "competition" / "self" / "opportunity"
    finding_ref TEXT,
    feedback_type TEXT NOT NULL,  -- "agree" / "disagree" / "modify" / "add"
    original_value TEXT,
    user_comment TEXT,
    user_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_financial_operator_cq ON financial_quarterly(operator_id, calendar_quarter);
CREATE INDEX IF NOT EXISTS idx_subscriber_operator_cq ON subscriber_quarterly(operator_id, calendar_quarter);
CREATE INDEX IF NOT EXISTS idx_network_operator_cq ON network_infrastructure(operator_id, calendar_quarter);
CREATE INDEX IF NOT EXISTS idx_competitive_operator_cq ON competitive_scores(operator_id, calendar_quarter);
CREATE INDEX IF NOT EXISTS idx_intelligence_market ON intelligence_events(market, event_date);
CREATE INDEX IF NOT EXISTS idx_intelligence_operator ON intelligence_events(operator_id, event_date);
CREATE INDEX IF NOT EXISTS idx_macro_country_cq ON macro_environment(country, calendar_quarter);
CREATE INDEX IF NOT EXISTS idx_earnings_operator_cq ON earnings_call_highlights(operator_id, calendar_quarter);
CREATE INDEX IF NOT EXISTS idx_provenance_entity ON data_provenance(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_tariff_operator_period ON tariffs(operator_id, snapshot_period);
CREATE INDEX IF NOT EXISTS idx_tariff_type_period ON tariffs(plan_type, snapshot_period);
