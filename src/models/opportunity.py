"""Data models for Look 5: Opportunities (SPAN Matrix)."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SPANPosition:
    """Position on the SPAN (Strategy Positioning and Action Navigation) matrix."""
    opportunity_name: str
    # Market attractiveness (Y-axis) -- weighted average
    market_size_score: float = 0.0       # 1-10
    market_growth_score: float = 0.0     # 1-10
    profit_potential_score: float = 0.0  # 1-10
    strategic_value_score: float = 0.0   # 1-10
    market_attractiveness: float = 0.0   # Computed: weighted average
    # Competitive position (X-axis) -- weighted average
    market_share_score: float = 0.0      # 1-10
    product_fit_score: float = 0.0       # 1-10
    brand_channel_score: float = 0.0     # 1-10
    tech_capability_score: float = 0.0   # 1-10
    competitive_position: float = 0.0    # Computed: weighted average
    # SPAN quadrant
    quadrant: str = ""                   # "grow_invest" / "acquire_skills" / "harvest" / "avoid_exit"
    recommended_strategy: str = ""
    bubble_size: float = 1.0             # For bubble chart (proportional to market size)


@dataclass
class OpportunityItem:
    name: str
    description: str = ""
    derived_from: list[str] = field(default_factory=list)  # Which analyses it came from
    addressable_market: str = "N/A"      # "N/A" if unknown, never fabricate
    addressable_market_source: str = ""
    our_capability: str = ""
    competition_intensity: str = ""
    time_window: str = ""                # "immediate" / "1-2 years" / "3-5 years"
    priority: str = "P1"                 # "P0" / "P1" / "P2"
    priority_rationale: str = ""


@dataclass
class OpportunityInsight:
    """Complete output of Look 5: Opportunities."""
    # SPAN matrix positions
    span_positions: list[SPANPosition] = field(default_factory=list)
    # Grouped by quadrant
    grow_invest: list[str] = field(default_factory=list)
    acquire_skills: list[str] = field(default_factory=list)
    harvest: list[str] = field(default_factory=list)
    avoid_exit: list[str] = field(default_factory=list)
    # Time-based windows
    window_opportunities: list[str] = field(default_factory=list)
    # Detailed opportunity items
    opportunities: list[OpportunityItem] = field(default_factory=list)
    key_message: str = ""
