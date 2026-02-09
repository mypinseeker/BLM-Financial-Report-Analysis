"""Data models for Look 4: Self Analysis (BMC + Capability Assessment)."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class SegmentChange:
    metric: str                 # "revenue" / "subscribers" / "arpu" / "churn" / "margin"
    current_value: Any = None
    previous_value: Any = None
    yoy_value: Any = None
    change_qoq: float = 0.0
    change_yoy: float = 0.0
    direction: str = "stable"   # "improving" / "declining" / "stable"
    significance: str = "minor"  # "significant" / "moderate" / "minor"


@dataclass
class ChangeAttribution:
    attribution_type: str       # "management_explanation" / "tariff_competition" / "customer_feedback" / "market_change" / "product_change"
    description: str = ""
    confidence: str = "medium"  # "high" / "medium" / "low"
    evidence: list[str] = field(default_factory=list)
    source: str = ""            # "earnings_call" / "tariff_scraping" / "nps_survey"


@dataclass
class SegmentAnalysis:
    segment_name: str           # "Mobile" / "Fixed Broadband" / "B2B" / "TV" / "Wholesale"
    segment_id: str = ""        # "mobile" / "fixed" / "b2b" / "tv" / "wholesale"
    # Layer 1: WHAT (data)
    key_metrics: dict = field(default_factory=dict)
    changes: list[SegmentChange] = field(default_factory=list)
    trend_data: dict = field(default_factory=dict)  # {metric: [q1, q2, ...]}
    competitor_comparison: dict = field(default_factory=dict)
    # Layer 2: WHY (attribution)
    attributions: list[ChangeAttribution] = field(default_factory=list)
    # Overall judgment
    health_status: str = "stable"  # "strong" / "stable" / "weakening" / "critical"
    key_message: str = ""
    action_required: str = ""


@dataclass
class NetworkAnalysis:
    # Current state
    technology_mix: dict = field(default_factory=dict)  # {"cable": 70, "fiber": 5, ...}
    controlled_vs_resale: dict = field(default_factory=dict)  # {"self_built": 75, "resale": 25}
    coverage: dict = field(default_factory=dict)  # {"5g": 90, "4g": 99.5, ...}
    quality_scores: dict = field(default_factory=dict)  # {"connect_test": 78, ...}
    homepass_vs_connect: dict = field(default_factory=dict)
    # Evolution strategy
    evolution_strategy: dict = field(default_factory=dict)
    investment_direction: str = ""
    vs_competitors: str = ""
    # Impact assessment
    consumer_impact: str = ""
    b2b_impact: str = ""
    cost_impact: str = ""


@dataclass
class ExposurePoint:
    trigger_action: str         # "1&1 migrating 11M users onto own network"
    side_effect: str = ""       # "Network load surges on Vodafone"
    attack_vector: str = ""     # "Competitors promote 'Vodafone network is slow'"
    severity: str = "medium"    # "high" / "medium" / "low"
    evidence: list[str] = field(default_factory=list)


@dataclass
class BMCCanvas:
    """Business Model Canvas - 9 building blocks."""
    key_partners: list[str] = field(default_factory=list)
    key_activities: list[str] = field(default_factory=list)
    key_resources: list[str] = field(default_factory=list)
    value_propositions: list[str] = field(default_factory=list)
    customer_relationships: list[str] = field(default_factory=list)
    channels: list[str] = field(default_factory=list)
    customer_segments: list[str] = field(default_factory=list)
    cost_structure: list[str] = field(default_factory=list)
    revenue_streams: list[str] = field(default_factory=list)


@dataclass
class SelfInsight:
    """Complete output of Look 4: Self Analysis."""
    # Operating metrics
    financial_health: dict = field(default_factory=dict)
    revenue_breakdown: dict = field(default_factory=dict)
    # Market positions
    market_positions: dict = field(default_factory=dict)
    share_trends: dict = field(default_factory=dict)
    # Business segment deep-dives
    segment_analyses: list[SegmentAnalysis] = field(default_factory=list)
    # Network deep-dive
    network: NetworkAnalysis = field(default_factory=NetworkAnalysis)
    # Customer perception
    customer_perception: dict = field(default_factory=dict)
    # Leadership
    leadership_changes: list[dict] = field(default_factory=list)
    # BMC
    bmc: BMCCanvas = field(default_factory=BMCCanvas)
    # Organization
    org_culture: str = ""
    talent_assessment: dict = field(default_factory=dict)
    # Strategic review
    performance_gap: str = ""
    opportunity_gap: str = ""
    strategic_review: str = ""
    # Integrated judgment
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    exposure_points: list[ExposurePoint] = field(default_factory=list)
    health_rating: str = "stable"  # "healthy" / "stable" / "concerning" / "critical"
    key_message: str = ""
