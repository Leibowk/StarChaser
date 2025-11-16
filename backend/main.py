from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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

sites.append(bouldevardPark)

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/sites")
def get_sites():
    return sites