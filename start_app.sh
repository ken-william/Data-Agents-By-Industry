#!/usr/bin/env bg
#!/bin/bash
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

# Ensure python virtualenv is active
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Ensure frontend is built
if [ ! -d "frontend/dist" ]; then
    echo "Building frontend static assets..."
    cd frontend && npx vite build && cd ..
fi

echo "Starting Uvicorn Server on http://0.0.0.0:8000..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
