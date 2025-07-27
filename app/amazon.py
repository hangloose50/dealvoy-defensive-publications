from app import time
from app import cloudscraper
from app.bs4 import BeautifulSoup
from app.requests.exceptions import HTTPError

# Create a cloudscraper session
_scraper = cloudscraper.create_scraper()
_scraper.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.amazon.com/",
})

def fetch_search_page(query, page=1, retries=3):
    url = f"https://www.amazon.com/s?k={query}&page={page}"
    for attempt in range(1, retries + 1):
        resp = _scraper.get(url, timeout=10)
        print(f"🔍 [DEBUG] Fetching: {resp.url} → {resp.status_code}")
        snippet = resp.text[:200].replace("\n", " ")
        print(f"🔍 [DEBUG] HTML snippet: {snippet}…\n")
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
def get_total_pages(query):
    soup = fetch_search_page(query, 1)
    nodes = soup.select("ul.a-pagination li.a-normal a")
    nums  = [int(a.text) for a in nodes if a.text.isdigit()]
    return max(nums) if nums else 1

def parse_search_results(soup):
    products = []
    selector = "div.s-main-slot div[data-component-type='s-search-result']"
    for item in soup.select(selector):
        asin = item.get("data-asin","").strip()
        if not asin: continue

        title_el = item.select_one("h2 a span")
        title    = title_el.text.strip() if title_el else None

        pw = item.select_one("span.a-price .a-price-whole")
        pf = item.select_one("span.a-price .a-price-fraction")
        price = None
        if pw:
            w = pw.text.strip().replace(",","").rstrip(".")
            f = pf.text.strip().replace(",","") if pf else ""
            try:
                price = float(f"{w}.{f}" if f else w)
            except ValueError:
                price = None

        link = item.select_one("h2 a")
        detail = link["href"] if link and link.has_attr("href") else None

        if title and price is not None and detail:
            products.append({
                "asin":        asin,
                "title":       title,
                "price":       price,
                "detail_path": detail
            })
    return products

def fetch_detail_page(path, retries=2):
    url = "https://www.amazon.com" + path
    for attempt in range(1, retries+1):
        try:
            r = _scraper.get(url, timeout=8)
            r.raise_for_status()
            return BeautifulSoup(r.text, "html.parser")
        except HTTPError as e:
            code = getattr(e.response, "status_code", None)
            if code in (429, 503) and attempt < retries:
                time.sleep(1 + attempt)
                continue
            break
    return None

def extract_upc(detail_soup):
    if not detail_soup:
        return None
    # table
    for row in detail_soup.select("#productDetails_detailBullets_sections1 tr"):
        k = row.select_one("th").text.lower()
        v = row.select_one("td").text
        if "upc" in k or "ean" in k:
            digits = "".join(filter(str.isdigit, v))
            if 12 <= len(digits) <= 14:
                return digits
    # bullets
    for li in detail_soup.select("#detailBullets_feature_div li"):
        txt = li.text.lower()
        if "upc" in txt or "ean" in txt:
            digits = "".join(filter(str.isdigit, txt))
            if 12 <= len(digits) <= 14:
                return digits
    return None

def scrape_amazon(query, max_pages=None):
    if max_pages is None:
        max_pages = get_total_pages(query)
        print(f"ℹ️ Detected {max_pages} pages for '{query}'")

    results = []
    for page in range(1, max_pages+1):
        print(f"➡️ Fetching page {page}/{max_pages}")
        soup = fetch_search_page(query, page)
        hits = parse_search_results(soup)
        print(f"   🔍 Found {len(hits)} items on page {page}")
        if not hits:
            break

        for idx, prod in enumerate(hits, start=1):
            time.sleep(random.uniform(0.3,0.6))
            dsoup = fetch_detail_page(prod["detail_path"])
            prod["upc"] = extract_upc(dsoup)
            del prod["detail_path"]
            results.append(prod)
            print(f"     [{idx}/{len(hits)}] {prod['asin']} → UPC={prod['upc'] or '–'}")

        time.sleep(random.uniform(1.0,2.0))

    print(f"🏁 Completed scrape: {len(results)} total items\n")
    return results
