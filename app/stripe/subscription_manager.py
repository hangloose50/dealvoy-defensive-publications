from typing import Dict, List, Optional
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
