#!/usr/bin/env sh

set -e

echo "Running DB migrations"
alembic upgrade head
echo "DB migrations success"

echo "Starting application"
uvicorn src.fast_api:app --host ${HOST} --port ${PORT}