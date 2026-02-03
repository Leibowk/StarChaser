from fastapi import Request

from repositories.site_repo import SiteRepository
from services.site_service import SiteService
from services.visibility_service import VisibilityService
from services.light_pollution_service import LightPollutionService
from services.drive_time_service import DriveTimeService
from services.open_weather_map_service import OpenWeatherMapService
from services.date_time_service import DateTimeService


def create_site_service(**overrides) -> SiteService:
    """Build the full service graph. Accepts optional keyword overrides for any dependency (for tests)."""
    date_time_service = overrides.pop("date_time_service", None) or DateTimeService()
    lp_service = overrides.pop("lp_service", None) or LightPollutionService()
    open_weather_service = overrides.pop(
        "open_weather_service",
        None
    ) or OpenWeatherMapService(date_time_service=date_time_service)
    visibility_service = overrides.pop(
        "visibility_service",
        None
    ) or VisibilityService(lp_service=lp_service, weather_service=open_weather_service)
    site_repo = overrides.pop("site_repo", None) or SiteRepository()
    drive_service = overrides.pop("drive_service", None) or DriveTimeService()

    return SiteService(
        site_repo=site_repo,
        lp_service=lp_service,
        visibility_service=visibility_service,
        drive_service=drive_service,
    )


def get_site_service(request: Request) -> SiteService:
    """FastAPI dependency. Returns the SiteService from app.state."""
    return request.app.state.site_service
