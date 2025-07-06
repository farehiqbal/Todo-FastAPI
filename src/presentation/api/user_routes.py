from fastapi import APIRouter, Depends, HTTPException

from src.application.services.user_service import UserService
from src.application.dtos.user.create_user import CreateUserRequest
from src.application.dtos.user.login_user import LoginRequest
from src.application.dtos.user.user_response import UserResponse
from src.application.dtos.user.login_response import LoginResponse
from src.presentation.dependencies import get_user_service
from src.presentation.auth import get_current_user_id


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse)
async def register_user(
    request: CreateUserRequest,
    user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.create_user(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=LoginResponse)
async def login_user(
    request: LoginRequest,
    user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.login(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user_id: str = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service)
):
    """Get current user's profile (requires authentication)"""
    try:
        return await user_service.get_user(current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))