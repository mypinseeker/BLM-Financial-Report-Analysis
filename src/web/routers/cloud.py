"""Cloud status endpoint."""

from fastapi import APIRouter

from src.web.services.supabase_data import get_data_service

router = APIRouter(prefix="/api/cloud", tags=["cloud"])


@router.get("/status")
def cloud_status():
    """Return row counts for all Supabase tables."""
    svc = get_data_service()
    return svc.get_cloud_status()
