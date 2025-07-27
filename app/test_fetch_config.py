# test_fetch_config.py

from app.http_utils import fetch_concurrent

URLS = [
    "https://www.amazon.com/Best-Sellers-Grocery-Food/zgbs/grocery",
    "https://www.amazon.com/s?k=protein+bars",
    "https://www.amazon.com/s?k=coffee+pods",
]

def main():
    results = fetch_concurrent(URLS)
    for url, resp in results:
        code = resp.status_code if resp else "Failed"
        print(f"{code} <- {url}")

if __name__ == "__main__":
    main()

