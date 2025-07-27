from app import gspread

# Uses your service-account JSON in credentials.json
gc = gspread.service_account(filename="credentials.json")
sheet_id = "1O0BXpXUieWzfAOidvYqCgD2exYWk-ClNrS_ShFuqRKM"

sh = gc.open_by_key(sheet_id)
sh.share(
    "sourcingbot@unique-antonym-465523-h1.iam.gserviceaccount.com",
    perm_type="user",
    role="writer"
)
print("✅ Sheet shared with service account")
