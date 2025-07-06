#!/bin/bash
set -e

# Function to wait for postgres
wait_for_postgres() {
    echo "Waiting for PostgreSQL to be ready..."
    while ! pg_isready -h db -p 5432 -U todouser; do
        sleep 1
    done
    echo "PostgreSQL is ready!"
}

# Wait for database to be ready
wait_for_postgres

# Run database migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Create tables if they don't exist (fallback)
echo "Ensuring tables are created..."
python -c "
import asyncio
from src.infrastructure.database.connection import create_tables
asyncio.run(create_tables())
print('Tables created successfully!')
"

echo "Starting FastAPI server on port 8090..."
# Start the application
exec uvicorn main:app --host 0.0.0.0 --port 8090
