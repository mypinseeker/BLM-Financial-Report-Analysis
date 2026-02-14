"""Tests for cli_extract — batch extraction CLI helpers.

Covers:
- _parse_filename: extracting entity_id and table_type from filenames
- _strip_provenance: removing _-prefixed metadata before DB write
- _ensure_operators: registering LATAM operators in SQLite
- _upsert_rows: dispatching rows to correct db.upsert_*() methods
- Commit end-to-end: write mock JSON, run commit, verify DB contents
"""
import sys
import os
import json
import pytest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.cli_extract import (
    _parse_filename,
    _strip_provenance,
    _ensure_operators,
    _upsert_rows,
    _save_json,
    _do_commit,
    EXTRACTION_DIR,
)
from src.database.db import TelecomDatabase
from src.database.operator_directory import OPERATOR_DIRECTORY, get_non_group_operators


# =====================================================================
# _parse_filename
# =====================================================================

class TestParseFilename:
    def test_tigo_guatemala_financial(self):
        entity, ttype = _parse_filename("tigo_guatemala_financial")
        assert entity == "tigo_guatemala"
        assert ttype == "financial"

    def test_el_salvador_macro(self):
        entity, ttype = _parse_filename("el_salvador_macro")
        assert entity == "el_salvador"
        assert ttype == "macro"

    def test_claro_gt_financial(self):
        entity, ttype = _parse_filename("claro_gt_financial")
        assert entity == "claro_gt"
        assert ttype == "financial"

    def test_tigo_colombia_subscriber(self):
        entity, ttype = _parse_filename("tigo_colombia_subscriber")
        assert entity == "tigo_colombia"
        assert ttype == "subscriber"

    def test_tigo_honduras_network(self):
        entity, ttype = _parse_filename("tigo_honduras_network")
        assert entity == "tigo_honduras"
        assert ttype == "network"

    def test_guatemala_macro(self):
        entity, ttype = _parse_filename("guatemala_macro")
        assert entity == "guatemala"
        assert ttype == "macro"

    def test_tigo_el_salvador_financial(self):
        entity, ttype = _parse_filename("tigo_el_salvador_financial")
        assert entity == "tigo_el_salvador"
        assert ttype == "financial"

    def test_unknown_type_raises(self):
        with pytest.raises(ValueError, match="Cannot parse"):
            _parse_filename("tigo_guatemala_unknown")

    def test_tariff_type(self):
        entity, ttype = _parse_filename("tigo_guatemala_tariff")
        assert entity == "tigo_guatemala"
        assert ttype == "tariff"


# =====================================================================
# _strip_provenance
# =====================================================================

class TestStripProvenance:
    def test_removes_underscore_prefixed(self):
        rows = [
            {
                "operator_id": "tigo_guatemala",
                "total_revenue": 100,
                "_extraction_method": "gemini_pdf",
                "_source_url": "http://example.com",
                "_extracted_at": "2026-02-14T12:00:00Z",
            }
        ]
        clean = _strip_provenance(rows)
        assert len(clean) == 1
        assert "operator_id" in clean[0]
        assert "total_revenue" in clean[0]
        assert "_extraction_method" not in clean[0]
        assert "_source_url" not in clean[0]
        assert "_extracted_at" not in clean[0]

    def test_no_provenance_fields(self):
        rows = [{"operator_id": "x", "value": 1}]
        clean = _strip_provenance(rows)
        assert clean == rows

    def test_empty_list(self):
        assert _strip_provenance([]) == []


# =====================================================================
# _ensure_operators
# =====================================================================

class TestEnsureOperators:
    def test_registers_latam_operators(self):
        db = TelecomDatabase(":memory:")
        db.init()
        count = _ensure_operators(db)
        assert count > 0
        # Check that all LATAM operators are registered
        latam_ops = [
            op_id for op_id, info in OPERATOR_DIRECTORY.items()
            if info.get("region") == "Latin America"
        ]
        assert count == len(latam_ops)
        db.close()

    def test_idempotent(self):
        db = TelecomDatabase(":memory:")
        db.init()
        count1 = _ensure_operators(db)
        count2 = _ensure_operators(db)
        assert count1 == count2
        db.close()


# =====================================================================
# _upsert_rows — financial
# =====================================================================

class TestUpsertRowsFinancial:
    def test_financial_upsert(self):
        db = TelecomDatabase(":memory:")
        db.init()
        db.upsert_operator("tigo_guatemala", country="Guatemala", market="guatemala")

        rows = [
            {
                "operator_id": "tigo_guatemala",
                "period": "Q4 2025",
                "calendar_quarter": "CQ4_2025",
                "period_start": "2025-10-01",
                "period_end": "2025-12-31",
                "total_revenue": 500.0,
                "ebitda": 200.0,
            }
        ]
        count = _upsert_rows(db, "tigo_guatemala", "financial", rows)
        assert count == 1

        # Verify data
        result = db.conn.execute(
            "SELECT total_revenue, ebitda FROM financial_quarterly WHERE operator_id = ?",
            ("tigo_guatemala",),
        ).fetchone()
        assert result is not None
        assert result[0] == 500.0
        assert result[1] == 200.0
        db.close()


