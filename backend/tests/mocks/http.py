class ResponseMock:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    async def json(self):
        return self._json_data

    def json_sync(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise HttpClientMock.RequestException(f"{self.status_code} error")


class HttpClientMock:
    def __init__(self, responses=None, should_raise=False):
        self.responses = responses or []
        self.should_raise = should_raise
        self.calls = []

    async def get(self, url, params=None, timeout=None):
        if self.should_raise:
            raise Exception("Network error")

        self.calls.append({
            "url": url,
            "params": params,
            "timeout": timeout,
        })

        if not self.responses:
            raise Exception("No more mock responses")

        resp = self.responses.pop(0)
        # Patch for compatibility: mimic httpx.Response interface
        resp.json = resp.json_sync
        return resp