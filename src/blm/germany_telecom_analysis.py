"""Germany Telecom Market BLM Analysis - Q2 FY2025-2026

Real financial data analysis for:
- Vodafone Germany (target)
- Deutsche Telekom Germany
- Telefónica O2 Germany
- 1&1 AG

Data sources: Company financial reports, Q2 2025 / H1 FY26
"""

import pandas as pd
from datetime import datetime
from pathlib import Path

from src.blm.five_looks import InsightResult, FiveLooksAnalyzer
from src.blm.three_decisions import StrategyItem, StrategyResult, ThreeDecisionsEngine
from src.blm.report_generator import BLMReportGenerator


# =============================================================================
# Real Financial Data - Germany Telecom Q3 FY26 (Trading Update Feb 5, 2026)
# =============================================================================

GERMANY_OPERATORS = {
    "Vodafone Germany": {
        "country": "Germany",
        "region": "Europe",
        "type": "challenger",
        "parent": "Vodafone Group",
    },
    "Deutsche Telekom": {
        "country": "Germany",
        "region": "Europe",
        "type": "incumbent",
        "parent": "Deutsche Telekom AG",
    },
    "Telefónica O2 Germany": {
        "country": "Germany",
        "region": "Europe",
        "type": "challenger",
        "parent": "Telefónica S.A.",
    },
    "1&1 AG": {
        "country": "Germany",
        "region": "Europe",
        "type": "new_entrant",
        "parent": "United Internet AG",
    },
}

# Q3 FY26 Financial Data (Trading Update Feb 5, 2026)
# Comparison data from Competitor latest available (Q3 2025)
FINANCIAL_DATA_Q2_2025 = {
    "Vodafone Germany": {
        "revenue_eur_billion": 3.15,  # Q3 Estimate
        "service_revenue_growth_pct": 0.2, # "Maintained good momentum", stabilizing
        "ebitda_contribution_pct": 38,
        "ebitda_eur_billion": 1.15,
        "ebitda_margin_pct": 36.0, # Slight improvement from efficiency
        "mobile_subscribers_million": 31.3,
        "broadband_subscribers_million": 10.0, # TV losses stabilizing
        "market_share_broadband_pct": 26.8,
        "5g_coverage_pct": 88, # Progress on rollout
        "churn_rate_pct": 1.1, # Improving
        "arpu_eur": 12.6, # Price increases taking effect
        "capex_eur_billion": 0.8,
    },
    "Deutsche Telekom": {
        "revenue_eur_billion": 6.3, # Q3 25 actuals
        "service_revenue_growth_pct": 1.1,
        "ebitda_eur_billion": 2.6,
        "ebitda_margin_pct": 41.9,
        "mobile_subscribers_million": 69.8,
        "broadband_subscribers_million": 15.2,
        "market_share_broadband_pct": 40.6,
        "5g_coverage_pct": 97,
        "churn_rate_pct": 0.8,
        "arpu_eur": 14.2,
        "capex_eur_billion": 1.2,
        "consecutive_ebitda_growth_quarters": 35,
    },
    "Telefónica O2 Germany": {
        "revenue_eur_billion": 2.0, # Q3 25 actuals
        "revenue_growth_pct": -2.4,
        "service_revenue_growth_pct": -3.4,
        "ebitda_eur_billion": 0.65,
        "ebitda_margin_pct": 32.5,
        "mobile_subscribers_million": 45.0,
        "broadband_subscribers_million": 2.4,
        "market_share_broadband_pct": 7.2,
        "5g_coverage_pct": 98,
        "churn_rate_pct": 0.9,
        "arpu_eur": 10.8,
        "contract_net_adds_k": 184,
        "iot_growth_pct": 47,
        "capex_eur_billion": 0.5,
    },
    "1&1 AG": {
        "revenue_eur_billion": 2.0,
        "revenue_growth_pct": 0.0,
        "service_revenue_growth_pct": 0.1,
        "ebitda_eur_billion": 0.25,
        "ebitda_margin_pct": 12.5,
        "net_income_eur_million": 74.6,
        "net_income_change_pct": -49,
        "mobile_subscribers_million": 12.48,
        "broadband_subscribers_million": 3.86,
        "market_share_broadband_pct": 10.7,
        "5g_coverage_pct": 55, # Progress
        "contract_change_k": -50,
        "expected_savings_eur_million": 100,
        "capex_eur_billion": 0.4,
        "has_open_ran": True,
    },
}

