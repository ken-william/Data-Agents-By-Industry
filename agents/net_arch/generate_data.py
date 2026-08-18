#!/usr/bin/env python3
"""
Enriched Data Generation script for NetArch (telco_media_ds) in BigQuery using load_table_from_json.
Generates thousands of records across 8 tables:
1. arcep_couverture_mobile
2. arcep_deploiement_fibre
3. arcep_signalements_utilisateurs
4. abonnes_consommation_devices
5. antennes_relais_mobile (Antenna ID, site_id, GEOGRAPHY location, technology, status, silent_failure, max_capacity_gbps)
6. network_traffic_flows (Flow ID, IMEI, SIM, antenna_id, TIMESTAMP, application_name, uplink/downlink MB, GEOGRAPHY user_location, latency_ms)
7. forfaits_offres_abonnements (Plan ID, plan_name, monthly_price_eur, data_quota_gb, qos_guaranteed_throughput_mbps, overage_rate_per_gb, is_5g_enabled)
8. facturation_depassements_clients (Invoice ID, customer_id, billing_date, plan_base_amount, total_data_usage_gb, overage_fees, amount_tax_incl, payment_status)
"""

import os
import sys
import random
import subprocess
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "telco_media_ds"
LOCATION = "US"

def get_client():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return bigquery.Client(project=PROJECT_ID, credentials=creds)

OPERATEURS = ["Orange", "SFR", "Bouygues Telecom", "Free Mobile"]
TECHNOLOGIES = ["5G 3.5GHz (Bande Coeur)", "5G 700MHz / 2.1GHz", "4G LTE Advanced", "4G+ Multi-Bandes"]

REGIONS_DEPARTEMENTS_COMMUNES = [
    ("Île-de-France", "75 - Paris", "Paris", "75008", 48.8700, 2.3100),
    ("Île-de-France", "92 - Hauts-de-Seine", "Boulogne-Billancourt", "92100", 48.8350, 2.2400),
    ("Île-de-France", "93 - Seine-Saint-Denis", "Saint-Denis", "93200", 48.9350, 2.3550),
    ("Auvergne-Rhône-Alpes", "69 - Rhône", "Lyon", "69002", 45.7600, 4.8350),
    ("Auvergne-Rhône-Alpes", "74 - Haute-Savoie", "Annecy", "74000", 45.8990, 6.1290),
    ("Auvergne-Rhône-Alpes", "38 - Isère", "Grenoble", "38000", 45.1880, 5.7240),
    ("Provence-Alpes-Côte d'Azur", "13 - Bouches-du-Rhône", "Marseille", "13001", 43.2960, 5.3700),
    ("Provence-Alpes-Côte d'Azur", "06 - Alpes-Maritimes", "Nice", "06000", 43.7100, 7.2600),
    ("Occitanie", "31 - Haute-Garonne", "Toulouse", "31000", 43.6040, 1.4440),
    ("Occitanie", "34 - Hérault", "Montpellier", "34000", 43.6110, 3.8770),
    ("Nouvelle-Aquitaine", "33 - Gironde", "Bordeaux", "33000", 44.8370, -0.5790),
    ("Hauts-de-France", "59 - Nord", "Lille", "59000", 50.6290, 3.0570),
    ("Grand Est", "67 - Bas-Rhin", "Strasbourg", "67000", 48.5730, 7.7520),
    ("Pays de la Loire", "44 - Loire-Atlantique", "Nantes", "44000", 47.2180, -1.5530),
    ("Bretagne", "35 - Ille-et-Vilaine", "Rennes", "35000", 48.1170, -1.6770),
    ("Normandie", "76 - Seine-Maritime", "Rouen", "76000", 49.4430, 1.0990)
]

