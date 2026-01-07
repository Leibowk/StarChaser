from datetime import datetime, time, timedelta
import requests
from typing import Optional
from enums.time_visibility import TimeVisibility
from config import settings
from models.weather import Weather


class WeatherService:
    def __init__(self, http_client=requests):
        self.http_client = http_client
        self.base_url = settings.WEATHER.URL
        self.api_key = settings.WEATHER.API_KEY
        self.timeout = 5  # seconds

    def get_forecast_weather(self, lat: float, lon: float, time_visibility: Optional[TimeVisibility]) -> Optional[Weather]:
        """
        Fetches forecast weather for a lat/lon and returns a Weather model.
        """
        daytime = date_time_helper(time_visibility)

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
            print(f"[WeatherService] Error fetching weather: {e}")
            return None
        
    
def date_time_helper(time_visibility: Optional[TimeVisibility]) -> datetime:
    """
    Returns a datetime object based on the TimeVisibility enum.
    
    Rules:
    - None -> tonight at 10 PM
    - NOW -> forecast datetime
    - TONIGHT -> today at 10 PM
    - TOMORROW_NIGHT -> tomorrow at 10 PM
    - NIGHTS_3_FROM_NOW -> 3 nights from today at 10 PM
    """
    now = datetime.now()
    target_time = time(22, 0)  # 10:00 PM

    if time_visibility is None:
        # Default to tonight at 10 PM
        return datetime.combine(now.date(), target_time)
    
    if time_visibility == TimeVisibility.NOW:
        return now

    if time_visibility == TimeVisibility.TONIGHT:
        return datetime.combine(now.date(), target_time)

    if time_visibility == TimeVisibility.TOMORROW_NIGHT:
        tomorrow = now.date() + timedelta(days=1)
        return datetime.combine(tomorrow, target_time)

    if time_visibility == TimeVisibility.NIGHTS_3_FROM_NOW:
        three_nights = now.date() + timedelta(days=3)
        return datetime.combine(three_nights, target_time)

    # fallback just in case
    return datetime.combine(now.date(), target_time)