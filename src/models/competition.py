"""Data models for Look 3: Competition (Porter's Five Forces)."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CompetitorImplication:
    implication_type: str       # "opportunity" / "threat" / "learning" / "puzzling"
    description: str = ""
    evidence: list[str] = field(default_factory=list)
    suggested_action: str = ""


@dataclass
class PorterForce:
    force_name: str             # "existing_competitors" / "new_entrants" / "substitutes" / "supplier_power" / "buyer_power"
    force_level: str = "medium"  # "high" / "medium" / "low"
    key_factors: list[dict] = field(default_factory=list)  # [{name, description, impact, trend}]
    implications: list[str] = field(default_factory=list)


@dataclass
class CompetitorDeepDive:
    operator: str
    # Basic health check
    financial_health: dict = field(default_factory=dict)
    subscriber_health: dict = field(default_factory=dict)
    network_status: dict = field(default_factory=dict)
    # Enhanced dimensions
    product_portfolio: list[str] = field(default_factory=list)
    new_product_pipeline: list[str] = field(default_factory=list)
    growth_strategy: str = ""
    supply_chain_status: str = ""
    ecosystem_partners: list[str] = field(default_factory=list)
    core_control_points: list[str] = field(default_factory=list)
    business_model: str = ""
    org_structure: str = ""
    incentive_system: str = ""
    talent_culture: str = ""
    ma_activity: list[str] = field(default_factory=list)
    # Diagnosis
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)
    likely_future_actions: list[str] = field(default_factory=list)
    implications: list[CompetitorImplication] = field(default_factory=list)


@dataclass
class CompetitionInsight:
    """Complete output of Look 3: Competition."""
    five_forces: dict = field(default_factory=dict)  # {force_name: PorterForce}
    overall_competition_intensity: str = "medium"  # "high" / "medium" / "low"
    competitor_analyses: dict = field(default_factory=dict)  # {operator_id: CompetitorDeepDive}
    comparison_table: dict = field(default_factory=dict)  # {metric: {operator: value}}
    competitive_landscape: str = ""
    key_message: str = ""
