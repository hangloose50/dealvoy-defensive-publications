# pipeline.py
# ─────────────────────────────────────────────────
from app.amazon import scrape_amazon
from app.push_to_sheets import push_to_sheet, SHEET_ID

def run_amazon_pipeline(query, worksheet="Amazon", max_pages=None):
    mode = "auto" if max_pages is None else max_pages
    print(f"🔍 Amazon → '{query}' (pages={mode})")

    products = scrape_amazon(query, max_pages=max_pages)
    if not products:
        print("⚠️ No products found.")
        return

    # Format rows: [ASIN, Title, $Price, UPC]
    rows = []
    for p in products:
        row = [p["asin"], p["title"], f"${p['price']:.2f}"]
        if p.get("upc") is not None:
            row.append(p["upc"] or "")
        rows.append(row)

    push_to_sheet(SHEET_ID, rows, worksheet)

if __name__ == "__main__":
    # ───── YOUR CONFIG ─────
    query     = "usb+charger"
    worksheet = "Amazon"

    # Option A: scrape exactly 30 pages
    max_pages = 30

    # Option B: scrape ALL pages (auto-detect last page)
    # max_pages = None
    # ─────────────────────────

    run_amazon_pipeline(query, worksheet, max_pages)

