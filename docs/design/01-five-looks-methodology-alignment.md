# BLM 五看方法论对齐 — 全面更新
# Five Looks Methodology Alignment — Comprehensive Update

---

## 一、六项决策落实总览

| 决策 | 变更内容 |
|------|---------|
| ① 顺序调整 | 看趋势 → 看市场/客户 → 看竞争 → 看自己 → SWOT → 看机会 |
| ② 客户分析 | "看市场"升级为"看市场/客户"，增加客户细分、购买行为、痛点需求 |
| ③ 波特五力 | "看竞争"从仅看同行扩展为完整五力分析 |
| ④ 组织内部 | "看自己"增加流程瓶颈、人才储备、企业文化、BMC 商业模式画布 |
| ⑤ SPAN 矩阵 | "看机会"引入市场吸引力 × 竞争地位的二维定位 |
| ⑥ SWOT 综合 | 在看自己和看机会之间增加 SWOT 分析桥梁 |

---

## 二、更新后的五看全景

### 2.1 顺序与逻辑

```
由外而内，层层聚焦：

  看趋势（宏观大势）
    ↓ 大环境给行业什么影响？
  看市场/客户（行业 + 客户）
    ↓ 市场里有什么变化？客户要什么？
  看竞争（竞争格局）
    ↓ 对手在做什么？五种竞争力量如何？
  看自己（内部审视）
    ↓ 我的情况如何？差距在哪？
  ── SWOT 综合分析 ──（前四看的桥梁）
    ↓ 内部优劣势 × 外部机会威胁 → 四种策略方向
  看机会（机会筛选）
    ↓ 哪些机会值得抓？SPAN 矩阵定位
```

### 2.2 更新后的五看总览

| 序号 | 看 | 方法论命名 | 核心框架 | 核心问题 |
|------|------|----------|---------|---------|
| 01 | 看趋势 | Trend | PEST | 宏观大势和行业趋势对我有什么影响？ |
| 02 | 看市场/客户 | Market/Customer | 市场地图 + $APPEALS | 市场有什么变化？客户要什么？ |
| 03 | 看竞争 | Competitor | 波特五力 | 五种竞争力量如何？对手在做什么？ |
| 04 | 看自己 | Self | BMC + 能力盘点 | 我的经营、能力、组织准备度如何？ |
| 桥梁 | SWOT 综合 | — | SWOT 矩阵 | 内部 SW × 外部 OT → 四种策略 |
| 05 | 看机会 | Opportunity | SPAN 矩阵 | 哪些机会值得抓？优先级如何？ |

---

## 三、01 看趋势（Trend）

### 3.1 定位

> 第一看。由外向内的起点。看清楚大势，才知道顺势而为还是逆势突围。

**已有设计**：PEST 框架已在"看宏观 PEST 框架对齐规范"中完成。
**本次变更**：从第四看移到第一看，命名从"看宏观"改为"看趋势"。

### 3.2 方法论要求的输出

来自原文的明确要求，看趋势必须回答：

1. 市场正在发生的重大变化有哪些？
2. 产业政策有哪些重大改变？对企业影响是怎样的？
3. 产业格局的变化带给我们的影响、机遇和挑战有哪些？
4. 整体市场空间有多大？增长率是多少？利润将发生什么样的变化？
5. 新技术的发展趋势及变化是怎样的？本企业可参与的市场空间有多大？

同时要输出：战略机会、市场规模、市场增长/衰落速度、市场利润变化、
市场集中度、生命周期阶段、新的商业模式、新的技术革命、关键成功因素。

### 3.3 数据模型

沿用已定义的 `PESTFactor` 和 `PESTAnalysis`，增加行业环境要素：

```python
@dataclass
class TrendAnalysis:
    """看趋势的完整输出"""
    # PEST 四维度（已定义）
    pest: PESTAnalysis
    
    # 行业环境分析（方法论新增要求）
    industry_market_size: str              # 整体市场空间
    industry_growth_rate: str              # 市场增长率
    industry_profit_trend: str             # 利润变化趋势
    industry_concentration: str            # 市场集中度（CR4 等）
    industry_lifecycle_stage: str          # 生命周期阶段（成长/成熟/衰退）
    new_business_models: list[str]         # 新的商业模式
    technology_revolution: list[str]       # 新的技术革命
    key_success_factors: list[str]         # 关键成功因素
    value_transfer_trends: list[str]       # 价值转移趋势
    
    key_message: str
```

