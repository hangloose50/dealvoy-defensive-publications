from utils import fetch_with_retries, get_json
from app.abc import ABC, abstractmethod

class BaseScraper(ABC):
    @abstractmethod
    def search(self, query: str, pages: int) -> list[dict]:
        pass

    @abstractmethod
    def fetch_upc(self, item: dict) -> str | None:
        pass
    
# Stub for registry discovery 
def scrape_base() -> list[dict]:
    # TODO: implement actual logic
    return []
