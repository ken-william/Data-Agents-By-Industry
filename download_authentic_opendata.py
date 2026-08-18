#!/usr/bin/env python3
"""
Downloads 100% REAL Open Data CSV datasets from official French Open Data endpoints
with robust column name sanitization for BigQuery and GCS.
"""

import os
import re
import sys
import subprocess
import urllib.request
import pandas as pd
from google.oauth2 import credentials
from google.cloud import bigquery

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
LOCATION = "EU"

REAL_DATA_SOURCES = {
    "transit_navigator": [
        {
            "filename": "frequentation_gares_sncf.csv",
            "table_name": "frequentation_gares_sncf",
            "url": "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/frequentation-gares/exports/csv?lang=fr&timezone=Europe%2FParis&use_labels=true&delimiter=%3B",
            "delimiter": ";"
        },
        {
            "filename": "sncf_regularite_lignes.csv",
            "table_name": "sncf_regularite_lignes",
            "url": "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/regularite-mensuelle-tgv-aqst/exports/csv?lang=fr&timezone=Europe%2FParis&use_labels=true&delimiter=%3B",
            "delimiter": ";"
        }
    ],
    "helios": [
        {
            "filename": "enedis_bornes_irve.csv",
            "table_name": "enedis_bornes_irve",
            "url": "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/bornes-irve/exports/csv?lang=fr&timezone=Europe%2FParis&use_labels=true&delimiter=%3B",
            "delimiter": ";"
        }
    ]
}

DATASET_MAPPING = {
    "credit_advisor": "fsi_creditadvisor_dataset",
    "shelf_optimizer": "retail_cpg_ds",
    "sully": "public_sector_employment_ds",
    "transit_navigator": "transport_mobility_ds",
    "earth_intel": "skywatch_aerospace_ds",
    "pulse_checker": "healthcare_pharma_ds",
    "net_arch": "telco_media_ds",
    "ceres": "agriculture_rurality_ds",
    "cine_analyst": "entertainment_cinema_ds",
    "arena_manager": "sports_infrastructure_ds",
    "helios": "power_energy_ds"
}

def sanitize_col(col):
    col = str(col).strip()
    col = col.replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a").replace("ô", "o").replace("ç", "c")
    col = col.replace("%", "pct").replace("+", "plus").replace(">", "gt").replace("<", "lt")
    col = re.sub(r'[^a-zA-Z0-9_]', '_', col)
    col = re.sub(r'_+', '_', col).strip('_')
    return col.lower()

def main():
    print(f"Downloading Authentic Open Data for project '{PROJECT_ID}'...")
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = credentials.Credentials(token)
    client = bigquery.Client(project=PROJECT_ID, credentials=creds)

    for agent_name, sources in REAL_DATA_SOURCES.items():
        dataset_id = DATASET_MAPPING[agent_name]
        data_dir = f"agents/{agent_name}/data"
        bucket_name = f"gs://talktodata-{agent_name.replace('_', '-')}-raw-data"
        os.makedirs(data_dir, exist_ok=True)

        for src in sources:
            fname = src["filename"]
            tname = src["table_name"]
            url = src["url"]
            delim = src.get("delimiter", ";")
            local_csv = f"{data_dir}/{fname}"

            print(f"\n[+] Fetching authentic Open Data: {fname}...")
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response, open(local_csv, 'wb') as out_file:
                    out_file.write(response.read())

                df = pd.read_csv(local_csv, sep=delim, low_memory=False)
                df.columns = [sanitize_col(c) for c in df.columns]
                df.to_csv(local_csv, index=False)
                print(f"  ✓ Saved & sanitized local CSV: {local_csv} ({len(df)} rows, {len(df.columns)} cols)")

                # Upload to GCS
                gcs_dest = f"{bucket_name}/{fname}"
                subprocess.run(f"gcloud storage cp {local_csv} {gcs_dest}", shell=True, capture_output=True)
                print(f"  ✓ Uploaded to GCS: {gcs_dest}")

                # Load into BigQuery
                table_ref = f"{PROJECT_ID}.{dataset_id}.{tname}"
                job_config = bigquery.LoadJobConfig(
                    source_format=bigquery.SourceFormat.CSV,
                    skip_leading_rows=1,
                    autodetect=True,
                    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
                )
                with open(local_csv, "rb") as source_file:
                    job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
                job.result()
                print(f"  ✓ Successfully loaded into BigQuery: `{dataset_id}.{tname}`")

            except Exception as e:
                print(f"  ❌ Error processing {fname}: {e}")

    print("\nSUCCESS: All authentic Open Data tables loaded into BigQuery & GCS successfully!")

if __name__ == "__main__":
    main()
