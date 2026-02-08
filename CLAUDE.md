# CLAUDE.md — BLM Financial Report Analysis 项目指南
# 本文件是所有 Agent 的唯一入口。开始任何工作前必须先读这个文件。

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
