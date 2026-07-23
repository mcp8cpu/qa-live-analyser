class AccessibilityChecker:
    """Runs axe-core against whatever page is currently loaded in the live check."""

    AXE_CDN = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.1/axe.min.js"
    IMPACT_ORDER = ["minor", "moderate", "serious", "critical"]

    def __init__(self, page, fail_on_impact="serious"):
        self.page = page
        self.fail_on_impact = fail_on_impact
        self.results = []

    def run(self):
        try:
            self.page.add_script_tag(url=self.AXE_CDN)
            axe_results = self.page.evaluate("async () => await axe.run()")
            violations = axe_results.get("violations", [])

            threshold_index = self.IMPACT_ORDER.index(self.fail_on_impact)
            blocking = [
                v for v in violations
                if self.IMPACT_ORDER.index(v.get("impact", "minor")) >= threshold_index
            ]
            passed = len(blocking) == 0

            summary = [
                {"id": v["id"], "impact": v["impact"], "nodes_affected": len(v["nodes"])}
                for v in violations
            ]
            label = f"blocking={len(blocking)}, total_violations={len(violations)}, details={summary}"
            self.results.append({"check": "accessibility", "passed": passed, "detail": label})
            return passed, summary
        except Exception as e:
            self.results.append({"check": "accessibility", "passed": False, "detail": str(e)})
            return False, []

    def get_results(self):
        return self.results
