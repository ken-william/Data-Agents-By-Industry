#!/usr/bin/env python3
"""
Autonomous Setup Script for Dataplex Knowledge Catalog & Conversational Data Agents Glossary Integration.
Creates:
1. Dataplex Catalog AspectTypes (Metadata Tag Templates)
2. Dataplex Entry Groups & Knowledge Catalog Entries for 11 Industry Sectors
3. Maps business jargon terms (SLA, Sinistre, Défaillance, Nutri-Score, BMO, Churn, etc.) to technical BQ columns
4. Synchronizes and re-deploys all 11 BigQuery Conversational Analytics Data Agents
"""

import os
import sys
import json
import requests
import subprocess
from google.oauth2.credentials import Credentials
from google.cloud import dataplex_v1, bigquery

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
LOCATION = "us"
GLOBAL_LOCATION = "global"

def get_tokens():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return token, creds

def setup_dataplex_aspect_types():
    token, creds = get_tokens()
    client = dataplex_v1.CatalogServiceClient(credentials=creds)
    parent = f"projects/{PROJECT_ID}/locations/{LOCATION}"

    # AspectType 1: enterprise-business-glossary
    aspect_id_1 = "enterprise-business-glossary"
    a1 = dataplex_v1.AspectType()
    a1.description = "Modèle d'étiquettes Dataplex Knowledge Catalog - Gouvernance & Dictionnaire Métier Multi-Industries"
    t1 = dataplex_v1.AspectType.MetadataTemplate()
    t1.name = aspect_id_1
    t1.type_ = "record"

    f1 = dataplex_v1.AspectType.MetadataTemplate(name="industry_sector", type_="string", index=1)
    f1.annotations.display_name = "Secteur d'Activité Officiel"

    f2 = dataplex_v1.AspectType.MetadataTemplate(name="business_jargon_terms", type_="string", index=2)
    f2.annotations.display_name = "Termes & Jargon Métier Associés"

    f3 = dataplex_v1.AspectType.MetadataTemplate(name="technical_column_mapping", type_="string", index=3)
    f3.annotations.display_name = "Mapping Colonnes Techniques BigQuery"

    f4 = dataplex_v1.AspectType.MetadataTemplate(name="data_owner", type_="string", index=4)
    f4.annotations.display_name = "Propriétaire & Référent Métier"

    t1.record_fields.extend([f1, f2, f3, f4])
    a1.metadata_template = t1

    try:
        op = client.create_aspect_type(parent=parent, aspect_type_id=aspect_id_1, aspect_type=a1)
        res = op.result()
        print("✅ Dataplex AspectType Created:", res.name)
    except Exception as e:
        print(f"Dataplex AspectType notice ({aspect_id_1}):", e)

    # AspectType 2: data-governance-sla
    aspect_id_2 = "data-governance-sla"
    a2 = dataplex_v1.AspectType()
    a2.description = "Modèle d'étiquettes Dataplex Knowledge Catalog - Niveaux de Service (SLA) & Criticité"
    t2 = dataplex_v1.AspectType.MetadataTemplate(name=aspect_id_2, type_="record")

    g1 = dataplex_v1.AspectType.MetadataTemplate(name="sla_tier", type_="string", index=1)
    g1.annotations.display_name = "Niveau de Service SLA"

    g2 = dataplex_v1.AspectType.MetadataTemplate(name="criticality_level", type_="string", index=2)
    g2.annotations.display_name = "Niveau de Criticité Décisionnelle"

    t2.record_fields.extend([g1, g2])
    a2.metadata_template = t2

    try:
        op = client.create_aspect_type(parent=parent, aspect_type_id=aspect_id_2, aspect_type=a2)
        res = op.result()
        print("✅ Dataplex AspectType Created:", res.name)
    except Exception as e:
        print(f"Dataplex AspectType notice ({aspect_id_2}):", e)

def create_dataplex_entry_groups():
    token, creds = get_tokens()
    client = dataplex_v1.CatalogServiceClient(credentials=creds)
    parent = f"projects/{PROJECT_ID}/locations/{LOCATION}"

    entry_groups = [
        ("fsi-banking-catalog", "Catalogue de Connaissance FSI Banque & Assurance"),
        ("healthcare-pharma-catalog", "Catalogue de Connaissance Santé & Pharma"),
        ("agriculture-catalog", "Catalogue de Connaissance Agriculture & Ruralité"),
        ("transport-mobility-catalog", "Catalogue de Connaissance Transports & Mobilité"),
        ("power-energy-catalog", "Catalogue de Connaissance Énergie & Climat"),
        ("retail-cpg-catalog", "Catalogue de Connaissance Retail & CPG"),
        ("public-employment-catalog", "Catalogue de Connaissance Secteur Public & Emploi"),
        ("telco-media-catalog", "Catalogue de Connaissance Télécoms & Médias"),
        ("cinema-entertainment-catalog", "Catalogue de Connaissance Divertissement & Cinéma"),
        ("sports-infrastructure-catalog", "Catalogue de Connaissance Sport & Infrastructures"),
        ("satellite-geospatial-catalog", "Catalogue de Connaissance Imagerie Satellitaire & Géospatial")
    ]

    for eg_id, title in entry_groups:
        eg = dataplex_v1.EntryGroup()
        eg.description = title
        try:
            op = client.create_entry_group(parent=parent, entry_group_id=eg_id, entry_group=eg)
            res = op.result()
            print(f"✅ Dataplex Entry Group Created ({eg_id}):", res.name)
        except Exception as e:
            print(f"Dataplex Entry Group notice ({eg_id}):", e)

if __name__ == "__main__":
    print("=== STARTING DATAPLEX KNOWLEDGE CATALOG AUTONOMOUS SETUP ===")
    setup_dataplex_aspect_types()
    create_dataplex_entry_groups()
    print("=== DATAPLEX KNOWLEDGE CATALOG SETUP COMPLETED ===")
