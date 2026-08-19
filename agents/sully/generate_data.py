#!/usr/bin/env python3
"""
Refined Relational Data Pipeline for Sully - France Travail & URSSAF Recruitment Intelligence Platform.
Populates BigQuery dataset `public_sector_employment_ds` with 7 fully interconnected tables:

1. `bmo_recrutement_2025`: 50,076 authentic France Travail BMO 2025 recruitment forecast records.
2. `rome_arborescence_2024`: 12,243 authentic France Travail ROME 4.0 job titles, appellations, and domain classifications.
3. `entreprises_urssaf_declarations`: Company establishments with SIRET, NAF, employee counts, payroll, and OETH disability gaps.
4. `offres_emploi_recrutement`: Job vacancies with vacancy duration > 6 months, daily vacancy costs, rejection rates & motifs.
5. `france_travail_demandeurs`: Talent profiles including explicit record for Anna FT-99720068.
6. `candidatures_postulations_suivi`: ATS applications linking candidates, job offers, companies, matching scores & refusal motifs.
7. `france_travail_formations_aides`: Vocational training courses (POEI, AFPR, PMSMP immersion 15j) and recruitment subsidies.
"""

import os
import sys
import glob
import re
import csv
import random
import subprocess
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "public_sector_employment_ds"
LOCATION = "US"
BUCKET_NAME = f"gs://talktodata-sully-raw-data"
RESUMES_BUCKET = "gs://sully-candidate-resumes-data-agents"
BMO_EXCEL_PATH = os.path.join(os.path.dirname(__file__), "data", "bmo_recrutement_2025.xlsx")
ROME_EXCEL_PATH = os.path.join(os.path.dirname(__file__), "data", "rome_arborescence_2024.xlsx")
RESUMES_DIR = os.path.join(os.path.dirname(__file__), "data", "resumes")

GRAND_DOMAINES_MAP = {
    "A": "Agriculture et Pêche, Espaces naturels et Espaces verts",
    "B": "Arts et Façonnage d'ouvrages d'art",
    "C": "Banque, Assurance, Immobilier",
    "D": "Commerce, Vente et Grande distribution",
    "E": "Communication, Média et Multimédia",
    "F": "Construction, Bâtiment et Travaux publics",
    "G": "Hôtellerie-Restauration, Tourisme, Loisirs et Animation",
    "H": "Industrie",
    "I": "Installation et Maintenance",
    "J": "Santé",
    "K": "Services à la personne et à la collectivité",
    "L": "Spectacle",
    "M": "Information et Communication / Informatique",
    "N": "Transport et Logistique"
}

REAL_COMPANIES_SAMPLE = [
    ("35600000000014", "Hôpital national de paris", "8610Z - Activités hospitalières", "Santé & Établissements Hospitaliers", "Établissement Public", 45000, 1850000000.0, 120, "75004", "75", "Île-de-France", "Paris", "QPV - Quartier Prioritaire"),
    ("77568000000028", "Hôpitaux Civils de Lyon (HCL)", "8610Z - Activités hospitalières", "Santé & Établissements Hospitaliers", "Établissement Public", 24000, 980000000.0, 45, "69002", "69", "Auvergne-Rhône-Alpes", "Lyon", "Zone Standard"),
    ("32630000000042", "TF1 Group", "6020Z - Édition de chaînes de télévision", "Média, Télévision & Multimédia", "SA à Conseil d'administration", 3200, 240000000.0, 18, "92100", "92", "Île-de-France", "Boulogne-Billancourt", "Zone Standard"),
    ("88910000000012", "ACC - Automotive Cells Company", "2720Z - Fabrication de piles et d'accumulateurs", "Fabrication de Batteries & Gigafactory", "SAS", 1800, 95000000.0, 8, "59500", "59", "Hauts-de-France", "Douai", "Zone Standard"),
    ("89920000000023", "Envision AESC Douai", "2720Z - Fabrication de batteries lithium-ion", "Fabrication de Batteries & Gigafactory", "SAS", 1200, 72000000.0, 6, "59500", "59", "Hauts-de-France", "Douai", "Zone Standard"),
    ("89930000000034", "Verkor Dunkerque", "2720Z - Fabrication de batteries pour véhicules électriques", "Fabrication de Batteries & Gigafactory", "SAS", 1500, 88000000.0, 10, "59140", "59", "Hauts-de-France", "Dunkerque", "Zone Standard"),
    ("89940000000045", "Prologium Dunkerque", "2720Z - Recherche & Fabrication de batteries solides", "Fabrication de Batteries & Gigafactory", "SAS", 850, 52000000.0, 4, "59140", "59", "Hauts-de-France", "Dunkerque", "Zone Standard"),
    ("33790000000055", "Capgemini France", "6202A - Conseil en systèmes informatiques", "Services Informatiques & ESN", "SAS", 28000, 1420000000.0, 85, "92130", "92", "Île-de-France", "Issy-les-Moulineaux", "Zone Standard"),
    ("54200000000068", "Sanofi France", "2120Z - Fabrication de préparations pharmaceutiques", "Industrie Pharmaceutique & Santé", "SA", 19500, 1150000000.0, 32, "75008", "75", "Île-de-France", "Paris", "Zone Standard"),
    ("38012000000084", "SNCF Voyageurs", "4910Z - Transport ferroviaire de voyageurs", "Transport & Logistique", "SA", 68000, 2900000000.0, 140, "93200", "93", "Île-de-France", "Saint-Denis", "QPV - Quartier Prioritaire")
]

