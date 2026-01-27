from datetime import date, timedelta
from typing import Optional
from schemas.light_pollution import LightPollution
from schemas.weather import Weather
from enums.time_visibility import TimeVisibility
from enums.site_visibility import SiteVisibility
from schemas.visibility import Visibility
from repositories.site_repo import SiteRepository
from services.visibility_service import VisibilityService
from services.light_pollution_service import LightPollutionService
from services.drive_time_service import DriveTimeService
from schemas.site import Site
from schemas.site_summary import SiteSummary
import logging
import time

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

    def get_site(self, site_id: int, time: TimeVisibility) -> Site:
        r = self.site_repo.get_site(site_id)
        if not r:
            return None

        night_date = self.resolve_night_date(time)
        vis_record = self.site_repo.get_visibility(site_id, night_date)
        if vis_record:
            visibility = Visibility(
                score=vis_record.score,
                category=VisibilityService.category_from_score(vis_record.score),
                weather=Weather(**vis_record.weather) if vis_record.weather else None,
                light_pollution=LightPollution(**vis_record.light_pollution) if vis_record.light_pollution else None
                )
        else:
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
        visib: SiteVisibility,
        time: TimeVisibility,
        name: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        drive_time: Optional[int] = None
        ) -> list[Site]:

        polygon = None

        if drive_time is not None:
            polygon = self.drive_service.get_drive_time_polygon(lat, lon, drive_time)

        night_date = self.resolve_night_date(time)
        min_score = self.visibility_service.score_from_category(visib)            

        rows = self.site_repo.search(name, polygon, night_date, min_score)
        sites = []
        for r in rows:
            visibility = Visibility(
                score=r.score,
                category=VisibilityService.category_from_score(r.score),
                weather=Weather(**r.weather) if r.weather else None,
                light_pollution=LightPollution(**r.light_pollution) if r.light_pollution else None
            )
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

        return sites
    
    def precompute_visibility(self, time_buckets):
        logger = logging.getLogger(__name__)
        sites = self.site_repo.get_all_sites()
        total_sites = len(sites)
        logger.info(f"Starting precompute for {total_sites} sites and {len(time_buckets)} time buckets")

        records = []
        processed = 0

        for i, s in enumerate(sites):
            try:
                visibilities = self.visibility_service.compute_visibilities(s.latitude, s.longitude, time_buckets)
                for t in time_buckets:
                    visibility = visibilities.get(t)
                    if visibility:
                        night_date = self.resolve_night_date(t)
                        records.append(
                            {
                                "site_id": s.id,
                                "date": night_date,
                                "score": visibility.score,
                                "weather": visibility.weather.model_dump() if visibility.weather else None,
                                "light_pollution": visibility.light_pollution.model_dump() if visibility.light_pollution else None
                            }
                        )
                        processed += 1
                time.sleep(0.1)  # Small delay to avoid rate limits
            except Exception as e:
                logger.error(f"Failed to compute visibility for site {s.id}: {e}")
                continue
            if (i + 1) % 10 == 0:  # Log every 10 sites
                logger.info(f"Processed {i + 1}/{total_sites} sites")

        logger.info(f"Computed {processed} visibility records, upserting to DB")
        self.site_repo.upsert_visibility(records)
        logger.info("Precompute visibility completed")

    @staticmethod
    def resolve_night_date(bucket: TimeVisibility) -> date:
        today = date.today()

        return {
            TimeVisibility.TONIGHT: today,
            TimeVisibility.TOMORROW_NIGHT: today + timedelta(days=1),
            TimeVisibility.NIGHTS_3_FROM_NOW: today + timedelta(days=2),
        }[bucket]
                