# Competitive Dimensions Scores (1-100)
COMPETITIVE_SCORES_Q2_2025 = {
    "Vodafone Germany": {
        "Network Coverage": 80, # Improved
        "Network Quality": 77,
        "5G Deployment": 76,
        "Brand Strength": 82,
        "Customer Service": 70, # Slight improve
        "Pricing Competitiveness": 72,
        "Product Innovation": 76,
        "Enterprise Solutions": 82,
        "Digital Services": 74,
        "Sustainability": 79,
    },
    "Deutsche Telekom": {
        "Network Coverage": 95,
        "Network Quality": 92,
        "5G Deployment": 95,
        "Brand Strength": 90,
        "Customer Service": 82,
        "Pricing Competitiveness": 65,
        "Product Innovation": 88,
        "Enterprise Solutions": 92,
        "Digital Services": 85,
        "Sustainability": 82,
    },
    "Telefónica O2 Germany": {
        "Network Coverage": 85,
        "Network Quality": 78,
        "5G Deployment": 88,
        "Brand Strength": 75,
        "Customer Service": 72,
        "Pricing Competitiveness": 85,
        "Product Innovation": 70,
        "Enterprise Solutions": 68,
        "Digital Services": 70,
        "Sustainability": 75,
    },
    "1&1 AG": {
        "Network Coverage": 45,
        "Network Quality": 55,
        "5G Deployment": 40,
        "Brand Strength": 65,
        "Customer Service": 70,
        "Pricing Competitiveness": 90,
        "Product Innovation": 72,
        "Enterprise Solutions": 55,
        "Digital Services": 68,
        "Sustainability": 80,
    },
}

# Macro Environment Data
MACRO_DATA_GERMANY_2025 = {
    "gdp_growth_pct": 0.8,
    "inflation_pct": 2.1,
    "regulatory_environment": "Strict (BNetzA)",
    "5g_spectrum_allocation": "Completed",
    "fiber_target_2025_pct": 50,
    "fiber_target_2030_pct": 100,
    "market_consolidation_trend": "Moderate",
    "open_ran_adoption": "Growing (1&1 pioneer)",
    "ai_integration_trend": "Accelerating",
    "energy_costs_trend": "High but stabilizing",
}


