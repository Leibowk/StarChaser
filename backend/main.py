from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from repositories.site_repo import SiteRepository
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
site_repo = SiteRepository()

# Serve your image_tiles folder
tiles_path = os.path.join(os.path.dirname(__file__), "image_tiles")
bi_tiles_path = os.path.join(os.path.dirname(__file__), "binary_tiles")

app.mount("/tiles", StaticFiles(directory=tiles_path), name="tiles")
app.mount("/bi_tiles", StaticFiles(directory=bi_tiles_path, html=False), name="bi_tiles")

@app.get("/sites")
def get_sites():
    return site_repo.get_all_sites()
