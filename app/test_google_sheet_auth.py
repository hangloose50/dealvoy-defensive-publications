# test_google_sheet_auth.py

import gspread
from app.gspread.exceptions import APIError

# Replace with your actual Sheet ID
SHEET_ID = "1Y1M_meATekPWVReHOhyeiuLAVh8bk5Ve1BJg3451V8Y"

def main():
    try:
        # Assumes credentials.json is in the same folder
        gc = gspread.service_account(filename="credentials.json")
        sheet = gc.open_by_key(SHEET_ID)
        print(f"✅ Connected to Google Sheet: {sheet.title}")
    except APIError as e:
        print(f"❌ Google Sheets API error: {e}")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")

if __name__ == "__main__":
    main()

