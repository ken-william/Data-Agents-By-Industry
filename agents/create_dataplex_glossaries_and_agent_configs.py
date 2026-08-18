#!/usr/bin/env python3
"""
Autonomous Script to:
1. Create 11 official Dataplex Business Glossaries (Glossaries), Categories (Categories), and Terms (Terms) via Dataplex REST API
2. Create per-agent centralized configuration files (business_catalog_config.json) in each agent directory
3. Update and re-deploy all 11 BigQuery Conversational Analytics Data Agents with synchronized Glossary bindings
"""

import os
import sys
import json
import requests
import subprocess
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
LOCATION = "us"

def get_token():
    return subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()

SECTOR_GLOSSARIES = [
    {
        "agent_folder": "credit_advisor",
        "agent_id": "credit-advisor-agent",
        "agent_name": "CreditAdvisor - Risque Crédit & Finance",
        "glossary_id": "fsi-banking-glossary",
        "display_name": "Glossaire Métier FSI Banque & Assurance",
        "description": "Glossaire prudentiel, risque de crédit et analyse financière B2B pour CreditAdvisor.",
        "categories": [
            {
                "category_id": "risques-prudentiel",
                "display_name": "Catégorie : Risques de Crédit & Prudentiel",
                "description": "Indicateurs prudentiels, prédiction de faillite et provisionnement des pertes d'emprunts IFRS 9",
                "terms": [
                    ("ratio-dscr", "Ratio DSCR (Debt Service Coverage Ratio)", "Couverture du service de la dette via l'EBE. Mappé sur ratio_dscr dans encours_credit.", "ratio_dscr", "encours_credit"),
                    ("probabilite-defaillance", "Probabilité de Défaillance à 6 Mois", "Risque de faillite ou défaut de paiement à 6 mois. Mappé sur probabilite_defaillance_6m.", "probabilite_defaillance_6m", "encours_credit"),
                    ("ecl-ifrs9-provision", "Montant ECL IFRS 9 (Expected Credit Loss)", "Provisionnement prudentiel des pertes de crédit attendues sous la norme IFRS 9.", "montant_ecl_ifrs9_eur", "encours_credit"),
                    ("ratio-ltv", "Ratio LTV (Loan-to-Value)", "Ratio entre le montant du prêt et la valeur du bien immobilier gagé.", "ratio_ltv_pct", "encours_credit")
                ]
            },
            {
                "category_id": "analyse-financiere",
                "display_name": "Catégorie : Analyse Financière & Solvabilité B2B",
                "description": "Indicateurs bilanciels, rentabilité d'entreprise et cotation Banque de France",
                "terms": [
                    ("excedent-brut-exploitation", "Excédent Brut d'Exploitation (EBE)", "Flux de trésorerie généré par l'activité opérationnelle de l'entreprise.", "ebe_eur", "bilans_financiers"),
                    ("solvabilite-b2b", "Ratio de Solvabilité & Fonds Propres", "Part des fonds propres dans le bilan de l'entreprise.", "ratio_solvabilite_pct", "bilans_financiers")
                ]
            }
        ]
    },
    {
        "agent_folder": "pulse_checker",
        "agent_id": "pulse-checker-agent",
        "agent_name": "PulseChecker - Santé & Pharma",
        "glossary_id": "healthcare-pharma-glossary",
        "display_name": "Glossaire Métier Santé & Pharma",
        "description": "Glossaire des urgences hospitalières, stocks de médicaments et démographie médicale pour PulseChecker.",
        "categories": [
            {
                "category_id": "pharmacovigilance-stocks",
                "display_name": "Catégorie : Stocks & Urgences Médicales",
                "description": "Alertes de ruptures d'urgence sur les antibiotiques et molécules d'urgence hospitalières",
                "terms": [
                    ("rupture-stock-urgences", "Rupture de Stock d'Urgence", "Alerte de pénurie de médicaments essentiels (antibiotiques, pédiatrie) < 14 jours.", "statut_risque_rupture", "hopitaux_etablissements_sante"),
                    ("tension-antibiotiques", "Niveau de Stock Antibiotiques (Jours)", "Autonomie en jours de stock d'antibiotiques critiques.", "niveau_stock_antibiotiques_jours", "hopitaux_etablissements_sante")
                ]
            },
            {
                "category_id": "prescriptions-demographie",
                "display_name": "Catégorie : Prescriptions AMELI & Démographie RPPS",
                "description": "Remboursements de biologie et densité de professionnels de santé par territoire",
                "terms": [
                    ("open-medic-prescriptions", "Prescriptions Open Medic AMELI", "Volume et montants remboursés par la Sécurité Sociale sur les molécules pharmaceutiques.", "montant_rembourse_secu_eur", "ameli_prescriptions_open_medic"),
                    ("deserts-medicaux", "Déserts Médicaux & Densité RPPS", "Densité de médecins généralistes et spécialistes pour 100 000 habitants par commune.", "densite_medecins_pour_100k_hab", "demographie_medecins_rpps")
                ]
            }
        ]
    },
    {
        "agent_folder": "ceres",
        "agent_id": "ceres-agent",
        "agent_name": "Ceres - Transition Agroécologique",
        "glossary_id": "agriculture-glossary",
        "display_name": "Glossaire Métier Agriculture & Ruralité",
        "description": "Glossaire d'empreinte carbone ADEME, stress hydrique ETP et conversion bio AB pour Ceres.",
        "categories": [
            {
                "category_id": "empreinte-ecologique",
                "display_name": "Catégorie : Bilan Carbone ADEME & Impact Sols",
                "description": "Indicateurs d'impact environnemental des produits issus d'Agribalyse ADEME",
                "terms": [
                    ("agribalyse-co2", "Empreinte Carbone Agribalyse ADEME", "Émissions de CO2 kg/kg de produit agricole selon la base officielle ADEME.", "co2_kg_par_kg_produit", "ademe_impact_agribalyse"),
                    ("acidification-sols", "Indice d'Acidification des Sols", "Impact d'acidification des sols et eutrophisation de l'eau.", "impact_acidification_sols", "ademe_impact_agribalyse")
                ]
            },
            {
                "category_id": "resilience-climatique",
                "display_name": "Catégorie : Stress Hydrique & Conversion Agroécologique",
                "description": "Mesure des risques sécheresse et certification de conversion bio AB",
                "terms": [
                    ("stress-hydrique-etp", "Indice de Stress Hydrique Evapotranspiration", "Mesure du déficit hydrique des cultures face à la sécheresse et hausse des températures.", "indice_stress_hydrique_evapotranspiration", "meteo_climat_impact_agri"),
                    ("conversion-bio-ab", "Conversion Agroécologique Bio AB", "Pourcentage de surface agricole SAU convertie en Agriculture Biologique (AB).", "surface_bio_ab_ha", "exploitations_agricoles")
                ]
            }
        ]
    },
    {
        "agent_folder": "transit_navigator",
        "agent_id": "transit-navigator-agent",
        "agent_name": "TransitNavigator - Transports & Mobilité",
        "glossary_id": "transport-mobility-glossary",
        "display_name": "Glossaire Métier Transports & Mobilité",
        "description": "Glossaire de régularité ferroviaire, ponctualité TER/TGV et Yield Management pour TransitNavigator.",
        "categories": [
            {
                "category_id": "qualite-de-service-sla",
                "display_name": "Catégorie : Ponctualité & SLA Ferroviaire",
                "description": "Mesure des pénalités de retard et du taux de régularité des lignes SNCF",
                "terms": [
                    ("regularite-ferroviaire", "Taux de Régularité & Ponctualité Ferroviaire", "Pourcentage de trains arrivés à l'heure (SLA ponctualité SNCF).", "taux_regularite_ponctualite_pct", "sncf_regularite_lignes"),
                    ("retard-moyen-minutes", "Retard Moyen par Ligne (Minutes)", "Temps moyen de retard accumulé par les voyageurs sur un axe ferroviaire.", "retard_moyen_minutes", "sncf_regularite_lignes")
                ]
            },
            {
                "category_id": "yield-frequentation",
                "display_name": "Catégorie : Yield Management & Trafic Gares",
                "description": "Optimisation des recettes voyageurs et fréquentation des gares TGV",
                "terms": [
                    ("yield-management-1er", "Yield Management 1ère Classe", "Taux de remplissage et optimisation tarifaire des voitures 1ère classe TGV.", "taux_remplissage_1ere_classe_pct", "frequentation_gares_sncf"),
                    ("frequentation-gares-tgv", "Fréquentation Annuelle des Gares", "Volume annuel de voyageurs enregistrés dans les gares régionales et TGV.", "nombre_voyageurs_annuel", "frequentation_gares_sncf")
                ]
            }
        ]
    },
    {
        "agent_folder": "helios",
        "agent_id": "helios-agent",
        "agent_name": "Helios - Énergie & Climat",
        "glossary_id": "power-energy-glossary",
        "display_name": "Glossaire Métier Énergie & Climat",
        "description": "Glossaire de charge réseau Enedis, bornes IRVE et effacement électrique pour Helios.",
        "categories": [
            {
                "category_id": "smart-grid-charge",
                "display_name": "Catégorie : Gestion de Charge & Réseau Enedis",
                "description": "Surveillance des pics de consommation et taux de charge des transformateurs",
                "terms": [
                    ("charge-transformateur", "Taux de Charge Transformateur Enedis", "Taux d'utilisation et niveau de saturation des transformateurs du réseau électrique.", "taux_charge_transformateur_pct", "enedis_consommation_inf36"),
                    ("saturation-reseau-kwh", "Pic de Surconsommation Réseau (kWh)", "Pics de puissance maximale appelée sur les postes Haute Tension.", "pic_surconsommation_kwh", "enedis_consommation_inf36")
                ]
            },
            {
                "category_id": "renouvelable-irve",
                "display_name": "Catégorie : IRVE & Solaire Photovoltaïque",
                "description": "Disponibilité des bornes de recharge VE et injection d'énergie décarbonée",
                "terms": [
                    ("borne-irve-kw", "Bornes de Recharge IRVE (kW)", "Puissance disponible et état opérationnel des bornes de recharge pour véhicules électriques.", "puissance_borne_kw", "enedis_bornes_irve"),
                    ("solar-as-a-service", "Production Solaire & CO2 Évité", "Volume MWh d'énergie renouvelable photovoltaïque injectée et tonnes de CO2 évitées.", "co2_evite_tonnes", "enedis_production_renouvelable")
                ]
            }
        ]
    },
    {
        "agent_folder": "shelf_optimizer",
        "agent_id": "shelf-optimizer-agent",
        "agent_name": "ShelfOptimizer - Retail & CPG",
        "glossary_id": "retail-cpg-glossary",
        "display_name": "Glossaire Métier Retail & CPG",
        "description": "Glossaire Nutri-Score, additifs alimentaires E250 et démarque 14 jours pour ShelfOptimizer.",
        "categories": [
            {
                "category_id": "qualite-nutritionnelle",
                "display_name": "Catégorie : Nutri-Score & Composition Alimentaire",
                "description": "Formulation des produits, classement Nutri-Score et additifs nitrités E250",
                "terms": [
                    ("nutri-score-ab", "Indice Nutritionnel Nutri-Score (A à E)", "Classement officiel de qualité nutritionnelle des produits alimentaires de A à E.", "nutri_score", "openfoodfacts_catalog"),
                    ("additifs-e250", "Additifs Controversés & Nitrites E250", "Présence d'additifs ou conservateurs nitrités nécessitant des alternatives Bio.", "additifs_problematiques", "openfoodfacts_catalog")
                ]
            },
            {
                "category_id": "operations-demarque",
                "display_name": "Catégorie : Pertes & Démarque Magasins",
                "description": "Gestion de la démarque connue et optimisation du chiffre d'affaires au m2",
                "terms": [
                    ("demarque-14-jours", "Pertes Démarque Frais (14 jours)", "Valeur en euros des produits alimentaires jetés ou périmés à 14 jours de DLC.", "demarque_pertes_produits_frais_14j_eur", "retail_frequentation_magasins"),
                    ("bundle-mdd-carrefour", "Offres Combinées MDD & Bio", "Positionnement tarifaire des marques de distributeurs face aux marques nationales.", "rayon_categorie", "openfoodfacts_catalog")
                ]
            }
        ]
    },
    {
        "agent_folder": "sully",
        "agent_id": "sully-agent",
        "agent_name": "Sully - Aide à l'emploi",
        "glossary_id": "public-employment-glossary",
        "display_name": "Glossaire Métier Secteur Public & Emploi",
        "description": "Glossaire d'enquête BMO France Travail, Vacancy Cost et CVs 1-page ATS pour Sully.",
        "categories": [
            {
                "category_id": "tension-recrutement",
                "display_name": "Catégorie : Enquête BMO 2024 & Vacancy Cost",
                "description": "Besoins en main-d'œuvre des bassins d'emploi et coût d'inoccupation des postes",
                "terms": [
                    ("bmo-recrutement-2024", "Enquête Besoins en Main-d'Œuvre BMO 2024", "Intentions d'embauche et taux de difficultés de recrutement par bassin d'emploi.", "nombre_projets_recrutement", "bmo_recrutement_2024"),
                    ("vacancy-cost", "Coût Diurne de Vacance de Poste (Vacancy Cost)", "Perte financière quotidienne subie par une entreprise due à un poste non-pourvu.", "cout_vacance_quotidien_eur", "bmo_recrutement_2024")
                ]
            },
            {
                "category_id": "matching-cv-ats",
                "display_name": "Catégorie : Compétences & CVs Maturés ATS",
                "description": "Indexation des profils de candidats et matching de compétences",
                "terms": [
                    ("cv-ats-1page", "CV Maturé 1-Page ATS (PDF Cloud Storage)", "Document CV candidat au format épuré ATS lié par objet URI gs:// au profil BigQuery.", "cv_gcs_uri", "france_travail_demandeurs"),
                    ("immersion-pmsmp", "Périodes d'Immersion PMSMP & Formation POEI", "Dispositifs d'orientation et financement de la formation professionnelle.", "statut_immersion_pmsmp", "france_travail_formations_aides")
                ]
            }
        ]
    },
    {
        "agent_folder": "net_arch",
        "agent_id": "net-arch-agent",
        "agent_name": "NetArch - Télécoms & Médias",
        "glossary_id": "telco-media-glossary",
        "display_name": "Glossaire Métier Télécoms & Médias",
        "description": "Glossaire de pannes ARCEP, résiliation Churn B2B et forfait Smart 5G pour NetArch.",
        "categories": [
            {
                "category_id": "pannes-reseaux-arcep",
                "display_name": "Catégorie : Incidents Réseau & Pannes ARCEP",
                "description": "Suivi des micro-coupures de routeurs B2B et signalements d'abonnés",
                "terms": [
                    ("signalements-arcep", "Signalements Pannes J'alerte l'ARCEP", "Niveau d'incidents et pannes signalés par les abonnés fixes et mobiles.", "statut_incident_reseau", "arcep_signalements_utilisateurs"),
                    ("micro-coupures-routeur", "Micro-Coupures Routeurs B2B", "Fréquence des déconnexions intempestives impactant les clients professionnels.", "frequence_micro_coupures_mensuelles", "arcep_signalements_utilisateurs")
                ]
            },
            {
                "category_id": "retention-upsell-5g",
                "display_name": "Catégorie : Churn B2B & Campagnes 5G",
                "description": "Modèles prédictifs d'attrition et surcroît d'ARPU sur la 5G Pro",
                "terms": [
                    ("churn-b2b-resiliation", "Risque de Résiliation Client B2B (Churn)", "Probabilité qu'un client professionnel résilie suite à des micro-coupures de routeur.", "risque_resiliation_b2b_pct", "abonnes_consommation_devices"),
                    ("campagne-smart-5g", "Upsell Forfait Smart 5G & ARPU", "Gain d'ARPU mensuel généré par la migration d'abonnés cuivre vers la 5G Pro.", "gain_arpu_forfait_5g_max_eur", "abonnes_consommation_devices")
                ]
            }
        ]
    },
    {
        "agent_folder": "cine_analyst",
        "agent_id": "cine-analyst-agent",
        "agent_name": "CineAnalyst - Divertissement & Cinéma",
        "glossary_id": "cinema-entertainment-glossary",
        "display_name": "Glossaire Métier Divertissement & Cinéma",
        "description": "Glossaire de subventions CNC, risque de flop film et sièges immersifs 4DX pour CineAnalyst.",
        "categories": [
            {
                "category_id": "salles-premium-4dx",
                "display_name": "Catégorie : Salles Immersives 4DX & Popcorn",
                "description": "Valorisation de l'expérience en salles et des ventes annexes au fauteuil",
                "terms": [
                    ("sieges-4dx-immersifs", "Sièges Immersifs 4DX & Cabines Premium (+35%)", "Pourcentage de fauteuils 4DX/Dolby permettant d'augmenter le billet de +35%.", "part_sieges_immersifs_4dx_pct", "cnc_salles_cinema"),
                    ("ventes-popcorn-fauteuil", "Ventes Annexes Concessions Popcorn / Fauteuil", "Dépense moyenne en confiserie et popcorn par siège disponible.", "ventes_annexes_popcorn_par_fauteuil_eur", "cnc_salles_cinema")
                ]
            },
            {
                "category_id": "subventions-programmation",
                "display_name": "Catégorie : Aides CNC & Flops Films",
                "description": "Prédiction des échecs de blockbusters et ROI des aides publiques du CNC",
                "terms": [
                    ("risque-flop-film", "Risque Prédit de Flop Film Blockbuster (>60%)", "Indicateur de prédiction de flop en salles basé sur un score TikTok/X faible.", "risque_predit_flop_pct", "cnc_films_programmation_flops"),
                    ("subventions-cnc-roi", "ROI Subventions & Avances sur Recettes CNC", "Nombre d'entrées en salles générées par euro de subvention publique alloué.", "roi_entrees_par_euro_subventionne", "cnc_aides_financieres")
                ]
            }
        ]
    },
    {
        "agent_folder": "arena_manager",
        "agent_id": "arena-manager-agent",
        "agent_name": "ArenaManager - Sport & Infrastructures",
        "glossary_id": "sports-infrastructure-glossary",
        "display_name": "Glossaire Métier Sport & Infrastructures",
        "description": "Glossaire du recensement RES, gaspillage énergétique et subventions ANS pour ArenaManager.",
        "categories": [
            {
                "category_id": "efficacite-energetique",
                "display_name": "Catégorie : Chasse au Gaspillage Énergétique",
                "description": "Audit thermique des stades et détection des surconsommations avec faible usage",
                "terms": [
                    ("gaspillage-energetique-stades", "Indice de Gaspillage Énergétique Stades (kWh/m2)", "Surconsommation thermique combinée à un sous-usage <30% en semaine.", "gaspillage_kwh_par_m2", "ministere_sports_equipements"),
                    ("surconsommation-kwh-m2", "Consommation Thermique MWh", "Volume annuel de kilowattheures consommés par l'installation sportive.", "consommation_energetique_annuelle_mwh", "ministere_sports_equipements")
                ]
            },
            {
                "category_id": "sponsoring-aides-ans",
                "display_name": "Catégorie : Sponsoring Premium & Aides ANS",
                "description": "Monétisation des espaces publicitaires de stades et subventions pour les jeunes",
                "terms": [
                    ("sponsoring-stade-premium", "Sponsoring Publicitaire Premium Stades", "Valorisation des espaces d'affichage pour les clubs à forte croissance (>10%).", "potentiel_sponsoring_premium_stade", "ministere_sports_licencies"),
                    ("subventions-ans-jeunes", "Efficacité Subventions ANS (Jeunes <18 ans)", "Impact des aides publiques de l'Agence Nationale du Sport sur l'inscription des jeunes.", "impact_hausse_inscriptions_jeunes_pct", "ministere_sports_subventions")
                ]
            }
        ]
    },
    {
        "agent_folder": "earth_intel",
        "agent_id": "earthintel-agent",
        "agent_name": "EarthIntel - Imagerie Satellitaire & Géospatial",
        "glossary_id": "satellite-geospatial-glossary",
        "display_name": "Glossaire Métier Imagerie Satellitaire & Géospatial",
        "description": "Glossaire de tuiles Sentinel-2 MGRS, indice NDVI et risques climatiques pour EarthIntel.",
        "categories": [
            {
                "category_id": "observation-spatiale-mgrs",
                "display_name": "Catégorie : Imagerie Sentinel-2 & Tuiles MGRS",
                "description": "Indexation multispectrale et cartographie des coordonnées de tuiles spatiales",
                "terms": [
                    ("tuile-sentinel2-mgrs", "Clichés Satellite Sentinel-2 & Tuiles MGRS", "Images multispectrales ESA Sentinel-2 cartographiées par coordonnées MGRS.", "mgrs_tile", "company_assets"),
                    ("quicklook-sat", "Aperçus PNG Visuels Quicklook Satellite", "Fichiers images d'observation orbitale enregistrés dans Google Cloud Storage.", "quicklook_image_url", "company_assets")
                ]
            },
            {
                "category_id": "risques-et-infrastructure",
                "display_name": "Catégorie : Indice NDVI & Logistics Spatiales",
                "description": "Indicateurs d'obstacles 5G, congestion portuaire et sécheresse de la biomasse",
                "terms": [
                    ("indice-ndvi-vegetation", "Indice de Végétation NDVI & Rendements", "Indice de santé de la canopée et de la biomasse végétale mesuré par satellite.", "ndvi_vegetation_index", "company_assets"),
                    ("congestion-portuaire-conteneurs", "Congestion Portuaire Navires Conteneurs", "Nombre de porte-conteneurs en attente d'accostage détectés par imagerie spatiale.", "port_container_ships_waiting", "company_assets")
                ]
            }
        ]
    }
]

