import pytest
import pytest_asyncio
from services.site_service import SiteService
from schemas.site import Site
from schemas.site_summary import SiteSummary
from ..mocks.services import LPServiceMock, WeatherApiServiceMock, VisibilityServiceMock
from ..mocks.repos import SiteRepoMock
from enums.time_visibility import TimeVisibility

@pytest_asyncio.fixture
async def site_service():
    svc = SiteService()
    svc.visibility_service = VisibilityServiceMock()
    svc.site_repo = SiteRepoMock()
    svc.lp_service = LPServiceMock()
    svc.weather_service = WeatherApiServiceMock()
    return svc

@pytest.mark.asyncio
async def test_get_all_sites(site_service):
    sites = await site_service.get_all_sites()
    assert len(sites) == 2
    for s in sites:
        assert isinstance(s, SiteSummary)
        assert s.light_pollution.lp_zone == "2a"


@pytest.mark.asyncio
async def test_get_site_exists(site_service):
    site = await site_service.get_site(1, TimeVisibility.TONIGHT)
    assert isinstance(site, Site)
    assert site.id == 1
    assert site.visibility.light_pollution.lp_zone == "2a"
    assert site.visibility.weather.condition == "Clear"

@pytest.mark.asyncio
async def test_get_site_missing(site_service):
    site = await site_service.get_site(999, TimeVisibility.TONIGHT)
    assert site is None
