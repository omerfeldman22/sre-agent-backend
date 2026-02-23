"""Application configuration — reads from environment variables."""

from __future__ import annotations

import os


class Settings:
    """Simple settings container backed by env vars."""

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # CORS — comma-separated list of allowed origins
    ALLOWED_ORIGINS: list[str] = [
        o.strip()
        for o in os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:5173,http://localhost:3000,https://omerfsre.azurewebsites.net",
        ).split(",")
        if o.strip()
    ]

    # Observability
    APPLICATIONINSIGHTS_CONNECTION_STRING: str = os.getenv(
        "APPLICATIONINSIGHTS_CONNECTION_STRING", ""
    )

    # App metadata
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