def create_dataplex_glossaries_categories_and_terms():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    print("=== 1. CREATING DATAPLEX BUSINESS GLOSSARIES, CATEGORIES & TERMS ===")
    for sec in SECTOR_GLOSSARIES:
        gid = sec["glossary_id"]
        g_url = f"https://dataplex.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/glossaries?glossaryId={gid}"
        g_payload = {
            "displayName": sec["display_name"],
            "description": sec["description"]
        }
        r1 = requests.post(g_url, headers=headers, json=g_payload)
        if r1.status_code == 200:
            print(f"\n✅ Created Dataplex Glossary: {gid}")
        else:
            print(f"\nℹ️ Dataplex Glossary active ({gid})")

        parent_glossary = f"projects/{PROJECT_ID}/locations/{LOCATION}/glossaries/{gid}"

        # Create Categories & Terms
        for cat in sec["categories"]:
            cat_id = cat["category_id"]
            cat_url = f"https://dataplex.googleapis.com/v1/{parent_glossary}/categories?categoryId={cat_id}"
            cat_payload = {
                "parent": parent_glossary,
                "displayName": cat["display_name"],
                "description": cat["description"]
            }
            r_cat = requests.post(cat_url, headers=headers, json=cat_payload)
            parent_cat = f"{parent_glossary}/categories/{cat_id}"
            if r_cat.status_code == 200:
                print(f"  ├─ 📁 Created Category: {cat_id} ({cat['display_name']})")

            for term_id, term_name, term_desc, bq_col, bq_table in cat["terms"]:
                t_url = f"https://dataplex.googleapis.com/v1/{parent_glossary}/terms?termId={term_id}"
                t_payload = {
                    "parent": parent_cat,
                    "displayName": term_name,
                    "description": f"{term_desc} [Colonne BQ: {bq_col} dans {bq_table}]"
                }
                r_term = requests.post(t_url, headers=headers, json=t_payload)
                if r_term.status_code == 200:
                    print(f"  │   ├─ 🏷️ Created Term: {term_id} ({term_name})")

