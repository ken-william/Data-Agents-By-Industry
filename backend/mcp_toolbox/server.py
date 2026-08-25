#!/usr/bin/env python3
"""
MCP Toolbox Server for BigQuery Conversational Analytics Data Agents.
Official MCP Toolbox Integration: https://mcp-toolbox.dev/integrations/bigquery/tools/bigquery-conversational-analytics/

Exposes the 11 already-deployed GCP Vertex AI Data Agents as standard Model Context Protocol (MCP) tools.
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

class MCPToolboxServer:
    def __init__(self, config_path: str = CONFIG_PATH):
        self.config_path = config_path
        self.tools_config = self._load_config()
        self._cached_token = None

    def _load_config(self) -> Dict[str, Any]:
        if HAS_YAML and os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                logger.warning(f"Failed to parse {self.config_path} with yaml: {e}")
        return {}

    def get_access_token(self) -> str:
        """Retrieves Google Cloud access token via ADC or gcloud auth."""
        try:
            token = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip()
            return token
        except Exception as e:
            logger.warning(f"Failed to fetch gcloud access token: {e}")
            return ""

    def list_tools(self) -> List[Dict[str, Any]]:
        """Returns all 11 BigQuery Conversational Analytics Data Agent tools."""
        tools = []
        for tool_name, tool_data in self.tools_config.get("tools", {}).items():
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
        Executes a BigQuery Conversational Analytics Tool by querying the existing deployed
        GCP Vertex AI Data Agent (projects/data-agents-by-industry/locations/global/dataAgents/...).
        """
        arguments = arguments or {}
        prompt = arguments.get("prompt", "")
        tool_data = self.tools_config.get("tools", {}).get(tool_name)
        
        if not tool_data:
            return {
                "isError": True,
                "content": [{"type": "text", "text": f"Tool '{tool_name}' not found in MCP Toolbox."}]
            }

        agent_id = tool_data.get("agent_id")
        if not agent_id:
            return {
                "isError": True,
                "content": [{"type": "text", "text": f"Agent ID not configured for tool '{tool_name}'."}]
            }

        token = self.get_access_token()
        if not token:
            return {
                "isError": True,
                "content": [{"type": "text", "text": "Google Cloud Authentication Error: Unable to retrieve access token."}]
            }

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
            
            if response.status_code != 200:
                return {
                    "isError": True,
                    "content": [{"type": "text", "text": f"Vertex AI API Error ({response.status_code}): {response.text}"}]
                }

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
        except Exception as e:
            logger.error(f"Error querying agent {agent_id}: {str(e)}")
            return {
                "isError": True,
                "content": [{"type": "text", "text": f"Agent Execution Error: {str(e)}"}]
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
