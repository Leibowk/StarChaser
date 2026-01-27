

from typing import Optional
from enums.time_visibility import TimeVisibility
from schemas.light_pollution import LightPollution
from schemas.weather import Weather
from enums.site_visibility import SiteVisibility
from schemas.visibility import Visibility
from services.light_pollution_service import LightPollutionService
from services.open_weather_map_service import OpenWeatherMapService


class VisibilityService:
    def __init__(self):
        self.lp_service = LightPollutionService()
        self.weather_service = OpenWeatherMapService()

    VISIBILITY_THRESHOLDS = {
        SiteVisibility.Perfect: 99,
        SiteVisibility.Amazing: 90,
        SiteVisibility.Great: 80,
        SiteVisibility.Good: 60,
        SiteVisibility.Ok: 50,
        SiteVisibility.Bad: 30,
        SiteVisibility.Terrible: 0
    }

    def compute_visibility(self, lat, long, time_visibility: Optional[TimeVisibility] = None) -> Visibility:

        lp = self.lp_service.get_for_location(lat, long)
        weather = self.weather_service.get_forecast_weather(lat, long, time_visibility)
        
        score = self.compute_score(lp, weather)

        category = self.category_from_score(score)

        return Visibility(
            score=score,
            category=category,
            light_pollution=lp,
            weather=weather,
        )

    def compute_visibilities(self, lat, long, times: list[TimeVisibility]) -> dict[TimeVisibility, Visibility]:
        lp = self.lp_service.get_for_location(lat, long)
        weathers = self.weather_service.get_forecast_weathers(lat, long, times)

        result = {}
        for t in times:
            weather = weathers.get(t)
            if weather:
                score = self.compute_score(lp, weather)
                category = self.category_from_score(score)
                result[t] = Visibility(
                    score=score,
                    category=category,
                    light_pollution=lp,
                    weather=weather,
                )
            else:
                result[t] = None
        return result
    
    def compute_score(self, lp: LightPollution, weather: Weather):
        lp_factor = lp.lp_index/47
        cloud_factor = weather.cloud_coverage/100
        aqi = 1-self.aqi_factor(weather.aqi)
        effective_vis = min(weather.avgvis_km, 15)
        vis_distance = 1 - (effective_vis / 15)
        score = 1-lp_factor - cloud_factor - aqi - (vis_distance * 0.15)
        if score < 0:
            score = 0
        return score*100
    
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
            case s if s >= 99:
                return SiteVisibility.Perfect
            case s if s >= 90:
                return SiteVisibility.Amazing
            case s if s >= 80:
                return SiteVisibility.Great
            case s if s >= 60:
                return SiteVisibility.Good
            case s if s >= 50:
                return SiteVisibility.Ok
            case s if s >= 30:
                return SiteVisibility.Bad
            case _:
                return SiteVisibility.Terrible
    
    def score_from_category(self, category: Optional[SiteVisibility] = None) -> int:
        if category == None:
            return 0
        
        return self.VISIBILITY_THRESHOLDS[category]

    @staticmethod      
    def meets_visibility_threshold(score: float, min_category: SiteVisibility) -> bool:
        """
        Returns True if the score meets or exceeds the threshold defined by min_category.
        """
        thresholds = {
            SiteVisibility.Perfect: 99,
            SiteVisibility.Amazing: 90,
            SiteVisibility.Great:   80,
            SiteVisibility.Good:    60,
            SiteVisibility.Ok:      50,
            SiteVisibility.Bad:     30,
            SiteVisibility.Terrible:0.0,
        }

        min_score = thresholds[min_category]
        return score >= min_score