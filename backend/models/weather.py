from pydantic import BaseModel

class Weather(BaseModel):
    cloud_coverage: int
    avgvis_km: float
    avgvis_miles: float
    condition: str
    aqi: int | None
    


