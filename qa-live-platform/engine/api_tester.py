import time

import requests


class APITester:
    """Generic API checks: status code and response time, run live against a submitted URL."""

    def __init__(self):
        self.results = []

    def _record(self, name, passed, detail=""):
        self.results.append({"check": name, "passed": passed, "detail": str(detail)})

    def check_status(self, url, expected_status=200, method="GET"):
        start = time.time()
        try:
            resp = requests.request(method, url, timeout=10)
            elapsed = round(time.time() - start, 3)
            passed = resp.status_code == expected_status
            self._record(
                "api_status",
                passed,
                f"status={resp.status_code}, expected={expected_status}, time={elapsed}s",
            )
            return resp, elapsed
        except Exception as e:
            self._record("api_status", False, e)
            return None, None

    def check_response_time(self, elapsed, max_seconds=2.0):
        passed = elapsed is not None and elapsed <= max_seconds
        self._record("api_response_time", passed, f"elapsed={elapsed}s, max={max_seconds}s")
        return passed

    def get_results(self):
        return self.results
