# BLM 财报时间维度对齐规范
# Financial Period Alignment Specification

---

## 一、问题描述

### 1.1 财年 vs 日历年

不同运营商使用不同的财年：

| 运营商 | 财年 | 含义 | Q3 对应的绝对时间 |
|--------|------|------|------------------|
| **Vodafone** | FY26 = 2025.04 → 2026.03 | 4月起算 | Q3 FY26 = 2025.10 → 2025.12 |
| **Deutsche Telekom** | 2025 = 2025.01 → 2025.12 | 日历年 | Q4 2025 = 2025.10 → 2025.12 |
| **Telefónica O2** | 2025 = 2025.01 → 2025.12 | 日历年 | Q4 2025 = 2025.10 → 2025.12 |
| **1&1 AG** | 2025 = 2025.01 → 2025.12 | 日历年 | Q4 2025 = 2025.10 → 2025.12 |

**同一段时间（2025年10月-12月），四家运营商的叫法各不相同：**
- Vodafone：Q3 FY26
- 其他三家：Q4 2025

如果按字面把 Q3 和 Q3 对齐，对比结果就是错的。

### 1.2 财报发布时间不同步

同一个季度，各家运营商的财报发布日期不同：

```
2025年10月-12月 这个季度：
  Vodafone (Q3 FY26):     2026年2月5日发布
  Deutsche Telekom (Q4):  2026年2月27日发布
  O2 (Q4):                2026年2月20日发布
  1&1 (Q4):               2026年3月6日发布
```

所以在 2026年2月8日做分析时：
- Vodafone 已发布 ✅
- Deutsche Telekom 未发布 ❌（还要等19天）
- O2 未发布 ❌（还要等12天）
- 1&1 未发布 ❌（还要等26天）

---

## 二、解决方案：标准化时间轴

### 2.1 核心概念

数据库内部使用**自然季度（Calendar Quarter）**作为统一的时间标准：

```
标准季度标识 = "CQ{Q}_{YEAR}"

CQ1_2025 = 2025年1月 → 2025年3月
CQ2_2025 = 2025年4月 → 2025年6月
CQ3_2025 = 2025年7月 → 2025年9月
CQ4_2025 = 2025年10月 → 2025年12月
```

每条数据记录同时保存：
- `period`：运营商自己的叫法（"Q3 FY26"）——用于显示
- `calendar_quarter`：标准化后的自然季度（"CQ4_2025"）——用于对齐和对比
- `period_start` / `period_end`：精确的起止日期——用于排序

### 2.2 数据库 Schema 更新

```sql
-- financial_quarterly 表更新
CREATE TABLE financial_quarterly (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id     TEXT NOT NULL REFERENCES operators(operator_id),
    
    -- 运营商原始期间标识（用于显示）
    period          TEXT NOT NULL,               -- "Q3 FY26" / "Q4 2025"
    
    -- 标准化时间（用于对齐和对比）
    calendar_quarter TEXT NOT NULL,              -- "CQ4_2025" ← 统一标识
    period_start    DATE NOT NULL,              -- 2025-10-01
    period_end      DATE NOT NULL,              -- 2025-12-31
    
    -- 财报发布信息
    report_date     DATE,                       -- 2026-02-05（财报发布日）
    report_status   TEXT DEFAULT 'published',   -- "published" / "pending" / "estimated"
    
    -- ... 其余字段不变
    
    UNIQUE(operator_id, calendar_quarter)  -- 用 calendar_quarter 而不是 period 做唯一约束
);

-- subscriber_quarterly 表同样更新
CREATE TABLE subscriber_quarterly (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id     TEXT NOT NULL REFERENCES operators(operator_id),
    
    period          TEXT NOT NULL,
    calendar_quarter TEXT NOT NULL,
    period_start    DATE NOT NULL,
    period_end      DATE NOT NULL,
    report_status   TEXT DEFAULT 'published',
    
    -- ... 其余字段不变
    
    UNIQUE(operator_id, calendar_quarter)
);
```

