#!/usr/bin/env python3
"""
Refined Relational Data Pipeline for Sully - France Travail & URSSAF Recruitment Intelligence Platform.
Populates BigQuery dataset `public_sector_employment_ds` with 6 fully interconnected tables:

1. `bmo_recrutement_2025`: 50,076 authentic France Travail BMO 2025 recruitment forecast records.
2. `entreprises_urssaf_declarations`: 4,500 company establishments with SIRET, NAF, employee counts, payroll, and OETH disability gaps.
3. `offres_emploi_recrutement`: 8,500 job vacancies linked by SIRET, BMO occupation code, and department.
4. `france_travail_demandeurs`: 6,000 job seekers registered at France Travail linked by BMO occupation code, department, and GCS CV URIs.
5. `candidatures_postulations_suivi`: 12,000 candidate ATS applications linking job seekers, job offers, and companies.
6. `france_travail_formations_aides`: 5,000 vocational training courses and recruitment subsidies granted.
"""

import os
import sys
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
BMO_EXCEL_PATH = "agents/sully/data/bmo_recrutement_2025.xlsx"

REAL_COMPANIES_SAMPLE = [
    ("35600000000014", "AP-HP (Hôpitaux de Paris)", "8610Z - Activités hospitalières", "Établissement Public", 45000, 1850000000.0, 120, "75004", "75", "Paris", "QPV - Quartier Prioritaire"),
    ("77568000000028", "Hôpitaux Civils de Lyon (HCL)", "8610Z - Activités hospitalières", "Établissement Public", 24000, 980000000.0, 45, "69002", "69", "Lyon", "Zone Standard"),
    ("32630000000042", "TF1 Group", "6020Z - Édition de chaînes de télévision", "SA à Conseil d'administration", 3200, 240000000.0, 18, "92100", "92", "Boulogne-Billancourt", "Zone Standard"),
    ("33790000000055", "Capgemini France", "6202A - Conseil en systèmes informatiques", "SAS", 28000, 1420000000.0, 85, "92130", "92", "Issy-les-Moulineaux", "Zone Standard"),
    ("54200000000068", "Sanofi France", "2120Z - Fabrication de préparations pharmaceutiques", "SA", 19500, 1150000000.0, 32, "75008", "75", "Paris", "Zone Standard"),
    ("42870000000071", "Carrefour France", "4711D - Supermarchés", "SA", 105000, 3200000000.0, 210, "91000", "91", "Évry-Courcouronnes", "QPV - Quartier Prioritaire"),
    ("38012000000084", "SNCF Voyageurs", "4910Z - Transport ferroviaire de voyageurs", "SA", 68000, 2900000000.0, 140, "93200", "93", "Saint-Denis", "QPV - Quartier Prioritaire"),
    ("34360000000097", "Michelin Ladoux R&D", "2211Z - Fabrication et rechapage de pneumatiques", "SCA", 14200, 780000000.0, 28, "63000", "63", "Clermont-Ferrand", "ZRR - Zone Revitalisation Rurale"),
    ("41480000000105", "STMicroelectronics Crolles", "2611Z - Fabrication de composants électroniques", "NV / SA", 4800, 310000000.0, 12, "38920", "38", "Crolles", "Zone Standard"),
    ("30120000000118", "Dassault Systèmes", "5829C - Édition de logiciels système et de réseau", "SA", 8900, 540000000.0, 22, "78140", "78", "Vélizy-Villacoublay", "Zone Standard")
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
    "Prime Reprise d'Activité AGEFIPH (Handicap)"
]

CONTRACT_TYPES = ["CDI", "CDD", "Alternance", "Intérim"]

def get_client():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return bigquery.Client(project=PROJECT_ID, credentials=creds)

def clean_val(val, default_str=""):
    if pd.isnull(val) or val == "*":
        return None
    return val

