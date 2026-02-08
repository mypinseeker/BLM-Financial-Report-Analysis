# BLM 五看输出件规范
# Five Looks Output Specification

---

## 一、输出格式总览

五看分析完成后，系统输出四种格式的报告，全部保留：

| 格式 | 用途 | 文件 |
|------|------|------|
| **PPT** | 主力交付物，给客户做汇报 | `blm_{operator}_{period}.pptx` |
| **HTML** | 交互式在线阅读，可发邮件 | `blm_{operator}_{period}.html` |
| **JSON** | 机器可读，供 API 查询、二次开发 | `blm_{operator}_{period}.json` |
| **TXT** | 快速阅读，命令行输出 | `blm_{operator}_{period}.txt` |

所有格式共享同一套分析数据，只是呈现方式不同。

---

## 二、运营商品牌风格

### 2.1 核心原则

> PPT 的视觉风格跟随洞察主角运营商的品牌形象。
> 分析 Vodafone 就用 Vodafone 配色，分析 O2 就用 O2 配色。

### 2.2 运营商风格库

```python
# src/blm/ppt_styles.py

from dataclasses import dataclass

@dataclass
class PPTStyle:
    """PPT 视觉风格配置"""
    name: str
    display_name: str              # 显示名称
    
    # 色彩
    primary_color: tuple           # 主色调（品牌色）
    secondary_color: tuple         # 辅助色
    accent_color: tuple            # 强调色
    text_color: tuple              # 正文色
    light_text_color: tuple        # 浅色文字
    background_color: tuple        # 背景色
    positive_color: tuple          # 正面/增长（绿色系）
    negative_color: tuple          # 负面/下降（红色系）
    warning_color: tuple           # 警告/注意（黄色系）
    
    # 字体
    title_font: str
    body_font: str
    cjk_font: str                  # 中文字体
    
    # 字号
    title_size: int
    subtitle_size: int
    heading_size: int
    body_size: int
    small_size: int
    footnote_size: int

# ─── 德国市场 ───

VODAFONE_STYLE = PPTStyle(
    name="vodafone",
    display_name="Vodafone",
    primary_color=(230, 0, 0),           # Vodafone Red #E60000
    secondary_color=(51, 51, 51),        # Dark Gray
    accent_color=(77, 77, 77),           # Medium Gray
    text_color=(51, 51, 51),
    light_text_color=(128, 128, 128),
    background_color=(255, 255, 255),
    positive_color=(0, 150, 57),         # #009639
    negative_color=(230, 0, 0),
    warning_color=(255, 165, 0),
    title_font="Vodafone Rg",            # 回退 Arial
    body_font="Vodafone Lt",             # 回退 Arial
    cjk_font="Microsoft YaHei",
    title_size=36, subtitle_size=24, heading_size=20,
    body_size=14, small_size=11, footnote_size=9,
)

DEUTSCHE_TELEKOM_STYLE = PPTStyle(
    name="deutsche_telekom",
    display_name="Deutsche Telekom",
    primary_color=(226, 0, 116),         # Telekom Magenta #E20074
    secondary_color=(51, 51, 51),
    accent_color=(163, 0, 85),           # Dark Magenta
    text_color=(51, 51, 51),
    light_text_color=(128, 128, 128),
    background_color=(255, 255, 255),
    positive_color=(0, 150, 57),
    negative_color=(226, 0, 116),
    warning_color=(255, 165, 0),
    title_font="TeleGrotesk Next",       # 回退 Arial
    body_font="TeleGrotesk Next",
    cjk_font="Microsoft YaHei",
    title_size=36, subtitle_size=24, heading_size=20,
    body_size=14, small_size=11, footnote_size=9,
)

O2_STYLE = PPTStyle(
    name="o2",
    display_name="O2 / Telefónica",
    primary_color=(0, 101, 175),         # O2 Blue #0065AF
    secondary_color=(0, 55, 100),        # Dark Blue
    accent_color=(0, 175, 215),          # Light Blue #00AFD7
    text_color=(51, 51, 51),
    light_text_color=(128, 128, 128),
    background_color=(255, 255, 255),
    positive_color=(0, 150, 57),
    negative_color=(220, 50, 50),
    warning_color=(255, 165, 0),
    title_font="Arial",
    body_font="Arial",
    cjk_font="Microsoft YaHei",
    title_size=36, subtitle_size=24, heading_size=20,
    body_size=14, small_size=11, footnote_size=9,
)

ONE_AND_ONE_STYLE = PPTStyle(
    name="one_and_one",
    display_name="1&1",
    primary_color=(0, 55, 107),          # 1&1 Blue #00376B
    secondary_color=(0, 140, 210),       # Light Blue
    accent_color=(230, 120, 30),         # Orange accent
    text_color=(51, 51, 51),
    light_text_color=(128, 128, 128),
    background_color=(255, 255, 255),
    positive_color=(0, 150, 57),
    negative_color=(220, 50, 50),
    warning_color=(255, 165, 0),
    title_font="Arial",
    body_font="Arial",
    cjk_font="Microsoft YaHei",
    title_size=36, subtitle_size=24, heading_size=20,
    body_size=14, small_size=11, footnote_size=9,
)

# ─── 中国市场 ───

CHINA_MOBILE_STYLE = PPTStyle(
    name="china_mobile",
    display_name="中国移动",
    primary_color=(0, 112, 192),         # China Mobile Blue
    secondary_color=(0, 70, 127),
    accent_color=(0, 176, 80),           # Green accent
    text_color=(51, 51, 51),
    light_text_color=(128, 128, 128),
    background_color=(255, 255, 255),
    positive_color=(0, 150, 57),
    negative_color=(220, 50, 50),
    warning_color=(255, 165, 0),
    title_font="Arial",
    body_font="Arial",
    cjk_font="SimHei",
    title_size=36, subtitle_size=24, heading_size=20,
    body_size=14, small_size=11, footnote_size=9,
)

# ─── 全球运营商（可扩展）───

AT_AND_T_STYLE = PPTStyle(
    name="att",
    display_name="AT&T",
    primary_color=(0, 159, 219),         # AT&T Blue #009FDB
    secondary_color=(0, 50, 100),
    accent_color=(255, 122, 0),          # Orange
    text_color=(51, 51, 51),
    light_text_color=(128, 128, 128),
    background_color=(255, 255, 255),
    positive_color=(0, 150, 57),
    negative_color=(220, 50, 50),
    warning_color=(255, 165, 0),
    title_font="Arial",
    body_font="Arial",
    cjk_font="Microsoft YaHei",
    title_size=36, subtitle_size=24, heading_size=20,
    body_size=14, small_size=11, footnote_size=9,
)

# ─── 风格注册表 ───

OPERATOR_STYLES = {
    # Germany
    "vodafone_germany": VODAFONE_STYLE,
    "deutsche_telekom": DEUTSCHE_TELEKOM_STYLE,
    "o2_germany": O2_STYLE,
    "one_and_one": ONE_AND_ONE_STYLE,
    # China
    "china_mobile": CHINA_MOBILE_STYLE,
    # USA
    "att": AT_AND_T_STYLE,
    # ... 可继续扩展
}

# 默认风格（当运营商没有定义专属风格时）
DEFAULT_STYLE = PPTStyle(
    name="default",
    display_name="BLM Analysis",
    primary_color=(41, 65, 122),         # Professional Navy
    secondary_color=(51, 51, 51),
    accent_color=(0, 120, 200),
    text_color=(51, 51, 51),
    light_text_color=(128, 128, 128),
    background_color=(255, 255, 255),
    positive_color=(0, 150, 57),
    negative_color=(220, 50, 50),
    warning_color=(255, 165, 0),
    title_font="Arial",
    body_font="Arial",
    cjk_font="Microsoft YaHei",
    title_size=36, subtitle_size=24, heading_size=20,
    body_size=14, small_size=11, footnote_size=9,
)


def get_style(operator_id: str) -> PPTStyle:
    """根据运营商 ID 获取对应的 PPT 风格"""
    return OPERATOR_STYLES.get(operator_id, DEFAULT_STYLE)
```

