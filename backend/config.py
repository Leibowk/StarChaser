import json
from pydantic_settings import BaseSettings
from pydantic import BaseModel


class PostgresSettings(BaseModel):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int = 5432
    DB: str


class WeatherSettings(BaseModel):
    URL: str
    API_KEY: str


class Settings(BaseSettings):
    POSTGRES: PostgresSettings
    WEATHER: WeatherSettings


with open("localsettings.json") as f:
    data = json.load(f)

settings = Settings(**data)