### 2.3 运营商财年配置

```python
# src/database/operator_directory.py 中增加财年配置

OPERATOR_DIRECTORY = {
    "vodafone_germany": {
        "display_name": "Vodafone Germany",
        # ...
        "fiscal_year_start_month": 4,   # 4月开始
        "fiscal_year_label": "FY",      # 使用 "FY26" 格式
        "quarter_naming": "fiscal",     # "fiscal" = Q1 从财年起算 / "calendar" = Q1 从1月起算
    },
    "deutsche_telekom": {
        "display_name": "Deutsche Telekom",
        # ...
        "fiscal_year_start_month": 1,   # 1月开始（日历年）
        "fiscal_year_label": "",        # 使用 "2025" 格式
        "quarter_naming": "calendar",
    },
    "o2_germany": {
        "display_name": "Telefónica O2 Germany",
        # ...
        "fiscal_year_start_month": 1,
        "fiscal_year_label": "",
        "quarter_naming": "calendar",
    },
    "one_and_one": {
        "display_name": "1&1 AG",
        # ...
        "fiscal_year_start_month": 1,
        "fiscal_year_label": "",
        "quarter_naming": "calendar",
    },
    # 其他全球运营商的财年配置
    "bt_group": {
        "fiscal_year_start_month": 4,   # BT 也是4月开始
        "fiscal_year_label": "FY",
        "quarter_naming": "fiscal",
    },
    "ntt_docomo": {
        "fiscal_year_start_month": 4,   # 日本运营商也是4月
        "fiscal_year_label": "FY",
        "quarter_naming": "fiscal",
    },
    # 大部分运营商是日历年...
}
```

### 2.4 期间转换工具

