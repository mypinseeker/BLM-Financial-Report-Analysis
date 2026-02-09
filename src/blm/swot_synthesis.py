"""SWOT Synthesis -- Bridge between Look 4 (Self) and Look 5 (Opportunities).

Aggregates findings from the first four looks into a SWOT matrix and derives
four strategy quadrants (SO / WO / ST / WT).

Source mapping:
    S (Strengths)      <- self_analysis.strengths
    W (Weaknesses)     <- self_analysis.weaknesses + exposure_points descriptions
    O (Opportunities)  <- trends.pest.policy_opportunities + market_customer.opportunities
    T (Threats)        <- trends.pest.policy_threats + market_customer.threats
                          + high-pressure forces from competition.five_forces
"""

from __future__ import annotations

from typing import Optional

from src.models.swot import SWOTAnalysis
from src.models.trend import TrendAnalysis
from src.models.market import MarketCustomerInsight
from src.models.competition import CompetitionInsight
from src.models.self_analysis import SelfInsight
from src.models.provenance import ProvenanceStore


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _extract_strengths(self_analysis: SelfInsight) -> list[str]:
    """Pull strengths directly from the self analysis."""
    return list(self_analysis.strengths) if self_analysis.strengths else []


def _extract_weaknesses(self_analysis: SelfInsight) -> list[str]:
    """Pull weaknesses from the self analysis plus exposure point descriptions."""
    items: list[str] = []
    if self_analysis.weaknesses:
        items.extend(self_analysis.weaknesses)
    if self_analysis.exposure_points:
        for ep in self_analysis.exposure_points:
            description = ep.side_effect or ep.trigger_action
            if description and description not in items:
                items.append(description)
    return items


def _extract_opportunities(
    trends: TrendAnalysis,
    market_customer: MarketCustomerInsight,
) -> list[str]:
    """Aggregate opportunities from trend policy_opportunities and market opportunities."""
    items: list[str] = []
    if trends and trends.pest and trends.pest.policy_opportunities:
        items.extend(trends.pest.policy_opportunities)
    if market_customer and market_customer.opportunities:
        for mc in market_customer.opportunities:
            desc = mc.description
            if desc and desc not in items:
                items.append(desc)
    return items


def _extract_threats(
    trends: TrendAnalysis,
    market_customer: MarketCustomerInsight,
    competition: CompetitionInsight,
) -> list[str]:
    """Aggregate threats from trends, market, and high-pressure competitive forces."""
    items: list[str] = []
    if trends and trends.pest and trends.pest.policy_threats:
        items.extend(trends.pest.policy_threats)
    if market_customer and market_customer.threats:
        for mc in market_customer.threats:
            desc = mc.description
            if desc and desc not in items:
                items.append(desc)
    if competition and competition.five_forces:
        for force_name, force in competition.five_forces.items():
            if getattr(force, "force_level", "low") == "high":
                label = f"High {force_name.replace('_', ' ')} pressure"
                if label not in items:
                    items.append(label)
    return items


def _generate_so_strategies(strengths: list[str], opportunities: list[str]) -> list[str]:
    """Generate SO strategies (offensive): leverage strengths to capture opportunities.

    Produces 2-4 actionable one-sentence strategies by pairing strength
    categories with opportunity categories.
    """
    if not strengths or not opportunities:
        return []
    strategies: list[str] = []
    n_pairs = min(4, max(2, min(len(strengths), len(opportunities))))
    for i in range(n_pairs):
        s = strengths[i % len(strengths)]
        o = opportunities[i % len(opportunities)]
        strategies.append(
            f"Leverage '{s}' to capture the opportunity of '{o}'."
        )
    return strategies


def _generate_wo_strategies(weaknesses: list[str], opportunities: list[str]) -> list[str]:
    """Generate WO strategies (improvement): fix weaknesses to unlock opportunities.

    Produces 2-4 actionable one-sentence strategies.
    """
    if not weaknesses or not opportunities:
        return []
    strategies: list[str] = []
    n_pairs = min(4, max(2, min(len(weaknesses), len(opportunities))))
    for i in range(n_pairs):
        w = weaknesses[i % len(weaknesses)]
        o = opportunities[i % len(opportunities)]
        strategies.append(
            f"Address weakness '{w}' to unlock the opportunity of '{o}'."
        )
    return strategies