### 3.4 PPT Slide

```
S05  看趋势 — PEST 宏观环境仪表盘（四象限）
S06  看趋势 — 行业环境分析（市场规模/增速/利润/集中度/生命周期）
S07  [可选] 重点趋势深度分析
```

---

## 四、02 看市场/客户（Market/Customer）

### 4.1 定位

> 第二看。在看清趋势之后，深入分析本行业市场的变化和客户的需求。
> 不是从厂家"卖方"立场出发，更多站在客户"买方"视角识别市场机会。

**已有设计**：市场变化检测（同行驱动 + 外部玩家驱动 + 三个时间层）。
**本次新增**：系统性的客户分析维度。

### 4.2 方法论要求的问题清单

看市场/客户必须回答：

1. 这个市场上有哪些机会？
2. 哪些客户群的需求没有得到满足？是否存在新的客户群？
3. 哪些客户群是竞争对手服务不到位的？
4. 可以通过哪些细分标准将客户进行分类？
5. 客户在未来五年的发展战略方向是什么？在客户的发展战略当中存在哪些痛点？
6. 客户面临的压力和挑战有哪些？哪些 KPI 跟公司有关，可以帮助客户改善？
7. 客户组织和流程（决策及采购）会有大的变化吗？
8. 促使客户作出购买决定的关键因素是什么？

### 4.3 新增：客户分析框架

#### 电信行业的客户细分

```
消费者客户（C 端）
├── 高端用户：高 ARPU，追求网络质量和体验
├── 主流用户：中等 ARPU，价格和体验平衡
├── 价格敏感用户：低 ARPU，以价格为第一决策因素
├── 年轻群体：数字原住民，重视数据流量和 App 体验
├── 银发群体：数字素养低，需要简单易用的服务
└── 移民群体：国际通话需求，多语言服务

企业客户（B 端）
├── 大企业 / 跨国公司：复杂 ICT 需求，多站点，全球连接
├── 中型企业：数字化转型中，需要打包解决方案
├── 小微企业 / SOHO：简单连接需求，价格敏感
├── 政府 / 公共部门：合规要求高，采购流程复杂
└── 垂直行业：制造业 IoT、医疗、教育等专业需求

批发客户
├── MVNO：转售移动网络
├── ISP：批发宽带接入
└── OTT / 云厂商：网络能力合作
```

#### $APPEALS 模型适配电信行业

| 要素 | 英文 | 电信行业的含义 | 数据来源 |
|------|------|--------------|---------|
| **价格** | $ (Price) | 套餐定价、促销力度、合约优惠 | 资费采集 |
| **可获得性** | A (Availability) | 覆盖范围（5G/Fiber）、开通速度、渠道便利性 | 覆盖数据 + 渠道分析 |
| **包装** | P (Packaging) | 融合套餐设计、品牌形象、门店体验 | 竞品套餐分析 |
| **性能** | P (Performance) | 网速、时延、可靠性、通话质量 | 网络测试报告 |
| **易用性** | E (Ease of Use) | App 体验、自助服务、客服响应 | App 评分 + NPS |
| **保障性** | A (Assurances) | SLA 保证、故障响应、数据安全 | B2B 合同条款 |
| **生命周期成本** | L (Lifecycle Cost) | TCO、设备分期、解约费 | 资费分析 |
| **社会接受度** | S (Social Acceptance) | 品牌口碑、ESG 形象、推荐意愿 | 社交媒体 + NPS |

### 4.4 数据模型

