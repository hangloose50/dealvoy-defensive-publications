#!/usr/bin/env python3
"""
HomeDepot.com Scraper - Compliant retail scraper for Home Depot products
Uses Home Depot's public product search and respects robots.txt
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

class HomeDepotScraper(RetailScraperBase):
    """
    HomeDepot.com scraper with compliance and anti-bot features
    """
    
    def __init__(self):
        super().__init__(
            source_name="HomeDepot",
            base_url="https://www.homedepot.com"
        )
        
        # Home Depot specific settings
        self.search_endpoint = "https://www.homedepot.com/s/"
        
        # Update headers for Home Depot
        self.headers.update({
            'Referer': 'https://www.homedepot.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        })
        
    def search_products(self, query: str, max_results: int = 10) -> List[ProductData]:
        """Search for products on HomeDepot.com"""
        products = []
        
        try:
            # Reset session for fresh start
            self.reset_session()
            
            # Check compliance first
            if not self.check_compliance():
                print("❌ HomeDepot scraping not allowed by robots.txt")
                return products
            
            # Use Home Depot's search endpoint
            search_url = f"{self.search_endpoint}{quote(query)}"
            
            response = self.make_request(search_url)
            if response.status_code != 200:
                print(f"❌ HomeDepot search failed: {response.status_code}")
                return products
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find product cards - Home Depot uses pods
            product_cards = soup.find_all('div', class_=re.compile(r'browse-search__pod|product-pod')) or \
                           soup.find_all('article', attrs={'data-testid': re.compile(r'product')}) or \
                           soup.find_all('div', attrs={'data-automation-id': re.compile(r'product')})
            
            for card in product_cards[:max_results]:
                product = self._parse_product_card(card)
                if product and self.validate_product_data(product):
                    products.append(product)
                    
        except Exception as e:
            print(f"❌ HomeDepot search error: {str(e)}")
        
        return products
    
    def _parse_product_card(self, card_element) -> Optional[ProductData]:
        """Parse product information from Home Depot product card"""
        try:
            # Extract title - Home Depot uses specific class patterns
            title_elem = card_element.find('span', class_=re.compile(r'product-title|product-header')) or \
                        card_element.find('a', class_=re.compile(r'product-title')) or \
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
            
            # Extract price - Home Depot uses specific price classes
            price_elem = card_element.find('span', class_=re.compile(r'price-format__main-price')) or \
                        card_element.find('div', class_=re.compile(r'price')) or \
                        card_element.find('span', class_=re.compile(r'price'))
            
            price = None
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price = self.extract_price(price_text)
            
            # Extract image
            img_elem = card_element.find('img', class_=re.compile(r'product-image')) or \
                      card_element.find('img')
            image_url = None
            if img_elem:
                image_url = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('data-lazy-src')
                # Handle relative URLs
                if image_url and image_url.startswith('/'):
                    image_url = urljoin(self.base_url, image_url)
            
            # Check stock status
            stock_elem = card_element.find('span', class_=re.compile(r'fulfillment|availability')) or \
                        card_element.find(text=re.compile(r'out of stock|unavailable', re.I))
            
            in_stock = True
            if stock_elem:
                if hasattr(stock_elem, 'get_text'):
                    stock_text = stock_elem.get_text(strip=True).lower()
                else:
                    stock_text = str(stock_elem).lower()
                in_stock = 'out of stock' not in stock_text and 'unavailable' not in stock_text
            
            # Extract model number (common for Home Depot)
            model_elem = card_element.find('span', class_=re.compile(r'model')) or \
                        card_element.find('div', class_=re.compile(r'model'))
            model = model_elem.get_text(strip=True) if model_elem else None
            
            return ProductData(
                title=title,
                price=price,
                in_stock=in_stock,
                product_url=product_url,
                image_url=image_url,
                upc=None,  # Will be extracted from product page
                sku=model,  # Use model number as SKU
                source=self.source_name
            )
            
        except Exception as e:
            print(f"❌ Error parsing HomeDepot product card: {str(e)}")
            return None
    
    def get_product_details(self, product_url: str) -> Optional[ProductData]:
        """Get detailed product information from Home Depot product page"""
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
            print(f"❌ Error getting HomeDepot product details: {str(e)}")
            return None
    
    def _extract_product_title(self, soup) -> Optional[str]:
        """Extract product title from Home Depot product page"""
        selectors = [
            'h1[data-automation-id="product-title"]',
            'h1.product-title',
            'h1',
            '.product-header h1',
            '[data-testid="product-title"]'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return None
    
    def _extract_product_price(self, soup) -> Optional[float]:
        """Extract product price from Home Depot product page"""
        selectors = [
            '.price-format__main-price',
            '.price-current',
            '.current-price',
            '.price',
            '[data-automation-id*="price"]'
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
        """Extract stock status from Home Depot product page"""
        # Look for stock indicators
        out_of_stock_selectors = [
            '.availability--unavailable',
            '.out-of-stock',
            '[data-automation-id*="unavailable"]'
        ]
        
        for selector in out_of_stock_selectors:
            if soup.select_one(selector):
                return False
        
        # Check for text indicators
        stock_indicators = soup.find_all(text=re.compile(r'out of stock|unavailable|sold out|not available online', re.I))
        return len(stock_indicators) == 0
    
    def _extract_product_image(self, soup) -> Optional[str]:
        """Extract main product image from Home Depot product page"""
        selectors = [
            '.mediagallery__mainimage img',
            '.product-image img',
            '.hero-image img',
            'img[data-automation-id*="product-image"]'
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
        """Extract brand from Home Depot product page"""
        selectors = [
            '[data-automation-id="product-brand"]',
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
        """Extract model number or SKU from Home Depot product page"""
        # Look for model number in various places
        model_patterns = [
            r'"model"[:\s]*"?([^"]+)"?',
            r'Model[:\s#]*([A-Za-z0-9\-_]+)',
            r'model[:\s#]*([A-Za-z0-9\-_]+)',
            r'"sku"[:\s]*"?([^"]+)"?',
            r'SKU[:\s#]*([A-Za-z0-9\-_]+)'
        ]
        
        for pattern in model_patterns:
            match = re.search(pattern, page_content, re.IGNORECASE)
            if match:
                return match.group(1)
        
        # Try to find model in specific elements
        model_selectors = [
            '[data-automation-id*="model"]',
            '.model-number',
            '.sku-number',
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

def scrape_homedepot(query: str = "tools", max_results: int = 10) -> List[dict]:
    """Main function to scrape Home Depot products"""
    print(f"🔨 Scraping HomeDepot for: {query}")
    
    scraper = HomeDepotScraper()
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
    
    print(f"✅ Found {len(product_dicts)} HomeDepot products")
    return product_dicts

def demo_homedepot_scraper():
    """Demo the Home Depot scraper"""
    print("🔨 HomeDepot Scraper Demo")
    print("=" * 40)
    
    # Test searches
    test_queries = ["drill", "paint", "lumber"]
    
    for query in test_queries:
        print(f"\n🔍 Searching for: {query}")
        products = scrape_homedepot(query, 3)
        
        for i, product in enumerate(products, 1):
            print(f"  {i}. {product['title'][:50]}...")
            print(f"     Price: ${product['price']}")
            print(f"     In Stock: {product['in_stock']}")
            if product['sku']:
                print(f"     Model: {product['sku']}")

if __name__ == "__main__":
    demo_homedepot_scraper()
