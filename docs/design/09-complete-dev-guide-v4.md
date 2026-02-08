# BLM Financial Report Analysis
# 完整工程化开发指南 v4（最终整合版）

> 本文档整合了前四轮讨论的全部设计决策，是给 Claude Code 的唯一开发参考文档。

---

## 一、产品定义

### 这个工具是什么

一个本地运行的电信运营商战略分析工具。用户给出指令，工具自动从互联网采集数据、
存入本地数据库、执行 BLM（五看三定）分析、输出专业 PPT/HTML 报告。

### 三句话说清楚核心逻辑

1. **用户按需订阅运营商**——只关注 Vodafone 就只存 Vodafone 的数据，关注整个德国市场就订阅德国四家。
2. **数据库逐季积累**——历史数据只采一次，后续只增量更新新季度，不重复采集。
3. **每个数字可溯源**——PPT 上任何数字都能追溯到原始来源 URL、PDF 页码、提取方式。

---

## 二、用户使用流程

```
# 首次使用：用户选择关注范围
blm-analyze init
> 选择市场: [x] Germany  [ ] China  [ ] USA
> Germany 运营商: [x] Vodafone Germany  [x] Deutsche Telekom  [x] O2  [ ] 1&1
> 确认订阅 3 家运营商，开始初始化数据库...
> ✓ 数据库创建: data/telecom.db
> ✓ 运营商注册完成
> 开始采集历史数据（最近 8 个季度）...
> ✓ Vodafone Germany: 8 季度财务 + 用户 + 竞争力数据
> ✓ Deutsche Telekom: 8 季度数据
> ✓ O2 Germany: 8 季度数据
> ✓ 德国市场宏观数据
> ✓ 近 90 天情报事件 42 条
> 初始化完成！数据库大小: 12MB

# 日常使用：直接分析
blm-analyze run "Vodafone Germany" --format ppt
> 数据库中已有最新数据 (Q3 FY26, updated 2 days ago)
> Running Five Looks analysis...
> Running Three Decisions...
> Generating PPT...
> ✓ output/blm_vodafone_germany_q3_fy26.pptx

# 季度更新：新季度财报出来后
blm-analyze update
> 检查更新...
> ⚠ Vodafone Germany: Q4 FY26 Trading Update 已发布 (2026-05-20)
> ⚠ Deutsche Telekom: Q1 2026 Report 已发布 (2026-05-15)
> 开始增量采集...
> ✓ Vodafone Germany Q4 FY26 数据入库 (28 个数据点, 全部 HIGH 置信度)
> ✓ Deutsche Telekom Q1 2026 数据入库

# 追加运营商：业务范围扩大
blm-analyze subscribe "1&1 AG"
> 注册运营商: 1&1 AG (Germany)
> 采集历史数据 (8 季度)...
> ✓ 完成

# 数据溯源：任意数字追根溯源
blm-analyze explain "Vodafone Germany" revenue_eur_billion "Q3 FY26"
> 📊 revenue_eur_billion = 3092 EUR million
>    📌 主来源: Vodafone Group Q3 FY26 Trading Update (2026-02-05), p.4
>       链接: https://investors.vodafone.com/...
>       提取: table_extraction, confidence 0.95
>       原文: "Total revenue €3,092m"
```

---

