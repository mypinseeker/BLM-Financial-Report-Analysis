# BLM 五看分析框架详细设计
# Five Looks Analysis Framework — Detailed Design

---

## 总览

本文档是五看分析引擎的详细设计，基于与用户的逐项讨论定稿。
它定义了每一"看"要回答什么问题、看什么维度、数据从哪来、如何输出。

### 五看全景

| 看 | 本质 | 核心问题 |
|----|------|---------|
| 看市场 | 市场里的变化 | 发生了什么变化？对我是机会还是威胁？ |
| 看自己 | 健康体检 | 我现在的状况如何？哪里有隐患？ |
| 看对手 | 给对手做体检 | 对手在做什么？对我有什么启示？ |
| 看宏观 | 做生意的天气 | 外部大环境对我的经营有什么影响？ |
| 看机会 | 前四看的汇总 | 哪些机会值得抓？优先级是什么？ |

### 关键边界规则

- **看市场 vs 看宏观**：看市场 = 本地电信行业内已经发生的具体变化；看宏观 = 全球性的、方向性的外部大环境
- **看市场 vs 看对手**：看市场关注变化如何改变市场格局；看对手关注具体某家在干什么
- **看机会**：纯粹从前四看推导，不独立采集数据

### 五看结束后的人机共创环节

五看分析完成后，系统不直接进入"三定"，而是先与用户对话：
1. 呈现关键发现，请用户确认
2. 回答用户的疑问（基于溯源数据给出依据）
3. 接纳用户的补充和修正（用户可能有内部信息）
4. 达成共识后锁定结论，进入三定

**数据原则：用户反馈单独存储，不污染原始采集数据。**

---

## 一、看市场

### 1.1 核心问题

> **市场里发生了什么变化？每个变化对我是机会还是威胁？**
> 
> 运营商已经在这个市场里了，他没办法选择市场。
> 所以他需要看到市场里有没有新的变化，以及这些变化对他的影响。

### 1.2 与现有代码的差距

当前 `five_looks.py` 的 `look_at_market()` 是**静态快照**：市场有多大、份额多少、增长多少。
`germany_telecom_analysis.py` 的手工版本更丰富但仍然是快照。

需要升级为：**变化检测 + 影响评估**。

### 1.3 分析维度

#### 变化来源 A：同行驱动的变化（电信行业内）

| 变化类型 | 示例 | 数据来源 |
|---------|------|---------|
| 定价/套餐策略变化 | 某家打价格战、推不限量套餐 | 运营商官网、媒体报道 |
| 并购/合作 | 网络共享协议、MVNO 合作 | 新闻、监管公告 |
| 技术动作 | 率先商用 5G SA、大规模建光纤 | 运营商财报、技术媒体 |
| 市场格局变化 | 份额此消彼长、用户流向变化 | 财报交叉计算、监管机构数据 |

#### 变化来源 B：行业外玩家驱动的变化

| 变化类型 | 示例 | 数据来源 |
|---------|------|---------|
| OTT 侵蚀 | 视频、通信、企业服务被替代 | 行业报告、媒体 |
| 科技公司跨界 | AI 公司需要算力和网络、云厂商进入企业通信 | 行业媒体、分析师报告 |
| 新技术创造需求或替代 | AI 流量需求、FWA 替代固网、卫星互联网 | 行业报告、技术媒体 |
| 产业链变化 | 设备商/芯片供应链波动对网络建设的影响 | 行业媒体、供应商财报 |

#### 三个时间层

| 时间层 | 范围 | 数据来源 |
|-------|------|---------|
| **短期** | 本季度内发生的具体事件 | 新闻、财报、运营商公告 |
| **中期** | 半年到一年的可见趋势 | 行业报告、分析师研究 |
| **长期** | 结构性变迁（但不含监管/立法，那属于看宏观） | GSMA/Analysys Mason 长期预测 |

### 1.4 输出结构

