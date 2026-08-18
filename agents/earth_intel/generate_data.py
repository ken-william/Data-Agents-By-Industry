#!/usr/bin/env python3
"""
Enriched Data Generation script for EarthIntel (skywatch_aerospace_ds.company_assets)
Covers all 10 Enterprise Industry Sectors with geospatial metrics:
- FSI (Banque & Assurance): flood_risk_score, fire_risk_score
- Santé & Pharma: stagnant_water_km2, mosquito_outbreak_risk
- Agriculture: ndvi_vegetation_index, drought_stress_index
- Transports & Mobilité: port_container_ships_waiting, logistics_congestion_index
- Énergie (Utilities): powerline_tree_encroachment_distance_m, canopy_growth_rate_pct
- Retail & CPG: deforestation_rate_pct_5y, zero_deforestation_csrd_verified
- Secteur Public: urban_heat_island_celsius, storm_damage_score
- Télécoms: canopy_density_5g_obstacle_pct, wave_propagation_clearance
- Divertissement & Cinéma: snow_cover_historical_pct, natural_scenery_score
- Sport & Infrastructures: stadium_heat_island_celsius, green_cooling_canopy_pct
"""

import os
import sys
import subprocess
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "skywatch_aerospace_ds"
TABLE_ID = "company_assets"
LOCATION = "US"

def get_client():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return bigquery.Client(project=PROJECT_ID, credentials=creds)

