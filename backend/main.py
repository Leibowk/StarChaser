from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.site_service import SiteService
from fastapi.staticfiles import StaticFiles
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

@app.get("/sites")
def get_sites():
    return site_service.get_all_sites()

@app.get("/site/{site_id}")
def get_site(site_id: int):
    return site_service.get_site(site_id)
