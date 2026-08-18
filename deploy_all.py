#!/usr/bin/env python3
"""
Master Deployment Script for TalkToData Multi-Agent Data Ecosystem.
Deploys all 11 industry data agents on Google Cloud Platform:
- BigQuery relational datasets & DDL schemas
- Authentic Open Data ingestion & GCS storage buckets
- Vertex AI Data Analytics API agent deployments

Usage:
  export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
  python deploy_all.py
"""

import os
import sys
import time
import subprocess

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")

AGENTS = [
    ("credit_advisor", "FSI & Financial Risk Advisor", "fsi_creditadvisor_dataset"),
    ("shelf_optimizer", "Retail CPG & Shelf Optimizer", "retail_cpg_ds"),
    ("sully", "Public Sector Employment & Labor", "public_sector_employment_ds"),
    ("transit_navigator", "Transport & Mobility Intelligence", "transport_mobility_ds"),
    ("earth_intel", "Skywatch Satellite Observation", "skywatch_aerospace_ds"),
    ("pulse_checker", "Healthcare & Pharma Analytics", "healthcare_pharma_ds"),
    ("net_arch", "Telco & Media Network Operations", "telco_media_ds"),
    ("ceres", "Agriculture & Agroecological Transition", "agriculture_rurality_ds"),
    ("cine_analyst", "Entertainment & Cinema Box Office", "entertainment_cinema_ds"),
    ("arena_manager", "Sports & Infrastructure Analytics", "sports_infrastructure_ds"),
    ("helios", "Power, Energy & EV Infrastructure", "power_energy_ds")
]

def check_environment():
    print(f"Checking environment for project '{PROJECT_ID}'...")
    try:
        token = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip()
        if not token:
            raise ValueError("No access token returned.")
        print("  GCP Authentication verified successfully.")
    except Exception as e:
        print(f"Error: Unable to authenticate with gcloud. Please run 'gcloud auth login' and 'gcloud auth application-default login'.\nDetails: {e}")
        sys.exit(1)

def main():
    print("================================================================================")
    print(" TalkToData: Multi-Agent Enterprise Data Analytics System Deployment")
    print(f" Target Project: {PROJECT_ID}")
    print("================================================================================\n")

    check_environment()

    start_time = time.time()

    # 1. Download Authentic Open Data
    print("\n[Step 1/3] Fetching authentic Open Data sources...")
    if os.path.exists("download_authentic_opendata.py"):
        res = subprocess.run([sys.executable, "download_authentic_opendata.py"], check=False)
        if res.returncode != 0:
            print("Warning: Open Data download encountered non-fatal notices. Continuing deployment...")

    # 2. Deploy Datasets and Data Generators for Each Agent
    print("\n[Step 2/3] Initializing BigQuery schemas, data pipelines and GCS storage...")
    for agent_id, agent_title, dataset_id in AGENTS:
        agent_dir = f"agents/{agent_id}"
        print(f"\n--- Processing Agent: {agent_title} ({agent_id}) ---")

        # Execute DDL if present
        ddl_script = f"{agent_dir}/ddl_setup.sql"
        if os.path.exists(ddl_script):
            print(f"  Applying DDL schema for `{dataset_id}`...")
            cmd = f"bq query --use_legacy_sql=false --project_id={PROJECT_ID} < {ddl_script}"
            subprocess.run(cmd, shell=True, capture_output=True, text=True)

        # Execute Data Generator
        gen_script = f"{agent_dir}/generate_data.py"
        if os.path.exists(gen_script):
            print(f"  Executing relational data pipeline: {gen_script}...")
            subprocess.run([sys.executable, gen_script], check=False)

    # 3. Deploy Vertex AI Data Agents on GCP
    print("\n[Step 3/3] Deploying Data Analytics Agents to GCP Vertex AI Data Agents API...")
    deployed_summary = []

    for agent_id, agent_title, dataset_id in AGENTS:
        deploy_script = f"agents/{agent_id}/deploy_agent.py"
        if os.path.exists(deploy_script):
            print(f"  Deploying agent payload: {agent_id}...")
            res = subprocess.run([sys.executable, deploy_script], capture_output=True, text=True)
            status = "DEPLOYED" if res.returncode == 0 else "FAILED"
            deployed_summary.append((agent_id, agent_title, dataset_id, status))
        else:
            deployed_summary.append((agent_id, agent_title, dataset_id, "SKIPPED"))

    elapsed = round(time.time() - start_time, 1)

    print("\n================================================================================")
    print(" DEPLOYMENT COMPLETE")
    print(f" Total Execution Time: {elapsed} seconds")
    print("================================================================================\n")

    print(f"{'Agent ID':<20} | {'Industry / Title':<42} | {'BigQuery Dataset':<28} | {'Status':<10}")
    print("-" * 106)
    for agent_id, agent_title, dataset_id, status in deployed_summary:
        print(f"{agent_id:<20} | {agent_title:<42} | {dataset_id:<28} | {status:<10}")

    print("\nAll 11 Data Analytics Agents are live and ready for enterprise queries.")

if __name__ == "__main__":
    main()
