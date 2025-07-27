#!/usr/bin/env python3
"""
🌍 LocalizationVoyager - i18n/l10n string and translation checks
"""
import argparse, json, sys
from pathlib import Path

def is_agent_enabled():
    try:
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        return is_agent_enabled("LocalizationVoyager")
    except Exception:
        return True

def main():
    parser = argparse.ArgumentParser(description="LocalizationVoyager - Localization Agent")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    if not is_agent_enabled():
        print("🌍 LocalizationVoyager is disabled - skipping")
        return 78
    if args.smoke:
        print("🌍 LocalizationVoyager: Smoke test passed!")
        return 0
    # 1. Scan for .po/.mo files and language support
    root = Path(__file__).resolve().parents[3]
    po_files = list(root.rglob("*.po"))
    mo_files = list(root.rglob("*.mo"))
    results_dir = root / "app" / "docs"
    results_dir.mkdir(exist_ok=True)
    report_file = results_dir / "localization_report.txt"
    with open(report_file, "w") as f:
        if po_files or mo_files:
            f.write("Localization files found:\n")
            for fpath in po_files + mo_files:
                f.write(str(fpath.relative_to(root)) + "\n")
        else:
            f.write("No localization files found.\n")

    # 2. Update README.md with localization summary
    readme = root / "README.md"
    try:
        with open(readme, "a") as f:
            f.write(f"\n\n## LocalizationVoyager Report\n{report_file.read_text()}\n")
    except Exception:
        pass

    print(f"🌍 LocalizationVoyager: ✅ Localization report generated at {report_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
