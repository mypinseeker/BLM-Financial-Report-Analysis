"""Multi-Quarter Market Share Analyzer — pure-function library.

Computes market share history across operators, share movement metrics
(gain/loss velocity, rank changes), and HHI concentration trends.

Design constraints:
  - No numpy/scipy — stdlib `math` only
  - All functions handle empty, single-value, all-zeros, and None-filled arrays
  - Pure functions — no side effects, no DB access
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, asdict
from typing import Optional


# ============================================================================
# Data models
# ============================================================================

@dataclass
class OperatorShareSeries:
    """Share time-series for a single operator."""
    operator_id: str = ""
    display_name: str = ""
    share_pct: list[float] = field(default_factory=list)
    quarters: list[str] = field(default_factory=list)
    latest_share_pct: Optional[float] = None
    share_change_pp: Optional[float] = None
    avg_quarterly_change_pp: Optional[float] = None
    direction: str = "stable"
    rank_latest: Optional[int] = None
    rank_change: Optional[int] = None

    def to_dict(self) -> dict:
        d = asdict(self)
        for k, v in d.items():
            if isinstance(v, float):
                d[k] = round(v, 2)
            elif isinstance(v, list):
                d[k] = [round(x, 2) if isinstance(x, float) else x for x in v]
        return d


@dataclass
class MarketConcentration:
    """HHI and CR3 concentration metrics."""
    hhi: float = 0.0
    hhi_label: str = "competitive"
    cr3: float = 0.0
    hhi_trend: list[float] = field(default_factory=list)
    hhi_direction: str = "stable"

    def to_dict(self) -> dict:
        d = asdict(self)
        for k, v in d.items():
            if isinstance(v, float):
                d[k] = round(v, 2)
            elif isinstance(v, list):
                d[k] = [round(x, 2) if isinstance(x, float) else x for x in v]
        return d


@dataclass
class ShareAnalysis:
    """Complete share analysis for one metric across all operators."""
    metric_type: str = ""
    quarters: list[str] = field(default_factory=list)
    operator_series: list[OperatorShareSeries] = field(default_factory=list)
    concentration: MarketConcentration = field(default_factory=MarketConcentration)
    target_operator_id: str = ""
    target_series: Optional[OperatorShareSeries] = None
    share_leader_id: Optional[str] = None
    biggest_gainer_id: Optional[str] = None
    biggest_loser_id: Optional[str] = None
    key_message: str = ""

    def to_dict(self) -> dict:
        d = {
            "metric_type": self.metric_type,
            "quarters": self.quarters,
            "operator_series": [s.to_dict() for s in self.operator_series],
            "concentration": self.concentration.to_dict(),
            "target_operator_id": self.target_operator_id,
            "target_series": self.target_series.to_dict() if self.target_series else None,
            "share_leader_id": self.share_leader_id,
            "biggest_gainer_id": self.biggest_gainer_id,
            "biggest_loser_id": self.biggest_loser_id,
            "key_message": self.key_message,
        }
        return d


# ============================================================================
# Internal helpers
# ============================================================================

def _safe_float(val) -> Optional[float]:
    """Convert a value to float, returning None on failure."""
    if val is None:
        return None
    try:
        f = float(val)
        return f if math.isfinite(f) else None
    except (TypeError, ValueError):
        return None


def _classify_direction(change_pp: Optional[float]) -> str:
    """Classify share movement direction from pp change."""
    if change_pp is None:
        return "stable"
    if change_pp > 0.5:
        return "gaining"
    if change_pp < -0.5:
        return "losing"
    return "stable"


# ============================================================================
# Pure functions
# ============================================================================

def _extract_revenue_shares(
    market_ts: list[dict],
    quarters: list[str],
) -> dict[str, dict[str, Optional[float]]]:
    """Compute revenue share % per operator per quarter.

    Returns: {operator_id: {quarter: share_pct}} where share_pct is 0-100.
    """
    # Group rows by quarter
    by_quarter: dict[str, list[dict]] = {}
    for row in market_ts:
        cq = row.get("calendar_quarter", "")
        if cq in quarters:
            by_quarter.setdefault(cq, []).append(row)

    # All operators across all quarters
    all_ops: set[str] = set()
    for rows in by_quarter.values():
        for row in rows:
            op = row.get("operator_id", "")
            if op:
                all_ops.add(op)

    result: dict[str, dict[str, Optional[float]]] = {op: {} for op in all_ops}

    for cq in quarters:
        rows = by_quarter.get(cq, [])
        total = 0.0
        op_revs: dict[str, float] = {}
        for row in rows:
            op = row.get("operator_id", "")
            rev = _safe_float(row.get("total_revenue"))
            if op and rev is not None and rev > 0:
                op_revs[op] = rev
                total += rev

        for op in all_ops:
            if total > 0 and op in op_revs:
                result[op][cq] = (op_revs[op] / total) * 100.0
            else:
                result[op][cq] = None

    return result


def _extract_subscriber_shares(
    sub_data_by_op: dict[str, list[dict]],
    quarters: list[str],
    field_name: str,
) -> dict[str, dict[str, Optional[float]]]:
    """Compute subscriber share % per operator per quarter.

    Args:
        sub_data_by_op: {operator_id: [subscriber rows]}
        quarters: ordered list of CQ labels
        field_name: e.g. "mobile_total_k" or "broadband_total_k"

    Returns: {operator_id: {quarter: share_pct}}
    """
    all_ops = set(sub_data_by_op.keys())
    if not all_ops:
        return {}

    # Build per-op per-quarter value lookup
    op_q_val: dict[str, dict[str, float]] = {op: {} for op in all_ops}
    for op, rows in sub_data_by_op.items():
        for row in rows:
            cq = row.get("calendar_quarter", "")
            val = _safe_float(row.get(field_name))
            if cq and val is not None and val > 0:
                op_q_val[op][cq] = val

    result: dict[str, dict[str, Optional[float]]] = {op: {} for op in all_ops}

    for cq in quarters:
        total = sum(op_q_val[op].get(cq, 0) for op in all_ops)
        for op in all_ops:
            v = op_q_val[op].get(cq)
            if total > 0 and v is not None and v > 0:
                result[op][cq] = (v / total) * 100.0
            else:
                result[op][cq] = None

    return result


def _build_operator_series(
    op_id: str,
    display_name: str,
    shares_by_quarter: dict[str, Optional[float]],
    quarters: list[str],
    ranks_by_quarter: dict[str, int],
) -> OperatorShareSeries:
    """Build an OperatorShareSeries from per-quarter share data."""
    share_list = [shares_by_quarter.get(cq) for cq in quarters]
    valid = [(i, v) for i, v in enumerate(share_list) if v is not None]

    latest = valid[-1][1] if valid else None
    change_pp = None
    avg_change = None
    if len(valid) >= 2:
        change_pp = valid[-1][1] - valid[0][1]
        n_gaps = valid[-1][0] - valid[0][0]
        avg_change = change_pp / n_gaps if n_gaps > 0 else 0.0

    # Ranks
    rank_latest = ranks_by_quarter.get(quarters[-1]) if quarters else None
    rank_earliest = ranks_by_quarter.get(quarters[0]) if quarters else None
    rank_change = None
    if rank_latest is not None and rank_earliest is not None:
        # Positive means improved (rank went down numerically = better)
        rank_change = rank_earliest - rank_latest

    return OperatorShareSeries(
        operator_id=op_id,
        display_name=display_name,
        share_pct=[v if v is not None else 0.0 for v in share_list],
        quarters=list(quarters),
        latest_share_pct=round(latest, 2) if latest is not None else None,
        share_change_pp=round(change_pp, 2) if change_pp is not None else None,
        avg_quarterly_change_pp=round(avg_change, 2) if avg_change is not None else None,
        direction=_classify_direction(change_pp),
        rank_latest=rank_latest,
        rank_change=rank_change,
    )


def _compute_hhi(shares_by_quarter: dict[str, list[float]]) -> list[float]:
    """Compute HHI per quarter. shares_by_quarter: {quarter: [share_pct per op]}.

    HHI = sum(share_i^2), range 0-10000 for pct inputs.
    """
    result = []
    for cq, shares in shares_by_quarter.items():
        valid = [s for s in shares if s is not None and s > 0]
        if valid:
            hhi = sum(s * s for s in valid)
            result.append(round(hhi, 2))
        else:
            result.append(0.0)
    return result


def _classify_hhi(hhi: float) -> str:
    """Classify HHI into concentration label."""
    if hhi >= 2500:
        return "highly_concentrated"
    if hhi >= 1500:
        return "moderately_concentrated"
    return "competitive"


def _compute_ranks(
    shares_data: dict[str, dict[str, Optional[float]]],
    quarters: list[str],
) -> dict[str, dict[str, int]]:
    """Compute per-quarter rank for each operator.

    Returns: {operator_id: {quarter: rank}} where rank 1 = highest share.
    """
    result: dict[str, dict[str, int]] = {op: {} for op in shares_data}

    for cq in quarters:
        # Collect (op, share) pairs, treating None as 0
        items = []
        for op in shares_data:
            v = shares_data[op].get(cq)
            items.append((op, v if v is not None else 0.0))

        # Sort by share descending
        items.sort(key=lambda x: -x[1])

        for rank, (op, _) in enumerate(items, start=1):
            result[op][cq] = rank

    return result


def _identify_share_movements(
    series_list: list[OperatorShareSeries],
) -> tuple[Optional[str], Optional[str]]:
    """Identify the biggest gainer and biggest loser by share_change_pp.

    Returns: (biggest_gainer_id, biggest_loser_id).
    """
    if not series_list:
        return None, None

    valid = [(s.operator_id, s.share_change_pp) for s in series_list
             if s.share_change_pp is not None]

    if not valid:
        return None, None

    gainer = max(valid, key=lambda x: x[1])
    loser = min(valid, key=lambda x: x[1])

    gainer_id = gainer[0] if gainer[1] > 0.1 else None
    loser_id = loser[0] if loser[1] < -0.1 else None

    return gainer_id, loser_id


def _generate_key_message(
    target_series: Optional[OperatorShareSeries],
    concentration: MarketConcentration,
    metric_type: str,
) -> str:
    """Generate a 1-sentence key message for the share analysis."""
    metric_label = metric_type.replace("_", " ").title()

    if target_series is None:
        return f"{metric_label} share data unavailable for the target operator."

    direction = target_series.direction
    pp = target_series.share_change_pp
    latest = target_series.latest_share_pct
    rank = target_series.rank_latest

    parts = []
    if latest is not None:
        rank_str = f" (#{rank})" if rank else ""
        parts.append(f"{metric_label} share: {latest:.1f}%{rank_str}")

    if pp is not None:
        pp_str = f"{pp:+.1f}pp"
        parts.append(f"{direction} ({pp_str})")

    hhi_label = concentration.hhi_label.replace("_", " ")
    parts.append(f"market is {hhi_label} (HHI {concentration.hhi:,.0f})")

    if concentration.hhi_direction != "stable":
        parts.append(concentration.hhi_direction)

    return "; ".join(parts) + "."


# ============================================================================
# Orchestrator
# ============================================================================

def compute_share_analysis(
    market_ts: list[dict],
    sub_data_by_op: dict[str, list[dict]],
    quarters: list[str],
    target_operator_id: str,
    metric_type: str = "revenue",
    display_names: Optional[dict[str, str]] = None,
) -> ShareAnalysis:
    """Compute complete share analysis for one metric type.

    Args:
        market_ts: Financial timeseries rows (all operators, all quarters).
            Only needed when metric_type="revenue".
        sub_data_by_op: {operator_id: subscriber rows}. Only needed for
            metric_type="mobile_subscribers" or "broadband_subscribers".
        quarters: Ordered list of CQ labels (e.g. ["CQ1_2024", ..., "CQ4_2025"]).
        target_operator_id: The target operator to highlight.
        metric_type: One of "revenue", "mobile_subscribers", "broadband_subscribers".
        display_names: Optional {operator_id: display_name} map.

    Returns:
        ShareAnalysis with all computed metrics.
    """
    if not quarters:
        return ShareAnalysis(metric_type=metric_type, target_operator_id=target_operator_id)

    display_names = display_names or {}

    # 1. Extract share percentages
    if metric_type == "revenue":
        shares_data = _extract_revenue_shares(market_ts, quarters)
    elif metric_type == "mobile_subscribers":
        shares_data = _extract_subscriber_shares(sub_data_by_op, quarters, "mobile_total_k")
    elif metric_type == "broadband_subscribers":
        shares_data = _extract_subscriber_shares(sub_data_by_op, quarters, "broadband_total_k")
    else:
        return ShareAnalysis(metric_type=metric_type, target_operator_id=target_operator_id)

    if not shares_data:
        return ShareAnalysis(
            metric_type=metric_type,
            quarters=quarters,
            target_operator_id=target_operator_id,
        )

    # 2. Compute ranks
    ranks = _compute_ranks(shares_data, quarters)

    # 3. Build operator series
    series_list = []
    for op_id, q_shares in shares_data.items():
        name = display_names.get(op_id, op_id.replace("_", " ").title())
        series = _build_operator_series(op_id, name, q_shares, quarters, ranks.get(op_id, {}))
        series_list.append(series)

    # Sort by latest share descending
    series_list.sort(key=lambda s: -(s.latest_share_pct or 0))

    # 4. HHI concentration
    shares_by_q: dict[str, list[float]] = {}
    for cq in quarters:
        vals = []
        for op_id in shares_data:
            v = shares_data[op_id].get(cq)
            if v is not None:
                vals.append(v)
        shares_by_q[cq] = vals

    hhi_trend = _compute_hhi(shares_by_q)
    latest_hhi = hhi_trend[-1] if hhi_trend else 0.0

    # CR3
    latest_shares = sorted(
        [s.latest_share_pct for s in series_list if s.latest_share_pct is not None],
        reverse=True,
    )
    cr3 = sum(latest_shares[:3]) if len(latest_shares) >= 3 else sum(latest_shares)

    # HHI direction
    hhi_direction = "stable"
    if len(hhi_trend) >= 2:
        hhi_change = hhi_trend[-1] - hhi_trend[0]
        if hhi_change > 50:
            hhi_direction = "concentrating"
        elif hhi_change < -50:
            hhi_direction = "fragmenting"

    concentration = MarketConcentration(
        hhi=round(latest_hhi, 2),
        hhi_label=_classify_hhi(latest_hhi),
        cr3=round(cr3, 2),
        hhi_trend=hhi_trend,
        hhi_direction=hhi_direction,
    )

    # 5. Identify target, leader, movers
    target_series = None
    for s in series_list:
        if s.operator_id == target_operator_id:
            target_series = s
            break

    share_leader = series_list[0].operator_id if series_list else None
    biggest_gainer, biggest_loser = _identify_share_movements(series_list)

    # 6. Key message
    key_msg = _generate_key_message(target_series, concentration, metric_type)

    return ShareAnalysis(
        metric_type=metric_type,
        quarters=quarters,
        operator_series=series_list,
        concentration=concentration,
        target_operator_id=target_operator_id,
        target_series=target_series,
        share_leader_id=share_leader,
        biggest_gainer_id=biggest_gainer,
        biggest_loser_id=biggest_loser,
        key_message=key_msg,
    )
