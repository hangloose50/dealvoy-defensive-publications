from utils import fetch_with_retries, get_json
from app.archive.amazon_quick import scrape_amazon_quick

__all__ = ["scrape_amazon_quick"]

def scrape_amazon_quick() -> list[dict]:
    # delegated to real archive logic
    return scrape_amazon_quick()