```python
@dataclass
class CustomerSegment:
    """一个客户细分"""
    segment_name: str             # "高端消费者" / "大企业"
    segment_type: str             # "consumer" / "enterprise" / "wholesale"
    size_estimate: str            # 该细分的规模估算
    growth_trend: str             # "growing" / "stable" / "shrinking"
    our_share: str                # 我们在该细分中的份额（如有数据）
    unmet_needs: list[str]        # 未满足的需求
    pain_points: list[str]        # 痛点
    purchase_decision_factors: list[str]  # 购买决策关键因素
    competitor_gaps: list[str]    # 竞对在该细分中服务不到位的地方
    opportunity: str              # 对我们的机会

@dataclass
class APPEALSAssessment:
    """$APPEALS 模型评估"""
    dimension: str                # "$" / "A1" / "P1" / "P2" / "E" / "A2" / "L" / "S"
    dimension_name: str           # "Price" / "Availability" / ...
    our_score: int                # 1-5 分
    competitor_scores: dict       # {"Deutsche Telekom": 4, "O2": 3, ...}
    customer_priority: str        # "critical" / "important" / "nice_to_have"
    gap_analysis: str             # 我们与客户期望的差距

@dataclass
class MarketCustomerInsight:
    """看市场/客户的完整输出"""
    # 市场变化分析（已有设计）
    market_snapshot: dict
    changes: list[MarketChange]
    opportunities: list[MarketChange]
    threats: list[MarketChange]
    
    # 客户分析（新增）
    customer_segments: list[CustomerSegment]
    appeals_assessment: list[APPEALSAssessment]  # C 端和 B 端分别做一套
    customer_value_migration: str                 # 客户价值转移趋势
    
    market_outlook: str
    key_message: str
```

### 4.5 PPT Slide

```
S08  看市场 — 市场变化全景（机会 vs 威胁清单）
S09  看市场 — 客户细分与需求分析
S10  看市场 — $APPEALS 竞争力评估（雷达图）
S11  [可选] 重点客户群深度分析
```

---

## 五、03 看竞争（Competitor）— 波特五力

### 5.1 定位

> 第三看。竞争分析不只是看同行对手，要看完整的五种竞争力量。
> 最终目的是站在市场/客户立场，制定赢得市场的策略和解决方案。

**已有设计**：每个同行对手做体检 + 对我的启示 + 横向对比。
**本次升级**：增加波特五力中缺失的三个维度。

### 5.2 波特五力框架 — 电信行业适配

```
                  ┌───────────────────────┐
                  │  潜在竞争者（新进入者）  │
                  │  如：1&1 自建网络       │
                  │  Starlink 卫星互联网    │
                  │  科技公司跨界           │
                  └───────────┬───────────┘
                              │
                              ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────┐
│ 供应商议价能力 │───→│  同行业现有竞争者  │←───│  买方议价能力  │
│              │    │                  │    │              │
│ 设备商：       │    │ DT / VF / O2    │    │ C 端：低      │
│ 华为/爱立信    │    │ 直接竞争        │    │ （个体弱）     │
│ /诺基亚       │    │                  │    │ B 端：高      │
│              │    │ 竞争激烈程度      │    │ （大客户强）   │
│ 芯片：高管控   │    │ 市场集中度       │    │ 政府采购：很高 │
│ 光纤/铁塔     │    │ 差异化程度       │    │              │
└──────────────┘    └──────────────────┘    └──────────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │  替代品的威胁           │
                  │  OTT 替代传统通信       │
                  │  Wi-Fi 替代蜂窝         │
                  │  云厂商替代传统 ICT     │
                  └───────────────────────┘
```

### 5.3 五力分析维度

#### ① 同行业现有竞争者（已有，增强）

保留原有设计（每个对手做体检 + 启示），增加方法论要求的分析要素：

| 原有 | 新增 |
|------|------|
| 财务体检 | 市场增长策略 |
| 用户体检 | 产品系列及新产品上市计划 |
| 网络状态 | 供应链和产能情况 |
| 优缺点 | 生态与合作伙伴 |
| 对我的启示 | 核心控制点及商业模式 |
| | 组织结构和激励体系 |
| | 人才和文化氛围 |
| | 投资并购动向 |

方法论"三不要三要"原则写入分析引擎：
- 不只收集信息，要提出应对策略
- 不只看表面，要从解决方案/产品策略/人力策略发现问题
- 不只看已发生的，要预判未来可能的行动

#### ② 潜在竞争者（新进入者）

