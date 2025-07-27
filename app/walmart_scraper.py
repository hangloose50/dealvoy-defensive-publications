from utils import fetch_with_retries, get_json
import walmart_scraper.pyquests
from app.bs4 import BeautifulSoup
from app import csv
import walmart_scraper.py

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

# Read Walmart category/search page URLs from file
with open("walmart_urls.txt", "r") as f:
    walmart_urls = [line.strip() for line in f if line.strip()]

def extract_products(url):
    try:
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.find_all("div", class_=re.compile("search-result-gridview-item"))

        results = []

        for item in items:
            title_tag = item.find("a", class_=re.compile("product-title-link"))
            price_tag = item.find("span", class_=re.compile("price-group"))
            image_tag = item.find("img")
            
            title = title_tag.get_text(strip=True) if title_tag else ""
            link = "https://www.walmart.com" + title_tag['href'] if title_tag and title_tag.has_attr('href') else ""
            sku_match = re.search(r"/(\d+)", link)
            sku = sku_match.group(1) if sku_match else ""
            price = price_tag['aria-label'].replace("$", "") if price_tag and price_tag.has_attr('aria-label') else ""
            image_url = image_tag['src'] if image_tag and image_tag.has_attr('src') else ""

            if sku:
                results.append([title, price, sku, link, image_url])
        return results

    except Exception as e:
        print(f"âŒ Error with {url}: {e}")
        return []

all_walmart_products = []

for url in walmart_urls:
    print(f"ðŸ›ï¸ Scanning Walmart category: {url}")
    data = extract_products(url)
    all_walmart_products.extend(data)

with open("walmart_products.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Price", "SKU", "Product URL", "Image URL"])
    for row in all_walmart_products:
        writer.writerow(row)

print(f"âœ… Scraped {len(all_walmart_products)} Walmart products to walmart_products.csv")
    
# Stub for registry discovery 
def scrape_walmart() -> list[dict]:
    # TODO: implement actual logic
    return []

