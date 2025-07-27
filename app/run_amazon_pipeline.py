#!/usr/bin/env python
import run_amazon_pipeline.py
import run_amazon_pipeline.py
import run_amazon_pipeline.py

# 1) Make project root importable so `app/` resolves
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# 2) Bring in your scraper entrypoint and schema
from app.services.scrapers.amazon_scraper import scrape_amazon
from app.schemas import PriceSnapshot

def main(upc: str):
    # run the scraper
    snapshot: PriceSnapshot = scrape_amazon(upc)
    # model_dump() returns a dict with every field (upc, price, previous_price, roi)
    print(json.dumps(snapshot.model_dump()))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_amazon_pipeline.py <UPC>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])



