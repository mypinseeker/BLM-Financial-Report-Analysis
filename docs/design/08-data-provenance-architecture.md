# BLM 数据溯源架构设计
# Data Provenance & Lineage System

---

## 问题陈述

当前代码的问题（以 `germany_telecom_analysis.py` 第 61 行为例）：

```python
"revenue_eur_billion": 3.092,  # Total revenue €3,092M   ← 这个 3.092 哪来的？
```

你现在只有一行注释 `_source: "Vodafone Q3 FY26 Trading Update, Feb 5, 2026"` 挂在整个运营商字典上。
但你无法回答：

- 这个 3.092 具体来自 PDF 的第几页？
- 解析时是表格提取还是文本正则匹配？
- 是否有其他来源给出不同数字？如果有，为什么选了这个？
- 这个数据是什么时候采集的？是否已过期？

**你的目标：**
> PPT 上的每一个数字，我都能追溯到原始来源链接和提取方式。

---

## 1. 核心数据模型设计

### 1.1 SourceReference — 数据来源引用

```python
# src/collectors/provenance.py

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class SourceType(Enum):
    """数据来源类型"""
    FINANCIAL_REPORT_PDF = "financial_report_pdf"
    EARNINGS_CALL_TRANSCRIPT = "earnings_call_transcript"
    INVESTOR_PRESENTATION = "investor_presentation"
    EXCEL_DATA = "excel_data"
    REGULATORY_REPORT = "regulatory_report"      # BNetzA 等监管机构
    GOVERNMENT_STATISTICS = "government_statistics"  # Destatis, IMF
    NEWS_ARTICLE = "news_article"
    ANALYST_REPORT = "analyst_report"
    COMPANY_PRESS_RELEASE = "press_release"
    WEBSITE_SCRAPE = "website_scrape"             # 资费页面等
    NETWORK_TEST = "network_test"                 # Connect/Chip 测试
    SOCIAL_MEDIA = "social_media"                 # LinkedIn 等
    CALCULATED = "calculated"                     # 由其他数据计算得出
    AI_EXTRACTED = "ai_extracted"                 # Claude API 辅助提取
    MANUAL = "manual"                             # 手工录入（兼容现有数据）


class Confidence(Enum):
    """数据置信度"""
    HIGH = "high"          # 来自一手来源（运营商官方财报），完全匹配
    MEDIUM = "medium"      # 来自权威二手来源，或一手来源但有解析不确定性
    LOW = "low"            # 来自媒体报道/推算/AI 提取
    ESTIMATED = "estimated"  # 不可得的数据，基于其他数据推算


class FreshnessStatus(Enum):
    """数据时效性状态"""
    CURRENT = "current"        # 在有效期内
    STALE = "stale"            # 过期但仍可参考
    EXPIRED = "expired"        # 已过期，不应使用
    UNKNOWN = "unknown"        # 无法确定


@dataclass
class SourceReference:
    """单个数据来源引用 — 系统中最基本的溯源单元"""

    # 来源标识
    source_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    source_type: SourceType = SourceType.MANUAL

    # 来源定位
    url: Optional[str] = None               # 原始链接
    document_name: Optional[str] = None     # 文档名称 "Vodafone Q3 FY26 Trading Update"
    page_number: Optional[int] = None       # PDF 页码
    table_index: Optional[int] = None       # 页内第几个表格
    section: Optional[str] = None           # 章节名称 "Financial Highlights"
    cell_reference: Optional[str] = None    # 单元格位置 "Row 3, Col 2"

    # 来源组织
    publisher: Optional[str] = None         # 发布者 "Vodafone Group"
    author: Optional[str] = None            # 作者（如分析师姓名）

    # 时间维度
    publication_date: Optional[datetime] = None   # 来源的发布日期
    data_period: Optional[str] = None             # 数据所属期间 "Q3 FY26"
    collected_at: Optional[datetime] = None       # 我们采集的时间
    expires_at: Optional[datetime] = None         # 数据过期时间

    # 提取方式
    extraction_method: Optional[str] = None  # "table_extraction", "regex", "ai_extraction"
    extraction_confidence: float = 1.0       # 0.0 - 1.0 提取算法的置信度
    raw_text: Optional[str] = None           # 提取时的原始文本片段

    # 置信度
    confidence: Confidence = Confidence.HIGH

    @property
    def freshness(self) -> FreshnessStatus:
        """计算数据时效性"""
        if self.expires_at is None:
            return FreshnessStatus.UNKNOWN
        now = datetime.now()
        if now < self.expires_at:
            return FreshnessStatus.CURRENT
        # 过期不超过 30 天 → stale
        days_expired = (now - self.expires_at).days
        if days_expired <= 30:
            return FreshnessStatus.STALE
        return FreshnessStatus.EXPIRED

    def to_citation(self) -> str:
        """生成人类可读的引用文本"""
        parts = []
        if self.document_name:
            parts.append(self.document_name)
        if self.publisher:
            parts.append(f"by {self.publisher}")
        if self.publication_date:
            parts.append(f"({self.publication_date.strftime('%Y-%m-%d')})")
        if self.page_number is not None:
            parts.append(f"p.{self.page_number}")
        if self.section:
            parts.append(f"§{self.section}")
        return ", ".join(parts)
```

