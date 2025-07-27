from app.http_utils import fetch_concurrent
from app.bs4 import BeautifulSoup

def harvest_category_urls(seed_urls):
    results = fetch_concurrent(seed_urls, max_workers=5)
    # parse each resp.text with BeautifulSoup to extract sub-links...
