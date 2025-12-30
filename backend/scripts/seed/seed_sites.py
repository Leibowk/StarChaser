# backend/seeds/seed_sites.py

from db import SessionLocal
from models.site_db import SiteDB
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

def seed_sites() -> None:
    session = SessionLocal()

    # Prevent duplicate seeding
    existing = session.query(SiteDB).count()
    if existing > 0:
        print("Sites already seeded, skipping.")
        session.close()
        return

    sites = [
        SiteDB(
            name="Boulevard Park",
            description="Beautiful waterway looking over the bay",
            geom=from_shape(Point(-122.5024262, 48.731718), srid=4326),
            elevation_m=None,
        ),
        SiteDB(
            name="Sehome Hill Arboretum",
            description="Hill and forest area behind Western Washington University",
            geom=from_shape(Point(-122.4798767, 48.7354156), srid=4326),
            elevation_m=None,
        ),
        SiteDB(
            name="Larrabee State Park",
            description="Large camping park on Samish Bay with a beach, 2 freshwater lakes & miles of hiking & biking trails.",
            geom=from_shape(Point(-122.4669355, 48.6624933), srid=4326),
            elevation_m=None,
        ),
        SiteDB(
            name="Pasayten Wilderness",
            description="531,000-acre preserve offering multiple trails, scenic peaks, waterways & abundant flora & fauna.",
            geom=from_shape(Point(-120.5621193, 48.8150877), srid=4326),
            elevation_m=None,
        ),
        SiteDB(
            name="Galbraith Mountain",
            description="Mt Biker's Haven",
            geom=from_shape(Point(-122.458955, 48.7171746), srid=4326),
            elevation_m=None,
        ),
        SiteDB(
            name="Strathcona Park",
            description="Dog-friendly park with a playground, climbing wall & skate park, plus a variety of sports courts.",
            geom=from_shape(Point(-123.0872729, 49.275182), srid=4326),
            elevation_m=None,
        ),
    ]

    session.add_all(sites)
    session.commit()
    session.close()

    print("Seeded sites successfully.")

if __name__ == "__main__":
    seed_sites()
