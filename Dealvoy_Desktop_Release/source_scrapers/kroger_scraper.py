from RetailScraperBase import RetailScraperBase, ProductData
from typing import List, Optional
from urllib.parse import quote
from bs4 import BeautifulSoup
import re

class KrogerScraper(RetailScraperBase):
    def __init__(self):
        super().__init__(
            source_name="Kroger",
            base_url="https://www.kroger.com"
        )
        self.search_endpoint = "https://www.kroger.com/search"

    def search_products(self, query: str, max_results: int = 10) -> List[ProductData]:
        products = []
        self.reset_session()
        if not self.check_compliance():
            print("❌ Kroger scraping not allowed by robots.txt")
            return products
        search_url = f"{self.search_endpoint}?query={quote(query)}"
        response = self.make_request(search_url)
        if hasattr(response, 'status_code') and response.status_code in [403, 500]:
            print("🔄 Anti-bot detection, retrying with Selenium...")
            response = self.make_request(search_url, use_selenium=True)
        if response.status_code != 200:
            print(f"❌ Kroger search failed: {response.status_code}")
            return products
        soup = BeautifulSoup(response.content, 'html.parser')
        product_cards = soup.find_all('div', class_=re.compile(r'ProductCard'))
        for card in product_cards[:max_results]:
            title_elem = card.find('a', class_=re.compile(r'ProductCard-title'))
            price_elem = card.find('span', class_=re.compile(r'ProductCard-price'))
            url_elem = title_elem
            image_elem = card.find('img', class_=re.compile(r'ProductCard-image'))
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
