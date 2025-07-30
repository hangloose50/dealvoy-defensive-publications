import json
import time
from datetime import datetime

LOG_PATH = "scraper_status_log.json"

# Simulate ping/check for all scrapers (stub for real implementation)
def ping_scrapers():
    # In real use, this would check each scraper's endpoint or heartbeat
    with open(LOG_PATH, "r") as f:
        status = json.load(f)
    # Update timestamps for demo
    now = datetime.utcnow().isoformat() + "Z"
    for entry in status:
        if entry["status"] == "pass":
            entry["last_success"] = now
            entry["fail_count"] = 0
            entry["last_error"] = None
        else:
            entry["last_fail"] = now
            entry["fail_count"] += 1
    with open(LOG_PATH, "w") as f:
        json.dump(status, f, indent=2)
    print("[Monitor] Scraper status log updated.")

if __name__ == "__main__":
    ping_scrapers()
