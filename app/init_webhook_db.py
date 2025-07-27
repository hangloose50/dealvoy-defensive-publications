from app.db import Base, engine
from app.models import Webhook, WebhookLog  # ensure BOTH are imported

Base.metadata.create_all(bind=engine)

print("âœ… Tables created.")

