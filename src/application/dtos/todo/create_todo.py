from pydantic import BaseModel
from typing import Optional

class CreateTodoRequest(BaseModel):
    title: str
    description: Optional[str] = None
    user_id: Optional[str] = None  # Will be set from JWT token