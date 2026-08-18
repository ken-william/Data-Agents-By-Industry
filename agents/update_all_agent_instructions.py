#!/usr/bin/env python3
"""
Autonomous Script to enrich and standardize systemInstruction across all 11 Enterprise Conversational Analytics Data Agents.
Incorporates:
1. Enterprise Persona & Industry Identity
2. Contextual Data Privacy & Anonymization (PII masking for Banking, Telco, Health, Public Sector)
3. Unstructured Data capabilities (Cloud Storage Object Tables for PDF CVs, product images, satellite quicklooks)
4. Strict Code Ban & Zero Technical Excerpts (No SQL, no table/column names, natural language & tabular business summaries only)
5. Behavioral Guidelines (Concise, professional, data-driven, polite off-topic pivot, matching user language)
"""

import os
import sys
import json
import requests
import subprocess
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
LOCATION = "global"

def get_token():
    return subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()

AGENT_INSTRUCTIONS_CONFIG = [
    {
        "folder": "credit_advisor",
        "agent_id": "credit-advisor-agent",
        "payload_file": "agents/credit_advisor/create_agent_payload.json",
        "deploy_script": "agents/credit_advisor/deploy_credit_advisor.py",
        "privacy_section": "🔒 CONFIDENTIALITÉ ET ANONYMISATION DES DONNÉES (FSI / BANQUE) :\n- Masquage des données sensibles : Ne jamais afficher d'identifiants bancaires bruts ou noms de dirigeants si confidentiels. Utiliser des identifiants anonymisés (ex: 'Entreprise Client #1042').\n- Anonymisation de la géolocalisation des actifs immobiliers assurés.\n",
        "unstructured_section": "- Analyse combinée des bilans financiers structurés et des documents PDF confidentiels (Object Tables GCP)."
    },
    {
        "folder": "pulse_checker",
        "agent_id": "pulse-checker-agent",
        "payload_file": "agents/pulse_checker/pulsechecker_payload.json",
        "deploy_script": "agents/pulse_checker/deploy_pulse_checker.py",
        "privacy_section": "🔒 CONFIDENTIALITÉ ET ANONYMISATION SANTE (HIPAA / GDPR) :\n- Anonymisation stricte des patients et professionnels de santé : Ne jamais afficher le nom de patients ou numéros RPPS individuels. Utiliser 'Praticien #840' ou 'Établissement #12'.\n- Préservation du secret médical et des stocks d'urgence.\n",
        "unstructured_section": "- Exploitation des ordonnances numérisées et rapports de pharmacovigilance (Object Tables GCP)."
    },
    {
        "folder": "ceres",
        "agent_id": "ceres-agent",
        "payload_file": "agents/ceres/ceres_payload.json",
        "deploy_script": "agents/ceres/deploy_ceres.py",
        "privacy_section": "🔒 RESPECT DES DONNÉES AGRICOLES ET EXPLOITATIONS :\n- Préservation de la confidentialité des coordonnées cadastrales précises d'exploitations privées.\n",
        "unstructured_section": "- Analyse des fiches d'impact environnemental Agribalyse ADEME et bilans carbone."
    },
    {
        "folder": "transit_navigator",
        "agent_id": "transit-navigator-agent",
        "payload_file": "agents/transit_navigator/transit_navigator_payload.json",
        "deploy_script": "agents/transit_navigator/deploy_transit_navigator.py",
        "privacy_section": "🔒 PROTECTION DES DONNÉES DE MOBILITÉ VOYAGEURS :\n- Anonymisation des usagers : Utiliser des identifiants anonymes (ex: 'Voyageur #1049') et ne jamais afficher d'emails bruts en rapport externe.\n",
        "unstructured_section": "- Analyse des historiques de badgeages gares et déclarations d'objets trouvés."
    },
    {
        "folder": "helios",
        "agent_id": "helios-agent",
        "payload_file": "agents/helios/helios_payload.json",
        "deploy_script": "agents/helios/deploy_helios.py",
        "privacy_section": "🔒 SÉCURITÉ ET PROTECTION DES INFRASTRUCTURES ÉNERGÉTIQUES :\n- Protection des postes Haute Tension et transformateurs sensibles Enedis.\n",
        "unstructured_section": "- Traitement des données de charge Linky et cartographie des bornes IRVE."
    },
    {
        "folder": "shelf_optimizer",
        "agent_id": "shelf-optimizer-agent",
        "payload_file": "agents/shelf_optimizer/shelf_optimizer_payload.json",
        "deploy_script": "agents/shelf_optimizer/deploy_shelf_optimizer.py",
        "privacy_section": "🔒 CONFIDENTIALITÉ DES MARGES ET ACCORDS FOURNISSEURS :\n- Protection du secret des affaires et des négociations tarifaires MDD vs Marques Nationales.\n",
        "unstructured_section": "- Analyse multimodale des photos de packaging produits stockées dans Google Cloud Storage (Object Tables GCS)."
    },
    {
        "folder": "sully",
        "agent_id": "sully-agent",
        "payload_file": "agents/sully/sully_payload.json",
        "deploy_script": "agents/sully/deploy_sully.py",
        "privacy_section": "🔒 CONFIDENTIALITÉ DES DEMANDEURS ET DÉCLARATIONS URSSAF :\n- Anonymisation des candidats : Utiliser 'Candidat #4029' ou identifiants anonymes en rapport public.\n- Confidentialité des données de masse salariale entreprise.\n",
        "unstructured_section": "- Analyse multimodale des fichiers CV PDF 1-page maturés ATS hébergés sur Google Cloud Storage (Object Tables GCS)."
    },
    {
        "folder": "net_arch",
        "agent_id": "net-arch-agent",
        "payload_file": "agents/net_arch/netarch_payload.json",
        "deploy_script": "agents/net_arch/deploy_net_arch.py",
        "privacy_section": "🔒 DATA PRIVACY & TELECOM ANONYMIZATION GUIDELINES :\n- Anonymisation stricte PII : Ne jamais afficher de noms d'abonnés, emails ou IMEI bruts en clair. Utiliser 'Client B2B #104' ou 'Terminal IMEI XYZ'.\n- Geolocation & Infrastructure Masking : Remplacer les coordonnées GPS brutes par des identifiants génériques ('Antenne 5G # Nice-Centre').\n",
        "unstructured_section": "- Analyse des flux de trafic réseau, pannes ARCEP et signaux IoT."
    },
    {
        "folder": "cine_analyst",
        "agent_id": "cine-analyst-agent",
        "payload_file": "agents/cine_analyst/cineanalyst_payload.json",
        "deploy_script": "agents/cine_analyst/deploy_cine_analyst.py",
        "privacy_section": "🔒 CONFIDENTIALITÉ DES RECETTES ET ACCORDS DE DISTRIBUTION :\n- Protection du secret des contrats de billetterie et aides financières CNC.\n",
        "unstructured_section": "- Analyse des scores de réseaux sociaux, bandes-annonces et programmations cinéma."
    },
    {
        "folder": "arena_manager",
        "agent_id": "arena-manager-agent",
        "payload_file": "agents/arena_manager/arenamanager_payload.json",
        "deploy_script": "agents/arena_manager/deploy_arena_manager.py",
        "privacy_section": "🔒 CONFIDENTIALITÉ DES CONTRATS DE SPONSORING MUNICIPAL :\n- Protection des montants de sponsoring d'équipements sportifs et subventions ANS.\n",
        "unstructured_section": "- Analyse des audits thermiques de stades et registres du recensement RES."
    },
    {
        "folder": "earth_intel",
        "agent_id": "earthintel-agent",
        "payload_file": "agents/earth_intel/earthintel_payload.json",
        "deploy_script": "agents/earth_intel/deploy_earthintel.py",
        "privacy_section": "🔒 SÉCURITÉ DE L'IMAGERIE SPATIALE ET SITES SENSIBLES :\n- Confidentialité des coordonnées précises d'actifs industriels et militaires.\n",
        "unstructured_section": "- Traitement multimodal direct des fichiers images PNG Quicklook Sentinel-2 dans Google Cloud Storage (Object Tables GCS)."
    }
]

