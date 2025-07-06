#!/bin/bash
set -e

echo "Starting deployment script..."

# Run database migrations
echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI server..."
# Start the application using uvicorn
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
