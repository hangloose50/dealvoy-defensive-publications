from utils import fetch_with_retries, get_json
from app.archive.amazon_selenium import scrape_amazon_browser

__all__ = ["scrape_amazon_browser"]

def scrape_amazon_browser() -> list[dict]:
    # delegated to real archive logic
    return scrape_amazon_browser()

