from pipelines.walmart_scraper import WalmartScraper
from shared.upc_service      import CsvUPCService
from shared.push_to_sheets   import push_to_sheets

def main():
    upc_svc = CsvUPCService()
    scraper = WalmartScraper(upc_service=upc_svc)

    queries = ['laptop stand','portable power bank','gaming mouse',
               'hdmi cable','mechanical keyboard']

    all_items = []
    for q in queries:
        print(f"🔍 Walmart searching for: {q}")
        items = scraper.search(q)
        print(f"   🛒 Retrieved {len(items)} items")
        push_to_sheets(items, 'Walmart')
        all_items.extend(items)

    upc_svc.update_cache(all_items)

if __name__ == '__main__':
    main()
