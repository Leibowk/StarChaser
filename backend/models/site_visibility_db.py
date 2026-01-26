from sqlalchemy import Column, Date, Index, Integer, Float, ForeignKey, TIMESTAMP, JSON, Enum, func
from db import Base
from models.site_db import SiteDB

class SiteVisibilityDB(Base):
    __tablename__ = "site_visibility"

    id = Column(Integer, primary_key=True)

    site_id = Column(Integer, ForeignKey(SiteDB.id, ondelete="CASCADE"), nullable=False)

    # core visibility
    score = Column(Float, nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)

    # complex data stored as JSON
    light_pollution = Column(JSON, nullable=True)
    weather = Column(JSON, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("ix_site_visibility_date", "date"),
        Index("ix_site_visibility_score", "score"),
        Index("ix_site_visibility_date_score", "date", "score"),
    )