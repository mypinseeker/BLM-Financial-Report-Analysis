"""Tests for MD generator final-mode feedback filtering."""
import pytest
from unittest.mock import MagicMock
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Minimal FiveLooksResult stub
# ---------------------------------------------------------------------------

@dataclass
class _Stub:
    """Generic attribute holder for test stubs."""
    _data: dict = field(default_factory=dict, repr=False)

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        return self._data.get(name)


def _make_result():
    """Build a minimal FiveLooksResult-like object for testing."""
    r = _Stub(_data={
        "target_operator": "vodafone_germany",
        "market": "germany",
        "analysis_period": "CQ4_2025",
        "provenance": None,
        "tariff_analysis": None,

        "trends": _Stub(_data={
            "pest": _Stub(_data={
                "political_factors": [
                    _Stub(_data={"factor_name": "Spectrum Reg", "current_status": "Strict",
                                  "impact_type": "threat", "severity": "high",
                                  "trend_direction": "stable", "time_horizon": "medium_term"}),
                    _Stub(_data={"factor_name": "EU DMA", "current_status": "Pending",
                                  "impact_type": "opportunity", "severity": "medium",
                                  "trend_direction": "intensifying", "time_horizon": "long_term"}),
                ],
                "economic_factors": [
                    _Stub(_data={"factor_name": "Inflation", "current_status": "High CPI",
                                  "impact_type": "threat", "severity": "medium"}),
                ],
                "society_factors": [],
                "technology_factors": [
                    _Stub(_data={"factor_name": "5G Rollout", "current_status": "Accelerating",
                                  "impact_type": "opportunity", "severity": "high"}),
                ],
                "overall_weather": "mixed",
                "weather_explanation": "Regulatory headwinds offset by tech tailwinds",
                "policy_opportunities": [],
                "policy_threats": [],
            }),
            "industry_market_size": "€50B",
            "industry_growth_rate": "+1.2%",
            "industry_lifecycle_stage": "mature",
            "industry_concentration": "Oligopoly",
            "key_success_factors": [],
            "value_transfer_trends": [],
            "new_business_models": [],
            "technology_revolution": [],
            "key_message": "Mature market with regulatory headwinds.",
        }),

        "market_customer": _Stub(_data={
            "market_snapshot": {},
            "changes": [
                _Stub(_data={"change_type": "bundle", "description": "FMC growth",
                              "impact_type": "opportunity", "severity": "medium", "source": "analyst"}),
                _Stub(_data={"change_type": "pricing", "description": "MVNO pressure",
                              "impact_type": "threat", "severity": "high", "source": "market"}),
            ],
            "appeals_assessment": [],
            "customer_segments": [
                _Stub(_data={"segment_name": "Consumer Mobile", "segment_type": "consumer",
                              "growth_trend": "flat", "size_estimate": "", "our_share": ""}),
            ],
            "customer_value_migration": "",
            "opportunities": [],
            "threats": [],
            "market_outlook": "",
            "key_message": "Price competition intensifying.",
        }),

        "competition": _Stub(_data={
            "five_forces": {
                "existing_competitors": _Stub(_data={
                    "force_name": "Existing Competitors", "force_level": "high",
                    "key_factors": [], "implications": [],
                }),
            },
            "competitor_analyses": {
                "dt_germany": _Stub(_data={
                    "financial_health": {}, "subscriber_health": {},
                    "growth_strategy": "FMC convergence",
                    "strengths": [], "weaknesses": [],
                    "implications": [], "likely_future_actions": [],
                }),
            },
            "comparison_table": {},
            "competitive_landscape": "",
            "overall_competition_intensity": "high",
            "key_message": "DT dominates in FMC.",
        }),

        "self_analysis": _Stub(_data={
            "financial_health": {},
            "revenue_breakdown": {},
            "segment_analyses": [],
            "network": None,
            "bmc": None,
            "strengths": [],
            "weaknesses": [],
            "exposure_points": [
                _Stub(_data={"trigger_action": "Cable loss", "side_effect": "Churn",
                              "attack_vector": "Competitor", "severity": "high"}),
                _Stub(_data={"trigger_action": "Price war", "side_effect": "Margin drop",
                              "attack_vector": "Market", "severity": "medium"}),
            ],
            "management_commentary": [],
            "leadership_changes": [],
            "org_culture": "",
            "performance_gap": "",
            "opportunity_gap": "",
            "strategic_review": "",
            "health_rating": "stable",
            "key_message": "Strong mobile, weak fixed.",
        }),

        "swot": _Stub(_data={
            "strengths": ["Strong brand", "5G leadership", "Network reach"],
            "weaknesses": ["High debt", "Cable dependency"],
            "opportunities": ["FMC upsell", "B2B cloud"],
            "threats": ["Price war", "Regulatory fines"],
            "so_strategies": [],
            "wo_strategies": [],
            "st_strategies": [],
            "wt_strategies": [],
            "key_message": "Leverage 5G to offset cable weakness.",
        }),

        "opportunities": _Stub(_data={
            "span_positions": [
                _Stub(_data={"opportunity_name": "FMC Bundle", "quadrant": "grow_invest",
                              "market_attractiveness": 8.0, "competitive_position": 6.5,
                              "recommended_strategy": "Invest aggressively"}),
                _Stub(_data={"opportunity_name": "IoT Platform", "quadrant": "acquire_skills",
                              "market_attractiveness": 7.0, "competitive_position": 4.0,
                              "recommended_strategy": "Build capability"}),
            ],
            "grow_invest": ["FMC Bundle"],
            "acquire_skills": ["IoT Platform"],
            "harvest": [],
            "avoid_exit": [],
            "opportunities": [],
            "window_opportunities": [],
            "key_message": "FMC is the top priority.",
        }),

        "three_decisions": None,
    })
    return r


