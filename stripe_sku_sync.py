#!/usr/bin/env python3
"""
Stripe SKU Sync System
Ensures Stripe pricing matches corrected tiers and plans
"""

import json
import datetime
from typing import Dict, List

class StripeSKUSync:
    """
    Synchronizes Stripe SKUs with corrected pricing tiers
    """
    
    def __init__(self):
        self.stripe_config = {
            "mode": "test",  # sandbox mode for testing
            "api_version": "2023-10-16",
            "webhook_endpoint": "https://dealvoy.com/webhook/stripe"
        }
        
        # Corrected tier pricing structure
        self.corrected_tiers = {
            "starter": {
                "name": "Starter",
                "monthly_price": 0,
                "annual_price": 0,
                "scan_limit": 100,
                "agents": 5,
                "features": ["Basic scanning", "5 AI agents", "Mobile app access"]
            },
            "professional": {
                "name": "Professional", 
                "monthly_price": 29.99,
                "annual_price": 239.99,  # 33% savings
                "scan_limit": 1000,
                "agents": 15,
                "features": ["1,000 scans/month", "15 AI agents", "Priority support", "Advanced analytics"]
            },
            "enterprise": {
                "name": "Enterprise",
                "monthly_price": 79.99,
                "annual_price": 639.99,  # 33% savings
                "scan_limit": 10000,
                "agents": 25,
                "features": ["10,000 scans/month", "25 AI agents", "Dedicated support", "API access"]
            },
            "titan": {
                "name": "Titan",
                "monthly_price": 159.99,
                "annual_price": 1279.99,  # 33% savings
                "scan_limit": -1,  # unlimited
                "agents": 35,
                "features": ["Unlimited scans", "35 AI agents", "White-glove support", "Custom integrations"]
            },
            "odyssey": {
                "name": "Odyssey", 
                "monthly_price": 299.99,
                "annual_price": 2399.99,  # 33% savings
                "scan_limit": -1,  # unlimited
                "agents": 42,
                "features": ["Unlimited scans", "42 AI agents", "Enterprise integrations", "Custom development"]
            },
            "vanguard": {
                "name": "Vanguard",
                "monthly_price": 599.99,
                "annual_price": 4799.99,  # 33% savings  
                "scan_limit": -1,  # unlimited
                "agents": 46,
                "features": ["Unlimited scans", "All 46 AI agents", "Complete automation", "Patent-protected features"]
            }
        }
        
    def generate_stripe_products(self) -> Dict:
        """Generate Stripe product definitions"""
        
        products = {}
        
        for tier_id, tier_data in self.corrected_tiers.items():
            # Monthly product
            monthly_product = {
                "id": f"prod_{tier_id}_monthly",
                "name": f"Dealvoy {tier_data['name']} - Monthly",
                "description": f"{tier_data['name']} plan with {tier_data['agents']} AI agents",
                "type": "service",
                "active": True,
                "metadata": {
                    "tier": tier_id,
                    "billing": "monthly",
                    "agents": tier_data['agents'],
                    "scan_limit": tier_data['scan_limit']
                }
            }
            
            # Annual product  
            annual_product = {
                "id": f"prod_{tier_id}_annual",
                "name": f"Dealvoy {tier_data['name']} - Annual",
                "description": f"{tier_data['name']} plan with {tier_data['agents']} AI agents (33% savings)",
                "type": "service", 
                "active": True,
                "metadata": {
                    "tier": tier_id,
                    "billing": "annual", 
                    "agents": tier_data['agents'],
                    "scan_limit": tier_data['scan_limit']
                }
            }
            
            products[f"{tier_id}_monthly"] = monthly_product
            products[f"{tier_id}_annual"] = annual_product
            
        return products
    
    def generate_stripe_prices(self) -> Dict:
        """Generate Stripe price objects for all tiers"""
        
        prices = {}
        
        for tier_id, tier_data in self.corrected_tiers.items():
            # Skip starter tier pricing (free)
            if tier_data['monthly_price'] == 0:
                continue
                
            # Monthly price
            monthly_price = {
                "id": f"price_{tier_id}_monthly",
                "product": f"prod_{tier_id}_monthly",
                "unit_amount": int(tier_data['monthly_price'] * 100),  # Convert to cents
                "currency": "usd",
                "recurring": {
                    "interval": "month",
                    "interval_count": 1
                },
                "active": True,
                "metadata": {
                    "tier": tier_id,
                    "billing": "monthly"
                }
            }
            
            # Annual price
            annual_price = {
                "id": f"price_{tier_id}_annual", 
                "product": f"prod_{tier_id}_annual",
                "unit_amount": int(tier_data['annual_price'] * 100),  # Convert to cents
                "currency": "usd",
                "recurring": {
                    "interval": "year",
                    "interval_count": 1
                },
                "active": True,
                "metadata": {
                    "tier": tier_id,
                    "billing": "annual"
                }
            }
            
            prices[f"{tier_id}_monthly"] = monthly_price
            prices[f"{tier_id}_annual"] = annual_price
            
        return prices
    
    def validate_pricing_consistency(self) -> Dict:
        """Validate pricing consistency across all tiers"""
        
        issues = []
        warnings = []
        
        # Check for duplicate pricing
        monthly_prices = []
        annual_prices = []
        
        for tier_id, tier_data in self.corrected_tiers.items():
            monthly = tier_data['monthly_price']
            annual = tier_data['annual_price']
            
            if monthly in monthly_prices:
                issues.append(f"Duplicate monthly price: ${monthly} ({tier_id})")
            monthly_prices.append(monthly)
            
            if annual in annual_prices:
                issues.append(f"Duplicate annual price: ${annual} ({tier_id})")
            annual_prices.append(annual)
            
            # Validate annual savings
            if monthly > 0 and annual > 0:
                expected_annual = monthly * 12 * 0.67  # 33% savings
                if abs(annual - expected_annual) > 1:
                    warnings.append(f"{tier_id}: Annual price ${annual} doesn't match 33% savings (expected ${expected_annual:.2f})")
        
        # Check tier progression
        previous_price = 0
        for tier_id, tier_data in self.corrected_tiers.items():
            current_price = tier_data['monthly_price']
            if current_price > 0 and current_price <= previous_price:
                issues.append(f"Tier progression issue: {tier_id} (${current_price}) should be higher than previous tier")
            if current_price > 0:
                previous_price = current_price
        
        return {
            "validation_passed": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "total_tiers": len(self.corrected_tiers),
            "pricing_tiers": len([t for t in self.corrected_tiers.values() if t['monthly_price'] > 0])
        }
    
    def generate_sync_report(self) -> Dict:
        """Generate comprehensive sync report"""
        
        products = self.generate_stripe_products()
        prices = self.generate_stripe_prices()
        validation = self.validate_pricing_consistency()
        
        return {
            "sync_timestamp": datetime.datetime.now().isoformat(),
            "stripe_config": self.stripe_config,
            "tier_summary": {
                "total_tiers": len(self.corrected_tiers),
                "free_tiers": len([t for t in self.corrected_tiers.values() if t['monthly_price'] == 0]),
                "paid_tiers": len([t for t in self.corrected_tiers.values() if t['monthly_price'] > 0]),
                "products_generated": len(products),
                "prices_generated": len(prices)
            },
            "validation_results": validation,
            "products": products,
            "prices": prices,
            "recommended_actions": [
                "Update Stripe dashboard with new products",
                "Configure webhook endpoints", 
                "Test payment flows",
                "Update pricing page with corrected tiers",
                "Validate trial flows"
            ]
        }

