from pydantic import BaseModel
from typing import Optional
from schemas.visibility import Visibility

class Site(BaseModel):
    id: int
    latitude: float
    longitude: float
    name: str
    description: Optional[str]
    visibility: Optional[Visibility]