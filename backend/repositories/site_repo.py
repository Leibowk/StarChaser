from typing import Optional
from datetime import date
from models.site_db import SiteDB
from models.site_visibility_db import SiteVisibilityDB
from sqlalchemy import and_, select, func
from db import AsyncSessionLocal
from geoalchemy2 import Geometry
from enums.search_order import SearchOrder


class SiteRepository:
    def __init__(self):
        pass

    async def get_all_sites(self):
        async with AsyncSessionLocal() as session:
            query = select(
                SiteDB.id,
                SiteDB.name,
                SiteDB.description,
                func.ST_X(SiteDB.geom.cast(Geometry)).label("longitude"),
                func.ST_Y(SiteDB.geom.cast(Geometry)).label("latitude")
            )
            result = await session.execute(query)
            return result.all()

    async def get_site(self, site_id):
        async with AsyncSessionLocal() as session:
            query = select(
                SiteDB.id,
                SiteDB.name,
                SiteDB.description,
                func.ST_X(SiteDB.geom.cast(Geometry)).label("longitude"),
                func.ST_Y(SiteDB.geom.cast(Geometry)).label("latitude")
            ).where(SiteDB.id == site_id)
            result = await session.execute(query)
            return result.first()
    
    async def get_visibility(self, site_id: int, date: date):
        async with AsyncSessionLocal() as session:
            query = select(SiteVisibilityDB).where(
                and_(SiteVisibilityDB.site_id == site_id, SiteVisibilityDB.date == date)
            )
            result = await session.execute(query)
            row = result.first()
            if row:
                return row[0]
            return None
    

    async def search(
        self,
        lat: float,
        lon: float,
        drive_time_polygon: dict,
        date: date,
        min_score: int,
        limit: int,
        offset: int,
        order_by: SearchOrder,
        name: Optional[str] = None,
    ):
        async with AsyncSessionLocal() as session:
            user_point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
            distance_expr = func.ST_Distance(SiteDB.geom.cast(Geometry), user_point)

            polygon_geom = func.ST_SetSRID(
                func.ST_GeomFromGeoJSON(drive_time_polygon),
                4326
            )

            query = select(
                SiteDB.id,
                SiteDB.name,
                SiteDB.description,
                func.ST_X(SiteDB.geom.cast(Geometry)).label("longitude"),
                func.ST_Y(SiteDB.geom.cast(Geometry)).label("latitude"),
                SiteVisibilityDB.score,
                SiteVisibilityDB.weather,
                SiteVisibilityDB.light_pollution
            ).join(SiteVisibilityDB, and_(SiteDB.id == SiteVisibilityDB.site_id, SiteVisibilityDB.date == date))

            filters = [
                func.ST_Intersects(SiteDB.geom, polygon_geom),
                SiteVisibilityDB.score >= min_score,
            ]
            if name:
                filters.append(SiteDB.name.ilike(f"%{name}%"))

            query = query.where(and_(*filters))

            # Composite ORDER BY: always both columns
            if order_by == SearchOrder.Visibility:
                query = query.order_by(SiteVisibilityDB.score.desc(), distance_expr.asc())
            else:
                query = query.order_by(distance_expr.asc(), SiteVisibilityDB.score.desc())

            query = query.limit(limit).offset(offset)

            result = await session.execute(query)
            return result.all()

    async def upsert_visibility(self, records: list[dict]):
        async with AsyncSessionLocal() as session:
            for r in records:
                query = select(SiteVisibilityDB).filter_by(site_id=r["site_id"], date=r["date"])
                result = await session.execute(query)
                existing = result.scalars().first()

                if existing:
                    existing.score = r["score"]
                    existing.weather = r["weather"]
                    existing.light_pollution = r["light_pollution"]
                else:
                    session.add(SiteVisibilityDB(**r))

            await session.commit()