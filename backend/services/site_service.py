from typing import Optional
from enums.time_visibility import TimeVisibility
from enums.site_visibility import SiteVisibility
from schemas.visibility import Visibility
from repositories.site_repo import SiteRepository
from services.visibility_service import VisibilityService
from services.light_pollution_service import LightPollutionService
from services.drive_time_service import DriveTimeService
from schemas.site import Site
from schemas.site_summary import SiteSummary

class SiteService:
    def __init__(self):
        self.site_repo = SiteRepository()
        self.lp_service = LightPollutionService()
        self.visibility_service = VisibilityService()
        self.drive_service = DriveTimeService()

    def get_all_sites(self) -> list[SiteSummary]:
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

    def get_site(self, site_id: int, time: Optional[TimeVisibility] = None) -> Site:
        r = self.site_repo.get_site(site_id)
        if not r:
            return None

        visibility = self.visibility_service.compute_visibility(r.latitude, r.longitude, time)
        return Site(
            id=r.id,
            name=r.name,
            description=r.description,
            latitude=r.latitude,
            longitude=r.longitude,
            visibility=visibility)

    def search(
        self,
        name: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        drive_time: Optional[int] = None,
        visib: Optional[SiteVisibility] = None,
        time: Optional[TimeVisibility] = None) -> list[Site]:

        polygon = None

        polygon = self.drive_service.get_drive_time_polygon(lat, lon, drive_time)

        rows = self.site_repo.search(name, polygon)
        
        sites = []

        for r in rows:
            if visib is not None:
                visibility = self.visibility_service.compute_visibility(r.latitude, r.longitude, time)
                valid = self.visibility_service.meets_visibility_threshold(visibility.score, visib)
                if valid:
                    sites.append(
                        Site(
                            id=r.id,
                            name=r.name,
                            description=r.description,
                            latitude=r.latitude,
                            longitude=r.longitude,
                            visibility=visibility
                        )
                    )
            else:
                sites.append(
                        Site(
                            id=r.id,
                            name=r.name,
                            description=r.description,
                            latitude=r.latitude,
                            longitude=r.longitude,
                            visibility=None
                        )
                    )

        return sites
