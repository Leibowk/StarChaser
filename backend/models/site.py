from pydantic import BaseModel

class Site(BaseModel):
    latitude: float
    longitude: float
    name: str
    description: str