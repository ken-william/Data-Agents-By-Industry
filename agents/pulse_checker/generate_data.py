#!/usr/bin/env python3
"""
Mass Data Generation and OpenData Ingestion for PulseChecker (healthcare_pharma_ds) in BigQuery using load_table_from_json.
Generates thousands of realistic healthcare, Open Medic, Open Bio, and RPPS records.
"""

import os
import sys
import random
import subprocess
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "healthcare_pharma_ds"
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

ANTIBIOTIQUES = ["Amoxicilline / Acide Clavulanique", "Céfotaxime", "Azithromycine", "Vancomycine Injectable", "Ciprofloxacine", "Cefatriaxone", "Pénicilline G"]
AUTRES_MOL = ["Pembrolizumab", "Ramipril", "Doliprane 1000mg", "Metformine", "Atorvastatine", "Ibuprofène 400mg"]

ACTES_BIO = [
    "Séquençage Génétique Oncologique", "Dosage Biomarqueurs Cardiaques Rares",
    "Dépistage Prénatal Non Invasif (DPNI)", "Profil Sérologique & Immuno-oncologie",
    "Panel PCR Pathogènes Rares", "Séquençage Haut Débit Exome", "Bilan d'Hémostase Complexe"
]

def setup_and_enrich_pulsechecker():
    client = get_client()

    dataset_ref = bigquery.DatasetReference(PROJECT_ID, DATASET_ID)
    try:
        dataset = client.get_dataset(dataset_ref)
        print(f"Dataset '{DATASET_ID}' ready.")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = LOCATION
        dataset.description = "Dataset d'intelligence de santé publique, prescriptions Open Medic, biologie Open Bio et démographie RPPS pour PulseChecker"
        client.create_dataset(dataset)

    # 1. hopitaux_etablissements_sante (~2,500 rows)
    t1_id = f"{PROJECT_ID}.{DATASET_ID}.hopitaux_etablissements_sante"
    rows_h = []
    types_h = ["CHU", "CH", "Clinique Privée", "ESPIC"]
    villes_list = ["Lyon", "Annecy", "Chambéry", "Grenoble", "Saint-Étienne", "Clermont-Ferrand", "Bourg-en-Bresse", "Marseille", "Paris", "Toulouse", "Strasbourg", "Bordeaux", "Lille", "Nantes"]

    for i in range(1, 2501):
        reg = "Auvergne-Rhône-Alpes" if i <= 800 else random.choice(FRENCH_REGIONS)
        dep = random.choice(DEPARTEMENTS_ARA) if reg == "Auvergne-Rhône-Alpes" else random.choice(DEPARTEMENTS_OTHER)
        ville = random.choice(villes_list)
        t_h = random.choice(types_h)
        stock_j = random.randint(4, 35)
        statut = "Critique (Pénurie < 15j)" if stock_j < 15 else ("Sous Surveillance" if stock_j < 22 else "Normal")

        rows_h.append({
            "id_etablissement": f"HOP-{i:04d}",
            "nom_etablissement": f"Hôpital {t_h} {ville} #{i}",
            "type_etablissement": t_h,
            "code_finess": f"{random.randint(10, 95):02d}000{i:04d}",
            "region": reg,
            "departement": dep,
            "ville": ville,
            "capacite_lits": random.randint(120, 1800),
            "niveau_stock_antibiotiques_jours": stock_j,
            "taux_occupation_lits_pct": round(random.uniform(78.0, 98.5), 1),
            "statut_risque_rupture": statut
        })

    job1 = client.load_table_from_json(rows_h, t1_id)
    job1.result()
    print(f"Loaded {len(rows_h)} rows into hopitaux_etablissements_sante via BigQuery Load Job.")

    # 2. ameli_prescriptions_open_medic (~4,000 rows)
    t2_id = f"{PROJECT_ID}.{DATASET_ID}.ameli_prescriptions_open_medic"
    rows_p = []
    for i in range(1, 4001):
        h_id = f"HOP-{random.randint(1, 2500):04d}"
        is_anti = random.choice([True, True, False])
        if is_anti:
            classe = "Antibiotiques"
            atc = "J01 - Antibiotiques Systémiques"
            mol = random.choice(ANTIBIOTIQUES)
            boites = random.randint(3000, 25000)
            var_pct = round(random.uniform(15.0, 52.0), 1)
            montant = round(boites * random.uniform(20.0, 45.0), 2)
            tension = True
        else:
            classe = random.choice(["Oncologie", "Cardiologie", "Analgésiques"])
            atc = "L04 / C09 / N02"
            mol = random.choice(AUTRES_MOL)
            boites = random.randint(1000, 15000)
            var_pct = round(random.uniform(-5.0, 14.0), 1)
            montant = round(boites * random.uniform(50.0, 400.0), 2)
            tension = False

        rows_p.append({
            "id_prescription": f"PRESC-{i:05d}",
            "id_etablissement": h_id,
            "annee_mois": "2026-08",
            "code_atc_classe": atc,
            "nom_substance_active": mol,
            "classe_therapeutique": classe,
            "nombre_boites_prescrites": boites,
            "variation_mensuelle_demande_pct": var_pct,
            "montant_rembourse_ameli_eur": montant,
            "tension_approvisionnement_flag": tension
        })

    job2 = client.load_table_from_json(rows_p, t2_id)
    job2.result()
    print(f"Loaded {len(rows_p)} rows into ameli_prescriptions_open_medic via BigQuery Load Job.")

    # 3. ameli_biologie_open_bio (~3,000 rows)
    t3_id = f"{PROJECT_ID}.{DATASET_ID}.ameli_biologie_open_bio"
    rows_b = []
    for i in range(1, 3001):
        reg = random.choice(FRENCH_REGIONS)
        dep = random.choice(DEPARTEMENTS_ARA if reg == "Auvergne-Rhône-Alpes" else DEPARTEMENTS_OTHER)
        acte = random.choice(ACTES_BIO)
        vol = random.randint(25000, 250000)
        crois = round(random.uniform(12.0, 42.0), 1)
        montant = round(vol * random.uniform(35.0, 85.0), 2)
        couverture = "Sous-équipé (Tension Forte)" if crois > 25.0 else "Partiellement Couvert"

        rows_b.append({
            "id_acte_bio": f"BIO-{i:04d}",
            "region": reg,
            "departement": dep,
            "code_categorie_bio": f"B0{random.randint(1, 5)} - Biologie Spécialisée",
            "nom_acte_biologie": acte,
            "volume_actes_annuel": vol,
            "croissance_annuelle_demande_pct": crois,
            "montant_depenses_open_bio_eur": montant,
            "niveau_couverture_locale": couverture
        })

    job3 = client.load_table_from_json(rows_b, t3_id)
    job3.result()
    print(f"Loaded {len(rows_b)} rows into ameli_biologie_open_bio via BigQuery Load Job.")

    # 4. demographie_medecins_rpps (~1,500 rows)
    t4_id = f"{PROJECT_ID}.{DATASET_ID}.demographie_medecins_rpps"
    rows_rpps = []
    territoires_names = ["Bassin d'Annecy & Genevois", "Pays de Gex & Ain Nord", "Cannes-Grasse-Théoule", "Versailles Grand Ouest", "Grand Lyon Est", "Bassin Littoral Montpellier"]

    for i in range(1, 1501):
        reg = random.choice(FRENCH_REGIONS)
        dep = random.choice(DEPARTEMENTS_ARA if reg == "Auvergne-Rhône-Alpes" else DEPARTEMENTS_OTHER)
        nom_t = f"{random.choice(territoires_names)} Zone #{i}"
        dens = round(random.uniform(95.0, 260.0), 1)
        pop = random.randint(80000, 500000)
        tension_idx = round(random.uniform(0.30, 0.85), 2)
        opp = "Priorité Forte (ROI Élevé)" if dens < 170.0 else "Opportunité Modérée"

        rows_rpps.append({
            "id_territoire": f"TER-{i:04d}",
            "region": reg,
            "departement": dep,
            "nom_territoire": nom_t,
            "densite_medecins_pour_100k_hab": dens,
            "nombre_specialistes_biologie": random.randint(2, 18),
            "nombre_specialistes_oncologie": random.randint(1, 15),
            "population_totale": pop,
            "indice_tension_demographique": tension_idx,
            "opportunite_investissement_clinique": opp
        })

    job4 = client.load_table_from_json(rows_rpps, t4_id)
    job4.result()
    print(f"Loaded {len(rows_rpps)} rows into demographie_medecins_rpps via BigQuery Load Job.")

    print(f"✅ Successfully loaded thousands of records for PulseChecker in {DATASET_ID}!")

if __name__ == "__main__":
    setup_and_enrich_pulsechecker()
