# File: debug_scrapers.py

import pkgutil
from app.pprint import pprint

# grab the scrapers package path
scrapers_pkg = importlib.import_module("app.services.scrapers")
path = scrapers_pkg.__path__

loaded = []
skipped = {}

for _, module_name, _ in pkgutil.iter_modules(path):
    if not module_name.endswith("_scraper"):
        continue
    try:
        importlib.import_module(f"app.services.scrapers.{module_name}")
        loaded.append(module_name)
    except Exception as e:
        skipped[module_name] = repr(e)

print("âœ… Loaded modules:")
pprint(loaded)

print("\nâš ï¸  Skipped modules and errors:")
pprint(skipped)
