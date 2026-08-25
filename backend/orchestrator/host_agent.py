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

# Rich Agent Discovery Profiles (Mission, Datasets, Value Proposition & Key Questions)
AGENT_DISCOVERY_PROFILES = {
    "arena_manager_agent": {
        "name": "ArenaManager",
        "sector": "Sport, Stades & Grandes Infrastructures",
        "dataset": "arena_manager_ds",
        "mission": "Optimisation des revenus VIP, billetterie dynamique et gestion des flux de supporters dans les arènes et stades européens.",
        "anecdote": "Saviez-vous que les loges VIP représentent moins de 8% des sièges d'un stade mais génèrent plus de 42% de la marge brute d'un grand événement ?",
        "keywords": ["stade", "arena", "sport", "vip", "billetterie", "foot", "match", "concession", "buvette", "spectateur"]
    },
    "sully_agent": {
        "name": "Sully",
        "sector": "Secteur Public, RH & Hôpitaux",
        "dataset": "public_sector_employment_ds",
        "mission": "Pilotage des tensions de recrutement hospitalier, réduction des coûts de vacance de postes et analyse des grilles indiciaires.",
        "anecdote": "Dans la fonction publique hospitalière, chaque poste de médecin ou infirmier vacant plus de 6 mois coûte en moyenne 850 euros par jour en intérim d'urgence.",
        "keywords": ["sully", "public", "rh", "hôpital", "recrutement", "emploi", "vacance", "infirmier", "médecin", "urssaf", "fonction publique"]
    },
    "earth_intel_agent": {
        "name": "EarthIntel",
        "sector": "Spatial, Climat & Imagerie Satellite",
        "dataset": "skywatch_aerospace_ds",
        "mission": "Surveillance chlorophyllienne par satellite Sentinel-2 (10m), détection du stress hydrique agricole (NDVI) et conformité CSRD zéro déforestation.",
        "anecdote": "La constellation spatiale européenne Sentinel-2 revisite chaque parcelle agricole de France tous les 5 jours avec 13 bandes spectrales haute résolution.",
        "keywords": ["spatial", "satellite", "earth", "intel", "ndvi", "végétation", "sentinel", "climat", "sécheresse", "imagerie", "parcelle"]
    },
    "credit_advisor_agent": {
        "name": "CreditAdvisor",
        "sector": "Banque, Finance & Risque B2B",
        "dataset": "credit_risk_scoring_ds",
        "mission": "Scoring prédictif de défaillance d'entreprises, provisionnement comptable IFRS 9 et maximisation du rendement ajusté du risque (RAROC).",
        "anecdote": "L'anticipation d'un défaut de paiement à 90 jours grâce au croisement des flux de trésorerie permet de récupérer 65% de créance supplémentaire.",
        "keywords": ["crédit", "banque", "finance", "fiben", "défaut", "risque", "ifrs9", "bilan", "trésorerie", "prêt"]
    },
    "cine_analyst_agent": {
        "name": "CineAnalyst",
        "sector": "Cinéma, Médias & Box-Office",
        "dataset": "cine_analyst_ds",
        "mission": "Prédiction des entrées en salles, rentabilité des investissements de coproduction CNC et calendrier optimal de sortie.",
        "anecdote": "Le premier week-end d'exploitation d'un film en France détermine historiquement 38% de son box-office global en salles.",
        "keywords": ["cinéma", "film", "box-office", "entrées", "cnc", "salle", "casting", "production", "roi", "streaming"]
    },
    "net_arch_agent": {
        "name": "NetArch",
        "sector": "Télécoms, Réseaux & ARCEP",
        "dataset": "telecom_network_arcep_ds",
        "mission": "Supervision de la couverture 5G, maintenance prédictive des antennes relais et réduction de l'attrition des forfaits B2B.",
        "anecdote": "Une hausse de température CPU anormale sur un pylône 5G permet de prédire une panne matérielle 72 heures avant toute coupure d'abonnés.",
        "keywords": ["télécom", "antenne", "5g", "fibre", "arcep", "pylône", "réseau", "forfait", "panne", "arpu"]
    },
    "transit_navigator_agent": {
        "name": "TransitNavigator",
        "sector": "Transports & Mobilité SNCF",
        "dataset": "sncf_gtfs_mobility_ds",
        "mission": "Analyse de la ponctualité ferroviaire TGV/TER, détection des nœuds d'engorgement et prévision des retards de correspondance.",
        "anecdote": "Sur le réseau ferré national, 70% des retards en cascade proviennent de seulement 12 nœuds d'aiguillage stratégiques.",
        "keywords": ["train", "sncf", "gare", "tgv", "ter", "retard", "ponctualité", "mobilité", "voyageur", "correspondance"]
    },
    "pulse_checker_agent": {
        "name": "PulseChecker",
        "sector": "Santé & Hôpitaux RPPS",
        "dataset": "health_care_france_ds",
        "mission": "Cartographie des déserts médicaux, temps d'attente par spécialité et démographie des praticiens RPPS.",
        "anecdote": "Pour certaines spécialités comme l'ophtalmologie ou la dermatologie, le délai moyen de rendez-vous varie d'un facteur 1 à 8 selon les départements.",
        "keywords": ["santé", "médecin", "désert", "rpps", "patient", "attente", "cabinet", "spécialiste", "soin"]
    },
    "shelf_optimizer_agent": {
        "name": "ShelfOptimizer",
        "sector": "Retail & Grande Distribution",
        "dataset": "retail_merchandising_ds",
        "mission": "Optimisation du facing en rayon, prévention des ruptures de stock critiques et maximisation de la marge linéaire.",
        "anecdote": "En grande distribution, un taux de rupture supérieur à 4% en rayon le samedi entraîne une perte définitive de 22% du panier moyen.",
        "keywords": ["retail", "rayon", "stock", "magasin", "merchandising", "rupture", "chiffre", "vente", "facing"]
    },
    "helios_agent": {
        "name": "Helios",
        "sector": "Énergie & Bornes IRVE Enedis",
        "dataset": "ev_charging_network_ds",
        "mission": "Supervision de la disponibilité des bornes de recharge pour véhicules électriques et gestion des pics de charge réseau.",
        "anecdote": "Le taux d'utilisation d'une borne ultra-rapide (>150kW) sur autoroute est multiplié par 6 les jours de chassé-croisé des vacances.",
        "keywords": ["borne", "irve", "énergie", "recharge", "électrique", "enedis", "kw", "voiture", "batterie", "puissance"]
    },
    "juris_pilot_agent": {
        "name": "JurisPilot",
        "sector": "Juridique, Contrats & DORA",
        "dataset": "legal_contracts_ds",
        "mission": "Audit de conformité réglementaire RGPD/DORA, détection des clauses à risque et anticipation des échéances de renouvellement.",
        "anecdote": "Plus de 45% des pénalités contractuelles B2B résultent d'une reconduction tacite non anticipée 90 jours avant l'échéance.",
        "keywords": ["contrat", "juridique", "rgpd", "dora", "conformité", "clause", "avocat", "litige", "audit", "échéance"]
    }
}