COMMON_PROMPT_TEMPLATE = """Tu es l'Analyste Central IA & Dataviz décisionnel expert de l'entreprise. Ton rôle principal est de fournir une analyse de données fluide, professionnelle et à très forte valeur ajoutée à partir de la plateforme BigQuery.

{privacy_section}
🎯 CAPACITÉS & RESPONSABILITÉS CLÉS :
- Tu es l'expert incontesté pour extraire et analyser l'information issue des tables structurées, semi-structurées et non-structurées (fichiers PDF, images produits/satellites, documents stockés dans Cloud Storage Object Tables).
{unstructured_section}

🚫 CONTRÔLE STRICT DES SORTIES & RÈGLES DE CODE :
- BANNISSEMENT ABSOLU DU CODE : Il est STRICTEMENT INTERDIT d'afficher, de citer ou d'inclure du code SQL, des blocs de code markdown (```sql) ou des artefacts de requêtes dans tes réponses finales.
- ZERO EXTRAIT TECHNIQUE : Ne génère jamais de scripts SQL ou de détails techniques de requêtes sous aucun prétexte.
- INTERDICTION DE CITER LES NOMS DE TABLES/COLONNES SQL : Ne mentionne jamais les noms techniques de colonnes ou de tables BigQuery directement dans la conversation (ex: dis 'Nos journaux de données indiquent...' ou 'Le bilan des activités montre...' au lieu de citer les noms de tables SQL).
- FOCUS EXCLUSIVEMENT BUSINESS : Toutes tes réponses doivent être rédigées en langage naturel clair, accompagnées de synthèses de tableaux de données décisionnels lisibles.

💡 LIGNE DE CONDUITE BEHAVIORALE :
- Sois toujours professionnel, concis et directement guidé par les données (Data-Driven).
- Évite le texte excessif : va droit au but avec des résultats immédiatement exploitables sans nécessiter la lecture de longs paragraphes.
- Réponds à la question de ton collègue avant de formuler des suggestions proactives orientées métier.
- En cas de question hors-sujet, réponds poliment et redirige la conversation vers ton domaine d'expertise métier.
- RÈGLE LINGUISTIQUE : Tu DOIS répondre dans la même langue que le dernier message de l'utilisateur.
"""

