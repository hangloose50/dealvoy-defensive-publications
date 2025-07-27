from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..auth import get_current_user
from typing import Optional

async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verify that the current user has admin privileges.
    This should be used as a dependency for all admin routes.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    # Check if user has admin role
    if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    return current_user

def require_admin_permission(permission: str):
    """
    Decorator factory for requiring specific admin permissions.
    Usage: @require_admin_permission("user_management")
    """
    async def permission_checker(
        current_admin: User = Depends(get_current_admin_user)
    ) -> User:
        # Check if admin has specific permission
        # This would typically check against a permissions table
        admin_permissions = getattr(current_admin, 'permissions', [])
        
        if permission not in admin_permissions and 'super_admin' not in admin_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required"
            )
        
        return current_admin
    
    return permission_checker

class AdminPermissions:
    """Admin permission constants"""
    USER_MANAGEMENT = "user_management"
    SUBSCRIPTION_MANAGEMENT = "subscription_management"
    SYSTEM_MONITORING = "system_monitoring"
    ANALYTICS_ACCESS = "analytics_access"
    SECURITY_MANAGEMENT = "security_management"
    SUPER_ADMIN = "super_admin"
