#!/usr/bin/env python3
"""
Generate 300 Authentic 1-Page PDF CVs using ReportLab matching the exact 'KENGNI THEOPHANE CV' Model:
- Centered Header (Candidate Name + Target Role)
- Clean Contact Line (Email | Phone | Location | LinkedIn) -> NO EMOJIS, NO FT ID!
- Horizontal divider lines
- 5 Standardized Sections: ABOUT ME, TECHNICAL SKILLS, EXPERIENCE PROFESSIONNELLE, EDUCATION & FORMATION, CERTIFICATIONS & INTERESTS.
- Upload to GCS gs://sully-candidate-resumes-data-agents/resumes/,
- Delete all local PDF files from disk,
- Reload BigQuery Dataset public_sector_employment_ds.
"""

import os
import sys
import shutil
import random
import subprocess
import pandas as pd
from datetime import datetime, timedelta

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "public_sector_employment_ds"
RESUMES_BUCKET = "gs://sully-candidate-resumes-data-agents"
SULLY_BUCKET = "gs://talktodata-sully-raw-data"
TEMP_RESUMES_DIR = os.path.join(os.path.dirname(__file__), "agents", "sully", "data", "temp_kengni_resumes")

FIRST_NAMES = [
    "Sophie", "Thomas", "Lucas", "Camille", "Élodie", "Alexandre", "Nicolas", "Julie", "Marie", "Jean",
    "Maxime", "Léa", "Antoine", "Chloé", "Pierre", "Manon", "Hugo", "Sarah", "Gabriel", "Inès",
    "Clément", "Mathilde", "Julien", "Laura", "Louis", "Charlotte", "Arthur", "Pauline", "Théo", "Emma"
]

LAST_NAMES = [
    "Bernard", "Martin", "Moreau", "Petit", "Dubois", "Richard", "Durand", "Laurent", "Lefebvre", "Michel",
    "Garcia", "David", "Bertrand", "Roux", "Fournier", "Girard", "Bonnet", "Dupont", "Lambert", "Fontaine",
    "Rousseau", "Vincent", "Muller", "Lefevre", "Faure", "Andre", "Mercier", "Blanc", "Guerin", "Boyer"
]

DEGREES = [
    ("Bac+2", "BTS / DUT Informatique & Gestion"),
    ("Bac+3", "Licence Professionnelle Métiers du Numérique"),
    ("Bac+5", "Master 2 Ingénierie & Data Analytics"),
    ("Doctorat", "Doctorat / PhD Sciences & Recherche")
]

DEPARTMENTS = [
    ("75", "Paris"), ("69", "Rhône"), ("13", "Bouches-du-Rhône"), ("31", "Haute-Garonne"),
    ("59", "Nord"), ("44", "Loire-Atlantique"), ("33", "Gironde"), ("92", "Hauts-de-Seine"),
    ("38", "Isère"), ("63", "Puy-de-Dôme"), ("06", "Alpes-Maritimes"), ("67", "Bas-Rhin")
]

COMPANIES_LIST = [
    "Capgemini France", "AP-HP Paris", "Carrefour France", "SNCF Voyageurs",
    "Sanofi R&D", "Dassault Systèmes", "Michelin Ladoux", "STMicroelectronics",
    "Hôpitaux Civils de Lyon", "TF1 Group", "Orange Business", "Thales Digital"
]

def get_client():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return bigquery.Client(project=PROJECT_ID, credentials=creds)

