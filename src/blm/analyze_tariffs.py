"""Tariff deep-analysis module.

Queries tariff data from the database and produces structured comparison
data suitable for PPT chart/table generation.

Output dict sections:
  1. mobile_postpaid_comparison — cross-operator tier comparison
  2. value_per_gb — EUR/GB ranking
  3. price_evolution — historical price by operator/tier
  4. fixed_comparison — DSL/Cable/Fiber cross-operator
  5. fmc_comparison — convergence bundle comparison
  6. five_g_erosion — 5G premium trend over snapshots
  7. strategic_insights — text bullets
"""

from __future__ import annotations

import re
from typing import Optional


def analyze_tariffs(
    db,
    market: str,
    target_operator: str,
    latest_snapshot: str = "H1_2026",
) -> dict:
    """Run tariff analysis and return structured results dict.

    Args:
        db: Initialized TelecomDatabase instance.
        market: Market identifier (e.g. "germany").
        target_operator: Protagonist operator_id.
        latest_snapshot: The snapshot period to use for current comparisons.

    Returns:
        dict with 7 analysis sections.
    """
    result = {}

    # 1. Mobile postpaid cross-operator comparison
    result["mobile_postpaid_comparison"] = _mobile_postpaid_comparison(
        db, market, latest_snapshot
    )

    # 2. EUR/GB value ranking
    result["value_per_gb"] = _value_per_gb(db, market, latest_snapshot)

    # 3. Price evolution per operator
    result["price_evolution"] = _price_evolution(db, market)

    # 4. Fixed broadband comparison
    result["fixed_comparison"] = _fixed_comparison(db, market, latest_snapshot)

    # 5. FMC bundle comparison
    result["fmc_comparison"] = _fmc_comparison(db, market, latest_snapshot)

    # 6. 5G premium erosion
    result["five_g_erosion"] = _five_g_erosion(db, market)

    # 7. Strategic insights
    result["strategic_insights"] = _strategic_insights(
        result, target_operator
    )

    return result


# =========================================================================
# Section builders
# =========================================================================

def _mobile_postpaid_comparison(db, market: str, snapshot: str) -> list:
    """Group mobile postpaid tariffs by tier with all operators."""
    rows = db.get_tariff_comparison(market, "mobile_postpaid", snapshot)
    tiers_order = ["s", "m", "l", "xl"]
    tier_map: dict[str, list] = {t: [] for t in tiers_order}

    for row in rows:
        tier = row.get("plan_tier", "")
        if tier not in tier_map:
            continue
        tier_map[tier].append({
            "operator_id": row["operator_id"],
            "display_name": row.get("display_name", row["operator_id"]),
            "plan_name": row["plan_name"],
            "price": row.get("monthly_price"),
            "data": row.get("data_allowance", ""),
            "includes_5g": bool(row.get("includes_5g", 0)),
        })

    result = []
    for tier in tiers_order:
        operators = tier_map[tier]
        if operators:
            result.append({"tier": tier, "operators": operators})
    return result


def _parse_data_gb(data_str) -> Optional[float]:
    """Convert data_allowance string to numeric GB. Returns None for unlimited."""
    if data_str is None:
        return None
    s = str(data_str).strip().lower()
    if "unlim" in s:
        return None
    m = re.match(r"([\d.]+)\s*(gb|tb|mb)?", s)
    if not m:
        return None
    val = float(m.group(1))
    unit = (m.group(2) or "gb").lower()
    if unit == "tb":
        return val * 1024
    if unit == "mb":
        return val / 1024
    return val


def _value_per_gb(db, market: str, snapshot: str) -> list:
    """Compute EUR/GB for all mobile postpaid plans and rank."""
    rows = db.get_tariff_comparison(market, "mobile_postpaid", snapshot)
    entries = []
    for row in rows:
        price = row.get("monthly_price")
        data_gb = _parse_data_gb(row.get("data_allowance"))
        if price is None or data_gb is None or data_gb <= 0:
            continue
        eur_per_gb = round(price / data_gb, 2)
        entries.append({
            "operator": row.get("display_name", row["operator_id"]),
            "plan": row["plan_name"],
            "price": price,
            "data_gb": data_gb,
            "eur_per_gb": eur_per_gb,
        })
    entries.sort(key=lambda x: x["eur_per_gb"])
    return entries


def _price_evolution(db, market: str) -> dict:
    """Price history per operator across all snapshots for mobile postpaid."""
    all_tariffs = db.get_tariffs(market=market, plan_type="mobile_postpaid")

    # Group by operator_id -> snapshot -> tier -> price
    op_data: dict[str, dict[str, dict]] = {}
    for t in all_tariffs:
        op = t["operator_id"]
        snap = t["snapshot_period"]
        tier = t.get("plan_tier", "")
        price = t.get("monthly_price")
        if op not in op_data:
            op_data[op] = {}
        if snap not in op_data[op]:
            op_data[op][snap] = {}
        op_data[op][snap][tier] = price

    # Build sorted timeline per operator
    result = {}
    for op, snap_dict in op_data.items():
        snapshots_sorted = sorted(snap_dict.keys())
        timeline = []
        for snap in snapshots_sorted:
            entry = {"snapshot": snap}
            entry.update(snap_dict[snap])
            timeline.append(entry)
        result[op] = timeline
    return result


