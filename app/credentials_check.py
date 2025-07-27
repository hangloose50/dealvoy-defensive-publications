import credentials_check.py

try:
    with open("credentials.json", "r", encoding="utf-8-sig") as f:
        cfg = json.load(f)
    print("âœ… Parsed credentials.json; client_email =", cfg.get("client_email"))
except Exception as e:
    print("âŒ credentials.json parse error:", e)
    sys.exit(1)

