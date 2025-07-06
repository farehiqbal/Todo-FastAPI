from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.todo import Todo

class TodoRepository(ABC):
    """
    Abstract repository for Todo operations.
    This defines WHAT operations we need, not HOW to do them.
    """
    
    @abstractmethod
    async def save(self, todo: Todo) -> Todo:
        """Save a todo and return the saved todo"""
        pass
    
    @abstractmethod
    async def get_by_id(self, todo_id: str) -> Optional[Todo]:
        """Get todo by ID, return None if not found"""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> List[Todo]:
        """Get all todos for a specific user"""
        pass
    
    @abstractmethod
    async def update(self, todo: Todo) -> Todo:
        """Update an existing todo"""
        pass
    
    @abstractmethod
    async def delete(self, todo_id: str) -> bool:
        """Delete todo, return True if deleted, False if not found"""
        pass
    
    @abstractmethod
    async def get_completed_todos(self, user_id: str) -> List[Todo]:
        """Get all completed todos for a user"""
        pass
    
    @abstractmethod
    async def get_pending_todos(self, user_id: str) -> List[Todo]:
        """Get all pending todos for a user"""
        pass