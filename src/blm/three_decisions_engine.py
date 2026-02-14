"""Three Decisions Engine — rule-based strategic decision derivation.

Transforms FiveLooksResult + StrategicDiagnosis into three actionable decisions:
  1. Define Strategy (定策略)
  2. Define Key Tasks (定重点工作)
  3. Define Execution (定执行)

All computation is deterministic and rule-based (no AI/LLM dependency).
"""
from __future__ import annotations

from src.models.decisions import (
    ThreeDecisions, StrategyDecision, StrategicPillar,
    KeyTasksDecision, KeyTask,
    ExecutionDecision, Milestone, GovernanceItem,
)


class ThreeDecisionsComputer:
    """Compute Three Decisions from FiveLooksResult + StrategicDiagnosis."""

    def __init__(self, result, diagnosis, config=None):
        self.r = result
        self.d = diagnosis
        self.config = config

    def compute(self) -> ThreeDecisions:
        strategy = self._compute_strategy()
        key_tasks = self._compute_key_tasks()
        execution = self._compute_execution(key_tasks)
        narrative = self._build_narrative(strategy, key_tasks)

        return ThreeDecisions(
            strategy=strategy,
            key_tasks=key_tasks,
            execution=execution,
            narrative=narrative,
            diagnosis_label=self.d.central_diagnosis_label or "Unknown",
        )

    # ------------------------------------------------------------------
    # Decision 1: Strategy
    # ------------------------------------------------------------------

    def _compute_strategy(self) -> StrategyDecision:
        rank = self.d.operator_rank or 3
        stance = self.d.competitive_stance or "Balanced"
        fh = _safe_dict(self.r.self_analysis, "financial_health")

        pillars = [
            self._growth_pillar(rank, fh),
            self._competitive_pillar(rank, stance),
            self._transformation_pillar(),
            self._customer_pillar(),
        ]

        theme = self._overall_direction(rank, stance)
        return StrategyDecision(
            pillars=pillars,
            overall_direction=theme,
            competitive_posture=stance.split("(")[0].strip() if stance else "Balanced",
        )

    def _growth_pillar(self, rank: int, fh: dict) -> StrategicPillar:
        yoy = fh.get("revenue_yoy_pct", 0) or 0
        # Identify best growth segments
        grow_segs = self._segments_by_action("GROW")
        seg_names = ", ".join(s.segment_name for s in grow_segs[:3]) or "core segments"

        if rank == 1:
            direction = f"Defend leadership through ecosystem expansion in {seg_names}"
            kpis = ["Maintain #1 revenue share", f"Grow {seg_names} by 5-8% YoY"]
        elif rank == 2:
            direction = f"Close the gap to market leader — accelerate {seg_names}"
            kpis = ["Gain 1-2pp revenue share", f"Grow {seg_names} double-digit"]
        else:
            direction = f"Focused growth in high-momentum segments: {seg_names}"
            kpis = [f"Grow {seg_names} above market rate", "Improve segment profitability"]

        return StrategicPillar(
            name="Growth Strategy",
            direction=direction,
            rationale=f"Revenue YoY {yoy:+.1f}%, rank #{rank} in market",
            priority="P0",
            kpis=kpis,
        )

    def _competitive_pillar(self, rank: int, stance: str) -> StrategicPillar:
        weaknesses = _safe_list(self.r.self_analysis, "weaknesses")
        top_weakness = weaknesses[0] if weaknesses else "operational gaps"

        if "Offensive" in stance:
            direction = "Capitalize on competitive strengths to gain market share"
            kpis = ["Outgrow competitors in key segments", "Increase service differentiation"]
        elif "Defensive" in stance or "Turnaround" in stance:
            direction = f"Shore up competitive position — address: {top_weakness}"
            kpis = [f"Close {top_weakness} gap within 12 months", "Reduce customer churn"]
        else:
            direction = "Differentiate on quality and innovation to justify premium positioning"
            kpis = ["Improve NPS by 5 points", "Launch 2+ differentiating services"]

        return StrategicPillar(
            name="Competitive Strategy",
            direction=direction,
            rationale=f"Stance: {stance}, {len(weaknesses)} identified weaknesses",
            priority="P0",
            kpis=kpis,
        )

    def _transformation_pillar(self) -> StrategicPillar:
        net = getattr(self.r.self_analysis, "network", None)
        evolution = ""
        if net and hasattr(net, "evolution_strategy"):
            ev = net.evolution_strategy
            if isinstance(ev, dict):
                evolution = ev.get("summary", "")
            elif isinstance(ev, str):
                evolution = ev

        if "fiber" in evolution.lower() or "ftth" in evolution.lower():
            direction = "Accelerate fiber transition — converged network as competitive moat"
            kpis = ["Fiber homepass coverage +20%", "FMC bundle attach rate 50%+"]
        elif "5g" in evolution.lower():
            direction = "5G-first network modernization — quality leadership"
            kpis = ["5G population coverage 80%+", "5G revenue contribution 15%+"]
        else:
            direction = "Network modernization to close infrastructure gaps"
            kpis = ["Capex efficiency improvement", "Network quality score top 2"]

        return StrategicPillar(
            name="Transformation Strategy",
            direction=direction,
            rationale=f"Network evolution: {evolution[:80]}..." if evolution else "Network data limited",
            priority="P1",
            kpis=kpis,
        )

    def _customer_pillar(self) -> StrategicPillar:
        segs = _safe_list(self.r.self_analysis, "segment_analyses")
        maintain_segs = [s for s in segs if "MAINTAIN" in (getattr(s, "action_required", "") or "")]
        urgent_segs = [s for s in segs if "URGENT" in (getattr(s, "action_required", "") or "")]

        if urgent_segs:
            names = ", ".join(s.segment_name for s in urgent_segs[:2])
            direction = f"Urgent customer retention in {names} — stop value erosion"
            kpis = [f"Reduce {names} churn by 20%", "Improve segment ARPU"]
            priority = "P0"
        elif maintain_segs:
            names = ", ".join(s.segment_name for s in maintain_segs[:2])
            direction = f"Optimize value extraction in stable segments: {names}"
            kpis = [f"Upsell rate +10% in {names}", "Cross-sell convergence bundles"]
            priority = "P1"
        else:
            direction = "Customer-centric value management across all segments"
            kpis = ["ARPU growth above inflation", "Churn reduction to market best"]
            priority = "P1"

        return StrategicPillar(
            name="Customer Strategy",
            direction=direction,
            rationale=f"{len(urgent_segs)} urgent + {len(maintain_segs)} stable segments",
            priority=priority,
            kpis=kpis,
        )

    def _overall_direction(self, rank: int, stance: str) -> str:
        label = self.d.central_diagnosis_label or ""
        if rank == 1:
            return f"As {label}: defend leadership through innovation and ecosystem lock-in"
        elif rank == 2 and "Offensive" in stance:
            return f"As {label}: close the leadership gap with aggressive growth in high-momentum segments"
        elif "Defensive" in stance or "Turnaround" in stance:
            return f"As {label}: stabilize core business, then selectively invest for turnaround"
        else:
            return f"As {label}: differentiate and grow through focused investment in competitive advantages"

    # ------------------------------------------------------------------
    # Decision 2: Key Tasks
    # ------------------------------------------------------------------

    def _compute_key_tasks(self) -> KeyTasksDecision:
        tasks = []

        # Network tasks — from network analysis
        tasks.extend(self._network_tasks())
        # Business tasks — from growth segments + opportunities
        tasks.extend(self._business_tasks())
        # Customer tasks — from segment health
        tasks.extend(self._customer_tasks())
        # Efficiency tasks — from financial metrics
        tasks.extend(self._efficiency_tasks())

        # Sort by priority
        priority_order = {"P0": 0, "P1": 1, "P2": 2}
        tasks.sort(key=lambda t: priority_order.get(t.priority, 9))

        resource = self._estimate_resources(tasks)
        return KeyTasksDecision(tasks=tasks[:8], resource_implication=resource)

    def _network_tasks(self) -> list[KeyTask]:
        tasks = []
        net = getattr(self.r.self_analysis, "network", None)
        evolution = ""
        if net and hasattr(net, "evolution_strategy"):
            ev = net.evolution_strategy
            if isinstance(ev, dict):
                evolution = ev.get("summary", "")

        if "fiber" in evolution.lower() or "cable" in evolution.lower():
            tasks.append(KeyTask(
                name="Accelerate Fixed Network Upgrade",
                domain="Network",
                description="Drive DOCSIS/Fiber rollout to increase homepass and improve quality scores",
                priority="P0",
                kpis=["Homepass coverage +15%", "Speed tier upgrades"],
                time_window="immediate",
            ))

        if "5g" in evolution.lower():
            tasks.append(KeyTask(
                name="5G Coverage Expansion",
                domain="Network",
                description="Expand 5G population coverage to strengthen mobile competitive position",
                priority="P1",
                kpis=["5G pop coverage target", "5G attach rate"],
                time_window="1-2 years",
            ))

        if not tasks:
            tasks.append(KeyTask(
                name="Network Quality Optimization",
                domain="Network",
                description="Improve network reliability and customer experience scores",
                priority="P1",
                kpis=["Network quality index improvement"],
                time_window="immediate",
            ))

        return tasks

    def _business_tasks(self) -> list[KeyTask]:
        tasks = []
        grow_segs = self._segments_by_action("GROW")

        for seg in grow_segs[:2]:
            rev = (seg.trend_data or {}).get("revenue", [])
            latest = rev[-1] if rev else 0
            tasks.append(KeyTask(
                name=f"Accelerate {seg.segment_name} Growth",
                domain="Business",
                description=f"{seg.segment_name} at €{latest:,.0f}M showing strong momentum — invest to scale",
                priority="P0",
                kpis=[f"{seg.segment_name} revenue +10% YoY", "Market share gain"],
                time_window="immediate",
            ))

        # Add opportunity-driven task from SPAN grow_invest
        opps = getattr(self.r, "opportunities", None)
        gi_count = sum(1 for sp in (opps.span_positions or [])
                       if sp.quadrant == "grow_invest") if opps else 0
        if gi_count > 5:
            tasks.append(KeyTask(
                name="Opportunity Portfolio Execution",
                domain="Business",
                description=f"{gi_count} grow/invest opportunities identified — establish execution office",
                priority="P1",
                kpis=["Launch 3+ priority initiatives", "Pipeline contribution tracking"],
                time_window="1-2 years",
            ))

        return tasks

    def _customer_tasks(self) -> list[KeyTask]:
        tasks = []
        segs = _safe_list(self.r.self_analysis, "segment_analyses")

        # Segments needing attention
        urgent = [s for s in segs if "URGENT" in (getattr(s, "action_required", "") or "")]
        declining = [s for s in segs
                     if "MONITOR" in (getattr(s, "action_required", "") or "")
                     or "SUSTAIN" in (getattr(s, "action_required", "") or "")]

        if urgent:
            names = ", ".join(s.segment_name for s in urgent[:2])
            tasks.append(KeyTask(
                name=f"Customer Retention — {names}",
                domain="Customer",
                description=f"Urgent: {names} showing decline — deploy retention programs",
                priority="P0",
                kpis=["Churn reduction 20%", "Save rate improvement"],
                time_window="immediate",
            ))

        if declining:
            names = ", ".join(s.segment_name for s in declining[:2])
            tasks.append(KeyTask(
                name=f"Stabilize {names}",
                domain="Customer",
                description=f"Monitor {names} performance — prepare intervention if decline continues",
                priority="P1",
                kpis=["Subscriber trend stabilization", "ARPU floor maintenance"],
                time_window="1-2 years",
            ))

        # General CX task
        tasks.append(KeyTask(
            name="Customer Experience Enhancement",
            domain="Customer",
            description="Improve digital touchpoints and service resolution to boost NPS",
            priority="P1",
            kpis=["NPS +5 points", "First-call resolution rate 80%+"],
            time_window="1-2 years",
        ))

        return tasks

    def _efficiency_tasks(self) -> list[KeyTask]:
        fh = _safe_dict(self.r.self_analysis, "financial_health")
        margin = fh.get("ebitda_margin_pct", 0) or 0

        tasks = []
        if margin < 30:
            tasks.append(KeyTask(
                name="Margin Recovery Program",
                domain="Efficiency",
                description=f"EBITDA margin at {margin:.1f}% — below industry average, drive cost optimization",
                priority="P0",
                kpis=["EBITDA margin +2pp", "Opex reduction 5%"],
                time_window="immediate",
            ))
        else:
            tasks.append(KeyTask(
                name="Operational Efficiency & Automation",
                domain="Efficiency",
                description=f"EBITDA margin {margin:.1f}% — maintain through smart automation and resource reallocation",
                priority="P2",
                kpis=["Process automation 30%+", "Cost-to-serve reduction"],
                time_window="3-5 years",
            ))

        return tasks

    # ------------------------------------------------------------------
    # Decision 3: Execution
    # ------------------------------------------------------------------

    def _compute_execution(self, key_tasks: KeyTasksDecision) -> ExecutionDecision:
        milestones = self._build_milestones(key_tasks.tasks)
        governance = self._build_governance()
        traps = [t for t in (self.d.strategic_traps or []) if t]
        risks = self._build_risks()

        return ExecutionDecision(
            milestones=milestones,
            governance=governance,
            risk_mitigation=risks,
            traps_to_avoid=traps,
        )

    def _build_milestones(self, tasks: list[KeyTask]) -> list[Milestone]:
        p0_tasks = [t for t in tasks if t.priority == "P0"]
        p1_tasks = [t for t in tasks if t.priority == "P1"]

        milestones = [
            Milestone(
                quarter="Q1",
                name="Foundation & Quick Wins",
                deliverables=[f"Launch: {t.name}" for t in p0_tasks[:3]] +
                             ["Establish governance cadence", "Baseline KPI measurement"],
                priority="P0",
            ),
            Milestone(
                quarter="Q2",
                name="Scale & Build Capabilities",
                deliverables=[f"Scale: {t.name}" for t in p0_tasks[:3]] +
                             [f"Initiate: {t.name}" for t in p1_tasks[:2]],
                priority="P0",
            ),
            Milestone(
                quarter="Q3",
                name="Optimize & Iterate",
                deliverables=["Mid-year review and course correction",
                              "Optimize P0 initiatives based on Q1-Q2 data",
                              "Expand P1 initiatives to full scale"],
                priority="P1",
            ),
            Milestone(
                quarter="Q4",
                name="Assess & Plan Next Year",
                deliverables=["Year-end results assessment",
                              "Lessons learned documentation",
                              "Next-year strategy refresh based on outcomes"],
                priority="P1",
            ),
        ]
        return milestones

    def _build_governance(self) -> list[GovernanceItem]:
        return [
            GovernanceItem(
                mechanism="Monthly Progress Review",
                cadence="Monthly",
                description="Track P0 task progress, KPI trends, and resource utilization",
            ),
            GovernanceItem(
                mechanism="Quarterly Strategic Checkpoint",
                cadence="Quarterly",
                description="Evaluate strategy execution, adjust priorities, reallocate resources",
            ),
            GovernanceItem(
                mechanism="Mid-Year Strategic Adjustment",
                cadence="Semi-annual",
                description="Major review of market conditions and strategy effectiveness",
            ),
        ]

    def _build_risks(self) -> list[dict]:
        risks = []
        # Competitive risk
        comp = self.r.competition
        if comp and hasattr(comp, "five_forces"):
            forces = comp.five_forces or []
            high_forces = [f for f in forces if getattr(f, "intensity", "") in ("high", "very_high")]
            if high_forces:
                risks.append({
                    "risk": "Competitive intensity escalation",
                    "likelihood": "Medium-High",
                    "mitigation": "Monitor competitor moves monthly; maintain pricing flexibility",
                })

        # Execution risk
        risks.append({
            "risk": "Resource constraints delay P0 initiatives",
            "likelihood": "Medium",
            "mitigation": "Ring-fence P0 budgets; establish escalation path for blockers",
        })

        # Market risk
        risks.append({
            "risk": "Macro-economic slowdown reduces consumer spending",
            "likelihood": "Low-Medium",
            "mitigation": "Prepare value-tier offerings; shift mix toward B2B resilience",
        })

        return risks

    # ------------------------------------------------------------------
    # Narrative
    # ------------------------------------------------------------------

    def _build_narrative(self, strategy: StrategyDecision, key_tasks: KeyTasksDecision) -> str:
        label = self.d.central_diagnosis_label or "the operator"
        stance = strategy.competitive_posture
        p0_count = sum(1 for t in key_tasks.tasks if t.priority == "P0")
        total = len(key_tasks.tasks)
        domains = sorted(set(t.domain for t in key_tasks.tasks))
        domain_str = ", ".join(domains)

        return (
            f"As {label}, the strategic posture is {stance}. "
            f"{strategy.overall_direction}. "
            f"Execution focuses on {p0_count} P0-priority tasks out of {total} across "
            f"{domain_str}, with quarterly milestones and monthly governance checkpoints."
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _segments_by_action(self, keyword: str) -> list:
        segs = _safe_list(self.r.self_analysis, "segment_analyses")
        return [s for s in segs if keyword in (getattr(s, "action_required", "") or "")]

    def _estimate_resources(self, tasks: list[KeyTask]) -> str:
        p0 = sum(1 for t in tasks if t.priority == "P0")
        p1 = sum(1 for t in tasks if t.priority == "P1")
        p2 = sum(1 for t in tasks if t.priority == "P2")
        return f"{p0} P0 (immediate), {p1} P1 (1-2 years), {p2} P2 (3-5 years)"


# ---------------------------------------------------------------------------
# Safe accessors
# ---------------------------------------------------------------------------

def _safe_dict(obj, attr: str) -> dict:
    if obj is None:
        return {}
    val = getattr(obj, attr, None)
    return val if isinstance(val, dict) else {}


def _safe_list(obj, attr: str) -> list:
    if obj is None:
        return []
    val = getattr(obj, attr, None)
    return val if isinstance(val, list) else []
