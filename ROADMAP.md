# ROADMAP.md — 五看分析引擎开发路标
# Phase 1: 五看重构（三定在 Phase 2）

---

## 里程碑总览

```
M0  项目基础设施          ████░░░░░░░░░░░░░░░░  预计 1 天
M1  数据层               ████████░░░░░░░░░░░░  预计 2 天
M2  五看分析引擎          ████████████████░░░░  预计 3-4 天
M3  输出层               ████████████████████  预计 2-3 天
M4  集成测试 & 联调       ████████████████████  预计 1-2 天
                                              ──────────
                                              总计 9-12 天
```

---

## M0: 项目基础设施

> 目标：搭建新的项目骨架，设计文档入库，旧代码归档

### 任务清单

| ID | 任务 | 产出文件 | 依赖 |
|----|------|---------|------|
| M0.1 | 创建新目录结构 | `src/database/`, `src/models/`, `src/output/` | — |
| M0.2 | 设计文档复制到 `docs/design/` | 12 份 .md 文件 | — |
| M0.3 | CLAUDE.md 和 ROADMAP.md 放到项目根目录 | 2 个文件 | — |
| M0.4 | 更新 requirements.txt | 添加缺失依赖 | — |
| M0.5 | 旧代码标记为 legacy（移到 `src/blm/_legacy/`） | 不删除，只移动 | — |

---

## M1: 数据层

> 目标：SQLite 数据库 + 运营商注册表 + 财年对齐 + 种子数据

### M1.1 数据库 Schema

| ID | 任务 | 产出文件 |
|----|------|---------|
| M1.1a | 编写完整 DDL（所有表） | `src/database/schema.sql` |
| M1.1b | 数据库初始化脚本 | `src/database/init_db.py` |

核心表清单（参考设计文档 09）：
- `operators` — 运营商注册表
- `subscriptions` — 用户订阅配置
- `financial_quarterly` — 财务季度数据（含 calendar_quarter）
- `subscriber_quarterly` — 用户季度数据
- `network_infrastructure` — 网络基础设施
- `tariffs` — 资费数据
- `competitive_scores` — 竞争力评分
- `intelligence_events` — 新闻/事件/动态
- `executives` — 高管信息
- `macro_environment` — 宏观环境（PEST）
- `earnings_call_highlights` — 财报电话会要点
- `source_registry` — 数据来源注册表
- `data_provenance` — 数据溯源记录
- `user_feedback` — 用户反馈

### M1.2 PeriodConverter

| ID | 任务 | 产出文件 |
|----|------|---------|
| M1.2a | PeriodConverter 类 + 预置转换器 | `src/database/period_utils.py` |
| M1.2b | 单元测试 | `tests/test_period_utils.py` |

关键逻辑：Vodafone Q3 FY26 ↔ CQ4_2025 ↔ DT Q4 2025

### M1.3 运营商注册表

| ID | 任务 | 产出文件 |
|----|------|---------|
| M1.3a | 运营商目录 + 财年配置 | `src/database/operator_directory.py` |

初始运营商：Vodafone Germany, Deutsche Telekom, Telefónica O2, 1&1 AG

### M1.4 TelecomDatabase

| ID | 任务 | 产出文件 |
|----|------|---------|
| M1.4a | 数据库访问类（CRUD + 查询 + 对比） | `src/database/db.py` |
| M1.4b | 种子数据脚本（从现有硬编码数据迁移） | `src/database/seed_germany.py` |
| M1.4c | 单元测试 | `tests/test_database.py` |

种子数据来源：`germany_telecom_analysis.py` + `germany_market_comprehensive_data.py` 中的硬编码数据

---

## M2: 五看分析引擎

> 目标：五看 + SWOT 的分析引擎，从数据库读数据，输出结构化结果

### M2.0 数据模型

| ID | 任务 | 产出文件 |
|----|------|---------|
| M2.0a | 看趋势数据模型 | `src/models/trend.py` |
| M2.0b | 看市场/客户数据模型 | `src/models/market.py` |
| M2.0c | 看竞争数据模型 | `src/models/competition.py` |
| M2.0d | 看自己数据模型 | `src/models/self_analysis.py` |
| M2.0e | SWOT 数据模型 | `src/models/swot.py` |
| M2.0f | 看机会数据模型 | `src/models/opportunity.py` |
| M2.0g | 溯源数据模型 | `src/models/provenance.py` |
| M2.0h | 用户反馈数据模型 | `src/models/feedback.py` |

