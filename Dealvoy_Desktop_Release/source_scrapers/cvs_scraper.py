#!/usr/bin/env python3
"""
CVS.com Scraper - Compliant retail scraper for CVS products
Uses CVS's public product search and respects robots.txt
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

class CVSScraper(RetailScraperBase):
    """
    CVS.com scraper with compliance and anti-bot features
    """
    
    def __init__(self):
        super().__init__(
            source_name="CVS",
            base_url="https://www.cvs.com"
        )
        
        # CVS specific settings
        self.search_endpoint = "https://www.cvs.com/shop"
        
        # Update headers for CVS
        self.headers.update({
            'Referer': 'https://www.cvs.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        })
        
    def search_products(self, query: str, max_results: int = 10) -> List[ProductData]:
        """Search for products on CVS.com, with Selenium fallback if blocked"""
        products = []
        try:
            # Reset session for fresh start
            self.reset_session()
            
            # Check compliance first
            if not self.check_compliance():
                print("❌ CVS scraping not allowed by robots.txt")
                return products
            # Use CVS's search endpoint
            search_url = f"{self.search_endpoint}?searchTerm={quote(query)}"
            response = self.make_request(search_url)
            
            # If blocked or got header overflow, retry with Selenium
            if (hasattr(response, 'status_code') and response.status_code in [403, 500]) or \
               (hasattr(response, 'text') and 'got more than 100 headers' in str(response)):
                print("🔄 Anti-bot detection triggered, retrying with Selenium...")
                # Set US geolocation headers/cookies in Selenium
                driver = self.get_driver()
                driver.get(search_url)
                # Clear cookies before setting new ones to avoid overflow
                try:
                    # Step 1: Open base URL, set cookies, then go to search URL
                    driver.get(self.base_url)
                    time.sleep(2)
                    try:
                        cookies = [c['name'] for c in driver.get_cookies()]
                        if 'CVS_LOCALE' not in cookies:
                            driver.add_cookie({'name': 'CVS_LOCALE', 'value': 'US', 'domain': '.cvs.com'})
                        if 'CVS_COUNTRY' not in cookies:
                            driver.add_cookie({'name': 'CVS_COUNTRY', 'value': 'US', 'domain': '.cvs.com'})
                    except Exception as e:
                        print(f"Cookie set error: {e}")
                    driver.get(search_url)
                    time.sleep(5)
                    page_source = driver.page_source
                    # Save page source for debugging
                    with open('/tmp/cvs_selenium_debug.html', 'w', encoding='utf-8') as f:
                        f.write(page_source)
                    print("[DEBUG] Saved Selenium page source to /tmp/cvs_selenium_debug.html")
                    soup = BeautifulSoup(page_source, 'html.parser')
                except Exception as e:
                    print(f"Selenium fallback error: {e}")
            elif hasattr(response, 'content'):
                soup = BeautifulSoup(response.content, 'html.parser')
            else:
                print(f"❌ CVS search failed: {getattr(response, 'status_code', 'unknown')}")
                return products
            # Find product cards - Updated for current US CVS.com structure
            product_cards = soup.find_all('li', {'data-testid': re.compile(r'^product-tile-')})
            if not product_cards:
                product_cards = soup.find_all('div', class_=re.compile(r'product-item|product-card'))
            if not product_cards:
                product_cards = soup.find_all('article', class_=re.compile(r'product'))
            if not product_cards:
                product_cards = soup.find_all('div', attrs={'data-testid': re.compile(r'product')})
            for card in product_cards[:max_results]:
                product = self._parse_product_card(card)
                if product and self.validate_product_data(product):
                    products.append(product)
        except Exception as e:
            print(f"❌ CVS search error: {str(e)}")
        finally:
            self.close_driver()
        return products
    
    def _parse_product_card(self, card_element) -> Optional[ProductData]:
        """Parse product information from CVS product card (updated selectors)"""
        try:
            # Extract title
            title_elem = card_element.find('p', {'data-testid': 'product-title'})
            if not title_elem:
                title_elem = card_element.find('h3')
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
            price_elem = card_element.find('span', {'data-testid': 'product-price'})
            if not price_elem:
                price_elem = card_element.find('span', class_=re.compile(r'price'))
            price = None
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price = self.extract_price(price_text)
            # Extract image
            img_elem = card_element.find('img', {'data-testid': 'product-image'})
            if not img_elem:
                img_elem = card_element.find('img')
            image_url = None
            if img_elem:
                image_url = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('data-lazy-src')
                if image_url and image_url.startswith('/'):
                    image_url = urljoin(self.base_url, image_url)
            # Check stock status
            stock_elem = card_element.find(text=re.compile(r'out of stock|unavailable|sold out', re.I))
            in_stock = stock_elem is None
            # Extract brand if available
            brand_elem = card_element.find('span', class_=re.compile(r'brand')) or \
                        card_element.find('div', class_=re.compile(r'brand'))
            brand = brand_elem.get_text(strip=True) if brand_elem else None
            return ProductData(
                title=title,
                price=price,
                in_stock=in_stock,
                product_url=product_url,
                image_url=image_url,
                upc=None,
                sku=None,
                source=self.source_name,
                brand=brand
            )
        except Exception as e:
            print(f"❌ Error parsing CVS product card: {str(e)}")
            return None
    
    def get_product_details(self, product_url: str) -> Optional[ProductData]:
        """Get detailed product information from CVS product page"""
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
            sku = self._extract_sku(soup, response.text)
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
            print(f"❌ Error getting CVS product details: {str(e)}")
            return None
    
    def _extract_product_title(self, soup) -> Optional[str]:
        """Extract product title from CVS product page"""
        selectors = [
            'h1[data-testid="product-title"]',
            'h1.product-title',
            'h1',
            '.product-name h1',
            '[data-testid*="title"] h1'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return None
    
    def _extract_product_price(self, soup) -> Optional[float]:
        """Extract product price from CVS product page"""
        selectors = [
            '[data-testid*="price"]',
            '.price-current',
            '.current-price',
            '.price',
            '.product-price'
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
        """Extract stock status from CVS product page"""
        # Look for out of stock indicators
        out_of_stock_selectors = [
            '[data-testid*="out-of-stock"]',
            '.out-of-stock',
            '.unavailable'
        ]
        
        for selector in out_of_stock_selectors:
            if soup.select_one(selector):
                return False
        
        # Check for text indicators
        stock_indicators = soup.find_all(text=re.compile(r'out of stock|unavailable|sold out|not available', re.I))
        return len(stock_indicators) == 0
    
    def _extract_product_image(self, soup) -> Optional[str]:
        """Extract main product image from CVS product page"""
        selectors = [
            '.product-image img',
            '[data-testid*="image"] img',
            '.hero-image img',
            'img[alt*="product"]'
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
        """Extract brand from CVS product page"""
        selectors = [
            '[data-testid*="brand"]',
            '.brand-name',
            '.product-brand',
            '.brand'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return None
    
    def _extract_sku(self, soup, page_content: str) -> Optional[str]:
        """Extract SKU from CVS product page"""
        # Look for SKU in various places
        sku_patterns = [
            r'"sku"[:\s]*"?([^"]+)"?',
            r'SKU[:\s]*([A-Za-z0-9]+)',
            r'sku[:\s]*([A-Za-z0-9]+)',
            r'product_id[:\s]*"?([^"]+)"?',
            r'itemId[:\s]*"?([^"]+)"?'
        ]
        
        for pattern in sku_patterns:
            match = re.search(pattern, page_content, re.IGNORECASE)
            if match:
                return match.group(1)
        
        # Try to find SKU in meta tags or data attributes
        sku_elem = soup.find(attrs={'data-sku': True}) or \
                  soup.find('meta', {'name': 'sku'}) or \
                  soup.find('span', class_=re.compile(r'sku'))
        
        if sku_elem:
            if sku_elem.get('data-sku'):
                return sku_elem['data-sku']
            elif sku_elem.get('content'):
                return sku_elem['content']
            else:
                sku_text = sku_elem.get_text(strip=True)
                sku_match = re.search(r'sku[:\s]*([A-Za-z0-9]+)', sku_text, re.I)
                if sku_match:
                    return sku_match.group(1)
        
        return None

def scrape_cvs(query: str = "vitamins", max_results: int = 10) -> List[dict]:
    """Main function to scrape CVS products"""
    print(f"💊 Scraping CVS for: {query}")
    
    scraper = CVSScraper()
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
    
    print(f"✅ Found {len(product_dicts)} CVS products")
    return product_dicts

def demo_cvs_scraper():
    """Demo the CVS scraper"""
    print("💊 CVS Scraper Demo")
    print("=" * 40)
    
    # Test searches
    test_queries = ["pain relief", "vitamins", "skincare"]
    
    for query in test_queries:
        print(f"\n🔍 Searching for: {query}")
        products = scrape_cvs(query, 3)
        
        for i, product in enumerate(products, 1):
            print(f"  {i}. {product['title'][:50]}...")
            print(f"     Price: ${product['price']}")
            print(f"     In Stock: {product['in_stock']}")
            if product['brand']:
                print(f"     Brand: {product['brand']}")

if __name__ == "__main__":
    demo_cvs_scraper()
