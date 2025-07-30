#!/usr/bin/env python3
"""
Lowes.com Scraper - Compliant retail scraper for Lowe's products
Uses Lowe's public product search and respects robots.txt
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

class LowesScraper(RetailScraperBase):
    """
    Lowes.com scraper with compliance and anti-bot features
    """
    
    def __init__(self):
        super().__init__(
            source_name="Lowes",
            base_url="https://www.lowes.com"
        )
        
        # Lowe's specific settings
        self.search_endpoint = "https://www.lowes.com/search"
        
        # Update headers for Lowe's
        self.headers.update({
            'Referer': 'https://www.lowes.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        })
        
    def search_products(self, query: str, max_results: int = 10) -> List[ProductData]:
        """Search for products on Lowes.com"""
        products = []
        
        try:
            # Reset session for fresh start
            self.reset_session()
            
            # Check compliance first
            if not self.check_compliance():
                print("❌ Lowes scraping not allowed by robots.txt")
                return products
            
            # Use Lowe's search endpoint
            search_url = f"{self.search_endpoint}?searchTerm={quote(query)}"
            
            response = self.make_request(search_url)
            
            # If blocked (403), retry with Selenium
            if hasattr(response, 'status_code') and response.status_code in [403, 500]:
                print("🔄 Anti-bot detection (403/500), retrying with Selenium...")
                response = self.make_request(search_url, use_selenium=True)
            
            if response.status_code != 200:
                print(f"❌ Lowes search failed: {response.status_code}")
                return products
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find product cards - Lowe's uses specific patterns
            product_cards = soup.find_all('div', class_=re.compile(r'srp-item|product-item|plp-product')) or \
                           soup.find_all('article', attrs={'data-testid': re.compile(r'product')}) or \
                           soup.find_all('div', attrs={'data-itemid': True})
            
            for card in product_cards[:max_results]:
                product = self._parse_product_card(card)
                if product and self.validate_product_data(product):
                    products.append(product)
                    
        except Exception as e:
            print(f"❌ Lowes search error: {str(e)}")
        
        return products
    
    def _parse_product_card(self, card_element) -> Optional[ProductData]:
        """Parse product information from Lowe's product card"""
        try:
            # Extract title - Lowe's uses various title patterns
            title_elem = card_element.find('h3', class_=re.compile(r'product-title|item-title')) or \
                        card_element.find('a', class_=re.compile(r'product-title')) or \
                        card_element.find('span', class_=re.compile(r'product-title')) or \
                        card_element.find('h3') or \
                        card_element.find('h4')
            
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
            
            # Extract price - Lowe's uses specific price formats
            price_elem = card_element.find('span', class_=re.compile(r'sr-price|current-price|price-current')) or \
                        card_element.find('div', class_=re.compile(r'price')) or \
                        card_element.find('span', string=re.compile(r'^\$[\d,.]+'))
            
            price = None
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price = self.extract_price(price_text)
            
            # Extract image
            img_elem = card_element.find('img', class_=re.compile(r'product-image|item-image')) or \
                      card_element.find('img')
            image_url = None
            if img_elem:
                image_url = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('data-lazy-src')
                # Handle relative URLs
                if image_url and image_url.startswith('/'):
                    image_url = urljoin(self.base_url, image_url)
            
            # Check stock status
            stock_elem = card_element.find('span', class_=re.compile(r'availability|stock-status')) or \
                        card_element.find(text=re.compile(r'out of stock|unavailable|sold out', re.I))
            
            in_stock = True
            if stock_elem:
                if hasattr(stock_elem, 'get_text'):
                    stock_text = stock_elem.get_text(strip=True).lower()
                else:
                    stock_text = str(stock_elem).lower()
                in_stock = 'out of stock' not in stock_text and 'unavailable' not in stock_text
            
            # Extract model number (common for Lowe's)
            model_elem = card_element.find('span', class_=re.compile(r'model|item-number')) or \
                        card_element.find('div', class_=re.compile(r'model'))
            model = model_elem.get_text(strip=True) if model_elem else None
            
            # Extract brand
            brand_elem = card_element.find('span', class_=re.compile(r'brand')) or \
                        card_element.find('div', class_=re.compile(r'brand'))
            brand = brand_elem.get_text(strip=True) if brand_elem else None
            
            return ProductData(
                title=title,
                price=price,
                in_stock=in_stock,
                product_url=product_url,
                image_url=image_url,
                upc=None,  # Will be extracted from product page
                sku=model,  # Use model number as SKU
                source=self.source_name,
                brand=brand
            )
            
        except Exception as e:
            print(f"❌ Error parsing Lowes product card: {str(e)}")
            return None
    
    def get_product_details(self, product_url: str) -> Optional[ProductData]:
        """Get detailed product information from Lowe's product page"""
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
            sku = self._extract_model_sku(soup, response.text)
            brand = self._extract_brand(soup)
            
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
            print(f"❌ Error getting Lowes product details: {str(e)}")
            return None
    
    def _extract_product_title(self, soup) -> Optional[str]:
        """Extract product title from Lowe's product page"""
        selectors = [
            'h1[data-testid="product-title"]',
            'h1.product-title',
            'h1',
            '.pdp-product-name h1',
            '[data-automation-id="product-title"]'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return None
    
    def _extract_product_price(self, soup) -> Optional[float]:
        """Extract product price from Lowe's product page"""
        selectors = [
            '.price-current',
            '.current-price',
            '.sr-price',
            '.price',
            '[data-testid*="price"]'
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
        """Extract stock status from Lowe's product page"""
        # Look for stock indicators
        out_of_stock_selectors = [
            '.out-of-stock',
            '.unavailable',
            '[data-testid*="unavailable"]'
        ]
        
        for selector in out_of_stock_selectors:
            if soup.select_one(selector):
                return False
        
        # Check for text indicators
        stock_indicators = soup.find_all(text=re.compile(r'out of stock|unavailable|sold out|not available', re.I))
        return len(stock_indicators) == 0
    
    def _extract_product_image(self, soup) -> Optional[str]:
        """Extract main product image from Lowe's product page"""
        selectors = [
            '.product-image img',
            '.hero-image img',
            '.pdp-image img',
            'img[data-testid*="product-image"]'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                img_url = elem.get('src') or elem.get('data-src')
                if img_url and img_url.startswith('/'):
                    img_url = urljoin(self.base_url, img_url)
                return img_url
        return None
    
    def _extract_brand(self, soup) -> Optional[str]:
        """Extract brand from Lowe's product page"""
        selectors = [
            '[data-testid="product-brand"]',
            '.brand-name',
            '.product-brand',
            '.brand'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return None
    
    def _extract_model_sku(self, soup, page_content: str) -> Optional[str]:
        """Extract model number or SKU from Lowe's product page"""
        # Look for model number in various places
        model_patterns = [
            r'"model"[:\s]*"?([^"]+)"?',
            r'Model[:\s#]*([A-Za-z0-9\-_]+)',
            r'model[:\s#]*([A-Za-z0-9\-_]+)',
            r'"itemNumber"[:\s]*"?([^"]+)"?',
            r'Item[:\s#]*([A-Za-z0-9\-_]+)'
        ]
        
        for pattern in model_patterns:
            match = re.search(pattern, page_content, re.IGNORECASE)
            if match:
                return match.group(1)
        
        # Try to find model in specific elements
        model_selectors = [
            '[data-testid*="model"]',
            '.model-number',
            '.item-number',
            '.product-model'
        ]
        
        for selector in model_selectors:
            elem = soup.select_one(selector)
            if elem:
                model_text = elem.get_text(strip=True)
                # Extract alphanumeric model from text
                model_match = re.search(r'([A-Za-z0-9\-_]+)', model_text)
                if model_match:
                    return model_match.group(1)
        
        return None

def scrape_lowes(query: str = "appliances", max_results: int = 10) -> List[dict]:
    """Main function to scrape Lowe's products"""
    print(f"🏠 Scraping Lowes for: {query}")
    
    scraper = LowesScraper()
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
    
    print(f"✅ Found {len(product_dicts)} Lowes products")
    return product_dicts

def demo_lowes_scraper():
    """Demo the Lowe's scraper"""
    print("🏠 Lowes Scraper Demo")
    print("=" * 40)
    
    # Test searches
    test_queries = ["refrigerator", "garden tools", "lighting"]
    
    for query in test_queries:
        print(f"\n🔍 Searching for: {query}")
        products = scrape_lowes(query, 3)
        
        for i, product in enumerate(products, 1):
            print(f"  {i}. {product['title'][:50]}...")
            print(f"     Price: ${product['price']}")
            print(f"     In Stock: {product['in_stock']}")
            if product['brand']:
                print(f"     Brand: {product['brand']}")

if __name__ == "__main__":
    demo_lowes_scraper()
