from fastapi import APIRouter, Depends, HTTPException, Request
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
