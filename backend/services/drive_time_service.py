import json
from shapely import unary_union
from shapely.geometry import shape, mapping
import httpx
from config import settings

class DriveTimeService:
    def __init__(self, http_client=None):
        self.http_client = http_client or httpx.AsyncClient()
        self.base_url = settings.DRIVE_TIME_API.URL
        self.api_key = settings.DRIVE_TIME_API.API_KEY
        self.timeout = 5

    async def get_drive_time_polygon(self, lat: float, lon: float, minutes: int) -> str:
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }
        body = {
            "locations": [[lon, lat]],
            "range": [minutes * 60],
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(self.base_url, json=body, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            if not data.get("features"):
                raise ValueError("Drive-time API returned no polygons")
            polygons = [shape(f["geometry"]) for f in data["features"]]
            merged_polygon = unary_union(polygons)
            return json.dumps(mapping(merged_polygon))
