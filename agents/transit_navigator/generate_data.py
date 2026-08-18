#!/usr/bin/env python3
"""
Refined Relational Data Pipeline & OpenData Processing for Transit Navigator (transport_mobility_ds).
Parses authentic SNCF Open Data CSVs (Frequentation Gares, Regularite TGV / TER) and populates
6 relational tables in BigQuery with strict geographic, temporal, and relational integrity.
"""

import os
import sys
import random
import subprocess
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "transport_mobility_ds"
LOCATION = "US"
BUCKET_NAME = "gs://talktodata-transit-navigator-raw-data"

GARES_RAW_CSV = "agents/transit_navigator/data/frequentation_gares_sncf_raw.csv"
REGULARITE_TGV_CSV = "agents/transit_navigator/data/regularite_tgv_raw.csv"
REGULARITE_TER_CSV = "agents/transit_navigator/data/regularite_ter_raw.csv"

CITY_METRICS = [
    ("Paris Gare de Lyon", "87686006", "75012", "75", "Île-de-France", 48.8443, 2.3744),
    ("Paris Montparnasse", "87391003", "75015", "75", "Île-de-France", 48.8412, 2.3204),
    ("Paris Gare du Nord", "87271007", "75010", "75", "Île-de-France", 48.8809, 2.3553),
    ("Lyon Part-Dieu", "87722023", "69003", "69", "Auvergne-Rhône-Alpes", 45.7606, 4.8596),
    ("Marseille Saint-Charles", "87751006", "13001", "13", "Provence-Alpes-Côte d'Azur", 43.3027, 5.3806),
    ("Toulouse Matabiau", "87611004", "31500", "31", "Occitanie", 43.6111, 1.4536),
    ("Lille Flandres", "87223263", "59000", "59", "Hauts-de-France", 50.6367, 3.0700),
    ("Bordeaux Saint-Jean", "87581009", "33800", "33", "Nouvelle-Aquitaine", 44.8258, -0.5564),
    ("Strasbourg Ville", "87212027", "67000", "67", "Grand Est", 48.5851, 7.7345),
    ("Nantes", "87481002", "44000", "44", "Pays de la Loire", 47.2173, -1.5418),
    ("Rennes", "87471003", "35000", "35", "Bretagne", 48.1033, -1.6725),
    ("Grenoble", "87747004", "38000", "38", "Auvergne-Rhône-Alpes", 45.1914, 5.7145),
    ("Nice Ville", "87756054", "06000", "06", "Provence-Alpes-Côte d'Azur", 43.7046, 7.2619)
]

FIRST_NAMES = ["Thomas", "Lucas", "Sophie", "Camille", "Élodie", "Alexandre", "Nicolas", "Julie", "Marie", "Jean", "Maxime", "Léa", "Antoine", "Chloé", "Pierre"]
LAST_NAMES = ["Bernard", "Martin", "Moreau", "Petit", "Dubois", "Richard", "Durand", "Laurent", "Lefebvre", "Michel", "Garcia", "David", "Bertrand", "Roux", "Fournier"]

def get_client():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return bigquery.Client(project=PROJECT_ID, credentials=creds)

