from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from ..database import get_db
from ..models import User, Subscription, Usage, SystemMetric
from ..auth import get_current_admin_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users")
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    plan: Optional[str] = Query(None),
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get paginated list of users with filters"""
    try:
        query = db.query(User)
        
        # Apply filters
        if search:
            query = query.filter(
                User.email.contains(search) | 
                User.full_name.contains(search)
            )
        
        if status:
            query = query.filter(User.subscription_status == status)
            
        if plan:
            query = query.filter(User.plan_id == plan)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        users = query.offset(skip).limit(limit).all()
        
        return {
            "users": [
                {
                    "id": user.id,
                    "email": user.email,
                    "name": user.full_name,
                    "plan": user.plan_id,
                    "status": user.subscription_status,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "last_login": user.last_login.isoformat() if user.last_login else None,
                    "revenue": calculate_user_revenue(user.id, db),
                    "usage": get_user_usage_summary(user.id, db)
                }
                for user in users
            ],
            "total": total,
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Failed to get users: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve users")

@router.get("/users/{user_id}")
async def get_user_details(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific user"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get subscription details
        subscription = db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.status.in_(["active", "trialing"])
        ).first()
        
        # Get usage statistics
        usage_stats = get_detailed_user_usage(user_id, db)
        
        # Get revenue information
        revenue_stats = get_user_revenue_breakdown(user_id, db)
        
        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.full_name,
                "plan": user.plan_id,
                "status": user.subscription_status,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "last_login": user.last_login.isoformat() if user.last_login else None,
                "stripe_customer_id": user.stripe_customer_id
            },
            "subscription": {
                "id": subscription.id if subscription else None,
                "status": subscription.status if subscription else None,
                "current_period_start": subscription.current_period_start if subscription else None,
                "current_period_end": subscription.current_period_end if subscription else None,
                "trial_end": subscription.trial_end if subscription else None
            } if subscription else None,
            "usage": usage_stats,
            "revenue": revenue_stats
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user details: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user details")

@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    status: str,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update user status (active, suspended, etc.)"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        valid_statuses = ["active", "inactive", "suspended"]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail="Invalid status")
        
        user.subscription_status = status
        db.commit()
        
        logger.info(f"Admin {current_admin.id} updated user {user_id} status to {status}")
        
        return {"message": f"User status updated to {status}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update user status: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user status")

@router.get("/analytics/overview")
async def get_analytics_overview(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get high-level analytics overview"""
    try:
        # Calculate date ranges
        now = datetime.utcnow()
        last_month = now - timedelta(days=30)
        last_week = now - timedelta(days=7)
        
        # Total users
        total_users = db.query(User).count()
        new_users_month = db.query(User).filter(User.created_at >= last_month).count()
        
        # Active subscriptions
        active_subs = db.query(Subscription).filter(
            Subscription.status.in_(["active", "trialing"])
        ).count()
        
        # Revenue calculation (mock for now)
        monthly_revenue = calculate_monthly_revenue(db)
        
        # API usage
        api_calls_week = get_api_usage_count(last_week, now, db)
        
        # System health
        system_health = get_system_health_summary(db)
        
        return {
            "users": {
                "total": total_users,
                "new_this_month": new_users_month,
                "growth_rate": calculate_growth_rate(new_users_month, total_users)
            },
            "subscriptions": {
                "active": active_subs,
                "conversion_rate": calculate_conversion_rate(db)
            },
            "revenue": {
                "monthly": monthly_revenue,
                "growth": calculate_revenue_growth(db)
            },
            "usage": {
                "api_calls_week": api_calls_week,
                "average_per_user": api_calls_week / max(active_subs, 1)
            },
            "system_health": system_health
        }
        
    except Exception as e:
        logger.error(f"Failed to get analytics overview: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics")

@router.get("/system/health")
async def get_system_health(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get detailed system health metrics"""
    try:
        # Get latest system metrics
        metrics = db.query(SystemMetric).filter(
            SystemMetric.timestamp >= datetime.utcnow() - timedelta(minutes=5)
        ).all()
        
        # Service status (this would typically come from monitoring service)
        services = [
            {
                "name": "Web API",
                "status": "online",
                "uptime": "99.9%",
                "response_time": "120ms",
                "last_check": "30s ago"
            },
            {
                "name": "Scraper Service", 
                "status": "online",
                "uptime": "98.7%",
                "response_time": "340ms",
                "last_check": "45s ago"
            },
            {
                "name": "AI Processing",
                "status": "degraded", 
                "uptime": "97.2%",
                "response_time": "890ms",
                "last_check": "1m ago"
            }
        ]
        
        return {
            "metrics": [
                {
                    "name": metric.name,
                    "value": metric.value,
                    "status": metric.status,
                    "timestamp": metric.timestamp.isoformat()
                }
                for metric in metrics
            ],
            "services": services,
            "overall_status": "healthy"  # Calculate based on metrics
        }
        
    except Exception as e:
        logger.error(f"Failed to get system health: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve system health")

# Helper functions
def calculate_user_revenue(user_id: int, db: Session) -> float:
    """Calculate total revenue from a user"""
    # This would typically query payment records
    return 297.0  # Mock value

def get_user_usage_summary(user_id: int, db: Session) -> Dict[str, int]:
    """Get user usage summary"""
    # This would query actual usage records
    return {
        "product_scans": 1247,
        "api_calls": 892
    }

def get_detailed_user_usage(user_id: int, db: Session) -> Dict[str, Any]:
    """Get detailed usage statistics for a user"""
    return {
        "current_month": {
            "product_scans": 1247,
            "api_calls": 892,
            "scraper_usage": 45
        },
        "last_month": {
            "product_scans": 1105,
            "api_calls": 756,
            "scraper_usage": 38
        }
    }

def get_user_revenue_breakdown(user_id: int, db: Session) -> Dict[str, Any]:
    """Get revenue breakdown for a user"""
    return {
        "total_revenue": 582.0,
        "monthly_payments": [
            {"month": "2024-07", "amount": 97.0},
            {"month": "2024-06", "amount": 97.0},
            {"month": "2024-05", "amount": 97.0}
        ]
    }

def calculate_monthly_revenue(db: Session) -> float:
    """Calculate total monthly revenue"""
    return 28430.0  # Mock value

def calculate_growth_rate(new_count: int, total_count: int) -> float:
    """Calculate growth rate percentage"""
    if total_count == 0:
        return 0.0
    return (new_count / total_count) * 100

def calculate_conversion_rate(db: Session) -> float:
    """Calculate trial to paid conversion rate"""
    return 85.5  # Mock value

def calculate_revenue_growth(db: Session) -> float:
    """Calculate revenue growth percentage"""
    return 15.2  # Mock value

def get_api_usage_count(start_date: datetime, end_date: datetime, db: Session) -> int:
    """Get API usage count for date range"""
    return 24500  # Mock value

def get_system_health_summary(db: Session) -> Dict[str, str]:
    """Get overall system health summary"""
    return {
        "status": "healthy",
        "cpu_usage": "45%",
        "memory_usage": "67%",
        "database_load": "32%"
    }
