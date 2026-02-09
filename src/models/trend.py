"""Data models for Look 1: Trends (PEST Framework)."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PESTFactor:
    """A single factor within one PEST dimension."""
    dimension: str              # "P" / "E" / "S" / "T"
    dimension_name: str         # "Political" / "Economic" / "Society" / "Technology"
    factor_name: str            # e.g., "Gigabit Strategy", "GDP Growth"
    current_status: str = ""    # Description of current state
    trend: str = ""             # Description of how it's changing
    trend_direction: str = "stable"  # "improving" / "worsening" / "stable" / "uncertain"
    industry_impact: str = ""   # Impact on the telecom industry
    company_impact: str = ""    # Specific impact on target company
    impact_type: str = "neutral"  # "opportunity" / "threat" / "neutral" / "both"
    severity: str = "medium"    # "high" / "medium" / "low"
    time_horizon: str = "medium_term"  # "short_term" / "medium_term" / "long_term"
    predictability: str = "uncertain"  # "predictable" / "uncertain" / "volatile"
    evidence: list[str] = field(default_factory=list)
    data_source: str = ""


@dataclass
class PESTAnalysis:
    """Complete PEST analysis across four dimensions."""
    political_factors: list[PESTFactor] = field(default_factory=list)
    economic_factors: list[PESTFactor] = field(default_factory=list)
    society_factors: list[PESTFactor] = field(default_factory=list)
    technology_factors: list[PESTFactor] = field(default_factory=list)

    # Cross-cutting summaries
    overall_weather: str = "mixed"  # "sunny" / "cloudy" / "stormy" / "mixed"
    weather_explanation: str = ""
    policy_opportunities: list[str] = field(default_factory=list)
    policy_threats: list[str] = field(default_factory=list)
    tech_addressable_market: str = ""
    key_message: str = ""


@dataclass
class TrendAnalysis:
    """Complete output of Look 1: Trends."""
    pest: PESTAnalysis = field(default_factory=PESTAnalysis)

    # Industry environment
    industry_market_size: str = ""
    industry_growth_rate: str = ""
    industry_profit_trend: str = ""
    industry_concentration: str = ""      # e.g., "CR4 = 95%"
    industry_lifecycle_stage: str = ""    # "growth" / "mature" / "decline"
    new_business_models: list[str] = field(default_factory=list)
    technology_revolution: list[str] = field(default_factory=list)
    key_success_factors: list[str] = field(default_factory=list)
    value_transfer_trends: list[str] = field(default_factory=list)

    key_message: str = ""
