import time

import requests
from bs4 import BeautifulSoup


class UITester:
    """Generic UI checks that work against any URL submitted through the live form."""

    def __init__(self, page):
        self.page = page
        self.results = []

    def _record(self, name, passed, detail=""):
        self.results.append({"check": name, "passed": passed, "detail": str(detail)})

    def load_page(self, url, timeout=15000):
        start = time.time()
        try:
            response = self.page.goto(url, timeout=timeout, wait_until="load")
            load_time = round(time.time() - start, 2)
            status_ok = response is not None and response.status < 400
            self._record(
                "page_load",
                status_ok,
                f"status={response.status if response else 'none'}, time={load_time}s",
            )
            return status_ok
        except Exception as e:
            self._record("page_load", False, e)
            return False

    def check_title(self):
        title = self.page.title()
        self._record("title_check", bool(title), f"title='{title}'")
        return bool(title)

    def check_broken_links(self, max_links=20):
        html = self.page.content()
        soup = BeautifulSoup(html, "html.parser")
        links = [a.get("href") for a in soup.find_all("a", href=True)]
        links = [link for link in links if link.startswith("http")][:max_links]
        broken = []
        for link in links:
            try:
                r = requests.head(link, timeout=5, allow_redirects=True)
                if r.status_code >= 400:
                    broken.append((link, r.status_code))
            except Exception as e:
                broken.append((link, str(e)))
        passed = len(broken) == 0
        self._record("broken_links", passed, f"checked={len(links)}, broken={broken}")
        return passed

    def check_forms_present(self):
        forms = self.page.query_selector_all("form")
        self._record("forms_present", True, f"forms_found={len(forms)}")
        return len(forms) > 0

    def get_results(self):
        return self.results