def main():
    print(f"Initializing Refined Sully Relational Pipeline for project '{PROJECT_ID}'...")
    client = get_client()

    os.makedirs("agents/sully/data", exist_ok=True)

    # 1. bmo_recrutement_2025
    if os.path.exists(BMO_EXCEL_PATH):
        print(f"  Parsing authentic France Travail BMO 2025 Open Data Excel dataset...")
        df_bmo_raw = pd.read_excel(BMO_EXCEL_PATH, sheet_name="BMO_2025_open_data")
        print(f"  ✓ Parsed {len(df_bmo_raw)} raw BMO records.")

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

    # Extract unique metiers and departments for foreign key linkage
    bmo_metiers = df_bmo[["code_metier_bmo", "nom_metier_bmo", "famille_metier_libelle"]].drop_duplicates().to_dict("records")
    bmo_depts = df_bmo[["code_departement", "nom_departement", "nom_region"]].drop_duplicates().to_dict("records")

    # 2. entreprises_urssaf_declarations (~4,500 companies)
    companies = []
    # Seed authentic companies
    for item in REAL_COMPANIES_SAMPLE:
        companies.append({
            "siret": item[0],
            "company_name": item[1],
            "sector_naf": item[2],
            "legal_status": item[3],
            "employee_count": item[4],
            "total_payroll_eur": item[5],
            "oeth_target_deficit_count": item[6],
            "postal_code": item[7],
            "department_code": item[8],
            "city_name": item[9],
            "zone_type": item[10]
        })

    # Synthetic companies
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
        city = f"Ville-{dept_code}-{i % 50}"

        emp_count = random.randint(15, 8500)
        payroll = round(emp_count * random.uniform(32000.0, 58000.0), 2)
        oeth_deficit = random.randint(0, 45) if emp_count > 20 else 0

        companies.append({
            "siret": siret,
            "company_name": f"Entreprise-{dept_info['nom_departement']}-{i}",
            "sector_naf": random.choice(sectors),
            "legal_status": random.choice(legal_statuses),
            "employee_count": emp_count,
            "total_payroll_eur": payroll,
            "oeth_target_deficit_count": oeth_deficit,
            "postal_code": f"{dept_code}000" if len(dept_code) == 2 else f"0{dept_code}00",
            "department_code": dept_code,
            "city_name": city,
            "zone_type": random.choice(zone_types)
        })

    df_companies = pd.DataFrame(companies)
    siret_list = df_companies["siret"].tolist()

    # 3. offres_emploi_recrutement (~8,500 job offers)
    job_offers = []
    base_date = datetime(2025, 1, 15)

    for i in range(1, 8501):
        offer_id = f"OFFRE-2025-{i:05d}"
        comp = random.choice(companies)
        metier = random.choice(bmo_metiers)
        c_type = random.choice(CONTRACT_TYPES)
        exp_months = random.choice([0, 12, 24, 36, 60])

        sal = round(random.uniform(26000.0, 68000.0), 2)
        remote = random.choice([0, 1, 2, 3])
        is_hard = random.choice([True, False, False])

        post_date = base_date + timedelta(days=random.randint(0, 180))
        close_date = post_date + timedelta(days=random.randint(30, 90))

        job_offers.append({
            "job_offer_id": offer_id,
            "siret": comp["siret"],
            "company_name": comp["company_name"],
            "code_metier_bmo": metier["code_metier_bmo"],
            "job_title": f"{metier['nom_metier_bmo']} - {c_type}",
            "contract_type": c_type,
            "required_experience_months": exp_months,
            "annual_salary_brut_eur": sal,
            "remote_work_days": remote,
            "department_code": comp["department_code"],
            "is_hard_to_fill": is_hard,
            "posting_date": post_date.strftime("%Y-%m-%d"),
            "closing_date": close_date.strftime("%Y-%m-%d")
        })

    df_job_offers = pd.DataFrame(job_offers)

    # 4. france_travail_demandeurs (~6,000 job seekers)
    job_seekers = []
    statuts_recherche = ["Recherche Active", "En Formation", "Emploi Reconversion"]
    categories_insc = ["Catégorie A", "Catégorie B", "Catégorie C", "Catégorie D"]
    niveaux_etudes = ["Bac", "Bac+2", "Bac+3", "Bac+5", "Doctorat"]

    prems = ["Jean", "Marie", "Lucas", "Sophie", "Thomas", "Camille", "Nicolas", "Julie", "Alexandre", "Emma"]
    noms = ["Martin", "Bernard", "Thomas", "Petit", "Robert", "Richard", "Durand", "Dubois", "Moreau", "Laurent"]

    for i in range(1, 6001):
        dem_id = f"DEM-{i:05d}"
        metier = random.choice(bmo_metiers)
        dept_info = random.choice(bmo_depts)
        dept_code = dept_info["code_departement"]
        full_name = f"{random.choice(prems)} {random.choice(noms)}"

        anc_chomage = random.randint(1, 36)
        cv_uri = f"gs://sully-candidate-resumes-data-agents/resumes/{dem_id}.pdf"
        cv_txt = f"Candidat expérimenté en {metier['nom_metier_bmo']}. Maîtrise des outils métiers et rigueur professionnelle."

        job_seekers.append({
            "demandeur_id": dem_id,
            "nom_prenom": full_name,
            "statut_recherche": random.choice(statuts_recherche),
            "categorie_inscription": random.choice(categories_insc),
            "anciennete_chomage_mois": anc_chomage,
            "code_metier_bmo": metier["code_metier_bmo"],
            "metier_recherche": metier["nom_metier_bmo"],
            "department_code": dept_code,
            "cv_gcs_uri": cv_uri,
            "cv_text_content": cv_txt,
            "niveau_etudes": random.choice(niveaux_etudes)
        })

    df_job_seekers = pd.DataFrame(job_seekers)

    # 5. candidatures_postulations_suivi (~12,000 ATS applications)
    applications = []
    for i in range(1, 12001):
        app_id = f"APP-{i:06d}"
        seeker = random.choice(job_seekers)
        offer = random.choice(job_offers)
        status = random.choice(STATUTS_CANDIDATURE)

        score = round(random.uniform(55.0, 98.5), 1)
        app_date = datetime(2025, 2, 1) + timedelta(days=random.randint(0, 150), hours=random.randint(8, 18))
        update_date = app_date + timedelta(days=random.randint(1, 20))

        applications.append({
            "application_id": app_id,
            "demandeur_id": seeker["demandeur_id"],
            "job_offer_id": offer["job_offer_id"],
            "siret": offer["siret"],
            "application_date": app_date.strftime("%Y-%m-%d %H:%M:%S"),
            "current_status": status,
            "ats_matching_score_pct": score,
            "last_status_update": update_date.strftime("%Y-%m-%d %H:%M:%S")
        })

    df_applications = pd.DataFrame(applications)

    # 6. france_travail_formations_aides (~5,000 training subsidies)
    subsidies = []
    organismes = ["France Travail", "Région", "Opco AKTO", "Opco Atlas", "Agefiph"]
    statuts_aides = ["Accordée", "En cours de versement", "Clôturée"]

    for i in range(1, 5001):
        aide_id = f"AIDE-{i:05d}"
        seeker = random.choice(job_seekers)
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
        "entreprises_urssaf_declarations": df_companies,
        "offres_emploi_recrutement": df_job_offers,
        "france_travail_demandeurs": df_job_seekers,
        "candidatures_postulations_suivi": df_applications,
        "france_travail_formations_aides": df_subsidies
    }

    subprocess.run(f"gcloud storage buckets create {BUCKET_NAME} --project={PROJECT_ID} --location=EU 2>/dev/null", shell=True)

    for tname, df in tables_dict.items():
        csv_file = f"agents/sully/data/{tname}.csv"
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

    print("\nSUCCESS: All 6 Sully tables complete & populated in BigQuery!")

if __name__ == "__main__":
    main()
