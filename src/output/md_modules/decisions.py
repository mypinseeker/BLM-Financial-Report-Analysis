"""Module 06: Three Decisions — Strategy, Key Tasks, Execution renderer.

Produces the Three Decisions section containing:
1. Strategic Direction (4 pillars)
2. Key Tasks by Domain (prioritized)
3. Execution Roadmap (quarterly milestones)
4. Governance & Risk Management
5. Strategic Traps to Avoid
"""
from __future__ import annotations

from ..md_utils import (
    section_header, md_table, bold, bullet_list,
    safe_get, safe_list,
)


def render_decisions(result, diagnosis, config) -> str:
    """Render Three Decisions module from FiveLooksResult + StrategicDiagnosis."""
    try:
        from src.blm.three_decisions_engine import ThreeDecisionsComputer
        decisions = ThreeDecisionsComputer(result, diagnosis, config).compute()
    except Exception as e:
        return f"\n*Three Decisions generation failed: {e}*\n"

    parts = []

    # Section header
    parts.append(section_header("Three Decisions — Strategy & Execution", 2))
    parts.append(f"> {bold('Diagnosis')}: {decisions.diagnosis_label}")
    parts.append(f"> {bold('Posture')}: {decisions.strategy.competitive_posture}")
    parts.append(f"> {bold('Direction')}: {decisions.strategy.overall_direction}")
    parts.append("")

    # Decision 1: Strategy
    parts.append(section_header("Decision 1: Define Strategy", 3))
    parts.append(decisions.strategy.overall_direction)
    parts.append("")

    rows = []
    for p in decisions.strategy.pillars:
        kpi_str = "; ".join(p.kpis[:3])
        rows.append([p.priority, p.name, p.direction, kpi_str])
    if rows:
        parts.append(md_table(
            ["Priority", "Pillar", "Direction", "KPIs"],
            rows,
        ))
    parts.append("")

    # Decision 2: Key Tasks
    parts.append(section_header("Decision 2: Define Key Tasks", 3))
    parts.append(f"Resource allocation: {decisions.key_tasks.resource_implication}")
    parts.append("")

    task_rows = []
    for t in decisions.key_tasks.tasks:
        kpi_str = "; ".join(t.kpis[:2])
        task_rows.append([t.priority, t.domain, t.name, t.description[:60], kpi_str])
    if task_rows:
        parts.append(md_table(
            ["Priority", "Domain", "Task", "Description", "KPIs"],
            task_rows,
        ))
    parts.append("")

    # Decision 3: Execution
    parts.append(section_header("Decision 3: Define Execution", 3))

    # Milestones
    parts.append(section_header("Quarterly Roadmap", 4))
    for ms in decisions.execution.milestones:
        parts.append(f"**{ms.quarter}: {ms.name}** ({ms.priority})")
        for d in ms.deliverables:
            parts.append(f"  - {d}")
        parts.append("")

    # Governance
    if decisions.execution.governance:
        parts.append(section_header("Governance", 4))
        for g in decisions.execution.governance:
            parts.append(f"- **{g.mechanism}** ({g.cadence}): {g.description}")
        parts.append("")

    # Traps to avoid
    if decisions.execution.traps_to_avoid:
        parts.append(section_header("Strategic Traps to Avoid", 4))
        for trap in decisions.execution.traps_to_avoid:
            if isinstance(trap, dict):
                parts.append(f"- **{trap.get('trap', '')}**: "
                             f"{trap.get('temptation', '')} — "
                             f"Reality: {trap.get('reality', '')}")
            else:
                parts.append(f"- {trap}")
        parts.append("")

    # Risks
    if decisions.execution.risk_mitigation:
        parts.append(section_header("Key Risks & Mitigation", 4))
        risk_rows = []
        for r in decisions.execution.risk_mitigation:
            risk_rows.append([
                r.get("risk", ""),
                r.get("likelihood", ""),
                r.get("mitigation", ""),
            ])
        parts.append(md_table(["Risk", "Likelihood", "Mitigation"], risk_rows))
        parts.append("")

    # Narrative summary
    parts.append(section_header("Strategic Narrative", 4))
    parts.append(decisions.narrative)

    return "\n".join(parts)
