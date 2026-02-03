import httpx
import asyncio
from typing import Optional
from enums.time_visibility import TimeVisibility
from config import settings
from schemas.weather import Weather
from services.date_time_service import DateTimeService


class OpenWeatherMapService:
    def __init__(self, http_client=None, date_time_service=None):
        self.http_client = http_client or httpx.AsyncClient()
        self.base_url = settings.OPEN_WEATHER_MAP.URL
        self.api_key = settings.OPEN_WEATHER_MAP.API_KEY
        self.timeout = 5  # seconds
        self.datetimeservice = date_time_service or DateTimeService()

    async def get_forecast_weather(self, lat: float, lon: float, time_visibility: Optional[TimeVisibility]) -> Optional[Weather]:
        daytime = self.datetimeservice.date_time_helper(time_visibility)
        weather_params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"
        }
        try:
            client = self.http_client
            weather_resp = await client.get(
                f"{self.base_url}forecast",
                params=weather_params
            )
            weather_resp.raise_for_status()
            weather_data = await weather_resp.json() if asyncio.iscoroutinefunction(weather_resp.json) else weather_resp.json()

            target_unix = int(daytime.timestamp())
            best_item = None
            diff = float("inf")
            for item in weather_data.get("list", []):
                dt = item.get("dt")
                if dt is None:
                    continue
                delta = abs(dt - target_unix)
                if delta < diff:
                    diff = delta
                    best_item = item
            if not best_item:
                return None
            cloud_coverage = best_item.get("clouds", {}).get("all", 0)
            avgvis_m = best_item.get("visibility", 0)
            avgvis_km = avgvis_m / 1000.0
            condition = best_item.get("weather", [{}])[0].get("description", "")

            air_resp = await client.get(
                f"{self.base_url}air_pollution/forecast",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key
                }
            )
            air_resp.raise_for_status()
            air_data = await air_resp.json() if asyncio.iscoroutinefunction(air_resp.json) else air_resp.json()
            best_aqi = None
            best_diff = float("inf")
            for entry in air_data.get("list", []):
                dt = entry.get("dt")
                if dt is None:
                    continue
                delta = abs(dt - target_unix)
                if delta < best_diff:
                    best_diff = delta
                    best_aqi = entry
            aqi = best_aqi.get("main", {}).get("aqi") if best_aqi else None
            return Weather(
                cloud_coverage=cloud_coverage,
                avgvis_km=avgvis_km,
                avgvis_miles=avgvis_km * 0.621371,
                condition=condition,
                aqi=aqi,
            )
        except Exception as e:
            print(f"[OpenWeatherMapService] Error fetching weather: {e}")
            return None

    async def get_forecast_weathers(self, lat: float, lon: float, times: list[TimeVisibility]) -> dict[TimeVisibility, Weather]:
        target_times = {t: int(self.datetimeservice.date_time_helper(t).timestamp()) for t in times}
        weather_params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                weather_resp = await client.get(
                    f"{self.base_url}forecast",
                    params=weather_params
                )
                weather_resp.raise_for_status()
                weather_data = weather_resp.json()
                air_resp = await client.get(
                    f"{self.base_url}air_pollution/forecast",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key
                    }
                )
                air_resp.raise_for_status()
                air_data = air_resp.json()
                result = {}
                for time_vis, target_unix in target_times.items():
                    best_item = None
                    diff = float("inf")
                    for item in weather_data.get("list", []):
                        dt = item.get("dt")
                        if dt is None:
                            continue
                        delta = abs(dt - target_unix)
                        if delta < diff:
                            diff = delta
                            best_item = item
                    if not best_item:
                        result[time_vis] = None
                        continue
                    cloud_coverage = best_item.get("clouds", {}).get("all", 0)
                    avgvis_m = best_item.get("visibility", 0)
                    avgvis_km = avgvis_m / 1000.0
                    condition = best_item.get("weather", [{}])[0].get("description", "")
                    best_aqi = None
                    best_diff = float("inf")
                    for entry in air_data.get("list", []):
                        dt = entry.get("dt")
                        if dt is None:
                            continue
                        delta = abs(dt - target_unix)
                        if delta < best_diff:
                            best_diff = delta
                            best_aqi = entry
                    aqi = best_aqi.get("main", {}).get("aqi") if best_aqi else None
                    result[time_vis] = Weather(
                        cloud_coverage=cloud_coverage,
                        avgvis_km=avgvis_km,
                        avgvis_miles=avgvis_km * 0.621371,
                        condition=condition,
                        aqi=aqi,
                    )
                return result
        except Exception as e:
            print(f"[OpenWeatherMapService] Error fetching batched weather: {e}")
            return {t: None for t in times}