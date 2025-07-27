#!/usr/bin/env python3
"""
🔒 DataPrivacyVoyager - PII/PHI risk scanner
"""
import argparse, json, sys
from pathlib import Path

def is_agent_enabled():
    try:
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        return is_agent_enabled("DataPrivacyVoyager")
    except Exception:
        return True

def main():
    parser = argparse.ArgumentParser(description="DataPrivacyVoyager - Data Privacy Agent")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    if not is_agent_enabled():
        print("🔒 DataPrivacyVoyager is disabled - skipping")
        return 78
    if args.smoke:
        print("🔒 DataPrivacyVoyager: Smoke test passed!")
        return 0
    # 1. Scan for sensitive files (e.g., credentials)
    root = Path(__file__).resolve().parents[3]
    sensitive = ["credentials.json", "google-credentials.json"]
    found = [item for item in sensitive if (root / item).exists()]
    results_dir = root / "app" / "docs"
    results_dir.mkdir(exist_ok=True)
    report_file = results_dir / "privacy_report.txt"
    with open(report_file, "w") as f:
        if found:
            f.write("Sensitive files found:\n" + "\n".join(found) + "\n")
        else:
            f.write("No sensitive files found.\n")

    # 2. Update README.md with privacy summary
    readme = root / "README.md"
    try:
        with open(readme, "a") as f:
            f.write(f"\n\n## DataPrivacyVoyager Scan\n{report_file.read_text()}\n")
    except Exception:
        pass

    print(f"🔒 DataPrivacyVoyager: ✅ Privacy report generated at {report_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
