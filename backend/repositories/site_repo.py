from models.site_db import SiteDB  # your ORM model
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from db import SessionLocal
from geoalchemy2 import Geometry

class SiteRepository:
    def __init__(self):
        self.session = SessionLocal()

    def get_all_sites(self):
        query = select(
            SiteDB.id,
            SiteDB.name,
            SiteDB.description,
            func.ST_X(SiteDB.geom.cast(Geometry)).label("longitude"),
            func.ST_Y(SiteDB.geom.cast(Geometry)).label("latitude")
        )
        result = self.session.execute(query).all()

        sites = []
        for row in result:
            sites.append({
                "id": row.id,
                "name": row.name,
                "description": row.description,
                "latitude": row.latitude,   # NOTE: ST_X is longitude
                "longitude": row.longitude    # ST_Y is latitude
            })
        return sites
