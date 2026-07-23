import re

from flask import Flask, jsonify, render_template, request

import storage
from engine.accessibility_checker import AccessibilityChecker
from engine.api_tester import APITester
from engine.browser_manager import BrowserManager
from engine.performance_checker import PerformanceChecker
from engine.ui_tester import UITester

app = Flask(__name__)


def run_web_check(url):
    bm = BrowserManager(headless=True)
    page = bm.start()
    all_results = []
    try:
        ui = UITester(page)
        loaded = ui.load_page(url)
        if loaded:
            ui.check_title()
            ui.check_forms_present()
            ui.check_broken_links()
        all_results.extend(ui.get_results())

        if loaded:
            perf = PerformanceChecker(page)
            perf.measure()
            all_results.extend(perf.get_results())

            acc = AccessibilityChecker(page)
            acc.run()
            all_results.extend(acc.get_results())
    finally:
        bm.stop()
    return all_results


def run_api_check(url):
    api = APITester()
    resp, elapsed = api.check_status(url)
    if resp is not None:
        api.check_response_time(elapsed)
    return api.get_results()


def name_from_url(url):
    cleaned = re.sub(r"^https?://", "", url)
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", cleaned).strip("_")
    return cleaned[:40] or "target"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/run", methods=["POST"])
def api_run():
    data = request.get_json(force=True) or {}
    url = (data.get("url") or "").strip()
    check_type = data.get("type", "web")

    if not url.startswith("http://") and not url.startswith("https://"):
        return jsonify({"error": "URL must start with http:// or https://"}), 400

    try:
        if check_type == "api":
            results = run_api_check(url)
        else:
            results = run_web_check(url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    target_name = name_from_url(url)
    run_data = storage.save_run(target_name, url, check_type, results)
    return jsonify(run_data)


@app.route("/api/history")
def api_history():
    runs = storage.load_all_runs()
    return jsonify(runs[-30:])


if __name__ == "__main__":
    app.run(debug=True, port=5000)
