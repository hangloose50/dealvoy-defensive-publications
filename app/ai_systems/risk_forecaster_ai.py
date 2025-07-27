#!/usr/bin/env python3
"""
⚠️ RiskForecaster AI - Predicts market risks and investment safety
Advanced risk analysis and forecasting for e-commerce arbitrage
"""

import json
import time
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

class RiskForecasterAI:
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.reports_dir = self.project_path / "dist" / "intelligence_reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.risk_models = self._initialize_risk_models()
        
    def _initialize_risk_models(self) -> Dict[str, Any]:
        """Initialize risk assessment models and parameters"""
        return {
            "risk_categories": {
                "market_risk": {
                    "weight": 0.25,
                    "factors": ["competition_level", "market_saturation", "price_volatility"],
                    "description": "Risk from market conditions and competition"
                },
                "operational_risk": {
                    "weight": 0.20,
                    "factors": ["supplier_reliability", "shipping_delays", "inventory_management"],
                    "description": "Risk from operational challenges"
                },
                "financial_risk": {
                    "weight": 0.20,
                    "factors": ["margin_pressure", "cash_flow", "payment_terms"],
                    "description": "Risk from financial factors"
                },
                "regulatory_risk": {
                    "weight": 0.15,
                    "factors": ["policy_changes", "compliance_requirements", "platform_restrictions"],
                    "description": "Risk from regulatory changes"
                },
                "product_risk": {
                    "weight": 0.20,
                    "factors": ["return_rates", "quality_issues", "seasonal_dependency"],
                    "description": "Risk specific to products"
                }
            },
            "risk_thresholds": {
                "low": 0.3,
                "medium": 0.6,
                "high": 0.8
            },
            "forecasting_models": {
                "trend_analysis": {"lookback_days": 90, "confidence_interval": 0.85},
                "volatility_analysis": {"window_size": 30, "threshold": 0.2},
                "seasonal_analysis": {"cycle_length": 365, "min_history": 180}
            }
        }
    
    def assess_market_risk(self, market_data: Dict[str, Any]) -> Dict[str, float]:
        """Assess market-related risks"""
        risk_scores = {}
        
        # Competition risk
        competition_level = market_data.get("competition_level", 0.5)
        risk_scores["competition_risk"] = min(competition_level * 1.2, 1.0)
        
        # Market saturation risk
        market_size = market_data.get("market_size", 50000)
        new_entrants = market_data.get("new_entrants_monthly", 10)
        saturation_rate = new_entrants / (market_size / 1000)  # Normalized
        risk_scores["saturation_risk"] = min(saturation_rate * 0.8, 1.0)
        
        # Price volatility risk
        price_variance = market_data.get("price_variance_30d", 0.15)
        risk_scores["volatility_risk"] = min(price_variance * 3, 1.0)
        
        # Platform dependency risk
        platform_concentration = market_data.get("single_platform_dependency", 0.7)
        risk_scores["platform_risk"] = platform_concentration
        
        return risk_scores
    
    def assess_operational_risk(self, operational_data: Dict[str, Any]) -> Dict[str, float]:
        """Assess operational risks"""
        risk_scores = {}
        
        # Supplier reliability risk
        supplier_rating = operational_data.get("supplier_reliability_score", 0.8)
        risk_scores["supplier_risk"] = 1 - supplier_rating
        
        # Shipping and logistics risk
        shipping_delays = operational_data.get("avg_shipping_delay_days", 2)
        risk_scores["logistics_risk"] = min(shipping_delays / 10, 1.0)
        
        # Inventory management risk
        inventory_turnover = operational_data.get("inventory_turnover_ratio", 6)
        optimal_turnover = 8  # Target turnover ratio
        if inventory_turnover < optimal_turnover:
            risk_scores["inventory_risk"] = (optimal_turnover - inventory_turnover) / optimal_turnover
        else:
            risk_scores["inventory_risk"] = 0.1  # Low risk for high turnover
        
        # Quality control risk
        defect_rate = operational_data.get("product_defect_rate", 0.02)
        risk_scores["quality_risk"] = min(defect_rate * 10, 1.0)
        
        return risk_scores
    
    def assess_financial_risk(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """Assess financial risks"""
        risk_scores = {}
        
        # Margin pressure risk
        current_margin = financial_data.get("current_margin", 0.25)
        target_margin = financial_data.get("target_margin", 0.30)
        if current_margin < target_margin:
            risk_scores["margin_risk"] = (target_margin - current_margin) / target_margin
        else:
            risk_scores["margin_risk"] = 0.1
        
        # Cash flow risk
        cash_flow_ratio = financial_data.get("operating_cash_flow_ratio", 1.2)
        if cash_flow_ratio < 1.0:
            risk_scores["cashflow_risk"] = 1 - cash_flow_ratio
        else:
            risk_scores["cashflow_risk"] = max(0, (1.5 - cash_flow_ratio) / 1.5)
        
        # Payment terms risk
        avg_payment_days = financial_data.get("avg_payment_terms_days", 30)
        risk_scores["payment_risk"] = min(avg_payment_days / 60, 1.0)
        
        # Currency exposure risk (for international sourcing)
        currency_exposure = financial_data.get("foreign_currency_exposure", 0.2)
        risk_scores["currency_risk"] = currency_exposure
        
        return risk_scores
    
    def assess_regulatory_risk(self, regulatory_data: Dict[str, Any]) -> Dict[str, float]:
        """Assess regulatory and compliance risks"""
        risk_scores = {}
        
        # Platform policy risk
        policy_changes_frequency = regulatory_data.get("policy_changes_per_year", 2)
        risk_scores["policy_risk"] = min(policy_changes_frequency / 6, 1.0)
        
        # Compliance complexity risk
        compliance_requirements = regulatory_data.get("compliance_requirements_count", 5)
        risk_scores["compliance_risk"] = min(compliance_requirements / 10, 1.0)
        
        # International trade risk
        cross_border_percentage = regulatory_data.get("cross_border_trade_percentage", 0.1)
        risk_scores["trade_risk"] = cross_border_percentage
        
        # Intellectual property risk
        ip_dispute_likelihood = regulatory_data.get("ip_dispute_likelihood", 0.05)
        risk_scores["ip_risk"] = ip_dispute_likelihood
        
        return risk_scores
    
    def assess_product_risk(self, product_data: Dict[str, Any]) -> Dict[str, float]:
        """Assess product-specific risks"""
        risk_scores = {}
        
        # Return rate risk
        return_rate = product_data.get("return_rate", 0.1)
        risk_scores["return_risk"] = min(return_rate * 2, 1.0)
        
        # Seasonal dependency risk
        seasonal_variance = product_data.get("seasonal_variance", 0.3)
        risk_scores["seasonal_risk"] = seasonal_variance
        
        # Product lifecycle risk
        product_age_months = product_data.get("product_age_months", 12)
        typical_lifecycle = product_data.get("typical_lifecycle_months", 36)
        lifecycle_progress = product_age_months / typical_lifecycle
        risk_scores["lifecycle_risk"] = min(lifecycle_progress, 1.0)
        
        # Brand dependency risk
        brand_concentration = product_data.get("single_brand_dependency", 0.4)
        risk_scores["brand_risk"] = brand_concentration
        
        return risk_scores
    
    def calculate_composite_risk_score(self, all_risk_assessments: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """Calculate composite risk score from all assessments"""
        category_scores = {}
        
        # Calculate weighted average for each category
        for category, weight in [(k, v["weight"]) for k, v in self.risk_models["risk_categories"].items()]:
            if category.replace("_risk", "") in all_risk_assessments:
                risk_data = all_risk_assessments[category.replace("_risk", "")]
                category_avg = sum(risk_data.values()) / len(risk_data) if risk_data else 0.5
                category_scores[category] = category_avg * weight
        
        # Overall risk score
        overall_risk = sum(category_scores.values())
        risk_level = self._get_risk_level(overall_risk)
        
        return {
            "overall_risk_score": round(overall_risk, 3),
            "risk_level": risk_level,
            "category_scores": category_scores,
            "risk_breakdown": self._generate_risk_breakdown(category_scores),
            "confidence": self._calculate_risk_confidence(all_risk_assessments)
        }
    
    def _get_risk_level(self, score: float) -> str:
        """Convert risk score to level"""
        thresholds = self.risk_models["risk_thresholds"]
        if score >= thresholds["high"]:
            return "HIGH"
        elif score >= thresholds["medium"]:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_risk_breakdown(self, category_scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """Generate detailed risk breakdown"""
        breakdown = []
        
        for category, score in category_scores.items():
            risk_info = self.risk_models["risk_categories"].get(category, {})
            breakdown.append({
                "category": category.replace("_", " ").title(),
                "score": round(score, 3),
                "level": self._get_risk_level(score / risk_info.get("weight", 0.2)),
                "description": risk_info.get("description", ""),
                "contribution": round((score / sum(category_scores.values())) * 100, 1) if sum(category_scores.values()) > 0 else 0
            })
        
        # Sort by contribution
        breakdown.sort(key=lambda x: x["contribution"], reverse=True)
        return breakdown
    
    def _calculate_risk_confidence(self, all_assessments: Dict[str, Dict[str, float]]) -> float:
        """Calculate confidence in risk assessment"""
        data_completeness = len(all_assessments) / len(self.risk_models["risk_categories"])
        
        # Factor in data quality
        total_factors = sum(len(factors) for factors in all_assessments.values())
        non_zero_factors = sum(1 for factors in all_assessments.values() 
                              for score in factors.values() if score > 0)
        
        data_quality = non_zero_factors / total_factors if total_factors > 0 else 0.5
        
        # Combined confidence
        confidence = (data_completeness * 0.6) + (data_quality * 0.4)
        return round(confidence, 3)
    
    def forecast_risk_trends(self, historical_data: List[Dict[str, Any]], 
                           forecast_days: int = 30) -> Dict[str, Any]:
        """Forecast risk trends based on historical data"""
        if len(historical_data) < 7:
            return {
                "error": "Insufficient historical data for forecasting",
                "minimum_required": 7,
                "provided": len(historical_data)
            }
        
        # Extract risk scores from historical data
        risk_timeline = []
        for entry in historical_data[-30:]:  # Last 30 data points
            if "risk_score" in entry:
                risk_timeline.append({
                    "date": entry.get("date", ""),
                    "risk_score": entry["risk_score"],
                    "volatility": entry.get("volatility", 0)
                })
        
        # Calculate trend
        recent_scores = [entry["risk_score"] for entry in risk_timeline[-7:]]
        earlier_scores = [entry["risk_score"] for entry in risk_timeline[-14:-7]] if len(risk_timeline) >= 14 else recent_scores
        
        recent_avg = sum(recent_scores) / len(recent_scores)
        earlier_avg = sum(earlier_scores) / len(earlier_scores)
        trend_direction = "increasing" if recent_avg > earlier_avg else "decreasing"
        trend_magnitude = abs(recent_avg - earlier_avg)
        
        # Forecast future risk
        forecast_base = recent_scores[-1] if recent_scores else 0.5
        trend_factor = trend_magnitude * (1 if trend_direction == "increasing" else -1)
        
        # Generate forecast
        forecast_points = []
        for day in range(1, forecast_days + 1):
            # Apply trend with diminishing effect over time
            diminishing_factor = math.exp(-day / 20)  # Trend effect diminishes over time
            forecasted_risk = forecast_base + (trend_factor * diminishing_factor * day / 7)
            forecasted_risk = max(0, min(forecasted_risk, 1.0))  # Clamp between 0 and 1
            
            forecast_date = datetime.now() + timedelta(days=day)
            forecast_points.append({
                "date": forecast_date.strftime("%Y-%m-%d"),
                "forecasted_risk": round(forecasted_risk, 3),
                "confidence": round(max(0.5, 1.0 - (day / forecast_days) * 0.5), 3)
            })
        
        return {
            "forecast_period_days": forecast_days,
            "trend_analysis": {
                "direction": trend_direction,
                "magnitude": round(trend_magnitude, 3),
                "current_risk": round(recent_avg, 3)
            },
            "forecast_points": forecast_points,
            "risk_alerts": self._generate_risk_alerts(forecast_points),
            "recommendations": self._generate_risk_recommendations(trend_direction, recent_avg)
        }
    
    def _generate_risk_alerts(self, forecast_points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate risk alerts based on forecast"""
        alerts = []
        
        for point in forecast_points:
            risk_score = point["forecasted_risk"]
            confidence = point["confidence"]
            
            if risk_score > 0.8 and confidence > 0.7:
                alerts.append({
                    "date": point["date"],
                    "alert_type": "HIGH_RISK",
                    "message": f"High risk level predicted ({risk_score:.1%})",
                    "urgency": "HIGH"
                })
            elif risk_score > 0.6 and confidence > 0.8:
                alerts.append({
                    "date": point["date"],
                    "alert_type": "MEDIUM_RISK",
                    "message": f"Elevated risk level predicted ({risk_score:.1%})",
                    "urgency": "MEDIUM"
                })
        
        return alerts
    
    def _generate_risk_recommendations(self, trend_direction: str, current_risk: float) -> List[str]:
        """Generate risk mitigation recommendations"""
        recommendations = []
        
        if trend_direction == "increasing":
            recommendations.append("Monitor risk factors closely as trend is increasing")
            recommendations.append("Consider reducing position sizes or diversifying")
            
            if current_risk > 0.7:
                recommendations.append("Implement immediate risk mitigation strategies")
                recommendations.append("Consider exit strategies for high-risk positions")
        else:
            recommendations.append("Risk trend is favorable, but maintain vigilance")
            
        if current_risk > 0.6:
            recommendations.append("Review and strengthen risk management protocols")
            recommendations.append("Increase monitoring frequency")
        
        recommendations.append("Regular portfolio rebalancing recommended")
        return recommendations
    
    def run(self) -> Dict[str, Any]:
        """Main execution function"""
        print("⚠️ [RiskForecaster AI] Analyzing risk landscape...")
        
        # Sample data for risk analysis
        sample_market_data = {
            "competition_level": 0.65,
            "market_size": 75000,
            "new_entrants_monthly": 12,
            "price_variance_30d": 0.18,
            "single_platform_dependency": 0.8
        }
        
        sample_operational_data = {
            "supplier_reliability_score": 0.85,
            "avg_shipping_delay_days": 3,
            "inventory_turnover_ratio": 6.5,
            "product_defect_rate": 0.015
        }
        
        sample_financial_data = {
            "current_margin": 0.22,
            "target_margin": 0.28,
            "operating_cash_flow_ratio": 1.1,
            "avg_payment_terms_days": 35,
            "foreign_currency_exposure": 0.15
        }
        
        sample_regulatory_data = {
            "policy_changes_per_year": 3,
            "compliance_requirements_count": 7,
            "cross_border_trade_percentage": 0.2,
            "ip_dispute_likelihood": 0.03
        }
        
        sample_product_data = {
            "return_rate": 0.12,
            "seasonal_variance": 0.4,
            "product_age_months": 18,
            "typical_lifecycle_months": 48,
            "single_brand_dependency": 0.6
        }
        
        # Generate historical data for forecasting
        historical_data = []
        base_date = datetime.now() - timedelta(days=30)
        for i in range(30):
            date = base_date + timedelta(days=i)
            # Simulate risk scores with some variance
            base_risk = 0.4 + (i * 0.01) + (math.sin(i * 0.3) * 0.1)
            historical_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "risk_score": max(0, min(base_risk, 1.0)),
                "volatility": 0.15 + (math.cos(i * 0.2) * 0.05)
            })
        
        print("   🔍 Assessing market risks...")
        market_risks = self.assess_market_risk(sample_market_data)
        
        print("   ⚙️ Evaluating operational risks...")
        operational_risks = self.assess_operational_risk(sample_operational_data)
        
        print("   💰 Analyzing financial risks...")
        financial_risks = self.assess_financial_risk(sample_financial_data)
        
        print("   📜 Checking regulatory risks...")
        regulatory_risks = self.assess_regulatory_risk(sample_regulatory_data)
        
        print("   📦 Examining product risks...")
        product_risks = self.assess_product_risk(sample_product_data)
        
        # Compile all risk assessments
        all_risk_assessments = {
            "market": market_risks,
            "operational": operational_risks,
            "financial": financial_risks,
            "regulatory": regulatory_risks,
            "product": product_risks
        }
        
        print("   📊 Calculating composite risk score...")
        composite_risk = self.calculate_composite_risk_score(all_risk_assessments)
        
        print("   🔮 Generating risk forecast...")
        risk_forecast = self.forecast_risk_trends(historical_data, 30)
        
        # Create comprehensive report
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "ai_system": "RiskForecasterAI",
                "version": "1.0.0",
                "assessment_categories": len(all_risk_assessments)
            },
            "executive_summary": {
                "overall_risk_level": composite_risk["risk_level"],
                "overall_risk_score": composite_risk["overall_risk_score"],
                "highest_risk_category": max(composite_risk["risk_breakdown"], key=lambda x: x["contribution"])["category"],
                "forecast_trend": risk_forecast["trend_analysis"]["direction"],
                "risk_alerts_count": len(risk_forecast["risk_alerts"]),
                "confidence": composite_risk["confidence"],
                "recommendation": self._get_overall_risk_recommendation(composite_risk, risk_forecast)
            },
            "detailed_risk_assessment": {
                "composite_analysis": composite_risk,
                "category_breakdown": all_risk_assessments,
                "risk_factors_summary": self._summarize_risk_factors(all_risk_assessments)
            },
            "risk_forecast": risk_forecast,
            "mitigation_strategies": self._generate_mitigation_strategies(composite_risk, all_risk_assessments)
        }
        
        # Save report
        report_file = self.reports_dir / f"risk_forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("✅ RiskForecaster AI: Analysis completed!")
        print(f"   ⚠️ Overall Risk Level: {composite_risk['risk_level']}")
        print(f"   📊 Risk Score: {composite_risk['overall_risk_score']:.3f}")
        print(f"   📈 Trend: {risk_forecast['trend_analysis']['direction'].title()}")
        print(f"   🚨 Alerts: {len(risk_forecast['risk_alerts'])}")
        print(f"   📄 Full Report: {report_file}")
        
        # Print top risk factors
        top_risks = sorted(composite_risk["risk_breakdown"], key=lambda x: x["contribution"], reverse=True)[:3]
        print("\n🎯 Top Risk Factors:")
        for risk in top_risks:
            print(f"   {risk['category']}: {risk['contribution']}% contribution ({risk['level']} level)")
        
        print("⚠️ [RiskForecaster AI] Ready for risk management!")
        return report
    
    def _summarize_risk_factors(self, all_assessments: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """Summarize key risk factors"""
        high_risk_factors = []
        medium_risk_factors = []
        
        for category, risks in all_assessments.items():
            for factor, score in risks.items():
                if score > 0.7:
                    high_risk_factors.append(f"{category}.{factor}")
                elif score > 0.4:
                    medium_risk_factors.append(f"{category}.{factor}")
        
        return {
            "high_risk_factors": high_risk_factors,
            "medium_risk_factors": medium_risk_factors,
            "total_factors_assessed": sum(len(risks) for risks in all_assessments.values())
        }
    
    def _generate_mitigation_strategies(self, composite_risk: Dict[str, Any], 
                                      all_assessments: Dict[str, Dict[str, float]]) -> List[Dict[str, Any]]:
        """Generate risk mitigation strategies"""
        strategies = []
        
        # Focus on highest contributing risk categories
        top_risks = sorted(composite_risk["risk_breakdown"], key=lambda x: x["contribution"], reverse=True)[:3]
        
        for risk_item in top_risks:
            category = risk_item["category"].lower().replace(" ", "_")
            
            if "market" in category:
                strategies.append({
                    "risk_category": risk_item["category"],
                    "strategy": "Diversification Strategy",
                    "actions": [
                        "Diversify across multiple product categories",
                        "Reduce dependency on single platforms",
                        "Monitor competitor activities closely"
                    ],
                    "priority": "HIGH" if risk_item["level"] == "HIGH" else "MEDIUM"
                })
            elif "operational" in category:
                strategies.append({
                    "risk_category": risk_item["category"],
                    "strategy": "Operational Excellence",
                    "actions": [
                        "Establish backup suppliers",
                        "Improve inventory management systems",
                        "Implement quality control processes"
                    ],
                    "priority": "HIGH" if risk_item["level"] == "HIGH" else "MEDIUM"
                })
            elif "financial" in category:
                strategies.append({
                    "risk_category": risk_item["category"],
                    "strategy": "Financial Risk Management",
                    "actions": [
                        "Improve cash flow management",
                        "Negotiate better payment terms",
                        "Consider currency hedging"
                    ],
                    "priority": "HIGH" if risk_item["level"] == "HIGH" else "MEDIUM"
                })
        
        return strategies
    
    def _get_overall_risk_recommendation(self, composite_risk: Dict[str, Any], 
                                       forecast: Dict[str, Any]) -> str:
        """Generate overall risk recommendation"""
        risk_level = composite_risk["risk_level"]
        trend = forecast["trend_analysis"]["direction"]
        alerts = len(forecast["risk_alerts"])
        
        if risk_level == "HIGH" or (risk_level == "MEDIUM" and trend == "increasing"):
            return "CAUTION: Implement immediate risk mitigation strategies"
        elif risk_level == "MEDIUM" and alerts > 3:
            return "MONITOR: Watch risk factors closely and prepare contingency plans"
        elif risk_level == "LOW" and trend == "decreasing":
            return "FAVORABLE: Risk environment is positive, maintain current strategies"
        else:
            return "STABLE: Continue monitoring with standard risk management practices"

def run():
    """CLI entry point"""
    risk_ai = RiskForecasterAI()
    risk_ai.run()

if __name__ == "__main__":
    run()
