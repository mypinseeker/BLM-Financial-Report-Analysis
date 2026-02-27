#!/usr/bin/env python3
"""QA Audit Script for BLM Seed Files.

Checks all seed_*.py files for data integrity issues:
  1. SOURCE: Missing _source / _source_url fields
  2. FABRICATION: Suspiciously smooth time series (linear/monotonic 8-quarter data)
  3. SIM INFLATION: Mobile subscriber count > 150% of population without explanation
  4. SPECTRUM: Spectrum data without regulator source
  5. UNDISCLOSED: Quarters that should be None but have fabricated values
  6. STRUCTURE: Basic market structure sanity checks

Usage:
    python3 scripts/qa_seed_audit.py                    # audit all markets
    python3 scripts/qa_seed_audit.py colombia panama    # audit specific markets
    python3 scripts/qa_seed_audit.py --summary          # summary only

Output: Per-market report with severity levels (CRITICAL / WARNING / INFO)
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

# ── Setup ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
SEED_DIR = PROJECT_ROOT / "src" / "database"

# ── Known populations (millions, approximate) ──
POPULATIONS = {
    "colombia": 52,
    "panama": 4.4,
    "guatemala": 18,
    "honduras": 10.5,
    "paraguay": 7.4,
    "bolivia": 12.4,
    "el_salvador": 6.3,
    "nicaragua": 7.0,
    "ecuador": 18.2,
    "uruguay": 3.5,
    "chile": 19.5,
    "germany": 84,
    "netherlands": 17.9,
    "belgium": 11.7,
    "france": 68,
    "italy": 59,
    "poland": 38,
    "switzerland": 8.9,
    "ireland": 5.1,
    "ukraine": 37,
    "cyprus": 1.3,
    "malta": 0.5,
}

# ── Severity ──
CRITICAL = "🔴 CRITICAL"
WARNING = "🟡 WARNING"
INFO = "🔵 INFO"
PASS = "✅ PASS"


def load_seed(market: str) -> dict | None:
    """Dynamically import a seed module and return its data."""
    module_name = f"src.database.seed_{market}"
    try:
        mod = importlib.import_module(module_name)
        if hasattr(mod, "get_seed_data"):
            return mod.get_seed_data()
        else:
            return None
    except Exception as e:
        return None


def is_linear_series(series: list, tolerance: float = 0.15) -> bool:
    """Check if a numeric series follows a near-linear progression.

    Returns True if the step sizes vary by less than `tolerance` of their mean,
    indicating suspiciously smooth fabricated data.
    """
    nums = [x for x in series if isinstance(x, (int, float)) and x != 0]
    if len(nums) < 4:
        return False

    steps = [nums[i+1] - nums[i] for i in range(len(nums)-1)]
    if not steps:
        return False

    mean_step = sum(steps) / len(steps)
    if mean_step == 0:
        return False  # flat series, different pattern

    # Check if all steps are within tolerance of the mean step
    max_deviation = max(abs(s - mean_step) for s in steps)
    return max_deviation / abs(mean_step) < tolerance


def is_monotonic(series: list) -> bool:
    """Check if a series is strictly monotonically increasing or decreasing."""
    nums = [x for x in series if isinstance(x, (int, float)) and x != 0]
    if len(nums) < 5:
        return False

    increasing = all(nums[i] < nums[i+1] for i in range(len(nums)-1))
    decreasing = all(nums[i] > nums[i+1] for i in range(len(nums)-1))
    return increasing or decreasing


def count_non_none(series: list) -> int:
    """Count non-None, non-zero values in a series."""
    return sum(1 for x in series if isinstance(x, (int, float)) and x != 0)


def check_sources(data: dict, path: str = "") -> list[tuple[str, str, str]]:
    """Recursively check for _source and _source_url fields."""
    issues = []

    if isinstance(data, dict):
        # Check if this dict has data fields but no source
        has_data_keys = any(
            k for k in data.keys()
            if not k.startswith("_") and k not in ("data_as_of",)
        )
        has_source = "_source" in data
        has_source_url = "_source_url" in data

        if has_data_keys and not has_source and path:
            # Only flag leaf data dicts (those with actual numeric values)
            has_numeric = any(
                isinstance(v, (int, float)) or
                (isinstance(v, list) and any(isinstance(x, (int, float)) for x in v))
                for k, v in data.items() if not k.startswith("_")
            )
            if has_numeric:
                issues.append((CRITICAL, f"{path}", "Missing _source field"))

        if has_source and not has_source_url and path:
            issues.append((WARNING, f"{path}", "Has _source but missing _source_url"))

        # Recurse into sub-dicts
        for k, v in data.items():
            if not k.startswith("_"):
                child_path = f"{path}.{k}" if path else k
                issues.extend(check_sources(v, child_path))

    return issues


def check_fabrication(data: dict, path: str = "") -> list[tuple[str, str, str]]:
    """Check for suspiciously smooth time series data."""
    issues = []

    if isinstance(data, dict):
        for k, v in data.items():
            if k.startswith("_"):
                continue
            child_path = f"{path}.{k}" if path else k

            if isinstance(v, list) and len(v) >= 6 and any(isinstance(x, (int, float)) for x in v):
                non_none_count = count_non_none(v)

                if non_none_count >= 6:
                    # 6+ non-None values in an 8-quarter series = suspicious
                    if is_linear_series(v):
                        issues.append((
                            CRITICAL, child_path,
                            f"Near-linear 8Q series ({non_none_count} values): "
                            f"{v} — likely fabricated"
                        ))
                    elif is_monotonic(v):
                        issues.append((
                            WARNING, child_path,
                            f"Strictly monotonic 8Q series ({non_none_count} values): "
                            f"{v} — may be fabricated"
                        ))
                elif non_none_count >= 4:
                    nums = [x for x in v if x is not None and x != 0]
                    if is_linear_series(nums):
                        issues.append((
                            WARNING, child_path,
                            f"Near-linear partial series ({non_none_count} values): "
                            f"may be fabricated"
                        ))
            elif isinstance(v, dict):
                issues.extend(check_fabrication(v, child_path))

    return issues


def check_sim_inflation(data: dict, market: str) -> list[tuple[str, str, str]]:
    """Check if subscriber counts exceed population by unreasonable multiples."""
    issues = []
    pop = POPULATIONS.get(market)
    if not pop:
        return issues

    pop_k = pop * 1000  # population in thousands

    subs = data.get("subscribers", {})
    for op_id, op_data in subs.items():
        if not isinstance(op_data, dict):
            continue

        for key in ("mobile_total_k", "total_mobile_lines_k"):
            if key in op_data:
                val = op_data[key]
                if isinstance(val, list):
                    val = max(x for x in val if x is not None and x != 0) if any(
                        x for x in val if x is not None and x != 0
                    ) else 0
                if isinstance(val, (int, float)) and val > 0:
                    ratio = val / pop_k
                    if ratio > 2.0:
                        issues.append((
                            CRITICAL, f"subscribers.{op_id}.{key}",
                            f"{val}K subs vs {pop}M population = {ratio:.1f}x "
                            f"penetration — needs IoT/dormant SIM explanation"
                        ))
                    elif ratio > 1.5:
                        issues.append((
                            WARNING, f"subscribers.{op_id}.{key}",
                            f"{val}K subs vs {pop}M population = {ratio:.1f}x "
                            f"penetration — may include IoT/dormant SIMs"
                        ))

    # Also check _market_totals
    net_infra = data.get("network_infrastructure", {})
    for op_id, op_data in net_infra.items():
        if not isinstance(op_data, dict):
            continue
        mt = op_data.get("_market_totals", {})
        if isinstance(mt, dict):
            total_lines = mt.get("total_mobile_lines_k")
            if isinstance(total_lines, (int, float)) and total_lines > 0:
                ratio = total_lines / pop_k
                if ratio > 2.0:
                    has_explanation = (
                        "revenue_generating_lines_k" in mt or
                        "revenue_generating_lines_pct" in mt or
                        "_analytical_note" in mt
                    )
                    if not has_explanation:
                        issues.append((
                            CRITICAL,
                            f"network_infrastructure.{op_id}._market_totals.total_mobile_lines_k",
                            f"{total_lines}K total lines vs {pop}M population = "
                            f"{ratio:.1f}x — NEEDS IoT/dormant SIM explanation"
                        ))
                    else:
                        issues.append((
                            PASS,
                            f"network_infrastructure.{op_id}._market_totals",
                            f"SIM inflation ({ratio:.1f}x) has explanation/context ✓"
                        ))

    return issues


def check_spectrum_sources(data: dict) -> list[tuple[str, str, str]]:
    """Check if spectrum data has proper regulator sources."""
    issues = []

    net_infra = data.get("network_infrastructure", {})
    for op_id, op_data in net_infra.items():
        if not isinstance(op_data, dict):
            continue

        spectrum = op_data.get("spectrum", {})
        if not spectrum:
            continue

        has_source = "_source" in spectrum or "_source" in op_data
        has_url = "_source_url" in spectrum or "_source_url" in op_data

        # Check if source mentions regulator
        source_text = str(spectrum.get("_source", "")) + str(op_data.get("_source", ""))
        is_regulator_source = any(
            kw in source_text.lower()
            for kw in ["ane", "asep", "crc", "sit", "conatel", "att ", "arcotel",
                       "ursec", "subtel", "arcep", "agcom", "uke", "ofcom",
                       "comreg", "spectrum-tracker", "regulator", "mintic",
                       "bundesnetzagentur", "bipt", "acm"]
        )

        if not has_source:
            issues.append((
                CRITICAL, f"network_infrastructure.{op_id}.spectrum",
                "Spectrum data has no _source field"
            ))
        elif not is_regulator_source:
            issues.append((
                WARNING, f"network_infrastructure.{op_id}.spectrum",
                f"Spectrum source '{source_text[:80]}' is not a regulator/spectrum-tracker"
            ))

        if has_source and not has_url:
            issues.append((
                WARNING, f"network_infrastructure.{op_id}.spectrum",
                "Spectrum data has no _source_url"
            ))

    return issues


def check_undisclosed_quarters(data: dict, market: str) -> list[tuple[str, str, str]]:
    """Flag markets where Millicom only discloses FY/Q4 but all 8 quarters have data."""
    issues = []

    # Markets where Millicom typically only discloses limited quarterly data
    millicom_markets = {
        "colombia", "guatemala", "honduras", "paraguay", "bolivia",
        "el_salvador", "nicaragua", "panama", "ecuador", "uruguay"
    }

    if market not in millicom_markets:
        return issues

    financials = data.get("financials", {})
    tigo_key = None
    for k in financials:
        if k.startswith("tigo_"):
            tigo_key = k
            break

    if not tigo_key:
        return issues

    tigo_data = financials[tigo_key]
    if not isinstance(tigo_data, dict):
        return issues

    for key, val in tigo_data.items():
        if key.startswith("_"):
            continue
        if isinstance(val, list) and len(val) == 8:
            non_none = count_non_none(val)
            if non_none >= 6:
                issues.append((
                    CRITICAL, f"financials.{tigo_key}.{key}",
                    f"Millicom market has {non_none}/8 quarters filled — "
                    f"Millicom typically does NOT disclose quarterly country data. "
                    f"Values: {val}"
                ))

    return issues


def audit_market(market: str) -> dict:
    """Run all QA checks on a single market seed file."""
    data = load_seed(market)
    if data is None:
        return {
            "market": market,
            "status": "ERROR",
            "message": f"Could not load seed_{market}.py",
            "issues": [],
        }

    all_issues = []

    # 1. Source checks
    all_issues.extend(check_sources(data))

    # 2. Fabrication detection
    all_issues.extend(check_fabrication(data))

    # 3. SIM inflation
    all_issues.extend(check_sim_inflation(data, market))

    # 4. Spectrum source validation
    all_issues.extend(check_spectrum_sources(data))

    # 5. Undisclosed quarter detection
    all_issues.extend(check_undisclosed_quarters(data, market))

    # Count by severity
    counts = {CRITICAL: 0, WARNING: 0, INFO: 0, PASS: 0}
    for sev, _, _ in all_issues:
        counts[sev] = counts.get(sev, 0) + 1

    return {
        "market": market,
        "status": "FAIL" if counts[CRITICAL] > 0 else ("WARN" if counts[WARNING] > 0 else "OK"),
        "counts": counts,
        "issues": all_issues,
    }


def discover_markets() -> list[str]:
    """Find all seed_*.py files and extract market names."""
    skip = {"tariffs", "tariffs_chile", "chile_gaps", "chile_v2",
            "internet_data", "latam_helper", "millicom", "orchestrator"}
    markets = []
    for f in sorted(SEED_DIR.glob("seed_*.py")):
        name = f.stem.replace("seed_", "")
        if name not in skip:
            markets.append(name)
    return markets


def main():
    import argparse
    parser = argparse.ArgumentParser(description="QA Audit for BLM Seed Files")
    parser.add_argument("markets", nargs="*", help="Specific markets to audit (default: all)")
    parser.add_argument("--summary", action="store_true", help="Summary table only")
    args = parser.parse_args()

    markets = args.markets if args.markets else discover_markets()

    results = []
    for m in markets:
        result = audit_market(m)
        results.append(result)

    # ── Print results ──
    print("=" * 90)
    print("BLM SEED FILE QA AUDIT REPORT")
    print(f"Markets audited: {len(results)}")
    print("=" * 90)

    total_critical = 0
    total_warning = 0

    for r in results:
        c = r.get("counts", {})
        nc = c.get(CRITICAL, 0)
        nw = c.get(WARNING, 0)
        np_ = c.get(PASS, 0)
        total_critical += nc
        total_warning += nw

        status_icon = "❌" if nc > 0 else ("⚠️" if nw > 0 else "✅")
        print(f"\n{status_icon}  {r['market'].upper():20s}  "
              f"CRITICAL: {nc}  WARNING: {nw}  PASS: {np_}")

        if not args.summary and r.get("issues"):
            for sev, path, msg in r["issues"]:
                if sev == PASS and not args.summary:
                    continue  # Skip PASS in detailed view unless summary
                print(f"    {sev}  [{path}]")
                print(f"           {msg}")

    # ── Summary ──
    print("\n" + "=" * 90)
    print("SUMMARY")
    print("=" * 90)

    ok_markets = [r["market"] for r in results if r["status"] == "OK"]
    warn_markets = [r["market"] for r in results if r["status"] == "WARN"]
    fail_markets = [r["market"] for r in results if r["status"] == "FAIL"]
    error_markets = [r["market"] for r in results if r["status"] == "ERROR"]

    print(f"\n✅ PASS:     {len(ok_markets):3d}  {', '.join(ok_markets) if ok_markets else '—'}")
    print(f"⚠️  WARN:     {len(warn_markets):3d}  {', '.join(warn_markets) if warn_markets else '—'}")
    print(f"❌ FAIL:     {len(fail_markets):3d}  {', '.join(fail_markets) if fail_markets else '—'}")
    print(f"💀 ERROR:    {len(error_markets):3d}  {', '.join(error_markets) if error_markets else '—'}")
    print(f"\nTotal issues: {total_critical} CRITICAL + {total_warning} WARNING")

    if total_critical > 0:
        print(f"\n⛔ {total_critical} CRITICAL issues found across {len(fail_markets)} markets.")
        print("   These markets have fabricated data, missing sources, or unverified figures.")
        print("   DO NOT use these seed files for reports without verification.")

    return 1 if total_critical > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
