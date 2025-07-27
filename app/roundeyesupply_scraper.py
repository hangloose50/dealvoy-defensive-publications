from utils import fetch_with_retries, get_json
from app import time

class RoundEyeSupplyScraper:
    def __init__(self, upc_service):
        self.upc_service = upc_service

    def search(self, query):
        time.sleep(1)
        base = query.replace("+", " ").title()
        return [
            {
                "title": f"{base} RoundEyeSupplyScraper Item {i}",
                "price": 10.0 + i,
                "upc": f"RoundEyeSupplyScraper-MOCK-{i}",
                "amazon_price": round((10.0 + i) * 1.5, 2)
            }
            for i in range(1, 4)
        ]
    
# Stub for registry discovery 
def scrape_roundeyesupply() -> list[dict]:
    # TODO: implement actual logic
    return []