| 分析要素 | 电信行业示例 | 数据来源 |
|---------|------------|---------|
| 谁可能进入 | 科技公司（Google Fi）、卫星（Starlink）、公用事业公司建光纤 | 行业媒体 |
| 进入壁垒高低 | 频谱牌照、网络建设投资、监管审批 | 监管分析 |
| 进入后的影响 | 对价格、份额、竞争格局的冲击 | 分析师报告 |
| 当前的进入者 | 1&1（正在建网）——已经进来了 | 财报 + 新闻 |

#### ③ 替代品的威胁

| 替代关系 | 被替代的业务 | 替代品 | 数据来源 |
|---------|------------|-------|---------|
| OTT 替代通信 | 短信/语音 | WhatsApp/Signal/Teams | 用户行为数据 |
| OTT 替代 TV | 传统 Cable TV | Netflix/Disney+/YouTube | 行业报告 |
| Wi-Fi 替代蜂窝 | 移动数据 | 免费 Wi-Fi 热点 | 流量分析 |
| 云厂商替代 ICT | 传统 B2B ICT | AWS/Azure/GCP 直销 | B2B 市场分析 |
| FWA 替代固网 | DSL/Cable | 5G FWA | 运营商财报 |

#### ④ 供应商议价能力（新增）

| 供应商类别 | 议价能力 | 对运营商的影响 | 数据来源 |
|-----------|---------|--------------|---------|
| 网络设备商（华为/爱立信/诺基亚）| 高（寡头） | 设备采购价格、技术路线绑定 | 行业分析 |
| 芯片供应商 | 很高 | 网络设备和终端的供应瓶颈 | 供应链新闻 |
| 铁塔/基础设施 | 中-高 | 基站租金、选址受限 | 铁塔公司财报 |
| 光纤供应商 | 中 | 光缆价格影响 CAPEX | 行业价格指数 |
| IT/云平台 | 中 | BSS/OSS 系统升级依赖 | IT 供应商分析 |
| 内容提供商 | 低-中 | TV/内容采购成本 | 内容市场分析 |

#### ⑤ 买方议价能力（新增）

| 买方类别 | 议价能力 | 分析要点 | 数据来源 |
|---------|---------|---------|---------|
| 个人消费者 | 低（单个用户弱） | 但转网成本低，集体"用脚投票" | 流失率 / 转网数据 |
| 企业大客户 | 高 | 大额合同、竞标、多供应商策略 | B2B 市场分析 |
| 政府/公共采购 | 很高 | 合规要求、最低价中标、政策偏好 | 采购公告 |
| MVNO/批发客户 | 中-高 | 批发费率谈判、合同条款 | 批发市场分析 |
| 监管机构（间接） | 很高 | 费率管制、互联互通定价 | 监管公告 |

### 5.4 数据模型

```python
@dataclass
class PorterForce:
    """波特五力中的一个力量"""
    force_name: str           # "existing_competitors" / "new_entrants" / 
                              # "substitutes" / "supplier_power" / "buyer_power"
    force_level: str          # "high" / "medium" / "low"
    key_factors: list[dict]   # 每个因素 {name, description, impact, trend}
    implications: list[str]   # 对我们的启示
    
@dataclass
class CompetitorDeepDive:
    """单个同行对手的深度分析（增强版）"""
    operator: str
    
    # 基础体检（已有）
    financial_health: dict
    subscriber_health: dict
    network_status: dict
    
    # 增强维度（新增）
    product_portfolio: list[str]         # 产品系列
    new_product_pipeline: list[str]      # 新产品上市计划
    growth_strategy: str                 # 市场增长策略
    supply_chain_status: str             # 供应链和产能
    ecosystem_partners: list[str]        # 生态与合作
    core_control_points: list[str]       # 核心控制点
    business_model: str                  # 商业模式
    org_structure: str                   # 组织结构
    incentive_system: str                # 激励体系
    talent_culture: str                  # 人才与文化
    ma_activity: list[str]               # 投资并购
    
    # 诊断判断
    strengths: list[str]
    weaknesses: list[str]
    problems: list[str]
    
    # 三不要三要：预判
    likely_future_actions: list[str]     # 预判对手未来可能的行动
    
    # 对我的启示
    implications: list[CompetitorImplication]

@dataclass
class CompetitionInsight:
    """看竞争的完整输出"""
    # 波特五力总览
    five_forces: dict[str, PorterForce]
    overall_competition_intensity: str    # "intense" / "moderate" / "low"
    
    # 同行对手深度分析
    competitor_analyses: dict[str, CompetitorDeepDive]
    
    # 横向对比
    comparison_table: dict
    
    # 综合判断
    competitive_landscape: str
    key_message: str
```

