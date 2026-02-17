def _make_site_row(id, name, desc, lat, lon, score=85, weather=None, lp=None):
    return type("Row", (), {
        "id": id, "name": name, "description": desc,
        "latitude": lat, "longitude": lon,
        "score": score,
        "weather": weather or {"cloud_coverage": 10, "avgvis_km": 12.0, "avgvis_miles": 7.46, "condition": "Clear", "aqi": 25},
        "light_pollution": lp or {"lp_index": 0.1, "mag_arcsec": 21.5, "lp_zone": "2a", "color_zone": "#000000"},
    })()


class SiteRepoMock:
    async def get_all_sites(self):
        return [
            type("Row", (), {"id": 1, "name": "Site A", "description": "Desc A", "latitude": 48.0, "longitude": -122.0})(),
            type("Row", (), {"id": 2, "name": "Site B", "description": "Desc B", "latitude": 49.0, "longitude": -123.0})(),
        ]

    async def get_sites(self, lat, lon, search_polygon, limit, date):
        return [
            _make_site_row(1, "Site A", "Desc A", 48.0, -122.0),
            _make_site_row(2, "Site B", "Desc B", 49.0, -123.0),
        ][:limit]

    async def get_site(self, site_id):
        if site_id == 1:
            return type("Row", (), {"id": 1, "name": "Site A", "description": "Desc A", "latitude": 48.0, "longitude": -122.0})()
        return None

    async def get_visibility(self, site_id, night_date):
        # Return a mock visibility record or None
        return None