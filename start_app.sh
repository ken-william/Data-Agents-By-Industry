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

# Ensure python virtualenv is active if present
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "Starting Uvicorn Server on http://0.0.0.0:8000..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
