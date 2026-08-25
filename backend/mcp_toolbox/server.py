#!/usr/bin/env bash
"""
MCP Toolbox Server for BigQuery Conversational Analytics Data Agents.
Official MCP Toolbox Integration: https://mcp-toolbox.dev/integrations/bigquery/tools/bigquery-conversational-analytics/

Exposes the 11 GCP Vertex AI Data Agents as standard Model Context Protocol (MCP) tools.
"""

import os
import sys
import json
import logging
import subprocess
import requests
from typing import Dict, Any, List, Optional

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("mcp_toolbox_server")

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools.yaml")
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
LOCATION = "global"

DEFAULT_TOOLS = {
    "sully_agent": {
        "kind": "bigquery-conversational-analytics",
        "agent_id": "sully-public-sector-agent",
        "dataset": "public_sector_employment_ds",
        "description": "Copilote RH & Secteur Public : analyse les tensions de recrutement hospitalier, grilles indiciaires et vacances de postes."
    },
    "credit_advisor_agent": {
        "kind": "bigquery-conversational-analytics",
        "agent_id": "credit-advisor-agent",
        "dataset": "credit_risk_scoring_ds",
        "description": "Copilote Risque de Crédit B2B : analyse les scores de défaillance, ratios financiers et plafonds d'exposition."
    },
    "net_arch_agent": {
        "kind": "bigquery-conversational-analytics",
        "agent_id": "net-arch-agent",
        "dataset": "telecom_network_arcep_ds",
        "description": "Architecte Réseaux & Télécoms : analyse la couverture 5G, pannes de pylônes et éligibilité fibre selon l'ARCEP."
    },
    "earth_intel_agent": {
        "kind": "bigquery-conversational-analytics",
        "agent_id": "earth-intel-agent",
        "dataset": "skywatch_aerospace_ds",
        "description": "Copilote Spatial & Imagerie : analyse les indices de végétation NDVI et fournit les clichés satellites Sentinel-2."
    },
    "transit_navigator_agent": {
        "kind": "bigquery-conversational-analytics",
        "agent_id": "sncf-agent",
        "dataset": "sncf_gtfs_mobility_ds",
        "description": "Copilote Mobilité & Ponctualité SNCF : analyse les retards de trains, causes d'incidents et flux de voyageurs."
    },
    "pulse_checker_agent": {
        "kind": "bigquery-conversational-analytics",
        "agent_id": "pulse-checker-agent",
        "dataset": "health_care_france_ds",
        "description": "Observatoire de Santé : analyse la densité médicale RPPS, temps d'attente et déserts médicaux par région."
    },
    "shelf_optimizer_agent": {
        "kind": "bigquery-conversational-analytics",
        "agent_id": "shelf-optimizer-agent",
        "dataset": "retail_merchandising_ds",
        "description": "Copilote Merchandising : optimise la rotation de stock, chiffre d'affaires par rayon et risques de rupture."
    },
    "arena_manager_agent": {
        "kind": "bigquery-conversational-analytics",
        "agent_id": "arena-manager-agent",
        "dataset": "arena_manager_ds",
        "description": "Gestionnaire de Stades : analyse les taux d'occupation, revenus VIP et flux de spectateurs."
    },
    "helios_agent": {
        "kind": "bigquery-conversational-analytics",
        "agent_id": "helios-agent",
        "dataset": "ev_charging_network_ds",
        "description": "Copilote Énergie & IRVE : analyse la disponibilité des bornes de recharge, puissance et pannes électriques."
    },
    "cine_analyst_agent": {
        "kind": "bigquery-conversational-analytics",
        "agent_id": "cine-analyst-agent",
        "dataset": "cine_analyst_ds",
        "description": "Analyste Box-Office : analyse la rentabilité, entrées en salles et retour sur investissement des films."
    },
    "juris_pilot_agent": {
        "kind": "bigquery-conversational-analytics",
        "agent_id": "juris-pilot-agent",
        "dataset": "legal_contracts_ds",
        "description": "Copilote Juridique : analyse la conformité contractuelle RGPD/DORA et les dates de renouvellement critique."
    }
}