## 三、系统架构总览

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLI / Orchestrator                       │
│   blm-analyze init / subscribe / update / run / explain          │
└───────────┬───────────────────────────────────────┬─────────────┘
            │                                       │
    ┌───────▼───────────────────────┐    ┌──────────▼──────────┐
    │     Collection Layer          │    │   Analysis Layer     │
    │  (五看驱动的四类采集器)         │    │   (现有，不修改)       │
    │                               │    │                      │
    │  FinancialReportCollector     │    │  FiveLooksAnalyzer   │
    │  MarketDataCollector          │    │  ThreeDecisionsEngine│
    │  MacroEnvironmentCollector    │    │  GermanyTelecomBLM   │
    │  IntelligenceMonitor          │    │  Analyzer            │
    │                               │    │                      │
    │  每个采集器输出 TrackedValue   │    │  接口: dict[str,float]│
    └───────────┬───────────────────┘    └──────────▲──────────┘
                │                                    │
    ┌───────────▼───────────────────────────────────┐│
    │              SQLite Database                    ││
    │              data/telecom.db                    ││
    │                                                ││
    │  operators        (用户订阅的运营商)              ││
    │  financial_quarterly  (财务数据)                  ││
    │  subscriber_quarterly (用户数据)                  ││
    │  competitive_scores   (竞争力评分)                ││
    │  network_infrastructure (网络)                   ││
    │  tariffs             (资费)                      ││
    │  macro_environment   (宏观)                      ││
    │  executives          (高管)                      ││
    │  market_totals       (市场总量)                   ││
    │  user_flows          (用户流动)                   ││
    │  intelligence_events (情报, FTS5全文索引)          ││
    │  data_provenance     (溯源记录)                   ││
    │                                                ││
    │  export_for_analyzer() ─────────────────────────┘│
    │  导出为现有引擎兼容的 dict 格式                      │
    └─────────────────────────────┬────────────────────┘
                                  │
                       ┌──────────▼──────────┐
                       │   Output Layer       │
                       │   (现有，小幅扩展)     │
                       │                      │
                       │  BLMPPTGenerator     │
                       │  Enhanced (3264L)    │
                       │  ComprehensivePPT    │
                       │  HTML/JSON/TXT       │
                       │  + 溯源附录页 (新增)   │
                       └──────────────────────┘
```

---

## 四、用户订阅模型

核心理念：**数据库是空的白板，用户按需填充。**

```python
# src/database/subscription.py

class SubscriptionManager:
    """管理用户关注哪些运营商和市场"""

    def init_workspace(self, markets: list[str], operators: list[str]):
        """首次初始化：用户选择关注范围
        
        示例:
            manager.init_workspace(
                markets=["germany"],
                operators=["vodafone_germany", "deutsche_telekom", "o2_germany"]
            )
        """
        # 1. 在 operators 表中注册选中的运营商
        # 2. 创建该市场的宏观环境记录框架
        # 3. 触发历史数据回填（最近 8 季度）

    def subscribe(self, operator_id: str):
        """追加订阅一个运营商
        
        场景：用户分析德国市场时发现需要看 1&1 的数据
        - 注册运营商
        - 回填历史数据
        - 不影响已有数据
        """

    def unsubscribe(self, operator_id: str):
        """取消订阅（不删数据，只标记 is_active=FALSE）"""

    def get_subscribed_operators(self, market: str = None) -> list[dict]:
        """获取用户当前订阅的运营商列表"""

    def get_subscribed_markets(self) -> list[str]:
        """获取用户关注的市场列表"""
```

### 预置运营商目录

用户不需要手动输入运营商信息。系统内置目录（从现有 `GLOBAL_OPERATORS` 扩展），用户只需选择：

```python
# src/database/operator_directory.py

