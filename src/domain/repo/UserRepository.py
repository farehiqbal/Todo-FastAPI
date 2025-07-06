from abc import ABC, abstractmethod
from typing import Optional
from ..entities.user import User

class UserRepository(ABC):
    """
    Abstract repository for User operations.
    This defines WHAT operations we need, not HOW to do them.
    """
    
    @abstractmethod
    async def save(self, user: User) -> User:
        """Save a user and return the saved user"""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID, return None if not found"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email, return None if not found"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """Delete user, return True if deleted, False if not found"""
        pass