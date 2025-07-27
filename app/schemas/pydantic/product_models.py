from pydantic import BaseModel, Field, UUID4, HttpUrl
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class ProductSnapshot(BaseModel):
    """Product price snapshot from a retailer"""
    upc: str = Field(..., description="Universal Product Code")
    title: str = Field(..., description="Product title")
    brand: Optional[str] = Field(None, description="Product brand")
    price: Decimal = Field(..., description="Current price")
    previous_price: Optional[Decimal] = Field(None, description="Previous price for comparison")
    currency: str = Field(default="USD", description="Currency code")
    retailer: str = Field(..., description="Retailer name")
    url: Optional[HttpUrl] = Field(None, description="Product URL")
    in_stock: bool = Field(default=True, description="Availability status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Snapshot timestamp")
    
class ProductIdentification(BaseModel):
    """Product identification from OCR/vision"""
    title: str = Field(..., description="Extracted product title")
    brand: Optional[str] = Field(None, description="Identified brand")
    upc: Optional[str] = Field(None, description="Extracted UPC/barcode")
    category: Optional[str] = Field(None, description="Product category")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Identification confidence")
    
class PriceDelta(BaseModel):
    """Price change analysis"""
    upc: str
    current_price: Decimal
    previous_price: Optional[Decimal]
    delta_amount: Decimal
    delta_percentage: float
    is_deal: bool = Field(description="Meets ROI threshold")
    roi_percentage: float
