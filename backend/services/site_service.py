from repositories.site_repo import SiteRepository
from services.light_pollution_service import LightPollutionService
from services.weather_service import WeatherService
from models.site import Site
from models.site_summary import SiteSummary

class SiteService:
    def __init__(self):
        self.site_repo = SiteRepository()
        self.lp_service = LightPollutionService()
        self.weather_service = WeatherService()

    def get_all_sites(self):
        rows = self.site_repo.get_all_sites()
        sites = []

        for r in rows:
            lp = self.lp_service.get_for_location(r.latitude, r.longitude)
            sites.append(
                SiteSummary(
                    id=r.id,
                    name=r.name,
                    description=r.description,
                    latitude=r.latitude,
                    longitude=r.longitude,
                    light_pollution=lp,
                )
            )
        return sites

    def get_site(self, site_id: int):
        r = self.site_repo.get_site(site_id)
        if not r:
            return None

        lp = self.lp_service.get_for_location(r.latitude, r.longitude)
        weather = self.weather_service.get_current_weather(r.latitude, r.longitude)
        return Site(
            id=r.id,
            name=r.name,
            description=r.description,
            latitude=r.latitude,
            longitude=r.longitude,
            light_pollution=lp,
            weather=weather
        )
