# BLM 五看 —"看自己"细分业务分析补充规范
# Look at Self: Business Segment Deep-Dive Specification

---

## 一、设计原则

> 每一个细分业务都要单独打开，至少一页。
> 每一个业务都要讲经营的变化，以及变化背后的原因。
> 先看财报数据，再分析财报背后变化的原因。

### 分析结构：两层逻辑

```
第一层：是什么（What）— 来自财报数据
  收入变化 / 用户数变化 / 利润变化 / ARPU 变化 / 留存率变化

第二层：为什么（Why）— 来自多维归因
  ← 财报中管理层的解释（Earnings Call、MD&A）
  ← 资费竞争的影响（我的定价 vs 对手定价变化）
  ← 用户反馈/满意度变化（NPS、App评分、投诉数据）
  ← 市场环境变化（从"看市场"中关联）
  ← 网络/产品变化（新产品上线、网络升级等）
```

---

## 二、细分业务清单

以下业务是运营商的主流分类。具体运营商可能有增减，系统应支持灵活配置。

| 业务 | 典型包含 |
|------|---------|
| **移动业务** | 消费者移动（后付费/预付费）、IoT/M2M |
| **固网宽带** | DSL、Cable、FTTH、FWA |
| **B2B/企业** | 企业连接、ICT 解决方案、云服务、安全 |
| **TV & 融合** | IPTV、Cable TV、融合套餐（FMC）|
| **批发业务** | 网络批发、MVNO、漫游 |
| **其他/新兴** | 数字服务、金融科技、广告等（视运营商而定）|

---

## 三、每个细分业务的分析模板

### 3.1 数据模型

```python
@dataclass
class SegmentChange:
    """一个细分业务中的具体变化"""
    metric: str                   # "revenue" / "subscribers" / "arpu" / "churn" / "margin"
    current_value: any            # 本季度值
    previous_value: any           # 上季度值
    yoy_value: any                # 去年同期值（如有）
    change_qoq: float            # 环比变化
    change_yoy: float            # 同比变化（如有）
    direction: str                # "improving" / "declining" / "stable"
    significance: str             # "significant" / "moderate" / "minor"

@dataclass
class ChangeAttribution:
    """变化的归因分析"""
    attribution_type: str         # "management_explanation" / "tariff_competition" / 
                                  # "customer_feedback" / "market_change" / "product_change"
    description: str              # 归因描述
    confidence: str               # "high" / "medium" / "low"
    evidence: list[str]           # 支撑证据（关联溯源）
    source: str                   # 来源类型 "earnings_call" / "tariff_scraping" / "nps_survey"

@dataclass
class SegmentAnalysis:
    """单个细分业务的完整分析"""
    segment_name: str             # "移动业务"
    segment_id: str               # "mobile"
    
    # 第一层：是什么（数据）
    key_metrics: dict             # 本季度核心指标
    changes: list[SegmentChange]  # 关键指标的变化
    trend_data: dict              # 8 季度趋势数据（用于画图）
    competitor_comparison: dict   # 与竞对的同维度对比
    
    # 第二层：为什么（归因）
    attributions: list[ChangeAttribution]  # 变化的原因清单
    
    # 综合判断
    health_status: str            # "strong" / "stable" / "weakening" / "critical"
    key_message: str              # 一句话总结这个业务
    action_required: str          # 需要的行动（如有）
```

### 3.2 每个业务具体看什么

#### 移动业务

```
[第一层：是什么]
  收入指标：移动服务收入、增速（QoQ / YoY）
  用户指标：总用户数、后付费/预付费拆分、净增用户数
  价值指标：ARPU、新客 ARPU、后付费占比
  留存指标：月度流失率、合同用户占比
  新兴：IoT 连接数、IoT 增速

[第二层：为什么]
  财报解释：管理层在 Earnings Call 中对移动业务的说明
  资费竞争：我的主力套餐 vs 竞对主力套餐价格对比
            - 谁在降价？降了多少？对我有什么影响？
  用户反馈：移动网络质量评价、App 评分变化
  市场因素：号码携带流向、新进入者影响（如 1&1）
  产品因素：新套餐上线效果、5G 升级拉动
```

#### 固网宽带

```
[第一层：是什么]
  收入指标：固网服务收入、增速
  用户指标：宽带总用户、按技术拆分（Cable/DSL/Fiber/FWA）
  价值指标：宽带 ARPU、升级率（低速→高速）
  留存指标：净增/流失、流失率
  网络：Home Pass vs Home Connect、光纤渗透率

[第二层：为什么]
  财报解释：固网业务下滑/增长的管理层解释
  资费竞争：我的宽带定价 vs 竞对定价（如德电 Fiber vs Vodafone Cable）
  用户反馈：宽带体验评价、速度满意度、投诉数据
  技术替代：Cable 用户被 Fiber 分流？DSL 用户被 FWA 替代？
  基建因素：光纤建设进度、Cable 网络升级（DOCSIS 3.1→4.0）
```

