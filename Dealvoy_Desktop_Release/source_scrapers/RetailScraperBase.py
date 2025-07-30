#!/usr/bin/env python3
"""
RetailScraperBase - Modular base class for retail source scrapers
Provides standardized scraping framework with compliance and anti-bot features
"""

import time
import random
import requests
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

@dataclass
class ProductData:
    """Standardized product data structure"""
    title: str
    price: Optional[float]
    in_stock: bool
    product_url: str
    image_url: Optional[str]
    upc: Optional[str]
    sku: Optional[str]
    source: str
    category: Optional[str] = None
    brand: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    sale_price: Optional[float] = None
    shipping_info: Optional[str] = None

class RobotsTxtChecker:
    """Check robots.txt compliance before scraping"""
    
    @staticmethod
    def can_fetch(base_url: str, user_agent: str = "*") -> bool:
        """Check if scraping is allowed by robots.txt"""
        try:
            robots_url = urljoin(base_url, "/robots.txt")
            response = requests.get(robots_url, timeout=5)
            
            if response.status_code == 200:
                robots_content = response.text.lower()
                # Simple robots.txt parsing - look for disallow rules
                lines = robots_content.split('\n')
                
                current_user_agent = None
                for line in lines:
                    line = line.strip()
                    if line.startswith('user-agent:'):
                        current_user_agent = line.split(':', 1)[1].strip()
                    elif line.startswith('disallow:') and (current_user_agent == '*' or current_user_agent == user_agent.lower()):
                        disallowed_path = line.split(':', 1)[1].strip()
                        if disallowed_path == '/':
                            return False
                            
            return True
        except:
            # If can't fetch robots.txt, assume scraping is allowed
            return True

class RetailScraperBase(ABC):
    """
    Base class for retail source scrapers with built-in compliance and anti-bot features
    """
    
    def __init__(self, source_name: str, base_url: str):
        self.source_name = source_name
        self.base_url = base_url
        self.session = requests.Session()
        self.driver = None
        
        # Rate limiting settings
        self.min_delay = 1.0
        self.max_delay = 3.0
        self.request_count = 0
        self.last_request_time = 0
        
        # Headers to mimic real browser with enhanced anti-bot measures
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
        }
        self.session.headers.update(self.headers)
        
    def check_compliance(self) -> bool:
        """Check if scraping this source is compliant with robots.txt"""
        return RobotsTxtChecker.can_fetch(self.base_url, self.headers['User-Agent'])
    
    def rate_limit(self):
        """Implement rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_delay:
            sleep_time = random.uniform(self.min_delay, self.max_delay)
            time.sleep(sleep_time)
            
        self.last_request_time = time.time()
        self.request_count += 1
        
        # Longer delay every 10 requests
        if self.request_count % 10 == 0:
            time.sleep(random.uniform(5.0, 10.0))
    
    def get_driver(self) -> webdriver.Chrome:
        """Get undetected Chrome driver for JavaScript-heavy sites"""
        if self.driver is None:
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            # Removed problematic/deprecated options for compatibility
            # options.add_experimental_option("excludeSwitches", ["enable-automation"])
            # options.add_experimental_option('useAutomationExtension', False)
            # Use undetected-chromedriver
            self.driver = uc.Chrome(options=options)
            try:
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            except Exception:
                pass
        return self.driver
    
    def close_driver(self):
        """Close the webdriver"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None
    
    def reset_session(self):
        """Reset session and clear all cookies/headers for fresh start"""
        self.close_driver()
        self.session.close()
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.request_count = 0
    
    def make_request(self, url: str, use_selenium: bool = False, retries: int = 3) -> requests.Response:
        """Make a rate-limited, compliant request with enhanced error handling"""
        self.rate_limit()
        
        for attempt in range(retries):
            try:
                if use_selenium:
                    driver = self.get_driver()
                    driver.get(url)
                    time.sleep(random.uniform(2, 5))  # Mimic human behavior
                    
                    # Create a mock response object with page source
                    class MockResponse:
                        def __init__(self, content, status_code=200):
                            self.content = content.encode('utf-8')
                            self.text = content
                            self.status_code = status_code
                    
                    return MockResponse(driver.page_source)
                else:
                    # Enhanced session request with better timeouts and headers
                    response = self.session.get(
                        url, 
                        timeout=(10, 30),  # Connect timeout, read timeout
                        allow_redirects=True,
                        headers={
                            **self.headers,
                            'Referer': self.base_url,
                        }
                    )
                    return response
                    
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, 
                    requests.exceptions.HTTPError) as e:
                print(f"⚠️  Request attempt {attempt + 1} failed: {str(e)}")
                if attempt < retries - 1:
                    sleep_time = random.uniform(2, 5) * (attempt + 1)  # Exponential backoff
                    print(f"🔄 Retrying in {sleep_time:.1f}s...")
                    time.sleep(sleep_time)
                    continue
                else:
                    # Final attempt failed, create a mock failed response
                    class FailedResponse:
                        def __init__(self):
                            self.status_code = 500
                            self.content = b''
                            self.text = ''
                    return FailedResponse()
            except Exception as e:
                print(f"❌ Unexpected error on attempt {attempt + 1}: {str(e)}")
                if attempt < retries - 1:
                    time.sleep(random.uniform(1, 3))
                    continue
                else:
                    class FailedResponse:
                        def __init__(self):
                            self.status_code = 500
                            self.content = b''
                            self.text = ''
                    return FailedResponse()
    
    def extract_price(self, price_text: str) -> Optional[float]:
        """Extract price from text string"""
        if not price_text:
            return None
            
        # Remove common currency symbols and text
        price_clean = price_text.replace('$', '').replace(',', '').replace('USD', '').strip()
        
        # Extract first number that looks like a price
        import re
        price_match = re.search(r'(\d+\.?\d*)', price_clean)
        
        if price_match:
            try:
                return float(price_match.group(1))
            except ValueError:
                return None
        return None
    
    def extract_upc(self, product_page_content: str) -> Optional[str]:
        """Extract UPC from product page content"""
        import re
        
        # Common UPC patterns
        upc_patterns = [
            r'UPC[:\s]*(\d{12,13})',
            r'upc[:\s]*(\d{12,13})',
            r'Universal Product Code[:\s]*(\d{12,13})',
            r'Product Code[:\s]*(\d{12,13})',
            r'Item Number[:\s]*(\d{12,13})',
            r'"upc"[:\s]*"(\d{12,13})"',
            r'"gtin"[:\s]*"(\d{12,13})"'
        ]
        
        for pattern in upc_patterns:
            match = re.search(pattern, product_page_content, re.IGNORECASE)
            if match:
                upc = match.group(1)
                if len(upc) in [12, 13]:  # Valid UPC length
                    return upc
        return None
    
    @abstractmethod
    def search_products(self, query: str, max_results: int = 10) -> List[ProductData]:
        """Search for products on the retail site"""
        pass
    
    @abstractmethod
    def get_product_details(self, product_url: str) -> Optional[ProductData]:
        """Get detailed product information from product page"""
        pass
    
    def scrape_category(self, category_url: str, max_results: int = 50) -> List[ProductData]:
        """Scrape products from a category page"""
        # Default implementation - override in subclasses
        products = []
        try:
            response = self.make_request(category_url)
            if hasattr(response, 'status_code') and response.status_code == 200:
                # Parse category page and extract product URLs
                # This is a placeholder - implement in subclasses
                pass
        except Exception as e:
            print(f"Error scraping category {category_url}: {str(e)}")
        
        return products
    
    def validate_product_data(self, product: ProductData) -> bool:
        """Validate that product data meets minimum requirements"""
        required_fields = ['title', 'product_url', 'source']
        
        for field in required_fields:
            if not getattr(product, field):
                return False
                
        # Price validation
        if product.price is not None and (product.price < 0 or product.price > 100000):
            return False
            
        return True
    
    def get_scraper_info(self) -> Dict[str, Any]:
        """Get information about this scraper"""
        return {
            "name": self.source_name,
            "base_url": self.base_url,
            "compliance_checked": self.check_compliance(),
            "requests_made": self.request_count,
            "status": "active"
        }

