#!/usr/bin/env python3
"""
Mass Data Generation script for ArenaManager dataset (sports_infrastructure_ds) in BigQuery using load_table_from_json.
Generates thousands of realistic records across 4 tables:
1. ministere_sports_equipements (Complexes, Energy consumption MWh, kWh/m2 waste, Weekday utilization %, Premium sponsorship status)
2. ministere_sports_licencies (Federations, Youth <18 %, Annual growth %, Premium stadium ads potential)
3. ministere_sports_subventions (ANS Subsidies, Grant amounts €, Impact on youth registration %, Efficiency ratio)
4. ministere_sports_desequilibre_territoires (Demographic growth %, Approved facilities gap, Missing equipment recommendations)
"""

import os
import sys
import random
import subprocess
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "sports_infrastructure_ds"
LOCATION = "US"

def get_client():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return bigquery.Client(project=PROJECT_ID, credentials=creds)

TYPES_EQUIPEMENTS = [
    ("Piscine Couverte 50m / Complexe Aquatique", 1200.0),
    ("Gymnase Polyvalent Municipal", 450.0),
    ("Stade d'Athlétisme & Football", 850.0),
    ("Dojo Régional de Judo & Arts Martiaux", 320.0),
    ("Complexe de Tennis Couvert", 280.0),
    ("Palais des Sports & Arena Municipal", 2100.0)
]

FEDERATIONS = [
    "Fédération Française de Natation",
    "Fédération Française de Football",
    "Fédération Française de Tennis",
    "Fédération Française de Judo & Arts Martiaux",
    "Fédération Française de Basket-Ball",
    "Fédération Française de Handball",
    "Fédération Française de Rugby"
]

REGIONS_DEPARTEMENTS_COMMUNES = [
    ("Auvergne-Rhône-Alpes", "69 - Rhône", "Lyon"),
    ("Auvergne-Rhône-Alpes", "74 - Haute-Savoie", "Annecy"),
    ("Auvergne-Rhône-Alpes", "38 - Isère", "Grenoble"),
    ("Île-de-France", "75 - Paris", "Paris"),
    ("Île-de-France", "93 - Seine-Saint-Denis", "Saint-Denis"),
    ("Île-de-France", "92 - Hauts-de-Seine", "Boulogne-Billancourt"),
    ("Provence-Alpes-Côte d'Azur", "13 - Bouches-du-Rhône", "Marseille"),
    ("Provence-Alpes-Côte d'Azur", "06 - Alpes-Maritimes", "Nice"),
    ("Occitanie", "31 - Haute-Garonne", "Toulouse"),
    ("Occitanie", "34 - Hérault", "Montpellier"),
    ("Nouvelle-Aquitaine", "33 - Gironde", "Bordeaux"),
    ("Hauts-de-France", "59 - Nord", "Lille"),
    ("Grand Est", "67 - Bas-Rhin", "Strasbourg"),
    ("Pays de la Loire", "44 - Loire-Atlantique", "Nantes"),
    ("Bretagne", "35 - Ille-et-Vilaine", "Rennes"),
    ("Normandie", "76 - Seine-Maritime", "Rouen")
]

PROJETS_SUBVENTIONS = [
    "Isolation Thermique & Pompes à Chaleur Géothermiques",
    "Installation Éclairage LED & Ombrage Photovoltaïque",
    "Renouvellement Bassins & Récupération d'Eau de Pluie",
    "Modernisation Vestiaires & Accessibilité PMR",
    "Création Dojo Municipal Polyvalent & Terrain Synthétique"
]

