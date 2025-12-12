import json
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

# load your JSON manually
with open("localsettings.json") as f:
    data = json.load(f)

settings = Settings(**data)