```python
@dataclass
class MarketChange:
    """一个市场变化事件"""
    change_type: str          # "pricing" / "merger" / "technology" / "ott" / "new_entrant" / ...
    source: str               # "同行驱动" / "行业外玩家驱动"
    time_horizon: str         # "short_term" / "medium_term" / "long_term"
    description: str          # 变化描述
    impact_type: str          # "opportunity" / "threat" / "both"
    impact_description: str   # 对目标运营商的具体影响
    severity: str             # "high" / "medium" / "low"
    evidence: list[str]       # 支撑这个判断的数据点（关联溯源）

@dataclass
class MarketInsight:
    """看市场的完整输出"""
    # 基础市场数据（保留，作为背景）
    market_snapshot: dict               # 市场规模/份额/渗透率等
    
    # 核心输出：变化清单
    changes: list[MarketChange]         # 所有识别到的变化
    
    # 按影响分类的汇总
    opportunities: list[MarketChange]   # 对我有利的变化
    threats: list[MarketChange]         # 对我不利的变化
    
    # 综合判断
    market_outlook: str                 # "favorable" / "challenging" / "mixed"
    key_message: str                    # 一句话总结
```

### 1.5 PPT 输出页

**看市场（1-2 页）**

第 1 页 — 市场变化全景：
- 左侧：市场基础数据快照（规模/份额/增速）作为背景
- 右侧：变化清单，按"机会"和"威胁"分两列
- 每个变化标注时间层（短/中/长）和严重程度

第 2 页（可选）— 重点变化深度分析：
- 选取 2-3 个影响最大的变化做展开分析
- 每个包含：变化描述、数据支撑、对我的影响、建议行动

### 1.6 数据采集需求

| 需要的数据 | 采集器 | 数据库表 |
|-----------|--------|---------|
| 市场总量/份额/渗透率 | MarketDataCollector | market_totals |
| 用户流动/转网 | MarketDataCollector | user_flows |
| 资费变化 | MarketDataCollector | tariffs |
| 竞对动作（定价/并购/技术） | IntelligenceMonitor | intelligence_events |
| OTT/科技公司动态 | IntelligenceMonitor | intelligence_events |
| 行业趋势报告 | MacroEnvironmentCollector | intelligence_events |

---

## 二、看自己

### 2.1 核心问题

> **给自己做一次全面的健康检查和身体扫描。**
> 
> 既看客观指标（体检报告上的数字），
> 也做诊断判断（哪里强、哪里弱、哪里容易被攻击）。

### 2.2 与现有代码的差距

当前 `look_at_self()` 看的维度：收入、利润率、份额、竞争力评分、NPS。
`germany_telecom_analysis.py` 更丰富：收入拆解、ARPU、用户净增、网络差距、1&1 迁移。

需要升级的重点：
- **网络深度分析**（不只是覆盖率，要看技术结构、自主可控、演进策略）
- **动态暴露面**（不是静态短板，而是因经营动作而新出现的脆弱点）

### 2.3 分析维度（七个子维度）

#### ① 经营情况

| 指标 | 说明 | 数据来源 |
|------|------|---------|
| 总收入 / 服务收入 / 增速 | 整体经营健康度 | financial_quarterly |
| 收入拆解（移动/固网/B2B/TV/批发） | 哪些业务在增长、哪些在萎缩 | financial_quarterly |
| EBITDA / 利润率 / 增速 | 盈利能力 | financial_quarterly |
| ARPU 及趋势 | 用户价值变化 | subscriber_quarterly |
| OPEX / CAPEX 及占比 | 投资效率 | financial_quarterly |

#### ② 市场份额

| 指标 | 说明 |
|------|------|
| 各业务线的市场份额 | 移动/宽带/B2B/TV 分别的位置 |
| 份额变化趋势 | 是在涨还是在跌 |
| 与主要竞对的差距 | 跟第一名差多少、跟身后的差多少 |

#### ③ 网络（深度分析，三个层次）

**层次 1 — 现状：**