# =====================================================================
# _upsert_rows — subscriber
# =====================================================================

class TestUpsertRowsSubscriber:
    def test_subscriber_upsert(self):
        db = TelecomDatabase(":memory:")
        db.init()
        db.upsert_operator("tigo_guatemala", country="Guatemala", market="guatemala")

        rows = [
            {
                "operator_id": "tigo_guatemala",
                "period": "Q4 2025",
                "calendar_quarter": "CQ4_2025",
                "period_start": "2025-10-01",
                "period_end": "2025-12-31",
                "mobile_total_k": 12000,
            }
        ]
        count = _upsert_rows(db, "tigo_guatemala", "subscriber", rows)
        assert count == 1

        result = db.conn.execute(
            "SELECT mobile_total_k FROM subscriber_quarterly WHERE operator_id = ?",
            ("tigo_guatemala",),
        ).fetchone()
        assert result is not None
        assert result[0] == 12000
        db.close()


# =====================================================================
# _upsert_rows — network
# =====================================================================

class TestUpsertRowsNetwork:
    def test_network_upsert(self):
        db = TelecomDatabase(":memory:")
        db.init()
        db.upsert_operator("tigo_guatemala", country="Guatemala", market="guatemala")

        rows = [
            {
                "operator_id": "tigo_guatemala",
                "calendar_quarter": "CQ4_2025",
                "four_g_coverage_pct": 85.0,
                "fiber_homepass_k": 500,
            }
        ]
        count = _upsert_rows(db, "tigo_guatemala", "network", rows)
        assert count == 1

        result = db.conn.execute(
            "SELECT four_g_coverage_pct, fiber_homepass_k FROM network_infrastructure WHERE operator_id = ?",
            ("tigo_guatemala",),
        ).fetchone()
        assert result is not None
        assert result[0] == 85.0
        assert result[1] == 500
        db.close()


# =====================================================================
# _upsert_rows — macro
# =====================================================================

class TestUpsertRowsMacro:
    def test_macro_upsert(self):
        db = TelecomDatabase(":memory:")
        db.init()

        rows = [
            {
                "country": "Guatemala",
                "calendar_quarter": "CQ4_2025",
                "gdp_growth_pct": 3.5,
                "inflation_pct": 4.2,
            }
        ]
        count = _upsert_rows(db, "guatemala", "macro", rows)
        assert count == 1

        result = db.conn.execute(
            "SELECT gdp_growth_pct, inflation_pct FROM macro_environment WHERE country = ?",
            ("Guatemala",),
        ).fetchone()
        assert result is not None
        assert result[0] == 3.5
        assert result[1] == 4.2
        db.close()


# =====================================================================
# _upsert_rows — unknown type
# =====================================================================

class TestUpsertRowsUnknown:
    def test_unknown_type_raises(self):
        db = TelecomDatabase(":memory:")
        db.init()
        with pytest.raises(ValueError, match="Unknown table type"):
            _upsert_rows(db, "x", "bogus", [{"a": 1}])
        db.close()


# =====================================================================
# _save_json
# =====================================================================

class TestSaveJson:
    def test_save_and_load(self, tmp_path):
        path = tmp_path / "test.json"
        data = [{"operator_id": "tigo_gt", "total_revenue": 100}]
        _save_json(path, data, source_url="http://example.com/report.pdf")

        loaded = json.loads(path.read_text())
        assert len(loaded) == 1
        assert loaded[0]["operator_id"] == "tigo_gt"
        assert loaded[0]["_extraction_method"] == "gemini_pdf"
        assert loaded[0]["_source_url"] == "http://example.com/report.pdf"
        assert "_extracted_at" in loaded[0]

    def test_save_search_mode(self, tmp_path):
        path = tmp_path / "test.json"
        data = [{"country": "Guatemala", "gdp_growth_pct": 3.5}]
        _save_json(path, data, source_url="")

        loaded = json.loads(path.read_text())
        assert loaded[0]["_extraction_method"] == "gemini_search"


# =====================================================================
# Commit end-to-end
# =====================================================================

