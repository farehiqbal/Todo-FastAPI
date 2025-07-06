from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TodoResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: str
    completed: bool
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    @classmethod
    def from_entity(cls, todo):
        return cls(
            id=todo.id,
            user_id=todo.user_id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            created_at=todo.created_at,
            completed_at=todo.completed_at
        )