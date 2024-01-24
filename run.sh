#!/bin/sh

export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8000}

# Activate the virtual environment
source venv/bin/activate

# The program is run with the following command:
exec uvicorn --reload --host "$HOST" --port "$PORT" 

# uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8003