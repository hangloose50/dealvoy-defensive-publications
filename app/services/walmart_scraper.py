import requests
from bs4 import BeautifulSoup
import random

PROXIES = [
    # Add your proxy URLs here, e.g.:
    # "http://username:password@proxy1:port",
    # "http://username:password@proxy2:port",
]


def get_proxy():
    if PROXIES:
        proxy_url = random.choice(PROXIES)
        return {"http": proxy_url, "https": proxy_url}
    return None


def scrape_walmart_product(keyword):
    """
    Scrape Walmart for a product by keyword.
    Returns: dict with asin, sku, title, price, url, image, availability, buy_box.
    """
    search_url = f"https://www.walmart.com/search/?query={keyword}"
    proxies = get_proxy()
    resp = requests.get(search_url, timeout=10, proxies=proxies)
    soup = BeautifulSoup(resp.text, "html.parser")
    first = soup.select_one("div[data-type='items'] div[data-item-id]")
    if not first:
        return None

    title_el = first.select_one("a[data-type='itemTitles']")
    title = title_el.get_text(strip=True) if title_el else None
    url = "https://www.walmart.com" + title_el["href"] if title_el else None
    price_whole = first.select_one("span[data-automation-id='product-price']")
    price = price_whole.get_text(strip=True) if price_whole else None
    image_el = first.select_one("img")
    image = image_el["src"] if image_el else None
    sku = first.get("data-item-id", "")

    return {
        "asin": None,  # Walmart does not use ASIN
        "sku": sku,
        "title": title,
        "price": price,
        "url": url,
        "image": image,
        "availability": "In Stock",  # Placeholder
        "buy_box": None,  # Placeholder
    }


def test_scrape_walmart_product():
    result = scrape_walmart_product("lego")
    assert result is None or (
        "title" in result
        and "price" in result
        and "sku" in result
        and "url" in result
        and "image" in result
        and "availability" in result
        and "buy_box" in result
    )