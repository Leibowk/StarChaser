from typing import Union
from shapely.geometry import Polygon, MultiPolygon, shape
import requests
from config import settings

class DriveTimeService:
    def __init__(self, http_client=requests):
        self.http_client = http_client
        self.base_url = settings.DRIVE_TIME_API.URL
        self.api_key = settings.DRIVE_TIME_API.API_KEY
        self.timeout = 5

    def get_drive_time_polygon(self, lat: float, lon: float, minutes: int) -> Union[Polygon, MultiPolygon]:
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }

        body = {
            "locations": [[lon, lat]],
            "range": [minutes * 60],
        }

        resp = self.http_client.post(self.base_url, json=body, headers=headers, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()

        # Extract first polygon geometry
        geometry = data["features"][0]["geometry"]
        return shape(geometry)