#### B2B / 企业业务

```
[第一层：是什么]
  收入指标：B2B 总收入、增速、占总收入比
  拆分：连接收入 vs ICT/云/安全收入
  客户指标：企业客户数、大客户 vs SME
  项目指标：新签合同额、续约率

[第二层：为什么]
  财报解释：B2B 战略的执行进展
  竞争：德电 T-Systems 的动作、云厂商（AWS/Azure）的渠道竞争
  需求端：企业数字化转型需求、AI 带来的新需求
  能力端：自身的云/安全/IoT 解决方案能力变化（如收购 Skaylink）
```

#### TV & 融合

```
[第一层：是什么]
  用户指标：TV 用户数、净增/流失
  融合指标：FMC 用户数、FMC 渗透率、捆绑折扣用户
  价值指标：融合用户 vs 单一用户的 ARPU 差异

[第二层：为什么]
  OTT 替代：Netflix/Disney+ 等对传统 TV 的冲击
  融合策略：捆绑套餐的吸引力变化
  竞对：德电 MagentaEINS 融合策略的竞争压力
```

#### 批发业务

```
[第一层：是什么]
  收入指标：批发收入、增速
  客户指标：批发客户数、承载用户数
  
[第二层：为什么]
  结构性变化：如 1&1 迁入带来的批发收入增长
  监管：互联互通费率变化
  合同：批发协议续签/到期影响
```

---

## 四、PPT Slide 规范更新

### 4.1 更新后的"看自己" Slide 结构

原来的 S07-S09 扩展为：

```
── 看自己 ──
S07   经营总体体检（财务总览 + 收入拆解 + 市场份额位置）
S08   移动业务深度分析
S09   固网宽带深度分析
S10   B2B 企业业务深度分析
S11   TV & 融合 / 批发 / 其他业务分析（可合并为 1 页或拆开）
S12   网络深度分析（技术结构 + 演进策略 + 竞对对比）
S13   优势、短板与暴露面
```

### 4.2 每个细分业务 Slide 的统一模板