| 指标 | 说明 |
|------|------|
| 技术组合 | 我靠什么接入技术覆盖用户（Cable/DSL/Fiber/FWA），各占多少 |
| 各技术的竞争力 | 每种技术的体验上限，跟对手的技术比能不能打 |
| 自主可控程度 | 哪些是自建的、哪些是转售/租用的（如 Vodafone 光纤转售德电） |
| 转化效率 | Home Pass vs Home Connect 的差距（如德电光纤的问题） |
| 5G/4G 覆盖率 | 基础覆盖指标 |
| 网络质量评分 | 第三方测试结果（Connect/Chip/OpenSignal） |

**层次 2 — 演进策略：**

| 指标 | 说明 |
|------|------|
| 网络发展方向 | 5G SA vs NSA、Fiber 速率目标（1G vs 10G）、OpenRAN |
| 投资方向 | CAPEX 投到哪了——加固现有技术还是转型新技术 |
| 时间表 | 关键里程碑和目标日期 |
| 与竞对策略的差异 | 我的路线跟对手一样吗？激进还是保守？ |

**层次 3 — 策略影响：**

| 分析点 | 说明 |
|--------|------|
| 对消费者体验的影响 | 这个网络路线下，用户能得到什么体验 |
| 对 B2B 能力的影响 | 网络切片、边缘计算、低时延等能力 |
| 对成本结构的影响 | 网络技术选择对长期运营成本的影响 |

#### ④ 用户评价

| 指标 | 数据来源 |
|------|---------|
| NPS / CSAT | 公开调研、App Store 评分 |
| App 评分 | App Store / Google Play |
| 投诉率 | 监管机构投诉数据 |
| 社交媒体情感 | IntelligenceMonitor |

#### ⑤ 管理团队变化

| 指标 | 数据来源 |
|------|---------|
| C-level 人事变动 | executives 表 |
| 关键岗位更替 | 公司公告、LinkedIn |
| 变动的潜在影响 | 新高管的背景/风格可能带来的策略转向 |

#### ⑥ 优势与短板

综合 ①-⑤ 的数据，识别：
- **优势**：哪些维度的指标明显优于市场或竞对
- **短板**：哪些维度明显落后

#### ⑦ 容易被攻击的暴露面

这是"看自己"最有价值的部分——不是静态的弱点，而是**动态的、因经营动作而新暴露出来的脆弱点**。

判断逻辑：
```
某个经营动作（本身可能是好事）
    → 产生了副作用
        → 这个副作用被对手看到了
            → 对手可以利用这个副作用来攻击我
```

示例：
- Vodafone 迁入 1100 万 1&1 用户 → 网络负荷骤增 → 对手可以打"Vodafone 网络拥挤"
- 德电 Fiber Home Pass 很高但 Home Connect 低 → 投资回报率被质疑
- 某运营商大幅降价获客 → ARPU 下降 → 利润率恶化

### 2.4 输出结构

```python
@dataclass
class NetworkAnalysis:
    """网络深度分析"""
    # 现状
    technology_mix: dict          # {"cable": 70, "fiber_own": 5, "fiber_resale": 15, "dsl": 10}
    controlled_vs_resale: dict    # {"self_built": 75, "resale": 25}
    coverage: dict                # {"5g": 90, "4g": 99.5, "fiber_homepass": 24.0}
    quality_scores: dict          # {"connect_test": 78, "chip_test": 82}
    homepass_vs_connect: dict     # {"homepass_m": 24.0, "connect_m": 1.5, "conversion_pct": 6.3}
    
    # 演进策略
    evolution_strategy: dict      # {"5g": "NSA, SA planned 2026", "fiber": "10G target", ...}
    investment_direction: str     # "加固 Cable + 转售 Fiber"
    vs_competitors: str           # "比德电保守，比 O2 激进"
    
    # 影响评估
    consumer_impact: str
    b2b_impact: str
    cost_impact: str

@dataclass
class ExposurePoint:
    """一个容易被攻击的暴露面"""
    trigger_action: str           # 触发的经营动作 "迁入 1100 万 1&1 用户"
    side_effect: str              # 副作用 "网络负荷骤增"
    attack_vector: str            # 对手的攻击方式 "宣传 Vodafone 网络拥挤"
    severity: str                 # "high" / "medium" / "low"
    evidence: list[str]           # 支撑数据

@dataclass
class SelfInsight:
    """看自己的完整输出"""
    # 经营指标
    financial_health: dict
    revenue_breakdown: dict
    
    # 市场份额
    market_positions: dict
    share_trends: dict
    
    # 网络深度分析
    network: NetworkAnalysis
    
    # 用户评价
    customer_perception: dict
    
    # 管理团队
    leadership_changes: list[dict]
    
    # 综合判断
    strengths: list[str]
    weaknesses: list[str]
    exposure_points: list[ExposurePoint]
    
    # 整体健康评级
    health_rating: str            # "healthy" / "stable" / "concerning" / "critical"
    key_message: str
```