### 5.5 PPT Slide

```
S12  看竞争 — 波特五力全景（五力图 + 每力的强度评估）
S13  看竞争 — 对手 A 深度分析
S14  看竞争 — 对手 B 深度分析
S15  看竞争 — 对手 C 深度分析
S16  看竞争 — 横向对比总结
S17  [可选] 新进入者 & 替代品威胁专题
```

---

## 六、04 看自己（Self）— 增强版

### 6.1 定位

> 第四看。在看清外部（趋势 + 市场 + 竞争）之后，审视自身的准备度。
> 不仅看经营数据，还要看组织能力、流程、人才、文化。

**已有设计**：经营体检 + 细分业务深度 + 网络深度 + 暴露面。
**本次新增**：组织内部维度 + BMC 商业模式画布 + 战略执行回顾。

### 6.2 方法论要求的问题清单

1. 企业的组织绩效 KPI 完成得怎样？
2. 造成**业绩差距**和**机会差距**的主要原因有哪些？
3. 企业的关键成功因素有哪些？如何强化核心竞争力？
4. 通过哪些方式来弥补企业的劣势？
5. 企业的市场份额和行业定位是怎样的？
6. 未来 3-5 年的战略意图是什么？
7. 企业的业务组合和能力组合有哪些？如何进一步协同？
8. 业务流程、组织架构如何更好地支撑业务发展？关键瓶颈有哪些？
9. 人才储备和培养是否足以支撑业务发展？
10. 企业文化和组织氛围需要调整吗？

### 6.3 新增维度

在已有的七个维度（经营、市场份额、网络、用户评价、管理团队、优劣势、暴露面）
基础上，增加以下维度：

#### ⑧ 业绩差距 vs 机会差距

```
业绩差距（Performance Gap）：
  实际经营结果 vs 计划目标 的差距
  → 我定的 KPI 完成了吗？差多少？差在哪？

机会差距（Opportunity Gap）：
  当前业务 vs 可以看见但尚未抓住的市场机会 的差距
  → 市场上有哪些机会我还没碰？为什么没碰？
```

#### ⑨ 业务组合分析

| 业务 | 收入占比 | 增速 | 利润贡献 | 战略角色 |
|------|---------|------|---------|---------|
| 移动 C 端 | 45% | +2% | 高 | 现金牛 |
| 固网宽带 | 20% | -3% | 中 | 需要转型 |
| B2B | 25% | +5% | 高 | 增长引擎 |
| TV | 5% | -1% | 低 | 待评估 |
| 批发 | 5% | +15% | 中 | 短期利好 |

#### ⑩ 组织与流程

| 分析要素 | 内容 | 数据来源 |
|---------|------|---------|
| 组织架构 | 事业部制 vs 矩阵式？最近有无重组？ | 年报 + 新闻 |
| 关键流程瓶颈 | 业务审批效率、网络部署速度、客户投诉处理时长 | 运营数据 / 财报披露 |
| 数字化运营成熟度 | 自助服务渗透率、数字化渠道占比、AI 应用 | 财报 + 行业对标 |

#### ⑪ 人才储备

| 分析要素 | 内容 | 数据来源 |
|---------|------|---------|
| 员工总数及趋势 | 增减趋势、人效（收入/人） | 财报 |
| 关键岗位 | 技术人才（5G/AI/云）、销售人才的充足度 | LinkedIn / 招聘数据 |
| 高管稳定性 | C-level 变动频率——频繁变动意味着战略不稳定 | executives 表 |
| 人才竞争力 | 雇主品牌（Glassdoor 评分）、薪资水平 | Glassdoor / Kununu |

#### ⑫ 企业文化与组织氛围

| 分析要素 | 内容 | 数据来源 |
|---------|------|---------|
| 文化特征 | 创新型 vs 稳健型？进取 vs 保守？ | 年报/CEO 讲话/媒体分析 |
| 员工满意度 | Glassdoor/Kununu 评分及趋势 | 公开评分平台 |
| 变革能力 | 过往重大变革的执行效果（如品牌重塑、组织重组） | 历史分析 |

