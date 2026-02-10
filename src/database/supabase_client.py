"""BLMSupabaseClient — Supabase connection and utility layer for BLM project.

Reads credentials from src/database/.env (SUPABASE_URL, SUPABASE_SERVICE_KEY).
Provides upsert, select, file upload/download helpers.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client, Client


# Load .env from src/database/.env
_ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(_ENV_PATH)


class BLMSupabaseClient:
    """Supabase client wrapper for BLM cloud persistence."""

    def __init__(self, url: str = None, key: str = None):
        self.url = url or os.getenv("SUPABASE_URL")
        self.key = key or os.getenv("SUPABASE_SERVICE_KEY")
        if not self.url or not self.key:
            raise ValueError(
                "Missing SUPABASE_URL or SUPABASE_SERVICE_KEY. "
                f"Set them in {_ENV_PATH} or pass as arguments."
            )
        self.client: Client = create_client(self.url, self.key)

    def upsert(self, table: str, data: list[dict], on_conflict: str) -> int:
        """Upsert rows into a table.

        Args:
            table: Table name
            data: List of row dicts
            on_conflict: Comma-separated conflict column names

        Returns:
            Number of rows upserted
        """
        if not data:
            return 0
        resp = (
            self.client.table(table)
            .upsert(data, on_conflict=on_conflict)
            .execute()
        )
        return len(resp.data) if resp.data else 0

    def select(self, table: str, filters: dict = None, limit: int = 10000) -> list[dict]:
        """Select rows from a table with optional equality filters.

        Args:
            table: Table name
            filters: Dict of column=value equality filters
            limit: Max rows to return

        Returns:
            List of row dicts
        """
        query = self.client.table(table).select("*").limit(limit)
        if filters:
            for col, val in filters.items():
                query = query.eq(col, val)
        resp = query.execute()
        return resp.data or []

    def count(self, table: str, filters: dict = None) -> int:
        """Count rows in a table with optional filters."""
        query = self.client.table(table).select("*", count="exact")
        if filters:
            for col, val in filters.items():
                query = query.eq(col, val)
        resp = query.execute()
        return resp.count if resp.count is not None else len(resp.data or [])

    def upload_file(self, bucket: str, path: str, file_bytes: bytes,
                    content_type: str = "application/octet-stream") -> str:
        """Upload a file to Supabase Storage.

        Args:
            bucket: Storage bucket name
            path: File path within bucket
            file_bytes: File content bytes
            content_type: MIME type

        Returns:
            The storage path
        """
        self.client.storage.from_(bucket).upload(
            path, file_bytes,
            file_options={"content-type": content_type, "upsert": "true"}
        )
        return path

    def download_file(self, bucket: str, path: str) -> bytes:
        """Download a file from Supabase Storage.

        Returns:
            File content as bytes
        """
        return self.client.storage.from_(bucket).download(path)

    def ensure_bucket(self, bucket: str, public: bool = False):
        """Create a storage bucket if it doesn't exist."""
        try:
            self.client.storage.get_bucket(bucket)
        except Exception:
            self.client.storage.create_bucket(
                bucket, options={"public": public}
            )

    def execute_sql(self, sql: str) -> dict:
        """Execute raw SQL via Supabase RPC (requires pg_net or supabase SQL editor).

        For schema init, we use the REST API approach instead.
        """
        return self.client.rpc("exec_sql", {"query": sql}).execute()
