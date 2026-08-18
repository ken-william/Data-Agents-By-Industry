#!/usr/bin/env python3
"""
Relational Data Generation and OpenData Processing for ShelfOptimizer (retail_cpg_ds).
Reads authentic product records from 'agents/shelf_optimizer/data/openfoodfacts_catalog.csv'
and populates 5 refined merchandising tables:
1. openfoodfacts_catalog (Master product catalog with Nutri-Score, NOVA, additives & GCS image URLs)
2. retail_frequentation_magasins (Store footfall, time slots & 14-day fresh produce loss predictions)
3. retail_prix_moyens_panier (Average basket price & category gross margins)
4. retail_analyse_lineaire_ruptures (Shelf stockout rates & planogram compliance audits)
5. retail_cross_selling_associations (Product affinity rules & MDD cross-selling bundles)
"""

import os
import sys
import random
import subprocess
import pandas as pd
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "retail_cpg_ds"
LOCATION = "US"
OFF_CSV_PATH = "agents/shelf_optimizer/data/openfoodfacts_catalog.csv"
BUCKET_NAME = "gs://talktodata-shelf-optimizer-raw-data"

CITY_DEPT_REGION = {
    "Paris": ("75 - Paris", "Île-de-France"),
    "Lyon": ("69 - Rhône", "Auvergne-Rhône-Alpes"),
    "Marseille": ("13 - Bouches-du-Rhône", "Provence-Alpes-Côte d'Azur"),
    "Toulouse": ("31 - Haute-Garonne", "Occitanie"),
    "Bordeaux": ("33 - Gironde", "Nouvelle-Aquitaine"),
    "Lille": ("59 - Nord", "Hauts-de-France"),
    "Strasbourg": ("67 - Bas-Rhin", "Grand Est"),
    "Nantes": ("44 - Loire-Atlantique", "Pays de la Loire"),
    "Rennes": ("35 - Ille-et-Vilaine", "Bretagne")
}

def get_client():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return bigquery.Client(project=PROJECT_ID, credentials=creds)

