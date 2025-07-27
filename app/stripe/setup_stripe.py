#!/usr/bin/env python3
"""
Stripe Setup Script - Creates products and prices in Stripe
Run this script once to set up your Stripe account with Dealvoy plans
"""

import stripe
import os
from typing import Dict, Any

# Load environment variables
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_products_and_prices():
    """Create all products and prices in Stripe"""
    
    products_config = [
        {
            "name": "Dealvoy Starter",
            "description": "Free plan with basic features for new sellers",
            "prices": [
                {
                    "unit_amount": 0,
                    "currency": "usd",
                    "recurring": {"interval": "month"},
                    "nickname": "starter_monthly"
                }
            ]
        },
        {
            "name": "Dealvoy Professional", 
            "description": "Advanced AI features for growing e-commerce businesses",
            "prices": [
                {
                    "unit_amount": 9700,  # $97.00
                    "currency": "usd",
                    "recurring": {"interval": "month"},
                    "nickname": "professional_monthly"
                },
                {
                    "unit_amount": 97000,  # $970.00 (10 months price for annual)
                    "currency": "usd", 
                    "recurring": {"interval": "year"},
                    "nickname": "professional_yearly"
                }
            ]
        },
        {
            "name": "Dealvoy Enterprise",
            "description": "Full platform access with unlimited usage and dedicated support",
            "prices": [
                {
                    "unit_amount": 29700,  # $297.00
                    "currency": "usd",
                    "recurring": {"interval": "month"},
                    "nickname": "enterprise_monthly"
                },
                {
                    "unit_amount": 297000,  # $2970.00 (10 months price for annual)
                    "currency": "usd",
                    "recurring": {"interval": "year"},
                    "nickname": "enterprise_yearly"
                }
            ]
        },
        {
            "name": "API Usage",
            "description": "Additional API calls beyond plan limits",
            "prices": [
                {
                    "unit_amount": 1,  # $0.01 per call
                    "currency": "usd",
                    "billing_scheme": "per_unit",
                    "usage_type": "metered",
                    "nickname": "api_usage"
                }
            ]
        }
    ]
    
    created_products = {}
    
    for product_config in products_config:
        # Create product
        product = stripe.Product.create(
            name=product_config["name"],
            description=product_config["description"],
            type="service"
        )
        
        created_products[product.id] = {
            "product": product,
            "prices": []
        }
        
        print(f"Created product: {product.name} ({product.id})")
        
        # Create prices for the product
        for price_config in product_config["prices"]:
            price_data = {
                "product": product.id,
                "currency": price_config["currency"],
                "nickname": price_config["nickname"]
            }
            
            if "unit_amount" in price_config:
                price_data["unit_amount"] = price_config["unit_amount"]
            
            if "recurring" in price_config:
                price_data["recurring"] = price_config["recurring"]
            
            if "billing_scheme" in price_config:
                price_data["billing_scheme"] = price_config["billing_scheme"]
                
            if "usage_type" in price_config:
                price_data["usage_type"] = price_config["usage_type"]
            
            price = stripe.Price.create(**price_data)
            created_products[product.id]["prices"].append(price)
            
            print(f"  Created price: {price.nickname} ({price.id}) - ${price.unit_amount/100}")
    
    return created_products

def setup_webhook_endpoints():
    """Set up webhook endpoints in Stripe"""
    webhook_url = input("Enter your webhook URL (e.g., https://yourdomain.com/stripe/webhook): ")
    
    events = [
        "customer.subscription.created",
        "customer.subscription.updated", 
        "customer.subscription.deleted",
        "invoice.payment_succeeded",
        "invoice.payment_failed",
        "customer.created",
        "customer.updated"
    ]
    
    webhook = stripe.WebhookEndpoint.create(
        url=webhook_url,
        enabled_events=events
    )
    
    print(f"Created webhook endpoint: {webhook.id}")
    print(f"Webhook secret: {webhook.secret}")
    print("Add this secret to your STRIPE_WEBHOOK_SECRET environment variable")
    
    return webhook

def main():
    """Main setup function"""
    print("Setting up Stripe for Dealvoy...")
    
    if not stripe.api_key:
        print("Error: STRIPE_SECRET_KEY environment variable not set")
        return
    
    try:
        # Create products and prices
        print("\nCreating products and prices...")
        products = create_products_and_prices()
        
        # Set up webhook endpoints
        print("\nSetting up webhook endpoints...")
        webhook = setup_webhook_endpoints()
        
        print("\n✅ Stripe setup completed successfully!")
        print("\nNext steps:")
        print("1. Add the webhook secret to your environment variables")
        print("2. Update your application with the created price IDs")
        print("3. Test the integration with test cards")
        
        # Print price IDs for easy copying
        print("\nPrice IDs for your configuration:")
        for product_id, data in products.items():
            print(f"\nProduct: {data['product'].name}")
            for price in data["prices"]:
                print(f"  {price.nickname}: {price.id}")
                
    except Exception as e:
        print(f"Error during setup: {e}")

if __name__ == "__main__":
    main()
