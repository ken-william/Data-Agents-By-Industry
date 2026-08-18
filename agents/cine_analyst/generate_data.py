#!/usr/bin/env python3
"""
Relational Data Generation and CNC Cinema OpenData Processing for CineAnalyst (entertainment_cinema_ds).
Reads base Excel dataset 'agents/cine_analyst/data/Fréquentation et films dans les salles de cinéma.xlsx'
and builds 5 refined relational tables:
1. cnc_frequentation_historique (Historical annual attendance, box-office revenue & ticket price)
2. cnc_films_exploitation_nationalite (Films in distribution by nationality: French, US, European)
3. cnc_films_nouveautes_genres (First-run releases by genre: Fiction, Documentary, Animation)
4. cnc_performance_box_office_tops (Admissions of Top 10, Top 20, Top 30, Top 100 films)
5. salles_cinema_etablissements (Cinema theater circuits & multiplexes with strict geography)
"""

import os
import sys
import random
import subprocess
import pandas as pd
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "entertainment_cinema_ds"
LOCATION = "US"
EXCEL_PATH = "agents/cine_analyst/data/Fréquentation et films dans les salles de cinéma.xlsx"
BUCKET_NAME = "gs://talktodata-cine-analyst-raw-data"

CITY_DEPT_REGION = {
    "Paris": ("75 - Paris", "Île-de-France"),
    "Lyon": ("69 - Rhône", "Auvergne-Rhône-Alpes"),
    "Marseille": ("13 - Bouches-du-Rhône", "Provence-Alpes-Côte d'Azur"),
    "Toulouse": ("31 - Haute-Garonne", "Occitanie"),
    "Bordeaux": ("33 - Gironde", "Nouvelle-Aquitaine"),
    "Lille": ("59 - Nord", "Hauts-de-France"),
    "Strasbourg": ("67 - Bas-Rhin", "Grand Est"),
    "Nantes": ("44 - Loire-Atlantique", "Pays de la Loire"),
    "Rennes": ("35 - Ille-et-Vilaine", "Bretagne"),
    "Nice": ("06 - Alpes-Maritimes", "Provence-Alpes-Côte d'Azur"),
    "Montpellier": ("34 - Hérault", "Occitanie"),
    "Annecy": ("74 - Haute-Savoie", "Auvergne-Rhône-Alpes")
}

CIRCUITS_CINEMA = [
    ("Pathé Gaumont", [12, 16, 20], [1800, 2400, 3200]),
    ("UGC Ciné Cité", [10, 14, 18], [1500, 2100, 2800]),
    ("CGR Cinémas", [8, 12, 15], [1200, 1700, 2300]),
    ("MK2", [5, 8, 11], [600, 950, 1400]),
    ("Kinepolis", [12, 14, 16], [2200, 2600, 3100]),
    ("Cinéma Indépendant Art & Essai", [2, 3, 4], [250, 450, 650])
]

def get_client():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return bigquery.Client(project=PROJECT_ID, credentials=creds)