def deploy_stripe_sync():
    """Deploy Stripe SKU synchronization"""
    
    print("💳 STRIPE SKU SYNC DEPLOYMENT")
    print("=" * 50)
    
    sync_system = StripeSKUSync()
    
    # Generate sync report
    report = sync_system.generate_sync_report()
    
    print(f"📊 Tier Summary:")
    print(f"   • Total Tiers: {report['tier_summary']['total_tiers']}")
    print(f"   • Free Tiers: {report['tier_summary']['free_tiers']}")
    print(f"   • Paid Tiers: {report['tier_summary']['paid_tiers']}")
    print(f"   • Products Generated: {report['tier_summary']['products_generated']}")
    print(f"   • Prices Generated: {report['tier_summary']['prices_generated']}")
    
    # Validation results
    validation = report['validation_results']
    if validation['validation_passed']:
        print(f"\n✅ Pricing Validation: PASSED")
    else:
        print(f"\n❌ Pricing Validation: FAILED")
        for issue in validation['issues']:
            print(f"   • {issue}")
    
    if validation['warnings']:
        print(f"\n⚠️ Warnings:")
        for warning in validation['warnings']:
            print(f"   • {warning}")
    
    # Show corrected pricing
    print(f"\n💰 Corrected Pricing Structure:")
    for tier_id, tier_data in sync_system.corrected_tiers.items():
        monthly = f"${tier_data['monthly_price']:.2f}" if tier_data['monthly_price'] > 0 else "FREE"
        annual = f"${tier_data['annual_price']:.2f}" if tier_data['annual_price'] > 0 else "FREE"
        scan_limit = "Unlimited" if tier_data['scan_limit'] == -1 else f"{tier_data['scan_limit']:,}"
        
        print(f"   • {tier_data['name']}: {monthly}/month, {annual}/year")
        print(f"     Scans: {scan_limit}, Agents: {tier_data['agents']}")
    
    # Save sync report
    with open("stripe_sku_sync_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Sync report saved: stripe_sku_sync_report.json")
    print(f"\n🎯 Next Steps:")
    for action in report['recommended_actions']:
        print(f"   • {action}")

if __name__ == "__main__":
    deploy_stripe_sync()
