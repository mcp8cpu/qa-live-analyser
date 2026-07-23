import json
import time
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def save_run(target_name, url, check_type, results):
    timestamp = int(time.time())
    passed = sum(1 for r in results if r["passed"])
    failed = len(results) - passed

    run_data = {
        "target": target_name,
        "url": url,
        "type": check_type,
        "timestamp": timestamp,
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "results": results,
    }

    path = DATA_DIR / f"run_{timestamp}.json"
    with open(path, "w") as f:
        json.dump(run_data, f, indent=2)

    return run_data


def load_all_runs():
    runs = []
    for f in sorted(DATA_DIR.glob("run_*.json")):
        with open(f) as fh:
            runs.append(json.load(fh))
    return runs
