from typing import Optional
from pydantic import BaseModel
from enums.site_visibility import SiteVisibility
from models.weather import Weather
from models.light_pollution import LightPollution

class Visibility(BaseModel):
    score: float
    category: SiteVisibility
    light_pollution: Optional[LightPollution]
    weather: Optional[Weather]