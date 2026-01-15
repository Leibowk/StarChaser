import math
import pytest
import numpy as np
from unittest.mock import patch, mock_open
from services.light_pollution_service import LightPollutionService
from schemas.light_pollution import LightPollution

@pytest.fixture
def lp_service():
    return LightPollutionService()

@patch("gzip.open")
@patch("pathlib.Path.exists", return_value=True)
@patch("numpy.frombuffer")
def test_get_for_location_returns_lp(mock_frombuffer, mock_exists, mock_gzip, lp_service):
    # Arrange
    mock_frombuffer.return_value = np.zeros(600*600, dtype=np.int8)
    
    # Act
    result = lp_service.get_for_location(48.75, -122.48)
    
    # Assert
    assert result is not None
    assert isinstance(result, LightPollution)
    assert result.lp_index >= 0
    assert result.mag_arcsec >= 0
    assert result.lp_zone is not None
    assert result.color_zone.startswith("rgba")

@patch("pathlib.Path.exists", return_value=False)
def test_get_for_location_tile_missing(mock_exists, lp_service):
    # If tile does not exist, returns None
    result = lp_service.get_for_location(48.75, -122.48)
    assert result is None

def test_zone_from_ratio(lp_service):
    # Very low ratio
    zone, color = lp_service._zone_from_ratio(0.005)
    assert zone == "0"
    assert color.startswith("rgba")

    # Very high ratio
    zone, color = lp_service._zone_from_ratio(50)
    assert zone == "7b"
    assert color.startswith("rgba")