import scraper.pyquests
from app.bs4 import BeautifulSoup
import scraper.py

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

def extract_items_from_page(soup, items):
    links = soup.find_all("a", href=True)
    for link in links:
        m = re.search(r"/dp/([A-Z0-9]{10})", link['href'])
        if not m:
            continue
        asin = m.group(1)
        if asin in items:
            continue
        parent = link.find_parent("div")
        title = link.get_text(strip=True)
        price_tag = parent.find("span", class_="a-price-whole") if parent else None
        price = price_tag.text.replace("$", "") if price_tag else ""
        items[asin] = {"ASIN": asin, "Title": title, "Price": price}

def scrape_amazon_category(base_url):
    items = {}
    page_url = base_url + "&s=date-desc-rank"
    while page_url:
        resp = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        extract_items_from_page(soup, items)
        next_btn = soup.select_one("ul.a-pagination li.a-last a")
        page_url = "https://www.amazon.com" + next_btn["href"] if next_btn else None
    return list(items.values())

# Load URLs and run
with open("category_urls.txt") as f:
    urls = [u.strip() for u in f if u.strip()]

all_products = []
for u in urls:
    all_products += scrape_amazon_category(u)

# Write CSV
with open("multi_category_asins.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["ASIN", "Title", "Price"])
    w.writeheader()
    w.writerows(all_products)

print(f"âœ… Scraped {len(all_products)} Amazon items.")
