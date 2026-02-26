"""Response model for the /api/about endpoint."""

from pydantic import BaseModel


class AboutInfo(BaseModel):
    """Basic service/application information returned by GET /api/about."""

    service: str       # Logical name of this backend service
    version: str       # Semver application version (from APP_VERSION env var)
    environment: str   # Deployment environment, e.g. "production" or "development"
    status: str        # Operational status — always "ok" when the service is up
