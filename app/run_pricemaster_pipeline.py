import multiprocessing
from app.concurrent.futures import ThreadPoolExecutor, as_completed

from app.pipelines.pricemaster_scraper import PricemasterScraper
from app.shared.upc_service import CsvUPCService
from app.shared.push_to_sheets import push_to_sheets

def main():
    upc_svc = CsvUPCService()
    scraper = PricemasterScraper(upc_service=upc_svc)

    queries = 

    all_items = []
    for q in queries:
        print(f"🔍 Searching '{q}' on pricemaster")
        items = scraper.search(q)
        print(f"   🛒 Retrieved {len(items)} items")

        sheet_name = f"{siteLabel}_{q.split('+')[0].capitalize()}"
        push_to_sheets(items, sheet_name)
        all_items.extend(items)

    upc_svc.update_cache(all_items)

if __name__ == '__main__':
    main()
