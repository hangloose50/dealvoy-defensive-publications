# test_selenium_scrape.py

from app.amazon_selenium import scrape_amazon_browser

results = scrape_amazon_browser("usb+charger", max_pages=1)

print(f"\n🧾 Extracted {len(results)} products:\n")
for i, item in enumerate(results, start=1):
    print(f"{i:2}. ASIN: {item['asin']}")
    print(f"    Title: {item['title'][:60]}")
    print(f"    Price: ${item['price']:.2f}")
    print(f"    UPC:   {item['upc'] or '–'}\n")
