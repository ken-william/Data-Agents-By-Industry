#!/usr/bin/env bash
# ==============================================================================
# Talk to Data - Cloud Run Deployment Script (us-central1)
# ==============================================================================

PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"data-agents-by-industry"}
REGION="us-central1"
SERVICE_NAME="talktodata-app"

echo "================================================================================"
echo " Deploying Talk to Data to GCP Cloud Run in region '$REGION'"
echo " GCP Project: $PROJECT_ID"
echo "================================================================================"

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$BASE_DIR"

# Build frontend production dist
echo "1. Building frontend production assets..."
cd frontend && npx vite build && cd ..

# Deploy to Cloud Run using gcloud source deploy
echo "2. Deploying to Cloud Run in $REGION..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --project $PROJECT_ID \
  --allow-unauthenticated \
  --platform managed \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID

echo "================================================================================"
echo " Cloud Run Deployment Complete!"
echo " Service URL: https://$SERVICE_NAME-uc.a.run.app"
echo "================================================================================"
