# CLAUDE.md — BLM Financial Report Analysis 项目指南
# 本文件是所有 Agent 的唯一入口。开始任何工作前必须先读这个文件。

---

## ⛔ 铁律：数据完整性（MANDATORY — 违反即失败）

**本项目的一切数据必须有明确、可追溯的来源。严禁编造任何数据。**

### 绝对禁止
1. **禁止编造时间序列** — 不得用线性递增/递减填充8个季度。运营商未披露的季度必须为 `None`
2. **禁止编造频谱数据** — 频谱分配必须来自国家监管机构（ANE/ASEP/CRC等）或 spectrum-tracker.com，需有精确频率范围
3. **禁止编造用户数** — 不同来源（CRC/AMX/Millicom/GSMA）的统计口径不同，不可混用。休眠SIM、IoT必须说明
4. **禁止编造竞争评分** — 所有评分必须有来源或明确标注为"分析师主观评估"
5. **禁止省略来源标注** — seed_*.py 中每个数据块必须有 `_source` + `_source_url`，否则视为未验证数据

### 强制执行
1. **写入前验证** — 任何数据写入 seed 文件或报告前，必须先确认来源可追溯
2. **QA 脚本必跑** — 修改 seed 文件后必须运行 `python3 scripts/qa_seed_audit.py <market>` 并确认 0 CRITICAL
3. **未披露 = None** — 运营商未公开的季度数据、国别ARPU/CAPEX等，必须标注 None 或 "not disclosed"，绝不用估算值填充
4. **常识校验** — 用户数超过人口150%必须解释（IoT/休眠SIM）；增速/利润率必须与财报一致
5. **频谱拍卖必查** — 进入任何市场分析前，必须确认近3年是否有频谱拍卖事件（3.5 GHz 5G、700 MHz等）

### 数据来源优先级
```
① 运营商财报/IR（最高）
② 监管机构官方统计（ANE/CRC/ASEP/SIT 等）
③ spectrum-tracker.com（频谱数据）
④ 行业报告（TeleSemana/GSMA/DPL News）
⑤ 无法获取 → 标注 "not disclosed / not available"
```

### QA 验证规则（R1-R8）
| 规则 | 说明 |
|---|---|
| **R1** | 无来源不入报告 — 每个数字必须标注具体来源 |
| **R2** | 来源层级 — 按上述优先级使用来源 |
| **R3** | seed文件标注 — 每个数据块必须有 `_source` + `_source_url` |
| **R4** | 未披露数据 — 标注 None / "not disclosed"，不得编造 |
| **R5** | 频谱数据 — 必须来自监管机构，标注 Band ID、FDD/TDD、频率范围 |
| **R6** | 报告标注 — 报告末尾必须有"数据来源与置信度"附录 |
| **R7** | 市场结构验证 — 先验证运营商数量、并购事件、频谱拍卖，再做分析 |
| **R8** | **QA 闭环** — 修改后必须跑 `qa_seed_audit.py`，0 CRITICAL 才可提交 |

### 历史教训（2026-02-27 审计发现）
- **22个市场中0个通过QA** — 579个CRITICAL + 334个WARNING
- 根因：AI生成seed数据 → 没有交叉校验 → 直接写入报告
- Colombia示例：sub-3GHz频谱表全错、2023年12月3.5GHz拍卖遗漏、1.025亿SIM含54%休眠未说明
- **从此以后：先验证，再写入，最后QA确认**

---

## 项目概述

基于华为 BLM（Business Leadership Model）方法论的电信运营商战略分析工具。
通过"五看"分析框架，自动采集公开数据、分析运营商竞争态势，
输出 PPT/HTML/JSON/TXT 格式的战略分析报告。

**当前阶段**：五看分析引擎重构（Phase 1）
**目标**：将五看从硬编码数据 + 简单分析，升级为方法论对齐 + 数据库驱动 + 结构化输出

---

## 五看方法论（最终版）

```
01 看趋势（Trend）    — PEST 框架        — 宏观大势和行业环境
02 看市场/客户（Market/Customer） — $APPEALS   — 市场变化 + 客户细分需求
03 看竞争（Competitor）  — 波特五力         — 五种竞争力量 + 同行深度分析
04 看自己（Self）      — BMC + 能力盘点   — 经营体检 + 细分业务 + 组织能力
── SWOT 综合分析 ──     — SWOT 矩阵       — 前四看汇总 → 四种策略方向
05 看机会（Opportunity）— SPAN 矩阵       — 机会筛选 + 二维定位
```

---

## 设计文档索引（按优先级阅读）

所有设计文档在 `docs/design/` 目录下。
如果你是第一次接触本项目，请按以下顺序阅读：

| 优先级 | 文件 | 内容 |
|--------|------|------|
| ★★★ | `docs/design/01-five-looks-methodology-alignment.md` | **最重要**。五看的完整定义、数据模型、PPT Slide 清单 |
| ★★★ | `docs/design/02-five-looks-detailed-design.md` | 每一看的详细维度、输出结构、数据采集需求 |
| ★★☆ | `docs/design/03-look-at-self-segment-analysis.md` | 看自己的细分业务深度分析模板（数据层+归因层） |
| ★★☆ | `docs/design/04-look-at-trends-pest-framework.md` | 看趋势的 PEST 四维度详细定义和数据模型 |
| ★★☆ | `docs/design/05-output-format-specification.md` | PPT/HTML/JSON/TXT 四种输出格式的详细规范 |
| ★★☆ | `docs/design/06-ppt-content-principles.md` | 每页必须有 Key Message + 先长后短两轮输出 |
| ★★☆ | `docs/design/07-fiscal-period-alignment.md` | 财年/日历年对齐、PeriodConverter、未发布数据处理 |
| ★☆☆ | `docs/design/08-data-provenance-architecture.md` | TrackedValue/SourceReference 数据溯源体系 |
| ★☆☆ | `docs/design/09-complete-dev-guide-v4.md` | 数据库 Schema、订阅模型、采集器架构（早期版本，部分已被上面的文档覆盖） |

