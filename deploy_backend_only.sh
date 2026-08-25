#!/usr/bin/env bash
# ==============================================================================
# One-Click Headless Backend Deployment (ADK Orchestrator + MCP Toolbox)
# Decoupled from Frontend for 100% Modularity
# ==============================================================================

set -e

PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"data-agents-by-industry"}
REGION=${REGION:-"europe-west9"}
SERVICE_NAME="talktodata-backend"

echo "================================================================================"
echo "🚀 Déploiement du Backend Découplé (Orchestrateur ADK + MCP Toolbox)"
echo "  Projet GCP : $PROJECT_ID"
echo "  Région     : $REGION"
echo "  Service    : $SERVICE_NAME"
echo "================================================================================"

gcloud config set project "$PROJECT_ID"

# Enable Cloud Run & Cloud Build APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# Deploy headless backend using Dockerfile.backend
echo "Construction de l'image backend et déploiement sur Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
    --source . \
    --region "$REGION" \
    --allow-unauthenticated \
    --port 8080 \
    --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID" \
    --memory 2Gi \
    --cpu 2 \
    --min-instances 0 \
    --max-instances 10 \
    --timeout 300s

echo "================================================================================"
echo "✅ Backend Découplé déployé avec succès !"
BACKEND_URL=$(gcloud run services describe "$SERVICE_NAME" --region "$REGION" --format 'value(status.url)')
echo "🌐 URL de l'API / WebSocket Orchestrateur : $BACKEND_URL"
echo "  - Discovery MCP   : $BACKEND_URL/api/mcp/tools"
echo "  - Chat Universel  : $BACKEND_URL/api/orchestrator/chat"
echo "  - WebSocket Live  : wss://${BACKEND_URL#https://}/ws/live"
echo "================================================================================"
