# test_amazon.py

from app.amazon import fetch_search_page, parse_search_results

# 1) Fetch page 1 of “usb charger”
soup  = fetch_search_page("usb+charger", page=1)

# 2) Parse results
items = parse_search_results(soup)

# 3) Print count + first few ASINs/titles
print(f"⚡️ Found {len(items)} items on page 1")
for i, p in enumerate(items, start=1):
    print(f"{i}. {p['asin']} — {p['title'][:50]}")
