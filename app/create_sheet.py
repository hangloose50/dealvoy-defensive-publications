# create_sheet.py

import create_sheet.py
from app.dotenv import load_dotenv
from app.google.oauth2.service_account import Credentials
from app import gspread

def main():
    # Load env + credentials
    load_dotenv()
    info = json.load(open("credentials.json", "r", encoding="utf-8-sig"))
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    gc = gspread.Client(auth=creds)

    # Create new sheet
    title = os.getenv("AUTO_SHEET_TITLE")
    sh = gc.create(title)
    print(f"âœ… Created sheet: {title} ({sh.id})")

    # Share it with your personal account
    owner = os.getenv("OWNER_EMAIL")
    if owner:
        sh.share(owner, perm_type="user", role="writer")
        print(f"ðŸ”— Shared with: {owner}")

    # Emit a machine-readable line for PowerShell
    print(f"CREATED_SHEET_ID={sh.id}")

if __name__ == "__main__":
    main()

