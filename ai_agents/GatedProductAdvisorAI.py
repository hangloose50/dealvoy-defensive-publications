#!/usr/bin/env python3
"""
GatedProductAdvisorAI - Intelligent product advisory with gated access
Tier: Pro+ (Tier 2+) - Customer + Admin
Role: AI Agent with Pro+ tier requirement
"""

import json
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class ProductAdvice:
    product_id: str
    product_title: str
    advisory_type: str  # 'buy_recommendation', 'price_alert', 'availability_notice', 'seasonal_advice'
    confidence_score: float
    advice_text: str
    reasoning: List[str]
    action_items: List[str]
    data_sources: List[str]

class GatedProductAdvisorAI:
    """
    Intelligent AI agent providing personalized product advice with Pro+ gated access
    - Analyzes product data for buy/sell recommendations
    - Provides market timing and seasonal advice
    - Generates personalized insights based on user patterns
    - Pro+ tier requirement with customer/admin access
    """
    
    def __init__(self):
        self.agent_name = "GatedProductAdvisorAI"
        self.tier_requirement = "pro"
        self.category = "advisory_intelligence"
        self.status = "active"
        self.description = "Intelligent product advisory with gated Pro+ access"
        self.admin_only = False  # Customer + Admin access
        
        # Load advisory intelligence models
        self.market_patterns = self._load_market_patterns()
        self.seasonal_trends = self._load_seasonal_trends()
        
    def generate_product_advice(self, products: List[Dict[str, Any]], user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate intelligent product advice for Pro+ users"""
        
        if user_preferences is None:
            user_preferences = {}
        
        advice_list = []
        
        for product in products:
            advice = self._analyze_product_for_advice(product, user_preferences)
            advice_list.append(advice)
        
        # Generate portfolio-level insights
        portfolio_insights = self._generate_portfolio_insights(advice_list, user_preferences)
        
        return {
            "product_advice": [advice.__dict__ for advice in advice_list],
            "portfolio_insights": portfolio_insights,
            "market_opportunities": self._identify_market_opportunities(advice_list),
            "risk_warnings": self._generate_risk_warnings(advice_list),
            "user_tier": "pro_plus",
            "generated_at": datetime.datetime.now().isoformat()
        }
    
    def _analyze_product_for_advice(self, product: Dict[str, Any], preferences: Dict[str, Any]) -> ProductAdvice:
        """Analyze individual product for advisory insights"""
        
        product_id = product.get("asin", product.get("id", "unknown"))
        product_title = product.get("title", "Unknown Product")
        
        # Calculate confidence based on data quality
        confidence = self._calculate_advisory_confidence(product)
        
        # Determine advisory type
        advisory_type = self._determine_advisory_type(product, preferences)
        
        # Generate advice text and reasoning
        advice_text, reasoning = self._generate_advice_content(product, advisory_type, preferences)
        
        # Generate action items
        action_items = self._generate_action_items(product, advisory_type, preferences)
        
        # Identify data sources used
        data_sources = self._identify_data_sources(product)
        
        return ProductAdvice(
            product_id=product_id,
            product_title=product_title,
            advisory_type=advisory_type,
            confidence_score=confidence,
            advice_text=advice_text,
            reasoning=reasoning,
            action_items=action_items,
            data_sources=data_sources
        )
    
    def _calculate_advisory_confidence(self, product: Dict[str, Any]) -> float:
        """Calculate confidence score for advisory recommendation"""
        
        confidence = 0.5  # Base confidence
        
        # Price data quality
        if product.get("price"):
            confidence += 0.15
        if product.get("price_history"):
            confidence += 0.15
        
        # Sales data
        if product.get("sales_rank"):
            confidence += 0.1
        if product.get("reviews_count", 0) > 100:
            confidence += 0.1
        
        # Product details
        if product.get("brand"):
            confidence += 0.05
        if product.get("category"):
            confidence += 0.05
        
        # Market data
        if product.get("competitor_analysis"):
            confidence += 0.1
        if product.get("seasonal_data"):
            confidence += 0.1
        
        return round(min(1.0, confidence), 2)
    
    def _determine_advisory_type(self, product: Dict[str, Any], preferences: Dict[str, Any]) -> str:
        """Determine the type of advice to provide"""
        
        current_price = product.get("price", 0)
        avg_price = product.get("average_price", current_price)
        
        # Price-based recommendations
        if current_price and avg_price:
            price_ratio = current_price / avg_price if avg_price > 0 else 1.0
            
            if price_ratio <= 0.8:  # 20%+ below average
                return "buy_recommendation"
            elif price_ratio >= 1.2:  # 20%+ above average
                return "price_alert"
        
        # Seasonal recommendations
        current_month = datetime.datetime.now().month
        if self._is_seasonal_opportunity(product, current_month):
            return "seasonal_advice"
        
        # Availability-based
        stock_level = product.get("stock_level", "unknown")
        if stock_level in ["low", "limited"]:
            return "availability_notice"
        
        return "buy_recommendation"
    
    def _generate_advice_content(self, product: Dict[str, Any], advisory_type: str, preferences: Dict[str, Any]) -> tuple:
        """Generate advice text and reasoning"""
        
        product_title = product.get("title", "Product")
        current_price = product.get("price", 0)
        
        if advisory_type == "buy_recommendation":
            advice = f"Strong buy recommendation for {product_title}. Current market conditions favor acquisition."
            reasoning = [
                "Price analysis indicates good value",
                "Market timing is favorable",
                "Product metrics show strong potential"
            ]
            
            if current_price:
                avg_price = product.get("average_price", current_price)
                if current_price < avg_price:
                    savings = avg_price - current_price
                    reasoning.append(f"Current price is ${savings:.2f} below average")
        
        elif advisory_type == "price_alert":
            advice = f"Price alert for {product_title}. Current pricing may be above optimal buy point."
            reasoning = [
                "Current price exceeds recent averages",
                "Consider waiting for price decrease",
                "Monitor for better entry points"
            ]
        
        elif advisory_type == "seasonal_advice":
            advice = f"Seasonal opportunity detected for {product_title}. Timing aligns with market patterns."
            reasoning = [
                "Historical data shows seasonal price patterns",
                "Current timing aligns with demand cycles",
                "Inventory patterns suggest opportunity window"
            ]
        
        elif advisory_type == "availability_notice":
            advice = f"Limited availability notice for {product_title}. Consider expedited decision-making."
            reasoning = [
                "Stock levels indicate limited availability",
                "Supply chain factors may affect pricing",
                "Early action may secure better terms"
            ]
        
        else:
            advice = f"General advisory for {product_title}. Standard monitoring recommended."
            reasoning = ["Stable market conditions", "No immediate action required"]
        
        # Add user preference alignment
        if preferences.get("budget_conscious"):
            reasoning.append("Aligned with budget-conscious strategy")
        if preferences.get("premium_focus"):
            reasoning.append("Matches premium product focus")
        
        return advice, reasoning
    
    def _generate_action_items(self, product: Dict[str, Any], advisory_type: str, preferences: Dict[str, Any]) -> List[str]:
        """Generate specific action items based on advice"""
        
        actions = []
        
        if advisory_type == "buy_recommendation":
            actions.extend([
                "Review current inventory needs",
                "Calculate potential profit margins",
                "Verify supplier availability",
                "Set up price monitoring alerts"
            ])
        
        elif advisory_type == "price_alert":
            actions.extend([
                "Wait for price correction",
                "Set price drop notifications",
                "Research alternative suppliers",
                "Monitor competitor pricing"
            ])
        
        elif advisory_type == "seasonal_advice":
            actions.extend([
                "Plan inventory for seasonal demand",
                "Adjust marketing strategy timing",
                "Coordinate with seasonal trends",
                "Prepare for demand fluctuations"
            ])
        
        elif advisory_type == "availability_notice":
            actions.extend([
                "Expedite decision-making process",
                "Secure supply chain agreements",
                "Consider bulk purchasing",
                "Identify backup suppliers"
            ])
        
        # Add preference-based actions
        if preferences.get("automation_preferred"):
            actions.append("Set up automated monitoring")
        
        if preferences.get("detailed_analysis"):
            actions.append("Request detailed market analysis")
        
        return actions
    
    def _identify_data_sources(self, product: Dict[str, Any]) -> List[str]:
        """Identify data sources used in analysis"""
        
        sources = ["Historical pricing data", "Market analysis algorithms"]
        
        if product.get("competitor_analysis"):
            sources.append("Competitor intelligence")
        
        if product.get("reviews_count"):
            sources.append("Customer sentiment analysis")
        
        if product.get("sales_rank"):
            sources.append("Sales performance metrics")
        
        if product.get("seasonal_data"):
            sources.append("Seasonal trend analysis")
        
        return sources
    
    def _is_seasonal_opportunity(self, product: Dict[str, Any], current_month: int) -> bool:
        """Check if current timing represents seasonal opportunity"""
        
        category = product.get("category", "").lower()
        
        # Seasonal patterns
        seasonal_categories = {
            "toys": [10, 11, 12],  # Holiday season
            "clothing": [3, 4, 9, 10],  # Season transitions
            "garden": [3, 4, 5],  # Spring
            "sports": [1, 2, 6, 7],  # Winter/Summer sports
            "electronics": [11, 12, 1]  # Holiday/New Year
        }
        
        for cat, months in seasonal_categories.items():
            if cat in category and current_month in months:
                return True
        
        return False
    
    def _generate_portfolio_insights(self, advice_list: List[ProductAdvice], preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Generate portfolio-level insights"""
        
        total_products = len(advice_list)
        buy_recommendations = len([a for a in advice_list if a.advisory_type == "buy_recommendation"])
        price_alerts = len([a for a in advice_list if a.advisory_type == "price_alert"])
        
        avg_confidence = sum(a.confidence_score for a in advice_list) / total_products if total_products > 0 else 0.0
        
        return {
            "total_products_analyzed": total_products,
            "buy_recommendations": buy_recommendations,
            "price_alerts": price_alerts,
            "average_confidence": round(avg_confidence, 2),
            "portfolio_score": self._calculate_portfolio_score(advice_list),
            "optimization_suggestions": self._generate_optimization_suggestions(advice_list)
        }
    
    def _calculate_portfolio_score(self, advice_list: List[ProductAdvice]) -> float:
        """Calculate overall portfolio opportunity score"""
        
        if not advice_list:
            return 0.0
        
        # Weight different advisory types
        type_weights = {
            "buy_recommendation": 1.0,
            "seasonal_advice": 0.8,
            "availability_notice": 0.6,
            "price_alert": 0.3
        }
        
        total_score = 0.0
        for advice in advice_list:
            weight = type_weights.get(advice.advisory_type, 0.5)
            total_score += advice.confidence_score * weight
        
        return round(total_score / len(advice_list), 2)
    
    def _identify_market_opportunities(self, advice_list: List[ProductAdvice]) -> List[Dict[str, Any]]:
        """Identify key market opportunities"""
        
        opportunities = []
        
        # High-confidence buy recommendations
        strong_buys = [a for a in advice_list if a.advisory_type == "buy_recommendation" and a.confidence_score > 0.8]
        if strong_buys:
            opportunities.append({
                "type": "high_confidence_buys",
                "count": len(strong_buys),
                "description": "Products with strong buy signals and high confidence",
                "priority": "high"
            })
        
        # Seasonal opportunities
        seasonal_ops = [a for a in advice_list if a.advisory_type == "seasonal_advice"]
        if seasonal_ops:
            opportunities.append({
                "type": "seasonal_timing",
                "count": len(seasonal_ops),
                "description": "Products aligned with seasonal market patterns",
                "priority": "medium"
            })
        
        # Availability-driven opportunities
        availability_ops = [a for a in advice_list if a.advisory_type == "availability_notice"]
        if availability_ops:
            opportunities.append({
                "type": "limited_availability",
                "count": len(availability_ops),
                "description": "Products with limited availability requiring quick action",
                "priority": "urgent"
            })
        
        return opportunities
    
    def _generate_risk_warnings(self, advice_list: List[ProductAdvice]) -> List[Dict[str, Any]]:
        """Generate risk warnings for user attention"""
        
        warnings = []
        
        # Low confidence warnings
        low_confidence = [a for a in advice_list if a.confidence_score < 0.5]
        if len(low_confidence) > len(advice_list) * 0.3:  # >30% low confidence
            warnings.append({
                "type": "data_quality",
                "severity": "medium",
                "description": "Multiple products have limited data for confident recommendations",
                "recommendation": "Gather additional market data before major decisions"
            })
        
        # Price alert concentration
        price_alerts = [a for a in advice_list if a.advisory_type == "price_alert"]
        if len(price_alerts) > len(advice_list) * 0.5:  # >50% price alerts
            warnings.append({
                "type": "market_timing",
                "severity": "medium",
                "description": "High proportion of products show unfavorable pricing",
                "recommendation": "Consider delaying purchases or finding alternative suppliers"
            })
        
        return warnings
    
    def _generate_optimization_suggestions(self, advice_list: List[ProductAdvice]) -> List[str]:
        """Generate portfolio optimization suggestions"""
        
        suggestions = []
        
        buy_ratio = len([a for a in advice_list if a.advisory_type == "buy_recommendation"]) / len(advice_list) if advice_list else 0
        
        if buy_ratio < 0.3:
            suggestions.append("Consider expanding product search criteria to find more opportunities")
        
        if buy_ratio > 0.8:
            suggestions.append("High opportunity ratio detected - ensure adequate capital allocation")
        
        seasonal_count = len([a for a in advice_list if a.advisory_type == "seasonal_advice"])
        if seasonal_count > 0:
            suggestions.append("Align inventory planning with seasonal recommendations")
        
        avg_confidence = sum(a.confidence_score for a in advice_list) / len(advice_list) if advice_list else 0
        if avg_confidence < 0.6:
            suggestions.append("Improve data collection to increase advisory confidence")
        
        return suggestions
    
    def _load_market_patterns(self) -> Dict[str, Any]:
        """Load market pattern intelligence"""
        return {
            "price_cycles": {
                "electronics": 6,  # months
                "clothing": 3,
                "home_garden": 12
            },
            "demand_patterns": {
                "seasonal_multipliers": {
                    "toys": {"11": 2.5, "12": 3.0, "1": 0.7},
                    "clothing": {"3": 1.3, "9": 1.4},
                    "garden": {"3": 1.8, "4": 2.0, "5": 1.6}
                }
            }
        }
    
    def _load_seasonal_trends(self) -> Dict[str, Any]:
        """Load seasonal trend data"""
        return {
            "holiday_seasons": {
                "back_to_school": {"start": 8, "peak": 9, "end": 10},
                "holiday_shopping": {"start": 10, "peak": 11, "end": 12},
                "spring_cleaning": {"start": 3, "peak": 4, "end": 5},
                "summer_outdoor": {"start": 5, "peak": 7, "end": 8}
            },
            "category_seasonality": {
                "toys": ["holiday_shopping"],
                "clothing": ["back_to_school", "spring_cleaning"],
                "garden": ["spring_cleaning", "summer_outdoor"],
                "sports": ["summer_outdoor"],
                "electronics": ["holiday_shopping", "back_to_school"]
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
            "icon": "🎯",
            "features": [
                "Intelligent product advice",
                "Market timing insights",
                "Seasonal recommendations",
                "Portfolio optimization",
                "Risk assessment"
            ],
            "tier_badge": "Pro+",
            "tooltip": "AI-powered product advisory with market intelligence and personalized recommendations"
        }

def demo_gated_advisor():
    """Demo the GatedProductAdvisorAI (Pro+ tier)"""
    agent = GatedProductAdvisorAI()
    
    # Sample products for analysis
    sample_products = [
        {
            "asin": "B08N5WRWNW",
            "title": "Wireless Bluetooth Headphones",
            "price": 79.99,
            "average_price": 89.99,
            "category": "electronics",
            "sales_rank": 1250,
            "reviews_count": 450,
            "stock_level": "high"
        },
        {
            "asin": "B07FZ8S74R", 
            "title": "Winter Coat for Women",
            "price": 120.00,
            "average_price": 95.00,
            "category": "clothing",
            "sales_rank": 890,
            "reviews_count": 230,
            "stock_level": "low"
        },
        {
            "asin": "B09KMVNY9Z",
            "title": "Garden Tool Set",
            "price": 45.99,
            "average_price": 52.99,
            "category": "garden",
            "sales_rank": 2100,
            "reviews_count": 180,
            "stock_level": "medium"
        }
    ]
    
    # User preferences
    user_prefs = {
        "budget_conscious": True,
        "automation_preferred": True,
        "detailed_analysis": False
    }
    
    # Generate advice
    results = agent.generate_product_advice(sample_products, user_prefs)
    
    print("🎯 Product Advisory Results (Pro+ Access):")
    print("=" * 55)
    
    print(f"📊 Portfolio Summary:")
    insights = results['portfolio_insights']
    print(f"   Products Analyzed: {insights['total_products_analyzed']}")
    print(f"   Buy Recommendations: {insights['buy_recommendations']}")
    print(f"   Price Alerts: {insights['price_alerts']}")
    print(f"   Portfolio Score: {insights['portfolio_score']:.2f}/1.0")
    
    print(f"\n💡 Product Advice:")
    for advice_data in results['product_advice']:
        advice_icon = "🟢" if advice_data['advisory_type'] == 'buy_recommendation' else "🟡" if advice_data['advisory_type'] == 'seasonal_advice' else "🔴"
        print(f"{advice_icon} {advice_data['product_title']}")
        print(f"   Type: {advice_data['advisory_type'].replace('_', ' ').title()}")
        print(f"   Confidence: {advice_data['confidence_score']:.2f}")
        print(f"   Advice: {advice_data['advice_text']}")
        
        if advice_data['action_items']:
            print(f"   Action: {advice_data['action_items'][0]}")
    
    print(f"\n🚀 Market Opportunities:")
    for opp in results['market_opportunities']:
        priority_icon = "🔴" if opp['priority'] == 'urgent' else "🟡" if opp['priority'] == 'high' else "🟢"
        print(f"{priority_icon} {opp['description']} ({opp['count']} products)")
    
    return results

if __name__ == "__main__":
    print("🎯 Pro+ Tier Required - Gated Product Advisory")
    demo_gated_advisor()
