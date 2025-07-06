from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from src.infrastructure.config.settings import settings


class JWTHandler:
    def __init__(self):
        self.secret_key = settings.jwt_secret_key
        self.algorithm = settings.jwt_algorithm
        self.expires_delta = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    
    def create_access_token(self, user_id: str, email: str) -> str:
        """Create JWT access token"""
        expire = datetime.utcnow() + self.expires_delta
        payload = {
            "sub": user_id,  # Subject (user ID)
            "email": email,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload.get("sub")
            if user_id is None:
                return None
            return payload
        except JWTError:
            return None


jwt_handler = JWTHandler()
