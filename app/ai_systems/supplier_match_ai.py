#!/usr/bin/env python3
"""
🏬 SupplierMatch AI - Finds best wholesale/distributor sources per product and volume
Intelligent supplier recommendations for e-commerce arbitrage
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class SupplierMatchAI:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.reports_dir = self.project_path / "dist" / "intelligence_reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.supplier_database = self._load_supplier_database()
        
    def _load_supplier_database(self):
        """Load known supplier database"""
        return {
            "distributors": [
                {
                    "name": "TechDistro Inc",
                    "categories": ["electronics", "computer accessories"],
                    "min_order": 100,
                    "payment_terms": "net-30",
                    "shipping_time": 5,
                    "reliability_score": 0.92,
                    "price_competitiveness": 0.85,
                    "brands": ["Anker", "Aukey", "RAVPower"]
                },
                {
                    "name": "Home Solutions Wholesale",
                    "categories": ["home", "kitchen", "garden"],
                    "min_order": 50,
                    "payment_terms": "net-15",
                    "shipping_time": 7,
                    "reliability_score": 0.88,
                    "price_competitiveness": 0.90,
                    "brands": ["OXO", "Rubbermaid", "Black+Decker"]
                },
                {
                    "name": "Sports Gear Direct",
                    "categories": ["sports", "outdoor", "fitness"],
                    "min_order": 25,
                    "payment_terms": "prepay",
                    "shipping_time": 3,
                    "reliability_score": 0.95,
                    "price_competitiveness": 0.78,
                    "brands": ["Nike", "Adidas", "Under Armour"]
                }
            ],
            "wholesalers": [
                {
                    "name": "Bulk Buy Central",
                    "categories": ["general merchandise", "consumer goods"],
                    "min_order": 500,
                    "payment_terms": "net-45",
                    "shipping_time": 10,
                    "reliability_score": 0.82,
                    "price_competitiveness": 0.95,
                    "specialty": "high volume, low margin"
                },
                {
                    "name": "Premium Source",
                    "categories": ["luxury", "high-end electronics"],
                    "min_order": 10,
                    "payment_terms": "prepay",
                    "shipping_time": 2,
                    "reliability_score": 0.98,
                    "price_competitiveness": 0.65,
                    "specialty": "luxury items, authenticated goods"
                }
            ],
            "manufacturers": [
                {
                    "name": "Direct Factory Outlet",
                    "categories": ["private label", "custom products"],
                    "min_order": 1000,
                    "payment_terms": "50% upfront",
                    "shipping_time": 21,
                    "reliability_score": 0.75,
                    "price_competitiveness": 0.98,
                    "specialty": "private labeling, bulk manufacturing"
                }
            ]
        }
    
    def analyze_product_requirements(self, product_data):
        """Analyze product characteristics to determine supplier needs"""
        requirements = {
            "category": product_data.get("category", "general"),
            "volume_needed": product_data.get("target_quantity", 50),
            "budget_constraints": product_data.get("max_price_per_unit", 0),
            "time_sensitivity": product_data.get("urgency", "medium"),
            "quality_requirements": product_data.get("quality_level", "standard"),
            "brand_restrictions": product_data.get("brand_preferences", []),
            "payment_capability": product_data.get("payment_terms_preference", "net-30")
        }
        return requirements
    
    def score_supplier_match(self, supplier, requirements):
        """Score how well a supplier matches product requirements"""
        score = 0.0
        factors = {}
        
        # Category match (25% weight)
        category_match = 0.0
        if requirements["category"] in supplier.get("categories", []):
            category_match = 1.0
        elif any(cat in requirements["category"] for cat in supplier.get("categories", [])):
            category_match = 0.7
        score += category_match * 0.25
        factors["category_match"] = category_match
        
        # Volume compatibility (20% weight)
        volume_match = 0.0
        min_order = supplier.get("min_order", 0)
        if requirements["volume_needed"] >= min_order:
            volume_match = 1.0
        elif requirements["volume_needed"] >= min_order * 0.8:
            volume_match = 0.8
        score += volume_match * 0.20
        factors["volume_match"] = volume_match
        
        # Payment terms compatibility (15% weight)
        payment_match = 0.0
        supplier_terms = supplier.get("payment_terms", "prepay")
        if supplier_terms == requirements["payment_capability"]:
            payment_match = 1.0
        elif "net" in supplier_terms and "net" in requirements["payment_capability"]:
            payment_match = 0.8
        elif supplier_terms == "prepay":
            payment_match = 0.6
        score += payment_match * 0.15
        factors["payment_match"] = payment_match
        
        # Reliability score (20% weight)
        reliability = supplier.get("reliability_score", 0.5)
        score += reliability * 0.20
        factors["reliability"] = reliability
        
        # Price competitiveness (20% weight)
        price_comp = supplier.get("price_competitiveness", 0.5)
        score += price_comp * 0.20
        factors["price_competitiveness"] = price_comp
        
        return {
            "total_score": score,
            "factors": factors,
            "recommendation_level": self._get_recommendation_level(score)
        }
    
    def _get_recommendation_level(self, score):
        """Convert score to recommendation level"""
        if score >= 0.8:
            return "EXCELLENT"
        elif score >= 0.65:
            return "GOOD"
        elif score >= 0.5:
            return "FAIR"
        else:
            return "POOR"
    
    def find_best_suppliers(self, product_data):
        """Find and rank best suppliers for a product"""
        requirements = self.analyze_product_requirements(product_data)
        recommendations = []
        
        # Score all suppliers
        all_suppliers = (
            self.supplier_database["distributors"] + 
            self.supplier_database["wholesalers"] + 
            self.supplier_database["manufacturers"]
        )
        
        for supplier in all_suppliers:
            match_score = self.score_supplier_match(supplier, requirements)
            
            recommendation = {
                "supplier": supplier,
                "match_score": match_score,
                "estimated_cost_per_unit": self._estimate_cost(supplier, requirements),
                "estimated_delivery_time": supplier.get("shipping_time", 7),
                "risk_factors": self._assess_risks(supplier, requirements),
                "next_steps": self._generate_next_steps(supplier, match_score)
            }
            recommendations.append(recommendation)
        
        # Sort by score
        recommendations.sort(key=lambda x: x["match_score"]["total_score"], reverse=True)
        
        return recommendations[:5]  # Top 5 recommendations
    
    def _estimate_cost(self, supplier, requirements):
        """Estimate cost per unit from supplier"""
        base_cost = requirements.get("budget_constraints", 10.0)
        price_factor = supplier.get("price_competitiveness", 0.7)
        
        # Higher competitiveness = lower cost
        estimated_cost = base_cost * (1.5 - price_factor)
        
        return round(estimated_cost, 2)
    
    def _assess_risks(self, supplier, requirements):
        """Assess potential risks with supplier"""
        risks = []
        
        if supplier.get("min_order", 0) > requirements["volume_needed"] * 2:
            risks.append("High minimum order requirement")
        
        if supplier.get("payment_terms") == "prepay" and requirements["payment_capability"] != "prepay":
            risks.append("Payment terms mismatch")
        
        if supplier.get("reliability_score", 1.0) < 0.8:
            risks.append("Below-average reliability")
        
        if supplier.get("shipping_time", 0) > 14:
            risks.append("Long delivery times")
        
        return risks
    
    def _generate_next_steps(self, supplier, match_score):
        """Generate actionable next steps"""
        steps = []
        
        if match_score["total_score"] >= 0.8:
            steps.append("Contact supplier immediately for pricing")
            steps.append("Request product samples")
        elif match_score["total_score"] >= 0.6:
            steps.append("Research supplier further")
            steps.append("Compare with other options")
        else:
            steps.append("Consider alternative suppliers")
        
        steps.append("Verify supplier credentials")
        steps.append("Check recent customer reviews")
        
        return steps
    
    def generate_bulk_recommendations(self, product_list):
        """Generate supplier recommendations for multiple products"""
        bulk_analysis = {
            "products_analyzed": len(product_list),
            "recommendations": [],
            "volume_opportunities": [],
            "cost_savings": []
        }
        
        for product in product_list:
            recommendations = self.find_best_suppliers(product)
            bulk_analysis["recommendations"].append({
                "product": product.get("name", "Unknown"),
                "top_supplier": recommendations[0] if recommendations else None,
                "alternatives": recommendations[1:3] if len(recommendations) > 1 else []
            })
        
        # Identify volume opportunities
        supplier_volumes = {}
        for rec in bulk_analysis["recommendations"]:
            if rec["top_supplier"]:
                supplier_name = rec["top_supplier"]["supplier"]["name"]
                if supplier_name not in supplier_volumes:
                    supplier_volumes[supplier_name] = []
                supplier_volumes[supplier_name].append(rec["product"])
        
        for supplier, products in supplier_volumes.items():
            if len(products) >= 2:
                bulk_analysis["volume_opportunities"].append({
                    "supplier": supplier,
                    "products": products,
                    "potential_discount": f"{len(products) * 5}%",
                    "recommendation": "Combine orders for volume pricing"
                })
        
        return bulk_analysis
    
    def run(self):
        """Main execution function"""
        print("🏬 [SupplierMatch AI] Analyzing supplier opportunities...")
        
        # Sample product data for analysis
        sample_products = [
            {
                "name": "Wireless Phone Charger",
                "category": "electronics",
                "target_quantity": 100,
                "max_price_per_unit": 15.0,
                "urgency": "high",
                "quality_level": "standard"
            },
            {
                "name": "Kitchen Storage Container",
                "category": "home",
                "target_quantity": 50,
                "max_price_per_unit": 8.0,
                "urgency": "medium",
                "quality_level": "premium"
            },
            {
                "name": "Fitness Resistance Bands",
                "category": "sports",
                "target_quantity": 75,
                "max_price_per_unit": 12.0,
                "urgency": "low",
                "quality_level": "standard"
            }
        ]
        
        print(f"   📦 Analyzing {len(sample_products)} product requirements...")
        
        # Generate individual recommendations
        individual_recommendations = []
        for product in sample_products:
            recommendations = self.find_best_suppliers(product)
            individual_recommendations.append({
                "product": product["name"],
                "recommendations": recommendations
            })
        
        print("   🔍 Identifying bulk sourcing opportunities...")
        bulk_analysis = self.generate_bulk_recommendations(sample_products)
        
        # Create comprehensive report
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "ai_system": "SupplierMatchAI",
                "version": "1.0.0",
                "suppliers_in_database": len(self.supplier_database["distributors"]) + 
                                       len(self.supplier_database["wholesalers"]) + 
                                       len(self.supplier_database["manufacturers"])
            },
            "executive_summary": {
                "products_analyzed": len(sample_products),
                "total_suppliers_evaluated": len(self.supplier_database["distributors"]) + 
                                           len(self.supplier_database["wholesalers"]) + 
                                           len(self.supplier_database["manufacturers"]),
                "excellent_matches": len([r for rec in individual_recommendations 
                                        for r in rec["recommendations"] 
                                        if r["match_score"]["recommendation_level"] == "EXCELLENT"]),
                "volume_opportunities": len(bulk_analysis["volume_opportunities"]),
                "recommendation": self._get_overall_recommendation(individual_recommendations, bulk_analysis)
            },
            "individual_product_analysis": individual_recommendations,
            "bulk_sourcing_analysis": bulk_analysis,
            "supplier_database_summary": {
                "distributors": len(self.supplier_database["distributors"]),
                "wholesalers": len(self.supplier_database["wholesalers"]),
                "manufacturers": len(self.supplier_database["manufacturers"])
            }
        }
        
        # Save report
        report_file = self.reports_dir / f"supplier_match_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("✅ SupplierMatch AI: Analysis completed!")
        print(f"   📦 Products analyzed: {len(sample_products)}")
        print(f"   🏢 Suppliers evaluated: {report['executive_summary']['total_suppliers_evaluated']}")
        print(f"   ⭐ Excellent matches: {report['executive_summary']['excellent_matches']}")
        print(f"   📈 Volume opportunities: {report['executive_summary']['volume_opportunities']}")
        print(f"   📄 Full Report: {report_file}")
        
        # Print top recommendations
        if individual_recommendations:
            print("\n🎯 Top Supplier Matches:")
            for rec in individual_recommendations[:3]:
                if rec["recommendations"]:
                    top_match = rec["recommendations"][0]
                    print(f"   {rec['product']}: {top_match['supplier']['name']}")
                    print(f"      Score: {top_match['match_score']['total_score']:.2f} "
                          f"({top_match['match_score']['recommendation_level']})")
        
        print("🏬 [SupplierMatch AI] Ready for supplier optimization!")
        return report
    
    def _get_overall_recommendation(self, individual_recs, bulk_analysis):
        """Generate overall recommendation"""
        excellent_count = len([r for rec in individual_recs 
                             for r in rec["recommendations"] 
                             if r["match_score"]["recommendation_level"] == "EXCELLENT"])
        volume_opps = len(bulk_analysis["volume_opportunities"])
        
        if excellent_count >= 3 and volume_opps >= 1:
            return "EXCELLENT: Strong supplier matches with volume opportunities identified."
        elif excellent_count >= 2:
            return "GOOD: Multiple excellent supplier matches found."
        elif excellent_count >= 1:
            return "FAIR: Some good supplier options available."
        else:
            return "POOR: Limited supplier options. Consider expanding search criteria."

def run():
    """CLI entry point"""
    supplier_ai = SupplierMatchAI()
    supplier_ai.run()

if __name__ == "__main__":
    run()
