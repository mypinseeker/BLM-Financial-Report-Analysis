"""Tests for ProvenanceStore database persistence (save_to_db / load_from_db)."""

import pytest
from datetime import datetime

from src.database.db import TelecomDatabase
from src.models.provenance import (
    ProvenanceStore,
    SourceReference,
    SourceType,
    Confidence,
    TrackedValue,
)


@pytest.fixture
def db():
    """Fresh in-memory SQLite DB with schema."""
    database = TelecomDatabase(":memory:")
    database.init()
    yield database
    database.close()


def _make_source(source_id="src1", doc_name="Q4 2025 Report",
                 publisher="Millicom IR", source_type=SourceType.FINANCIAL_REPORT_PDF,
                 confidence=Confidence.HIGH):
    return SourceReference(
        source_type=source_type,
        source_id=source_id,
        url="https://example.com/report.pdf",
        document_name=doc_name,
        publisher=publisher,
        publication_date=datetime(2025, 12, 15),
        collected_at=datetime(2025, 12, 20, 10, 30, 0),
        extraction_method="manual",
        confidence=confidence,
    )


# ==================================================================
# Test: save empty store
# ==================================================================

def test_save_empty_store(db):
    """Saving an empty ProvenanceStore writes 0 rows."""
    store = ProvenanceStore()
    result = store.save_to_db(db)
    assert result == {"sources_saved": 0, "values_saved": 0}

    count = db.conn.execute("SELECT COUNT(*) FROM source_registry").fetchone()[0]
    assert count == 0
    count = db.conn.execute("SELECT COUNT(*) FROM data_provenance").fetchone()[0]
    assert count == 0


# ==================================================================
# Test: save sources
# ==================================================================

def test_save_sources(db):
    """Saving a store with registered sources populates source_registry."""
    store = ProvenanceStore()
    src1 = _make_source("src1", "Report A", "Publisher A")
    src2 = _make_source("src2", "Report B", "Publisher B",
                        source_type=SourceType.EARNINGS_CALL_TRANSCRIPT)
    store.register_source(src1)
    store.register_source(src2)

    result = store.save_to_db(db)
    assert result["sources_saved"] == 2
    assert result["values_saved"] == 0

    rows = db.conn.execute("SELECT * FROM source_registry ORDER BY source_id").fetchall()
    assert len(rows) == 2
    assert rows[0]["source_id"] == "src1"
    assert rows[0]["document_name"] == "Report A"
    assert rows[0]["source_type"] == "financial_report_pdf"
    assert rows[1]["source_id"] == "src2"
    assert rows[1]["source_type"] == "earnings_call_transcript"


# ==================================================================
# Test: save tracked values
# ==================================================================

def test_save_tracked_values(db):
    """Saving tracked values populates data_provenance with analysis_job_id."""
    store = ProvenanceStore()
    src = _make_source("src1")
    store.register_source(src)

    store.track(value=4350.0, field_name="total_revenue",
                operator="tigo_guatemala", period="CQ4_2025",
                source=src, unit="GTQ millions")
    store.track(value=8500, field_name="mobile_total_k",
                operator="tigo_guatemala", period="CQ4_2025",
                source=src, unit="thousands")

    result = store.save_to_db(db, analysis_job_id=42)
    assert result["sources_saved"] == 1
    assert result["values_saved"] == 2

    rows = db.conn.execute(
        "SELECT * FROM data_provenance WHERE analysis_job_id = 42"
    ).fetchall()
    assert len(rows) == 2

    row1 = rows[0]
    assert row1["field_name"] == "total_revenue"
    assert row1["operator_id"] == "tigo_guatemala"
    assert row1["period"] == "CQ4_2025"
    assert row1["value_text"] == "4350.0"
    assert row1["unit"] == "GTQ millions"
    assert row1["source_id"] == "src1"
    assert row1["analysis_job_id"] == 42
    assert row1["confidence"] == 1.0  # HIGH


# ==================================================================
# Test: save values without source
# ==================================================================

def test_save_value_without_source(db):
    """Tracked values without a source save with NULL source_id."""
    store = ProvenanceStore()
    store.track(value="estimated", field_name="market_position",
                operator="tigo_honduras")

    result = store.save_to_db(db, analysis_job_id=1)
    assert result["values_saved"] == 1

    row = db.conn.execute("SELECT * FROM data_provenance").fetchone()
    assert row["source_id"] is None
    assert row["confidence"] is None
    assert row["value_text"] == "estimated"


# ==================================================================
# Test: roundtrip save → load
# ==================================================================

def test_roundtrip(db):
    """Save then load: counts and field_names match."""
    store = ProvenanceStore()
    src1 = _make_source("src1", "Annual Report", "Millicom")
    src2 = _make_source("src2", "Regulatory Filing", "SIT Guatemala",
                        source_type=SourceType.REGULATORY_REPORT,
                        confidence=Confidence.MEDIUM)
    store.register_source(src1)
    store.register_source(src2)

    store.track(value=4350, field_name="total_revenue",
                operator="tigo_guatemala", period="CQ4_2025",
                source=src1, unit="GTQ millions")
    store.track(value=50.2, field_name="mobile_market_share_pct",
                operator="tigo_guatemala", period="CQ4_2025",
                source=src2, unit="%")
    store.track(value="positive", field_name="regulatory_outlook",
                operator="tigo_guatemala", source=src2)

    store.save_to_db(db, analysis_job_id=10)

    # Load back
    loaded = ProvenanceStore.load_from_db(db, analysis_job_id=10)

    # Verify counts
    assert len(loaded._sources) == 2
    assert len(loaded._values) == 3

    # Verify field names
    field_names = [v.field_name for v in loaded._values]
    assert "total_revenue" in field_names
    assert "mobile_market_share_pct" in field_names
    assert "regulatory_outlook" in field_names

    # Verify source linkage
    rev_val = [v for v in loaded._values if v.field_name == "total_revenue"][0]
    assert rev_val.primary_source is not None
    assert rev_val.primary_source.source_id == "src1"
    assert rev_val.primary_source.document_name == "Annual Report"
    assert rev_val.operator == "tigo_guatemala"
    assert rev_val.period == "CQ4_2025"
    assert rev_val.unit == "GTQ millions"


