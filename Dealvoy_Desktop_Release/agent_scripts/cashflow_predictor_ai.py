#!/usr/bin/env python3
"""
CashflowPredictorAI Agent
Financial forecasting and cash flow prediction agent
Protected by USPTO #63/850,603
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List
import random

class CashflowPredictorAI:
    """AI agent for cash flow prediction and financial forecasting"""
    
    def __init__(self):
        self.agent_name = "CashflowPredictorAI"
        self.version = "1.0.0"
        self.status = "active"
        self.prediction_models = ["linear", "seasonal", "growth", "conservative"]
        
    def predict_cashflow(self, business_data: Dict[str, Any], forecast_months: int = 12) -> Dict[str, Any]:
        """Predict cash flow for specified period"""
        try:
            historical_revenue = business_data.get("historical_revenue", [])
            monthly_expenses = business_data.get("monthly_expenses", {})
            growth_rate = business_data.get("growth_rate", 0.05)
            
            if not historical_revenue:
                # Generate baseline revenue data
                historical_revenue = self._generate_baseline_revenue(6)
            
            predictions = {}
            
            for model in self.prediction_models:
                predictions[model] = self._run_prediction_model(
                    model, historical_revenue, monthly_expenses, growth_rate, forecast_months
                )
            
            # Calculate consensus forecast
            consensus = self._calculate_consensus_forecast(predictions, forecast_months)
            
            # Calculate financial metrics
            metrics = self._calculate_financial_metrics(consensus, monthly_expenses)
            
            # Generate risk assessment
            risk_assessment = self._assess_financial_risks(consensus, metrics)
            
            result = {
                "business_id": business_data.get("business_id", "Unknown"),
                "forecast_period": f"{forecast_months} months",
                "model_predictions": predictions,
                "consensus_forecast": consensus,
                "financial_metrics": metrics,
                "risk_assessment": risk_assessment,
                "recommendations": self._generate_financial_recommendations(metrics, risk_assessment),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"CashflowPredictorAI generated {forecast_months}-month forecast")
            return result
            
        except Exception as e:
            logging.error(f"Cash flow prediction failed: {e}")
            return {"error": str(e)}
    
    def analyze_product_roi(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze ROI potential for a product"""
        try:
            selling_price = product_data.get("selling_price", 0)
            cost_price = product_data.get("cost_price", 0)
            estimated_sales = product_data.get("estimated_monthly_sales", 10)
            amazon_fees = product_data.get("amazon_fees", selling_price * 0.15)
            storage_fees = product_data.get("storage_fees", 5.0)
            
            # Calculate unit economics
            gross_profit = selling_price - cost_price - amazon_fees
            net_profit = gross_profit - storage_fees
            
            # Calculate ROI metrics
            roi_percentage = (net_profit / cost_price * 100) if cost_price > 0 else 0
            monthly_revenue = selling_price * estimated_sales
            monthly_profit = net_profit * estimated_sales
            
            # Calculate payback period
            initial_investment = cost_price * estimated_sales * 2  # 2 months inventory
            payback_months = initial_investment / monthly_profit if monthly_profit > 0 else float('inf')
            
            # Risk scoring
            risk_score = self._calculate_product_risk_score(product_data, roi_percentage)
            
            result = {
                "product_asin": product_data.get("asin", "Unknown"),
                "unit_economics": {
                    "selling_price": selling_price,
                    "cost_price": cost_price,
                    "amazon_fees": amazon_fees,
                    "storage_fees": storage_fees,
                    "gross_profit": round(gross_profit, 2),
                    "net_profit": round(net_profit, 2)
                },
                "roi_metrics": {
                    "roi_percentage": round(roi_percentage, 1),
                    "monthly_revenue": round(monthly_revenue, 2),
                    "monthly_profit": round(monthly_profit, 2),
                    "payback_months": round(payback_months, 1) if payback_months != float('inf') else None
                },
                "risk_assessment": {
                    "risk_score": risk_score,
                    "risk_level": self._get_risk_level(risk_score),
                    "key_risks": self._identify_key_risks(product_data, roi_percentage)
                },
                "profitability_grade": self._grade_profitability(roi_percentage, payback_months),
                "recommendations": self._generate_product_recommendations(roi_percentage, risk_score)
            }
            
            return result
            
        except Exception as e:
            logging.error(f"Product ROI analysis failed: {e}")
            return {"error": str(e)}
    
    def _generate_baseline_revenue(self, months: int) -> List[Dict[str, Any]]:
        """Generate baseline revenue data for modeling"""
        revenue_data = []
        base_revenue = 5000
        
        for i in range(months):
            date = datetime.now() - timedelta(days=30 * (months - i))
            revenue = base_revenue * (1 + random.uniform(-0.2, 0.3))
            
            revenue_data.append({
                "month": date.strftime("%Y-%m"),
                "revenue": round(revenue, 2),
                "expenses": round(revenue * 0.7, 2),
                "net_income": round(revenue * 0.3, 2)
            })
        
        return revenue_data
    
    def _run_prediction_model(self, model: str, historical_data: List[Dict], 
                             expenses: Dict, growth_rate: float, months: int) -> List[Dict[str, Any]]:
        """Run specific prediction model"""
        base_revenue = historical_data[-1]["revenue"] if historical_data else 5000
        predictions = []
        
        for i in range(months):
            month_date = datetime.now() + timedelta(days=30 * (i + 1))
            
            if model == "linear":
                predicted_revenue = base_revenue * (1 + growth_rate * (i + 1))
            elif model == "seasonal":
                seasonal_factor = 1 + 0.2 * (1 if (i + 1) % 12 in [11, 12, 1] else 0)
                predicted_revenue = base_revenue * (1 + growth_rate * (i + 1)) * seasonal_factor
            elif model == "growth":
                predicted_revenue = base_revenue * ((1 + growth_rate) ** (i + 1))
            else:  # conservative
                predicted_revenue = base_revenue * (1 + growth_rate * 0.5 * (i + 1))
            
            total_expenses = sum(expenses.values()) if expenses else predicted_revenue * 0.7
            net_cashflow = predicted_revenue - total_expenses
            
            predictions.append({
                "month": month_date.strftime("%Y-%m"),
                "predicted_revenue": round(predicted_revenue, 2),
                "predicted_expenses": round(total_expenses, 2),
                "predicted_cashflow": round(net_cashflow, 2)
            })
        
        return predictions
    
    def _calculate_consensus_forecast(self, predictions: Dict[str, List], months: int) -> List[Dict[str, Any]]:
        """Calculate consensus forecast from all models"""
        consensus = []
        
        for i in range(months):
            month_predictions = [model_pred[i] for model_pred in predictions.values()]
            
            avg_revenue = sum(pred["predicted_revenue"] for pred in month_predictions) / len(month_predictions)
            avg_expenses = sum(pred["predicted_expenses"] for pred in month_predictions) / len(month_predictions)
            avg_cashflow = avg_revenue - avg_expenses
            
            consensus.append({
                "month": month_predictions[0]["month"],
                "consensus_revenue": round(avg_revenue, 2),
                "consensus_expenses": round(avg_expenses, 2),
                "consensus_cashflow": round(avg_cashflow, 2),
                "confidence_interval": self._calculate_confidence_interval(month_predictions)
            })
        
        return consensus
    
    def _calculate_confidence_interval(self, predictions: List[Dict]) -> Dict[str, float]:
        """Calculate confidence interval for predictions"""
        revenues = [pred["predicted_revenue"] for pred in predictions]
        min_revenue = min(revenues)
        max_revenue = max(revenues)
        
        return {
            "lower_bound": round(min_revenue, 2),
            "upper_bound": round(max_revenue, 2),
            "variance": round((max_revenue - min_revenue) / 2, 2)
        }
    
    def _calculate_financial_metrics(self, forecast: List[Dict], expenses: Dict) -> Dict[str, Any]:
        """Calculate key financial metrics"""
        total_revenue = sum(month["consensus_revenue"] for month in forecast)
        total_expenses = sum(month["consensus_expenses"] for month in forecast)
        total_cashflow = total_revenue - total_expenses
        
        monthly_avg_revenue = total_revenue / len(forecast)
        monthly_avg_cashflow = total_cashflow / len(forecast)
        
        profit_margin = (total_cashflow / total_revenue * 100) if total_revenue > 0 else 0
        
        # Calculate cash runway
        monthly_burn = abs(min(month["consensus_cashflow"] for month in forecast))
        current_cash = 10000  # Assumed starting cash
        cash_runway_months = current_cash / monthly_burn if monthly_burn > 0 else float('inf')
        
        return {
            "total_projected_revenue": round(total_revenue, 2),
            "total_projected_expenses": round(total_expenses, 2),
            "total_projected_cashflow": round(total_cashflow, 2),
            "monthly_avg_revenue": round(monthly_avg_revenue, 2),
            "monthly_avg_cashflow": round(monthly_avg_cashflow, 2),
            "profit_margin_percentage": round(profit_margin, 1),
            "cash_runway_months": round(cash_runway_months, 1) if cash_runway_months != float('inf') else None
        }
    
    def _assess_financial_risks(self, forecast: List[Dict], metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Assess financial risks"""
        negative_months = sum(1 for month in forecast if month["consensus_cashflow"] < 0)
        volatility = sum(month["confidence_interval"]["variance"] for month in forecast) / len(forecast)
        
        risk_score = 0
        risk_factors = []
        
        # Negative cash flow risk
        if negative_months > len(forecast) * 0.3:
            risk_score += 30
            risk_factors.append("High probability of negative cash flow")
        
        # Volatility risk
        if volatility > metrics["monthly_avg_revenue"] * 0.2:
            risk_score += 25
            risk_factors.append("High revenue volatility")
        
        # Low profit margin risk
        if metrics["profit_margin_percentage"] < 10:
            risk_score += 20
            risk_factors.append("Low profit margins")
        
        # Cash runway risk
        if metrics.get("cash_runway_months", float('inf')) < 6:
            risk_score += 25
            risk_factors.append("Limited cash runway")
        
        return {
            "overall_risk_score": min(risk_score, 100),
            "risk_level": self._get_risk_level(risk_score),
            "risk_factors": risk_factors,
            "negative_cashflow_months": negative_months
        }
    
    def _calculate_product_risk_score(self, product_data: Dict, roi: float) -> int:
        """Calculate risk score for a product"""
        risk_score = 0
        
        # Competition risk
        competition_level = product_data.get("competition_level", "medium")
        if competition_level == "high":
            risk_score += 30
        elif competition_level == "medium":
            risk_score += 15
        
        # ROI risk
        if roi < 10:
            risk_score += 40
        elif roi < 20:
            risk_score += 20
        
        # Market saturation
        bsr = product_data.get("best_seller_rank", 100000)
        if bsr > 50000:
            risk_score += 20
        
        # Seasonality risk
        if product_data.get("seasonal", False):
            risk_score += 10
        
        return min(risk_score, 100)
    
    def _get_risk_level(self, score: int) -> str:
        """Convert risk score to level"""
        if score >= 70:
            return "high"
        elif score >= 40:
            return "medium"
        else:
            return "low"
    
    def _identify_key_risks(self, product_data: Dict, roi: float) -> List[str]:
        """Identify key risk factors"""
        risks = []
        
        if roi < 15:
            risks.append("Low return on investment")
        
        if product_data.get("competition_level") == "high":
            risks.append("High market competition")
        
        if product_data.get("best_seller_rank", 0) > 50000:
            risks.append("Poor market ranking")
        
        if product_data.get("seasonal", False):
            risks.append("Seasonal demand dependency")
        
        return risks
    
    def _grade_profitability(self, roi: float, payback_months: float) -> str:
        """Grade profitability potential"""
        if roi >= 30 and payback_months <= 3:
            return "A+"
        elif roi >= 25 and payback_months <= 4:
            return "A"
        elif roi >= 20 and payback_months <= 6:
            return "B+"
        elif roi >= 15 and payback_months <= 8:
            return "B"
        elif roi >= 10 and payback_months <= 12:
            return "C"
        else:
            return "D"
    
    def _generate_financial_recommendations(self, metrics: Dict, risk_assessment: Dict) -> List[str]:
        """Generate financial recommendations"""
        recommendations = []
        
        if risk_assessment["risk_level"] == "high":
            recommendations.append("Consider reducing expenses or increasing revenue streams")
        
        if metrics["profit_margin_percentage"] < 15:
            recommendations.append("Focus on improving profit margins")
        
        if metrics.get("cash_runway_months", float('inf')) < 6:
            recommendations.append("Secure additional funding or reduce burn rate")
        
        recommendations.append("Monitor cash flow weekly")
        recommendations.append("Maintain 3-6 months of operating expenses in reserve")
        
        return recommendations
    
    def _generate_product_recommendations(self, roi: float, risk_score: int) -> List[str]:
        """Generate product-specific recommendations"""
        recommendations = []
        
        if roi >= 25:
            recommendations.append("Strong ROI - consider scaling investment")
        elif roi >= 15:
            recommendations.append("Moderate ROI - proceed with caution")
        else:
            recommendations.append("Low ROI - consider alternative products")
        
        if risk_score >= 70:
            recommendations.append("High risk - implement strict monitoring")
        elif risk_score >= 40:
            recommendations.append("Medium risk - diversify portfolio")
        
        return recommendations
    
    def run(self, input_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main execution method"""
        input_data = input_data or {}
        
        if "business_data" in input_data:
            return self.predict_cashflow(
                input_data["business_data"],
                input_data.get("forecast_months", 12)
            )
        elif "product_data" in input_data:
            return self.analyze_product_roi(input_data["product_data"])
        
        return {
            "status": "ready",
            "agent": self.agent_name,
            "capabilities": ["cashflow_prediction", "roi_analysis", "risk_assessment"],
            "models": self.prediction_models
        }

if __name__ == "__main__":
    agent = CashflowPredictorAI()
    print(json.dumps(agent.run(), indent=2))
