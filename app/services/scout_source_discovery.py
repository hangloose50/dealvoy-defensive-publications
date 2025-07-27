import requests
from bs4 import BeautifulSoup
import json

def discover_retailers(search_terms=None, max_sites=10):
    if search_terms is None:
        search_terms = ["wholesale retailer", "bulk distributor", "online supplier"]

    discovered = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for term in search_terms:
        query = term.replace(" ", "+")
        url = f"https://www.bing.com/search?q={query}"
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.select("li.b_algo h2 a"):
            href = a.get("href")
            if href and href.startswith("http") and href not in discovered:
                discovered.append(href)
            if len(discovered) >= max_sites:
                break
        if len(discovered) >= max_sites:
            break

    return discovered

def analyze_site_for_products(site_url):
    """
    Checks if the site has product pages and public pricing.
    Returns a dict with product_page_urls and has_pricing.
    """
    try:
        resp = requests.get(site_url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        product_links = []
        has_pricing = False

        # Find links that look like product or shop pages
        for a in soup.find_all("a", href=True):
            text = a.get_text().lower()
            href = a["href"]
            if any(word in text for word in ["product", "shop", "catalog", "store"]):
                if href.startswith("http"):
                    product_links.append(href)
                elif href.startswith("/"):
                    product_links.append(site_url.rstrip("/") + href)
        # Check for price indicators
        if "$" in soup.text or "price" in soup.text.lower():
            has_pricing = True

        return {
            "site": site_url,
            "product_pages": list(set(product_links)),
            "has_pricing": has_pricing
        }
    except Exception as e:
        return {"site": site_url, "error": str(e)}

def auto_discover_and_analyze(search_terms=None, max_sites=10, save_to="discovered_sites.json"):
    sites = discover_retailers(search_terms, max_sites)
    results = []
    for site in sites:
        analysis = analyze_site_for_products(site)
        results.append(analysis)
    # Save results to a JSON config file
    with open(save_to, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    return results