def main():
    print(f"Initializing Refined ShelfOptimizer Relational Pipeline for project '{PROJECT_ID}'...")
    client = get_client()

    os.makedirs("agents/shelf_optimizer/data", exist_ok=True)

    # 1. openfoodfacts_catalog
    if os.path.exists(OFF_CSV_PATH):
        df_off = pd.read_csv(OFF_CSV_PATH, low_memory=False)
        print(f"  ✓ Parsed {len(df_off)} authentic Open Food Facts product records from base CSV.")
    else:
        raise FileNotFoundError(f"Missing base CSV: {OFF_CSV_PATH}")

    product_records = df_off.to_dict("records")
    ean_list = [str(r.get("code_barre_ean")) for r in product_records]

    # 2. retail_frequentation_magasins
    rows_freq = []
    cities = list(CITY_DEPT_REGION.keys())
    brands = ["Carrefour Hyper", "Auchan Super", "Monoprix", "E.Leclerc", "Intermarché"]
    time_slots = ["08h-11h", "11h-14h", "14h-17h", "17h-20h"]

    magasin_list = []
    for idx in range(1, 151):
        commune = random.choice(cities)
        dept, region = CITY_DEPT_REGION[commune]
        brand = random.choice(brands)
        mag_id = f"MAG-{idx:04d}"
        mag_name = f"{brand} {commune} #{idx}"
        magasin_list.append({"id_magasin": mag_id, "nom_magasin": mag_name, "commune": commune, "departement": dept, "region": region})

        for slot in time_slots:
            clients = random.randint(350, 2800)
            conv_pct = round(random.uniform(62.0, 88.5), 1)
            demarque_14j = round(random.uniform(1200.0, 18500.0), 2)
            consigne = "REASSORT_URGENT_AUTOMATIQUE" if demarque_14j > 12000.0 else "CONFORME"

            rows_freq.append({
                "id_magasin": mag_id,
                "nom_magasin": mag_name,
                "enseigne": brand,
                "commune": commune,
                "code_departement": dept,
                "nom_region": region,
                "tranche_horaire": slot,
                "affluence_clients_jour": clients,
                "taux_conversion_passage_caisses_pct": conv_pct,
                "demarque_pertes_produits_frais_14j_eur": demarque_14j,
                "consigne_reassort_automatique": consigne
            })

    df_freq = pd.DataFrame(rows_freq)

    # 3. retail_prix_moyens_panier
    rows_panier = []
    rayons = ["Produits Frais", "Épicerie", "Boissons", "Produits Laitiers", "Surgelés", "Boulangerie"]

    for idx in range(1, 1501):
        commune = random.choice(cities)
        dept, region = CITY_DEPT_REGION[commune]
        rayon = random.choice(rayons)
        panier_eur = round(random.uniform(28.5, 95.0), 2)
        marge_pct = round(random.uniform(22.0, 48.5), 1)
        bio_pct = round(random.uniform(12.0, 38.0), 1)
        mdd_pct = round(random.uniform(25.0, 55.0), 1)

        rows_panier.append({
            "id_releve_panier": f"PAN-{idx:05d}",
            "commune": commune,
            "code_departement": dept,
            "nom_region": region,
            "rayon_categorie": rayon,
            "prix_moyen_panier_eur": panier_eur,
            "marge_brute_pct": marge_pct,
            "part_produits_bio_pct": bio_pct,
            "part_marques_distributeur_pct": mdd_pct
        })

    df_panier = pd.DataFrame(rows_panier)

    # 4. retail_analyse_lineaire_ruptures
    rows_lineaire = []
    for idx in range(1, 3501):
        m = random.choice(magasin_list)
        p = random.choice(product_records)
        fac_theo = random.randint(6, 24)
        fac_obs = random.randint(0, fac_theo)
        conf_pct = round((fac_obs / fac_theo) * 100.0, 1)
        rupt_pct = round(100.0 - conf_pct, 1)

        statut = "RUPTURE_SHELF_OUT" if fac_obs == 0 else ("STOCK_FAIBLE" if conf_pct < 50.0 else "CONFORME")

        rows_lineaire.append({
            "id_releve_lineaire": f"LIN-{idx:05d}",
            "id_magasin": m["id_magasin"],
            "code_barre_ean": str(p["code_barre_ean"]),
            "rayon_categorie": str(p["rayon_categorie"]),
            "nombre_facings_theorique": fac_theo,
            "nombre_facings_constate": fac_obs,
            "taux_conformite_planogramme_pct": conf_pct,
            "taux_rupture_lineaire_pct": rupt_pct,
            "statut_stock_lineaire": statut
        })

    df_lineaire = pd.DataFrame(rows_lineaire)

    # 5. retail_cross_selling_associations
    rows_cross = []
    piliers = [p for p in product_records if "Marque" in str(p.get("marque_entreprise")) or "Danone" in str(p.get("marque_entreprise")) or "Coca" in str(p.get("marque_entreprise")) or "Nestlé" in str(p.get("marque_entreprise"))]
    mdds = [p for p in product_records if "MDD" in str(p.get("marque_entreprise")) or "Marque Repère" in str(p.get("marque_entreprise")) or "Auchan" in str(p.get("marque_entreprise")) or "Carrefour" in str(p.get("marque_entreprise"))]

    if not piliers:
        piliers = product_records[:20]
    if not mdds:
        mdds = product_records[20:40]

    for idx in range(1, 1001):
        pil = random.choice(piliers)
        mdd = random.choice(mdds)
        conf_pct = round(random.uniform(65.0, 94.0), 1)
        hausse_ticket = round(random.uniform(4.5, 14.2), 1)
        bundle_desc = f"Offre Duo : -30% sur {mdd['nom_produit']} (MDD) à l'achat de {pil['nom_produit']}"

        rows_cross.append({
            "id_association": f"XSELL-{idx:04d}",
            "code_barre_ean_principal": str(pil["code_barre_ean"]),
            "code_barre_ean_associe_mdd": str(mdd["code_barre_ean"]),
            "nom_produit_principal": str(pil["nom_produit"]),
            "nom_produit_mdd_associe": str(mdd["nom_produit"]),
            "indice_confiance_association_pct": conf_pct,
            "hausse_ticket_moyen_projete_pct": hausse_ticket,
            "offre_bundle_recommandee": bundle_desc
        })

    df_cross = pd.DataFrame(rows_cross)

    # Save CSVs locally and upload to BigQuery & GCS
    tables_dict = {
        "openfoodfacts_catalog": df_off,
        "retail_frequentation_magasins": df_freq,
        "retail_prix_moyens_panier": df_panier,
        "retail_analyse_lineaire_ruptures": df_lineaire,
        "retail_cross_selling_associations": df_cross
    }

    subprocess.run(f"gcloud storage buckets create {BUCKET_NAME} --project={PROJECT_ID} --location=EU 2>/dev/null", shell=True)

    for tname, df in tables_dict.items():
        csv_file = f"agents/shelf_optimizer/data/{tname}.csv"
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

    print("\nSUCCESS: All 5 ShelfOptimizer tables complete & populated in BigQuery!")

if __name__ == "__main__":
    main()
