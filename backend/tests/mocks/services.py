from enums.site_visibility import SiteVisibility
from schemas.visibility import Visibility
from schemas.light_pollution import LightPollution
from schemas.weather import Weather

class LPServiceMock:
    def get_for_location(self, lat, lon):
        return LightPollution(lp_index=0.1, mag_arcsec=21.5, lp_zone="2a", color_zone="#000000")

class WeatherApiServiceMock:
    def get_current_weather(self, lat, lon):
        return Weather(cloud_coverage=50, avgvis_km=10.0, avgvis_miles=6.2, condition="Clear", aqi=1)
    
class OpenWeatherMapServiceMock:
    async def get_forecast_weather(self, lat, lon, time_visibility=None):
        return Weather(
            cloud_coverage=10,      # %
            avgvis_km=12.0,         # km
            avgvis_miles=7.46,
            condition="Clear",
            aqi=25,                 # good air quality
        )
    
class VisibilityServiceMock:
    async def compute_visibility(self, lat, long, time_visibility) -> Visibility:
        return Visibility(
            score=0.85,
            category=SiteVisibility.Great,
            light_pollution=LightPollution(
                lp_index=0.1,
                mag_arcsec=21.5,
                lp_zone="2a",
                color_zone="#000000",
            ),
            weather=Weather(
                cloud_coverage=50,
                avgvis_km=10.0,
                avgvis_miles=6.2,
                condition="Clear",
                aqi=1,
            ))