```python
# src/database/period_utils.py

from datetime import date
from dataclasses import dataclass


@dataclass
class PeriodInfo:
    """一个财报期间的完整信息"""
    operator_period: str      # 运营商叫法: "Q3 FY26"
    calendar_quarter: str     # 标准化: "CQ4_2025"
    period_start: date        # 2025-10-01
    period_end: date          # 2025-12-31
    fiscal_year: str          # "FY26" / "2025"
    fiscal_quarter: int       # 3（运营商视角的第几季度）
    calendar_year: int        # 2025
    calendar_q: int           # 4（自然年的第几季度）


class PeriodConverter:
    """财年 ↔ 自然季度 转换器"""

    def __init__(self, fiscal_year_start_month: int = 1, 
                 fiscal_year_label: str = "",
                 quarter_naming: str = "calendar"):
        self.fy_start = fiscal_year_start_month
        self.fy_label = fiscal_year_label
        self.naming = quarter_naming

    def to_calendar_quarter(self, operator_period: str) -> PeriodInfo:
        """将运营商自己的期间标识转换为标准化信息
        
        示例:
            vodafone_converter.to_calendar_quarter("Q3 FY26")
            → PeriodInfo(calendar_quarter="CQ4_2025", period_start=2025-10-01, ...)
            
            dt_converter.to_calendar_quarter("Q4 2025")
            → PeriodInfo(calendar_quarter="CQ4_2025", period_start=2025-10-01, ...)
        """
        # 解析运营商的期间标识
        fiscal_q, fiscal_year = self._parse_period(operator_period)
        
        # 计算绝对月份
        if self.fy_start == 1:
            # 日历年：Q1=1月, Q2=4月, Q3=7月, Q4=10月
            start_month = (fiscal_q - 1) * 3 + 1
            year = fiscal_year
        else:
            # 非标准财年：如 Vodafone FY 从4月开始
            # Q1 FY26 = 2025年4月, Q2 FY26 = 2025年7月, Q3 FY26 = 2025年10月
            start_month = self.fy_start + (fiscal_q - 1) * 3
            year = fiscal_year - 1  # FY26 的前三个季度在 2025 年
            if start_month > 12:
                start_month -= 12
                year += 1
        
        # 计算自然季度
        calendar_q = (start_month - 1) // 3 + 1
        
        # 构建日期
        period_start = date(year, start_month, 1)
        end_month = start_month + 2
        end_year = year
        if end_month > 12:
            end_month -= 12
            end_year += 1
        
        # 月末日期
        import calendar as cal
        last_day = cal.monthrange(end_year, end_month)[1]
        period_end = date(end_year, end_month, last_day)
        
        return PeriodInfo(
            operator_period=operator_period,
            calendar_quarter=f"CQ{calendar_q}_{year}",
            period_start=period_start,
            period_end=period_end,
            fiscal_year=f"{self.fy_label}{fiscal_year}" if self.fy_label else str(fiscal_year),
            fiscal_quarter=fiscal_q,
            calendar_year=year,
            calendar_q=calendar_q,
        )

    def from_calendar_quarter(self, cq: str) -> str:
        """将标准化季度转换回运营商的叫法
        
        示例:
            vodafone_converter.from_calendar_quarter("CQ4_2025")
            → "Q3 FY26"
            
            dt_converter.from_calendar_quarter("CQ4_2025")
            → "Q4 2025"
        """
        # 解析标准季度
        parts = cq.replace("CQ", "").split("_")
        cal_q = int(parts[0])
        cal_year = int(parts[1])
        
        if self.fy_start == 1:
            # 日历年：直接返回
            return f"Q{cal_q} {cal_year}"
        else:
            # 计算对应的财年季度
            start_month = (cal_q - 1) * 3 + 1
            months_since_fy_start = (start_month - self.fy_start) % 12
            fiscal_q = months_since_fy_start // 3 + 1
            
            # 计算财年
            if start_month >= self.fy_start:
                fy = cal_year + 1
            else:
                fy = cal_year
            
            return f"Q{fiscal_q} {self.fy_label}{fy}"

    def generate_timeline(self, n_quarters: int = 8, 
                          end_cq: str = None) -> list[str]:
        """生成连续 N 个季度的标准化时间线
        
        返回:
            ["CQ1_2024", "CQ2_2024", ..., "CQ4_2025"]
        """
        if end_cq is None:
            today = date.today()
            end_q = (today.month - 1) // 3 + 1
            end_year = today.year
        else:
            parts = end_cq.replace("CQ", "").split("_")
            end_q = int(parts[0])
            end_year = int(parts[1])
        
        timeline = []
        q, y = end_q, end_year
        for _ in range(n_quarters):
            timeline.append(f"CQ{q}_{y}")
            q -= 1
            if q == 0:
                q = 4
                y -= 1
        
        return list(reversed(timeline))

    def _parse_period(self, period: str) -> tuple[int, int]:
        """解析运营商期间标识为 (季度, 年份)"""
        import re
        
        # "Q3 FY26" → (3, 26→2026)
        m = re.match(r'Q(\d)\s*(?:FY)?(\d{2,4})', period, re.IGNORECASE)
        if m:
            q = int(m.group(1))
            y = int(m.group(2))
            if y < 100:
                y += 2000
            return q, y
        
        raise ValueError(f"Cannot parse period: {period}")


# 预置转换器
CONVERTERS = {
    "vodafone_germany": PeriodConverter(fiscal_year_start_month=4, 
                                         fiscal_year_label="FY",
                                         quarter_naming="fiscal"),
    "deutsche_telekom": PeriodConverter(),   # 默认日历年
    "o2_germany": PeriodConverter(),
    "one_and_one": PeriodConverter(),
    "bt_group": PeriodConverter(fiscal_year_start_month=4,
                                 fiscal_year_label="FY",
                                 quarter_naming="fiscal"),
}

def get_converter(operator_id: str) -> PeriodConverter:
    """获取运营商的期间转换器"""
    return CONVERTERS.get(operator_id, PeriodConverter())
```

---

## 三、对齐后的对比逻辑

### 3.1 数据入库时自动对齐