# Example implementation for testing
class TestRetailScraper(RetailScraperBase):
    """Test implementation of the retail scraper base"""
    
    def __init__(self):
        super().__init__("Test Retailer", "https://example.com")
    
    def search_products(self, query: str, max_results: int = 10) -> List[ProductData]:
        """Mock product search"""
        return [
            ProductData(
                title=f"Sample Product for {query}",
                price=29.99,
                in_stock=True,
                product_url="https://example.com/product/1",
                image_url="https://example.com/image/1.jpg",
                upc="123456789012",
                sku="SKU123",
                source=self.source_name
            )
        ]
    
    def get_product_details(self, product_url: str) -> Optional[ProductData]:
        """Mock product details"""
        return ProductData(
            title="Sample Product Details",
            price=29.99,
            in_stock=True,
            product_url=product_url,
            image_url="https://example.com/image/1.jpg",
            upc="123456789012",
            sku="SKU123",
            source=self.source_name,
            brand="Sample Brand",
            rating=4.5,
            review_count=100
        )

def demo_scraper_base():
    """Demo the scraper base functionality"""
    print("🔧 Retail Scraper Base Demo")
    print("=" * 40)
    
    # Test scraper
    scraper = TestRetailScraper()
    
    # Check compliance
    print(f"Compliance Check: {scraper.check_compliance()}")
    
    # Test search
    products = scraper.search_products("test query", 5)
    print(f"Search Results: {len(products)} products found")
    
    # Test validation
    for product in products:
        is_valid = scraper.validate_product_data(product)
        print(f"Product Valid: {is_valid}")
    
    # Get scraper info
    info = scraper.get_scraper_info()
    print(f"Scraper Info: {info}")
    
    return products

if __name__ == "__main__":
    demo_scraper_base()