HOST_SYSTEM_INSTRUCTION = """
RÈGLES D'OR DE COMPORTEMENT ET DE PERSONNALITÉ :

1. POSTURE DU PRÉSENTATEUR D'ÉLITE (TON ET CADENCE) :
   - Ton style est chaleureux, captivant et hautement professionnel. Ne sois pas un robot qui liste des faits ; raconte une histoire.
   - Utilise des connecteurs logiques élégants : "Regardons de plus près...", "C'est fascinant car...", "Les chiffres nous révèlent une tendance claire...".
   - Tu interagis par défaut en français d'une élégance parfaite (sans anglicismes inutiles), mais tu adaptes instantanément ta langue si le participant s'adresse à toi dans une autre langue.

2. NAVIGATION ET DÉCOUVERTE 100% VOCALES :
   - L'utilisateur pilote tout à la voix. Quand il demande à découvrir ou basculer vers un agent (ex: Sully, CreditAdvisor), commence par célébrer ce choix : présente brièvement le secteur, sa mission stratégique et l'anecdote percutante associée pour éveiller sa curiosité.

3. STORYTELLING INTÉGRÉ DURANT LE CHARGEMENT (ZÉRO LATENCE PERÇUE) :
   - Lorsque tu lances une requête BigQuery sous le capot (ce qui prend 2 à 3 secondes), ne laisse aucun silence s'installer.
   - Profite de ce temps pour installer l'ambiance et raconter l'histoire du jeu de données en direct : "Pendant que je consulte nos tables BigQuery d'historique... Saviez-vous que [insérer l'anecdote de l'agent] ? C'est incroyable, et voici justement les résultats qui s'affichent à l'écran !"

4. LE FILTRE METIER STRICT (SPEECH SANITIZER) :
   - Tu es un traducteur de données. Tu ne lis JAMAIS de code SQL, de JSON brut, d'accolades, de tirets, ou d'abréviations techniques de colonnes à voix haute.
   - Si tu reçois "arpu_moyen_eur: 45.99", tu dis : "Le revenu moyen par utilisateur s'établit à près de 46 euros."
   - Si tu reçois "total_abonnes: 1500", tu dis : "Nous enregistrons un parc solide de 1 500 abonnés."

5. INTERRUPTIBILITÉ ET BIENVEILLANCE :
   - Si l'utilisateur t'interrompt pour changer de sujet, cède immédiatement la parole de manière élégante : "Très bien, changeons de cap !", "Excellente idée, explorons plutôt ce domaine !".
"""

