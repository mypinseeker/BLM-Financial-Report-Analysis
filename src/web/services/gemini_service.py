"""GeminiService — httpx REST wrapper for Gemini API.

Uses direct REST calls (no SDK) to stay under Vercel's 15MB Lambda limit.
Supports: text generation, Google Search Grounding, file upload, file-based extraction.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)

GEMINI_MODEL = "gemini-2.0-flash"
BASE_URL = "https://generativelanguage.googleapis.com"
GENERATE_URL = f"{BASE_URL}/v1beta/models/{GEMINI_MODEL}:generateContent"
UPLOAD_URL = f"{BASE_URL}/upload/v1beta/files"


class GeminiError(Exception):
    """Raised when a Gemini API call fails."""


class GeminiService:
    """Thin httpx wrapper around Gemini REST API."""

    def __init__(self, api_key: str | None = None, timeout: float = 55.0):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        if not self.api_key:
            raise GeminiError("GEMINI_API_KEY not set")
        self.timeout = timeout

    # ------------------------------------------------------------------
    # Core: generate content
    # ------------------------------------------------------------------

    async def generate_content(
        self,
        prompt: str,
        system_instruction: str = "",
        response_mime_type: str = "application/json",
    ) -> dict:
        """Send a text prompt and return parsed JSON response."""
        body: dict[str, Any] = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": response_mime_type,
                "temperature": 0.1,
            },
        }
        if system_instruction:
            body["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }
        return await self._call_generate(body)

    # ------------------------------------------------------------------
    # Google Search Grounding
    # ------------------------------------------------------------------

    async def generate_with_search(
        self,
        prompt: str,
        system_instruction: str = "",
    ) -> dict:
        """Generate with Google Search Grounding tool enabled.

        Returns raw text (not JSON) since search-grounded responses
        are often free-form. We parse the JSON ourselves.
        """
        body: dict[str, Any] = {
            "contents": [{"parts": [{"text": prompt}]}],
            "tools": [{"google_search": {}}],
            "generationConfig": {
                "temperature": 0.1,
            },
        }
        if system_instruction:
            body["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }
        return await self._call_generate(body, parse_json=True)

    # ------------------------------------------------------------------
    # File upload (for PDF processing)
    # ------------------------------------------------------------------

    async def upload_file(
        self,
        file_bytes: bytes,
        mime_type: str = "application/pdf",
        display_name: str = "uploaded_file",
    ) -> str:
        """Upload a file to Gemini Files API. Returns the file URI."""
        url = f"{UPLOAD_URL}?key={self.api_key}"

        # Gemini Files API uses multipart upload with metadata + file
        headers = {
            "X-Goog-Upload-Protocol": "multipart",
        }

        # Build multipart manually
        import io
        boundary = "---gemini-upload-boundary---"
        body = io.BytesIO()

        # Part 1: metadata JSON
        body.write(f"--{boundary}\r\n".encode())
        body.write(b"Content-Type: application/json; charset=UTF-8\r\n\r\n")
        metadata = {"file": {"displayName": display_name}}
        body.write(json.dumps(metadata).encode())
        body.write(b"\r\n")

        # Part 2: file content
        body.write(f"--{boundary}\r\n".encode())
        body.write(f"Content-Type: {mime_type}\r\n\r\n".encode())
        body.write(file_bytes)
        body.write(b"\r\n")
        body.write(f"--{boundary}--\r\n".encode())

        content_type = f"multipart/related; boundary={boundary}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                url,
                content=body.getvalue(),
                headers={**headers, "Content-Type": content_type},
            )

        if resp.status_code not in (200, 201):
            raise GeminiError(
                f"File upload failed ({resp.status_code}): {resp.text[:500]}"
            )

        data = resp.json()
        file_uri = data.get("file", {}).get("uri", "")
        if not file_uri:
            raise GeminiError(f"No file URI in response: {data}")

        logger.info("Uploaded file: %s -> %s", display_name, file_uri)
        return file_uri

    # ------------------------------------------------------------------
    # Generate with uploaded file
    # ------------------------------------------------------------------

    async def generate_with_file(
        self,
        file_uri: str,
        prompt: str,
        system_instruction: str = "",
    ) -> dict:
        """Generate content using an uploaded file (e.g., PDF) as context."""
        body: dict[str, Any] = {
            "contents": [
                {
                    "parts": [
                        {"fileData": {"mimeType": "application/pdf", "fileUri": file_uri}},
                        {"text": prompt},
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.1,
            },
        }
        if system_instruction:
            body["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }
        return await self._call_generate(body)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    async def _call_generate(
        self, body: dict, *, parse_json: bool = False
    ) -> dict:
        """Make the actual generateContent POST request."""
        url = f"{GENERATE_URL}?key={self.api_key}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, json=body)

        if resp.status_code != 200:
            raise GeminiError(
                f"Gemini API error ({resp.status_code}): {resp.text[:500]}"
            )

        data = resp.json()

        # Extract text from response
        candidates = data.get("candidates", [])
        if not candidates:
            raise GeminiError(f"No candidates in Gemini response: {data}")

        parts = candidates[0].get("content", {}).get("parts", [])
        if not parts:
            raise GeminiError("Empty parts in Gemini response")

        text = parts[0].get("text", "")

        # If responseMimeType was application/json, Gemini returns parsed JSON directly
        # If parse_json is True, we try to parse the text ourselves
        if parse_json:
            return self._extract_json(text)

        # For JSON responses, try to parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            return self._extract_json(text)

    @staticmethod
    def _extract_json(text: str) -> dict:
        """Try to extract JSON from text that may contain markdown."""
        # Try direct parse first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try extracting from ```json ... ```
        import re
        match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        # Try finding first { ... } or [ ... ]
        for start_char, end_char in [("{", "}"), ("[", "]")]:
            start = text.find(start_char)
            end = text.rfind(end_char)
            if start != -1 and end > start:
                try:
                    return json.loads(text[start : end + 1])
                except json.JSONDecodeError:
                    pass

        raise GeminiError(f"Could not parse JSON from Gemini response: {text[:300]}")


# ------------------------------------------------------------------
# Singleton
# ------------------------------------------------------------------

_gemini: GeminiService | None = None


def get_gemini_service() -> GeminiService:
    """Return a cached GeminiService instance."""
    global _gemini
    if _gemini is None:
        _gemini = GeminiService()
    return _gemini
