#!/usr/bin/env python3
"""
Relational Data Generation and CNC Cinema OpenData Processing for CineAnalyst (cinema_boxoffice_ds).
Reads base Excel dataset 'agents/cine_analyst/data/Fréquentation et films dans les salles de cinéma.xlsx'
and builds 7 refined relational tables:
1. cnc_frequentation_historique (Historical annual attendance, box-office revenue & ticket price)
2. cnc_films_exploitation_nationalite (Films in distribution by nationality: French, US, European)
3. cnc_films_nouveautes_genres (First-run releases by genre: Fiction, Documentary, Animation)
4. cnc_performance_box_office_tops (Admissions of Top 10, Top 20, Top 30, Top 100 films)
5. salles_cinema_etablissements (Cinema theater circuits & multiplexes with strict geography)
6. cnc_films_nouveautes_titres_boxoffice (Individual Movie Titles, Budgets, 1st Week Admissions, Flop Risk & Social Buzz)
7. salles_formats_projection_frequentation (IMAX 3D, 4DX Immersif, Dolby Cinema vs Standard Occupancy & Ticket Prices)
"""

import os
import sys
import random
import subprocess
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "cinema_boxoffice_ds"
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

    # Step 1: Execute ddl_setup.sql
    ddl_path = os.path.join(os.path.dirname(__file__), "ddl_setup.sql")
    if os.path.exists(ddl_path):
        with open(ddl_path, "r", encoding="utf-8") as f:
            sql_script = f.read().replace("${PROJECT_ID}", PROJECT_ID)
        for stmt in sql_script.split(";"):
            stmt = stmt.strip()
            if stmt:
                client.query(stmt).result()
        print("  ✓ Executed ddl_setup.sql to ensure exact cinema_boxoffice_ds schemas!")

    # Step 2: Read authentic CNC Excel
    df_freq, df_expl, df_genre, df_perf = parse_cnc_excel()

    # Step 3: Build Table 5: salles_cinema_etablissements
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

    # Step 4: Build Table 6: cnc_films_nouveautes_titres_boxoffice
    movies = [
        # Major Hits / High Retention
        ("FILM-2025-001", "Le Comte de Monte-Cristo", "Fiction", "Français", 43000000.0, "2024-06-28", 1250000, 9300000, 22, 0.92, 96.5, 2.1),
        ("FILM-2025-002", "L'Amour Ouf", "Fiction", "Français", 32000000.0, "2024-10-16", 1050000, 4800000, 16, 0.89, 91.0, 5.0),
        ("FILM-2025-003", "Dune: Partie 2", "Fiction", "Américain", 190000000.0, "2024-02-28", 1380000, 4200000, 14, 0.88, 94.0, 4.2),
        ("FILM-2025-004", "Vaiana 2", "Animation", "Américain", 150000000.0, "2024-11-27", 1450000, 5600000, 12, 0.94, 97.0, 1.5),
        ("FILM-2025-005", "Gladiator II", "Fiction", "Américain", 240000000.0, "2024-11-13", 1120000, 3900000, 10, 0.82, 88.0, 12.0),
        ("FILM-2025-006", "Monsieur Aznavour", "Fiction", "Français", 26000000.0, "2024-10-23", 610000, 2100000, 11, 0.86, 85.0, 8.5),
        ("FILM-2025-007", "Vice-Versa 2", "Animation", "Américain", 175000000.0, "2024-06-19", 1680000, 8400000, 18, 0.95, 98.0, 1.0),
        ("FILM-2025-008", "Un P'tit Truc En Plus", "Fiction", "Français", 4500000.0, "2024-05-01", 1100000, 10800000, 26, 0.96, 99.0, 0.5),

        # High Budget Flops / High Risk
        ("FILM-2025-009", "Joker: Folie à Deux", "Fiction", "Américain", 190000000.0, "2024-10-02", 620000, 1150000, 5, 0.45, 41.0, 79.0),
        ("FILM-2025-010", "Emmanuelle", "Fiction", "Français", 24000000.0, "2024-09-25", 180000, 320000, 4, 0.42, 32.0, 82.5),
        ("FILM-2025-011", "Megalopolis", "Fiction", "Américain", 120000000.0, "2024-09-25", 140000, 260000, 3, 0.38, 28.0, 88.0),
        ("FILM-2025-012", "Argylle", "Fiction", "Américain", 200000000.0, "2024-01-31", 210000, 450000, 4, 0.35, 25.0, 91.0),
        ("FILM-2025-013", "Borderlands", "Fiction", "Américain", 115000000.0, "2024-08-07", 110000, 190000, 3, 0.31, 21.0, 94.5),
        ("FILM-2025-014", "Madame Web", "Fiction", "Américain", 80000000.0, "2024-02-14", 165000, 310000, 4, 0.36, 29.0, 87.0),

        # Additional Releases Across Genres & Origins
        ("FILM-2025-015", "La Petite Vadrouille", "Fiction", "Français", 8500000.0, "2024-06-05", 210000, 650000, 8, 0.78, 72.0, 18.0),
        ("FILM-2025-016", "Moi, Moche et Méchant 4", "Animation", "Américain", 100000000.0, "2024-07-10", 1420000, 4300000, 12, 0.91, 92.0, 3.5),
        ("FILM-2025-017", "Kraven le Chasseur", "Fiction", "Américain", 130000000.0, "2024-12-18", 340000, 780000, 5, 0.52, 48.0, 68.0),
        ("FILM-2025-018", "La Nuit du 12 (Re-sortie)", "Fiction", "Français", 4200000.0, "2024-03-15", 95000, 520000, 10, 0.85, 84.0, 9.0),
        ("FILM-2025-019", "Le Robot Sauvage", "Animation", "Américain", 78000000.0, "2024-10-09", 580000, 2400000, 11, 0.90, 93.0, 4.0),
        ("FILM-2025-020", "Kaamelott : Deuxième Volet", "Fiction", "Français", 28000000.0, "2025-01-15", 980000, 3800000, 14, 0.87, 95.0, 6.0)
    ]

    df_movies = pd.DataFrame(movies, columns=[
        "movie_id", "titre_film", "genre", "nationalite", "budget_production_eur",
        "date_sortie_salles", "entrees_premiere_semaine", "entrees_cumulees_total",
        "semaines_affiche", "coefficient_maintien_semaine2", "index_buzz_reseaux_sociaux",
        "risque_flop_box_office_pct"
    ])

    # Step 5: Build Table 7: salles_formats_projection_frequentation
    formats = [
        ("FMT-001", "Standard 2D", 28.5, 7.42, 0.0, 650.0),
        ("FMT-002", "IMAX 3D", 68.5, 14.50, 95.4, 1980.0),
        ("FMT-003", "4DX Immersif", 74.2, 16.80, 126.4, 2450.0),
        ("FMT-004", "Dolby Cinema", 62.0, 13.90, 87.3, 1720.0),
        ("FMT-005", "ScreenX 270°", 58.0, 12.50, 68.5, 1480.0)
    ]
    df_formats = pd.DataFrame(formats, columns=[
        "format_id", "nom_format_projection", "taux_occupation_moyen_seance_pct",
        "prix_moyen_billet_format_eur", "surcout_prix_billet_pct", "recette_annuelle_par_fauteuil_eur"
    ])

    # Save CSVs locally and upload to BigQuery & GCS
    tables_dict = {
        "cnc_frequentation_historique": df_freq,
        "cnc_films_exploitation_nationalite": df_expl,
        "cnc_films_nouveautes_genres": df_genre,
        "cnc_performance_box_office_tops": df_perf,
        "salles_cinema_etablissements": df_salles,
        "cnc_films_nouveautes_titres_boxoffice": df_movies,
        "salles_formats_projection_frequentation": df_formats
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

    print("\nSUCCESS: Refined CineAnalyst 7-table data pipeline complete!")

if __name__ == "__main__":
    main()
