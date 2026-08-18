#!/usr/bin/env python3
"""
Mass Data Generation and OpenData Ingestion for ShelfOptimizer (retail_cpg_ds) in BigQuery using load_table_from_json.
Generates thousands of realistic Open Food Facts catalog products, Nutri-Score A-E, Nova 1-4, additives, prices, weather impact, and retail waste records.
"""

import os
import sys
import random
import subprocess
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "retail_cpg_ds"
LOCATION = "US"

def get_client():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return bigquery.Client(project=PROJECT_ID, credentials=creds)

RAYONS = ["Produits Frais", "Épicerie Sucrée", "Épicerie Salée", "Boissons & Jus", "Traiteur & Plats Cuisinés", "Boulangerie & Pâtisserie"]

MARQUES = ["MDD Marque Repère", "MDD Carrefour Bio", "MDD Auchan Gourmet", "Nestlé", "Danone", "Ferrero", "Barilla", "Fleury Michon", "Lu", "Tropicana"]

ADDITIFS_LIST = [
    ("E250 (Nitrite de sodium), E102 (Tartrazine)", "E250/E102 problématiques", "Saucisson Bio sans Nitrites (Nutri-Score B)"),
    ("Huile de Palme, Sirop de Glucose-Fructose", "Huile de Palme ultra-transformée", "Pâte à tartiner Bio sans huile de palme (Nutri-Score A)"),
    ("E452 (Polyphosphates), E621 (Glutamate)", "Polyphosphates & Glutamate", "Jambon cuit AC sans polyphosphates (Nutri-Score B)"),
    ("E133 (Bleu brillant), E129 (Rouge allura)", "Colorants Azoïques E133/E129", "Jus de Fruits 100% Pur Jus Bio (Nutri-Score A)"),
    ("Aucun additif artificiel", "Conforme Qualité Maximale", "Produit Naturel Certifié Bio (Nutri-Score A)")
]

IMAGE_URLS_SAMPLE = [
    "https://images.openfoodfacts.org/images/products/301/762/042/2003/front_fr.400.jpg",
    "https://images.openfoodfacts.org/images/products/316/893/001/0010/front_fr.400.jpg",
    "https://images.openfoodfacts.org/images/products/302/329/000/7001/front_fr.400.jpg",
    "https://images.openfoodfacts.org/images/products/327/019/002/1004/front_fr.400.jpg",
    "https://images.openfoodfacts.org/images/products/304/692/001/2005/front_fr.400.jpg"
]

HYPERMARCHES = [
    "Carrefour Hyper Vélizy", "Auchan Hyper V2 Lille", "Leclerc Hyper Blagnac Toulouse",
    "E.Leclerc Hyper Part-Dieu Lyon", "Hyper U Bordeaux Lac", "Carrefour Hyper Antibes",
    "Auchan Hyper St-Priest", "Cora Hyper Cormontreuil", "Geant Casino Marseille", "Leclerc Hyper Bois d'Arcy"
]

WEATHER_CONDITIONS = ["Pluie Forte", "Soleil & Chaleur", "Grand Froid", "Vag de Froid", "Normal / Couvert"]

