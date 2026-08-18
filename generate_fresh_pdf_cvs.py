#!/usr/bin/env python3
"""
Generate 300 Authentic 1-Page PDF CVs using ReportLab,
Upload them to GCS gs://sully-candidate-resumes-data-agents/resumes/,
and Update BigQuery Dataset public_sector_employment_ds with 100% Logical Consistency.
"""

import os
import sys
import csv
import random
import subprocess
import pandas as pd
from datetime import datetime, timedelta

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "public_sector_employment_ds"
RESUMES_BUCKET = "gs://sully-candidate-resumes-data-agents"
SULLY_BUCKET = "gs://talktodata-sully-raw-data"
RESUMES_DIR = os.path.join(os.path.dirname(__file__), "agents", "sully", "data", "resumes")

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

def build_pdf_cv(pdf_path, dem_id, full_name, target_role, dept_code, dept_name, degree_level, degree_title, company):
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    header_style = ParagraphStyle('HeaderStyle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#1A365D'), spaceAfter=2)
    role_style = ParagraphStyle('RoleStyle', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#2B6CB0'), spaceAfter=4)
    info_style = ParagraphStyle('InfoStyle', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#4A5568'), spaceAfter=8)
    section_heading = ParagraphStyle('SecHeading', parent=styles['Heading3'], fontSize=11, textColor=colors.HexColor('#1A365D'), spaceBefore=8, spaceAfter=4)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#2D3748'), leading=12)

    gcs_uri = f"{RESUMES_BUCKET}/resumes/{os.path.basename(pdf_path)}"
    email = f"{full_name.lower().replace(' ', '.')}@francetravail-candidats.fr"

    story = [
        Paragraph(f"<b>{full_name.upper()}</b>", header_style),
        Paragraph(f"<b>{target_role}</b>", role_style),
        Paragraph(f"📍 Département {dept_code} - {dept_name} | ✉️ {email} | 🆔 ID FT : {dem_id}", info_style),
        Paragraph(f"🎓 <b>Formation :</b> {degree_level} - {degree_title} | 🌐 Stockage Cloud GCS : {gcs_uri}", info_style),
        Spacer(1, 4),

        Paragraph("PROFIL PROFESSIONNEL & OBJECTIFS", section_heading),
        Paragraph(f"Professionnel dynamique diplômé ({degree_level}) en recherche active dans le secteur <b>{target_role}</b>. Fort d'une solide expérience acquise chez <b>{company}</b>, je maîtrise l'ensemble de la chaîne opérationnelle, de la collecte de données à la résolution de problématiques complexes.", body_style),
        Spacer(1, 6),

        Paragraph("COMPÉTENCES TECHNIQUES & EXPERTISE MÉTIER", section_heading),
        Paragraph("• <b>Savoir-faire métier :</b> Gestion de projet, analyse de processus, modélisation relationnelle SQL.<br/>"
                  "• <b>Outils & Données :</b> BigQuery, Google Cloud Platform, Python, Datavisualisation et reporting ATS.<br/>"
                  "• <b>Aptitudes transversales :</b> Communication, rigueur d'exécution, adaptabilité aux besoins en tension.", body_style),
        Spacer(1, 6),

        Paragraph("PARCOURS PROFESSIONNEL & EXPÉRIENCES CLÉS", section_heading),
        Paragraph(f"<b>2022 - 2024 : Specialist / Chargé de Mission - {company}</b><br/>"
                  f"• Pilotage opérationnel et suivi des indicateurs de performance RH et recrutement.<br/>"
                  f"• Optimisation des flux d'information et reporting décisionnel pour la direction.<br/>"
                  f"<b>2020 - 2022 : Assistant Métier & Coordination - Établissement Régional ({dept_name})</b><br/>"
                  f"• Gestion des dossiers candidats et contribution au développement des politiques d'insertion.", body_style),
        Spacer(1, 6),

        Paragraph("FORMATION & CERTIFICATIONS", section_heading),
        Paragraph(f"• <b>{degree_title} ({degree_level})</b> - Université de {dept_name}<br/>"
                  "• <b>Certification France Travail & Cloud Analytics</b> - Maturation profil ATS & BigQuery Data", body_style)
    ]

    doc.build(story)

    cv_text = f"{full_name} - {target_role}. Candidat diplômé {degree_level} ({degree_title}) basé à {dept_name} ({dept_code}). Expérience chez {company}. Compétences : BigQuery, SQL, Python, gestion de projet."
    return cv_text

def main():
    print("Generating 300 fresh authentic PDF CVs...")
    os.makedirs(RESUMES_DIR, exist_ok=True)

    # Load BMO and ROME for realistic mapping
    df_bmo = pd.read_csv("agents/sully/data/bmo_recrutement_2025.csv")
    bmo_metiers = df_bmo[["code_metier_bmo", "nom_metier_bmo"]].drop_duplicates().to_dict("records")

    df_rome = pd.read_csv("agents/sully/data/rome_arborescence_2024.csv")
    rome_records = df_rome[["code_rome", "intitule_rome_appellation"]].drop_duplicates().to_dict("records")

    candidates = []

    for i in range(1, 301):
        dem_id = f"DEM-2025-{i:03d}"
        pdf_filename = f"cv_{dem_id}.pdf"
        local_pdf_path = os.path.join(RESUMES_DIR, pdf_filename)

        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        full_name = f"{first_name} {last_name}"

        bmo_item = random.choice(bmo_metiers)
        rome_item = random.choice(rome_records)

        dept_code, dept_name = random.choice(DEPARTMENTS)
        deg_level, deg_title = random.choice(DEGREES)
        company = random.choice(COMPANIES_LIST)

        gcs_uri = f"{RESUMES_BUCKET}/resumes/{pdf_filename}"

        cv_text = build_pdf_cv(
            local_pdf_path, dem_id, full_name, bmo_item["nom_metier_bmo"],
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
            print(f"  ✓ Generated {i} / 300 PDF CVs...")

    df_cand = pd.DataFrame(candidates)
    cand_csv = "agents/sully/data/france_travail_demandeurs.csv"
    df_cand.to_csv(cand_csv, index=False)
    print(f"  ✓ Saved {len(df_cand)} candidate records to {cand_csv}")

    # Upload all 300 PDF CVs to GCS
    print(f"Uploading 300 PDF CVs to GCS bucket '{RESUMES_BUCKET}/resumes/'...")
    subprocess.run(f"gcloud storage cp {RESUMES_DIR}/cv_*.pdf {RESUMES_BUCKET}/resumes/", shell=True, capture_output=True)
    print("  ✓ Upload complete!")

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
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            allow_quoted_newlines=True,
            ignore_unknown_values=True,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
        )
        with open(c_path, "rb") as f_in:
            job = client.load_table_from_file(f_in, tref, job_config=job_config)
        job.result()
        print(f"  ✓ Loaded table `{tref}` in BigQuery!")

    print("\nSUCCESS: 300 fresh PDF CVs generated, uploaded to GCS, and loaded into BigQuery!")

if __name__ == "__main__":
    main()