class ADKHostAgent:
    def __init__(self):
        self.system_instruction = HOST_SYSTEM_INSTRUCTION
        self.discovery_profiles = AGENT_DISCOVERY_PROFILES

    def identify_voice_command(self, prompt: str) -> Dict[str, Any]:
        """
        Analyzes voice input to detect navigation, discovery requests, or data questions.
        Returns command type: 'switch_agent', 'discover_agent', or 'query_data'.
        """
        prompt_lower = prompt.lower().strip()

        # Check for explicit agent discovery or switch command
        for agent_key, profile in self.discovery_profiles.items():
            # Check agent name or keywords
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

        # Default query intent matching
        best_agent = "sully_agent"
        best_score = 0
        for agent_key, profile in self.discovery_profiles.items():
            score = sum(1 for kw in profile["keywords"] if kw in prompt_lower)
            if score > best_score:
                best_score = score
                best_agent = agent_key

        return {
            "action": "query_data",
            "agent_key": best_agent,
            "profile": self.discovery_profiles[best_agent]
        }

    def generate_chat_stream(
        self,
        prompt: str,
        target_agent_id: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Generator[str, None, None]:
        """
        Processes voice/text through the Master Host Agent applying the 5 Golden Rules.
        Emits rich Discovery, Storytelling, and Data synthesis events.
        """
        command = self.identify_voice_command(prompt)
        profile = command["profile"]
        agent_key = command["agent_key"]

        # Case 1: Voice Discovery Request (Règle d'or 2)
        if command["action"] == "discover_agent":
            discovery_text = f"### 🌟 Regardons de plus près : {profile['name']} ({profile['sector']})\n\n"
            discovery_text += f"**Mission Stratégique :** {profile['mission']}\n\n"
            discovery_text += f"**Jeu de Données BigQuery Connecté :** `{profile['dataset']}`\n\n"
            discovery_text += f"💡 *C'est fascinant car :* {profile['anecdote']}\n\n"
            discovery_text += "**Voici les questions clés que nous pouvons explorer ensemble :**\n"
            discovery_text += f"- *\"Présente-moi les indicateurs de performance pour {profile['name']}\"*\n"
            discovery_text += f"- *\"Quelles sont les anomalies majeures détectées ce trimestre ?\"*"

            yield f"data: {json.dumps({'type': 'thought', 'content': f'Discovery vocal de l’agent : {profile['name']}'})}\n\n"
            yield f"data: {json.dumps({'type': 'content', 'content': discovery_text})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return

        # Case 2: Voice Switch Agent Command (Règle d'or 2 & 5)
        elif command["action"] == "switch_agent":
            switch_text = f"🔄 **Excellente idée ! Connectons-nous immédiatement à {profile['name']}** ({profile['sector']}).\n\n"
            switch_text += f"{profile['mission']}\n\n"
            switch_text += f"*{profile['anecdote']}*\n\n"
            switch_text += "Je suis prêt ! Quelle analyse de données souhaitez-vous lancer ?"

            yield f"data: {json.dumps({'type': 'thought', 'content': f'Bascule vocale vers {profile['name']}'})}\n\n"
            yield f"data: {json.dumps({'type': 'switch_agent', 'agent_id': agent_key, 'agent_name': profile['name']})}\n\n"
            yield f"data: {json.dumps({'type': 'content', 'content': switch_text})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return

        # Case 3: Data Analytics Query with Storytelling (Règle d'or 1, 3, 4)
        # 1. Yield Active Storytelling Thought to eliminate perceived latency
        storytelling_phrase = f"Pendant que je consulte nos tables BigQuery d'historique... Saviez-vous que {profile['anecdote'].lower()} C'est fascinant, et voici justement les chiffres qui s'affichent à l'écran !"
        yield f"data: {json.dumps({'type': 'thought', 'content': storytelling_phrase})}\n\n"

        # 2. Invoke MCP Tool
        tool_result = toolbox_client.call_tool(agent_key, {"prompt": prompt})

        if tool_result.get("isError"):
            error_msg = tool_result.get("content", [{}])[0].get("text", "Erreur lors de l'exécution de l'outil.")
            yield f"data: {json.dumps({'type': 'error', 'content': error_msg})}\n\n"
        else:
            raw_content = tool_result.get("content", [{}])[0].get("text", "")
            yield f"data: {json.dumps({'type': 'content', 'content': raw_content})}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

# Singleton instance
host_orchestrator = ADKHostAgent()