### 1.2 TrackedValue — 带溯源的数据值

```python
@dataclass
class TrackedValue:
    """一个带有完整溯源链的数据值 — 系统的核心单元。
    
    每一个出现在分析报告中的数字/文本，都应该是一个 TrackedValue。
    """

    # 值本身
    value: any                                  # 数值或文本
    field_name: str                             # 字段名 "revenue_eur_billion"
    operator: Optional[str] = None              # 所属运营商 "Vodafone Germany"
    period: Optional[str] = None                # 所属时间段 "Q3 FY26"

    # 溯源链
    primary_source: Optional[SourceReference] = None    # 主来源（最终采信的来源）
    alternative_sources: list[SourceReference] = field(default_factory=list)  # 其他来源
    
    # 冲突解决
    conflict_resolution: Optional[str] = None   # 如有冲突，为什么选了 primary_source
    # 例如: "Vodafone 官方 Trading Update 数据优先于 Reuters 报道"

    # 计算链
    derived_from: list['TrackedValue'] = field(default_factory=list)  # 如果是计算值，从哪些值计算而来
    derivation_formula: Optional[str] = None    # 计算公式 "total_revenue = sum(all operators)"

    # 元信息
    unit: Optional[str] = None                  # "EUR billion", "%", "million"
    last_updated: Optional[datetime] = None

    @property
    def confidence(self) -> Confidence:
        """综合置信度 = 最低来源置信度"""
        if self.primary_source:
            return self.primary_source.confidence
        return Confidence.ESTIMATED

    @property
    def freshness(self) -> FreshnessStatus:
        if self.primary_source:
            return self.primary_source.freshness
        return FreshnessStatus.UNKNOWN

    @property
    def has_conflict(self) -> bool:
        return len(self.alternative_sources) > 0

    def explain(self) -> str:
        """生成完整的数据溯源说明 — 回答'这个数字怎么来的？'"""
        lines = []
        lines.append(f"📊 {self.field_name} = {self.value} {self.unit or ''}")
        lines.append(f"   运营商: {self.operator or 'N/A'} | 时期: {self.period or 'N/A'}")
        lines.append(f"   置信度: {self.confidence.value} | 时效: {self.freshness.value}")
        
        if self.primary_source:
            lines.append(f"   📌 主来源: {self.primary_source.to_citation()}")
            if self.primary_source.url:
                lines.append(f"      链接: {self.primary_source.url}")
            if self.primary_source.extraction_method:
                lines.append(f"      提取方式: {self.primary_source.extraction_method}")
            if self.primary_source.raw_text:
                lines.append(f"      原文: \"{self.primary_source.raw_text[:100]}...\"")
        
        if self.alternative_sources:
            lines.append(f"   ⚠️ 存在 {len(self.alternative_sources)} 个其他来源:")
            for alt in self.alternative_sources:
                lines.append(f"      - {alt.to_citation()} → 值: 未采信")
            if self.conflict_resolution:
                lines.append(f"   🔍 采信理由: {self.conflict_resolution}")
        
        if self.derived_from:
            lines.append(f"   🔗 计算来源: {self.derivation_formula or '见依赖值'}")
            for dep in self.derived_from:
                lines.append(f"      ← {dep.field_name} = {dep.value}")
        
        return "\n".join(lines)
```

