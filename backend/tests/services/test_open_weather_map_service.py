from services.open_weather_map_service import OpenWeatherMapService
from schemas.weather import Weather
from enums.time_visibility import TimeVisibility
from ..mocks.http import ResponseMock, HttpClientMock
from datetime import datetime, timezone
import pytest

FORECAST_JSON = {
    "list": [
        {
            "dt": 1700000000,
            "clouds": {"all": 60},
            "visibility": 8500,
            "weather": [{"description": "clear sky"}],
        }
    ]
}

AIR_JSON = {
    "list": [
        {
            "dt": 1700000000,
            "main": {"aqi": 1}
        }
    ]
}

class TestOpenWeatherMapService:
    @pytest.mark.asyncio
    async def test_get_forecast_weather_success(self, monkeypatch):
        # Freeze datetime helper
        fixed_dt = datetime.fromtimestamp(1700000000, tz=timezone.utc)

        monkeypatch.setattr(
            "services.open_weather_map_service.DateTimeService.date_time_helper",
            lambda self, _: fixed_dt
        )

        http_client = HttpClientMock(
            responses=[
                ResponseMock(FORECAST_JSON),
                ResponseMock(AIR_JSON),
            ]
        )

        service = OpenWeatherMapService(http_client=http_client)

        result = await service.get_forecast_weather(
            lat=48.75,
            lon=-122.48,
            time_visibility=TimeVisibility.TONIGHT
        )

        assert isinstance(result, Weather)
        assert result.cloud_coverage == 60
        assert result.avgvis_km == 8.5
        assert round(result.avgvis_miles, 2) == round(8.5 * 0.621371, 2)
        assert result.condition == "clear sky"
        assert result.aqi == 1

    @pytest.mark.asyncio
    async def test_get_forecast_weather_missing_entries(self, monkeypatch):
        fixed_dt = datetime.fromtimestamp(1700000000, tz=timezone.utc)

        monkeypatch.setattr(
            "services.open_weather_map_service.DateTimeService.date_time_helper",
            lambda self, _: fixed_dt
        )

        http_client = HttpClientMock(
            responses=[
                ResponseMock({"list": []}),
                ResponseMock({"list": []}),
            ]
        )

        service = OpenWeatherMapService(http_client=http_client)

        result = await service.get_forecast_weather(
            0.0, 0.0, TimeVisibility.TONIGHT
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_get_forecast_weather_http_error(self):
        http_client = HttpClientMock(
            responses=[
                ResponseMock({}, status_code=500)
            ]
        )

        service = OpenWeatherMapService(http_client=http_client)

        result = await service.get_forecast_weather(
            48.75, -122.48, TimeVisibility.TONIGHT
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_get_forecast_weather_network_error(self):
        http_client = HttpClientMock(should_raise=True)
        service = OpenWeatherMapService(http_client=http_client)

        result = await service.get_forecast_weather(
            48.75, -122.48, TimeVisibility.TONIGHT
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_weather_request_params(self, monkeypatch):
        fixed_dt = datetime.fromtimestamp(1700000000, tz=timezone.utc)

        monkeypatch.setattr(
            "services.open_weather_map_service.DateTimeService.date_time_helper",
            lambda self, _: fixed_dt
        )

        http_client = HttpClientMock(
            responses=[
                ResponseMock(FORECAST_JSON),
                ResponseMock(AIR_JSON),
            ]
        )

        service = OpenWeatherMapService(http_client=http_client)
        await service.get_forecast_weather(10.5, 20.5, TimeVisibility.TONIGHT)
        forecast_call = http_client.calls[0]
        assert forecast_call["params"]["lat"] == 10.5
        assert forecast_call["params"]["lon"] == 20.5
        assert forecast_call["params"]["units"] == "metric"
        assert "appid" in forecast_call["params"]
