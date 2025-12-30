from models.light_pollution import LightPollution
from models.weather import Weather

class LPServiceMock:
    def get_for_location(self, lat, lon):
        return LightPollution(lp_index=0.1, mag_arcsec=21.5, lp_zone="2a", color_zone="#000000")

class WeatherServiceMock:
    def get_current_weather(self, lat, lon):
        return Weather(cloud_coverage=50, avgvis_km=10.0, avgvis_miles=6.2, condition="Clear", aqi=1)