"""BLM 三定策略引擎 (Three Decisions Strategy Engine).

Implements the "Three Decisions" (三定) framework from BLM:
1. 定策略 (Set Strategy) - Strategic direction, differentiation, positioning
2. 定重点工作 (Set Key Tasks) - Critical tasks, key initiatives
3. 定执行 (Set Execution) - Action plans, milestones, KPIs
"""

from dataclasses import dataclass, field
from typing import Optional
import pandas as pd
import numpy as np

from src.blm.five_looks import InsightResult, FiveLooksAnalyzer


@dataclass
class StrategyItem:
    """A single strategic element."""
    name: str
    description: str
    priority: str  # "P0", "P1", "P2"
    category: str
    timeline: str = ""
    owner: str = ""
    kpis: list[str] = field(default_factory=list)


@dataclass
class StrategyResult:
    """Container for strategy decision results."""
    decision_type: str  # "strategy", "key_tasks", "execution"
    title: str
    summary: str
    items: list[StrategyItem]
    metrics: dict = field(default_factory=dict)


class ThreeDecisionsEngine:
    """BLM 三定策略引擎 - generates strategic recommendations."""

    def __init__(
        self,
        five_looks_results: dict[str, InsightResult],
        target_operator: str,
    ):
        """Initialize with Five Looks analysis results.

        Args:
            five_looks_results: Dict from FiveLooksAnalyzer.run_full_analysis()
            target_operator: The operator being analyzed
        """
        self.insights = five_looks_results
        self.target = target_operator

    def run_full_strategy(self) -> dict[str, StrategyResult]:
        """Generate complete Three Decisions strategy.

        Returns:
            Dict with strategy, key_tasks, execution results.
        """
        return {
            "strategy": self.define_strategy(),
            "key_tasks": self.define_key_tasks(),
            "execution": self.define_execution(),
        }

    # =========================================================================
    # 1. 定策略 (Define Strategy)
    # =========================================================================
    def define_strategy(self) -> StrategyResult:
        """Define strategic direction, positioning, and differentiation."""
        items = []

        # Extract key insights
        market = self.insights.get("market")
        self_insight = self.insights.get("self")
        competitor = self.insights.get("competitor")
        opportunity = self.insights.get("opportunity")

        # Strategy 1: Growth Strategy
        growth_direction = self._determine_growth_strategy(market, self_insight)
        items.append(StrategyItem(
            name="增长战略",
            description=growth_direction["description"],
            priority="P0",
            category="growth",
            kpis=growth_direction["kpis"],
        ))

        # Strategy 2: Competitive Strategy
        competitive_strategy = self._determine_competitive_strategy(competitor, self_insight)
        items.append(StrategyItem(
            name="竞争战略",
            description=competitive_strategy["description"],
            priority="P0",
            category="competitive",
            kpis=competitive_strategy["kpis"],
        ))

        # Strategy 3: Digital Transformation Strategy
        digital_strategy = self._determine_digital_strategy(market, self_insight)
        items.append(StrategyItem(
            name="数字化转型战略",
            description=digital_strategy["description"],
            priority="P1",
            category="transformation",
            kpis=digital_strategy["kpis"],
        ))

        # Strategy 4: Customer Strategy
        customer_strategy = self._determine_customer_strategy(self_insight)
        items.append(StrategyItem(
            name="客户经营战略",
            description=customer_strategy["description"],
            priority="P1",
            category="customer",
            kpis=customer_strategy["kpis"],
        ))

        summary = f"""
{self.target} 战略规划:

1. 【增长战略】{growth_direction['description']}
2. 【竞争战略】{competitive_strategy['description']}
3. 【数字化转型战略】{digital_strategy['description']}
4. 【客户经营战略】{customer_strategy['description']}
"""

        return StrategyResult(
            decision_type="strategy",
            title="定策略 (Define Strategy)",
            summary=summary.strip(),
            items=items,
            metrics={
                "total_strategies": len(items),
                "p0_strategies": sum(1 for i in items if i.priority == "P0"),
                "p1_strategies": sum(1 for i in items if i.priority == "P1"),
            },
        )

    def _determine_growth_strategy(self, market: InsightResult, self_insight: InsightResult) -> dict:
        """Determine growth strategy based on market and self insights."""
        market_growth = market.metrics.get("market_growth_pct", 3) if market else 3
        market_share = self_insight.metrics.get("market_share_pct", 30) if self_insight else 30

        if market_share > 40:
            # Market leader - defend and expand
            return {
                "description": "巩固领先地位，通过差异化服务和生态建设维持份额，同时开拓新兴业务增长点",
                "kpis": ["市场份额保持>40%", "新业务收入占比>15%", "用户ARPU提升5%"],
            }
        elif market_share > 25:
            # Strong challenger - aggressive growth
            return {
                "description": "积极进攻策略，通过价值创新和渠道深耕提升市场份额，缩小与领导者差距",
                "kpis": ["市场份额提升2pp", "新增用户>500万/季", "收入增速超行业3pp"],
            }
        else:
            # Follower - focused growth
            return {
                "description": "聚焦差异化细分市场，在特定领域建立竞争优势，实现精准增长",
                "kpis": ["目标细分市场份额>30%", "细分市场收入增长>20%", "客户满意度>80分"],
            }

    def _determine_competitive_strategy(self, competitor: InsightResult, self_insight: InsightResult) -> dict:
        """Determine competitive strategy."""
        growth_gap = competitor.metrics.get("growth_gap_pct", 0) if competitor else 0
        top_strength = self_insight.metrics.get("top_strength", "Network Coverage") if self_insight else "Network Coverage"

        if growth_gap > 2:
            # Outperforming - capitalize on momentum
            return {
                "description": f"持续强化{top_strength}核心优势，扩大领先差距，同时补齐短板防止被追赶",
                "kpis": ["核心优势维度保持领先10分以上", "短板维度缩小差距5分", "品牌认知度提升"],
            }
        elif growth_gap > -2:
            # Neck and neck - differentiate
            return {
                "description": "实施差异化竞争策略，在关键细分市场和客户群建立独特价值主张",
                "kpis": ["差异化产品收入占比>20%", "重点客群份额提升", "产品创新数量"],
            }
        else:
            # Underperforming - catch up
            return {
                "description": "实施追赶战略，重点投入关键竞争短板，通过创新突破打破竞争格局",
                "kpis": ["与领先者差距缩小", "创新业务收入增速>30%", "关键能力指标提升"],
            }

    def _determine_digital_strategy(self, market: InsightResult, self_insight: InsightResult) -> dict:
        """Determine digital transformation strategy."""
        _5g_pct = market.metrics.get("5g_penetration_pct", 30) if market else 30

        if _5g_pct < 40:
            return {
                "description": "加速5G网络建设和用户迁移，打造5G应用生态，抢占数字化先机",
                "kpis": ["5G用户渗透率>50%", "5G网络覆盖率>80%", "5G应用收入占比>10%"],
            }
        else:
            return {
                "description": "深化数字化运营，发展云计算、大数据、AI等新能力，实现业务模式升级",
                "kpis": ["数字化服务收入增长>25%", "运营效率提升10%", "数字化触点渗透率>70%"],
            }

    def _determine_customer_strategy(self, self_insight: InsightResult) -> dict:
        """Determine customer strategy."""
        nps = self_insight.metrics.get("nps_score", 35) if self_insight else 35

        if nps < 40:
            return {
                "description": "实施客户体验提升专项，优化全触点服务流程，建立以客户为中心的运营体系",
                "kpis": ["NPS提升10分", "客户满意度>85分", "投诉率下降30%"],
            }
        else:
            return {
                "description": "深化客户价值经营，通过精准营销和个性化服务提升用户ARPU和生命周期价值",
                "kpis": ["ARPU提升8%", "高价值用户占比提升", "用户生命周期价值提升15%"],
            }

    # =========================================================================
    # 2. 定重点工作 (Define Key Tasks)
    # =========================================================================
    def define_key_tasks(self) -> StrategyResult:
        """Define critical tasks and key initiatives."""
        items = []

        opportunity = self.insights.get("opportunity")
        self_insight = self.insights.get("self")
        market = self.insights.get("market")

        # Extract opportunities and gaps
        opp_data = opportunity.data if opportunity and not opportunity.data.empty else pd.DataFrame()

        # Key Task Categories
        task_categories = {
            "network": {
                "name": "网络能力提升",
                "tasks": [
                    ("5G网络深度覆盖", "完成重点城市5G连续覆盖，提升室内深度覆盖"),
                    ("网络质量优化", "实施网络质量专项提升，降低投诉率"),
                ],
            },
            "business": {
                "name": "业务创新发展",
                "tasks": [
                    ("新兴业务培育", "加速云计算、物联网、数字化服务等新业务发展"),
                    ("政企市场突破", "深耕行业客户，打造标杆案例，扩大政企收入"),
                ],
            },
            "customer": {
                "name": "客户经营提升",
                "tasks": [
                    ("存量经营优化", "实施精准营销，提升用户价值和粘性"),
                    ("流失管控", "建立预警机制，降低用户流失率"),
                ],
            },
            "efficiency": {
                "name": "运营效率提升",
                "tasks": [
                    ("数字化运营", "推进智慧运营，提升自动化和智能化水平"),
                    ("成本优化", "实施降本增效，优化资源配置"),
                ],
            },
        }

        priority_map = {0: "P0", 1: "P0", 2: "P1", 3: "P1"}
        idx = 0

        for cat_key, cat_info in task_categories.items():
            for task_name, task_desc in cat_info["tasks"]:
                items.append(StrategyItem(
                    name=task_name,
                    description=task_desc,
                    priority=priority_map.get(idx, "P2"),
                    category=cat_key,
                    timeline="Q1-Q4",
                    kpis=[f"{task_name}完成率", f"{task_name}效果指标"],
                ))
                idx += 1

        summary = f"""
{self.target} 重点工作清单:

【网络能力提升】
- P0: 5G网络深度覆盖
- P0: 网络质量优化

【业务创新发展】
- P1: 新兴业务培育
- P1: 政企市场突破

【客户经营提升】
- P1: 存量经营优化
- P2: 流失管控

【运营效率提升】
- P2: 数字化运营
- P2: 成本优化
"""

        return StrategyResult(
            decision_type="key_tasks",
            title="定重点工作 (Define Key Tasks)",
            summary=summary.strip(),
            items=items,
            metrics={
                "total_tasks": len(items),
                "p0_tasks": sum(1 for i in items if i.priority == "P0"),
                "p1_tasks": sum(1 for i in items if i.priority == "P1"),
                "p2_tasks": sum(1 for i in items if i.priority == "P2"),
            },
        )

    # =========================================================================
    # 3. 定执行 (Define Execution)
    # =========================================================================
    def define_execution(self) -> StrategyResult:
        """Define action plans, milestones, and KPIs."""
        key_tasks = self.define_key_tasks()

        items = []
        execution_plan = []

        # Generate execution items for each key task
        for task in key_tasks.items[:6]:  # Top 6 tasks
            # Q1 milestone
            items.append(StrategyItem(
                name=f"{task.name} - Q1里程碑",
                description=f"完成{task.name}方案设计和试点启动",
                priority=task.priority,
                category="milestone",
                timeline="Q1",
                kpis=["方案完成", "试点启动"],
            ))
            # Q2 milestone
            items.append(StrategyItem(
                name=f"{task.name} - Q2里程碑",
                description=f"{task.name}全面推广实施",
                priority=task.priority,
                category="milestone",
                timeline="Q2",
                kpis=["推广覆盖率>50%"],
            ))

            execution_plan.append({
                "task": task.name,
                "q1": "方案设计 & 试点",
                "q2": "全面推广",
                "q3": "优化迭代",
                "q4": "效果评估",
                "owner": "待定",
                "kpi": task.kpis[0] if task.kpis else "完成率",
            })

        # Add governance items
        items.append(StrategyItem(
            name="战略执行管控机制",
            description="建立月度review、季度复盘机制，确保战略有效落地",
            priority="P0",
            category="governance",
            timeline="全年",
            kpis=["月度review完成率100%", "季度复盘覆盖率100%"],
        ))

        items.append(StrategyItem(
            name="资源保障机制",
            description="匹配人力、资金、技术资源，建立跨部门协同机制",
            priority="P0",
            category="governance",
            timeline="全年",
            kpis=["关键岗位到位率", "预算执行率"],
        ))

        summary = f"""
{self.target} 执行计划:

【执行节奏】
- Q1: 方案设计、资源准备、试点启动
- Q2: 全面推广、能力建设
- Q3: 优化迭代、攻坚克难
- Q4: 效果评估、总结沉淀

【管控机制】
- 月度: 进度review会
- 季度: 战略复盘会
- 半年: 中期评估调整
- 年度: 年终总结表彰

【KPI体系】
- 收入类: 收入增长率、新业务收入占比
- 用户类: 用户份额、ARPU、流失率
- 质量类: 网络质量、客户满意度、NPS
- 效率类: 运营成本率、人均产出
"""

        return StrategyResult(
            decision_type="execution",
            title="定执行 (Define Execution)",
            summary=summary.strip(),
            items=items,
            metrics={
                "total_milestones": len([i for i in items if i.category == "milestone"]),
                "governance_items": len([i for i in items if i.category == "governance"]),
                "execution_plan": execution_plan,
            },
        )


def generate_blm_strategy(
    data: dict[str, pd.DataFrame],
    target_operator: str,
    competitors: list[str] = None,
) -> dict:
    """Convenience function to run full BLM analysis.

    Args:
        data: Dict of DataFrames from TelecomDataGenerator
        target_operator: The operator to analyze
        competitors: List of competitor names

    Returns:
        Dict with 'five_looks' and 'three_decisions' results.
    """
    # Run Five Looks analysis
    analyzer = FiveLooksAnalyzer(data, target_operator, competitors)
    five_looks = analyzer.run_full_analysis()

    # Run Three Decisions strategy
    strategy_engine = ThreeDecisionsEngine(five_looks, target_operator)
    three_decisions = strategy_engine.run_full_strategy()

    return {
        "five_looks": five_looks,
        "three_decisions": three_decisions,
        "target_operator": target_operator,
        "competitors": competitors or [],
    }
