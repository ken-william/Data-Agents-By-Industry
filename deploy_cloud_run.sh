#!/usr/bin/env bash
# ==============================================================================
# One-Click Cloud Run Deployment for Talk to Data (ADK + MCP Toolbox + React UI)
# Project: data-agents-by-industry
# Region: europe-west9 (Paris) / europe-west1 (Belgium)
# ==============================================================================

set -e

PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"data-agents-by-industry"}
REGION=${REGION:-"us-central1"}
SERVICE_NAME="talktodata"

echo "================================================================================"
echo "🚀 Déploiement de Talk to Data sur Google Cloud Run"
echo "  Projet GCP : $PROJECT_ID"
echo "  Région     : $REGION"
echo "  Service    : $SERVICE_NAME"
echo "================================================================================"

# 1. Configurer gcloud
gcloud config set project "$PROJECT_ID"

# 2. Activer les APIs GCP nécessaires si pas déjà fait
echo "Activer les APIs Cloud Run, Cloud Build & Artifact Registry..."
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com

# 3. Déployer sur Cloud Run avec Cloud Build source-based build
echo "Construction de l'image et déploiement sur Cloud Run..."
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
echo "✅ Déploiement terminé avec succès !"
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region "$REGION" --format 'value(status.url)')
echo "🌐 URL Publique de l'application : $SERVICE_URL"
echo "================================================================================"
