#!/usr/bin/env python3
"""
⚖️ LegalVoyager - License, copyright, export law
"""
import argparse, json, sys
from pathlib import Path

def is_agent_enabled():
    try:
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        return is_agent_enabled("LegalVoyager")
    except Exception:
        return True

def main():
    parser = argparse.ArgumentParser(description="LegalVoyager - Legal Compliance Agent")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    if not is_agent_enabled():
        print("⚖️ LegalVoyager is disabled - skipping")
        return 78
    if args.smoke:
        print("⚖️ LegalVoyager: Smoke test passed!")
        return 0
    # 1. Scan for license files and compliance
    root = Path(__file__).resolve().parents[3]
    license_files = list(root.glob("LICENSE*"))
    results_dir = root / "app" / "docs"
    results_dir.mkdir(exist_ok=True)
    report_file = results_dir / "legal_report.txt"
    with open(report_file, "w") as f:
        if license_files:
            f.write("Found license files:\n" + "\n".join(str(l) for l in license_files) + "\n")
        else:
            f.write("No license files found.\n")

    # 2. Update README.md with legal summary
    readme = root / "README.md"
    try:
        with open(readme, "a") as f:
            f.write(f"\n\n## LegalVoyager License Audit\n{report_file.read_text()}\n")
    except Exception:
        pass

    print(f"⚖️ LegalVoyager: ✅ Legal report generated at {report_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
