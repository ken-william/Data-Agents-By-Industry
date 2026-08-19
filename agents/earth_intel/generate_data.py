#!/usr/bin/env python3
"""
Refined Relational Data Pipeline & Multimodal Processing for Earth Intel (skywatch_aerospace_ds).
Unifies Sentinel-2 satellite scene metadata, GCS Object Tables for direct Quicklook PNG image analysis,
industrial asset risk audits across 10 enterprise sectors, and CSRD Zero Deforestation compliance.
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
DATASET_ID = "skywatch_aerospace_ds"
LOCATION = "US"
BUCKET_NAME = "gs://talktodata-earth-intel-raw-data"
IMAGES_DIR = "satellite_imagery"

def get_client():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return bigquery.Client(project=PROJECT_ID, credentials=creds)

def main():
    print(f"Initializing Refined Earth Intel Pipeline for project '{PROJECT_ID}'...")
    client = get_client()

    # Step 1: Execute ddl_setup.sql
    ddl_path = os.path.join(os.path.dirname(__file__), "ddl_setup.sql")
    if os.path.exists(ddl_path):
        with open(ddl_path, "r", encoding="utf-8") as f:
            sql_script = f.read().replace("${PROJECT_ID}", PROJECT_ID)
        for stmt in sql_script.split(";"):
            stmt = stmt.strip()
            if stmt:
                client.query(stmt).result()
        print("  ✓ Executed ddl_setup.sql to ensure exact skywatch_aerospace_ds schemas!")

    # Step 2: Build Table 1: company_assets
    assets = [
        # 1. FSI (Banque & Assurance)
        ("AST-FSI-01", "AXA Assurances", "Banque & Assurance", "Portefeuille Immobilier Côte d'Azur", "Actif Immobilier Assuré", "31TDF", 43.70, 7.26, "Nice", "PACA", "France", 0.95, 250000000.0, "Compliant", 0.88, 0.72, 1.2, "Faible", 0.45, 0, 15.0, 0.0, 3.8, 12.0, 0.0, 15.0),
        ("AST-FSI-02", "BNP Paribas Real Estate", "Banque & Assurance", "Parc d'Activité Logistique Vallée du Rhône", "Immobilier Commercial", "31TFL", 45.72, 4.84, "Lyon", "Auvergne-Rhône-Alpes", "France", 0.92, 180000000.0, "Compliant", 0.78, 0.35, 2.5, "Modéré", 0.52, 0, 8.0, 0.0, 4.2, 18.0, 0.0, 22.0),

        # 2. Santé & Pharma
        ("AST-SANTE-01", "Sanofi Pasteur", "Santé & Pharma", "Complexe de Bioproduction de Marcy-l'Étoile", "Usine Vaccins & Pharma", "31TFL", 45.78, 4.71, "Marcy-l'Étoile", "Auvergne-Rhône-Alpes", "France", 0.98, 420000000.0, "Compliant", 0.25, 0.15, 8.4, "Élevé", 0.68, 0, 22.0, 0.0, 2.1, 8.0, 0.0, 35.0),
        ("AST-SANTE-02", "CHRU de Montpellier", "Santé & Pharma", "Pôle Hospitalo-Universitaire Lapeyronie", "Établissement Hospitalier", "31TDF", 43.63, 3.86, "Montpellier", "Occitanie", "France", 0.96, 310000000.0, "Compliant", 0.45, 0.62, 12.1, "Élevé", 0.38, 0, 18.0, 0.0, 4.9, 14.0, 0.0, 18.0),

        # 3. Agriculture & Ruralité
        ("AST-AGRI-01", "Coopérative Agrial", "Agriculture & Ruralité", "Bassin Céréalier et Domaines Agricoles", "Exploitation Agricole", "31TLD", 45.83, 3.12, "Clermont-Ferrand", "Auvergne-Rhône-Alpes", "France", 0.89, 125000000.0, "Compliant", 0.32, 0.40, 0.5, "Faible", 0.76, 0, 50.0, 0.0, 1.2, 5.0, 5.0, 45.0),
        ("AST-AGRI-02", "InVivo Agro", "Agriculture & Ruralité", "Grands Domaines Viticoles du Libournais", "Vignobles & Cultures", "30TYQ", 44.91, -0.24, "Libourne", "Nouvelle-Aquitaine", "France", 0.91, 165000000.0, "Compliant", 0.41, 0.30, 0.8, "Faible", 0.82, 0, 45.0, 0.0, 1.8, 6.0, 2.0, 52.0),

        # 4. Transports & Mobilité
        ("AST-TRANS-01", "CMA CGM", "Transports & Mobilité", "Terminal Portuaire de Fos-sur-Mer", "Hub Logistique Portuaire", "31TFJ", 43.43, 4.88, "Fos-sur-Mer", "PACA", "France", 0.99, 890000000.0, "Under Audit", 0.65, 0.20, 15.0, "Faible", 0.22, 28, 65.0, 0.0, 3.1, 4.0, 0.0, 8.0),
        ("AST-TRANS-02", "Grand Port Maritime de Dunkerque", "Transports & Mobilité", "Terminal à Conteneurs Flandres", "Port Maritime", "31UDS", 51.04, 2.37, "Dunkerque", "Hauts-de-France", "France", 0.96, 540000000.0, "Compliant", 0.70, 0.10, 22.0, "Faible", 0.18, 19, 80.0, 0.0, 2.8, 3.0, 0.0, 6.0),

        # 5. Énergie & Climat
        ("AST-NRG-01", "EDF Réseau Haute Tension", "Énergie & Climat", "Ligne HT 400kV Massif Central", "Réseau Électrique HT", "31TDH", 43.55, 2.75, "Lacaune", "Occitanie", "France", 0.99, 620000000.0, "Compliant", 0.20, 0.85, 0.3, "Faible", 0.72, 0, 2.4, 0.0, 1.5, 65.0, 12.0, 68.0),
        ("AST-NRG-02", "RTE Électricité de France", "Énergie & Climat", "Poste de Transformation de Crest", "Infrastructures Électriques", "31TGM", 44.72, 5.02, "Crest", "Auvergne-Rhône-Alpes", "France", 0.97, 410000000.0, "Compliant", 0.35, 0.78, 0.6, "Faible", 0.65, 0, 3.1, 0.0, 2.2, 58.0, 8.0, 55.0),

        # 6. Retail & CPG
        ("AST-RETAIL-01", "Carrefour Group Sourcing", "Retail & CPG", "Sourcing Soja & Cacao Brésil/Paraguay", "Chaîne d'Approvisionnement", "31UDQ", 48.94, 2.49, "Aulnay-sous-Bois", "Île-de-France", "France", 0.94, 380000000.0, "Compliant (Zéro Déforestation Certifié)", 0.15, 0.10, 0.0, "Nul", 0.88, 0, 100.0, 0.0, 1.0, 2.0, 0.0, 75.0),
        ("AST-RETAIL-02", "Danone Nutricia Sourcing", "Retail & CPG", "Approvisionnement Huile de Palme Indonésie", "Sourcing Matières Premières", "31UUD", 48.91, 2.29, "Asnières-sur-Seine", "Île-de-France", "France", 0.93, 290000000.0, "Verified CSRD", 0.10, 0.05, 0.0, "Nul", 0.91, 0, 100.0, 0.0, 1.1, 3.0, 0.0, 80.0),

        # 7. Secteur Public & Emploi
        ("AST-PUB-01", "Métropole de Nice Côte d'Azur", "Secteur Public & Emploi", "Zone d'Étalement Urbain & Littoral", "Territoire Métropolitain", "31TDF", 43.68, 7.20, "Nice", "PACA", "France", 0.90, 150000000.0, "Compliant", 0.82, 0.68, 3.5, "Modéré", 0.35, 0, 35.0, 0.0, 4.8, 15.0, 0.0, 25.0),
        ("AST-PUB-02", "Ville de Marseille", "Secteur Public & Emploi", "Centre Urbain & Quartiers Nord", "Infrastructures Urbaines", "31TFJ", 43.30, 5.37, "Marseille", "PACA", "France", 0.92, 220000000.0, "Compliant", 0.75, 0.55, 4.2, "Modéré", 0.28, 0, 40.0, 0.0, 5.4, 20.0, 0.0, 18.0),

        # 8. Télécoms & Médias
        ("AST-TELCO-01", "Orange Télécom", "Télécoms & Médias", "Réseau d'Antennes 5G Massif Vosgien", "Infrastructures Réseau 5G", "32UFU", 48.12, 6.88, "Gérardmer", "Grand Est", "France", 0.91, 140000000.0, "Compliant", 0.15, 0.30, 0.2, "Nul", 0.78, 0, 12.0, 0.0, 1.8, 74.5, 15.0, 65.0),
        ("AST-TELCO-02", "Bouygues Telecom", "Télécoms & Médias", "Relais 5G Zone Forestière Landes", "Pylônes & Couverture 5G", "30TYQ", 44.40, -0.90, "Biscarrosse", "Nouvelle-Aquitaine", "France", 0.88, 115000000.0, "Compliant", 0.22, 0.60, 0.4, "Nul", 0.81, 0, 15.0, 0.0, 2.1, 68.0, 10.0, 70.0),

        # 9. Divertissement & Cinéma
        ("AST-CINE-01", "Pathé Films Production", "Divertissement & Cinéma", "Décor Naturel Mont-Blanc Chamonix", "Site de Tournage Cinéma", "31TGM", 45.92, 6.86, "Chamonix-Mont-Blanc", "Auvergne-Rhône-Alpes", "France", 0.85, 45000000.0, "Compliant", 0.10, 0.15, 0.1, "Nul", 0.60, 0, 100.0, 0.0, -1.2, 85.0, 78.5, 88.0),
        ("AST-CINE-02", "StudioCanal", "Divertissement & Cinéma", "Site de Tournage Massif de la Vanoise", "Décor Montagne & Neige", "31TGK", 45.35, 6.70, "Val d'Isère", "Auvergne-Rhône-Alpes", "France", 0.82, 38000000.0, "Compliant", 0.12, 0.18, 0.1, "Nul", 0.58, 0, 100.0, 0.0, -1.8, 88.0, 82.0, 92.0),

        # 10. Sport & Infrastructures
        ("AST-SPORT-01", "Stade de France Consortium", "Sport & Infrastructures", "Stade de France & Parvis Saint-Denis", "Grand Stade National", "31UDQ", 48.92, 2.36, "Saint-Denis", "Île-de-France", "France", 0.99, 650000000.0, "Compliant", 0.60, 0.10, 1.8, "Faible", 0.25, 0, 25.0, 0.0, 5.8, 12.0, 0.0, 14.5),
        ("AST-SPORT-02", "Olympique Lyonnais Groupe", "Sport & Infrastructures", "Groupama Stadium & OL OL-Park", "Complexe Sportif Arena", "31TFL", 45.76, 4.98, "Décines-Charpieu", "Auvergne-Rhône-Alpes", "France", 0.96, 320000000.0, "Compliant", 0.50, 0.20, 2.1, "Faible", 0.32, 0, 30.0, 0.0, 4.6, 15.0, 0.0, 28.0)
    ]

    asset_rows = []
    for r in assets:
        asset_rows.append({
            "asset_id": r[0],
            "company_name": r[1],
            "industry_sector": r[2],
            "asset_name": r[3],
            "asset_type": r[4],
            "mgrs_tile": r[5],
            "latitude": r[6],
            "longitude": r[7],
            "location_geo": f"POINT({r[7]} {r[6]})",
            "city": r[8],
            "region": r[9],
            "country": r[10],
            "criticality_score": r[11],
            "annual_revenue_impact_eur": r[12],
            "csrd_compliance_status": r[13],
            "flood_risk_score": r[14],
            "fire_risk_score": r[15],
            "stagnant_water_km2": r[16],
            "mosquito_outbreak_risk": r[17],
            "ndvi_vegetation_index": r[18],
            "port_container_ships_waiting": r[19],
            "powerline_tree_encroachment_m": r[20],
            "deforestation_rate_pct_5y": r[21],
            "urban_heat_island_celsius": r[22],
            "canopy_density_5g_obstacle_pct": r[23],
            "snow_cover_historical_pct": r[24],
            "stadium_green_cooling_canopy_pct": r[25]
        })
    df_assets = pd.DataFrame(asset_rows)
    print(f"  ✓ Processed {len(df_assets)} company assets across 10 enterprise sectors.")

    # Step 3: Build Table 2: sentinel_2_index
    mgrs_tiles = list(set([r[5] for r in assets]))
    scenes = []
    for idx, tile in enumerate(mgrs_tiles * 3):
        dt = datetime(2026, 8, 15) - timedelta(days=idx * 4)
        scene_id = f"S2B_MSIL2A_{dt.strftime('%Y%m%dT%H%M%S')}_{tile}"
        quicklook_uri = f"https://storage.googleapis.com/talktodata-earth-intel-raw-data/{IMAGES_DIR}/s2_{tile}_quicklook.png"

        scenes.append({
            "scene_id": scene_id,
            "mgrs_tile": tile,
            "acquisition_date": dt.strftime("%Y-%m-%d"),
            "cloud_cover_pct": round(random.uniform(0.5, 12.0), 1),
            "constellation_satellite": random.choice(["Sentinel-2A", "Sentinel-2B"]),
            "ndvi_mean": round(random.uniform(0.25, 0.85), 2),
            "ndwi_water_mean": round(random.uniform(-0.15, 0.45), 2),
            "quicklook_image_url": quicklook_uri
        })
    df_scenes = pd.DataFrame(scenes)
    print(f"  ✓ Processed {len(df_scenes)} Sentinel-2 satellite scene metadata records.")

    # Step 4: Build Table 3: satellites_constellations_metadonnees
    satellites_data = [
        {"satellite_id": "SENTINEL-2A", "operator": "ESA / Copernicus", "spatial_resolution_m": 10.0, "revisit_time_days": 5, "spectral_bands_count": 13, "orbit_type": "Orbite Héliosynchrone LEO"},
        {"satellite_id": "SENTINEL-2B", "operator": "ESA / Copernicus", "spatial_resolution_m": 10.0, "revisit_time_days": 5, "spectral_bands_count": 13, "orbit_type": "Orbite Héliosynchrone LEO"},
        {"satellite_id": "LANDSAT-9", "operator": "NASA / USGS", "spatial_resolution_m": 15.0, "revisit_time_days": 8, "spectral_bands_count": 11, "orbit_type": "Orbite Héliosynchrone LEO"},
        {"satellite_id": "COPERNICUS-DEM", "operator": "ESA / DLR", "spatial_resolution_m": 30.0, "revisit_time_days": 30, "spectral_bands_count": 1, "orbit_type": "Modèle Numérique de Terrain"}
    ]
    df_sats = pd.DataFrame(satellites_data)

    # Step 5: Build Table 4: inondations_incendies_alertes
    alerts = []
    alert_types = [
        "Inondation Majeure & Crue Lit Majeur",
        "Départ de Feu de Forêt & Stress Hydrique",
        "Canicule & Îlot de Chaleur Urbain",
        "Risque Sanitaire Moustique Vecteur"
    ]
    severities = ["Modéré", "Critique", "Urgence Majeure"]

    scene_records = df_scenes.to_dict("records")
    asset_records = df_assets.to_dict("records")

    for i in range(1, 31):
        aid = f"ALR-2026-{i:03d}"
        ast = random.choice(asset_records)
        sc = random.choice(scene_records)

        alerts.append({
            "alert_id": aid,
            "asset_id": ast["asset_id"],
            "scene_id": sc["scene_id"],
            "alert_type": random.choice(alert_types),
            "severity_level": random.choice(severities),
            "alert_date": f"2026-08-15 {random.randint(8,18):02d}:00:00",
            "financial_loss_risk_eur": round(ast["annual_revenue_impact_eur"] * random.uniform(0.02, 0.15), 2)
        })
    df_alerts = pd.DataFrame(alerts)
    print(f"  ✓ Processed {len(df_alerts)} climate hazard alert records.")

    # Step 6: Build Table 5: deforestation_csrd_verification
    csrd_list = []
    commodities = [("Soja", "Brésil"), ("Cacao", "Côte d'Ivoire"), ("Huile de Palme", "Indonésie"), ("Bois / Pâte à papier", "Finlande")]

    c_idx = 1
    for ast in asset_records:
        if ast["industry_sector"] in ["Retail & CPG", "Agriculture & Ruralité", "Santé & Pharma"]:
            cid = f"CSRD-2026-{c_idx:03d}"
            comm, ctry = random.choice(commodities)

            csrd_list.append({
                "verification_id": cid,
                "asset_id": ast["asset_id"],
                "commodity_type": comm,
                "sourcing_country": ctry,
                "verified_deforestation_free": True,
                "canopy_loss_hectares": round(random.uniform(0.0, 0.4), 2),
                "audit_date": "2026-08-01"
            })
            c_idx += 1
    df_csrd = pd.DataFrame(csrd_list)
    print(f"  ✓ Processed {len(df_csrd)} CSRD Zero Deforestation verification records.")

    # Step 7: Upload CSVs & Load BigQuery
    tables_map = {
        "company_assets": df_assets,
        "sentinel_2_index": df_scenes,
        "satellites_constellations_metadonnees": df_sats,
        "inondations_incendies_alertes": df_alerts,
        "deforestation_csrd_verification": df_csrd
    }

    for tname, df in tables_map.items():
        csv_path = f"agents/earth_intel/data/{tname}.csv"
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

    print("\nSUCCESS: All 5 Earth Intel tables complete & populated in BigQuery!")

if __name__ == "__main__":
    main()