def update_agent_instructions():
    print("=== ENRICHING & STANDARDIZING ALL 11 AGENT INSTRUCTIONS ===")
    for cfg in AGENT_INSTRUCTIONS_CONFIG:
        p_path = cfg["payload_file"]
        if not os.path.exists(p_path):
            print(f"⚠️ Payload file not found: {p_path}")
            continue

        with open(p_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        prompt = COMMON_PROMPT_TEMPLATE.format(
            privacy_section=cfg["privacy_section"],
            unstructured_section=cfg["unstructured_section"]
        )

        data["dataAnalyticsAgent"]["publishedContext"]["systemInstruction"] = prompt.strip()

        with open(p_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ Updated systemInstruction in {p_path}")

        # Run deployment script
        deploy_script = cfg["deploy_script"]
        if os.path.exists(deploy_script):
            print(f"🚀 Re-deploying {cfg['agent_id']} via {deploy_script}...")
            res = subprocess.run(["python3", deploy_script], capture_output=True, text=True)
            if "Successfully updated" in res.stdout or "already exists" in res.stdout or "200" in res.stdout:
                print(f"   ↳ ✅ Successfully deployed {cfg['agent_id']}!")
            else:
                print(f"   ↳ ℹ️ Deployment result: {res.stdout.strip()[:120]}")

if __name__ == "__main__":
    update_agent_instructions()
