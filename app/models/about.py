from pydantic import BaseModel


class AboutInfo(BaseModel):
    service: str
    version: str
    environment: str
    status: str
