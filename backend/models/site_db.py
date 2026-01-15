from sqlalchemy import JSON, Column, Integer, String, Float, TIMESTAMP, UniqueConstraint, func
from geoalchemy2 import Geography
from db import Base

class SiteDB(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)

    # Core site data
    name = Column(String, nullable=False)
    description = Column(String)

    # Spatial
    geom = Column(Geography("POINT", srid=4326), nullable=False)
    elevation_m = Column(Float)

    # Raw source
    source = Column(String)
    source_ref = Column(String)
    category = Column(String)
    notes = Column(JSON)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("source", "source_ref", name="uq_sites_source"),
    )