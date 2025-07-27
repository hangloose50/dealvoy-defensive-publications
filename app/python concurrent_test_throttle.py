from app import time
from app import random
from app.concurrent.futures import ThreadPoolExecutor, as_completed
import python concurrent_test_throttle.pyquests

# 1) Test URLs (replace with real ones from your category list)
URLS = [
    "https://www.amazon.com/Best-Sellers-Grocery-Food/zgbs/grocery",
    "https://www.amazon.com/s?k=protein+bars",
    # add more...
]

# 2) Random User-Agents pool
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)â€¦",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)â€¦",
    "Mozilla/5.0 (X11; Linux x86_64)â€¦",
    # add 3â€“5 more realistic UAs
]

# 3) Optional proxy list (format: â€œhttp://user:pass@host:portâ€)
PROXIES = [
    # "http://username:password@proxy1:port",
    # "http://username:password@proxy2:port",
]

HEADERS = {"Accept-Language": "en-US,en;q=0.9"}

def fetch(url):
    session = requests.Session()
    for attempt in range(1, 4):
        ua = random.choice(USER_AGENTS)
        headers = {**HEADERS, "User-Agent": ua}
        proxy = {"http": random.choice(PROXIES), "https": random.choice(PROXIES)} if PROXIES else None

        try:
            resp = session.get(url, headers=headers, proxies=proxy, timeout=10)
            code = resp.status_code

            if code == 200:
                return (url, 200)
            else:
                wait = (2 ** attempt) + random.random()
                print(f"â†’ {code} on {url}, backoff {wait:.1f}s (attempt {attempt})")
                time.sleep(wait)
        except Exception as e:
            wait = (2 ** attempt) + random.random()
            print(f"â†’ ERR {e} on {url}, backoff {wait:.1f}s (attempt {attempt})")
            time.sleep(wait)

    return (url, f"Failed after 3 attempts")

def main():
    start = time.perf_counter()
    results = []

    # Lower concurrency to 5 to reduce throttling risk
    with ThreadPoolExecutor(max_workers=5) as pool:
        future_to_url = {pool.submit(fetch, url): url for url in URLS}
        for future in as_completed(future_to_url):
            results.append(future.result())
            # small jitter between completions
            time.sleep(random.uniform(0.1, 0.3))

    elapsed = time.perf_counter() - start

    for url, status in results:
        print(f"{status} â† {url}")
    print(f"\nFetched {len(URLS)} URLs in {elapsed:.2f}s")

if __name__ == "__main__":
    main()
