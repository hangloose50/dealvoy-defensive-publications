from pipelines.frontiercoop_scraper import FrontierCoopScraper
from shared.upc_service              import CsvUPCService
from shared.push_to_sheets           import push_to_sheets

def main():
    upc_svc  = CsvUPCService()
    scraper  = FrontierCoopScraper(upc_service=upc_svc)

    queries = ['organic+tea', 'essential+oil', 'bulk+spices']

    all_items = []
    for q in queries:
        print(f"🔍 FrontierCoop searching for: {q}")
        items = scraper.search(q)
        print(f"   🛒 Retrieved {len(items)} items")
        push_to_sheets(items, f"FrontierCoop_{q.split('+')[0].capitalize()}")
        all_items.extend(items)

    upc_svc.update_cache(all_items)

if __name__ == '__main__':
    main()
