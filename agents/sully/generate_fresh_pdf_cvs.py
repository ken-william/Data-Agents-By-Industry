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

SULLY_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SULLY_DIR, "data")
TEMP_RESUMES_DIR = os.path.join(DATA_DIR, "temp_kengni_resumes")

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
    "Thales Group", "Dassault Systèmes", "EDF Énergie", "Orange Télécom",
    "Sanofi Pasteur", "CMA CGM Logistique", "AXA Assurances", "BNP Paribas Real Estate"
]

ROLES_LIST = [
    ("Ingénieur Data & Big Data Analyst", "Data & IT"),
    ("Développeur Fullstack Python / React", "IT & Digital"),
    ("Chef de Projet Transformation Digitale", "Management & Conseil"),
    ("Consultant Cybersécurité & Réseaux", "Télécoms & IT"),
    ("Responsable Logistique & Supply Chain", "Transports & Mobilité"),
    ("Analyste Risque Crédit & Finance", "Banque & Finance"),
    ("Gestionnaire de Projets de Santé", "Santé & Pharma"),
    ("Directeur d'Exploitation Commerciale", "Retail & CPG")
]

def get_client():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return bigquery.Client(project=PROJECT_ID, credentials=creds)

def generate_kengni_pdf_cv(filename, name, role, email, phone, location, linkedin_url):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=1,
        textColor=colors.HexColor('#0F172A')
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        alignment=1,
        textColor=colors.HexColor('#2563EB')
    )

    contact_style = ParagraphStyle(
        'DocContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.HexColor('#475569')
    )

    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        alignment=0,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=4
    )

    story = []

    # 1. Header (Centered Name & Target Role)
    story.append(Paragraph(name.upper(), title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph(role.upper(), subtitle_style))
    story.append(Spacer(1, 4))

    # 2. Contact Line (NO EMOJIS, NO FT ID)
    contact_line = f"{email} | {phone} | {location} | {linkedin_url}"
    story.append(Paragraph(contact_line, contact_style))
    story.append(Spacer(1, 6))

    # Horizontal Divider
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceBefore=2, spaceAfter=8))

    # 3. Section 1: ABOUT ME / PROFIL PROFESSIONNEL
    story.append(Paragraph("PROFIL PROFESSIONNEL", heading_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E2E8F0'), spaceBefore=1, spaceAfter=4))
    about_text = (
        f"Professionnel expérimenté et passionné par l'excellence opérationnelle et l'innovation dans le domaine {role.lower()}. "
        "Solide capacité d'analyse, de résolution de problèmes complexes et de travail en équipe pluridisciplinaire. "
        "Orienté résultats avec une parfaite maîtrise des enjeux stratégiques et des bonnes pratiques du secteur."
    )
    story.append(Paragraph(about_text, body_style))
    story.append(Spacer(1, 6))

    # 4. Section 2: TECHNICAL SKILLS & COMPÉTENCES
    story.append(Paragraph("COMPÉTENCES TECHNIQUES & EXPERTISES", heading_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E2E8F0'), spaceBefore=1, spaceAfter=4))
    skills_text = (
        "<b>Savoir-faire :</b> Gestion de projet, Analyse de données, Pilotage de la performance, Optimisation des processus, Conduite du changement.<br/>"
        "<b>Outils & Technologies :</b> Python, SQL, BigQuery, Cloud Computing, Pack Office Avancé, Dataviz & Dashboarding.<br/>"
        "<b>Langues :</b> Français (Langue maternelle), Anglais (Courant / Professionnel)."
    )
    story.append(Paragraph(skills_text, body_style))
    story.append(Spacer(1, 6))

    # 5. Section 3: EXPERIENCE PROFESSIONNELLE
    story.append(Paragraph("EXPÉRIENCE PROFESSIONNELLE", heading_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E2E8F0'), spaceBefore=1, spaceAfter=4))

    comp1 = random.choice(COMPANIES_LIST)
    exp1 = (
        f"<b>{role}</b> — <i>{comp1}</i> (2021 - Présent)<br/>"
        "• Pilotage et coordination des projets stratégiques à forte valeur ajoutée.<br/>"
        "• Conception et mise en œuvre d'outils d'analyse décisionnelle améliorant l'efficacité opérationnelle de 25%.<br/>"
        "• Management fonctionnel des équipes et suivi rigoureux des KPIs et livrables."
    )
    story.append(Paragraph(exp1, body_style))
    story.append(Spacer(1, 4))

    comp2 = random.choice([c for c in COMPANIES_LIST if c != comp1])
    exp2 = (
        f"<b>Analyste & Chargé de Mission</b> — <i>{comp2}</i> (2018 - 2021)<br/>"
        "• Analyse des besoins métier et rédaction des cahiers des charges fonctionnels.<br/>"
        "• Optimisation de la qualité des données et automatisation des reportings hebdomadaires."
    )
    story.append(Paragraph(exp2, body_style))
    story.append(Spacer(1, 6))

    # 6. Section 4: EDUCATION & FORMATION
    story.append(Paragraph("EDUCATION & FORMATION", heading_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E2E8F0'), spaceBefore=1, spaceAfter=4))
    edu_text = (
        "<b>Master 2 / Diplôme d'Ingénieur</b> — Université / Grande École (2018)<br/>"
        "Specialisation Ingénierie, Systèmes d'Information et Gestion de Projets."
    )
    story.append(Paragraph(edu_text, body_style))
    story.append(Spacer(1, 6))

    # 7. Section 5: CERTIFICATIONS & INTERESTS
    story.append(Paragraph("CERTIFICATIONS & CENTRES D'INTÉRÊT", heading_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E2E8F0'), spaceBefore=1, spaceAfter=4))
    cert_text = (
        "<b>Certifications :</b> Certification Gestion de Projet Agile / Scrum, Certification Cloud Analytics.<br/>"
        "<b>Centres d'intérêt :</b> Veille technologique, Sport (Course à pied, Tennis), Engagements associatifs."
    )
    story.append(Paragraph(cert_text, body_style))

    doc.build(story)

def generate_and_upload_all_cvs():
    print(f"Generating 300 Clean Kengni Model PDF CVs into '{TEMP_RESUMES_DIR}'...")
    os.makedirs(TEMP_RESUMES_DIR, exist_ok=True)

    candidates = []
    for i in range(1, 301):
        did = f"DEM-2025-{i:03d}"
        fn = random.choice(FIRST_NAMES)
        ln = random.choice(LAST_NAMES)
        full_name = f"{fn} {ln}"
        role, domain = random.choice(ROLES_LIST)
        dept_code, city = random.choice(DEPARTMENTS)
        deg_lvl, deg_label = random.choice(DEGREES)

        email = f"{fn.lower()}.{ln.lower()}@email-candidat.fr"
        phone = f"+33 6 {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)}"
        location = f"{city} ({dept_code}), France"
        linkedin = f"linkedin.com/in/{fn.lower()}-{ln.lower()}"

        pdf_filename = f"cv_{did}.pdf"
        local_pdf_path = os.path.join(TEMP_RESUMES_DIR, pdf_filename)
        gcs_pdf_uri = f"{RESUMES_BUCKET}/resumes/{pdf_filename}"

        # Generate local 1-page PDF
        generate_kengni_pdf_cv(local_pdf_path, full_name, role, email, phone, location, linkedin)

        candidates.append({
            "demandeur_id": did,
            "nom": ln,
            "prenom": fn,
            "intitule_poste_recherche": role,
            "domaine_professionnel": domain,
            "department_code": dept_code,
            "ville": city,
            "niveau_diplome": deg_lvl,
            "intitule_diplome": deg_label,
            "experience_annees": random.randint(2, 15),
            "pretention_salariale_brut_annuel_eur": float(random.randint(35, 85) * 1000),
            "disponibilite_immediate": random.choice([True, False]),
            "cv_gcs_uri": gcs_pdf_uri,
            "categorie_inscription": "Catégorie A",
            "anciennete_chomage_mois": random.randint(1, 24)
        })

    df_cand = pd.DataFrame(candidates)
    cand_csv = os.path.join(DATA_DIR, "france_travail_demandeurs.csv")
    df_cand.to_csv(cand_csv, index=False)
    print(f"  ✓ Saved updated candidate database: {cand_csv} ({len(df_cand)} rows)")

    # Upload all PDFs to GCS bucket
    print(f"Uploading 300 PDF CVs to GCS bucket '{RESUMES_BUCKET}/resumes/'...")
    cmd_upload = f"gcloud storage cp {TEMP_RESUMES_DIR}/*.pdf {RESUMES_BUCKET}/resumes/"
    subprocess.run(cmd_upload, shell=True, check=True)
    print("  ✓ Upload to GCS complete!")

    # Clean up local PDF files directory completely
    print("Removing temporary local PDF files from disk...")
    shutil.rmtree(TEMP_RESUMES_DIR, ignore_errors=True)
    resumes_dir_old = os.path.join(DATA_DIR, "resumes")
    shutil.rmtree(resumes_dir_old, ignore_errors=True)
    print("  ✓ All local PDF CV files deleted successfully! CVs live strictly in GCS bucket.")

    # Update ATS applications table candidatures_postulations_suivi.csv
    offers_csv = os.path.join(DATA_DIR, "offres_emploi_recrutement.csv")
    df_offers = pd.read_csv(offers_csv)

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
    apps_csv = os.path.join(DATA_DIR, "candidatures_postulations_suivi.csv")
    df_apps.to_csv(apps_csv, index=False)

    # Reload all 7 tables into BigQuery
    client = get_client()
    tables = [
        "bmo_recrutement_2025", "rome_arborescence_2024", "entreprises_urssaf_declarations",
        "offres_emploi_recrutement", "france_travail_demandeurs", "candidatures_postulations_suivi",
        "france_travail_formations_aides"
    ]

    for tname in tables:
        c_path = os.path.join(DATA_DIR, f"{tname}.csv")
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
    generate_and_upload_all_cvs()
