from utils.health import init_dashboard, ping_webhook, ensure_headers

gc, sh = init_dashboard()
ping_webhook(f"Sourcing sheet ready: {sh.title}")
ensure_headers(sh)
import dashboard_builder.py
import dashboard_builder.py
from app.dotenv import load_dotenv
from app.google.oauth2.service_account import Credentials
from app import gspread

# ✅ Load environment variables
load_dotenv(dotenv_path=".env")
sheet_id = os.getenv("SPREADSHEET_ID")
if not sheet_id:
    raise ValueError("❌ SPREADSHEET_ID is missing from .env")

# ✅ Load service-account credentials
with open("credentials.json", "r", encoding="utf-8-sig") as f:
    try:
        info = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ credentials.json failed to parse: {e}")

email = info.get("client_email")
if not email:
    raise ValueError("❌ client_email missing from credentials.json")
print(f"🔐 Using service account: {email}")

# ✅ Authenticate with scopes
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file"
]
creds = Credentials.from_service_account_info(info, scopes=scopes)
gc = gspread.Client(auth=creds)

# ✅ Try connecting to the sheet
try:
    sh = gc.open_by_key(sheet_id)
    print(f"📄 Connected to sheet: {sh.title}")
except gspread.exceptions.SpreadsheetNotFound:
    raise ValueError("❌ Sheet not found. Check SPREADSHEET_ID and sharing permissions.")

