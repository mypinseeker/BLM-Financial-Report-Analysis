"""BLM 五看分析引擎 (Five Looks Analysis Engine).

Implements the "Five Looks" (五看) framework from BLM:
1. 看市场 (Look at Market) - Market insight
2. 看自己 (Look at Self) - Self assessment
3. 看对手 (Look at Competitors) - Competitive analysis
4. 看宏观 (Look at Macro) - Macro environment
5. 看机会 (Look at Opportunities) - Opportunity identification
"""

from dataclasses import dataclass, field
from typing import Optional
import pandas as pd
import numpy as np


@dataclass
class InsightResult:
    """Container for analysis insight results."""
    category: str  # e.g., "market", "self", "competitor", "macro", "opportunity"
    title: str
    findings: list[str]
    metrics: dict
    data: pd.DataFrame
    recommendations: list[str] = field(default_factory=list)


class FiveLooksAnalyzer:
    """BLM 五看分析引擎 - analyzes telecom operators across 5 dimensions."""

    def __init__(
        self,
        data: dict[str, pd.DataFrame],
        target_operator: str,
        competitors: list[str] = None,
    ):
        """Initialize analyzer with data.

        Args:
            data: Dict of DataFrames with keys: market, financial, competitive, macro, segments, customer
            target_operator: The operator being analyzed (e.g., "China Mobile")
            competitors: List of competitor names to compare against
        """
        self.data = data
        self.target = target_operator
        self.competitors = competitors or []
        self.all_operators = [target_operator] + self.competitors

    def run_full_analysis(self) -> dict[str, InsightResult]:
        """Run complete Five Looks analysis.

        Returns:
            Dict mapping look type to InsightResult.
        """
        return {
            "market": self.look_at_market(),
            "self": self.look_at_self(),
            "competitor": self.look_at_competitors(),
            "macro": self.look_at_macro(),
            "opportunity": self.look_at_opportunities(),
        }

    # =========================================================================
    # 1. 看市场 (Look at Market)
    # =========================================================================
    def look_at_market(self) -> InsightResult:
        """Analyze market size, structure, trends, and segments."""
        market_df = self.data.get("market", pd.DataFrame())
        segment_df = self.data.get("segments", pd.DataFrame())

        if market_df.empty:
            return InsightResult(
                category="market", title="市场洞察", findings=["无市场数据"],
                metrics={}, data=pd.DataFrame(),
            )

        # Latest quarter data
        latest_q = market_df["quarter"].max()
        latest = market_df[market_df["quarter"] == latest_q]

        # Market metrics
        total_subs = latest["subscribers_million"].sum()
        avg_5g_pct = latest["5g_users_pct"].mean()
        avg_churn = latest["churn_rate_pct"].mean()

        # Growth trend
        first_q = market_df["quarter"].min()
        first_data = market_df[market_df["quarter"] == first_q]
        growth_rate = (
            (latest["subscribers_million"].sum() - first_data["subscribers_million"].sum())
            / first_data["subscribers_million"].sum() * 100
        ) if not first_data.empty else 0

        # Segment analysis
        findings = [
            f"市场总用户规模: {total_subs:.0f}M",
            f"5G用户渗透率: {avg_5g_pct:.1f}%",
            f"市场平均流失率: {avg_churn:.2f}%",
            f"分析期间市场增长: {growth_rate:.1f}%",
        ]

        # Segment growth insights
        if not segment_df.empty:
            growth_segs = segment_df[segment_df["is_growth_segment"] == True]
            if not growth_segs.empty:
                avg_growth = growth_segs.groupby("segment")["yoy_growth_pct"].mean()
                top_seg = avg_growth.idxmax()
                findings.append(f"增长最快细分市场: {top_seg} ({avg_growth[top_seg]:.1f}% YoY)")

        metrics = {
            "total_subscribers_million": round(total_subs, 1),
            "5g_penetration_pct": round(avg_5g_pct, 1),
            "market_growth_pct": round(growth_rate, 1),
            "avg_churn_pct": round(avg_churn, 2),
        }

        recommendations = [
            "持续关注5G用户迁移速度和价值提升",
            "重点发展数字化转型等新兴业务板块",
            "优化存量用户经营，降低流失率",
        ]

        return InsightResult(
            category="market",
            title="市场洞察 (Look at Market)",
            findings=findings,
            metrics=metrics,
            data=latest,
            recommendations=recommendations,
        )

    # =========================================================================
    # 2. 看自己 (Look at Self)
    # =========================================================================
    def look_at_self(self) -> InsightResult:
        """Analyze own performance, capabilities, and gaps."""
        market_df = self.data.get("market", pd.DataFrame())
        fin_df = self.data.get("financial", pd.DataFrame())
        comp_df = self.data.get("competitive", pd.DataFrame())
        cust_df = self.data.get("customer", pd.DataFrame())

        findings = []
        metrics = {}

        # Market position
        if not market_df.empty:
            latest_q = market_df["quarter"].max()
            latest = market_df[(market_df["quarter"] == latest_q) & (market_df["operator"] == self.target)]
            if not latest.empty:
                share = latest["market_share_pct"].iloc[0]
                subs = latest["subscribers_million"].iloc[0]
                metrics["market_share_pct"] = share
                metrics["subscribers_million"] = subs
                findings.append(f"市场份额: {share:.1f}%")
                findings.append(f"用户规模: {subs:.1f}M")

        # Financial performance
        if not fin_df.empty:
            target_fin = fin_df[fin_df["operator"] == self.target]
            if not target_fin.empty:
                latest_fin = target_fin[target_fin["quarter"] == target_fin["quarter"].max()]
                rev = latest_fin["revenue_billion_usd"].iloc[0]
                margin = latest_fin["profit_margin_pct"].iloc[0]
                growth = latest_fin["revenue_growth_yoy_pct"].iloc[0]
                metrics["revenue_billion_usd"] = rev
                metrics["profit_margin_pct"] = margin
                metrics["revenue_growth_pct"] = growth
                findings.append(f"季度收入: ${rev:.1f}B")
                findings.append(f"利润率: {margin:.1f}%")
                findings.append(f"收入增长: {growth:.1f}% YoY")

        # Competitive strengths/weaknesses
        if not comp_df.empty:
            target_comp = comp_df[comp_df["operator"] == self.target]
            if not target_comp.empty:
                latest_comp = target_comp[target_comp["quarter"] == target_comp["quarter"].max()]
                strengths = latest_comp.nlargest(3, "score")[["dimension", "score"]]
                weaknesses = latest_comp.nsmallest(3, "score")[["dimension", "score"]]
                findings.append(f"核心优势: {', '.join(strengths['dimension'].tolist())}")
                findings.append(f"待改进项: {', '.join(weaknesses['dimension'].tolist())}")
                metrics["top_strength"] = strengths.iloc[0]["dimension"]
                metrics["top_weakness"] = weaknesses.iloc[0]["dimension"]

        # Customer metrics
        if not cust_df.empty:
            target_cust = cust_df[cust_df["operator"] == self.target]
            if not target_cust.empty:
                latest_cust = target_cust[target_cust["quarter"] == target_cust["quarter"].max()]
                nps = latest_cust["nps_score"].iloc[0]
                metrics["nps_score"] = nps
                findings.append(f"NPS得分: {nps:.0f}")

        recommendations = [
            "强化核心竞争优势，建立差异化壁垒",
            "针对薄弱环节制定专项提升计划",
            "优化客户体验，提升NPS和满意度",
        ]

        return InsightResult(
            category="self",
            title="自身洞察 (Look at Self)",
            findings=findings,
            metrics=metrics,
            data=pd.DataFrame([metrics]) if metrics else pd.DataFrame(),
            recommendations=recommendations,
        )

    # =========================================================================
    # 3. 看对手 (Look at Competitors)
    # =========================================================================
    def look_at_competitors(self) -> InsightResult:
        """Analyze competitor performance and positioning."""
        market_df = self.data.get("market", pd.DataFrame())
        fin_df = self.data.get("financial", pd.DataFrame())
        comp_df = self.data.get("competitive", pd.DataFrame())

        findings = []
        metrics = {}
        comparison_data = []

        if not self.competitors:
            return InsightResult(
                category="competitor", title="竞争洞察", findings=["未指定竞争对手"],
                metrics={}, data=pd.DataFrame(),
            )

        latest_q = market_df["quarter"].max() if not market_df.empty else None

        for comp in self.competitors:
            comp_metrics = {"operator": comp}

            # Market share
            if not market_df.empty and latest_q:
                comp_market = market_df[(market_df["quarter"] == latest_q) & (market_df["operator"] == comp)]
                if not comp_market.empty:
                    comp_metrics["market_share_pct"] = comp_market["market_share_pct"].iloc[0]

            # Financial
            if not fin_df.empty:
                comp_fin = fin_df[fin_df["operator"] == comp]
                if not comp_fin.empty:
                    latest_fin = comp_fin[comp_fin["quarter"] == comp_fin["quarter"].max()]
                    comp_metrics["revenue_billion_usd"] = latest_fin["revenue_billion_usd"].iloc[0]
                    comp_metrics["profit_margin_pct"] = latest_fin["profit_margin_pct"].iloc[0]
                    comp_metrics["revenue_growth_pct"] = latest_fin["revenue_growth_yoy_pct"].iloc[0]

            # Competitive scores
            if not comp_df.empty:
                comp_scores = comp_df[comp_df["operator"] == comp]
                if not comp_scores.empty:
                    latest_scores = comp_scores[comp_scores["quarter"] == comp_scores["quarter"].max()]
                    avg_score = latest_scores["score"].mean()
                    comp_metrics["avg_competitive_score"] = round(avg_score, 1)

            comparison_data.append(comp_metrics)
            findings.append(
                f"{comp}: 份额{comp_metrics.get('market_share_pct', 'N/A'):.1f}%, "
                f"收入${comp_metrics.get('revenue_billion_usd', 0):.1f}B, "
                f"增长{comp_metrics.get('revenue_growth_pct', 0):.1f}%"
            )

        # Compare with self
        if not fin_df.empty:
            self_fin = fin_df[fin_df["operator"] == self.target]
            if not self_fin.empty:
                self_latest = self_fin[self_fin["quarter"] == self_fin["quarter"].max()]
                self_growth = self_latest["revenue_growth_yoy_pct"].iloc[0]
                avg_comp_growth = np.mean([c.get("revenue_growth_pct", 0) for c in comparison_data])
                if self_growth > avg_comp_growth:
                    findings.append(f"✓ 我方增速({self_growth:.1f}%)高于竞争对手平均({avg_comp_growth:.1f}%)")
                else:
                    findings.append(f"⚠ 我方增速({self_growth:.1f}%)低于竞争对手平均({avg_comp_growth:.1f}%)")
                metrics["growth_gap_pct"] = round(self_growth - avg_comp_growth, 1)

        recommendations = [
            "密切跟踪竞争对手的战略动态和业务创新",
            "在差异化领域建立竞争优势",
            "关注对手的薄弱环节，寻找突破机会",
        ]

        return InsightResult(
            category="competitor",
            title="竞争洞察 (Look at Competitors)",
            findings=findings,
            metrics=metrics,
            data=pd.DataFrame(comparison_data),
            recommendations=recommendations,
        )

    # =========================================================================
    # 4. 看宏观 (Look at Macro)
    # =========================================================================
    def look_at_macro(self) -> InsightResult:
        """Analyze macro environment: economy, policy, technology trends."""
        macro_df = self.data.get("macro", pd.DataFrame())

        if macro_df.empty:
            return InsightResult(
                category="macro", title="宏观环境洞察", findings=["无宏观数据"],
                metrics={}, data=pd.DataFrame(),
            )

        latest_q = macro_df["quarter"].max()
        latest = macro_df[macro_df["quarter"] == latest_q]

        findings = []
        metrics = {}

        # Average metrics across countries
        avg_gdp = latest["gdp_growth_pct"].mean()
        avg_5g_coverage = latest["5g_coverage_pct"].mean()
        avg_digital = latest["digital_economy_pct"].mean()
        avg_penetration = latest["telecom_penetration_pct"].mean()

        metrics["avg_gdp_growth_pct"] = round(avg_gdp, 1)
        metrics["avg_5g_coverage_pct"] = round(avg_5g_coverage, 1)
        metrics["avg_digital_economy_pct"] = round(avg_digital, 1)

        findings.append(f"平均GDP增长率: {avg_gdp:.1f}%")
        findings.append(f"平均5G网络覆盖: {avg_5g_coverage:.1f}%")
        findings.append(f"数字经济占比: {avg_digital:.1f}%")
        findings.append(f"电信渗透率: {avg_penetration:.1f}%")

        # Competitive intensity
        intensity_counts = latest["competitive_intensity"].value_counts()
        dominant = intensity_counts.idxmax() if not intensity_counts.empty else "Unknown"
        findings.append(f"市场竞争强度: {dominant}")
        metrics["competitive_intensity"] = dominant

        # Trends
        first_q = macro_df["quarter"].min()
        first = macro_df[macro_df["quarter"] == first_q]
        if not first.empty:
            _5g_growth = avg_5g_coverage - first["5g_coverage_pct"].mean()
            findings.append(f"5G覆盖增长: +{_5g_growth:.1f}pp (分析期间)")

        recommendations = [
            "把握数字经济发展机遇，加速数字化转型",
            "积极响应政策导向，争取政策支持",
            "关注技术演进趋势，提前布局6G等前沿技术",
        ]

        return InsightResult(
            category="macro",
            title="宏观环境洞察 (Look at Macro)",
            findings=findings,
            metrics=metrics,
            data=latest,
            recommendations=recommendations,
        )

    # =========================================================================
    # 5. 看机会 (Look at Opportunities)
    # =========================================================================
    def look_at_opportunities(self) -> InsightResult:
        """Identify gaps, opportunities, and threats."""
        # Synthesize from other analyses
        market = self.look_at_market()
        self_analysis = self.look_at_self()
        competitors = self.look_at_competitors()
        macro = self.look_at_macro()

        opportunities = []
        threats = []
        gaps = []

        # Growth opportunity from segments
        segment_df = self.data.get("segments", pd.DataFrame())
        if not segment_df.empty:
            growth_segs = segment_df[
                (segment_df["operator"] == self.target) &
                (segment_df["is_growth_segment"] == True)
            ]
            if not growth_segs.empty:
                for seg in growth_segs["segment"].unique():
                    seg_data = growth_segs[growth_segs["segment"] == seg]
                    avg_growth = seg_data["yoy_growth_pct"].mean()
                    if avg_growth > 10:
                        opportunities.append(f"{seg}: 高增长潜力 ({avg_growth:.0f}% CAGR)")

        # Competitive gaps
        comp_df = self.data.get("competitive", pd.DataFrame())
        if not comp_df.empty and self.competitors:
            latest_q = comp_df["quarter"].max()
            target_scores = comp_df[
                (comp_df["quarter"] == latest_q) &
                (comp_df["operator"] == self.target)
            ].set_index("dimension")["score"]

            for comp in self.competitors:
                comp_scores = comp_df[
                    (comp_df["quarter"] == latest_q) &
                    (comp_df["operator"] == comp)
                ].set_index("dimension")["score"]

                for dim in target_scores.index:
                    if dim in comp_scores.index:
                        gap = target_scores[dim] - comp_scores[dim]
                        if gap < -10:
                            gaps.append(f"vs {comp} 在 {dim}: 落后 {abs(gap):.0f}分")
                        elif gap > 10:
                            opportunities.append(f"vs {comp} 在 {dim}: 领先 {gap:.0f}分")

        # Macro-driven opportunities/threats
        if "5g_penetration_pct" in market.metrics:
            if market.metrics["5g_penetration_pct"] < 50:
                opportunities.append("5G用户渗透仍有较大提升空间")

        if "competitive_intensity" in macro.metrics:
            if macro.metrics["competitive_intensity"] == "High":
                threats.append("市场竞争激烈，价格战风险")

        # Customer-driven insights
        cust_df = self.data.get("customer", pd.DataFrame())
        if not cust_df.empty:
            target_cust = cust_df[cust_df["operator"] == self.target]
            if not target_cust.empty:
                latest_cust = target_cust[target_cust["quarter"] == target_cust["quarter"].max()]
                digital_pct = latest_cust["digital_engagement_pct"].iloc[0]
                if digital_pct < 60:
                    opportunities.append(f"数字化触点渗透率仅{digital_pct:.0f}%，提升空间大")

        findings = []
        findings.append("=== 机会 ===")
        findings.extend([f"✓ {o}" for o in opportunities[:5]])
        findings.append("=== 差距 ===")
        findings.extend([f"△ {g}" for g in gaps[:5]])
        findings.append("=== 威胁 ===")
        findings.extend([f"⚠ {t}" for t in threats[:3]])

        metrics = {
            "opportunities_count": len(opportunities),
            "gaps_count": len(gaps),
            "threats_count": len(threats),
        }

        recommendations = [
            "优先投入高增长业务领域",
            "针对竞争差距制定追赶计划",
            "建立风险预警和应对机制",
        ]

        return InsightResult(
            category="opportunity",
            title="机会洞察 (Look at Opportunities)",
            findings=findings,
            metrics=metrics,
            data=pd.DataFrame({
                "type": ["Opportunity"] * len(opportunities) + ["Gap"] * len(gaps) + ["Threat"] * len(threats),
                "description": opportunities + gaps + threats,
            }),
            recommendations=recommendations,
        )
