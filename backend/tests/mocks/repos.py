class SiteRepoMock:
    async def get_all_sites(self):
        return [
            type("Row", (), {"id": 1, "name": "Site A", "description": "Desc A", "latitude": 48.0, "longitude": -122.0})(),
            type("Row", (), {"id": 2, "name": "Site B", "description": "Desc B", "latitude": 49.0, "longitude": -123.0})(),
        ]

    async def get_site(self, site_id):
        if site_id == 1:
            return type("Row", (), {"id": 1, "name": "Site A", "description": "Desc A", "latitude": 48.0, "longitude": -122.0})()
        return None

    async def get_visibility(self, site_id, night_date):
        # Return a mock visibility record or None
        return None