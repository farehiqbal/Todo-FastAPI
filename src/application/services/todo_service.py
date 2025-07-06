from datetime import datetime
import uuid
from typing import List, Optional

from src.domain.entities.todo import Todo
from src.domain.repo.TodoRepository import TodoRepository
from src.domain.repo.UserRepository import UserRepository
from src.application.dtos.todo.create_todo import CreateTodoRequest
from src.application.dtos.todo.update_todo import UpdateTodoRequest
from src.application.dtos.todo.todo_response import TodoResponse


class TodoService:
    def __init__(self, todo_repo: TodoRepository, user_repo: UserRepository):
        self.todo_repo = todo_repo
        self.user_repo = user_repo
    
    async def create_todo(self, request: CreateTodoRequest) -> TodoResponse:
        # Check user exists
        user = await self.user_repo.get_by_id(request.user_id)
        if not user:
            raise ValueError("User not found")
        
        # Create todo
        todo = Todo(
            id=str(uuid.uuid4()),
            user_id=request.user_id,
            title=request.title,
            description=request.description or "",
            completed=False,
            created_at=datetime.utcnow(),
            completed_at=None
        )
        
        # Save and return
        saved_todo = await self.todo_repo.save(todo)
        return TodoResponse.from_entity(saved_todo)
    
    async def get_user_todos(self, user_id: str) -> List[TodoResponse]:
        # Check user exists
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Get todos
        todos = await self.todo_repo.get_by_user_id(user_id)
        return [TodoResponse.from_entity(todo) for todo in todos]
    
    async def get_todo(self, todo_id: str, user_id: str) -> TodoResponse:
        todo = await self.todo_repo.get_by_id(todo_id)
        if not todo:
            raise ValueError("Todo not found")
        
        if todo.user_id != user_id:
            raise ValueError("Not your todo")
        
        return TodoResponse.from_entity(todo)
    
    async def update_todo(self, request: UpdateTodoRequest, user_id: str) -> TodoResponse:
        # Get todo
        todo = await self.todo_repo.get_by_id(request.todo_id)
        if not todo:
            raise ValueError("Todo not found")
        
        if todo.user_id != user_id:
            raise ValueError("Not your todo")
        
        # Update fields
        if request.title:
            todo.update_title(request.title)
        if request.description is not None:
            todo.description = request.description
        
        # Save and return
        updated_todo = await self.todo_repo.update(todo)
        return TodoResponse.from_entity(updated_todo)
    
    async def complete_todo(self, todo_id: str, user_id: str) -> TodoResponse:
        # Get todo
        todo = await self.todo_repo.get_by_id(todo_id)
        if not todo:
            raise ValueError("Todo not found")
        
        if todo.user_id != user_id:
            raise ValueError("Not your todo")
        
        # Mark complete
        todo.mark_complete()
        
        # Save and return
        updated_todo = await self.todo_repo.update(todo)
        return TodoResponse.from_entity(updated_todo)
    
    async def delete_todo(self, todo_id: str, user_id: str) -> bool:
        # Get todo
        todo = await self.todo_repo.get_by_id(todo_id)
        if not todo:
            raise ValueError("Todo not found")
        
        if todo.user_id != user_id:
            raise ValueError("Not your todo")
        
        # Delete
        return await self.todo_repo.delete(todo_id)