import random
from bs4 import BeautifulSoup
from app.http_utils import fetch_with_retries

PROXIES = [
    # "http://username:password@proxy1:port",
    # "http://username:password@proxy2:port",
]

def get_proxy():
    if PROXIES:
        proxy_url = random.choice(PROXIES)
        return {"http": proxy_url, "https": proxy_url}
    return None

def scrape_amazon(query: str, max_results: int = 5) -> list[dict]:
    """
    Search Amazon for `query` and return up to `max_results` products.
    Each product is a dict: {"asin", "title", "price", "url", ...}.
    """
    search_url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"
    proxies = get_proxy()
    resp = fetch_with_retries(search_url, proxies=proxies)
    if not resp or not resp.text:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    items = []
    for card in soup.select("div.s-result-item[data-asin]")[:max_results]:
        asin        = card.get("data-asin", "")
        title_el    = card.select_one("h2 a span")
        price_whole = card.select_one(".a-price-whole")
        price_frac  = card.select_one(".a-price-fraction")
        link        = card.select_one("h2 a")
        url_tail    = link.get("href", "") if link else ""
        image_el    = card.select_one("img.s-image")
        availability = "In Stock"  # Placeholder
        buy_box = None  # Placeholder

        price = None
        if price_whole and price_frac:
            price = f"{price_whole.get_text(strip=True)}.{price_frac.get_text(strip=True)}"

        items.append({
            "asin":  asin,
            "title": title_el.get_text(strip=True) if title_el else None,
            "price": price,
            "url":   f"https://www.amazon.com{url_tail}",
            "image": image_el["src"] if image_el else None,
            "availability": availability,
            "buy_box": buy_box,
        })
    return items
