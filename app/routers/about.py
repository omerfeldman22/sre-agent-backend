"""About endpoint."""

from __future__ import annotations

from fastapi import APIRouter

from app.config import settings
from app.models.about import AboutInfo

router = APIRouter(tags=["About"])


@router.get("/about", response_model=AboutInfo)
async def get_about():
    """Return basic service/application information."""
    return AboutInfo(
        service="sre-order-tracker-api",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        status="ok",
    )