def setup_and_enrich_shelf_optimizer():
    client = get_client()

    dataset_ref = bigquery.DatasetReference(PROJECT_ID, DATASET_ID)
    try:
        dataset = client.get_dataset(dataset_ref)
        print(f"Dataset '{DATASET_ID}' ready.")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = LOCATION
        dataset.description = "Dataset de catalogue produits Open Food Facts, prix et fréquentation retail pour ShelfOptimizer"
        client.create_dataset(dataset)

    job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)

    # 1. openfoodfacts_catalog (~4,500 rows)
    s1 = [
        bigquery.SchemaField("code_barre_ean", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("nom_produit", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("marque_entreprise", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("rayon_categorie", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("nutri_score", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("nova_score", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("additifs_problematiques", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("alternatives_saines_recommandees", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("empreinte_carbone_100g", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("chiffre_affaires_annuel_eur", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("produit_image_url", "STRING", mode="NULLABLE"),
    ]
    t1_ref = dataset_ref.table("openfoodfacts_catalog")
    t1 = bigquery.Table(t1_ref, schema=s1)
    client.create_table(t1, exists_ok=True)

    t1_id = f"{PROJECT_ID}.{DATASET_ID}.openfoodfacts_catalog"
    rows_c = []
    prefix_p = ["Pâte à Tartiner", "Céréales Gourmandes", "Jambon Supérieur", "Yaourt Fraise", "Plat Cuisiné Lasagnes", "Biscuits Chocolat", "Jus d'Orange Pur Jus", "Pain de Mie Bio", "Fromage Fondu", "Sauce Tomate Basilic"]

    for i in range(1, 4501):
        ean = f"3{random.randint(10000000001, 99999999999)}"
        rayon = random.choice(RAYONS)
        marque = random.choice(MARQUES)
        nom = f"{random.choice(prefix_p)} {marque.split()[-1]} #{i}"

        # Assign Nutri-Score & NOVA
        if "Bio" in marque or "Pur Jus" in nom:
            ns = random.choice(["A", "B", "A"])
            nova = random.choice([1, 2])
            add_item = ADDITIFS_LIST[4]
        else:
            ns = random.choice(["C", "D", "E", "D", "E"])
            nova = random.choice([3, 4, 4])
            add_item = random.choice(ADDITIFS_LIST[:4])

        ca = round(random.uniform(150000.0, 18500000.0), 2)
        img_url = random.choice(IMAGE_URLS_SAMPLE)

        rows_c.append({
            "code_barre_ean": ean,
            "nom_produit": nom,
            "marque_entreprise": marque,
            "rayon_categorie": rayon,
            "nutri_score": ns,
            "nova_score": nova,
            "additifs_problematiques": add_item[0],
            "alternatives_saines_recommandees": add_item[2],
            "empreinte_carbone_100g": round(random.uniform(0.08, 0.95), 2),
            "chiffre_affaires_annuel_eur": ca,
            "produit_image_url": img_url
        })

    job1 = client.load_table_from_json(rows_c, t1_id, job_config=job_config)
    job1.result()
    print(f"Loaded {len(rows_c)} rows into openfoodfacts_catalog via BigQuery Load Job.")

    # 2. retail_prix_moyens_panier (~2,000 rows)
    s2 = [
        bigquery.SchemaField("id_panier", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("rayon_categorie", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("type_gamme", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("prix_moyen_article_eur", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("evolution_prix_6m_pct", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("volume_ventes_annuel_unites", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("marge_brute_pct", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("elasticite_prix", "FLOAT64", mode="NULLABLE"),
    ]
    t2_ref = dataset_ref.table("retail_prix_moyens_panier")
    t2 = bigquery.Table(t2_ref, schema=s2)
    client.create_table(t2, exists_ok=True)

    t2_id = f"{PROJECT_ID}.{DATASET_ID}.retail_prix_moyens_panier"
    rows_p = []
    gammes = ["MDD Marque Repère", "Bio AB", "Label Rouge", "Marque Nationale Premium"]

    for i in range(1, 2001):
        rayon = random.choice(RAYONS)
        gamme = random.choice(gammes)
        prix = round(random.uniform(1.85, 14.50), 2)
        evol_6m = round(random.uniform(2.1, 14.8), 1)
        vol_unites = random.randint(15000, 850000)

        marge = round(random.uniform(32.0, 54.0), 1) if "MDD" in gamme else round(random.uniform(18.0, 31.0), 1)
        elast = round(random.uniform(-1.8, -0.4), 2)

        rows_p.append({
            "id_panier": f"PANIER-{i:04d}",
            "rayon_categorie": rayon,
            "type_gamme": gamme,
            "prix_moyen_article_eur": prix,
            "evolution_prix_6m_pct": evol_6m,
            "volume_ventes_annuel_unites": vol_unites,
            "marge_brute_pct": marge,
            "elasticite_prix": elast
        })

    job2 = client.load_table_from_json(rows_p, t2_id, job_config=job_config)
    job2.result()
    print(f"Loaded {len(rows_p)} rows into retail_prix_moyens_panier via BigQuery Load Job.")

    # 3. retail_frequentation_magasins (~3,500 rows)
    s3 = [
        bigquery.SchemaField("id_magasin", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("nom_magasin", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("ville", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("tranche_horaire", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("conditions_meteo", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("nombre_passage_caisses", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("panier_moyen_eur", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("demarque_pertes_produits_frais_14j_eur", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("consigne_reassort_automatique", "STRING", mode="NULLABLE"),
    ]
    t3_ref = dataset_ref.table("retail_frequentation_magasins")
    t3 = bigquery.Table(t3_ref, schema=s3)
    client.create_table(t3, exists_ok=True)

    t3_id = f"{PROJECT_ID}.{DATASET_ID}.retail_frequentation_magasins"
    rows_f = []
    tranches = ["08h-12h", "12h-14h", "14h-17h", "17h-20h"]

    for i in range(1, 3501):
        mag = HYPERMARCHES[(i - 1) % len(HYPERMARCHES)]
        ville = mag.split()[-1]
        tranche = random.choice(tranches)
        meteo = random.choice(WEATHER_CONDITIONS)
        caisses = random.randint(800, 6500)
        panier = round(random.uniform(28.50, 78.90), 2)
        demarque_14j = round(random.uniform(1450.0, 38500.0), 2)

        if demarque_14j > 22000.0 or "Pluie" in meteo:
            reassort = "Réassort Automatique Modéré (-15% Démarque)"
        elif demarque_14j < 8000.0 and tranche == "17h-20h":
            reassort = "Réassort Automatique Boost (+25% Volume)"
        else:
            reassort = "Réassort Automatique Standard"

        rows_f.append({
            "id_magasin": f"MAG-{i:04d}",
            "nom_magasin": mag,
            "ville": ville,
            "tranche_horaire": tranche,
            "conditions_meteo": meteo,
            "nombre_passage_caisses": caisses,
            "panier_moyen_eur": panier,
            "demarque_pertes_produits_frais_14j_eur": demarque_14j,
            "consigne_reassort_automatique": reassort
        })

    job3 = client.load_table_from_json(rows_f, t3_id, job_config=job_config)
    job3.result()
    print(f"Loaded {len(rows_f)} rows into retail_frequentation_magasins via BigQuery Load Job.")

    print(f"✅ Successfully loaded thousands of records for ShelfOptimizer in {DATASET_ID}!")

if __name__ == "__main__":
    setup_and_enrich_shelf_optimizer()
