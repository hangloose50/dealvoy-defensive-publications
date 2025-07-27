from app.sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Text
from app.sqlalchemy.dialects.postgresql import UUID
from app.db import Base
from app import uuid
from datetime import datetime

class Webhook(Base):
    __tablename__ = "webhooks"

    id       = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name     = Column(String)
    endpoint = Column(String)
    active   = Column(Boolean, default=True)

class WebhookLog(Base):
    __tablename__ = "webhook_logs"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    webhook_id  = Column(UUID(as_uuid=True), ForeignKey("webhooks.id"))
    item_upc    = Column(String, nullable=False)
    status      = Column(Integer, nullable=True)
    attempts    = Column(Integer, default=0)
    response    = Column(Text)
    timestamp   = Column(DateTime, default=datetime.utcnow)


