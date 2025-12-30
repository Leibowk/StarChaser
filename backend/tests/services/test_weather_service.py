import requests
from services.weather_service import WeatherService
from models.weather import Weather
from tests.mocks.http import ResponseMock, HttpClientMock

class TestWeatherService:
    def test_get_current_weather_success(self):
        fake_response = ResponseMock({
            "current": {
                "cloud": 60,
                "vis_km": 8.5,
                "vis_miles": 5.3,
                "condition": {"text": "Clear"},
                "air_quality": {"us-epa-index": 1},
            }
        })

        http_client = HttpClientMock(response=fake_response)
        service = WeatherService(http_client=http_client)

        result = service.get_current_weather(48.75, -122.48)

        assert isinstance(result, Weather)
        assert result.cloud_coverage == 60
        assert result.avgvis_km == 8.5
        assert result.avgvis_miles == 5.3
        assert result.condition == "Clear"
        assert result.aqi == 1

    def test_get_current_weather_missing_fields(self):
        fake_response = ResponseMock({
            "current": {}
        })

        http_client = HttpClientMock(response=fake_response)
        service = WeatherService(http_client=http_client)

        result = service.get_current_weather(0.0, 0.0)

        assert isinstance(result, Weather)
        assert result.cloud_coverage == 0
        assert result.avgvis_km == 0.0
        assert result.avgvis_miles == 0.0
        assert result.condition == ""
        assert result.aqi is None

    def test_get_current_weather_http_error(self):
        fake_response = ResponseMock({}, status_code=500)

        http_client = HttpClientMock(response=fake_response)
        service = WeatherService(http_client=http_client)

        result = service.get_current_weather(48.75, -122.48)

        assert result is None

    def test_get_current_weather_network_error(self):
        http_client = HttpClientMock(should_raise=True)
        service = WeatherService(http_client=http_client)

        result = service.get_current_weather(48.75, -122.48)

        assert result is None

    def test_weather_request_params(self):
        fake_response = ResponseMock({"current": {}})
        http_client = HttpClientMock(response=fake_response)

        service = WeatherService(http_client=http_client)
        service.get_current_weather(10.5, 20.5)

        params = http_client.last_request["params"]

        assert params["q"] == "10.5,20.5"
        assert params["aqi"] == "yes"
        assert "key" in params