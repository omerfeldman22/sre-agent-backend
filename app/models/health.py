from enum import Enum
from pydantic import BaseModel


class HealthCheckResult(str, Enum):
    UP = "up"
    DOWN = "down"


class HealthChecks(BaseModel):
    database: HealthCheckResult
    cache: HealthCheckResult


class HealthStatus(BaseModel):
    status: str  # "healthy" | "degraded" | "unhealthy"
    version: str
    uptime: float
    checks: HealthChecks
