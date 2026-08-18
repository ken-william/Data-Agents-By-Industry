#!/usr/bin/env python3
"""
Relational Data Generation and Enedis IRVE OpenData Processing for Helios (power_energy_ds).
Reads base CSV dataset 'agents/helios/data/enedis_bornes_irve.csv' to extract 10,000 authentic 
EV charging stations and builds 4 refined relational tables:
1. enedis_bornes_irve (Authentic Enedis IRVE station master)
2. enedis_consommation_inf36 (Transformer load telemetry horodated pas 30min)
3. enedis_production_renouvelable (Solar, Wind & Biomass generation capacity)
4. enedis_clients_industriels (B2B industrial consumer flexibilities)
"""

import os
import sys
import random
import subprocess
import pandas as pd
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "power_energy_ds"
LOCATION = "US"
BASE_CSV_PATH = "agents/helios/data/enedis_bornes_irve.csv"
BUCKET_NAME = "gs://talktodata-helios-raw-data"

CITY_DEPT_REGION = {
    "Paris": ("75 - Paris", "Île-de-France"),
    "Lyon": ("69 - Rhône", "Auvergne-Rhône-Alpes"),
    "Annecy": ("74 - Haute-Savoie", "Auvergne-Rhône-Alpes"),
    "Grenoble": ("38 - Isère", "Auvergne-Rhône-Alpes"),
    "Marseille": ("13 - Bouches-du-Rhône", "Provence-Alpes-Côte d'Azur"),
    "Nice": ("06 - Alpes-Maritimes", "Provence-Alpes-Côte d'Azur"),
    "Toulouse": ("31 - Haute-Garonne", "Occitanie"),
    "Montpellier": ("34 - Hérault", "Occitanie"),
    "Bordeaux": ("33 - Gironde", "Nouvelle-Aquitaine"),
    "Lille": ("59 - Nord", "Hauts-de-France"),
    "Strasbourg": ("67 - Bas-Rhin", "Grand Est"),
    "Nantes": ("44 - Loire-Atlantique", "Pays de la Loire"),
    "Rennes": ("35 - Ille-et-Vilaine", "Bretagne")
}

def get_client():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return bigquery.Client(project=PROJECT_ID, credentials=creds)

def parse_base_irve_csv():
    print(f"Parsing authentic Enedis IRVE base dataset: '{BASE_CSV_PATH}'...")
    if not os.path.exists(BASE_CSV_PATH):
        print(f"Error: Base CSV file '{BASE_CSV_PATH}' not found!")
        sys.exit(1)

    df_raw = pd.read_csv(BASE_CSV_PATH, low_memory=False)
    print(f"  ✓ Successfully parsed {len(df_raw)} raw Enedis IRVE station records.")

    clean_bornes = []
    for idx, row in df_raw.iterrows():
        st_id = str(row.get("id_station_itinerance")) if pd.notnull(row.get("id_station_itinerance")) else f"IRVE-ST-{idx+1:05d}"
        nom_st = str(row.get("nom_station")) if pd.notnull(row.get("nom_station")) else f"Station IRVE #{idx+1}"
        op = str(row.get("nom_operateur")) if pd.notnull(row.get("nom_operateur")) else "Freshmile France"
        amenageur = str(row.get("nom_amenageur")) if pd.notnull(row.get("nom_amenageur")) else "Enedis Mobility"
        addr = str(row.get("adresse_station")) if pd.notnull(row.get("adresse_station")) else "Adresse non spécifiée"
        commune = str(row.get("consolidated_commune")) if pd.notnull(row.get("consolidated_commune")) else "Paris"
        cp = str(row.get("consolidated_code_postal")) if pd.notnull(row.get("consolidated_code_postal")) else "75001"
        dept = str(row.get("departement")) if pd.notnull(row.get("departement")) else "75 - Paris"
        region = str(row.get("region")) if pd.notnull(row.get("region")) else "Île-de-France"
        
        # Format dept & region nicely if missing or raw number
        if dept in ["nan", ""] or not ("-" in dept):
            if commune in CITY_DEPT_REGION:
                dept, region = CITY_DEPT_REGION[commune]
            else:
                dept = "75 - Paris"
                region = "Île-de-France"

        pdc = int(row.get("nbre_pdc")) if pd.notnull(row.get("nbre_pdc")) else 2
        power = float(row.get("puissance_nominale")) if pd.notnull(row.get("puissance_nominale")) else 22.0
        combo = bool(row.get("prise_type_combo_ccs", False))
        t2 = bool(row.get("prise_type_2", True))
        d_service = str(row.get("date_mise_en_service"))[:10] if pd.notnull(row.get("date_mise_en_service")) else "2024-01-15"

        clean_bornes.append({
            "id_station_itinerance": st_id,
            "nom_station": nom_st,
            "nom_operateur": op,
            "nom_amenageur": amenageur,
            "adresse_station": addr,
            "commune": commune,
            "code_postal": cp,
            "code_departement": dept,
            "nom_region": region,
            "nbre_pdc": pdc,
            "puissance_nominale_kw": power,
            "prise_combo_ccs": combo,
            "prise_type_2": t2,
            "date_mise_en_service": d_service
        })

    return pd.DataFrame(clean_bornes)

