#!/usr/bin/env python3
"""
CategoryAI Agent
Product classification and categorization agent
Protected by USPTO #63/850,603
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, List

class CategoryAI:
    """AI agent for product classification and categorization"""
    
    def __init__(self):
        self.agent_name = "CategoryAI"
        self.version = "1.0.0"
        self.status = "active"
        self.amazon_categories = {
            "Electronics": ["Computers", "Phones", "Accessories"],
            "Home & Kitchen": ["Appliances", "Furniture", "Decor"],
            "Sports & Outdoors": ["Fitness", "Camping", "Sports Equipment"],
            "Books": ["Fiction", "Non-Fiction", "Educational"],
            "Clothing": ["Men", "Women", "Kids"]
        }
        
    def classify_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Classify a product into appropriate category"""
        try:
            title = product_data.get("title", "").lower()
            description = product_data.get("description", "").lower()
            keywords = product_data.get("keywords", [])
            
            category_scores = {}
            
            # Score each category based on keyword matches
            for main_category, subcategories in self.amazon_categories.items():
                score = 0
                
                # Check main category keywords
                if main_category.lower() in title or main_category.lower() in description:
                    score += 50
                
                # Check subcategory keywords
                for subcategory in subcategories:
                    if subcategory.lower() in title or subcategory.lower() in description:
                        score += 30
                
                # Check product keywords
                for keyword in keywords:
                    if keyword.lower() in title or keyword.lower() in description:
                        score += 10
                
                category_scores[main_category] = score
            
            # Find best match
            best_category = max(category_scores.keys(), key=lambda k: category_scores[k])
            confidence = category_scores[best_category]
            
            result = {
                "product_title": product_data.get("title", "Unknown"),
                "classified_category": best_category,
                "confidence_score": confidence,
                "all_scores": category_scores,
                "subcategories": self.amazon_categories[best_category],
                "classification_timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"CategoryAI classified product as {best_category} with {confidence}% confidence")
            return result
            
        except Exception as e:
            logging.error(f"Product classification failed: {e}")
            return {"error": str(e)}
    
    def suggest_keywords(self, category: str) -> List[str]:
        """Suggest relevant keywords for a category"""
        keyword_suggestions = {
            "Electronics": ["tech", "digital", "smart", "wireless", "portable"],
            "Home & Kitchen": ["durable", "stylish", "functional", "modern", "quality"],
            "Sports & Outdoors": ["performance", "professional", "adventure", "fitness", "outdoor"],
            "Books": ["bestseller", "educational", "inspiring", "comprehensive", "acclaimed"],
            "Clothing": ["comfortable", "stylish", "durable", "trendy", "premium"]
        }
        
        return keyword_suggestions.get(category, ["quality", "premium", "best"])
    
    def run(self, input_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main execution method"""
        input_data = input_data or {}
        
        if "product_data" in input_data:
            return self.classify_product(input_data["product_data"])
        elif "category" in input_data:
            keywords = self.suggest_keywords(input_data["category"])
            return {"category": input_data["category"], "suggested_keywords": keywords}
        
        return {
            "status": "ready",
            "agent": self.agent_name,
            "available_categories": list(self.amazon_categories.keys()),
            "capabilities": ["product_classification", "keyword_suggestion", "category_analysis"]
        }

if __name__ == "__main__":
    agent = CategoryAI()
    print(json.dumps(agent.run(), indent=2))
