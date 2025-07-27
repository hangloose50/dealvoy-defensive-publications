from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Dict, Any
from datetime import datetime

class WebhookRequest(BaseModel):
    """Webhook delivery request"""
    webhook_id: UUID4 = Field(..., description="Target webhook ID")
    items: List[Dict[str, Any]] = Field(..., description="Items to deliver")
    priority: int = Field(default=1, description="Delivery priority")
    
class WebhookResponse(BaseModel):
    """Webhook delivery response"""
    status: str = Field(..., description="Delivery status")
    delivered_count: int = Field(..., description="Items successfully delivered")
    failed_count: int = Field(default=0, description="Items that failed")
    message: str = Field(..., description="Status message")
    
class ScanRequest(BaseModel):
    """Product scan request"""
    image_data: Optional[str] = Field(None, description="Base64 encoded image")
    image_url: Optional[str] = Field(None, description="Image URL")
    ocr_enabled: bool = Field(default=True, description="Enable OCR processing")
    
class ScanResponse(BaseModel):
    """Product scan response"""
    product: Optional[ProductIdentification] = Field(None, description="Identified product")
    prices: List[ProductSnapshot] = Field(default=[], description="Found prices")
    deals: List[PriceDelta] = Field(default=[], description="Deal opportunities")
    processing_time: float = Field(..., description="Processing time in seconds")