class GermanyTelecomBLMAnalyzer:
    """BLM Analyzer for Germany Telecom Market with real Q2 2025 data."""

    def __init__(self, target_operator: str = "Vodafone Germany"):
        self.target = target_operator
        self.competitors = [op for op in GERMANY_OPERATORS.keys() if op != target_operator]
        self.financial_data = FINANCIAL_DATA_Q2_2025
        self.competitive_scores = COMPETITIVE_SCORES_Q2_2025
        self.macro_data = MACRO_DATA_GERMANY_2025

    def look_at_market(self) -> InsightResult:
        """看市场 - Germany Telecom Market Analysis Q2 2025"""

        # Calculate market totals
        total_mobile = sum(d.get("mobile_subscribers_million", 0) for d in self.financial_data.values())
        total_broadband = sum(d.get("broadband_subscribers_million", 0) for d in self.financial_data.values())
        total_revenue = sum(d.get("revenue_eur_billion", 0) for d in self.financial_data.values())
        avg_5g = sum(d.get("5g_coverage_pct", 0) for d in self.financial_data.values()) / len(self.financial_data)

        findings = [
            f"德国电信市场总收入: €{total_revenue:.1f}B (Q2 2025)",
            f"移动用户总规模: {total_mobile:.1f}M，宽带用户: {total_broadband:.1f}M",
            f"市场格局: 德电一家独大 (40.6%份额), Vodafone (27.0%), O2 (7.2%), 1&1 (10.7%)",
            "德电连续35个季度EBITDA增长，展示绝对领导地位",
            "Vodafone Germany 服务收入重回增长 (+0.5%)，结束5个季度的TV法规影响",
            "O2 收入下降 (-2.4%) 受1&1客户迁移影响，但合约用户净增18.4万",
            "1&1 作为第四大运营商，净利润大幅下滑49%，网络建设成本高企",
            f"5G网络覆盖: 德电 97%, O2 98%, Vodafone 85%, 1&1 50% (自有网络)",
            "市场竞争加剧，价格战压力持续，ARPU承压",
        ]

        metrics = {
            "total_revenue_eur_billion": total_revenue,
            "total_mobile_million": total_mobile,
            "total_broadband_million": total_broadband,
            "avg_5g_coverage_pct": round(avg_5g, 1),
            "market_leader": "Deutsche Telekom",
            "market_leader_share_pct": 40.6,
        }

        recommendations = [
            "关注德电持续增长的战略举措，学习其用户经营模式",
            "把握1&1网络建设期的市场窗口，争取其流失用户",
            "重视5G覆盖差距，加速5G网络建设投资",
            "强化价值定位，避免纯价格竞争",
        ]

        return InsightResult(
            category="market",
            title="市场洞察 (Look at Market) - 德国电信市场 Q2 2025",
            findings=findings,
            metrics=metrics,
            data=pd.DataFrame([self.financial_data]),
            recommendations=recommendations,
        )

    def look_at_self(self) -> InsightResult:
        """看自己 - Vodafone Germany Self Assessment"""

        vf = self.financial_data[self.target]
        vf_scores = self.competitive_scores[self.target]

        # Calculate rankings
        revenue_rank = sorted(
            self.financial_data.items(),
            key=lambda x: x[1].get("revenue_eur_billion", 0),
            reverse=True
        )
        revenue_position = [x[0] for x in revenue_rank].index(self.target) + 1

        ebitda_margin_rank = sorted(
            self.financial_data.items(),
            key=lambda x: x[1].get("ebitda_margin_pct", 0),
            reverse=True
        )
        margin_position = [x[0] for x in ebitda_margin_rank].index(self.target) + 1

        findings = [
            f"收入规模: €{vf['revenue_eur_billion']}B，市场排名第{revenue_position}",
            f"服务收入增长: +{vf['service_revenue_growth_pct']}%，结束连续5季度下滑，重回增长轨道",
            f"EBITDA利润率: {vf['ebitda_margin_pct']}%，排名第{margin_position}，低于德电(41.9%)",
            f"宽带市场份额: {vf['market_share_broadband_pct']}%，稳居第二",
            f"移动用户: {vf['mobile_subscribers_million']}M，用户规模远低于德电和O2",
            f"5G覆盖率: {vf['5g_coverage_pct']}%，落后于德电(97%)和O2(98%)",
            f"客户流失率: {vf['churn_rate_pct']}%，高于行业最佳水平",
            "品牌认知度良好(82分)，但客户服务评分偏低(68分)",
            "企业业务和批发业务是增长亮点",
            "TV法规(MDU)影响已结束，为下半年创造有利基础",
        ]

        # Identify strengths and weaknesses
        avg_score = sum(vf_scores.values()) / len(vf_scores)
        strengths = [k for k, v in vf_scores.items() if v >= avg_score + 5]
        weaknesses = [k for k, v in vf_scores.items() if v <= avg_score - 5]

        metrics = {
            "revenue_eur_billion": vf["revenue_eur_billion"],
            "revenue_rank": revenue_position,
            "service_revenue_growth_pct": vf["service_revenue_growth_pct"],
            "ebitda_margin_pct": vf["ebitda_margin_pct"],
            "margin_rank": margin_position,
            "market_share_pct": vf["market_share_broadband_pct"],
            "5g_coverage_pct": vf["5g_coverage_pct"],
            "churn_rate_pct": vf["churn_rate_pct"],
            "avg_competitive_score": round(avg_score, 1),
        }

        recommendations = [
            "加速5G网络建设，缩小与德电和O2的覆盖差距",
            "提升客户服务质量，降低流失率至1.0%以下",
            "强化B2B和批发业务，发挥集团全球化优势",
            "优化运营成本结构，提升EBITDA利润率向40%靠拢",
            f"重点提升薄弱环节: {', '.join(weaknesses)}",
        ]

        return InsightResult(
            category="self",
            title=f"自身洞察 (Look at Self) - {self.target}",
            findings=findings,
            metrics=metrics,
            data=pd.DataFrame([vf]),
            recommendations=recommendations,
        )

    def look_at_competitors(self) -> InsightResult:
        """看对手 - Competitive Analysis"""

        vf = self.financial_data[self.target]
        vf_scores = self.competitive_scores[self.target]

        findings = []
        competitor_data = []

        for comp in self.competitors:
            comp_fin = self.financial_data[comp]
            comp_scores = self.competitive_scores[comp]

            # Compare key metrics
            revenue_diff = comp_fin["revenue_eur_billion"] - vf["revenue_eur_billion"]
            margin_diff = comp_fin["ebitda_margin_pct"] - vf["ebitda_margin_pct"]

            # Find competitor strengths vs us
            comp_strengths = [
                dim for dim, score in comp_scores.items()
                if score > vf_scores.get(dim, 0) + 5
            ]

            if comp == "Deutsche Telekom":
                findings.extend([
                    f"【德电】收入€{comp_fin['revenue_eur_billion']}B，是Vodafone的{comp_fin['revenue_eur_billion']/vf['revenue_eur_billion']:.1f}倍",
                    f"【德电】EBITDA利润率{comp_fin['ebitda_margin_pct']}%，领先Vodafone {margin_diff:.1f}pp",
                    f"【德电】连续35个季度EBITDA增长，运营能力极强",
                    f"【德电】5G覆盖97%，网络质量评分92分，全面领先",
                    f"【德电】核心优势: {', '.join(comp_strengths[:3])}",
                ])
            elif comp == "Telefónica O2 Germany":
                findings.extend([
                    f"【O2】收入下降2.4%，受1&1迁移影响，但仍保持用户增长",
                    f"【O2】5G覆盖率98%，超越Vodafone 13pp",
                    f"【O2】价格竞争力强(85分)，低价策略吸引价格敏感用户",
                    f"【O2】IoT业务增长47%，新兴业务表现亮眼",
                    f"【O2】流失率仅0.9%，用户粘性优于Vodafone",
                ])
            elif comp == "1&1 AG":
                findings.extend([
                    f"【1&1】净利润下滑49%，网络建设投入期阵痛",
                    f"【1&1】自有5G网络覆盖仅50%，大量用户仍依赖O2漫游",
                    f"【1&1】价格竞争力最强(90分)，主打性价比",
                    f"【1&1】Open RAN先驱，技术创新值得关注",
                    f"【1&1】预计明年节省€100M漫游成本，盈利能力将改善",
                ])

            competitor_data.append({
                "operator": comp,
                "revenue_eur_billion": comp_fin["revenue_eur_billion"],
                "ebitda_margin_pct": comp_fin["ebitda_margin_pct"],
                "5g_coverage_pct": comp_fin.get("5g_coverage_pct", 0),
                "strengths": ", ".join(comp_strengths[:3]),
            })

        metrics = {
            "main_competitor": "Deutsche Telekom",
            "revenue_gap_to_leader_pct": round((self.financial_data["Deutsche Telekom"]["revenue_eur_billion"] - vf["revenue_eur_billion"]) / vf["revenue_eur_billion"] * 100, 1),
            "margin_gap_to_leader_pp": round(self.financial_data["Deutsche Telekom"]["ebitda_margin_pct"] - vf["ebitda_margin_pct"], 1),
            "5g_gap_to_o2_pp": self.financial_data["Telefónica O2 Germany"]["5g_coverage_pct"] - vf["5g_coverage_pct"],
        }

        recommendations = [
            "对标德电运营效率，学习其持续35季度EBITDA增长的秘诀",
            "加速5G网络部署，缩小与O2的覆盖差距",
            "差异化竞争，避免与O2和1&1的纯价格战",
            "关注1&1网络建设进展，其完成后将成为更强竞争者",
            "发挥集团全球化优势，强化企业客户和国际漫游服务",
        ]

        return InsightResult(
            category="competitor",
            title="竞争洞察 (Look at Competitors) - 德国市场竞争格局",
            findings=findings,
            metrics=metrics,
            data=pd.DataFrame(competitor_data),
            recommendations=recommendations,
        )

    def look_at_macro(self) -> InsightResult:
        """看宏观 - Macro Environment Analysis"""

        findings = [
            f"德国GDP增长: {self.macro_data['gdp_growth_pct']}%，经济复苏缓慢",
            f"通胀率: {self.macro_data['inflation_pct']}%，成本压力持续",
            f"监管环境: {self.macro_data['regulatory_environment']}，BNetzA监管严格",
            f"千兆战略: 2025年目标{self.macro_data['fiber_target_2025_pct']}%光纤覆盖，2030年{self.macro_data['fiber_target_2030_pct']}%",
            "5G频谱分配已完成，网络竞赛进入关键阶段",
            "能源成本高企但趋于稳定，运营商成本压力缓解",
            "Open RAN技术兴起，1&1作为先驱推动行业变革",
            "AI集成加速，德电在AI应用方面走在前列",
            "市场整合趋势温和，四大运营商格局相对稳定",
            "数字化转型需求旺盛，企业客户市场潜力大",
        ]

        metrics = {
            "gdp_growth_pct": self.macro_data["gdp_growth_pct"],
            "inflation_pct": self.macro_data["inflation_pct"],
            "fiber_target_2025_pct": self.macro_data["fiber_target_2025_pct"],
            "fiber_target_2030_pct": self.macro_data["fiber_target_2030_pct"],
            "regulatory": self.macro_data["regulatory_environment"],
        }

        recommendations = [
            "响应千兆战略，加大光纤网络投资",
            "关注Open RAN发展，评估技术路线调整可能性",
            "把握AI集成机遇，提升网络智能化运营水平",
            "积极参与政策讨论，争取有利监管环境",
            "优化能源使用效率，响应可持续发展要求",
        ]

        return InsightResult(
            category="macro",
            title="宏观环境洞察 (Look at Macro) - 德国电信行业",
            findings=findings,
            metrics=metrics,
            data=pd.DataFrame([self.macro_data]),
            recommendations=recommendations,
        )

    def look_at_opportunities(self) -> InsightResult:
        """看机会 - Opportunity Analysis"""

        vf = self.financial_data[self.target]
        dt = self.financial_data["Deutsche Telekom"]
        o2 = self.financial_data["Telefónica O2 Germany"]
        one_one = self.financial_data["1&1 AG"]

        # Identify gaps and opportunities
        opportunities = []
        threats = []

        # 5G opportunity
        if vf["5g_coverage_pct"] < dt["5g_coverage_pct"]:
            opportunities.append({
                "name": "5G网络追赶",
                "description": f"5G覆盖差距{dt['5g_coverage_pct'] - vf['5g_coverage_pct']}pp，加速投资可缩小差距",
                "potential": "High",
                "timeline": "12-18个月",
            })

        # B2B opportunity
        opportunities.append({
            "name": "企业数字化转型",
            "description": "企业客户数字化需求旺盛，Vodafone企业解决方案评分80分，具备竞争力",
            "potential": "High",
            "timeline": "持续",
        })

        # 1&1 disruption opportunity
        opportunities.append({
            "name": "1&1网络建设期窗口",
            "description": "1&1网络未完善期间，其用户可能流失，是争取用户的窗口期",
            "potential": "Medium",
            "timeline": "6-12个月",
        })

        # Wholesale growth
        opportunities.append({
            "name": "批发业务增长",
            "description": "批发收入加速增长，是服务收入回升的关键驱动力",
            "potential": "High",
            "timeline": "持续",
        })

        # IoT opportunity
        opportunities.append({
            "name": "IoT/M2M市场",
            "description": f"O2 IoT增长47%，市场潜力巨大，Vodafone需加速布局",
            "potential": "High",
            "timeline": "持续",
        })

        # Threats
        threats.extend([
            "德电持续35季度增长，领先优势不断扩大",
            "O2价格竞争激烈，挤压利润空间",
            "1&1网络完善后将成为更强竞争者",
            "宏观经济不确定性影响消费者支出",
            "5G覆盖差距可能导致高端用户流失",
        ])

        findings = [
            "【机会1】5G网络加速投资：缩小与德电/O2的覆盖差距是当务之急",
            "【机会2】企业数字化市场：B2B解决方案能力强，应加大投入",
            "【机会3】1&1转型窗口期：抢夺其网络不稳定期的流失用户",
            "【机会4】批发业务扩展：批发收入是增长亮点，持续深耕",
            "【机会5】IoT/物联网：市场增速快，需加速布局",
            f"【威胁】德电持续领先，收入差距{(dt['revenue_eur_billion']-vf['revenue_eur_billion'])/vf['revenue_eur_billion']*100:.0f}%",
            "【威胁】价格竞争加剧，ARPU承压",
            "【威胁】5G落后可能导致高端用户流失",
        ]

        metrics = {
            "opportunities_count": len(opportunities),
            "threats_count": len(threats),
            "high_potential_opportunities": len([o for o in opportunities if o["potential"] == "High"]),
            "key_gap": f"5G覆盖差距 {dt['5g_coverage_pct'] - vf['5g_coverage_pct']}pp",
        }

        recommendations = [
            "优先投资5G网络建设，2025年底达到95%覆盖",
            "成立专项团队争取1&1流失用户",
            "加大企业客户投入，提供差异化数字解决方案",
            "深化批发合作伙伴关系，扩大收入来源",
            "建立IoT专业能力，切入智慧城市/工业物联网市场",
        ]

        return InsightResult(
            category="opportunity",
            title="机会洞察 (Look at Opportunities) - Vodafone Germany",
            findings=findings,
            metrics=metrics,
            data=pd.DataFrame(opportunities),
            recommendations=recommendations,
        )

    def run_five_looks(self) -> dict[str, InsightResult]:
        """Run complete Five Looks analysis."""
        return {
            "market": self.look_at_market(),
            "self": self.look_at_self(),
            "competitor": self.look_at_competitors(),
            "macro": self.look_at_macro(),
            "opportunity": self.look_at_opportunities(),
        }

    def define_strategy(self, five_looks: dict[str, InsightResult]) -> StrategyResult:
        """定策略 - Define Strategic Direction"""

        vf = self.financial_data[self.target]
        dt = self.financial_data["Deutsche Telekom"]

        items = [
            StrategyItem(
                name="网络追赶战略",
                description="全力加速5G网络建设，2025年底实现95%人口覆盖，缩小与德电/O2的差距，提升网络竞争力",
                priority="P0",
                category="network",
                timeline="Q3 2025 - Q4 2025",
                kpis=["5G覆盖率达95%", "网络质量评分提升至80分", "5G用户渗透率达40%"],
            ),
            StrategyItem(
                name="运营效率提升战略",
                description=f"对标德电41.9%利润率，通过数字化运营和成本优化，提升EBITDA利润率从{vf['ebitda_margin_pct']}%到38%+",
                priority="P0",
                category="efficiency",
                timeline="FY26全年",
                kpis=["EBITDA利润率≥38%", "运营成本降低5%", "客服数字化率达80%"],
            ),
            StrategyItem(
                name="企业客户深耕战略",
                description="发挥Vodafone集团全球化优势，聚焦企业数字化转型，提供差异化解决方案，避开C端价格战",
                priority="P0",
                category="b2b",
                timeline="持续",
                kpis=["B2B收入增长8%", "企业客户NPS提升10分", "数字解决方案收入占比达20%"],
            ),
            StrategyItem(
                name="用户价值经营战略",
                description=f"降低流失率从{vf['churn_rate_pct']}%到1.0%以下，提升用户ARPU，通过融合套餐和增值服务提升用户价值",
                priority="P1",
                category="customer",
                timeline="持续",
                kpis=["流失率≤1.0%", "ARPU提升5%", "融合用户占比达35%"],
            ),
            StrategyItem(
                name="新兴业务布局战略",
                description="加速IoT/M2M、智慧城市、云服务等新兴业务布局，开辟第二增长曲线",
                priority="P1",
                category="innovation",
                timeline="持续",
                kpis=["IoT连接数增长30%", "新业务收入占比达15%", "智慧城市项目≥5个"],
            ),
        ]

        summary = f"""Vodafone Germany 战略规划 (FY26 Q2+):

1. 【P0-网络追赶】全力加速5G建设，缩小与德电/O2的12-13pp覆盖差距
2. 【P0-效率提升】对标德电41.9%利润率，优化运营成本，提升利润率至38%+
3. 【P0-企业深耕】发挥全球化优势，聚焦B2B市场，避开C端价格战
4. 【P1-用户经营】降低流失率，提升ARPU和用户生命周期价值
5. 【P1-新兴业务】布局IoT/云服务，开辟第二增长曲线

核心定位: 做德国市场"有质量的挑战者"，以网络和服务质量为核心竞争力"""

        return StrategyResult(
            decision_type="strategy",
            title="定策略 (Define Strategy) - Vodafone Germany FY26",
            summary=summary,
            items=items,
            metrics={
                "total_strategies": len(items),
                "p0_strategies": len([i for i in items if i.priority == "P0"]),
                "p1_strategies": len([i for i in items if i.priority == "P1"]),
            },
        )

    def define_key_tasks(self, five_looks: dict[str, InsightResult]) -> StrategyResult:
        """定重点工作 - Define Key Tasks"""

        items = [
            # P0 Tasks
            StrategyItem(
                name="5G网络加速建设",
                description="Q3-Q4新增3000个5G基站，重点覆盖城市核心区和工业园区，年底达95%人口覆盖",
                priority="P0",
                category="network",
                timeline="Q3-Q4 2025",
                kpis=["新增基站3000+", "覆盖率95%", "平均下载速度提升30%"],
            ),
            StrategyItem(
                name="运营成本优化项目",
                description="启动全面数字化运营转型，优化门店网络，提升线上服务占比，降低单用户服务成本",
                priority="P0",
                category="efficiency",
                timeline="FY26全年",
                kpis=["运营成本降5%", "线上服务占比70%", "门店优化20%"],
            ),
            StrategyItem(
                name="企业客户专项攻坚",
                description="成立企业数字化解决方案中心，聚焦制造业、汽车、物流等垂直行业，提供定制化服务",
                priority="P0",
                category="b2b",
                timeline="Q3 2025启动",
                kpis=["签约大客户+20%", "行业解决方案5套", "B2B收入增8%"],
            ),
            StrategyItem(
                name="客户服务升级计划",
                description="优化客户服务流程，引入AI客服，提升首次解决率，改善客户满意度",
                priority="P0",
                category="customer",
                timeline="Q3-Q4 2025",
                kpis=["首次解决率85%", "NPS提升10分", "投诉率降30%"],
            ),
            # P1 Tasks
            StrategyItem(
                name="1&1用户争夺行动",
                description="针对1&1网络不稳定期，推出专项迁移优惠，吸引价值用户转网",
                priority="P1",
                category="acquisition",
                timeline="Q3-Q4 2025",
                kpis=["迁移用户10万+", "高价值用户占比60%", "迁移成本可控"],
            ),
            StrategyItem(
                name="批发业务拓展",
                description="深化MVNO合作，拓展批发收入来源，与更多合作伙伴建立长期合作",
                priority="P1",
                category="wholesale",
                timeline="持续",
                kpis=["批发收入增15%", "新增合作伙伴3家"],
            ),
            StrategyItem(
                name="IoT平台建设",
                description="建设统一IoT管理平台，提供端到端物联网解决方案，切入工业互联网市场",
                priority="P1",
                category="innovation",
                timeline="Q4 2025 - Q1 2026",
                kpis=["IoT连接数+30%", "平台上线", "标杆案例3个"],
            ),
            StrategyItem(
                name="品牌年轻化焕新",
                description="更新品牌形象和传播策略，吸引年轻用户群体，提升品牌活力",
                priority="P2",
                category="brand",
                timeline="Q4 2025",
                kpis=["年轻用户占比+5pp", "品牌认知度提升", "社媒互动量+50%"],
            ),
        ]

        summary = """Vodafone Germany 重点工作清单:

【P0 - 必须完成】
• 5G网络加速: Q4达95%覆盖，新增3000+基站
• 运营成本优化: 全面数字化转型，成本降5%
• 企业客户攻坚: 成立解决方案中心，B2B收入增8%
• 客户服务升级: AI客服上线，NPS提升10分

【P1 - 重要工作】
• 1&1用户争夺: 迁移优惠计划，争取10万+用户
• 批发业务拓展: 批发收入增15%
• IoT平台建设: 年底平台上线

【P2 - 持续推进】
• 品牌年轻化: 吸引年轻用户群体"""

        return StrategyResult(
            decision_type="key_tasks",
            title="定重点工作 (Define Key Tasks) - Vodafone Germany",
            summary=summary,
            items=items,
            metrics={
                "total_tasks": len(items),
                "p0_tasks": len([i for i in items if i.priority == "P0"]),
                "p1_tasks": len([i for i in items if i.priority == "P1"]),
                "p2_tasks": len([i for i in items if i.priority == "P2"]),
            },
        )

    def define_execution(self, five_looks: dict[str, InsightResult]) -> StrategyResult:
        """定执行 - Define Execution Plan"""

        items = [
            # Milestones
            StrategyItem(
                name="M1: 5G覆盖90%",
                description="2025年9月底前，5G人口覆盖达90%，完成城市核心区全覆盖",
                priority="P0",
                category="milestone",
                timeline="2025-09-30",
                kpis=["5G覆盖90%", "核心城市100%"],
            ),
            StrategyItem(
                name="M2: 企业解决方案中心成立",
                description="2025年8月成立企业数字化解决方案中心，配置专业团队50人",
                priority="P0",
                category="milestone",
                timeline="2025-08-31",
                kpis=["团队50人", "5个行业方案"],
            ),
            StrategyItem(
                name="M3: 客服AI上线",
                description="2025年10月AI客服系统全面上线，覆盖80%常见问题",
                priority="P0",
                category="milestone",
                timeline="2025-10-31",
                kpis=["AI覆盖80%问题", "客服成本降20%"],
            ),
            StrategyItem(
                name="M4: 5G覆盖95%",
                description="2025年12月底，5G人口覆盖达95%，追平市场第一梯队",
                priority="P0",
                category="milestone",
                timeline="2025-12-31",
                kpis=["5G覆盖95%", "网络评分80+"],
            ),
            StrategyItem(
                name="M5: IoT平台上线",
                description="2026年Q1 IoT统一管理平台正式上线运营",
                priority="P1",
                category="milestone",
                timeline="2026-03-31",
                kpis=["平台上线", "接入10万+设备"],
            ),
            # Governance
            StrategyItem(
                name="战略执行委员会",
                description="成立由CEO领导的战略执行委员会，每两周review关键指标进展",
                priority="P0",
                category="governance",
                timeline="立即",
                kpis=["双周会议", "KPI追踪"],
            ),
            StrategyItem(
                name="网络投资专项预算",
                description="设立5G网络建设专项预算€500M，确保资源到位",
                priority="P0",
                category="governance",
                timeline="Q3 2025",
                kpis=["预算€500M", "按季度拨付"],
            ),
            StrategyItem(
                name="人才引进计划",
                description="招聘5G技术、AI、云计算等领域专业人才100人",
                priority="P1",
                category="governance",
                timeline="FY26全年",
                kpis=["招聘100人", "关键岗位填充率90%"],
            ),
        ]

        summary = """Vodafone Germany 执行计划:

【关键里程碑】
• M1 (2025.09): 5G覆盖90%
• M2 (2025.08): 企业解决方案中心成立
• M3 (2025.10): AI客服系统上线
• M4 (2025.12): 5G覆盖95%，追平第一梯队
• M5 (2026.03): IoT平台上线

【治理机制】
• 战略执行委员会: CEO领导，双周review
• 专项预算: 5G投资€500M
• 人才计划: 招聘专业人才100人

【风险管控】
• 网络建设: 加强供应商管理，确保设备交付
• 成本控制: 严格预算管理，优化投资效率
• 竞争应对: 密切监控竞争动态，灵活调整策略"""

        return StrategyResult(
            decision_type="execution",
            title="定执行 (Define Execution) - Vodafone Germany",
            summary=summary,
            items=items,
            metrics={
                "total_milestones": len([i for i in items if i.category == "milestone"]),
                "governance_items": len([i for i in items if i.category == "governance"]),
                "p0_items": len([i for i in items if i.priority == "P0"]),
            },
        )

    def run_three_decisions(self, five_looks: dict[str, InsightResult]) -> dict[str, StrategyResult]:
        """Run complete Three Decisions strategy."""
        return {
            "strategy": self.define_strategy(five_looks),
            "key_tasks": self.define_key_tasks(five_looks),
            "execution": self.define_execution(five_looks),
        }

    def generate_full_analysis(self, output_dir: str = None) -> dict:
        """Generate complete BLM analysis with reports."""

        # Run Five Looks
        five_looks = self.run_five_looks()

        # Run Three Decisions
        three_decisions = self.run_three_decisions(five_looks)

        # Generate reports
        report_gen = BLMReportGenerator(output_dir=output_dir)

        html_path = report_gen.generate_html_report(
            five_looks=five_looks,
            three_decisions=three_decisions,
            target_operator=self.target,
            competitors=self.competitors,
            title="BLM 战略分析报告 - 德国电信市场 Q2 2025",
            filename=f"blm_vodafone_germany_q2_2025.html",
        )

        text_path = report_gen.generate_text_report(
            five_looks=five_looks,
            three_decisions=three_decisions,
            target_operator=self.target,
            competitors=self.competitors,
            title="BLM Strategic Analysis - Germany Telecom Q2 2025",
            filename=f"blm_vodafone_germany_q2_2025.txt",
        )

        json_path = report_gen.generate_json_report(
            five_looks=five_looks,
            three_decisions=three_decisions,
            target_operator=self.target,
            competitors=self.competitors,
            title="BLM Strategic Analysis - Vodafone Germany Q2 2025",
            filename=f"blm_vodafone_germany_q2_2025.json",
        )

        return {
            "target_operator": self.target,
            "competitors": self.competitors,
            "five_looks": five_looks,
            "three_decisions": three_decisions,
            "reports": {
                "html": html_path,
                "text": text_path,
                "json": json_path,
            },
        }


