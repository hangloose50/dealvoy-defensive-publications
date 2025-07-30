#!/usr/bin/env python3
"""
BundleProfitEstimator - Advanced profit estimation for product bundles
Tier: Pro+ (Tier 2+) - Customer + Admin  
Role: AI Agent with Pro+ tier requirement
"""

import json
import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import statistics

@dataclass
class BundleEstimate:
    bundle_id: str
    bundle_name: str
    products: List[Dict[str, Any]]
    estimated_profit: float
    profit_margin: float
    confidence_level: float
    risk_factors: List[str]
    optimization_suggestions: List[str]
    market_demand_score: float

class BundleProfitEstimator:
    """
    Advanced AI agent for estimating profit potential of product bundles
    - Analyzes product combinations for profit optimization
    - Calculates market demand and pricing strategies
    - Provides bundle composition recommendations
    - Pro+ tier requirement with customer/admin access
    """
    
    def __init__(self):
        self.agent_name = "BundleProfitEstimator"
        self.tier_requirement = "pro"
        self.category = "profit_analytics"
        self.status = "active"
        self.description = "Advanced profit estimation for product bundles"
        self.admin_only = False  # Customer + Admin access
        
        # Load profit calculation models
        self.market_multipliers = self._load_market_multipliers()
        self.bundle_synergies = self._load_bundle_synergies()
        
    def estimate_bundle_profits(self, product_bundles: List[Dict[str, Any]], market_conditions: Dict[str, Any] = None) -> Dict[str, Any]:
        """Estimate profit potential for product bundles"""
        
        if market_conditions is None:
            market_conditions = self._get_default_market_conditions()
        
        bundle_estimates = []
        
        for bundle in product_bundles:
            estimate = self._analyze_bundle_profit(bundle, market_conditions)
            bundle_estimates.append(estimate)
        
        # Generate portfolio analysis
        portfolio_analysis = self._generate_portfolio_analysis(bundle_estimates)
        
        return {
            "bundle_estimates": [estimate.__dict__ for estimate in bundle_estimates],
            "portfolio_analysis": portfolio_analysis,
            "market_insights": self._generate_market_insights(bundle_estimates, market_conditions),
            "optimization_recommendations": self._generate_optimization_recommendations(bundle_estimates),
            "tier_access": "pro_plus",
            "estimated_at": datetime.datetime.now().isoformat()
        }
    
    def _analyze_bundle_profit(self, bundle: Dict[str, Any], market_conditions: Dict[str, Any]) -> BundleEstimate:
        """Analyze profit potential for a single bundle"""
        
        bundle_id = bundle.get("id", f"bundle_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
        bundle_name = bundle.get("name", "Unnamed Bundle")
        products = bundle.get("products", [])
        
        if not products:
            return self._create_empty_estimate(bundle_id, bundle_name)
        
        # Calculate base profit metrics
        total_cost, total_revenue = self._calculate_bundle_financials(products, market_conditions)
        estimated_profit = total_revenue - total_cost
        profit_margin = (estimated_profit / total_revenue * 100) if total_revenue > 0 else 0.0
        
        # Calculate confidence level
        confidence = self._calculate_confidence_level(products, market_conditions)
        
        # Analyze risk factors
        risk_factors = self._identify_risk_factors(products, market_conditions)
        
        # Generate optimization suggestions
        optimization_suggestions = self._generate_bundle_optimizations(products, estimated_profit, profit_margin)
        
        # Calculate market demand score
        demand_score = self._calculate_market_demand_score(products, market_conditions)
        
        return BundleEstimate(
            bundle_id=bundle_id,
            bundle_name=bundle_name,
            products=products,
            estimated_profit=round(estimated_profit, 2),
            profit_margin=round(profit_margin, 2),
            confidence_level=round(confidence, 2),
            risk_factors=risk_factors,
            optimization_suggestions=optimization_suggestions,
            market_demand_score=round(demand_score, 2)
        )
    
    def _calculate_bundle_financials(self, products: List[Dict[str, Any]], market_conditions: Dict[str, Any]) -> Tuple[float, float]:
        """Calculate total cost and revenue for bundle"""
        
        total_cost = 0.0
        total_revenue = 0.0
        
        for product in products:
            # Calculate individual product costs
            unit_cost = product.get("cost", product.get("price", 0) * 0.7)  # Assume 30% margin if cost not provided
            quantity = product.get("quantity", 1)
            
            # Apply market multipliers
            category = product.get("category", "general").lower()
            market_multiplier = self.market_multipliers.get(category, 1.0)
            
            # Calculate revenue with bundle synergy
            unit_price = product.get("price", unit_cost * 1.5)  # Default 50% markup
            synergy_boost = self._calculate_synergy_boost(products, product)
            
            product_cost = unit_cost * quantity
            product_revenue = unit_price * quantity * market_multiplier * synergy_boost
            
            # Apply market condition adjustments
            seasonal_factor = market_conditions.get("seasonal_factor", 1.0)
            demand_factor = market_conditions.get("demand_factor", 1.0)
            
            total_cost += product_cost
            total_revenue += product_revenue * seasonal_factor * demand_factor
        
        return total_cost, total_revenue
    
    def _calculate_synergy_boost(self, all_products: List[Dict[str, Any]], current_product: Dict[str, Any]) -> float:
        """Calculate synergy boost from product combinations"""
        
        current_category = current_product.get("category", "").lower()
        synergy_boost = 1.0  # Base multiplier
        
        # Check for complementary products
        for other_product in all_products:
            if other_product == current_product:
                continue
                
            other_category = other_product.get("category", "").lower()
            
            # Apply synergy rules
            if current_category in self.bundle_synergies and other_category in self.bundle_synergies[current_category]:
                synergy_boost *= self.bundle_synergies[current_category][other_category]
        
        # Cap synergy boost to reasonable limits
        return min(synergy_boost, 1.5)  # Max 50% boost
    
    def _calculate_confidence_level(self, products: List[Dict[str, Any]], market_conditions: Dict[str, Any]) -> float:
        """Calculate confidence level for profit estimate"""
        
        confidence = 0.5  # Base confidence
        
        # Data quality factors
        has_cost_data = sum(1 for p in products if p.get("cost")) / len(products)
        has_price_data = sum(1 for p in products if p.get("price")) / len(products)
        has_sales_data = sum(1 for p in products if p.get("sales_rank")) / len(products)
        
        confidence += has_cost_data * 0.2
        confidence += has_price_data * 0.15
        confidence += has_sales_data * 0.1
        
        # Market data quality
        if market_conditions.get("data_quality") == "high":
            confidence += 0.1
        elif market_conditions.get("data_quality") == "low":
            confidence -= 0.1
        
        # Product diversity (reduces risk)
        categories = set(p.get("category", "unknown") for p in products)
        if len(categories) > 1:
            confidence += 0.05
        
        # Bundle size factor
        if 3 <= len(products) <= 7:  # Optimal bundle size
            confidence += 0.05
        elif len(products) > 10:  # Too complex
            confidence -= 0.1
        
        return min(1.0, max(0.0, confidence))
    
    def _identify_risk_factors(self, products: List[Dict[str, Any]], market_conditions: Dict[str, Any]) -> List[str]:
        """Identify risk factors for bundle profitability"""
        
        risks = []
        
        # Market condition risks
        if market_conditions.get("volatility", "medium") == "high":
            risks.append("High market volatility may affect pricing")
        
        if market_conditions.get("competition", "medium") == "high":
            risks.append("High competition may pressure margins")
        
        # Product-specific risks
        seasonal_products = [p for p in products if p.get("seasonal", False)]
        if len(seasonal_products) > len(products) * 0.5:
            risks.append("Bundle heavily dependent on seasonal products")
        
        # Price variance risk
        prices = [p.get("price", 0) for p in products if p.get("price")]
        if prices:
            price_cv = statistics.stdev(prices) / statistics.mean(prices) if len(prices) > 1 and statistics.mean(prices) > 0 else 0
            if price_cv > 0.5:  # High coefficient of variation
                risks.append("High price variance between bundle products")
        
        # Inventory risks
        low_stock_products = [p for p in products if p.get("stock_level") == "low"]
        if low_stock_products:
            risks.append(f"Limited inventory for {len(low_stock_products)} product(s)")
        
        # Category concentration risk
        categories = [p.get("category") for p in products]
        if len(set(categories)) == 1:
            risks.append("Bundle concentrated in single product category")
        
        return risks
    
    def _generate_bundle_optimizations(self, products: List[Dict[str, Any]], profit: float, margin: float) -> List[str]:
        """Generate optimization suggestions for bundle"""
        
        suggestions = []
        
        # Margin optimization
        if margin < 20:
            suggestions.append("Consider increasing bundle price or reducing costs to improve margin")
        elif margin > 60:
            suggestions.append("High margin detected - consider competitive pricing strategy")
        
        # Product mix optimization
        if len(products) < 3:
            suggestions.append("Add complementary products to increase bundle value")
        elif len(products) > 8:
            suggestions.append("Consider reducing bundle complexity for better customer appeal")
        
        # Category diversity
        categories = set(p.get("category") for p in products)
        if len(categories) == 1:
            suggestions.append("Add products from complementary categories to increase appeal")
        
        # Price point optimization
        prices = [p.get("price", 0) for p in products if p.get("price")]
        if prices:
            avg_price = sum(prices) / len(prices)
            if avg_price < 20:
                suggestions.append("Consider adding higher-value products to increase bundle worth")
            elif avg_price > 100:
                suggestions.append("High-value bundle - ensure target market alignment")
        
        # Seasonal optimization
        seasonal_count = sum(1 for p in products if p.get("seasonal", False))
        if seasonal_count > 0:
            suggestions.append("Optimize timing for seasonal product components")
        
        return suggestions
    
    def _calculate_market_demand_score(self, products: List[Dict[str, Any]], market_conditions: Dict[str, Any]) -> float:
        """Calculate market demand score for bundle"""
        
        demand_score = 0.5  # Base score
        
        # Individual product demand
        for product in products:
            sales_rank = product.get("sales_rank", 999999)
            reviews_count = product.get("reviews_count", 0)
            
            # Better sales rank = higher demand
            if sales_rank < 1000:
                demand_score += 0.1
            elif sales_rank < 10000:
                demand_score += 0.05
            
            # More reviews = higher demand
            if reviews_count > 500:
                demand_score += 0.1
            elif reviews_count > 100:
                demand_score += 0.05
        
        # Normalize by number of products
        demand_score = demand_score / len(products) if products else 0.5
        
        # Market condition factors
        demand_factor = market_conditions.get("demand_factor", 1.0)
        seasonal_factor = market_conditions.get("seasonal_factor", 1.0)
        
        demand_score *= demand_factor * seasonal_factor
        
        return min(1.0, max(0.0, demand_score))
    
    def _create_empty_estimate(self, bundle_id: str, bundle_name: str) -> BundleEstimate:
        """Create empty estimate for bundles with no products"""
        
        return BundleEstimate(
            bundle_id=bundle_id,
            bundle_name=bundle_name,
            products=[],
            estimated_profit=0.0,
            profit_margin=0.0,
            confidence_level=0.0,
            risk_factors=["No products in bundle"],
            optimization_suggestions=["Add products to bundle"],
            market_demand_score=0.0
        )
    
    def _get_default_market_conditions(self) -> Dict[str, Any]:
        """Get default market conditions"""
        return {
            "seasonal_factor": 1.0,
            "demand_factor": 1.0,
            "volatility": "medium",
            "competition": "medium",
            "data_quality": "medium"
        }
    
    def _generate_portfolio_analysis(self, estimates: List[BundleEstimate]) -> Dict[str, Any]:
        """Generate portfolio-level analysis"""
        
        if not estimates:
            return {"total_bundles": 0, "total_profit": 0.0, "average_margin": 0.0}
        
        total_profit = sum(est.estimated_profit for est in estimates)
        profit_margins = [est.profit_margin for est in estimates]
        avg_margin = sum(profit_margins) / len(profit_margins)
        avg_confidence = sum(est.confidence_level for est in estimates) / len(estimates)
        
        # Categorize bundles by performance
        high_profit = [est for est in estimates if est.estimated_profit > 100]
        high_margin = [est for est in estimates if est.profit_margin > 30]
        high_confidence = [est for est in estimates if est.confidence_level > 0.7]
        
        return {
            "total_bundles": len(estimates),
            "total_estimated_profit": round(total_profit, 2),
            "average_margin": round(avg_margin, 2),
            "average_confidence": round(avg_confidence, 2),
            "high_profit_bundles": len(high_profit),
            "high_margin_bundles": len(high_margin),
            "high_confidence_bundles": len(high_confidence),
            "portfolio_score": self._calculate_portfolio_score(estimates)
        }
    
    def _calculate_portfolio_score(self, estimates: List[BundleEstimate]) -> float:
        """Calculate overall portfolio performance score"""
        
        if not estimates:
            return 0.0
        
        # Weight different factors
        profit_score = sum(min(est.estimated_profit / 100, 1.0) for est in estimates) / len(estimates)
        margin_score = sum(min(est.profit_margin / 50, 1.0) for est in estimates) / len(estimates)
        confidence_score = sum(est.confidence_level for est in estimates) / len(estimates)
        demand_score = sum(est.market_demand_score for est in estimates) / len(estimates)
        
        # Weighted combination
        portfolio_score = (profit_score * 0.3 + margin_score * 0.25 + confidence_score * 0.25 + demand_score * 0.2)
        
        return round(portfolio_score, 2)
    
    def _generate_market_insights(self, estimates: List[BundleEstimate], market_conditions: Dict[str, Any]) -> Dict[str, Any]:
        """Generate market insights for decision making"""
        
        insights = {
            "market_outlook": "neutral",
            "recommended_focus": [],
            "risk_alerts": []
        }
        
        if not estimates:
            return insights
        
        # Calculate average metrics
        avg_profit = sum(est.estimated_profit for est in estimates) / len(estimates)
        avg_margin = sum(est.profit_margin for est in estimates) / len(estimates)
        
        # Market outlook
        if avg_profit > 75 and avg_margin > 25:
            insights["market_outlook"] = "positive"
        elif avg_profit < 25 or avg_margin < 15:
            insights["market_outlook"] = "challenging"
        
        # Recommended focus areas
        best_performers = sorted(estimates, key=lambda x: x.estimated_profit, reverse=True)[:3]
        if best_performers:
            insights["recommended_focus"] = [
                f"Focus on '{bundle.bundle_name}' with ${bundle.estimated_profit:.0f} profit potential"
                for bundle in best_performers
            ]
        
        # Risk alerts
        high_risk_bundles = [est for est in estimates if len(est.risk_factors) > 3]
        if high_risk_bundles:
            insights["risk_alerts"].append(f"{len(high_risk_bundles)} bundle(s) have multiple risk factors")
        
        return insights
    
    def _generate_optimization_recommendations(self, estimates: List[BundleEstimate]) -> List[Dict[str, Any]]:
        """Generate strategic optimization recommendations"""
        
        recommendations = []
        
        if not estimates:
            return recommendations
        
        # Low margin bundles
        low_margin = [est for est in estimates if est.profit_margin < 20]
        if low_margin:
            recommendations.append({
                "type": "margin_improvement",
                "priority": "high",
                "description": f"Optimize {len(low_margin)} bundle(s) with low profit margins",
                "affected_bundles": len(low_margin)
            })
        
        # High-confidence opportunities
        high_confidence = [est for est in estimates if est.confidence_level > 0.8 and est.estimated_profit > 50]
        if high_confidence:
            recommendations.append({
                "type": "scaling_opportunity",
                "priority": "medium",
                "description": f"Scale {len(high_confidence)} high-confidence profitable bundle(s)",
                "affected_bundles": len(high_confidence)
            })
        
        # Bundle diversity
        total_products = sum(len(est.products) for est in estimates)
        avg_bundle_size = total_products / len(estimates) if estimates else 0
        if avg_bundle_size < 3:
            recommendations.append({
                "type": "bundle_expansion",
                "priority": "medium",
                "description": "Consider expanding bundle sizes to increase value",
                "affected_bundles": len(estimates)
            })
        
        return recommendations
    
    def _load_market_multipliers(self) -> Dict[str, float]:
        """Load market multipliers by category"""
        return {
            "electronics": 1.15,
            "books": 0.95,
            "clothing": 1.1,
            "home": 1.05,
            "sports": 1.08,
            "toys": 1.2,
            "health": 1.12,
            "automotive": 1.06,
            "garden": 1.03,
            "general": 1.0
        }
    
    def _load_bundle_synergies(self) -> Dict[str, Dict[str, float]]:
        """Load synergy multipliers between product categories"""
        return {
            "electronics": {
                "accessories": 1.15,
                "cables": 1.1,
                "cases": 1.1
            },
            "clothing": {
                "accessories": 1.12,
                "shoes": 1.08,
                "bags": 1.1
            },
            "home": {
                "kitchen": 1.1,
                "decor": 1.08,
                "storage": 1.05
            },
            "sports": {
                "fitness": 1.15,
                "outdoor": 1.1,
                "equipment": 1.12
            },
            "health": {
                "supplements": 1.1,
                "wellness": 1.08,
                "fitness": 1.12
            }
        }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Return agent information for dashboard display"""
        return {
            "name": self.agent_name,
            "tier_requirement": self.tier_requirement,
            "category": self.category,
            "status": self.status,
            "description": self.description,
            "admin_only": self.admin_only,
            "icon": "📊",
            "features": [
                "Bundle profit estimation",
                "Market demand analysis",
                "Synergy calculation",
                "Risk assessment",
                "Portfolio optimization"
            ],
            "tier_badge": "Pro+",
            "tooltip": "Advanced profit estimation and optimization for product bundles with market intelligence"
        }

def demo_bundle_estimator():
    """Demo the BundleProfitEstimator (Pro+ tier)"""
    agent = BundleProfitEstimator()
    
    # Sample bundles for analysis
    sample_bundles = [
        {
            "id": "TECH_001",
            "name": "Premium Electronics Bundle",
            "products": [
                {
                    "id": "laptop", "category": "electronics", "price": 899.99, "cost": 650.00,
                    "quantity": 1, "sales_rank": 1200, "reviews_count": 340
                },
                {
                    "id": "mouse", "category": "accessories", "price": 29.99, "cost": 18.00,
                    "quantity": 1, "sales_rank": 890, "reviews_count": 120
                },
                {
                    "id": "case", "category": "cases", "price": 39.99, "cost": 22.00,
                    "quantity": 1, "sales_rank": 1500, "reviews_count": 89
                }
            ]
        },
        {
            "id": "HOME_001",
            "name": "Kitchen Essentials Bundle",
            "products": [
                {
                    "id": "blender", "category": "kitchen", "price": 89.99, "cost": 55.00,
                    "quantity": 1, "sales_rank": 2100, "reviews_count": 230
                },
                {
                    "id": "cutting_board", "category": "kitchen", "price": 24.99, "cost": 12.00,
                    "quantity": 1, "sales_rank": 3200, "reviews_count": 145
                },
                {
                    "id": "knife_set", "category": "kitchen", "price": 49.99, "cost": 28.00,
                    "quantity": 1, "sales_rank": 1800, "reviews_count": 189
                }
            ]
        }
    ]
    
    # Market conditions
    market_conditions = {
        "seasonal_factor": 1.1,  # Slight seasonal boost
        "demand_factor": 1.05,   # Mild demand increase
        "volatility": "medium",
        "competition": "medium",
        "data_quality": "high"
    }
    
    # Estimate profits
    results = agent.estimate_bundle_profits(sample_bundles, market_conditions)
    
    print("📊 Bundle Profit Estimation Results (Pro+ Access):")
    print("=" * 58)
    
    print(f"📈 Portfolio Summary:")
    analysis = results['portfolio_analysis']
    print(f"   Total Bundles: {analysis['total_bundles']}")
    print(f"   Total Estimated Profit: ${analysis['total_estimated_profit']:,.2f}")
    print(f"   Average Margin: {analysis['average_margin']:.1f}%")
    print(f"   Portfolio Score: {analysis['portfolio_score']:.2f}/1.0")
    
    print(f"\n💰 Bundle Details:")
    for bundle_data in results['bundle_estimates']:
        profit_icon = "🟢" if bundle_data['estimated_profit'] > 100 else "🟡" if bundle_data['estimated_profit'] > 50 else "🔴"
        print(f"{profit_icon} {bundle_data['bundle_name']}")
        print(f"   Profit: ${bundle_data['estimated_profit']:,.2f} ({bundle_data['profit_margin']:.1f}% margin)")
        print(f"   Confidence: {bundle_data['confidence_level']:.2f} | Demand Score: {bundle_data['market_demand_score']:.2f}")
        
        if bundle_data['optimization_suggestions']:
            print(f"   Suggestion: {bundle_data['optimization_suggestions'][0]}")
    
    print(f"\n🎯 Market Insights:")
    insights = results['market_insights']
    print(f"   Market Outlook: {insights['market_outlook'].title()}")
    if insights['recommended_focus']:
        print(f"   Focus: {insights['recommended_focus'][0]}")
    
    return results

if __name__ == "__main__":
    print("📊 Pro+ Tier Required - Bundle Profit Estimation")
    demo_bundle_estimator()
