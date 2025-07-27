import multiprocessing
from app.concurrent.futures import ThreadPoolExecutor, as_completed

from app.pipelines.ebay_scraper import EbayScraper
from app.shared.upc_service import CsvUPCService
from app.shared.push_to_sheets import push_to_sheets
from app.pipelines.amazon_scraper import AmazonScraper  # reuse your existing module

def scrape_term(q, ebay, amazon):
    print(f\"🔍 eBay searching for: {q}\")
    items = ebay.search(q, max_pages=2)
    opportunities = []
    for itm in items:
        upc = itm.get('upc')
        ebay_price = itm.get('price')
        amz_price = amazon.get_price(upc)  # implement get_price in your AmazonScraper
        if amz_price and ebay_price:
            margin = (amz_price - ebay_price) / ebay_price
            if margin > 0.3 and ebay_price > 10:
                itm.update({'amazon_price': amz_price, 'margin': margin})
                opportunities.append(itm)
    print(f\"   🏷️ Found {len(opportunities)} arb opportunities for '{q}'\")
    return opportunities

def main():
    # Setup
    upc_svc = CsvUPCService('upc_cache.csv')
    ebay = EbayScraper(upc_service=upc_svc)
    amazon = AmazonScraper(upc_workers=5, headless=True, upc_service=upc_svc)

    # Queries
    queries = [
        'wireless+headphones','fitness+tracker','gaming+keyboard',
        # add your own eBay search terms here
    ]

    # Parallel execution
    cores = multiprocessing.cpu_count()
    workers = min(len(queries), max(1, cores//2))
    print(f\"⚙️ Running eBay pipeline with {workers} workers\")

    all_ops = []
    with ThreadPoolExecutor(max_workers=workers) as exe:
        futures = {exe.submit(scrape_term, q, ebay, amazon): q for q in queries}
        for fut in as_completed(futures):
            all_ops.extend(fut.result())

    # Push results
    push_to_sheets(all_ops, 'eBay_Arbitrage')

    # Update UPC cache
    upc_svc.update_cache(all_ops)

if __name__ == '__main__':
    main()