def run_vodafone_germany_analysis():
    """Run Vodafone Germany BLM analysis and print results."""

    print("=" * 70)
    print("  BLM 战略分析: Vodafone Germany vs 德国竞争对手")
    print("  数据时间: Q2 2025 (FY26)")
    print("=" * 70)
    print()

    analyzer = GermanyTelecomBLMAnalyzer(target_operator="Vodafone Germany")
    results = analyzer.generate_full_analysis()

    # Print Five Looks Summary
    print("=" * 70)
    print("  五看分析 (Five Looks Analysis)")
    print("=" * 70)

    for key, insight in results["five_looks"].items():
        print()
        print("-" * 70)
        print(f"  {insight.title}")
        print("-" * 70)
        print()
        print("  [关键指标]")
        for mkey, mval in insight.metrics.items():
            print(f"    • {mkey}: {mval}")
        print()
        print("  [洞察发现]")
        for finding in insight.findings[:5]:
            print(f"    • {finding}")
        print()
        print("  [建议]")
        for rec in insight.recommendations[:3]:
            print(f"    → {rec}")

    # Print Three Decisions Summary
    print()
    print("=" * 70)
    print("  三定策略 (Three Decisions Strategy)")
    print("=" * 70)

    for key, decision in results["three_decisions"].items():
        print()
        print("-" * 70)
        print(f"  {decision.title}")
        print("-" * 70)
        print()
        print("  [概要]")
        for line in decision.summary.split("\n")[:10]:
            print(f"    {line}")
        print()
        print("  [关键举措]")
        for item in decision.items[:5]:
            print(f"    [{item.priority}] {item.name}")
            print(f"         {item.description[:60]}...")

    print()
    print("=" * 70)
    print("  报告已生成:")
    print("=" * 70)
    for fmt, path in results["reports"].items():
        print(f"  • {fmt.upper()}: {path}")

    return results


if __name__ == "__main__":
    run_vodafone_germany_analysis()
