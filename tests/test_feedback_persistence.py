"""Tests for user feedback persistence (P1-5).

Covers:
- UserFeedback model (FEEDBACK_TYPES, defaults, new fields, to_dict)
- SQLite schema (new columns, UNIQUE constraint, index)
- Upsert (insert, update, multiple findings)
- Query (filter by look_category, operator, job)
- Clear (removes records, job isolation)
"""
import sys
import os
import pytest
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.models.feedback import UserFeedback, FEEDBACK_TYPES
from src.database.db import TelecomDatabase


# =====================================================================
# Model Tests
# =====================================================================

class TestFeedbackModel:
    def test_feedback_types_constant(self):
        assert FEEDBACK_TYPES == ("confirmed", "disputed", "modified", "supplemented")

    def test_default_feedback_type(self):
        fb = UserFeedback(look_category="trends")
        assert fb.feedback_type == "confirmed"

    def test_new_fields_defaults(self):
        fb = UserFeedback(look_category="market")
        assert fb.analysis_job_id == 0
        assert fb.operator_id == ""
        assert fb.period == ""

    def test_new_fields_set(self):
        fb = UserFeedback(
            look_category="competition",
            analysis_job_id=42,
            operator_id="vf_de",
            period="CQ4_2025",
        )
        assert fb.analysis_job_id == 42
        assert fb.operator_id == "vf_de"
        assert fb.period == "CQ4_2025"

    def test_to_dict_keys(self):
        fb = UserFeedback(look_category="self")
        d = fb.to_dict()
        expected_keys = {
            "look_category", "finding_ref", "feedback_type",
            "original_value", "user_comment", "user_value",
            "analysis_job_id", "operator_id", "period", "created_at",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_created_at_iso(self):
        fb = UserFeedback(look_category="swot")
        d = fb.to_dict()
        # Should be an ISO string
        assert isinstance(d["created_at"], str)
        # Should be parseable
        datetime.fromisoformat(d["created_at"])

    def test_to_dict_values(self):
        fb = UserFeedback(
            look_category="trends",
            finding_ref="pest_eco",
            feedback_type="disputed",
            user_comment="Disagree with projection",
            analysis_job_id=7,
            operator_id="dt_de",
            period="CQ4_2025",
        )
        d = fb.to_dict()
        assert d["look_category"] == "trends"
        assert d["finding_ref"] == "pest_eco"
        assert d["feedback_type"] == "disputed"
        assert d["user_comment"] == "Disagree with projection"
        assert d["analysis_job_id"] == 7
        assert d["operator_id"] == "dt_de"
        assert d["period"] == "CQ4_2025"


# =====================================================================
# Schema Tests
# =====================================================================

class TestFeedbackSchema:
    def setup_method(self):
        self.db = TelecomDatabase(":memory:")
        self.db.init()

    def teardown_method(self):
        self.db.close()

    def test_user_feedback_table_exists(self):
        rows = self.db.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='user_feedback'"
        ).fetchall()
        assert len(rows) == 1

    def test_new_columns_exist(self):
        info = self.db.conn.execute("PRAGMA table_info(user_feedback)").fetchall()
        col_names = [row["name"] for row in info]
        assert "analysis_job_id" in col_names
        assert "operator_id" in col_names
        assert "period" in col_names

    def test_unique_constraint(self):
        """Inserting duplicate (job, operator, look, finding) should trigger conflict."""
        self.db.upsert_feedback({
            "analysis_job_id": 1, "operator_id": "vf_de",
            "look_category": "trends", "finding_ref": "pest_eco",
            "feedback_type": "confirmed", "user_comment": "ok",
        })
        self.db.upsert_feedback({
            "analysis_job_id": 1, "operator_id": "vf_de",
            "look_category": "trends", "finding_ref": "pest_eco",
            "feedback_type": "disputed", "user_comment": "changed mind",
        })
        rows = self.db.get_feedback(analysis_job_id=1)
        # Should be 1 row (upserted), not 2
        assert len(rows) == 1
        assert rows[0]["feedback_type"] == "disputed"

    def test_feedback_index_exists(self):
        indexes = self.db.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_feedback_job'"
        ).fetchall()
        assert len(indexes) == 1


# =====================================================================
# Upsert Tests
# =====================================================================

