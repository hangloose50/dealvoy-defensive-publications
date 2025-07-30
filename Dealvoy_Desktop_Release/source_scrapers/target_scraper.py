#!/usr/bin/env python3
"""
Target.com Scraper - Compliant retail scraper for Target products
Uses Target's public product search and respects robots.txt
"""


import json
import re
import time
from typing import List, Optional
from urllib.parse import quote, urljoin
import requests
from bs4 import BeautifulSoup

# Bulletproof import for RetailScraperBase
import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
from RetailScraperBase import RetailScraperBase, ProductData

class TargetScraper(RetailScraperBase):
    """
    Target.com scraper with compliance and anti-bot features
    """
    
    def __init__(self):
        super().__init__(
            source_name="Target",
            base_url="https://www.target.com"
        )
        
        # Target-specific settings
        self.search_endpoint = "https://www.target.com/s"
        self.api_endpoint = "https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2"
        
        # Update headers for Target
        self.headers.update({
            'Referer': 'https://www.target.com/',
            'Accept': 'application/json, text/plain, */*',
            'X-Requested-With': 'XMLHttpRequest'
        })
        
    def search_products(self, query: str, max_results: int = 10) -> List[ProductData]:
        """Search for products on Target.com"""
        products = []
        
        try:
            # Reset session for fresh start
            self.reset_session()
            
            # Check compliance first
            if not self.check_compliance():
                print("❌ Target scraping not allowed by robots.txt")
                return products
            
            # Use Target's search endpoint
            search_url = f"{self.search_endpoint}?searchTerm={quote(query)}"
            
            response = self.make_request(search_url)
            if response.status_code != 200:
                print(f"❌ Target search failed: {response.status_code}")
                return products
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find product cards
            product_cards = soup.find_all('div', {'data-test': 'product-card'}) or \
                           soup.find_all('div', class_=re.compile(r'ProductCard'))
            
            for card in product_cards[:max_results]:
                product = self._parse_product_card(card)
                if product and self.validate_product_data(product):
                    products.append(product)
                    
        except Exception as e:
            print(f"❌ Target search error: {str(e)}")
        
        return products
    
    def _parse_product_card(self, card_element) -> Optional[ProductData]:
        """Parse product information from Target product card"""
        try:
            # Extract title
            title_elem = card_element.find('a', {'data-test': 'product-title'}) or \
                        card_element.find('h3') or \
                        card_element.find('div', class_=re.compile(r'title|name', re.I))
            
            title = title_elem.get_text(strip=True) if title_elem else None
            if not title:
                return None
            
            # Extract product URL
            url_elem = card_element.find('a', href=True)
            product_url = None
            if url_elem:
                href = url_elem['href']
                if href.startswith('/'):
                    product_url = urljoin(self.base_url, href)
                else:
                    product_url = href
            
            # Extract price
            price_elem = card_element.find('span', {'data-test': 'product-price'}) or \
                        card_element.find('span', class_=re.compile(r'price', re.I))
            
            price = None
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price = self.extract_price(price_text)
            
            # Extract image
            img_elem = card_element.find('img')
            image_url = img_elem.get('src') or img_elem.get('data-src') if img_elem else None
            
            # Check stock status
            stock_elem = card_element.find('span', {'data-test': 'fulfillment-shipping'}) or \
                        card_element.find('div', class_=re.compile(r'stock|availability', re.I))
            
            in_stock = True  # Default to in stock
            if stock_elem:
                stock_text = stock_elem.get_text(strip=True).lower()
                in_stock = 'out of stock' not in stock_text and 'unavailable' not in stock_text
            
            # Extract brand if available
            brand_elem = card_element.find('span', {'data-test': 'product-brand'}) or \
                        card_element.find('div', class_=re.compile(r'brand', re.I))
            brand = brand_elem.get_text(strip=True) if brand_elem else None
            
            return ProductData(
                title=title,
                price=price,
                in_stock=in_stock,
                product_url=product_url,
                image_url=image_url,
                upc=None,  # Will be extracted from product page
                sku=None,
                source=self.source_name,
                brand=brand
            )
            
        except Exception as e:
            print(f"❌ Error parsing Target product card: {str(e)}")
            return None
    
    def get_product_details(self, product_url: str) -> Optional[ProductData]:
        """Get detailed product information from Target product page"""
        try:
            response = self.make_request(product_url)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract detailed information
            title = self._extract_product_title(soup)
            price = self._extract_product_price(soup)
            in_stock = self._extract_stock_status(soup)
            image_url = self._extract_product_image(soup)
            upc = self.extract_upc(response.text)
            brand = self._extract_brand(soup)
            
            # Extract SKU/TCIN (Target's internal ID)
            sku = self._extract_tcin(soup, response.text)
            
            return ProductData(
                title=title,
                price=price,
                in_stock=in_stock,
                product_url=product_url,
                image_url=image_url,
                upc=upc,
                sku=sku,
                source=self.source_name,
                brand=brand
            )
            
        except Exception as e:
            print(f"❌ Error getting Target product details: {str(e)}")
            return None
    
    def _extract_product_title(self, soup) -> Optional[str]:
        """Extract product title from Target product page"""
        selectors = [
            'h1[data-test="product-title"]',
            'h1.ProductTitle',
            'h1',
            '[data-test="product-title"]'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return None
    
    def _extract_product_price(self, soup) -> Optional[float]:
        """Extract product price from Target product page"""
        selectors = [
            '[data-test="product-price"]',
            '.ProductPrice',
            '[class*="price"]',
            '.price'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                price_text = elem.get_text(strip=True)
                price = self.extract_price(price_text)
                if price:
                    return price
        return None
    
    def _extract_stock_status(self, soup) -> bool:
        """Extract stock status from Target product page"""
        # Look for stock indicators
        stock_indicators = soup.find_all(text=re.compile(r'out of stock|unavailable|sold out', re.I))
        return len(stock_indicators) == 0
    
    def _extract_product_image(self, soup) -> Optional[str]:
        """Extract main product image from Target product page"""
        selectors = [
            'img[data-test="product-image"]',
            '.ProductImages img',
            '.product-image img',
            'img[alt*="product"]'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get('src') or elem.get('data-src')
        return None
    
    def _extract_brand(self, soup) -> Optional[str]:
        """Extract brand from Target product page"""
        selectors = [
            '[data-test="product-brand"]',
            '.ProductBrand',
            '[class*="brand"]'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return None
    
    def _extract_tcin(self, soup, page_content: str) -> Optional[str]:
        """Extract TCIN (Target's SKU) from product page"""
        # Look for TCIN in various places
        tcin_patterns = [
            r'"tcin"[:\s]*"?(\d+)"?',
            r'TCIN[:\s]*(\d+)',
            r'tcin[:\s]*(\d+)',
            r'product_id[:\s]*"?(\d+)"?'
        ]
        
        for pattern in tcin_patterns:
            match = re.search(pattern, page_content, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

def scrape_target(query: str = "electronics", max_results: int = 10) -> List[dict]:
    """Main function to scrape Target products"""
    print(f"🎯 Scraping Target for: {query}")
    
    scraper = TargetScraper()
    products = scraper.search_products(query, max_results)
    
    # Convert to dict format for compatibility
    product_dicts = []
    for product in products:
        product_dict = {
            'title': product.title,
            'price': product.price,
            'in_stock': product.in_stock,
            'url': product.product_url,
            'image': product.image_url,
            'upc': product.upc,
            'sku': product.sku,
            'source': product.source,
            'brand': product.brand
        }
        product_dicts.append(product_dict)
    
    print(f"✅ Found {len(product_dicts)} Target products")
    return product_dicts

def demo_target_scraper():
    """Demo the Target scraper"""
    print("🎯 Target Scraper Demo")
    print("=" * 40)
    
    # Test searches
    test_queries = ["wireless headphones", "coffee maker", "laptop"]
    
    for query in test_queries:
        print(f"\n🔍 Searching for: {query}")
        products = scrape_target(query, 3)
        
        for i, product in enumerate(products, 1):
            print(f"  {i}. {product['title'][:50]}...")
            print(f"     Price: ${product['price']}")
            print(f"     In Stock: {product['in_stock']}")
            print(f"     Brand: {product.get('brand', 'N/A')}")

if __name__ == "__main__":
    demo_target_scraper()
