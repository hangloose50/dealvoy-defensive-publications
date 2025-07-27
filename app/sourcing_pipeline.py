from app import subprocess
from app import datetime
from app import csv
import sourcing_pipeline.py
from app import ctypes
from app import gspread
from app.oauth2client.service_account import ServiceAccountCredentials
from app.gspread.exceptions import SpreadsheetNotFound

# 1) Authenticate with Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)

# 2) Open your sheet by its ID (replace with your real ID)
SHEET_ID = "1YIM_meATekPWvREhOhyeiuLAVh8bk5Ve1BJg34J51V8"
try:
    sheet = client.open_by_key(SHEET_ID)
except SpreadsheetNotFound:
    # fallback: create a new sheet if not found
    sheet = client.create("SourcingMasterSheet")
    SHEET_ID = sheet.id
    sheet = client.open_by_key(SHEET_ID)
    ctypes.windll.user32.MessageBoxW(
        0,
        "âš ï¸ Original sheet not found.\nCreated new sheet: SourcingMasterSheet",
        "SourcingBot Notice",
        0
    )

# 3) Ensure the required worksheet tabs exist
required_tabs = ["Amazon", "Walmart", "Target", "Costco", "eBay"]
existing_tabs = [ws.title for ws in sheet.worksheets()]
for tab in required_tabs:
    if tab not in existing_tabs:
        sheet.add_worksheet(title=tab, rows="1000", cols="10")

# 4) Ensure the URL files exist (create blank ones if missing)
url_files = [
    "category_urls.txt",
    "walmart_urls.txt",
    "target_urls.txt",
    "costco_urls.txt",
    "ebay_urls.txt"
]
for fn in url_files:
    if not os.path.exists(fn):
        with open(fn, "w", encoding="utf-8") as f:
            f.write("# Paste one URL per line\n")

# 5) Run each scraper and the ASIN converter
for script in [
    "scraper.py",
    "ta_converter.py",
    "walmart_scraper.py",
    "target_scraper.py",
    "costco_scraper.py",
    "ebay_scraper.py"
]:
    subprocess.run(["python", script], check=True)

# 6) Push each CSV into its corresponding sheet tab
def push_csv(tab_name, headers, csv_path):
    ws = sheet.worksheet(tab_name)
    ws.clear()
    ws.append_row(headers)
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            ws.append_row(row)

push_csv("Amazon",  ["ASIN", "Title", "Price"],                     "multi_category_asins.csv")
push_csv("Walmart", ["Title", "Price", "SKU", "Product URL", "Image URL"], "walmart_products.csv")
push_csv("Target",  ["Title", "Price", "SKU", "Product URL"],        "target_products.csv")
push_csv("Costco",  ["Title", "Price", "SKU", "Product URL"],        "costco_products.csv")
push_csv("eBay",    ["Title", "Price", "Product URL"],               "ebay_products.csv")

# 7) Write a timestamped log file
now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
os.makedirs("Logs", exist_ok=True)
with open(f"Logs/log_{now}.txt", "w", encoding="utf-8") as log:
    log.write(f"Sourcing run completed at {now}\n")
    log.write(f"Data pushed to sheet ID {SHEET_ID}\n")

# 8) Display a Windows desktop notification on success
ctypes.windll.user32.MessageBoxW(
    0,
    "âœ… Sourcing run complete.\nCheck your Google Sheet & Logs folder.",
    "SourcingBot",
    1
)