### 2.5 PPT 输出页

**看自己（2-3 页）**

第 1 页 — 经营体检报告：
- 关键财务指标卡片（收入/利润/增速/ARPU）
- 收入拆解（移动/固网/B2B/TV/批发）柱状图
- 市场份额位置

第 2 页 — 网络深度分析：
- 技术组合饼图（Cable/Fiber/DSL 占比）
- 自建 vs 转售比例
- 网络演进策略路线图
- 与竞对网络策略对比

第 3 页 — 优势、短板与暴露面：
- 左列：优势清单（绿色）
- 中列：短板清单（黄色）
- 右列：暴露面清单（红色）——每个标注触发动作和对手可能的攻击方式

### 2.6 数据采集需求

| 需要的数据 | 采集器 | 数据库表 |
|-----------|--------|---------|
| 财务数据 | FinancialReportCollector | financial_quarterly |
| 用户数据 | FinancialReportCollector | subscriber_quarterly |
| 网络基础设施 | FinancialReportCollector + MarketDataCollector | network_infrastructure |
| 竞争力评分 | MarketDataCollector | competitive_scores |
| 人事变动 | IntelligenceMonitor | executives |
| 用户评价/投诉 | MarketDataCollector + IntelligenceMonitor | competitive_scores + intelligence_events |

---

## 三、看对手

### 3.1 核心问题

> **站在对手的角度给他做一次体检，然后反推对我的启示。**
> 
> 要看他的优点、不足、遇到的问题。
> 他的问题就是我的机会；他特别牛的地方值得学习；
> 特别费解的地方值得深究。

### 3.2 分析结构

**每个对手单独分析，最后做横向对比。**

#### 每个对手的分析模板

| 维度 | 内容 | 数据来源 |
|------|------|---------|
| **财务体检** | 收入/利润/增速/趋势变化 | financial_quarterly |
| **用户体检** | 净增/流失/ARPU | subscriber_quarterly |
| **网络状态与演进** | 覆盖/技术路线/投资方向 | network_infrastructure |
| **优点/成功策略** | 哪些做得好、什么策略在奏效 | AI 基于财务+新闻综合判断 |
| **不足/恶化指标** | 哪些在变差、什么业务在萎缩 | 财务趋势分析 |
| **遇到的问题** | 具体困境（如 O2 失去批发收入） | 财报 + 新闻 |
| **对我的启示** | 见下方 | 综合推导 |

#### "对我的启示"四个维度

```python
@dataclass
class CompetitorImplication:
    """一个对手状况对我的启示"""
    implication_type: str    # "opportunity" / "threat" / "learning" / "puzzling"
    description: str
    evidence: list[str]
    suggested_action: str    # 初步的行动建议
```

- **机会（opportunity）**：对手的问题或弱点，我可以利用
  - 例：O2 因 1&1 迁走导致收入下降 → 我可以争取其动摇的用户
- **威胁（threat）**：对手的优势或动作，对我构成压力
  - 例：德电连续 35 季度 EBITDA 增长 → 差距在持续扩大
- **值得学习（learning）**：对手做得特别好的地方
  - 例：德电的 MagentaEINS 融合策略非常成功，值得借鉴
- **费解（puzzling）**：看不懂的操作，需要进一步观察
  - 例：某运营商在亏损的情况下仍在大规模补贴获客，背后逻辑是什么？

