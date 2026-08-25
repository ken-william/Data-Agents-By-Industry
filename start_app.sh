#!/usr/bin/env bash
# ==============================================================================
# Talk to Data - One-Click Application Startup Script
# ==============================================================================

PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"data-agents-by-industry"}
export GOOGLE_CLOUD_PROJECT=$PROJECT_ID

echo "================================================================================"
echo " Starting Talk to Data Application (FastAPI + React + Vertex AI Data Agents)"
echo " Target GCP Project: $PROJECT_ID"
echo "================================================================================"

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$BASE_DIR"

# Free up port 8000 if occupied by previous run
fuser -k 8000/tcp 2>/dev/null || pkill -f uvicorn 2>/dev/null || true
sleep 1

# Ensure python virtualenv is active
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Ensure frontend dependencies & static build assets exist
if [ -d "frontend" ]; then
    if [ ! -d "frontend/node_modules" ]; then
        echo "Installing frontend dependencies (npm install)..."
        (cd frontend && npm install)
    fi
    if [ ! -d "frontend/dist" ]; then
        echo "Building frontend static assets..."
        (cd frontend && npm run build)
    fi
fi

echo "Starting Uvicorn Server on http://0.0.0.0:8000..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
