from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing import Optional, List
from uuid import UUID

from src.domain.entities.todo import Todo
from src.domain.repo.TodoRepository import TodoRepository
from ..models.todo_model import TodoModel


class TodoRepositoryImpl(TodoRepository):
    """
    SQLAlchemy implementation of TodoRepository.
    This is HOW we store todos in PostgreSQL.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, todo: Todo) -> Todo:
        """Save a todo and return the saved todo"""
        try:
            # Convert domain entity to database model
            todo_model = TodoModel(
                id=UUID(todo.id) if isinstance(todo.id, str) else todo.id,
                user_id=UUID(todo.user_id) if isinstance(todo.user_id, str) else todo.user_id,
                title=todo.title,
                description=todo.description,
                completed=todo.completed,
                created_at=todo.created_at,
                completed_at=todo.completed_at
            )
            
            self.session.add(todo_model)
            await self.session.flush()  # Ensures we get the ID back
            
            # Convert back to domain entity
            return self._model_to_entity(todo_model)
        except ValueError as e:
            print(f"Error saving todo - Invalid UUID: {e}")
            raise ValueError("Invalid ID format")
        
        # Convert back to domain entity
        return self._model_to_entity(todo_model)
    
    async def get_by_id(self, todo_id: str) -> Optional[Todo]:
        """Get todo by ID, return None if not found"""
        try:
            uuid_obj = UUID(todo_id)
            query = select(TodoModel).where(TodoModel.id == uuid_obj)
            result = await self.session.execute(query)
            todo_model = result.scalar_one_or_none()
            
            if todo_model:
                return self._model_to_entity(todo_model)
            return None
        except ValueError as e:
            print(f"Invalid UUID format: {todo_id}, error: {e}")
            return None
    
    async def get_by_user_id(self, user_id: str) -> List[Todo]:
        """Get all todos for a specific user"""
        try:
            uuid_obj = UUID(user_id)
            query = select(TodoModel).where(TodoModel.user_id == uuid_obj)
            result = await self.session.execute(query)
            todo_models = result.scalars().all()
            
            return [self._model_to_entity(model) for model in todo_models]
        except ValueError as e:
            print(f"Invalid UUID format: {user_id}, error: {e}")
            return []
    
    async def update(self, todo: Todo) -> Todo:
        """Update an existing todo"""
        try:
            # First get the existing model
            uuid_obj = UUID(todo.id)
            query = select(TodoModel).where(TodoModel.id == uuid_obj)
            result = await self.session.execute(query)
            todo_model = result.scalar_one_or_none()
            
            if not todo_model:
                raise ValueError(f"Todo with id {todo.id} not found")
            
            # Update the model with new values
            todo_model.title = todo.title
            todo_model.description = todo.description
            todo_model.completed = todo.completed
            todo_model.completed_at = todo.completed_at
            
            await self.session.flush()
            
            return self._model_to_entity(todo_model)
        except ValueError as e:
            if "not found" in str(e):
                raise e
            print(f"Invalid UUID format: {todo.id}, error: {e}")
            raise ValueError(f"Invalid todo ID format")
    
    async def delete(self, todo_id: str) -> bool:
        """Delete todo, return True if deleted, False if not found"""
        try:
            uuid_obj = UUID(todo_id)
            query = delete(TodoModel).where(TodoModel.id == uuid_obj)
            result = await self.session.execute(query)
            return result.rowcount > 0
        except ValueError as e:
            print(f"Invalid UUID format: {todo_id}, error: {e}")
            return False
        return result.rowcount > 0
    
    async def get_completed_todos(self, user_id: str) -> List[Todo]:
        """Get all completed todos for a user"""
        try:
            uuid_obj = UUID(user_id)
            query = select(TodoModel).where(
                TodoModel.user_id == uuid_obj,
                TodoModel.completed == True
            )
            result = await self.session.execute(query)
            todo_models = result.scalars().all()
            
            return [self._model_to_entity(model) for model in todo_models]
        except ValueError as e:
            print(f"Invalid UUID format: {user_id}, error: {e}")
            return []
    
    async def get_pending_todos(self, user_id: str) -> List[Todo]:
        """Get all pending todos for a user"""
        try:
            uuid_obj = UUID(user_id)
            query = select(TodoModel).where(
                TodoModel.user_id == uuid_obj,
                TodoModel.completed == False
            )
            result = await self.session.execute(query)
            todo_models = result.scalars().all()
            
            return [self._model_to_entity(model) for model in todo_models]
        except ValueError as e:
            print(f"Invalid UUID format: {user_id}, error: {e}")
            return []
    
    def _model_to_entity(self, todo_model: TodoModel) -> Todo:
        """Convert database model to domain entity"""
        todo = Todo(
            id=str(todo_model.id),
            user_id=str(todo_model.user_id),
            title=todo_model.title,
            description=todo_model.description or ""
        )
        todo.completed = todo_model.completed
        todo.created_at = todo_model.created_at
        todo.completed_at = todo_model.completed_at
        return todo
