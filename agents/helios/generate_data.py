#!/usr/bin/env python3
"""
Mass Data Generation and OpenData Ingestion for Helios (power_energy_ds) in BigQuery using load_table_from_json.
Generates thousands of realistic Enedis electricity consumption, renewable production, IRVE charging hub, and industrial client records.
"""

import os
import sys
import random
import subprocess
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "power_energy_ds"
LOCATION = "US"

def get_client():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return bigquery.Client(project=PROJECT_ID, credentials=creds)

FRENCH_REGIONS = [
    "Auvergne-Rhône-Alpes", "Île-de-France", "Provence-Alpes-Côte d'Azur",
    "Nouvelle-Aquitaine", "Occitanie", "Grand Est", "Hauts-de-France",
    "Pays de la Loire", "Bretagne", "Normandie", "Bourgogne-Franche-Comté"
]

DEPARTEMENTS_ARA = ["69 - Rhône", "74 - Haute-Savoie", "38 - Isère", "42 - Loire", "63 - Puy-de-Dôme", "73 - Savoie", "01 - Ain", "26 - Drôme"]
DEPARTEMENTS_OTHER = ["75 - Paris", "13 - Bouches-du-Rhône", "31 - Haute-Garonne", "33 - Gironde", "59 - Nord", "44 - Loire-Atlantique", "67 - Bas-Rhin", "06 - Alpes-Maritimes", "34 - Hérault"]

COMMUNES_SAMPLE = [
    "Lyon", "Annecy", "Grenoble", "Saint-Étienne", "Chambéry", "Clermont-Ferrand", "Bourg-en-Bresse",
    "Paris", "Marseille", "Toulouse", "Bordeaux", "Lille", "Strasbourg", "Nantes", "Nice", "Rennes",
    "Versailles", "Cannes", "Thonon-les-Bains", "Gex", "Grasse", "Périgueux", "Valence", "Amiens"
]

SECTEURS_INDUSTRIELS = ["Chimie & Pharmacie", "Metallurgie & Métaux", "Agroalimentaire", "Automobile & Aéronautique", "Papier & Carton", "Matériaux de Construction", "Data Centers & Tech"]

