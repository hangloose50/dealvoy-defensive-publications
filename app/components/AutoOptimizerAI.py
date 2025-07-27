"""
AutoOptimizerAI - Enhanced AI Recommendation Engine
Part of Dealvoy Arbitrage Intelligence System
Protected by USPTO Patent #63/850,603
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
from dataclasses import dataclass

@dataclass
class ProductRecommendation:
    """AI-generated product recommendation with confidence scoring"""
    product_id: str
    action: str  # "buy", "watch", "avoid"
    confidence: float  # 0.0 to 1.0
    roi_estimate: float
    risk_level: str  # "low", "medium", "high"
    reasoning: List[str]
    expires_at: datetime

class TrendAI:
    """Market trend analysis component"""
    
    def __init__(self):
        self.trend_data = {}
        self.category_baselines = {
            'electronics': {'avg_roi': 25.0, 'volatility': 0.15},
            'home': {'avg_roi': 18.5, 'volatility': 0.12},
            'toys': {'avg_roi': 30.2, 'volatility': 0.22},
            'health': {'avg_roi': 22.8, 'volatility': 0.18},
            'books': {'avg_roi': 15.3, 'volatility': 0.08},
            'clothing': {'avg_roi': 35.1, 'volatility': 0.28}
        }
    
    def analyze_category_trend(self, category: str, historical_data: List[Dict]) -> Dict:
        """Analyze trend patterns for a specific category"""
        baseline = self.category_baselines.get(category, {'avg_roi': 20.0, 'volatility': 0.15})
        
        if not historical_data:
            return {
                'trend_direction': 'stable',
                'confidence': 0.5,
                'roi_projection': baseline['avg_roi'],
                'volatility_score': baseline['volatility']
            }
        
        # Simulate trend analysis
        recent_performance = np.mean([item.get('roi', 0) for item in historical_data[-10:]])
        trend_slope = self._calculate_trend_slope(historical_data)
        
        return {
            'trend_direction': 'rising' if trend_slope > 0.05 else 'falling' if trend_slope < -0.05 else 'stable',
            'confidence': min(0.95, 0.6 + abs(trend_slope) * 2),
            'roi_projection': recent_performance * (1 + trend_slope),
            'volatility_score': baseline['volatility']
        }
    
    def _calculate_trend_slope(self, data: List[Dict]) -> float:
        """Calculate trend slope using linear regression"""
        if len(data) < 2:
            return 0.0
        
        x = np.arange(len(data))
        y = np.array([item.get('roi', 0) for item in data])
        
        if np.std(y) == 0:
            return 0.0
        
        slope = np.corrcoef(x, y)[0, 1] * (np.std(y) / np.std(x))
        return slope / 100  # Normalize to percentage

class RepricingStrategistAI:
    """AI component for pricing strategy analysis"""
    
    def __init__(self):
        self.pricing_models = {}
        self.competitive_intelligence = {}
    
    def analyze_pricing_opportunity(self, product_data: Dict) -> Dict:
        """Analyze pricing competitiveness and opportunity"""
        current_price = product_data.get('current_price', 0)
        competitor_prices = product_data.get('competitor_prices', [])
        
        if not competitor_prices:
            return {
                'pricing_advantage': 'unknown',
                'recommended_action': 'research',
                'margin_opportunity': 0.0
            }
        
        avg_competitor_price = np.mean(competitor_prices)
        price_position = (current_price - avg_competitor_price) / avg_competitor_price
        
        if price_position < -0.15:  # 15% below average
            return {
                'pricing_advantage': 'strong',
                'recommended_action': 'buy',
                'margin_opportunity': abs(price_position) * 100
            }
        elif price_position < -0.05:  # 5% below average
            return {
                'pricing_advantage': 'moderate',
                'recommended_action': 'watch',
                'margin_opportunity': abs(price_position) * 100
            }
        else:
            return {
                'pricing_advantage': 'weak',
                'recommended_action': 'avoid',
                'margin_opportunity': 0.0
            }

class AutoOptimizerAI:
    """Enhanced AI engine for product recommendations and optimization"""
    
    def __init__(self):
        self.trend_ai = TrendAI()
        self.repricing_ai = RepricingStrategistAI()
        self.user_history = {}
        self.learning_data = {}
        self.confidence_threshold = 0.7
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def recommend_product(self, product_data: Dict, user_id: str = "default") -> ProductRecommendation:
        """
        Generate AI-powered product recommendation
        
        Args:
            product_data: Product information including price, rank, category, etc.
            user_id: User identifier for personalized recommendations
            
        Returns:
            ProductRecommendation object with action and reasoning
        """
        try:
            # Extract product information
            product_id = product_data.get('id', 'unknown')
            category = product_data.get('category', 'other')
            current_roi = product_data.get('roi', 0)
            sales_rank = product_data.get('sales_rank', 999999)
            gating_status = product_data.get('gating', 'unknown')
            
            # Get user's historical performance
            user_performance = self._get_user_performance(user_id, category)
            
            # Analyze market trends
            trend_analysis = self.trend_ai.analyze_category_trend(
                category, 
                user_performance.get('historical_data', [])
            )
            
            # Analyze pricing opportunity
            pricing_analysis = self.repricing_ai.analyze_pricing_opportunity(product_data)
            
            # Calculate recommendation scores
            scores = self._calculate_recommendation_scores(
                product_data, trend_analysis, pricing_analysis, user_performance
            )
            
            # Generate recommendation
            recommendation = self._generate_recommendation(
                product_id, scores, trend_analysis, pricing_analysis
            )
            
            # Update learning data
            self._update_learning_data(user_id, product_data, recommendation)
            
            self.logger.info(f"Generated recommendation for {product_id}: {recommendation.action}")
            return recommendation
            
        except Exception as e:
            self.logger.error(f"Error generating recommendation: {str(e)}")
            return self._fallback_recommendation(product_data.get('id', 'unknown'))
    
    def _calculate_recommendation_scores(self, product_data: Dict, trend_analysis: Dict, 
                                       pricing_analysis: Dict, user_performance: Dict) -> Dict:
        """Calculate various scoring metrics for recommendation"""
        
        # ROI Score (0-100)
        roi = product_data.get('roi', 0)
        roi_score = min(100, max(0, roi * 2))  # Scale ROI to 0-100
        
        # Trend Score (0-100)
        trend_direction = trend_analysis.get('trend_direction', 'stable')
        trend_confidence = trend_analysis.get('confidence', 0.5)
        trend_score = {
            'rising': 80 * trend_confidence,
            'stable': 50 * trend_confidence,
            'falling': 20 * trend_confidence
        }.get(trend_direction, 50)
        
        # Sales Rank Score (0-100, lower rank = higher score)
        sales_rank = product_data.get('sales_rank', 999999)
        rank_score = max(0, 100 - (sales_rank / 10000))  # Normalize rank
        
        # Pricing Score (0-100)
        pricing_advantage = pricing_analysis.get('pricing_advantage', 'unknown')
        pricing_score = {
            'strong': 90,
            'moderate': 70,
            'weak': 30,
            'unknown': 50
        }.get(pricing_advantage, 50)
        
        # Gating Score (0-100)
        gating_status = product_data.get('gating', 'unknown')
        gating_score = {
            'ungated': 100,
            'gated': 60,
            'restricted': 20,
            'unknown': 70
        }.get(gating_status, 70)
        
        # User Performance Score (0-100)
        category = product_data.get('category', 'other')
        user_success_rate = user_performance.get('success_rates', {}).get(category, 0.5)
        user_score = user_success_rate * 100
        
        return {
            'roi_score': roi_score,
            'trend_score': trend_score,
            'rank_score': rank_score,
            'pricing_score': pricing_score,
            'gating_score': gating_score,
            'user_score': user_score
        }
    
    def _generate_recommendation(self, product_id: str, scores: Dict, 
                               trend_analysis: Dict, pricing_analysis: Dict) -> ProductRecommendation:
        """Generate final recommendation based on scores"""
        
        # Calculate weighted overall score
        weights = {
            'roi_score': 0.25,
            'trend_score': 0.20,
            'rank_score': 0.15,
            'pricing_score': 0.20,
            'gating_score': 0.10,
            'user_score': 0.10
        }
        
        overall_score = sum(scores[key] * weights[key] for key in weights)
        confidence = min(0.95, overall_score / 100)
        
        # Determine action based on score thresholds
        if overall_score >= 75 and confidence >= self.confidence_threshold:
            action = "buy"
            risk_level = "low" if overall_score >= 85 else "medium"
        elif overall_score >= 50:
            action = "watch"
            risk_level = "medium"
        else:
            action = "avoid"
            risk_level = "high"
        
        # Generate reasoning
        reasoning = self._generate_reasoning(scores, trend_analysis, pricing_analysis, action)
        
        # Calculate ROI estimate
        base_roi = max(0, scores['roi_score'] / 2)  # Convert score back to ROI estimate
        trend_adjustment = (trend_analysis.get('roi_projection', base_roi) - base_roi) * 0.3
        roi_estimate = base_roi + trend_adjustment
        
        return ProductRecommendation(
            product_id=product_id,
            action=action,
            confidence=confidence,
            roi_estimate=roi_estimate,
            risk_level=risk_level,
            reasoning=reasoning,
            expires_at=datetime.now() + timedelta(hours=24)
        )
    
    def _generate_reasoning(self, scores: Dict, trend_analysis: Dict, 
                          pricing_analysis: Dict, action: str) -> List[str]:
        """Generate human-readable reasoning for the recommendation"""
        reasoning = []
        
        # ROI reasoning
        if scores['roi_score'] > 70:
            reasoning.append("Strong ROI potential detected")
        elif scores['roi_score'] < 30:
            reasoning.append("Low ROI potential - margin concerns")
        
        # Trend reasoning
        trend_direction = trend_analysis.get('trend_direction', 'stable')
        if trend_direction == 'rising':
            reasoning.append("Category showing positive trend momentum")
        elif trend_direction == 'falling':
            reasoning.append("Category experiencing downward trend")
        
        # Pricing reasoning
        pricing_advantage = pricing_analysis.get('pricing_advantage', 'unknown')
        if pricing_advantage == 'strong':
            reasoning.append("Significant pricing advantage over competitors")
        elif pricing_advantage == 'weak':
            reasoning.append("Limited pricing competitiveness")
        
        # Sales rank reasoning
        if scores['rank_score'] > 70:
            reasoning.append("Excellent sales rank positioning")
        elif scores['rank_score'] < 30:
            reasoning.append("Poor sales rank may indicate low demand")
        
        # Gating reasoning
        if scores['gating_score'] == 100:
            reasoning.append("Product is ungated - easy market entry")
        elif scores['gating_score'] <= 20:
            reasoning.append("Product has significant gating restrictions")
        
        # Action-specific reasoning
        if action == "buy":
            reasoning.append("All indicators align for profitable arbitrage")
        elif action == "watch":
            reasoning.append("Mixed signals - monitor for better entry point")
        else:
            reasoning.append("Risk factors outweigh potential rewards")
        
        return reasoning[:4]  # Limit to top 4 reasons
    
    def _get_user_performance(self, user_id: str, category: str) -> Dict:
        """Get user's historical performance data"""
        if user_id not in self.user_history:
            return {
                'success_rates': {category: 0.5},
                'historical_data': [],
                'total_scans': 0
            }
        
        user_data = self.user_history[user_id]
        return {
            'success_rates': user_data.get('success_rates', {category: 0.5}),
            'historical_data': user_data.get('historical_data', []),
            'total_scans': user_data.get('total_scans', 0)
        }
    
    def _update_learning_data(self, user_id: str, product_data: Dict, 
                            recommendation: ProductRecommendation) -> None:
        """Update learning data for continuous improvement"""
        if user_id not in self.learning_data:
            self.learning_data[user_id] = {
                'recommendations': [],
                'outcomes': [],
                'performance_metrics': {}
            }
        
        self.learning_data[user_id]['recommendations'].append({
            'timestamp': datetime.now().isoformat(),
            'product_id': recommendation.product_id,
            'action': recommendation.action,
            'confidence': recommendation.confidence,
            'roi_estimate': recommendation.roi_estimate
        })
    
    def _fallback_recommendation(self, product_id: str) -> ProductRecommendation:
        """Generate fallback recommendation when analysis fails"""
        return ProductRecommendation(
            product_id=product_id,
            action="watch",
            confidence=0.3,
            roi_estimate=0.0,
            risk_level="high",
            reasoning=["Insufficient data for analysis", "Manual review recommended"],
            expires_at=datetime.now() + timedelta(hours=6)
        )
    
    def update_user_feedback(self, user_id: str, product_id: str, 
                           actual_outcome: Dict) -> None:
        """Update system with actual outcomes for learning"""
        if user_id not in self.user_history:
            self.user_history[user_id] = {
                'success_rates': {},
                'historical_data': [],
                'total_scans': 0
            }
        
        category = actual_outcome.get('category', 'other')
        was_profitable = actual_outcome.get('profitable', False)
        
        # Update success rates
        if category not in self.user_history[user_id]['success_rates']:
            self.user_history[user_id]['success_rates'][category] = 0.5
        
        current_rate = self.user_history[user_id]['success_rates'][category]
        # Simple exponential moving average
        alpha = 0.1
        new_rate = (1 - alpha) * current_rate + alpha * (1.0 if was_profitable else 0.0)
        self.user_history[user_id]['success_rates'][category] = new_rate
        
        # Add to historical data
        self.user_history[user_id]['historical_data'].append({
            'timestamp': datetime.now().isoformat(),
            'product_id': product_id,
            'category': category,
            'profitable': was_profitable,
            'roi': actual_outcome.get('actual_roi', 0)
        })
        
        # Keep only last 100 entries
        if len(self.user_history[user_id]['historical_data']) > 100:
            self.user_history[user_id]['historical_data'] = \
                self.user_history[user_id]['historical_data'][-100:]
        
        self.logger.info(f"Updated feedback for user {user_id}, product {product_id}")
    
    def get_weekly_insights(self, user_id: str = "default") -> Dict:
        """Generate weekly performance insights"""
        if user_id not in self.learning_data:
            return {
                'total_recommendations': 0,
                'accuracy_rate': 0.0,
                'top_categories': [],
                'improvement_suggestions': []
            }
        
        user_data = self.learning_data[user_id]
        recommendations = user_data.get('recommendations', [])
        
        # Calculate weekly stats
        week_ago = datetime.now() - timedelta(days=7)
        weekly_recs = [
            r for r in recommendations 
            if datetime.fromisoformat(r['timestamp']) > week_ago
        ]
        
        return {
            'total_recommendations': len(weekly_recs),
            'accuracy_rate': self._calculate_accuracy_rate(user_id),
            'top_categories': self._get_top_categories(user_id),
            'improvement_suggestions': self._generate_improvement_suggestions(user_id)
        }
    
    def _calculate_accuracy_rate(self, user_id: str) -> float:
        """Calculate recommendation accuracy rate"""
        if user_id not in self.user_history:
            return 0.5
        
        historical_data = self.user_history[user_id].get('historical_data', [])
        if not historical_data:
            return 0.5
        
        successful = sum(1 for item in historical_data if item.get('profitable', False))
        return successful / len(historical_data) if historical_data else 0.5
    
    def _get_top_categories(self, user_id: str) -> List[str]:
        """Get user's top performing categories"""
        if user_id not in self.user_history:
            return []
        
        success_rates = self.user_history[user_id].get('success_rates', {})
        return sorted(success_rates.keys(), key=lambda k: success_rates[k], reverse=True)[:3]
    
    def _generate_improvement_suggestions(self, user_id: str) -> List[str]:
        """Generate personalized improvement suggestions"""
        suggestions = []
        
        if user_id not in self.user_history:
            return ["Start scanning more products to improve AI accuracy"]
        
        success_rates = self.user_history[user_id].get('success_rates', {})
        
        # Find underperforming categories
        for category, rate in success_rates.items():
            if rate < 0.3:
                suggestions.append(f"Consider avoiding {category} category - low success rate")
            elif rate > 0.7:
                suggestions.append(f"Focus more on {category} category - high success rate")
        
        if len(suggestions) == 0:
            suggestions.append("Continue current strategy - performance is balanced")
        
        return suggestions[:3]  # Limit to top 3 suggestions

