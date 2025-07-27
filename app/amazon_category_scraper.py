from utils import fetch_with_retries
from pathlib import Path
from app.bs4 import BeautifulSoup

def scrape_amazon_category() -> list[dict]:
    path = Path(__file__).parent.parent.parent / "data" / "category_urls.txt"
    try:
        with open(path) as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("No category_urls.txt found; skipping.")
        return []

    results = []
    for url in urls:
        try:
            html = fetch_with_retries(url)
            soup = BeautifulSoup(html, "html.parser")

            # Example selectors — adjust to match actual Amazon category page
            title = soup.select_one("h1.product-title")
            upc = soup.select_one("span.upc")
            price = soup.select_one("span.price")

            if title and upc and price:
                results.append({
                    "title": title.text.strip(),
                    "upc": upc.text.strip(),
                    "price": float(price.text.strip().replace("$", ""))
                })
        except Exception as e:
            print(f"[Error] Failed to scrape {url}: {e}")
    return results
