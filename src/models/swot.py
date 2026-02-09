"""Data models for SWOT Synthesis."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class SWOTAnalysis:
    """SWOT Matrix with four strategy quadrants."""
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    opportunities: list[str] = field(default_factory=list)
    threats: list[str] = field(default_factory=list)
    # Four strategy quadrants
    so_strategies: list[str] = field(default_factory=list)  # Leverage strengths for opportunities
    wo_strategies: list[str] = field(default_factory=list)  # Fix weaknesses to seize opportunities
    st_strategies: list[str] = field(default_factory=list)  # Use strengths to defend against threats
    wt_strategies: list[str] = field(default_factory=list)  # Weakness + threat = exit or defend
    key_message: str = ""
