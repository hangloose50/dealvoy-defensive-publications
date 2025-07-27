import pkgutil
import importlib
import logging
from typing import Dict, Callable, Optional, List

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

SCRAPER_REGISTRY: Dict[str, Callable] = {}

for _, module_name, _ in pkgutil.iter_modules(__path__):
    if not module_name.endswith("_scraper"):
        continue
    try:
        module = importlib.import_module(f"{__name__}.{module_name}")
    except Exception as e:
        logger.warning(f"Skipping scraper {module_name}: {e}")
        continue
    for attr in dir(module):
        if attr.startswith("scrape_"):
            fn = getattr(module, attr)
            if callable(fn):
                key = attr.replace("scrape_", "").title().replace("_", "")
                SCRAPER_REGISTRY[key] = fn

def discover_scrapers(active_sources: Optional[List[str]] = None) -> Dict[str, Callable]:
    if active_sources:
        return {k: fn for k, fn in SCRAPER_REGISTRY.items() if k in active_sources}
    return SCRAPER_REGISTRY




