#!/usr/bin/env python3
"""
Relational Data Generation and ARCEP Telecom OpenData Processing for NetArch (telecom_network_ds).
Populates 12 refined relational tables:
1. arcep_sites_mobiles_metropole (Official ARCEP 2G/3G/4G/5G mobile tower sites in France)
2. arcep_historique_deploiement_5g (5G deployment history by operator & frequency band)
3. telecom_qualite_service_metrique (QoS download/upload throughputs & ping latency)
4. telecom_incidents_equipements_reseau (Equipment outages, micro-cuts & SLAs)
5. catalogue_forfaits_abonnements (Reference catalog of plans: eco, student, surf, max, family, pro_flex, enterprise_unlimited)
6. abonnes_master_customers (Central subscriber CRM: B2B Pro 500GB-3TB & B2C, real names, emails, postal codes)
7. parc_equipements_sim_imei (IMEI hardware codes, IMSI SIM tag codes, ICCID & 5G SA capabilities)
8. network_traffic_flows (Partitioned GEOGRAPHY traffic flows table with IMEI, antenna, app & MB volumes)
9. maintenance_predictive_pylones (IoT sensors, CPU temp, battery health, 7-day failure probability %)
10. signalements_dysfonctionnements_utilisateurs (User alerts in 100% theoretical 5G communes)
11. deploiement_fibre_ftth_departements (FttH fiber deployment lag vs Plan France THD)
12. consommation_historique_trimestrielle_previsions (Q1 real data consumption history & Q2 predictions)
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
DATASET_ID = "telecom_network_ds"
LOCATION = "US"
ARCEP_CSV_URL = "https://data.arcep.fr/mobile/sites/2026_T1/2026_T1_sites_Metropole.csv"
LOCAL_CSV_PATH = "agents/net_arch/data/arcep_sites_mobiles_metropole.csv"
BUCKET_NAME = "gs://talktodata-net-arch-raw-data"

CITY_DEPT_REGION = {
    "Paris": ("75 - Paris", "Île-de-France", 48.8566, 2.3522, "75001"),
    "Lyon": ("69 - Rhône", "Auvergne-Rhône-Alpes", 45.7640, 4.8357, "69001"),
    "Annecy": ("74 - Haute-Savoie", "Auvergne-Rhône-Alpes", 45.8992, 6.1294, "74000"),
    "Grenoble": ("38 - Isère", "Auvergne-Rhône-Alpes", 45.1885, 5.7245, "38000"),
    "Marseille": ("13 - Bouches-du-Rhône", "Provence-Alpes-Côte d'Azur", 43.2965, 5.3698, "13001"),
    "Nice": ("06 - Alpes-Maritimes", "Provence-Alpes-Côte d'Azur", 43.7102, 7.2620, "06000"),
    "Toulouse": ("31 - Haute-Garonne", "Occitanie", 43.6047, 1.4442, "31000"),
    "Montpellier": ("34 - Hérault", "Occitanie", 43.6108, 3.8767, "34000"),
    "Bordeaux": ("33 - Gironde", "Nouvelle-Aquitaine", 44.8378, -0.5792, "33000"),
    "Lille": ("59 - Nord", "Hauts-de-France", 50.6292, 3.0573, "59000"),
    "Strasbourg": ("67 - Bas-Rhin", "Grand Est", 48.5734, 7.7521, "67000"),
    "Nantes": ("44 - Loire-Atlantique", "Pays de la Loire", 47.2184, -1.5536, "44000"),
    "Rennes": ("35 - Ille-et-Vilaine", "Bretagne", 48.1173, -1.6778, "35000")
}

FIRST_NAMES = ["Sophie", "Thomas", "Lucas", "Camille", "Élodie", "Alexandre", "Nicolas", "Julie", "Marie", "Jean", "Maxime", "Léa", "Antoine", "Chloé", "Pierre", "Manon", "Hugo", "Sarah", "Gabriel", "Inès"]
LAST_NAMES = ["Bernard", "Martin", "Moreau", "Petit", "Dubois", "Richard", "Durand", "Laurent", "Lefebvre", "Michel", "Garcia", "David", "Bertrand", "Roux", "Fournier", "Girard", "Bonnet", "Dupont"]

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

SMARTPHONES_5G = [
    ("Apple", "iPhone 15 Pro 5G", True, True),
    ("Apple", "iPhone 14 5G", True, False),
    ("Samsung", "Galaxy S24 Ultra 5G", True, True),
    ("Samsung", "Galaxy A55 5G", True, False),
    ("Google", "Pixel 8 Pro 5G", True, True),
    ("Xiaomi", "Xiaomi 13 Pro 5G", True, False),
    ("Cisco", "Routeur 5G Pro Industrial", True, True)
]

SMARTPHONES_4G = [
    ("Apple", "iPhone 11 4G", False, False),
    ("Samsung", "Galaxy A51 4G", False, False),
    ("Huawei", "P30 Pro 4G", False, False)
]

APPS_LIST = [
    ("Netflix", "Streaming 4K Video"),
    ("YouTube 4K", "Streaming 4K Video"),
    ("Microsoft Teams", "Visio Pro"),
    ("Google Meet", "Visio Pro"),
    ("TikTok", "Réseaux Sociaux"),
    ("Instagram", "Réseaux Sociaux"),
    ("Google Cloud Drive", "Cloud Storage"),
    ("Fortnite Mobile", "Gaming en Ligne")
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
            dept_name, reg_name, lat_c, lon_c, pcode = CITY_DEPT_REGION[commune]

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
    print(f"Initializing Refined NetArch 12-Table Pipeline for project '{PROJECT_ID}'...")
    client = get_client()

    os.makedirs("agents/net_arch/data", exist_ok=True)

    # Step 1: Execute DDL
    ddl_path = os.path.join(os.path.dirname(__file__), "ddl_setup.sql")
    if os.path.exists(ddl_path):
        with open(ddl_path, "r", encoding="utf-8") as f:
            sql_script = f.read().replace("${PROJECT_ID}", PROJECT_ID)
        for stmt in sql_script.split(";"):
            stmt = stmt.strip()
            if stmt:
                client.query(stmt).result()
        print("  ✓ Executed ddl_setup.sql to ensure exact telecom_network_ds schemas!")

    # 1. arcep_sites_mobiles_metropole
    df_sites = fetch_and_clean_arcep_sites()

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
        dept, region, lat_c, lon_c, pcode = CITY_DEPT_REGION[commune]
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
        dept, region, lat_c, lon_c, pcode = CITY_DEPT_REGION[commune]
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

    # 5. Table 5: catalogue_forfaits_abonnements
    plans = [
        ("bcd0ce84-2380-4b0f-b6b1-8804cfd4c3e2", "eco", 9.99, 20, 50, 2.0, False),
        ("0202ab7d-f966-4ea5-a694-88c52f4a0403", "student", 12.99, 80, 100, 1.5, False),
        ("d2546cfe-cafb-4f3b-936c-d3eba3ca61b5", "surf", 15.99, 130, 150, 1.0, False),
        ("d8e5fbf0-1264-43be-b31d-d017a7441f42", "max", 19.99, 200, 500, 1.0, True),
        ("e6bc3465-258f-4342-9477-4369d089a6d9", "family", 29.99, 300, 1000, 1.0, True),
        ("f7a9128d-1144-48cd-b12e-9901ad8991aa", "pro_flex_enterprise", 89.99, 1500, 2000, 0.5, True)
    ]
    df_plans = pd.DataFrame(plans, columns=[
        "plan_id", "plan_name", "monthly_price_eur", "data_quota_gb",
        "qos_guaranteed_throughput_mbps", "overage_rate_per_gb", "is_5g_enabled"
    ])

    # 6. Table 6: abonnes_master_customers & Table 7: parc_equipements_sim_imei & Table 8: network_traffic_flows
    rows_customers = []
    rows_hardware = []
    rows_traffic = []

    company_names = ["TotalEnergies IT Fleet", "Sanofi Pharma Digital", "OVHcloud Infrastructure", "Airbus Cyber Defense", "Capgemini Engineering", "Atos Worldline Systems", "Stellantis R&D Mobile", "Dassault Systems Telecom", "Michelin Digital Fleet", "Thales Optronics Pro"]
    anfr_site_ids = df_sites["id_station_anfr"].tolist() if len(df_sites) > 0 else [f"ANFR-000000{i}" for i in range(1, 10)]

    for idx in range(1, 5001):
        cid = f"CLI-{idx:05d}"
        is_b2b = (idx <= 1500)
        
        fn = random.choice(FIRST_NAMES)
        ln = random.choice(LAST_NAMES)
        
        if is_b2b:
            c_type = "B2B_PROFESSIONNEL"
            comp = random.choice(company_names)
            c_name = f"{comp} - {fn} {ln}"
            email = f"{fn.lower()}.{ln.lower()}@{comp.split()[0].lower()}.fr"
            siret = f"450{random.randint(10000000, 99999999)}"
        else:
            c_type = "B2C_PARTICULIER"
            c_name = f"{fn} {ln}"
            email = f"{fn.lower()}.{ln.lower()}@email-client.fr"
            siret = None

        phone = f"+336{random.randint(10000000, 99999999)}"
        commune = random.choice(cities)
        dept, region, lat_c, lon_c, pcode = CITY_DEPT_REGION[commune]

        # Realistic Professional B2B High Data Usage (500 GB to 3,500 GB / month!)
        is_5g_target = (idx <= 1800)
        if is_b2b:
            if is_5g_target:
                m_brand, m_model, dev_5g, dev_5g_sa = random.choice(SMARTPHONES_5G)
                plan_id = "d2546cfe-cafb-4f3b-936c-d3eba3ca61b5"
                plan_name = "surf"
                plan_5g = False
                quota_gb = 130.0
                # Enterprise B2B high usage: 650 Go to 2,850 Go/month!
                conso_gb = round(random.uniform(650.0, 2850.0), 1)
                usage_pct = round((conso_gb / quota_gb) * 100.0, 1)
                fees_eur = round((conso_gb - quota_gb) * 1.0, 2)
            else:
                m_brand, m_model, dev_5g, dev_5g_sa = random.choice(SMARTPHONES_5G)
                plan_id = "f7a9128d-1144-48cd-b12e-9901ad8991aa"
                plan_name = "pro_flex_enterprise"
                plan_5g = True
                quota_gb = 1500.0
                conso_gb = round(random.uniform(850.0, 3200.0), 1)
                usage_pct = round((conso_gb / quota_gb) * 100.0, 1)
                fees_eur = round(max(0.0, (conso_gb - quota_gb) * 0.5), 2)
            arpu_actuel = round(89.99 if plan_5g else 45.99, 2)
        else:
            # B2C Consumer Data Usage
            if is_5g_target:
                m_brand, m_model, dev_5g, dev_5g_sa = random.choice(SMARTPHONES_5G)
                plan_id = "d2546cfe-cafb-4f3b-936c-d3eba3ca61b5"
                plan_name = "surf"
                plan_5g = False
                quota_gb = 130.0
                usage_pct = round(random.uniform(85.0, 135.0), 1)
                conso_gb = round((quota_gb * usage_pct) / 100.0, 1)
                fees_eur = round(max(0.0, (conso_gb - quota_gb) * 1.0), 2)
            else:
                if random.random() < 0.60:
                    m_brand, m_model, dev_5g, dev_5g_sa = random.choice(SMARTPHONES_5G)
                else:
                    m_brand, m_model, dev_5g, dev_5g_sa = random.choice(SMARTPHONES_4G)
                plan_5g = (random.random() < 0.40) if dev_5g else False
                plan_id = "d8e5fbf0-1264-43be-b31d-d017a7441f42" if plan_5g else "0202ab7d-f966-4ea5-a694-88c52f4a0403"
                plan_name = "max" if plan_5g else "student"
                quota_gb = float(200 if plan_5g else 80)
                conso_gb = round(quota_gb * random.uniform(0.35, 0.95), 1)
                usage_pct = round((conso_gb / quota_gb) * 100.0, 1)
                fees_eur = 0.00
            arpu_actuel = round(19.99 if plan_5g else 15.99, 2)

        arpu_pot_5g = round(arpu_actuel + 25.00 if is_b2b else arpu_actuel + 10.00, 2)
        gain_arpu = round(arpu_pot_5g - arpu_actuel, 2)

        micro_cuts = random.randint(6, 28) if (is_b2b and random.random() < 0.35) else random.randint(0, 3)
        churn_risk = round(min(98.5, 15.0 + micro_cuts * 3.8 + (20.0 if usage_pct > 100 else 0)), 1)
        upsell_propensity = round(min(99.0, 85.0 + (10.0 if dev_5g and not plan_5g else 0.0)), 1)

        sub_date = (datetime(2023, 1, 1) + timedelta(days=random.randint(1, 600))).strftime("%Y-%m-%d")

        rows_customers.append({
            "id_client": cid,
            "nom_client": c_name,
            "email_contact": email,
            "telephone_contact": phone,
            "type_client": c_type,
            "siret_entreprise": siret,
            "plan_id": plan_id,
            "plan_name": plan_name,
            "statut_contrat": "ACTIF",
            "score_nps_satisfaction": random.randint(6, 10),
            "date_souscription": sub_date,
            "arpu_mensuel_actuel_eur": arpu_actuel,
            "arpu_potentiel_5g_max_eur": arpu_pot_5g,
            "gain_arpu_potentiel_eur": gain_arpu,
            "consommation_donnees_mensuelle_gb": conso_gb,
            "quota_donnees_mensuel_gb": quota_gb,
            "taux_utilisation_quota_mars_pct": usage_pct,
            "frais_hors_forfait_eur": fees_eur,
            "commune": commune,
            "code_departement": dept,
            "nom_region": region,
            "nb_micro_coupures_reseau_30j": micro_cuts,
            "score_risque_churn_pct": churn_risk,
            "score_propension_upsell_5g_pct": upsell_propensity
        })

        # Table 7: Hardware & SIM/IMEI Codes
        imei = f"35{random.randint(1000000000003, 9999999999999)}"
        imsi = f"20810{random.randint(1000000000, 9999999999)}"
        iccid = f"893310{random.randint(100000000000, 999999999999)}"

        rows_hardware.append({
            "id_equipement_client": f"EQP-{idx:05d}",
            "id_client": cid,
            "constructeur": m_brand,
            "modele_terminal": m_model,
            "imei": imei,
            "imsi_sim_tag_code": imsi,
            "iccid_sim_card": iccid,
            "type_carte_sim": "eSIM Virtuelle" if random.random() < 0.40 else "Nano-SIM Physique",
            "compatible_5g": dev_5g,
            "compatible_5g_standalone": dev_5g_sa,
            "annee_commercialisation": random.choice([2023, 2024, 2025]),
            "date_premiere_connexion_reseau": sub_date
        })

        # Table 8: network_traffic_flows (Exact user schema with GEOGRAPHY points)
        if idx <= 1500:
            for s_idx in range(1, 3):
                app_name, t_type = random.choice(APPS_LIST)
                u_lat = lat_c + random.uniform(-0.02, 0.02)
                u_lon = lon_c + random.uniform(-0.02, 0.02)
                wkt_point = f"POINT({u_lon:.4f} {u_lat:.4f})"
                ts_str = f"2025-03-{random.randint(1,28):02d} {random.randint(8,22):02d}:{random.randint(0,59):02d}:00"

                rows_traffic.append({
                    "flow_id": f"FLOW-{idx:05d}-{s_idx}",
                    "imei": imei,
                    "antenna_id": random.choice(anfr_site_ids),
                    "timestamp": ts_str,
                    "application_name": app_name,
                    "traffic_type": t_type,
                    "volume_mb_uplink": round(random.uniform(15.0, 850.0) if is_b2b else random.uniform(2.0, 150.0), 2),
                    "volume_mb_downlink": round(random.uniform(450.0, 14800.0) if is_b2b else random.uniform(25.0, 1850.0), 2),
                    "user_location": wkt_point,
                    "latency_ms": random.randint(12, 65),
                    "postal_code": pcode
                })

    df_customers = pd.DataFrame(rows_customers)
    df_hardware = pd.DataFrame(rows_hardware)
    df_traffic = pd.DataFrame(rows_traffic)

    # 7. Table 9: maintenance_predictive_pylones
    rows_maint = []
    for idx, anfr_id in enumerate(anfr_site_ids[:300]):
        commune = random.choice(cities)
        dept, region, lat_c, lon_c, pcode = CITY_DEPT_REGION[commune]
        op = random.choice(ops)
        cpu_temp = round(random.uniform(42.0, 88.5), 1)
        cpu_load = round(random.uniform(25.0, 96.0), 1)
        prob_fail = round(min(98.0, max(2.0, (cpu_temp - 50.0) * 1.8 + (cpu_load - 50.0) * 0.9)), 1)
        comp = random.choice(["Carte Alimentation DC", "Ventilateur Baie 3.5GHz", "Module Optique SFP+ 10G", "Liaison FH Réalignement"]) if prob_fail > 60.0 else "Aucun (Normal)"

        rows_maint.append({
            "id_pylone_sensor": f"SNS-{idx+1:04d}",
            "id_station_anfr": anfr_id,
            "nom_operateur": op,
            "commune": commune,
            "temperature_processeur_c": cpu_temp,
            "charge_cpu_pct": cpu_load,
            "stabilite_tension_volts": round(random.uniform(47.2, 48.8), 2),
            "etat_sante_batterie_secours_pct": round(random.uniform(65.0, 100.0), 1),
            "vibration_mat_mm": round(random.uniform(0.1, 4.2), 2),
            "probabilite_panne_7j_pct": prob_fail,
            "composant_a_remplacer_prioritaire": comp
        })
    df_maint = pd.DataFrame(rows_maint)

    # 8. signalements_dysfonctionnements_utilisateurs
    rows_signalements = []
    motifs = ["Micro-coupures quotidiennes B2B", "Débit nul malgré 5G affichée 100%", "Absence de signal indoor en zone bureau"]
    for idx in range(1, 801):
        commune = random.choice(cities)
        dept, region, lat_c, lon_c, pcode = CITY_DEPT_REGION[commune]
        rows_signalements.append({
            "id_signalement": f"SIG-{idx:04d}",
            "commune": commune,
            "code_departement": dept,
            "nom_region": region,
            "couverture_5g_theorique_pct": 100.0,
            "nombre_signalements_panne": random.randint(45, 620),
            "type_dysfonctionnement": random.choice(motifs),
            "statut_investigation_technique": random.choice(["AUDIT_EN_COURS", "ANOMALIE_CONFIRMEE", "CORRIGE"])
        })
    df_signalements = pd.DataFrame(rows_signalements)

    # 9. deploiement_fibre_ftth_departements
    rows_ftth = []
    for dept_code, dept_name, reg_name, raccordables, totaux, pct in DEPARTEMENTS_FTTH:
        rows_ftth.append({
            "code_departement": dept_code,
            "nom_departement": dept_name,
            "nom_region": reg_name,
            "locaux_raccordables_ftth": raccordables,
            "locaux_totaux_departement": totaux,
            "taux_couverture_ftth_actuel_pct": pct,
            "objectif_plan_france_thd_pct": 100.0,
            "retard_deploiement_pct": round(100.0 - pct, 1)
        })
    df_ftth = pd.DataFrame(rows_ftth)

    # 10. consommation_historique_trimestrielle_previsions
    rows_forecast = [
        {"periode_id": "PER-2025-01", "mois_label": "Janvier 2025", "trimestre": "Q1 2025", "est_prevision": False, "consommation_moyenne_par_abonne_go": 450.5, "consommation_totale_reseau_tb": 48500.0, "taux_croissance_mensuel_pct": 5.2},
        {"periode_id": "PER-2025-02", "mois_label": "Février 2025", "trimestre": "Q1 2025", "est_prevision": False, "consommation_moyenne_par_abonne_go": 520.8, "consommation_totale_reseau_tb": 56200.0, "taux_croissance_mensuel_pct": 15.6},
        {"periode_id": "PER-2025-03", "mois_label": "Mars 2025", "trimestre": "Q1 2025", "est_prevision": False, "consommation_moyenne_par_abonne_go": 610.2, "consommation_totale_reseau_tb": 68100.0, "taux_croissance_mensuel_pct": 17.1},
        {"periode_id": "PER-2025-04", "mois_label": "Avril 2025 (Prévision)", "trimestre": "Q2 2025", "est_prevision": True, "consommation_moyenne_par_abonne_go": 720.0, "consommation_totale_reseau_tb": 79200.0, "taux_croissance_mensuel_pct": 18.0},
        {"periode_id": "PER-2025-05", "mois_label": "Mai 2025 (Prévision)", "trimestre": "Q2 2025", "est_prevision": True, "consommation_moyenne_par_abonne_go": 850.5, "consommation_totale_reseau_tb": 92500.0, "taux_croissance_mensuel_pct": 18.1},
        {"periode_id": "PER-2025-06", "mois_label": "Juin 2025 (Prévision)", "trimestre": "Q2 2025", "est_prevision": True, "consommation_moyenne_par_abonne_go": 980.0, "consommation_totale_reseau_tb": 108100.0, "taux_croissance_mensuel_pct": 15.2}
    ]
    df_forecast = pd.DataFrame(rows_forecast)

    # Save CSVs locally and upload to BigQuery & GCS
    tables_dict = {
        "arcep_sites_mobiles_metropole": df_sites,
        "arcep_historique_deploiement_5g": df_deploiement,
        "telecom_qualite_service_metrique": df_qos,
        "telecom_incidents_equipements_reseau": df_incidents,
        "catalogue_forfaits_abonnements": df_plans,
        "abonnes_master_customers": df_customers,
        "parc_equipements_sim_imei": df_hardware,
        "network_traffic_flows": df_traffic,
        "maintenance_predictive_pylones": df_maint,
        "signalements_dysfonctionnements_utilisateurs": df_signalements,
        "deploiement_fibre_ftth_departements": df_ftth,
        "consommation_historique_trimestrielle_previsions": df_forecast
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

    print("\nSUCCESS: All 12 NetArch tables complete & populated in BigQuery!")

if __name__ == "__main__":
    main()
