import pytest
from backend.services.visibility_service import VisibilityService
from ..mocks.services import LPServiceMock, OpenWeatherMapServiceMock
from enums.site_visibility import SiteVisibility
from enums.time_visibility import TimeVisibility
from schemas.visibility import Visibility
from schemas.light_pollution import LightPollution
from schemas.weather import Weather


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def visibility_service():
    svc = VisibilityService()
    svc.lp_service = LPServiceMock()
    svc.weather_service = OpenWeatherMapServiceMock()
    return svc


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_compute_visibility_returns_visibility(visibility_service):
    result = await visibility_service.compute_visibility(
        lat=48.75,
        long=-122.48,
        time_visibility=TimeVisibility.TONIGHT
    )

    assert isinstance(result, Visibility)
    assert result.light_pollution.lp_zone == "2a"
    assert result.weather.condition == "Clear"
    assert 0 <= result.score <= 100
    assert isinstance(result.category, SiteVisibility)


# ---------------------------------------------------------------------------
# Score calculation
# ---------------------------------------------------------------------------

def test_compute_score_reasonable_conditions(visibility_service):
    lp = LightPollution(lp_index=0.1, mag_arcsec=21.5, lp_zone="2a", color_zone="#000000")

    weather = Weather(
        cloud_coverage=10,
        avgvis_km=12,
        avgvis_miles=7.46,
        condition="Clear",
        aqi=25,
    )

    score = visibility_service.compute_score(lp, weather)

    assert 0 <= score <= 100


def test_compute_score_never_negative(visibility_service):
    lp = LightPollution(lp_index=0.1, mag_arcsec=21.5, lp_zone="2a", color_zone="#000000")

    weather = Weather(
        cloud_coverage=100,
        avgvis_km=0,
        avgvis_miles=0,
        condition="Overcast",
        aqi=500,
    )

    score = visibility_service.compute_score(lp, weather)

    assert score == 0


# ---------------------------------------------------------------------------
# AQI factor
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "aqi,expected",
    [
        (25, 1.0),
        (75, 0.8),
        (125, 0.6),
        (175, 0.3),
        (250, 0.1),
        (400, 0.0),
    ],
)
def test_aqi_factor(aqi, expected):
    assert VisibilityService.aqi_factor(aqi) == expected


# ---------------------------------------------------------------------------
# Category mapping
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "score,expected",
    [
        (99, SiteVisibility.Perfect),
        (95, SiteVisibility.Amazing),
        (85, SiteVisibility.Great),
        (65, SiteVisibility.Good),
        (55, SiteVisibility.Ok),
        (35, SiteVisibility.Bad),
        (10, SiteVisibility.Terrible),
    ],
)
def test_category_from_score(score, expected):
    assert VisibilityService.category_from_score(score) == expected


# ---------------------------------------------------------------------------
# Threshold logic
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "score,min_category,expected",
    [
        (99, SiteVisibility.Perfect, True),
        (90, SiteVisibility.Amazing, True),
        (89, SiteVisibility.Amazing, False),
        (80, SiteVisibility.Great, True),
        (79, SiteVisibility.Great, False),
        (60, SiteVisibility.Good, True),
        (59, SiteVisibility.Good, False),
        (50, SiteVisibility.Ok, True),
        (49, SiteVisibility.Ok, False),
        (30, SiteVisibility.Bad, True),
        (29, SiteVisibility.Bad, False),
        (0, SiteVisibility.Terrible, True),
    ],
)
def test_meets_visibility_threshold(score, min_category, expected):
    assert VisibilityService.meets_visibility_threshold(score, min_category) is expected
