-- BLM Schema v3 — PostgreSQL / Supabase version
-- Run in Supabase Dashboard → SQL Editor

CREATE TABLE IF NOT EXISTS operator_groups (
    group_id TEXT PRIMARY KEY, group_name TEXT NOT NULL, brand_name TEXT,
    headquarters TEXT, ir_url TEXT, stock_ticker TEXT,
    markets_count INTEGER DEFAULT 0, notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(), updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS group_subsidiaries (
    id BIGSERIAL PRIMARY KEY,
    group_id TEXT NOT NULL REFERENCES operator_groups(group_id),
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    market TEXT NOT NULL, ownership_pct REAL, ownership_type TEXT,
    acquired_date DATE, local_brand TEXT, is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(), UNIQUE(group_id, operator_id)
);

CREATE TABLE IF NOT EXISTS analysis_jobs (
    id BIGSERIAL PRIMARY KEY, job_type TEXT NOT NULL, group_id TEXT,
    market TEXT, target_operator TEXT, analysis_period TEXT NOT NULL,
    n_quarters INTEGER DEFAULT 8, status TEXT DEFAULT 'pending',
    progress JSONB DEFAULT '{}', config JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(), started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ, error_message TEXT
);

ALTER TABLE operators ADD COLUMN IF NOT EXISTS group_id TEXT REFERENCES operator_groups(group_id);
ALTER TABLE analysis_outputs ADD COLUMN IF NOT EXISTS output_category TEXT DEFAULT 'other';

CREATE INDEX IF NOT EXISTS idx_subsidiaries_group ON group_subsidiaries(group_id);
CREATE INDEX IF NOT EXISTS idx_subsidiaries_operator ON group_subsidiaries(operator_id);
CREATE INDEX IF NOT EXISTS idx_subsidiaries_market ON group_subsidiaries(market);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON analysis_jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_group ON analysis_jobs(group_id);
CREATE INDEX IF NOT EXISTS idx_jobs_market ON analysis_jobs(market);
CREATE INDEX IF NOT EXISTS idx_operators_group ON operators(group_id);
