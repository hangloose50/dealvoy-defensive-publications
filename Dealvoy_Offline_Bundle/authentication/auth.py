from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
import bcrypt
import logging
import re
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Dealvoy Authentication API",
    description="Authentication and user management for Dealvoy AI Platform",
    version="1.0.0",
    docs_url="/auth/docs",
    redoc_url="/auth/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT Configuration
SECRET_KEY = "dealvoy-secret-key-change-in-production"  # Change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

# Security
security = HTTPBearer()

# Demo Users Database (Replace with real database in production)
demo_users = {
    "demo@dealvoy.ai": {
        "id": "user_demo_001",
        "email": "demo@dealvoy.ai",
        "password_hash": bcrypt.hashpw("demo123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        "first_name": "Demo",
        "last_name": "User",
        "role": "user",
        "company": "Demo Company",
        "business_type": "amazon-seller",
        "monthly_revenue": "10k-50k",
        "is_active": True,
        "trial_end_date": datetime.now() + timedelta(days=30),
        "created_at": datetime.now() - timedelta(days=5),
        "last_login": None
    },
    "admin@dealvoy.ai": {
        "id": "user_admin_001",
        "email": "admin@dealvoy.ai",
        "password_hash": bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        "first_name": "Admin",
        "last_name": "User",
        "role": "admin",
        "company": "Dealvoy Inc",
        "business_type": "enterprise",
        "monthly_revenue": "500k+",
        "is_active": True,
        "trial_end_date": None,  # No trial for admin
        "created_at": datetime.now() - timedelta(days=100),
        "last_login": None
    },
    "user@dealvoy.ai": {
        "id": "user_standard_001",
        "email": "user@dealvoy.ai",
        "password_hash": bcrypt.hashpw("user123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        "first_name": "Standard",
        "last_name": "User",
        "role": "user",
        "company": "E-commerce Store",
        "business_type": "shopify-store",
        "monthly_revenue": "50k-100k",
        "is_active": True,
        "trial_end_date": datetime.now() + timedelta(days=15),
        "created_at": datetime.now() - timedelta(days=15),
        "last_login": None
    }
}

# Pydantic Models
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    remember_me: Optional[bool] = False

class UserSignup(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    company: Optional[str] = Field(None, max_length=100)
    business_type: Optional[str] = None
    monthly_revenue: Optional[str] = None
    marketing_consent: Optional[bool] = False

class UserProfile(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    company: Optional[str]
    business_type: Optional[str]
    monthly_revenue: Optional[str]
    is_active: bool
    trial_end_date: Optional[datetime]
    created_at: datetime
    last_login: Optional[datetime]

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserProfile

class PasswordReset(BaseModel):
    email: EmailStr

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)

# Helper Functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_password(password: str) -> str:
    """Hash password with bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def validate_password_strength(password: str) -> Dict[str, Any]:
    """Validate password strength"""
    errors = []
    score = 0
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    else:
        score += 1
    
    if len(password) >= 12:
        score += 1
    
    if re.search(r"[a-z]", password):
        score += 1
    else:
        errors.append("Password must contain lowercase letters")
    
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        errors.append("Password must contain uppercase letters")
    
    if re.search(r"\d", password):
        score += 1
    else:
        errors.append("Password must contain numbers")
    
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    
    strength_levels = ["weak", "fair", "good", "strong"]
    strength = strength_levels[min(score // 2, 3)]
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "strength": strength,
        "score": score
    }

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extract current user from JWT token"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if user_id is None or token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Find user in demo database
    user = None
    for email, user_data in demo_users.items():
        if user_data["id"] == user_id:
            user = user_data
            break
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user

# API Endpoints
@app.post("/auth/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    """Authenticate user and return JWT tokens"""
    try:
        # Find user
        user = demo_users.get(user_data.email.lower())
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(user_data.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is active
        if not user["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )
        
        # Update last login
        user["last_login"] = datetime.now()
        
        # Create tokens
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        if user_data.remember_me:
            access_token_expires = timedelta(days=7)  # Extended for remember me
        
        access_token = create_access_token(
            data={"sub": user["id"]}, 
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(data={"sub": user["id"]})
        
        # Create user profile
        user_profile = UserProfile(
            id=user["id"],
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            role=user["role"],
            company=user.get("company"),
            business_type=user.get("business_type"),
            monthly_revenue=user.get("monthly_revenue"),
            is_active=user["is_active"],
            trial_end_date=user.get("trial_end_date"),
            created_at=user["created_at"],
            last_login=user["last_login"]
        )
        
        logger.info(f"User {user_data.email} logged in successfully")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=int(access_token_expires.total_seconds()),
            user=user_profile
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service error"
        )

@app.post("/auth/signup", response_model=TokenResponse)
async def signup(user_data: UserSignup):
    """Register new user account"""
    try:
        # Check if user already exists
        if user_data.email.lower() in demo_users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Validate password strength
        password_validation = validate_password_strength(user_data.password)
        if not password_validation["is_valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password validation failed: {', '.join(password_validation['errors'])}"
            )
        
        # Create new user
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        hashed_password = hash_password(user_data.password)
        
        new_user = {
            "id": user_id,
            "email": user_data.email.lower(),
            "password_hash": hashed_password,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "role": "user",
            "company": user_data.company,
            "business_type": user_data.business_type,
            "monthly_revenue": user_data.monthly_revenue,
            "is_active": True,
            "trial_end_date": datetime.now() + timedelta(days=30),
            "created_at": datetime.now(),
            "last_login": datetime.now()
        }
        
        # Add to demo database
        demo_users[user_data.email.lower()] = new_user
        
        # Create tokens
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_id}, 
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(data={"sub": user_id})
        
        # Create user profile
        user_profile = UserProfile(
            id=new_user["id"],
            email=new_user["email"],
            first_name=new_user["first_name"],
            last_name=new_user["last_name"],
            role=new_user["role"],
            company=new_user.get("company"),
            business_type=new_user.get("business_type"),
            monthly_revenue=new_user.get("monthly_revenue"),
            is_active=new_user["is_active"],
            trial_end_date=new_user.get("trial_end_date"),
            created_at=new_user["created_at"],
            last_login=new_user["last_login"]
        )
        
        logger.info(f"New user {user_data.email} registered successfully")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=int(access_token_expires.total_seconds()),
            user=user_profile
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration service error"
        )

@app.post("/auth/refresh")
async def refresh_token(refresh_token: str):
    """Refresh access token using refresh token"""
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if user_id is None or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Create new access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_id}, 
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": int(access_token_expires.total_seconds())
        }
        
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@app.get("/auth/profile", response_model=UserProfile)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return UserProfile(
        id=current_user["id"],
        email=current_user["email"],
        first_name=current_user["first_name"],
        last_name=current_user["last_name"],
        role=current_user["role"],
        company=current_user.get("company"),
        business_type=current_user.get("business_type"),
        monthly_revenue=current_user.get("monthly_revenue"),
        is_active=current_user["is_active"],
        trial_end_date=current_user.get("trial_end_date"),
        created_at=current_user["created_at"],
        last_login=current_user["last_login"]
    )

@app.put("/auth/profile")
async def update_profile(
    profile_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Update user profile"""
    try:
        # Update allowed fields
        allowed_fields = ["first_name", "last_name", "company", "business_type", "monthly_revenue"]
        for field in allowed_fields:
            if field in profile_data:
                current_user[field] = profile_data[field]
        
        logger.info(f"Profile updated for user {current_user['email']}")
        
        return {"message": "Profile updated successfully"}
        
    except Exception as e:
        logger.error(f"Profile update error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile update failed"
        )

@app.post("/auth/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: dict = Depends(get_current_user)
):
    """Change user password"""
    try:
        # Verify current password
        if not verify_password(password_data.current_password, current_user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Validate new password
        password_validation = validate_password_strength(password_data.new_password)
        if not password_validation["is_valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password validation failed: {', '.join(password_validation['errors'])}"
            )
        
        # Update password
        current_user["password_hash"] = hash_password(password_data.new_password)
        
        logger.info(f"Password changed for user {current_user['email']}")
        
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password change error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )

@app.post("/auth/forgot-password")
async def forgot_password(reset_data: PasswordReset):
    """Initiate password reset process"""
    try:
        # Find user
        user = demo_users.get(reset_data.email.lower())
        if not user:
            # Don't reveal if email exists or not
            return {"message": "If the email exists, a reset link has been sent"}
        
        # In production: Generate reset token and send email
        # For demo: Just log the action
        logger.info(f"Password reset requested for {reset_data.email}")
        
        return {"message": "If the email exists, a reset link has been sent"}
        
    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset service error"
        )

@app.post("/auth/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout user (client should delete tokens)"""
    logger.info(f"User {current_user['email']} logged out")
    return {"message": "Logged out successfully"}

@app.get("/auth/validate")
async def validate_token(current_user: dict = Depends(get_current_user)):
    """Validate current token"""
    return {"valid": True, "user_id": current_user["id"]}

# Health check
@app.get("/auth/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Dealvoy Authentication API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

# Demo users endpoint (for testing)
@app.get("/auth/demo-users")
async def get_demo_users():
    """Get demo user credentials for testing"""
    return {
        "demo_users": [
            {"email": "demo@dealvoy.ai", "password": "demo123", "role": "user"},
            {"email": "admin@dealvoy.ai", "password": "admin123", "role": "admin"},
            {"email": "user@dealvoy.ai", "password": "user123", "role": "user"}
        ],
        "note": "These are demo credentials for testing purposes only"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
