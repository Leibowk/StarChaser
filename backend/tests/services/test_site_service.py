import pytest
from services.site_service import SiteService
from models.site import Site
from models.site_summary import SiteSummary
from tests.mocks.services import LPServiceMock, WeatherServiceMock, VisibilityServiceMock
from tests.mocks.repos import SiteRepoMock

@pytest.fixture
def site_service():
    svc = SiteService()
    svc.visibility_service = VisibilityServiceMock()
    svc.site_repo = SiteRepoMock()
    svc.lp_service = LPServiceMock()
    svc.weather_service = WeatherServiceMock()
    return svc

def test_get_all_sites(site_service):
    sites = site_service.get_all_sites()
    assert len(sites) == 2
    for s in sites:
        assert isinstance(s, SiteSummary)
        assert s.light_pollution.lp_zone == "2a"

def test_get_site_exists(site_service):
    site = site_service.get_site(1)
    assert isinstance(site, Site)
    assert site.id == 1
    assert site.visibility.light_pollution.lp_zone == "2a"
    assert site.visibility.weather.condition == "Clear"

def test_get_site_missing(site_service):
    site = site_service.get_site(999)
    assert site is None
