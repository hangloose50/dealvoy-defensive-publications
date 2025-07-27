#!/usr/bin/env python3
"""
🗃️ SchemaVoyager - Generates schemas from data patterns
Creates Pydantic, SQL, or JSON schemas from input/output data analysis
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class SchemaVoyager:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.schemas_dir = self.project_path / "app" / "schemas"
        self.schemas_dir.mkdir(parents=True, exist_ok=True)
        
    def analyze_existing_schemas(self):
        """Analyze existing schema files for patterns"""
        patterns = []
        
        schema_file = self.project_path / "app" / "schemas.py"
        if schema_file.exists():
            with open(schema_file, 'r') as f:
                content = f.read()
                # Extract class definitions
                classes = re.findall(r'class (\w+)\([^)]*\):', content)
                patterns.extend(classes)
                
        return patterns
    
    def detect_data_patterns(self):
        """Scan codebase for data structures that need schemas"""
        data_patterns = []
        
        # Look for common data patterns in Python files
        for py_file in self.project_path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Look for dict/JSON patterns
                dict_patterns = re.findall(r'{\s*["\'](\w+)["\']:', content)
                for pattern in dict_patterns:
                    if pattern not in ['__name__', '__main__', 'self']:
                        data_patterns.append({
                            'type': 'dict_field',
                            'name': pattern,
                            'file': str(py_file)
                        })
                        
                # Look for API response patterns
                if 'price' in content.lower() and 'upc' in content.lower():
                    data_patterns.append({
                        'type': 'product_data',
                        'file': str(py_file)
                    })
                    
                if 'webhook' in content.lower():
                    data_patterns.append({
                        'type': 'webhook_data', 
                        'file': str(py_file)
                    })
                    
            except Exception:
                continue
                
        return data_patterns
    
    def generate_pydantic_schemas(self):
        """Generate Pydantic model schemas"""
        schemas = {}
        
        # Product-related schemas
        schemas["product_models.py"] = '''from pydantic import BaseModel, Field, UUID4, HttpUrl
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
'''

        # Webhook and API schemas
        schemas["api_models.py"] = '''from pydantic import BaseModel, Field, UUID4
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
'''

        # Database schemas
        schemas["db_models.py"] = '''from sqlalchemy import Column, Integer, String, Decimal, DateTime, Boolean, Text
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
'''

        return schemas
    
    def generate_json_schemas(self):
        """Generate JSON schema definitions"""
        schemas = {}
        
        schemas["product.schema.json"] = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Product Snapshot",
            "type": "object",
            "properties": {
                "upc": {"type": "string", "pattern": "^[0-9]{8,14}$"},
                "title": {"type": "string", "minLength": 1},
                "brand": {"type": "string"},
                "price": {"type": "number", "minimum": 0},
                "previous_price": {"type": "number", "minimum": 0},
                "currency": {"type": "string", "default": "USD"},
                "retailer": {"type": "string", "minLength": 1},
                "url": {"type": "string", "format": "uri"},
                "in_stock": {"type": "boolean", "default": True},
                "timestamp": {"type": "string", "format": "date-time"}
            },
            "required": ["upc", "title", "price", "retailer"],
            "additionalProperties": False
        }
        
        schemas["scan_response.schema.json"] = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Scan Response",
            "type": "object",
            "properties": {
                "product": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "brand": {"type": "string"},
                        "upc": {"type": "string"},
                        "category": {"type": "string"},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1}
                    }
                },
                "prices": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/product_snapshot"}
                },
                "processing_time": {"type": "number", "minimum": 0}
            },
            "definitions": {
                "product_snapshot": {
                    "$ref": "product.schema.json"
                }
            }
        }
        
        return schemas
    
    def save_schemas(self, schema_type, schemas):
        """Save generated schemas to files"""
        saved_files = []
        
        type_dir = self.schemas_dir / schema_type
        type_dir.mkdir(exist_ok=True)
        
        for filename, content in schemas.items():
            file_path = type_dir / filename
            
            if filename.endswith('.json'):
                with open(file_path, 'w') as f:
                    json.dump(content, f, indent=2)
            else:
                with open(file_path, 'w') as f:
                    f.write(content)
                    
            saved_files.append(str(file_path))
            
        return saved_files
    
    def run(self):
        """Main execution function"""
        print("🗃️ [SchemaVoyager] Analyzing data patterns for schema generation...")
        
        # Analyze existing patterns
        existing = self.analyze_existing_schemas()
        data_patterns = self.detect_data_patterns()
        
        print(f"   Found {len(existing)} existing schemas")
        print(f"   Detected {len(data_patterns)} data patterns")
        
        # Generate schemas
        print("🗃️ [SchemaVoyager] Generating optimized schemas...")
        
        pydantic_schemas = self.generate_pydantic_schemas()
        json_schemas = self.generate_json_schemas()
        
        # Save schemas
        pydantic_files = self.save_schemas("pydantic", pydantic_schemas)
        json_files = self.save_schemas("json", json_schemas)
        
        print("✅ SchemaVoyager: Generated schemas:")
        print("   📝 Pydantic Models:")
        for file_path in pydantic_files:
            print(f"      {file_path}")
        print("   📋 JSON Schemas:")
        for file_path in json_files:
            print(f"      {file_path}")
            
        # Generate migration script
        migration_script = self.schemas_dir / "create_tables.sql"
        with open(migration_script, 'w') as f:
            f.write('''-- Auto-generated database migration
-- Generated by SchemaVoyager

CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    upc VARCHAR(20) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    brand VARCHAR(100),
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_upc ON products(upc);

CREATE TABLE IF NOT EXISTS price_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_upc VARCHAR(20) NOT NULL,
    retailer VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    url TEXT,
    in_stock BOOLEAN DEFAULT TRUE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_price_history_upc ON price_history(product_upc);
CREATE INDEX idx_price_history_timestamp ON price_history(timestamp);

CREATE TABLE IF NOT EXISTS webhook_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    webhook_id UUID NOT NULL,
    payload TEXT NOT NULL,
    status_code INTEGER,
    response TEXT,
    attempts INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')
        
        print(f"   🗄️ {migration_script}")
        print("🗃️ [SchemaVoyager] Ready for data modeling!")

def run():
    """CLI entry point"""
    voyager = SchemaVoyager()
    voyager.run()

if __name__ == "__main__":
    run()
