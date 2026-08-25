"""
Google ADK Central Orchestrator Agent (Master Host / Virtual Presenter).
Tier 2 of Talk to Data Architecture.

Charismatic, multilingual master presenter that enables 100% hands-free voice navigation,
discovering and switching agents by voice, narrating rich storytelling during BigQuery execution,
and delivering polished business syntheses.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional, Generator

try:
    from mcp_toolbox.toolbox_client import toolbox_client
except ImportError:
    from backend.mcp_toolbox.toolbox_client import toolbox_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("adk_orchestrator")

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
LOCATION = "global"

# Rich Multi-Domain Agent Knowledge Base (Context, Metrics, Dynamic Thinking Banks & Sector Hooks)
AGENT_KNOWLEDGE_BASE = {
    "arena_manager_agent": {
        "name": "ArenaManager",
        "sector": "Sport, Stades & Grandes Infrastructures",
        "dataset": "arena_manager_ds",
        "mission": "Optimisation de la billetterie dynamique, maximisation des revenus des loges VIP et régulation des flux spectateurs.",
        "anecdote": "Les loges VIP représentent moins de 8% des sièges d'un stade mais génèrent plus de 42% de la marge brute d'un grand événement.",
        "key_metrics": ["taux d'occupation VIP", "revenu moyen par siège (RevPAS)", "temps d'attente aux buvettes", "marge nette par tribune"],
        "thinking_phrases": [
            "Pendant que j'interroge les flux de billetterie et de restauration du stade...",
            "Regardons la rentabilité comparée entre tribunes grand public et loges privatives...",
            "Nos modèles BigQuery croisent l'affluence en temps réel et les consommations moyennes...",
            "J'analyse les données d'occupation des sièges et les pics d'accès aux buvettes..."
        ],
        "scenario_intros": [
            "Bienvenue dans l'espace ArenaManager ! Nous pilotons ici l'économie des grands stades et arènes sportives.",
            "Regardons de plus près l'exploitation événementielle et la rentabilité des espaces VIP avec ArenaManager.",
            "Nous voici connectés à la télémétrie des stades. Nous pouvons analyser l'affluence, la marge des loges ou les flux de supporters."
        ],
        "keywords": ["stade", "arena", "sport", "vip", "billetterie", "foot", "match", "concession", "buvette", "spectateur", "tribune"]
    },
    "sully_agent": {
        "name": "Sully",
        "sector": "Secteur Public, RH & Hôpitaux",
        "dataset": "public_sector_employment_ds",
        "mission": "Pilotage des tensions de recrutement hospitalier, réduction des surcoûts d'intérim et analyse des grilles indiciaires.",
        "anecdote": "Chaque poste de médecin ou infirmier vacant plus de 6 mois coûte en moyenne 850 euros par jour en intérim d'urgence.",
        "key_metrics": ["taux de vacance indiciaire", "surcoût intérim journalier (850€/j)", "délai moyen de recrutement", "taux de rotation des effectifs"],
        "thinking_phrases": [
            "Pendant que je consulte les grilles indiciaires et les vacances de postes hospitaliers...",
            "Regardons la répartition des surcoûts d'intérim médical par département...",
            "Nos modèles BigQuery croisent les départs à la retraite et les tensions de recrutement...",
            "J'extrais l'historique des délais d'embauche pour les spécialités en tension critique..."
        ],
        "scenario_intros": [
            "Bienvenue dans le pôle RH hospitalier avec Sully. Nous analysons ici les tensions d'embauche et le coût des remplacements.",
            "Regardons de plus près la gestion des effectifs de santé et la masse salariale publique avec Sully.",
            "Nous voici sur le pilotage RH du secteur public. Nous pouvons évaluer les surcoûts d'intérim ou les postes vacants par région."
        ],
        "keywords": ["sully", "public", "rh", "hôpital", "recrutement", "emploi", "vacance", "infirmier", "médecin", "urssaf", "fonction publique", "soignant"]
    },
    "earth_intel_agent": {
        "name": "EarthIntel",
        "sector": "Spatial, Climat & Imagerie Satellite",
        "dataset": "skywatch_aerospace_ds",
        "mission": "Surveillance chlorophyllienne par satellite Sentinel-2 (10m), détection du stress hydrique agricole (NDVI) et conformité CSRD zéro déforestation.",
        "anecdote": "La constellation spatiale européenne Sentinel-2 revisite chaque parcelle agricole de France tous les 5 jours avec 13 bandes spectrales haute résolution.",
        "key_metrics": ["indice de vigueur végétale NDVI (0-1)", "taux d'humidité du sol", "surface en stress hydrique critique", "couverture nuageuse (%)"],
        "thinking_phrases": [
            "Pendant que j'interroge les dernières passes spectrales du satellite Sentinel-2...",
            "Regardons l'évolution de l'indice de biomasse NDVI sur les parcelles observées...",
            "Nos modèles orbitaux comparent la réflectance infrarouge avec la moyenne saisonnière...",
            "J'analyse les zones agricoles présentant un déficit hydrique sévère..."
        ],
        "scenario_intros": [
            "Bienvenue sur EarthIntel. Nous analysons la santé des sols et le climat grâce aux satellites européens Sentinel-2.",
            "Regardons de plus près les observations spatiales haute résolution et le stress hydrique des cultures avec EarthIntel.",
            "Nous voici sur l'intelligence géospatiale. Nous pouvons inspecter les parcelles agricoles ou vérifier la conformité environnementale."
        ],
        "keywords": ["spatial", "satellite", "earth", "intel", "ndvi", "végétation", "sentinel", "climat", "sécheresse", "imagerie", "parcelle", "chlorophylle"]
    },
    "credit_advisor_agent": {
        "name": "CreditAdvisor",
        "sector": "Banque, Finance & Risque B2B",
        "dataset": "credit_risk_scoring_ds",
        "mission": "Scoring prédictif de défaillance d'entreprises, provisionnement comptable IFRS 9 et maximisation du rendement ajusté du risque (RAROC).",
        "anecdote": "L'anticipation d'un défaut de paiement à 90 jours grâce au croisement des flux de trésorerie permet de récupérer 65% de créance supplémentaire.",
        "key_metrics": ["probabilité de défaut à 1 an (PD)", "perte en cas de défaut (LGD)", "provisionnement IFRS 9 (Bucket 1, 2, 3)", "ratio de levier financier"],
        "thinking_phrases": [
            "Pendant que nos modèles BigQuery calculent les scores de solvabilité et ratios IFRS 9...",
            "Regardons l'exposition au risque de crédit et les créances sous surveillance...",
            "J'évalue la probabilité de défaillance des contreparties selon leur structure de dette...",
            "Nos algorithmes financiers comparent les flux de trésorerie avec les seuils d'alerte bancaire..."
        ],
        "scenario_intros": [
            "Bienvenue dans le pôle Risque et Crédit B2B avec CreditAdvisor. Nous anticipons ici les défauts de paiement et calibrons les provisions.",
            "Regardons de plus près la solvabilité des portefeuilles d'entreprises et le scoring prudentiel avec CreditAdvisor.",
            "Nous voici connectés aux données bancaires. Nous pouvons analyser les encours à risque, les ratios IFRS 9 ou la solidité des bilans."
        ],
        "keywords": ["crédit", "banque", "finance", "fiben", "défaut", "risque", "ifrs9", "bilan", "trésorerie", "prêt", "solvabilité", "encours"]
    },
    "cine_analyst_agent": {
        "name": "CineAnalyst",
        "sector": "Cinéma, Médias & Box-Office",
        "dataset": "cine_analyst_ds",
        "mission": "Prédiction des entrées en salles, rentabilité des investissements de coproduction CNC et calendrier optimal de sortie.",
        "anecdote": "Le premier week-end d'exploitation d'un film en France détermine historiquement 38% de son box-office global en salles.",
        "key_metrics": ["entrées premier week-end", "coefficient de persistance en salles", "taux de retour sur investissement CNC", "part de marché par distributeur"],
        "thinking_phrases": [
            "Pendant que je consulte les chiffres d'entrées CNC et les historiques de box-office...",
            "Regardons la rentabilité des coproductions par rapport à leur budget initial...",
            "Nos modèles prédictifs comparent la fréquentation des salles selon le genre et le casting...",
            "J'analyse l'impact du bouche-à-oreille sur la durée d'exploitation des longs-métrages..."
        ],
        "scenario_intros": [
            "Bienvenue sur CineAnalyst. Nous décryptons l'économie du 7ème art, les investissements du CNC et les prévisions d'entrées en salles.",
            "Regardons de plus près les performances du box-office et la rentabilité des films avec CineAnalyst.",
            "Nous voici sur l'analyse cinématographique. Nous pouvons évaluer le potentiel d'un casting ou optimiser une date de sortie."
        ],
        "keywords": ["cinéma", "film", "box-office", "entrées", "cnc", "salle", "casting", "production", "roi", "streaming", "distributeur"]
    },
    "net_arch_agent": {
        "name": "NetArch",
        "sector": "Télécoms, Réseaux & ARCEP",
        "dataset": "telecom_network_arcep_ds",
        "mission": "Supervision de la couverture 5G, maintenance prédictive des antennes relais et réduction de l'attrition des forfaits B2B.",
        "anecdote": "Une hausse de température CPU anormale sur un pylône 5G permet de prédire une panne matérielle 72 heures avant toute coupure d'abonnés.",
        "key_metrics": ["revenu moyen par abonné (ARPU)", "taux de disponibilité des cellules 5G (99.9%)", "taux de churn mensuel", "débit moyen descendant (Mbps)"],
        "thinking_phrases": [
            "Pendant que j'interroge la télémétrie des antennes relais et les métriques ARCEP...",
            "Regardons la corrélation entre les incidents réseau et les résiliations de forfaits...",
            "Nos modèles télécoms inspectent la charge de trafic sur les cellules 5G en heure de pointe...",
            "J'analyse les disparités d'ARPU et de fidélité selon les gammes d'abonnements..."
        ],
        "scenario_intros": [
            "Bienvenue sur NetArch. Nous supervisons ici l'infrastructure télécoms 5G et la rentabilité des parcs d'abonnés.",
            "Regardons de plus près la qualité de service réseau et la fidélisation client avec NetArch.",
            "Nous voici au cœur des réseaux télécoms. Nous pouvons diagnostiquer des cellules saturées ou analyser l'ARPU par forfait."
        ],
        "keywords": ["télécom", "antenne", "5g", "fibre", "arcep", "pylône", "réseau", "forfait", "panne", "arpu", "client", "churn", "débit"]
    },
    "transit_navigator_agent": {
        "name": "TransitNavigator",
        "sector": "Transports & Mobilité SNCF",
        "dataset": "sncf_gtfs_mobility_ds",
        "mission": "Analyse de la ponctualité ferroviaire TGV/TER, détection des nœuds d'engorgement et prévision des retards de correspondance.",
        "anecdote": "Sur le réseau ferré national, 70% des retards en cascade proviennent de seulement 12 nœuds d'aiguillage stratégiques.",
        "key_metrics": ["taux de régularité à 5 minutes (%)", "retard moyen au terminus (minutes)", "temps de correspondance critique", "taux d'occupation des rames"],
        "thinking_phrases": [
            "Pendant que je consulte les flux horaires GTFS et les relevés de ponctualité SNCF...",
            "Regardons les gares et lignes ferroviaires concentrant les plus forts retards cumulés...",
            "Nos algorithmes identifient les effets dominos sur les correspondances en heure de pointe...",
            "J'extrais les causes principales de ralentissement sur les corridors à grande vitesse..."
        ],
        "scenario_intros": [
            "Bienvenue sur TransitNavigator. Nous analysons la régularité ferroviaire et la ponctualité des trains sur le réseau national.",
            "Regardons de plus près les flux de voyageurs et la fluidité des correspondances avec TransitNavigator.",
            "Nous voici sur la mobilité ferroviaire. Nous pouvons cibler les lignes en retard ou évaluer l'impact des travaux sur la ponctualité."
        ],
        "keywords": ["train", "sncf", "gare", "tgv", "ter", "retard", "ponctualité", "mobilité", "voyageur", "correspondance", "ferroviaire", "ligne"]
    },
    "pulse_checker_agent": {
        "name": "PulseChecker",
        "sector": "Santé & Hôpitaux RPPS",
        "dataset": "health_care_france_ds",
        "mission": "Cartographie des déserts médicaux, temps d'attente par spécialité et démographie des praticiens RPPS.",
        "anecdote": "Pour certaines spécialités comme l'ophtalmologie ou la dermatologie, le délai moyen de rendez-vous varie d'un facteur 1 à 8 selon les départements.",
        "key_metrics": ["densité médicale pour 100 000 habitants", "délai moyen de prise en charge (jours)", "âge moyen des praticiens", "indice de tension territoriale"],
        "thinking_phrases": [
            "Pendant que je consulte l'annuaire national RPPS et les données d'accès aux soins...",
            "Regardons la densité de spécialistes par bassin de population...",
            "Nos modèles cartographient les zones sous-dotées nécessitant des renforts médicaux...",
            "J'analyse les délais d'attente moyens pour les consultations spécialisées..."
        ],
        "scenario_intros": [
            "Bienvenue sur PulseChecker. Nous cartographions l'offre de soins et la démographie médicale sur l'ensemble du territoire.",
            "Regardons de plus près l'accessibilité aux médecins et les déserts médicaux avec PulseChecker.",
            "Nous voici sur la santé publique. Nous pouvons mesurer les délais d'attente ou cibler les territoires en pénurie de spécialistes."
        ],
        "keywords": ["santé", "médecin", "désert", "rpps", "patient", "attente", "cabinet", "spécialiste", "soin", "consultation", "praticien"]
    },
    "shelf_optimizer_agent": {
        "name": "ShelfOptimizer",
        "sector": "Retail & Grande Distribution",
        "dataset": "retail_merchandising_ds",
        "mission": "Optimisation du facing en rayon, prévention des ruptures de stock critiques et maximisation de la marge linéaire.",
        "anecdote": "En grande distribution, un taux de rupture supérieur à 4% en rayon le samedi entraîne une perte définitive de 22% du panier moyen.",
        "key_metrics": ["taux de rupture en rayon (OOS)", "rendement au mètre linéaire (€/m)", "rotation des stocks", "marge brute par famille de produits"],
        "thinking_phrases": [
            "Pendant que j'interroge les tickets de caisse et les niveaux de stock en linéaire...",
            "Regardons les produits générant les plus fortes marges par mètre carré de rayon...",
            "Nos modèles merchandising identifient les références à risque de rupture imminente...",
            "J'analyse l'élasticité prix et la rotation des gammes en point de vente..."
        ],
        "scenario_intros": [
            "Bienvenue sur ShelfOptimizer. Nous maximisons la rentabilité des rayons et prévenons les ruptures de stock en grande distribution.",
            "Regardons de plus près l'agencement des linéaires et le chiffre d'affaires au mètre carré avec ShelfOptimizer.",
            "Nous voici dans le retail. Nous pouvons auditer les taux de rupture du week-end ou optimiser la marge des têtes de gondole."
        ],
        "keywords": ["retail", "rayon", "stock", "magasin", "merchandising", "rupture", "chiffre", "vente", "facing", "linéaire", "produit", "grande distribution"]
    },
    "helios_agent": {
        "name": "Helios",
        "sector": "Énergie & Bornes IRVE Enedis",
        "dataset": "ev_charging_network_ds",
        "mission": "Supervision de la disponibilité des bornes de recharge pour véhicules électriques et gestion des pics de charge réseau.",
        "anecdote": "Le taux d'utilisation d'une borne ultra-rapide (>150kW) sur autoroute est multiplié par 6 les jours de chassé-croisé des vacances.",
        "key_metrics": ["taux de disponibilité opérationnelle (%)", "puissance délivrée en pic (MWh)", "temps moyen de recharge", "taux de rotation par point de charge"],
        "thinking_phrases": [
            "Pendant que je consulte la télémétrie des bornes de recharge et la charge Enedis...",
            "Regardons la disponibilité des stations de recharge ultra-rapide sur les axes autoroutiers...",
            "Nos modèles énergétiques analysent la courbe de puissance injectée lors des heures de pointe...",
            "J'évalue le taux de panne et les besoins de renforcement réseau par département..."
        ],
        "scenario_intros": [
            "Bienvenue sur Helios. Nous supervisons le maillage des bornes de recharge électrique et la stabilité du réseau énergétique.",
            "Regardons de plus près la disponibilité des infrastructures IRVE et la consommation électrique avec Helios.",
            "Nous voici sur la transition énergétique. Nous pouvons surveiller les pics de charge autoroutiers ou la fiabilité des bornes."
        ],
        "keywords": ["borne", "irve", "énergie", "recharge", "électrique", "enedis", "kw", "voiture", "batterie", "puissance", "mwh", "station"]
    },
    "juris_pilot_agent": {
        "name": "JurisPilot",
        "sector": "Juridique, Contrats & DORA",
        "dataset": "legal_contracts_ds",
        "mission": "Audit de conformité réglementaire RGPD/DORA, détection des clauses à risque et anticipation des échéances de renouvellement.",
        "anecdote": "Plus de 45% des pénalités contractuelles B2B résultent d'une reconduction tacite non anticipée 90 jours avant l'échéance.",
        "key_metrics": ["score de conformité réglementaire (0-100%)", "clauses léonines détectées", "volume d'engagements financiers échus", "délai moyen de revue contractuelle"],
        "thinking_phrases": [
            "Pendant que j'audite la base de contrats et les exigences de la directive DORA...",
            "Regardons les contrats fournisseurs comportant des clauses d'indemnisation à risque...",
            "Nos algorithmes juridiques scannent les dates de préavis pour éviter les reconductions tacites...",
            "J'analyse le niveau de conformité RGPD et les garanties de sécurité des prestataires tiers..."
        ],
        "scenario_intros": [
            "Bienvenue sur JurisPilot. Nous sécurisons les engagements juridiques et auditons la conformité réglementaire DORA et RGPD.",
            "Regardons de plus près la gestion des risques contractuels et les échéances critiques avec JurisPilot.",
            "Nous voici sur l'audit juridique. Nous pouvons détecter les clauses pénales abusives ou cartographier les contrats à renouveler."
        ],
        "keywords": ["contrat", "juridique", "rgpd", "dora", "conformité", "clause", "avocat", "litige", "audit", "échéance", "pénalité", "fournisseur"]
    }
}

HOST_SYSTEM_INSTRUCTION = """
RÈGLES D'OR DU PRÉSENTATEUR ET COMMENTATEUR DE DONNÉES EN DIRECT :

