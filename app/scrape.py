# app/routers/scrape.py

from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID

from app.orchestrator import run_all_scrapers
from app.dependencies import get_db, get_webhook_id

router = APIRouter(prefix="/scrape", tags=["scrape"])

@router.post("/", response_model=dict)
def scrape_and_ingest(
    upcs: List[str],
    db = Depends(get_db),
    webhook_id: UUID = Depends(get_webhook_id)
):
    """
    Run all registered scrapers against each UPC,
    compute deltas, and dispatch qualifying items.
    """
    return run_all_scrapers(webhook_id, upcs, db)