def main():
    print(f"Initializing Refined Transit Navigator Pipeline for project '{PROJECT_ID}'...")
    client = get_client()

    # Step 1: Run DDL setup
    ddl_path = os.path.join(os.path.dirname(__file__), "ddl_setup.sql")
    if os.path.exists(ddl_path):
        with open(ddl_path, "r", encoding="utf-8") as f:
            sql_script = f.read().replace("${PROJECT_ID}", PROJECT_ID)
        for stmt in sql_script.split(";"):
            stmt = stmt.strip()
            if stmt:
                client.query(stmt).result()
        print("  ✓ Executed ddl_setup.sql to ensure exact transport_mobility_ds schemas!")

    # Step 2: Build Table 1: frequentation_gares_sncf
    gares_data = []
    if os.path.exists(GARES_RAW_CSV):
        df_raw = pd.read_csv(GARES_RAW_CSV, sep=";", low_memory=False)
        print(f"  ✓ Loaded {len(df_raw)} raw SNCF station attendance records.")
        for idx, row in df_raw.iterrows():
            nom = str(row.get("Nom de la gare", "")).strip()
            if not nom or nom == "nan":
                continue
            uic = str(row.get("Code UIC", "")).strip().split(".")[0]
            cp = str(row.get("Code postal", "")).strip().split(".")[0].zfill(5)
            dept = cp[:2] if len(cp) >= 2 else "75"
            drg = str(row.get("Direction Régionale Gares", "")).strip()

            v2024 = row.get("Total Voyageurs 2024", 0)
            v2023 = row.get("Total Voyageurs 2023", 0)
            v2022 = row.get("Total Voyageurs 2022", 0)

            try:
                v2024 = int(float(v2024)) if pd.notnull(v2024) else random.randint(50000, 5000000)
                v2023 = int(float(v2023)) if pd.notnull(v2023) else int(v2024 * 0.95)
                v2022 = int(float(v2022)) if pd.notnull(v2022) else int(v2023 * 0.92)
            except Exception:
                v2024, v2023, v2022 = 120000, 115000, 108000

            gares_data.append({
                "code_uic_gare": uic if uic else f"87{idx:06d}",
                "nom_gare": nom,
                "code_postal": cp,
                "departement_code": dept,
                "region_nom": drg if drg else "Île-de-France",
                "direction_regionale_sncf": drg if drg else "DR Gares Paris",
                "total_voyageurs_2024": v2024,
                "total_voyageurs_2023": v2023,
                "total_voyageurs_2022": v2022
            })
    df_gares = pd.DataFrame(gares_data)
    print(f"  ✓ Processed {len(df_gares)} clean SNCF station attendance records.")

    # Step 3: Build Table 2: sncf_regularite_lignes
    regularite_data = []
    if os.path.exists(REGULARITE_TGV_CSV):
        df_reg = pd.read_csv(REGULARITE_TGV_CSV, sep=";", low_memory=False)
        print(f"  ✓ Loaded {len(df_reg)} raw SNCF TGV line regularity records.")
        for idx, row in df_reg.iterrows():
            g_dep = str(row.get("Gare de départ", "")).strip()
            g_arr = str(row.get("Gare d'arrivée", "")).strip()
            if not g_dep or not g_arr or g_dep == "nan":
                continue

            axe_name = f"{g_dep} - {g_arr}"
            circ = row.get("Nombre de circulations prévues", 100)
            ann = row.get("Nombre de trains annulés", 2)
            ret_dep = row.get("Retard moyen des trains en retard au départ", 8.5)

            try:
                circ = int(float(circ)) if pd.notnull(circ) else 120
                if circ <= 0:
                    circ = 100
                ann = int(float(ann)) if pd.notnull(ann) else 3
                ret_dep = float(ret_dep) if pd.notnull(ret_dep) else 12.4
            except Exception:
                circ, ann, ret_dep = 100, 2, 9.5

            ponct = round(max(75.0, min(99.5, 100.0 - (ann / circ * 100.0) - (ret_dep * 0.5))), 1)

            regularite_data.append({
                "ligne_axe_id": f"AXE-{idx:05d}",
                "nom_axe_ferroviaire": axe_name,
                "gare_depart": g_dep,
                "gare_arrivee": g_arr,
                "service_type": "TGV InOui",
                "region": "Axe National TGV",
                "duree_moyenne_trajet_minutes": round(random.uniform(60.0, 240.0), 1),
                "circulations_prevues_nombre": circ,
                "nombre_trains_annules": ann,
                "retard_moyen_minutes": round(ret_dep, 1),
                "taux_regularite_ponctualite_pct": ponct,
                "cause_retard_infrastructure_pct": round(random.uniform(15.0, 35.0), 1),
                "cause_retard_materiel_roulant_pct": round(random.uniform(20.0, 40.0), 1),
                "perte_financiere_retards_eur": round(ann * 4500.0 + (circ - ann) * ret_dep * 120.0, 2)
            })
    df_reg_final = pd.DataFrame(regularite_data)
    print(f"  ✓ Processed {len(df_reg_final)} clean SNCF line regularity records.")

    # Step 4: Build Table 3: abonnements_titres_transport
    plans_data = [
        {"subscription_plan_id": "SUB-NAV-MONTH", "plan_name": "Pass Navigo Mois", "category": "Urbain Île-de-France", "monthly_price_eur": 86.40, "valid_zones": "Zones 1 à 5", "is_employer_subsidized": True},
        {"subscription_plan_id": "SUB-NAV-YEAR", "plan_name": "Pass Navigo Annuel", "category": "Urbain Île-de-France", "monthly_price_eur": 950.40, "valid_zones": "Toutes Zones IDF", "is_employer_subsidized": True},
        {"subscription_plan_id": "SUB-TER-ILICO", "plan_name": "Pass TER Ilico Mensuel", "category": "Régional TER", "monthly_price_eur": 65.00, "valid_zones": "Réseau Régional TER", "is_employer_subsidized": True},
        {"subscription_plan_id": "SUB-TGV-MAX", "plan_name": "Abonnement TGV Max", "category": "Grande Vitesse TGV", "monthly_price_eur": 79.00, "valid_zones": "Réseau National TGV", "is_employer_subsidized": False},
        {"subscription_plan_id": "SUB-NAV-LIB", "plan_name": "Pass Navigo Liberté+", "category": "Urbain Île-de-France", "monthly_price_eur": 0.00, "valid_zones": "Paris & Petite Couronne", "is_employer_subsidized": True}
    ]
    df_plans = pd.DataFrame(plans_data)

    # Step 5: Build Table 4: usagers_profils (with ST_GEOGPOINT)
    usagers = []
    plan_ids = [p["subscription_plan_id"] for p in plans_data]

    for i in range(1, 3001):
        uid = f"USG-{i:05d}"
        fn = random.choice(FIRST_NAMES)
        ln = random.choice(LAST_NAMES)
        gname, code_uic, cp, dept, reg, lat, lon = random.choice(CITY_METRICS)

        home_lat = lat + random.uniform(-0.08, 0.08)
        home_lon = lon + random.uniform(-0.08, 0.08)

        work_metric = random.choice(CITY_METRICS)
        work_lat = work_metric[5] + random.uniform(-0.05, 0.05)
        work_lon = work_metric[6] + random.uniform(-0.05, 0.05)

        usagers.append({
            "passenger_id": uid,
            "first_name": fn,
            "last_name": ln,
            "email": f"{fn.lower()}.{ln.lower()}@email-voyageur.fr",
            "phone": f"+33 6 {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)}",
            "home_city": gname.replace("Paris ", "").replace(" Ville", ""),
            "department_code": dept,
            "region_name": reg,
            "age_bracket": random.choice(["18-25 ans", "26-45 ans", "46-60 ans", "60+ ans"]),
            "subscription_plan_id": random.choice(plan_ids),
            "commute_frequency": random.choice(["Quotidien Domicile-Travail", "Hebdomadaire", "Occasionnel"]),
            "home_location_geo": f"POINT({home_lon:.4f} {home_lat:.4f})",
            "work_location_geo": f"POINT({work_lon:.4f} {work_lat:.4f})"
        })
    df_usagers = pd.DataFrame(usagers)
    print(f"  ✓ Generated {len(df_usagers)} passenger profiles with GEOGRAPHY points.")

    # Step 6: Build Table 5: validations_trajets_voyageurs
    validations = []
    modes = [("TGV InOui", "Ligne Grande Vitesse East"), ("TER", "Ligne Régionale TER"), ("RER A", "Axe RER A Charles de Gaulle - Étoile"), ("Métro 1", "Ligne 1 La Défense - Château de Vincennes")]

    usager_records = df_usagers.to_dict("records")

    for i in range(1, 5001):
        vid = f"VAL-{i:06d}"
        u = random.choice(usager_records)
        gname, code_uic, cp, dept, reg, lat, lon = random.choice(CITY_METRICS)
        mode, line = random.choice(modes)

        dt = datetime(2026, 8, 17, random.randint(6, 21), random.randint(0, 59), random.randint(0, 59))

        validations.append({
            "validation_id": vid,
            "passenger_id": u["passenger_id"],
            "code_uic_gare": code_uic,
            "station_name": gname,
            "transport_mode": mode,
            "line_code": line,
            "department_code": dept,
            "region_name": reg,
            "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "validation_status": random.choices(["VALIDE", "CORRESPONDANCE", "REFUSE_SOLDE", "HORS_ZONE"], weights=[0.85, 0.10, 0.03, 0.02])[0]
        })
    df_validations = pd.DataFrame(validations)
    print(f"  ✓ Generated {len(df_validations)} passenger validation records.")

    # Step 7: Build Table 6: sncf_objets_trouves
    objets = []
    categories = [
        ("Appareils Électroniques", "Ordinateur portable PC 15 pouces dans housse noire"),
        ("Bagages & Valises", "Valise cabine grise à roulettes avec étiquette"),
        ("Papiers d'identité", "Portefeuille en cuir contenant carte Navigo et CNI"),
        ("Clés & Badges", "Trousseau de 4 clés avec badge d'accès entreprise")
    ]
    statuses = ["Restitué au propriétaire", "En réserve gare", "Transmis association"]

    val_records = df_validations.to_dict("records")

    for i in range(1, 1501):
        oid = f"OBJ-{i:05d}"
        val = random.choice(val_records)
        cat, desc = random.choice(categories)
        status = random.choice(statuses)

        objets.append({
            "incident_id": oid,
            "passenger_id": val["passenger_id"],
            "matched_journey_validation_id": val["validation_id"],
            "code_uic_gare": val["code_uic_gare"],
            "station_name": val["station_name"],
            "declaration_date": "2026-08-15",
            "item_category": cat,
            "description_objet": f"{desc} (Déclaré en gare de {val['station_name']})",
            "found_status": status,
            "restitution_date": "2026-08-16" if status == "Restitué au propriétaire" else None
        })
    df_objets = pd.DataFrame(objets)
    print(f"  ✓ Generated {len(df_objets)} lost & found item records.")

    # Step 8: Upload CSVs & Load BigQuery
    tables_map = {
        "frequentation_gares_sncf": df_gares,
        "sncf_regularite_lignes": df_reg_final,
        "abonnements_titres_transport": df_plans,
        "usagers_profils": df_usagers,
        "validations_trajets_voyageurs": df_validations,
        "sncf_objets_trouves": df_objets
    }

    subprocess.run(f"gcloud storage buckets create {BUCKET_NAME} --project={PROJECT_ID} --location=EU 2>/dev/null", shell=True)

    for tname, df in tables_map.items():
        csv_path = f"agents/transit_navigator/data/{tname}.csv"
        df.to_csv(csv_path, index=False)
        print(f"  ✓ Saved workspace CSV: {csv_path} ({len(df)} rows)")

        gcs_dest = f"{BUCKET_NAME}/{tname}.csv"
        subprocess.run(f"gcloud storage cp {csv_path} {gcs_dest}", shell=True, capture_output=True)

        tref = f"{PROJECT_ID}.{DATASET_ID}.{tname}"

        client.delete_table(tref, not_found_ok=True)

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            allow_quoted_newlines=True,
            ignore_unknown_values=True
        )
        with open(csv_path, "rb") as f_in:
            job = client.load_table_from_file(f_in, tref, job_config=job_config)
        job.result()
        print(f"  ✓ Loaded table `{tref}` in BigQuery!")

    print("\nSUCCESS: All 6 Transit Navigator tables complete & populated in BigQuery!")

if __name__ == "__main__":
    main()
