"""GroupSummaryGenerator — cross-market comparison report for group analysis.

Takes individual market FiveLooksResult objects and produces a structured
comparison dict covering revenue, subscribers, competitive position,
common opportunities/threats, and capex investment.
"""

from __future__ import annotations

from collections import Counter
from typing import Optional


class GroupSummaryGenerator:
    """Generate a cross-market summary from individual market FiveLooksResults."""

    def generate(self, market_results: dict, group_info: dict) -> dict:
        """Generate a cross-market summary.

        Args:
            market_results: {market_id: FiveLooksResult, ...}
            group_info: dict with group metadata (group_name, headquarters, etc.)

        Returns:
            Structured dict with comparison data.
        """
        summary = {
            "group_id": group_info.get("group_id", ""),
            "group_name": group_info.get("group_name", ""),
            "market_count": len(market_results),
            "markets": list(market_results.keys()),
            "revenue_comparison": self._compare_revenue(market_results),
            "subscriber_comparison": self._compare_subscribers(market_results),
            "competitive_position": self._compare_competitive_position(market_results),
            "common_opportunities": self._find_common_opportunities(market_results),
            "common_threats": self._find_common_threats(market_results),
            "capex_investment": self._compare_capex(market_results),
            "health_ratings": self._compare_health(market_results),
            "key_findings": self._derive_key_findings(market_results),
        }
        return summary

    # ------------------------------------------------------------------
    # Revenue comparison
    # ------------------------------------------------------------------

    def _compare_revenue(self, market_results: dict) -> dict:
        """Per-market total revenue, growth, EBITDA margin."""
        comparison = {}
        for market, result in market_results.items():
            sa = result.self_analysis
            if sa is None:
                comparison[market] = {
                    "total_revenue": None,
                    "revenue_growth_pct": None,
                    "ebitda_margin_pct": None,
                }
                continue

            fh = sa.financial_health or {}
            comparison[market] = {
                "total_revenue": fh.get("total_revenue"),
                "revenue_growth_pct": fh.get("revenue_yoy_pct") or fh.get("service_revenue_growth_pct"),
                "ebitda_margin_pct": fh.get("ebitda_margin_pct"),
                "ebitda": fh.get("ebitda"),
            }
        return comparison

    # ------------------------------------------------------------------
    # Subscriber comparison
    # ------------------------------------------------------------------

    def _compare_subscribers(self, market_results: dict) -> dict:
        """Per-market mobile subs, broadband subs, ARPU."""
        comparison = {}
        for market, result in market_results.items():
            sa = result.self_analysis
            if sa is None:
                comparison[market] = {}
                continue

            fh = sa.financial_health or {}

            # Primary: financial_health; fallback: segment_analyses key_metrics
            mobile_k = fh.get("mobile_total_k") or fh.get("mobile_subscribers_k")
            bb_k = fh.get("broadband_total_k") or fh.get("broadband_subscribers_k")
            arpu = fh.get("mobile_arpu") or fh.get("blended_arpu")

            if (mobile_k is None or bb_k is None or arpu is None) and sa.segment_analyses:
                for seg in sa.segment_analyses:
                    km = seg.key_metrics or {}
                    if mobile_k is None:
                        mobile_k = km.get("mobile_total_k") or km.get("mobile_subscribers_k")
                    if bb_k is None:
                        bb_k = km.get("broadband_total_k") or km.get("broadband_subscribers_k")
                    if arpu is None:
                        arpu = km.get("mobile_arpu") or km.get("blended_arpu")

            comparison[market] = {
                "mobile_subs_k": mobile_k,
                "broadband_subs_k": bb_k,
                "mobile_arpu": arpu,
            }
        return comparison

    # ------------------------------------------------------------------
    # Competitive position
    # ------------------------------------------------------------------

    def _compare_competitive_position(self, market_results: dict) -> dict:
        """Per-market target operator ranking and market position."""
        comparison = {}
        for market, result in market_results.items():
            comp = result.competition
            if comp is None:
                comparison[market] = {"ranking": None, "intensity": None}
                continue

            ranking = getattr(comp, "target_ranking", None)
            intensity = getattr(comp, "overall_competition_intensity", None)
            comparison[market] = {
                "ranking": ranking,
                "intensity": intensity,
            }
        return comparison

    # ------------------------------------------------------------------
    # Common opportunities
    # ------------------------------------------------------------------

    def _find_common_opportunities(self, market_results: dict) -> list[str]:
        """Find opportunity themes appearing in 2+ markets."""
        all_opps = []
        for market, result in market_results.items():
            opp = result.opportunities
            if opp is None:
                continue

            # Extract opportunity names/descriptions
            opps_list = getattr(opp, "opportunities", [])
            for o in opps_list:
                name = o.name if hasattr(o, "name") else str(o)
                all_opps.append(self._normalize_theme(name))

            # Also check SWOT opportunities
            swot = result.swot
            if swot:
                for o in getattr(swot, "opportunities", []):
                    all_opps.append(self._normalize_theme(str(o)))

        # Find themes appearing 2+ times
        counts = Counter(all_opps)
        return [theme for theme, count in counts.most_common()
                if count >= 2 and theme]

    # ------------------------------------------------------------------
    # Common threats
    # ------------------------------------------------------------------

    def _find_common_threats(self, market_results: dict) -> list[str]:
        """Find threat themes appearing in 2+ markets."""
        all_threats = []
        for market, result in market_results.items():
            swot = result.swot
            if swot is None:
                continue

            for t in getattr(swot, "threats", []):
                all_threats.append(self._normalize_theme(str(t)))

            # Also from competition
            comp = result.competition
            if comp:
                forces = comp.five_forces if hasattr(comp, "five_forces") else {}
                for force_name, force in forces.items():
                    level = force.force_level if hasattr(force, "force_level") else str(force)
                    if level == "high":
                        all_threats.append(self._normalize_theme(f"High {force_name}"))

        counts = Counter(all_threats)
        return [theme for theme, count in counts.most_common()
                if count >= 2 and theme]

    # ------------------------------------------------------------------
    # Capex comparison
    # ------------------------------------------------------------------

    def _compare_capex(self, market_results: dict) -> dict:
        """Per-market capex/revenue ratio."""
        comparison = {}
        for market, result in market_results.items():
            sa = result.self_analysis
            if sa is None:
                comparison[market] = {"capex_to_revenue_pct": None}
                continue

            fh = sa.financial_health or {}
            comparison[market] = {
                "capex_to_revenue_pct": fh.get("capex_to_revenue_pct"),
                "capex": fh.get("capex"),
            }
        return comparison

    # ------------------------------------------------------------------
    # Health comparison
    # ------------------------------------------------------------------

    def _compare_health(self, market_results: dict) -> dict:
        """Per-market health rating."""
        comparison = {}
        for market, result in market_results.items():
            sa = result.self_analysis
            if sa is None:
                comparison[market] = "N/A"
                continue
            comparison[market] = getattr(sa, "health_rating", "N/A")
        return comparison

    # ------------------------------------------------------------------
    # Key findings
    # ------------------------------------------------------------------

    def _derive_key_findings(self, market_results: dict) -> list[str]:
        """Derive cross-market key findings."""
        findings = []

        # Best/worst performing markets by revenue growth
        revenue_data = {}
        for market, result in market_results.items():
            sa = result.self_analysis
            if sa is None:
                continue
            fh = sa.financial_health or {}
            growth = fh.get("revenue_yoy_pct") or fh.get("service_revenue_growth_pct")
            if growth is not None:
                revenue_data[market] = growth

        if revenue_data:
            best = max(revenue_data, key=revenue_data.get)
            worst = min(revenue_data, key=revenue_data.get)
            findings.append(
                f"Strongest revenue growth: {best} ({revenue_data[best]:+.1f}%)"
            )
            if best != worst:
                findings.append(
                    f"Weakest revenue growth: {worst} ({revenue_data[worst]:+.1f}%)"
                )

        # Markets with high competitive intensity
        high_intensity = []
        for market, result in market_results.items():
            comp = result.competition
            if comp is None:
                continue
            intensity = getattr(comp, "overall_competition_intensity", "")
            if intensity == "high":
                high_intensity.append(market)
        if high_intensity:
            findings.append(
                f"High competitive intensity in: {', '.join(high_intensity)}"
            )

        # Count total opportunities
        total_opps = 0
        for result in market_results.values():
            opp = result.opportunities
            if opp:
                total_opps += len(getattr(opp, "opportunities", []))
        if total_opps:
            findings.append(
                f"Total opportunities identified across all markets: {total_opps}"
            )

        return findings

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_theme(text: str) -> str:
        """Normalize an opportunity/threat theme for comparison.

        Simplifies text to enable cross-market matching of similar themes.
        """
        if not text:
            return ""
        # Lowercase, strip, take first 60 chars for coarse matching
        normalized = text.lower().strip()
        # Remove common prefixes
        for prefix in ("high ", "low ", "strong ", "weak "):
            if normalized.startswith(prefix):
                normalized = normalized[len(prefix):]
        return normalized[:60]
