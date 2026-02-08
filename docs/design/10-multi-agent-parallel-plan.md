# BLM 多 Agent 并行开发方案
# Multi-Agent Parallel Development Plan

---

## 一、团队结构

```
                        你（产品负责人 / 决策者）
                              │
                    ┌─────────┴─────────┐
                    │                   │
              架构师 Agent            QA/Reviewer Agent
              (Architect)            (Reviewer)
                    │                   │
         ┌────┬────┼────┬────┐         │
         │    │    │    │    │         │
        Dev1 Dev2 Dev3 Dev4 Dev5       │
        看趋势 看市场 看竞争 看自己 看机会    │
         │    │    │    │    │         │
         └────┴────┴────┴────┘         │
              │ PR 提交                │
              └───────────────────────→┘
                  Code Review + 合入
```

### 角色定义

| 角色 | 数量 | 职责 | 用什么工具 |
|------|------|------|-----------|
| **你** | 1 | 决策、审批 PR、验收 | GitHub Web |
| **架构师** | 1 | 搭建基础设施（M0+M1+M2.0），定义接口，确保一致性 | Claude Code (第一个启动) |
| **Dev 1-5** | 5 | 各负责一看的分析引擎 + 对应的 PPT Slide | Claude Code (并行启动) |
| **QA/Reviewer** | 1 | Review PR，检查代码质量/逻辑/一致性 | Claude Code 或 Claude Chat |

---

## 二、分支策略

```
main
  └── claude/five-looks-v2 (集成分支)
        ├── arch/infrastructure     ← 架构师：M0 + M1 + M2.0
        ├── dev/look-at-trends      ← Dev1：看趋势
        ├── dev/look-at-market      ← Dev2：看市场/客户
        ├── dev/look-at-competition ← Dev3：看竞争
        ├── dev/look-at-self        ← Dev4：看自己
        ├── dev/look-at-opportunity ← Dev5：SWOT + 看机会
        └── dev/output-layer        ← 架构师或指定 Dev：输出层
```

### 合并流程

```
1. 架构师先完成 arch/infrastructure
   → PR → QA Review → 合入 claude/five-looks-v2

2. Dev 1-5 从 claude/five-looks-v2 拉最新代码，开始并行开发
   → 每个 Dev 完成后提 PR → QA Review → 合入

3. 输出层在引擎完成后开始
   → PR → QA Review → 合入

4. 最终 claude/five-looks-v2 → main
```

---

## 三、架构师的任务（必须先完成）

架构师是第一个启动的 Agent，他的输出是所有 Dev 的基础。

### 产出清单

```
src/
├── database/
│   ├── schema.sql              ← 完整的数据库 DDL
│   ├── db.py                   ← TelecomDatabase 类（含所有查询方法）
│   ├── period_utils.py         ← PeriodConverter
│   ├── operator_directory.py   ← 运营商注册表
│   ├── init_db.py              ← 数据库初始化
│   └── seed_germany.py         ← 种子数据（从硬编码迁移）
├── models/
│   ├── __init__.py             ← 统一导出
│   ├── trend.py                ← PESTFactor, TrendAnalysis
│   ├── market.py               ← MarketChange, CustomerSegment, APPEALSAssessment
│   ├── competition.py          ← PorterForce, CompetitorDeepDive
│   ├── self_analysis.py        ← SegmentAnalysis, NetworkAnalysis, etc.
│   ├── swot.py                 ← SWOTAnalysis
│   ├── opportunity.py          ← SPANPosition, OpportunityInsight
│   ├── provenance.py           ← TrackedValue, SourceReference
│   └── feedback.py             ← UserFeedback
├── blm/
│   └── engine.py               ← BLMAnalysisEngine 骨架（接口定义，方法留空）
└── output/
    └── ppt_styles.py           ← 运营商品牌风格库
```

### 关键：接口契约

架构师需要在 `engine.py` 中定义每个 look 的**接口签名**，让 Dev 知道：
- 输入是什么（从数据库查询哪些数据）
- 输出是什么（返回什么数据模型）

