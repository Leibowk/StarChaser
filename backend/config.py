import json
from pydantic_settings import BaseSettings
from pydantic import BaseModel


class PostgresSettings(BaseModel):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int = 5432
    DB: str


class ApiSettings(BaseModel):
    URL: str
    API_KEY: str

class SecretSettings(BaseModel):
    Key: str


class Settings(BaseSettings):
    POSTGRES: PostgresSettings
    WEATHER_API: ApiSettings
    OPEN_WEATHER_MAP: ApiSettings
    DRIVE_TIME_API: ApiSettings
    Secrets: SecretSettings


with open("localsettings.json") as f:
    data = json.load(f)

settings = Settings(**data)