### 1.3 ProvenanceStore — 全局溯源存储

```python
class ProvenanceStore:
    """全局溯源数据库 — 管理本次分析中所有 TrackedValue 的注册和查询。
    
    这是回答"PPT 第 X 页第 Y 个数字怎么来的？"的核心组件。
    """

    def __init__(self):
        self._values: dict[str, TrackedValue] = {}  # key → TrackedValue
        self._sources: dict[str, SourceReference] = {}  # source_id → SourceReference

    # === 注册 ===

    def register_source(self, source: SourceReference) -> str:
        """注册一个数据来源"""
        self._sources[source.source_id] = source
        return source.source_id

    def register_value(self, tracked_value: TrackedValue) -> str:
        """注册一个带溯源的数据值"""
        key = self._make_key(tracked_value.operator, tracked_value.field_name, tracked_value.period)
        self._values[key] = tracked_value
        if tracked_value.primary_source:
            self.register_source(tracked_value.primary_source)
        for alt in tracked_value.alternative_sources:
            self.register_source(alt)
        return key

    def track(self, value, field_name, operator=None, period=None,
              source=None, unit=None, **kwargs) -> TrackedValue:
        """快捷方法：创建并注册一个 TrackedValue"""
        tv = TrackedValue(
            value=value,
            field_name=field_name,
            operator=operator,
            period=period,
            primary_source=source,
            unit=unit,
            last_updated=datetime.now(),
            **kwargs,
        )
        self.register_value(tv)
        return tv

    # === 查询 ===

    def explain(self, operator: str, field_name: str, period: str = None) -> str:
        """查询一个数据点的完整溯源说明"""
        key = self._make_key(operator, field_name, period)
        tv = self._values.get(key)
        if tv is None:
            return f"❌ 未找到溯源记录: {operator}.{field_name} ({period})"
        return tv.explain()

    def get_value(self, operator: str, field_name: str, period: str = None) -> Optional[TrackedValue]:
        key = self._make_key(operator, field_name, period)
        return self._values.get(key)

    def get_all_for_operator(self, operator: str) -> list[TrackedValue]:
        return [v for v in self._values.values() if v.operator == operator]

    def get_conflicts(self) -> list[TrackedValue]:
        """返回所有存在来源冲突的数据点"""
        return [v for v in self._values.values() if v.has_conflict]

    def get_stale_data(self) -> list[TrackedValue]:
        """返回所有过期或即将过期的数据点"""
        return [v for v in self._values.values() 
                if v.freshness in (FreshnessStatus.STALE, FreshnessStatus.EXPIRED)]

    def get_low_confidence(self) -> list[TrackedValue]:
        """返回所有低置信度数据点"""
        return [v for v in self._values.values() 
                if v.confidence in (Confidence.LOW, Confidence.ESTIMATED)]

    # === 数据质量报告 ===

    def quality_report(self) -> dict:
        """生成数据质量总结"""
        total = len(self._values)
        return {
            "total_data_points": total,
            "high_confidence": sum(1 for v in self._values.values() if v.confidence == Confidence.HIGH),
            "medium_confidence": sum(1 for v in self._values.values() if v.confidence == Confidence.MEDIUM),
            "low_confidence": sum(1 for v in self._values.values() if v.confidence == Confidence.LOW),
            "estimated": sum(1 for v in self._values.values() if v.confidence == Confidence.ESTIMATED),
            "with_conflicts": sum(1 for v in self._values.values() if v.has_conflict),
            "stale_data": sum(1 for v in self._values.values() if v.freshness == FreshnessStatus.STALE),
            "expired_data": sum(1 for v in self._values.values() if v.freshness == FreshnessStatus.EXPIRED),
            "unique_sources": len(self._sources),
        }

    # === 序列化 ===

    def to_json(self) -> dict:
        """导出完整溯源数据（可保存到文件，供 API 查询）"""
        ...

    def to_footnotes(self) -> list[str]:
        """导出为脚注列表（可放到 PPT/报告末尾）"""
        ...

    # === 内部 ===

    @staticmethod
    def _make_key(operator, field_name, period=None):
        parts = [operator or "_global", field_name]
        if period:
            parts.append(period)
        return "::".join(parts)
```

