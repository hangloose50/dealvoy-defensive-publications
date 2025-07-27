# seed_webhook.py
from app.db import SessionLocal
from app.models import Webhook

db = SessionLocal()

test_wh = Webhook(
    name="HTTPBin Test",
    endpoint="https://httpbin.org/post",
    active=True
)

db.add(test_wh)
db.commit()
print("âœ… Seeded webhook ID:", test_wh.id)

