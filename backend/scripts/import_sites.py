import requests
from sqlalchemy.orm import Session
from geoalchemy2 import WKTElement
from models.site_db import SiteDB
from db import SessionLocal  # your SQLAlchemy session factory

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
QUERY = """
[out:json][timeout:25];

// Get Whatcom County boundary
area["name"="Whatcom County"]["admin_level"="6"]["boundary"="administrative"]->.whatcom;

// Get Bellingham inside Whatcom County
area["name"="Bellingham"]["admin_level"="8"](area.whatcom)->.bellingham;

// --- All parks and relevant features inside Bellingham ---
(
  node["tourism"="camp_site"](area.bellingham);
  way["tourism"="camp_site"](area.bellingham);
  relation["tourism"="camp_site"](area.bellingham);

  node["highway"="trailhead"](area.bellingham);
  way["highway"="trailhead"](area.bellingham);
  relation["highway"="trailhead"](area.bellingham);

  node["tourism"="picnic_site"](area.bellingham);
  way["tourism"="picnic_site"](area.bellingham);
  relation["tourism"="picnic_site"](area.bellingham);

  node["leisure"="park"](area.bellingham);
  way["leisure"="park"](area.bellingham);
  relation["leisure"="park"](area.bellingham);

  node["tourism"="viewpoint"](area.bellingham);
  way["tourism"="viewpoint"](area.bellingham);
  relation["tourism"="viewpoint"](area.bellingham);
)->.parks_all;

// --- Parks as polygons for containment ---
(
  way["leisure"="park"](area.bellingham);
  relation["leisure"="park"](area.bellingham);
)->.parks_poly;

(.parks_poly; map_to_area;)->.park_areas;

// --- Access points inside parks ---
(
  node["amenity"="parking"](area.park_areas);
  way["amenity"="parking"](area.park_areas);

  node["tourism"="camp_site"](area.park_areas);
  way["tourism"="camp_site"](area.park_areas);

  node["highway"="trailhead"](area.park_areas);
  way["highway"="trailhead"](area.park_areas);

  node["tourism"="viewpoint"](area.park_areas);
  way["tourism"="viewpoint"](area.park_areas);
)->.park_access;

// --- UNION: parks OR access points ---
(
  .parks_all;
  .park_access;
);

out body geom;
"""
def centroid_from_bounds(bounds):
    """Compute centroid from min/max lat/lon."""
    if not bounds:
        return None, None
    lat = (bounds["minlat"] + bounds["maxlat"]) / 2
    lon = (bounds["minlon"] + bounds["maxlon"]) / 2
    return lat, lon

def fetch_overpass_data(max_retries=5):
    for attempt in range(max_retries):
        try:
            response = requests.post(OVERPASS_URL, data={"data": QUERY}, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Attempt {attempt+1}/{max_retries} failed: {e}")
    raise RuntimeError("Failed to fetch data from Overpass API after multiple attempts.")

def parse_and_insert_sites(data):
    db: Session = SessionLocal()
    inserted = 0
    try:
        for elem in data.get("elements", []):
            lat = elem.get("lat")
            lon = elem.get("lon")
            if lat is None or lon is None:
                lat, lon = centroid_from_bounds(elem.get("bounds"))

            name = elem.get("tags", {}).get("name") or "Unnamed Site"
            category = None
            tags = elem.get("tags", {})

            # determine category from tags, e.g., park, campground, viewpoint
            if "tourism" in tags:
                category = tags["tourism"]
            elif "leisure" in tags:
                category = tags["leisure"]
            elif "highway" in tags:
                category = tags["highway"]
            elif "amenity" in tags:
                category = tags["amenity"]

            source_ref = f"{elem['type']}_{elem['id']}"
            
            exists = db.query(SiteDB).filter_by(source="osm", source_ref=source_ref).first()
            if exists:
                continue
            
            site = SiteDB(
                name=name,
                description=tags.get("description"),
                category=category,
                geom=WKTElement(f"POINT({lon} {lat})", srid=4326),
                elevation_m=tags.get("ele"),
                source="osm",
                source_ref=source_ref,
                notes=tags
            )

            # Use upsert style: avoid duplicates based on source+source_ref
            try:
                db.add(site)
                db.commit()
                inserted += 1
            except Exception:
                db.rollback()  # could be duplicate or other error
        print(f"Inserted {inserted} new sites.")
    finally:
        db.close()

def main():
    data = fetch_overpass_data()
    parse_and_insert_sites(data)

if __name__ == "__main__":
    main()