#### ⑬ 战略执行回顾

| 分析要素 | 内容 |
|---------|------|
| 上一轮战略目标 | 之前定的战略方向是什么 |
| 执行完成度 | 哪些做到了、哪些没做到 |
| 战略意图更新 | 未来 3-5 年的战略意图是否需要调整 |

### 6.4 BMC 商业模式画布（简化版）

方法论推荐用 BMC 九宫格分析自身商业模式。
对电信运营商适配如下：

```
┌───────────────┬───────────────┬───────────────┬───────────────┬───────────────┐
│ 关键合作伙伴   │ 关键活动       │ 价值主张       │ 客户关系       │ 客户细分       │
│               │               │               │               │               │
│ 设备商         │ 网络建设/运维  │ 可靠的连接     │ 门店+App+客服  │ C 端消费者     │
│ 铁塔公司       │ 产品开发       │ 高速宽带       │ 融合捆绑       │ B2B 企业       │
│ 内容提供商     │ 客户服务       │ 企业数字化     │ 长约锁定       │ 批发客户       │
│ MVNO 合作方   │ 渠道管理       │ 一站式方案     │ 自助服务       │ 政府/公共      │
│               │               │               │               │               │
├───────────────┼───────────────┤               ├───────────────┼───────────────┤
│ 关键资源       │               │               │ 渠道           │               │
│               │               │               │               │               │
│ 频谱牌照       │               │               │ 线下门店       │               │
│ 网络基础设施   │               │               │ 线上商城       │               │
│ 品牌           │               │               │ 代理渠道       │               │
│ 客户基础       │               │               │ 企业直销       │               │
│               │               │               │               │               │
├───────────────┴───────────────┼───────────────┴───────────────┴───────────────┤
│ 成本结构                       │ 收入来源                                       │
│                               │                                               │
│ 网络 CAPEX / OPEX             │ 月租费 / 流量费 / 批发费                         │
│ 频谱费用                       │ B2B 解决方案收入                                │
│ 人力成本                       │ 设备销售                                       │
│ 内容采购                       │ 广告 / 增值服务                                 │
└───────────────────────────────┴───────────────────────────────────────────────┘
```

BMC 的价值：与竞对的 BMC 做对比，可以看出商业模式差异。

### 6.5 PPT Slide 更新

```
S18  看自己 — 经营总体体检（KPI 达成 + 业绩差距/机会差距）
S19  看自己 — 移动业务深度（数据 + 归因）
S20  看自己 — 固网宽带深度
S21  看自己 — B2B 企业业务深度
S22  看自己 — TV/融合/批发/其他
S23  看自己 — 网络深度分析
S24  看自己 — 业务组合 & 商业模式画布
S25  看自己 — 组织、人才与文化
S26  看自己 — 优势、短板与暴露面
```

---

## 七、SWOT 综合分析（桥梁）

### 7.1 定位

> 前四看的汇总枢纽。将外部环境（OT）和内部能力（SW）交叉匹配，
> 推导四种策略方向，为"看机会"提供结构化输入。

### 7.2 SWOT 来源映射

```
S（优势）← 看自己的 strengths
W（劣势）← 看自己的 weaknesses + exposure_points
O（机会）← 看趋势的 policy_opportunities + 看市场的 opportunities
T（威胁）← 看趋势的 threats + 看市场的 threats + 看竞争的 five_forces 压力
```

### 7.3 四象限策略

```
              优势 S                    劣势 W
         ┌──────────────────────┬──────────────────────┐
 机会 O  │  SO 策略              │  WO 策略              │
         │  利用优势抓住机会      │  弥补劣势以抓住机会    │
         │  （进攻型）            │  （改进型）            │
         │                      │                      │
         │  示例：利用 Cable 广   │  示例：加速光纤投资    │
         │  覆盖优势，抢先推 FWA  │  弥补自有率不足，参与  │
         │                      │  千兆战略补贴          │
         ├──────────────────────┼──────────────────────┤
 威胁 T  │  ST 策略              │  WT 策略              │
         │  利用优势抵御威胁      │  防御或退出            │
         │  （防御型）            │  （收缩型）            │
         │                      │                      │
         │  示例：用品牌和企业    │  示例：减少对 DSL 的   │
         │  客户优势防御 O2       │  投入，逐步退出        │
         │  价格战               │  低速宽带市场          │
         └──────────────────────┴──────────────────────┘
```

