#!/usr/bin/env python3
"""
ProductMatcherAI - Advanced product matching and duplicate detection
Tier: Pro+ (Tier 2+)
Role: Customer AI Agent
"""

import json
import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import difflib

@dataclass
class ProductMatch:
    product_id: str
    match_id: str
    confidence: float
    match_type: str  # 'exact', 'variant', 'similar', 'potential'
    differences: List[str]
    price_variance: float

class ProductMatcherAI:
    """
    Advanced AI agent for product matching and duplicate detection
    - Identifies duplicate listings across platforms
    - Detects product variants and bundles
    - Prevents selling conflicts and pricing errors
    """
    
    def __init__(self):
        self.agent_name = "ProductMatcherAI"
        self.tier_requirement = "pro"
        self.category = "product_intelligence"
        self.status = "active"
        self.description = "Identifies duplicate products and variants across platforms"
        
    def find_product_matches(self, target_product: Dict, product_database: List[Dict]) -> Dict:
        """Find potential matches for a target product"""
        
        matches = []
        
        for candidate in product_database:
            match_result = self._compare_products(target_product, candidate)
            if match_result.confidence > 0.5:  # Only include high-confidence matches
                matches.append(match_result)
        
        # Sort by confidence
        matches.sort(key=lambda x: x.confidence, reverse=True)
        
        return {
            "target_product": target_product,
            "matches": [match.__dict__ for match in matches],
            "match_summary": self._generate_match_summary(matches),
            "recommendations": self._generate_match_recommendations(matches),
            "analyzed_at": datetime.datetime.now().isoformat()
        }
    
    def _compare_products(self, product1: Dict, product2: Dict) -> ProductMatch:
        """Compare two products and determine match confidence"""
        
        # Skip self-comparison
        if product1.get('id') == product2.get('id'):
            return ProductMatch(
                product_id=product1.get('id', ''),
                match_id=product2.get('id', ''),
                confidence=0.0,
                match_type='self',
                differences=[],
                price_variance=0.0
            )
        
        confidence_factors = []
        differences = []
        
        # Title similarity
        title_similarity = self._calculate_text_similarity(
            product1.get('title', ''), 
            product2.get('title', '')
        )
        confidence_factors.append(('title', title_similarity, 0.4))
        
        # Brand matching
        brand_match = self._compare_brands(
            product1.get('brand', ''), 
            product2.get('brand', '')
        )
        confidence_factors.append(('brand', brand_match, 0.3))
        
        # Category matching
        category_match = self._compare_categories(
            product1.get('category', ''), 
            product2.get('category', '')
        )
        confidence_factors.append(('category', category_match, 0.2))
        
        # Price comparison
        price_similarity, price_variance = self._compare_prices(
            product1.get('price', 0), 
            product2.get('price', 0)
        )
        confidence_factors.append(('price', price_similarity, 0.1))
        
        # Calculate overall confidence
        weighted_confidence = sum(score * weight for _, score, weight in confidence_factors)
        
        # Determine match type
        match_type = self._determine_match_type(weighted_confidence, differences)
        
        # Record significant differences
        if title_similarity < 0.8:
            differences.append(f"Title difference: {title_similarity:.0%} similarity")
        if brand_match < 0.9:
            differences.append(f"Brand mismatch: {product1.get('brand', 'N/A')} vs {product2.get('brand', 'N/A')}")
        if abs(price_variance) > 0.2:
            differences.append(f"Price variance: {price_variance:.0%}")
        
        return ProductMatch(
            product_id=product1.get('id', ''),
            match_id=product2.get('id', ''),
            confidence=round(weighted_confidence, 2),
            match_type=match_type,
            differences=differences,
            price_variance=round(price_variance, 2)
        )
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text strings"""
        if not text1 or not text2:
            return 0.0
        
        # Normalize texts
        text1_clean = text1.lower().strip()
        text2_clean = text2.lower().strip()
        
        # Use sequence matcher for similarity
        similarity = difflib.SequenceMatcher(None, text1_clean, text2_clean).ratio()
        return similarity
    
    def _compare_brands(self, brand1: str, brand2: str) -> float:
        """Compare brand names with fuzzy matching"""
        if not brand1 or not brand2:
            return 0.0
        
        brand1_clean = brand1.lower().strip()
        brand2_clean = brand2.lower().strip()
        
        if brand1_clean == brand2_clean:
            return 1.0
        
        # Check for common brand variations
        brand_variations = {
            'apple': ['apple inc', 'apple computer'],
            'amazon': ['amazon basics', 'amazonbasics'],
            'google': ['google llc', 'alphabet inc']
        }
        
        for main_brand, variations in brand_variations.items():
            if (brand1_clean == main_brand and brand2_clean in variations) or \
               (brand2_clean == main_brand and brand1_clean in variations):
                return 0.9
        
        # Use text similarity as fallback
        return self._calculate_text_similarity(brand1, brand2)
    
    def _compare_categories(self, cat1: str, cat2: str) -> float:
        """Compare product categories"""
        if not cat1 or not cat2:
            return 0.0
        
        cat1_clean = cat1.lower().strip()
        cat2_clean = cat2.lower().strip()
        
        if cat1_clean == cat2_clean:
            return 1.0
        
        # Check for category hierarchy matches
        if cat1_clean in cat2_clean or cat2_clean in cat1_clean:
            return 0.8
        
        return 0.0
    
    def _compare_prices(self, price1: float, price2: float) -> Tuple[float, float]:
        """Compare prices and calculate similarity and variance"""
        if not price1 or not price2:
            return 0.0, 0.0
        
        variance = (price2 - price1) / price1 if price1 > 0 else 0.0
        abs_variance = abs(variance)
        
        # Price similarity decreases with variance
        if abs_variance <= 0.05:  # Within 5%
            similarity = 1.0
        elif abs_variance <= 0.15:  # Within 15%
            similarity = 0.8
        elif abs_variance <= 0.3:   # Within 30%
            similarity = 0.5
        else:
            similarity = 0.2
        
        return similarity, variance
    
    def _determine_match_type(self, confidence: float, differences: List[str]) -> str:
        """Determine the type of match based on confidence and differences"""
        if confidence >= 0.95:
            return 'exact'
        elif confidence >= 0.85:
            return 'variant'
        elif confidence >= 0.65:
            return 'similar'
        elif confidence >= 0.5:
            return 'potential'
        else:
            return 'no_match'
    
    def _generate_match_summary(self, matches: List[ProductMatch]) -> Dict:
        """Generate summary of match results"""
        if not matches:
            return {
                "total_matches": 0,
                "high_confidence": 0,
                "exact_matches": 0,
                "variants": 0,
                "average_confidence": 0.0
            }
        
        total = len(matches)
        high_confidence = len([m for m in matches if m.confidence > 0.8])
        exact_matches = len([m for m in matches if m.match_type == 'exact'])
        variants = len([m for m in matches if m.match_type == 'variant'])
        avg_confidence = sum(m.confidence for m in matches) / total
        
        return {
            "total_matches": total,
            "high_confidence": high_confidence,
            "exact_matches": exact_matches,
            "variants": variants,
            "average_confidence": round(avg_confidence, 2)
        }
    
    def _generate_match_recommendations(self, matches: List[ProductMatch]) -> List[Dict]:
        """Generate recommendations based on match results"""
        recommendations = []
        
        exact_matches = [m for m in matches if m.match_type == 'exact']
        if exact_matches:
            recommendations.append({
                "type": "duplicate_alert",
                "priority": "high",
                "message": f"Found {len(exact_matches)} exact duplicate(s)",
                "action": "Review for potential listing conflicts"
            })
        
        high_price_variance = [m for m in matches if abs(m.price_variance) > 0.3]
        if high_price_variance:
            recommendations.append({
                "type": "pricing_alert",
                "priority": "medium", 
                "message": f"Found {len(high_price_variance)} match(es) with significant price differences",
                "action": "Consider repricing strategy"
            })
        
        variants = [m for m in matches if m.match_type == 'variant']
        if variants:
            recommendations.append({
                "type": "variant_opportunity",
                "priority": "low",
                "message": f"Found {len(variants)} product variant(s)",
                "action": "Consider bundling or cross-promotion"
            })
        
        return recommendations
    
    def get_agent_info(self) -> Dict:
        """Return agent information for dashboard display"""
        return {
            "name": self.agent_name,
            "tier_requirement": self.tier_requirement,
            "category": self.category,
            "status": self.status,
            "description": self.description,
            "icon": "🔍",
            "features": [
                "Duplicate product detection",
                "Variant identification",
                "Cross-platform matching",
                "Price variance analysis",
                "Conflict prevention"
            ],
            "tier_badge": "Pro+",
            "tooltip": "Prevent listing conflicts by identifying duplicate products and variants"
        }

def demo_product_matcher():
    """Demo the ProductMatcherAI"""
    agent = ProductMatcherAI()
    
    # Sample product database
    products = [
        {"id": "1", "title": "iPhone 15 Pro 128GB Blue", "brand": "Apple", "category": "Electronics", "price": 999.99},
        {"id": "2", "title": "iPhone 15 Pro 128GB - Blue", "brand": "Apple Inc", "category": "Electronics", "price": 1049.99},
        {"id": "3", "title": "iPhone 15 Pro 256GB Blue", "brand": "Apple", "category": "Electronics", "price": 1199.99},
        {"id": "4", "title": "Samsung Galaxy S24 128GB", "brand": "Samsung", "category": "Electronics", "price": 899.99},
        {"id": "5", "title": "Apple iPhone 15 Pro Blue 128GB", "brand": "Apple", "category": "Electronics", "price": 995.00}
    ]
    
    target = {"id": "target", "title": "iPhone 15 Pro 128GB Blue", "brand": "Apple", "category": "Electronics", "price": 999.99}
    
    # Find matches
    results = agent.find_product_matches(target, products)
    
    print("🔍 Product Matching Results:")
    print("=" * 50)
    print(f"Target: {target['title']}")
    print(f"Total Matches: {results['match_summary']['total_matches']}")
    print(f"High Confidence: {results['match_summary']['high_confidence']}")
    print(f"Exact Matches: {results['match_summary']['exact_matches']}")
    
    print(f"\n📊 Top Matches:")
    for match in results['matches'][:3]:
        match_icon = "🎯" if match['match_type'] == 'exact' else "🔄" if match['match_type'] == 'variant' else "📋"
        print(f"{match_icon} ID {match['match_id']}: {match['confidence']:.0%} confidence ({match['match_type']})")
    
    print(f"\n💡 Recommendations:")
    for rec in results['recommendations']:
        priority_icon = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
        print(f"{priority_icon} {rec['message']}")
    
    return results

if __name__ == "__main__":
    demo_product_matcher()
