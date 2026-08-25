#!/usr/bin/env bash
# ==============================================================================
# Script de Configuration des Rôles et Droits IAM pour Talk to Data
# Projet GCP: data-agents-by-industry
# ==============================================================================

set -e

PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"data-agents-by-industry"}
USER_EMAIL="theophane@ericdjatsa.altostrat.com"
SA_NAME="talktodata-runner"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo "================================================================================"
echo "🛡️ Configuration Complète des Droits IAM - Talk to Data"
echo "  Projet GCP            : $PROJECT_ID"
echo "  Compte Développeur   : $USER_EMAIL"
echo "  Compte de Service SA  : $SA_EMAIL"
echo "================================================================================"

# 1. Vérifier / Créer le Compte de Service Dédié pour Cloud Run & MCP Toolbox
echo "1. Création du Service Account pour Cloud Run..."
if ! gcloud iam service-accounts describe "$SA_EMAIL" --project="$PROJECT_ID" >/dev/null 2>&1; then
    gcloud iam service-accounts create "$SA_NAME" \
        --display-name="TalkToData Runtime & MCP Runner" \
        --project="$PROJECT_ID"
    echo "✅ Service Account '$SA_EMAIL' créé avec succès."
else
    echo "ℹ️ Service Account '$SA_EMAIL' existe déjà."
fi

# 2. Rôles pour le Service Account d'exécution Cloud Run (Runtime)
echo "2. Attribution des rôles au Service Account ($SA_EMAIL)..."

SA_ROLES=(
    # BigQuery : Exécution des requêtes SQL et lecture des 11 datasets
    "roles/bigquery.admin"
    "roles/bigquery.jobUser"
    "roles/bigquery.dataViewer"

    # Vertex AI : Inférence LLM, Gemini Live et Conversational Analytics
    "roles/aiplatform.user"
    
    # Dataplex : Knowledge Catalog & Gouvernance
    "roles/dataplex.viewer"

    # Cloud Storage : Lecture des CVs PDF et images satellites Sentinel-2
    "roles/storage.objectViewer"

    # Observabilité : Cloud Logging et Cloud Monitoring
    "roles/logging.logWriter"
    "roles/monitoring.metricWriter"
)

for role in "${SA_ROLES[@]}"; do
    echo "  -> Ajout du rôle $role au Service Account..."
    gcloud projects add-iam-policy-binding "$PROJECT_ID" \
        --member="serviceAccount:${SA_EMAIL}" \
        --role="$role" \
        --condition=None >/dev/null
done

# 3. Rôles pour votre Compte Utilisateur / Développeur ($USER_EMAIL)
echo "3. Attribution des rôles d'administration au compte Développeur ($USER_EMAIL)..."

USER_ROLES=(
    # Droits de gestion IAM : Permet de donner des droits aux Service Accounts
    "roles/resourcemanager.projectIamAdmin"
    "roles/iam.serviceAccountUser"
    "roles/iam.serviceAccountAdmin"

    # Déploiement Cloud Run & Cloud Build
    "roles/run.admin"
    "roles/cloudbuild.builds.editor"
    "roles/artifactregistry.admin"

    # Vertex AI & Data Agents
    "roles/aiplatform.admin"
    "roles/aiplatform.user"

    # BigQuery & Stockage
    "roles/bigquery.admin"
    "roles/storage.admin"
    "roles/serviceusage.serviceUsageConsumer"
)

for role in "${USER_ROLES[@]}"; do
    echo "  -> Ajout du rôle $role à l'utilisateur..."
    gcloud projects add-iam-policy-binding "$PROJECT_ID" \
        --member="user:${USER_EMAIL}" \
        --role="$role" \
        --condition=None >/dev/null || echo "⚠️ L'attribution de $role nécessite les droits Owner/IAM Admin."
done

echo "================================================================================"
echo "✅ Configuration des rôles IAM terminée !"
echo "================================================================================"
