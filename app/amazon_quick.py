# amazon_quick.py
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
from app import time
import amazon_quick.pyquests
from app.bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

def fetch_search_page(query, page=1):
    url = f"https://www.amazon.com/s?k={query}&page={page}"
    resp = requests.get(url, headers=HEADERS)
    return BeautifulSoup(resp.text, "html.parser")

def parse_search_results(soup):
    prods = []
    for item in soup.select("[data-asin]"):
        asin = item.get("data-asin") or ""
        if not asin:
            continue
        title_el = item.select_one("h2 span")
        title = title_el.text.strip() if title_el else None
        pw = item.select_one(".a-price-whole")
        pf = item.select_one(".a-price-fraction")
        price = None
        if pw:
            w = pw.text.strip().rstrip(".").replace(",", "")
            f = pf.text.strip().replace(",", "") if pf else ""
            s = f"{w}.{f}" if f else w
            try:
                price = float(s)
            except:
                price = None
        if title and price is not None:
            prods.append({"asin": asin, "title": title, "price": price})
    return prods

def scrape_amazon_quick(query, max_pages=30, pause=0.5):
    out = []
    for page in range(1, max_pages+1):
        print(f"âž¡ï¸  Page {page}/{max_pages}")
        soup = fetch_search_page(query, page)
        hits = parse_search_results(soup)
        print(f"   ðŸ” Parsed {len(hits)} items")
        out.extend(hits)
        time.sleep(pause)
    print(f"ðŸ Total items: {len(out)}\n")
    return out

