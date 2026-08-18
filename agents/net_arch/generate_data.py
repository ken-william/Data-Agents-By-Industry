#!/usr/bin/env python3
"""
Relational Data Generation and ARCEP Telecom OpenData Processing for NetArch (telecom_network_ds).
Populates 7 refined relational tables:
1. arcep_sites_mobiles_metropole (Official ARCEP 2G/3G/4G/5G mobile tower sites in France)
2. arcep_historique_deploiement_5g (5G deployment history by operator & frequency band)
3. telecom_qualite_service_metrique (QoS download/upload throughputs & ping latency)
4. telecom_incidents_equipements_reseau (Equipment outages, micro-cuts & SLAs)
5. abonnes_clients_b2b_b2c (Subscribers master: Churn B2B, Smart 5G Upsell, >80% March quota, fees, copper >150GB)
6. signalements_dysfonctionnements_utilisateurs (User alerts in 100% theoretical 5G communes)
7. deploiement_fibre_ftth_departements (FttH fiber deployment lag vs Plan France THD)
"""

import os
import sys
import random
import subprocess
import pandas as pd
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "telecom_network_ds"
LOCATION = "US"
ARCEP_CSV_URL = "https://data.arcep.fr/mobile/sites/2026_T1/2026_T1_sites_Metropole.csv"
LOCAL_CSV_PATH = "agents/net_arch/data/arcep_sites_mobiles_metropole.csv"
BUCKET_NAME = "gs://talktodata-net-arch-raw-data"

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

DEPARTEMENTS_FTTH = [
    ("75 - Paris", "Paris", "Île-de-France", 1250000, 1260000, 99.2),
    ("69 - Rhône", "Rhône", "Auvergne-Rhône-Alpes", 890000, 920000, 96.7),
    ("13 - Bouches-du-Rhône", "Bouches-du-Rhône", "Provence-Alpes-Côte d'Azur", 910000, 980000, 92.8),
    ("31 - Haute-Garonne", "Haute-Garonne", "Occitanie", 650000, 710000, 91.5),
    ("33 - Gironde", "Gironde", "Nouvelle-Aquitaine", 780000, 890000, 87.6),
    ("59 - Nord", "Nord", "Hauts-de-France", 1100000, 1250000, 88.0),
    ("67 - Bas-Rhin", "Bas-Rhin", "Grand Est", 540000, 600000, 90.0),
    ("44 - Loire-Atlantique", "Loire-Atlantique", "Pays de la Loire", 680000, 750000, 90.6),
    ("35 - Ille-et-Vilaine", "Ille-et-Vilaine", "Bretagne", 490000, 560000, 87.5),
    ("23 - Creuse", "Creuse", "Nouvelle-Aquitaine", 38000, 68000, 55.8),
    ("48 - Lozère", "Lozère", "Occitanie", 25000, 48000, 52.1),
    ("09 - Ariège", "Ariège", "Occitanie", 52000, 95000, 54.7),
    ("15 - Cantal", "Cantal", "Auvergne-Rhône-Alpes", 42000, 82000, 51.2)
]

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