#### 横向对比页

| 对比维度 | 对手 A | 对手 B | 对手 C | 我 |
|---------|--------|--------|--------|-----|
| 收入 | | | | |
| 利润率 | | | | |
| 用户增长 | | | | |
| ARPU | | | | |
| 5G 覆盖 | | | | |
| 网络策略 | | | | |
| 战略方向 | | | | |
| 综合竞争态势 | | | | |

### 3.3 输出结构

```python
@dataclass
class CompetitorAnalysis:
    """单个对手的分析"""
    operator: str
    
    # 体检数据
    financial_health: dict
    subscriber_health: dict
    network_status: dict
    
    # 诊断判断
    strengths: list[str]          # 优点
    weaknesses: list[str]         # 不足
    problems: list[str]           # 遇到的问题
    
    # 对我的启示
    implications: list[CompetitorImplication]

@dataclass
class CompetitorInsight:
    """看对手的完整输出"""
    # 每个对手的详细分析
    individual_analyses: dict[str, CompetitorAnalysis]
    
    # 横向对比
    comparison_table: pd.DataFrame
    
    # 综合判断
    competitive_landscape: str    # 竞争格局总体判断
    key_message: str
```

### 3.4 PPT 输出页

- **每个对手 1 页**（详细分析 + 对我的启示）
- **横向对比 1 页**（关键指标对比表 + 竞争态势雷达图）

### 3.5 数据采集需求

与"看自己"基本对称——对手的财务、用户、网络数据都需要采集。
差异在于对手的数据只能来自公开信息，深度不如自己。

额外需要：
- 对手的新闻/动态（IntelligenceMonitor → intelligence_events）
- 对手的战略宣示（Earnings Call、Investor Day → strategy 表）

---

## 四、看宏观

### 4.1 核心问题

> **运营商做生意的天气：是好天气还是坏天气，
> 是可以预测的还是阴晴不定的。**
> 
> 运营商改变不了天气，但需要知道天气如何来决定行动。

### 4.2 与"看市场"的边界

- **看市场**：本地电信行业内已经发生的具体变化
- **看宏观**：全球性的、方向性的外部大环境

### 4.3 分析维度（四个子维度）

#### ① 宏观经济（大气候）

| 指标 | 影响 | 数据来源 |
|------|------|---------|
| GDP 增长率 | 消费者支出能力 | IMF / Destatis |
| 通胀率 | 定价空间 / 成本压力 | ECB / Destatis |
| 就业率 / 消费者信心 | 用户付费意愿 | Eurostat |
| 能源成本 | 网络运营成本 | Eurostat 能源价格指数 |
| 利率环境 | 融资成本 / 投资回报要求 | ECB |

#### ② 国家战略（政策风向）

| 方向 | 示例 | 数据来源 |
|------|------|---------|
| 数字化战略 | 德国千兆战略、光纤全覆盖目标 | 政府战略文件 |
| 产业政策 | 对 5G/AI/云计算的国家级推动、补贴 | 政府公告 |
| 安全战略 | 供应商限制政策（如对华为的限制） | 政府决策 |
| 复苏基金 | EU 复苏基金中的数字化投资部分 | EU/国家公告 |

#### ③ 监管策略（游戏规则）

| 方向 | 示例 | 数据来源 |
|------|------|---------|
| 电信监管 | 频谱分配/拍卖、网络共享规则、互联互通 | BNetzA 公告 |
| 网络安全立法 | NIS2 指令实施、数据保护（GDPR 执法） | BSI / EU 法规 |
| 税收政策 | 公司税/数字税变化 | 财政部公告 |
| 竞争法 | 并购审批规则、市场支配力审查 | 竞争管理局 |

#### ④ 行业大趋势（行业气候）

