#!/usr/bin/env python3
"""
💰 CashflowPredictor AI - Predicts cash flow and financial scenarios
Advanced financial forecasting for e-commerce arbitrage optimization
"""

import json
import time
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

class CashflowPredictorAI:
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.reports_dir = self.project_path / "dist" / "intelligence_reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.financial_models = self._initialize_financial_models()
        
    def _initialize_financial_models(self) -> Dict[str, Any]:
        """Initialize financial forecasting models and parameters"""
        return {
            "cash_flow_components": {
                "revenue_streams": {
                    "product_sales": {"volatility": 0.15, "growth_trend": 0.02},
                    "bundled_products": {"volatility": 0.20, "growth_trend": 0.05},
                    "premium_margins": {"volatility": 0.25, "growth_trend": 0.03},
                    "volume_discounts": {"volatility": 0.10, "growth_trend": 0.01}
                },
                "expense_categories": {
                    "product_costs": {"percentage": 0.65, "variability": 0.05},
                    "platform_fees": {"percentage": 0.15, "variability": 0.02},
                    "shipping_costs": {"percentage": 0.08, "variability": 0.10},
                    "storage_fees": {"percentage": 0.03, "variability": 0.15},
                    "advertising": {"percentage": 0.05, "variability": 0.20},
                    "operational": {"percentage": 0.04, "variability": 0.05}
                }
            },
            "seasonality_patterns": {
                "Q1": {"multiplier": 0.85, "description": "Post-holiday slowdown"},
                "Q2": {"multiplier": 0.95, "description": "Spring recovery"},
                "Q3": {"multiplier": 1.05, "description": "Summer growth"},
                "Q4": {"multiplier": 1.35, "description": "Holiday surge"}
            },
            "risk_factors": {
                "market_volatility": 0.12,
                "supplier_disruption": 0.08,
                "platform_policy": 0.05,
                "competition_impact": 0.10,
                "economic_conditions": 0.15
            },
            "forecasting_parameters": {
                "confidence_intervals": [0.50, 0.80, 0.95],
                "monte_carlo_iterations": 1000,
                "scenario_count": 3,  # Conservative, Expected, Optimistic
                "forecast_horizon_months": 12
            }
        }
    
    def analyze_current_financial_position(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current financial health and cash flow position"""
        monthly_revenue = financial_data.get("monthly_revenue", 0)
        monthly_expenses = financial_data.get("monthly_expenses", 0)
        current_cash = financial_data.get("current_cash", 0)
        inventory_value = financial_data.get("inventory_value", 0)
        
        # Calculate key metrics
        monthly_profit = monthly_revenue - monthly_expenses
        profit_margin = (monthly_profit / monthly_revenue) if monthly_revenue > 0 else 0
        cash_runway = (current_cash / monthly_expenses) if monthly_expenses > 0 else float('inf')
        
        # Working capital analysis
        working_capital = current_cash + inventory_value
        working_capital_ratio = working_capital / monthly_expenses if monthly_expenses > 0 else 0
        
        # Cash velocity
        cash_conversion_days = financial_data.get("cash_conversion_days", 45)
        inventory_turnover = 365 / cash_conversion_days if cash_conversion_days > 0 else 8
        
        return {
            "current_metrics": {
                "monthly_revenue": monthly_revenue,
                "monthly_expenses": monthly_expenses,
                "monthly_profit": round(monthly_profit, 2),
                "profit_margin": round(profit_margin * 100, 1),
                "cash_runway_months": round(cash_runway, 1) if cash_runway != float('inf') else "Indefinite"
            },
            "liquidity_analysis": {
                "current_cash": current_cash,
                "inventory_value": inventory_value,
                "working_capital": working_capital,
                "working_capital_ratio": round(working_capital_ratio, 2)
            },
            "operational_efficiency": {
                "cash_conversion_days": cash_conversion_days,
                "inventory_turnover": round(inventory_turnover, 1),
                "revenue_per_dollar_invested": round(monthly_revenue / max(working_capital, 1), 2)
            },
            "financial_health_score": self._calculate_financial_health_score(
                profit_margin, cash_runway, working_capital_ratio, inventory_turnover
            )
        }
    
    def _calculate_financial_health_score(self, profit_margin: float, cash_runway: float, 
                                        wc_ratio: float, inventory_turnover: float) -> Dict[str, Any]:
        """Calculate overall financial health score"""
        # Normalize scores (0-1)
        margin_score = min(max(profit_margin * 5, 0), 1)  # 20% margin = 1.0
        runway_score = min(cash_runway / 6, 1) if cash_runway != float('inf') else 1  # 6 months = 1.0
        liquidity_score = min(wc_ratio / 3, 1)  # 3x ratio = 1.0
        efficiency_score = min(inventory_turnover / 12, 1)  # 12 turns/year = 1.0
        
        # Weighted average
        overall_score = (margin_score * 0.3 + runway_score * 0.25 + 
                        liquidity_score * 0.25 + efficiency_score * 0.20)
        
        return {
            "overall_score": round(overall_score, 3),
            "score_breakdown": {
                "profitability": round(margin_score, 3),
                "cash_stability": round(runway_score, 3),
                "liquidity": round(liquidity_score, 3),
                "efficiency": round(efficiency_score, 3)
            },
            "health_level": self._get_health_level(overall_score),
            "improvement_priorities": self._identify_improvement_priorities(
                margin_score, runway_score, liquidity_score, efficiency_score
            )
        }
    
    def _get_health_level(self, score: float) -> str:
        """Convert health score to level"""
        if score >= 0.8:
            return "EXCELLENT"
        elif score >= 0.6:
            return "GOOD"
        elif score >= 0.4:
            return "FAIR"
        else:
            return "POOR"
    
    def _identify_improvement_priorities(self, margin: float, runway: float, 
                                       liquidity: float, efficiency: float) -> List[str]:
        """Identify areas needing improvement"""
        priorities = []
        scores = [
            (margin, "Improve profit margins"),
            (runway, "Build cash reserves"),
            (liquidity, "Increase working capital"),
            (efficiency, "Optimize inventory turnover")
        ]
        
        # Sort by lowest scores first
        scores.sort(key=lambda x: x[0])
        
        for score, priority in scores[:2]:  # Top 2 priorities
            if score < 0.7:
                priorities.append(priority)
        
        return priorities
    
    def generate_cash_flow_forecast(self, financial_data: Dict[str, Any], 
                                  forecast_months: int = 12) -> Dict[str, Any]:
        """Generate detailed cash flow forecast"""
        base_revenue = financial_data.get("monthly_revenue", 0)
        base_expenses = financial_data.get("monthly_expenses", 0)
        starting_cash = financial_data.get("current_cash", 0)
        
        # Generate monthly forecasts
        monthly_forecasts = []
        cumulative_cash = starting_cash
        
        for month in range(1, forecast_months + 1):
            month_data = self._forecast_month(
                month, base_revenue, base_expenses, cumulative_cash
            )
            cumulative_cash = month_data["ending_cash"]
            monthly_forecasts.append(month_data)
        
        # Calculate summary statistics
        total_revenue = sum(m["revenue"] for m in monthly_forecasts)
        total_expenses = sum(m["expenses"] for m in monthly_forecasts)
        net_profit = total_revenue - total_expenses
        
        return {
            "forecast_period": f"{forecast_months} months",
            "monthly_forecasts": monthly_forecasts,
            "summary_projections": {
                "total_revenue": round(total_revenue, 2),
                "total_expenses": round(total_expenses, 2),
                "net_profit": round(net_profit, 2),
                "final_cash_position": round(cumulative_cash, 2),
                "average_monthly_profit": round(net_profit / forecast_months, 2)
            },
            "cash_flow_insights": self._analyze_cash_flow_patterns(monthly_forecasts),
            "risk_assessment": self._assess_forecast_risks(monthly_forecasts, financial_data)
        }
    
    def _forecast_month(self, month: int, base_revenue: float, 
                       base_expenses: float, starting_cash: float) -> Dict[str, Any]:
        """Forecast a single month's cash flow"""
        # Apply seasonality
        quarter = ((month - 1) // 3) + 1
        quarter_key = f"Q{quarter}"
        seasonal_multiplier = self.financial_models["seasonality_patterns"][quarter_key]["multiplier"]
        
        # Apply growth trend (assuming 2% monthly growth)
        growth_factor = (1.02 ** (month - 1))
        
        # Add some variability
        variability = 1 + (math.sin(month * 0.5) * 0.1)  # ±10% variability
        
        # Calculate projections
        projected_revenue = base_revenue * seasonal_multiplier * growth_factor * variability
        projected_expenses = base_expenses * (1 + (month * 0.005))  # Slight expense inflation
        
        monthly_profit = projected_revenue - projected_expenses
        ending_cash = starting_cash + monthly_profit
        
        return {
            "month": month,
            "quarter": quarter,
            "starting_cash": round(starting_cash, 2),
            "revenue": round(projected_revenue, 2),
            "expenses": round(projected_expenses, 2),
            "monthly_profit": round(monthly_profit, 2),
            "ending_cash": round(ending_cash, 2),
            "seasonal_factor": seasonal_multiplier,
            "cash_flow_status": "positive" if monthly_profit > 0 else "negative"
        }
    
    def _analyze_cash_flow_patterns(self, monthly_forecasts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in the cash flow forecast"""
        profits = [m["monthly_profit"] for m in monthly_forecasts]
        cash_positions = [m["ending_cash"] for m in monthly_forecasts]
        
        # Identify cash flow trends
        positive_months = len([p for p in profits if p > 0])
        negative_months = len([p for p in profits if p < 0])
        
        # Find minimum cash position
        min_cash_month = min(monthly_forecasts, key=lambda x: x["ending_cash"])
        max_cash_month = max(monthly_forecasts, key=lambda x: x["ending_cash"])
        
        # Calculate volatility
        avg_profit = sum(profits) / len(profits)
        profit_volatility = math.sqrt(sum((p - avg_profit) ** 2 for p in profits) / len(profits))
        
        return {
            "positive_cash_flow_months": positive_months,
            "negative_cash_flow_months": negative_months,
            "cash_flow_consistency": round(positive_months / len(monthly_forecasts), 2),
            "minimum_cash_position": {
                "month": min_cash_month["month"],
                "amount": min_cash_month["ending_cash"]
            },
            "maximum_cash_position": {
                "month": max_cash_month["month"],
                "amount": max_cash_month["ending_cash"]
            },
            "profit_volatility": round(profit_volatility, 2),
            "trend_analysis": self._identify_cash_flow_trend(profits)
        }
    
    def _identify_cash_flow_trend(self, profits: List[float]) -> str:
        """Identify overall trend in cash flow"""
        first_half = profits[:len(profits)//2]
        second_half = profits[len(profits)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg * 1.1:
            return "strongly_improving"
        elif second_avg > first_avg * 1.05:
            return "improving"
        elif second_avg < first_avg * 0.9:
            return "declining"
        elif second_avg < first_avg * 0.95:
            return "slightly_declining"
        else:
            return "stable"
    
    def _assess_forecast_risks(self, monthly_forecasts: List[Dict[str, Any]], 
                             financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risks in the cash flow forecast"""
        risks = []
        risk_score = 0.0
        
        # Cash runway risk
        negative_cash_months = [m for m in monthly_forecasts if m["ending_cash"] < 0]
        if negative_cash_months:
            risks.append(f"Cash shortfall predicted in month {negative_cash_months[0]['month']}")
            risk_score += 0.4
        
        # Minimum cash position risk
        min_cash = min(m["ending_cash"] for m in monthly_forecasts)
        monthly_expenses = financial_data.get("monthly_expenses", 0)
        if min_cash < monthly_expenses * 2:  # Less than 2 months runway
            risks.append("Low cash reserves predicted")
            risk_score += 0.2
        
        # Seasonality risk
        q4_months = [m for m in monthly_forecasts if m["quarter"] == 4]
        if q4_months and any(m["monthly_profit"] < 0 for m in q4_months):
            risks.append("Negative cash flow during peak season")
            risk_score += 0.3
        
        # Volatility risk
        profits = [m["monthly_profit"] for m in monthly_forecasts]
        profit_range = max(profits) - min(profits)
        avg_profit = sum(profits) / len(profits)
        if profit_range > abs(avg_profit) * 2:
            risks.append("High profit volatility")
            risk_score += 0.1
        
        return {
            "risk_factors": risks,
            "overall_risk_score": min(risk_score, 1.0),
            "risk_level": self._get_risk_level(risk_score),
            "mitigation_recommendations": self._generate_risk_mitigation(risks)
        }
    
    def _get_risk_level(self, score: float) -> str:
        """Convert risk score to level"""
        if score >= 0.7:
            return "HIGH"
        elif score >= 0.4:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_risk_mitigation(self, risks: List[str]) -> List[str]:
        """Generate risk mitigation recommendations"""
        mitigations = []
        
        if any("shortfall" in risk for risk in risks):
            mitigations.append("Secure emergency credit line or additional capital")
        if any("reserves" in risk for risk in risks):
            mitigations.append("Build cash reserves during profitable periods")
        if any("volatility" in risk for risk in risks):
            mitigations.append("Diversify revenue streams to reduce volatility")
        if any("season" in risk for risk in risks):
            mitigations.append("Optimize inventory and marketing for seasonal peaks")
        
        if not mitigations:
            mitigations.append("Maintain regular financial monitoring")
        
        return mitigations
    
    def scenario_analysis(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate multiple financial scenarios"""
        base_revenue = financial_data.get("monthly_revenue", 0)
        base_expenses = financial_data.get("monthly_expenses", 0)
        
        scenarios = {
            "conservative": {
                "revenue_adjustment": 0.85,
                "expense_adjustment": 1.10,
                "description": "Conservative scenario with lower revenue and higher costs"
            },
            "expected": {
                "revenue_adjustment": 1.0,
                "expense_adjustment": 1.0,
                "description": "Expected scenario based on current trends"
            },
            "optimistic": {
                "revenue_adjustment": 1.25,
                "expense_adjustment": 0.95,
                "description": "Optimistic scenario with growth and cost optimization"
            }
        }
        
        scenario_results = {}
        
        for scenario_name, adjustments in scenarios.items():
            adjusted_data = financial_data.copy()
            adjusted_data["monthly_revenue"] = base_revenue * adjustments["revenue_adjustment"]
            adjusted_data["monthly_expenses"] = base_expenses * adjustments["expense_adjustment"]
            
            forecast = self.generate_cash_flow_forecast(adjusted_data, 12)
            
            scenario_results[scenario_name] = {
                "adjustments": adjustments,
                "final_cash_position": forecast["summary_projections"]["final_cash_position"],
                "total_profit": forecast["summary_projections"]["net_profit"],
                "risk_level": forecast["risk_assessment"]["risk_level"]
            }
        
        return {
            "scenarios": scenario_results,
            "scenario_comparison": self._compare_scenarios(scenario_results),
            "recommended_strategy": self._recommend_strategy(scenario_results)
        }
    
    def _compare_scenarios(self, scenarios: Dict[str, Any]) -> Dict[str, Any]:
        """Compare different scenarios"""
        cash_positions = {name: data["final_cash_position"] for name, data in scenarios.items()}
        profits = {name: data["total_profit"] for name, data in scenarios.items()}
        
        best_cash = max(cash_positions, key=cash_positions.get)
        best_profit = max(profits, key=profits.get)
        
        return {
            "best_cash_scenario": best_cash,
            "best_profit_scenario": best_profit,
            "cash_position_range": {
                "minimum": min(cash_positions.values()),
                "maximum": max(cash_positions.values()),
                "spread": max(cash_positions.values()) - min(cash_positions.values())
            },
            "profit_range": {
                "minimum": min(profits.values()),
                "maximum": max(profits.values()),
                "spread": max(profits.values()) - min(profits.values())
            }
        }
    
    def _recommend_strategy(self, scenarios: Dict[str, Any]) -> Dict[str, str]:
        """Recommend strategy based on scenario analysis"""
        conservative = scenarios["conservative"]
        expected = scenarios["expected"]
        optimistic = scenarios["optimistic"]
        
        # Strategy based on conservative scenario performance
        if conservative["final_cash_position"] > 0 and conservative["total_profit"] > 0:
            strategy = "AGGRESSIVE"
            reasoning = "Even conservative scenario shows positive outcomes"
        elif expected["final_cash_position"] > 0:
            strategy = "BALANCED"
            reasoning = "Expected scenario is positive, but conservative has risks"
        else:
            strategy = "DEFENSIVE"
            reasoning = "Multiple scenarios show risks, focus on cash preservation"
        
        return {
            "recommended_strategy": strategy,
            "reasoning": reasoning,
            "key_actions": self._generate_strategy_actions(strategy)
        }
    
    def _generate_strategy_actions(self, strategy: str) -> List[str]:
        """Generate actions based on strategy"""
        actions = {
            "AGGRESSIVE": [
                "Increase inventory investments",
                "Expand into new product categories",
                "Negotiate longer payment terms with suppliers",
                "Invest in growth marketing"
            ],
            "BALANCED": [
                "Maintain steady growth pace",
                "Build modest cash reserves",
                "Monitor market conditions closely",
                "Optimize operational efficiency"
            ],
            "DEFENSIVE": [
                "Reduce inventory levels",
                "Focus on high-margin products",
                "Secure emergency funding",
                "Cut non-essential expenses"
            ]
        }
        
        return actions.get(strategy, ["Monitor financial position regularly"])
    
    def run(self) -> Dict[str, Any]:
        """Main execution function"""
        print("💰 [CashflowPredictor AI] Analyzing financial projections...")
        
        # Sample financial data for analysis
        sample_financial_data = {
            "monthly_revenue": 25000,
            "monthly_expenses": 19000,
            "current_cash": 15000,
            "inventory_value": 12000,
            "cash_conversion_days": 35,
            "credit_limit": 10000,
            "seasonal_business": True
        }
        
        print("   📊 Analyzing current financial position...")
        current_analysis = self.analyze_current_financial_position(sample_financial_data)
        
        print("   🔮 Generating 12-month cash flow forecast...")
        cash_flow_forecast = self.generate_cash_flow_forecast(sample_financial_data, 12)
        
        print("   🎯 Running scenario analysis...")
        scenario_analysis = self.scenario_analysis(sample_financial_data)
        
        # Create comprehensive report
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "ai_system": "CashflowPredictorAI",
                "version": "1.0.0",
                "forecast_horizon_months": 12
            },
            "executive_summary": {
                "current_financial_health": current_analysis["financial_health_score"]["health_level"],
                "health_score": current_analysis["financial_health_score"]["overall_score"],
                "projected_12_month_profit": cash_flow_forecast["summary_projections"]["net_profit"],
                "final_cash_position": cash_flow_forecast["summary_projections"]["final_cash_position"],
                "cash_flow_risk_level": cash_flow_forecast["risk_assessment"]["risk_level"],
                "recommended_strategy": scenario_analysis["recommended_strategy"]["recommended_strategy"],
                "positive_cash_flow_months": cash_flow_forecast["cash_flow_insights"]["positive_cash_flow_months"],
                "recommendation": self._get_overall_financial_recommendation(
                    current_analysis, cash_flow_forecast, scenario_analysis
                )
            },
            "current_financial_analysis": current_analysis,
            "cash_flow_forecast": cash_flow_forecast,
            "scenario_analysis": scenario_analysis,
            "financial_models_used": {
                "seasonality_included": True,
                "growth_assumptions": "2% monthly growth",
                "risk_factors_considered": len(self.financial_models["risk_factors"])
            }
        }
        
        # Save report
        report_file = self.reports_dir / f"cashflow_forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("✅ CashflowPredictor AI: Analysis completed!")
        print(f"   💼 Financial Health: {current_analysis['financial_health_score']['health_level']}")
        print(f"   📈 12-Month Profit: ${cash_flow_forecast['summary_projections']['net_profit']:,.2f}")
        print(f"   💰 Final Cash: ${cash_flow_forecast['summary_projections']['final_cash_position']:,.2f}")
        print(f"   ⚠️ Risk Level: {cash_flow_forecast['risk_assessment']['risk_level']}")
        print(f"   🎯 Strategy: {scenario_analysis['recommended_strategy']['recommended_strategy']}")
        print(f"   📄 Full Report: {report_file}")
        
        # Print key insights
        min_cash = cash_flow_forecast["cash_flow_insights"]["minimum_cash_position"]
        print(f"\n💡 Key Insights:")
        print(f"   Lowest Cash: ${min_cash['amount']:,.2f} in Month {min_cash['month']}")
        print(f"   Cash Flow Consistency: {cash_flow_forecast['cash_flow_insights']['cash_flow_consistency']*100:.0f}%")
        print(f"   Trend: {cash_flow_forecast['cash_flow_insights']['trend_analysis'].replace('_', ' ').title()}")
        
        print("💰 [CashflowPredictor AI] Ready for financial optimization!")
        return report
    
    def _get_overall_financial_recommendation(self, current: Dict[str, Any], 
                                            forecast: Dict[str, Any], 
                                            scenarios: Dict[str, Any]) -> str:
        """Generate overall financial recommendation"""
        health_level = current["financial_health_score"]["health_level"]
        risk_level = forecast["risk_assessment"]["risk_level"]
        strategy = scenarios["recommended_strategy"]["recommended_strategy"]
        final_cash = forecast["summary_projections"]["final_cash_position"]
        
        if health_level == "EXCELLENT" and risk_level == "LOW" and final_cash > 50000:
            return "EXCELLENT: Strong financial position with positive growth trajectory"
        elif health_level in ["GOOD", "EXCELLENT"] and strategy == "AGGRESSIVE":
            return "GOOD: Solid foundation ready for aggressive expansion"
        elif risk_level == "MEDIUM" and final_cash > 0:
            return "CAUTIOUS: Positive outlook but monitor cash flow closely"
        elif risk_level == "HIGH" or final_cash < 0:
            return "CONCERNING: Implement defensive strategies and secure additional funding"
        else:
            return "STABLE: Continue current operations with regular monitoring"

def run():
    """CLI entry point"""
    cashflow_ai = CashflowPredictorAI()
    cashflow_ai.run()

if __name__ == "__main__":
    run()