---

## 2. 冲突解决引擎

当多个来源给出不同数字时，系统需要自动判断采信哪个。

```python
# src/collectors/conflict_resolver.py

class ConflictResolver:
    """数据冲突解决引擎
    
    优先级规则（从高到低）：
    1. 运营商官方一手来源（财报 PDF/新闻稿）> 二手来源（媒体/分析师）
    2. 同一来源类型中，日期更新的 > 日期更旧的
    3. 数据粒度更细的 > 更粗的（如季报 > 年报中的季度推算）
    4. 多个来源一致的值 > 孤证
    5. 监管机构数据 > 运营商自报数据（对于市场份额等）
    """

    # 来源类型优先级（数字越大优先级越高）
    SOURCE_PRIORITY = {
        SourceType.FINANCIAL_REPORT_PDF: 100,
        SourceType.EXCEL_DATA: 95,
        SourceType.INVESTOR_PRESENTATION: 90,
        SourceType.EARNINGS_CALL_TRANSCRIPT: 85,
        SourceType.COMPANY_PRESS_RELEASE: 80,
        SourceType.REGULATORY_REPORT: 95,         # 监管机构数据很权威
        SourceType.GOVERNMENT_STATISTICS: 90,
        SourceType.NETWORK_TEST: 85,
        SourceType.ANALYST_REPORT: 60,
        SourceType.NEWS_ARTICLE: 50,
        SourceType.WEBSITE_SCRAPE: 70,
        SourceType.AI_EXTRACTED: 40,
        SourceType.SOCIAL_MEDIA: 30,
        SourceType.CALCULATED: 75,
        SourceType.MANUAL: 10,
    }

    def resolve(self, candidates: list[tuple[any, SourceReference]]) -> TrackedValue:
        """从多个候选值中选出最佳值。
        
        Args:
            candidates: [(value, source_ref), ...] — 每个来源给出的值和来源信息
            
        Returns:
            TrackedValue — 包含主来源和其他来源的完整记录
        """
        if not candidates:
            raise ValueError("No candidates to resolve")
        
        if len(candidates) == 1:
            value, source = candidates[0]
            return TrackedValue(
                value=value,
                primary_source=source,
                field_name="",  # 调用者填充
            )

        # 按优先级排序
        scored = []
        for value, source in candidates:
            score = self._calculate_score(source)
            scored.append((score, value, source))
        scored.sort(key=lambda x: x[0], reverse=True)

        # 最高分为主来源
        _, best_value, best_source = scored[0]
        alternatives = [source for _, _, source in scored[1:]]
        
        # 生成冲突解决说明
        resolution = self._explain_resolution(scored)

        return TrackedValue(
            value=best_value,
            primary_source=best_source,
            alternative_sources=alternatives,
            conflict_resolution=resolution,
            field_name="",  # 调用者填充
        )

    def _calculate_score(self, source: SourceReference) -> float:
        """计算来源综合得分"""
        score = self.SOURCE_PRIORITY.get(source.source_type, 0)

        # 时效性加权：每过期 30 天扣 10 分
        if source.publication_date:
            days_old = (datetime.now() - source.publication_date).days
            score -= max(0, (days_old - 30)) * 0.3

        # 提取置信度加权
        score *= source.extraction_confidence

        return score

    def _explain_resolution(self, scored: list) -> str:
        """生成冲突解决说明"""
        if len(scored) < 2:
            return ""
        top_score, top_value, top_source = scored[0]
        second_score, second_value, second_source = scored[1]
        
        if top_value == second_value:
            return f"多个来源一致: {top_source.source_type.value} 和 {second_source.source_type.value} 均给出相同值"
        
        return (
            f"采信 {top_source.source_type.value} "
            f"(得分 {top_score:.0f}) 优于 {second_source.source_type.value} "
            f"(得分 {second_score:.0f}). "
            f"主来源值: {top_value}, 备选值: {second_value}"
        )
```

