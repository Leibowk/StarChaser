

from models.light_pollution import LightPollution
from models.weather import Weather
from enums.site_visibility import SiteVisibility
from models.visibility import Visibility
from services.light_pollution_service import LightPollutionService
from services.weather_service import WeatherService


class VisibilityService:
    def __init__(self):
        self.lp_service = LightPollutionService()
        self.weather_service = WeatherService()

    def compute_visibility(self, lat, long) -> Visibility:

        lp = self.lp_service.get_for_location(lat, long)
        weather = self.weather_service.get_current_weather(lat, long)
        
        score = self.compute_score(lp, weather)

        category = self.category_from_score(score)

        return Visibility(
            score=score,
            category=category,
            light_pollution=lp,
            weather=weather,
        )
    
    def compute_score(self, lp: LightPollution, weather: Weather):
        lp_factor = lp.lp_index/47
        cloud_factor = weather.cloud_coverage/100
        aqi = 1-self.aqi_factor(weather.aqi)
        score = 1-lp_factor - cloud_factor - aqi
        if score < 0:
            score = 0
        return score
    
    @staticmethod
    def aqi_factor(aqi: float) -> float:
        if aqi <= 50:
            return 1.0
        elif aqi <= 100:
            return 0.8
        elif aqi <= 150:
            return 0.6
        elif aqi <= 200:
            return 0.3
        elif aqi <= 300:
            return 0.1
        else:
            return 0.0
        
    @staticmethod
    def category_from_score(score: float) -> SiteVisibility:
        match score:
            case s if s >= 0.95:
                return SiteVisibility.Perfect
            case s if s >= 0.80:
                return SiteVisibility.Great
            case s if s >= 0.60:
                return SiteVisibility.Good
            case s if s >= 0.50:
                return SiteVisibility.Ok
            case s if s >= 0.30:
                return SiteVisibility.Bad
            case _:
                return SiteVisibility.Terrible

    @staticmethod      
    def meets_visibility_threshold(score: float, min_category: SiteVisibility) -> bool:
        """
        Returns True if the score meets or exceeds the threshold defined by min_category.
        """
        thresholds = {
            SiteVisibility.Perfect: 0.95,
            SiteVisibility.Great:   0.80,
            SiteVisibility.Good:    0.60,
            SiteVisibility.Ok:      0.50,
            SiteVisibility.Bad:     0.30,
            SiteVisibility.Terrible:0.0,
        }

        min_score = thresholds[min_category]
        return score >= min_score