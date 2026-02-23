"""OpenTelemetry + Azure Monitor telemetry bootstrap.

Call ``setup_telemetry()`` once at application startup.
"""

from __future__ import annotations

import logging

from app.config import settings

logger = logging.getLogger(__name__)


def setup_telemetry() -> None:
    """Configure OpenTelemetry tracing and metrics with Azure Monitor export.

    If no Application Insights connection string is set the function is a no-op,
    so local development works without any cloud dependency.
    """
    conn_str = settings.APPLICATIONINSIGHTS_CONNECTION_STRING
    if not conn_str:
        logger.info("No App Insights connection string — telemetry disabled")
        return

    try:
        from azure.monitor.opentelemetry import configure_azure_monitor

        configure_azure_monitor(
            connection_string=conn_str,
            enable_live_metrics=True,
        )
        logger.info("Azure Monitor telemetry configured")
    except ImportError:
        logger.warning(
            "azure-monitor-opentelemetry not installed — telemetry disabled"
        )
    except Exception:
        logger.exception("Failed to configure Azure Monitor telemetry")