### 7.4 数据模型

```python
@dataclass
class SWOTAnalysis:
    """SWOT 综合分析"""
    strengths: list[str]          # 来自"看自己"
    weaknesses: list[str]         # 来自"看自己"
    opportunities: list[str]      # 来自"看趋势" + "看市场"
    threats: list[str]            # 来自"看趋势" + "看市场" + "看竞争"
    
    # 四象限策略
    so_strategies: list[str]      # 利用优势抓机会
    wo_strategies: list[str]      # 弥补劣势抓机会
    st_strategies: list[str]      # 利用优势防威胁
    wt_strategies: list[str]      # 劣势 + 威胁 → 退出或防守
    
    key_message: str

```

### 7.5 PPT Slide

```
S27  SWOT 综合分析（四象限矩阵 + 四种策略方向）
```

---

## 八、05 看机会（Opportunity）— SPAN 矩阵

### 8.1 定位

> 第五看。在 SWOT 分析之后，用 SPAN 矩阵对机会点做二维定位和筛选。

**已有设计**：机会点清单 + 优先级排序 + Addressable Market。
**本次升级**：引入 SPAN 矩阵做结构化评估。

### 8.2 SPAN 矩阵

```
        高  ┌──────────────────┬──────────────────┐
            │                  │                  │
  市        │  获取技能          │  增长/投资         │
  场        │  (Acquire Skills) │  (Grow/Invest)   │
  吸        │                  │                  │
  引        │  市场有吸引力      │  明星市场          │
  力        │  但我们竞争力弱    │  加大投入          │
            │  → 补能力再进入   │  → 高增长目标      │
            │                  │                  │
            ├──────────────────┼──────────────────┤
            │                  │                  │
            │  避免/退出         │  收获/重新细分     │
            │  (Avoid/Exit)    │  (Harvest)       │
            │                  │                  │
            │  既没吸引力       │  我们有竞争力      │
            │  我们又不擅长     │  但市场吸引力低    │
            │  → 撤退          │  → 收割利润       │
            │                  │                  │
        低  └──────────────────┴──────────────────┘
            低                                   高
                          竞争地位
```

### 8.3 市场吸引力评估（纵轴）

| 评估要素 | 权重 | 评分(1-5) | 数据来源 |
|---------|------|----------|---------|
| 市场规模 | 30% | | Addressable Market 数据 |
| 市场增长率（CAGR） | 25% | | 行业报告 |
| 盈利潜力 | 25% | | 竞争强度 + 利润率分析 |
| 战略价值 | 20% | | 与公司战略意图的匹配度 |

市场吸引力得分 = Σ(权重 × 评分)

### 8.4 竞争地位评估（横轴）

| 评估要素 | 权重 | 评分(1-5) | 数据来源 |
|---------|------|----------|---------|
| 市场份额 | 25% | | 看自己的市场份额数据 |
| 产品/服务满足度 | 25% | | $APPEALS 评估 |
| 品牌/渠道优势 | 25% | | 看自己 + 看竞争 |
| 技术/网络能力 | 25% | | 网络深度分析 |

竞争地位得分 = Σ(权重 × 评分)

### 8.5 每个机会点的定位

```python
@dataclass
class SPANPosition:
    """一个机会点在 SPAN 矩阵中的位置"""
    opportunity_name: str
    
    # 市场吸引力（纵轴）
    market_size_score: float
    market_growth_score: float
    profit_potential_score: float
    strategic_value_score: float
    market_attractiveness: float     # 加权总分
    
    # 竞争地位（横轴）
    market_share_score: float
    product_fit_score: float
    brand_channel_score: float
    tech_capability_score: float
    competitive_position: float      # 加权总分
    
    # 象限定位
    quadrant: str                    # "grow_invest" / "acquire_skills" / 
                                     # "harvest" / "avoid_exit"
    recommended_strategy: str        # 对应象限的策略建议
    
    # 气泡大小
    bubble_size: float               # 用 Addressable Market 大小决定气泡大小

@dataclass
class OpportunityInsight:
    """看机会的完整输出"""
    # SPAN 矩阵
    span_positions: list[SPANPosition]
    
    # 按象限分类
    grow_invest: list[SPANPosition]       # 明星：加大投入
    acquire_skills: list[SPANPosition]    # 问题：先补能力
    harvest: list[SPANPosition]           # 金牛：收割利润
    avoid_exit: list[SPANPosition]        # 瘦狗：退出
    
    # 机会窗口
    window_opportunities: list[dict]       # 有明确时间窗口的机会
    
    key_message: str
```