| 趋势 | 影响 | 数据来源 |
|------|------|---------|
| OTT 竞争演变 | 全球范围内的管道化趋势 | GSMA / 行业报告 |
| AI 对网络需求 | 算力/带宽的新增需求 | 行业报告 / 技术媒体 |
| 技术代际演进 | 5G→6G、Wi-Fi 7、卫星互联网 | 标准组织 / 行业报告 |
| 全球电信并购整合 | 行业整合趋势对本地市场的潜在影响 | 分析师报告 |
| 可持续发展要求 | ESG / 碳减排对网络建设的约束 | 监管 / 行业报告 |

### 4.4 输出结构

```python
@dataclass
class MacroFactor:
    """一个宏观因素"""
    category: str             # "economy" / "national_strategy" / "regulation" / "industry_trend"
    factor: str               # 具体因素描述
    direction: str            # "favorable" / "unfavorable" / "neutral" / "uncertain"
    impact_on_telecom: str    # 对电信行业的具体影响
    severity: str             # "high" / "medium" / "low"
    predictability: str       # "predictable" / "uncertain" / "volatile"
    evidence: list[str]

@dataclass
class MacroInsight:
    """看宏观的完整输出"""
    factors: list[MacroFactor]
    
    # 按维度汇总
    economy_outlook: str
    policy_outlook: str
    regulation_outlook: str
    industry_trend_outlook: str
    
    # 天气预报式的综合判断
    overall_weather: str      # "sunny" / "cloudy" / "stormy" / "unpredictable"
    key_message: str
```

### 4.5 PPT 输出页

**看宏观（1-2 页）**

第 1 页 — 宏观环境仪表盘：
- 四象限布局（经济 / 国家战略 / 监管 / 行业趋势）
- 每个象限：关键指标 + 方向（↑↓→）+ 对我的影响
- 顶部：天气图标（晴/阴/暴风雨）作为总体判断

第 2 页（可选）— 重点政策/趋势深度分析

### 4.6 数据采集需求

| 需要的数据 | 采集器 | 数据库表 |
|-----------|--------|---------|
| 经济指标 | MacroEnvironmentCollector | macro_environment |
| 政策/战略文件 | MacroEnvironmentCollector | macro_environment |
| 监管公告 | MacroEnvironmentCollector | macro_environment + intelligence_events |
| 行业趋势报告 | MacroEnvironmentCollector | intelligence_events |

---

## 五、看机会

### 5.1 核心问题

> **从前四看中提炼出具体的、可行动的机会点，量化并排序。**

### 5.2 推导逻辑

看机会不独立采集数据，而是从前四看中交叉推导：

```
看市场的变化 × 看自己的能力 × 看对手的弱点 × 看宏观的趋势
    → 哪些变化我有能力抓住 + 对手抓不住 + 大环境支持
        → 这就是机会
```

具体推导路径：

| 推导来源 | 机会类型 | 示例 |
|---------|---------|------|
| 市场变化 + 自身优势 | 我擅长的方向恰好市场在增长 | AI 流量需求增长 + 我有网络容量优势 |
| 对手弱点 + 自身能力 | 对手做不好的我能做 | O2 失去批发收入 + 我有网络承载能力 |
| 宏观政策 + 自身条件 | 政策支持的方向我有基础 | 国家复苏基金 + 我在光纤合作上有布局 |
| 市场变化 + 对手问题 | 竞争格局变动创造的缝隙 | 1&1 网络不稳定期 → 用户可能流动 |
| 自身短板被填补后 | 补短板带来的增量 | B2B 连接基础上拓展云/安全/数字化 |

### 5.3 输出结构

```python
@dataclass
class OpportunityItem:
    """一个机会点"""
    name: str                       # 机会名称
    description: str                # 机会描述
    
    # 推导来源
    derived_from: list[str]         # 来自哪些"看" ["market:OTT侵蚀", "self:B2B能力"]
    
    # 评估维度
    addressable_market: str         # Addressable Market（引用行业报告，无数据则留空）
    addressable_market_source: str  # 数据来源 "GSMA Intelligence 2025" 或 "数据暂缺"
    our_capability: str             # 我们做这件事的能力评估 "strong" / "moderate" / "weak"
    competition_intensity: str      # 竞争强度 "low" / "medium" / "high"
    time_window: str                # 时间窗口 "urgent" / "6-12 months" / "ongoing"
    
    # 优先级
    priority: str                   # "P0" / "P1" / "P2"
    priority_rationale: str         # 排序理由

@dataclass  
class OpportunityInsight:
    """看机会的完整输出"""
    opportunities: list[OpportunityItem]   # 按优先级排序的机会清单
    threats: list[str]                     # 威胁清单（前四看中识别的）
    
    key_message: str
```

