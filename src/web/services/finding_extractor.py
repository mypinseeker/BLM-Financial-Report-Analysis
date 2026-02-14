"""FindingExtractor — walks saved JSON output and extracts discrete findings.

Provides feedback-to-PPT decision mapping and key_message override extraction.
Used by the feedback web UI to present findings for user annotation, and by
the finalize endpoint to convert feedback into generator parameters.
"""
from __future__ import annotations

from typing import Any


class FindingExtractor:
    """Extract discrete findings from a BLM analysis JSON output."""

    def extract_all(self, json_data: dict) -> dict[str, list[dict]]:
        """Return {look_category: [{finding_ref, label, value, section}, ...]}.

        Args:
            json_data: Full JSON output from BLMJsonExporter (top-level keys:
                       meta, five_looks, data_quality, provenance).
        """
        five = json_data.get("five_looks", {})
        findings: dict[str, list[dict]] = {}

        extractors = [
            ("trends", self._extract_trends, five.get("trends")),
            ("market", self._extract_market, five.get("market_customer")),
            ("competition", self._extract_competition, five.get("competition")),
            ("self", self._extract_self, five.get("self_analysis")),
            ("swot", self._extract_swot, five.get("swot")),
            ("opportunity", self._extract_opportunities, five.get("opportunities")),
        ]

        for category, extractor, data in extractors:
            if data:
                findings[category] = extractor(data)
            else:
                findings[category] = []

        return findings

    # ------------------------------------------------------------------
    # Per-look extractors
    # ------------------------------------------------------------------

    def _extract_trends(self, trends: dict) -> list[dict]:
        items = []
        pest = trends.get("pest") or {}
        dim_map = {
            "political": "political_factors",
            "economic": "economic_factors",
            "social": "society_factors",
            "technology": "technology_factors",
        }
        for dim_key, attr in dim_map.items():
            factors = pest.get(attr) or []
            for i, f in enumerate(factors):
                items.append({
                    "finding_ref": f"pest_{dim_key}_{i}",
                    "label": f.get("factor_name", f"Factor {i}"),
                    "value": f.get("current_status") or f.get("industry_impact", ""),
                    "section": f"PEST — {dim_key.title()}",
                })

        km = trends.get("key_message", "")
        if km:
            items.append({
                "finding_ref": "trends_key_message",
                "label": "Key Message",
                "value": km,
                "section": "Trends Key Message",
            })
        return items

    def _extract_market(self, market: dict) -> list[dict]:
        items = []
        for i, c in enumerate(market.get("changes") or []):
            items.append({
                "finding_ref": f"market_change_{i}",
                "label": c.get("description", f"Change {i}"),
                "value": c.get("impact_type", ""),
                "section": "Market Changes",
            })

        for i, dim in enumerate(market.get("appeals_assessment") or []):
            name = dim.get("dimension_name") or dim.get("dimension", f"dim_{i}")
            items.append({
                "finding_ref": f"appeals_{name.lower().replace(' ', '_')}",
                "label": f"$APPEALS — {name}",
                "value": str(dim.get("our_score", "")),
                "section": "$APPEALS",
            })

        for i, seg in enumerate(market.get("customer_segments") or []):
            items.append({
                "finding_ref": f"segment_{i}",
                "label": seg.get("segment_name", f"Segment {i}"),
                "value": seg.get("growth_trend", ""),
                "section": "Customer Segments",
            })

        km = market.get("key_message", "")
        if km:
            items.append({
                "finding_ref": "market_key_message",
                "label": "Key Message",
                "value": km,
                "section": "Market Key Message",
            })
        return items

    def _extract_competition(self, comp: dict) -> list[dict]:
        items = []
        forces = comp.get("five_forces") or {}
        for force_id, force in forces.items():
            items.append({
                "finding_ref": f"porter_{force_id}",
                "label": force.get("force_name", force_id.replace("_", " ").title()),
                "value": force.get("force_level", ""),
                "section": "Porter's Five Forces",
            })

        analyses = comp.get("competitor_analyses") or {}
        for op_id, dd in analyses.items():
            items.append({
                "finding_ref": f"competitor_{op_id}",
                "label": op_id.replace("_", " ").title(),
                "value": dd.get("growth_strategy", ""),
                "section": "Competitor Deep Dives",
            })

        km = comp.get("key_message", "")
        if km:
            items.append({
                "finding_ref": "competition_key_message",
                "label": "Key Message",
                "value": km,
                "section": "Competition Key Message",
            })
        return items

    def _extract_self(self, self_data: dict) -> list[dict]:
        items = []
        for i, seg in enumerate(self_data.get("segment_analyses") or []):
            name = seg.get("segment_name", f"segment_{i}")
            items.append({
                "finding_ref": f"self_segment_{name.lower().replace(' ', '_')}",
                "label": name,
                "value": seg.get("health_status", ""),
                "section": "Segment Analysis",
            })

        network = self_data.get("network")
        if network:
            items.append({
                "finding_ref": "network_analysis",
                "label": "Network Assessment",
                "value": network.get("investment_direction", ""),
                "section": "Network",
            })

        for i, ep in enumerate(self_data.get("exposure_points") or []):
            items.append({
                "finding_ref": f"exposure_{i}",
                "label": ep.get("trigger_action", f"Exposure {i}"),
                "value": ep.get("side_effect", ""),
                "section": "Exposure Points",
            })

        km = self_data.get("key_message", "")
        if km:
            items.append({
                "finding_ref": "self_key_message",
                "label": "Key Message",
                "value": km,
                "section": "Self Key Message",
            })
        return items

    def _extract_swot(self, swot: dict) -> list[dict]:
        items = []
        for quad, prefix in [
            ("strengths", "strength"),
            ("weaknesses", "weakness"),
            ("opportunities", "swot_opportunity"),
            ("threats", "threat"),
        ]:
            for i, item in enumerate(swot.get(quad) or []):
                label = item if isinstance(item, str) else str(item)
                items.append({
                    "finding_ref": f"{prefix}_{i}",
                    "label": label[:80],
                    "value": label,
                    "section": f"SWOT — {quad.title()}",
                })
        return items

    def _extract_opportunities(self, opp: dict) -> list[dict]:
        items = []
        for i, sp in enumerate(opp.get("span_positions") or []):
            items.append({
                "finding_ref": f"span_{i}",
                "label": sp.get("opportunity_name", f"SPAN {i}"),
                "value": sp.get("quadrant", ""),
                "section": "SPAN Matrix",
            })

        km = opp.get("key_message", "")
        if km:
            items.append({
                "finding_ref": "opportunity_key_message",
                "label": "Key Message",
                "value": km,
                "section": "Opportunities Key Message",
            })
        return items