def main():
    print(f"Initializing Refined Helios Relational Pipeline for project '{PROJECT_ID}'...")
    client = get_client()

    # Step 1: Read authentic Enedis IRVE dataset
    df_bornes = parse_base_irve_csv()
    print(f"  ✓ Processed {len(df_bornes)} clean Enedis IRVE stations.")

    # Step 2: Build enedis_consommation_inf36 (Linked to station IDs and communes)
    rows_consommation = []
    station_records = df_bornes.to_dict("records")

    for idx in range(1, 4001):
        st = random.choice(station_records)
        commune = st["commune"]
        dept = st["code_departement"]
        region = st["nom_region"]
        st_id = st["id_station_itinerance"]
        
        cap_max = float(random.choice([500, 800, 1000, 1200, 1500, 2000]))
        pic_kw = round(cap_max * random.uniform(0.40, 0.98), 1)
        charge_pct = round((pic_kw / cap_max) * 100.0, 1)

        risque = "Saturation / Disjonction Imminente 48h" if charge_pct > 88.0 else ("Sous Surveillance Forte" if charge_pct > 75.0 else "Normal")

        rows_consommation.append({
            "id_releve": f"REL-{idx:05d}",
            "id_station_itinerance": st_id,
            "commune": commune,
            "code_departement": dept,
            "nom_region": region,
            "nom_transformateur_quartier": f"TR-ENEDIS-{commune.upper()[:4]}-{idx:04d}",
            "horodate_pas30min": "2026-08-17 18:30:00 UTC",
            "consommation_totale_mwh": round(pic_kw * 0.03, 2),
            "pic_consommation_kw": pic_kw,
            "capacite_max_transformateur_kw": cap_max,
            "taux_charge_transformateur_pct": charge_pct,
            "risque_tension_reseau": risque
        })

    df_consommation = pd.DataFrame(rows_consommation)

    # Step 3: Build enedis_production_renouvelable
    rows_production = []
    for idx in range(1, 2001):
        st = random.choice(station_records)
        commune = st["commune"]
        dept = st["code_departement"]
        region = st["nom_region"]

        filiere = random.choice(["Solaire Photovoltaïque", "Éolien Terrestre", "Hydraulique", "Biomasse / Biogaz"])
        p_inst = round(random.uniform(50.0, 8500.0), 1)
        prod_mwh = round(p_inst * random.uniform(0.15, 0.42) * 24.0, 1)

        rows_production.append({
            "id_installation": f"PROD-ENEDIS-{idx:05d}",
            "commune": commune,
            "code_departement": dept,
            "nom_region": region,
            "filiere_energie": filiere,
            "puissance_installee_kw": p_inst,
            "production_journaliere_mwh": prod_mwh,
            "taux_injection_reseau_pct": round(random.uniform(85.0, 100.0), 1)
        })

    df_production = pd.DataFrame(rows_production)

    # Step 4: Build enedis_clients_industriels
    rows_industriels = []
    secteurs = ["Chimie & Pharmacie", "Métallurgie", "Agroalimentaire", "Automobile", "Data Centers"]
    
    for idx in range(1, 1001):
        st = random.choice(station_records)
        commune = st["commune"]
        dept = st["code_departement"]
        region = st["nom_region"]

        secteur = random.choice(secteurs)
        conso_annuelle = round(random.uniform(1200.0, 45000.0), 1)
        ef_score = round(random.uniform(0.12, 0.58), 3)

        rows_industriels.append({
            "id_client_indus": f"INDUS-{idx:05d}",
            "raison_sociale": f"Industrie {commune} #{idx}",
            "secteur_activite": secteur,
            "commune": commune,
            "code_departement": dept,
            "nom_region": region,
            "consommation_annuelle_mwh": conso_annuelle,
            "puissance_souscrite_kva": round(conso_annuelle / 4.2, 1),
            "empreinte_carbone_mwh_co2": round(conso_annuelle * ef_score, 2),
            "optin_flexibilite_effacement": random.choice([True, False])
        })

    df_industriels = pd.DataFrame(rows_industriels)

    # Save CSVs locally and upload to BigQuery & GCS
    tables_dict = {
        "enedis_bornes_irve": df_bornes,
        "enedis_consommation_inf36": df_consommation,
        "enedis_production_renouvelable": df_production,
        "enedis_clients_industriels": df_industriels
    }

    subprocess.run(f"gcloud storage buckets create {BUCKET_NAME} --project={PROJECT_ID} --location=EU 2>/dev/null", shell=True)

    for tname, df in tables_dict.items():
        csv_file = f"agents/helios/data/{tname}.csv"
        df.to_csv(csv_file, index=False)
        print(f"  ✓ Saved workspace CSV: {csv_file} ({len(df)} rows)")

        # Upload to GCS
        gcs_dest = f"{BUCKET_NAME}/{tname}.csv"
        subprocess.run(f"gcloud storage cp {csv_file} {gcs_dest}", shell=True, capture_output=True)

        # Load to BigQuery
        tref = f"{PROJECT_ID}.{DATASET_ID}.{tname}"
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
        )
        with open(csv_file, "rb") as f_in:
            job = client.load_table_from_file(f_in, tref, job_config=job_config)
        job.result()
        print(f"  ✓ Loaded table `{tref}` in BigQuery!")

    print("\nSUCCESS: Refined Helios data pipeline complete!")

if __name__ == "__main__":
    main()
