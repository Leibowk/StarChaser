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

        sites = []
        for row in result:
          sites.append(
                Site(
                    id=row.id,
                    name=row.name,
                    description=row.description,
                    latitude=row.latitude,
                    longitude=row.longitude
                )
          )
        return sites

    def get_site(self, site_id):
        query = select(
            SiteDB.id,
            SiteDB.name,
            SiteDB.description,
            func.ST_X(SiteDB.geom.cast(Geometry)).label("longitude"),
            func.ST_Y(SiteDB.geom.cast(Geometry)).label("latitude")
        ).where(SiteDB.id == site_id)
        result = self.session.execute(query).first()
        if result:
            return Site(
                id=result.id,
                name=result.name,
                description=result.description,
                latitude=result.latitude,
                longitude=result.longitude
            )
        return None
