from app.http_utils import fetch_many

URLS = [ … ]  # your category URLs

def main():
    results = fetch_many(URLS, max_workers=5)
    for url, resp in results:
        status = resp.status_code if resp else "Failed"
        print(f"{status} <- {url}")

if __name__ == "__main__":
    main()