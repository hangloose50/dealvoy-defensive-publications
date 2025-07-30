#!/usr/bin/env python3
"""
BestBuy.com Scraper - Compliant retail scraper for Best Buy products
Uses Best Buy's public product search and respects robots.txt
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

class BestBuyScraper(RetailScraperBase):
    """
    BestBuy.com scraper with compliance and anti-bot features
    """
    
    def __init__(self):
        super().__init__(
            source_name="BestBuy",
            base_url="https://www.bestbuy.com"
        )
        
        # Best Buy specific settings
        self.search_endpoint = "https://www.bestbuy.com/site/searchpage.jsp"
        
        # Update headers for Best Buy
        self.headers.update({
            'Referer': 'https://www.bestbuy.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache'
        })
        
    def search_products(self, query: str, max_results: int = 10) -> List[ProductData]:
        """Search for products on BestBuy.com"""
        products = []
        
        try:
            # Reset session for fresh start
            self.reset_session()
            
            # Check compliance first
            if not self.check_compliance():
                print("❌ BestBuy scraping not allowed by robots.txt")
                return products
            
            # Use Best Buy's search endpoint
            search_url = f"{self.search_endpoint}?st={quote(query)}"
            
            response = self.make_request(search_url)
            
            # If timeout or blocked, retry with Selenium
            if hasattr(response, 'status_code') and response.status_code in [403, 500]:
                print("🔄 Anti-bot/timeout detected, retrying with Selenium...")
                response = self.make_request(search_url, use_selenium=True)
            
            if response.status_code != 200:
                print(f"❌ BestBuy search failed: {response.status_code}")
                return products
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find product cards
            product_cards = soup.find_all('li', class_=re.compile(r'sku-item')) or \
                           soup.find_all('div', class_=re.compile(r'product-item')) or \
                           soup.find_all('article', class_=re.compile(r'product'))
            
            for card in product_cards[:max_results]:
                product = self._parse_product_card(card)
                if product and self.validate_product_data(product):
                    products.append(product)
                    
        except Exception as e:
            print(f"❌ BestBuy search error: {str(e)}")
        
        return products
    
    def _parse_product_card(self, card_element) -> Optional[ProductData]:
        """Parse product information from Best Buy product card"""
        try:
            # Extract title
            title_elem = card_element.find('h4', class_=re.compile(r'sku-title')) or \
                        card_element.find('a', class_=re.compile(r'sku-title')) or \
                        card_element.find('h3') or \
                        card_element.find('a', title=True)
            
            title = None
            if title_elem:
                if title_elem.name == 'a' and title_elem.get('title'):
                    title = title_elem.get('title')
                else:
                    title = title_elem.get_text(strip=True)
            
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
            price_elem = card_element.find('span', class_=re.compile(r'current-price')) or \
                        card_element.find('div', class_=re.compile(r'pricing-price')) or \
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
                image_url = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('data-lazy')
            
            # Check stock status
            stock_elem = card_element.find('button', class_=re.compile(r'add-to-cart')) or \
                        card_element.find('span', text=re.compile(r'out of stock|sold out', re.I))
            
            in_stock = True
            if stock_elem:
                if 'out of stock' in stock_elem.get_text(strip=True).lower() or \
                   'sold out' in stock_elem.get_text(strip=True).lower():
                    in_stock = False
            
            # Extract SKU if available
            sku_elem = card_element.find('span', class_=re.compile(r'sku')) or \
                      card_element.find(attrs={'data-sku': True})
            sku = None
            if sku_elem:
                if sku_elem.get('data-sku'):
                    sku = sku_elem['data-sku']
                else:
                    sku_text = sku_elem.get_text(strip=True)
                    sku_match = re.search(r'sku[:\s]*(\d+)', sku_text, re.I)
                    if sku_match:
                        sku = sku_match.group(1)
            
            return ProductData(
                title=title,
                price=price,
                in_stock=in_stock,
                product_url=product_url,
                image_url=image_url,
                upc=None,  # Will be extracted from product page
                sku=sku,
                source=self.source_name
            )
            
        except Exception as e:
            print(f"❌ Error parsing BestBuy product card: {str(e)}")
            return None
    
    def get_product_details(self, product_url: str) -> Optional[ProductData]:
        """Get detailed product information from Best Buy product page"""
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
            
            return ProductData(
                title=title,
                price=price,
                in_stock=in_stock,
                product_url=product_url,
                image_url=image_url,
                upc=upc,
                sku=sku,
                source=self.source_name
            )
            
        except Exception as e:
            print(f"❌ Error getting BestBuy product details: {str(e)}")
            return None
    
    def _extract_product_title(self, soup) -> Optional[str]:
        """Extract product title from Best Buy product page"""
        selectors = [
            'h1.heading-5.v-fw-regular',
            'h1[data-automation-id="product-title"]',
            'h1.sku-title',
            'h1',
            '.product-title'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return None
    
    def _extract_product_price(self, soup) -> Optional[float]:
        """Extract product price from Best Buy product page"""
        selectors = [
            '.pricing-current-price',
            '.current-price',
            'span[aria-label*="current price"]',
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
        """Extract stock status from Best Buy product page"""
        # Look for stock indicators
        out_of_stock_indicators = [
            'button[disabled]',
            '.btn-disabled',
            '.sold-out'
        ]
        
        for selector in out_of_stock_indicators:
            if soup.select_one(selector):
                return False
        
        # Check for text indicators
        stock_indicators = soup.find_all(text=re.compile(r'out of stock|unavailable|sold out', re.I))
        return len(stock_indicators) == 0
    
    def _extract_product_image(self, soup) -> Optional[str]:
        """Extract main product image from Best Buy product page"""
        selectors = [
            '.primary-image img',
            '.product-image img',
            'img[alt*="product"]',
            '.hero-image img'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get('src') or elem.get('data-src')
        return None
    
    def _extract_sku(self, soup, page_content: str) -> Optional[str]:
        """Extract SKU from Best Buy product page"""
        # Look for SKU in various places
        sku_patterns = [
            r'"sku"[:\s]*"?(\d+)"?',
            r'SKU[:\s]*(\d+)',
            r'sku[:\s]*(\d+)',
            r'modelNumber[:\s]*"([^"]+)"',
            r'model[:\s]*"([^"]+)"'
        ]
        
        for pattern in sku_patterns:
            match = re.search(pattern, page_content, re.IGNORECASE)
            if match:
                return match.group(1)
        
        # Try to find SKU in meta tags
        sku_meta = soup.find('meta', {'property': 'product:retailer_item_id'}) or \
                  soup.find('meta', {'name': 'sku'})
        if sku_meta:
            return sku_meta.get('content')
        
        return None

def scrape_bestbuy(query: str = "electronics", max_results: int = 10) -> List[dict]:
    """Main function to scrape Best Buy products"""
    print(f"🛒 Scraping BestBuy for: {query}")
    
    scraper = BestBuyScraper()
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
            'source': product.source
        }
        product_dicts.append(product_dict)
    
    print(f"✅ Found {len(product_dicts)} BestBuy products")
    return product_dicts

def demo_bestbuy_scraper():
    """Demo the Best Buy scraper"""
    print("🛒 BestBuy Scraper Demo")
    print("=" * 40)
    
    # Test searches
    test_queries = ["laptop", "gaming headset", "smartphone"]
    
    for query in test_queries:
        print(f"\n🔍 Searching for: {query}")
        products = scrape_bestbuy(query, 3)
        
        for i, product in enumerate(products, 1):
            print(f"  {i}. {product['title'][:50]}...")
            print(f"     Price: ${product['price']}")
            print(f"     In Stock: {product['in_stock']}")
            if product['sku']:
                print(f"     SKU: {product['sku']}")

if __name__ == "__main__":
    demo_bestbuy_scraper()
