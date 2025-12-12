from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, func
from geoalchemy2 import Geography
from db import Base

class SiteDB(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    geom = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)
    elevation_m = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