**关于 Addressable Market 的铁律：**
- 有行业报告数据 → 引用并标注来源
- 没有数据 → `addressable_market: "数据暂缺"`, `addressable_market_source: ""`
- **绝对不编造数字**

### 5.4 PPT 输出页

**看机会（1-2 页）**

第 1 页 — 机会点清单：
- 优先级排序的表格
- 每个机会：名称 / Addressable Market / 能力匹配度 / 竞争强度 / 时间窗口
- 无 Addressable Market 数据的标注"待补充"

第 2 页（可选）— 前三大机会的深度分析：
- 每个机会的推导链（从哪个"看"推出来的）
- 初步的行动方向

---

## 六、人机共创环节

### 6.1 流程

```
五看分析完成
    ↓
系统呈现关键发现和结论
    ↓
用户逐项确认/质疑/修正/补充
    ↓
系统回答疑问（基于溯源数据）
    ↓
双方达成共识，锁定五看结论
    ↓
进入三定
```

### 6.2 数据存储

```python
@dataclass
class UserFeedback:
    """用户对某个分析结论的反馈"""
    look_category: str          # "market" / "self" / "competitor" / "macro" / "opportunity"
    finding_index: int          # 对应 findings 列表中的第几条
    
    feedback_type: str          # "confirmed" / "disputed" / "modified" / "supplemented"
    user_comment: str           # 用户的意见
    user_value: any             # 用户给出的修正值（如有）
    
    timestamp: datetime
```

```sql
-- 用户反馈表（独立于原始数据）
CREATE TABLE user_feedback (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id     TEXT NOT NULL,          -- 本次分析的唯一标识
    look_category   TEXT NOT NULL,
    finding_ref     TEXT NOT NULL,          -- 对应的发现/结论标识
    
    feedback_type   TEXT NOT NULL,          -- "confirmed" / "disputed" / "modified" / "supplemented"
    original_value  TEXT,                   -- AI 给出的原始结论
    user_comment    TEXT,                   -- 用户意见
    user_value      TEXT,                   -- 用户修正值
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6.3 最终输出件的合成逻辑

```
原始数据（数据库，不可改）
    + AI 分析结论（五看引擎输出）
        + 用户反馈（确认/修正/补充）
            = 最终版本的五看结论
                → 输入到三定
                → 生成 PPT
```

PPT 中对于用户修正过的结论，可以标注"已确认"或"已调整"。

---

## 七、现有代码改造清单

### 需要重构的文件

| 文件 | 改造内容 |
|------|---------|
| `src/blm/five_looks.py` | InsightResult 升级为支持新的输出结构；FiveLooksAnalyzer 的五个方法按新维度重写 |
| `src/blm/germany_telecom_analysis.py` | GermanyTelecomBLMAnalyzer 的五个方法按新维度重写；硬编码数据迁移到数据库后，改为从 db.export_*() 读取 |

### 需要新建的文件

| 文件 | 内容 |
|------|------|
| `src/blm/models.py` | 新数据类：MarketChange, NetworkAnalysis, ExposurePoint, CompetitorAnalysis, CompetitorImplication, MacroFactor, OpportunityItem, UserFeedback |
| `src/blm/interactive.py` | 人机共创交互模块：呈现结论、接收反馈、合成最终版本 |

### PPT 生成器扩展

| 文件 | 改造内容 |
|------|---------|
| `src/blm/ppt_generator_enhanced.py` | 按新的 PPT 页结构增加/修改 slide 生成方法；看自己增加网络深度页；看对手增加单独分析页；看机会增加 Addressable Market 列 |