```python
class TelecomDatabase:
    
    def upsert_financial(self, operator_id: str, period: str, data: dict, ...):
        """写入财务数据时，自动计算 calendar_quarter"""
        converter = get_converter(operator_id)
        period_info = converter.to_calendar_quarter(period)
        
        data["calendar_quarter"] = period_info.calendar_quarter
        data["period_start"] = period_info.period_start
        data["period_end"] = period_info.period_end
        # ... 正常入库
```

### 3.2 跨运营商对比时按 calendar_quarter 对齐

```python
def get_market_comparison(self, market: str, calendar_quarter: str) -> pd.DataFrame:
    """获取同一自然季度内所有运营商的数据
    
    示例:
        get_market_comparison("germany", "CQ4_2025")
        → 返回 Vodafone (Q3 FY26), DT (Q4 2025), O2 (Q4 2025), 1&1 (Q4 2025)
          全部是 2025.10-12 的数据，正确对齐
    """
    with self._conn() as conn:
        return pd.read_sql("""
            SELECT f.*, o.display_name, f.period as operator_period
            FROM financial_quarterly f
            JOIN operators o ON f.operator_id = o.operator_id
            WHERE o.market = ? AND f.calendar_quarter = ?
        """, conn, params=(market, calendar_quarter))
```

### 3.3 处理未发布的情况

```python
def get_market_comparison_latest(self, market: str) -> pd.DataFrame:
    """获取每个运营商的最新可用数据
    
    当部分运营商尚未发布最新季报时，
    返回的数据中该运营商的 report_status = 'pending'
    """
    with self._conn() as conn:
        # 先确定最新的标准季度
        latest_cq = conn.execute("""
            SELECT MAX(calendar_quarter) FROM financial_quarterly f
            JOIN operators o ON f.operator_id = o.operator_id
            WHERE o.market = ?
        """, (market,)).fetchone()[0]
        
        # 获取该季度所有运营商的数据
        result = pd.read_sql("""
            SELECT f.*, o.display_name, o.operator_id
            FROM financial_quarterly f
            JOIN operators o ON f.operator_id = o.operator_id
            WHERE o.market = ? AND f.calendar_quarter = ?
        """, conn, params=(market, latest_cq))
        
        # 检查哪些运营商缺数据
        all_operators = pd.read_sql(
            "SELECT operator_id, display_name FROM operators WHERE market=? AND is_active=TRUE",
            conn, params=(market,)
        )
        
        missing = set(all_operators["operator_id"]) - set(result["operator_id"])
        
        # 对缺失的运营商，标记为 pending
        for op_id in missing:
            op_name = all_operators[all_operators["operator_id"] == op_id]["display_name"].iloc[0]
            pending_row = {
                "operator_id": op_id,
                "display_name": op_name,
                "calendar_quarter": latest_cq,
                "report_status": "pending",
                # 所有数值字段为 None
            }
            result = pd.concat([result, pd.DataFrame([pending_row])], ignore_index=True)
        
        return result
```

---

## 四、显示规则

### 4.1 图表和表格中的时间轴显示

**X 轴标签：双行显示**

```
图表 X 轴（8 个季度）：

    CQ1_2024    CQ2_2024    CQ3_2024    CQ4_2024    CQ1_2025    CQ2_2025    CQ3_2025    CQ4_2025
    ─────────   ─────────   ─────────   ─────────   ─────────   ─────────   ─────────   ─────────
    2024.1-3    2024.4-6    2024.7-9    2024.10-12  2025.1-3    2025.4-6    2025.7-9    2025.10-12
```

或者更简洁：

```
    Q1'24    Q2'24    Q3'24    Q4'24    Q1'25    Q2'25    Q3'25    Q4'25
```

这里用**自然季度**做 X 轴，不用任何运营商的财年叫法，避免混淆。

### 4.2 数据表中的标注

当对比表中需要显示运营商原始期间名时，用括号标注：

```
| 指标          | Vodafone         | DT              | O2              |
|              | (Q3 FY26)        | (Q4 2025)       | (Q4 2025)       |
|              | 2025.10-12       | 2025.10-12      | 2025.10-12      |
|─────────────|─────────────────|────────────────|────────────────|
| 收入 (€M)    | 3,092            | 6,200           | 2,000           |
| EBITDA (%)   | 36.2%            | 42.1%           | 32.5%           |
```