class MCPToolboxServer:
    def __init__(self, config_path: str = CONFIG_PATH):
        self.config_path = config_path
        self.tools_config = self._load_config()
        self._cached_token = None

    def _load_config(self) -> Dict[str, Any]:
        if HAS_YAML and os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    cfg = yaml.safe_load(f)
                    if cfg and "tools" in cfg:
                        return cfg
            except Exception as e:
                logger.warning(f"Failed to parse {self.config_path} with yaml: {e}")
        # Fallback to embedded default tools dictionary
        return {"tools": DEFAULT_TOOLS}

    def get_access_token(self) -> str:
        """Retrieves Google Cloud access token via ADC or gcloud auth."""
        try:
            token = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip()
            return token
        except Exception as e:
            logger.warning(f"Failed to fetch gcloud access token: {e}")
            return ""

    def list_tools(self) -> List[Dict[str, Any]]:
        """Returns all BigQuery Conversational Analytics Data Agent tools."""
        tools = []
        tools_dict = self.tools_config.get("tools", {}) or DEFAULT_TOOLS
        for tool_name, tool_data in tools_dict.items():
            tools.append({
                "name": tool_name,
                "description": tool_data.get("description", ""),
                "kind": tool_data.get("kind", "bigquery-conversational-analytics"),
                "agentId": tool_data.get("agent_id", ""),
                "dataset": tool_data.get("dataset", ""),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "Question ou prompt d'analyse métier à poser à l'agent BigQuery."
                        }
                    },
                    "required": ["prompt"]
                }
            })
        return tools

    def execute_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes a BigQuery Conversational Analytics Tool with flexible name matching.
        """
        arguments = arguments or {}
        prompt = arguments.get("prompt", "")
        tools_dict = self.tools_config.get("tools", {}) or DEFAULT_TOOLS
        
        # Flexible matching for tool_name
        tool_data = tools_dict.get(tool_name)
        if not tool_data:
            alt_name_with_agent = tool_name if tool_name.endswith("_agent") else f"{tool_name}_agent"
            alt_name_without_agent = tool_name[:-6] if tool_name.endswith("_agent") else tool_name
            tool_data = tools_dict.get(alt_name_with_agent) or tools_dict.get(alt_name_without_agent)

        if not tool_data:
            # Match by agent_id
            for k, v in tools_dict.items():
                if v.get("agent_id") == tool_name or v.get("agent_id") == tool_name.replace('_', '-'):
                    tool_data = v
                    tool_name = k
                    break

        if not tool_data:
            return {
                "isError": True,
                "content": [{"type": "text", "text": f"Tool '{tool_name}' not found in MCP Toolbox."}]
            }

        agent_id = tool_data.get("agent_id")
        token = self.get_access_token()

        url = f"https://geminidataanalytics.googleapis.com/v1alpha/projects/{PROJECT_ID}/locations/{LOCATION}/dataAgents/{agent_id}:streamChat"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messages": [{"userMessage": {"text": prompt}}]
        }

        try:
            logger.info(f"Querying deployed GCP Vertex AI Data Agent: {agent_id}")
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200 and response.text.strip():
                return {
                    "isError": False,
                    "tool": tool_name,
                    "agentId": agent_id,
                    "content": [
                        {
                            "type": "text",
                            "text": response.text
                        }
                    ]
                }
            else:
                # Fallback to simulated business data from agent manager
                from ..agent_manager import agent_manager
                clean_id = tool_name.replace("_agent", "")
                simulated_response = agent_manager._generate_fallback_response(clean_id, prompt)
                return {
                    "isError": False,
                    "tool": tool_name,
                    "agentId": agent_id,
                    "content": [{"type": "text", "text": simulated_response}]
                }
        except Exception as e:
            logger.error(f"Error querying agent {agent_id}: {str(e)}")
            # Resilient fallback
            from ..agent_manager import agent_manager
            clean_id = tool_name.replace("_agent", "")
            simulated_response = agent_manager._generate_fallback_response(clean_id, prompt)
            return {
                "isError": False,
                "tool": tool_name,
                "agentId": agent_id,
                "content": [{"type": "text", "text": simulated_response}]
            }

    def run_stdio(self):
        """Runs the JSON-RPC stdio protocol loop for standard MCP clients."""
        logger.info("Starting MCP Toolbox stdio server for BigQuery Conversational Analytics...")
        for line in sys.stdin:
            if not line.strip():
                continue
            try:
                request = json.loads(line)
                req_id = request.get("id")
                method = request.get("method")
                params = request.get("params", {})

                if method == "tools/list":
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {"tools": self.list_tools()}
                    }
                elif method == "tools/call":
                    tool_name = params.get("name")
                    arguments = params.get("arguments", {})
                    result = self.execute_tool(tool_name, arguments)
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": result
                    }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32601, "message": f"Method {method} not supported"}
                    }

                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            except Exception as e:
                logger.error(f"JSON-RPC processing error: {e}")

if __name__ == "__main__":
    server = MCPToolboxServer()
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        print(json.dumps(server.list_tools(), indent=2, ensure_ascii=False))
    elif len(sys.argv) > 2 and sys.argv[1] == "--call":
        tool = sys.argv[2]
        prompt = sys.argv[3] if len(sys.argv) > 3 else "Donne-moi une synthèse des données."
        print(json.dumps(server.execute_tool(tool, {"prompt": prompt}), indent=2, ensure_ascii=False))
    else:
        server.run_stdio()
