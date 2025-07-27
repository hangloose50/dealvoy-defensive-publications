import stripe
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
