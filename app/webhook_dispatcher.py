from app.models import WebhookLog
from app.schemas import ItemDispatchPayload
from app.sqlalchemy.orm import Session
from uuid import UUID

def dispatch_items_to_webhook(
    webhook_id: UUID,
    items: list[ItemDispatchPayload],
    db: Session
) -> dict:
    dispatched = 0
    failed = 0

    for item in items:
        try:
            log_entry = WebhookLog(
                webhook_id=webhook_id,
                item_upc=item.upc,
                status=202,
                attempts=0,
                response="queued"
            )
            db.add(log_entry)
            dispatched += 1
        except Exception as e:
            print(f"Failed to dispatch {item.upc}: {e}")
            failed += 1

    db.commit()

    return {
        "status": "queued",
        "dispatched": dispatched,
        "failed": failed,
        "message": f"{dispatched} items queued for webhook delivery"
    }


