# check_webhook_logs.py
from app.db import SessionLocal
from app.models import WebhookLog

db = SessionLocal()
logs = db.query(WebhookLog).order_by(WebhookLog.timestamp.desc()).limit(5).all()

for log in logs:
    print(f"[{log.timestamp}] UPC: {log.item_upc} â†’ Status: {log.status}, Attempts: {log.attempts}")
    print(f"Response:\n{log.response}\n---")