---

## 项目结构（目标架构）

```
BLM-Financial-Report-Analysis/
├── CLAUDE.md                          ← 你在这里
├── ROADMAP.md                         ← 开发路标
├── docs/
│   └── design/                        ← 设计文档（上面的索引）
├── config/
│   └── default.yaml
├── src/
│   ├── database/                      ← 数据层（新建）
│   │   ├── schema.sql                 ← 数据库 DDL
│   │   ├── db.py                      ← TelecomDatabase 类
│   │   ├── period_utils.py            ← PeriodConverter 财年对齐
│   │   └── operator_directory.py      ← 运营商注册表 + 财年配置
│   ├── models/                        ← 数据模型（新建）
│   │   ├── trend.py                   ← PESTFactor, TrendAnalysis
│   │   ├── market.py                  ← MarketChange, CustomerSegment, APPEALSAssessment
│   │   ├── competition.py             ← PorterForce, CompetitorDeepDive
│   │   ├── self_analysis.py           ← SegmentAnalysis, NetworkAnalysis, ExposurePoint
│   │   ├── swot.py                    ← SWOTAnalysis
│   │   ├── opportunity.py             ← SPANPosition, OpportunityInsight
│   │   ├── provenance.py              ← TrackedValue, SourceReference
│   │   └── feedback.py                ← UserFeedback
│   ├── blm/                           ← 分析引擎（重构）
│   │   ├── engine.py                  ← BLMAnalysisEngine 主入口
│   │   ├── look_at_trends.py          ← 01 看趋势
│   │   ├── look_at_market_customer.py ← 02 看市场/客户
│   │   ├── look_at_competition.py     ← 03 看竞争
│   │   ├── look_at_self.py            ← 04 看自己
│   │   ├── swot_synthesis.py          ← SWOT 综合
│   │   ├── look_at_opportunities.py   ← 05 看机会
│   │   └── interactive.py             ← 人机共创模块
│   ├── output/                        ← 输出层（重构）
│   │   ├── ppt_styles.py              ← 运营商品牌风格库
│   │   ├── ppt_generator.py           ← PPT 生成器（统一为一个）
│   │   ├── ppt_charts.py              ← 图表生成
│   │   ├── html_generator.py          ← HTML 报告
│   │   ├── json_exporter.py           ← JSON 导出
│   │   └── txt_formatter.py           ← TXT 格式化
│   └── cli.py                         ← 命令行入口
├── tests/
│   ├── test_models.py
│   ├── test_database.py
│   ├── test_period_utils.py
│   ├── test_engine.py
│   ├── test_look_at_trends.py
│   ├── test_look_at_market.py
│   ├── test_look_at_competition.py
│   ├── test_look_at_self.py
│   ├── test_swot.py
│   ├── test_look_at_opportunities.py
│   └── test_ppt_generator.py
└── data/
    ├── telecom.db                     ← SQLite 数据库
    ├── raw/                           ← 原始下载的财报等
    ├── processed/                     ← 处理后的中间数据
    └── output/                        ← 生成的报告
```

---

## 现有代码资产（可复用部分）

| 现有文件 | 代码量 | 复用方式 |
|---------|--------|---------|
| `src/blm/ppt_generator_enhanced.py` | 113K | 拆分重构：slide 布局方法迁移到新 `ppt_generator.py`，增加新页面类型 |
| `src/blm/ppt_charts.py` | 32K | 大部分可复用：趋势图/雷达图/柱状图，新增气泡图(SPAN)/五力图 |
| `src/blm/comprehensive_analysis_ppt.py` | 60K | 业务分析图表代码合并到新 PPT 生成器，原文件废弃 |
| `src/blm/germany_telecom_analysis.py` | 51K | 硬编码数据作为数据库初始 seed 数据；分析逻辑迁移到新的 look_at_*.py |
| `src/blm/germany_market_comprehensive_data.py` | 37K | 纯数据文件，全部迁移到数据库 seed |
| `src/blm/three_decisions.py` | 17K | Phase 2 再重构，当前保留 |
| `src/blm/report_generator.py` | 21K | HTML 模板迁移到 `html_generator.py`，增加溯源和交互 |
| `src/blm/ppt_generator.py` | 28K | PPTStyle 定义迁移到 `ppt_styles.py`，原文件废弃 |
| `src/blm/telecom_data.py` | 15K | 数据加载逻辑被数据库替代，废弃 |

---

## 技术栈

- **Python 3.11+**
- **SQLite**：数据存储（`data/telecom.db`）
- **python-pptx**：PPT 生成
- **matplotlib**：图表
- **pandas**：数据处理
- **jinja2**：HTML 模板
- **click**：CLI

---

## 关键设计原则

1. **数据库驱动**：所有数据存在 SQLite，不硬编码
2. **溯源体系**：每个数据点有 source_url / source_date / confidence
3. **财年对齐**：用 calendar_quarter (CQ4_2025) 做跨运营商对比
4. **未发布数据留空**：不用旧数据冒充新数据
5. **每页有结论**：PPT 每页底部必须有 Key Message 横条
6. **先长后短**：Draft 版完整呈现，Final 版经用户确认后精简
7. **用户反馈不污染原始数据**：三层架构（原始数据 + AI 结论 + 用户反馈）
8. **Addressable Market 无数据就留空**：绝不编造数字
