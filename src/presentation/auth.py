from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.infrastructure.auth.jwt_handler import jwt_handler

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Dependency to get current authenticated user from JWT token
    """
    token = credentials.credentials
    payload = jwt_handler.verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload

def get_current_user_id(current_user: dict = Depends(get_current_user)) -> str:
    """Extract user ID from current user"""
    return current_user["sub"]
