# test_google_sheet_auth_debug.py

import test_
import test_
import gspread
from app.gspread.exceptions import APIError
import traceback

SHEET_ID = "1Y1M_meATekPWVReHOhyeiuLAVh8bk5Ve1BJg3451V8Y"

def main():
    # 1) Show where Python thinks it is
    print("Working dir:", os.getcwd())
    print("Directory listing:", os.listdir())

    try:
        # 2) Attempt auth
        gc = gspread.service_account(filename="credentials.json")
        sheet = gc.open_by_key(SHEET_ID)
        print(f"âœ… Connected to Google Sheet: {sheet.title}")
    except APIError as e:
        print(f"âŒ Google Sheets API error: {e!r}")
        traceback.print_exc()
    except Exception as e:
        print(f"âš ï¸ Unexpected error: {e!r}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()