```python
# src/blm/engine.py — 架构师定义的骨架

class BLMAnalysisEngine:
    def __init__(self, db: TelecomDatabase, target_operator: str, market: str,
                 period: str = None, n_quarters: int = 8):
        ...

    def run_five_looks(self) -> FiveLooksResult:
        """按顺序执行五看 + SWOT"""
        trends = self.look_at_trends()
        market = self.look_at_market_customer()
        competition = self.look_at_competition()
        self_analysis = self.look_at_self()
        swot = self.synthesize_swot(trends, market, competition, self_analysis)
        opportunities = self.look_at_opportunities(trends, market, competition, 
                                                     self_analysis, swot)
        return FiveLooksResult(...)

    def look_at_trends(self) -> TrendAnalysis:
        """01 看趋势 — Dev1 实现"""
        raise NotImplementedError

    def look_at_market_customer(self) -> MarketCustomerInsight:
        """02 看市场/客户 — Dev2 实现"""
        raise NotImplementedError

    def look_at_competition(self) -> CompetitionInsight:
        """03 看竞争 — Dev3 实现"""
        raise NotImplementedError

    def look_at_self(self) -> SelfInsight:
        """04 看自己 — Dev4 实现"""
        raise NotImplementedError

    def synthesize_swot(self, ...) -> SWOTAnalysis:
        """SWOT 综合 — Dev5 实现"""
        raise NotImplementedError

    def look_at_opportunities(self, ...) -> OpportunityInsight:
        """05 看机会 — Dev5 实现"""
        raise NotImplementedError
```

---

## 四、每个 Dev 的任务

### Dev1: 看趋势

| 分支 | `dev/look-at-trends` |
|------|---------------------|
| 实现文件 | `src/blm/look_at_trends.py` |
| 测试文件 | `tests/test_look_at_trends.py` |
| PPT Slides | S05 PEST 仪表盘, S06 行业环境, S07 [可选]深度 |
| 参考设计 | `docs/design/04-看宏观PEST框架对齐规范.md` |
| 输入 | `macro_environment` 表, `intelligence_events` 表 |
| 输出 | `TrendAnalysis` 对象 |

### Dev2: 看市场/客户

| 分支 | `dev/look-at-market` |
|------|---------------------|
| 实现文件 | `src/blm/look_at_market_customer.py` |
| 测试文件 | `tests/test_look_at_market.py` |
| PPT Slides | S08 市场全景, S09 客户细分, S10 $APPEALS, S11 [可选]深度 |
| 参考设计 | `docs/design/01-五看方法论对齐全面更新.md` 第四章 |
| 输入 | `financial_quarterly`, `subscriber_quarterly`, `tariffs`, `intelligence_events` |
| 输出 | `MarketCustomerInsight` 对象 |

### Dev3: 看竞争

| 分支 | `dev/look-at-competition` |
|------|--------------------------|
| 实现文件 | `src/blm/look_at_competition.py` |
| 测试文件 | `tests/test_look_at_competition.py` |
| PPT Slides | S12 五力全景, S13-S15 对手详细, S16 横向对比, S17 [可选]专题 |
| 参考设计 | `docs/design/01-五看方法论对齐全面更新.md` 第五章 |
| 输入 | 全量运营商数据 |
| 输出 | `CompetitionInsight` 对象 |

### Dev4: 看自己

| 分支 | `dev/look-at-self` |
|------|---------------------|
| 实现文件 | `src/blm/look_at_self.py` |
| 测试文件 | `tests/test_look_at_self.py` |
| PPT Slides | S18-S26（最多的 Slides：经营+业务+网络+组织+暴露面） |
| 参考设计 | `docs/design/01-五看方法论对齐全面更新.md` 第六章 + `03-看自己细分业务补充规范.md` |
| 输入 | 目标运营商全量数据 + 竞对数据 |
| 输出 | `SelfInsight` 对象 |

### Dev5: SWOT + 看机会

| 分支 | `dev/look-at-opportunity` |
|------|--------------------------|
| 实现文件 | `src/blm/swot_synthesis.py` + `src/blm/look_at_opportunities.py` |
| 测试文件 | `tests/test_swot.py` + `tests/test_look_at_opportunities.py` |
| PPT Slides | S27 SWOT, S28 SPAN, S29 机会清单, S30 [可选]深度 |
| 参考设计 | `docs/design/01-五看方法论对齐全面更新.md` 第七、八章 |
| 输入 | 前四看的输出（需要 Dev1-4 的数据模型定义，但可以先用 mock 数据开发） |
| 输出 | `SWOTAnalysis` + `OpportunityInsight` 对象 |

**注意**：Dev5 依赖前四看的输出。但因为数据模型由架构师定义，Dev5 可以用 mock 数据并行开发。最终集成时才接入真实数据。

---

## 五、QA/Reviewer 的职责

### Review 检查清单

对每个 Dev 的 PR，Reviewer 检查：

