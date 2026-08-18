#!/usr/bin/env python3
"""
Populates Dataplex Knowledge Catalog Entry Groups with structured Dataplex Entries and Aspects
for ALL 11 Industry Datasets in Google BigQuery.
"""

import os
import sys
import subprocess
from google.oauth2.credentials import Credentials
from google.cloud import dataplex_v1

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
LOCATION = "us"

def get_client():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return dataplex_v1.CatalogServiceClient(credentials=creds)

CATALOG_ENTRIES = [
    # 1. FSI Banking & Assurance
    ("fsi-banking-catalog", "bq-encours-credit", "fsi_creditadvisor_dataset", "encours_credit",
     "FSI Banque & Assurance",
     "Risque de crédit, Défaillance 6 mois, Score ECL IFRS 9, Ratio DSCR, Ratio LTV, Prêt immobilier, Taux Euribor",
     "Direction des Risques & Credit Risk Advisor"),
    ("fsi-banking-catalog", "bq-bilans-financiers", "fsi_creditadvisor_dataset", "bilans_financiers",
     "FSI Banque & Assurance",
     "Bilans comptables, Solvabilité entreprise, EBE, Chiffre d'affaires, Endettement net, Ratio de levier, Fond de roulement",
     "Direction de l'Analyse Financière B2B"),
    ("fsi-banking-catalog", "bq-entreprises", "fsi_creditadvisor_dataset", "entreprises",
     "FSI Banque & Assurance",
     "SIREN, SIRET, Code NAF, Note FIBEN Banque de France, Effectif salarié, Cotation de crédit",
     "Référentiel Client Entreprises"),

    # 2. Santé & Pharma
    ("healthcare-pharma-catalog", "bq-hopitaux-sante", "healthcare_pharma_ds", "hopitaux_etablissements_sante",
     "Santé & Pharma",
     "Hôpitaux, Lits de réanimation, Rupture de stock d'urgence, Pénurie d'antibiotiques, Déserts médicaux",
     "Direction des Affaires Médicales & PulseChecker"),
    ("healthcare-pharma-catalog", "bq-prescriptions-medic", "healthcare_pharma_ds", "ameli_prescriptions_open_medic",
     "Santé & Pharma",
     "Open Medic AMELI, Prescriptions pharmaceutiques, Remboursements Sécurité Sociale, Molécules actives",
     "Direction de la Pharmacovigilance"),

    # 3. Agriculture & Ruralité
    ("agriculture-catalog", "bq-ademe-agribalyse", "agriculture_rurality_ds", "ademe_impact_agribalyse",
     "Agriculture & Ruralité",
     "ADEME Agribalyse, Bilan Carbone CO2, Empreinte environnementale, Acidification des sols, Eutrophisation",
     "Direction de la Transition Écologique Ceres"),
    ("agriculture-catalog", "bq-meteo-climat-agri", "agriculture_rurality_ds", "meteo_climat_impact_agri",
     "Agriculture & Ruralité",
     "Stress hydrique ETP, Evapotranspiration, Précipitations, Sécheresse agricole, Rendement récoltes",
     "Observatoire Climat & Agroécologie"),

    # 4. Transports & Mobilité
    ("transport-mobility-catalog", "bq-sncf-regularite", "transport_mobility_ds", "sncf_regularite_lignes",
     "Transports & Mobilité",
     "Régularité ferroviaire, Ponctualité TER/TGV, Retard moyen minutes, SLA ferroviaire, Yield 1ère classe",
     "Direction de la Qualité de Service TransitNavigator"),
    ("transport-mobility-catalog", "bq-frequentation-gares", "transport_mobility_ds", "frequentation_gares_sncf",
     "Transports & Mobilité",
     "Fréquentation gares SNCF, Flux voyageurs annuels, Intermodalité, Gares TGV",
     "Direction des Gares & Connexions"),

    # 5. Énergie & Climat
    ("power-energy-catalog", "bq-enedis-consommation", "power_energy_ds", "enedis_consommation_inf36",
     "Énergie & Climat",
     "Consommation Enedis Linky, Taux de charge transformateur, Saturation réseau, Surconsommation kWh",
     "Direction Enedis Smart Grid & Helios"),
    ("power-energy-catalog", "bq-enedis-irve", "power_energy_ds", "enedis_bornes_irve",
     "Énergie & Climat",
     "Infrastructure IRVE, Bornes de recharge véhicules électriques, Puissance kW, Effacement réseau",
     "Direction Mobilité Électrique"),

    # 6. Retail & CPG
    ("retail-cpg-catalog", "bq-openfoodfacts", "retail_cpg_ds", "openfoodfacts_catalog",
     "Retail & CPG",
     "Nutri-Score A-E, Score NOVA 1-4, Additif controversé E250, Alternative saine Bio, Photothèque GCS",
     "Direction de la Qualité Alimentaire ShelfOptimizer"),
    ("retail-cpg-catalog", "bq-retail-magasins", "retail_cpg_ds", "retail_frequentation_magasins",
     "Retail & CPG",
     "Fréquentation supermarchés, Démarque produits frais 14 jours, Ventes au m2, Promotion catalogue",
     "Direction des Opérations Magasins"),

    # 7. Secteur Public & Emploi
    ("public-employment-catalog", "bq-bmo-recrutement", "public_sector_employment_ds", "bmo_recrutement_2024",
     "Secteur Public & Emploi",
     "Enquête BMO 2024 France Travail, Intentions d'embauche, Métiers en tension, Vacancy Cost",
     "Direction des Politiques de l'Emploi Sully"),
    ("public-employment-catalog", "bq-demandeurs-cv", "public_sector_employment_ds", "france_travail_demandeurs",
     "Secteur Public & Emploi",
     "Demandeurs d'emploi, Matching compétences, Diplômes, CVs 1-page ATS PDF GCS, Immersion PMSMP",
     "Direction des Opérations Agences Emploi"),

    # 8. Télécoms & Médias
    ("telco-media-catalog", "bq-arcep-signalements", "telco_media_ds", "arcep_signalements_utilisateurs",
     "Télécoms & Médias",
     "J'alerte l'ARCEP, Pannes réseaux fixes et mobiles, Micro-coupures routeurs B2B, SLA Télécom",
     "Direction Qualité Réseau NetArch"),
    ("telco-media-catalog", "bq-abonnes-consumption", "telco_media_ds", "abonnes_consommation_devices",
     "Télécoms & Médias",
     "Consommation data Go, Frais hors-forfait, Churn B2B, Campagne Smart 5G, Upsell ARPU",
     "Direction Marketing B2B Télécom"),

    # 9. Divertissement & Cinéma
    ("cinema-entertainment-catalog", "bq-cnc-salles", "entertainment_cinema_ds", "cnc_salles_cinema",
     "Divertissement & Cinéma",
     "CNC Salles de cinéma, Sièges immersifs 4DX (+35%), Ventes annexes popcorn/fauteuil, Recettes billetterie",
     "Direction de l'Exploitation Cinématographique CineAnalyst"),
    ("cinema-entertainment-catalog", "bq-cnc-flops", "entertainment_cinema_ds", "cnc_films_programmation_flops",
     "Divertissement & Cinéma",
     "Risque prédit de flop film >60%, Buzz TikTok/X, Réajustement séances grand public",
     "Direction de la Programmation Salles"),

    # 10. Sport & Infrastructures
    ("sports-infrastructure-catalog", "bq-sports-equipements", "sports_infrastructure_ds", "ministere_sports_equipements",
     "Sport & Infrastructures",
     "Recensement RES Ministère des Sports, Gaspillage énergétique kWh/m2, Taux d'utilisation <30% semaine, Piscines 50m",
     "Direction des Sports & ArenaManager"),
    ("sports-infrastructure-catalog", "bq-sports-licencies", "sports_infrastructure_ds", "ministere_sports_licencies",
     "Sport & Infrastructures",
     "Licenciés par fédération, Part jeunes <18 ans %, Sponsoring publicitaire premium stades, Croissance +10%",
     "Direction du Développement Sportif Local"),

    # 11. Imagerie Satellitaire & Géospatial
    ("satellite-geospatial-catalog", "bq-company-assets", "skywatch_aerospace_ds", "company_assets",
     "Imagerie Satellitaire & Géospatial",
     "Sites industriels, Indice NDVI végétation, Risque inondation/incendie, Eaux stagnantes moustiques, Canopée 5G",
     "Direction Géospatiale & EarthIntel")
]

