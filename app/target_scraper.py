from utils import fetch_with_retries, get_json
import target_scraper.pyquests
from app.bs4 import BeautifulSoup
from app import csv

headers = {"User-Agent":"Mozilla/5.0"}

def scrape_target_category(url):
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    products = []
    for card in soup.select("li.h-padding-h-tight"):
        title = card.select_one("a").get_text(strip=True) if card.select_one("a") else ""
        price = card.select_one("span[data-test='product-price']").get_text(strip=True).replace("$","") if card.select_one("span[data-test='product-price']") else ""
        sku = card.get("data-test-sku") or ""
        link = "https://www.target.com" + card.select_one("a")["href"] if card.select_one("a") else ""
        products.append([title,price,sku,link])
    return products

# Bulk run
with open("target_urls.txt") as f:
    urls = [u.strip() for u in f if u.strip()]

all_t = []
for u in urls:
    all_t += scrape_target_category(u)

with open("target_products.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Title","Price","SKU","Product URL"])
    w.writerows(all_t)

print(f"âœ… Scraped {len(all_t)} Target items.")
# Stub for registry
def scrape_target() -> list[dict]:
    # TODO: implement scraper logic
    return []