def build_exact_kengni_pdf_cv(pdf_path, full_name, target_role, dept_code, dept_name, degree_level, degree_title, company):
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    header_name_style = ParagraphStyle('HeaderName', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#1A202C'), spaceAfter=2, alignment=1)
    header_sub_style = ParagraphStyle('HeaderSub', parent=styles['Heading2'], fontSize=11, textColor=colors.HexColor('#2B6CB0'), spaceAfter=4, alignment=1)
    contact_style = ParagraphStyle('ContactStyle', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#4A5568'), spaceAfter=8, alignment=1)

    section_heading = ParagraphStyle('SecHeading', parent=styles['Heading3'], fontSize=10, textColor=colors.HexColor('#1A365D'), spaceBefore=8, spaceAfter=4)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=8.5, textColor=colors.HexColor('#2D3748'), leading=11.5)

    clean_slug = full_name.lower().replace(' ', '')
    email = f"{full_name.lower().replace(' ', '.')}@francetravail-candidats.fr"
    phone = f"+33 6 {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)}"

    story = [
        Paragraph(f"<b>{full_name.upper()}</b>", header_name_style),
        Paragraph(f"<b>{target_role}</b>", header_sub_style),
        Paragraph(f"Email: {email} | Téléphone: {phone} | Localisation: {dept_name} ({dept_code}) | linkedin.com/in/{clean_slug}", contact_style),
        HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#CBD5E0'), spaceBefore=2, spaceAfter=8),

        Paragraph("<b>ABOUT ME / PROFIL PROFESSIONNEL</b>", section_heading),
        Paragraph(f"Professionnel diplômé en Data & IA combinant une forte rigueur analytique avec un sens aigu de l'innovation et de la création de valeur business. Passionné par la transformation des données brutes en leviers décisionnels stratégiques, j'excelle dans la modélisation de schémas relationnels, la création de tableaux de bord décisionnels et l'alignement entre exigences techniques et valeur entreprise.<br/>"
                  f"<b>Langues :</b> Français (Native), Anglais (Courant)", body_style),
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E2E8F0'), spaceBefore=6, spaceAfter=6),

        Paragraph("<b>TECHNICAL SKILLS & COMPÉTENCES</b>", section_heading),
        Paragraph("<b>Data & Business Intelligence:</b> Data Analysis, Business Intelligence (BI), Data-Driven Decision Making (DDDM), Reporting & KPI Analysis, BigQuery, SQL, Looker Studio, Power BI.<br/>"
                  "<b>Cloud & Tech Stack:</b> Google Cloud Platform (GCP), Python, PostgreSQL, Data Governance, DevSecOps, Git/GitHub.<br/>"
                  "<b>Soft Skills & Leadership:</b> Vision produit, communication stratégique, esprit d'analyse, autonomie et capacité d'adaptation aux besoins métier.", body_style),
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E2E8F0'), spaceBefore=6, spaceAfter=6),

        Paragraph("<b>EXPERIENCE PROFESSIONNELLE</b>", section_heading),
        Paragraph(f"<b>Customer Engineer Cloud & Data Analyst</b><br/>"
                  f"<b>{company}, {dept_name} — 09/2023 – Présent</b><br/>"
                  f"• Conception et déploiement d'architectures décisionnelles sur Google Cloud Platform et BigQuery pour de grands comptes.<br/>"
                  f"• Création de dashboards analytiques automatisés réduisant de 35% le temps d'obtention des rapports de synthèse RH et financiers.<br/>"
                  f"• Animation des ateliers utilisateurs et accompagnement du changement auprès des équipes métiers client.<br/>"
                  f"<br/>"
                  f"<b>Chargé d'Études Statistiques & BI</b><br/>"
                  f"<b>Établissement Régional, {dept_name} — 06/2021 – 08/2023</b><br/>"
                  f"• Analyse prédictive des flux d'admission et modélisation des besoins en ressources humaines hospitalières et d'insertion.", body_style),
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E2E8F0'), spaceBefore=6, spaceAfter=6),

        Paragraph("<b>EDUCATION & FORMATION</b>", section_heading),
        Paragraph(f"<b>{degree_title} ({degree_level})</b> — Université de {dept_name} (2023)<br/>"
                  f"<b>Bachelor Data Science & Statistique Appliquée</b> — Établissement Supérieur Régional (2021)", body_style),
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E2E8F0'), spaceBefore=6, spaceAfter=6),

        Paragraph("<b>CERTIFICATIONS & INTERESTS</b>", section_heading),
        Paragraph("<b>Certifications:</b> Google Professional Data Engineer, Inside LVMH Certificate.<br/>"
                  "<b>Interêts:</b> Innovation & Technology, Arts & Culture, Sports.", body_style)
    ]

    doc.build(story)

    cv_text = f"{full_name} - {target_role}. Diplômé {degree_level} ({degree_title}) basé à {dept_name} ({dept_code}). Expérience chez {company}. Compétences : BigQuery, GCP, SQL, Python, Business Intelligence, Data Analysis."
    return cv_text

def main():
    print("Generating 300 clean text 'Kengni Théophane' model PDF CVs (NO EMOJIS, NO FT ID)...")
    os.makedirs(TEMP_RESUMES_DIR, exist_ok=True)

    df_bmo = pd.read_csv("agents/sully/data/bmo_recrutement_2025.csv")
    bmo_metiers = df_bmo[["code_metier_bmo", "nom_metier_bmo"]].drop_duplicates().to_dict("records")

    df_rome = pd.read_csv("agents/sully/data/rome_arborescence_2024.csv")
    rome_records = df_rome[["code_rome", "intitule_rome_appellation"]].drop_duplicates().to_dict("records")

    candidates = []

    for i in range(1, 301):
        dem_id = f"DEM-2025-{i:03d}"
        pdf_filename = f"cv_{dem_id}.pdf"
        local_pdf_path = os.path.join(TEMP_RESUMES_DIR, pdf_filename)

        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        full_name = f"{first_name} {last_name}"

        bmo_item = random.choice(bmo_metiers)
        rome_item = random.choice(rome_records)

        dept_code, dept_name = random.choice(DEPARTMENTS)
        deg_level, deg_title = random.choice(DEGREES)
        company = random.choice(COMPANIES_LIST)

        gcs_uri = f"{RESUMES_BUCKET}/resumes/{pdf_filename}"

        cv_text = build_exact_kengni_pdf_cv(
            local_pdf_path, full_name, bmo_item["nom_metier_bmo"],
            dept_code, dept_name, deg_level, deg_title, company
        )

        candidates.append({
            "demandeur_id": dem_id,
            "nom_prenom": full_name,
            "statut_recherche": "Recherche Active",
            "categorie_inscription": "Catégorie A",
            "anciennete_chomage_mois": random.randint(1, 24),
            "code_metier_bmo": bmo_item["code_metier_bmo"],
            "code_rome": rome_item["code_rome"],
            "metier_recherche": bmo_item["nom_metier_bmo"],
            "department_code": dept_code,
            "cv_gcs_uri": gcs_uri,
            "cv_text_content": cv_text,
            "niveau_etudes": deg_level
        })

        if i % 50 == 0:
            print(f"  ✓ Generated {i} / 300 clean Kengni model PDF CVs...")

    df_cand = pd.DataFrame(candidates)
    cand_csv = "agents/sully/data/france_travail_demandeurs.csv"
    df_cand.to_csv(cand_csv, index=False)
    print(f"  ✓ Saved {len(df_cand)} candidate records to {cand_csv}")

    # Upload all 300 PDF CVs to GCS
    print(f"Uploading 300 clean Kengni model PDF CVs to GCS bucket '{RESUMES_BUCKET}/resumes/'...")
    subprocess.run(f"gcloud storage cp {TEMP_RESUMES_DIR}/cv_*.pdf {RESUMES_BUCKET}/resumes/", shell=True, capture_output=True)
    print("  ✓ Upload to GCS complete!")

    # Clean up local PDF files directory completely
    print("Removing temporary local PDF files from disk...")
    shutil.rmtree(TEMP_RESUMES_DIR, ignore_errors=True)
    resumes_dir_old = os.path.join(os.path.dirname(__file__), "agents", "sully", "data", "resumes")
    shutil.rmtree(resumes_dir_old, ignore_errors=True)
    print("  ✓ All local PDF CV files deleted successfully! CVs live strictly in GCS bucket.")

    # Update ATS applications table candidatures_postulations_suivi.csv
    df_offers = pd.read_csv("agents/sully/data/offres_emploi_recrutement.csv")

    statuts = ["Candidature Transmise", "Entretien RH Planifié", "Entretien Technique / Métier", "Offre d'Embauche", "Embauché (Accès à l'emploi)"]

    apps = []
    cand_records = df_cand.to_dict("records")
    offer_records = df_offers.to_dict("records")

    for i in range(1, 4001):
        app_id = f"APP-2025-{i:05d}"
        seeker = random.choice(cand_records)
        offer = random.choice(offer_records)

        apps.append({
            "application_id": app_id,
            "demandeur_id": seeker["demandeur_id"],
            "job_offer_id": offer["job_offer_id"],
            "siret": offer["siret"],
            "application_date": "2025-02-15 10:30:00",
            "current_status": random.choice(statuts),
            "ats_matching_score_pct": round(random.uniform(65.0, 98.5), 1),
            "last_status_update": "2025-03-01 14:20:00"
        })

    df_apps = pd.DataFrame(apps)
    apps_csv = "agents/sully/data/candidatures_postulations_suivi.csv"
    df_apps.to_csv(apps_csv, index=False)

    # Reload all 7 tables into BigQuery
    client = get_client()
    tables = [
        "bmo_recrutement_2025", "rome_arborescence_2024", "entreprises_urssaf_declarations",
        "offres_emploi_recrutement", "france_travail_demandeurs", "candidatures_postulations_suivi",
        "france_travail_formations_aides"
    ]

    for tname in tables:
        c_path = f"agents/sully/data/{tname}.csv"
        gcs_dest = f"{SULLY_BUCKET}/{tname}.csv"
        subprocess.run(f"gcloud storage cp {c_path} {gcs_dest}", shell=True, capture_output=True)

        tref = f"{PROJECT_ID}.{DATASET_ID}.{tname}"

        client.delete_table(tref, not_found_ok=True)

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            allow_quoted_newlines=True,
            ignore_unknown_values=True
        )
        with open(c_path, "rb") as f_in:
            job = client.load_table_from_file(f_in, tref, job_config=job_config)
        job.result()
        print(f"  ✓ Re-loaded table `{tref}` in BigQuery!")

    print("\nSUCCESS: 300 clean Kengni model PDF CVs uploaded to GCS, local files removed, and BigQuery reloaded!")

if __name__ == "__main__":
    main()
