import os
import stripe

stripe.api_key = os.getenv("STRIPE_API_KEY")

# Define product and price data
plans = [
    {
        "name": "Starter",
        "price": 2900,
        "features": {"agent_access_limit": 10, "scan_limit": 100}
    },
    {
        "name": "Pro",
        "price": 9900,
        "features": {"agent_access_limit": 41, "scan_limit": 2500}
    },
    {
        "name": "Enterprise",
        "price": 24900,
        "features": {"agent_access_limit": "unlimited", "scan_limit": "custom", "support": "priority"}
    }
]

for plan in plans:
    product = stripe.Product.create(name=f"Dealvoy {plan['name']}")
    price = stripe.Price.create(
        unit_amount=plan["price"],
        currency="usd",
        recurring={"interval": "month"},
        product=product.id
    )
    print(f"Created {plan['name']} plan: Product ID {product.id}, Price ID {price.id}")
