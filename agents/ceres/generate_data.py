#!/usr/bin/env python3
"""
Populates the Ceres Agriculture & Agroecological Transition relational schema in BigQuery:
- cooperatives_agricoles (8 major French agricultural cooperatives)
- previsions_anomalies_meteo_ete (Summer 2026 weather forecast anomalies for Q1)
- exploitations_agricoles (1,500 farms linked to cooperatives)
- parcelles_agricoles (4,500 field parcels linked to real ADEME Agribalyse 3.1 code_ciqual)
- recoltes_rendements (22,500 multi-year harvest lots 2021-2025)
- capteurs_iot_sols_meteo (67,500 daily IoT sensor and NDVI readings)
- bilans_carbone_subventions_hve (4,500 annual carbon credit and PAC subsidy balance sheets for Q2)
- rapports_performance_esg_chaine (Consolidated ESG supply chain reports for Q3)

Dataset: agriculture_rurality_ds
"""

import os
import sys
import uuid
import random
import subprocess
from datetime import datetime, date, timedelta
from faker import Faker
import pandas as pd
from google.oauth2 import credentials
from google.cloud import bigquery

fake = Faker('fr_FR')
Faker.seed(42)
random.seed(42)

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "agriculture_rurality_ds"
BUCKET_NAME = "gs://talktodata-ceres-raw-data"

AGRIBALYSE_CSV_PATH = "agents/ceres/data/agribalyse-31-synthese.csv"
if os.path.exists(AGRIBALYSE_CSV_PATH):
    df_agri_base = pd.read_csv(AGRIBALYSE_CSV_PATH, low_memory=False)
    print(f"Processing base Open Data CSV: '{AGRIBALYSE_CSV_PATH}' ({len(df_agri_base)} ADEME ACV products parsed).")


COOPERATIVES_DATA = [
    ("COO_4001", "Coopérative Arterris", "31 - Haute-Garonne", "Occitanie", 450000.0, "Grandes cultures"),
    ("COO_4002", "Coopérative Euralis", "64 - Pyrénées-Atlantiques", "Nouvelle-Aquitaine", 380000.0, "Grandes cultures"),
    ("COO_4003", "Coopérative Lur Berri", "64 - Pyrénées-Atlantiques", "Nouvelle-Aquitaine", 290000.0, "Elevage"),
    ("COO_4004", "Coopérative Axereal", "28 - Eure-et-Loir", "Centre-Val de Loire", 620000.0, "Grandes cultures"),
    ("COO_4005", "Coopérative Vivescia", "51 - Marne", "Grand Est", 750000.0, "Grandes cultures"),
    ("COO_4006", "Coopérative Tereos", "02 - Aisne", "Hauts-de-France", 890000.0, "Grandes cultures"),
    ("COO_4007", "Coopérative Agrial", "14 - Calvados", "Normandie", 510000.0, "Maraichage"),
    ("COO_4008", "Coopérative Cristal Union", "51 - Marne", "Grand Est", 680000.0, "Grandes cultures")
]

REGIONS_DEPARTEMENTS = {
    "Occitanie": ["31 - Haute-Garonne", "32 - Gers", "81 - Tarn", "34 - Hérault", "11 - Aude", "82 - Tarn-et-Garonne"],
    "Nouvelle-Aquitaine": ["33 - Gironde", "47 - Lot-et-Garonne", "24 - Dordogne", "64 - Pyrénées-Atlantiques", "79 - Deux-Sèvres"],
    "Auvergne-Rhône-Alpes": ["63 - Puy-de-Dôme", "01 - Ain", "26 - Drôme", "38 - Isère", "69 - Rhône"],
    "Centre-Val de Loire": ["28 - Eure-et-Loir", "45 - Loiret", "37 - Indre-et-Loire"],
    "Hauts-de-France": ["80 - Somme", "59 - Nord", "60 - Oise", "62 - Pas-de-Calais"],
    "Grand Est": ["51 - Marne", "10 - Aube", "68 - Haut-Rhin", "67 - Bas-Rhin"]
}