# ==================================================================
# Test: quality_report after roundtrip
# ==================================================================

def test_quality_report_after_roundtrip(db):
    """quality_report() on loaded store matches original store."""
    store = ProvenanceStore()
    src_high = _make_source("s1", confidence=Confidence.HIGH)
    src_med = _make_source("s2", confidence=Confidence.MEDIUM)
    store.register_source(src_high)
    store.register_source(src_med)

    store.track(value=100, field_name="f1", source=src_high)
    store.track(value=200, field_name="f2", source=src_high)
    store.track(value=300, field_name="f3", source=src_med)
    store.track(value=400, field_name="f4")  # no source → estimated

    original_report = store.quality_report()

    store.save_to_db(db, analysis_job_id=99)
    loaded = ProvenanceStore.load_from_db(db, analysis_job_id=99)
    loaded_report = loaded.quality_report()

    # Total data points must match
    assert loaded_report["total_data_points"] == original_report["total_data_points"]
    # Unique sources: loaded gets only sources referenced by values (2)
    assert loaded_report["unique_sources"] == 2
    # Confidence breakdown should match
    assert loaded_report["high_confidence"] == original_report["high_confidence"]
    assert loaded_report["medium_confidence"] == original_report["medium_confidence"]
    assert loaded_report["estimated"] == original_report["estimated"]


# ==================================================================
# Test: load by job_id isolation
# ==================================================================

def test_load_by_job_id(db):
    """Two jobs saved, loading one returns only its data."""
    # Job 1
    store1 = ProvenanceStore()
    src1 = _make_source("s1a")
    store1.register_source(src1)
    store1.track(value=100, field_name="revenue_job1", source=src1)
    store1.track(value=200, field_name="subs_job1", source=src1)
    store1.save_to_db(db, analysis_job_id=1)

    # Job 2
    store2 = ProvenanceStore()
    src2 = _make_source("s2a", doc_name="Different Report")
    store2.register_source(src2)
    store2.track(value=999, field_name="revenue_job2", source=src2)
    store2.save_to_db(db, analysis_job_id=2)

    # Load job 1
    loaded1 = ProvenanceStore.load_from_db(db, analysis_job_id=1)
    assert len(loaded1._values) == 2
    assert all(v.field_name.endswith("_job1") for v in loaded1._values)

    # Load job 2
    loaded2 = ProvenanceStore.load_from_db(db, analysis_job_id=2)
    assert len(loaded2._values) == 1
    assert loaded2._values[0].field_name == "revenue_job2"


# ==================================================================
# Test: load nonexistent job returns empty store
# ==================================================================

def test_load_nonexistent_job(db):
    """Loading a job that doesn't exist returns an empty store."""
    loaded = ProvenanceStore.load_from_db(db, analysis_job_id=999)
    assert len(loaded._sources) == 0
    assert len(loaded._values) == 0
    assert loaded.quality_report()["total_data_points"] == 0


# ==================================================================
# Test: save idempotent sources
# ==================================================================

def test_save_idempotent_sources(db):
    """Saving the same source twice doesn't duplicate rows."""
    store = ProvenanceStore()
    src = _make_source("src1")
    store.register_source(src)
    store.track(value=100, field_name="f1", source=src)

    store.save_to_db(db, analysis_job_id=1)
    store.save_to_db(db, analysis_job_id=2)  # save again with different job

    sources = db.conn.execute("SELECT COUNT(*) FROM source_registry").fetchone()[0]
    assert sources == 1  # source is upserted, not duplicated

    values = db.conn.execute("SELECT COUNT(*) FROM data_provenance").fetchone()[0]
    assert values == 2  # one per job save


# ==================================================================
# Test: engine provenance integration
# ==================================================================

def test_engine_provenance_saves(db):
    """Running the engine on a seeded DB produces provenance data that can be saved."""
    # Seed a market
    from src.database.seed_orchestrator import _seed_germany_into, _apply_v3_schema
    _apply_v3_schema(db)
    _seed_germany_into(db)

    # Run engine
    from src.blm.engine import BLMAnalysisEngine
    engine = BLMAnalysisEngine(
        db=db,
        target_operator="vodafone_germany",
        market="germany",
        target_period="CQ4_2025",
    )
    result = engine.run_five_looks()

    # Save provenance
    stats = result.provenance.save_to_db(db, analysis_job_id=1)
    assert stats["sources_saved"] >= 0
    assert stats["values_saved"] >= 0

    # Load back and verify
    loaded = ProvenanceStore.load_from_db(db, analysis_job_id=1)
    assert loaded.quality_report()["total_data_points"] == stats["values_saved"]
