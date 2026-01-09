import json
from shapely import unary_union
from shapely.geometry import shape, mapping
import requests
from config import settings

class DriveTimeService:
    def __init__(self, http_client=requests):
        self.http_client = http_client
        self.base_url = settings.DRIVE_TIME_API.URL
        self.api_key = settings.DRIVE_TIME_API.API_KEY
        self.timeout = 5

    def get_drive_time_polygon(self, lat: float, lon: float, minutes: int) -> str:
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

        if not data.get("features"):
            raise ValueError("Drive-time API returned no polygons")

        # Merge all features in case API returns multiple ranges
        polygons = [shape(f["geometry"]) for f in data["features"]]
        merged_polygon = unary_union(polygons)

        return json.dumps(mapping(merged_polygon))