OPERATOR_DIRECTORY = {
    # Germany
    "vodafone_germany": {
        "display_name": "Vodafone Germany",
        "parent": "Vodafone Group",
        "country": "Germany", "region": "Europe", "market": "germany",
        "type": "challenger",
        "ir_url": "https://investors.vodafone.com/",
        "fiscal_year_end": "March",
        "currency": "EUR",
    },
    "deutsche_telekom": {
        "display_name": "Deutsche Telekom",
        "parent": "Deutsche Telekom AG",
        "country": "Germany", "region": "Europe", "market": "germany",
        "type": "incumbent",
        "ir_url": "https://www.telekom.com/en/investor-relations",
        "fiscal_year_end": "December",
        "currency": "EUR",
    },
    # ... 24+ 运营商，覆盖现有 GLOBAL_OPERATORS 全部
}
```

---

## 五、数据采集设计（五看驱动）

### 原则回顾

> **五看看什么，数据采集就要覆盖什么。**
> 不限于 IR 网站——还包括监管机构、媒体、分析师、政策等公开信息。

### 四类采集器与五看的映射

| 采集器 | 服务的"看" | 采集什么 |
|--------|-----------|---------|
| **FinancialReportCollector** | 看自己 + 看对手 | 运营商财报 PDF/PPT/Excel/Earnings Call |
| **MarketDataCollector** | 看市场 | 市场总量、份额、资费、网络质量排名 |
| **MacroEnvironmentCollector** | 看宏观 | GDP、监管政策、网络安全立法、税收 |
| **IntelligenceMonitor** | 看对手(动态) + 看机会 | 媒体报道、人事变动、网络事故、分析师评价 |

### 采集器与数据库的关系

每个采集器只负责：
1. 从互联网获取原始数据
2. 解析成结构化 `TrackedValue`（带溯源）
3. 写入 SQLite 数据库对应表

**采集器不直接与分析引擎交互。** 分析引擎只读数据库。

```
互联网 → Collector → TrackedValue → SQLite DB → export_for_analyzer() → 分析引擎
```

### 采集范围由用户订阅决定

```python
class DataCollectionOrchestrator:
    """根据用户订阅范围调度采集"""

    def collect_all(self):
        """采集用户订阅的所有运营商数据"""
        subscribed = self.subscription.get_subscribed_operators()
        markets = self.subscription.get_subscribed_markets()
        
        for op in subscribed:
            self.financial_collector.collect(op["operator_id"])
        
        for market in markets:
            self.market_collector.collect(market)
            self.macro_collector.collect(market)
        
        for op in subscribed:
            self.intelligence_monitor.collect(op["operator_id"])

    def collect_incremental(self):
        """增量采集：只采新季度数据"""
        for op in self.subscription.get_subscribed_operators():
            latest_in_db = self.db.get_latest_period(op["operator_id"])
            latest_available = self.financial_collector.check_latest(op["operator_id"])
            if latest_available > latest_in_db:
                self.financial_collector.collect(op["operator_id"], period=latest_available)
```

---

## 六、数据溯源设计

### 核心数据类型

```python
@dataclass
class TrackedValue:
    """每一个数据点 = 值 + 溯源信息"""
    value: any
    field_name: str
    operator: str = None
    period: str = None
    unit: str = None

    # 主来源
    primary_source: SourceReference = None
    # 备选来源（如有多个来源给出不同值）
    alternative_sources: list[SourceReference] = field(default_factory=list)
    # 冲突解决理由
    conflict_resolution: str = None
    # 计算依赖（如果是派生值）
    derived_from: list['TrackedValue'] = field(default_factory=list)
    derivation_formula: str = None

@dataclass
class SourceReference:
    """一个来源的完整信息"""
    source_type: str        # "financial_report_pdf" / "news_article" / ...
    url: str = None         # 原始链接
    document_name: str = None
    publisher: str = None
    publication_date: datetime = None
    page_number: int = None
    section: str = None
    extraction_method: str = None
    extraction_confidence: float = 1.0
    raw_text: str = None
    confidence: str = "high"  # "high" / "medium" / "low" / "estimated"
    expires_at: datetime = None