---

## 3. 时效性管理

```python
# src/collectors/freshness.py

class FreshnessPolicy:
    """数据时效性策略
    
    不同类型的数据有不同的保鲜期。
    """

    # 数据类型 → 有效期（天）
    DEFAULT_TTL = {
        # 财务数据：下个财报发布前有效（约 90 天）
        "financial_quarterly": 90,
        "financial_annual": 365,
        
        # 市场数据：季度更新
        "market_size": 90,
        "market_share": 90,
        "tariff_pricing": 30,       # 资费可能随时变
        
        # 宏观数据：年度/季度更新
        "gdp": 90,
        "regulation": 180,
        "policy": 90,
        
        # 情报数据：快速过期
        "news": 7,                  # 新闻 7 天内有参考价值
        "analyst_rating": 30,
        "network_incident": 14,
        "executive_change": 365,    # 人事变动相对稳定
        
        # 网络数据
        "network_coverage": 90,
        "network_test_score": 180,  # 测试一般半年做一次
    }

    @classmethod
    def get_expiry(cls, data_category: str, collected_at: datetime) -> datetime:
        """计算数据过期时间"""
        ttl_days = cls.DEFAULT_TTL.get(data_category, 90)
        return collected_at + timedelta(days=ttl_days)

    @classmethod
    def should_refresh(cls, tracked_value: TrackedValue) -> bool:
        """判断数据是否应该刷新"""
        return tracked_value.freshness in (
            FreshnessStatus.STALE, 
            FreshnessStatus.EXPIRED,
        )

    @classmethod
    def filter_valid(cls, values: list[TrackedValue]) -> list[TrackedValue]:
        """过滤掉已过期的数据"""
        return [v for v in values if v.freshness != FreshnessStatus.EXPIRED]
```

---

## 4. 采集器如何产出 TrackedValue

以 `FinancialReportCollector` 为例：

```python
# src/collectors/financial_report_collector.py（伪代码）

class FinancialReportCollector(BaseCollector):

    def collect(self, operator: str, period: str = "latest") -> dict[str, TrackedValue]:
        """采集并解析财报，返回带溯源的数据"""
        
        # 1. 下载 PDF
        pdf_path = self._download_report(operator, period)
        
        # 2. 创建来源引用
        base_source = SourceReference(
            source_type=SourceType.FINANCIAL_REPORT_PDF,
            url="https://investors.vodafone.com/...",
            document_name="Vodafone Group Q3 FY26 Trading Update",
            publisher="Vodafone Group",
            publication_date=datetime(2026, 2, 5),
            data_period="Q3 FY26",
            collected_at=datetime.now(),
            expires_at=FreshnessPolicy.get_expiry("financial_quarterly", datetime.now()),
        )
        
        # 3. 解析 PDF，每个提取的数值都带上来源
        parsed = self.pdf_parser.parse(pdf_path)
        
        results = {}
        
        # 例：revenue 从表格中提取
        results["revenue_eur_billion"] = TrackedValue(
            value=3.092,
            field_name="revenue_eur_billion",
            operator="Vodafone Germany",
            period="Q3 FY26",
            unit="EUR billion",
            primary_source=SourceReference(
                **base_source.__dict__,  # 继承基础信息
                source_id=str(uuid.uuid4())[:8],
                page_number=4,
                table_index=1,
                section="Financial Highlights",
                cell_reference="Row 'Total Revenue', Col 'Q3 FY26'",
                extraction_method="table_extraction",
                extraction_confidence=0.95,
                raw_text="Total revenue €3,092m",
                confidence=Confidence.HIGH,
            ),
            last_updated=datetime.now(),
        )
        
        # 例：EBITDA margin 从文本推算
        results["ebitda_margin_pct"] = TrackedValue(
            value=36.2,
            field_name="ebitda_margin_pct",
            operator="Vodafone Germany",
            period="Q3 FY26",
            unit="%",
            primary_source=SourceReference(
                **base_source.__dict__,
                source_id=str(uuid.uuid4())[:8],
                page_number=7,
                extraction_method="calculated_from_text",
                extraction_confidence=0.8,
                raw_text="EBITDAaL contribution of 32% of Group...",
                confidence=Confidence.MEDIUM,
            ),
            derivation_formula="ebitda / revenue * 100",
            derived_from=[results["revenue_eur_billion"]],
        )
        
        return results
```

