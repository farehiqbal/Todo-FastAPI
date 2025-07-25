from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from infrastructure.database.models import Base
from infrastructure.database.models.user_model import UserModel
from infrastructure.database.models.todo_model import TodoModel

# this is the Alembic Config object
config = context.config

# Set the database URL from environment
from infrastructure.config.settings import settings

# Handle different database URL formats (asyncpg vs psycopg2)
database_url = settings.database_url
if database_url.startswith("postgresql+asyncpg://"):
    # For migrations, use psycopg2 (synchronous)
    database_url = database_url.replace("+asyncpg", "")

config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for auto-generation
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()