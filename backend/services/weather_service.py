import requests
from typing import Optional
from config import settings
from models.weather import Weather


class WeatherService:
    def __init__(self):
        self.base_url = settings.WEATHER.URL
        self.api_key = settings.WEATHER.API_KEY
        self.timeout = 5  # seconds

    def get_current_weather(self, lat: float, lon: float) -> Optional[Weather]:
        """
        Fetches current weather for a lat/lon and returns a Weather model.
        """
        params = {
            "key": self.api_key,
            "q": f"{lat},{lon}",
            "aqi": "yes",
        }

        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()

            current = data.get("current", {})
            air_quality = current.get("air_quality", {})

            return Weather(
                cloud_coverage=current.get("cloud", 0),
                avgvis_km=current.get("vis_km", 0.0),
                avgvis_miles=current.get("vis_miles", 0.0),
                condition=current.get("condition", {}).get("text", ""),
                aqi=air_quality.get("us-epa-index"),
            )

        except requests.RequestException as e:
            print(f"[WeatherService] Error fetching weather: {e}")
            return None