def _generate_st_strategies(strengths: list[str], threats: list[str]) -> list[str]:
    """Generate ST strategies (defensive): use strengths to counter threats.

    Produces 2-4 actionable one-sentence strategies.
    """
    if not strengths or not threats:
        return []
    strategies: list[str] = []
    n_pairs = min(4, max(2, min(len(strengths), len(threats))))
    for i in range(n_pairs):
        s = strengths[i % len(strengths)]
        t = threats[i % len(threats)]
        strategies.append(
            f"Use strength '{s}' to counter the threat of '{t}'."
        )
    return strategies


def _generate_wt_strategies(weaknesses: list[str], threats: list[str]) -> list[str]:
    """Generate WT strategies (retreat/defend): minimize weaknesses and avoid threats.

    Produces 2-4 actionable one-sentence strategies.
    """
    if not weaknesses or not threats:
        return []
    strategies: list[str] = []
    n_pairs = min(4, max(2, min(len(weaknesses), len(threats))))
    for i in range(n_pairs):
        w = weaknesses[i % len(weaknesses)]
        t = threats[i % len(threats)]
        strategies.append(
            f"Mitigate weakness '{w}' and defend against the threat of '{t}'."
        )
    return strategies


def _build_key_message(
    strengths: list[str],
    weaknesses: list[str],
    opportunities: list[str],
    threats: list[str],
) -> str:
    """Construct a summary key message for the SWOT analysis."""
    n_s = len(strengths)
    n_w = len(weaknesses)
    n_o = len(opportunities)
    n_t = len(threats)

    if n_s == 0 and n_w == 0 and n_o == 0 and n_t == 0:
        return "Insufficient data to produce a SWOT assessment."

    # Determine dominant posture
    internal_balance = n_s - n_w
    external_balance = n_o - n_t

    if internal_balance > 0 and external_balance > 0:
        posture = "offensive (SO-dominant)"
    elif internal_balance > 0 and external_balance <= 0:
        posture = "defensive (ST-dominant)"
    elif internal_balance <= 0 and external_balance > 0:
        posture = "improvement-focused (WO-dominant)"
    else:
        posture = "cautious (WT-dominant)"

    return (
        f"SWOT analysis identifies {n_s} strengths, {n_w} weaknesses, "
        f"{n_o} opportunities, and {n_t} threats. "
        f"The recommended strategic posture is {posture}."
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def synthesize_swot(
    trends: TrendAnalysis,
    market_customer: MarketCustomerInsight,
    competition: CompetitionInsight,
    self_analysis: SelfInsight,
    provenance: Optional[ProvenanceStore] = None,
) -> SWOTAnalysis:
    """Synthesize SWOT analysis from the first four looks.

    Parameters
    ----------
    trends : TrendAnalysis
        Output of Look 1 (Trends / PEST).
    market_customer : MarketCustomerInsight
        Output of Look 2 (Market / Customer).
    competition : CompetitionInsight
        Output of Look 3 (Competition / Porter's Five Forces).
    self_analysis : SelfInsight
        Output of Look 4 (Self / BMC + Capability Assessment).
    provenance : ProvenanceStore, optional
        Shared provenance store for data tracking.

    Returns
    -------
    SWOTAnalysis
        Populated SWOT matrix with four strategy quadrants and a key message.
    """
    # Handle None inputs gracefully
    if trends is None:
        trends = TrendAnalysis()
    if market_customer is None:
        market_customer = MarketCustomerInsight()
    if competition is None:
        competition = CompetitionInsight()
    if self_analysis is None:
        self_analysis = SelfInsight()

    # --- Step 1: Extract SWOT items ---
    strengths = _extract_strengths(self_analysis)
    weaknesses = _extract_weaknesses(self_analysis)
    opportunities = _extract_opportunities(trends, market_customer)
    threats = _extract_threats(trends, market_customer, competition)

    # --- Step 2: Generate four-quadrant strategies ---
    so_strategies = _generate_so_strategies(strengths, opportunities)
    wo_strategies = _generate_wo_strategies(weaknesses, opportunities)
    st_strategies = _generate_st_strategies(strengths, threats)
    wt_strategies = _generate_wt_strategies(weaknesses, threats)

    # --- Step 3: Build key message ---
    key_message = _build_key_message(strengths, weaknesses, opportunities, threats)

    # --- Step 4: Optionally track in provenance ---
    if provenance is not None:
        provenance.track(
            value=len(strengths) + len(weaknesses) + len(opportunities) + len(threats),
            field_name="swot_total_items",
        )

    return SWOTAnalysis(
        strengths=strengths,
        weaknesses=weaknesses,
        opportunities=opportunities,
        threats=threats,
        so_strategies=so_strategies,
        wo_strategies=wo_strategies,
        st_strategies=st_strategies,
        wt_strategies=wt_strategies,
        key_message=key_message,
    )
