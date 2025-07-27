from sqlalchemy import Column, Integer, String, Decimal, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class Product(Base):
    """Product master table"""
    __tablename__ = 'products'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    upc = Column(String(20), unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    brand = Column(String(100))
    category = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PriceHistory(Base):
    """Price tracking history"""
    __tablename__ = 'price_history'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_upc = Column(String(20), nullable=False, index=True)
    retailer = Column(String(100), nullable=False)
    price = Column(Decimal(10, 2), nullable=False)
    url = Column(Text)
    in_stock = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

class WebhookLog(Base):
    """Webhook delivery logs"""
    __tablename__ = 'webhook_logs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    webhook_id = Column(UUID(as_uuid=True), nullable=False)
    payload = Column(Text, nullable=False)
    status_code = Column(Integer)
    response = Column(Text)
    attempts = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
