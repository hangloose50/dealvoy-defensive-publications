# check_visibility.py
import check_visibility.py
from app.google.oauth2.service_account import Credentials
from app.googleapiclient.discovery import build

# Load service account
with open("credentials.json", "r", encoding="utf-8-sig") as f:
    info = json.load(f)
    email = info.get("client_email")
    print(f"ðŸ” Using service account: {email}")

# Authenticate
scopes = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
creds = Credentials.from_service_account_info(info, scopes=scopes)
service = build("drive", "v3", credentials=creds)

# List visible sheets
results = service.files().list(
    q="mimeType='application/vnd.google-apps.spreadsheet'",
    fields="files(id, name)",
    pageSize=10
).execute()

sheets = results.get("files", [])
if not sheets:
    print("âŒ Service account sees no spreadsheets")
else:
    print("ðŸ“‹ Service account can access:")
    for sheet in sheets:
        print(f"  - {sheet['name']} ({sheet['id']})")
