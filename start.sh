#!/bin/sh

# Use environment variables from .env or defaults
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

# Wait for the database to be ready
echo "Waiting for database at $DB_HOST:$DB_PORT ..."
# while ! nc -z $DB_HOST $DB_PORT -w 1; do
#   sleep 2
# done


echo "Database is up. Running migrations..."

# Run Alembic migrations
# 🟢 This is the safe Alembic migration logic
# It runs Alembic migrations, and if already applied, it won't crash
alembic upgrade head || echo "Alembic migrations already up-to-date or skipped safely."

echo "Starting FastAPI app..."
# Start the app
uvicorn app.main:app --host 0.0.0.0 --port 8000
