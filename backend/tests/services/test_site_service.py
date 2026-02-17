import pytest
import pytest_asyncio
from datetime import date
from services.site_service import SiteService
from schemas.site import Site
from ..mocks.services import LPServiceMock, VisibilityServiceMock
from ..mocks.repos import SiteRepoMock
from enums.time_visibility import TimeVisibility

@pytest_asyncio.fixture
async def site_service():
    return SiteService(
        site_repo=SiteRepoMock(),
        visibility_service=VisibilityServiceMock(),
        lp_service=LPServiceMock(),
    )

@pytest.mark.asyncio
async def test_get_sites(site_service):
    night_date = date.today()
    sites = await site_service.get_sites(lat=48.75, lon=-122.52, zoom=9, limit=50, day=night_date)
    assert len(sites) == 2
    for s in sites:
        assert isinstance(s, Site)
        assert s.visibility is not None
        assert s.visibility.light_pollution.lp_zone == "2a"


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
