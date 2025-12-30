

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
        # Default assumptions if data missing
        lp_score = 1.0
        cloud_score = 1.0

        if lp:
            # assume lp.lp_index where higher = worse
            lp_score = max(0.0, 1.0 - min(lp.lp_index / 5.0, 1.0))

        if weather:
            cloud_score = max(0.0, 1.0 - weather.cloud_coverage / 100.0)

        score = round(0.7 * lp_score + 0.3 * cloud_score, 3)

        category = self.category_from_score(score)

        return Visibility(
            score=score,
            category=category,
            light_pollution=lp,
            weather=weather,
        )
    
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