```

### 溯源存入数据库

采集器产出 `TrackedValue` → 值写入业务表 → 溯源信息写入 `data_provenance` 表。

### 冲突解决

当多个来源给出不同值时，`ConflictResolver` 按以下优先级自动选择：

```
运营商官方财报 PDF (100分) > 监管机构数据 (95分) > Excel 数据表 (95分) 
> 投资者 PPT (90分) > Earnings Call (85分) > 官方新闻稿 (80分) 
> 分析师报告 (60分) > 媒体报道 (50分) > AI 提取 (40分)
```

同类型中，更新的优先于更旧的。

### 时效性管理

不同数据有不同保鲜期：
- 财务季报数据：90 天（下个季报前有效）
- 资费数据：30 天（随时可能变）
- 新闻情报：7 天
- 人事变动：365 天

过期数据标记为 `stale`，超过 30 天未更新标记为 `expired`。

---

## 七、数据库 Schema（核心表）

```sql
-- 运营商（用户订阅后才有记录）
CREATE TABLE operators (
    operator_id     TEXT PRIMARY KEY,
    display_name    TEXT NOT NULL,
    parent_company  TEXT,
    country         TEXT NOT NULL,
    region          TEXT NOT NULL,
    operator_type   TEXT NOT NULL,
    market          TEXT,
    ir_url          TEXT,
    currency        TEXT DEFAULT 'EUR',
    is_active       BOOLEAN DEFAULT TRUE,
    subscribed_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 季度财务数据（对应 FINANCIAL_DATA + REVENUE_DATA + PROFITABILITY_DATA + INVESTMENT_DATA）
CREATE TABLE financial_quarterly (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id     TEXT NOT NULL REFERENCES operators(operator_id),
    period          TEXT NOT NULL,
    period_end      DATE,
    -- 收入
    total_revenue REAL, service_revenue REAL, service_revenue_growth REAL,
    mobile_service_revenue REAL, mobile_service_growth REAL,
    fixed_service_revenue REAL, fixed_service_growth REAL,
    b2b_revenue REAL, b2b_growth REAL,
    tv_revenue REAL, wholesale_revenue REAL,
    -- 利润
    ebitda REAL, ebitda_margin REAL, ebitda_growth REAL,
    net_income REAL, profit_margin REAL,
    -- 投资
    opex REAL, opex_to_revenue REAL, capex REAL, capex_to_revenue REAL,
    employees_k REAL,
    -- 元数据
    currency TEXT DEFAULT 'EUR', unit TEXT DEFAULT 'million',
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(operator_id, period)
);

-- 季度用户数据（对应 MOBILE/FIXED/TV/B2B 全部用户维度）
CREATE TABLE subscriber_quarterly (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id TEXT NOT NULL REFERENCES operators(operator_id),
    period TEXT NOT NULL,
    -- 移动
    mobile_total_m REAL, mobile_consumer_m REAL, mobile_iot_m REAL,
    mobile_postpaid_m REAL, mobile_prepaid_m REAL,
    postpaid_ratio REAL, mobile_arpu REAL, mobile_churn REAL,
    mobile_net_adds_k REAL, new_customer_arpu_growth REAL,
    -- 固网
    broadband_total_m REAL, broadband_fiber_m REAL,
    broadband_cable_m REAL, broadband_dsl_m REAL,
    broadband_arpu REAL, broadband_net_adds_k REAL,
    -- TV & FMC
    tv_subs_m REAL, tv_net_adds_k REAL,
    fmc_subs_m REAL, fmc_penetration REAL,
    -- B2B
    b2b_connections_k REAL, iot_connections_m REAL,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(operator_id, period)
);

-- 竞争力评分
CREATE TABLE competitive_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id TEXT NOT NULL, period TEXT NOT NULL,
    dimension TEXT NOT NULL, score REAL NOT NULL,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(operator_id, period, dimension)
);

-- 网络基础设施
CREATE TABLE network_infrastructure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id TEXT NOT NULL, period TEXT NOT NULL,
    coverage_5g_pct REAL, coverage_4g_pct REAL,
    base_stations_5g INTEGER, ran_vendor TEXT,
    sa_status TEXT, spectrum_json TEXT,
    cable_homes_m REAL, fiber_homes_m REAL,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(operator_id, period)
);

-- 资费
CREATE TABLE tariffs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id TEXT NOT NULL, captured_date DATE NOT NULL,
    product_type TEXT, tier TEXT, plan_name TEXT,
    data_gb REAL, speed_mbps REAL, price_eur REAL,
    has_5g BOOLEAN, promotion TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 宏观环境
