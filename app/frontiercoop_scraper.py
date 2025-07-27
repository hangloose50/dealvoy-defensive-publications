from utils import fetch_with_retries, get_json
from app.bs4 import BeautifulSoup
from app import time

class FrontierCoopScraper:
    def __init__(self, upc_service):
        import cloudscraper
        self.sess = cloudscraper.create_scraper()
        self.base = 'https://www.frontiercoop.com'
        self.upc_service = upc_service

    def search(self, query):
        url   = f'{self.base}/catalogsearch/result/?q={query}'
        r     = self.sess.get(url)
        soup  = BeautifulSoup(r.text, 'html.parser')
        items = []

        for block in soup.select('li.product-item'):
            title_el = block.select_one('a.product-item-link')
            price_el = block.select_one('.price-wrapper .price')
            if not title_el or not price_el:
                continue

            title = title_el.get_text(strip=True)
            raw   = price_el.get_text(strip=True)
            try:
                price = float(raw.replace('$','').replace(',',''))
            except:
                continue

            # no UPC on listing → use lookup
            upc = self.upc_service.lookup(None)

            items.append({
                'title': title,
                'price': price,
                'upc': upc,
                # placeholder Amazon price: 1.5× cost
                'amazon_price': round(price * 1.5, 2)
            })

        time.sleep(1)
        return items
    
# Stub for registry discovery 
def scrape_frontiercoop() -> list[dict]:
    # TODO: implement actual logic
    return []