def fetch_and_clean_arcep_sites():
    print(f"Fetching official ARCEP Mon Réseau Mobile dataset from '{ARCEP_CSV_URL}'...")
    try:
        df_raw = pd.read_csv(ARCEP_CSV_URL, sep=';', nrows=10000, low_memory=False)
        print(f"  ✓ Downloaded {len(df_raw)} authentic ARCEP mobile site records.")
    except Exception as e:
        print(f"  Warning: Live ARCEP fetch error ({e}). Checking local workspace fallback...")
        if os.path.exists(LOCAL_CSV_PATH):
            df_raw = pd.read_csv(LOCAL_CSV_PATH, low_memory=False)
        else:
            raise e

    clean_sites = []
    for idx, row in df_raw.iterrows():
        anfr_id = str(row.get("id_station_anfr")) if pd.notnull(row.get("id_station_anfr")) else f"ANFR-{idx+1:07d}"
        num_st = str(row.get("num_site")) if pd.notnull(row.get("num_site")) else f"ST-{idx+1:05d}"
        op_name = str(row.get("nom_op")) if pd.notnull(row.get("nom_op")) else "Orange"
        commune = str(row.get("nom_com")) if pd.notnull(row.get("nom_com")) else "Paris"
        insee_com = str(row.get("insee_com")) if pd.notnull(row.get("insee_com")) else "75001"
        dept_name = str(row.get("nom_dep")) if pd.notnull(row.get("nom_dep")) else "75 - Paris"
        reg_name = str(row.get("nom_reg")) if pd.notnull(row.get("nom_reg")) else "Île-de-France"
        
        if commune in CITY_DEPT_REGION:
            dept_name, reg_name = CITY_DEPT_REGION[commune]

        lat = parse_float(row.get("latitude"), 48.8566)
        lon = parse_float(row.get("longitude"), 2.3522)

        s2g = bool(parse_float(row.get("site_2g"), 1) == 1)
        s3g = bool(parse_float(row.get("site_3g"), 1) == 1)
        s4g = bool(parse_float(row.get("site_4g"), 1) == 1)
        s5g = bool(parse_float(row.get("site_5g"), 0) == 1)
        s5g_3500 = bool(parse_float(row.get("site_5g_3500_m_hz"), 0) == 1)
        szb = bool(parse_float(row.get("site_ZB"), 0) == 1 or parse_float(row.get("site_DCC"), 0) == 1)

        clean_sites.append({
            "id_station_anfr": anfr_id,
            "num_site": num_st,
            "nom_operateur": op_name,
            "commune": commune,
            "code_insee_commune": insee_com,
            "code_departement": dept_name,
            "nom_region": reg_name,
            "latitude": lat,
            "longitude": lon,
            "site_2g": s2g,
            "site_3g": s3g,
            "site_4g": s4g,
            "site_5g": s5g,
            "site_5g_3500mhz": s5g_3500,
            "site_zone_blanche_dcc": szb
        })

    return pd.DataFrame(clean_sites)

