"""About endpoint – returns basic service metadata."""

from __future__ import annotations

from fastapi import APIRouter

from app.config import settings
from app.models.about import AboutInfo

router = APIRouter(tags=["About"])

_SERVICE_NAME = "sre-order-tracker-api"
_DESCRIPTION = "Backend API for the E-Commerce Order Tracker demo workload."
_CONTACT = "https://github.com/omerfeldman22/sre-agent-backend/issues"
_REPOSITORY = "https://github.com/omerfeldman22/sre-agent-backend"


@router.get("/about", response_model=AboutInfo)
async def get_about():
    """Return basic service information (version, environment, contact)."""
    return AboutInfo(
        service=_SERVICE_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        description=_DESCRIPTION,
        contact=_CONTACT,
        repository=_REPOSITORY,
    )