### 2.3 使用方式

```python
# 自动根据主角运营商选择风格
style = get_style("vodafone_germany")  # → Vodafone Red
generator = BLMPPTGeneratorEnhanced(style=style)
```

---

## 三、PPT Slide 规范（完整 Slide 清单）

### 3.1 整体结构

```
┌─────────────────────────────────────────────────────────────┐
│ SECTION 0: 开场                                              │
│   S01  封面                                                   │
│   S02  目录                                                   │
│   S03  数据来源与质量概览                                       │
│   S04  执行摘要                                               │
├─────────────────────────────────────────────────────────────┤
│ SECTION 1: 五看分析                                           │
│                                                              │
│   ── 看市场 ──                                                │
│   S05  市场变化全景（机会 vs 威胁清单）                           │
│   S06  [可选] 重点变化深度分析                                   │
│                                                              │
│   ── 看自己 ──                                                │
│   S07  经营体检报告（财务指标 + 收入拆解 + 市场份额）               │
│   S08  网络深度分析（技术结构 + 演进策略 + 竞对对比）               │
│   S09  优势、短板与暴露面                                       │
│                                                              │
│   ── 看对手 ──                                                │
│   S10  对手 A 详细分析（体检 + 优缺点 + 对我启示）               │
│   S11  对手 B 详细分析                                         │
│   S12  对手 C 详细分析                                         │
│   S13  横向对比总结                                            │
│                                                              │
│   ── 看宏观 ──                                                │
│   S14  宏观环境仪表盘（四象限 + 天气判断）                        │
│   S15  [可选] 重点政策/趋势深度分析                              │
│                                                              │
│   ── 看机会 ──                                                │
│   S16  机会点清单（优先级 + Addressable Market）                 │
│   S17  [可选] Top 3 机会深度分析                                │
│                                                              │
│   ── 综合 ──                                                  │
│   S18  竞争力雷达图                                            │
│   S19  Gap 分析                                               │
├─────────────────────────────────────────────────────────────┤
│ SECTION 2: 经营详细分析（数据支撑层）                             │
│   S20  季度经营分析                                            │
│   S21  8 季度历史趋势                                          │
├─────────────────────────────────────────────────────────────┤
│ SECTION 3: 三定策略                                           │
│   S22  定策略                                                 │
│   S23  定重点工作                                              │
│   S24  定执行（时间线 + KPI）                                   │
├─────────────────────────────────────────────────────────────┤
│ SECTION 4: 收尾                                              │
│   S25  总结与下一步                                            │
│   S26  数据溯源附录                                            │
│   S27  封底                                                   │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 每页 Slide 的详细规范

#### S01 封面

```
布局：全屏品牌色背景
内容：
  - 报告标题："{运营商名} BLM 战略分析报告"
  - 副标题："基于 BLM (Business Leadership Model) 方法论"
  - 信息卡片：分析对象 | 竞争对手 | 报告日期 | 数据期间
  - 框架说明："五看 + 三定"
