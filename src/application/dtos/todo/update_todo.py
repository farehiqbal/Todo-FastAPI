from pydantic import BaseModel
from typing import Optional


class UpdateTodoRequest(BaseModel):
    todo_id: Optional[str] = None  # Will be set from URL path
    title: Optional[str] = None
    description: Optional[str] = None