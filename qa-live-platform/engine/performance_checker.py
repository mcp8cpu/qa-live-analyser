class PerformanceChecker:
    """Reads real browser Navigation Timing data for whatever page was just loaded."""

    def __init__(self, page, max_load_ms=5000):
        self.page = page
        self.max_load_ms = max_load_ms
        self.results = []

    def measure(self):
        try:
            timing = self.page.evaluate(
                """() => {
                    const t = performance.timing;
                    return {
                        dns_ms: t.domainLookupEnd - t.domainLookupStart,
                        tcp_ms: t.connectEnd - t.connectStart,
                        ttfb_ms: t.responseStart - t.requestStart,
                        dom_load_ms: t.domContentLoadedEventEnd - t.navigationStart,
                        full_load_ms: t.loadEventEnd - t.navigationStart
                    };
                }"""
            )
            passed = timing["full_load_ms"] < self.max_load_ms
            self.results.append({"check": "performance", "passed": passed, "detail": str(timing)})
            return passed, timing
        except Exception as e:
            self.results.append({"check": "performance", "passed": False, "detail": str(e)})
            return False, {}

    def get_results(self):
        return self.results