# Integration functions for dashboard and mobile app
def integrate_with_scanner(product_data: Dict, user_id: str = "default") -> Dict:
    """Integration function for real-time scanning"""
    optimizer = AutoOptimizerAI()
    recommendation = optimizer.recommend_product(product_data, user_id)
    
    return {
        'product_id': recommendation.product_id,
        'action': recommendation.action,
        'confidence': recommendation.confidence,
        'roi_estimate': recommendation.roi_estimate,
        'risk_level': recommendation.risk_level,
        'reasoning': recommendation.reasoning,
        'expires_at': recommendation.expires_at.isoformat()
    }

def batch_analyze_products(product_list: List[Dict], user_id: str = "default") -> List[Dict]:
    """Batch analysis for product library"""
    optimizer = AutoOptimizerAI()
    results = []
    
    for product_data in product_list:
        try:
            recommendation = optimizer.recommend_product(product_data, user_id)
            results.append({
                'product_id': recommendation.product_id,
                'action': recommendation.action,
                'confidence': recommendation.confidence,
                'roi_estimate': recommendation.roi_estimate,
                'risk_level': recommendation.risk_level,
                'reasoning': recommendation.reasoning[:2]  # Abbreviated for batch
            })
        except Exception as e:
            results.append({
                'product_id': product_data.get('id', 'unknown'),
                'action': 'error',
                'confidence': 0.0,
                'roi_estimate': 0.0,
                'risk_level': 'high',
                'reasoning': [f"Analysis failed: {str(e)}"]
            })
    
    return results

if __name__ == "__main__":
    # Test the system
    optimizer = AutoOptimizerAI()
    
    # Test product
    test_product = {
        'id': 'TEST-001',
        'name': 'Test Wireless Earbuds',
        'category': 'electronics',
        'roi': 35.5,
        'sales_rank': 12450,
        'gating': 'ungated',
        'current_price': 49.99,
        'competitor_prices': [59.99, 64.99, 52.99]
    }
    
    recommendation = optimizer.recommend_product(test_product)
    print(f"Recommendation: {recommendation.action}")
    print(f"Confidence: {recommendation.confidence:.2f}")
    print(f"ROI Estimate: {recommendation.roi_estimate:.1f}%")
    print(f"Reasoning: {', '.join(recommendation.reasoning)}")
