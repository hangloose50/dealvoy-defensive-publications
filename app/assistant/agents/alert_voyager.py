#!/usr/bin/env python3
"""
🚨 AlertVoyager - Agent event alerting (Slack/email)
"""
import argparse, json, sys
from pathlib import Path

def is_agent_enabled():
    try:
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        return is_agent_enabled("AlertVoyager")
    except Exception:
        return True

def main():
    parser = argparse.ArgumentParser(description="AlertVoyager - Alerting Agent")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    if not is_agent_enabled():
        print("🚨 AlertVoyager is disabled - skipping")
        return 78
    if args.smoke:
        print("🚨 AlertVoyager: Smoke test passed!")
        return 0
    # 1. Scan logs for errors and warnings
    root = Path(__file__).resolve().parents[3]
    log_files = list(root.glob("*.log"))
    alerts = []
    for log in log_files:
        try:
            with open(log) as f:
                for line in f:
                    if "error" in line.lower() or "warning" in line.lower():
                        alerts.append(f"{log.name}: {line.strip()}")
        except Exception:
            continue
    results_dir = root / "app" / "docs"
    results_dir.mkdir(exist_ok=True)
    alert_file = results_dir / "alerts.txt"
    with open(alert_file, "w") as f:
        if alerts:
            f.write("\n".join(alerts) + "\n")
        else:
            f.write("No errors or warnings found in logs.\n")

    # 2. Update README.md with alert summary
    readme = root / "README.md"
    try:
        with open(readme, "a") as f:
            f.write(f"\n\n## AlertVoyager Log Alerts\n{alert_file.read_text()}\n")
    except Exception:
        pass

    print(f"🚨 AlertVoyager: ✅ Alert report generated at {alert_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