def parse_cnc_excel():
    print(f"Parsing official CNC Cinema base dataset: '{EXCEL_PATH}'...")
    if not os.path.exists(EXCEL_PATH):
        print(f"Error: Excel file '{EXCEL_PATH}' not found!")
        sys.exit(1)

    # 1. Sheet freqciné
    df_freq = pd.read_excel(EXCEL_PATH, sheet_name='freqciné', skiprows=5)
    df_freq.columns = ['annee', 'blank', 'entrees_totales', 'recette_totale_eur', 'prix_moyen_ticket_eur']
    df_freq = df_freq[['annee', 'entrees_totales', 'recette_totale_eur', 'prix_moyen_ticket_eur']].dropna(subset=['annee'])
    df_freq['annee'] = pd.to_numeric(df_freq['annee'], errors='coerce')
    df_freq = df_freq.dropna(subset=['annee']).astype({'annee': int})
    df_freq['entrees_totales'] = pd.to_numeric(df_freq['entrees_totales'], errors='coerce').fillna(0).astype(int)
    df_freq['recette_totale_eur'] = pd.to_numeric(df_freq['recette_totale_eur'], errors='coerce').fillna(0.0)
    df_freq['prix_moyen_ticket_eur'] = pd.to_numeric(df_freq['prix_moyen_ticket_eur'], errors='coerce').fillna(0.0)

    # 2. Sheet filmexpl
    df_expl = pd.read_excel(EXCEL_PATH, sheet_name='filmexpl', skiprows=5)
    df_expl.columns = ['annee', 'films_francais', 'films_americains', 'films_europeens', 'autres_films', 'total_films']
    df_expl = df_expl.dropna(subset=['annee'])
    df_expl['annee'] = pd.to_numeric(df_expl['annee'], errors='coerce')
    df_expl = df_expl.dropna(subset=['annee']).astype({'annee': int})
    for col in ['films_francais', 'films_americains', 'films_europeens', 'autres_films', 'total_films']:
        df_expl[col] = pd.to_numeric(df_expl[col], errors='coerce').fillna(0)

    # 3. Sheet genre sortie1
    df_genre = pd.read_excel(EXCEL_PATH, sheet_name='genre sortie1', skiprows=5)
    df_genre.columns = ['annee', 'films_fiction', 'films_documentaire', 'films_animation', 'total_nouveautes']
    df_genre = df_genre.dropna(subset=['annee'])
    df_genre['annee'] = pd.to_numeric(df_genre['annee'], errors='coerce')
    df_genre = df_genre.dropna(subset=['annee']).astype({'annee': int})
    for col in ['films_fiction', 'films_documentaire', 'films_animation', 'total_nouveautes']:
        df_genre[col] = pd.to_numeric(df_genre[col], errors='coerce').fillna(0)

    # 4. Sheet perform
    df_perf = pd.read_excel(EXCEL_PATH, sheet_name='perform', skiprows=5)
    df_perf.columns = ['annee', 'top_10_entrees', 'top_20_entrees', 'top_30_entrees', 'top_100_entrees']
    df_perf = df_perf.dropna(subset=['annee'])
    df_perf['annee'] = pd.to_numeric(df_perf['annee'], errors='coerce')
    df_perf = df_perf.dropna(subset=['annee']).astype({'annee': int})
    for col in ['top_10_entrees', 'top_20_entrees', 'top_30_entrees', 'top_100_entrees']:
        df_perf[col] = pd.to_numeric(df_perf[col], errors='coerce').fillna(0).astype(int)

    return df_freq, df_expl, df_genre, df_perf

def main():
    print(f"Initializing CineAnalyst Relational Pipeline for project '{PROJECT_ID}'...")
    client = get_client()

    # Step 1: Read authentic CNC Excel
    df_freq, df_expl, df_genre, df_perf = parse_cnc_excel()
    print(f"  ✓ Parsed {len(df_freq)} historical frequency years (1938-2025).")
    print(f"  ✓ Parsed {len(df_expl)} nationality distribution years.")
    print(f"  ✓ Parsed {len(df_genre)} genre release years.")
    print(f"  ✓ Parsed {len(df_perf)} box office top performance years.")

    # Step 2: Build salles_cinema_etablissements with strict geography
    rows_salles = []
    cities = list(CITY_DEPT_REGION.keys())
    salle_idx = 1

    for cname, screens_list, seats_list in CIRCUITS_CINEMA:
        for _ in range(120):
            commune = random.choice(cities)
            dept, region = CITY_DEPT_REGION[commune]
            ecrans = random.choice(screens_list)
            fauteuils = random.choice(seats_list)
            is_art_essai = (cname == "Cinéma Indépendant Art & Essai" or random.random() < 0.20)

            rows_salles.append({
                "id_salle": f"CIN-{salle_idx:05d}",
                "nom_etablissement": f"{cname} {commune}",
                "circuit_cinema": cname,
                "commune": commune,
                "code_departement": dept,
                "nom_region": region,
                "nombre_ecrans": ecrans,
                "nombre_fauteuils": fauteuils,
                "classification_art_et_essai": is_art_essai
            })
            salle_idx += 1

    df_salles = pd.DataFrame(rows_salles)

    # Save CSVs locally and upload to BigQuery & GCS
    tables_dict = {
        "cnc_frequentation_historique": df_freq,
        "cnc_films_exploitation_nationalite": df_expl,
        "cnc_films_nouveautes_genres": df_genre,
        "cnc_performance_box_office_tops": df_perf,
        "salles_cinema_etablissements": df_salles
    }

    subprocess.run(f"gcloud storage buckets create {BUCKET_NAME} --project={PROJECT_ID} --location=EU 2>/dev/null", shell=True)

    for tname, df in tables_dict.items():
        csv_file = f"agents/cine_analyst/data/{tname}.csv"
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

    print("\nSUCCESS: Refined CineAnalyst data pipeline complete!")

if __name__ == "__main__":
    main()