1. POSTURE DU COMMENTATEUR EXPERT (SYNTHÈSE ET IMPACT) :
   - Tu n'es PAS un lecteur de texte ni une machine qui énumère des listes : tu es un **analyste d'affaires d'élite et commentateur en direct**.
   - Ne lis JAMAIS les tableaux ligne par ligne ni les colonnes brutes : ils sont DÉJÀ affichés visuellement sous les yeux de l'utilisateur.
   - Ton rôle vocal est de **commenter l'observation majeure** en 2 ou 3 phrases percutantes :
     1. Le fait marquant ou la tendance générale.
     2. Le chiffre ou l'anomalie la plus critique (ex: "Les anesthésistes concentrent 62% des surcoûts d'intérim").
     3. Une conclusion concise invitant l'interlocuteur à regarder les détails à l'écran (ex: "Tous les détails sont dans le tableau à l'écran. Souhaitez-vous explorer les pistes d'optimisation ?").

2. ADAPTATION AU NIVEAU DE L'INTERLOCUTEUR :
   - Adapte immédiatement ton vocabulaire et ta profondeur d'analyse à l'interlocuteur :
     - Profil Dirigeant / Décideur : Focalise-toi sur le ROI, la marge, les risques et l'impact stratégique.
     - Profil Métier / Analyste : Précise les seuils, les départements et les volumes.
   - Utilise un français chaleureux, fluide, naturel et sans jargon technique ou SQL.

