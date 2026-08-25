"""
Google ADK Agent Definition for Master Host Orchestrator.
Directly compatible with `adk web` CLI and Google Agent Engine.
"""

import os

# Use Google AI Studio if GEMINI_API_KEY is provided, else use Vertex AI
if os.environ.get("GEMINI_API_KEY"):
    os.environ.pop("GOOGLE_GENAI_USE_VERTEXAI", None)
else:
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "1"
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
    os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")

from google.adk import Agent
from .host_agent import HOST_SYSTEM_INSTRUCTION
try:
    from mcp_toolbox.toolbox_client import toolbox_client
except ImportError:
    from backend.mcp_toolbox.toolbox_client import toolbox_client

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
LOCATION = "global"

# Define Python tool wrapper functions for ADK
def query_bigquery_data_agent(agent_name: str, prompt: str) -> str:
    """
    Invoque un des 11 Data Agents BigQuery (sully_agent, arena_manager_agent, credit_advisor_agent, earth_intel_agent, etc.)
    via le protocole MCP Toolbox pour récupérer les données d'affaires en direct.
    
    Args:
        agent_name: Le nom de l'agent sectoriel (ex: 'sully_agent', 'arena_manager_agent', 'credit_advisor_agent', etc.)
        prompt: La question d'analyse métier à poser.
    """
    result = toolbox_client.call_tool(agent_name, {"prompt": prompt})
    return result.get("content", [{}])[0].get("text", "Analyse BigQuery complétée.")

# Official Google ADK Root Agent
agent = Agent(
    name="talktodata_host_orchestrator",
    description="Agent Hôte et Maître de Cérémonie Talk to Data connecté à la flotte de 11 Data Agents BigQuery via MCP Toolbox.",
    model="gemini-3-flash-preview",
    instruction=HOST_SYSTEM_INSTRUCTION,
    tools=[query_bigquery_data_agent]
)

root_agent = agent
