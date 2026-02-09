"""Data models for Look 2: Market/Customer ($APPEALS Framework)."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MarketChange:
    change_type: str            # "pricing" / "merger" / "technology" / "ott" / "new_entrant"
    description: str = ""
    source: str = ""            # "peer_driven" / "external_player_driven"
    time_horizon: str = "medium_term"
    impact_type: str = "neutral"  # "opportunity" / "threat" / "both"
    impact_description: str = ""
    severity: str = "medium"
    evidence: list[str] = field(default_factory=list)


@dataclass
class CustomerSegment:
    segment_name: str
    segment_type: str = "consumer"  # "consumer" / "enterprise" / "wholesale"
    size_estimate: str = ""
    growth_trend: str = "stable"    # "growing" / "stable" / "shrinking"
    our_share: str = ""
    unmet_needs: list[str] = field(default_factory=list)
    pain_points: list[str] = field(default_factory=list)
    purchase_decision_factors: list[str] = field(default_factory=list)
    competitor_gaps: list[str] = field(default_factory=list)
    opportunity: str = ""


@dataclass
class APPEALSAssessment:
    """Assessment on one $APPEALS dimension."""
    dimension: str              # "$" / "A1" / "P1" / "P2" / "E" / "A2" / "L" / "S"
    dimension_name: str         # "Price" / "Availability" / "Packaging" / "Performance" / "Ease" / "Assurances" / "Lifecycle" / "Social"
    our_score: float = 0.0      # 1-5 scale
    competitor_scores: dict = field(default_factory=dict)  # {operator_id: score}
    customer_priority: str = "important"  # "critical" / "important" / "nice_to_have"
    gap_analysis: str = ""


@dataclass
class MarketCustomerInsight:
    """Complete output of Look 2: Market/Customer."""
    market_snapshot: dict = field(default_factory=dict)  # {total_revenue, total_subscribers, ...}
    changes: list[MarketChange] = field(default_factory=list)
    opportunities: list[MarketChange] = field(default_factory=list)
    threats: list[MarketChange] = field(default_factory=list)
    customer_segments: list[CustomerSegment] = field(default_factory=list)
    appeals_assessment: list[APPEALSAssessment] = field(default_factory=list)
    customer_value_migration: str = ""
    market_outlook: str = "mixed"  # "favorable" / "challenging" / "mixed"
    key_message: str = ""
