from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from ..config.settings import settings

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()


# Dependency function for FastAPI
async def get_session() -> AsyncSession:
    """
    Dependency function to get database session.
    This will be used by FastAPI for dependency injection.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Function to create all tables
async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Function to close engine
async def close_engine():
    """Close database engine"""
    await engine.dispose()