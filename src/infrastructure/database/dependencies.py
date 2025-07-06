"""
Dependency injection container for repositories.
This helps manage the lifecycle of repositories and their dependencies.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Protocol

from src.domain.repo.UserRepository import UserRepository
from src.domain.repo.TodoRepository import TodoRepository
from .repo.user_repository_impl import UserRepositoryImpl
from .repo.todo_repository_impl import TodoRepositoryImpl


class RepositoryContainer:
    """Container for repository dependencies"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self._user_repo: UserRepository = None
        self._todo_repo: TodoRepository = None
    
    @property
    def user_repository(self) -> UserRepository:
        """Get user repository instance"""
        if self._user_repo is None:
            self._user_repo = UserRepositoryImpl(self.session)
        return self._user_repo
    
    @property
    def todo_repository(self) -> TodoRepository:
        """Get todo repository instance"""
        if self._todo_repo is None:
            self._todo_repo = TodoRepositoryImpl(self.session)
        return self._todo_repo


async def get_repository_container(session: AsyncSession) -> RepositoryContainer:
    """Factory function to create repository container"""
    return RepositoryContainer(session)