class TestFeedbackUpsert:
    def setup_method(self):
        self.db = TelecomDatabase(":memory:")
        self.db.init()

    def teardown_method(self):
        self.db.close()

    def test_insert_new(self):
        self.db.upsert_feedback({
            "analysis_job_id": 1, "operator_id": "vf_de",
            "look_category": "trends", "finding_ref": "pest_eco",
            "feedback_type": "confirmed", "user_comment": "Agree",
        })
        rows = self.db.get_feedback(analysis_job_id=1)
        assert len(rows) == 1
        assert rows[0]["user_comment"] == "Agree"

    def test_upsert_update(self):
        base = {
            "analysis_job_id": 1, "operator_id": "vf_de",
            "look_category": "competition", "finding_ref": "porter_rivalry",
        }
        self.db.upsert_feedback({**base, "feedback_type": "confirmed", "user_comment": "v1"})
        self.db.upsert_feedback({**base, "feedback_type": "modified", "user_comment": "v2"})
        rows = self.db.get_feedback(analysis_job_id=1)
        assert len(rows) == 1
        assert rows[0]["feedback_type"] == "modified"
        assert rows[0]["user_comment"] == "v2"

    def test_multiple_findings(self):
        for i, finding in enumerate(["pest_eco", "pest_tech", "pest_social"]):
            self.db.upsert_feedback({
                "analysis_job_id": 1, "operator_id": "vf_de",
                "look_category": "trends", "finding_ref": finding,
                "feedback_type": "confirmed", "user_comment": f"note_{i}",
            })
        rows = self.db.get_feedback(analysis_job_id=1)
        assert len(rows) == 3

    def test_period_stored(self):
        self.db.upsert_feedback({
            "analysis_job_id": 5, "operator_id": "dt_de",
            "look_category": "self", "finding_ref": "bmc_vp",
            "feedback_type": "supplemented", "period": "CQ4_2025",
        })
        rows = self.db.get_feedback(analysis_job_id=5)
        assert rows[0]["period"] == "CQ4_2025"


# =====================================================================
# Query Tests
# =====================================================================

class TestFeedbackQuery:
    def setup_method(self):
        self.db = TelecomDatabase(":memory:")
        self.db.init()
        # Seed test data
        for look in ["trends", "market", "competition"]:
            self.db.upsert_feedback({
                "analysis_job_id": 1, "operator_id": "vf_de",
                "look_category": look, "finding_ref": f"{look}_item",
                "feedback_type": "confirmed",
            })
        self.db.upsert_feedback({
            "analysis_job_id": 1, "operator_id": "dt_de",
            "look_category": "trends", "finding_ref": "pest_eco",
            "feedback_type": "disputed",
        })
        self.db.upsert_feedback({
            "analysis_job_id": 2, "operator_id": "vf_de",
            "look_category": "trends", "finding_ref": "pest_eco",
            "feedback_type": "modified",
        })

    def teardown_method(self):
        self.db.close()

    def test_filter_by_job(self):
        rows = self.db.get_feedback(analysis_job_id=1)
        assert len(rows) == 4

    def test_filter_by_operator(self):
        rows = self.db.get_feedback(analysis_job_id=1, operator_id="vf_de")
        assert len(rows) == 3

    def test_filter_by_look_category(self):
        rows = self.db.get_feedback(analysis_job_id=1, look_category="trends")
        assert len(rows) == 2  # vf_de + dt_de

    def test_filter_combined(self):
        rows = self.db.get_feedback(
            analysis_job_id=1, operator_id="vf_de", look_category="trends"
        )
        assert len(rows) == 1

    def test_no_filters_returns_all(self):
        rows = self.db.get_feedback()
        assert len(rows) == 5

    def test_job_isolation(self):
        rows = self.db.get_feedback(analysis_job_id=2)
        assert len(rows) == 1
        assert rows[0]["feedback_type"] == "modified"


# =====================================================================
# Clear Tests
# =====================================================================

class TestFeedbackClear:
    def setup_method(self):
        self.db = TelecomDatabase(":memory:")
        self.db.init()
        for finding in ["a", "b", "c"]:
            self.db.upsert_feedback({
                "analysis_job_id": 1, "operator_id": "vf_de",
                "look_category": "trends", "finding_ref": finding,
                "feedback_type": "confirmed",
            })
        self.db.upsert_feedback({
            "analysis_job_id": 1, "operator_id": "dt_de",
            "look_category": "trends", "finding_ref": "x",
            "feedback_type": "confirmed",
        })

    def teardown_method(self):
        self.db.close()

    def test_clear_removes_records(self):
        count = self.db.clear_feedback(1, "vf_de")
        assert count == 3
        remaining = self.db.get_feedback(analysis_job_id=1, operator_id="vf_de")
        assert len(remaining) == 0

    def test_clear_job_isolation(self):
        """Clearing vf_de should not affect dt_de."""
        self.db.clear_feedback(1, "vf_de")
        remaining = self.db.get_feedback(analysis_job_id=1, operator_id="dt_de")
        assert len(remaining) == 1

    def test_clear_nonexistent_returns_zero(self):
        count = self.db.clear_feedback(999, "nobody")
        assert count == 0
