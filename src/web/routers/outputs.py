"""Analysis output endpoints — list and download."""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from typing import Optional

from src.web.services.supabase_data import get_data_service

router = APIRouter(prefix="/api/outputs", tags=["outputs"])

# MIME type mapping
_MIME = {
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".pdf": "application/pdf",
    ".md": "text/markdown",
    ".html": "text/html",
    ".json": "application/json",
    ".txt": "text/plain",
}


@router.get("")
def list_outputs(market_id: Optional[str] = Query(None)):
    """Return analysis output file metadata."""
    svc = get_data_service()
    return svc.get_analysis_outputs(market_id=market_id)


@router.get("/{output_id}/download")
def download_output(output_id: int):
    """Download an output file from Supabase Storage."""
    svc = get_data_service()
    record = svc.get_output(output_id)
    if not record:
        raise HTTPException(404, f"Output #{output_id} not found")

    storage_path = record.get("storage_path")
    if not storage_path:
        raise HTTPException(404, "No storage_path for this output")

    try:
        data = svc.download_output_file(storage_path)
    except Exception as exc:
        raise HTTPException(502, f"Storage download failed: {exc}")

    filename = storage_path.rsplit("/", 1)[-1]
    ext = "." + filename.rsplit(".", 1)[-1] if "." in filename else ""
    content_type = _MIME.get(ext, "application/octet-stream")

    return Response(
        content=data,
        media_type=content_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
