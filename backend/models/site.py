from pydantic import BaseModel
from typing import Optional
from models.visibility import Visibility

class Site(BaseModel):
    id: int
    latitude: float
    longitude: float
    name: str
    description: str
    visibility: Optional[Visibility]