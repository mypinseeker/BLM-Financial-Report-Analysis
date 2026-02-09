"""Look 5: Opportunities -- SPAN Matrix analysis.

Extracts opportunity items from the four preceding analyses plus the SWOT
synthesis, scores each on a two-dimensional SPAN matrix
(Market Attractiveness x Competitive Position), assigns quadrants, and
ranks by priority.

SPAN quadrants:
    grow_invest     -- high attractiveness, strong position -> invest heavily
    acquire_skills  -- high attractiveness, weak position   -> build capability first
    harvest         -- low attractiveness, strong position  -> extract cash
    avoid_exit      -- low attractiveness, weak position    -> retreat / divest

Addressable market is set to "N/A" whenever no reliable data exists (per
design principle: never fabricate numbers).
"""

from __future__ import annotations

from typing import Optional

from src.models.opportunity import (
    SPANPosition,
    OpportunityItem,
    OpportunityInsight,
)
from src.models.trend import TrendAnalysis
from src.models.market import MarketCustomerInsight
from src.models.competition import CompetitionInsight
from src.models.self_analysis import SelfInsight
from src.models.swot import SWOTAnalysis
from src.models.provenance import ProvenanceStore


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Weights for market attractiveness (Y-axis)
_MA_WEIGHT_MARKET_SIZE = 0.30
_MA_WEIGHT_MARKET_GROWTH = 0.25
_MA_WEIGHT_PROFIT_POTENTIAL = 0.25
_MA_WEIGHT_STRATEGIC_VALUE = 0.20

# Weights for competitive position (X-axis)
_CP_WEIGHT_MARKET_SHARE = 0.25
_CP_WEIGHT_PRODUCT_FIT = 0.25
_CP_WEIGHT_BRAND_CHANNEL = 0.25
_CP_WEIGHT_TECH_CAPABILITY = 0.25

# Threshold for quadrant assignment (on a 1-10 scale)
_QUADRANT_THRESHOLD = 5.0


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _compute_market_attractiveness(
    market_size_score: float,
    market_growth_score: float,
    profit_potential_score: float,
    strategic_value_score: float,
) -> float:
    """Weighted average for market attractiveness (1-10 scale)."""
    return (
        _MA_WEIGHT_MARKET_SIZE * market_size_score
        + _MA_WEIGHT_MARKET_GROWTH * market_growth_score
        + _MA_WEIGHT_PROFIT_POTENTIAL * profit_potential_score
        + _MA_WEIGHT_STRATEGIC_VALUE * strategic_value_score
    )


def _compute_competitive_position(
    market_share_score: float,
    product_fit_score: float,
    brand_channel_score: float,
    tech_capability_score: float,
) -> float:
    """Weighted average for competitive position (1-10 scale)."""
    return (
        _CP_WEIGHT_MARKET_SHARE * market_share_score
        + _CP_WEIGHT_PRODUCT_FIT * product_fit_score
        + _CP_WEIGHT_BRAND_CHANNEL * brand_channel_score
        + _CP_WEIGHT_TECH_CAPABILITY * tech_capability_score
    )


def _assign_quadrant(market_attractiveness: float, competitive_position: float) -> str:
    """Map SPAN scores to a quadrant label."""
    if market_attractiveness >= _QUADRANT_THRESHOLD:
        if competitive_position >= _QUADRANT_THRESHOLD:
            return "grow_invest"
        return "acquire_skills"
    else:
        if competitive_position >= _QUADRANT_THRESHOLD:
            return "harvest"
        return "avoid_exit"


def _quadrant_strategy(quadrant: str) -> str:
    """Return a default recommended strategy string for a quadrant."""
    return {
        "grow_invest": "Invest aggressively to grow market share and revenue.",
        "acquire_skills": "Build missing capabilities before committing major resources.",
        "harvest": "Maximize short-term returns while maintaining competitive advantages.",
        "avoid_exit": "Consider exit or minimal maintenance investment.",
    }.get(quadrant, "Evaluate further before committing resources.")


def _priority_from_quadrant(quadrant: str) -> str:
    """Assign a default priority based on quadrant."""
    return {
        "grow_invest": "P0",
        "acquire_skills": "P1",
        "harvest": "P1",
        "avoid_exit": "P2",
    }.get(quadrant, "P2")


def _clamp(value: float, low: float = 1.0, high: float = 10.0) -> float:
    """Clamp a numeric value between low and high."""
    return max(low, min(high, value))


# ---------------------------------------------------------------------------
# Opportunity extraction
# ---------------------------------------------------------------------------