class TestCommitEndToEnd:
    def test_commit_financial_from_json(self, tmp_path, monkeypatch):
        """Write mock JSON to tmp dir, run commit, verify DB contents."""
        # Create mock extraction JSON
        extraction_dir = tmp_path / "extraction"
        extraction_dir.mkdir()

        rows = [
            {
                "operator_id": "tigo_guatemala",
                "period": "Q4 2025",
                "calendar_quarter": "CQ4_2025",
                "period_start": "2025-10-01",
                "period_end": "2025-12-31",
                "total_revenue": 500.0,
                "_extraction_method": "gemini_pdf",
                "_source_url": "http://example.com/report.pdf",
                "_extracted_at": "2026-02-14T12:00:00Z",
            }
        ]
        (extraction_dir / "tigo_guatemala_financial.json").write_text(
            json.dumps(rows, indent=2)
        )

        # Monkey-patch EXTRACTION_DIR
        import src.cli_extract as cli_mod
        monkeypatch.setattr(cli_mod, "EXTRACTION_DIR", extraction_dir)

        # Use in-memory DB — need to monkeypatch _get_db
        db = TelecomDatabase(":memory:")
        db.init()
        # Prevent _do_commit from closing the connection so we can verify
        real_close = db.close
        monkeypatch.setattr(db, "close", lambda: None)
        monkeypatch.setattr(cli_mod, "_get_db", lambda db_path="": db)

        _do_commit(operator="tigo_guatemala", all_ops=False, db_path=":memory:")

        # Verify data is in DB
        result = db.conn.execute(
            "SELECT total_revenue FROM financial_quarterly WHERE operator_id = ?",
            ("tigo_guatemala",),
        ).fetchone()
        assert result is not None
        assert result[0] == 500.0

        # Verify provenance metadata was stripped
        cols = [d[0] for d in db.conn.execute(
            "SELECT * FROM financial_quarterly LIMIT 1"
        ).description]
        assert "_extraction_method" not in cols

        real_close()

    def test_commit_all(self, tmp_path, monkeypatch):
        """Commit multiple files with --all."""
        extraction_dir = tmp_path / "extraction"
        extraction_dir.mkdir()

        # Financial
        fin_rows = [
            {
                "operator_id": "tigo_honduras",
                "period": "Q4 2025",
                "calendar_quarter": "CQ4_2025",
                "period_start": "2025-10-01",
                "period_end": "2025-12-31",
                "total_revenue": 300.0,
                "_extraction_method": "gemini_pdf",
                "_source_url": "",
                "_extracted_at": "2026-02-14T12:00:00Z",
            }
        ]
        (extraction_dir / "tigo_honduras_financial.json").write_text(
            json.dumps(fin_rows, indent=2)
        )

        # Macro
        macro_rows = [
            {
                "country": "Honduras",
                "calendar_quarter": "CQ4_2025",
                "gdp_growth_pct": 3.0,
                "_extraction_method": "gemini_search",
                "_source_url": "",
                "_extracted_at": "2026-02-14T12:00:00Z",
            }
        ]
        (extraction_dir / "honduras_macro.json").write_text(
            json.dumps(macro_rows, indent=2)
        )

        import src.cli_extract as cli_mod
        monkeypatch.setattr(cli_mod, "EXTRACTION_DIR", extraction_dir)

        db = TelecomDatabase(":memory:")
        db.init()
        real_close = db.close
        monkeypatch.setattr(db, "close", lambda: None)
        monkeypatch.setattr(cli_mod, "_get_db", lambda db_path="": db)

        _do_commit(operator=None, all_ops=True, db_path=":memory:")

        # Verify financial
        fin = db.conn.execute(
            "SELECT total_revenue FROM financial_quarterly WHERE operator_id = ?",
            ("tigo_honduras",),
        ).fetchone()
        assert fin is not None
        assert fin[0] == 300.0

        # Verify macro
        macro = db.conn.execute(
            "SELECT gdp_growth_pct FROM macro_environment WHERE country = ?",
            ("Honduras",),
        ).fetchone()
        assert macro is not None
        assert macro[0] == 3.0

        real_close()


# =====================================================================
# get_non_group_operators
# =====================================================================

class TestGetNonGroupOperators:
    def test_guatemala_non_millicom(self):
        result = get_non_group_operators("guatemala", "millicom")
        assert "tigo_guatemala" not in result
        assert "claro_gt" in result
        assert "movistar_gt" in result

    def test_colombia_non_millicom(self):
        result = get_non_group_operators("colombia", "millicom")
        assert "tigo_colombia" not in result
        assert "claro_co" in result

    def test_empty_market(self):
        result = get_non_group_operators("nonexistent", "millicom")
        assert result == []


# =====================================================================
# Prompt country parameter
# =====================================================================

class TestPromptCountryParam:
    def test_financial_prompt_with_country(self):
        from src.extraction.prompts import get_financial_prompt
        sys_inst, prompt = get_financial_prompt(
            "tigo_guatemala", "Tigo Guatemala", "GTQ", "CQ4_2025",
            country="Guatemala",
        )
        assert "CONSOLIDATED" in prompt
        assert "Guatemala" in prompt
        assert "Tigo Guatemala" in prompt

    def test_financial_prompt_without_country(self):
        from src.extraction.prompts import get_financial_prompt
        sys_inst, prompt = get_financial_prompt(
            "tigo_guatemala", "Tigo Guatemala", "GTQ", "CQ4_2025",
        )
        assert "CONSOLIDATED" not in prompt

    def test_subscriber_prompt_with_country(self):
        from src.extraction.prompts import get_subscriber_prompt
        _, prompt = get_subscriber_prompt(
            "tigo_guatemala", "Tigo Guatemala", "CQ4_2025",
            country="Guatemala",
        )
        assert "CONSOLIDATED" in prompt

    def test_network_prompt_with_country(self):
        from src.extraction.prompts import get_network_prompt
        _, prompt = get_network_prompt(
            "tigo_guatemala", "Tigo Guatemala", "CQ4_2025",
            country="Guatemala",
        )
        assert "CONSOLIDATED" in prompt
