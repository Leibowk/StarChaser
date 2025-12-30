from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.site_service import SiteService
from fastapi.staticfiles import StaticFiles
from models.site import Site
from models.site_summary import SiteSummary
import os

app = FastAPI()

# CORS settings
origins = [
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
tiles_path = os.path.join(os.path.dirname(__file__), "image_tiles")
app.mount("/tiles", StaticFiles(directory=tiles_path), name="tiles")

@app.get("/sites", response_model=list[SiteSummary])
def get_sites() -> list[SiteSummary]:
    return site_service.get_all_sites()

@app.get("/site/{site_id}", response_model=Site)
def get_site(site_id: int) -> Site:
    return site_service.get_site(site_id)

@app.get("/sites/search", response_model=list[SiteSummary])
def search(
    name: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius_km: Optional[float] = None) -> list[SiteSummary]:
    return site_service.search(name, lat, lon, radius_km)