CREATE TABLE macro_environment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT NOT NULL, period TEXT NOT NULL,
    gdp_growth REAL, inflation REAL,
    regulatory_text TEXT, cybersecurity_text TEXT,
    tax_policy_text TEXT, energy_cost_index REAL,
    digital_economy_pct REAL, competitive_intensity TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(country, period)
);

-- 高管
CREATE TABLE executives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id TEXT NOT NULL, role TEXT, name TEXT,
    since_date DATE, background TEXT,
    is_current BOOLEAN DEFAULT TRUE,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 战略
CREATE TABLE strategy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id TEXT NOT NULL, period TEXT NOT NULL,
    priorities_json TEXT, initiatives_json TEXT,
    guidance TEXT, achievements_json TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(operator_id, period)
);

-- 市场总量
CREATE TABLE market_totals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market TEXT NOT NULL, period TEXT NOT NULL,
    total_mobile_m REAL, total_broadband_m REAL,
    total_revenue_m REAL, adoption_5g_pct REAL,
    fiber_penetration_pct REAL, market_shares_json TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(market, period)
);

-- 用户流动
CREATE TABLE user_flows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market TEXT, period TEXT,
    from_operator TEXT, to_operator TEXT,
    flow_k REAL,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(market, period, from_operator, to_operator)
);

-- 情报事件（含全文搜索）
CREATE TABLE intelligence_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id TEXT, market TEXT,
    event_type TEXT NOT NULL,
    event_date DATE NOT NULL,
    headline TEXT NOT NULL,
    summary TEXT, full_text TEXT,
    sentiment TEXT, severity TEXT,
    source_name TEXT, source_url TEXT, source_type TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE VIRTUAL TABLE intelligence_fts USING fts5(
    headline, summary, full_text,
    content=intelligence_events, content_rowid=id
);

-- 数据溯源（每个数据点的来源链）
CREATE TABLE data_provenance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL, record_id INTEGER NOT NULL,
    field_name TEXT NOT NULL,
    source_type TEXT, source_url TEXT, document_name TEXT,
    publisher TEXT, publication_date DATE,
    page_number INTEGER, section TEXT,
    extraction_method TEXT, extraction_confidence REAL DEFAULT 1.0,
    raw_text TEXT,
    confidence TEXT DEFAULT 'high',
    expires_at DATE,
    is_primary BOOLEAN DEFAULT TRUE,
    alternative_value TEXT, conflict_resolution TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_prov_lookup ON data_provenance(table_name, record_id, field_name);
```

---

## 八、数据库 → 分析引擎的桥接

现有分析引擎和 PPT 生成器**完全不修改**。数据库提供 `export_*` 方法输出兼容格式：

```python
class TelecomDatabase:

    def export_for_germany_analyzer(self, period: str) -> tuple:
        """输出 (financial_data_dict, competitive_scores_dict, macro_data_dict)
        格式与 germany_telecom_analysis.py 中的硬编码字典完全一致"""

    def export_historical_for_ppt(self, market: str, n_quarters: int = 8) -> dict:
        """输出 REVENUE_DATA_8Q / PROFITABILITY_DATA_8Q / USER_DATA_8Q 等
        格式与 germany_market_comprehensive_data.py 完全一致"""

    def export_for_five_looks(self, market: str, period: str) -> dict[str, pd.DataFrame]:
        """输出 {market, financial, competitive, macro, segments, customer} DataFrames
        格式与 FiveLooksAnalyzer.__init__ 的 data 参数完全一致"""
```

---

## 九、开发阶段划分

### Phase 0: 工程基础 ⏱️ 1 天

```
新建文件:
  CLAUDE.md
  src/database/__init__.py
  src/database/db.py              ← SQLite 数据库核心
  src/database/schema.sql         ← 建表 SQL
  src/database/subscription.py    ← 用户订阅管理
  src/database/operator_directory.py ← 预置运营商目录
  src/collectors/__init__.py
  src/collectors/provenance.py    ← TrackedValue + SourceReference
  src/collectors/conflict_resolver.py
  src/collectors/freshness.py
  tests/test_database.py
  tests/test_provenance.py
