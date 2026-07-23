# QA Live Platform (full-stack)

A real full-stack version of the QA automation project: a webpage where you type
in **any URL**, click **Run check**, and a Flask backend actually launches a
headless browser (or calls the API) and returns real results — not cached demo
data.

## How it's different from the other project folder

- `qa-automation-platform/` = a CLI tool + config file you run from a terminal
- `qa-live-platform/` (this one) = a website with a form; the backend runs the
  same kind of checks live, on demand, triggered by a button click

## Stack

- **Backend**: Flask (`app.py`) — receives a URL, runs Playwright/requests checks, returns JSON
- **Frontend**: `templates/index.html` — plain HTML/CSS/JS, calls the backend with `fetch()`
- **Engine**: `engine/` — the actual check logic (UI, API, performance, accessibility)
- **Storage**: `storage.py` — saves every run as a JSON file in `data/`, powers the trend chart

## Run it locally

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
playwright install
python app.py
```

Then open **http://127.0.0.1:5060** in your browser. Type in a URL, pick
"Website" or "API," click **Run check** — the result table and trend chart
update live.

## Important: this needs a real server, not GitHub Pages

GitHub Pages only serves static files — it can't run Python or launch a
browser. To make this **publicly** accessible (not just on your own laptop),
you'd need to deploy it to a host that runs real backend code, e.g. Render,
Railway, or Fly.io (all have free tiers). Playwright needs a bit of extra
setup on most hosts (installing browser binaries in their build step) —
ask if you want help with that deployment step specifically.
