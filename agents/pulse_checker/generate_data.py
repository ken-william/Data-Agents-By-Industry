#!/usr/bin/env python3
"""
Relational Data Generation and Official FINESS OpenData Processing for PulseChecker (healthcare_medical_ds).
Fetches authentic FINESS French Hospitals dataset from data.gouv.fr API
and builds 5 refined relational tables:
1. finess_etablissements_sante (Official FINESS French Hospitals, CHUs & Clinics)
2. hopitaux_flux_admissions_urgences (Emergency Room admissions, wait times & Plan Blanc)
3. hopitaux_blocs_operatoires_chirurgie (Surgical operating rooms & ICU capacity)
4. pharmacie_stock_medicaments_tension (Hospital pharmacy critical drug shortages)
5. personnel_medical_garde_planning (Medical staff on-call duty & absenteeism)
"""

import os
import sys
import random
import subprocess
import pandas as pd
import requests
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "healthcare_medical_ds"
LOCATION = "US"
FINESS_CSV_URL = "https://www.data.gouv.fr/api/1/datasets/r/56d56d07-1f41-47e0-8a01-836a34dab232"
LOCAL_CSV_PATH = "agents/pulse_checker/data/finess_etablissements_sante.csv"
BUCKET_NAME = "gs://talktodata-pulse-checker-raw-data"

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

def parse_float(val, default=0.0):
    if pd.isnull(val):
        return default
    try:
        return float(str(val).replace(',', '.').strip())
    except ValueError:
        return default

def fetch_and_clean_finess_hospitals():
    print(f"Fetching official FINESS French Hospitals dataset from '{FINESS_CSV_URL}'...")
    try:
        df_raw = pd.read_csv(FINESS_CSV_URL, nrows=5000, low_memory=False)
        print(f"  ✓ Downloaded {len(df_raw)} authentic FINESS hospital records.")
    except Exception as e:
        print(f"  Warning: Live FINESS fetch error ({e}). Checking local workspace fallback...")
        if os.path.exists(LOCAL_CSV_PATH):
            df_raw = pd.read_csv(LOCAL_CSV_PATH, low_memory=False)
        else:
            raise e

    clean_hospitals = []
    for idx, row in df_raw.iterrows():
        finess_id = str(row.get("finess_et")) if pd.notnull(row.get("finess_et")) else f"FIN-{idx+1:08d}"
        nom = str(row.get("rs")) if pd.notnull(row.get("rs")) else f"Centre Hospitalier #{idx+1}"
        cat = str(row.get("libcategetab")) if pd.notnull(row.get("libcategetab")) else "Centre Hospitalier Général"
        commune = str(row.get("ville")) if pd.notnull(row.get("ville")) else "Paris"
        cp = str(row.get("code_postal")) if pd.notnull(row.get("code_postal")) else "75001"
        
        # Ensure dept & region
        if commune in CITY_DEPT_REGION:
            dept, region = CITY_DEPT_REGION[commune]
        else:
            dept = f"{str(cp)[:2]} - Département {str(cp)[:2]}"
            region = "Île-de-France"

        cap_lits = int(parse_float(row.get("capacité_totale"), 250))
        cap_lits = max(40, min(2200, cap_lits))
        cap_rea = max(8, int(cap_lits * 0.08))
        cap_urg = max(12, int(cap_lits * 0.12))

        lat = parse_float(row.get("latitude"), 48.8566)
        lon = parse_float(row.get("longitude"), 2.3522)

        clean_hospitals.append({
            "id_finess_etablissement": finess_id,
            "nom_etablissement": nom,
            "categorie_etablissement": cat,
            "commune": commune,
            "code_postal": str(cp)[:5],
            "code_departement": dept,
            "nom_region": region,
            "capacite_totale_lits": cap_lits,
            "capacite_lits_reanimation": cap_rea,
            "capacite_lits_urgences": cap_urg,
            "latitude": lat,
            "longitude": lon
        })

    return pd.DataFrame(clean_hospitals)