def _extract_raw_opportunities(
    trends: TrendAnalysis,
    market_customer: MarketCustomerInsight,
    competition: CompetitionInsight,
    self_analysis: SelfInsight,
    swot: SWOTAnalysis,
) -> list[dict]:
    """Gather raw opportunity candidates from every available source.

    Each entry is a dict with keys: name, description, derived_from, source_scores.
    ``source_scores`` carries heuristic sub-dimension scores used later.
    """
    raw: list[dict] = []
    seen_names: set[str] = set()

    def _add(name: str, description: str, derived_from: list[str],
             source_scores: Optional[dict] = None) -> None:
        if name in seen_names:
            return
        seen_names.add(name)
        raw.append({
            "name": name,
            "description": description,
            "derived_from": derived_from,
            "source_scores": source_scores or {},
        })

    # 1. SO strategies (high priority because they combine strength + opportunity)
    if swot and swot.so_strategies:
        for idx, strat in enumerate(swot.so_strategies):
            _add(
                name=f"SO-{idx + 1}",
                description=strat,
                derived_from=["swot_so_strategy"],
                source_scores={
                    "strategic_value_score": 8,
                    "product_fit_score": 7,
                },
            )

    # 2. Market changes classified as opportunities
    if market_customer and market_customer.opportunities:
        for mc in market_customer.opportunities:
            _add(
                name=mc.description[:60] if mc.description else f"Market-{mc.change_type}",
                description=mc.description,
                derived_from=["market_opportunity", mc.change_type],
                source_scores={
                    "market_growth_score": 7 if mc.severity == "high" else 5,
                },
            )

    # 3. Technology trends from PEST
    if trends and trends.technology_revolution:
        for tech in trends.technology_revolution:
            _add(
                name=tech[:60],
                description=f"Technology trend: {tech}",
                derived_from=["trend_technology"],
                source_scores={
                    "market_growth_score": 6,
                    "tech_capability_score": 6,
                },
            )

    # 4. Policy opportunities from PEST
    if trends and trends.pest and trends.pest.policy_opportunities:
        for po in trends.pest.policy_opportunities:
            _add(
                name=po[:60],
                description=f"Policy opportunity: {po}",
                derived_from=["trend_policy_opportunity"],
                source_scores={
                    "strategic_value_score": 7,
                },
            )

    # 5. Competitor weaknesses paired with our strengths
    if competition and competition.competitor_analyses:
        for op_id, deep_dive in competition.competitor_analyses.items():
            if deep_dive.weaknesses:
                for cw in deep_dive.weaknesses[:2]:
                    _add(
                        name=f"Exploit {op_id} weakness: {cw[:40]}",
                        description=f"Competitor {op_id} is weak in: {cw}",
                        derived_from=["competitor_weakness", op_id],
                        source_scores={
                            "market_share_score": 6,
                            "brand_channel_score": 6,
                        },
                    )

    # 6. WO strategies (improvement opportunities)
    if swot and swot.wo_strategies:
        for idx, strat in enumerate(swot.wo_strategies):
            _add(
                name=f"WO-{idx + 1}",
                description=strat,
                derived_from=["swot_wo_strategy"],
                source_scores={
                    "strategic_value_score": 6,
                    "product_fit_score": 4,
                },
            )

    return raw


def _score_opportunity(
    raw: dict,
    self_analysis: SelfInsight,
    competition: CompetitionInsight,
) -> SPANPosition:
    """Score a raw opportunity on both SPAN dimensions and assign quadrant.

    When hard data is unavailable the function uses heuristic defaults (5/10)
    supplemented by any ``source_scores`` hints extracted earlier.
    """
    scores = raw.get("source_scores", {})

    # Market attractiveness sub-scores
    market_size_score = _clamp(scores.get("market_size_score", 5.0))
    market_growth_score = _clamp(scores.get("market_growth_score", 5.0))
    profit_potential_score = _clamp(scores.get("profit_potential_score", 5.0))
    strategic_value_score = _clamp(scores.get("strategic_value_score", 5.0))

    market_attractiveness = _compute_market_attractiveness(
        market_size_score, market_growth_score,
        profit_potential_score, strategic_value_score,
    )

    # Competitive position sub-scores
    market_share_score = _clamp(scores.get("market_share_score", 5.0))
    product_fit_score = _clamp(scores.get("product_fit_score", 5.0))
    brand_channel_score = _clamp(scores.get("brand_channel_score", 5.0))
    tech_capability_score = _clamp(scores.get("tech_capability_score", 5.0))

    competitive_position = _compute_competitive_position(
        market_share_score, product_fit_score,
        brand_channel_score, tech_capability_score,
    )

    quadrant = _assign_quadrant(market_attractiveness, competitive_position)
    recommended_strategy = _quadrant_strategy(quadrant)

    return SPANPosition(
        opportunity_name=raw["name"],
        market_size_score=market_size_score,
        market_growth_score=market_growth_score,
        profit_potential_score=profit_potential_score,
        strategic_value_score=strategic_value_score,
        market_attractiveness=round(market_attractiveness, 2),
        market_share_score=market_share_score,
        product_fit_score=product_fit_score,
        brand_channel_score=brand_channel_score,
        tech_capability_score=tech_capability_score,
        competitive_position=round(competitive_position, 2),
        quadrant=quadrant,
        recommended_strategy=recommended_strategy,
        bubble_size=1.0,  # Default; overridden if addressable market data exists
    )


