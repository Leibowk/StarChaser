from typing import Optional
from models.site_db import SiteDB
from sqlalchemy.orm import Session
from sqlalchemy import and_, select, func
from db import SessionLocal
from geoalchemy2 import Geometry

class SiteRepository:
    def __init__(self):
        self.session = SessionLocal()

    def get_all_sites(self) -> list[SiteDB]:
        query = select(
            SiteDB.id,
            SiteDB.name,
            SiteDB.description,
            func.ST_X(SiteDB.geom.cast(Geometry)).label("longitude"),
            func.ST_Y(SiteDB.geom.cast(Geometry)).label("latitude")
        )
        result = self.session.execute(query).all()

        return result

    def get_site(self, site_id) -> SiteDB:
        query = select(
            SiteDB.id,
            SiteDB.name,
            SiteDB.description,
            func.ST_X(SiteDB.geom.cast(Geometry)).label("longitude"),
            func.ST_Y(SiteDB.geom.cast(Geometry)).label("latitude")
        ).where(SiteDB.id == site_id)
        result = self.session.execute(query).first()
        return result
    
    def search(
        self,
        name: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        radius_km: Optional[float] = None,
        drive_time_polygon: Optional[dict] = None) -> list[SiteDB]:

        query = select(
            SiteDB.id,
            SiteDB.name,
            SiteDB.description,
            func.ST_X(SiteDB.geom.cast(Geometry)).label("longitude"),
            func.ST_Y(SiteDB.geom.cast(Geometry)).label("latitude")
        )

        filters = []

        # --- Name filter (case-insensitive contains) ---
        if name:
            filters.append(SiteDB.name.ilike(f"%{name}%"))

        # --- Radius filter (only if all 3 present) ---
        if lat is not None and lon is not None and radius_km is not None:
            radius_meters = radius_km * 1000

            point = func.ST_SetSRID(
                func.ST_MakePoint(lon, lat),
                4326
            )

            filters.append(
                func.ST_DWithin(
                    SiteDB.geom,
                    point,
                    radius_meters
                )
            )

        if drive_time_polygon is not None:
            polygon_geom = func.ST_SetSRID(
                func.ST_GeomFromGeoJSON(drive_time_polygon),
                4326
            )

            filters.append(
                func.ST_Intersects(
                    SiteDB.geom,
                    polygon_geom
                )
            )

        if filters:
            query = query.where(and_(*filters))

        result = self.session.execute(query).all()
        return result
