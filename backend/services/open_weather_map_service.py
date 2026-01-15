import requests
from typing import Optional
from enums.time_visibility import TimeVisibility
from config import settings
from schemas.weather import Weather
from services.date_time_service import DateTimeService

class OpenWeatherMapService:
    def __init__(self, http_client=requests):
        self.http_client = http_client
        self.base_url = settings.OPEN_WEATHER_MAP.URL
        self.api_key = settings.OPEN_WEATHER_MAP.API_KEY
        self.timeout = 5  # seconds
        self.datetimeservice = DateTimeService()

    def get_forecast_weather(self, lat: float, lon: float, time_visibility: Optional[TimeVisibility]) -> Optional[Weather]:
        daytime = self.datetimeservice.date_time_helper(time_visibility)

        # --- Weather Forecast ---
        weather_params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"  # get metric units
        }

        try:
            # Forecast
            weather_resp = self.http_client.get(
                f"{self.base_url}forecast",
                params=weather_params,
                timeout=self.timeout,
            )
            weather_resp.raise_for_status()
            weather_data = weather_resp.json()

            # Find nearest forecast entry by datetime
            target_unix = int(daytime.timestamp())
            best_item = None
            diff = float("inf")

            for item in weather_data.get("list", []):
                # "dt" is Unix timestamp
                dt = item.get("dt")
                if dt is None:
                    continue

                delta = abs(dt - target_unix)
                if delta < diff:
                    diff = delta
                    best_item = item

            if not best_item:
                return None

            # Extract weather info
            cloud_coverage = best_item.get("clouds", {}).get("all", 0)
            avgvis_m = best_item.get("visibility", 0)  # meters
            avgvis_km = avgvis_m / 1000.0
            condition = best_item.get("weather", [{}])[0].get("description", "")

            # --- Air Pollution Forecast (AQI) ---
            aqi = None
            air_resp = self.http_client.get(
                f"{self.base_url}air_pollution/forecast",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key
                },
                timeout=self.timeout,
            )
            air_resp.raise_for_status()
            air_data = air_resp.json()

            # Find nearest air quality entry
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

            if best_aqi:
                aqi = best_aqi.get("main", {}).get("aqi")

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