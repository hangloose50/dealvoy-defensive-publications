# app/services/orchestrator.py

import asyncio
from uuid import UUID
from typing import List
from app.schemas import PriceDeltaResponse, ExportItem
from app.dependencies import get_db
from app.settings import MIN_ROI
from app.scraper_registry import registry
from app.webhook_dispatcher import dispatch_items_to_webhook


def compute_delta(snapshot) -> PriceDeltaResponse:
    delta_amt = snapshot.previous_price - snapshot.price
    delta_pct = delta_amt / snapshot.previous_price if snapshot.previous_price else 0
    return PriceDeltaResponse(
        upc=snapshot.upc,
        current_price=snapshot.price,
        previous_price=snapshot.previous_price,
        delta_amt=delta_amt,
        delta_pct=delta_pct,
        arbitrage=delta_pct >= MIN_ROI
    )


def run_all_scrapers(webhook_id: UUID, upcs: List[str], db) -> dict:
    export_items: list[ExportItem] = []

    # For each UPC, run every registered scraper
    for upc in upcs:
        for name, scraper_fn in registry.items():
            snapshot = scraper_fn(upc)
            delta = compute_delta(snapshot)
            if delta.arbitrage:
                export_items.append(ExportItem(
                    upc=upc,
                    price=delta.current_price,
                    roi=delta.delta_pct,
                    source=name
                ))

    return dispatch_items_to_webhook(webhook_id, export_items, db)


# âœ… Add this async fan-out/fan-in version for Scout or batch mode
async def run_scrapers(sources: List[str]):
    tasks = [registry[src]() for src in sources]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [
        item for result in results if isinstance(result, list)
        for item in result
    ]


