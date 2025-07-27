from app import time
from app.concurrent.futures import ThreadPoolExecutor
import concurrent_test.pyquests

# Replace these with real URLs from your category_urls.txt
URLS = [
    "https://www.amazon.com/Best-Sellers-Grocery-Food/zgbs/grocery",
    "https://www.amazon.com/s?k=protein+bars",
    # â€¦
]

def fetch(url):
    try:
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
        return (url, r.status_code)
    except Exception as e:
        return (url, f"ERR: {e}")

def main():
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(fetch, URLS))
    elapsed = time.perf_counter() - start

    for url, status in results:
        print(f"{status} â† {url}")
    print(f"\nFetched {len(URLS)} URLs in {elapsed:.2f}s")

if __name__ == "__main__":
    main()
