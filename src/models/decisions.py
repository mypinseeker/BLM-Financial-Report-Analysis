"""Data models for BLM Three Decisions (三定).

Decision 1: Define Strategy (定策略) — Strategic direction and positioning
Decision 2: Define Key Tasks (定重点工作) — Critical initiatives by domain
Decision 3: Define Execution (定执行) — Quarterly roadmap, governance, KPIs
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class StrategicPillar:
    """One of 4 strategic pillars in the Strategy Decision."""
    name: str               # e.g., "Growth Strategy"
    direction: str          # e.g., "Aggressive market share gains in B2B"
    rationale: str          # Why this direction was chosen
    priority: str = "P1"    # P0 / P1 / P2
    kpis: list[str] = field(default_factory=list)


@dataclass
class StrategyDecision:
    """Decision 1: Define Strategy (定策略)."""
    pillars: list[StrategicPillar] = field(default_factory=list)
    overall_direction: str = ""     # 1-sentence strategic theme
    competitive_posture: str = ""   # Offensive / Defensive / Turnaround / Cautious


@dataclass
class KeyTask:
    """A single critical task in the Key Tasks Decision."""
    name: str
    domain: str             # Network / Business / Customer / Efficiency
    description: str
    priority: str = "P1"    # P0 / P1 / P2
    owner: str = ""         # Functional area responsible
    kpis: list[str] = field(default_factory=list)
    time_window: str = ""   # immediate / 1-2 years / 3-5 years


@dataclass
class KeyTasksDecision:
    """Decision 2: Define Key Tasks (定重点工作)."""
    tasks: list[KeyTask] = field(default_factory=list)
    resource_implication: str = ""


@dataclass
class Milestone:
    """A quarterly execution milestone."""
    quarter: str        # Q1 / Q2 / Q3 / Q4
    name: str
    deliverables: list[str] = field(default_factory=list)
    priority: str = "P0"


@dataclass
class GovernanceItem:
    """A governance mechanism for execution oversight."""
    mechanism: str      # e.g., "Monthly Progress Review"
    cadence: str        # e.g., "Monthly", "Quarterly"
    description: str = ""


@dataclass
class ExecutionDecision:
    """Decision 3: Define Execution (定执行)."""
    milestones: list[Milestone] = field(default_factory=list)
    governance: list[GovernanceItem] = field(default_factory=list)
    risk_mitigation: list[dict] = field(default_factory=list)
    traps_to_avoid: list[dict] = field(default_factory=list)


@dataclass
class ThreeDecisions:
    """Container for all three BLM decisions."""
    strategy: StrategyDecision = field(default_factory=StrategyDecision)
    key_tasks: KeyTasksDecision = field(default_factory=KeyTasksDecision)
    execution: ExecutionDecision = field(default_factory=ExecutionDecision)
    narrative: str = ""         # 2-3 sentence synthesis
    diagnosis_label: str = ""   # From StrategicDiagnosis