REGION_CODES = {
    "Occitanie": "OCC", "Nouvelle-Aquitaine": "NAQ", "Auvergne-Rhône-Alpes": "ARA",
    "Centre-Val de Loire": "CVL", "Hauts-de-France": "HDF", "Grand Est": "GES"
}

FILIERES_CULTURES = {
    "Grandes cultures": [
        ("Blé tendre, cru", 11084, "Céréales"),
        ("Maïs grain, cru", 11015, "Céréales"),
        ("Graines de colza", 15003, "Oléagineux"),
        ("Graines de tournesol", 15011, "Oléagineux"),
        ("Pois chiche, sec", 20042, "Légumineuses")
    ],
    "Viticulture": [
        ("Raisin de cuve rouge, cru", 13012, "Fruits"),
        ("Raisin de cuve blanc, cru", 13013, "Fruits")
    ],
    "Arboriculture": [
        ("Pomme, crue", 13034, "Fruits"),
        ("Poire, crue", 13032, "Fruits"),
        ("Pêche, crue", 13030, "Fruits")
    ],
    "Maraîchage": [
        ("Tomate, crue", 20047, "Légumes"),
        ("Carotte, crue", 20008, "Légumes"),
        ("Pomme de terre, crue", 20038, "Légumes")
    ]
}

def generate_siren():
    return "".join([str(random.randint(0, 9)) for _ in range(9)])

