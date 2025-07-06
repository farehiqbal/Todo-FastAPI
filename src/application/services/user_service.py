from datetime import datetime
import uuid
import hashlib

from src.domain.entities.user import User
from src.domain.repo.UserRepository import UserRepository
from src.application.dtos.user.create_user import CreateUserRequest
from src.application.dtos.user.login_user import LoginRequest
from src.application.dtos.user.user_response import UserResponse
from src.application.dtos.user.login_response import LoginResponse
from src.infrastructure.auth.jwt_handler import jwt_handler


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    async def create_user(self, request: CreateUserRequest) -> UserResponse:
        # Check if user already exists
        existing_user = await self.user_repo.get_by_email(request.email)
        if existing_user:
            raise ValueError("User already exists")
        
        # Create user
        user = User(
            id=str(uuid.uuid4()),
            username=request.username,
            email=request.email,
            password_hash=self._hash_password(request.password),
            is_active=True,
            created_at=datetime.utcnow()
        )
        
        # Save and return
        saved_user = await self.user_repo.save(user)
        return UserResponse.from_entity(saved_user)
    
    async def login(self, request: LoginRequest) -> LoginResponse:
        # Get user by email
        user = await self.user_repo.get_by_email(request.email)
        if not user:
            raise ValueError("Invalid email or password")
        
        # Check password
        if user.password_hash != self._hash_password(request.password):
            raise ValueError("Invalid email or password")
        
        # Check if active
        if not user.is_active:
            raise ValueError("User account is deactivated")
        
        # Generate JWT token
        access_token = jwt_handler.create_access_token(user.id, user.email)
        
        return LoginResponse(
            user=UserResponse.from_entity(user),
            access_token=access_token
        )
    
    async def get_user(self, user_id: str) -> UserResponse:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        return UserResponse.from_entity(user)