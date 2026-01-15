from pydantic import BaseModel

class LightPollution(BaseModel):
    lp_index: float
    mag_arcsec: float
    lp_zone: str
    color_zone: str