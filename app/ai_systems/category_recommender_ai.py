#!/usr/bin/env python3
"""
📚 CategoryRecommender AI - Suggests optimal product categories for maximum profit
Intelligent category analysis for e-commerce arbitrage optimization
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class CategoryRecommenderAI:
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.reports_dir = self.project_path / "dist" / "intelligence_reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.category_data = self._load_category_intelligence()
        
    def _load_category_intelligence(self) -> Dict[str, Any]:
        """Load comprehensive category performance data"""
        return {
            "amazon_categories": {
                "Home & Kitchen": {
                    "competition_level": 0.75,
                    "profit_margin_avg": 0.35,
                    "sales_velocity": 0.82,
                    "seasonal_variance": 0.3,
                    "barrier_to_entry": "low",
                    "trending_subcategories": ["Organization", "Smart Home", "Kitchen Gadgets"],
                    "avg_sale_price": 25.99,
                    "return_rate": 0.12
                },
                "Electronics": {
                    "competition_level": 0.92,
                    "profit_margin_avg": 0.18,
                    "sales_velocity": 0.95,
                    "seasonal_variance": 0.4,
                    "barrier_to_entry": "high",
                    "trending_subcategories": ["Phone Accessories", "Audio", "Gaming"],
                    "avg_sale_price": 49.99,
                    "return_rate": 0.08
                },
                "Sports & Outdoors": {
                    "competition_level": 0.65,
                    "profit_margin_avg": 0.42,
                    "sales_velocity": 0.68,
                    "seasonal_variance": 0.6,
                    "barrier_to_entry": "medium",
                    "trending_subcategories": ["Fitness", "Outdoor Gear", "Water Sports"],
                    "avg_sale_price": 34.99,
                    "return_rate": 0.15
                },
                "Health & Personal Care": {
                    "competition_level": 0.70,
                    "profit_margin_avg": 0.38,
                    "sales_velocity": 0.78,
                    "seasonal_variance": 0.2,
                    "barrier_to_entry": "medium",
                    "trending_subcategories": ["Vitamins", "Beauty", "Personal Care"],
                    "avg_sale_price": 19.99,
                    "return_rate": 0.10
                },
                "Toys & Games": {
                    "competition_level": 0.80,
                    "profit_margin_avg": 0.45,
                    "sales_velocity": 0.65,
                    "seasonal_variance": 0.8,
                    "barrier_to_entry": "low",
                    "trending_subcategories": ["Educational Toys", "STEM", "Board Games"],
                    "avg_sale_price": 22.99,
                    "return_rate": 0.18
                },
                "Automotive": {
                    "competition_level": 0.55,
                    "profit_margin_avg": 0.32,
                    "sales_velocity": 0.58,
                    "seasonal_variance": 0.3,
                    "barrier_to_entry": "medium",
                    "trending_subcategories": ["Car Accessories", "Tools", "Maintenance"],
                    "avg_sale_price": 28.99,
                    "return_rate": 0.14
                }
            },
            "market_trends": {
                "growing_categories": ["Health & Personal Care", "Home & Kitchen", "Pet Supplies"],
                "declining_categories": ["CDs & Vinyl", "Office Products"],
                "seasonal_peaks": {
                    "Q4": ["Toys & Games", "Electronics", "Home & Kitchen"],
                    "Q1": ["Health & Personal Care", "Sports & Outdoors"],
                    "Q2": ["Sports & Outdoors", "Automotive"],
                    "Q3": ["Back to School", "Electronics"]
                }
            },
            "profit_optimization": {
                "high_margin_categories": ["Sports & Outdoors", "Toys & Games", "Health & Personal Care"],
                "fast_moving_categories": ["Electronics", "Home & Kitchen"],
                "low_competition_categories": ["Automotive", "Sports & Outdoors"],
                "stable_categories": ["Health & Personal Care", "Home & Kitchen"]
            }
        }
    
    def analyze_category_opportunity(self, category: str) -> Dict[str, Any]:
        """Analyze opportunity score for a specific category"""
        if category not in self.category_data["amazon_categories"]:
            return {"error": f"Category '{category}' not found in database"}
        
        cat_data = self.category_data["amazon_categories"][category]
        
        # Calculate opportunity score (0-100)
        opportunity_factors = {
            "profit_potential": cat_data["profit_margin_avg"] * 30,  # 30% weight
            "sales_velocity": cat_data["sales_velocity"] * 25,       # 25% weight
            "low_competition": (1 - cat_data["competition_level"]) * 20,  # 20% weight
            "stability": (1 - cat_data["seasonal_variance"]) * 15,   # 15% weight
            "market_size": min(cat_data["avg_sale_price"] / 50, 1) * 10  # 10% weight
        }
        
        opportunity_score = sum(opportunity_factors.values())
        
        # Risk assessment
        risk_factors = []
        if cat_data["competition_level"] > 0.8:
            risk_factors.append("High competition")
        if cat_data["return_rate"] > 0.15:
            risk_factors.append("High return rate")
        if cat_data["seasonal_variance"] > 0.6:
            risk_factors.append("High seasonal variance")
        if cat_data["barrier_to_entry"] == "high":
            risk_factors.append("High barrier to entry")
        
        return {
            "category": category,
            "opportunity_score": round(opportunity_score, 1),
            "opportunity_factors": opportunity_factors,
            "risk_factors": risk_factors,
            "recommendation": self._get_category_recommendation(opportunity_score, risk_factors),
            "category_data": cat_data
        }
    
    def _get_category_recommendation(self, score: float, risks: List[str]) -> str:
        """Generate recommendation based on score and risks"""
        if score >= 80 and len(risks) <= 1:
            return "EXCELLENT: High opportunity, low risk"
        elif score >= 70 and len(risks) <= 2:
            return "GOOD: Strong opportunity with manageable risks"
        elif score >= 60:
            return "FAIR: Moderate opportunity, monitor risks carefully"
        else:
            return "POOR: Limited opportunity, high risk"
    
    def recommend_categories_for_budget(self, budget: float, experience_level: str = "beginner") -> List[Dict[str, Any]]:
        """Recommend categories based on budget and experience"""
        recommendations = []
        
        for category, data in self.category_data["amazon_categories"].items():
            analysis = self.analyze_category_opportunity(category)
            
            # Budget compatibility
            min_investment = data["avg_sale_price"] * 10  # Assume 10 units minimum
            budget_compatible = budget >= min_investment
            
            # Experience level filtering
            experience_compatible = True
            if experience_level == "beginner":
                if data["barrier_to_entry"] == "high" or data["competition_level"] > 0.85:
                    experience_compatible = False
            elif experience_level == "intermediate":
                if data["barrier_to_entry"] == "high" and data["competition_level"] > 0.90:
                    experience_compatible = False
            
            if budget_compatible and experience_compatible:
                analysis["budget_fit"] = {
                    "min_investment": min_investment,
                    "recommended_units": min(int(budget / data["avg_sale_price"]), 50),
                    "budget_utilization": min(min_investment / budget, 1.0)
                }
                recommendations.append(analysis)
        
        # Sort by opportunity score
        recommendations.sort(key=lambda x: x["opportunity_score"], reverse=True)
        return recommendations
    
    def find_trending_subcategories(self, main_category: str = None) -> Dict[str, Any]:
        """Find trending subcategories across all or specific category"""
        trending_analysis = {
            "analysis_date": datetime.now().isoformat(),
            "trending_subcategories": [],
            "growth_indicators": {},
            "recommendations": []
        }
        
        categories_to_analyze = [main_category] if main_category else list(self.category_data["amazon_categories"].keys())
        
        for category in categories_to_analyze:
            if category in self.category_data["amazon_categories"]:
                cat_data = self.category_data["amazon_categories"][category]
                for subcat in cat_data["trending_subcategories"]:
                    trend_score = self._calculate_trend_score(category, subcat)
                    trending_analysis["trending_subcategories"].append({
                        "main_category": category,
                        "subcategory": subcat,
                        "trend_score": trend_score,
                        "opportunity_level": self._get_trend_opportunity(trend_score)
                    })
        
        # Sort by trend score
        trending_analysis["trending_subcategories"].sort(key=lambda x: x["trend_score"], reverse=True)
        
        # Generate recommendations
        top_trends = trending_analysis["trending_subcategories"][:5]
        for trend in top_trends:
            trending_analysis["recommendations"].append({
                "subcategory": f"{trend['main_category']} > {trend['subcategory']}",
                "action": "Consider expanding into this subcategory",
                "priority": "HIGH" if trend["trend_score"] > 85 else "MEDIUM"
            })
        
        return trending_analysis
    
    def _calculate_trend_score(self, category: str, subcategory: str) -> float:
        """Calculate trend score for subcategory"""
        base_score = 70
        
        # Category-specific bonuses
        category_data = self.category_data["amazon_categories"][category]
        
        # High sales velocity bonus
        if category_data["sales_velocity"] > 0.8:
            base_score += 10
        
        # Low competition bonus
        if category_data["competition_level"] < 0.7:
            base_score += 8
        
        # Subcategory-specific adjustments
        trend_bonuses = {
            "Smart Home": 15,
            "Gaming": 12,
            "Fitness": 10,
            "Educational Toys": 8,
            "Organization": 6
        }
        
        if subcategory in trend_bonuses:
            base_score += trend_bonuses[subcategory]
        
        return min(base_score, 100)
    
    def _get_trend_opportunity(self, score: float) -> str:
        """Convert trend score to opportunity level"""
        if score >= 85:
            return "EXCELLENT"
        elif score >= 75:
            return "GOOD"
        elif score >= 65:
            return "FAIR"
        else:
            return "POOR"
    
    def seasonal_category_planning(self, months_ahead: int = 3) -> Dict[str, Any]:
        """Plan category focus based on seasonal trends"""
        current_month = datetime.now().month
        seasonal_plan = {
            "planning_horizon": f"{months_ahead} months",
            "seasonal_recommendations": [],
            "preparation_timeline": {},
            "inventory_suggestions": {}
        }
        
        # Quarter mapping
        quarter_map = {
            1: "Q1", 2: "Q1", 3: "Q1",
            4: "Q2", 5: "Q2", 6: "Q2",
            7: "Q3", 8: "Q3", 9: "Q3",
            10: "Q4", 11: "Q4", 12: "Q4"
        }
        
        for month_offset in range(months_ahead):
            target_month = (current_month + month_offset - 1) % 12 + 1
            target_quarter = quarter_map[target_month]
            
            if target_quarter in self.category_data["market_trends"]["seasonal_peaks"]:
                peak_categories = self.category_data["market_trends"]["seasonal_peaks"][target_quarter]
                
                for category in peak_categories:
                    if category in self.category_data["amazon_categories"]:
                        cat_data = self.category_data["amazon_categories"][category]
                        seasonal_plan["seasonal_recommendations"].append({
                            "month": target_month,
                            "quarter": target_quarter,
                            "category": category,
                            "preparation_time": "2-3 months before peak",
                            "expected_margin": cat_data["profit_margin_avg"],
                            "seasonal_variance": cat_data["seasonal_variance"]
                        })
        
        return seasonal_plan
    
    def run(self) -> Dict[str, Any]:
        """Main execution function"""
        print("📚 [CategoryRecommender AI] Analyzing category opportunities...")
        
        # Analyze all categories
        print("   🔍 Evaluating category performance...")
        category_analyses = []
        for category in self.category_data["amazon_categories"].keys():
            analysis = self.analyze_category_opportunity(category)
            category_analyses.append(analysis)
        
        # Sort by opportunity score
        category_analyses.sort(key=lambda x: x["opportunity_score"], reverse=True)
        
        # Budget-based recommendations
        print("   💰 Generating budget-based recommendations...")
        budget_scenarios = {
            "small_budget": self.recommend_categories_for_budget(1000, "beginner"),
            "medium_budget": self.recommend_categories_for_budget(5000, "intermediate"),
            "large_budget": self.recommend_categories_for_budget(15000, "advanced")
        }
        
        # Trending analysis
        print("   📈 Identifying trending subcategories...")
        trending_analysis = self.find_trending_subcategories()
        
        # Seasonal planning
        print("   📅 Creating seasonal category plan...")
        seasonal_plan = self.seasonal_category_planning(6)
        
        # Create comprehensive report
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "ai_system": "CategoryRecommenderAI",
                "version": "1.0.0",
                "categories_analyzed": len(self.category_data["amazon_categories"])
            },
            "executive_summary": {
                "top_opportunity": category_analyses[0]["category"] if category_analyses else "None",
                "top_opportunity_score": category_analyses[0]["opportunity_score"] if category_analyses else 0,
                "excellent_categories": len([c for c in category_analyses if c["opportunity_score"] >= 80]),
                "trending_subcategories": len(trending_analysis["trending_subcategories"]),
                "seasonal_opportunities": len(seasonal_plan["seasonal_recommendations"]),
                "recommendation": self._get_overall_category_recommendation(category_analyses)
            },
            "category_analysis": category_analyses,
            "budget_recommendations": budget_scenarios,
            "trending_analysis": trending_analysis,
            "seasonal_planning": seasonal_plan,
            "market_intelligence": self.category_data["market_trends"]
        }
        
        # Save report
        report_file = self.reports_dir / f"category_recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("✅ CategoryRecommender AI: Analysis completed!")
        print(f"   📊 Categories analyzed: {len(self.category_data['amazon_categories'])}")
        print(f"   ⭐ Excellent opportunities: {report['executive_summary']['excellent_categories']}")
        print(f"   📈 Trending subcategories: {report['executive_summary']['trending_subcategories']}")
        print(f"   📄 Full Report: {report_file}")
        
        # Print top recommendations
        if category_analyses:
            print("\n🎯 Top Category Opportunities:")
            for analysis in category_analyses[:3]:
                print(f"   {analysis['category']}: {analysis['opportunity_score']}/100")
                print(f"      {analysis['recommendation']}")
        
        print("📚 [CategoryRecommender AI] Ready for category optimization!")
        return report
    
    def _get_overall_category_recommendation(self, analyses: List[Dict[str, Any]]) -> str:
        """Generate overall recommendation"""
        excellent_count = len([a for a in analyses if a["opportunity_score"] >= 80])
        good_count = len([a for a in analyses if 70 <= a["opportunity_score"] < 80])
        
        if excellent_count >= 3:
            return "EXCELLENT: Multiple high-opportunity categories available."
        elif excellent_count >= 1 or good_count >= 3:
            return "GOOD: Strong category opportunities identified."
        elif good_count >= 1:
            return "FAIR: Some viable category options available."
        else:
            return "POOR: Limited category opportunities. Consider market research."

def run():
    """CLI entry point"""
    category_ai = CategoryRecommenderAI()
    category_ai.run()

if __name__ == "__main__":
    run()