```
□ 代码质量
  □ 类型标注完整（dataclass 字段、函数签名）
  □ 文档字符串清晰
  □ 无硬编码数据（所有数据从数据库查询）
  □ 异常处理（数据缺失时不崩溃）

□ 设计一致性
  □ 数据模型与 src/models/ 中的定义一致
  □ 方法签名与 engine.py 中的接口契约一致
  □ 输出结构能被 PPT 生成器消费

□ 方法论合规
  □ 分析维度覆盖设计文档的要求
  □ 每个分析都有 key_message
  □ 数据溯源信息完整

□ 测试质量
  □ 有正常路径测试
  □ 有数据缺失的边界测试
  □ 有未发布数据（pending）的处理测试

□ 财年对齐
  □ 使用 calendar_quarter 做跨运营商对比
  □ 不把不同财年的 Q3 直接对齐
```

---

## 六、启动步骤

### Step 1: 你先把文件上传到 GitHub

需要上传的文件：

```
项目根目录/
├── CLAUDE.md
├── ROADMAP.md
└── docs/design/
    ├── 01-五看方法论对齐全面更新.md
    ├── 02-五看分析框架详细设计.md
    ├── 03-看自己细分业务补充规范.md
    ├── 04-看宏观PEST框架对齐规范.md
    ├── 05-五看输出件规范.md
    ├── 06-PPT内容原则补充规范.md
    ├── 07-财报时间维度对齐规范.md
    ├── 08-数据溯源架构设计.md
    └── 09-完整开发指南-v4.md
```

### Step 2: 启动架构师 Agent

```bash
cd BLM-Financial-Report-Analysis
git checkout claude/continue-previous-work-bNei7
git checkout -b arch/infrastructure

claude  # 启动 Claude Code

# 给架构师的指令：
> 你是本项目的架构师。请阅读 CLAUDE.md 和 ROADMAP.md，
> 然后执行 M0 和 M1（项目基础设施 + 数据层）以及 M2.0（数据模型）。
> 同时在 src/blm/engine.py 中定义五看的接口骨架。
> 完成后提交并告诉我。
```

### Step 3: 架构师完成后，创建集成分支并合入

```bash
git checkout claude/continue-previous-work-bNei7
git merge arch/infrastructure
git push
```

### Step 4: 启动 5 个 Dev Agent（并行）

每个 Dev 在一个单独的终端窗口：

```bash
# 终端 1 — Dev1 看趋势
git checkout -b dev/look-at-trends claude/continue-previous-work-bNei7
claude
> 你是 Dev1，负责"看趋势"。请阅读 CLAUDE.md，
> 然后阅读 docs/design/04-看宏观PEST框架对齐规范.md，
> 实现 src/blm/look_at_trends.py 和对应的测试。
> 输入输出接口见 src/blm/engine.py 和 src/models/trend.py。

# 终端 2 — Dev2 看市场
git checkout -b dev/look-at-market claude/continue-previous-work-bNei7
claude
> 你是 Dev2，负责"看市场/客户"...

# 终端 3 — Dev3 看竞争
# 终端 4 — Dev4 看自己
# 终端 5 — Dev5 SWOT + 看机会
```

### Step 5: Dev 完成后，QA Review

```bash
# 每个 Dev 完成后 push 并创建 PR
# 启动 QA Agent 做 Review

claude
> 你是 QA Reviewer。请 review dev/look-at-trends 分支的 PR。
> 按照 docs/design/ 中的 multi-agent-plan.md 的 Review 检查清单逐项检查。
> 输出 Review 意见。
```

### Step 6: 合入 + 输出层

```bash
# 所有 PR review 通过后合入
# 然后做输出层（M3）和集成测试（M4）
```

---

## 七、并行度与依赖关系

```
时间 →

Phase A (架构师独占)：
  [── arch/infrastructure ──]
                              ↓ 合入

Phase B (5 Dev 并行)：
  [── Dev1: 看趋势 ────────]
  [── Dev2: 看市场 ────────]
  [── Dev3: 看竞争 ────────]
  [── Dev4: 看自己 ────────]  ← 工作量最大，可能最晚完成
  [── Dev5: SWOT+机会 ─────]  ← 用 mock 数据先行，最后接入真实数据
                              ↓ 全部合入

Phase C (输出层)：
  [── PPT/HTML/JSON/TXT ───]
                              ↓

Phase D (集成测试)：
  [── 端到端测试 ──]
```

**瓶颈**：
- Phase A 是串行的，必须先完成
- Phase B 中 Dev4（看自己）工作量最大（9 页 Slide + 5 个细分业务）
- Phase C 必须在 Phase B 全部完成后才能开始

**总耗时预估**：
- Phase A: 1-2 天
- Phase B: 3-4 天（并行，取最慢的 Dev4）
- Phase C: 2-3 天
- Phase D: 1 天
- **总计: 7-10 天**（比串行的 9-12 天快了 20-30%）