---

## 5. 分析引擎如何消费 TrackedValue

现有引擎接口（`InsightResult.metrics: dict`）不需要大改。
通过 `DataNormalizer` 做桥接：

```python
# src/collectors/normalizer.py

class DataNormalizer:
    
    def __init__(self, provenance_store: ProvenanceStore):
        self.store = provenance_store

    def to_financial_data_dict(self, tracked_data: dict[str, dict[str, TrackedValue]]) -> dict:
        """转为现有 FINANCIAL_DATA_Q3_FY26 兼容格式。
        
        输入: {"Vodafone Germany": {"revenue_eur_billion": TrackedValue(3.092, ...), ...}, ...}
        输出: {"Vodafone Germany": {"revenue_eur_billion": 3.092, ...}, ...}
        
        同时将所有 TrackedValue 注册到 ProvenanceStore。
        """
        result = {}
        for operator, fields in tracked_data.items():
            result[operator] = {}
            for field_name, tv in fields.items():
                result[operator][field_name] = tv.value  # 现有引擎只看 value
                
                # 同时注册到溯源存储
                tv.operator = operator
                tv.field_name = field_name
                self.store.register_value(tv)
        
        return result
```

这样现有的 `GermanyTelecomBLMAnalyzer` 和 `BLMPPTGeneratorEnhanced` **完全不需要修改**，
它们照常使用 `dict[str, float]`。而溯源信息平行存储在 `ProvenanceStore` 中。

---

## 6. 查询 API — "这个数字怎么来的？"

### 6.1 CLI 查询

```bash
# 查询某个具体数据点
blm-analyze provenance explain \
    --operator "Vodafone Germany" \
    --field "revenue_eur_billion" \
    --period "Q3 FY26"

# 输出：
# 📊 revenue_eur_billion = 3.092 EUR billion
#    运营商: Vodafone Germany | 时期: Q3 FY26
#    置信度: high | 时效: current
#    📌 主来源: Vodafone Group Q3 FY26 Trading Update, by Vodafone Group, (2026-02-05), p.4, §Financial Highlights
#       链接: https://investors.vodafone.com/...
#       提取方式: table_extraction (confidence: 0.95)
#       原文: "Total revenue €3,092m"

# 查看所有冲突数据
blm-analyze provenance conflicts

# 查看过期数据
blm-analyze provenance stale

# 生成数据质量报告
blm-analyze provenance quality-report
```

### 6.2 JSON API（供前端/自动化调用）

