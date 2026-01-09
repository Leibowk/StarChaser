import json
from typing import Optional
from enums.time_visibility import TimeVisibility
from enums.site_visibility import SiteVisibility
from models.visibility import Visibility
from repositories.site_repo import SiteRepository
from services.visibility_service import VisibilityService
from services.light_pollution_service import LightPollutionService
from services.drive_time_service import DriveTimeService
from models.site import Site
from models.site_summary import SiteSummary
from shapely.geometry import mapping

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
        radius_km: Optional[float] = None,
        drive_time: Optional[int] = None,
        visib: Optional[SiteVisibility] = None,
        time: Optional[TimeVisibility] = None) -> list[Site]:

        polygon = None

        if drive_time is not None:
            if lat is None or lon is None:
                raise ValueError("lat/lon required when using drive_time")

            if radius_km is not None:
                raise ValueError("Use either radius_km or drive_time, not both")

            polygon = self.drive_service.get_drive_time_polygon(lat, lon, drive_time)

        polygon_geojson = None

        if polygon is not None:
            polygon_geojson = polygon_geojson = json.dumps(mapping(polygon))

        rows = self.site_repo.search(name, lat, lon, radius_km, polygon_geojson)
        
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