风格：主色调全铺底，白色文字
```

#### S02 目录

```
布局：左侧竖线时间轴
内容：
  01 执行摘要
  02 五看分析（看市场 | 看自己 | 看对手 | 看宏观 | 看机会）
  03 三定策略（定策略 | 定重点工作 | 定执行）
  04 总结与附录
```

#### S03 数据来源与质量概览

```
布局：信息密度中等
内容：
  - 数据质量仪表盘（来自 ProvenanceStore.quality_report()）
    - 数据点总数 / High 置信度占比 / 存在冲突的数据点数
  - 主要数据来源列表（Top 10 来源，含链接）
  - 数据采集时间 / 最新数据期间
  - 数据覆盖度（哪些维度有数据、哪些缺失）
脚注："完整溯源信息见附录"
```

#### S04 执行摘要

```
布局：上方指标卡片 + 下方关键结论
内容：
  - 4 个核心指标卡片（收入 / 市场份额 / 利润率 / 网络覆盖）
  - 五看核心结论（每看一句话提炼）
  - 战略重点（P0 级别 2-3 条）
  - 底部一句话 Key Message（品牌色横条）
```

#### S05 看市场 — 市场变化全景

```
布局：左右分栏
内容：
  左侧 — 市场快照（背景数据）：
    - 市场总规模 / 增速
    - 4 家份额饼图或条形图
    - 5G 渗透率 / 光纤渗透率
  右侧 — 变化清单：
    上半部分：🟢 机会（绿色标记）
      - 每项：变化描述 + 时间层标签（短/中/长）+ 来源类型（同行/外部）
    下半部分：🔴 威胁（红色标记）
      - 同上
  底部：一句话市场总体判断