# ======================================================================
# TestMdFinalMode
# ======================================================================

class TestMdFinalMode:
    def test_draft_mode_default(self):
        from src.output.md_generator import BLMMdGenerator
        gen = BLMMdGenerator()
        md = gen.generate(_make_result())
        assert "Strong brand" in md
        assert "5G leadership" in md
        assert "Network reach" in md
        assert "**Final**" not in md

    def test_final_mode_footer(self):
        from src.output.md_generator import BLMMdGenerator
        gen = BLMMdGenerator()
        md = gen.generate(_make_result(), mode="final")
        assert "**Final** report incorporating user feedback" in md

    def test_final_mode_removes_disputed_strength(self):
        from src.output.md_generator import BLMMdGenerator
        gen = BLMMdGenerator()
        feedback = [
            {"look_category": "swot", "finding_ref": "strength_1",
             "feedback_type": "disputed"},
        ]
        md = gen.generate(_make_result(), mode="final", feedback=feedback)
        # "Strong brand" (index 0) and "Network reach" (index 2) should remain
        assert "Strong brand" in md
        assert "Network reach" in md
        # "5G leadership" (index 1) should be removed
        assert "5G leadership" not in md

    def test_final_mode_modifies_strength(self):
        from src.output.md_generator import BLMMdGenerator
        gen = BLMMdGenerator()
        feedback = [
            {"look_category": "swot", "finding_ref": "strength_0",
             "feedback_type": "modified", "user_value": "Premium brand positioning"},
        ]
        md = gen.generate(_make_result(), mode="final", feedback=feedback)
        assert "Premium brand positioning" in md
        assert "User Modified" in md

    def test_final_mode_supplements_threat(self):
        from src.output.md_generator import BLMMdGenerator
        gen = BLMMdGenerator()
        feedback = [
            {"look_category": "swot", "finding_ref": "threat_0",
             "feedback_type": "supplemented", "user_comment": "Expected in H2"},
        ]
        md = gen.generate(_make_result(), mode="final", feedback=feedback)
        assert "Expected in H2" in md
        assert "Price war" in md

    def test_final_mode_removes_disputed_pest_factor(self):
        from src.output.md_generator import BLMMdGenerator
        gen = BLMMdGenerator()
        feedback = [
            {"look_category": "trends", "finding_ref": "pest_political_0",
             "feedback_type": "disputed"},
        ]
        md = gen.generate(_make_result(), mode="final", feedback=feedback)
        # "Spectrum Reg" should be removed, "EU DMA" should remain
        assert "Spectrum Reg" not in md
        assert "EU DMA" in md

    def test_final_mode_removes_disputed_exposure(self):
        from src.output.md_generator import BLMMdGenerator
        gen = BLMMdGenerator()
        feedback = [
            {"look_category": "self", "finding_ref": "exposure_0",
             "feedback_type": "disputed"},
        ]
        md = gen.generate(_make_result(), mode="final", feedback=feedback)
        assert "Cable loss" not in md
        assert "Price war" in md  # exposure_1 should remain

    def test_final_mode_removes_disputed_span(self):
        from src.output.md_generator import BLMMdGenerator
        gen = BLMMdGenerator()
        feedback = [
            {"look_category": "opportunity", "finding_ref": "span_0",
             "feedback_type": "disputed"},
        ]
        md = gen.generate(_make_result(), mode="final", feedback=feedback)
        # SPAN Position Details table should not contain FMC Bundle
        # (it may still appear in grow_invest quadrant detail — that's OK)
        span_section = md.split("SPAN Position Details")[1].split("---")[0] if "SPAN Position Details" in md else ""
        assert "FMC Bundle" not in span_section
        assert "IoT Platform" in md

    def test_no_feedback_equals_draft(self):
        from src.output.md_generator import BLMMdGenerator
        gen = BLMMdGenerator()
        draft = gen.generate(_make_result(), mode="draft")
        final_no_fb = gen.generate(_make_result(), mode="final", feedback=[])
        # Final with empty feedback should have same content + footer
        assert "**Final**" in final_no_fb
        # Both should have all findings
        assert "Strong brand" in draft
        assert "Strong brand" in final_no_fb

    def test_final_mode_removes_disputed_market_change(self):
        from src.output.md_generator import BLMMdGenerator
        gen = BLMMdGenerator()
        feedback = [
            {"look_category": "market", "finding_ref": "market_change_1",
             "feedback_type": "disputed"},
        ]
        md = gen.generate(_make_result(), mode="final", feedback=feedback)
        assert "FMC growth" in md
        assert "MVNO pressure" not in md
