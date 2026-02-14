"""Tests for FindingExtractor, feedback_to_ppt_decisions, and filter_findings_by_feedback."""
import pytest

from src.web.services.finding_extractor import (
    FindingExtractor,
    feedback_to_ppt_decisions,
    feedback_to_key_message_overrides,
)
from src.output.md_utils import filter_findings_by_feedback


# ---------------------------------------------------------------------------
# Sample JSON fixture (simplified from BLMJsonExporter output)
# ---------------------------------------------------------------------------

SAMPLE_JSON = {
    "meta": {"target_operator": "vodafone_germany", "market": "germany"},
    "five_looks": {
        "trends": {
            "pest": {
                "political_factors": [
                    {"factor_name": "Spectrum Regulation", "current_status": "Strict", "impact_type": "threat"},
                    {"factor_name": "EU Digital Markets Act", "current_status": "Pending", "impact_type": "opportunity"},
                ],
                "economic_factors": [
                    {"factor_name": "Inflation Pressure", "current_status": "High CPI", "impact_type": "threat"},
                ],
                "society_factors": [],
                "technology_factors": [
                    {"factor_name": "5G Rollout", "current_status": "Accelerating", "impact_type": "opportunity"},
                ],
            },
            "key_message": "Mature market with regulatory headwinds.",
        },
        "market_customer": {
            "changes": [
                {"description": "FMC bundle growth", "impact_type": "opportunity"},
                {"description": "MVNO price pressure", "impact_type": "threat"},
            ],
            "appeals_assessment": [
                {"dimension_name": "Price", "our_score": 6.5},
                {"dimension_name": "Performance", "our_score": 8.0},
            ],
            "customer_segments": [
                {"segment_name": "Consumer Mobile", "growth_trend": "flat"},
            ],
            "key_message": "Price competition intensifying.",
        },
        "competition": {
            "five_forces": {
                "existing_competitors": {"force_name": "Existing Competitors", "force_level": "high"},
                "new_entrants": {"force_name": "New Entrants", "force_level": "low"},
            },
            "competitor_analyses": {
                "dt_germany": {"growth_strategy": "FMC convergence"},
            },
            "key_message": "DT dominates in FMC.",
        },
        "self_analysis": {
            "segment_analyses": [
                {"segment_name": "Mobile", "health_status": "stable"},
                {"segment_name": "Fixed", "health_status": "growing"},
            ],
            "network": {"investment_direction": "5G expansion"},
            "exposure_points": [
                {"trigger_action": "Cable share loss", "side_effect": "Churn increase"},
            ],
            "key_message": "Strong mobile, weak fixed.",
        },
        "swot": {
            "strengths": ["Strong brand", "5G leadership"],
            "weaknesses": ["High debt", "Cable dependency"],
            "opportunities": ["FMC upsell", "B2B cloud"],
            "threats": ["Price war", "Regulatory fines"],
        },
        "opportunities": {
            "span_positions": [
                {"opportunity_name": "FMC Bundle", "quadrant": "grow_invest"},
                {"opportunity_name": "IoT Platform", "quadrant": "acquire_skills"},
            ],
            "key_message": "FMC is the top priority.",
        },
    },
}


# ======================================================================
# TestFindingExtractor
# ======================================================================

class TestFindingExtractor:
    def setup_method(self):
        self.extractor = FindingExtractor()
        self.findings = self.extractor.extract_all(SAMPLE_JSON)

    def test_all_six_categories_present(self):
        expected = {"trends", "market", "competition", "self", "swot", "opportunity"}
        assert set(self.findings.keys()) == expected

    def test_trends_findings(self):
        trends = self.findings["trends"]
        refs = [f["finding_ref"] for f in trends]
        assert "pest_political_0" in refs
        assert "pest_political_1" in refs
        assert "pest_economic_0" in refs
        assert "pest_technology_0" in refs
        assert "trends_key_message" in refs
        # No social factors — so no pest_social_*
        assert not any(r.startswith("pest_social_") for r in refs)

    def test_market_findings(self):
        market = self.findings["market"]
        refs = [f["finding_ref"] for f in market]
        assert "market_change_0" in refs
        assert "market_change_1" in refs
        assert "appeals_price" in refs
        assert "appeals_performance" in refs
        assert "segment_0" in refs
        assert "market_key_message" in refs

    def test_competition_findings(self):
        comp = self.findings["competition"]
        refs = [f["finding_ref"] for f in comp]
        assert "porter_existing_competitors" in refs
        assert "porter_new_entrants" in refs
        assert "competitor_dt_germany" in refs
        assert "competition_key_message" in refs

    def test_self_findings(self):
        self_f = self.findings["self"]
        refs = [f["finding_ref"] for f in self_f]
        assert "self_segment_mobile" in refs
        assert "self_segment_fixed" in refs
        assert "network_analysis" in refs
        assert "exposure_0" in refs
        assert "self_key_message" in refs

    def test_swot_findings(self):
        swot = self.findings["swot"]
        refs = [f["finding_ref"] for f in swot]
        assert "strength_0" in refs
        assert "strength_1" in refs
        assert "weakness_0" in refs
        assert "swot_opportunity_0" in refs
        assert "threat_0" in refs

    def test_opportunity_findings(self):
        opp = self.findings["opportunity"]
        refs = [f["finding_ref"] for f in opp]
        assert "span_0" in refs
        assert "span_1" in refs
        assert "opportunity_key_message" in refs

    def test_empty_json(self):
        findings = self.extractor.extract_all({})
        for cat in findings.values():
            assert cat == []

    def test_findings_have_label_and_value(self):
        for cat, items in self.findings.items():
            for f in items:
                assert "finding_ref" in f
                assert "label" in f
                assert "value" in f
                assert "section" in f


