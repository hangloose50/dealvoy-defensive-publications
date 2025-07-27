from fastapi import APIRouter, Depends
from app.sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.schemas import PriceDeltaResponse, WebhookExportResponse, ExportItem
from app.webhook_dispatcher import dispatch_items_to_webhook
from app.dependencies import get_db, get_webhook_id
from app.settings import MIN_ROI

router = APIRouter(prefix="/price", tags=["price"])

@router.post("/ingest", response_model=WebhookExportResponse)
def ingest_price_deltas(
    deltas: List[PriceDeltaResponse],
    db: Session = Depends(get_db),
    webhook_id: UUID = Depends(get_webhook_id)
):
    items_to_dispatch = [
        ExportItem(upc=d.upc, price=d.current_price, roi=d.delta_pct)
        for d in deltas
        if d.arbitrage and d.delta_pct >= MIN_ROI
    ]

    if not items_to_dispatch:
        return WebhookExportResponse(
            status="no_dispatch", dispatched=0, failed=0,
            message="No items met ROI threshold"
        )

    result = dispatch_items_to_webhook(webhook_id, items_to_dispatch, db)
    return WebhookExportResponse(**result)