```

#### S06 [可选] 重点变化深度分析

```
布局：2-3 个变化展开分析
每个变化包含：
  - 变化描述
  - 数据支撑（引用具体数字 + 溯源标记）
  - 对我的影响
  - 建议行动
```

#### S07 看自己 — 经营体检报告

```
布局：指标卡片 + 收入拆解图 + 份额
内容：
  顶部 — 4-6 个指标卡片：
    收入 / 服务收入增速 / EBITDA Margin / ARPU / 用户净增 / NPS
  中部左 — 收入拆解柱状图：
    移动 / 固网 / B2B / TV / 批发，标注 YoY 增速
  中部右 — 市场份额位置：
    各业务线的份额及排名变化
  底部 — 趋势判断（箭头标注关键指标方向）
```

#### S08 看自己 — 网络深度分析

```
布局：三层结构，从左到右
内容：
  第一列 — 网络现状：
    - 技术组合饼图（Cable 70% / Fiber 自有 5% / Fiber 转售 15% / DSL 10%）
    - 自建 vs 转售比例
    - 5G/4G 覆盖率
    - 网络质量评分（来自第三方测试）
    - Home Pass vs Home Connect 转化率
  第二列 — 演进策略：
    - 网络发展路线图（时间轴形式）
    - 关键里程碑和目标
    - CAPEX 投向
  第三列 — 竞对网络策略对比：
    - 我的路线 vs 每个竞对的路线（简要）
    - 激进/保守标注
  底部 — 网络策略对业务的影响评估
```

#### S09 看自己 — 优势、短板与暴露面

```
布局：三列等分
内容：
  左列（绿色）— 优势 Strengths：
    - 3-5 项核心优势，每项一句话
  中列（黄色）— 短板 Weaknesses：
    - 3-5 项短板
  右列（红色）— 暴露面 Exposure Points：
    - 2-3 个动态暴露面
    - 每个标注：触发动作 → 副作用 → 对手可能的攻击方式
    - 严重程度标签（High/Medium/Low）
```

#### S10-S12 看对手 — 每个对手一页

```
布局：上下分区
上半部分 — 对手体检：
  - 4 个指标卡片（收入/利润率/用户增长/ARPU）
  - 趋势箭头（vs 上季度）
  - 网络状态简要（覆盖率 + 技术路线一句话）
下半部分 — 诊断判断（三列）：
  左列 — ✅ 优点/成功策略
  中列 — ❌ 不足/问题
  右列 — 💡 对我的启示（标注类型：机会/威胁/学习/费解）