def setup_and_enrich_arenamanager():
    client = get_client()

    dataset_ref = bigquery.DatasetReference(PROJECT_ID, DATASET_ID)
    try:
        dataset = client.get_dataset(dataset_ref)
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = LOCATION
        dataset.description = "Dataset du Recensement des Équipements Sportifs (RES), licenciés et subventions pour ArenaManager"
        client.create_dataset(dataset)

    job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)

    # 1. ministere_sports_equipements (~3,500 rows)
    s1 = [
        bigquery.SchemaField("id_equipement", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("nom_equipement", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("type_equipement", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("region", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("departement", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("commune", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("etat_vetuste", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("consommation_energetique_annuelle_mwh", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("gaspillage_kwh_par_m2", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("taux_utilisation_semaine_pct", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("statut_homologation_officielle", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("alerte_gaspillage_energetique", "BOOLEAN", mode="REQUIRED"),
    ]
    t1_ref = dataset_ref.table("ministere_sports_equipements")
    t1 = bigquery.Table(t1_ref, schema=s1)
    client.create_table(t1, exists_ok=True)

    t1_id = f"{PROJECT_ID}.{DATASET_ID}.ministere_sports_equipements"
    rows_equip = []

    for i in range(1, 3501):
        reg, dep, com = random.choice(REGIONS_DEPARTEMENTS_COMMUNES)
        eq_type, base_mwh = random.choice(TYPES_EQUIPEMENTS)
        name = f"{eq_type} {com} #{i}"
        vetuste = random.choice(["Moderne & Rénové", "Satisfaisant", "Vétuste (Consommation Anormale)"])
        mwh = round(base_mwh * random.uniform(0.7, 1.8), 1)
        kwh_m2 = round(mwh * random.uniform(0.18, 0.45), 1)
        usage_semaine = round(random.uniform(15.0, 92.0), 1)
        homolog = random.choice(["Homologué Niveau National", "Homologué Niveau Régional", "En Attente de Mise aux Normes"])
        is_waste = (usage_semaine < 30.0 and kwh_m2 > 120.0)

        rows_equip.append({
            "id_equipement": f"EQ-RES-{i:05d}",
            "nom_equipement": name,
            "type_equipement": eq_type,
            "region": reg,
            "departement": dep,
            "commune": com,
            "etat_vetuste": vetuste,
            "consommation_energetique_annuelle_mwh": mwh,
            "gaspillage_kwh_par_m2": kwh_m2,
            "taux_utilisation_semaine_pct": usage_semaine,
            "statut_homologation_officielle": homolog,
            "alerte_gaspillage_energetique": is_waste
        })

    job1 = client.load_table_from_json(rows_equip, t1_id, job_config=job_config)
    job1.result()
    print(f"Loaded {len(rows_equip)} rows into ministere_sports_equipements via BigQuery Load Job.")

    # 2. ministere_sports_licencies (~3,000 rows)
    s2 = [
        bigquery.SchemaField("id_licence", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("region", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("departement", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("commune", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("federation_sportive", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("nombre_licencies_total", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("part_jeunes_moins_18ans_pct", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("croissance_licencies_pct", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("potentiel_sponsoring_premium_stade", "STRING", mode="NULLABLE"),
    ]
    t2_ref = dataset_ref.table("ministere_sports_licencies")
    t2 = bigquery.Table(t2_ref, schema=s2)
    client.create_table(t2, exists_ok=True)

    t2_id = f"{PROJECT_ID}.{DATASET_ID}.ministere_sports_licencies"
    rows_lic = []

    for i in range(1, 3001):
        reg, dep, com = random.choice(REGIONS_DEPARTEMENTS_COMMUNES)
        fed = random.choice(FEDERATIONS)
        nb_lic = random.randint(1200, 48000)
        part_jeunes = round(random.uniform(42.0, 78.0), 1)
        croissance = round(random.uniform(-4.0, 24.5), 1)
        sponsoring = "Priorité Forte (Campagne Sponsoring Premium)" if croissance > 10.0 else "Standard"

        rows_lic.append({
            "id_licence": f"LIC-FED-{i:05d}",
            "region": reg,
            "departement": dep,
            "commune": com,
            "federation_sportive": fed,
            "nombre_licencies_total": nb_lic,
            "part_jeunes_moins_18ans_pct": part_jeunes,
            "croissance_licencies_pct": croissance,
            "potentiel_sponsoring_premium_stade": sponsoring
        })

    job2 = client.load_table_from_json(rows_lic, t2_id, job_config=job_config)
    job2.result()
    print(f"Loaded {len(rows_lic)} rows into ministere_sports_licencies via BigQuery Load Job.")

    # 3. ministere_sports_subventions (~2,500 rows)
    s3 = [
        bigquery.SchemaField("id_subvention", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("region", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("departement", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("commune", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("nom_association_club", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("montant_subvention_ans_eur", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("projet_renovation", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("impact_hausse_inscriptions_jeunes_pct", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("cout_subvention_par_jeune_inscrit_eur", "FLOAT64", mode="NULLABLE"),
    ]
    t3_ref = dataset_ref.table("ministere_sports_subventions")
    t3 = bigquery.Table(t3_ref, schema=s3)
    client.create_table(t3, exists_ok=True)

    t3_id = f"{PROJECT_ID}.{DATASET_ID}.ministere_sports_subventions"
    rows_subv = []

    for i in range(1, 2501):
        reg, dep, com = random.choice(REGIONS_DEPARTEMENTS_COMMUNES)
        projet = random.choice(PROJETS_SUBVENTIONS)
        subv_eur = round(random.uniform(45000.0, 3200000.0), 2)
        impact_jeunes = round(random.uniform(5.0, 32.0), 1)
        jeunes_inscrits = random.randint(150, 2400)
        cost_per_youth = round(subv_eur / jeunes_inscrits, 2)

        rows_subv.append({
            "id_subvention": f"SUBV-ANS-{i:05d}",
            "region": reg,
            "departement": dep,
            "commune": com,
            "nom_association_club": f"Club Sportif Local {com} #{i}",
            "montant_subvention_ans_eur": subv_eur,
            "projet_renovation": projet,
            "impact_hausse_inscriptions_jeunes_pct": impact_jeunes,
            "cout_subvention_par_jeune_inscrit_eur": cost_per_youth
        })

    job3 = client.load_table_from_json(rows_subv, t3_id, job_config=job_config)
    job3.result()
    print(f"Loaded {len(rows_subv)} rows into ministere_sports_subventions via BigQuery Load Job.")

    # 4. ministere_sports_desequilibre_territoires (~1,000 rows)
    s4 = [
        bigquery.SchemaField("id_analyse_territoire", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("region", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("departement", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("commune", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("croissance_demographique_annuelle_pct", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("deficit_equipements_homologues_pct", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("equipement_manquant_prioritaire", "STRING", mode="NULLABLE"),
    ]
    t4_ref = dataset_ref.table("ministere_sports_desequilibre_territoires")
    t4 = bigquery.Table(t4_ref, schema=s4)
    client.create_table(t4, exists_ok=True)

    t4_id = f"{PROJECT_ID}.{DATASET_ID}.ministere_sports_desequilibre_territoires"
    rows_deseq = []

    missing_list = [
        "Piscine Aquatique Olympique manquante",
        "Dojo Municipal & Salle Arts Martiaux saturés",
        "Terrains de Tennis Couverts insuffisants",
        "Stade d'Athlétisme non-homologué",
        "Palais des Sports & Arena saturé"
    ]

    for i in range(1, 1001):
        reg, dep, com = random.choice(REGIONS_DEPARTEMENTS_COMMUNES)
        demo_growth = round(random.uniform(1.2, 5.4), 1)
        deficit = round(random.uniform(22.0, 68.0), 1)
        missing = random.choice(missing_list)

        rows_deseq.append({
            "id_analyse_territoire": f"DESEQ-{i:05d}",
            "region": reg,
            "departement": dep,
            "commune": com,
            "croissance_demographique_annuelle_pct": demo_growth,
            "deficit_equipements_homologues_pct": deficit,
            "equipement_manquant_prioritaire": missing
        })

    job4 = client.load_table_from_json(rows_deseq, t4_id, job_config=job_config)
    job4.result()
    print(f"Loaded {len(rows_deseq)} rows into ministere_sports_desequilibre_territoires via BigQuery Load Job.")

    print(f"✅ Successfully loaded 10,000+ authentic Sports Infrastructure & Licensing records for ArenaManager in {DATASET_ID}!")

if __name__ == "__main__":
    setup_and_enrich_arenamanager()
