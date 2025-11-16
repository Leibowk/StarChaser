from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8081",  # Expo dev server
    "http://127.0.0.1:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Site(BaseModel):
    latitude: float = 0
    longitude: float = 0
    name: str

sites = []

bouldevardPark = Site(
    latitude=48.731718,
    longitude=-122.5024262,
    name="Boulevard Park"
)

arb = Site(
    latitude=48.7354156,
    longitude=-122.4798767,
    name="Sehome Hill Arboretum"
)

galb = Site(
    latitude=48.7171746,
    longitude=-122.458955,
    name="Galbraith Mountain"
)

sites.append(bouldevardPark)
sites.append(arb)
sites.append(galb)

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/sites")
def get_sites():
    return sites