```

#### S13 看对手 — 横向对比总结

```
布局：对比表 + 竞争态势判断
内容：
  - 关键指标对比表（运营商为列，指标为行）
    行：收入 / 利润率 / 用户增长 / ARPU / 5G 覆盖 / 网络策略 / 战略方向
    标注：每个单元格用颜色表示优劣（绿=好，红=差，黄=中）
  - 竞争态势总结：一段话 + 竞争格局雷达图
```

#### S14 看宏观 — 宏观环境仪表盘

```
布局：四象限 + 顶部天气图标
顶部 — 天气图标（☀️晴 / ⛅阴 / 🌧️雨 / ⛈️暴风雨）+ 一句话判断
四象限：
  左上 — 宏观经济：GDP / 通胀 / 能源成本，每项带方向箭头 + 对我的影响
  右上 — 国家战略：数字化战略 / 产业政策 / 安全战略
  左下 — 监管策略：电信监管 / 网络安全立法 / 税收
  右下 — 行业大趋势：OTT / AI / 技术演进 / 并购整合
每个象限：2-3 个要点，标注 favorable / unfavorable / uncertain
```

#### S16 看机会 — 机会点清单

```
布局：优先级排序的表格
内容：
  表格列：优先级 / 机会名称 / 描述 / Addressable Market / 自身能力 / 竞争强度 / 时间窗口
  - P0 行高亮（品牌色背景）
  - Addressable Market 列：有数据显示具体数字 + 来源，无数据显示"待补充"
  - 底部：威胁清单（简要列举）
```

#### S18 竞争力雷达图

```
布局：雷达图 + 分析面板
内容：
  左侧 — 多运营商雷达图（10 个维度）
  右侧 — 优势/劣势分析 + 平均分
保留现有实现，加入品牌色适配
```

#### S26 数据溯源附录

```
布局：信息密集，参考性质
内容：
  - 所有数据来源列表（名称 + URL + 日期 + 引用次数）
  - 数据质量总结（High/Medium/Low/Estimated 分布）
  - 存在来源冲突的数据点清单（原值 vs 采信值 + 理由）
  - 过期数据警告
  - 人机共创环节中用户修正的条目（标注"用户已确认"或"用户已调整"）