```

### Phase 1: 财务报告采集 + 入库 ⏱️ 5-7 天

```
新建文件:
  src/collectors/base.py                     ← 采集器基类（缓存/限速/重试）
  src/collectors/financial_report_collector.py
  src/collectors/parsers/__init__.py
  src/collectors/parsers/pdf_financial_parser.py
  src/collectors/parsers/pptx_parser.py
  src/collectors/parsers/excel_parser.py
  src/collectors/parsers/transcript_parser.py
  config/ir_sources.yaml
  tests/test_financial_collector.py
```

### Phase 2: 市场 + 宏观采集 ⏱️ 4-5 天

```
新建文件:
  src/collectors/market_data_collector.py
  src/collectors/macro_environment_collector.py
  config/data_sources.yaml
  tests/test_market_collector.py
  tests/test_macro_collector.py
```

### Phase 3: 情报监控 + 编排器 + AI ⏱️ 4-5 天

```
新建文件:
  src/collectors/intelligence_monitor.py
  src/orchestrator.py
  src/ai/__init__.py
  src/ai/claude_analyzer.py
  tests/test_intelligence.py
  tests/test_orchestrator.py
```

### Phase 4: 集成 + CLI + 质量 ⏱️ 3 天

```
修改文件:
  src/blm/cli.py                 ← 添加 init/subscribe/update/run/explain 命令
  src/blm/ppt_generator_enhanced.py ← 添加溯源附录页（小幅扩展）
新建文件:
  tests/test_e2e.py
更新:
  README.md
  requirements.txt
```

---

## 十、文件结构

```
BLM-Financial-Report-Analysis/
├── CLAUDE.md                              ← Phase 0
├── .env.example
├── config/
│   ├── default.yaml
│   ├── ir_sources.yaml                    ← Phase 1
│   └── data_sources.yaml                  ← Phase 2
├── src/
│   ├── orchestrator.py                    ← Phase 3
│   ├── database/                          ← Phase 0 (新建)
│   │   ├── __init__.py
│   │   ├── db.py                          ← SQLite 核心
│   │   ├── schema.sql
│   │   ├── subscription.py                ← 用户订阅管理
│   │   └── operator_directory.py          ← 预置运营商目录
│   ├── collectors/                        ← Phase 1-3 (新建)
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── provenance.py                  ← TrackedValue 体系
│   │   ├── conflict_resolver.py
│   │   ├── freshness.py
│   │   ├── financial_report_collector.py
│   │   ├── market_data_collector.py
│   │   ├── macro_environment_collector.py
│   │   ├── intelligence_monitor.py
│   │   └── parsers/
│   │       ├── pdf_financial_parser.py
│   │       ├── pptx_parser.py
│   │       ├── excel_parser.py
│   │       └── transcript_parser.py
│   ├── ai/                                ← Phase 3 (新建)
│   │   ├── __init__.py
│   │   └── claude_analyzer.py
│   ├── blm/                               ← 现有代码 (基本不动)
│   │   ├── five_looks.py
│   │   ├── three_decisions.py
│   │   ├── germany_telecom_analysis.py
│   │   ├── germany_market_comprehensive_data.py
│   │   ├── ppt_generator_enhanced.py
│   │   ├── comprehensive_analysis_ppt.py
│   │   ├── telecom_data.py
│   │   ├── report_generator.py
│   │   ├── ppt_generator.py
│   │   ├── ppt_charts.py
│   │   ├── canva_integration.py
│   │   └── cli.py                         ← Phase 4 扩展
│   ├── data/
│   ├── analysis/
│   ├── visualization/
│   └── reports/
├── tests/
│   ├── test_database.py                   ← Phase 0
│   ├── test_provenance.py                 ← Phase 0
│   ├── test_financial_collector.py        ← Phase 1
│   ├── test_market_collector.py           ← Phase 2
│   ├── test_macro_collector.py            ← Phase 2
│   ├── test_intelligence.py              ← Phase 3
│   ├── test_orchestrator.py              ← Phase 3
│   ├── test_e2e.py                       ← Phase 4
│   └── ... (现有测试保留)
└── data/
    ├── telecom.db                         ← 用户本地数据库
    ├── cache/                             ← 采集缓存
    ├── raw/
    └── output/