```
┌─────────────────────────────────────────────────────────────────────┐
│ 标题: {业务名} 深度分析 | {Business Name} Analysis                    │
│ 副标题: {运营商名} · {期间}                                           │
├──────────────────────────────┬──────────────────────────────────────┤
│                              │                                      │
│  [左上] 趋势图表              │  [右上] 竞对对比表                      │
│                              │                                      │
│  8 季度趋势线图               │   指标    | 我  | 对手A | 对手B | 对手C │
│  (收入 or 用户 or ARPU)       │   收入    | xx  |  xx   |  xx   |  xx  │
│                              │   用户    | xx  |  xx   |  xx   |  xx  │
│  主角用品牌色                  │   ARPU   | xx  |  xx   |  xx   |  xx  │
│  竞对用灰色                   │   流失率  | xx  |  xx   |  xx   |  xx  │
│                              │   ...    |     |       |       |      │
├──────────────────────────────┴──────────────────────────────────────┤
│                                                                      │
│  [下半部分] 变化与归因                                                  │
│                                                                      │
│  ┌──────────────────────┐  ┌──────────────────────────────────────┐ │
│  │ 📊 关键变化（是什么）    │  │ 🔍 变化归因（为什么）                   │ │
│  │                        │  │                                     │ │
│  │ • 收入: ↑ +0.7% QoQ   │  │ 💼 财报解释:                         │ │
│  │   前值: +0.5%          │  │   "批发收入增长驱动..."                │ │
│  │                        │  │                                     │ │
│  │ • ARPU: ↑ €12.8       │  │ 💰 资费竞争:                         │ │
│  │   前值: €12.6          │  │   O2 降价 5%，但未影响我的高端用户     │ │
│  │                        │  │                                     │ │
│  │ • 流失: ↓ 1.05%       │  │ 👤 用户反馈:                         │ │
│  │   前值: 1.05% (持平)   │  │   NPS +3 分，App 评分 4.2→4.3       │ │
│  │                        │  │                                     │ │
│  │ • 净增: ↓ +80K        │  │ 🌐 市场因素:                         │ │
│  │   前值: +115K          │  │   1&1 迁移完成后竞争强度上升          │ │
│  │                        │  │                                     │ │
│  └──────────────────────┘  └──────────────────────────────────────┘ │
│                                                                      │
│  ─── 底部 Key Message（品牌色横条）──────────────────────────────────── │
│  "移动业务整体健康，ARPU 持续提升是核心亮点，但用户净增放缓需关注"       │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 4.3 设计要点

- **左上趋势图**：选择该业务最重要的 1-2 个指标做 8 季度趋势
- **右上对比表**：把我跟所有竞对的核心指标放一起，一目了然
- **左下关键变化**：用箭头标注每个指标的方向（↑ ↓ →），标注前值做对比
- **右下归因分析**：用图标区分来源类型（💼财报 💰资费 👤用户 🌐市场 🔧产品）
- **底部 Key Message**：一句话总结，用品牌色横条醒目显示

---

## 五、数据采集需求更新

细分业务分析需要以下数据：

### 5.1 "是什么"层（财报数据）

| 数据 | 来源 | 数据库表 |
|------|------|---------|
| 各业务线收入/利润 | FinancialReportCollector 解析财报 | financial_quarterly |
| 各业务线用户数 | FinancialReportCollector | subscriber_quarterly |
| ARPU | FinancialReportCollector | subscriber_quarterly |
| 流失率 | FinancialReportCollector | subscriber_quarterly |
| 竞对同维度数据 | FinancialReportCollector（对手财报）| 同上 |

### 5.2 "为什么"层（归因数据）

| 数据 | 来源 | 数据库表 |
|------|------|---------|
| 管理层解释 | Earnings Call 解析 | 新表：`earnings_call_highlights` |
| 资费对比 | MarketDataCollector 抓取资费页 | tariffs |
| 用户评价 | IntelligenceMonitor（App 评分、NPS 公开数据）| intelligence_events + competitive_scores |
| 市场变化关联 | 从"看市场"的分析结果中引用 | 交叉引用 |
| 产品变化 | IntelligenceMonitor（新闻/公告）| intelligence_events |

### 5.3 新增数据库表

```sql
-- Earnings Call 要点摘录
-- 用于"为什么"层的管理层解释
CREATE TABLE earnings_call_highlights (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id     TEXT NOT NULL REFERENCES operators(operator_id),
    period          TEXT NOT NULL,            -- "Q3 FY26"
    segment         TEXT,                     -- "mobile" / "fixed" / "b2b" / "overall"
    topic           TEXT NOT NULL,            -- "revenue_growth_driver" / "churn_improvement" 
    speaker         TEXT,                     -- "CEO" / "CFO"
    highlight       TEXT NOT NULL,            -- 管理层的原话或要点
    sentiment       TEXT,                     -- "positive" / "cautious" / "negative"
    
    source_url      TEXT,                     -- Earnings Call 链接
    collected_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(operator_id, period, segment, topic)
);
```

---

## 六、与现有代码的关系

### 合并 ComprehensiveAnalysisPPT 的业务分析

现有 `ComprehensiveAnalysisPPT` 已经有移动/固网/B2B/TV 的独立页面。
但它是独立于五看分析引擎的——直接读硬编码数据，没有归因分析。

**改造方案：**
- 将 `ComprehensiveAnalysisPPT` 中的业务分析图表代码迁移到 `BLMPPTGeneratorEnhanced`
- 增加"为什么"层的归因分析面板
- 数据来源从硬编码改为数据库查询
- 最终只保留一个 PPT 生成器（`BLMPPTGeneratorEnhanced`），避免两套 PPT 不一致

### 更新后的完整 Slide 清单

```
SECTION 0: 开场
  S01  封面
  S02  目录
  S03  数据来源与质量概览
  S04  执行摘要

SECTION 1: 五看分析

  ── 看市场 ──
  S05  市场变化全景
  S06  [可选] 重点变化深度

  ── 看自己 ──
  S07  经营总体体检
  S08  移动业务深度分析         ← 新增专属页
  S09  固网宽带深度分析         ← 新增专属页
  S10  B2B 企业业务深度分析     ← 新增专属页
  S11  TV/融合/批发/其他分析    ← 新增专属页
  S12  网络深度分析
  S13  优势、短板与暴露面

  ── 看对手 ──
  S14  对手 A 详细分析
  S15  对手 B 详细分析
  S16  对手 C 详细分析
  S17  横向对比总结

  ── 看宏观 ──
  S18  宏观环境仪表盘
  S19  [可选] 重点政策/趋势

  ── 看机会 ──
  S20  机会点清单
  S21  [可选] Top 3 机会深度

  ── 综合 ──
  S22  竞争力雷达图
  S23  Gap 分析

SECTION 2: 经营详细数据（支撑层）
  S24  季度经营分析
  S25  8 季度历史趋势

SECTION 3: 三定策略
  S26  定策略
  S27  定重点工作
  S28  定执行

SECTION 4: 收尾
  S29  总结与下一步
  S30  数据溯源附录
  S31  封底
```

总计约 25-31 页（视可选页和对手数量而定），信息量充分但不过度臃肿。
