#!/usr/bin/env python3
"""
Model Snapshot + Patent Export
Gathers all models, prompts, logs, vision samples, and git commit hash into a signed archive.
"""
import os
import tarfile
import hashlib
from pathlib import Path
from datetime import datetime
import subprocess

root = Path(__file__).resolve().parents[1]
dist = root / "dist"
dist.mkdir(exist_ok=True)

# 1. Gather files
snapshot_items = [
    (root / "models"),
    (root / "prompts"),
    (root / "app/docs"),
    (root / "logs"),
    (root / "assets"),
    (root / "app/vision"),
]

# 2. Find model files
model_files = list((root / "models").rglob("*.pt")) + \
              list((root / "models").rglob("*.onnx")) + \
              list((root / "models").rglob("*.pkl")) + \
              list((root / "models").rglob("*.joblib"))

# 3. Get git commit hash
try:
    commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root).decode().strip()
except Exception:
    commit_hash = "unknown"

# 4. Prepare manifest
manifest = []
for item in snapshot_items:
    if item.exists():
        for f in item.rglob("*"):
            if f.is_file():
                manifest.append(str(f.relative_to(root)))

# 5. Archive
now = datetime.now().strftime("%Y%m%d_%H%M%S")
snap_name = f"snapshot_dealvoy_{now}.tar.gz"
snap_path = dist / snap_name

# 6. SHA256 manifest
sha_manifest = dist / "manifest.sha256"
with open(sha_manifest, "w") as f:
    for relpath in manifest:
        h = hashlib.sha256()
        with open(root / relpath, "rb") as file:
            while chunk := file.read(8192):
                h.update(chunk)
        f.write(f"{h.hexdigest()}  {relpath}\n")
    f.write(f"commit: {commit_hash}\n")

# Prepare README
readme = dist / "README.txt"
with open(readme, "w") as f:
    f.write(f"Dealvoy Model Snapshot\nDate: {now}\nGit commit: {commit_hash}\nFiles: {len(manifest)}\n")

# Archive everything in one pass
with tarfile.open(snap_path, "w:gz") as tar:
    for relpath in manifest:
        tar.add(root / relpath, arcname=relpath)
    tar.add(readme, arcname="README.txt")
    tar.add(sha_manifest, arcname="manifest.sha256")

# 7. Signature file
sig = hashlib.sha256()
with open(snap_path, "rb") as f:
    while chunk := f.read(8192):
        sig.update(chunk)
sig_file = dist / f"{snap_name}.sig"
with open(sig_file, "w") as f:
    f.write(sig.hexdigest())

print(f"✅ Model snapshot created: {snap_path}\nSHA256: {sig.hexdigest()}")
