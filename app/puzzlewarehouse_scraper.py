from utils import fetch_with_retries, get_json
from app import time

class PuzzleWarehouseScraper:
    def __init__(self, upc_service):
        self.upc_service = upc_service

    def search(self, query):
        time.sleep(1)
        base = query.replace("+", " ").title()
        return [
            {
                "title": f"{base} PuzzleWarehouseScraper Item {i}",
                "price": 10.0 + i,
                "upc": f"PuzzleWarehouseScraper-MOCK-{i}",
                "amazon_price": round((10.0 + i) * 1.5, 2)
            }
            for i in range(1, 4)
        ]


# stub for registry
def scrape_puzzlewarehouse() -> list:
    return []
