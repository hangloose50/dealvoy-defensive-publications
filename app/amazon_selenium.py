# amazon_selenium.py

from app import time
from app import cloudscraper
from app.bs4 import BeautifulSoup
from app import undetected_chromedriver
from app.selenium.webdriver.common.by import By
from app.selenium.webdriver.support.ui import WebDriverWait
from app.selenium.webdriver.support import expected_conditions as EC
from app.concurrent.futures import ThreadPoolExecutor, as_completed

# ─── Browser Launcher ────────────────────────────────────────────────────────────
def launch_browser(headless=True):
    opts = uc.ChromeOptions()
    opts.headless = headless
    opts.add_argument("--window-size=1200,800")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    )
    return uc.Chrome(options=opts)

# ─── UPC Fetch via Cloudsraper (fast, no JS) ────────────────────────────────────
_scraper = cloudscraper.create_scraper()

def fetch_upc_cloudscraper(url):
    """
    GET detail page via cloudscraper & extract UPC/EAN from table or bullets.
    """
    try:
        r = _scraper.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
    except:
        return None

    # try productDetails table
    for row in soup.select("#productDetails_detailBullets_sections1 tr"):
        k = row.select_one("th").text.lower()
        v = row.select_one("td").text
        if "upc" in k or "ean" in k:
            digits = "".join(filter(str.isdigit, v))
            if 12 <= len(digits) <= 14:
                return digits

    # fallback to detail bullets
    for li in soup.select("#detailBullets_feature_div li"):
        txt = li.text.lower()
        if "upc" in txt or "ean" in txt:
            digits = "".join(filter(str.isdigit, txt))
            if 12 <= len(digits) <= 14:
                return digits

    return None

# ─── Main Scraper ────────────────────────────────────────────────────────────────
def scrape_amazon_browser(query, max_pages=1, upc_workers=5):
    driver = launch_browser(headless=True)
    items = []  # will hold dicts: asin,title,price,href

    for page in range(1, max_pages + 1):
        url = f"https://www.amazon.com/s?k={query}&page={page}"
        print(f"➡️ Browsing page {page}/{max_pages}")
        driver.get(url)

        # wait for any product card
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-asin]"))
            )
        except:
            print("⚠️ Timeout waiting for cards.")
            continue

        cards = driver.find_elements(By.CSS_SELECTOR, "div[data-asin]")
        print(f"   🔍 Found {len(cards)} items")

        # extract ASIN/title/price/href
        for idx, card in enumerate(cards, start=1):
            asin = card.get_attribute("data-asin") or ""
            if not asin:
                continue

            # title fallback chain
            title = None
            for sel in ("h2 a span", "span.a-text-normal", "h2", "span.a-size-medium"):
                try:
                    t = card.find_element(By.CSS_SELECTOR, sel).text.strip()
                    if t:
                        title = t
                        break
                except:
                    continue

            # price fallback chain
            price = None
            for pw, pf in (
                ("span.a-price .a-price-whole", "span.a-price .a-price-fraction"),
                ("span.a-price-whole",      "span.a-price-fraction")
            ):
                try:
                    w = card.find_element(By.CSS_SELECTOR, pw).text
                    f = card.find_element(By.CSS_SELECTOR, pf).text
                    price = float(f"{w}.{f}")
                    break
                except:
                    continue

            # link selector
            href = None
            for link_sel in ("h2 a", "a.a-link-normal"):
                try:
                    href = card.find_element(By.CSS_SELECTOR, link_sel).get_attribute("href")
                    if href:
                        break
                except:
                    continue

            if href:
                items.append({
                    "asin":   asin,
                    "title":  title or "",
                    "price":  price if price is not None else 0.0,
                    "href":   href
                })
            else:
                print(f"     ⚠️ Skipped ASIN {asin}: no link found")

            time.sleep(random.uniform(0.2, 0.4))

        time.sleep(random.uniform(1.0, 2.0))

    driver.quit()
    print(f"🏁 Collected {len(items)} items—proceeding to UPC fetch…")

    # ─── Parallel UPC Fetching ──────────────────────────────────────────────────
    with ThreadPoolExecutor(max_workers=upc_workers) as exe:
        futures = {exe.submit(fetch_upc_cloudscraper, it["href"]): it for it in items}
        for fut in as_completed(futures):
            it = futures[fut]
            try:
                upc = fut.result(timeout=15)
            except:
                upc = None
            it["upc"] = upc

    # now items each have asin, title, price, href, upc
    return items