def setup_and_enrich_helios():
    client = get_client()

    dataset_ref = bigquery.DatasetReference(PROJECT_ID, DATASET_ID)
    try:
        dataset = client.get_dataset(dataset_ref)
        print(f"Dataset '{DATASET_ID}' ready.")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = LOCATION
        dataset.description = "Dataset de consommation électrique Enedis pas 30min, production renouvelable, bornes IRVE et clients industriels pour Helios"
        client.create_dataset(dataset)

    job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)

    # 1. enedis_consommation_inf36 (~4,000 rows)
    s1 = [
        bigquery.SchemaField("id_releve", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("region", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("departement", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("commune", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("nom_transformateur_quartier", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("annee_mois_pas30min", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("consommation_totale_mwh", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("pic_consommation_kw", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("capacite_max_transformateur_kw", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("taux_charge_transformateur_pct", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("risque_tension_reseau", "STRING", mode="NULLABLE"),
    ]
    t1_ref = dataset_ref.table("enedis_consommation_inf36")
    t1 = bigquery.Table(t1_ref, schema=s1)
    client.create_table(t1, exists_ok=True)

    t1_id = f"{PROJECT_ID}.{DATASET_ID}.enedis_consommation_inf36"
    rows_c = []
    for i in range(1, 4001):
        reg = random.choice(FRENCH_REGIONS)
        dep = random.choice(DEPARTEMENTS_ARA if reg == "Auvergne-Rhône-Alpes" else DEPARTEMENTS_OTHER)
        commune = random.choice(COMMUNES_SAMPLE)
        transfo = f"TR-ENEDIS-{commune.upper()[:4]}-{i:04d}"
        cap_max = float(random.choice([500, 800, 1000, 1200, 1500, 2000]))
        pic_kw = round(cap_max * random.uniform(0.40, 0.98), 1)
        charge_pct = round((pic_kw / cap_max) * 100.0, 1)

        if charge_pct > 88.0:
            risque = "Saturation / Disjonction Imminente 48h"
        elif charge_pct > 75.0:
            risque = "Sous Surveillance Forte"
        else:
            risque = "Normal"

        rows_c.append({
            "id_releve": f"REL-{i:05d}",
            "region": reg,
            "departement": dep,
            "commune": commune,
            "nom_transformateur_quartier": transfo,
            "annee_mois_pas30min": "2026-08-17T18:30:00",
            "consommation_totale_mwh": round(pic_kw * 0.03, 2),
            "pic_consommation_kw": pic_kw,
            "capacite_max_transformateur_kw": cap_max,
            "taux_charge_transformateur_pct": charge_pct,
            "risque_tension_reseau": risque
        })

    job1 = client.load_table_from_json(rows_c, t1_id, job_config=job_config)
    job1.result()
    print(f"Loaded {len(rows_c)} rows into enedis_consommation_inf36 via BigQuery Load Job.")

    # 2. enedis_production_renouvelable (~3,000 rows)
    s2 = [
        bigquery.SchemaField("id_prod", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("region", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("departement", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("commune", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("filiere_energie", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("puissance_installee_mw", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("production_injectee_mwh", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("co2_evite_tonnes", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("taux_couverture_renouvelable_pct", "FLOAT64", mode="NULLABLE"),
    ]
    t2_ref = dataset_ref.table("enedis_production_renouvelable")
    t2 = bigquery.Table(t2_ref, schema=s2)
    client.create_table(t2, exists_ok=True)

    t2_id = f"{PROJECT_ID}.{DATASET_ID}.enedis_production_renouvelable"
    rows_p = []
    filieres = ["Solaire Photovoltaïque", "Éolien Terrestre", "Autoconsommation Collective Solaire", "Hydraulique", "Biomasse"]

    for i in range(1, 3001):
        reg = random.choice(FRENCH_REGIONS)
        dep = random.choice(DEPARTEMENTS_ARA if reg == "Auvergne-Rhône-Alpes" else DEPARTEMENTS_OTHER)
        commune = random.choice(COMMUNES_SAMPLE)
        fil = random.choice(filieres)
        puiss = round(random.uniform(0.5, 45.0), 2)
        prod = round(puiss * random.uniform(1200.0, 2400.0), 1)
        co2 = round(prod * 0.08, 1) # 80kg CO2/MWh évité vs mix résiduel
        couv = round(random.uniform(18.0, 64.0), 1)

        rows_p.append({
            "id_prod": f"PROD-{i:04d}",
            "region": reg,
            "departement": dep,
            "commune": commune,
            "filiere_energie": fil,
            "puissance_installee_mw": puiss,
            "production_injectee_mwh": prod,
            "co2_evite_tonnes": co2,
            "taux_couverture_renouvelable_pct": couv
        })

    job2 = client.load_table_from_json(rows_p, t2_id, job_config=job_config)
    job2.result()
    print(f"Loaded {len(rows_p)} rows into enedis_production_renouvelable via BigQuery Load Job.")

    # 3. enedis_bornes_irve (~3,500 rows)
    s3 = [
        bigquery.SchemaField("id_borne", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("region", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("departement", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("commune", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("station_recharge_nom", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("nombre_bornes_irve", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("puissance_max_kw", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("pic_recharge_ve_kw", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("densite_vehicules_electriques_pct", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("potentiel_deploiement_recharge_rapide", "STRING", mode="NULLABLE"),
    ]
    t3_ref = dataset_ref.table("enedis_bornes_irve")
    t3 = bigquery.Table(t3_ref, schema=s3)
    client.create_table(t3, exists_ok=True)

    t3_id = f"{PROJECT_ID}.{DATASET_ID}.enedis_bornes_irve"
    rows_b = []
    operators_irve = ["Station IRVE Supercharge", "Hub Recharge Express", "Station Électrique Urbaine", "Bornes Enedis Fast-Charge"]

    for i in range(1, 3501):
        reg = random.choice(FRENCH_REGIONS)
        dep = random.choice(DEPARTEMENTS_ARA if reg == "Auvergne-Rhône-Alpes" else DEPARTEMENTS_OTHER)
        commune = random.choice(COMMUNES_SAMPLE)
        nom_s = f"{random.choice(operators_irve)} {commune} #{i}"
        nb_b = random.randint(4, 32)
        p_max = float(random.choice([150, 300, 350, 500]))
        pic_ve = round(p_max * random.uniform(0.60, 0.96), 1)
        dens_ve = round(random.uniform(12.0, 34.0), 1)
        opp = "Priorité Forte (Sous-équipé)" if (dens_ve > 20.0 and nb_b < 15) else "Satisfaisant"

        rows_b.append({
            "id_borne": f"IRVE-{i:04d}",
            "region": reg,
            "departement": dep,
            "commune": commune,
            "station_recharge_nom": nom_s,
            "nombre_bornes_irve": nb_b,
            "puissance_max_kw": p_max,
            "pic_recharge_ve_kw": pic_ve,
            "densite_vehicules_electriques_pct": dens_ve,
            "potentiel_deploiement_recharge_rapide": opp
        })

    job3 = client.load_table_from_json(rows_b, t3_id, job_config=job_config)
    job3.result()
    print(f"Loaded {len(rows_b)} rows into enedis_bornes_irve via BigQuery Load Job.")

    # 4. enedis_clients_industriels (~2,500 rows)
    s4 = [
        bigquery.SchemaField("id_client_industriel", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("nom_entreprise_site", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("secteur_activite", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("region", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("departement", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("commune", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("consommation_annuelle_mwh", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("presence_panneaux_solaires", "BOOLEAN", mode="REQUIRED"),
        bigquery.SchemaField("surface_toiture_disponible_m2", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("potention_solaire_kwp", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("economie_co2_potentielle_tonnes", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("abonnement_mensuel_solar_as_a_service_eur", "FLOAT64", mode="NULLABLE"),
    ]
    t4_ref = dataset_ref.table("enedis_clients_industriels")
    t4 = bigquery.Table(t4_ref, schema=s4)
    client.create_table(t4, exists_ok=True)

    t4_id = f"{PROJECT_ID}.{DATASET_ID}.enedis_clients_industriels"
    rows_ind = []
    prefix_ind = ["Usine", "Complexe Industriel", "Site de Production", "Manufacture", "Hub Logistique"]

    for i in range(1, 2501):
        reg = random.choice(FRENCH_REGIONS)
        dep = random.choice(DEPARTEMENTS_ARA if reg == "Auvergne-Rhône-Alpes" else DEPARTEMENTS_OTHER)
        commune = random.choice(COMMUNES_SAMPLE)
        nom_site = f"{random.choice(prefix_ind)} {commune} #{i}"
        secteur = random.choice(SECTEURS_INDUSTRIELS)
        conso_mwh = round(random.uniform(4500.0, 85000.0), 1)

        # 30% of clients have solar, 70% do not (target for Solar-as-a-Service)
        has_solar = random.choice([False, False, False, True])
        surf_m2 = round(random.uniform(2500.0, 45000.0), 1)
        pot_kwp = round(surf_m2 * 0.18, 1) # 180Wp/m2
        co2_pot = round((pot_kwp * 1.15) * 0.08, 1)
        sub_month = round(pot_kwp * 4.5, 2)

        rows_ind.append({
            "id_client_industriel": f"IND-{i:04d}",
            "nom_entreprise_site": nom_site,
            "secteur_activite": secteur,
            "region": reg,
            "departement": dep,
            "commune": commune,
            "consommation_annuelle_mwh": conso_mwh,
            "presence_panneaux_solaires": has_solar,
            "surface_toiture_disponible_m2": surf_m2,
            "potention_solaire_kwp": pot_kwp,
            "economie_co2_potentielle_tonnes": co2_pot,
            "abonnement_mensuel_solar_as_a_service_eur": sub_month
        })

    job4 = client.load_table_from_json(rows_ind, t4_id, job_config=job_config)
    job4.result()
    print(f"Loaded {len(rows_ind)} rows into enedis_clients_industriels via BigQuery Load Job.")

    print(f"✅ Successfully loaded thousands of records for Helios in {DATASET_ID}!")

if __name__ == "__main__":
    setup_and_enrich_helios()
