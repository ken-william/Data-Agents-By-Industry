# TalkToData: Deployment & Operational Guide

This document provides step-by-step instructions for deploying, updating, and verifying the TalkToData multi-agent system on Google Cloud Platform (GCP).

---

## 1. Environment Setup

### System Prerequisites
* Operating System: Linux / macOS
* Python Version: 3.10 or higher
* Google Cloud SDK (`gcloud` CLI)
* Access to a GCP project with the following APIs enabled:
  * `bigquery.googleapis.com`
  * `storage.googleapis.com`
  * `geminidataanalytics.googleapis.com`

### Authenticate GCP Credentials
Run the following commands to authenticate your user session and Application Default Credentials (ADC):

```bash
# 1. Login with user credentials
gcloud auth login

# 2. Login Application Default Credentials for Python SDKs
gcloud auth application-default login

# 3. Configure target GCP Project ID
export GOOGLE_CLOUD_PROJECT="data-agents-by-industry"
gcloud config set project $GOOGLE_CLOUD_PROJECT
```

---

## 2. Automated One-Click Deployment

To deploy all 11 industry agents, BigQuery datasets, GCS buckets, and authentic Open Data sources, run:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run master deployment script
python deploy_all.py
```

### Expected Terminal Output

```text
================================================================================
 TalkToData: Multi-Agent Enterprise Data Analytics System Deployment
 Target Project: data-agents-by-industry
================================================================================

Checking environment for project 'data-agents-by-industry'...
  GCP Authentication verified successfully.

[Step 1/3] Fetching authentic Open Data sources...
  Saved & sanitized local CSV: agents/transit_navigator/data/frequentation_gares_sncf.csv
  Uploaded to GCS: gs://talktodata-transit-navigator-raw-data/frequentation_gares_sncf.csv
  Uploaded to GCS: gs://talktodata-helios-raw-data/enedis_bornes_irve.csv

[Step 2/3] Initializing BigQuery schemas, data pipelines and GCS storage...
--- Processing Agent: FSI & Financial Risk Advisor (credit_advisor) ---
  Applying DDL schema for `fsi_creditadvisor_dataset`...
  Executing relational data pipeline: agents/credit_advisor/generate_data.py...

--- Processing Agent: Agriculture & Agroecological Transition (ceres) ---
  Applying DDL schema for `agriculture_rurality_ds`...
  Executing relational data pipeline: agents/ceres/generate_data.py...

[Step 3/3] Deploying Data Analytics Agents to GCP Vertex AI Data Agents API...
  Deploying agent payload: credit_advisor...
  Deploying agent payload: ceres...

================================================================================
 DEPLOYMENT COMPLETE
 Total Execution Time: 42.5 seconds
================================================================================

Agent ID             | Industry / Title                           | BigQuery Dataset             | Status    
----------------------------------------------------------------------------------------------------------
credit_advisor       | FSI & Financial Risk Advisor               | fsi_creditadvisor_dataset    | DEPLOYED  
shelf_optimizer      | Retail CPG & Shelf Optimizer               | retail_cpg_ds                | DEPLOYED  
sully                | Public Sector Employment & Labor           | public_sector_employment_ds  | DEPLOYED  
transit_navigator    | Transport & Mobility Intelligence          | transport_mobility_ds        | DEPLOYED  
earth_intel          | Skywatch Satellite Observation             | skywatch_aerospace_ds        | DEPLOYED  
pulse_checker        | Healthcare & Pharma Analytics              | healthcare_pharma_ds         | DEPLOYED  
net_arch             | Telco & Media Network Operations           | telco_media_ds               | DEPLOYED  
ceres                | Agriculture & Agroecological Transition    | agriculture_rurality_ds      | DEPLOYED  
cine_analyst         | Entertainment & Cinema Box Office          | entertainment_cinema_ds      | DEPLOYED  
arena_manager        | Sports & Infrastructure Analytics          | sports_infrastructure_ds     | DEPLOYED  
helios               | Power, Energy & EV Infrastructure          | power_energy_ds              | DEPLOYED  
```

---

## 3. Individual Agent Deployment

If you make modifications to a single agent (e.g., `ceres`), you can deploy or update that specific agent independently:

```bash
# 1. Update schema or data for Ceres
python agents/ceres/generate_data.py

# 2. Deploy updated agent payload to Vertex AI
python agents/ceres/deploy_agent.py
```

---

## 4. Verification & Testing

### Test BigQuery Query Execution

Run a test query on BigQuery to verify table availability:

```bash
bq query --use_legacy_sql=false \
  --project_id=$GOOGLE_CLOUD_PROJECT \
  "SELECT c.nom_cooperative, m.baisse_rendement_predite_pct \
   FROM \`$GOOGLE_CLOUD_PROJECT.agriculture_rurality_ds.cooperatives_agricoles\` c \
   JOIN \`$GOOGLE_CLOUD_PROJECT.agriculture_rurality_ds.previsions_anomalies_meteo_ete\` m \
   ON c.code_departement = m.code_departement \
   WHERE m.baisse_rendement_predite_pct > 20.0"
```

### Test Cloud Storage Storage Buckets

Verify that Cloud Storage dedicated buckets are populated with authentic CSV files:

```bash
gcloud storage ls "gs://talktodata-*-raw-data/**"
```
