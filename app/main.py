from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, UUID4, HttpUrl
from typing import List
import httpx
import traceback

from app.schemas import (
    SubscribeRequest,
    SubscribeResponse,
    ExportItem,
    WebhookExportResponse,
)
from app.services.scrapers.amazon_scraper import scrape_amazon

# Enable debug so uncaught errors return tracebacks
app = FastAPI(debug=True)

# In-memory store of subscriptions
subscriptions: dict[UUID4, SubscribeRequest] = {}

# Catch-all exception handler (returns JSON with traceback)
@app.exception_handler(Exception)
async def all_exceptions(request: Request, exc: Exception):
    tb = traceback.format_exc()
    print("Unhandled exception:\n", tb)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "detail": str(exc), "traceback": tb}
    )

@app.post("/subscribe", response_model=SubscribeResponse)
async def subscribe(req: SubscribeRequest):
    if req.webhook_id in subscriptions:
        raise HTTPException(400, "webhook_id already registered")
    subscriptions[req.webhook_id] = req
    return SubscribeResponse(
        status="success",
        webhook_id=req.webhook_id,
        threshold=req.threshold
    )

@app.post("/scrape/", response_model=WebhookExportResponse)
async def scrape_endpoint(
    upcs: List[str],
    x_webhook_id: UUID4 = Header(..., alias="X-Webhook-ID")
):
    # 1) Validate subscription
    if x_webhook_id not in subscriptions:
        raise HTTPException(404, "Subscription not found")
    sub = subscriptions[x_webhook_id]

    # 2) Scrape & filter by ROI
    items: List[ExportItem] = []
    for upc in upcs:
        snap = scrape_amazon(upc)
        if snap.roi >= sub.threshold:
            items.append(ExportItem(upc=snap.upc, price=snap.price, roi=snap.roi))

    if not items:
        return WebhookExportResponse(
            status="no_items", dispatched=0, failed=0,
            message="No items met the threshold"
        )

            # 3) Dispatch to subscriber URL
    try:
        # force a pure Python str
        url = str(sub.url)
        print(f"Dispatching to URL (type={type(url)}): {url}")

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                url,
                json={"items": [i.model_dump() for i in items]},
                timeout=10.0
            )
            resp.raise_for_status()
    except Exception as exc:
        import traceback
        tb = traceback.format_exc()
        print("Dispatch exception:\n", tb)
        return WebhookExportResponse(
            status="failure",
            dispatched=0,
            failed=len(items),
            message=f"Dispatch error: {exc!r}"
        )

    # Success
    return WebhookExportResponse(
        status="success",
        dispatched=len(items),
        failed=0,
        message=f"{len(items)} item(s) dispatched"
    )
@app.post("/webhook-debug")
async def webhook_debug(request: Request):
    """
    Receives any POST, logs the JSON body, and echoes it back.
    """
    payload = await request.json()
    print("ðŸ’¥ Received webhook payload:", payload)
    return {"status": "received", "payload": payload}
from app.api import image_upload
app.include_router(image_upload.router)




