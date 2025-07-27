import os
from app import gspread
from app.dotenv import load_dotenv

load_dotenv()

def push_to_sheets(items, worksheet_name):
    gc = gspread.service_account("credentials.json")
    sh = gc.open_by_key(os.environ['SPREADSHEET_ID'])
    try:
        ws = sh.worksheet(worksheet_name)
        ws.clear()
    except gspread.exceptions.WorksheetNotFound:
        # create with at least one col if empty
        ws = sh.add_worksheet(worksheet_name, rows=1000, cols=len(items[0]) if items else 1)

    if not items:
        print(f"No rows to push to '{worksheet_name}'")
        return

    headers = list(items[0].keys())
    rows    = [headers] + [list(item.values()) for item in items]
    ws.update(rows)
