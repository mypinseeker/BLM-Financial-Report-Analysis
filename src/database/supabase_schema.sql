-- BLM Financial Report Analysis - Supabase (Postgres) Schema
-- Migrated from SQLite schema.sql + 2 new tables (market_configs, analysis_outputs)
-- Run via: python3 -m src.database.supabase_sync init

-- ============================================================================
-- Existing 12 tables (adapted from SQLite → Postgres)
-- ============================================================================

CREATE TABLE IF NOT EXISTS operators (
    operator_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    parent_company TEXT,
    country TEXT NOT NULL,
    region TEXT,
    market TEXT NOT NULL,
    operator_type TEXT,
    ir_url TEXT,
    fiscal_year_start_month INTEGER DEFAULT 1,
    fiscal_year_label TEXT DEFAULT '',
    quarter_naming TEXT DEFAULT 'calendar',
    currency TEXT DEFAULT 'EUR',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS financial_quarterly (
    id BIGSERIAL PRIMARY KEY,
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    period TEXT NOT NULL,
    calendar_quarter TEXT NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    report_date DATE,
    report_status TEXT DEFAULT 'published',
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
    ebitda REAL,
    ebitda_margin_pct REAL,
    ebitda_growth_pct REAL,
    net_income REAL,
    capex REAL,
    capex_to_revenue_pct REAL,
    opex REAL,
    opex_to_revenue_pct REAL,
    employees INTEGER,
    source_url TEXT,
    notes TEXT,
    collected_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(operator_id, calendar_quarter)
);

CREATE TABLE IF NOT EXISTS subscriber_quarterly (
    id BIGSERIAL PRIMARY KEY,
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    period TEXT NOT NULL,
    calendar_quarter TEXT NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    report_status TEXT DEFAULT 'published',
    mobile_total_k REAL,
    mobile_postpaid_k REAL,
    mobile_prepaid_k REAL,
    mobile_net_adds_k REAL,
    mobile_churn_pct REAL,
    mobile_arpu REAL,
    iot_connections_k REAL,
    broadband_total_k REAL,
    broadband_net_adds_k REAL,
    broadband_cable_k REAL,
    broadband_fiber_k REAL,
    broadband_dsl_k REAL,
    broadband_fwa_k REAL,
    broadband_arpu REAL,
    tv_total_k REAL,
    tv_net_adds_k REAL,
    fmc_total_k REAL,
    fmc_penetration_pct REAL,
    b2b_customers_k REAL,
    source_url TEXT,
    notes TEXT,
    collected_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(operator_id, calendar_quarter)
);

CREATE TABLE IF NOT EXISTS network_infrastructure (
    id BIGSERIAL PRIMARY KEY,
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    calendar_quarter TEXT NOT NULL,
    five_g_coverage_pct REAL,
    four_g_coverage_pct REAL,
    fiber_homepass_k REAL,
    fiber_connected_k REAL,
    cable_homepass_k REAL,
    cable_docsis31_pct REAL,
    technology_mix JSONB,
    quality_scores JSONB,
    source_url TEXT,
    notes TEXT,
    collected_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(operator_id, calendar_quarter)
);

CREATE TABLE IF NOT EXISTS tariffs (
    id BIGSERIAL PRIMARY KEY,
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    plan_name TEXT NOT NULL,
    plan_type TEXT,
    plan_tier TEXT,
    monthly_price REAL,
    data_allowance TEXT,
    speed_mbps REAL,
    contract_months INTEGER,
    includes_5g BOOLEAN DEFAULT FALSE,
    technology TEXT,
    effective_date DATE,
    snapshot_period TEXT,
    source_url TEXT,
    notes TEXT,
    collected_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(operator_id, plan_name, plan_type, snapshot_period)
);

CREATE TABLE IF NOT EXISTS competitive_scores (
    id BIGSERIAL PRIMARY KEY,
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    calendar_quarter TEXT NOT NULL,
    dimension TEXT NOT NULL,
    score REAL NOT NULL CHECK(score >= 0 AND score <= 100),
    notes TEXT,
    source_url TEXT,
    collected_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(operator_id, calendar_quarter, dimension)
);

CREATE TABLE IF NOT EXISTS intelligence_events (
    id BIGSERIAL PRIMARY KEY,
    operator_id TEXT,
    market TEXT,
    event_date DATE NOT NULL,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    impact_type TEXT,
    severity TEXT,
    source_url TEXT,
    notes TEXT,
    collected_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS executives (
    id BIGSERIAL PRIMARY KEY,
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    name TEXT NOT NULL,
    title TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    background TEXT,
    notes TEXT,
    collected_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(operator_id, name, title)
);

CREATE TABLE IF NOT EXISTS macro_environment (
    id BIGSERIAL PRIMARY KEY,
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
    collected_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(country, calendar_quarter)
);

CREATE TABLE IF NOT EXISTS earnings_call_highlights (
    id BIGSERIAL PRIMARY KEY,
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    calendar_quarter TEXT NOT NULL,
    segment TEXT,
    highlight_type TEXT,
    content TEXT NOT NULL,
    speaker TEXT,
    source_url TEXT,
    notes TEXT,
    collected_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS source_registry (
    source_id TEXT PRIMARY KEY,
    source_type TEXT,
    url TEXT,
    document_name TEXT,
    publisher TEXT,
    publication_date DATE,
    collected_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS data_provenance (
    id BIGSERIAL PRIMARY KEY,
    entity_type TEXT NOT NULL,
    entity_id BIGINT NOT NULL,
    field_name TEXT NOT NULL,
    source_id TEXT REFERENCES source_registry(source_id),
    confidence REAL CHECK(confidence >= 0 AND confidence <= 1),
    extraction_method TEXT,
    raw_text TEXT,
    collected_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- New table A: market_configs (stores MarketConfig dataclass)
-- ============================================================================

CREATE TABLE IF NOT EXISTS market_configs (
    market_id TEXT PRIMARY KEY,
    market_name TEXT NOT NULL,
    country TEXT NOT NULL,
    currency TEXT NOT NULL DEFAULT 'EUR',
    currency_symbol TEXT DEFAULT '€',
    regulatory_body TEXT,
    population_k REAL,
    customer_segments JSONB DEFAULT '[]',
    operator_bmc_enrichments JSONB DEFAULT '{}',
    operator_exposures JSONB DEFAULT '{}',
    pest_context JSONB DEFAULT '{}',
    competitive_landscape_notes JSONB DEFAULT '[]',
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- New table B: analysis_outputs (stores insight deliverables)
-- ============================================================================

CREATE TABLE IF NOT EXISTS analysis_outputs (
    id BIGSERIAL PRIMARY KEY,
    market_id TEXT NOT NULL,
    operator_id TEXT NOT NULL,
    analysis_period TEXT NOT NULL,
    output_type TEXT NOT NULL,
    module_name TEXT,
    file_name TEXT NOT NULL,
    content_text TEXT,
    storage_path TEXT,
    file_size_bytes BIGINT,
    slide_count INTEGER,
    chart_count INTEGER,
    version TEXT DEFAULT 'v1.0.0',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(market_id, operator_id, analysis_period, output_type, module_name)
);

-- ============================================================================
-- Indexes
-- ============================================================================

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
CREATE INDEX IF NOT EXISTS idx_outputs_market ON analysis_outputs(market_id, operator_id, analysis_period);
