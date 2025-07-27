#!/usr/bin/env python3
"""
🏷️ Product Matcher - Fuzzy matching for OCR results to product database
Uses OCR data to find product matches with confidence scoring
"""

import json
import re
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher

try:
    from fuzzywuzzy import fuzz, process
    FUZZYWUZZY_AVAILABLE = True
except ImportError:
    FUZZYWUZZY_AVAILABLE = False

class ProductMatcher:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.vision_dir = self.project_path / "app" / "vision"
        self.vision_dir.mkdir(parents=True, exist_ok=True)
        
        # Match results directory
        self.match_results_dir = self.vision_dir / "match_results"
        self.match_results_dir.mkdir(parents=True, exist_ok=True)
        
        # Load product database (stub for now)
        self.product_db = self._load_product_database()
        
    def _load_product_database(self) -> List[Dict]:
        """Load local product database (expandable)"""
        # This would eventually connect to your scraper database
        sample_products = [
            {
                "name": "Apple iPhone 15 Pro",
                "brand": "Apple",
                "upc": "194253434567",
                "model": "A3108",
                "price": "$999.00",
                "category": "Electronics"
            },
            {
                "name": "Samsung Galaxy S24",
                "brand": "Samsung", 
                "upc": "887276742113",
                "model": "SM-S921U",
                "price": "$799.00",
                "category": "Electronics"
            },
            {
                "name": "Nike Air Max 270",
                "brand": "Nike",
                "upc": "193655626234",
                "model": "AH8050",
                "price": "$150.00",
                "category": "Footwear"
            },
            {
                "name": "Adidas Ultraboost 22",
                "brand": "Adidas",
                "upc": "195751473897",
                "model": "GZ0127",
                "price": "$180.00",
                "category": "Footwear"
            }
        ]
        
        return sample_products
    
    def match_by_upc(self, upc: str) -> Optional[Dict]:
        """Exact UPC matching"""
        if not upc:
            return None
            
        # Clean UPC (remove spaces, dashes)
        clean_upc = re.sub(r'[^0-9]', '', upc)
        
        for product in self.product_db:
            if product.get("upc") == clean_upc:
                return {
                    "product": product,
                    "match_type": "upc_exact",
                    "confidence": 100,
                    "matched_field": "upc",
                    "matched_value": upc
                }
        
        return None
    
    def match_by_brand(self, brand: str, threshold: int = 80) -> List[Dict]:
        """Fuzzy brand matching"""
        if not brand or not FUZZYWUZZY_AVAILABLE:
            return []
            
        matches = []
        
        for product in self.product_db:
            product_brand = product.get("brand", "")
            if product_brand:
                similarity = fuzz.ratio(brand.upper(), product_brand.upper())
                if similarity >= threshold:
                    matches.append({
                        "product": product,
                        "match_type": "brand_fuzzy",
                        "confidence": similarity,
                        "matched_field": "brand",
                        "matched_value": brand
                    })
        
        # Sort by confidence
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        return matches
    
    def match_by_name(self, text: str, threshold: int = 70) -> List[Dict]:
        """Fuzzy product name matching"""
        if not text or not FUZZYWUZZY_AVAILABLE:
            return []
            
        matches = []
        
        for product in self.product_db:
            product_name = product.get("name", "")
            if product_name:
                similarity = fuzz.partial_ratio(text.upper(), product_name.upper())
                if similarity >= threshold:
                    matches.append({
                        "product": product,
                        "match_type": "name_fuzzy",
                        "confidence": similarity,
                        "matched_field": "name",
                        "matched_value": text
                    })
        
        # Sort by confidence
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        return matches
    
    def match_by_model(self, model: str, threshold: int = 85) -> List[Dict]:
        """Exact or fuzzy model matching"""
        if not model:
            return []
            
        matches = []
        
        for product in self.product_db:
            product_model = product.get("model", "")
            if product_model:
                # Try exact match first
                if model.upper() == product_model.upper():
                    matches.append({
                        "product": product,
                        "match_type": "model_exact",
                        "confidence": 100,
                        "matched_field": "model",
                        "matched_value": model
                    })
                elif FUZZYWUZZY_AVAILABLE:
                    similarity = fuzz.ratio(model.upper(), product_model.upper())
                    if similarity >= threshold:
                        matches.append({
                            "product": product,
                            "match_type": "model_fuzzy", 
                            "confidence": similarity,
                            "matched_field": "model",
                            "matched_value": model
                        })
        
        # Sort by confidence
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        return matches
    
    def query_amazon_scraper(self, search_term: str) -> Optional[Dict]:
        """Query local Amazon scraper endpoint (stub)"""
        try:
            # This would call your actual scraper API
            # For now, just return a mock response
            
            scraper_endpoint = "http://localhost:8000/api/search"
            
            # Mock response for demonstration
            mock_response = {
                "query": search_term,
                "results": [
                    {
                        "title": f"Product matching '{search_term}'",
                        "price": "$XX.XX",
                        "rating": "4.5/5",
                        "availability": "In Stock",
                        "source": "amazon_mock"
                    }
                ],
                "search_time": "150ms",
                "result_count": 1
            }
            
            return mock_response
            
        except Exception as e:
            return {
                "error": f"Scraper query failed: {str(e)}",
                "query": search_term
            }
    
    def match_ocr_data(self, ocr_result: Dict) -> Dict:
        """Main matching function - processes OCR data through all matchers"""
        if not isinstance(ocr_result, dict) or "filtered_data" not in ocr_result:
            return {
                "status": "error",
                "message": "Invalid OCR result format"
            }
        
        filtered_data = ocr_result["filtered_data"]
        all_matches = []
        search_queries = []
        
        print("🏷️ [ProductMatcher] Starting product matching...")
        
        # 1. Try UPC matching first (highest confidence)
        upcs = filtered_data.get("upcs", [])
        for upc_data in upcs:
            upc = upc_data["value"]
            match = self.match_by_upc(upc)
            if match:
                all_matches.append(match)
                print(f"   ✅ UPC Match: {match['product']['name']} (100% confidence)")
        
        # 2. Try brand matching
        brands = filtered_data.get("brands", [])
        for brand_data in brands:
            brand = brand_data["value"]
            matches = self.match_by_brand(brand, threshold=75)
            all_matches.extend(matches)
            if matches:
                print(f"   🏭 Brand Matches: {len(matches)} found for '{brand}'")
        
        # 3. Try model matching  
        models = filtered_data.get("models", [])
        for model_data in models:
            model = model_data["value"]
            matches = self.match_by_model(model, threshold=80)
            all_matches.extend(matches)
            if matches:
                print(f"   🔧 Model Matches: {len(matches)} found for '{model}'")
        
        # 4. Try general text matching
        product_texts = filtered_data.get("product_text", [])
        for text_data in product_texts:
            text = text_data["value"]
            if len(text) > 3:  # Skip very short text
                matches = self.match_by_name(text, threshold=60)
                all_matches.extend(matches[:2])  # Limit to top 2 matches
                search_queries.append(text)
        
        # 5. Remove duplicates and sort by confidence
        unique_matches = {}
        for match in all_matches:
            product_name = match["product"]["name"]
            if product_name not in unique_matches or match["confidence"] > unique_matches[product_name]["confidence"]:
                unique_matches[product_name] = match
        
        final_matches = list(unique_matches.values())
        final_matches.sort(key=lambda x: x["confidence"], reverse=True)
        
        # 6. Query scraper for additional results
        scraper_results = []
        for query in search_queries[:3]:  # Limit queries
            result = self.query_amazon_scraper(query)
            if result and "error" not in result:
                scraper_results.append(result)
        
        # Compile final result
        match_result = {
            "timestamp": datetime.now().isoformat(),
            "ocr_source": ocr_result.get("source", "unknown"),
            "local_matches": final_matches,
            "scraper_queries": scraper_results,
            "match_summary": {
                "total_matches": len(final_matches),
                "best_match": final_matches[0] if final_matches else None,
                "confidence_score": final_matches[0]["confidence"] if final_matches else 0,
                "match_types": list(set([m["match_type"] for m in final_matches]))
            },
            "status": "success"
        }
        
        return match_result
    
    def run_matching_pipeline(self, ocr_result: Dict, save_results: bool = True) -> Dict:
        """Complete matching pipeline with logging"""
        print("🏷️ [ProductMatcher] Running matching pipeline...")
        
        # Run matching
        match_result = self.match_ocr_data(ocr_result)
        
        if match_result.get("status") != "success":
            return match_result
        
        # Save results
        if save_results:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            result_file = self.match_results_dir / f"match_result_{timestamp}.json"
            with open(result_file, 'w') as f:
                json.dump(match_result, f, indent=2)
            print(f"📄 Match results saved: {result_file}")
        
        # Print summary
        summary = match_result.get("match_summary", {})
        best_match = summary.get("best_match")
        
        print("\n🏷️ Product Matching Results:")
        print(f"   📊 Total Matches: {summary.get('total_matches', 0)}")
        print(f"   🎯 Best Match: {best_match['product']['name'] if best_match else 'None'}")
        print(f"   ⭐ Confidence: {summary.get('confidence_score', 0)}%")
        print(f"   🔍 Match Types: {', '.join(summary.get('match_types', []))}")
        
        if best_match:
            product = best_match["product"]
            print(f"   🏭 Brand: {product.get('brand', 'Unknown')}")
            print(f"   💰 Price: {product.get('price', 'Unknown')}")
            print(f"   🏷️ UPC: {product.get('upc', 'Unknown')}")
        
        return match_result

def main():
    """Test the product matching pipeline"""
    # Create a sample OCR result for testing
    sample_ocr = {
        "source": "test",
        "filtered_data": {
            "upcs": [{"value": "194253434567", "confidence": 95}],
            "brands": [{"value": "APPLE", "confidence": 90}],
            "models": [{"value": "A3108", "confidence": 85}],
            "product_text": [{"value": "iPhone 15 Pro", "confidence": 80}]
        }
    }
    
    matcher = ProductMatcher()
    result = matcher.run_matching_pipeline(sample_ocr)
    
    if result.get("status") == "success":
        print("\n✅ ProductMatcher pipeline test successful!")
    else:
        print(f"\n❌ ProductMatcher pipeline failed: {result.get('message')}")
        
    return 0 if result.get("status") == "success" else 1

if __name__ == "__main__":
    exit(main())