def main():
    print(f"Initializing Refined NetArch Relational Pipeline for project '{PROJECT_ID}'...")
    client = get_client()

    os.makedirs("agents/net_arch/data", exist_ok=True)

    # 1. arcep_sites_mobiles_metropole
    df_sites = fetch_and_clean_arcep_sites()
    print(f"  ✓ Processed {len(df_sites)} clean ARCEP mobile site records.")

    # 2. arcep_historique_deploiement_5g
    rows_deploiement = []
    ops = ["Orange", "SFR", "Bouygues Telecom", "Free Mobile"]
    regions = list(set(df_sites["nom_region"].tolist())) if len(df_sites) > 0 else ["Île-de-France", "Auvergne-Rhône-Alpes", "Occitanie"]
    
    dates = ["2024-03-31", "2024-06-30", "2024-09-30", "2024-12-31", "2025-03-31", "2025-06-30"]
    for d in dates:
        for op in ops:
            for reg in regions:
                s700 = random.randint(150, 1200)
                s2100 = random.randint(200, 1800)
                s3500 = random.randint(100, 950)
                rows_deploiement.append({
                    "date_observation": d,
                    "nom_operateur": op,
                    "niveau_geographique": "Région",
                    "code_geographique": reg[:3].upper(),
                    "libelle_zone": reg,
                    "nb_sites_5g_700mhz": s700,
                    "nb_sites_5g_2100mhz": s2100,
                    "nb_sites_5g_3500mhz": s3500,
                    "nb_sites_5g_total": s700 + s2100 + s3500
                })

    df_deploiement = pd.DataFrame(rows_deploiement)

    # 3. telecom_qualite_service_metrique
    rows_qos = []
    cities = list(CITY_DEPT_REGION.keys())
    techs = [("5G 3.5GHz", 450.0, 65.0, 12.0), ("5G 700MHz", 180.0, 35.0, 18.0), ("4G+ LTE", 95.0, 22.0, 25.0), ("4G", 42.0, 12.0, 35.0)]

    for idx in range(1, 3501):
        commune = random.choice(cities)
        dept, region = CITY_DEPT_REGION[commune]
        op = random.choice(ops)
        t_name, dl_base, ul_base, lat_base = random.choice(techs)

        dl = round(dl_base * random.uniform(0.70, 1.35), 1)
        ul = round(ul_base * random.uniform(0.70, 1.30), 1)
        lat = round(lat_base * random.uniform(0.80, 1.40), 1)

        rows_qos.append({
            "id_mesure": f"QOS-{idx:05d}",
            "nom_operateur": op,
            "commune": commune,
            "code_departement": dept,
            "nom_region": region,
            "technologie_reseau": t_name,
            "debit_descendant_mbps": dl,
            "debit_montant_mbps": ul,
            "latence_ms": lat,
            "taux_couverture_4g_pct": round(random.uniform(94.5, 99.9), 1)
        })

    df_qos = pd.DataFrame(rows_qos)

    # 4. telecom_incidents_equipements_reseau
    rows_incidents = []
    eq_types = ["Routeur B2B Quartier", "Antenne 5G 3.5GHz", "Antenne 4G LTE", "PBO Fibre Optique", "NRO Central Enedis/SFR"]
    severities = ["Majeur - Micro-Coupures Répétées", "Moyen - Dégradation débit", "Mineur"]

    for idx in range(1, 1201):
        commune = random.choice(cities)
        dept, region = CITY_DEPT_REGION[commune]
        op = random.choice(ops)
        eq = random.choice(eq_types)
        sev = random.choice(severities)
        impacted = random.randint(150, 14500) if "Majeur" in sev else random.randint(20, 850)

        rows_incidents.append({
            "id_incident": f"INC-{idx:05d}",
            "nom_operateur": op,
            "commune": commune,
            "code_departement": dept,
            "nom_region": region,
            "type_equipement": eq,
            "severite_incident": sev,
            "nombre_abonnes_impactes": impacted,
            "statut_resolution": random.choice(["EN_COURS", "RESOLU", "INTERVENTION_EQUIPE"])
        })

    df_incidents = pd.DataFrame(rows_incidents)

    # 5. abonnes_clients_b2b_b2c (Subscribers Master: Churn B2B, Smart 5G Upsell, >80% March quota, fees, copper >150GB)
    rows_abonnes = []
    company_names = ["Thales Optronics", "Capgemini Engineering", "Sanofi Pharma", "Airbus Cyber", "Dassault Systems", "OVHcloud", "TotalEnergies IT", "Michelin Digital", "Stellantis R&D", "Atos Worldline"]
    
    for idx in range(1, 5001):
        is_b2b = (idx <= 1500)
        c_type = "B2B_PROFESSIONNEL" if is_b2b else "B2C_PARTICULIER"
        c_name = f"{random.choice(company_names)} #{idx}" if is_b2b else f"Client {random.choice(['Dupont', 'Martin', 'Bernard', 'Petit', 'Robert'])} {idx}"
        
        commune = random.choice(cities)
        dept, region = CITY_DEPT_REGION[commune]
        
        tech = random.choice(["CUIVRE_ADSL", "FIBRE_FTTH", "4G_MOBILE", "5G_MOBILE"])
        device_5g = random.choices([True, False], weights=[0.65, 0.35])[0]
        plan_5g = (tech == "5G_MOBILE") or (random.random() < 0.30 if device_5g else False)

        quota_gb = float(random.choice([50, 100, 150, 200, 300]))
        
        # High copper consumption >150GB scenario
        if tech == "CUIVRE_ADSL" and random.random() < 0.40:
            conso_gb = round(random.uniform(155.0, 380.0), 1)
        else:
            conso_gb = round(quota_gb * random.uniform(0.35, 1.25), 1)

        usage_pct = round((conso_gb / quota_gb) * 100.0, 1)
        
        # Out of plan fees if usage > 80%
        has_fees = (usage_pct > 80.0 and random.random() < 0.70)
        fees_eur = round(random.uniform(12.50, 85.00), 2) if has_fees else 0.00

        arpu_actuel = round(random.uniform(29.99, 89.99) if is_b2b else random.uniform(19.99, 44.99), 2)
        arpu_pot_5g = round(arpu_actuel + random.uniform(15.00, 35.00), 2)

        # Micro cuts & Churn B2B
        micro_cuts = random.randint(5, 28) if (is_b2b and random.random() < 0.35) else random.randint(0, 4)
        churn_risk = round(min(98.5, 20.0 + micro_cuts * 3.5 + (15.0 if usage_pct > 100 else 0)), 1)

        rows_abonnes.append({
            "id_client": f"CLI-{idx:05d}",
            "nom_client": c_name,
            "type_client": c_type,
            "technologie_actuelle": tech,
            "appareil_compatible_5g": device_5g,
            "forfait_actuel_5g": plan_5g,
            "consommation_donnees_mensuelle_gb": conso_gb,
            "quota_donnees_mensuel_gb": quota_gb,
            "taux_utilisation_quota_mars_pct": usage_pct,
            "frais_hors_forfait_eur": fees_eur,
            "arpu_mensuel_actuel_eur": arpu_actuel,
            "arpu_potentiel_5g_max_eur": arpu_pot_5g,
            "commune": commune,
            "code_departement": dept,
            "nom_region": region,
            "nb_micro_coupures_reseau_30j": micro_cuts,
            "risque_churn_pct": churn_risk
        })

    df_abonnes = pd.DataFrame(rows_abonnes)

    # 6. signalements_dysfonctionnements_utilisateurs
    rows_signalements = []
    motifs = ["Micro-coupures quotidiennes B2B", "Débit nul malgré 5G affichée 100%", "Absence de signal indoor en zone bureau"]
    
    for idx in range(1, 801):
        commune = random.choice(cities)
        dept, region = CITY_DEPT_REGION[commune]
        nb_alerts = random.randint(45, 620)
        
        rows_signalements.append({
            "id_signalement": f"SIG-{idx:04d}",
            "commune": commune,
            "code_departement": dept,
            "nom_region": region,
            "couverture_5g_theorique_pct": 100.0,
            "nombre_signalements_panne": nb_alerts,
            "type_dysfonctionnement": random.choice(motifs),
            "statut_investigation_technique": random.choice(["AUDIT_EN_COURS", "ANOMALIE_CONFIRMEE", "CORRIGE"])
        })

    df_signalements = pd.DataFrame(rows_signalements)

    # 7. deploiement_fibre_ftth_departements
    rows_ftth = []
    for dept_code, dept_name, reg_name, raccordables, totaux, pct in DEPARTEMENTS_FTTH:
        retard = round(100.0 - pct, 1)
        rows_ftth.append({
            "code_departement": dept_code,
            "nom_departement": dept_name,
            "nom_region": reg_name,
            "locaux_raccordables_ftth": raccordables,
            "locaux_totaux_departement": totaux,
            "taux_couverture_ftth_actuel_pct": pct,
            "objectif_plan_france_thd_pct": 100.0,
            "retard_deploiement_pct": retard
        })

    df_ftth = pd.DataFrame(rows_ftth)

    # Save CSVs locally and upload to BigQuery & GCS
    tables_dict = {
        "arcep_sites_mobiles_metropole": df_sites,
        "arcep_historique_deploiement_5g": df_deploiement,
        "telecom_qualite_service_metrique": df_qos,
        "telecom_incidents_equipements_reseau": df_incidents,
        "abonnes_clients_b2b_b2c": df_abonnes,
        "signalements_dysfonctionnements_utilisateurs": df_signalements,
        "deploiement_fibre_ftth_departements": df_ftth
    }

    subprocess.run(f"gcloud storage buckets create {BUCKET_NAME} --project={PROJECT_ID} --location=EU 2>/dev/null", shell=True)

    for tname, df in tables_dict.items():
        csv_file = f"agents/net_arch/data/{tname}.csv"
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

    print("\nSUCCESS: All 7 NetArch tables complete & populated in BigQuery!")

if __name__ == "__main__":
    main()
