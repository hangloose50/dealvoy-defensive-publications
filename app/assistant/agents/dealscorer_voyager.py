#!/usr/bin/env python3
"""
DealScorer Voyager - Advanced AI Deal Scoring and Profit Analysis

This agent provides intelligent deal scoring, profit margin analysis, and ROI 
prediction for e-commerce arbitrage opportunities.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from app.services.scout_dealscorer import score_deal


class DealScorerVoyager:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.dealscorer_dir = self.project_path / "dealscorer_analysis"
        self.dealscorer_dir.mkdir(parents=True, exist_ok=True)
        
        # Deal scoring thresholds
        self.profit_thresholds = {
            "minimal": 2.0,
            "standard": 5.0,
            "aggressive": 10.0,
            "premium": 20.0
        }
        
        # Market categories and their scoring modifiers
        self.category_modifiers = {
            "electronics": 1.2,
            "books": 0.8,
            "toys": 1.1,
            "health": 1.3,
            "home": 1.0,
            "fashion": 0.9,
            "sports": 1.1
        }
        
        # Risk factors
        self.risk_factors = {
            "brand_restricted": -3,
            "seasonal_item": -1,
            "high_competition": -2,
            "patent_risk": -4,
            "map_violation": -2,
            "low_demand": -2
        }

    def analyze_deal_batch(self, products: List[Dict]) -> Dict:
        """Analyze a batch of products for deal quality"""
        print("💰 [DealScorerVoyager] Analyzing deal batch...")
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "total_products": len(products),
            "scored_deals": [],
            "summary": {
                "excellent_deals": 0,
                "good_deals": 0,
                "fair_deals": 0,
                "poor_deals": 0
            },
            "top_recommendations": [],
            "risk_analysis": {}
        }
        
        for product in products:
            deal_score = self._comprehensive_deal_analysis(product)
            analysis["scored_deals"].append(deal_score)
            
            # Categorize deals
            score = deal_score["final_score"]
            if score >= 8:
                analysis["summary"]["excellent_deals"] += 1
            elif score >= 6:
                analysis["summary"]["good_deals"] += 1
            elif score >= 4:
                analysis["summary"]["fair_deals"] += 1
            else:
                analysis["summary"]["poor_deals"] += 1
        
        # Sort by score and get top recommendations
        analysis["scored_deals"].sort(key=lambda x: x["final_score"], reverse=True)
        analysis["top_recommendations"] = analysis["scored_deals"][:10]
        
        # Risk analysis
        analysis["risk_analysis"] = self._analyze_portfolio_risk(analysis["scored_deals"])
        
        return analysis

    def _comprehensive_deal_analysis(self, product: Dict) -> Dict:
        """Perform comprehensive deal analysis with AI-enhanced scoring"""
        
        # Base scoring from scout_dealscorer
        base_score = score_deal(product)
        
        # Enhanced analysis
        enhanced_analysis = {
            "product_id": product.get("asin") or product.get("upc") or "unknown",
            "product_title": product.get("title", "Unknown Product"),
            "base_score": base_score["score"],
            "base_reason": base_score["reason"],
            "enhanced_factors": {},
            "risk_assessment": {},
            "final_score": base_score["score"],
            "recommendation": "",
            "profit_analysis": {}
        }
        
        # Enhanced profit analysis
        enhanced_analysis["profit_analysis"] = self._analyze_profit_metrics(product)
        
        # Category-specific adjustments
        category = product.get("category", "unknown").lower()
        if category in self.category_modifiers:
            modifier = self.category_modifiers[category]
            enhanced_analysis["enhanced_factors"]["category_bonus"] = modifier - 1.0
            enhanced_analysis["final_score"] *= modifier
        
        # Risk factor analysis
        enhanced_analysis["risk_assessment"] = self._assess_risks(product)
        risk_penalty = sum(enhanced_analysis["risk_assessment"].values())
        enhanced_analysis["final_score"] += risk_penalty
        
        # Market trend analysis
        enhanced_analysis["enhanced_factors"]["market_trend"] = self._analyze_market_trend(product)
        
        # Clamp final score
        enhanced_analysis["final_score"] = max(1, min(10, enhanced_analysis["final_score"]))
        
        # Generate recommendation
        enhanced_analysis["recommendation"] = self._generate_recommendation(enhanced_analysis)
        
        return enhanced_analysis

    def _analyze_profit_metrics(self, product: Dict) -> Dict:
        """Analyze detailed profit metrics"""
        price = float(product.get("price", 0) or 0)
        cost = float(product.get("cost", 0) or 0)
        
        profit_metrics = {
            "gross_profit": price - cost,
            "profit_margin": ((price - cost) / price * 100) if price > 0 else 0,
            "roi_percentage": ((price - cost) / cost * 100) if cost > 0 else 0,
            "break_even_units": 1,  # Simplified
            "monthly_profit_potential": 0
        }
        
        # Estimate monthly profit potential
        sales_rank = int(product.get("sales_rank", 0) or 0)
        if sales_rank > 0:
            # Rough estimation: better rank = more sales
            if sales_rank < 10000:
                estimated_monthly_sales = 50
            elif sales_rank < 50000:
                estimated_monthly_sales = 20
            elif sales_rank < 100000:
                estimated_monthly_sales = 10
            else:
                estimated_monthly_sales = 5
                
            profit_metrics["monthly_profit_potential"] = profit_metrics["gross_profit"] * estimated_monthly_sales
        
        return profit_metrics

    def _assess_risks(self, product: Dict) -> Dict:
        """Assess various risk factors"""
        risks = {}
        
        # Brand restriction risk
        brand = product.get("brand", "").lower()
        restricted_brands = ["nike", "apple", "lego", "disney", "microsoft"]
        if brand in restricted_brands:
            risks["brand_restricted"] = self.risk_factors["brand_restricted"]
        
        # Competition risk (based on review count)
        reviews = int(product.get("reviews", 0) or 0)
        if reviews > 1000:
            risks["high_competition"] = self.risk_factors["high_competition"]
        
        # Demand risk (based on sales rank)
        sales_rank = int(product.get("sales_rank", 0) or 0)
        if sales_rank > 100000:
            risks["low_demand"] = self.risk_factors["low_demand"]
        
        return risks

    def _analyze_market_trend(self, product: Dict) -> float:
        """Analyze market trend for the product category"""
        # Simplified trend analysis
        category = product.get("category", "").lower()
        
        # Seasonal adjustments
        current_month = datetime.now().month
        if category in ["toys", "games"] and current_month in [10, 11, 12]:
            return 1.5  # Holiday boost
        elif category in ["electronics"] and current_month in [11, 12, 1]:
            return 1.3  # Holiday/New Year electronics boost
        elif category in ["fitness", "health"] and current_month in [1, 2]:
            return 1.2  # New Year fitness boost
        
        return 1.0  # Neutral

    def _generate_recommendation(self, analysis: Dict) -> str:
        """Generate AI-powered recommendation"""
        score = analysis["final_score"]
        profit = analysis["profit_analysis"]["gross_profit"]
        
        if score >= 8:
            return f"🟢 STRONG BUY - Excellent deal with ${profit:.2f} profit potential"
        elif score >= 6:
            return f"🟡 CONSIDER - Good opportunity with ${profit:.2f} profit"
        elif score >= 4:
            return f"🟠 CAUTION - Marginal deal, ${profit:.2f} profit but risks present"
        else:
            return f"🔴 AVOID - Poor deal quality, only ${profit:.2f} profit"

    def _analyze_portfolio_risk(self, deals: List[Dict]) -> Dict:
        """Analyze overall portfolio risk"""
        if not deals:
            return {}
            
        total_investment = sum(float(deal.get("profit_analysis", {}).get("gross_profit", 0)) for deal in deals)
        
        risk_analysis = {
            "total_portfolio_value": total_investment,
            "high_risk_percentage": 0,
            "category_concentration": {},
            "recommendation": ""
        }
        
        # Calculate category concentration
        categories = {}
        for deal in deals:
            category = deal.get("category", "unknown")
            categories[category] = categories.get(category, 0) + 1
        
        risk_analysis["category_concentration"] = categories
        
        # Risk recommendations
        if len(categories) < 3:
            risk_analysis["recommendation"] = "⚠️  Consider diversifying across more categories"
        else:
            risk_analysis["recommendation"] = "✅ Good category diversification"
        
        return risk_analysis

    def generate_market_insights(self) -> Dict:
        """Generate AI-powered market insights"""
        print("📊 [DealScorerVoyager] Generating market insights...")
        
        insights = {
            "timestamp": datetime.now().isoformat(),
            "market_conditions": {
                "overall_sentiment": "neutral",
                "hot_categories": ["electronics", "health", "home"],
                "cooling_categories": ["fashion", "books"],
                "seasonal_factors": self._get_seasonal_insights()
            },
            "profit_opportunities": {
                "high_margin_categories": ["health", "electronics"],
                "arbitrage_hotspots": ["clearance_items", "seasonal_transitions"],
                "emerging_trends": ["sustainability", "health_tech", "remote_work"]
            },
            "risk_warnings": {
                "brand_restrictions": "Increasing enforcement on major brands",
                "map_violations": "Stricter monitoring of minimum advertised prices",
                "market_saturation": "Competition increasing in popular categories"
            }
        }
        
        return insights

    def _get_seasonal_insights(self) -> Dict:
        """Get current seasonal market insights"""
        current_month = datetime.now().month
        
        seasonal_map = {
            1: {"focus": "fitness", "opportunity": "New Year resolutions"},
            2: {"focus": "valentine", "opportunity": "Gift items and electronics"},
            3: {"focus": "spring_prep", "opportunity": "Home and garden"},
            4: {"focus": "easter", "opportunity": "Toys and seasonal items"},
            5: {"focus": "graduation", "opportunity": "Electronics and gifts"},
            6: {"focus": "summer_prep", "opportunity": "Outdoor and sports"},
            7: {"focus": "summer_peak", "opportunity": "Travel and outdoor gear"},
            8: {"focus": "back_to_school", "opportunity": "Electronics and supplies"},
            9: {"focus": "fall_prep", "opportunity": "Home goods and fashion"},
            10: {"focus": "halloween", "opportunity": "Costumes and decorations"},
            11: {"focus": "holiday_prep", "opportunity": "All categories surge"},
            12: {"focus": "holiday_peak", "opportunity": "Gift items and electronics"}
        }
        
        return seasonal_map.get(current_month, {"focus": "general", "opportunity": "Standard market conditions"})

    def run_deal_analysis(self, input_file: str, output_file: str = None):
        """Run comprehensive deal analysis on input file"""
        input_path = Path(input_file)
        if not input_path.exists():
            print(f"❌ Input file not found: {input_file}")
            return False
            
        # Load products
        try:
            with open(input_path, 'r') as f:
                products = json.load(f)
                if not isinstance(products, list):
                    products = [products]
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in input file: {input_file}")
            return False
        
        # Analyze deals
        analysis = self.analyze_deal_batch(products)
        
        # Generate market insights
        insights = self.generate_market_insights()
        
        # Combine results
        complete_analysis = {
            "deal_analysis": analysis,
            "market_insights": insights,
            "generated_by": "DealScorerVoyager",
            "timestamp": datetime.now().isoformat()
        }
        
        # Save results
        if output_file:
            output_path = Path(output_file)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.dealscorer_dir / f"deal_analysis_{timestamp}.json"
        
        with open(output_path, 'w') as f:
            json.dump(complete_analysis, f, indent=2)
        
        print(f"💰 [DealScorerVoyager] Analysis complete: {output_path}")
        
        # Print summary
        self._print_analysis_summary(analysis)
        
        return True

    def _print_analysis_summary(self, analysis: Dict):
        """Print a summary of the deal analysis"""
        summary = analysis["summary"]
        total = analysis["total_products"]
        
        print(f"\n📊 DEALSCORER ANALYSIS SUMMARY")
        print(f"═══════════════════════════════")
        print(f"Total Products Analyzed: {total}")
        print(f"🟢 Excellent Deals: {summary['excellent_deals']} ({summary['excellent_deals']/total*100:.1f}%)")
        print(f"🟡 Good Deals: {summary['good_deals']} ({summary['good_deals']/total*100:.1f}%)")
        print(f"🟠 Fair Deals: {summary['fair_deals']} ({summary['fair_deals']/total*100:.1f}%)")
        print(f"🔴 Poor Deals: {summary['poor_deals']} ({summary['poor_deals']/total*100:.1f}%)")
        
        if analysis["top_recommendations"]:
            print(f"\n🏆 TOP 3 RECOMMENDATIONS:")
            for i, deal in enumerate(analysis["top_recommendations"][:3], 1):
                profit = deal["profit_analysis"]["gross_profit"]
                print(f"{i}. {deal['product_title'][:50]}... - Score: {deal['final_score']:.1f}, Profit: ${profit:.2f}")


def main():
    parser = argparse.ArgumentParser(description="DealScorer Voyager - AI Deal Analysis")
    parser.add_argument("--input", "-i", required=True, help="Input JSON file with product data")
    parser.add_argument("--output", "-o", help="Output file path (optional)")
    parser.add_argument("--project-path", default=".", help="Project root path")
    
    args = parser.parse_args()
    
    try:
        voyager = DealScorerVoyager(args.project_path)
        success = voyager.run_deal_analysis(args.input, args.output)
        
        if success:
            print(f"💰 DealScorerVoyager: Analysis completed successfully")
            return 0
        else:
            print(f"💰 DealScorerVoyager: Analysis failed")
            return 1
            
    except Exception as e:
        print(f"💰 DealScorerVoyager: Error - {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
