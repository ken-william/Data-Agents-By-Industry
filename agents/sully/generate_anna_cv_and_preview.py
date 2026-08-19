#!/usr/bin/env python3
"""
Generate Anna Kowalski's (FT-99720068) official 1-Page PDF CV and PNG Preview image,
and upload them directly to GCS gs://sully-candidate-resumes-data-agents/resumes/.
"""

import os
import sys
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

BUCKET_NAME = "gs://sully-candidate-resumes-data-agents"
SULLY_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SULLY_DIR, "data", "anna_cv")
os.makedirs(OUT_DIR, exist_ok=True)

pdf_filename = "cv_FT-99720068.pdf"
png_prefix = "cv_FT-99720068_preview"
pdf_path = os.path.join(OUT_DIR, pdf_filename)
png_path = os.path.join(OUT_DIR, f"{png_prefix}.png")

def create_anna_pdf():
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1,
        fontName='Helvetica-Bold'
    )

    role_style = ParagraphStyle(
        'RoleStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2563EB'),
        alignment=1,
        fontName='Helvetica-Bold'
    )

    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#4B5563'),
        alignment=1,
        fontName='Helvetica'
    )

    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=10,
        spaceAfter=4,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1F2937'),
        fontName='Helvetica'
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1F2937'),
        leftIndent=12,
        fontName='Helvetica'
    )

    story = []

    # Header
    story.append(Paragraph("ANNA KOWALSKI", name_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("RESPONSABLE SUPPLY CHAIN &amp; LOGISTIQUE VERTE", role_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("anna.kowalski@email-voyageur.fr | +33 6 12 34 56 78 | Paris (75) | Identifiant FT: FT-99720068", contact_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=10))

    # Profile Summary
    story.append(Paragraph("PROFIL &amp; OBJECTIF PROFESSIONNEL", section_style))
    story.append(Paragraph("Professionnelle diplômée en Logistique et Transports (Bac+3) justifiant de 5 années d'expérience en gestion de stocks, optimisation des réapprovisionnements et planification de flux de transport. Recherche activement un poste de <b>Responsable Supply Chain / Logistique Verte</b> en Île-de-France avec horaires adaptés (8h30-17h30) et accès direct en transports en commun.", body_style))
    story.append(Spacer(1, 8))

    # Technical Skills
    story.append(Paragraph("COMPÉTENCES CLÉS &amp; EXPERTISE", section_style))
    story.append(Paragraph("• <b>Gestion Supply Chain &amp; ERP</b> : Maîtrise avancée de SAP S/4HANA (modules MM/SD), Excel avancé (VBA, TCD), WMS Logistique.", bullet_style))
    story.append(Paragraph("• <b>Planification &amp; Transport</b> : Gestion et ordonnancement des flux de camionnage, réduction de l'empreinte carbone fret.", bullet_style))
    story.append(Paragraph("• <b>Gestion de Stocks</b> : Inventaires tournants, optimisation des seuils de réapprovisionnement et réduction des surstocks.", bullet_style))
    story.append(Paragraph("• <b>Langues</b> : Français (Natif), Anglais professionnel courant (TOEIC 850).", bullet_style))
    story.append(Spacer(1, 8))

    # Experience
    story.append(Paragraph("EXPÉRIENCE PROFESSIONNELLE", section_style))
    story.append(Paragraph("<b>Assistante Logistique &amp; Transport Senior</b> | ChronoLogistics Paris (2021 - 2024)", body_style))
    story.append(Paragraph("• Gestion quotidienne de l'approvisionnement des entrepôts d'Île-de-France (volume de 450 tonnes/semaine).", bullet_style))
    story.append(Paragraph("• Négociation et suivi des contrats de sous-traitance de transport routier (-12% de coûts logistiques).", bullet_style))
    story.append(Paragraph("• Supervision de l'équipe d'exploitation logistique (4 préparateurs de commandes).", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Gestionnaire de Stocks &amp; Flux</b> | Logistics Express IDF (2019 - 2021)", body_style))
    story.append(Paragraph("• Suivi informatique sous SAP des entrées/sorties et traitement des litiges fournisseurs.", bullet_style))
    story.append(Paragraph("• Mise en place de tableaux de bord kpi d'efficacité logistique sous Excel/PowerBI.", bullet_style))
    story.append(Spacer(1, 8))

    # Education
    story.append(Paragraph("FORMATION &amp; DIPLÔMES", section_style))
    story.append(Paragraph("• <b>Licence Professionnelle Métiers de la Logistique &amp; Transport</b> | Université Paris-Saclay (2019)", bullet_style))
    story.append(Paragraph("• <b>DUT Gestion Logistique et Transport (GLT)</b> | IUT de Tremblay-en-France (2018)", bullet_style))
    story.append(Spacer(1, 8))

    # Constraints / Mobility
    story.append(Paragraph("DISPONIBILITÉ &amp; CONTRAINTES LOGISTIQUES", section_style))
    story.append(Paragraph("• <b>Disponibilité</b> : Immédiate (Inscrite France Travail Catégorie A - 14 mois).", bullet_style))
    story.append(Paragraph("• <b>Horaires souhaités</b> : 8h30 - 17h30 (Impératif garde de 2 enfants en bas âge).", bullet_style))
    story.append(Paragraph("• <b>Mobilité</b> : Réseau Transports en Commun RER / Métro Île-de-France.", bullet_style))

    doc.build(story)
    print(f"  ✓ Built PDF CV at: {pdf_path}")

def convert_pdf_to_png():
    cmd = ["pdftoppm", "-png", "-r", "150", "-singlefile", pdf_path, os.path.join(OUT_DIR, png_prefix)]
    subprocess.run(cmd, check=True)
    print(f"  ✓ Converted PDF to PNG preview image at: {png_path}")

def upload_to_gcs():
    print(f"  Uploading Anna's PDF CV and PNG preview to GCS bucket '{BUCKET_NAME}'...")
    subprocess.run(f"gcloud storage cp {pdf_path} {BUCKET_NAME}/resumes/{pdf_filename}", shell=True, check=True)
    subprocess.run(f"gcloud storage cp {png_path} {BUCKET_NAME}/resumes/{png_prefix}.png", shell=True, check=True)

    # Set public read permission on GCS object so browser UI can render it directly
    subprocess.run(f"gcloud storage chmod a+r {BUCKET_NAME}/resumes/{png_prefix}.png 2>/dev/null", shell=True)
    subprocess.run(f"gcloud storage chmod a+r {BUCKET_NAME}/resumes/{pdf_filename} 2>/dev/null", shell=True)
    print("  ✓ Upload complete & public read permissions set!")

def main():
    create_anna_pdf()
    convert_pdf_to_png()
    upload_to_gcs()

if __name__ == "__main__":
    main()
