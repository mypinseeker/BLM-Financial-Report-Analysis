"""ExtractionService — orchestration layer for AI data extraction pipeline.

Coordinates: Gemini discovery → PDF download → table extraction → validation.
Each method is a standalone step callable from a single API endpoint.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import Any

import httpx

from src.database.operator_directory import OPERATOR_DIRECTORY
from src.extraction.prompts import (
    get_discovery_prompt,
    get_financial_prompt,
    get_subscriber_prompt,
    get_tariff_prompt,
    get_macro_prompt,
    get_network_prompt,
)
from src.web.services.gemini_service import GeminiService, get_gemini_service

logger = logging.getLogger(__name__)

# Valid calendar quarter pattern
CQ_PATTERN = re.compile(r"^CQ[1-4]_\d{4}$")

# Table types and their required fields
TABLE_REQUIRED_FIELDS: dict[str, list[str]] = {
    "financial": ["operator_id", "calendar_quarter", "period_start", "period_end"],
    "subscriber": ["operator_id", "calendar_quarter", "period_start", "period_end"],
    "tariff": ["operator_id", "plan_name", "plan_type"],
    "macro": ["country", "calendar_quarter"],
    "network": ["operator_id", "calendar_quarter"],
}


class ExtractionService:
    """Orchestrates the multi-step extraction pipeline."""

    def __init__(self, gemini: GeminiService | None = None):
        self.gemini = gemini or get_gemini_service()

    # ------------------------------------------------------------------
    # Step 1: Discover report
    # ------------------------------------------------------------------

    async def discover_report(self, operator_id: str) -> dict:
        """Use Gemini + Google Search to find the latest earnings report PDF.

        Returns: {pdf_url, report_title, report_period, ir_page_url, confidence}
        """
        op_info = OPERATOR_DIRECTORY.get(operator_id)
        if not op_info:
            raise ValueError(f"Unknown operator: {operator_id}")

        operator_name = op_info["display_name"]
        ir_url = op_info.get("ir_url", "")
        parent = op_info.get("parent_company", "")

        # Build a richer name for search
        search_name = operator_name
        if parent:
            search_name = f"{operator_name} ({parent})"

        system_inst, prompt = get_discovery_prompt(search_name, ir_url)
        result = await self.gemini.generate_with_search(prompt, system_inst)

        # Normalize result
        result.setdefault("pdf_url", "")
        result.setdefault("report_title", "")
        result.setdefault("report_period", "")
        result.setdefault("confidence", 0.5)

        return result

    # ------------------------------------------------------------------
    # Step 2: Download PDF and upload to Gemini
    # ------------------------------------------------------------------

    async def download_and_upload(
        self, pdf_url: str, display_name: str = "earnings_report"
    ) -> str:
        """Download a PDF from URL and upload to Gemini Files API.

        Returns: file_uri for use in subsequent extraction calls.
        """
        async with httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; BLMAnalysis/1.0)"
            },
        ) as client:
            resp = await client.get(pdf_url)

        if resp.status_code != 200:
            raise RuntimeError(
                f"Failed to download PDF ({resp.status_code}): {pdf_url}"
            )

        content_type = resp.headers.get("content-type", "")
        file_bytes = resp.content

        # Validate this is actually a PDF (check magic bytes and content-type)
        is_pdf = (
            file_bytes[:5] == b"%PDF-"
            or "pdf" in content_type.lower()
            or pdf_url.lower().endswith(".pdf")
        )
        if not is_pdf:
            raise RuntimeError(
                f"Downloaded file is not a PDF (content-type: {content_type}). "
                f"The URL may be an HTML page, not a direct PDF link: {pdf_url}"
            )

        size_mb = len(file_bytes) / (1024 * 1024)
        logger.info("Downloaded %.1f MB from %s", size_mb, pdf_url)

        if size_mb > 20:
            raise RuntimeError(f"PDF too large ({size_mb:.1f} MB). Max 20 MB.")

        file_uri = await self.gemini.upload_file(
            file_bytes, mime_type="application/pdf", display_name=display_name
        )
        return file_uri

    # ------------------------------------------------------------------
    # Step 3: Extract a specific table from the uploaded PDF
    # ------------------------------------------------------------------

    async def extract_table(
        self,
        file_uri: str,
        table_type: str,
        operator_id: str,
        target_quarter: str = "CQ4_2025",
        n_quarters: int = 4,
    ) -> list[dict]:
        """Extract data for one table type from the uploaded PDF.

        table_type: "financial" | "subscriber" | "tariff" | "macro" | "network"
        Returns: list of validated row dicts.
        """
        op_info = OPERATOR_DIRECTORY.get(operator_id, {})
        operator_name = op_info.get("display_name", operator_id)
        currency = op_info.get("currency", "USD")
        country = op_info.get("country", "")

        # Build the appropriate prompt
        if table_type == "financial":
            sys_inst, prompt = get_financial_prompt(
                operator_id, operator_name, currency, target_quarter, n_quarters
            )
        elif table_type == "subscriber":
            sys_inst, prompt = get_subscriber_prompt(
                operator_id, operator_name, target_quarter, n_quarters
            )
        elif table_type == "tariff":
            sys_inst, prompt = get_tariff_prompt(
                operator_id, operator_name, currency
            )
        elif table_type == "macro":
            sys_inst, prompt = get_macro_prompt(
                country, target_quarter, n_quarters
            )
        elif table_type == "network":
            sys_inst, prompt = get_network_prompt(
                operator_id, operator_name, target_quarter, n_quarters
            )
        else:
            raise ValueError(f"Unknown table type: {table_type}")

        # Build search-mode prompt enhancement (used by search fallback)
        parent = op_info.get("parent_company", "")
        search_hint = (
            f"\n\nIMPORTANT: Search the web for {operator_name}"
            f"{' (' + parent + ')' if parent else ''} quarterly financial results. "
            f"Look for earnings releases, investor presentations, and press releases "
            f"from the company's official website. Extract actual numbers reported "
            f"in the earnings results. Use Google Search to find the data."
        )

        # Call Gemini: use uploaded file if available, else fall back to search
        if file_uri and file_uri != "search":
            try:
                result = await self.gemini.generate_with_file(file_uri, prompt, sys_inst)
            except Exception as e:
                # Auto-fallback to search when file extraction fails
                # (e.g. "The document has no pages" from Gemini)
                logger.warning(
                    "File extraction failed for %s/%s: %s. Falling back to search.",
                    operator_id, table_type, e,
                )
                result = await self.gemini.generate_with_search(
                    prompt + search_hint, sys_inst
                )
        else:
            result = await self.gemini.generate_with_search(
                prompt + search_hint, sys_inst
            )

        # Normalize: result might be a dict with a "data" key or a list directly
        rows = self._normalize_rows(result)

        # Enrich: auto-fill missing fields derivable from other fields
        rows = self._enrich_rows(rows, table_type, operator_id, country)

        # Validate
        valid_rows, errors = self.validate_rows(table_type, rows)
        if errors:
            logger.warning(
                "Validation errors for %s/%s: %s",
                operator_id, table_type, errors[:5],
            )

        return valid_rows

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate_rows(
        self, table_type: str, rows: list[dict]
    ) -> tuple[list[dict], list[str]]:
        """Validate extracted rows. Returns (valid_rows, error_messages)."""
        required = TABLE_REQUIRED_FIELDS.get(table_type, [])
        valid = []
        errors = []

        for i, row in enumerate(rows):
            row_errors = []

            # Check required fields
            for field in required:
                if not row.get(field):
                    row_errors.append(f"Row {i}: missing required field '{field}'")

            # Validate calendar_quarter format
            cq = row.get("calendar_quarter", "")
            if cq and not CQ_PATTERN.match(cq):
                row_errors.append(
                    f"Row {i}: invalid calendar_quarter '{cq}' (expected CQn_YYYY)"
                )

            # Validate date fields
            for date_field in ("period_start", "period_end", "report_date", "effective_date"):
                val = row.get(date_field)
                if val and isinstance(val, str):
                    try:
                        datetime.strptime(val, "%Y-%m-%d")
                    except ValueError:
                        row_errors.append(
                            f"Row {i}: invalid date '{val}' for {date_field}"
                        )

            # Validate confidence
            conf = row.get("confidence")
            if conf is not None:
                try:
                    conf_val = float(conf)
                    if not (0.0 <= conf_val <= 1.0):
                        row_errors.append(f"Row {i}: confidence {conf_val} out of range")
                except (TypeError, ValueError):
                    row_errors.append(f"Row {i}: invalid confidence '{conf}'")

            if row_errors:
                errors.extend(row_errors)
            else:
                valid.append(row)

        return valid, errors

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    # Calendar quarter → (period_start, period_end) mapping
    _CQ_DATES = {
        "1": ("01-01", "03-31"),
        "2": ("04-01", "06-30"),
        "3": ("07-01", "09-30"),
        "4": ("10-01", "12-31"),
    }

    @classmethod
    def _enrich_rows(
        cls, rows: list[dict], table_type: str, operator_id: str, country: str
    ) -> list[dict]:
        """Auto-fill missing fields that can be derived from other fields.

        - period_start / period_end from calendar_quarter
        - operator_id if missing
        - country for macro rows
        """
        for row in rows:
            # Inject operator_id if missing (financial, subscriber, tariff, network)
            if table_type != "macro" and not row.get("operator_id"):
                row["operator_id"] = operator_id

            # Inject country for macro rows
            if table_type == "macro" and not row.get("country") and country:
                row["country"] = country

            # Derive period_start / period_end from calendar_quarter
            cq = row.get("calendar_quarter", "")
            match = CQ_PATTERN.match(cq) if cq else None
            if match:
                q_num = cq[2]  # "CQ4_2025" → "4"
                year = cq[4:]  # "CQ4_2025" → "2025"
                dates = cls._CQ_DATES.get(q_num)
                if dates:
                    if not row.get("period_start"):
                        row["period_start"] = f"{year}-{dates[0]}"
                    if not row.get("period_end"):
                        row["period_end"] = f"{year}-{dates[1]}"

        return rows

    @staticmethod
    def _normalize_rows(result: Any) -> list[dict]:
        """Normalize Gemini's response into a list of dicts."""
        if isinstance(result, list):
            return result
        if isinstance(result, dict):
            # Try common wrapper keys
            for key in ("data", "rows", "records", "results"):
                if key in result and isinstance(result[key], list):
                    return result[key]
            # Single record → wrap in list
            return [result]
        return []
