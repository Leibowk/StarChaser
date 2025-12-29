from repositories.site_repo import SiteRepository
from services.light_pollution_service import LightPollutionService
from models.site import Site

class SiteService:
    def __init__(self):
        self.site_repo = SiteRepository()
        self.lp_service = LightPollutionService()

    def get_all_sites(self):
        rows = self.site_repo.get_all_sites()
        sites = []

        for r in rows:
            lp = self.lp_service.get_for_location(r.latitude, r.longitude)
            sites.append(
                Site(
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
        return Site(
            id=r.id,
            name=r.name,
            description=r.description,
            latitude=r.latitude,
            longitude=r.longitude,
            light_pollution=lp,
        )
