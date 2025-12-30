class FakeResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise FakeHttpClient.RequestException(f"{self.status_code} error")


class FakeHttpClient:
    class RequestException(Exception):
        pass

    def __init__(self, response=None, should_raise=False):
        self.response = response
        self.should_raise = should_raise
        self.last_request = None

    def get(self, url, params=None, timeout=None):
        self.last_request = {
            "url": url,
            "params": params,
            "timeout": timeout,
        }

        if self.should_raise:
            raise FakeHttpClient.RequestException("Network error")

        return self.response