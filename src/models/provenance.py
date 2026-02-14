"""Data provenance tracking - TrackedValue and SourceReference.

Every data point in the analysis can trace back to its source document,
page, extraction method, and confidence level.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional
import uuid


class SourceType(Enum):
    FINANCIAL_REPORT_PDF = "financial_report_pdf"
    EARNINGS_CALL_TRANSCRIPT = "earnings_call_transcript"
    INVESTOR_PRESENTATION = "investor_presentation"
    REGULATORY_REPORT = "regulatory_report"
    GOVERNMENT_STATISTICS = "government_statistics"
    ANALYST_REPORT = "analyst_report"
    NEWS_ARTICLE = "news_article"
    NETWORK_TEST = "network_test"
    COMPANY_PRESS_RELEASE = "company_press_release"
    WEBSITE_SCRAPE = "website_scrape"
    AI_EXTRACTED = "ai_extracted"
    CALCULATED = "calculated"
    MANUAL = "manual"
    DATABASE_SEED = "database_seed"


class Confidence(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    ESTIMATED = "estimated"


class FreshnessStatus(Enum):
    CURRENT = "current"
    STALE = "stale"
    EXPIRED = "expired"
    UNKNOWN = "unknown"


@dataclass
class SourceReference:
    source_type: SourceType
    source_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    url: Optional[str] = None
    document_name: Optional[str] = None
    page_number: Optional[int] = None
    table_index: Optional[int] = None
    section: Optional[str] = None
    cell_reference: Optional[str] = None
    publisher: Optional[str] = None
    author: Optional[str] = None
    publication_date: Optional[datetime] = None
    data_period: Optional[str] = None
    collected_at: Optional[datetime] = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    extraction_method: Optional[str] = None
    extraction_confidence: float = 1.0
    raw_text: Optional[str] = None
    confidence: Confidence = Confidence.HIGH

    @property
    def freshness(self) -> FreshnessStatus:
        if self.expires_at is None:
            return FreshnessStatus.UNKNOWN
        now = datetime.now()
        if now < self.expires_at:
            return FreshnessStatus.CURRENT
        days_expired = (now - self.expires_at).days
        if days_expired <= 30:
            return FreshnessStatus.STALE
        return FreshnessStatus.EXPIRED

    def to_citation(self) -> str:
        parts = []
        if self.document_name:
            parts.append(self.document_name)
        if self.publisher:
            parts.append(f"by {self.publisher}")
        if self.publication_date:
            parts.append(f"({self.publication_date.strftime('%Y-%m-%d')})")
        if self.page_number:
            parts.append(f"p.{self.page_number}")
        if self.section:
            parts.append(f"\u00a7{self.section}")
        return " ".join(parts) if parts else f"[{self.source_type.value}]"


@dataclass
class TrackedValue:
    value: Any
    field_name: str
    operator: Optional[str] = None
    period: Optional[str] = None
    primary_source: Optional[SourceReference] = None
    alternative_sources: list[SourceReference] = field(default_factory=list)
    conflict_resolution: Optional[str] = None
    derived_from: list[TrackedValue] = field(default_factory=list)
    derivation_formula: Optional[str] = None
    unit: Optional[str] = None
    last_updated: Optional[datetime] = field(default_factory=datetime.now)

    @property
    def confidence(self) -> Confidence:
        if self.primary_source:
            return self.primary_source.confidence
        return Confidence.ESTIMATED

    @property
    def has_conflict(self) -> bool:
        return len(self.alternative_sources) > 0

    def explain(self) -> str:
        lines = [f"{self.field_name} = {self.value}"]
        if self.unit:
            lines[0] += f" {self.unit}"
        if self.operator:
            lines.append(f"  Operator: {self.operator}")
        if self.period:
            lines.append(f"  Period: {self.period}")
        lines.append(f"  Confidence: {self.confidence.value}")
        if self.primary_source:
            lines.append(f"  Source: {self.primary_source.to_citation()}")
        if self.derivation_formula:
            lines.append(f"  Formula: {self.derivation_formula}")
        return "\n".join(lines)


class ProvenanceStore:
    """Global provenance database for an analysis session."""

    def __init__(self):
        self._sources: dict[str, SourceReference] = {}
        self._values: list[TrackedValue] = []

    def register_source(self, source: SourceReference) -> str:
        self._sources[source.source_id] = source
        return source.source_id

    def register_value(self, tracked_value: TrackedValue) -> None:
        self._values.append(tracked_value)

    def track(self, value: Any, field_name: str, operator: str = None,
              period: str = None, source: SourceReference = None,
              unit: str = None, **kwargs) -> TrackedValue:
        tv = TrackedValue(
            value=value,
            field_name=field_name,
            operator=operator,
            period=period,
            primary_source=source,
            unit=unit,
        )
        self._values.append(tv)
        return tv

    def get_values(self, operator: str = None, field_name: str = None,
                   period: str = None) -> list[TrackedValue]:
        results = self._values
        if operator:
            results = [v for v in results if v.operator == operator]
        if field_name:
            results = [v for v in results if v.field_name == field_name]
        if period:
            results = [v for v in results if v.period == period]
        return results

    def quality_report(self) -> dict:
        total = len(self._values)
        by_confidence = {}
        for v in self._values:
            c = v.confidence.value
            by_confidence[c] = by_confidence.get(c, 0) + 1
        return {
            "total_data_points": total,
            "high_confidence": by_confidence.get("high", 0),
            "medium_confidence": by_confidence.get("medium", 0),
            "low_confidence": by_confidence.get("low", 0),
            "estimated": by_confidence.get("estimated", 0),
            "with_conflicts": sum(1 for v in self._values if v.has_conflict),
            "unique_sources": len(self._sources),
        }

    def to_footnotes(self) -> list[str]:
        seen = set()
        footnotes = []
        for v in self._values:
            if v.primary_source and v.primary_source.source_id not in seen:
                seen.add(v.primary_source.source_id)
                footnotes.append(v.primary_source.to_citation())
        return footnotes

    # ==================================================================
    # Persistence: save to / load from SQLite
    # ==================================================================

    def save_to_db(self, db, analysis_job_id: int = None) -> dict:
        """Persist all sources and tracked values to the database.

        Args:
            db: TelecomDatabase instance with open connection.
            analysis_job_id: Optional job ID to link provenance to.

        Returns:
            {"sources_saved": N, "values_saved": M}
        """
        conn = db.conn

        # 1. Upsert all SourceReference objects to source_registry
        sources_saved = 0
        for src in self._sources.values():
            pub_date = None
            if src.publication_date:
                pub_date = src.publication_date.strftime("%Y-%m-%d")
            collected = None
            if src.collected_at:
                collected = src.collected_at.strftime("%Y-%m-%d %H:%M:%S")

            conn.execute(
                """INSERT OR REPLACE INTO source_registry
                   (source_id, source_type, url, document_name, publisher,
                    publication_date, collected_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    src.source_id,
                    src.source_type.value,
                    src.url,
                    src.document_name,
                    src.publisher,
                    pub_date,
                    collected,
                ),
            )
            sources_saved += 1

        # 1b. Also upsert any sources referenced by values but not in _sources
        for tv in self._values:
            if tv.primary_source and tv.primary_source.source_id not in self._sources:
                src = tv.primary_source
                pub_date = None
                if src.publication_date:
                    pub_date = src.publication_date.strftime("%Y-%m-%d")
                collected = None
                if src.collected_at:
                    collected = src.collected_at.strftime("%Y-%m-%d %H:%M:%S")
                conn.execute(
                    """INSERT OR REPLACE INTO source_registry
                       (source_id, source_type, url, document_name, publisher,
                        publication_date, collected_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        src.source_id,
                        src.source_type.value,
                        src.url,
                        src.document_name,
                        src.publisher,
                        pub_date,
                        collected,
                    ),
                )
                sources_saved += 1

        # 2. Insert TrackedValue objects to data_provenance
        values_saved = 0
        for tv in self._values:
            source_id = tv.primary_source.source_id if tv.primary_source else None
            confidence_val = None
            if tv.primary_source:
                conf_map = {"high": 1.0, "medium": 0.7, "low": 0.4, "estimated": 0.2}
                confidence_val = conf_map.get(tv.primary_source.confidence.value, 0.5)

            extraction_method = None
            if tv.primary_source:
                extraction_method = tv.primary_source.extraction_method

            value_str = str(tv.value) if tv.value is not None else None

            conn.execute(
                """INSERT INTO data_provenance
                   (entity_type, entity_id, field_name, source_id, confidence,
                    extraction_method, raw_text, analysis_job_id, operator_id,
                    period, value_text, unit)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    "tracked_value",
                    0,
                    tv.field_name,
                    source_id,
                    confidence_val,
                    extraction_method,
                    tv.primary_source.raw_text if tv.primary_source else None,
                    analysis_job_id,
                    tv.operator,
                    tv.period,
                    value_str,
                    tv.unit,
                ),
            )
            values_saved += 1

        conn.commit()
        return {"sources_saved": sources_saved, "values_saved": values_saved}

    @classmethod
    def load_from_db(cls, db, analysis_job_id: int) -> "ProvenanceStore":
        """Load a ProvenanceStore from the database for a given job.

        Args:
            db: TelecomDatabase instance with open connection.
            analysis_job_id: The job ID to load provenance for.

        Returns:
            A populated ProvenanceStore instance.
        """
        store = cls()
        conn = db.conn

        # 1. Load data_provenance rows for this job
        rows = conn.execute(
            "SELECT * FROM data_provenance WHERE analysis_job_id = ?",
            (analysis_job_id,),
        ).fetchall()

        # 2. Collect referenced source_ids
        source_ids = set()
        for row in rows:
            sid = row["source_id"] if "source_id" in row.keys() else None
            if sid:
                source_ids.add(sid)

        # 3. Load referenced source_registry rows
        source_map = {}
        for sid in source_ids:
            src_row = conn.execute(
                "SELECT * FROM source_registry WHERE source_id = ?",
                (sid,),
            ).fetchone()
            if src_row:
                try:
                    st = SourceType(src_row["source_type"])
                except (ValueError, KeyError):
                    st = SourceType.MANUAL

                pub_date = None
                if src_row["publication_date"]:
                    try:
                        pub_date = datetime.strptime(
                            src_row["publication_date"], "%Y-%m-%d"
                        )
                    except (ValueError, TypeError):
                        pass

                collected = None
                if src_row["collected_at"]:
                    try:
                        collected = datetime.strptime(
                            src_row["collected_at"], "%Y-%m-%d %H:%M:%S"
                        )
                    except (ValueError, TypeError):
                        pass

                ref = SourceReference(
                    source_type=st,
                    source_id=src_row["source_id"],
                    url=src_row["url"],
                    document_name=src_row["document_name"],
                    publisher=src_row["publisher"],
                    publication_date=pub_date,
                    collected_at=collected,
                )
                source_map[sid] = ref
                store.register_source(ref)

        # 4. Reconstruct TrackedValue objects
        for row in rows:
            sid = row["source_id"] if "source_id" in row.keys() else None
            primary_source = source_map.get(sid) if sid else None

            # Parse confidence back
            if primary_source and row["confidence"] is not None:
                conf_val = row["confidence"]
                if conf_val >= 0.9:
                    primary_source.confidence = Confidence.HIGH
                elif conf_val >= 0.6:
                    primary_source.confidence = Confidence.MEDIUM
                elif conf_val >= 0.3:
                    primary_source.confidence = Confidence.LOW
                else:
                    primary_source.confidence = Confidence.ESTIMATED

            tv = TrackedValue(
                value=row["value_text"],
                field_name=row["field_name"],
                operator=row["operator_id"],
                period=row["period"],
                primary_source=primary_source,
                unit=row["unit"],
            )
            store.register_value(tv)

        return store
