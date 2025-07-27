from utils import fetch_with_retries, get_json
import ebay_scraper.pyquests
from app.bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0"}

def scrape_ebay_search(url):
    items = []
    page = 1
    while True:
        resp = requests.get(f"{url}&_pgn={page}&_sop=10", headers=headers)
        soup = BeautifulSoup(resp.text,"html.parser")
        cards = soup.select("li.s-item")
        if not cards: break
        for c in cards:
            title = c.select_one("h3.s-item__title").get_text(strip=True) if c.select_one("h3.s-item__title") else ""
            price = c.select_one("span.s-item__price").get_text(strip=True).replace("$","") if c.select_one("span.s-item__price") else ""
            link = c.select_one("a.s-item__link")["href"] if c.select_one("a.s-item__link") else ""
            items.append([title,price,link])
        page += 1
    return items

with open("ebay_urls.txt") as f:
    urls = [u.strip() for u in f if u.strip()]

all_e = []
for u in urls:
    all_e += scrape_ebay_search(u)

with open("ebay_products.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Title","Price","Product URL"])
    w.writerows(all_e)

print(f"âœ… Scraped {len(all_e)} eBay items.")
# Stub for registry
def scrape_ebay() -> list[dict]:
    # TODO: implement scraper logic
    return []