def main():
    print(f"Initializing Refined PulseChecker Relational Pipeline for project '{PROJECT_ID}'...")
    client = get_client()

    os.makedirs("agents/pulse_checker/data", exist_ok=True)

    # 1. finess_etablissements_sante
    df_hospitals = fetch_and_clean_finess_hospitals()
    print(f"  ✓ Processed {len(df_hospitals)} clean FINESS hospital records.")

    # 2. hopitaux_flux_admissions_urgences
    rows_urgences = []
    hosp_records = df_hospitals.to_dict("records")

    for idx in range(1, 4001):
        h = random.choice(hosp_records)
        admissions = random.randint(12, 85)
        attente_min = random.randint(35, 340)
        taux_occ = round(random.uniform(45.0, 142.0), 1)

        statut = "TENSION_EXTREME_PLAN_BLANC" if taux_occ > 110.0 else ("SOUS_TENSION" if taux_occ > 85.0 else "NORMAL")

        rows_urgences.append({
            "id_releve_urgences": f"URG-{idx:05d}",
            "id_finess_etablissement": h["id_finess_etablissement"],
            "nom_etablissement": h["nom_etablissement"],
            "commune": h["commune"],
            "code_departement": h["code_departement"],
            "nom_region": h["nom_region"],
            "horodate_pas_1heure": "2026-08-17 19:00:00 UTC",
            "nombre_admissions_heure": admissions,
            "temps_attente_moyen_minutes": attente_min,
            "taux_occupation_lits_urgences_pct": taux_occ,
            "statut_tension_urgences": statut
        })

    df_urgences = pd.DataFrame(rows_urgences)

    # 3. hopitaux_blocs_operatoires_chirurgie
    rows_blocs = []
    specialites = ["Chirurgie Viscérale & Digestive", "Orthopédie & Traumatologie", "Neurologie & Neurochirurgie", "Cardiologie Interventionnelle", "Oncologie Chirurgicale"]

    for idx in range(1, 1501):
        h = random.choice(hosp_records)
        spec = random.choice(specialites)
        salles = random.randint(4, 18)
        taux_bloc = round(random.uniform(60.0, 98.5), 1)
        prog = random.randint(25, 120)
        urg = random.randint(4, 35)
        delai_jours = random.randint(2, 45)

        rows_blocs.append({
            "id_bloc_operatoire": f"BLOC-{idx:04d}",
            "id_finess_etablissement": h["id_finess_etablissement"],
            "nom_etablissement": h["nom_etablissement"],
            "specialite_chirurgicale": spec,
            "nombre_salles_operatoires": salles,
            "taux_utilisation_bloc_pct": taux_bloc,
            "nombre_interventions_programmees": prog,
            "nombre_interventions_urgentes": urg,
            "delai_moyen_attente_chirurgie_jours": delai_jours
        })

    df_blocs = pd.DataFrame(rows_blocs)

    # 4. pharmacie_stock_medicaments_tension
    rows_pharmacie = []
    substances = [
        ("3400930012345", "Amoxicilline 1g"),
        ("3400930056789", "Paracétamol Injectable IV 10mg/ml"),
        ("3400930099999", "Insuline Rapide 100 UI/ml"),
        ("3400930088888", "Propofol Émulsion IV"),
        ("3400930077777", "Morphine Sulfate 10mg"),
        ("3400930066666", "Cefotaxime 1g Poudre Solution")
    ]

    for idx in range(1, 2501):
        h = random.choice(hosp_records)
        cip, substance = random.choice(substances)
        doses = random.randint(50, 8500)
        autonomie_j = random.randint(1, 45)

        statut_app = "RUPTURE_AVEREE_CRITIQUE" if autonomie_j <= 3 else ("REAPPROVISIONNEMENT_TENDU" if autonomie_j <= 10 else "STOCK_CONFORME")

        rows_pharmacie.append({
            "id_medicament": f"MED-{idx:05d}",
            "id_finess_etablissement": h["id_finess_etablissement"],
            "nom_etablissement": h["nom_etablissement"],
            "code_cip13": cip,
            "nom_substance_active": substance,
            "quantite_en_stock_doses": doses,
            "jours_autonomie_restants": autonomie_j,
            "statut_approvisionnement": statut_app
        })

    df_pharmacie = pd.DataFrame(rows_pharmacie)

    # 5. personnel_medical_garde_planning
    rows_personnel = []
    categories = ["Médecins Urgentistes", "Anesthésistes Réanimateurs", "Infirmiers IDE", "Aides-Soignants"]

    for idx in range(1, 2001):
        h = random.choice(hosp_records)
        cat = random.choice(categories)
        req = random.randint(8, 45)
        pres = random.randint(int(req * 0.60), req)
        absent_pct = round(((req - pres) / req) * 100.0, 1)
        heures_sup = round(random.uniform(4.0, 22.5), 1)

        statut_g = "SOUS_EFFECTIF_SEVERE" if absent_pct > 20.0 else "GARDE_CONFORME"

        rows_personnel.append({
            "id_planning": f"PLN-{idx:05d}",
            "id_finess_etablissement": h["id_finess_etablissement"],
            "nom_etablissement": h["nom_etablissement"],
            "categorie_personnel": cat,
            "effectif_present": pres,
            "effectif_requis_h24": req,
            "taux_absenteisme_pct": absent_pct,
            "nombre_heures_supplementaires_semaine": heures_sup,
            "statut_garde": statut_g
        })

    df_personnel = pd.DataFrame(rows_personnel)

    # Save CSVs locally and upload to BigQuery & GCS
    tables_dict = {
        "finess_etablissements_sante": df_hospitals,
        "hopitaux_flux_admissions_urgences": df_urgences,
        "hopitaux_blocs_operatoires_chirurgie": df_blocs,
        "pharmacie_stock_medicaments_tension": df_pharmacie,
        "personnel_medical_garde_planning": df_personnel
    }

    subprocess.run(f"gcloud storage buckets create {BUCKET_NAME} --project={PROJECT_ID} --location=EU 2>/dev/null", shell=True)

    for tname, df in tables_dict.items():
        csv_file = f"agents/pulse_checker/data/{tname}.csv"
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

    print("\nSUCCESS: All 5 PulseChecker tables complete & populated in BigQuery!")

if __name__ == "__main__":
    main()
