from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Optional
from uuid import UUID

from src.domain.entities.user import User
from src.domain.repo.UserRepository import UserRepository
from ..models.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    """
    SQLAlchemy implementation of UserRepository.
    This is HOW we store users in PostgreSQL.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, user: User) -> User:
        """Save a user and return the saved user"""
        try:
            # Convert domain entity to database model
            user_model = UserModel(
                id=UUID(user.id) if isinstance(user.id, str) else user.id,
                username=user.username,  # Added username
                email=user.email,
                password_hash=user.password_hash,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            
            self.session.add(user_model)
            await self.session.commit()
            await self.session.refresh(user_model)
            
            # Convert back to domain entity
            return self._model_to_entity(user_model)
        except ValueError as e:
            print(f"Error saving user - Invalid UUID: {e}")
            raise ValueError("Invalid user ID format")
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            # Validate and convert string to UUID
            uuid_obj = UUID(user_id)
            query = select(UserModel).where(UserModel.id == uuid_obj)
            result = await self.session.execute(query)
            user_model = result.scalar_one_or_none()
            
            if user_model:
                return self._model_to_entity(user_model)
            return None
        except ValueError as e:
            # Invalid UUID format
            print(f"Invalid UUID format: {user_id}, error: {e}")
            return None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        user_model = result.scalar_one_or_none()
        
        if user_model:
            return self._model_to_entity(user_model)
        return None
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        query = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(query)
        user_model = result.scalar_one_or_none()
        
        if user_model:
            return self._model_to_entity(user_model)
        return None
    
    async def delete(self, user_id: str) -> bool:
        """Delete user by ID"""
        query = delete(UserModel).where(UserModel.id == UUID(user_id))
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0
    
    def _model_to_entity(self, user_model: UserModel) -> User:
        """Convert UserModel to User entity"""
        return User(
            id=str(user_model.id),
            username=user_model.username,  # Added username
            email=user_model.email,
            password_hash=user_model.password_hash,
            is_active=user_model.is_active,
            created_at=user_model.created_at
        )