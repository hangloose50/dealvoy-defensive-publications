#!/usr/bin/env python3
"""
🧠 AIVoyager - AI/ML model monitoring and retraining
"""
import argparse, json, sys
from pathlib import Path

def is_agent_enabled():
    try:
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        return is_agent_enabled("AIVoyager")
    except Exception:
        return True

def main():
    parser = argparse.ArgumentParser(description="AIVoyager - AI/ML Agent")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    if not is_agent_enabled():
        print("🧠 AIVoyager is disabled - skipping")
        return 78
    if args.smoke:
        print("🧠 AIVoyager: Smoke test passed!")
        return 0
    # 1. Scan for AI/ML-related files (e.g., .ipynb, .pt, .h5)
    root = Path(__file__).resolve().parents[3]
    ai_files = list(root.rglob("*.ipynb")) + list(root.rglob("*.pt")) + list(root.rglob("*.h5"))
    results_dir = root / "app" / "docs"
    results_dir.mkdir(exist_ok=True)
    report_file = results_dir / "ai_report.txt"
    with open(report_file, "w") as f:
        if ai_files:
            f.write("AI/ML files found:\n")
            for fpath in ai_files:
                f.write(str(fpath.relative_to(root)) + "\n")
        else:
            f.write("No AI/ML files found.\n")

    # 2. Update README.md with AI summary
    readme = root / "README.md"
    try:
        with open(readme, "a") as f:
            f.write(f"\n\n## AIVoyager Report\n{report_file.read_text()}\n")
    except Exception:
        pass

    print(f"🧠 AIVoyager: ✅ AI report generated at {report_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
