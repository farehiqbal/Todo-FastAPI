from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.infrastructure.database.connection import get_session
from src.infrastructure.database.repo.user_repository_impl import UserRepositoryImpl
from src.infrastructure.database.repo.todo_repository_impl import TodoRepositoryImpl
from src.application.services.user_service import UserService
from src.application.services.todo_service import TodoService


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    user_repo = UserRepositoryImpl(session)
    return UserService(user_repo)


async def get_todo_service(session: AsyncSession = Depends(get_session)) -> TodoService:
    user_repo = UserRepositoryImpl(session)
    todo_repo = TodoRepositoryImpl(session)
    return TodoService(todo_repo, user_repo)