STATUTS_CANDIDATURE = [
    "Candidature Transmise", "Entretien RH Planifié", "Entretien Technique / Métier",
    "Offre / Proposition d'Embauche", "Refusé après entretien", "Embauché (Accès à l'emploi)"
]

DISPOSITIFS_AIDES_NOMS = [
    "AFPR (Action de Formation Préalable à l'Emploi)",
    "POEI (Préparation Opérationnelle à l'Emploi Individuelle)",
    "PMSMP (Immersion en Entreprise 15j)",
    "Aid'Emploi ZFU / QPV Recrutement",
    "Prime Reprise d'Activité AGEFIPH (Handicap)",
    "Compte Personnel de Formation (CPF Co-financé)"
]

CONTRACT_TYPES = ["CDI", "CDD", "Alternance", "Intérim"]

def get_client():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return bigquery.Client(project=PROJECT_ID, credentials=creds)

def parse_local_pdf_cv(pdf_path):
    if not os.path.exists(pdf_path):
        return None

    try:
        txt = subprocess.check_output(["pdftotext", pdf_path, "-"]).decode("utf-8", errors="ignore")
    except Exception:
        txt = ""

    filename = os.path.basename(pdf_path).replace(".pdf", "")
    dem_id = filename.replace("cv_", "").strip()

    name_match = re.search(r"([A-ZÉÈÊËÀÂÄÔÖÛÜÇ]{2,}\s+[A-ZÉÈÊËÀÂÄÔÖÛÜÇ]{2,})", txt)
    name = name_match.group(1).title() if name_match else f"Candidat {dem_id}"

    dept_match = re.search(r"📍\s*(\d{2,3})\s*-", txt)
    dept = dept_match.group(1) if dept_match else "75"

    deg_match = re.search(r"🎓\s*([^|\n]+)", txt)
    degree = deg_match.group(1).strip() if deg_match else "Bac+3"

    target_match = re.search(r"vers le métier de ([^.\n]+)", txt)
    target_role = target_match.group(1).strip() if target_match else "Data Analyst & Business Intelligence"

    gcs_uri = f"{RESUMES_BUCKET}/resumes/{os.path.basename(pdf_path)}"

    return {
        "demandeur_id": dem_id,
        "nom_prenom": name,
        "statut_recherche": "Recherche Active",
        "categorie_inscription": "Catégorie A",
        "anciennete_chomage_mois": random.randint(2, 24),
        "metier_recherche": target_role,
        "department_code": dept,
        "region_name": "Île-de-France" if dept in ["75", "92", "93", "94", "78", "91", "95"] else "Hauts-de-France",
        "freins_emploi_detail": "Aucun frein majeur identifié, disponible immédiatement.",
        "competences_actuelles": "Maîtrise bureautique, Analyse de données, Gestion de projet",
        "cv_gcs_uri": gcs_uri,
        "cv_text_content": txt[:1200].replace("\n", " ").strip(),
        "niveau_etudes": degree
    }

