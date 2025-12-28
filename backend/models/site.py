from pydantic import BaseModel

class Site(BaseModel):
    id: int
    latitude: float
    longitude: float
    name: str
    description: str