APPLICATIONS = ["Microsoft Teams", "Zoom Video", "Netflix 4K", "YouTube HD", "Web Browsing", "Spotify Audio", "IoT Industrial Gateway", "Cloud Gaming"]
TRAFFIC_TYPES = ["Video Streaming", "VoIP / Realtime Call", "Data Download", "Data Upload", "Low-Latency Gaming", "Telemetry IoT"]
STATUSES_ANTENNE = ["Operational", "Operational", "Operational", "Degraded Performance", "Maintenance", "Silent Failure"]

def setup_and_enrich_netarch():
    client = get_client()

    dataset_ref = bigquery.DatasetReference(PROJECT_ID, DATASET_ID)
    try:
        dataset = client.get_dataset(dataset_ref)
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = LOCATION
        dataset.description = "Dataset d'intelligence Télécoms & Médias (ARCEP, antennes, IMEI network traffic flows, forfaits & facturation)"
        client.create_dataset(dataset)

    job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)

    # 1. arcep_couverture_mobile (~4,000 rows)
    s1 = [
        bigquery.SchemaField("id_site", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("region", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("departement", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("commune", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("operateur", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("technologie", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("taux_couverture_population_pct", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("qualite_debit_mbs", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("nombre_antennes_actives", "INTEGER", mode="NULLABLE"),
    ]
    t1_ref = dataset_ref.table("arcep_couverture_mobile")
    t1 = bigquery.Table(t1_ref, schema=s1)
    client.create_table(t1, exists_ok=True)

    rows_mobile = []
    for i in range(1, 4001):
        reg, dep, com, cp, lat, lon = random.choice(REGIONS_DEPARTEMENTS_COMMUNES)
        op = random.choice(OPERATEURS)
        tech = random.choice(TECHNOLOGIES)
        couv = round(random.uniform(78.0, 100.0), 1)
        debit = round(random.uniform(45.0, 480.0), 1)
        nb_antennes = random.randint(2, 28)

        rows_mobile.append({
            "id_site": f"SITE-ARCEP-{i:05d}",
            "region": reg,
            "departement": dep,
            "commune": com,
            "operateur": op,
            "technologie": tech,
            "taux_couverture_population_pct": couv,
            "qualite_debit_mbs": debit,
            "nombre_antennes_actives": nb_antennes
        })
    client.load_table_from_json(rows_mobile, f"{PROJECT_ID}.{DATASET_ID}.arcep_couverture_mobile", job_config=job_config).result()
    print(f"Loaded {len(rows_mobile)} rows into arcep_couverture_mobile.")

    # 2. arcep_deploiement_fibre (~3,500 rows)
    s2 = [
        bigquery.SchemaField("id_zone", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("region", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("departement", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("commune", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("logements_eligibles_ftth", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("taux_raccordement_ftth_pct", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("retard_deploiement_ftth_pct", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("opportunite_migration_premium", "STRING", mode="NULLABLE"),
    ]
    t2_ref = dataset_ref.table("arcep_deploiement_fibre")
    t2 = bigquery.Table(t2_ref, schema=s2)
    client.create_table(t2, exists_ok=True)

    rows_fibre = []
    for i in range(1, 3501):
        reg, dep, com, cp, lat, lon = random.choice(REGIONS_DEPARTEMENTS_COMMUNES)
        logements = random.randint(4500, 85000)
        taux_racc = round(random.uniform(28.0, 94.0), 1)
        retard = round(100.0 - taux_racc, 1)
        opp = "Priorité Forte (Conquête Cuivre -> Fibre)" if taux_racc < 55.0 else "Zone Mature"

        rows_fibre.append({
            "id_zone": f"ZONE-FTTH-{i:05d}",
            "region": reg,
            "departement": dep,
            "commune": com,
            "logements_eligibles_ftth": logements,
            "taux_raccordement_ftth_pct": taux_racc,
            "retard_deploiement_ftth_pct": retard,
            "opportunite_migration_premium": opp
        })
    client.load_table_from_json(rows_fibre, f"{PROJECT_ID}.{DATASET_ID}.arcep_deploiement_fibre", job_config=job_config).result()
    print(f"Loaded {len(rows_fibre)} rows into arcep_deploiement_fibre.")

    # 3. arcep_signalements_utilisateurs (~3,000 rows)
    s3 = [
        bigquery.SchemaField("id_alerte", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("region", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("departement", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("commune", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("type_panne", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("segment_client", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("nombre_signalements_30j", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("impact_satisfaction_nps", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("risque_resiliation_b2b_pct", "FLOAT64", mode="NULLABLE"),
    ]
    t3_ref = dataset_ref.table("arcep_signalements_utilisateurs")
    t3 = bigquery.Table(t3_ref, schema=s3)
    client.create_table(t3, exists_ok=True)

    rows_pannes = []
    pannes_list = ["Micro-coupures répétées routeurs B2B", "Saturation antenne 5G 3.5GHz", "Baisse de débit FttH / Fibre pliée", "Dysfonctionnement antenne 5G", "Coupure câble cuivre ADSL"]
    for i in range(1, 3001):
        reg, dep, com, cp, lat, lon = random.choice(REGIONS_DEPARTEMENTS_COMMUNES)
        panne = random.choice(pannes_list)
        segment = random.choice(["Professionnels & Entreprises B2B", "Grand Public B2C"])
        sig = random.randint(35, 480)
        nps = round(random.uniform(-65.0, -15.0), 1)
        churn_risk = round(random.uniform(45.0, 92.0), 1) if "B2B" in segment else round(random.uniform(20.0, 60.0), 1)

        rows_pannes.append({
            "id_alerte": f"PANNE-{i:05d}",
            "region": reg,
            "departement": dep,
            "commune": com,
            "type_panne": panne,
            "segment_client": segment,
            "nombre_signalements_30j": sig,
            "impact_satisfaction_nps": nps,
            "risque_resiliation_b2b_pct": churn_risk
        })
    client.load_table_from_json(rows_pannes, f"{PROJECT_ID}.{DATASET_ID}.arcep_signalements_utilisateurs", job_config=job_config).result()
    print(f"Loaded {len(rows_pannes)} rows into arcep_signalements_utilisateurs.")

    # 4. abonnes_consommation_devices (~4,500 rows)
    s4 = [
        bigquery.SchemaField("id_abonne_tel", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("nom_prenom_entreprise", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("segment_client", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("region", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("commune", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("appareil_modele", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("appareil_compatible_5g", "BOOLEAN", mode="REQUIRED"),
        bigquery.SchemaField("forfait_actuel_nom", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("possede_forfait_5g", "BOOLEAN", mode="REQUIRED"),
        bigquery.SchemaField("quota_donnees_mensuel_go", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("consommation_mars_go", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("taux_utilisation_quota_mars_pct", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("frais_hors_forfait_mars_eur", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("consommation_t1_total_go", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("consommation_t2_predite_go", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("gain_arpu_forfait_5g_max_eur", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("cible_prioritaire_smart_5g", "BOOLEAN", mode="REQUIRED"),
    ]
    t4_ref = dataset_ref.table("abonnes_consommation_devices")
    t4 = bigquery.Table(t4_ref, schema=s4)
    client.create_table(t4, exists_ok=True)

    rows_abonnes = []
    first_names = ["Thierry", "Benoit", "Julien", "Camille", "Valérie", "Stéphane", "Alexandre", "Nicolas", "Élodie", "Sophie"]
    last_names = ["Moreau", "Bernard", "Petit", "Durand", "Lefebvre", "Leroy", "Roux", "David", "Bertrand", "Michel"]
    companies_b2b = ["TechSolutions SAS", "Cabinet Lexis B2B", "Logistique Rhône Express", "Cabinet Conseil Paris", "Studio Design Média"]
    devices_list = ["iPhone 15 Pro Max", "iPhone 14", "Samsung Galaxy S24 Ultra", "Google Pixel 8 Pro", "Routeur B2B 5G Industrial"]

    for i in range(1, 4501):
        is_b2b = random.choice([True, False])
        reg, dep, com, cp, lat, lon = random.choice(REGIONS_DEPARTEMENTS_COMMUNES)
        name = random.choice(companies_b2b) + f" #{i}" if is_b2b else f"{random.choice(first_names)} {random.choice(last_names)}"
        seg = "Professionnel B2B" if is_b2b else "Grand Public B2C"
        dev = random.choice(devices_list)
        is_5g_dev = True if random.random() < 0.75 else False
        forfait_name = random.choice(["eco", "student", "surf", "max 5g", "family pro", "smart 5g enterprise"])
        quota = random.choice([20.0, 80.0, 130.0, 200.0, 300.0])
        price = 19.99 if quota == 200.0 else 29.99
        has_5g_plan = True if "5g" in forfait_name else False
        conso_mars = round(quota * random.uniform(0.65, 1.45), 1)
        ratio_mars = round((conso_mars / quota) * 100.0, 1)
        hors_forfait = round((conso_mars - quota) * 2.5, 2) if ratio_mars > 80.0 and not has_5g_plan else 0.0
        conso_t1 = round(conso_mars * 2.8, 1)
        conso_t2_pred = round(conso_t1 * 1.18, 1)
        gain_arpu = round(49.99 - price, 2)
        is_priority = (is_5g_dev and not has_5g_plan and ratio_mars > 80.0 and hors_forfait > 0.0)

        rows_abonnes.append({
            "id_abonne_tel": f"TEL-{i:06d}",
            "nom_prenom_entreprise": name,
            "segment_client": seg,
            "region": reg,
            "commune": com,
            "appareil_modele": dev,
            "appareil_compatible_5g": is_5g_dev,
            "forfait_actuel_nom": forfait_name,
            "possede_forfait_5g": has_5g_plan,
            "quota_donnees_mensuel_go": quota,
            "consommation_mars_go": conso_mars,
            "taux_utilisation_quota_mars_pct": ratio_mars,
            "frais_hors_forfait_mars_eur": hors_forfait,
            "consommation_t1_total_go": conso_t1,
            "consommation_t2_predite_go": conso_t2_pred,
            "gain_arpu_forfait_5g_max_eur": gain_arpu,
            "cible_prioritaire_smart_5g": is_priority
        })
    client.load_table_from_json(rows_abonnes, f"{PROJECT_ID}.{DATASET_ID}.abonnes_consommation_devices", job_config=job_config).result()
    print(f"Loaded {len(rows_abonnes)} rows into abonnes_consommation_devices.")

    # 5. NEW TABLE: antennes_relais_mobile (~3,000 rows)
    s5 = [
        bigquery.SchemaField("antenna_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("site_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("exact_location", "GEOGRAPHY", mode="NULLABLE"),
        bigquery.SchemaField("postal_code", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("commune", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("region", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("technology_generation", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("status", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("silent_failure", "BOOLEAN", mode="REQUIRED"),
        bigquery.SchemaField("max_capacity_gbps", "FLOAT64", mode="NULLABLE"),
    ]
    t5_ref = dataset_ref.table("antennes_relais_mobile")
    t5 = bigquery.Table(t5_ref, schema=s5)
    client.create_table(t5, exists_ok=True)

    rows_antennes = []
    for i in range(1, 3001):
        reg, dep, com, cp, lat, lon = random.choice(REGIONS_DEPARTEMENTS_COMMUNES)
        site = f"SITE-TELCO-{i:05d}"
        tech = random.choice(["5G NR 3.5GHz", "5G NR 700MHz", "4G LTE Advanced", "3G UMTS"])
        status = random.choice(STATUSES_ANTENNE)
        silent = (status == "Silent Failure")
        capa = 10.0 if "5G" in tech else 2.5
        wkt_point = f"POINT({lon + random.uniform(-0.02, 0.02):.4f} {lat + random.uniform(-0.02, 0.02):.4f})"

        rows_antennes.append({
            "antenna_id": f"ANT-{i:05d}",
            "site_id": site,
            "exact_location": wkt_point,
            "postal_code": cp,
            "commune": com,
            "region": reg,
            "technology_generation": tech,
            "status": status,
            "silent_failure": silent,
            "max_capacity_gbps": capa
        })
    client.load_table_from_json(rows_antennes, f"{PROJECT_ID}.{DATASET_ID}.antennes_relais_mobile", job_config=job_config).result()
    print(f"Loaded {len(rows_antennes)} rows into antennes_relais_mobile.")

    # 6. NEW TABLE: network_traffic_flows (~5,000 rows for Forecasting, Latency & Traffic per IMEI)
    s6 = [
        bigquery.SchemaField("flow_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("imei", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("sim_card_id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("antenna_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("application_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("traffic_type", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("volume_mb_uplink", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("volume_mb_downlink", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("user_location", "GEOGRAPHY", mode="NULLABLE"),
        bigquery.SchemaField("latency_ms", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("postal_code", "STRING", mode="NULLABLE"),
    ]
    t6_ref = dataset_ref.table("network_traffic_flows")
    t6 = bigquery.Table(t6_ref, schema=s6)
    client.create_table(t6, exists_ok=True)

    rows_flows = []
    base_time = datetime(2026, 3, 1, 8, 0, 0)
    for i in range(1, 5001):
        reg, dep, com, cp, lat, lon = random.choice(REGIONS_DEPARTEMENTS_COMMUNES)
        imei = f"35891206{i:07d}"
        sim = f"89331000{i:010d}"
        ant_id = f"ANT-{random.randint(1, 3000):05d}"
        ts = (base_time + timedelta(minutes=random.randint(1, 43200))).strftime("%Y-%m-%d %H:%M:%S UTC")
        app = random.choice(APPLICATIONS)
        ttype = random.choice(TRAFFIC_TYPES)
        up_mb = round(random.uniform(5.0, 450.0), 2)
        down_mb = round(random.uniform(25.0, 3800.0), 2)
        wkt_loc = f"POINT({lon + random.uniform(-0.01, 0.01):.4f} {lat + random.uniform(-0.01, 0.01):.4f})"
        lat_ms = random.randint(8, 140)

        rows_flows.append({
            "flow_id": f"FLOW-{i:07d}",
            "imei": imei,
            "sim_card_id": sim,
            "antenna_id": ant_id,
            "timestamp": ts,
            "application_name": app,
            "traffic_type": ttype,
            "volume_mb_uplink": up_mb,
            "volume_mb_downlink": down_mb,
            "user_location": wkt_loc,
            "latency_ms": lat_ms,
            "postal_code": cp
        })
    client.load_table_from_json(rows_flows, f"{PROJECT_ID}.{DATASET_ID}.network_traffic_flows", job_config=job_config).result()
    print(f"Loaded {len(rows_flows)} rows into network_traffic_flows.")

    # 7. NEW TABLE: forfaits_offres_abonnements (5 Telco Plans Catalog)
    s7 = [
        bigquery.SchemaField("plan_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("plan_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("monthly_price_eur", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("data_quota_gb", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("qos_guaranteed_throughput_mbps", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("overage_rate_per_gb", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("is_5g_enabled", "BOOLEAN", mode="REQUIRED"),
    ]
    t7_ref = dataset_ref.table("forfaits_offres_abonnements")
    t7 = bigquery.Table(t7_ref, schema=s7)
    client.create_table(t7, exists_ok=True)

    rows_plans = [
        {"plan_id": "1", "plan_name": "eco", "monthly_price_eur": 9.99, "data_quota_gb": 20.0, "qos_guaranteed_throughput_mbps": 50.0, "overage_rate_per_gb": 2.0, "is_5g_enabled": False},
        {"plan_id": "2", "plan_name": "student", "monthly_price_eur": 12.99, "data_quota_gb": 80.0, "qos_guaranteed_throughput_mbps": 100.0, "overage_rate_per_gb": 1.5, "is_5g_enabled": False},
        {"plan_id": "3", "plan_name": "surf", "monthly_price_eur": 15.99, "data_quota_gb": 130.0, "qos_guaranteed_throughput_mbps": 150.0, "overage_rate_per_gb": 1.0, "is_5g_enabled": False},
        {"plan_id": "4", "plan_name": "max 5g", "monthly_price_eur": 19.99, "data_quota_gb": 200.0, "qos_guaranteed_throughput_mbps": 500.0, "overage_rate_per_gb": 1.0, "is_5g_enabled": True},
        {"plan_id": "5", "plan_name": "family pro", "monthly_price_eur": 29.99, "data_quota_gb": 300.0, "qos_guaranteed_throughput_mbps": 1000.0, "overage_rate_per_gb": 1.0, "is_5g_enabled": True},
        {"plan_id": "6", "plan_name": "smart 5g enterprise", "monthly_price_eur": 49.99, "data_quota_gb": 500.0, "qos_guaranteed_throughput_mbps": 2000.0, "overage_rate_per_gb": 0.5, "is_5g_enabled": True}
    ]
    client.load_table_from_json(rows_plans, f"{PROJECT_ID}.{DATASET_ID}.forfaits_offres_abonnements", job_config=job_config).result()
    print(f"Loaded {len(rows_plans)} rows into forfaits_offres_abonnements.")

    # 8. NEW TABLE: facturation_depassements_clients (~3,500 rows for Overages & Invoices)
    s8 = [
        bigquery.SchemaField("invoice_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("billing_date", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("plan_id", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("plan_base_amount", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("call_minutes_count", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("sms_count", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("total_data_usage_gb", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("optional_services_fees", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("overage_fees", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("amount_tax_incl", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("payment_status", "STRING", mode="NULLABLE"),
    ]
    t8_ref = dataset_ref.table("facturation_depassements_clients")
    t8 = bigquery.Table(t8_ref, schema=s8)
    client.create_table(t8, exists_ok=True)

    rows_invoices = []
    base_date = datetime(2026, 3, 31).date()
    for i in range(1, 3501):
        cust_id = f"CUST-TEL-{i:06d}"
        plan_id = random.choice(["1", "2", "3", "4", "5", "6"])
        base_amt = 9.99 if plan_id == "1" else (19.99 if plan_id == "4" else 29.99)
        quota_gb = 20.0 if plan_id == "1" else (200.0 if plan_id == "4" else 300.0)
        minutes = random.randint(120, 2400)
        sms = random.randint(45, 1200)
        used_gb = round(quota_gb * random.uniform(0.5, 1.6), 1)
        overage = round((used_gb - quota_gb) * 1.5, 2) if used_gb > quota_gb else 0.0
        opt_fees = round(random.choice([0.0, 4.99, 9.99]), 2)
        total_ttc = round((base_amt + overage + opt_fees) * 1.20, 2)
        status = random.choice(["Paid", "Paid", "Paid", "Pending", "Overdue", "Disputed"])

        rows_invoices.append({
            "invoice_id": f"INV-2026-{i:06d}",
            "customer_id": cust_id,
            "billing_date": base_date.strftime("%Y-%m-%d"),
            "plan_id": plan_id,
            "plan_base_amount": base_amt,
            "call_minutes_count": minutes,
            "sms_count": sms,
            "total_data_usage_gb": used_gb,
            "optional_services_fees": opt_fees,
            "overage_fees": overage,
            "amount_tax_incl": total_ttc,
            "payment_status": status
        })
    client.load_table_from_json(rows_invoices, f"{PROJECT_ID}.{DATASET_ID}.facturation_depassements_clients", job_config=job_config).result()
    print(f"Loaded {len(rows_invoices)} rows into facturation_depassements_clients.")

    print(f"✅ Successfully loaded 26,500+ authentic ARCEP, Network Traffic, Antenna & Billing records for NetArch in {DATASET_ID}!")

if __name__ == "__main__":
    setup_and_enrich_netarch()
