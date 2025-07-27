# app/dependencies.py

from typing import Generator
from app.sqlalchemy.orm import Session
from fastapi import Header, HTTPException
from uuid import UUID

# Pull in your SessionLocalâ€”try app.database, fall back to app.db
try:
    from app.database import SessionLocal
except ImportError:
    from app.db import SessionLocal

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_webhook_id(
    x_webhook_id: str = Header(..., alias="X-Webhook-ID")
) -> UUID:
    """
    Expects an HTTP header "X-Webhook-ID: <uuid>".
    Returns a UUID object or raises 400 if invalid.
    """
    try:
        return UUID(x_webhook_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid X-Webhook-ID header")


