#!/usr/bin/env python3
"""
💡 DealExplainer AI - Explains why deals are profitable and provides insights
Smart analysis and explanation system for e-commerce arbitrage decisions
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

class DealExplainerAI:
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.reports_dir = self.project_path / "dist" / "intelligence_reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.market_knowledge = self._load_market_knowledge()
        
    def _load_market_knowledge(self) -> Dict[str, Any]:
        """Load market intelligence and deal patterns"""
        return {
            "profitable_patterns": {
                "clearance_items": {
                    "profit_potential": 0.65,
                    "risk_level": "medium",
                    "explanation": "Clearance items often sell at 40-70% discount from MSRP, creating arbitrage opportunities"
                },
                "seasonal_mismatch": {
                    "profit_potential": 0.58,
                    "risk_level": "low",
                    "explanation": "Off-season items can be purchased cheap and sold during peak season"
                },
                "brand_premium": {
                    "profit_potential": 0.72,
                    "risk_level": "low",
                    "explanation": "Premium brands maintain value across platforms, enabling reliable arbitrage"
                },
                "new_product_launch": {
                    "profit_potential": 0.85,
                    "risk_level": "high",
                    "explanation": "New products may have pricing inconsistencies across platforms initially"
                },
                "bundle_breakup": {
                    "profit_potential": 0.55,
                    "risk_level": "medium",
                    "explanation": "Buying bundles and selling individual items can yield higher total revenue"
                }
            },
            "risk_indicators": {
                "high_return_rate": "Products with >20% return rate reduce net profit significantly",
                "patent_restrictions": "Check for patent or trademark restrictions before sourcing",
                "seasonal_dependency": "High seasonal variance increases inventory risk",
                "competition_surge": "Popular items may see rapid competition increase",
                "platform_policy": "Amazon/eBay policy changes can affect category profitability"
            },
            "success_factors": {
                "demand_validation": "Products with consistent sales rank indicate stable demand",
                "price_stability": "Items with stable pricing history are lower risk",
                "supplier_reliability": "Consistent supplier availability reduces sourcing risk",
                "market_size": "Larger markets provide more selling opportunities",
                "differentiation": "Unique value propositions reduce price competition"
            }
        }
    
    def analyze_deal_opportunity(self, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive analysis of a deal opportunity"""
        
        # Extract key metrics
        source_price = deal_data.get("source_price", 0)
        selling_price = deal_data.get("selling_price", 0)
        fees = deal_data.get("fees", 0)
        shipping_cost = deal_data.get("shipping_cost", 0)
        
        # Calculate profit metrics
        gross_profit = selling_price - source_price
        net_profit = gross_profit - fees - shipping_cost
        profit_margin = (net_profit / selling_price) if selling_price > 0 else 0
        roi = (net_profit / source_price) if source_price > 0 else 0
        
        # Analyze deal patterns
        deal_patterns = self._identify_deal_patterns(deal_data)
        risk_assessment = self._assess_deal_risks(deal_data)
        success_indicators = self._evaluate_success_factors(deal_data)
        
        # Generate explanations
        profitability_explanation = self._explain_profitability(
            profit_margin, roi, deal_patterns
        )
        risk_explanation = self._explain_risks(risk_assessment)
        recommendation = self._generate_recommendation(
            profit_margin, roi, risk_assessment, success_indicators
        )
        
        return {
            "deal_id": deal_data.get("product_name", "Unknown"),
            "financial_analysis": {
                "source_price": source_price,
                "selling_price": selling_price,
                "gross_profit": round(gross_profit, 2),
                "net_profit": round(net_profit, 2),
                "profit_margin": round(profit_margin * 100, 1),
                "roi": round(roi * 100, 1)
            },
            "deal_patterns": deal_patterns,
            "risk_assessment": risk_assessment,
            "success_indicators": success_indicators,
            "explanations": {
                "profitability": profitability_explanation,
                "risks": risk_explanation,
                "why_profitable": self._explain_why_profitable(deal_patterns, profit_margin),
                "key_insights": self._generate_key_insights(deal_data, profit_margin, roi)
            },
            "recommendation": recommendation,
            "confidence_score": self._calculate_confidence_score(
                profit_margin, risk_assessment, success_indicators
            )
        }
    
    def _identify_deal_patterns(self, deal_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify which profitable patterns this deal matches"""
        patterns = []
        
        # Check for clearance pattern
        if deal_data.get("discount_percentage", 0) > 40:
            patterns.append({
                "pattern": "clearance_items",
                "confidence": 0.8,
                "explanation": self.market_knowledge["profitable_patterns"]["clearance_items"]["explanation"]
            })
        
        # Check for brand premium
        brand = deal_data.get("brand", "").lower()
        premium_brands = ["apple", "sony", "nike", "lego", "dyson", "kitchenaid"]
        if any(pb in brand for pb in premium_brands):
            patterns.append({
                "pattern": "brand_premium",
                "confidence": 0.9,
                "explanation": self.market_knowledge["profitable_patterns"]["brand_premium"]["explanation"]
            })
        
        # Check for seasonal mismatch
        current_month = datetime.now().month
        category = deal_data.get("category", "").lower()
        if ("winter" in category or "holiday" in category) and current_month in [1,2,3,4]:
            patterns.append({
                "pattern": "seasonal_mismatch",
                "confidence": 0.7,
                "explanation": self.market_knowledge["profitable_patterns"]["seasonal_mismatch"]["explanation"]
            })
        
        return patterns
    
    def _assess_deal_risks(self, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risks associated with the deal"""
        risks = []
        risk_score = 0.0
        
        # High competition risk
        competition_level = deal_data.get("competition_level", 0.5)
        if competition_level > 0.8:
            risks.append("High competition may reduce margins")
            risk_score += 0.3
        
        # Return rate risk
        return_rate = deal_data.get("return_rate", 0.1)
        if return_rate > 0.2:
            risks.append("High return rate reduces net profit")
            risk_score += 0.25
        
        # Inventory risk
        sales_velocity = deal_data.get("sales_velocity", 0.5)
        if sales_velocity < 0.3:
            risks.append("Slow sales velocity increases inventory risk")
            risk_score += 0.2
        
        # Category risk
        category = deal_data.get("category", "").lower()
        if any(risky in category for risky in ["electronics", "fashion", "supplements"]):
            risks.append("Category has higher policy/return risks")
            risk_score += 0.15
        
        return {
            "risk_factors": risks,
            "risk_score": min(risk_score, 1.0),
            "risk_level": self._get_risk_level(risk_score)
        }
    
    def _get_risk_level(self, score: float) -> str:
        """Convert risk score to level"""
        if score >= 0.7:
            return "HIGH"
        elif score >= 0.4:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _evaluate_success_factors(self, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate factors that contribute to success"""
        success_factors = []
        success_score = 0.0
        
        # Demand validation
        sales_rank = deal_data.get("sales_rank", 1000000)
        if sales_rank < 50000:
            success_factors.append("Strong demand indicated by good sales rank")
            success_score += 0.3
        
        # Price stability
        price_variance = deal_data.get("price_variance", 0.5)
        if price_variance < 0.2:
            success_factors.append("Stable pricing history reduces risk")
            success_score += 0.25
        
        # Market size
        monthly_searches = deal_data.get("monthly_searches", 1000)
        if monthly_searches > 10000:
            success_factors.append("Large market provides good selling opportunities")
            success_score += 0.2
        
        # Profit margin
        profit_margin = deal_data.get("profit_margin", 0)
        if profit_margin > 0.3:
            success_factors.append("Healthy profit margin allows for price flexibility")
            success_score += 0.25
        
        return {
            "success_factors": success_factors,
            "success_score": min(success_score, 1.0)
        }
    
    def _explain_profitability(self, profit_margin: float, roi: float, patterns: List[Dict[str, Any]]) -> str:
        """Explain why the deal is profitable"""
        explanations = []
        
        if profit_margin > 0.3:
            explanations.append(f"Healthy {profit_margin*100:.1f}% profit margin provides good cushion for fees and unexpected costs")
        elif profit_margin > 0.15:
            explanations.append(f"Moderate {profit_margin*100:.1f}% profit margin offers reasonable returns")
        else:
            explanations.append(f"Low {profit_margin*100:.1f}% profit margin requires careful cost management")
        
        if roi > 0.5:
            explanations.append(f"Excellent {roi*100:.1f}% ROI indicates strong return on investment")
        elif roi > 0.25:
            explanations.append(f"Good {roi*100:.1f}% ROI provides solid returns")
        
        # Add pattern explanations
        for pattern in patterns:
            explanations.append(pattern["explanation"])
        
        return " | ".join(explanations)
    
    def _explain_risks(self, risk_assessment: Dict[str, Any]) -> str:
        """Explain the risks associated with the deal"""
        if not risk_assessment["risk_factors"]:
            return "Low risk opportunity with minimal concerns identified"
        
        risk_explanation = f"{risk_assessment['risk_level']} risk deal. "
        risk_explanation += "Key concerns: " + ", ".join(risk_assessment["risk_factors"])
        
        return risk_explanation
    
    def _explain_why_profitable(self, patterns: List[Dict[str, Any]], profit_margin: float) -> str:
        """Explain the core reasons why this deal is profitable"""
        if not patterns and profit_margin < 0.1:
            return "Limited profitability due to low margins and no clear arbitrage patterns"
        
        reasons = []
        if patterns:
            reasons.append(f"Matches {len(patterns)} profitable patterns: {', '.join([p['pattern'].replace('_', ' ').title() for p in patterns])}")
        
        if profit_margin > 0.2:
            reasons.append("Strong margin provides buffer against costs and competition")
        
        if not reasons:
            reasons.append("Basic arbitrage opportunity based on price differential")
        
        return " | ".join(reasons)
    
    def _generate_key_insights(self, deal_data: Dict[str, Any], profit_margin: float, roi: float) -> List[str]:
        """Generate key insights about the deal"""
        insights = []
        
        # Profit insights
        if profit_margin > 0.4:
            insights.append("Premium profit margins suggest strong value proposition or market inefficiency")
        elif profit_margin < 0.1:
            insights.append("Thin margins require high volume or cost optimization to be worthwhile")
        
        # Competition insights
        competition = deal_data.get("competition_level", 0.5)
        if competition < 0.3:
            insights.append("Low competition creates favorable selling environment")
        elif competition > 0.8:
            insights.append("High competition may require aggressive pricing or unique positioning")
        
        # Market insights
        sales_rank = deal_data.get("sales_rank", 1000000)
        if sales_rank < 10000:
            insights.append("Excellent sales rank indicates strong and consistent demand")
        
        # Category insights
        category = deal_data.get("category", "")
        if "electronics" in category.lower():
            insights.append("Electronics category requires attention to rapid technology changes")
        
        return insights
    
    def _generate_recommendation(self, profit_margin: float, roi: float, 
                               risk_assessment: Dict[str, Any], success_indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final recommendation"""
        
        # Calculate overall score
        profit_score = min(profit_margin * 3, 1.0)  # 33%+ margin = 1.0
        roi_score = min(roi * 2, 1.0)  # 50%+ ROI = 1.0
        risk_score = 1 - risk_assessment["risk_score"]
        success_score = success_indicators["success_score"]
        
        overall_score = (profit_score * 0.3 + roi_score * 0.3 + risk_score * 0.2 + success_score * 0.2)
        
        # Generate recommendation
        if overall_score >= 0.8:
            action = "STRONG BUY"
            reasoning = "Excellent opportunity with strong profits and manageable risks"
        elif overall_score >= 0.6:
            action = "BUY"
            reasoning = "Good opportunity with solid profit potential"
        elif overall_score >= 0.4:
            action = "CONSIDER"
            reasoning = "Moderate opportunity, evaluate carefully against alternatives"
        else:
            action = "PASS"
            reasoning = "Poor opportunity with limited profit potential or high risks"
        
        return {
            "action": action,
            "reasoning": reasoning,
            "confidence": round(overall_score * 100, 1),
            "priority": "HIGH" if overall_score >= 0.7 else "MEDIUM" if overall_score >= 0.5 else "LOW"
        }
    
    def _calculate_confidence_score(self, profit_margin: float, risk_assessment: Dict[str, Any], 
                                  success_indicators: Dict[str, Any]) -> float:
        """Calculate confidence in the analysis"""
        confidence = 0.5  # Base confidence
        
        # Higher margins increase confidence
        if profit_margin > 0.3:
            confidence += 0.3
        elif profit_margin > 0.15:
            confidence += 0.15
        
        # Lower risk increases confidence
        if risk_assessment["risk_score"] < 0.3:
            confidence += 0.2
        elif risk_assessment["risk_score"] < 0.6:
            confidence += 0.1
        
        # Success factors increase confidence
        confidence += success_indicators["success_score"] * 0.3
        
        return min(confidence, 1.0)
    
    def batch_analyze_deals(self, deals_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze multiple deals and compare them"""
        analyses = []
        
        for deal in deals_list:
            analysis = self.analyze_deal_opportunity(deal)
            analyses.append(analysis)
        
        # Sort by confidence score
        analyses.sort(key=lambda x: x["confidence_score"], reverse=True)
        
        # Generate batch insights
        batch_insights = {
            "total_deals": len(deals_list),
            "strong_buys": len([a for a in analyses if a["recommendation"]["action"] == "STRONG BUY"]),
            "buys": len([a for a in analyses if a["recommendation"]["action"] == "BUY"]),
            "average_margin": round(sum([a["financial_analysis"]["profit_margin"] for a in analyses]) / len(analyses), 1),
            "average_roi": round(sum([a["financial_analysis"]["roi"] for a in analyses]) / len(analyses), 1),
            "top_recommendations": analyses[:5]
        }
        
        return {
            "batch_analysis": batch_insights,
            "individual_analyses": analyses
        }
    
    def run(self) -> Dict[str, Any]:
        """Main execution function"""
        print("💡 [DealExplainer AI] Analyzing deal opportunities...")
        
        # Sample deals for analysis
        sample_deals = [
            {
                "product_name": "Wireless Bluetooth Earbuds",
                "source_price": 25.00,
                "selling_price": 49.99,
                "fees": 7.50,
                "shipping_cost": 3.00,
                "brand": "Sony",
                "category": "Electronics",
                "discount_percentage": 45,
                "competition_level": 0.7,
                "return_rate": 0.08,
                "sales_velocity": 0.8,
                "sales_rank": 25000,
                "monthly_searches": 15000,
                "price_variance": 0.15
            },
            {
                "product_name": "Kitchen Storage Containers",
                "source_price": 12.00,
                "selling_price": 24.99,
                "fees": 3.75,
                "shipping_cost": 2.50,
                "brand": "Rubbermaid",
                "category": "Home & Kitchen",
                "discount_percentage": 35,
                "competition_level": 0.5,
                "return_rate": 0.12,
                "sales_velocity": 0.6,
                "sales_rank": 45000,
                "monthly_searches": 8000,
                "price_variance": 0.1
            },
            {
                "product_name": "Fitness Resistance Bands",
                "source_price": 8.00,
                "selling_price": 19.99,
                "fees": 3.00,
                "shipping_cost": 2.00,
                "brand": "Generic",
                "category": "Sports & Outdoors",
                "discount_percentage": 50,
                "competition_level": 0.9,
                "return_rate": 0.15,
                "sales_velocity": 0.4,
                "sales_rank": 85000,
                "monthly_searches": 5000,
                "price_variance": 0.3
            }
        ]
        
        print(f"   🔍 Analyzing {len(sample_deals)} deal opportunities...")
        
        # Analyze individual deals
        individual_analyses = []
        for deal in sample_deals:
            analysis = self.analyze_deal_opportunity(deal)
            individual_analyses.append(analysis)
        
        # Batch analysis
        print("   📊 Generating batch insights...")
        batch_results = self.batch_analyze_deals(sample_deals)
        
        # Create comprehensive report
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "ai_system": "DealExplainerAI",
                "version": "1.0.0",
                "deals_analyzed": len(sample_deals)
            },
            "executive_summary": {
                "total_deals_analyzed": len(sample_deals),
                "strong_buy_recommendations": batch_results["batch_analysis"]["strong_buys"],
                "buy_recommendations": batch_results["batch_analysis"]["buys"],
                "average_profit_margin": batch_results["batch_analysis"]["average_margin"],
                "average_roi": batch_results["batch_analysis"]["average_roi"],
                "top_deal": batch_results["batch_analysis"]["top_recommendations"][0]["deal_id"] if batch_results["batch_analysis"]["top_recommendations"] else "None"
            },
            "deal_analyses": individual_analyses,
            "batch_insights": batch_results["batch_analysis"],
            "market_intelligence": self.market_knowledge
        }
        
        # Save report
        report_file = self.reports_dir / f"deal_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("✅ DealExplainer AI: Analysis completed!")
        print(f"   📦 Deals analyzed: {len(sample_deals)}")
        print(f"   ⭐ Strong Buy recommendations: {report['executive_summary']['strong_buy_recommendations']}")
        print(f"   💰 Average profit margin: {report['executive_summary']['average_profit_margin']}%")
        print(f"   📈 Average ROI: {report['executive_summary']['average_roi']}%")
        print(f"   📄 Full Report: {report_file}")
        
        # Print top deal explanation
        if individual_analyses:
            top_deal = individual_analyses[0]
            print(f"\n🎯 Top Deal Analysis - {top_deal['deal_id']}:")
            print(f"   Action: {top_deal['recommendation']['action']}")
            print(f"   Confidence: {top_deal['confidence_score']*100:.1f}%")
            print(f"   Profit Margin: {top_deal['financial_analysis']['profit_margin']}%")
            print(f"   Why Profitable: {top_deal['explanations']['why_profitable']}")
        
        print("💡 [DealExplainer AI] Ready for intelligent deal analysis!")
        return report

def run():
    """CLI entry point"""
    deal_ai = DealExplainerAI()
    deal_ai.run()

if __name__ == "__main__":
    run()