```python
# 分析完成后，provenance store 可导出为 JSON
provenance_json = store.to_json()

# 结构如下：
{
    "analysis_id": "blm_vodafone_2026-02-08",
    "generated_at": "2026-02-08T20:30:00Z",
    "quality_summary": {
        "total_data_points": 156,
        "high_confidence": 98,
        "medium_confidence": 35,
        "low_confidence": 15,
        "estimated": 8,
        "with_conflicts": 12,
        "stale_data": 3,
        "unique_sources": 28,
    },
    "data_points": {
        "Vodafone Germany::revenue_eur_billion::Q3 FY26": {
            "value": 3.092,
            "unit": "EUR billion",
            "confidence": "high",
            "freshness": "current",
            "primary_source": {
                "type": "financial_report_pdf",
                "document": "Vodafone Group Q3 FY26 Trading Update",
                "url": "https://investors.vodafone.com/...",
                "publisher": "Vodafone Group",
                "date": "2026-02-05",
                "page": 4,
                "extraction": "table_extraction",
                "raw_text": "Total revenue €3,092m"
            },
            "alternative_sources": [],
            "conflict_resolution": null
        },
        "Vodafone Germany::ebitda_margin_pct::Q3 FY26": {
            "value": 36.2,
            "confidence": "medium",
            "primary_source": { ... },
            "alternative_sources": [
                {
                    "type": "analyst_report",
                    "document": "JP Morgan - Vodafone Q3 Review",
                    "value_from_this_source": 36.5,
                    "date": "2026-02-06"
                }
            ],
            "conflict_resolution": "采信 financial_report_pdf (得分 95) 优于 analyst_report (得分 60)"
        }
    },
    "sources_registry": {
        "src_a1b2c3d4": {
            "type": "financial_report_pdf",
            "document": "Vodafone Group Q3 FY26 Trading Update",
            "url": "https://investors.vodafone.com/...",
            "publisher": "Vodafone Group",
            "date": "2026-02-05",
            "data_points_from_this_source": 42
        },
        ...
    }
}
```

### 6.3 PPT 中的溯源（脚注/附录）

在 `BLMPPTGeneratorEnhanced` 生成 PPT 时：
- 每页数据密集的 slides 底部加一行小字脚注："数据来源详见附录"
- PPT 末尾增加 **"数据来源与质量"** 附录页，列出：
  - 所有引用的来源（含链接）
  - 数据质量总结
  - 存在冲突的数据点标注

---

## 7. 与现有代码的集成方式

```
                          现有代码（不修改）
                    ┌─────────────────────────┐
                    │ GermanyTelecomBLMAnalyzer │
                    │ FiveLooksAnalyzer        │
                    │ BLMPPTGeneratorEnhanced  │
                    │                         │
                    │ 接口: dict[str, float]   │
                    └────────────▲────────────┘
                                │
                                │ .value 提取
                                │
┌───────────────────────────────┼────────────────────────────────┐
│               DataNormalizer                                   │
│                                                                │
│  TrackedValue(3.092, source=...) → {"revenue_eur_billion": 3.092}  │
│                                                                │
│  同时: ProvenanceStore.register(TrackedValue)                    │
└───────────────────────────────┼────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │   ProvenanceStore     │
                    │   (平行存储溯源信息)    │
                    │                       │
                    │   .explain(op, field) │
                    │   .quality_report()   │
                    │   .to_json()          │
                    └───────────────────────┘
```

**关键设计决策：溯源信息作为"影子层"平行存储，不侵入现有分析引擎接口。**

---

## 8. 落地到开发计划中

这不是一个单独的 Phase，而是贯穿所有 Phase 的基础设施：

| 阶段 | 溯源相关工作 |
|------|------------|
| Phase 0 | 创建 `src/collectors/provenance.py`（SourceReference + TrackedValue + ProvenanceStore） |
| Phase 0 | 创建 `src/collectors/conflict_resolver.py` |
| Phase 0 | 创建 `src/collectors/freshness.py` |
| Phase 1 | FinancialReportCollector 输出 `dict[str, TrackedValue]` 而非 `dict[str, float]` |
| Phase 2 | MarketDataCollector / MacroEnvironmentCollector 同上 |
| Phase 3 | IntelligenceMonitor 同上 |
| Phase 4 | DataNormalizer 做 TrackedValue → plain dict 转换 + ProvenanceStore 注册 |
| Phase 4 | 添加溯源查询 CLI 命令 |
| Phase 5 | PPT 生成器增加脚注/附录页 |
| Phase 5 | 生成 provenance.json 报告文件 |