3. DÉCOUVERTE ET NAVIGATION PROACTIVE :
   - Quand l'utilisateur choisit un secteur ou un agent, présente-le brièvement avec son anecdote clé (1 phrase de mise en contexte) et demande-lui ce qu'il souhaite explorer.
   - Ne monopolise jamais la parole : chaque intervention vocale doit être rythmée, fluide et durer moins de 20 secondes.

4. ZÉRO LATENCE ET TRANSITION VERBALE :
   - Pendant le temps de calcul BigQuery, annonce simplement la démarche en une phrase vivante et diversifiée : "Je consulte nos données d'historique...".
   - Dès que le tableau s'affiche, enchaîne directement avec le commentaire synthétique.

5. INTERRUPTIBILITÉ ET ÉCOUTE ACTIVE :
   - Si l'utilisateur pose une question ou change de cap, cède immédiatement la parole avec bienveillance : "Absolument !", "Regardons cela immédiatement !".
"""

def format_clean_table(rows: List[Dict[str, Any]]) -> str:
    """Converts a raw JSON result array from BigQuery into a clean Markdown table."""
    if not rows or not isinstance(rows, list):
        return ""

    # Filter internal technical fields
    headers = [k for k in rows[0].keys() if k != "quicklook_image_url"]
    if not headers:
        return ""

    md = "| " + " | ".join([h.replace('_', ' ').title() for h in headers]) + " |\n"
    md += "| " + " | ".join(["---" for _ in headers]) + " |\n"

    for r in rows[:10]:
        vals = [str(r.get(h, "")) for h in headers]
        md += "| " + " | ".join(vals) + " |\n"

    return md

class ADKHostAgent:
    def __init__(self):
        self.system_instruction = HOST_SYSTEM_INSTRUCTION
        self.knowledge_base = AGENT_KNOWLEDGE_BASE

    def identify_voice_command(self, prompt: str) -> Dict[str, Any]:
        """
        Analyzes voice input to detect:
        1. Global overview questions (What can you do? What datasets do you have?)
        2. Explicit agent discovery or switch commands
        3. Domain-specific data queries
        """
        prompt_lower = prompt.lower().strip()

        # Check for Global Platform Overview queries
        global_triggers = [
            "que sais-tu faire", "que peux-tu faire", "quelles sont les données",
            "quelles données", "présente la plateforme", "présente tous les agents",
            "quels sont les agents", "tour d'horizon", "de quoi tu disposes",
            "qu'est-ce que tu connais", "vue d'ensemble", "quels secteurs"
        ]
        if any(trigger in prompt_lower for trigger in global_triggers):
            return {"action": "global_overview"}

        # Check for explicit agent discovery or switch command
        for agent_key, profile in self.knowledge_base.items():
            if profile["name"].lower() in prompt_lower or any(kw in prompt_lower for kw in profile["keywords"]):
                if any(w in prompt_lower for w in ["qui est", "présente", "explique", "découvrir", "rôle", "c'est quoi"]):
                    return {
                        "action": "discover_agent",
                        "agent_key": agent_key,
                        "profile": profile
                    }
                elif any(w in prompt_lower for w in ["passe sur", "connecte", "ouvre", "va sur", "change pour", "sélectionne"]):
                    return {
                        "action": "switch_agent",
                        "agent_key": agent_key,
                        "profile": profile
                    }

        # Default query intent matching based on keyword scoring
        best_agent = "sully_agent"
        best_score = 0
        for agent_key, profile in self.knowledge_base.items():
            score = sum(1 for kw in profile["keywords"] if kw in prompt_lower)
            if score > best_score:
                best_score = score
                best_agent = agent_key

        return {
            "action": "query_data",
            "agent_key": best_agent,
            "profile": self.knowledge_base[best_agent]
        }

    def process_raw_vertex_response(self, raw_text: str, profile: Dict[str, Any]) -> Generator[str, None, None]:
        """
        Parses raw Vertex AI Conversational Analytics JSON response into clean Markdown
        tables, thoughts, texts, and follow-up suggestions.
        """
        if not raw_text:
            yield f"data: {json.dumps({'type': 'content', 'content': 'Analyse BigQuery complétée avec succès.'})}\n\n"
            return

        clean_parts = []
        extracted_images = []
        found_data = False

        try:
            parsed = json.loads(raw_text)
            items = parsed if isinstance(parsed, list) else [parsed]
            
            for item in items:
                if not isinstance(item, dict):
                    continue
                
                # Check system message
                sys_msg = item.get("systemMessage", item)
                data_obj = sys_msg.get("data", {})
                text_obj = sys_msg.get("text", {})
                text_type = text_obj.get("textType", "")

                # 1. Thoughts
                if text_type == "THOUGHT":
                    parts = text_obj.get("parts", [])
                    t_str = "\n".join(parts) if isinstance(parts, list) else str(parts)
                    yield f"data: {json.dumps({'type': 'thought', 'content': t_str})}\n\n"

                # 2. Final Response Text
                elif text_type == "FINAL_RESPONSE":
                    parts = text_obj.get("parts", [])
                    if parts and isinstance(parts, list):
                        clean_parts.append("\n".join(parts))
                    elif text_obj.get("text"):
                        clean_parts.append(text_obj.get("text"))

                # 3. Followup Questions
                elif text_type == "FOLLOWUP_QUESTIONS":
                    parts = text_obj.get("parts", [])
                    if parts and isinstance(parts, list):
                        q_md = "\n\n**Suggestions d'analyses complémentaires :**\n" + "\n".join([f"- {p}" for p in parts])
                        clean_parts.append(q_md)

                # 4. Result Data (Tables & Images)
                if "result" in data_obj:
                    rows = data_obj["result"].get("data", [])
                    if rows and isinstance(rows, list):
                        found_data = True
                        table_md = format_clean_table(rows)
                        if table_md:
                            clean_parts.append(f"\n\n### 📊 Synthèse Décisionnelle des Données\n\n{table_md}")
                        
                        # Extract Sentinel-2 images if present
                        for r in rows:
                            img = r.get("quicklook_image_url")
                            if img and img not in extracted_images:
                                extracted_images.append(img)

                # 5. Generated SQL
                if "generatedSql" in data_obj:
                    sql_text = data_obj["generatedSql"]
                    yield f"data: {json.dumps({'type': 'thought', 'content': f'SQL BigQuery exécuté: {sql_text}'})}\n\n"

        except Exception:
            clean_parts.append(raw_text)

        # Append Sentinel-2 images if present
        if extracted_images:
            clean_parts.append("\n\n### 📡 Clichés Satellites Sentinel-2 Associés\n")
            for img in extracted_images[:2]:
                clean_parts.append(f"![Sentinel-2 Satellite Image]({img})\n")

        final_content = "\n\n".join(clean_parts).strip()
        if not final_content:
            final_content = f"Les indicateurs clés pour {profile['name']} ont été actualisés d'après les dernières données BigQuery."

        yield f"data: {json.dumps({'type': 'content', 'content': final_content})}\n\n"

    def generate_chat_stream(
        self,
        prompt: str,
        target_agent_id: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Generator[str, None, None]:
        """
        Processes voice/text through the Master Host Agent applying the rich knowledge framework.
        Emits rich Global Overview, Discovery, Dynamic Storytelling, and Data synthesis events.
        """
        command = self.identify_voice_command(prompt)

        # Case 1: Global Platform Overview
        if command["action"] == "global_overview":
            overview_text = "### 🌐 Tour d'Horizon des 11 Pôles de Données Talk to Data\n\n"
            overview_text += "Je suis votre hôte et maître de cérémonie, connecté en direct à **11 agents sectoriels BigQuery** sur Google Cloud :\n\n"
            for _, p in self.knowledge_base.items():
                overview_text += f"- **{p['name']}** ({p['sector']}) : {p['mission']}\n"
            overview_text += "\n💡 *Vous pouvez me poser vos questions à la voix ou sélectionner un secteur pour lancer une analyse approfondie.*"

            yield f"data: {json.dumps({'type': 'thought', 'content': 'Présentation globale de l’écosystème Talk to Data'})}\n\n"
            yield f"data: {json.dumps({'type': 'content', 'content': overview_text})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return

        profile = command["profile"]
        agent_key = command["agent_key"]

        # Case 2: Voice Discovery Request
        if command["action"] == "discover_agent":
            intro = random.choice(profile["scenario_intros"])
            discovery_text = f"### 🌟 {profile['name']} — {profile['sector']}\n\n"
            discovery_text += f"**Mission Stratégique :** {profile['mission']}\n\n"
            discovery_text += f"**Jeu de Données BigQuery :** `{profile['dataset']}`\n\n"
            discovery_text += f"💡 *Le fait marquant :* {profile['anecdote']}\n\n"
            discovery_text += f"**Indicateurs clés surveillés :** {', '.join(profile['key_metrics'])}.\n\n"
            discovery_text += f"**Exemples de questions à poser :**\n"
            discovery_text += f"- *\"Quels sont les indicateurs clés pour {profile['name']} ?\"*\n"
            discovery_text += f"- *\"Quelles sont les anomalies détectées récemment ?\"*"

            yield f"data: {json.dumps({'type': 'thought', 'content': intro})}\n\n"
            yield f"data: {json.dumps({'type': 'content', 'content': discovery_text})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return

        # Case 3: Voice Switch Agent Command
        elif command["action"] == "switch_agent":
            intro = random.choice(profile["scenario_intros"])
            switch_text = f"🔄 **{intro}**\n\n"
            switch_text += f"{profile['mission']}\n\n"
            switch_text += f"*{profile['anecdote']}*\n\n"
            switch_text += f"Les indicateurs sous surveillance sont : **{', '.join(profile['key_metrics'])}**.\n\n"
            switch_text += "Quelle question ou analyse souhaitez-vous lancer ?"

            yield f"data: {json.dumps({'type': 'thought', 'content': f'Bascule vers {profile['name']}'})}\n\n"
            yield f"data: {json.dumps({'type': 'switch_agent', 'agent_id': agent_key, 'agent_name': profile['name']})}\n\n"
            yield f"data: {json.dumps({'type': 'content', 'content': switch_text})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return

        # Case 4: Data Analytics Query with Dynamic Thinking Phrase
        dynamic_thinking = random.choice(profile["thinking_phrases"])
        yield f"data: {json.dumps({'type': 'thought', 'content': dynamic_thinking})}\n\n"

        # Invoke MCP Tool
        tool_result = toolbox_client.call_tool(agent_key, {"prompt": prompt})

        if tool_result.get("isError"):
            error_msg = tool_result.get("content", [{}])[0].get("text", "Erreur lors de l'exécution de l'outil.")
            yield f"data: {json.dumps({'type': 'error', 'content': error_msg})}\n\n"
        else:
            raw_content = tool_result.get("content", [{}])[0].get("text", "")
            for event in self.process_raw_vertex_response(raw_content, profile):
                yield event

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

# Singleton instance
host_orchestrator = ADKHostAgent()
