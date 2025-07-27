from fastapi import APIRouter, Depends, HTTPException, Query
from app.sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db import get_db
from app.models import WebhookLog
from app.schemas import (
    WebhookExportRequest,
    WebhookExportResponse,
    WebhookLogEntry,
    WebhookLogsResponse
)

router = APIRouter(prefix="/api/v1/webhook", tags=["webhook"])

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# POST /export â€” queue items for delivery via webhook
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

@router.post(
    "/export",
    response_model=WebhookExportResponse,
    summary="Queue items for delivery to the webhook endpoint",
)
def export_items(
    request: WebhookExportRequest,
    db: Session = Depends(get_db),
):
    dispatched, failed = 0, 0

    for item in request.items:
        log_entry = WebhookLog(
            webhook_id=request.webhook_id,
            item_upc=item.upc,
            status=202,
            attempts=0,
            response="queued"
        )
        try:
            db.add(log_entry)
            dispatched += 1
        except Exception as e:
            failed += 1

    db.commit()

    return WebhookExportResponse(
        status="queued",
        dispatched=dispatched,
        failed=failed,
        message=f"{dispatched} items queued for webhook dispatch"
    )

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# GET /logs â€” fetch recent delivery logs for a webhook
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

@router.get(
    "/logs",
    response_model=WebhookLogsResponse,
    summary="Fetch recent webhook delivery logs",
)
def get_webhook_logs(
    webhook_id: UUID,
    limit: int = Query(25, gt=0, le=100),
    db: Session = Depends(get_db),
):
    logs = (
        db.query(WebhookLog)
          .filter(WebhookLog.webhook_id == webhook_id)
          .order_by(WebhookLog.timestamp.desc())
          .limit(limit)
          .all()
    )
    if not logs:
        raise HTTPException(404, detail=f"No logs found for webhook_id {webhook_id}")
    return WebhookLogsResponse(
        logs=[WebhookLogEntry.model_validate(log, from_attributes=True) for log in logs]


    )



