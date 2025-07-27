#!/usr/bin/env python3
"""
Offline Packager - Bundles code, dependencies, and assets for offline use
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path
import zipfile

def main():
    root = Path(__file__).resolve().parents[1]
    dist_dir = root / "dist/offline"
    dist_dir.mkdir(parents=True, exist_ok=True)
    # 1. Download wheels for all requirements
    req_file = root / "requirements.txt"
    if req_file.exists():
        subprocess.run([
            sys.executable, "-m", "pip", "download", "-r", str(req_file), "-d", str(dist_dir)
        ], check=True)
    # 2. Collect folders/files to bundle
    bundle_files = [
        "app", "assets", "prompts", "Makefile"
    ]
    # 3. Create zip
    bundle_zip = root / "dist/dealvoy_offline_bundle.zip"
    with zipfile.ZipFile(bundle_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for item in bundle_files:
            p = root / item
            if p.is_dir():
                for sub in p.rglob("*"):
                    if sub.is_file():
                        zipf.write(sub, sub.relative_to(root))
            elif p.is_file():
                zipf.write(p, p.relative_to(root))
        # Add offline wheels
        for whl in dist_dir.glob("*"):
            zipf.write(whl, Path("dist/offline") / whl.name)
    print(f"✅ Offline bundle created: {bundle_zip}")

if __name__ == "__main__":
    main()
