"""FastAPI application entry-point."""

from __future__ import annotations

import logging
import time
import uuid

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.telemetry import setup_telemetry
from app.routers import products, orders, inventory, health

# ─── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)

# ─── Telemetry ────────────────────────────────────────────────────────────────

setup_telemetry()

# ─── FastAPI App ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="SRE Order Tracker API",
    description="Backend API for the E-Commerce Order Tracker demo workload.",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

# ─── CORS ─────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["x-correlation-id"],
)


# ─── Middleware ───────────────────────────────────────────────────────────────

@app.middleware("http")
async def correlation_and_timing(request: Request, call_next):
    """Propagate / generate a correlation-id and log request duration."""
    correlation_id = request.headers.get("x-correlation-id", str(uuid.uuid4()))
    start = time.perf_counter()

    response: Response = await call_next(request)

    duration_ms = (time.perf_counter() - start) * 1000
    response.headers["x-correlation-id"] = correlation_id
    response.headers["x-response-time-ms"] = f"{duration_ms:.1f}"

    logger.info(
        "%s %s %d %.1fms cid=%s",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
        correlation_id,
    )
    return response


# ─── Routers ─────────────────────────────────────────────────────────────────

app.include_router(health.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(inventory.router, prefix="/api")


# ─── Root redirect ───────────────────────────────────────────────────────────

@app.get("/", include_in_schema=False)
async def root():
    return {"service": "sre-order-tracker-api", "version": settings.APP_VERSION}
