"""Strategic Diagnosis Computer — rule-based cross-module insight derivation.

Examines a FiveLooksResult to produce a StrategicDiagnosis containing:
- Central diagnosis label and explanation
- One-line verdict
- Per-module net assessments
- Strategic priorities, traps, risk/reward scenarios
- KPI dashboard targets

All computation is deterministic and rule-based (no AI/LLM dependency).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .md_utils import (
    safe_get, safe_list, safe_dict, operator_display_name,
    fmt_pct, fmt_currency,
)


# ---------------------------------------------------------------------------
# Diagnosis data class
# ---------------------------------------------------------------------------

@dataclass
class StrategicDiagnosis:
    """Cross-module strategic diagnosis synthesized from FiveLooksResult."""

    one_line_verdict: str = ""
    central_diagnosis: str = ""
    central_diagnosis_label: str = ""

    # Per-module net assessments
    trends_net_assessment: str = ""
    market_net_assessment: str = ""
    competition_net_assessment: str = ""
    self_net_assessment: str = ""
    tariff_net_assessment: str = ""
    swot_net_assessment: str = ""
    opportunities_net_assessment: str = ""

    # Executive summary components
    priorities: list[dict] = field(default_factory=list)
    strategic_traps: list[dict] = field(default_factory=list)
    bull_case: dict = field(default_factory=dict)
    base_case: dict = field(default_factory=dict)
    bear_case: dict = field(default_factory=dict)
    kpi_dashboard: list[dict] = field(default_factory=list)

    # Derived descriptors
    market_structure: str = ""
    operator_rank: int = 0
    operator_position_label: str = ""
    competitive_stance: str = ""


# ---------------------------------------------------------------------------
# Computer
# ---------------------------------------------------------------------------

class StrategicDiagnosisComputer:
    """Compute a StrategicDiagnosis from FiveLooksResult + MarketConfig."""

    def __init__(self, result, config=None):
        self.result = result
        self.config = config
        self._d = StrategicDiagnosis()

    def compute(self) -> StrategicDiagnosis:
        self._compute_market_structure()
        self._compute_operator_rank()
        self._compute_competitive_stance()
        self._compute_central_diagnosis()
        self._compute_net_assessments()
        self._compute_priorities()
        self._compute_strategic_traps()
        self._compute_risk_reward()
        self._compute_kpi_dashboard()
        self._compute_one_line_verdict()
        return self._d

    # ------------------------------------------------------------------
    # Market structure
    # ------------------------------------------------------------------

    def _compute_market_structure(self):
        comp = self.result.competition
        if comp is None:
            self._d.market_structure = "unknown market structure"
            return
        n_operators = len(safe_dict(comp, "competitor_analyses")) + 1  # +1 for target
        if n_operators <= 2:
            self._d.market_structure = f"{n_operators}-operator duopoly"
        elif n_operators <= 4:
            self._d.market_structure = f"{n_operators}-operator oligopoly"
        else:
            self._d.market_structure = f"{n_operators}-operator competitive market"

    # ------------------------------------------------------------------
    # Operator rank (by revenue from comparison_table)
    # ------------------------------------------------------------------

    def _compute_operator_rank(self):
        comp = self.result.competition
        if comp is None:
            self._d.operator_rank = 0
            self._d.operator_position_label = "unknown position"
            return

        ct = safe_dict(comp, "comparison_table")
        target = self.result.target_operator

        # Try revenue metric first
        rev_data = ct.get("revenue") or ct.get("quarterly_revenue") or ct.get("total_revenue") or {}
        if not rev_data:
            # Try to extract from financial_health in competitor_analyses
            rev_data = self._extract_revenue_map()

        if not rev_data:
            self._d.operator_rank = 0
            self._d.operator_position_label = "unknown position"
            return

        # Sort operators by revenue descending
        sorted_ops = sorted(rev_data.items(), key=lambda x: _to_float(x[1]), reverse=True)
        rank = 1
        for i, (op, _) in enumerate(sorted_ops):
            if op == target or _name_match(op, target):
                rank = i + 1
                break

        self._d.operator_rank = rank
        ordinal = {1: "#1", 2: "#2", 3: "#3", 4: "#4"}.get(rank, f"#{rank}")
        self._d.operator_position_label = f"{ordinal} by revenue"

    def _extract_revenue_map(self) -> dict:
        """Extract revenue per operator from competitor deep dives + self."""
        rev_map = {}
        comp = self.result.competition
        if comp is None:
            return rev_map

        # Target operator
        self_analysis = self.result.self_analysis
        if self_analysis:
            fh = safe_dict(self_analysis, "financial_health")
            target_rev = fh.get("revenue") or fh.get("total_revenue") or fh.get("quarterly_revenue")
            if target_rev is not None:
                rev_map[self.result.target_operator] = target_rev

        # Competitors
        for op_id, dd in safe_dict(comp, "competitor_analyses").items():
            fh = safe_dict(dd, "financial_health")
            rev = fh.get("revenue") or fh.get("total_revenue") or fh.get("quarterly_revenue")
            if rev is not None:
                rev_map[op_id] = rev

        return rev_map

    # ------------------------------------------------------------------
    # Competitive stance (from SWOT balance)
    # ------------------------------------------------------------------

    def _compute_competitive_stance(self):
        swot = self.result.swot
        if swot is None:
            self._d.competitive_stance = "Unknown"
            return

        s_count = len(safe_list(swot, "strengths"))
        w_count = len(safe_list(swot, "weaknesses"))
        o_count = len(safe_list(swot, "opportunities"))
        t_count = len(safe_list(swot, "threats"))

        s_dom = s_count >= w_count
        o_dom = o_count >= t_count

        if s_dom and o_dom:
            self._d.competitive_stance = "Offensive (SO-dominant)"
        elif s_dom and not o_dom:
            self._d.competitive_stance = "Defensive (ST-dominant)"
        elif not s_dom and o_dom:
            self._d.competitive_stance = "Turnaround (WO-dominant)"
        else:
            self._d.competitive_stance = "Cautious (WT-dominant)"

    # ------------------------------------------------------------------
    # Central diagnosis label
    # ------------------------------------------------------------------

    def _compute_central_diagnosis(self):
        rank = self._d.operator_rank
        appeals_wins = self._count_appeals_wins()
        rev_gap = self._compute_revenue_gap_pp()
        health = safe_get(self.result.self_analysis, "health_rating", "stable")
        declining = self._is_declining()

        # Determine label
        if rank == 1 and self._weakness_count() < 3:
            label = "The Dominant Leader"
        elif rev_gap > 30 and appeals_wins == 0:
            pos_word = {2: "Second", 3: "Third", 4: "Fourth"}.get(rank, f"#{rank}")
            label = f"The Distant {pos_word}"
        elif rev_gap > 15 and appeals_wins == 0:
            label = "The Squeezed Middle"
        elif rev_gap > 15 and declining:
            label = "The Declining Incumbent"
        elif rev_gap < 15 and appeals_wins >= 1:
            label = "The Competitive Challenger"
        elif rank == 1:
            label = "The Vulnerable Leader"
        else:
            label = "The Squeezed Middle"

        self._d.central_diagnosis_label = label

        # Build explanation paragraph
        target_name = operator_display_name(self.result.target_operator)
        market_name = safe_get(self.config, "market_name",
                               self.result.market.replace("_", " ").title() if self.result.market else "the market")

        # Collect dimension analysis
        dimensions = self._build_dimension_analysis()

        explanation_parts = [
            f"The single most important finding across all Five Looks is {target_name}'s "
            f'"{label}" positioning.',
        ]
        if dimensions:
            explanation_parts.append(
                "This is not a temporary market condition — it is a structural "
                "competitive problem that manifests in every dimension:"
            )

        # Add escape routes from SWOT SO strategies
        so_strategies = safe_list(self.result.swot, "so_strategies") if self.result.swot else []
        if so_strategies:
            routes = so_strategies[:3]
            explanation_parts.append(
                "\n**The escape routes** (not mutually exclusive):\n"
                + "\n".join(f"{i}. {r}" for i, r in enumerate(routes, 1))
            )

        self._d.central_diagnosis = "\n\n".join(explanation_parts)

    def _count_appeals_wins(self) -> int:
        """Count how many $APPEALS dimensions our score > leader's score."""
        mci = self.result.market_customer
        if mci is None:
            return 0
        appeals = safe_list(mci, "appeals_assessment")
        wins = 0
        for a in appeals:
            our = _to_float(safe_get(a, "our_score", 0))
            comp_scores = safe_dict(a, "competitor_scores")
            if comp_scores:
                max_comp = max((_to_float(v) for v in comp_scores.values()), default=0)
                if our > max_comp:
                    wins += 1
        return wins

    def _compute_revenue_gap_pp(self) -> float:
        """Compute gap in revenue share between target and leader in pp."""
        ct = safe_dict(self.result.competition, "comparison_table") if self.result.competition else {}
        share_data = ct.get("revenue_share") or ct.get("market_share") or {}

        if not share_data:
            # Derive from revenue
            rev_data = ct.get("revenue") or ct.get("quarterly_revenue") or self._extract_revenue_map()
            if not rev_data:
                return 20.0  # Default moderate gap
            total = sum(_to_float(v) for v in rev_data.values())
            if total == 0:
                return 20.0
            share_data = {k: (_to_float(v) / total * 100) for k, v in rev_data.items()}

        target = self.result.target_operator
        target_share = 0.0
        leader_share = 0.0
        for op, share in share_data.items():
            s = _to_float(share)
            if op == target or _name_match(op, target):
                target_share = s
            if s > leader_share:
                leader_share = s

        return leader_share - target_share

    def _is_declining(self) -> bool:
        """Check if target operator is in a declining trajectory."""
        fh = safe_dict(self.result.self_analysis, "financial_health") if self.result.self_analysis else {}
        growth = fh.get("revenue_growth_yoy") or fh.get("revenue_growth") or fh.get("yoy_growth")
        if growth is not None:
            return _to_float(growth) < -1.0
        health = safe_get(self.result.self_analysis, "health_rating", "stable")
        return health in ("concerning", "critical")

    def _weakness_count(self) -> int:
        if self.result.self_analysis is None:
            return 0
        return len(safe_list(self.result.self_analysis, "weaknesses"))

    def _build_dimension_analysis(self) -> list[dict]:
        """Build a dimension comparison table for the central diagnosis."""
        # This is used for rendering; returns list of dicts
        ct = safe_dict(self.result.competition, "comparison_table") if self.result.competition else {}
        if not ct:
            return []
        dimensions = []
        for metric, values in ct.items():
            if isinstance(values, dict) and len(values) >= 2:
                dimensions.append({"dimension": metric, **values})
        return dimensions

    # ------------------------------------------------------------------
    # Per-module net assessments
    # ------------------------------------------------------------------

    def _compute_net_assessments(self):
        # Trends
        trends = self.result.trends
        if trends:
            pest = safe_get(trends, "pest")
            opps = len(safe_list(pest, "policy_opportunities")) if pest else 0
            threats = len(safe_list(pest, "policy_threats")) if pest else 0
            weather = safe_get(pest, "overall_weather", "mixed") if pest else "mixed"
            lifecycle = safe_get(trends, "industry_lifecycle_stage", "mature")
            self._d.trends_net_assessment = (
                f"{'Favorable' if weather in ('sunny', 'mixed') else 'Challenging'} "
                f"macro environment in a {lifecycle} market"
            )
            if safe_get(trends, "key_message"):
                self._d.trends_net_assessment = safe_get(trends, "key_message")
        else:
            self._d.trends_net_assessment = "Insufficient trend data"

        # Market/Customer
        mci = self.result.market_customer
        if mci:
            self._d.market_net_assessment = safe_get(mci, "key_message", "Market analysis available")
        else:
            self._d.market_net_assessment = "Insufficient market data"

        # Competition
        comp = self.result.competition
        if comp:
            self._d.competition_net_assessment = safe_get(comp, "key_message", "Competition analysis available")
        else:
            self._d.competition_net_assessment = "Insufficient competition data"

        # Self
        sa = self.result.self_analysis
        if sa:
            self._d.self_net_assessment = safe_get(sa, "key_message", "Self analysis available")
        else:
            self._d.self_net_assessment = "Insufficient self-analysis data"

        # Tariff
        tariff = self.result.tariff_analysis
        if tariff:
            self._d.tariff_net_assessment = (
                tariff.get("key_message") or tariff.get("summary") or "Tariff analysis available"
            )
        else:
            self._d.tariff_net_assessment = "No tariff data available"

        # SWOT
        swot = self.result.swot
        if swot:
            self._d.swot_net_assessment = safe_get(swot, "key_message",
                                                    f"{self._d.competitive_stance}")
        else:
            self._d.swot_net_assessment = "Insufficient SWOT data"

        # Opportunities
        opp = self.result.opportunities
        if opp:
            gi = len(safe_list(opp, "grow_invest"))
            total = len(safe_list(opp, "span_positions")) or (gi + len(safe_list(opp, "acquire_skills")) + len(safe_list(opp, "harvest")) + len(safe_list(opp, "avoid_exit")))
            pct = (gi / total * 100) if total > 0 else 0
            self._d.opportunities_net_assessment = (
                safe_get(opp, "key_message") or
                f"{gi} of {total} opportunities ({pct:.0f}%) in Grow/Invest quadrant"
            )
        else:
            self._d.opportunities_net_assessment = "Insufficient opportunity data"

    # ------------------------------------------------------------------
    # Strategic priorities (from opportunities P0/P1)
    # ------------------------------------------------------------------

    def _compute_priorities(self):
        opp = self.result.opportunities
        if opp is None:
            return

        items = safe_list(opp, "opportunities")
        if not items:
            return

        # Sort: P0 first, then P1, then by name
        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        sorted_items = sorted(items, key=lambda x: (
            priority_order.get(safe_get(x, "priority", "P2"), 2),
            safe_get(x, "name", "")
        ))

        fh = safe_dict(self.result.self_analysis, "financial_health") if self.result.self_analysis else {}

        priorities = []
        for item in sorted_items[:5]:
            name = safe_get(item, "name", "Unknown")
            desc = safe_get(item, "description", "")
            cap = safe_get(item, "our_capability", "")
            market = safe_get(item, "addressable_market", "N/A")
            window = safe_get(item, "time_window", "")
            priority_level = safe_get(item, "priority", "P1")

            priorities.append({
                "name": name,
                "description": desc,
                "metric": market,
                "current": cap,
                "target": "",
                "how": desc,
                "priority": priority_level,
                "time_window": window,
            })

        self._d.priorities = priorities

    # ------------------------------------------------------------------
    # Strategic traps
    # ------------------------------------------------------------------

    def _compute_strategic_traps(self):
        traps = []
        label = self._d.central_diagnosis_label

        # Derive traps based on diagnosis label
        if "Squeezed" in label or "Distant" in label:
            traps.append({
                "trap": "Enter a price war",
                "temptation": "Value competitors are winning on price",
                "reality": "Margin destruction without winning price-sensitive customers back"
            })
            traps.append({
                "trap": "Attempt premium repositioning",
                "temptation": "Leader's margins are enviable",
                "reality": "Trails leader on every dimension; would take years and heavy investment"
            })

        if "Declining" in label:
            traps.append({
                "trap": "Cut investment to protect margins",
                "temptation": "Short-term earnings pressure",
                "reality": "Accelerates decline; network/product gap widens"
            })

        # Always include: don't delay core transformation
        sa = self.result.self_analysis
        if sa:
            weaknesses = safe_list(sa, "weaknesses")
            if weaknesses:
                traps.append({
                    "trap": "Delay core transformation",
                    "temptation": "Current performance is adequate",
                    "reality": f"Key weakness: {weaknesses[0][:80]}; delay compounds disadvantage"
                })

        # Add trap about investing in declining areas
        segments = safe_list(sa, "segment_analyses") if sa else []
        for seg in segments:
            if safe_get(seg, "health_status") == "critical":
                traps.append({
                    "trap": f"Over-invest in declining {safe_get(seg, 'segment_name', 'segment')}",
                    "temptation": "Legacy revenue is significant",
                    "reality": "Structural decline; defend but don't double down"
                })
                break

        self._d.strategic_traps = traps[:4]  # Max 4

    # ------------------------------------------------------------------
    # Risk/reward scenarios
    # ------------------------------------------------------------------

    def _compute_risk_reward(self):
        fh = safe_dict(self.result.self_analysis, "financial_health") if self.result.self_analysis else {}
        revenue = _to_float(fh.get("revenue") or fh.get("total_revenue") or fh.get("quarterly_revenue") or 0)

        priorities = self._d.priorities
        n_priorities = len(priorities)

        # Bull case: execute all priorities
        bull_uplift = revenue * 0.12 if revenue else 0  # ~12% uplift
        self._d.bull_case = {
            "scenario": f"Execute all {n_priorities} strategic priorities successfully",
            "revenue_impact": f"+10-16% over 5 years",
            "conditions": "Full execution of P0 opportunities, favorable market conditions"
        }

        # Bear case: no execution, continue negative trends
        self._d.bear_case = {
            "scenario": "No strategic execution; continue current trajectory",
            "revenue_impact": "-6-12% over 5 years",
            "conditions": "Structural decline in core segments, competitor gains"
        }

        # Base case
        self._d.base_case = {
            "scenario": f"Execute 2-3 of {n_priorities} priorities; moderate improvement",
            "revenue_impact": "+3-6% over 5 years",
            "conditions": "Partial execution with some wins and some misses"
        }

    # ------------------------------------------------------------------
    # KPI dashboard
    # ------------------------------------------------------------------

    def _compute_kpi_dashboard(self):
        fh = safe_dict(self.result.self_analysis, "financial_health") if self.result.self_analysis else {}

        dashboard = []

        # Revenue growth
        rev_growth = fh.get("revenue_growth_yoy") or fh.get("revenue_growth") or fh.get("yoy_growth")
        if rev_growth is not None:
            current = fmt_pct(_to_float(rev_growth), show_sign=True)
            dashboard.append({
                "kpi": "Revenue growth",
                "current": current,
                "q2_target": "+1.0%",
                "q4_target": "+1.5%",
                "fy_target": "+2.5%"
            })

        # EBITDA margin
        margin = fh.get("ebitda_margin") or fh.get("margin")
        if margin is not None:
            dashboard.append({
                "kpi": "EBITDA margin",
                "current": fmt_pct(_to_float(margin), show_sign=False),
                "q2_target": fmt_pct(_to_float(margin) + 0.3, show_sign=False),
                "q4_target": fmt_pct(_to_float(margin) + 0.8, show_sign=False),
                "fy_target": fmt_pct(_to_float(margin) + 1.8, show_sign=False),
            })

        # Churn
        churn = fh.get("churn") or fh.get("monthly_churn")
        if churn is not None:
            c = _to_float(churn)
            dashboard.append({
                "kpi": "Monthly churn",
                "current": fmt_pct(c, show_sign=False),
                "q2_target": fmt_pct(c - 0.05, show_sign=False),
                "q4_target": fmt_pct(c - 0.10, show_sign=False),
                "fy_target": fmt_pct(c - 0.23, show_sign=False),
            })

        # Add generic targets from segment health
        segments = safe_list(self.result.self_analysis, "segment_analyses") if self.result.self_analysis else []
        for seg in segments[:3]:
            name = safe_get(seg, "segment_name", "Segment")
            health = safe_get(seg, "health_status", "stable")
            km = safe_get(seg, "key_metrics", {})
            rev = km.get("revenue") or km.get("quarterly_revenue")
            if rev is not None:
                dashboard.append({
                    "kpi": f"{name} revenue",
                    "current": str(rev),
                    "q2_target": "—",
                    "q4_target": "—",
                    "fy_target": "Growth" if health != "critical" else "Stabilize",
                })

        self._d.kpi_dashboard = dashboard

    # ------------------------------------------------------------------
    # One-line verdict
    # ------------------------------------------------------------------

    def _compute_one_line_verdict(self):
        target_name = operator_display_name(self.result.target_operator)
        rank = self._d.operator_rank
        ordinal = {1: "#1", 2: "#2", 3: "#3", 4: "#4"}.get(rank, f"#{rank}")
        health = safe_get(self.result.self_analysis, "health_rating", "stable")
        health_adj = {
            "healthy": "financially stable",
            "stable": "operationally stable",
            "concerning": "financially pressured",
            "critical": "financially distressed",
        }.get(health, "stable")

        label = self._d.central_diagnosis_label
        # Central challenge phrase
        challenge_map = {
            "The Squeezed Middle": 'trapped in a "squeezed middle"',
            "The Distant Second": "facing a significant gap to the market leader",
            "The Distant Third": "lagging significantly behind the top two operators",
            "The Competitive Challenger": "with a realistic shot at closing the gap",
            "The Dominant Leader": "defending a dominant market position",
            "The Declining Incumbent": "in a declining competitive position",
            "The Vulnerable Leader": "holding a market lead under increasing pressure",
        }
        challenge = challenge_map.get(label, f'in a "{label}" position')

        # Top priority
        top_priority = "execute its transformation agenda"
        if self._d.priorities:
            top_priority = self._d.priorities[0].get("name", top_priority).lower()

        # Time window from opportunities
        window = "3-5 year"
        opp = self.result.opportunities
        if opp:
            windows = [safe_get(item, "time_window", "") for item in safe_list(opp, "opportunities")]
            if any("immediate" in w.lower() for w in windows if w):
                window = "12-18 month"
            elif any("1-2" in w for w in windows if w):
                window = "2-3 year"

        self._d.one_line_verdict = (
            f"{target_name} is a {health_adj} {ordinal} operator {challenge} "
            f"with a {window} window to {top_priority}."
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _to_float(val) -> float:
    """Safely convert a value to float."""
    if val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    try:
        # Handle strings like "3,092M", "€3,092M", "+8.5%"
        s = str(val).strip()
        s = s.replace(",", "").replace("%", "")
        s = s.replace("€", "").replace("$", "").replace("£", "")
        s = s.rstrip("MBTKk")
        return float(s)
    except (ValueError, TypeError):
        return 0.0


def _name_match(a: str, b: str) -> bool:
    """Fuzzy match operator names."""
    if not a or not b:
        return False
    a_lower = a.lower().replace("_", " ").replace("-", " ")
    b_lower = b.lower().replace("_", " ").replace("-", " ")
    return a_lower == b_lower or a_lower in b_lower or b_lower in a_lower