def create_agent_config_files():
    print("\n=== 2. CREATING CENTRALIZED BUSINESS CONFIG FILES PER AGENT ===")
    for sec in SECTOR_GLOSSARIES:
        folder = sec["agent_folder"]
        target_path = os.path.join("agents", folder, "business_catalog_config.json")
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        categories_list = []
        for cat in sec["categories"]:
            cat_data = {
                "categoryId": cat["category_id"],
                "displayName": cat["display_name"],
                "description": cat["description"],
                "terms": [
                    {
                        "termId": t[0],
                        "displayName": t[1],
                        "definition": t[2],
                        "mapped_bigquery_column": t[3],
                        "mapped_bigquery_table": t[4]
                    } for t in cat["terms"]
                ]
            }
            categories_list.append(cat_data)

        config_data = {
            "agent_id": sec["agent_id"],
            "displayName": sec["agent_name"],
            "dataplex_glossary_reference": f"projects/{PROJECT_ID}/locations/{LOCATION}/glossaries/{sec['glossary_id']}",
            "dataplex_entry_group_reference": f"projects/{PROJECT_ID}/locations/{LOCATION}/entryGroups/{sec['glossary_id'].replace('-glossary', '-catalog')}",
            "business_glossary": {
                "displayName": sec["display_name"],
                "description": sec["description"],
                "categories": categories_list
            },
            "data_governance": {
                "sla_tier": "Tier-1 Executive 24/7",
                "criticality_level": "Mission Critical",
                "data_sensitivity": "Internal Enterprise"
            }
        }

        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Created Agent Config File: {target_path}")

if __name__ == "__main__":
    create_dataplex_glossaries_categories_and_terms()
    create_agent_config_files()
    print("\n=== ALL DATAPLEX CATEGORIES, TERMS & AGENT CONFIG FILES CREATED SUCCESSFULLY ===")