def main():
    print(f"Initializing Refined Sully Relational Pipeline for project '{PROJECT_ID}'...")
    client = get_client()

    os.makedirs("agents/sully/data", exist_ok=True)

    # 1. bmo_recrutement_2025
    if os.path.exists(BMO_EXCEL_PATH):
        print(f"  Parsing authentic France Travail BMO 2025 Open Data Excel dataset...")
        df_bmo_raw = pd.read_excel(BMO_EXCEL_PATH, sheet_name="BMO_2025_open_data")

        bmo_rows = []
        for _, row in df_bmo_raw.iterrows():
            code_metier = str(row.get("Code métier BMO", "")).strip()
            nom_metier = str(row.get("Nom métier BMO", "")).strip()
            famille = str(row.get("Lbl_fam_met", "")).strip()
            reg_code = str(row.get("REG", "")).strip()
            reg_nom = str(row.get("NOM_REG", "")).strip()
            dept_code = str(row.get("Dept", "")).strip()
            dept_nom = str(row.get("NomDept", "")).strip()
            be_code = str(row.get("BE25", "")).strip()
            be_nom = str(row.get("NOMBE25", "")).strip()

            def parse_num(v):
                v_str = str(v).strip()
                if v_str in ["*", "nan", "None", ""]:
                    return 0
                try:
                    return int(float(v_str))
                except Exception:
                    return 0

            met = parse_num(row.get("met"))
            xmet = parse_num(row.get("xmet"))
            smet = parse_num(row.get("smet"))

            diff_pct = round((xmet / met * 100.0), 1) if met > 0 else 0.0

            bmo_rows.append({
                "code_metier_bmo": code_metier,
                "nom_metier_bmo": nom_metier,
                "famille_metier_libelle": famille,
                "code_region": reg_code,
                "nom_region": reg_nom,
                "code_departement": dept_code,
                "nom_departement": dept_nom,
                "code_bassin_emploi": be_code,
                "nom_bassin_emploi": be_nom,
                "projets_recrutement_nombre": met,
                "recrutements_difficiles_nombre": xmet,
                "recrutements_saisonniers_nombre": smet,
                "part_recrutements_difficiles_pct": diff_pct
            })

        df_bmo = pd.DataFrame(bmo_rows)
    else:
        raise FileNotFoundError(f"Missing BMO dataset: {BMO_EXCEL_PATH}")

    # Extract unique metiers and departments
    bmo_metiers = df_bmo[["code_metier_bmo", "nom_metier_bmo", "famille_metier_libelle"]].drop_duplicates().to_dict("records")
    bmo_depts = df_bmo[["code_departement", "nom_departement", "nom_region"]].drop_duplicates().to_dict("records")

    # 2. rome_arborescence_2024
    if os.path.exists(ROME_EXCEL_PATH):
        print(f"  Parsing official France Travail ROME 4.0 Arborescence dataset...")
        df_rome_raw = pd.read_excel(ROME_EXCEL_PATH, sheet_name="Arbo Principale 24-06-2024")

        rome_rows = []
        last_gd = "M"
        last_dp = "M18"
        last_rome = "M1801"

        for _, row in df_rome_raw.iterrows():
            c0 = str(row.iloc[0]).strip() if pd.notnull(row.iloc[0]) else ""
            c1 = str(row.iloc[1]).strip() if pd.notnull(row.iloc[1]) else ""
            c2 = str(row.iloc[2]).strip() if pd.notnull(row.iloc[2]) else ""
            c3 = str(row.iloc[3]).strip() if pd.notnull(row.iloc[3]) else ""
            c4 = str(row.iloc[4]).strip() if pd.notnull(row.iloc[4]) else ""

            if c0 in GRAND_DOMAINES_MAP:
                last_gd = c0
            if c1 and len(c1) <= 3:
                last_dp = f"{last_gd}{c1}"
            if c2 and len(c2) == 2:
                last_rome = f"{last_dp}{c2}"

            if c3 and c3 not in GRAND_DOMAINES_MAP.values():
                gd_lbl = GRAND_DOMAINES_MAP.get(last_gd, "Services et Tertiaire")
                rome_rows.append({
                    "code_rome": last_rome,
                    "intitule_rome_appellation": c3,
                    "grand_domaine_code": last_gd,
                    "grand_domaine_libelle": gd_lbl,
                    "domaine_prof_code": last_dp,
                    "domaine_prof_libelle": f"Domaine {last_dp}",
                    "code_ogr": c4
                })

        df_rome = pd.DataFrame(rome_rows)
    else:
        raise FileNotFoundError(f"Missing ROME dataset: {ROME_EXCEL_PATH}")

    rome_codes = df_rome["code_rome"].unique().tolist()

    # 3. entreprises_urssaf_declarations
    companies = []
    for item in REAL_COMPANIES_SAMPLE:
        companies.append({
            "siret": item[0],
            "company_name": item[1],
            "sector_naf": item[2],
            "secteur_activite_libelle": item[3],
            "legal_status": item[4],
            "employee_count": item[5],
            "total_payroll_eur": item[6],
            "oeth_target_deficit_count": item[7],
            "postal_code": item[8],
            "department_code": item[9],
            "region_name": item[10],
            "city_name": item[11],
            "zone_type": item[12]
        })

    sectors = [
        "6201Z - Programmation informatique", "8610Z - Activités hospitalières", "4711D - Supermarchés", 
        "4910Z - Transport ferroviaire", "2120Z - Industrie pharmaceutique", "7022Z - Conseil pour les affaires",
        "4321A - Travaux d'installation électrique", "5610A - Restauration traditionnelle", "8411Z - Administration publique générale"
    ]
    legal_statuses = ["SA", "SAS", "SARL", "Établissement Public", "ETI"]
    zone_types = ["Zone Standard", "QPV - Quartier Prioritaire", "ZRR - Zone Revitalisation Rurale"]

    for i in range(11, 4501):
        siret = f"4{random.randint(1000000000000, 9999999999999)}"
        dept_info = random.choice(bmo_depts)
        dept_code = dept_info["code_departement"]
        reg_name = dept_info["nom_region"]
        city = f"Ville-{dept_code}-{i % 50}"

        emp_count = random.randint(15, 8500)
        payroll = round(emp_count * random.uniform(32000.0, 58000.0), 2)
        oeth_deficit = random.randint(0, 45) if emp_count > 20 else 0

        sec_naf = random.choice(sectors)
        sec_lbl = sec_naf.split(" - ")[1] if " - " in sec_naf else "Industrie & Services"

        companies.append({
            "siret": siret,
            "company_name": f"Entreprise-{dept_info['nom_departement']}-{i}",
            "sector_naf": sec_naf,
            "secteur_activite_libelle": sec_lbl,
            "legal_status": random.choice(legal_statuses),
            "employee_count": emp_count,
            "total_payroll_eur": payroll,
            "oeth_target_deficit_count": oeth_deficit,
            "postal_code": f"{dept_code}000" if len(dept_code) == 2 else f"0{dept_code}00",
            "department_code": dept_code,
            "region_name": reg_name,
            "city_name": city,
            "zone_type": random.choice(zone_types)
        })

    df_companies = pd.DataFrame(companies)

    # 4. offres_emploi_recrutement
    job_offers = []
    base_date = datetime(2025, 1, 15)

    # Scenario 1 Specific Offers for Hôpital national de paris (> 6 months vacancy, high daily cost)
    sante_vacancies_hnp = [
        ("OFFRE-HNP-001", "35600000000014", "Hôpital national de paris", "Santé & Établissements Hospitaliers", "J1501", "J1501", "Infirmier de Soins Généraux et Bloc Opératoire", "CDI", 24, 42000.0, 0, "75", "Île-de-France", True, 215, 380.00, 81700.00, 68.5, "Contraintes d'horaires de nuit & Salaire fixe non attractif"),
        ("OFFRE-HNP-002", "35600000000014", "Hôpital national de paris", "Santé & Établissements Hospitaliers", "J1102", "J1102", "Médecin Urgentiste & Réanimateur", "CDI", 48, 85000.0, 0, "75", "Île-de-France", True, 240, 650.00, 156000.00, 74.0, "Charge de travail extrême & Pénurie nationale de praticiens"),
        ("OFFRE-HNP-003", "35600000000014", "Hôpital national de paris", "Santé & Établissements Hospitaliers", "J1502", "J1502", "Aide-Soignant en Services de Neurologie", "CDI", 12, 29000.0, 0, "75", "Île-de-France", True, 195, 220.00, 42900.00, 62.0, "Pénibilité perçue & Manque de logement proche hospitalier"),
        ("OFFRE-HNP-004", "35600000000014", "Hôpital national de paris", "Santé & Établissements Hospitaliers", "J1304", "J1304", "Manipulateur en Électroradiologie Médicale", "CDI", 24, 45000.0, 0, "75", "Île-de-France", True, 205, 310.00, 63550.00, 71.5, "Concurrence forte du secteur privé lucratif"),
        ("OFFRE-HNP-005", "35600000000014", "Hôpital national de paris", "Santé & Établissements Hospitaliers", "J1503", "J1503", "Cadre de Santé & Sage-Femme", "CDI", 36, 52000.0, 0, "75", "Île-de-France", True, 190, 340.00, 64600.00, 65.0, "Responsabilités d'encadrement sans revalorisation suffisante")
    ]
    for hnp in sante_vacancies_hnp:
        job_offers.append({
            "job_offer_id": hnp[0],
            "siret": hnp[1],
            "company_name": hnp[2],
            "secteur_activite_libelle": hnp[3],
            "code_metier_bmo": hnp[4],
            "code_rome": hnp[5],
            "job_title": hnp[6],
            "contract_type": hnp[7],
            "required_experience_months": hnp[8],
            "annual_salary_brut_eur": hnp[9],
            "remote_work_days": hnp[10],
            "department_code": hnp[11],
            "region_name": hnp[12],
            "is_hard_to_fill": hnp[13],
            "vacance_duree_jours": hnp[14],
            "cout_vacance_quotidien_eur": hnp[15],
            "cout_vacance_cumule_eur": hnp[16],
            "rejet_taux_pct": hnp[17],
            "motif_principal_rejet": hnp[18],
            "posting_date": "2025-01-10",
            "closing_date": "2025-09-30"
        })

    # Scenario 2 Specific Offers for TF1 Group (High rejection rate & specific rejection motifs)
    tf1_offers = [
        ("OFFRE-TF1-001", "32630000000042", "TF1 Group", "Média, Télévision & Multimédia", "E1101", "E1101", "Chef de Projet Média & Déploiement Numérique", "CDI", 36, 58000.0, 1, "92", "Île-de-France", True, 140, 290.00, 40600.00, 84.5, "Niveau de salaire proposé inférieur de 18% aux attentes du marché"),
        ("OFFRE-TF1-002", "32630000000042", "TF1 Group", "Média, Télévision & Multimédia", "E1102", "E1102", "Journaliste Reporter d'Images / JRI", "CDD", 24, 42000.0, 0, "92", "Île-de-France", True, 125, 240.00, 30000.00, 79.0, "Exigence de déplacements constants sans prise en charge complète"),
        ("OFFRE-TF1-003", "32630000000042", "TF1 Group", "Média, Télévision & Multimédia", "M1801", "M1801", "Ingénieur Régie Vidéo & Broadcast", "CDI", 48, 65000.0, 1, "92", "Île-de-France", True, 160, 350.00, 56000.00, 86.2, "Diplôme spécifique de grande école d'ingénieur exigé sans équivalence"),
        ("OFFRE-TF1-004", "32630000000042", "TF1 Group", "Média, Télévision & Multimédia", "E1104", "E1104", "Chargé de Programmation & Audience TV", "CDI", 12, 39000.0, 0, "92", "Île-de-France", True, 110, 190.00, 20900.00, 78.5, "Absence de jours de télétravail accordés")
    ]
    for tf in tf1_offers:
        job_offers.append({
            "job_offer_id": tf[0],
            "siret": tf[1],
            "company_name": tf[2],
            "secteur_activite_libelle": tf[3],
            "code_metier_bmo": tf[4],
            "code_rome": tf[5],
            "job_title": tf[6],
            "contract_type": tf[7],
            "required_experience_months": tf[8],
            "annual_salary_brut_eur": tf[9],
            "remote_work_days": tf[10],
            "department_code": tf[11],
            "region_name": tf[12],
            "is_hard_to_fill": tf[13],
            "vacance_duree_jours": tf[14],
            "cout_vacance_quotidien_eur": tf[15],
            "cout_vacance_cumule_eur": tf[16],
            "rejet_taux_pct": tf[17],
            "motif_principal_rejet": tf[18],
            "posting_date": "2025-02-01",
            "closing_date": "2025-08-31"
        })

    # Battery Gigafactories Offers in Hauts-de-France
    battery_offers = [
        ("OFFRE-BAT-001", "88910000000012", "ACC - Automotive Cells Company", "Fabrication de Batteries & Gigafactory", "H1206", "H1206", "Technicien de Maintenance Ligne de Production Batterie", "CDI", 24, 38000.0, 0, "59", "Hauts-de-France", True, 150, 310.00, 46500.00, 83.0, "Pénurie de techniciens qualifiés en électricité et automatismes"),
        ("OFFRE-BAT-002", "89920000000023", "Envision AESC Douai", "Fabrication de Batteries & Gigafactory", "H1401", "H1401", "Opérateur de Conduite d'Équipement d'Usinage", "CDI", 12, 32000.0, 0, "59", "Hauts-de-France", True, 135, 250.00, 33750.00, 88.0, "Manque de compétences en chimie et conduite de lignes automatisées"),
        ("OFFRE-BAT-003", "89930000000034", "Verkor Dunkerque", "Fabrication de Batteries & Gigafactory", "H1203", "H1203", "Ingénieur R&D Électrochimie & Cellules", "CDI", 36, 58000.0, 2, "59", "Hauts-de-France", True, 180, 420.00, 75600.00, 100.0, "Forte concurrence internationale sur les ingénieurs batterie"),
        ("OFFRE-BAT-004", "89940000000045", "Prologium Dunkerque", "Fabrication de Batteries & Gigafactory", "F1602", "F1602", "Électricien Industriel Haute Tension", "CDI", 24, 40000.0, 0, "59", "Hauts-de-France", True, 160, 290.00, 46400.00, 95.0, "Habilitations électriques spécialisées manquantes")
    ]
    for bat in battery_offers:
        job_offers.append({
            "job_offer_id": bat[0],
            "siret": bat[1],
            "company_name": bat[2],
            "secteur_activite_libelle": bat[3],
            "code_metier_bmo": bat[4],
            "code_rome": bat[5],
            "job_title": bat[6],
            "contract_type": bat[7],
            "required_experience_months": bat[8],
            "annual_salary_brut_eur": bat[9],
            "remote_work_days": bat[10],
            "department_code": bat[11],
            "region_name": bat[12],
            "is_hard_to_fill": bat[13],
            "vacance_duree_jours": bat[14],
            "cout_vacance_quotidien_eur": bat[15],
            "cout_vacance_cumule_eur": bat[16],
            "rejet_taux_pct": bat[17],
            "motif_principal_rejet": bat[18],
            "posting_date": "2025-01-20",
            "closing_date": "2025-08-30"
        })

    # Fill remaining general offers up to 8,500
    for i in range(14, 8501):
        offer_id = f"OFFRE-2025-{i:05d}"
        comp = random.choice(companies)
        metier = random.choice(bmo_metiers)
        code_rome = random.choice(rome_codes)
        c_type = random.choice(CONTRACT_TYPES)
        exp_months = random.choice([0, 12, 24, 36, 60])

        sal = round(random.uniform(26000.0, 68000.0), 2)
        remote = random.choice([0, 1, 2, 3])
        is_hard = random.choice([True, False, False])
        vac_days = random.randint(15, 120) if not is_hard else random.randint(125, 230)
        vac_cost = round(random.uniform(150.0, 380.0), 2)
        rejet_pct = round(random.uniform(25.0, 72.0), 1)

        post_date = base_date + timedelta(days=random.randint(0, 180))
        close_date = post_date + timedelta(days=random.randint(30, 90))

        job_offers.append({
            "job_offer_id": offer_id,
            "siret": comp["siret"],
            "company_name": comp["company_name"],
            "secteur_activite_libelle": comp["secteur_activite_libelle"],
            "code_metier_bmo": metier["code_metier_bmo"],
            "code_rome": code_rome,
            "job_title": f"{metier['nom_metier_bmo']} - {c_type}",
            "contract_type": c_type,
            "required_experience_months": exp_months,
            "annual_salary_brut_eur": sal,
            "remote_work_days": remote,
            "department_code": comp["department_code"],
            "region_name": comp["region_name"],
            "is_hard_to_fill": is_hard,
            "vacance_duree_jours": vac_days,
            "cout_vacance_quotidien_eur": vac_cost,
            "cout_vacance_cumule_eur": round(vac_days * vac_cost, 2),
            "rejet_taux_pct": rejet_pct,
            "motif_principal_rejet": "Écart entre prétentions salariales et grille entreprise",
            "posting_date": post_date.strftime("%Y-%m-%d"),
            "closing_date": close_date.strftime("%Y-%m-%d")
        })

    df_job_offers = pd.DataFrame(job_offers)

    # 5. france_travail_demandeurs (including explicit record for Anna FT-99720068)
    candidates = []

    # Scenario 3 Explicit Profile: Anna Kowalski FT-99720068
    anna_profile = {
        "demandeur_id": "FT-99720068",
        "nom_prenom": "Anna Kowalski",
        "statut_recherche": "Recherche Active",
        "categorie_inscription": "Catégorie A",
        "anciennete_chomage_mois": 14,
        "code_metier_bmo": "N1301",
        "code_rome": "N1301",
        "metier_recherche": "Responsable Supply Chain & Logistique Verte",
        "department_code": "75",
        "region_name": "Île-de-France",
        "freins_emploi_detail": "Garde de 2 enfants en bas âge (contrainte horaire stricte 8h30-17h30), Mobilité en Transports en Commun uniquement (pas de véhicule personnel), Prétentions salariales minimales de 38 000 € bruts/an.",
        "competences_actuelles": "Gestion des stocks et réapprovisionnement, Maîtrise avancée Excel & ERP SAP, Planification de flux de camionnage, Anglais professionnel.",
        "cv_gcs_uri": f"{RESUMES_BUCKET}/resumes/cv_FT-99720068.pdf",
        "cv_text_content": "Anna Kowalski (ID: FT-99720068). Titulaire d'un Bac+3 en Logistique et Transports. 5 ans d'expérience comme Assistante Logistique Senior. Souhaite évoluer vers un poste de Responsable Supply Chain avec de meilleurs avantages. Freins: Horaires stricts garde d'enfants (8h30-17h30), mobilité transports en commun.",
        "niveau_etudes": "Bac+3"
    }
    candidates.append(anna_profile)

    # Parse local PDF CVs
    local_pdfs = sorted(glob.glob(os.path.join(RESUMES_DIR, "cv_*.pdf")))
    print(f"  Parsing {len(local_pdfs)} authentic local candidate PDF CV files from '{RESUMES_DIR}'...")

    for pdf_path in local_pdfs:
        cand = parse_local_pdf_cv(pdf_path)
        if cand and cand["demandeur_id"] != "FT-99720068":
            cand["code_metier_bmo"] = random.choice(bmo_metiers)["code_metier_bmo"]
            cand["code_rome"] = random.choice(rome_codes)
            candidates.append(cand)

    df_job_seekers = pd.DataFrame(candidates)
    
    # Generate ~500 additional candidate profiles across Île-de-France and Hauts-de-France
    extra_seekers = []
    first_names = ["Thomas", "Lucas", "Sophie", "Camille", "Élodie", "Alexandre", "Nicolas", "Julie", "Marie", "Jean", "Maxime", "Léa", "Antoine", "Chloé", "Pierre"]
    last_names = ["Bernard", "Martin", "Moreau", "Petit", "Dubois", "Richard", "Durand", "Laurent", "Lefebvre", "Michel", "Garcia", "David", "Bertrand", "Roux", "Fournier"]
    metiers_target = [
        "Infirmier de Soins Généraux", "Médecin Urgentiste", "Aide-Soignant", "Technicien de Maintenance",
        "Chef de Projet Média", "Journaliste Reporter JRI", "Ingénieur Régie Broadcast", "Électricien Industriel",
        "Opérateur d'Usinage", "Responsable Logistique", "Développeur Web", "Analyste Data"
    ]

    for i in range(1, 501):
        dem_id = f"DEM-{i:04d}"
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        dept = random.choice(["75", "92", "93", "94", "59", "62", "69", "13", "31", "33"])
        reg = "Île-de-France" if dept in ["75", "92", "93", "94"] else ("Hauts-de-France" if dept in ["59", "62"] else "Région")

        extra_seekers.append({
            "demandeur_id": dem_id,
            "nom_prenom": f"{fn} {ln}",
            "statut_recherche": random.choice(["Recherche Active", "En Formation", "Emploi Reconversion"]),
            "categorie_inscription": random.choice(["Catégorie A", "Catégorie B", "Catégorie C"]),
            "anciennete_chomage_mois": random.randint(1, 24),
            "code_metier_bmo": random.choice(bmo_metiers)["code_metier_bmo"],
            "code_rome": random.choice(rome_codes),
            "metier_recherche": random.choice(metiers_target),
            "department_code": dept,
            "region_name": reg,
            "freins_emploi_detail": "Disponible immédiatement, mobilité régionale.",
            "competences_actuelles": "Savoir-faire métier, travail en équipe, autonomie",
            "cv_gcs_uri": f"{RESUMES_BUCKET}/resumes/cv_{dem_id}.pdf",
            "cv_text_content": f"CV de {fn} {ln}. Compétences et expérience en {random.choice(metiers_target)}.",
            "niveau_etudes": random.choice(["Bac", "Bac+2", "Bac+3", "Bac+5"])
        })

    df_job_seekers = pd.concat([df_job_seekers, pd.DataFrame(extra_seekers)], ignore_index=True)
    print(f"  ✓ Processed {len(df_job_seekers)} candidate profiles (including Anna FT-99720068)!")

    # 6. candidatures_postulations_suivi (~3,500 ATS applications)
    applications = []
    cand_records = df_job_seekers.to_dict("records")
    offer_records = df_job_offers.to_dict("records")

    # High matching applications for TF1 and Healthcare
    for i in range(1, 3501):
        app_id = f"APP-{i:05d}"
        seeker = random.choice(cand_records)
        offer = random.choice(offer_records)
        status = random.choice(STATUTS_CANDIDATURE)

        score = round(random.uniform(70.0, 98.5), 1)
        app_date = datetime(2025, 2, 1) + timedelta(days=random.randint(0, 150), hours=random.randint(8, 18))
        update_date = app_date + timedelta(days=random.randint(1, 20))

        refus_motif = offer["motif_principal_rejet"] if status == "Refusé après entretien" else None

        applications.append({
            "application_id": app_id,
            "demandeur_id": seeker["demandeur_id"],
            "job_offer_id": offer["job_offer_id"],
            "siret": offer["siret"],
            "company_name": offer["company_name"],
            "application_date": app_date.strftime("%Y-%m-%d %H:%M:%S"),
            "current_status": status,
            "ats_matching_score_pct": score,
            "motif_refus_detail": refus_motif,
            "last_status_update": update_date.strftime("%Y-%m-%d %H:%M:%S")
        })

    df_applications = pd.DataFrame(applications)

    # 7. france_travail_formations_aides (vocational training & subsidies)
    subsidies = []
    organismes = ["France Travail", "Région", "Opco AKTO", "Opco Atlas", "Agefiph"]
    statuts_aides = ["Accordée", "En cours de versement", "Clôturée"]

    # Specific subsidies for Anna (POEI, PMSMP Immersion 15j, CPF)
    anna_subsidies = [
        ("AIDE-ANNA-001", "FT-99720068", "33790000000055", "POEI (Préparation Opérationnelle à l'Emploi Individuelle - Supply Chain)", 4500.00, "2025-03-01", "2025-05-31", "Accordée", "France Travail"),
        ("AIDE-ANNA-002", "FT-99720068", "33790000000055", "PMSMP (Immersion en Entreprise 15j - Logistique Verte)", 0.00, "2025-06-01", "2025-06-15", "Clôturée", "France Travail"),
        ("AIDE-ANNA-003", "FT-99720068", "33790000000055", "Compte Personnel de Formation (CPF Co-financé ERP SAP)", 2200.00, "2025-04-01", "2025-04-30", "Clôturée", "Région")
    ]
    for asub in anna_subsidies:
        subsidies.append({
            "aide_id": asub[0],
            "demandeur_id": asub[1],
            "siret": asub[2],
            "nom_aide_dispositif": asub[3],
            "montant_aide_accordee_eur": asub[4],
            "date_debut_aide": asub[5],
            "date_expiration_aide": asub[6],
            "statut_aide": asub[7],
            "organisme_financeur": asub[8]
        })

    for i in range(4, 5001):
        aide_id = f"AIDE-{i:05d}"
        seeker = random.choice(cand_records)
        comp = random.choice(companies)
        dispositif = random.choice(DISPOSITIFS_AIDES_NOMS)

        amount = round(random.uniform(1500.0, 14500.0), 2)
        start_d = base_date + timedelta(days=random.randint(0, 120))
        end_d = start_d + timedelta(days=random.randint(60, 365))

        subsidies.append({
            "aide_id": aide_id,
            "demandeur_id": seeker["demandeur_id"],
            "siret": comp["siret"],
            "nom_aide_dispositif": dispositif,
            "montant_aide_accordee_eur": amount,
            "date_debut_aide": start_d.strftime("%Y-%m-%d"),
            "date_expiration_aide": end_d.strftime("%Y-%m-%d"),
            "statut_aide": random.choice(statuts_aides),
            "organisme_financeur": random.choice(organismes)
        })

    df_subsidies = pd.DataFrame(subsidies)

    # Save CSVs locally and upload to BigQuery & GCS
    tables_dict = {
        "bmo_recrutement_2025": df_bmo,
        "rome_arborescence_2024": df_rome,
        "entreprises_urssaf_declarations": df_companies,
        "offres_emploi_recrutement": df_job_offers,
        "france_travail_demandeurs": df_job_seekers,
        "candidatures_postulations_suivi": df_applications,
        "france_travail_formations_aides": df_subsidies
    }

    subprocess.run(f"gcloud storage buckets create {BUCKET_NAME} --project={PROJECT_ID} --location=EU 2>/dev/null", shell=True)

    for tname, df in tables_dict.items():
        csv_path = f"agents/sully/data/{tname}.csv"
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

    print("\nSUCCESS: All 7 Sully tables complete & populated in BigQuery!")

if __name__ == "__main__":
    main()
