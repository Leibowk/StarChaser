"""Geographic utilities for map viewport calculations."""

import math


def zoom_to_bbox(lat: float, lon: float, zoom: int) -> tuple[float, float, float, float]:
    """
    Compute geographic bounding box from center (lat, lon) and zoom level.
    Web Mercator: at zoom Z, lon_span = 360 / 2^Z.
    Returns (min_lat, min_lon, max_lat, max_lon).
    """
    n = 2.0 ** zoom
    lon_span = 360.0 / n
    # Latitude: approximate; at equator lat_span ~ 180/n
    lat_span = 180.0 / n
    min_lon = lon - lon_span / 2
    max_lon = lon + lon_span / 2
    min_lat = lat - lat_span / 2
    max_lat = lat + lat_span / 2
    return (min_lat, min_lon, max_lat, max_lon)


def zoom_to_polygon_geojson(lat: float, lon: float, zoom: int) -> dict:
    """
    Compute GeoJSON polygon for viewport at center (lat, lon) and zoom.
    Returns a dict suitable for ST_GeomFromGeoJSON (GeoJSON geometry).
    """
    min_lat, min_lon, max_lat, max_lon = zoom_to_bbox(lat, lon, zoom)
    # GeoJSON: [[min_lon, min_lat], [max_lon, min_lat], [max_lon, max_lat], [min_lon, max_lat], [min_lon, min_lat]]
    return {
        "type": "Polygon",
        "coordinates": [[
            [min_lon, min_lat],
            [max_lon, min_lat],
            [max_lon, max_lat],
            [min_lon, max_lat],
            [min_lon, min_lat],
        ]],
    }