def setup_enriched_earthintel_data():
    client = get_client()
    
    dataset_ref = bigquery.DatasetReference(PROJECT_ID, DATASET_ID)
    try:
        dataset = client.get_dataset(dataset_ref)
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = LOCATION
        dataset.description = "Dataset d'intelligence géospatiale universelle pour EarthIntel (Sentinel-2 ESA)"
        dataset = client.create_dataset(dataset)

    schema = [
        bigquery.SchemaField("asset_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("company_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("industry_sector", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("asset_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("asset_type", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("mgrs_tile", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("latitude", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("longitude", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("city", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("region", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("country", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("criticality_score", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("annual_revenue_impact_eur", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("csrd_compliance_status", "STRING", mode="NULLABLE"),
        
        # 10 Sectors Specific Geospatial Indicators
        bigquery.SchemaField("flood_risk_score", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("fire_risk_score", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("stagnant_water_km2", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("mosquito_outbreak_risk", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("ndvi_vegetation_index", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("port_container_ships_waiting", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("powerline_tree_encroachment_m", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("deforestation_rate_pct_5y", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("urban_heat_island_celsius", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("canopy_density_5g_obstacle_pct", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("snow_cover_historical_pct", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("stadium_green_cooling_canopy_pct", "FLOAT64", mode="NULLABLE"),
    ]

    table_ref = dataset_ref.table(TABLE_ID)
    table = bigquery.Table(table_ref, schema=schema)
    client.create_table(table, exists_ok=True)
    client.query(f"TRUNCATE TABLE `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`").result()

    assets = [
        # 1. FSI (Banque & Assurance)
        ("AST-FSI-01", "AXA Assurances", "Banque & Assurance", "Portefeuille Immobilier Côte d'Azur", "Actif Immobilier Assuré", "31TDF", 43.70, 7.26, "Nice", "PACA", "France", 0.95, 250000000.0, "Compliant", 0.88, 0.72, 1.2, "Faible", 0.45, 0, 15.0, 0.0, 3.8, 12.0, 0.0, 15.0),
        ("AST-FSI-02", "BNP Paribas Real Estate", "Banque & Assurance", "Parc d'Activité Logistique Vallée du Rhône", "Immobilier Commercial", "31TFL", 45.72, 4.84, "Lyon", "Auvergne-Rhône-Alpes", "France", 0.92, 180000000.0, "Compliant", 0.78, 0.35, 2.5, "Modéré", 0.52, 0, 8.0, 0.0, 4.2, 18.0, 0.0, 22.0),

        # 2. Santé & Pharma
        ("AST-SANTE-01", "Sanofi Pasteur", "Santé & Pharma", "Complexe de Bioproduction de Marcy-l'Étoile", "Usine Vaccins & Pharma", "31TFL", 45.78, 4.71, "Marcy-l'Étoile", "Auvergne-Rhône-Alpes", "France", 0.98, 420000000.0, "Compliant", 0.25, 0.15, 8.4, "Élevé (Vecteurs Moustique)", 0.68, 0, 22.0, 0.0, 2.1, 8.0, 0.0, 35.0),
        ("AST-SANTE-02", "CHRU de Montpellier", "Santé & Pharma", "Pôle Hospitalo-Universitaire Lapeyronie", "Établissement Hospitalier", "31TDF", 43.63, 3.86, "Montpellier", "Occitanie", "France", 0.96, 310000000.0, "Compliant", 0.45, 0.62, 12.1, "Élevé (Vecteurs Moustique)", 0.38, 0, 18.0, 0.0, 4.9, 14.0, 0.0, 18.0),

        # 3. Agriculture & Ruralité
        ("AST-AGRI-01", "Coopérative Agrial", "Agriculture & Ruralité", "Bassin Céréalier et Domaines Agricoles", "Exploitation Agricole", "31TLD", 45.83, 3.12, "Clermont-Ferrand", "Auvergne-Rhône-Alpes", "France", 0.89, 125000000.0, "Compliant", 0.32, 0.40, 0.5, "Faible", 0.76, 0, 50.0, 0.0, 1.2, 5.0, 5.0, 45.0),
        ("AST-AGRI-02", "InVivo Agro", "Agriculture & Ruralité", "Grands Domaines Viticoles du Libournais", "Vignobles & Cultures", "30TYQ", 44.91, -0.24, "Libourne", "Nouvelle-Aquitaine", "France", 0.91, 165000000.0, "Compliant", 0.41, 0.30, 0.8, "Faible", 0.82, 0, 45.0, 0.0, 1.8, 6.0, 2.0, 52.0),

        # 4. Transports & Mobilité
        ("AST-TRANS-01", "CMA CGM", "Transports & Mobilité", "Terminal Portuaire de Fos-sur-Mer", "Hub Logistique Portuaire", "31TFJ", 43.43, 4.88, "Fos-sur-Mer", "PACA", "France", 0.99, 890000000.0, "Under Audit", 0.65, 0.20, 15.0, "Faible", 0.22, 28, 65.0, 0.0, 3.1, 4.0, 0.0, 8.0),
        ("AST-TRANS-02", "Grand Port Maritime de Dunkerque", "Transports & Mobilité", "Terminal à Conteneurs Flandres", "Port Maritime", "31UDS", 51.04, 2.37, "Dunkerque", "Hauts-de-France", "France", 0.96, 540000000.0, "Compliant", 0.70, 0.10, 22.0, "Faible", 0.18, 19, 80.0, 0.0, 2.8, 3.0, 0.0, 6.0),

        # 5. Énergie (Utilities)
        ("AST-NRG-01", "EDF Réseau Haute Tension", "Énergie & Climat", "Ligne HT 400kV Massif Central", "Réseau Électrique HT", "31TDH", 43.55, 2.75, "Lacaune", "Occitanie", "France", 0.99, 620000000.0, "Compliant", 0.20, 0.85, 0.3, "Faible", 0.72, 0, 2.4, 0.0, 1.5, 65.0, 12.0, 68.0),
        ("AST-NRG-02", "RTE Électricité de France", "Énergie & Climat", "Poste de Transformation de Crest", "Infrastructures Électriques", "31TGM", 44.72, 5.02, "Crest", "Auvergne-Rhône-Alpes", "France", 0.97, 410000000.0, "Compliant", 0.35, 0.78, 0.6, "Faible", 0.65, 0, 3.1, 0.0, 2.2, 58.0, 8.0, 55.0),

        # 6. Retail & CPG (Zéro Déforestation)
        ("AST-RETAIL-01", "Carrefour Group Sourcing", "Retail & CPG", "Sourcing Soja & Cacao Brésil/Paraguay", "Chaîne d'Approvisionnement", "31UDQ", 48.94, 2.49, "Aulnay-sous-Bois", "Île-de-France", "France", 0.94, 380000000.0, "Compliant (Zéro Déforestation Certifié)", 0.15, 0.10, 0.0, "Nul", 0.88, 0, 100.0, 0.0, 1.0, 2.0, 0.0, 75.0),
        ("AST-RETAIL-02", "Danone Nutricia Sourcing", "Retail & CPG", "Approvisionnement Huile de Palme Indonésie", "Sourcing Matières Premières", "31UUD", 48.91, 2.29, "Asnières-sur-Seine", "Île-de-France", "France", 0.93, 290000000.0, "Verified CSRD", 0.10, 0.05, 0.0, "Nul", 0.91, 0, 100.0, 0.0, 1.1, 3.0, 0.0, 80.0),

        # 7. Secteur Public & Territoires
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

    rows = []
    for r in assets:
        rows.append({
            "asset_id": r[0],
            "company_name": r[1],
            "industry_sector": r[2],
            "asset_name": r[3],
            "asset_type": r[4],
            "mgrs_tile": r[5],
            "latitude": r[6],
            "longitude": r[7],
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
            "stadium_green_cooling_canopy_pct": r[25],
        })

    job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)
    t_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    job = client.load_table_from_json(rows, t_id, job_config=job_config)
    job.result()
    print(f"✅ Successfully loaded {len(rows)} enriched assets across all 10 enterprise sectors for EarthIntel in {t_id}!")

if __name__ == "__main__":
    setup_enriched_earthintel_data()
