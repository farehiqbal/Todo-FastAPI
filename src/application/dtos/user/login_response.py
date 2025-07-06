from pydantic import BaseModel
from .user_response import UserResponse


class LoginResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"
