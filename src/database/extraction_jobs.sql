-- extraction_jobs table — tracks AI data extraction pipeline jobs
-- Run this in Supabase SQL Editor

CREATE TABLE IF NOT EXISTS extraction_jobs (
    id BIGSERIAL PRIMARY KEY,
    operator_id TEXT NOT NULL,
    market TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    current_step TEXT,
    ir_url TEXT,
    discovered_pdf_url TEXT,
    report_title TEXT,
    report_period TEXT,
    gemini_file_uri TEXT,
    extracted_data JSONB DEFAULT '{}',
    approved_data JSONB DEFAULT '{}',
    source_id TEXT,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    approved_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_extraction_job_status ON extraction_jobs(status);
CREATE INDEX IF NOT EXISTS idx_extraction_job_operator ON extraction_jobs(operator_id);
