from typing import Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from middleware.rate_limit import register_rate_limiter
from middleware.auth import APIKeyMiddleware
from enums.site_visibility import SiteVisibility
from services.site_service import SiteService
from fastapi.staticfiles import StaticFiles
from models.site import Site
from models.site_summary import SiteSummary
import os
from config import settings

app = FastAPI()

api_primary_key = settings.Secrets.Key
app.add_middleware(APIKeyMiddleware, api_key=api_primary_key)
register_rate_limiter(app)

# CORS settings
origins = [
    "https://thestarchaser.com",
    "http://localhost:8081",
    "http://127.0.0.1:8080",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize repository
site_service = SiteService()

# Serve light pollution tiles
tiles_dir = os.path.join(os.path.dirname(__file__), "image_tiles")
app.mount("/tiles", StaticFiles(directory=tiles_dir), name="tiles")

@app.get("/sites", response_model=list[SiteSummary])
def get_sites() -> list[SiteSummary]:
    return site_service.get_all_sites()

@app.get("/site/{site_id}", response_model=Site)
def get_site(site_id: int) -> Site:
    return site_service.get_site(site_id)

@app.get(
        "/sites/search", 
        response_model=list[Site],
        summary="Search observation sites",
        description=(
            "Search sites by name and/or proximity.\n\n"
            "- `name`: substring match on site name\n"
            "- `lat`, `lon`, `radius_km`: return sites within a radius\n"
            "- Parameters may be combined (AND logic)"
        ))
def search(
    name: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius_km: Optional[float] = None,
    site_visib: Optional[SiteVisibility] = Query(
        None,
        description="Overall site visibility rating",
    )) -> list[Site]:
    return site_service.search(name, lat, lon, radius_km, site_visib)
