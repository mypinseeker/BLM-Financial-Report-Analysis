"""Data models for user feedback (3-layer architecture)."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


FEEDBACK_TYPES = ("confirmed", "disputed", "modified", "supplemented")


@dataclass
class UserFeedback:
    look_category: str          # "trends" / "market" / "competition" / "self" / "swot" / "opportunity"
    finding_ref: str = ""       # Reference to which finding this feedback is about
    feedback_type: str = "confirmed"  # confirmed / disputed / modified / supplemented
    original_value: Any = None
    user_comment: str = ""
    user_value: Any = None
    analysis_job_id: int = 0
    operator_id: str = ""
    period: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Serialize to dict with ISO-formatted created_at."""
        return {
            "look_category": self.look_category,
            "finding_ref": self.finding_ref,
            "feedback_type": self.feedback_type,
            "original_value": self.original_value,
            "user_comment": self.user_comment,
            "user_value": self.user_value,
            "analysis_job_id": self.analysis_job_id,
            "operator_id": self.operator_id,
            "period": self.period,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
