#!/bin/bash

pipenv run python -m app.database.wait

if [ "$RUN_MIGRATIONS_ON_STARTUP" = "true" ]; then
  echo "Running migrations on startup"
  pipenv run python -m alembic upgrade head
else
  echo "Not running migrations on startup"
fi

pipenv run python -m uvicorn app.main:app --port 8001 --host 0.0.0.0 --reload