def _fixed_comparison(db, market: str, snapshot: str) -> dict:
    """Compare fixed broadband tariffs across DSL, Cable, Fiber."""
    result = {}
    for plan_type in ("fixed_dsl", "fixed_cable", "fixed_fiber"):
        rows = db.get_tariff_comparison(market, plan_type, snapshot)
        entries = []
        for row in rows:
            entries.append({
                "operator_id": row["operator_id"],
                "display_name": row.get("display_name", row["operator_id"]),
                "plan_name": row["plan_name"],
                "price": row.get("monthly_price"),
                "speed_mbps": row.get("speed_mbps"),
                "tier": row.get("plan_tier", ""),
            })
        result[plan_type] = entries
    return result


def _fmc_comparison(db, market: str, snapshot: str) -> list:
    """Compare FMC bundle tariffs."""
    rows = db.get_tariff_comparison(market, "fmc_bundle", snapshot)
    entries = []
    for row in rows:
        entries.append({
            "operator_id": row["operator_id"],
            "display_name": row.get("display_name", row["operator_id"]),
            "plan_name": row["plan_name"],
            "price": row.get("monthly_price"),
            "tier": row.get("plan_tier", ""),
        })
    return entries


def _five_g_erosion(db, market: str) -> list:
    """Track 5G premium erosion across snapshots.

    For each snapshot, compute the average price of plans with vs without 5G
    in mobile postpaid, and the premium percentage.
    """
    all_tariffs = db.get_tariffs(market=market, plan_type="mobile_postpaid")

    # Group by snapshot
    snap_data: dict[str, dict] = {}
    for t in all_tariffs:
        snap = t["snapshot_period"]
        if snap not in snap_data:
            snap_data[snap] = {"with_5g": [], "without_5g": []}
        price = t.get("monthly_price")
        if price is None:
            continue
        if t.get("includes_5g"):
            snap_data[snap]["with_5g"].append(price)
        else:
            snap_data[snap]["without_5g"].append(price)

    result = []
    for snap in sorted(snap_data.keys()):
        d = snap_data[snap]
        with_prices = d["with_5g"]
        without_prices = d["without_5g"]
        avg_with = sum(with_prices) / len(with_prices) if with_prices else None
        avg_without = (
            sum(without_prices) / len(without_prices) if without_prices else None
        )

        premium_pct = None
        if avg_with is not None and avg_without is not None and avg_without > 0:
            premium_pct = round((avg_with / avg_without - 1) * 100, 1)

        result.append({
            "snapshot": snap,
            "premium_pct": premium_pct,
            "plans_with_5g": len(with_prices),
            "plans_without": len(without_prices),
            "avg_price_5g": round(avg_with, 1) if avg_with else None,
            "avg_price_no_5g": round(avg_without, 1) if avg_without else None,
        })
    return result


def _strategic_insights(analysis: dict, target_operator: str) -> list:
    """Derive text insights from the computed analysis sections."""
    insights = []

    # Value leader identification
    value_list = analysis.get("value_per_gb", [])
    if value_list:
        best = value_list[0]
        insights.append(
            f"Best value: {best['operator']} {best['plan']} at "
            f"EUR {best['eur_per_gb']:.2f}/GB"
        )

    # 5G erosion trend
    erosion = analysis.get("five_g_erosion", [])
    if len(erosion) >= 2:
        first = erosion[0]
        last = erosion[-1]
        if first.get("premium_pct") is not None and last.get("premium_pct") is not None:
            insights.append(
                f"5G premium eroded from {first['premium_pct']:+.0f}% "
                f"({first['snapshot']}) to {last['premium_pct']:+.0f}% "
                f"({last['snapshot']}) — 5G is now standard"
            )
        elif first.get("premium_pct") is not None and last.get("plans_without") == 0:
            insights.append(
                f"5G premium fully eroded: all plans now include 5G "
                f"as of {last['snapshot']}"
            )

    # Price gap analysis
    comparison = analysis.get("mobile_postpaid_comparison", [])
    for tier_data in comparison:
        ops = tier_data.get("operators", [])
        prices = [o["price"] for o in ops if o.get("price") is not None]
        if len(prices) >= 2:
            gap = max(prices) - min(prices)
            cheapest = min(ops, key=lambda o: o.get("price") or 999)
            most_exp = max(ops, key=lambda o: o.get("price") or 0)
            insights.append(
                f"Tier {tier_data['tier'].upper()}: EUR {gap:.0f} gap — "
                f"cheapest {cheapest['display_name']}, "
                f"most expensive {most_exp['display_name']}"
            )

    # FMC insight
    fmc = analysis.get("fmc_comparison", [])
    if fmc:
        fmc_prices = [f["price"] for f in fmc if f.get("price")]
        if fmc_prices:
            cheapest_fmc = min(fmc, key=lambda f: f.get("price") or 999)
            insights.append(
                f"Cheapest FMC bundle: {cheapest_fmc['display_name']} "
                f"{cheapest_fmc['plan_name']} at EUR {cheapest_fmc['price']:.0f}/mo"
            )

    return insights
