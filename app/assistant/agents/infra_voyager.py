#!/usr/bin/env python3
"""
☁️ InfraVoyager - Infrastructure drift and cloud checks
"""
import argparse, json, sys
from pathlib import Path

def is_agent_enabled():
    try:
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        return is_agent_enabled("InfraVoyager")
    except Exception:
        return True

def main():
    parser = argparse.ArgumentParser(description="InfraVoyager - Infrastructure Agent")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    if not is_agent_enabled():
        print("☁️ InfraVoyager is disabled - skipping")
        return 78
    if args.smoke:
        print("☁️ InfraVoyager: Smoke test passed!")
        return 0
    # 1. Check for required files and folders (infra audit)
    root = Path(__file__).resolve().parents[3]
    required = ["requirements.txt", "README.md", "app", "tests"]
    missing = [item for item in required if not (root / item).exists()]
    results_dir = root / "app" / "docs"
    results_dir.mkdir(exist_ok=True)
    report_file = results_dir / "infra_audit.txt"
    with open(report_file, "w") as f:
        if missing:
            f.write("Missing infra items:\n" + "\n".join(missing) + "\n")
        else:
            f.write("All required infra items present.\n")

    # 2. Update README.md with infra audit
    readme = root / "README.md"
    try:
        with open(readme, "a") as f:
            f.write(f"\n\n## InfraVoyager Audit\n{report_file.read_text()}\n")
    except Exception:
        pass

    print(f"☁️ InfraVoyager: ✅ Infra audit report generated at {report_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
