import logging
logging.basicConfig(level=logging.WARNING)

from app.services.scrapers import SCRAPER_REGISTRY

print('? Loaded scrapers:', list(SCRAPER_REGISTRY.keys()))