# ======================================================================
# Feedback → PPT decision mapping
# ======================================================================

# Maps finding_ref prefix → PPT slide_id(s)
FINDING_TO_SLIDES: dict[str, list[str] | None] = {
    "pest_": ["pest_dashboard", "trend_deep_dive"],
    "trends_key_message": ["industry_env"],
    "market_change_": ["market_changes"],
    "appeals_": ["appeals"],
    "segment_": ["segments"],
    "porter_": ["five_forces"],
    "competitor_": None,  # dynamic: slide_id = "competitor_{op_id}"
    "self_segment_": ["segments_self"],
    "network_": ["network"],
    "exposure_": ["exposure"],
    "strength_": ["swot"],
    "weakness_": ["swot"],
    "swot_opportunity_": ["swot"],
    "threat_": ["swot"],
    "span_": ["span_bubble", "priority_table"],
}


def _resolve_slide_ids(finding_ref: str) -> list[str]:
    """Resolve finding_ref to list of PPT slide_ids."""
    for prefix, slide_ids in FINDING_TO_SLIDES.items():
        if finding_ref.startswith(prefix):
            if slide_ids is None:
                # Dynamic: competitor_{op_id}
                return [finding_ref]
            return slide_ids
    return []


def feedback_to_ppt_decisions(feedback: list[dict]) -> dict[str, str]:
    """If ALL findings on a slide are 'disputed', mark slide for removal.

    Returns dict mapping slide_id -> "remove" (only disputed slides).
    """
    # Collect findings per slide_id
    slide_findings: dict[str, list[str]] = {}  # slide_id -> [feedback_type, ...]
    for fb in feedback:
        ref = fb.get("finding_ref", "")
        fb_type = fb.get("feedback_type", "confirmed")
        for sid in _resolve_slide_ids(ref):
            slide_findings.setdefault(sid, []).append(fb_type)

    decisions = {}
    for sid, types in slide_findings.items():
        if types and all(t == "disputed" for t in types):
            decisions[sid] = "remove"
    return decisions


def feedback_to_key_message_overrides(feedback: list[dict]) -> dict[str, str]:
    """Extract key_message overrides from 'modified' feedback on *_key_message refs.

    Returns dict mapping look_name -> new key_message value.
    """
    overrides = {}
    for fb in feedback:
        ref = fb.get("finding_ref", "")
        if ref.endswith("_key_message") and fb.get("feedback_type") == "modified":
            user_val = fb.get("user_value", "")
            if user_val:
                # "trends_key_message" -> "trends"
                look = ref.replace("_key_message", "")
                overrides[look] = user_val
    return overrides
