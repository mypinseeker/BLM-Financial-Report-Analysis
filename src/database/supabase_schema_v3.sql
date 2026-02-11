-- BLM Financial Report Analysis - Schema Extension v3
-- Adds: operator_groups, group_subsidiaries, analysis_jobs
-- Adds: group_id column to operators table
-- Run AFTER the base schema (schema.sql / supabase_schema.sql)

-- ============================================================================
-- 1. Operator Groups — multinational operator parent companies
-- ============================================================================
CREATE TABLE IF NOT EXISTS operator_groups (
    group_id TEXT PRIMARY KEY,
    group_name TEXT NOT NULL,
    brand_name TEXT,
    headquarters TEXT,
    ir_url TEXT,
    stock_ticker TEXT,
    markets_count INTEGER DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 2. Group Subsidiaries — group → operator mapping with ownership details
-- ============================================================================
CREATE TABLE IF NOT EXISTS group_subsidiaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id TEXT NOT NULL REFERENCES operator_groups(group_id),
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    market TEXT NOT NULL,
    ownership_pct REAL,
    ownership_type TEXT,          -- "direct", "indirect", "joint_venture"
    acquired_date DATE,
    local_brand TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(group_id, operator_id)
);

-- ============================================================================
-- 3. Analysis Jobs — analysis task queue for single-market and group analyses
-- ============================================================================
CREATE TABLE IF NOT EXISTS analysis_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_type TEXT NOT NULL,        -- "single_market", "group_analysis"
    group_id TEXT,                 -- NULL for single_market
    market TEXT,                   -- NULL for group (has many markets)
    target_operator TEXT,
    analysis_period TEXT NOT NULL, -- "CQ4_2025"
    n_quarters INTEGER DEFAULT 8,
    status TEXT DEFAULT 'pending', -- pending / running / completed / failed
    progress TEXT DEFAULT '{}',   -- JSON: {"guatemala": "completed", ...}
    config TEXT DEFAULT '{}',     -- JSON: additional parameters
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT
);

-- ============================================================================
-- 4. Add group_id to operators table
-- ============================================================================
-- Note: SQLite doesn't support ADD COLUMN IF NOT EXISTS.
-- For Supabase (PostgreSQL), use:
--   ALTER TABLE operators ADD COLUMN IF NOT EXISTS group_id TEXT REFERENCES operator_groups(group_id);
-- For SQLite, wrap in a try/except in Python, or:
ALTER TABLE operators ADD COLUMN group_id TEXT REFERENCES operator_groups(group_id);

-- ============================================================================
-- 5. Analysis Outputs — add output_category column for categorization
-- ============================================================================
-- Enables grouping outputs by: five_looks, sending, executive_summary, ppt, other
-- For Supabase: ALTER TABLE analysis_outputs ADD COLUMN IF NOT EXISTS output_category TEXT DEFAULT 'other';
ALTER TABLE analysis_outputs ADD COLUMN output_category TEXT DEFAULT 'other';

-- ============================================================================
-- Indexes
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_subsidiaries_group ON group_subsidiaries(group_id);
CREATE INDEX IF NOT EXISTS idx_subsidiaries_operator ON group_subsidiaries(operator_id);
CREATE INDEX IF NOT EXISTS idx_subsidiaries_market ON group_subsidiaries(market);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON analysis_jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_group ON analysis_jobs(group_id);
CREATE INDEX IF NOT EXISTS idx_jobs_market ON analysis_jobs(market);
CREATE INDEX IF NOT EXISTS idx_operators_group ON operators(group_id);
