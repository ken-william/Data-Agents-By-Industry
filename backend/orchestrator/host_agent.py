"""
Google ADK Central Orchestrator Agent (Master Host / Presenter).
Tier 2 of Talk to Data Architecture.

This agent acts as the universal conversational host. It interacts naturally with users,
narrates data storytelling, and automatically routes business questions to the appropriate
specialized BigQuery Data Agents exposed via MCP Toolbox.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional, Generator
from ..mcp_toolbox.toolbox_client import toolbox_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("adk_orchestrator")

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
LOCATION = "global"

HOST_SYSTEM_INSTRUCTION = """
Tu es l'Agent Hôte Virtuel et Maître de Cérémonie de la plateforme décisionnelle Talk to Data.
Ton rôle est d'accueillir chaleureusement les dirigeants et utilisateurs en français.

Tes missions :
1. COMPAGNIE & STORYTELLING : Présente le jeu de données avec élégance et pédagogie.
2. ROUTAGE AUTOMATIQUE : Tu as accès à 11 outils spécialisés via MCP Toolbox (Sully pour l'emploi public/RH, ArenaManager pour les stades, EarthIntel pour l'imagerie satellite, CineAnalyst pour le box-office, CreditAdvisor pour la finance, etc.).
3. APPELS D'OUTILS : Lorsque l'utilisateur pose une question métier, utilise l'outil MCP correspondant pour interroger les données BigQuery réelles.
4. SANITISATION & PRÉSENTATION : Ne lis JAMAIS de code SQL brut, d'identifiants de projets GCP ou de JSON complexe à voix haute. Traduis toujours les résultats en synthèse d'affaires claire, structurée et percutante (tableaux Markdown et points clés).
"""

class ADKHostAgent:
    def __init__(self):
        self.system_instruction = HOST_SYSTEM_INSTRUCTION
        self.tools = toolbox_client.get_adk_function_declarations()
        logger.info(f"ADK Host Agent initialized with {len(self.tools)} MCP Toolbox tools.")

    def list_available_agents_summary(self) -> List[Dict[str, Any]]:
        """Returns a user-friendly overview of all 11 connected Data Agents."""
        return toolbox_client.get_tool_definitions()

    def route_and_execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the selected MCP tool and returns clean structured data."""
        logger.info(f"ADK Orchestrator invoking MCP Tool: {tool_name}")
        return toolbox_client.call_tool(tool_name, arguments)

    def generate_chat_stream(
        self,
        prompt: str,
        target_agent_id: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Generator[str, None, None]:
        """
        Processes a user prompt through the ADK Orchestrator and yields SSE streaming events.
        Automatically executes MCP Toolbox tools and synthesizes results.
        """
        conversation_history = conversation_history or []
        
        # Determine matching tool
        matched_tool = None
        if target_agent_id:
            # Direct mapping from agent ID to MCP tool name
            for tool in self.tools:
                if target_agent_id in tool["name"] or tool.get("agentId") == target_agent_id:
                    matched_tool = tool["name"]
                    break

        # If no explicit agent specified, find best tool match by keyword analysis
        if not matched_tool:
            prompt_lower = prompt.lower()
            if any(k in prompt_lower for k in ["stade", "arena", "vip", "match", "billetterie"]):
                matched_tool = "arena_manager_agent"
            elif any(k in prompt_lower for k in ["satellite", "ndvi", "végétation", "sentinel"]):
                matched_tool = "earth_intel_agent"
            elif any(k in prompt_lower for k in ["cinéma", "film", "box-office", "entrées"]):
                matched_tool = "cine_analyst_agent"
            elif any(k in prompt_lower for k in ["crédit", "banque", "défaut", "risque", "exposition"]):
                matched_tool = "credit_advisor_agent"
            elif any(k in prompt_lower for k in ["train", "sncf", "retard", "ponctualité", "tgv"]):
                matched_tool = "transit_navigator_agent"
            elif any(k in prompt_lower for k in ["santé", "hôpital", "rpps", "médecin", "désert"]):
                matched_tool = "pulse_checker_agent"
            elif any(k in prompt_lower for k in ["rayon", "stock", "rupture", "merchandising"]):
                matched_tool = "shelf_optimizer_agent"
            elif any(k in prompt_lower for k in ["borne", "irve", "recharge", "enedis", "électrique"]):
                matched_tool = "helios_agent"
            elif any(k in prompt_lower for k in ["contrat", "juridique", "rgpd", "dora", "conformité"]):
                matched_tool = "juris_pilot_agent"
            elif any(k in prompt_lower for k in ["5g", "arcep", "pylône", "fibre", "télécom"]):
                matched_tool = "net_arch_agent"
            else:
                matched_tool = "sully_agent"

        # 1. Yield storytelling & thought event
        yield f"data: {json.dumps({'type': 'thought', 'content': f'Routage ADK vers l’outil MCP : {matched_tool}'})}\n\n"

        # 2. Invoke MCP Tool
        tool_result = self.route_and_execute_tool(matched_tool, {"prompt": prompt})

        if tool_result.get("isError"):
            error_msg = tool_result.get("content", [{}])[0].get("text", "Erreur lors de l'exécution de l'outil.")
            yield f"data: {json.dumps({'type': 'error', 'content': error_msg})}\n\n"
        else:
            raw_content = tool_result.get("content", [{}])[0].get("text", "")
            yield f"data: {json.dumps({'type': 'content', 'content': raw_content})}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

# Singleton instance
host_orchestrator = ADKHostAgent()