```

---

## 十一、依赖

```
# requirements.txt

# === 现有 ===
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
openpyxl>=3.1.0
pdfplumber>=0.9.0
jinja2>=3.1.0
click>=8.1.0
pyyaml>=6.0
pytest>=7.3.0
python-pptx>=0.6.21

# === 新增 ===
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
feedparser>=6.0.0
rich>=13.0.0
python-dotenv>=1.0.0
anthropic>=0.18.0      # 可选
```

SQLite 是 Python 内置的，不需要额外安装。

---

## 十二、验收标准

| Phase | 验收标准 |
|-------|---------|
| 0 | `blm-analyze init` 能交互式创建数据库并注册运营商 |
| 0 | `TrackedValue.explain()` 输出完整溯源说明 |
| 1 | `blm-analyze update` 能从 IR 网站下载并解析财报 PDF，数据入库 |
| 2 | 市场总量和宏观数据入库，`export_for_germany_analyzer()` 输出与硬编码格式一致 |
| 3 | `blm-analyze run "Vodafone Germany" --format ppt` 端到端从数据库读数据生成 PPT |
| 4 | `blm-analyze explain "Vodafone Germany" revenue_eur_billion "Q3 FY26"` 返回完整溯源 |

---

## 十三、Phase 0 的 Claude Code 提示词

合并分支后，在 Claude Code 中执行以下指令启动 Phase 0：

```
请阅读 CLAUDE.md 了解项目概况。

然后创建以下文件：

1. src/database/schema.sql — 包含所有 CREATE TABLE 语句
   参考本文档第七节的完整 Schema。

2. src/database/db.py — TelecomDatabase 类
   - __init__(db_path="data/telecom.db")：创建数据库并初始化表
   - 使用 sqlite3，支持 WAL 模式和外键
   - upsert_financial / upsert_subscribers：写入/更新数据
   - get_financial_history / get_market_financials：查询数据
   - export_for_germany_analyzer(period)：输出与现有硬编码格式兼容的字典
   - export_historical_for_ppt(market, n_quarters)：输出 8 季度历史格式
   - explain_field(table, operator, period, field)：查询溯源
   - get_data_freshness_report()：数据新鲜度报告

3. src/database/subscription.py — SubscriptionManager 类
   - init_workspace(markets, operators)
   - subscribe(operator_id) / unsubscribe(operator_id)
   - get_subscribed_operators(market=None)

4. src/database/operator_directory.py — OPERATOR_DIRECTORY 字典
   从 src/blm/telecom_data.py 的 GLOBAL_OPERATORS 扩展，
   加上 market/ir_url/fiscal_year_end/currency 等字段。
   同时包含 src/blm/germany_telecom_analysis.py 中的德国四家运营商。

5. src/collectors/provenance.py — TrackedValue + SourceReference 数据类
   参考本文档第六节。

6. src/collectors/conflict_resolver.py — ConflictResolver
   参考本文档第六节冲突解决部分。

7. src/collectors/freshness.py — FreshnessPolicy

8. tests/test_database.py — 测试数据库 CRUD、export 格式兼容性
9. tests/test_provenance.py — 测试溯源记录和查询

关键约束：
- export_for_germany_analyzer() 的输出必须能直接替代
  germany_telecom_analysis.py 中的 FINANCIAL_DATA_Q3_FY26 字典，
  让 GermanyTelecomBLMAnalyzer 无需修改即可使用。
- export_historical_for_ppt() 的输出必须与
  germany_market_comprehensive_data.py 中的 REVENUE_DATA_8Q 等格式一致，
  让 ComprehensiveAnalysisPPT 无需修改即可使用。
```
