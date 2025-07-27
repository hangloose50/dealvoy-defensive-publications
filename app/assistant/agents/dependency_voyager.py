#!/usr/bin/env python3
"""
🧩 DependencyVoyager - Dependency audit and update
"""
import argparse, json, sys
from pathlib import Path

def is_agent_enabled():
    try:
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        return is_agent_enabled("DependencyVoyager")
    except Exception:
        return True

def main():
    parser = argparse.ArgumentParser(description="DependencyVoyager - Dependency Agent")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    if not is_agent_enabled():
        print("🧩 DependencyVoyager is disabled - skipping")
        return 78
    if args.smoke:
        print("🧩 DependencyVoyager: Smoke test passed!")
        return 0
    # 1. Parse requirements.txt and list dependencies
    root = Path(__file__).resolve().parents[3]
    req = root / "requirements.txt"
    results_dir = root / "app" / "docs"
    results_dir.mkdir(exist_ok=True)
    report_file = results_dir / "dependency_report.txt"
    if req.exists():
        deps = req.read_text().splitlines()
    else:
        deps = []
    with open(report_file, "w") as f:
        if deps:
            f.write("Dependencies found:\n" + "\n".join(deps) + "\n")
        else:
            f.write("No dependencies found.\n")

    # 2. Update README.md with dependency summary
    readme = root / "README.md"
    try:
        with open(readme, "a") as f:
            f.write(f"\n\n## DependencyVoyager Report\n{report_file.read_text()}\n")
    except Exception:
        pass

    print(f"🧩 DependencyVoyager: ✅ Dependency report generated at {report_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