### M2.1 看趋势（Trend）

| ID | 任务 | 产出文件 |
|----|------|---------|
| M2.1a | PEST 分析引擎 | `src/blm/look_at_trends.py` |
| M2.1b | 行业环境分析（市场规模/增速/集中度） | 同上 |
| M2.1c | 单元测试 | `tests/test_look_at_trends.py` |

输入：`macro_environment` 表 + `intelligence_events` 表
输出：`TrendAnalysis` 对象

### M2.2 看市场/客户（Market/Customer）

| ID | 任务 | 产出文件 |
|----|------|---------|
| M2.2a | 市场变化检测引擎 | `src/blm/look_at_market_customer.py` |
| M2.2b | 客户细分分析 | 同上 |
| M2.2c | $APPEALS 评估 | 同上 |
| M2.2d | 单元测试 | `tests/test_look_at_market.py` |

输入：`financial_quarterly` + `subscriber_quarterly` + `tariffs` + `intelligence_events`
输出：`MarketCustomerInsight` 对象

### M2.3 看竞争（Competitor）

| ID | 任务 | 产出文件 |
|----|------|---------|
| M2.3a | 波特五力分析 | `src/blm/look_at_competition.py` |
| M2.3b | 同行对手深度分析（增强版） | 同上 |
| M2.3c | 横向对比 | 同上 |
| M2.3d | 单元测试 | `tests/test_look_at_competition.py` |

输入：全量数据（所有运营商的 financial + subscriber + network + intelligence）
输出：`CompetitionInsight` 对象

### M2.4 看自己（Self）

| ID | 任务 | 产出文件 |
|----|------|---------|
| M2.4a | 经营总体体检 + 业绩差距/机会差距 | `src/blm/look_at_self.py` |
| M2.4b | 细分业务深度分析（移动/固网/B2B/TV/批发） | 同上 |
| M2.4c | 网络深度分析 | 同上 |
| M2.4d | 组织、人才与文化分析 | 同上 |
| M2.4e | BMC 商业模式画布 | 同上 |
| M2.4f | 优势/短板/暴露面 | 同上 |
| M2.4g | 单元测试 | `tests/test_look_at_self.py` |

输入：目标运营商全量数据 + 竞对数据（用于对比）
输出：`SelfInsight` 对象

### M2.5 SWOT 综合

| ID | 任务 | 产出文件 |
|----|------|---------|
| M2.5a | SWOT 汇总（从前四看提取 S/W/O/T） | `src/blm/swot_synthesis.py` |
| M2.5b | 四象限策略推导（SO/WO/ST/WT） | 同上 |
| M2.5c | 单元测试 | `tests/test_swot.py` |

输入：前四看的输出对象
输出：`SWOTAnalysis` 对象

### M2.6 看机会（Opportunity）

| ID | 任务 | 产出文件 |
|----|------|---------|
| M2.6a | 机会点提取（从前四看 + SWOT 交叉推导） | `src/blm/look_at_opportunities.py` |
| M2.6b | SPAN 矩阵评分和定位 | 同上 |
| M2.6c | 单元测试 | `tests/test_look_at_opportunities.py` |

输入：前四看 + SWOT 的输出
输出：`OpportunityInsight` 对象（含 SPAN 位置）

### M2.7 分析引擎主入口

| ID | 任务 | 产出文件 |
|----|------|---------|
| M2.7a | BLMAnalysisEngine 类（串联五看 + SWOT） | `src/blm/engine.py` |
| M2.7b | 集成测试 | `tests/test_engine.py` |

```python
engine = BLMAnalysisEngine(db, target="vodafone_germany", market="germany")
result = engine.run_five_looks()
# result.trends: TrendAnalysis
# result.market_customer: MarketCustomerInsight
# result.competition: CompetitionInsight
# result.self_analysis: SelfInsight
# result.swot: SWOTAnalysis
# result.opportunities: OpportunityInsight
```

---

## M3: 输出层

> 目标：四种格式的报告输出

### M3.1 PPT 风格库

| ID | 任务 | 产出文件 |
|----|------|---------|
| M3.1a | 运营商品牌风格定义 | `src/output/ppt_styles.py` |

Vodafone Red / DT Magenta / O2 Blue / 1&1 Blue / 默认 Navy

### M3.2 PPT 生成器重构