### 4.3 未发布数据的显示

```
| 指标          | Vodafone         | DT              | O2              |
|              | (Q3 FY26) ✅     | (Q4 2025) ⏳    | (Q4 2025) ⏳    |
|─────────────|─────────────────|────────────────|────────────────|
| 收入 (€M)    | 3,092            | 待发布 (2/27)   | 待发布 (2/20)   |
| EBITDA (%)   | 36.2%            | —               | —               |
```

PPT 中：
- ✅ 已发布的数据正常显示
- ⏳ 未发布的单元格灰底 + "待发布" + 预计发布日期
- 不要用上一季度的数据冒充——空就是空

### 4.4 历史趋势图中的处理

8/12 个季度趋势图中，如果最新季度某个运营商数据缺失：
- 趋势线画到最后一个有数据的季度为止
- 不要用虚线预估
- 图例旁标注 "(截至 CQ3_2025)"

---

## 五、时间线长度

### 5.1 标准时间跨度

| 分析类型 | 推荐季度数 | 说明 |
|---------|-----------|------|
| 标准趋势分析 | 8 季度（2 年） | 足以看到趋势，不过分冗长 |
| 深度趋势分析 | 12 季度（3 年） | 看完整的策略周期 |
| 数据库最大存储 | 不限 | 有多少存多少，查询时按需截取 |

### 5.2 CLI 命令支持

```bash
# 默认 8 季度
blm-analyze run "Vodafone Germany" --format ppt

# 指定 12 季度
blm-analyze run "Vodafone Germany" --format ppt --quarters 12

# 指定时间范围
blm-analyze run "Vodafone Germany" --from CQ1_2023 --to CQ4_2025
```

---

## 六、财报发布日历

系统需要维护各运营商的预期发布日历，用于：
1. 提醒用户何时可以更新数据
2. 在对比中标注"⏳待发布"

```python
# 预期发布窗口（基于历史模式，每年可更新）
EARNINGS_CALENDAR = {
    "vodafone_germany": {
        # Vodafone FY26: Q1=Jul, Q2=Nov, Q3=Feb, Q4/Annual=May
        "Q1": {"months_after_period_end": 1, "typical_day": 20},
        "Q2": {"months_after_period_end": 1, "typical_day": 12},
        "Q3": {"months_after_period_end": 1, "typical_day": 5},
        "Q4": {"months_after_period_end": 2, "typical_day": 20},
    },
    "deutsche_telekom": {
        # DT: Q1=May, Q2=Aug, Q3=Nov, Q4/Annual=Feb末
        "Q1": {"months_after_period_end": 2, "typical_day": 15},
        "Q2": {"months_after_period_end": 1, "typical_day": 10},
        "Q3": {"months_after_period_end": 1, "typical_day": 10},
        "Q4": {"months_after_period_end": 2, "typical_day": 27},
    },
    # ...
}
```

---

## 七、需要更新的文件清单

| 文件 | 变更 |
|------|------|
| `src/database/schema.sql` | 所有季度表增加 `calendar_quarter`, `period_start`, `period_end`, `report_status` 字段；唯一约束改为 `(operator_id, calendar_quarter)` |
| `src/database/db.py` | `upsert_*` 方法自动调用 PeriodConverter 计算标准季度；新增 `get_market_comparison()` 方法 |
| `src/database/operator_directory.py` | 增加 `fiscal_year_start_month` 等财年配置 |
| 新建 `src/database/period_utils.py` | PeriodConverter 类 + 预置转换器 |
| `src/blm/ppt_generator_enhanced.py` | 图表 X 轴用自然季度标签；对比表双行显示（运营商叫法 + 绝对时间）；未发布数据灰底处理 |
| `src/blm/ppt_charts.py` | 趋势图支持缺失数据点（线段中断）|