def _build_opportunity_items(
    span_positions: list[SPANPosition],
    raw_list: list[dict],
) -> list[OpportunityItem]:
    """Build structured OpportunityItem instances from SPAN-scored positions."""
    items: list[OpportunityItem] = []
    raw_by_name = {r["name"]: r for r in raw_list}

    for sp in span_positions:
        raw = raw_by_name.get(sp.opportunity_name, {})
        priority = _priority_from_quadrant(sp.quadrant)
        items.append(
            OpportunityItem(
                name=sp.opportunity_name,
                description=raw.get("description", ""),
                derived_from=raw.get("derived_from", []),
                addressable_market="N/A",  # Never fabricate
                addressable_market_source="",
                our_capability="",
                competition_intensity="",
                time_window="",
                priority=priority,
                priority_rationale=f"Quadrant: {sp.quadrant}",
            )
        )
    return items


def _group_by_quadrant(
    span_positions: list[SPANPosition],
) -> dict[str, list[str]]:
    """Group opportunity names by SPAN quadrant."""
    groups: dict[str, list[str]] = {
        "grow_invest": [],
        "acquire_skills": [],
        "harvest": [],
        "avoid_exit": [],
    }
    for sp in span_positions:
        if sp.quadrant in groups:
            groups[sp.quadrant].append(sp.opportunity_name)
    return groups


def _build_key_message(
    span_positions: list[SPANPosition],
    groups: dict[str, list[str]],
) -> str:
    """Construct a summary key message for the opportunity analysis."""
    total = len(span_positions)
    if total == 0:
        return "No actionable opportunities identified from the available data."

    gi = len(groups.get("grow_invest", []))
    aq = len(groups.get("acquire_skills", []))
    hv = len(groups.get("harvest", []))
    ae = len(groups.get("avoid_exit", []))

    return (
        f"SPAN matrix positions {total} opportunities: "
        f"{gi} grow/invest, {aq} acquire skills, {hv} harvest, {ae} avoid/exit. "
        f"Focus resources on the {gi} grow/invest items for maximum strategic impact."
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_opportunities(
    trends: TrendAnalysis,
    market_customer: MarketCustomerInsight,
    competition: CompetitionInsight,
    self_analysis: SelfInsight,
    swot: SWOTAnalysis,
    db=None,
    target_operator: str = "",
    provenance: Optional[ProvenanceStore] = None,
) -> OpportunityInsight:
    """Analyze opportunities using the SPAN matrix framework.

    Parameters
    ----------
    trends : TrendAnalysis
        Output of Look 1.
    market_customer : MarketCustomerInsight
        Output of Look 2.
    competition : CompetitionInsight
        Output of Look 3.
    self_analysis : SelfInsight
        Output of Look 4.
    swot : SWOTAnalysis
        Output of the SWOT synthesis bridge.
    db : TelecomDatabase, optional
        Database handle for additional data lookups.
    target_operator : str
        Operator ID under analysis.
    provenance : ProvenanceStore, optional
        Shared provenance store.

    Returns
    -------
    OpportunityInsight
        Scored and classified opportunity items with SPAN positions.
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
    if swot is None:
        swot = SWOTAnalysis()

    # --- Step 1: Extract raw opportunity candidates ---
    raw_list = _extract_raw_opportunities(
        trends, market_customer, competition, self_analysis, swot,
    )

    # --- Step 2: Score each on SPAN matrix ---
    span_positions: list[SPANPosition] = []
    for raw in raw_list:
        sp = _score_opportunity(raw, self_analysis, competition)
        span_positions.append(sp)

    # --- Step 3: Group by quadrant ---
    groups = _group_by_quadrant(span_positions)

    # --- Step 4: Build detailed opportunity items ---
    opportunity_items = _build_opportunity_items(span_positions, raw_list)

    # --- Step 5: Build key message ---
    key_message = _build_key_message(span_positions, groups)

    # --- Step 6: Track in provenance ---
    if provenance is not None:
        provenance.track(
            value=len(span_positions),
            field_name="opportunity_count",
            operator=target_operator,
        )

    return OpportunityInsight(
        span_positions=span_positions,
        grow_invest=groups["grow_invest"],
        acquire_skills=groups["acquire_skills"],
        harvest=groups["harvest"],
        avoid_exit=groups["avoid_exit"],
        window_opportunities=[],  # Populated when time window data is available
        opportunities=opportunity_items,
        key_message=key_message,
    )
