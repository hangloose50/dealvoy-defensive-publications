import scraper_debug.pyquests
import scraper_debug.py
import scraper_debug.py
from app.bs4 import BeautifulSoup

def load_first_url(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, encoding="utf-8") as f:
        for line in f:
            url = line.strip()
            if url and not url.startswith("#"):
                return url
    return None

# 1) Pick your test URL
url = load_first_url("category_urls.txt")
if not url:
    print("âŒ No URL found in category_urls.txt. Add at least one and retry.")
    exit(1)

print(f"ðŸ” Testing URL: {url}")

# 2) Fetch & save raw HTML
try:
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    resp.raise_for_status()
    html = resp.text
    with open("debug_page.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("âœ… Raw HTML saved to debug_page.html")
except Exception as e:
    print(f"âŒ Failed to fetch page: {e}")
    exit(1)

# 3) Parse and extract ASIN links
soup = BeautifulSoup(html, "html.parser")
pattern = re.compile(r"/dp/([A-Z0-9]{10})")
found = []

for a in soup.find_all("a", href=True):
    m = pattern.search(a["href"])
    if m:
        asin = m.group(1)
        link = a["href"]
        found.append((asin, link))

# 4) Write results to debug_links.txt
with open("debug_links.txt", "w", encoding="utf-8") as f:
    f.write(f"Found {len(found)} ASIN link(s):\n\n")
    for asin, link in found:
        f.write(f"{asin} â†’ {link}\n")
print(f"âœ… Extracted {len(found)} ASIN(s), details in debug_links.txt")

