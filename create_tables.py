import asyncio
from src.infrastructure.database.connection import engine, Base

# Import models so they're registered with Base
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.models.todo_model import TodoModel

async def create_tables():
    print("Dropping existing tables...")
    async with engine.begin() as conn:
        # Drop all tables and recreate
        await conn.run_sync(Base.metadata.drop_all)
        print("Creating new tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())