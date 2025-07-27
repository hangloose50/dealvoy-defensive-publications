import os
from app.sourcing_tool.amazon_scraper import AmazonScraper
from app.services.upc_service import CsvUPCService
from app import gspread

# ——— Google Sheets setup ———
# Make sure you have a credentials.json for service_account()
# and have set the SPREADSHEET_ID env var to your sheet’s ID.
gc = gspread.service_account(filename="credentials.json")
sh = gc.open_by_key(os.environ["SPREADSHEET_ID"])

from app import gspread
from app.gspread.exceptions import WorksheetNotFound

def get_or_create(ws_key, title, rows=1000, cols=20):
    try:
        return ws_key.worksheet(title)
    except WorksheetNotFound:
        return ws_key.add_worksheet(title=title, rows=rows, cols=cols)

def push_to_sheets(rows, worksheet_name):
    if not rows:
        print(f"ℹ️ No rows to push to '{worksheet_name}'")
        return

    ws = get_or_create(sh, worksheet_name)
    values = [list(r.values()) for r in rows]
    ws.append_rows(values, value_input_option="RAW")
    print(f"✅ Appended {len(values)} rows to '{worksheet_name}'")
    """
    Appends each row (values only) into the given worksheet.
    """
    if not rows:
        print(f"ℹ️ No rows to push to '{worksheet_name}'")
        return

    ws = sh.worksheet(worksheet_name)
    values = [list(r.values()) for r in rows]
    ws.append_rows(values, value_input_option="RAW")
    print(f"✅ Appended {len(values)} rows to '{worksheet_name}'")

def main():
    # 1) Setup scraper & CSV‐backed UPC cache
    upc_svc = CsvUPCService("upc_cache.csv")
    scraper = AmazonScraper(upc_workers=5, headless=True, upc_service=upc_svc)

    # 2) Your new search terms
    queries = [
      "laptop+stand","portable+power+bank","gaming+mouse","bluetooth+speaker",
      "wireless+charger","mechanical+keyboard","noise+cancelling+headphones",
      "smart+watch","external+ssd","hdmi+cable"
    ]

    all_items = []
    for q in queries:
        display = q.replace("+"," ")
        print(f"🔍 Searching for: {display}")
        items = scraper.search(q, max_pages=2)
        print(f"   🛒 Retrieved {len(items)} items")
        all_items.extend(items)

    # 3) Split complete vs missing‐UPC
    complete = [i for i in all_items if i.get("upc")]
    missing  = [i for i in all_items if not i.get("upc")]

    print(f"📤 Pushing {len(complete)} complete‐UPC rows")
    push_to_sheets(complete, "Amazon")

    print(f"⚠️ Pushing {len(missing)} missing‐UPC rows")
    push_to_sheets(missing, "Amazon Missing UPC")

    # 4) Persist any new UPCs back to CSV
    upc_svc.update_cache(all_items)
    print("💾 Updated upc_cache.csv")

if __name__ == "__main__":
    main()
