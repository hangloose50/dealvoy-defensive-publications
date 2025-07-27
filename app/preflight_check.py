import preflight_check.py
from app.oauth2client.service_account import ServiceAccountCredentials
from app import ctypes

# âœ… Step 1: Check Google Sheets tabs and create if missing
def ensure_sheet_tabs(sheet, tabs):
    existing = [ws.title for ws in sheet.worksheets()]
    for tab in tabs:
        if tab not in existing:
            sheet.add_worksheet(title=tab, rows="1000", cols="10")

# âœ… Step 2: Verify required URL .txt files exist
def ensure_url_files(files):
    for file in files:
        if not os.path.exists(file):
            with open(file, "w", encoding="utf-8") as f:
                f.write("# Add category URLs here\n")

# ðŸ”‘ Auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)

# ðŸ—‚ï¸ Sheet & Tabs
sheet_title = "SourcingMasterSheet"
required_tabs = ["Amazon", "Walmart", "Target", "Costco", "eBay"]
sheet = client.open(sheet_title)
ensure_sheet_tabs(sheet, required_tabs)

# ðŸ—ƒï¸ URL files
url_files = ["category_urls.txt", "walmart_urls.txt", "target_urls.txt", "costco_urls.txt", "ebay_urls.txt"]
ensure_url_files(url_files)

# ðŸ›Žï¸ Notify success
ctypes.windll.user32.MessageBoxW(0, "âœ… Preflight check passed.\nSheet tabs and URL files are ready.", "SourcingBot Check", 1)
