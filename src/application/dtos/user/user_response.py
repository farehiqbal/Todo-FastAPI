from pydantic import BaseModel
from datetime import datetime


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    @classmethod
    def from_entity(cls, user):
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at
        )