脚注："完整溯源数据可通过 blm-analyze explain 命令查询"
```

---

## 四、HTML 输出规范

HTML 报告的内容与 PPT 对应，但有以下增强：

1. **交互性**：
   - 指标卡片可悬停显示溯源信息（tooltip）
   - 图表可缩放
   - 目录可点击跳转

2. **溯源集成**：
   - 每个数据点旁边有 🔍 图标
   - 点击展开溯源信息（来源 / 置信度 / 链接）
   - 存在冲突的数据点用 ⚠️ 标注

3. **人机共创标注**：
   - 用户确认的结论标注 ✅
   - 用户修正的结论标注 🔄，显示原始值和修正值
   - 用户补充的内容标注 ➕

4. **响应式布局**：适配桌面和平板

---

## 五、JSON 输出规范

JSON 是机器可读的完整数据导出，结构如下：

```json
{
    "meta": {
        "analysis_id": "blm_vodafone_germany_q3_fy26_20260208",
        "target_operator": "Vodafone Germany",
        "market": "germany",
        "period": "Q3 FY26",
        "competitors": ["Deutsche Telekom", "Telefónica O2 Germany", "1&1 AG"],
        "generated_at": "2026-02-08T20:30:00Z",
        "style": "vodafone"
    },
    
    "data_quality": {
        "total_data_points": 156,
        "confidence_distribution": {"high": 98, "medium": 35, "low": 15, "estimated": 8},
        "conflicts": 12,
        "stale_data": 3,
        "sources_count": 28
    },
    
    "five_looks": {
        "market": {
            "title": "市场洞察 (Look at Market)",
            "market_snapshot": { ... },
            "changes": [
                {
                    "change_type": "technology",
                    "source": "同行驱动",
                    "time_horizon": "medium_term",
                    "description": "德电加速 Fiber 部署...",
                    "impact_type": "threat",
                    "impact_description": "对 Vodafone Cable 业务构成...",
                    "severity": "high",
                    "evidence": ["dt_fiber_homepass_q3_fy26"]
                }
            ],
            "opportunities": [ ... ],
            "threats": [ ... ],
            "market_outlook": "mixed",
            "key_message": "..."
        },
        
        "self": {
            "title": "自身洞察 (Look at Self)",
            "financial_health": { ... },
            "market_positions": { ... },
            "network": {
                "technology_mix": { ... },
                "evolution_strategy": { ... },
                "vs_competitors": "..."
            },
            "customer_perception": { ... },
            "leadership_changes": [ ... ],
            "strengths": [ ... ],
            "weaknesses": [ ... ],
            "exposure_points": [
                {
                    "trigger_action": "迁入 1100 万 1&1 用户",
                    "side_effect": "网络负荷骤增",
                    "attack_vector": "对手宣传网络拥挤",
                    "severity": "high"
                }
            ],
            "health_rating": "stable",
            "key_message": "..."
        },
        
        "competitors": {
            "title": "竞争洞察 (Look at Competitors)",
            "individual_analyses": {
                "Deutsche Telekom": {
                    "financial_health": { ... },
                    "strengths": [ ... ],
                    "weaknesses": [ ... ],
                    "problems": [ ... ],
                    "implications": [
                        {
                            "type": "learning",
                            "description": "连续 35 季度 EBITDA 增长值得研究",
                            "suggested_action": "..."
                        }
                    ]
                },
                "Telefónica O2 Germany": { ... },
                "1&1 AG": { ... }
            },
            "comparison_table": { ... },
            "competitive_landscape": "...",
            "key_message": "..."
        },
        
        "macro": {
            "title": "宏观环境洞察 (Look at Macro)",
            "factors": [ ... ],
            "economy_outlook": "...",
            "policy_outlook": "...",
            "regulation_outlook": "...",
            "industry_trend_outlook": "...",
            "overall_weather": "cloudy",
            "key_message": "..."
        },
        
        "opportunities": {
            "title": "机会洞察 (Look at Opportunities)",
            "opportunities": [
                {
                    "name": "B2B 云安全服务",
                    "description": "...",
                    "derived_from": ["market:数字化需求增长", "self:Skaylink收购"],
                    "addressable_market": "€2.5B",
                    "addressable_market_source": "Analysys Mason 2025",
                    "our_capability": "moderate",
                    "competition_intensity": "medium",
                    "time_window": "ongoing",
                    "priority": "P0",
                    "priority_rationale": "..."
                }
            ],
            "threats": [ ... ],
            "key_message": "..."
        }
    },
    
    "user_feedback": [
        {
            "look": "self",
            "finding": "network_pressure_from_1and1_migration",
            "feedback_type": "confirmed",
            "comment": null
        },
        {
            "look": "opportunities",
            "finding": "b2b_cloud_security",
            "feedback_type": "modified",
            "original": "Addressable Market: €2.5B",
            "modified_to": "Addressable Market: €3.0B",
            "comment": "内部评估包含了安全咨询服务"
        }
    ],
    
    "provenance": {
        "summary": { ... },
        "data_points": { ... },
        "sources_registry": { ... }
    }
}
```

---

## 六、TXT 输出规范

纯文本适合命令行输出和快速阅读：

```
════════════════════════════════════════════════════════════
  Vodafone Germany BLM 战略分析报告
  数据期间: Q3 FY26 | 生成: 2026-02-08
  数据质量: 156 个数据点, 63% 高置信度, 12 处冲突
════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────
  01. 看市场 — 市场发生了什么变化？
