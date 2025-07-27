#!/usr/bin/env python3
"""
TrendAI Agent
Market trend analysis and prediction agent
Protected by USPTO #63/850,603
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List
import random

class TrendAI:
    """AI agent for market trend analysis and prediction"""
    
    def __init__(self):
        self.agent_name = "TrendAI"
        self.version = "1.0.0"
        self.status = "active"
        self.trend_indicators = ["price", "sales_rank", "review_count", "search_volume"]
        
    def analyze_trend(self, product_data: Dict[str, Any], time_period: int = 30) -> Dict[str, Any]:
        """Analyze market trend for a product"""
        try:
            historical_data = product_data.get("historical_data", [])
            current_metrics = product_data.get("current_metrics", {})
            
            if not historical_data:
                # Generate simulated trend data
                historical_data = self._generate_trend_data(time_period)
            
            trend_analysis = {}
            
            for indicator in self.trend_indicators:
                if indicator in current_metrics:
                    trend_direction = self._calculate_trend_direction(historical_data, indicator)
                    trend_strength = self._calculate_trend_strength(historical_data, indicator)
                    
                    trend_analysis[indicator] = {
                        "direction": trend_direction,
                        "strength": trend_strength,
                        "current_value": current_metrics[indicator],
                        "prediction": self._predict_future_value(historical_data, indicator)
                    }
            
            overall_trend = self._calculate_overall_trend(trend_analysis)
            
            result = {
                "product_id": product_data.get("asin", "Unknown"),
                "analysis_period": f"{time_period} days",
                "trend_analysis": trend_analysis,
                "overall_trend": overall_trend,
                "market_signals": self._generate_market_signals(trend_analysis),
                "recommendations": self._generate_recommendations(overall_trend),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"TrendAI analyzed trend: {overall_trend['direction']} with {overall_trend['confidence']}% confidence")
            return result
            
        except Exception as e:
            logging.error(f"Trend analysis failed: {e}")
            return {"error": str(e)}
    
    def predict_seasonal_trends(self, category: str) -> Dict[str, Any]:
        """Predict seasonal trends for a product category"""
        try:
            seasonal_patterns = {
                "Electronics": {
                    "Q1": {"demand": "low", "factor": 0.8},
                    "Q2": {"demand": "medium", "factor": 1.0},
                    "Q3": {"demand": "high", "factor": 1.3},
                    "Q4": {"demand": "peak", "factor": 1.6}
                },
                "Home & Kitchen": {
                    "Q1": {"demand": "medium", "factor": 1.1},
                    "Q2": {"demand": "high", "factor": 1.2},
                    "Q3": {"demand": "medium", "factor": 1.0},
                    "Q4": {"demand": "high", "factor": 1.3}
                },
                "Sports & Outdoors": {
                    "Q1": {"demand": "medium", "factor": 1.0},
                    "Q2": {"demand": "peak", "factor": 1.5},
                    "Q3": {"demand": "high", "factor": 1.3},
                    "Q4": {"demand": "low", "factor": 0.7}
                }
            }
            
            pattern = seasonal_patterns.get(category, {
                "Q1": {"demand": "medium", "factor": 1.0},
                "Q2": {"demand": "medium", "factor": 1.0},
                "Q3": {"demand": "medium", "factor": 1.0},
                "Q4": {"demand": "high", "factor": 1.2}
            })
            
            current_quarter = f"Q{((datetime.now().month - 1) // 3) + 1}"
            
            result = {
                "category": category,
                "seasonal_pattern": pattern,
                "current_quarter": current_quarter,
                "current_demand": pattern[current_quarter]["demand"],
                "demand_factor": pattern[current_quarter]["factor"],
                "best_quarters": [q for q, data in pattern.items() if data["factor"] >= 1.3],
                "analysis_date": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            logging.error(f"Seasonal trend prediction failed: {e}")
            return {"error": str(e)}
    
    def _generate_trend_data(self, days: int) -> List[Dict[str, Any]]:
        """Generate simulated historical trend data"""
        data = []
        base_date = datetime.now() - timedelta(days=days)
        
        for i in range(days):
            date = base_date + timedelta(days=i)
            data.append({
                "date": date.isoformat(),
                "price": 25.99 + random.uniform(-5, 5),
                "sales_rank": 10000 + random.randint(-2000, 2000),
                "review_count": 100 + random.randint(0, 10),
                "search_volume": 1000 + random.randint(-200, 200)
            })
        
        return data
    
    def _calculate_trend_direction(self, data: List[Dict], indicator: str) -> str:
        """Calculate trend direction for an indicator"""
        if len(data) < 2:
            return "stable"
        
        recent_avg = sum(item.get(indicator, 0) for item in data[-7:]) / min(7, len(data))
        older_avg = sum(item.get(indicator, 0) for item in data[:7]) / min(7, len(data))
        
        if recent_avg > older_avg * 1.05:
            return "increasing"
        elif recent_avg < older_avg * 0.95:
            return "decreasing"
        else:
            return "stable"
    
    def _calculate_trend_strength(self, data: List[Dict], indicator: str) -> float:
        """Calculate trend strength (0-100)"""
        if len(data) < 2:
            return 50.0
        
        values = [item.get(indicator, 0) for item in data]
        volatility = sum(abs(values[i] - values[i-1]) for i in range(1, len(values))) / len(values)
        
        # Normalize volatility to strength score
        strength = max(0, min(100, 100 - (volatility / max(values) * 100) if max(values) > 0 else 50))
        return round(strength, 1)
    
    def _predict_future_value(self, data: List[Dict], indicator: str) -> float:
        """Predict future value based on trend"""
        if not data:
            return 0
        
        recent_values = [item.get(indicator, 0) for item in data[-5:]]
        return sum(recent_values) / len(recent_values) if recent_values else 0
    
    def _calculate_overall_trend(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall trend from individual indicators"""
        directions = [info["direction"] for info in analysis.values()]
        strengths = [info["strength"] for info in analysis.values()]
        
        # Count direction votes
        increasing = directions.count("increasing")
        decreasing = directions.count("decreasing")
        stable = directions.count("stable")
        
        if increasing > decreasing and increasing > stable:
            overall_direction = "bullish"
        elif decreasing > increasing and decreasing > stable:
            overall_direction = "bearish"
        else:
            overall_direction = "neutral"
        
        avg_strength = sum(strengths) / len(strengths) if strengths else 50
        
        return {
            "direction": overall_direction,
            "confidence": round(avg_strength, 1),
            "signal_strength": "strong" if avg_strength > 75 else "moderate" if avg_strength > 50 else "weak"
        }
    
    def _generate_market_signals(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable market signals"""
        signals = []
        
        for indicator, data in analysis.items():
            if data["direction"] == "increasing" and data["strength"] > 70:
                signals.append(f"Strong upward momentum in {indicator}")
            elif data["direction"] == "decreasing" and data["strength"] > 70:
                signals.append(f"Strong downward pressure in {indicator}")
        
        return signals
    
    def _generate_recommendations(self, overall_trend: Dict[str, Any]) -> List[str]:
        """Generate trend-based recommendations"""
        recommendations = []
        
        direction = overall_trend["direction"]
        confidence = overall_trend["confidence"]
        
        if direction == "bullish" and confidence > 70:
            recommendations.extend([
                "Consider increasing inventory levels",
                "Optimize pricing for growth",
                "Expand marketing efforts"
            ])
        elif direction == "bearish" and confidence > 70:
            recommendations.extend([
                "Reduce inventory exposure",
                "Consider promotional pricing",
                "Focus on cost optimization"
            ])
        else:
            recommendations.extend([
                "Monitor market closely",
                "Maintain current strategy",
                "Prepare for trend reversal"
            ])
        
        return recommendations
    
    def run(self, input_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main execution method"""
        input_data = input_data or {}
        
        if "product_data" in input_data:
            return self.analyze_trend(
                input_data["product_data"],
                input_data.get("time_period", 30)
            )
        elif "category" in input_data:
            return self.predict_seasonal_trends(input_data["category"])
        
        return {
            "status": "ready",
            "agent": self.agent_name,
            "capabilities": ["trend_analysis", "seasonal_prediction", "market_signals"],
            "indicators": self.trend_indicators
        }

if __name__ == "__main__":
    agent = TrendAI()
    print(json.dumps(agent.run(), indent=2))
