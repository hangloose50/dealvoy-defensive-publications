#!/usr/bin/env python3
"""
Ungating Voyager - AI-Powered Amazon Ungating Prediction and Automation

This agent uses machine learning to predict Amazon category approval probability,
analyzes invoices, and automates ungating application preparation.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from app.services.scout_ungate import predict_ungating


class UngatingVoyager:
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.ungating_dir = self.project_path / "ungating_analysis"
        self.ungating_dir.mkdir(parents=True, exist_ok=True)
        
        # Brand restriction database
        self.restricted_brands = {
            "high_risk": ["Nike", "Apple", "LEGO", "Disney", "Microsoft", "Sony", "Canon", "Nikon"],
            "medium_risk": ["Samsung", "LG", "Panasonic", "Philips", "Bosch", "KitchenAid"],
            "low_risk": ["Generic", "Private Label", "Unbranded", "OEM"]
        }
        
        # Category gating requirements
        self.category_requirements = {
            "Health & Personal Care": {
                "difficulty": "high",
                "requirements": ["FDA approval", "invoices", "product testing"],
                "approval_rate": 0.3
            },
            "Beauty": {
                "difficulty": "medium",
                "requirements": ["brand authorization", "invoices"],
                "approval_rate": 0.6
            },
            "Toys & Games": {
                "difficulty": "medium",
                "requirements": ["safety certificates", "invoices"],
                "approval_rate": 0.7
            },
            "Electronics": {
                "difficulty": "low",
                "requirements": ["invoices", "brand authorization"],
                "approval_rate": 0.8
            },
            "Books": {
                "difficulty": "low",
                "requirements": ["invoices"],
                "approval_rate": 0.9
            }
        }
        
        # Success probability factors
        self.success_factors = {
            "seller_performance": {
                "excellent": 1.2,
                "good": 1.0,
                "fair": 0.8,
                "poor": 0.5
            },
            "account_age": {
                "new": 0.7,        # < 6 months
                "established": 1.0, # 6-24 months
                "veteran": 1.3      # > 24 months
            },
            "invoice_quality": {
                "professional": 1.2,
                "adequate": 1.0,
                "poor": 0.6
            }
        }

    def analyze_ungating_potential(self, products: List[Dict], seller_profile: Optional[Dict] = None) -> Dict:
        """Analyze ungating potential for a batch of products"""
        print("🔓 [UngatingVoyager] Analyzing ungating potential...")
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "total_products": len(products),
            "ungating_analysis": [],
            "summary": {
                "high_probability": 0,
                "medium_probability": 0,
                "low_probability": 0,
                "already_approved": 0
            },
            "recommendations": [],
            "application_strategy": {}
        }
        
        for product in products:
            ungating_result = self._comprehensive_ungating_analysis(product, seller_profile)
            analysis["ungating_analysis"].append(ungating_result)
            
            # Categorize by probability
            probability = ungating_result["success_probability"]
            if ungating_result["already_approved"]:
                analysis["summary"]["already_approved"] += 1
            elif probability >= 0.7:
                analysis["summary"]["high_probability"] += 1
            elif probability >= 0.4:
                analysis["summary"]["medium_probability"] += 1
            else:
                analysis["summary"]["low_probability"] += 1
        
        # Generate strategic recommendations
        analysis["recommendations"] = self._generate_ungating_strategy(analysis["ungating_analysis"])
        analysis["application_strategy"] = self._create_application_strategy(analysis["ungating_analysis"])
        
        return analysis

    def _comprehensive_ungating_analysis(self, product: Dict, seller_profile: Optional[Dict] = None) -> Dict:
        """Perform comprehensive ungating analysis for a single product"""
        
        # Base prediction from scout_ungate
        base_prediction = predict_ungating(product, seller_profile)
        
        # Enhanced analysis
        enhanced_analysis = {
            "product_id": product.get("asin") or product.get("upc") or "unknown",
            "product_title": product.get("title", "Unknown Product"),
            "brand": product.get("brand", "Unknown"),
            "category": product.get("category", "Unknown"),
            "base_prediction": base_prediction,
            "risk_level": "",
            "success_probability": base_prediction["confidence"],
            "already_approved": base_prediction["already_approved"],
            "requirements": [],
            "estimated_timeline": "",
            "preparation_steps": [],
            "risk_factors": [],
            "success_factors": []
        }
        
        # Determine risk level
        enhanced_analysis["risk_level"] = self._assess_brand_risk(product.get("brand", ""))
        
        # Category-specific requirements
        category = product.get("category", "")
        if category in self.category_requirements:
            cat_info = self.category_requirements[category]
            enhanced_analysis["requirements"] = cat_info["requirements"]
            enhanced_analysis["estimated_timeline"] = self._estimate_timeline(cat_info["difficulty"])
            
            # Adjust success probability based on category
            enhanced_analysis["success_probability"] *= cat_info["approval_rate"]
        
        # Seller profile adjustments
        if seller_profile:
            enhanced_analysis["success_probability"] *= self._calculate_seller_multiplier(seller_profile)
        
        # Generate preparation steps
        enhanced_analysis["preparation_steps"] = self._generate_preparation_steps(enhanced_analysis)
        
        # Identify risk and success factors
        enhanced_analysis["risk_factors"] = self._identify_risk_factors(product, enhanced_analysis)
        enhanced_analysis["success_factors"] = self._identify_success_factors(product, enhanced_analysis)
        
        # Clamp probability
        enhanced_analysis["success_probability"] = max(0.0, min(1.0, enhanced_analysis["success_probability"]))
        
        return enhanced_analysis

    def _assess_brand_risk(self, brand: str) -> str:
        """Assess the risk level for a specific brand"""
        brand_lower = brand.lower()
        
        for risk_level, brands in self.restricted_brands.items():
            if any(b.lower() in brand_lower for b in brands):
                return risk_level
        
        return "unknown"

    def _estimate_timeline(self, difficulty: str) -> str:
        """Estimate timeline based on difficulty"""
        timelines = {
            "low": "1-2 weeks",
            "medium": "2-4 weeks",
            "high": "4-8 weeks"
        }
        return timelines.get(difficulty, "Unknown")

    def _calculate_seller_multiplier(self, seller_profile: Dict) -> float:
        """Calculate success probability multiplier based on seller profile"""
        multiplier = 1.0
        
        # Performance multiplier
        performance = seller_profile.get("performance_level", "good")
        multiplier *= self.success_factors["seller_performance"].get(performance, 1.0)
        
        # Account age multiplier
        account_age = seller_profile.get("account_age_category", "established")
        multiplier *= self.success_factors["account_age"].get(account_age, 1.0)
        
        # Invoice quality multiplier
        invoice_quality = seller_profile.get("invoice_quality", "adequate")
        multiplier *= self.success_factors["invoice_quality"].get(invoice_quality, 1.0)
        
        return multiplier

    def _generate_preparation_steps(self, analysis: Dict) -> List[str]:
        """Generate specific preparation steps for ungating application"""
        steps = []
        
        # Base requirements
        if "invoices" in analysis["requirements"]:
            steps.append("Obtain 3+ authentic invoices from authorized distributors")
            steps.append("Ensure invoices show correct business name and tax information")
        
        if "brand authorization" in analysis["requirements"]:
            steps.append("Contact brand manufacturer for authorization letter")
            steps.append("Verify brand's Amazon seller requirements")
        
        if "FDA approval" in analysis["requirements"]:
            steps.append("Obtain FDA registration or approval documents")
            steps.append("Verify product compliance with FDA regulations")
        
        if "safety certificates" in analysis["requirements"]:
            steps.append("Obtain CPSC safety certificates")
            steps.append("Verify age-appropriate labeling and warnings")
        
        # Category-specific steps
        category = analysis["category"]
        if category == "Health & Personal Care":
            steps.append("Prepare product safety data sheets")
            steps.append("Document ingredient lists and allergen information")
        elif category == "Beauty":
            steps.append("Verify cosmetic product registration")
            steps.append("Prepare brand authenticity documentation")
        elif category == "Electronics":
            steps.append("Obtain FCC compliance certificates")
            steps.append("Prepare warranty and support documentation")
        
        # Risk mitigation steps
        if analysis["risk_level"] == "high_risk":
            steps.append("Consider partnering with authorized reseller")
            steps.append("Build strong sales history in unrestricted categories first")
        
        return steps

    def _identify_risk_factors(self, product: Dict, analysis: Dict) -> List[str]:
        """Identify factors that could hurt ungating success"""
        risks = []
        
        if analysis["risk_level"] == "high_risk":
            risks.append("Brand has strict authorization requirements")
        
        if analysis["category"] in ["Health & Personal Care", "Beauty"]:
            risks.append("Category has high regulatory requirements")
        
        brand = product.get("brand", "").lower()
        if "unknown" in brand or "generic" in brand:
            risks.append("Generic/unknown brand may lack proper documentation")
        
        price = float(product.get("price", 0) or 0)
        if price < 10:
            risks.append("Low-priced items may appear counterfeit")
        
        return risks

    def _identify_success_factors(self, product: Dict, analysis: Dict) -> List[str]:
        """Identify factors that could help ungating success"""
        factors = []
        
        if analysis["risk_level"] == "low_risk":
            factors.append("Brand typically has reasonable authorization requirements")
        
        if analysis["category"] in ["Books", "Electronics"]:
            factors.append("Category has relatively straightforward requirements")
        
        reviews = int(product.get("reviews", 0) or 0)
        if reviews > 100:
            factors.append("Product has strong market validation")
        
        rating = float(product.get("rating", 0) or 0)
        if rating >= 4.5:
            factors.append("High customer satisfaction indicates quality product")
        
        return factors

    def _generate_ungating_strategy(self, ungating_analysis: List[Dict]) -> List[Dict]:
        """Generate strategic recommendations for ungating approach"""
        recommendations = []
        
        # Group by risk level
        by_risk = {"high_risk": [], "medium_risk": [], "low_risk": []}
        for analysis in ungating_analysis:
            risk_level = analysis["risk_level"]
            if risk_level in by_risk:
                by_risk[risk_level].append(analysis)
        
        # Strategy for low-risk items
        if by_risk["low_risk"]:
            recommendations.append({
                "priority": "high",
                "strategy": "Start with low-risk brands",
                "items": len(by_risk["low_risk"]),
                "rationale": "Build approval history and credibility",
                "timeline": "1-2 weeks per application"
            })
        
        # Strategy for medium-risk items
        if by_risk["medium_risk"]:
            recommendations.append({
                "priority": "medium",
                "strategy": "Target medium-risk brands after initial success",
                "items": len(by_risk["medium_risk"]),
                "rationale": "Leverage proven track record",
                "timeline": "2-4 weeks per application"
            })
        
        # Strategy for high-risk items
        if by_risk["high_risk"]:
            recommendations.append({
                "priority": "low",
                "strategy": "Consider alternative approaches for high-risk brands",
                "items": len(by_risk["high_risk"]),
                "rationale": "May require significant investment and uncertain outcome",
                "timeline": "4-8 weeks per application",
                "alternatives": ["Find authorized distributors", "Focus on other categories"]
            })
        
        return recommendations

    def _create_application_strategy(self, ungating_analysis: List[Dict]) -> Dict:
        """Create detailed application strategy"""
        strategy = {
            "recommended_order": [],
            "batch_strategy": {},
            "resource_requirements": {},
            "success_timeline": {}
        }
        
        # Sort by success probability
        sorted_analysis = sorted(ungating_analysis, key=lambda x: x["success_probability"], reverse=True)
        
        # Recommended application order
        for i, analysis in enumerate(sorted_analysis[:10], 1):  # Top 10
            strategy["recommended_order"].append({
                "rank": i,
                "product": analysis["product_title"][:50],
                "brand": analysis["brand"],
                "probability": analysis["success_probability"],
                "timeline": analysis["estimated_timeline"]
            })
        
        # Batch strategy
        high_prob = [a for a in ungating_analysis if a["success_probability"] >= 0.7]
        medium_prob = [a for a in ungating_analysis if 0.4 <= a["success_probability"] < 0.7]
        
        strategy["batch_strategy"] = {
            "phase_1": {
                "focus": "High probability applications",
                "count": len(high_prob),
                "timeline": "Weeks 1-4"
            },
            "phase_2": {
                "focus": "Medium probability applications",
                "count": len(medium_prob),
                "timeline": "Weeks 5-12"
            }
        }
        
        return strategy

    def generate_invoice_requirements(self, products: List[Dict]) -> Dict:
        """Generate specific invoice requirements for products"""
        print("📄 [UngatingVoyager] Generating invoice requirements...")
        
        requirements = {
            "timestamp": datetime.now().isoformat(),
            "general_requirements": [
                "Business letterhead with complete contact information",
                "Invoice date within last 365 days",
                "Quantity and description matching Amazon listing",
                "Unit price and total amount clearly shown",
                "Supplier business name and tax ID",
                "Your business name exactly as registered with Amazon"
            ],
            "brand_specific": {},
            "category_specific": {},
            "checklist": []
        }
        
        # Analyze brands and categories
        brands = set()
        categories = set()
        
        for product in products:
            if product.get("brand"):
                brands.add(product["brand"])
            if product.get("category"):
                categories.add(product["category"])
        
        # Brand-specific requirements
        for brand in brands:
            risk_level = self._assess_brand_risk(brand)
            if risk_level == "high_risk":
                requirements["brand_specific"][brand] = [
                    "Authorization letter from brand manufacturer",
                    "Proof of authorized distributor relationship",
                    "Original manufacturer invoices (no third-party resellers)"
                ]
            elif risk_level == "medium_risk":
                requirements["brand_specific"][brand] = [
                    "Invoices from authorized distributors",
                    "Brand verification documentation if available"
                ]
        
        # Category-specific requirements
        for category in categories:
            if category in self.category_requirements:
                cat_reqs = self.category_requirements[category]["requirements"]
                requirements["category_specific"][category] = cat_reqs
        
        # Generate checklist
        requirements["checklist"] = [
            "✓ All invoices are authentic and unmodified",
            "✓ Invoice dates are within the last 12 months",
            "✓ Business names match Amazon account registration",
            "✓ Product descriptions match intended listings",
            "✓ All required category-specific documents included",
            "✓ Brand authorization letters obtained where required",
            "✓ Invoice amounts justify inventory quantities"
        ]
        
        return requirements

    def run_ungating_analysis(self, input_file: str, output_file: str = None, seller_profile_file: str = None):
        """Run comprehensive ungating analysis"""
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
        
        # Load seller profile if provided
        seller_profile = None
        if seller_profile_file:
            try:
                with open(seller_profile_file, 'r') as f:
                    seller_profile = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"⚠️  Could not load seller profile: {seller_profile_file}")
        
        # Analyze ungating potential
        analysis = self.analyze_ungating_potential(products, seller_profile)
        
        # Generate invoice requirements
        invoice_reqs = self.generate_invoice_requirements(products)
        
        # Combine results
        complete_analysis = {
            "ungating_analysis": analysis,
            "invoice_requirements": invoice_reqs,
            "generated_by": "UngatingVoyager",
            "timestamp": datetime.now().isoformat()
        }
        
        # Save results
        if output_file:
            output_path = Path(output_file)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.ungating_dir / f"ungating_analysis_{timestamp}.json"
        
        with open(output_path, 'w') as f:
            json.dump(complete_analysis, f, indent=2)
        
        print(f"🔓 [UngatingVoyager] Analysis complete: {output_path}")
        
        # Print summary
        self._print_analysis_summary(analysis)
        
        return True

    def _print_analysis_summary(self, analysis: Dict):
        """Print a summary of the ungating analysis"""
        summary = analysis["summary"]
        total = analysis["total_products"]
        
        print(f"\n🔓 UNGATING ANALYSIS SUMMARY")
        print(f"═══════════════════════════════")
        print(f"Total Products Analyzed: {total}")
        print(f"🟢 High Probability (≥70%): {summary['high_probability']} ({summary['high_probability']/total*100:.1f}%)")
        print(f"🟡 Medium Probability (40-69%): {summary['medium_probability']} ({summary['medium_probability']/total*100:.1f}%)")
        print(f"🔴 Low Probability (<40%): {summary['low_probability']} ({summary['low_probability']/total*100:.1f}%)")
        print(f"✅ Already Approved: {summary['already_approved']} ({summary['already_approved']/total*100:.1f}%)")
        
        if analysis["recommendations"]:
            print(f"\n📋 STRATEGIC RECOMMENDATIONS:")
            for i, rec in enumerate(analysis["recommendations"], 1):
                print(f"{i}. {rec['strategy']} ({rec['items']} items) - {rec['timeline']}")


def main():
    parser = argparse.ArgumentParser(description="Ungating Voyager - AI Ungating Analysis")
    parser.add_argument("--input", "-i", required=True, help="Input JSON file with product data")
    parser.add_argument("--output", "-o", help="Output file path (optional)")
    parser.add_argument("--seller-profile", "-s", help="Seller profile JSON file (optional)")
    parser.add_argument("--project-path", default=".", help="Project root path")
    
    args = parser.parse_args()
    
    try:
        voyager = UngatingVoyager(args.project_path)
        success = voyager.run_ungating_analysis(args.input, args.output, args.seller_profile)
        
        if success:
            print(f"🔓 UngatingVoyager: Analysis completed successfully")
            return 0
        else:
            print(f"🔓 UngatingVoyager: Analysis failed")
            return 1
            
    except Exception as e:
        print(f"🔓 UngatingVoyager: Error - {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
