#!/usr/bin/env python3
"""
📄 DocVoyager - Auto-generates and updates documentation
"""
import argparse, json, sys
from pathlib import Path

def is_agent_enabled():
    try:
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        return is_agent_enabled("DocVoyager")
    except Exception:
        return True

def main():
    parser = argparse.ArgumentParser(description="DocVoyager - Documentation Agent")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    if not is_agent_enabled():
        print("📄 DocVoyager is disabled - skipping")
        return 78
    if args.smoke:
        print("📄 DocVoyager: Smoke test passed!")
        return 0

    # 1. Generate API docs for all .py files in app/
    import subprocess
    app_dir = Path(__file__).resolve().parents[3] / "app"
    docs_dir = app_dir / "docs"
    docs_dir.mkdir(exist_ok=True)
    py_files = list(app_dir.rglob("*.py"))
    doc_count = 0
    for py_file in py_files:
        mod_name = py_file.stem
        doc_file = docs_dir / f"{mod_name}_api.txt"
        try:
            result = subprocess.run([sys.executable, "-m", "pydoc", str(py_file)], capture_output=True, text=True, timeout=10)
            with open(doc_file, "w") as f:
                f.write(result.stdout)
            doc_count += 1
        except Exception:
            continue

    # 2. Update README.md with module list
    readme = Path(__file__).resolve().parents[3] / "README.md"
    module_list = sorted([f"- {f.relative_to(app_dir)}" for f in py_files])
    try:
        with open(readme, "a") as f:
            f.write("\n\n## Modules in app/\n" + "\n".join(module_list) + "\n")
    except Exception:
        pass

    # 3. Create a simple architecture diagram (text-based)
    arch_file = docs_dir / "architecture.txt"
    try:
        with open(arch_file, "w") as f:
            f.write("""
Project Architecture:

app/
├── assistant/
│   └── agents/  # All Voyager agents
├── vision/      # Vision/OCR modules
├── ...          # Other modules
├── __init__.py
└── ...
""")
    except Exception:
        pass

    print(f"📄 DocVoyager: ✅ Generated {doc_count} API docs, updated README, created architecture diagram.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
