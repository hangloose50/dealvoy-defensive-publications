from fastapi import APIRouter, Request, HTTPException, Depends
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