# ======================================================================
# TestFeedbackToPptDecisions
# ======================================================================

class TestFeedbackToPptDecisions:
    def test_all_disputed_removes_slide(self):
        feedback = [
            {"finding_ref": "strength_0", "feedback_type": "disputed"},
            {"finding_ref": "weakness_0", "feedback_type": "disputed"},
            {"finding_ref": "swot_opportunity_0", "feedback_type": "disputed"},
            {"finding_ref": "threat_0", "feedback_type": "disputed"},
        ]
        decisions = feedback_to_ppt_decisions(feedback)
        assert decisions.get("swot") == "remove"

    def test_partial_disputed_keeps_slide(self):
        feedback = [
            {"finding_ref": "strength_0", "feedback_type": "disputed"},
            {"finding_ref": "weakness_0", "feedback_type": "confirmed"},
        ]
        decisions = feedback_to_ppt_decisions(feedback)
        assert "swot" not in decisions

    def test_modified_keeps_slide(self):
        feedback = [
            {"finding_ref": "pest_political_0", "feedback_type": "modified",
             "user_value": "Updated regulation"},
        ]
        decisions = feedback_to_ppt_decisions(feedback)
        assert "pest_dashboard" not in decisions

    def test_empty_feedback(self):
        assert feedback_to_ppt_decisions([]) == {}

    def test_key_message_overrides(self):
        feedback = [
            {"finding_ref": "trends_key_message", "feedback_type": "modified",
             "user_value": "Market is shifting to 5G."},
            {"finding_ref": "market_key_message", "feedback_type": "confirmed"},
        ]
        overrides = feedback_to_key_message_overrides(feedback)
        assert overrides == {"trends": "Market is shifting to 5G."}

    def test_key_message_overrides_empty(self):
        feedback = [
            {"finding_ref": "trends_key_message", "feedback_type": "confirmed"},
        ]
        assert feedback_to_key_message_overrides(feedback) == {}


# ======================================================================
# TestFilterFindingsByFeedback
# ======================================================================

class TestFilterFindingsByFeedback:
    def test_disputed_removed(self):
        items = ["Strong brand", "5G leadership", "Network reach"]
        feedback = [
            {"finding_ref": "strength_1", "feedback_type": "disputed"},
        ]
        result = filter_findings_by_feedback(items, "strength_", feedback)
        assert result == ["Strong brand", "Network reach"]

    def test_modified_replaced(self):
        items = ["Strong brand", "5G leadership"]
        feedback = [
            {"finding_ref": "strength_0", "feedback_type": "modified",
             "user_value": "Premium brand positioning"},
        ]
        result = filter_findings_by_feedback(items, "strength_", feedback)
        assert result[0] == "Premium brand positioning [User Modified]"
        assert result[1] == "5G leadership"

    def test_supplemented_annotated(self):
        items = ["Strong brand", "5G leadership"]
        feedback = [
            {"finding_ref": "strength_0", "feedback_type": "supplemented",
             "user_comment": "Also regional strength"},
        ]
        result = filter_findings_by_feedback(items, "strength_", feedback)
        assert "Also regional strength" in result[0]
        assert result[1] == "5G leadership"

    def test_confirmed_unchanged(self):
        items = ["Strong brand"]
        feedback = [
            {"finding_ref": "strength_0", "feedback_type": "confirmed"},
        ]
        result = filter_findings_by_feedback(items, "strength_", feedback)
        assert result == ["Strong brand"]

    def test_no_feedback_passthrough(self):
        items = ["a", "b", "c"]
        assert filter_findings_by_feedback(items, "x_", None) == items
        assert filter_findings_by_feedback(items, "x_", []) == items

    def test_dict_items_modified(self):
        items = [{"factor_name": "Regulation", "severity": "high"}]
        feedback = [
            {"finding_ref": "pest_political_0", "feedback_type": "modified",
             "user_value": "Regulation eased"},
        ]
        result = filter_findings_by_feedback(items, "pest_political_", feedback)
        assert result[0]["_user_modified"] is True
        assert result[0]["_user_value"] == "Regulation eased"

    def test_dict_items_supplemented(self):
        items = [{"factor_name": "Inflation"}]
        feedback = [
            {"finding_ref": "f_0", "feedback_type": "supplemented",
             "user_comment": "Easing in Q1"},
        ]
        result = filter_findings_by_feedback(items, "f_", feedback)
        assert result[0]["_user_note"] == "Easing in Q1"

    def test_empty_items(self):
        assert filter_findings_by_feedback([], "x_", [{"finding_ref": "x_0"}]) == []
