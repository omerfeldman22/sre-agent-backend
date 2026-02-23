"""Health-check endpoint."""

from __future__ import annotations

import time
from fastapi import APIRouter

from app.models.health import HealthCheckResult, HealthChecks, HealthStatus

router = APIRouter(tags=["Health"])

_start_time = time.time()
_VERSION = "1.0.0"


@router.get("/health", response_model=HealthStatus)
async def health_check():
    """Return overall service health."""
    db_ok = HealthCheckResult.UP
    cache_ok = HealthCheckResult.UP

    # Determine overall status
    if db_ok == HealthCheckResult.UP and cache_ok == HealthCheckResult.UP:
        overall = "healthy"
    elif db_ok == HealthCheckResult.DOWN and cache_ok == HealthCheckResult.DOWN:
        overall = "unhealthy"
    else:
        overall = "degraded"

    return HealthStatus(
        status=overall,
        version=_VERSION,
        uptime=round(time.time() - _start_time, 2),
        checks=HealthChecks(database=db_ok, cache=cache_ok),
    )
