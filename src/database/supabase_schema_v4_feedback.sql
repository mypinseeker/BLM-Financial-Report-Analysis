-- User Feedback persistence (P1-5)
-- Apply after supabase_schema_v3.sql

CREATE TABLE IF NOT EXISTS user_feedback (
    id BIGSERIAL PRIMARY KEY,
    analysis_job_id INTEGER,
    operator_id TEXT,
    period TEXT,
    look_category TEXT NOT NULL,
    finding_ref TEXT,
    feedback_type TEXT NOT NULL DEFAULT 'confirmed',
    original_value TEXT,
    user_comment TEXT,
    user_value TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(analysis_job_id, operator_id, look_category, finding_ref)
);

CREATE INDEX IF NOT EXISTS idx_feedback_job ON user_feedback(analysis_job_id, operator_id);
