from RetailScraperBase import RetailScraperBase, ProductData
from typing import List
from urllib.parse import quote
from bs4 import BeautifulSoup
import random, time

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
]

def get_product_data(query: str = "tractor", max_results: int = 10) -> List[ProductData]:
    return TractorSupplyScraper().search_products(query, max_results)

class TractorSupplyScraper(RetailScraperBase):
    def __init__(self):
        super().__init__(
            source_name="Tractor Supply",
            base_url="https://www.tractorsupply.com"
        )
        self.search_endpoint = "https://www.tractorsupply.com/tsc/search/"

    def search_products(self, query: str, max_results: int = 10) -> List[ProductData]:
        products = []
        self.reset_session()
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        time.sleep(random.uniform(1.2, 2.5))
        if not self.check_compliance():
            print("❌ Tractor Supply scraping not allowed by robots.txt")
            return products
        search_url = f"{self.search_endpoint}{quote(query)}"
        response = self.make_request(search_url, headers=headers)
        if hasattr(response, 'status_code') and response.status_code in [403, 500]:
            print("🔄 Anti-bot detection, retrying with Selenium...")
            response = self.make_request(search_url, use_selenium=True)
        if response.status_code != 200:
            print(f"❌ Tractor Supply search failed: {response.status_code}")
            return products
        soup = BeautifulSoup(response.content, 'html.parser')
        product_cards = soup.find_all('div', class_='product-tile')
        for card in product_cards[:max_results]:
            title_elem = card.find('a', class_='product-title')
            price_elem = card.find('span', class_='product-price')
            url_elem = title_elem
            image_elem = card.find('img', class_='product-image')
            title = title_elem.get_text(strip=True) if title_elem else None
            price = self.extract_price(price_elem.get_text()) if price_elem else None
            product_url = url_elem['href'] if url_elem and url_elem.has_attr('href') else None
            image_url = image_elem['src'] if image_elem and image_elem.has_attr('src') else None
            upc = None
            products.append(ProductData(
                product_url=product_url,
                title=title,
                price=price,
                stock=None,
                image=image_url,
                upc=upc
            ))
        return products