──────────────────────────────────────────────────────────

  [市场快照]
    总收入: €13.4B | 移动用户: 158.5M | 5G 渗透: 85%

  [🟢 机会]
    • [短期] 1&1 网络不稳定期，用户可能流动
    • [中期] AI 流量需求增长，网络容量成为竞争力

  [🔴 威胁]
    • [短期] O2 激进降价抢夺中低端用户
    • [长期] Fiber 替代 Cable 趋势加速

  → 总体判断: 市场环境复杂，机会与威胁并存

──────────────────────────────────────────────────────────
  02. 看自己 — 健康体检
──────────────────────────────────────────────────────────

  [经营指标]
    收入: €3.092B | EBITDA: 36.2% | ARPU: €12.8 | 净增: +80K
    
  [网络]
    技术组合: Cable 70% + Fiber 转售 15% + Fiber 自有 5% + DSL 10%
    5G 覆盖: 90% | 演进: NSA 为主, SA 计划 2026
    ⚠ 光纤自有率低，受制于德电转售

  [优势] 品牌认知 | 企业客户能力 | Cable 网络广覆盖
  [短板] 5G 覆盖落后 | 光纤自主可控不足 | 利润率低于德电
  [⚠ 暴露面]
    • 迁入 1100 万用户 → 网络负荷 → 对手攻击网络体验
      严重程度: HIGH

... (后续看对手/看宏观/看机会/三定 同样结构)

──────────────────────────────────────────────────────────
  数据溯源
──────────────────────────────────────────────────────────
  主要来源: Vodafone Q3 FY26 Trading Update (42 个数据点)
  完整溯源: blm-analyze explain "Vodafone Germany" <field> "Q3 FY26"
════════════════════════════════════════════════════════════
```

---

## 七、PPT 设计规则

### 7.1 版式

- **Slide 尺寸**：16:9（13.333" × 7.5"）
- **安全区域**：上下左右各留 0.5" 边距
- **页码**：右下角，小字号

### 7.2 色彩使用

- **品牌主色**：封面背景、Section 分隔页、数据高亮、图表主色
- **正面/增长**：统一用 `positive_color`（绿色系）
- **负面/下降**：统一用 `negative_color`（红色系或品牌色）
- **警告/注意**：统一用 `warning_color`（橙色系）
- **背景色层**：白色 → 浅灰 → 品牌色浅底（信息层次递进）

### 7.3 图表规则

- 图表主角运营商用品牌色，竞对用灰色系（区分但不喧宾夺主）
- 图表标题：左对齐，heading_size
- 图表来源标注：右下角，footnote_size
- 所有数字标注单位

### 7.4 文字规则

- 中文用 `cjk_font`，英文/数字用 `body_font`
- 标题层级：title → subtitle → heading → body → small → footnote
- 每页内容控制在一屏可读（不要出现需要翻屏的密集文字）
- Findings/结论用简洁句式，每条不超过两行

### 7.5 脚注

- 数据密集的页面底部加一行：
  `数据来源: {主要来源} | 数据期间: {period} | 详见附录`
- 字号：footnote_size（9pt）
- 颜色：light_text_color

---

## 八、与现有代码的改造关系

| 文件 | 改造 |
|------|------|
| `src/blm/ppt_generator.py` | PPTStyle 扩展（增加 positive/negative/warning/cjk_font 等字段）；新增 OPERATOR_STYLES 注册表 |
| `src/blm/ppt_generator_enhanced.py` | 五看部分从一个通用 `_add_insight_slide()` 拆分为每看专用方法；新增 S08 网络深度页、S10-S12 对手详细页、S16 机会清单页、S26 溯源附录页 |
| `src/blm/report_generator.py` | HTML 模板增加溯源 tooltip 和人机共创标注；JSON 结构升级为新的五看输出模型；TXT 格式按新规范重写 |
| `src/blm/comprehensive_analysis_ppt.py` | 接入品牌风格系统（现在是硬编码华为配色）|
| 新建 `src/blm/ppt_styles.py` | 独立的运营商风格库 |
