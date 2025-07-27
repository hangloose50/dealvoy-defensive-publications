from utils import fetch_with_retries, get_json
from app import time

class AmazonMissingUpcScraper:
    def __init__(self, upc_service):
        self.upc_service = upc_service

    def search(self, query):
        time.sleep(0.5)
        base = query.replace("+", " ").title()
        items = []
        for i in range(1,4):
            items.append({
                "title": f"{base} AmazonMissingUpcScraper Item {i}",
                "price": round(20.0 + i*5, 2),
                "upc": f"AmazonMissingUpcScraper-MOCK-{i}",
                "amazon_price": round((20.0 + i*5)*1.5, 2)
            })
        return items
    
# Stub for registry discovery 
def scrape_amazon_missing_upc() -> list[dict]:
    # TODO: implement actual logic
    return []
