from pydantic import BaseModel
from typing import Optional
from models.light_pollution import LightPollution

class SiteSummary(BaseModel):
    id: int
    latitude: float
    longitude: float
    name: str
    description: str
    light_pollution: Optional[LightPollution]