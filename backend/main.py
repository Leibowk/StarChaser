from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from repositories.site_repo import SiteRepository

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

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/sites")
def get_sites():
    return site_repo.get_all_sites()