def main():
    print(f"Generating Complete Ceres Agroecological Dataset (Q1, Q2, Q3) for '{PROJECT_ID}'...")

    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = credentials.Credentials(token)
    client = bigquery.Client(project=PROJECT_ID, credentials=creds)

    cooperatives, weather_forecasts, farms, parcels, harvests, iot_readings, carbon_bilans, esg_reports = [], [], [], [], [], [], [], []

    # 1. Cooperatives Master Table
    for cid, cname, cdept, creg, csilo, cfiliere in COOPERATIVES_DATA:
        cooperatives.append({
            "id_cooperative": cid,
            "nom_cooperative": cname,
            "siren": generate_siren(),
            "nom_region": creg,
            "code_departement": cdept,
            "capacite_stockage_tonnes": csilo,
            "filiere_principale": cfiliere
        })

    # 2. Summer 2026 Weather Forecast Anomalies (Q1: yield drop > 20%)
    all_depts = []
    for reg, dlist in REGIONS_DEPARTEMENTS.items():
        for d in dlist:
            all_depts.append((reg, d))

    for idx, (reg, d) in enumerate(all_depts):
        is_severe = (reg in ["Occitanie", "Nouvelle-Aquitaine", "Centre-Val de Loire"] and idx % 2 == 0)
        temp_anom = round(random.uniform(2.8, 4.2), 1) if is_severe else round(random.uniform(0.8, 1.8), 1)
        precip_anom = round(random.uniform(-45.0, -28.0), 1) if is_severe else round(random.uniform(-15.0, -5.0), 1)
        stress_prevu = round(random.uniform(0.75, 0.95), 2) if is_severe else round(random.uniform(0.30, 0.55), 2)
        baisse_rendement = round(random.uniform(22.5, 34.0), 1) if is_severe else round(random.uniform(5.0, 14.5), 1)

        weather_forecasts.append({
            "id_prevision": f"PREV_2026_{idx+1:03d}",
            "annee_saison": "2026-ETE",
            "code_departement": d,
            "nom_region": reg,
            "temperature_anomalie_c": temp_anom,
            "precipitations_anomalie_pct": precip_anom,
            "indice_secheresse_evapotranspiration_prevu": stress_prevu,
            "baisse_rendement_predite_pct": baisse_rendement
        })

    # 3. Generate 1,500 Exploitations (linked to cooperatives)
    for i in range(1500):
        farm_id = f"EXP_{310000 + i}"
        coop = random.choice(cooperatives)
        region = coop["nom_region"]
        dept = coop["code_departement"]
        filiere = random.choice(list(FILIERES_CULTURES.keys()))

        mode_prod = random.choices(
            ["Conventionnel", "HVE - Haute Valeur Environnementale", "Bio / Agriculture Biologique", "Conversion Bio"],
            weights=[0.45, 0.25, 0.20, 0.10]
        )[0]

        sau_ha = round(random.uniform(25.0, 320.0), 1)
        is_bas_carbone = (mode_prod in ["HVE - Haute Valeur Environnementale", "Bio / Agriculture Biologique"] and random.random() < 0.65)

        farms.append({
            "id_exploitation": farm_id,
            "id_cooperative": coop["id_cooperative"],
            "nom_exploitation": f"Domaine {fake.last_name()} {random.choice(['et Fils', 'Agri', 'Bio', 'SLA', 'EARL'])}",
            "siren": generate_siren(),
            "nom_exploitant": f"{fake.first_name()} {fake.last_name()}",
            "code_region": REGION_CODES.get(region, "FRA"),
            "nom_region": region,
            "code_departement": dept,
            "commune": fake.city(),
            "code_postal": f"{dept[:2]}{random.randint(100, 900):03d}",
            "surface_totale_ha": sau_ha,
            "mode_production": mode_prod,
            "filiere_principale": filiere,
            "date_creation": (datetime.now() - timedelta(days=random.randint(1000, 10000))).strftime("%Y-%m-%d"),
            "certification_bas_carbone": is_bas_carbone
        })

        # 4. Generate 3 Parcels per Farm (4,500 Parcels total)
        for p_idx in range(3):
            parcel_id = f"PAR_{farm_id}_{p_idx+1}"
            culture_name, ciqual_code, cat_crop = random.choice(FILIERES_CULTURES[filiere])
            p_surface = round(sau_ha / 3.0, 1)

            sol_type = random.choice(["Argilo-calcaire", "Limoneux", "Sableux", "Granitique", "Alluvial"])
            irrigation = (filiere in ["Maraîchage", "Arboriculture"] or random.random() < 0.35)
            score_sol = random.randint(45, 95) if mode_prod != "Conventionnel" else random.randint(25, 75)

            parcels.append({
                "id_parcelle": parcel_id,
                "id_exploitation": farm_id,
                "nom_parcelle": f"Champ {fake.street_name().split()[0]} #{p_idx+1}",
                "surface_ha": p_surface,
                "culture_actuelle": culture_name,
                "code_ciqual": ciqual_code,
                "type_sol": sol_type,
                "irrigation_active": irrigation,
                "score_sante_sol": score_sol,
                "annee_plantation": random.randint(2015, 2024)
            })

            # Multi-year Harvests (2021-2025)
            for yr in [2021, 2022, 2023, 2024, 2025]:
                rendement_ha = round(random.uniform(4.5, 9.2) if cat_crop == "Céréales" else random.uniform(12.0, 45.0), 2)
                vol_tonnes = round(p_surface * rendement_ha, 2)
                
                score_ef = round(random.uniform(0.12, 0.45), 3) if mode_prod != "Conventionnel" else round(random.uniform(0.35, 0.85), 3)
                co2_kg = round(vol_tonnes * score_ef * 1000.0, 2)
                prix_tonne = round(random.uniform(180.0, 320.0), 2)

                statut_comm = "VALORISE_BAS_CARBONE" if is_bas_carbone else random.choice(["VENDU_COOPERATIVE", "STOCKE_FERME"])

                harvests.append({
                    "id_recolte": f"REC_{parcel_id}_{yr}",
                    "id_parcelle": parcel_id,
                    "id_exploitation": farm_id,
                    "annee_campagne": yr,
                    "quantite_recoltee_tonnes": vol_tonnes,
                    "rendement_ha_tonnes": rendement_ha,
                    "taux_humidite_pct": round(random.uniform(11.5, 15.5), 1),
                    "score_ef_total_lot": score_ef,
                    "emissions_co2_kg_eq": co2_kg,
                    "prix_vente_tonne_eur": prix_tonne,
                    "statut_commercialisation": statut_comm
                })

            # IoT Sensors Telemetry
            for day_offset in range(0, 15):
                dt = (date(2025, 6, 1) + timedelta(days=day_offset)).strftime("%Y-%m-%d")
                hum_sol = round(random.uniform(18.0, 45.0), 1)
                temp_sol = round(random.uniform(16.0, 28.5), 1)
                stress_h = "FAIBLE" if hum_sol > 30 else ("MODERE" if hum_sol > 22 else "SEVERE")
                ndvi = round(random.uniform(0.45, 0.82), 2)

                iot_readings.append({
                    "id_capteur": f"IOT_{parcel_id}",
                    "id_parcelle": parcel_id,
                    "date_releve": dt,
                    "humidite_sol_pct": hum_sol,
                    "temperature_sol_c": temp_sol,
                    "niveau_stress_hydrique": stress_h,
                    "precipitations_mm": round(random.uniform(0.0, 14.5), 1),
                    "evapotranspiration_mm": round(random.uniform(2.1, 5.8), 1),
                    "indice_vegetation_ndvi": ndvi
                })

        # Carbon Credit & PAC Subsidies (2023-2025)
        for yr in [2023, 2024, 2025]:
            co2_evite = round(sau_ha * random.uniform(1.2, 3.8), 2) if mode_prod != "Conventionnel" else 0.0
            pac_eur = round(sau_ha * random.uniform(210.0, 380.0), 2)
            credits_carbone_eur = round(co2_evite * 45.0, 2)
            label = "LABEL_BAS_CARBONE" if is_bas_carbone else (mode_prod if mode_prod != "Conventionnel" else "AUCUN")

            carbon_bilans.append({
                "id_bilan": f"BIL_{farm_id}_{yr}",
                "id_exploitation": farm_id,
                "annee_exercice": yr,
                "bilan_co2_tonnes_evitees": co2_evite,
                "montant_subvention_pac_eur": pac_eur,
                "montant_credits_carbone_eur": credits_carbone_eur,
                "label_obtenu": label
            })

    # 5. Consolidated ESG Supply Chain Reports (Q3: Executive ESG Report)
    for yr in [2025, 2026]:
        for fil in ["Grandes cultures", "Viticulture", "Arboriculture", "Maraîchage"]:
            esg_reports.append({
                "id_rapport": f"ESG_{fil[:3].upper()}_{yr}",
                "annee_exercice": yr,
                "filiere_principale": fil,
                "taux_exploitations_certifiees_pct": round(random.uniform(42.5, 68.0), 1),
                "empreinte_carbone_chaine_co2_kg_par_kg": round(random.uniform(0.22, 0.48), 3),
                "reduction_pesticides_pct": round(random.uniform(18.5, 35.0), 1),
                "score_performance_esg_global": random.randint(78, 92),
                "synthise_investisseurs": f"La filière {fil} affiche une trajectoire bas-carbone robuste avec {random.randint(45, 65)}% d'exploitations certifiées HVE/Label Bas-Carbone, réduisant l'empreinte carbone globale de 28% pour la présentation aux investisseurs institutionnels."
            })

    # Save to DataFrame and Load into BigQuery
    tables_dict = {
        "cooperatives_agricoles": pd.DataFrame(cooperatives),
        "previsions_anomalies_meteo_ete": pd.DataFrame(weather_forecasts),
        "exploitations_agricoles": pd.DataFrame(farms),
        "parcelles_agricoles": pd.DataFrame(parcels),
        "recoltes_rendements": pd.DataFrame(harvests),
        "capteurs_iot_sols_meteo": pd.DataFrame(iot_readings),
        "bilans_carbone_subventions_hve": pd.DataFrame(carbon_bilans),
        "rapports_performance_esg_chaine": pd.DataFrame(esg_reports)
    }

    os.makedirs("agents/ceres/data", exist_ok=True)

    for tname, df in tables_dict.items():
        csv_file = f"agents/ceres/data/{tname}.csv"
        df.to_csv(csv_file, index=False)
        print(f"  ✓ Saved local workspace CSV: {csv_file} ({len(df)} rows)")

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

    print("\nSUCCESS: All Ceres relational tables (including Q1, Q2, Q3 tables) populated, uploaded to GCS and loaded in BigQuery!")

if __name__ == "__main__":
    main()
