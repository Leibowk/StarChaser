from models.site_db import SiteDB  # your ORM model
from models.site import Site       # import your Site type
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

        return result

    def get_site(self, site_id):
        query = select(
            SiteDB.id,
            SiteDB.name,
            SiteDB.description,
            func.ST_X(SiteDB.geom.cast(Geometry)).label("longitude"),
            func.ST_Y(SiteDB.geom.cast(Geometry)).label("latitude")
        ).where(SiteDB.id == site_id)
        result = self.session.execute(query).first()
        return result
