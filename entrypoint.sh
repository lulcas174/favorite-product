#!/bin/bash
set -e


echo "Waiting for the database to become available..."
until pg_isready -h db -p 5432; do
  sleep 1
done

echo "Database is available, running migrations..."
alembic upgrade head

echo "Running flake8 to check code style..."
flake8 || { echo "flake8 found issues. Please fix them before running the application."; exit 1; }

echo "Running unit tests..."
pytest --maxfail=1 --disable-warnings -q \
  || { echo "Unit tests failed. Please fix them before running the application."; exit 1; }

echo "Starting application..."
exec uvicorn src.index:app --host 0.0.0.0 --port 8000 --reload