def populate_dataplex_catalog():
    client = get_client()

    aspect_type_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/aspectTypes/enterprise-business-glossary"
    aspect_key = f"{PROJECT_ID}.{LOCATION}.enterprise-business-glossary"
    entry_type_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/entryTypes/dataset-table"

    print(f"=== POPULATING DATAPLEX KNOWLEDGE CATALOG WITH {len(CATALOG_ENTRIES)} ENTRIES ===")

    for eg_id, entry_id, dataset_id, table_id, sector, jargon, owner in CATALOG_ENTRIES:
        parent = f"projects/{PROJECT_ID}/locations/{LOCATION}/entryGroups/{eg_id}"

        entry = dataplex_v1.Entry()
        entry.entry_type = entry_type_name
        entry.fully_qualified_name = f"bigquery:{PROJECT_ID}.{dataset_id}.{table_id}"

        aspect = dataplex_v1.Aspect()
        aspect.aspect_type = aspect_type_name
        aspect.data = {
            "industry_sector": sector,
            "business_jargon_terms": jargon,
            "data_owner": owner
        }

        entry.aspects[aspect_key] = aspect

        try:
            created = client.create_entry(parent=parent, entry_id=entry_id, entry=entry)
            print(f"✅ Created Entry: {entry_id:<25} in {eg_id}")
        except Exception as e:
            if "already exists" in str(e).lower() or "409" in str(e):
                print(f"ℹ️ Entry already exists: {entry_id:<25} in {eg_id}")
            else:
                print(f"❌ Error creating entry {entry_id} in {eg_id}: {e}")

    print("=== DATAPLEX KNOWLEDGE CATALOG POPULATION COMPLETED ===")

if __name__ == "__main__":
    populate_dataplex_catalog()
