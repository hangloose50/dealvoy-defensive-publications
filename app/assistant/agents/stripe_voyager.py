#!/usr/bin/env python3
"""
💳 StripeVoyager - Configures Stripe payment infrastructure and subscription logic
Builds billing systems, webhooks, and subscription management for SaaS platforms
"""

import json
from datetime import datetime
from pathlib import Path

class StripeVoyager:
    def __init__(self, project_path: str = ".", enabled: bool = False):
        self.project_path = Path(project_path)
        self.enabled = enabled  # Default disabled for payment security
        self.stripe_dir = self.project_path / "app" / "stripe"
        self.stripe_dir.mkdir(parents=True, exist_ok=True)
        self.webhooks_dir = self.stripe_dir / "webhooks"
        self.webhooks_dir.mkdir(parents=True, exist_ok=True)
    
    def toggle_agent(self, enabled=None):
        """Toggle agent on/off for payment security"""
        if enabled is None:
            self.enabled = not self.enabled
        else:
            self.enabled = enabled
        
        status = "ENABLED" if self.enabled else "DISABLED"
        print(f"💳 [StripeVoyager] Status: {status}")
        if not self.enabled:
            print("   ⚠️  Payment operations disabled for security")
        return self.enabled
    
    def check_enabled(self, action_name="payment operation"):
        """Check if agent is enabled before performing payment operations"""
        if not self.enabled:
            print(f"🔒 [StripeVoyager] Payment agent disabled - skipping {action_name}")
            print("   Use toggle_agent(True) to enable payment operations")
            return False
        return True
    
    def create_stripe_config(self):
        """Create Stripe configuration and setup"""
        config = {
            "api_version": "2023-10-16",
            "currency": "usd",
            "billing_cycle": "monthly",
            "trial_period_days": 7,
            "grace_period_days": 3,
            "webhook_endpoints": [
                "customer.subscription.created",
                "customer.subscription.updated", 
                "customer.subscription.deleted",
                "invoice.payment_succeeded",
                "invoice.payment_failed",
                "customer.created",
                "customer.updated"
            ],
            "product_catalog": {
                "starter": {
                    "stripe_product_id": "prod_starter",
                    "price_id": "price_starter_monthly",
                    "amount": 0,
                    "interval": "month",
                    "features": [
                        "100 product scans/month",
                        "Basic profit calculator",
                        "5 scraper sources",
                        "Email support"
                    ]
                },
                "professional": {
                    "stripe_product_id": "prod_professional",
                    "price_id": "price_professional_monthly",
                    "amount": 9700,  # $97.00 in cents
                    "interval": "month",
                    "trial_period_days": 7,
                    "features": [
                        "5,000 product scans/month",
                        "AI deal scoring",
                        "15 scraper sources",
                        "Ungating predictions",
                        "Priority support",
                        "API access"
                    ]
                },
                "enterprise": {
                    "stripe_product_id": "prod_enterprise", 
                    "price_id": "price_enterprise_monthly",
                    "amount": 29700,  # $297.00 in cents
                    "interval": "month",
                    "features": [
                        "Unlimited product scans",
                        "All AI features",
                        "28+ scraper sources",
                        "Custom integrations",
                        "Dedicated support",
                        "API access (unlimited)"
                    ]
                }
            },
            "usage_based_pricing": {
                "api_calls": {
                    "price_id": "price_api_calls",
                    "unit_amount": 1,  # $0.01 per call
                    "billing_scheme": "per_unit"
                }
            }
        }
        
        return config
    
    def create_stripe_client(self):
        """Create Stripe client wrapper"""
        client_code = '''import stripe
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class StripeClient:
    def __init__(self):
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        self.webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        
    def create_customer(self, email: str, name: str, metadata: Dict[str, Any] = None) -> stripe.Customer:
        """Create a new Stripe customer"""
        return stripe.Customer.create(
            email=email,
            name=name,
            metadata=metadata or {}
        )
    
    def create_subscription(self, customer_id: str, price_id: str, trial_period_days: int = 7) -> stripe.Subscription:
        """Create a new subscription with trial period"""
        return stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_id}],
            trial_period_days=trial_period_days,
            payment_behavior="default_incomplete",
            payment_settings={"save_default_payment_method": "on_subscription"},
            expand=["latest_invoice.payment_intent"]
        )
    
    def update_subscription(self, subscription_id: str, price_id: str) -> stripe.Subscription:
        """Update subscription to new plan"""
        subscription = stripe.Subscription.retrieve(subscription_id)
        return stripe.Subscription.modify(
            subscription_id,
            items=[{
                "id": subscription["items"]["data"][0].id,
                "price": price_id
            }],
            proration_behavior="create_prorations"
        )
    
    def cancel_subscription(self, subscription_id: str, at_period_end: bool = True) -> stripe.Subscription:
        """Cancel subscription"""
        return stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=at_period_end
        )
    
    def create_usage_record(self, subscription_item_id: str, quantity: int, timestamp: int = None) -> stripe.UsageRecord:
        """Record usage for metered billing"""
        return stripe.UsageRecord.create(
            subscription_item=subscription_item_id,
            quantity=quantity,
            timestamp=timestamp or int(datetime.now().timestamp()),
            action="increment"
        )
    
    def create_portal_session(self, customer_id: str, return_url: str) -> stripe.billing_portal.Session:
        """Create customer portal session for self-service billing"""
        return stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=return_url
        )
    
    def create_checkout_session(self, price_id: str, success_url: str, cancel_url: str, 
                               customer_email: str = None, trial_period_days: int = 7) -> stripe.checkout.Session:
        """Create Stripe Checkout session"""
        session_params = {
            "payment_method_types": ["card"],
            "line_items": [{
                "price": price_id,
                "quantity": 1
            }],
            "mode": "subscription",
            "success_url": success_url,
            "cancel_url": cancel_url,
            "subscription_data": {
                "trial_period_days": trial_period_days
            }
        }
        
        if customer_email:
            session_params["customer_email"] = customer_email
            
        return stripe.checkout.Session.create(**session_params)
    
    def construct_webhook_event(self, payload: bytes, sig_header: str) -> stripe.Event:
        """Construct and verify webhook event"""
        return stripe.Webhook.construct_event(
            payload, sig_header, self.webhook_secret
        )
    
    def get_customer_subscriptions(self, customer_id: str) -> stripe.ListObject:
        """Get all subscriptions for a customer"""
        return stripe.Subscription.list(customer=customer_id)
    
    def get_subscription_usage(self, subscription_item_id: str, 
                             start_date: datetime, end_date: datetime) -> stripe.ListObject:
        """Get usage records for a subscription item"""
        return stripe.UsageRecordSummary.list(
            subscription_item=subscription_item_id,
            starting_after=int(start_date.timestamp()),
            ending_before=int(end_date.timestamp())
        )
'''
        
        client_file = self.stripe_dir / "stripe_client.py"
        with open(client_file, 'w') as f:
            f.write(client_code)
        
        return str(client_file)
    
    def create_webhook_handler(self):
        """Create webhook event handler"""
        webhook_code = '''from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import stripe
import logging
from typing import Dict, Any
from .stripe_client import StripeClient
from ..database import get_db
from ..models import User, Subscription
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)
router = APIRouter()
stripe_client = StripeClient()

@router.post("/stripe/webhook")
async def handle_stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhook events"""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe_client.construct_webhook_event(payload, sig_header)
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle the event
    if event["type"] == "customer.subscription.created":
        await handle_subscription_created(event["data"]["object"], db)
    elif event["type"] == "customer.subscription.updated":
        await handle_subscription_updated(event["data"]["object"], db)
    elif event["type"] == "customer.subscription.deleted":
        await handle_subscription_deleted(event["data"]["object"], db)
    elif event["type"] == "invoice.payment_succeeded":
        await handle_payment_succeeded(event["data"]["object"], db)
    elif event["type"] == "invoice.payment_failed":
        await handle_payment_failed(event["data"]["object"], db)
    elif event["type"] == "customer.created":
        await handle_customer_created(event["data"]["object"], db)
    else:
        logger.info(f"Unhandled event type: {event['type']}")
    
    return JSONResponse(content={"status": "success"})

async def handle_subscription_created(subscription: Dict[str, Any], db: Session):
    """Handle new subscription creation"""
    customer_id = subscription["customer"]
    
    # Find user by Stripe customer ID
    user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
    if not user:
        logger.error(f"User not found for customer {customer_id}")
        return
    
    # Create subscription record
    db_subscription = Subscription(
        user_id=user.id,
        stripe_subscription_id=subscription["id"],
        stripe_customer_id=customer_id,
        status=subscription["status"],
        current_period_start=subscription["current_period_start"],
        current_period_end=subscription["current_period_end"],
        plan_id=subscription["items"]["data"][0]["price"]["id"],
        trial_end=subscription.get("trial_end")
    )
    
    db.add(db_subscription)
    db.commit()
    
    # Update user status
    user.subscription_status = "active" if subscription["status"] == "active" else "trialing"
    user.plan_id = subscription["items"]["data"][0]["price"]["id"]
    db.commit()
    
    logger.info(f"Subscription created for user {user.id}")

async def handle_subscription_updated(subscription: Dict[str, Any], db: Session):
    """Handle subscription updates"""
    subscription_id = subscription["id"]
    
    # Find subscription record
    db_subscription = db.query(Subscription).filter(
        Subscription.stripe_subscription_id == subscription_id
    ).first()
    
    if not db_subscription:
        logger.error(f"Subscription not found: {subscription_id}")
        return
    
    # Update subscription
    db_subscription.status = subscription["status"]
    db_subscription.current_period_start = subscription["current_period_start"]
    db_subscription.current_period_end = subscription["current_period_end"]
    db_subscription.plan_id = subscription["items"]["data"][0]["price"]["id"]
    
    # Update user
    user = db_subscription.user
    user.subscription_status = subscription["status"]
    user.plan_id = subscription["items"]["data"][0]["price"]["id"]
    
    db.commit()
    logger.info(f"Subscription updated for user {user.id}")

async def handle_subscription_deleted(subscription: Dict[str, Any], db: Session):
    """Handle subscription cancellation"""
    subscription_id = subscription["id"]
    
    # Find subscription record
    db_subscription = db.query(Subscription).filter(
        Subscription.stripe_subscription_id == subscription_id
    ).first()
    
    if not db_subscription:
        logger.error(f"Subscription not found: {subscription_id}")
        return
    
    # Update subscription and user status
    db_subscription.status = "canceled"
    user = db_subscription.user
    user.subscription_status = "canceled"
    user.plan_id = "starter"  # Downgrade to free plan
    
    db.commit()
    logger.info(f"Subscription canceled for user {user.id}")

async def handle_payment_succeeded(invoice: Dict[str, Any], db: Session):
    """Handle successful payment"""
    customer_id = invoice["customer"]
    amount_paid = invoice["amount_paid"] / 100  # Convert from cents
    
    # Find user
    user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
    if user:
        # Update user's payment history, send receipt email, etc.
        logger.info(f"Payment succeeded: ${amount_paid} for user {user.id}")

async def handle_payment_failed(invoice: Dict[str, Any], db: Session):
    """Handle failed payment"""
    customer_id = invoice["customer"]
    
    # Find user
    user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
    if user:
        # Send payment failure notification, update status, etc.
        logger.warning(f"Payment failed for user {user.id}")

async def handle_customer_created(customer: Dict[str, Any], db: Session):
    """Handle new customer creation"""
    logger.info(f"New Stripe customer created: {customer['id']}")
'''
        
        webhook_file = self.webhooks_dir / "stripe_webhooks.py"
        with open(webhook_file, 'w') as f:
            f.write(webhook_code)
        
        return str(webhook_file)
    
    def create_subscription_manager(self):
        """Create subscription management service"""
        manager_code = '''from typing import Dict, List, Optional
from datetime import datetime, timedelta
from .stripe_client import StripeClient
from ..models import User, Subscription
from ..database import get_db
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class SubscriptionManager:
    def __init__(self):
        self.stripe_client = StripeClient()
        
        # Plan configurations
        self.plans = {
            "starter": {
                "price_id": "price_starter_monthly",
                "features": {
                    "product_scans_per_month": 100,
                    "scraper_sources": 5,
                    "ai_deal_scoring": False,
                    "ungating_predictions": False,
                    "api_access": False,
                    "priority_support": False
                }
            },
            "professional": {
                "price_id": "price_professional_monthly", 
                "features": {
                    "product_scans_per_month": 5000,
                    "scraper_sources": 15,
                    "ai_deal_scoring": True,
                    "ungating_predictions": True,
                    "api_access": True,
                    "api_calls_per_month": 1000,
                    "priority_support": True
                }
            },
            "enterprise": {
                "price_id": "price_enterprise_monthly",
                "features": {
                    "product_scans_per_month": -1,  # Unlimited
                    "scraper_sources": 28,
                    "ai_deal_scoring": True,
                    "ungating_predictions": True,
                    "api_access": True,
                    "api_calls_per_month": -1,  # Unlimited
                    "priority_support": True,
                    "dedicated_support": True,
                    "custom_integrations": True
                }
            }
        }
    
    async def create_subscription(self, user_id: int, plan_id: str, 
                                 db: Session) -> Dict[str, str]:
        """Create new subscription for user"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        if not user.stripe_customer_id:
            # Create Stripe customer
            customer = self.stripe_client.create_customer(
                email=user.email,
                name=user.full_name,
                metadata={"user_id": str(user.id)}
            )
            user.stripe_customer_id = customer.id
            db.commit()
        
        # Get plan configuration
        plan_config = self.plans.get(plan_id)
        if not plan_config:
            raise ValueError("Invalid plan ID")
        
        # Create subscription
        subscription = self.stripe_client.create_subscription(
            customer_id=user.stripe_customer_id,
            price_id=plan_config["price_id"],
            trial_period_days=7 if plan_id != "starter" else 0
        )
        
        return {
            "subscription_id": subscription.id,
            "client_secret": subscription.latest_invoice.payment_intent.client_secret,
            "status": subscription.status
        }
    
    async def upgrade_subscription(self, user_id: int, new_plan_id: str,
                                  db: Session) -> Dict[str, str]:
        """Upgrade user to new plan"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        subscription = db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.status.in_(["active", "trialing"])
        ).first()
        
        if not subscription:
            raise ValueError("No active subscription found")
        
        # Get new plan configuration
        new_plan_config = self.plans.get(new_plan_id)
        if not new_plan_config:
            raise ValueError("Invalid plan ID")
        
        # Update subscription
        updated_subscription = self.stripe_client.update_subscription(
            subscription.stripe_subscription_id,
            new_plan_config["price_id"]
        )
        
        return {
            "subscription_id": updated_subscription.id,
            "status": updated_subscription.status,
            "message": f"Successfully upgraded to {new_plan_id} plan"
        }
    
    async def cancel_subscription(self, user_id: int, immediate: bool = False,
                                 db: Session) -> Dict[str, str]:
        """Cancel user subscription"""
        subscription = db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.status.in_(["active", "trialing"])
        ).first()
        
        if not subscription:
            raise ValueError("No active subscription found")
        
        # Cancel subscription
        canceled_subscription = self.stripe_client.cancel_subscription(
            subscription.stripe_subscription_id,
            at_period_end=not immediate
        )
        
        return {
            "subscription_id": canceled_subscription.id,
            "status": canceled_subscription.status,
            "message": "Subscription canceled successfully"
        }
    
    def get_user_features(self, user: User) -> Dict[str, any]:
        """Get available features for user's current plan"""
        plan_id = user.plan_id or "starter"
        return self.plans.get(plan_id, self.plans["starter"])["features"]
    
    def check_feature_access(self, user: User, feature: str) -> bool:
        """Check if user has access to specific feature"""
        features = self.get_user_features(user)
        return features.get(feature, False)
    
    def check_usage_limit(self, user: User, usage_type: str, current_usage: int) -> Dict[str, any]:
        """Check if user is within usage limits"""
        features = self.get_user_features(user)
        limit = features.get(f"{usage_type}_per_month", 0)
        
        if limit == -1:  # Unlimited
            return {"allowed": True, "remaining": -1, "limit": -1}
        
        remaining = max(0, limit - current_usage)
        allowed = current_usage < limit
        
        return {
            "allowed": allowed,
            "remaining": remaining,
            "limit": limit,
            "current_usage": current_usage
        }
    
    async def record_usage(self, user_id: int, usage_type: str, quantity: int = 1):
        """Record usage for metered billing"""
        # Implementation depends on your usage tracking system
        logger.info(f"Recording {quantity} {usage_type} usage for user {user_id}")
    
    async def create_portal_session(self, user_id: int, return_url: str,
                                   db: Session) -> str:
        """Create Stripe customer portal session"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.stripe_customer_id:
            raise ValueError("User not found or no Stripe customer")
        
        session = self.stripe_client.create_portal_session(
            user.stripe_customer_id,
            return_url
        )
        
        return session.url
'''
        
        manager_file = self.stripe_dir / "subscription_manager.py"
        with open(manager_file, 'w') as f:
            f.write(manager_code)
        
        return str(manager_file)
    
    def create_billing_routes(self):
        """Create FastAPI routes for billing operations"""
        routes_code = '''from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..database import get_db
from ..models import User
from ..auth import get_current_user
from .subscription_manager import SubscriptionManager
from .stripe_client import StripeClient
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/billing", tags=["billing"])

subscription_manager = SubscriptionManager()
stripe_client = StripeClient()

@router.post("/create-checkout-session")
async def create_checkout_session(
    plan_id: str,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create Stripe Checkout session for subscription"""
    try:
        base_url = str(request.base_url).rstrip("/")
        success_url = f"{base_url}/dashboard?success=true&session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{base_url}/pricing?canceled=true"
        
        # Get plan configuration
        plans = subscription_manager.plans
        if plan_id not in plans:
            raise HTTPException(status_code=400, detail="Invalid plan ID")
        
        plan_config = plans[plan_id]
        
        session = stripe_client.create_checkout_session(
            price_id=plan_config["price_id"],
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=current_user.email,
            trial_period_days=7 if plan_id != "starter" else 0
        )
        
        return {"checkout_url": session.url}
        
    except Exception as e:
        logger.error(f"Failed to create checkout session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create checkout session")

@router.post("/upgrade-subscription")
async def upgrade_subscription(
    new_plan_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upgrade user subscription to new plan"""
    try:
        result = await subscription_manager.upgrade_subscription(
            current_user.id, new_plan_id, db
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to upgrade subscription: {e}")
        raise HTTPException(status_code=500, detail="Failed to upgrade subscription")

@router.post("/cancel-subscription") 
async def cancel_subscription(
    immediate: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel user subscription"""
    try:
        result = await subscription_manager.cancel_subscription(
            current_user.id, immediate, db
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to cancel subscription: {e}")
        raise HTTPException(status_code=500, detail="Failed to cancel subscription")

@router.get("/subscription-status")
async def get_subscription_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user subscription status"""
    try:
        features = subscription_manager.get_user_features(current_user)
        
        return {
            "plan_id": current_user.plan_id,
            "subscription_status": current_user.subscription_status,
            "features": features,
            "stripe_customer_id": current_user.stripe_customer_id
        }
    except Exception as e:
        logger.error(f"Failed to get subscription status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get subscription status")

@router.get("/usage")
async def get_usage_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current usage statistics"""
    try:
        # This would typically query your usage tracking system
        # For now, returning mock data
        mock_usage = {
            "product_scans": {"current": 1247, "limit": 5000},
            "api_calls": {"current": 342, "limit": 1000},
            "scraper_sources": {"current": 12, "limit": 15}
        }
        
        # Add usage limit checks
        for usage_type, data in mock_usage.items():
            limit_check = subscription_manager.check_usage_limit(
                current_user, usage_type, data["current"]
            )
            data.update(limit_check)
        
        return {"usage": mock_usage}
        
    except Exception as e:
        logger.error(f"Failed to get usage stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get usage stats")

@router.post("/create-portal-session")
async def create_portal_session(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create Stripe customer portal session"""
    try:
        base_url = str(request.base_url).rstrip("/")
        return_url = f"{base_url}/dashboard/billing"
        
        portal_url = await subscription_manager.create_portal_session(
            current_user.id, return_url, db
        )
        
        return {"portal_url": portal_url}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create portal session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create portal session")

@router.get("/plans")
async def get_available_plans():
    """Get all available subscription plans"""
    return {"plans": subscription_manager.plans}
'''
        
        routes_file = self.stripe_dir / "billing_routes.py"
        with open(routes_file, 'w') as f:
            f.write(routes_code)
        
        return str(routes_file)
    
    def create_stripe_setup_script(self):
        """Create setup script for Stripe products and prices"""
        setup_script = '''#!/usr/bin/env python3
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
        print("\\nCreating products and prices...")
        products = create_products_and_prices()
        
        # Set up webhook endpoints
        print("\\nSetting up webhook endpoints...")
        webhook = setup_webhook_endpoints()
        
        print("\\n✅ Stripe setup completed successfully!")
        print("\\nNext steps:")
        print("1. Add the webhook secret to your environment variables")
        print("2. Update your application with the created price IDs")
        print("3. Test the integration with test cards")
        
        # Print price IDs for easy copying
        print("\\nPrice IDs for your configuration:")
        for product_id, data in products.items():
            print(f"\\nProduct: {data['product'].name}")
            for price in data["prices"]:
                print(f"  {price.nickname}: {price.id}")
                
    except Exception as e:
        print(f"Error during setup: {e}")

if __name__ == "__main__":
    main()
'''
        
        setup_file = self.stripe_dir / "setup_stripe.py"
        with open(setup_file, 'w') as f:
            f.write(setup_script)
        
        return str(setup_file)
    
    def create_requirements_file(self):
        """Create requirements for Stripe integration"""
        requirements = '''# Stripe Integration Requirements
stripe==7.7.0
fastapi==0.104.1
sqlalchemy==2.0.23
pydantic==2.5.0
python-dotenv==1.0.0
'''
        
        req_file = self.stripe_dir / "requirements.txt"
        with open(req_file, 'w') as f:
            f.write(requirements)
        
        return str(req_file)
    
    def run(self):
        """Main execution function"""
        if not self.check_enabled("Stripe payment infrastructure setup"):
            return None
            
        print("💳 [StripeVoyager] Building Stripe payment infrastructure...")
        
        # Create configuration
        config = self.create_stripe_config()
        config_file = self.stripe_dir / "stripe_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Create all components
        client_file = self.create_stripe_client()
        webhook_file = self.create_webhook_handler() 
        manager_file = self.create_subscription_manager()
        routes_file = self.create_billing_routes()
        setup_file = self.create_stripe_setup_script()
        req_file = self.create_requirements_file()
        
        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "stripe_integration": {
                "api_version": config["api_version"],
                "plans_created": len(config["product_catalog"]),
                "webhook_events": len(config["webhook_endpoints"]),
                "files_created": [
                    str(config_file),
                    client_file,
                    webhook_file,
                    manager_file,
                    routes_file,
                    setup_file,
                    req_file
                ]
            },
            "pricing_summary": {
                plan: {
                    "amount": plan_data["amount"],
                    "interval": plan_data["interval"],
                    "features_count": len(plan_data["features"])
                }
                for plan, plan_data in config["product_catalog"].items()
            },
            "next_steps": [
                "Set STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET environment variables",
                "Run setup_stripe.py to create products in Stripe",
                "Install requirements: pip install -r requirements.txt",
                "Add billing routes to your FastAPI app",
                "Configure webhook endpoint URL in Stripe dashboard",
                "Test with Stripe test cards"
            ]
        }
        
        # Save report
        report_file = self.stripe_dir / "stripe_integration_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print("✅ StripeVoyager: Payment infrastructure created successfully!")
        print(f"   💰 Plans configured: {len(config['product_catalog'])}")
        print(f"   🔗 Webhook events: {len(config['webhook_endpoints'])}")
        print(f"   📁 Files created: {len(report['stripe_integration']['files_created'])}")
        print(f"   📋 Report: {report_file}")
        
        print("\n🚀 Stripe Integration Components:")
        print(f"   • Configuration: {config_file}")
        print(f"   • Client wrapper: {client_file}")
        print(f"   • Webhook handler: {webhook_file}")
        print(f"   • Subscription manager: {manager_file}")
        print(f"   • API routes: {routes_file}")
        print(f"   • Setup script: {setup_file}")
        print(f"   • Requirements: {req_file}")
        
        print("\n💡 Next Steps:")
        for step in report['next_steps']:
            print(f"   • {step}")
        
        print("💳 [StripeVoyager] Ready for SaaS billing deployment!")

def run():
    """CLI entry point"""
    voyager = StripeVoyager()
    voyager.run()

if __name__ == "__main__":
    run()