### 8.6 PPT Slide

```
S28  看机会 — SPAN 矩阵（气泡图：每个机会点一个气泡）
S29  看机会 — 机会点清单（优先级 + Addressable Market + 象限策略）
S30  [可选] Top 3 机会深度分析
```

---

## 九、更新后的完整 PPT Slide 清单

```
SECTION 0: 开场（4 页）
  S01  封面
  S02  目录
  S03  数据来源与质量概览
  S04  执行摘要

SECTION 1: 五看分析

  ── 01 看趋势 ──（2-3 页）
  S05  PEST 宏观环境仪表盘
  S06  行业环境分析（市场规模/增速/集中度/生命周期）
  S07  [可选] 重点趋势深度

  ── 02 看市场/客户 ──（3-4 页）
  S08  市场变化全景（机会 vs 威胁）
  S09  客户细分与需求分析
  S10  $APPEALS 竞争力评估
  S11  [可选] 重点客户群深度

  ── 03 看竞争 ──（4-6 页）
  S12  波特五力全景
  S13  对手 A 深度分析
  S14  对手 B 深度分析
  S15  对手 C 深度分析
  S16  横向对比总结
  S17  [可选] 新进入者 & 替代品专题

  ── 04 看自己 ──（7-9 页）
  S18  经营总体体检（KPI + 业绩差距/机会差距）
  S19  移动业务深度
  S20  固网宽带深度
  S21  B2B 企业业务深度
  S22  TV/融合/批发/其他
  S23  网络深度分析
  S24  业务组合 & 商业模式画布
  S25  组织、人才与文化
  S26  优势、短板与暴露面

  ── SWOT 综合 ──（1 页）
  S27  SWOT 矩阵 + 四种策略方向

  ── 05 看机会 ──（2-3 页）
  S28  SPAN 矩阵（气泡图）
  S29  机会点清单
  S30  [可选] Top 3 机会深度

SECTION 2: 经营详细数据（2 页）
  S31  季度经营分析
  S32  8/12 季度历史趋势

SECTION 3: 三定策略（3 页）
  S33  定策略
  S34  定重点工作
  S35  定执行

SECTION 4: 收尾（3 页）
  S36  总结与下一步
  S37  数据溯源附录
  S38  封底

初始完整版（Draft）：约 35-42 页
精简版（Final）：约 25-30 页
```

---

## 十、代码改造影响

| 变更 | 影响的文件 |
|------|-----------|
| 五看顺序调整 | `five_looks.py` 的 `run_five_looks()` 方法执行顺序；PPT 生成器的 slide 顺序 |
| "看趋势"命名 | 原 `look_at_macro()` 改为 `look_at_trends()`；InsightResult.category 从 "macro" 改为 "trends" |
| 客户分析新增 | `models.py` 增加 `CustomerSegment`, `APPEALSAssessment`；`look_at_market()` 升级为 `look_at_market_customer()` |
| 波特五力 | `models.py` 增加 `PorterForce`；`look_at_competitors()` 升级为 `look_at_competition()`；PPT 增加五力全景页 |
| 组织内部 | `models.py` 增加组织/人才/文化数据类；数据库增加 `org_capability` 表 |
| SWOT | `models.py` 增加 `SWOTAnalysis`；五看引擎增加 `synthesize_swot()` 方法；PPT 增加 SWOT 页 |
| SPAN | `models.py` 增加 `SPANPosition`；`look_at_opportunities()` 升级加入 SPAN 评分；PPT 增加 SPAN 气泡图页 |
