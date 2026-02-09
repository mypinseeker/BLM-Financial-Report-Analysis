"""Data models for user feedback (3-layer architecture)."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class UserFeedback:
    look_category: str          # "trends" / "market" / "competition" / "self" / "swot" / "opportunity"
    finding_ref: str = ""       # Reference to which finding this feedback is about
    feedback_type: str = "comment"  # "comment" / "correction" / "confirmation" / "rejection"
    original_value: Any = None
    user_comment: str = ""
    user_value: Any = None
    created_at: datetime = field(default_factory=datetime.now)