| ID | 任务 | 产出文件 |
|----|------|---------|
| M3.2a | PPT 基础框架（Slide 基类、布局工具、Key Message 横条） | `src/output/ppt_generator.py` |
| M3.2b | 看趋势 Slides（S05-S07） | 同上 |
| M3.2c | 看市场/客户 Slides（S08-S11）含 $APPEALS 雷达图 | 同上 |
| M3.2d | 看竞争 Slides（S12-S17）含五力图 | 同上 |
| M3.2e | 看自己 Slides（S18-S26）含业务深度模板 | 同上 |
| M3.2f | SWOT Slide（S27） | 同上 |
| M3.2g | 看机会 Slides（S28-S30）含 SPAN 气泡图 | 同上 |
| M3.2h | 通用 Slides（封面/目录/摘要/溯源/封底） | 同上 |
| M3.2i | Draft 版 vs Final 版支持 | 同上 |

### M3.3 图表扩展

| ID | 任务 | 产出文件 |
|----|------|---------|
| M3.3a | SPAN 气泡图 | `src/output/ppt_charts.py` |
| M3.3b | 波特五力图 | 同上 |
| M3.3c | SWOT 矩阵图 | 同上 |
| M3.3d | $APPEALS 雷达图 | 同上 |
| M3.3e | BMC 九宫格 | 同上 |

### M3.4 其他输出格式

| ID | 任务 | 产出文件 |
|----|------|---------|
| M3.4a | HTML 报告生成器（含溯源 tooltip） | `src/output/html_generator.py` |
| M3.4b | JSON 导出 | `src/output/json_exporter.py` |
| M3.4c | TXT 格式化 | `src/output/txt_formatter.py` |

---

## M4: 集成测试 & 联调

| ID | 任务 | 产出文件 |
|----|------|---------|
| M4.1 | 端到端测试：从 seed 数据到 PPT 输出 | `tests/test_integration.py` |
| M4.2 | CLI 入口更新 | `src/cli.py` |
| M4.3 | 生成 Vodafone Germany 样本报告 | `data/output/` |
| M4.4 | README 更新 | `README.md` |

---

## 建议的执行顺序

```
先做 M0 + M1（基础设施 + 数据层）
  ↓ 这是所有后续工作的地基
然后 M2.0（数据模型）
  ↓ 所有引擎模块共享的类型定义
然后 M2.1 → M2.2 → M2.3 → M2.4 → M2.5 → M2.6 → M2.7（五看引擎，按顺序）
  ↓ 每完成一看就可以单独测试
然后 M3（输出层）
  ↓ 引擎完成后再做输出
最后 M4（集成测试）
```

---

## Claude Code Agent 启动指南

### 推荐的 Agent 配置

使用 **Claude Code**（命令行 Agent）在本项目上工作。

```bash
# 1. Clone 项目
git clone https://github.com/mypinseeker/BLM-Financial-Report-Analysis.git
cd BLM-Financial-Report-Analysis
git checkout claude/continue-previous-work-bNei7

# 2. 将 CLAUDE.md 和 ROADMAP.md 放到项目根目录
# （Agent 启动时会自动读 CLAUDE.md）

# 3. 将设计文档放到 docs/design/
mkdir -p docs/design
# 复制 12 份设计文档到 docs/design/

# 4. 启动 Claude Code
claude

# 5. 给 Agent 的第一条指令
> 请阅读 CLAUDE.md 和 ROADMAP.md，然后从 M0 开始执行。
> 每完成一个里程碑后暂停，向我汇报进度。
```

### Agent 工作模式建议

- **单 Agent 顺序执行**：一个 Claude Code 实例按 M0→M1→M2→M3→M4 顺序
- 每完成一个里程碑运行测试，确认通过后再进入下一个
- 遇到设计不明确的地方，先查 `docs/design/` 中的文档；文档也没覆盖的，暂停问你

### 每个里程碑的验收标准

| 里程碑 | 验收标准 |
|--------|---------|
| M0 | 目录结构创建完毕，旧代码归档，设计文档在位 |
| M1 | `python -c "from src.database.db import TelecomDatabase; db = TelecomDatabase(); db.init()"` 成功；种子数据可查询 |
| M2 | `python -c "from src.blm.engine import BLMAnalysisEngine"` 成功；`pytest tests/test_engine.py` 通过 |
| M3 | 生成 Vodafone Germany 的 PPT 文件且可打开；所有 Slide 有 Key Message |
| M4 | 端到端 `blm-analyze run "Vodafone Germany" --format ppt` 成功输出报告 |
