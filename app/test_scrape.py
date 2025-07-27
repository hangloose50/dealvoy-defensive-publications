import cloudscraper
from app.bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()
url = "https://www.amazon.com/dp/B08C7KG5LP"

resp = scraper.get(url, timeout=10)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

selectors = [
    "#detailBullets_feature_div li",
    "#productDetails_detailBullets_sections1 tr"
]

print("🔍 Raw detail entries:")
for sel in selectors:
    for el in soup.select(sel):
        print(" ┗", el.text.strip())
