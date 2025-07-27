# app/services/pipeline_adapters.py

import pipeline_adapters.py
import pipeline_adapters.py
from app import subprocess
import pipeline_adapters.py

from app.schemas import PriceSnapshot
from app.services.scraper_registry import register

# Compute our project root and pipelines folder
ROOT_DIR     = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PIPELINE_DIR = os.path.join(ROOT_DIR, "pipelines")

def run_pipeline(source: str, upc: str) -> PriceSnapshot:
    """
    Runs: pipelines/run_<source>_pipeline.py <upc>
    Expects JSON on stdout with at least "upc" and "price".
    """
    script = f"run_{source.lower()}_pipeline.py"
    path   = os.path.join(PIPELINE_DIR, script)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Pipeline script not found at {path}")

    # Use the same Python interpreter to invoke the script
    proc = subprocess.run(
        [sys.executable, path, upc],
        capture_output=True,
        text=True,
        check=True
    )
    data = json.loads(proc.stdout)

    return PriceSnapshot(
        upc=data["upc"],
        price=data["price"],
        previous_price=data.get("previous_price", data["price"])
    )

@register
def amazon(upc: str) -> PriceSnapshot:
    return run_pipeline("amazon", upc)

@register
def ebay(upc: str) -> PriceSnapshot:
    return run_pipeline("ebay", upc)

@register
def walmart(upc: str) -> PriceSnapshot:
    return run_pipeline("walmart", upc)

# â€¦and so on for FrontierCoop, DandH, PuzzleWarehouse, etc.



