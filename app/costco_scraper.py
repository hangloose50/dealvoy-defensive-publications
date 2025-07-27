from utils import fetch_with_retries, get_json
# costco_scraper.py

from app.bs4 import BeautifulSoup
import costco_scraper.py

# your Costco category URLs
URLS = [
    "https://www.costco.com/some-category.html",
    # add more
]

def scrape_costco_category(url: str) -> list[dict]:
    """
    Fetch a Costco category page with retries.
    On failure, returns an empty list instead of raising.
    """
    resp = fetch_with_retries(url)
    if not resp:
        print(f"[timeout] skipped  {url}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    items = []
    for prod in soup.select(".product"):   # adjust to actual Costco markup
        title_tag = prod.select_one(".description")
        price_tag = prod.select_one(".price")
        title = title_tag.get_text(strip=True) if title_tag else "Unknown"
        price = price_tag.get_text(strip=True) if price_tag else None
        items.append({"title": title, "price": price})
    return items

def main():
    all_items = []
    for url in URLS:
        print(f" scraping  {url}")
        all_items.extend(scrape_costco_category(url))

    print(f"  Got {len(all_items)} items total")
    with open("costco_products.json", "w", encoding="utf-8") as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
# Stub for registry
def scrape_costco() -> list[dict]:
    # TODO: implement scraper logic
    return []

