import health.bak.py
import health.bak.py
import health.bak.pyquests
from app.dotenv import load_dotenv
from app.google.oauth2.service_account import Credentials
from app import gspread

REQUIRED_KEYS = ["SPREADSHEET_ID"]

def validate_env(dotenv_path=".env"):
    load_dotenv(dotenv_path=dotenv_path)
    missing = []
    for key in REQUIRED_KEYS:
        value = os.getenv(key)
        if not value or value.strip() == "":
            missing.append(key)
    if missing:
        raise ValueError(f"âŒ Missing .env keys: {', '.join(missing)}")
    print("ðŸ“¦ .env keys validated")

def validate_credentials(creds_path="credentials.json"):
    with open(creds_path, "r", encoding="utf-8-sig") as f:
        try:
            info = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"âŒ Could not parse {creds_path}: {e}")
    email = info.get("client_email")
    if not email:
        raise ValueError("âŒ Missing client_email in credentials.json")
    print(f"ðŸ” Using service account: {email}")
    return info

def init_dashboard(dotenv_path=".env", creds_path="credentials.json"):
    validate_env(dotenv_path)
    sheet_id = os.getenv("SPREADSHEET_ID")
    info = validate_credentials(creds_path)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    gc = gspread.Client(auth=creds)

    try:
        sh = gc.open_by_key(sheet_id)
        print(f"ðŸ“„ Connected to sheet: {sh.title}")
    except gspread.exceptions.SpreadsheetNotFound:
        raise ValueError("âŒ Sheet not found â€” check SPREADSHEET_ID and ensure itâ€™s shared with the service account")

    return gc, sh

def ping_webhook(message):
    url = os.getenv("WEBHOOK_URL")
    if not url:
        print("âš ï¸ Skipping webhook: WEBHOOK_URL not set")
        return
    payload = {"text": f"âœ… {message}"}
    try:
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            print(f"ðŸ“¡ Webhook sent: {message}")
        else:
            print(f"âŒ Webhook failed: {res.status_code}")
    except Exception as e:
        print(f"âŒ Webhook error: {e}")

def ensure_headers(sh, headers=None):
    headers = headers or ["ASIN", "UPC", "Title", "Price", "ROI", "Retailer", "Timestamp"]
    sheet = sh.sheet1
    first_row = sheet.row_values(1)
    if first_row != headers:
        sheet.update("A1", [headers])
        print("ðŸ§¾ Headers initialized")
    else:
        print("ðŸ§¾ Headers already present")


