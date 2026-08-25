"""
Google ADK Central Orchestrator Agent (Master Host / Presenter).
Tier 2 of Talk to Data Architecture.

This agent acts as the universal conversational host. It interacts naturally with users,
narrates data storytelling, and dynamically routes business questions to any connected
specialized BigQuery Data Agent exposed via MCP Toolbox.
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
Ton rôle est d'accompagner l'utilisateur, de comprendre ses besoins d'analyse métier et de converser avec lui avec fluidité et élégance.

Tes capacités fondamentales :
1. COMPAGNIE & STORYTELLING : Présente le contexte des données et meuble l'attente avec une narration captivante pendant les calculs.
2. ROUTAGE DYNAMIQUE UNIVERSEL : Tu découvres et te connectes dynamiquement à tous les Data Agents sectoriels disponibles via MCP Toolbox.
3. APPELS D'OUTILS SÉCURISÉS : Invoque automatiquement les outils MCP spécialisés pour interroger les données BigQuery réelles.
4. SYNTHÈSE VOCALE & ÉPURÉE : Ne transmets JAMAIS de code SQL brut, d'identifiants techniques ou de JSON non formaté. Traduis toujours les métriques en une synthèse d'affaires claire, structurée et prête pour la prise de décision.
"""

class ADKHostAgent:
    def __init__(self):
        self.system_instruction = HOST_SYSTEM_INSTRUCTION
        self.tools = toolbox_client.get_adk_function_declarations()
        logger.info(f"ADK Host Agent dynamically connected to {len(self.tools)} MCP Toolbox tools.")

    def list_available_agents_summary(self) -> List[Dict[str, Any]]:
        """Returns the dynamic catalog of all connected Data Agents and their capabilities."""
        return toolbox_client.get_tool_definitions()

    def route_and_execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the targeted MCP tool and returns clean structured data."""
        logger.info(f"ADK Orchestrator invoking MCP Tool: {tool_name}")
        return toolbox_client.call_tool(tool_name, arguments)

    def find_best_matching_tool(self, prompt: str, target_agent_id: Optional[str] = None) -> Optional[str]:
        """Dynamically matches user intent against all available MCP tool definitions."""
        available_tools = toolbox_client.get_tool_definitions()
        if not available_tools:
            return None

        # Direct match if target_agent_id provided
        if target_agent_id:
            for tool in available_tools:
                if target_agent_id in tool["name"] or tool.get("agentId") == target_agent_id:
                    return tool["name"]

        prompt_lower = prompt.lower()
        
        # Dynamic score matching based on tool name and description keywords
        best_tool = available_tools[0]["name"]
        best_score = 0

        for tool in available_tools:
            score = 0
            name_tokens = tool["name"].lower().replace("_", " ").split()
            desc_tokens = tool.get("description", "").lower().split()
            
            for token in name_tokens + desc_tokens:
                if len(token) > 3 and token in prompt_lower:
                    score += 1

            if score > best_score:
                best_score = score
                best_tool = tool["name"]

        return best_tool

    def generate_chat_stream(
        self,
        prompt: str,
        target_agent_id: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Generator[str, None, None]:
        """
        Processes a user prompt through the ADK Orchestrator and yields SSE streaming events.
        Dynamically executes MCP Toolbox tools and synthesizes results.
        """
        conversation_history = conversation_history or []
        
        matched_tool = self.find_best_matching_tool(prompt, target_agent_id)
        if not matched_tool:
            yield f"data: {json.dumps({'type': 'error', 'content': 'Aucun outil MCP disponible dans le catalogue.'})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return

        # 1. Yield storytelling & routing thought event
        yield f"data: {json.dumps({'type': 'thought', 'content': f'Routage intelligent ADK vers l’outil MCP : {matched_tool}'})}\n\n"

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
