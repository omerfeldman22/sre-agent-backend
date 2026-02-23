from __future__ import annotations

from pydantic import BaseModel


class AboutInfo(BaseModel):
    service: str
    version: str
    environment: str
    description: str
    contact: str
    repository: str
