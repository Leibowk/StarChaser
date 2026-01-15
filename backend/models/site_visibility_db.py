from sqlalchemy import Column, Index, Integer, Float, ForeignKey, TIMESTAMP, JSON, Enum, func
from db import Base
from models.site_db import SiteDB
from enums.site_visibility import SiteVisibility
from enums.time_visibility import TimeVisibility

class SiteVisibilityDB(Base):
    __tablename__ = "site_visibility"

    id = Column(Integer, primary_key=True)

    site_id = Column(Integer, ForeignKey(SiteDB.id, ondelete="CASCADE"), nullable=False)

    # core visibility
    score = Column(Float, nullable=False, index=True)
    time_bucket = Column(Enum(TimeVisibility), nullable=False, index=True)
    category = Column(Enum(SiteVisibility), nullable=False)

    # complex data stored as JSON
    light_pollution = Column(JSON, nullable=True)
    weather = Column(JSON, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("ix_site_visibility_time_bucket", "time_bucket"),
        Index("ix_site_visibility_score", "score"),
        Index("ix_site_visibility_time_score", "time_bucket", "score"),
    )