import requests
from typing import Optional
from services.date_time_service import DateTimeService
from enums.time_visibility import TimeVisibility
from config import settings
from schemas.weather import Weather


class WeatherApiService:
    def __init__(self, http_client=requests):
        self.http_client = http_client
        self.base_url = settings.WEATHER_API.URL
        self.api_key = settings.WEATHER_API.API_KEY
        self.timeout = 5  # seconds
        self.datetimeservice = DateTimeService()

    def get_forecast_weather(self, lat: float, lon: float, time_visibility: Optional[TimeVisibility] = None) -> Optional[Weather]:
        """
        Fetches forecast weather for a lat/lon and returns a Weather model.
        """
        daytime = self.datetimeservice.date_time_helper(time_visibility)

        params = {
            "key": self.api_key,
            "q": f"{lat},{lon}",
            "aqi": "yes",
            "days": 1,
            "dt": daytime.date(),
            "hour": daytime.time().hour
        }

        try:
            response = self.http_client.get(
                self.base_url,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()

            forecast = data.get("forecast", {}).get("forecastday", [])[0]
            air_quality = forecast.get("air_quality", {})

            return Weather(
                cloud_coverage=forecast.get("hour", {})[0].get("cloud", 0),
                avgvis_km=forecast.get("hour", {})[0].get("vis_km", 0.0),
                avgvis_miles=forecast.get("hour", {})[0].get("vis_miles", 0.0),
                condition=forecast.get("hour", {})[0].get("condition", {}).get("text", ""),
                aqi=air_quality.get("us-epa-index"),
            )

        except Exception as e:
            print(f"[WeatherApiService] Error fetching weather: {e}")
            return None