#!/usr/bin/env python3
"""
MCP Toolbox Server for BigQuery Data Agents.
Implements the Model Context Protocol (JSON-RPC) to expose declarative BigQuery tools
to Google ADK, Claude, Cursor, and any MCP-compliant AI Orchestrator.
"""

import os
import sys
import json
import logging
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

# Fallback default tools catalog if PyYAML is not installed
BUILTIN_TOOLS = {
    "sully_analyze_hospital_jobs": {
        "description": "Analyse les vacances de postes hospitaliers et tensions de recrutement dans le secteur public.",
        "statement": "SELECT establishment_name, job_category, region, vacancy_count, average_fill_delay_days FROM `data-agents-by-industry.public_sector_employment_ds.hospital_job_vacancies` ORDER BY vacancy_count DESC LIMIT 15"
    },
    "credit_advisor_evaluate_risk": {
        "description": "Évalue les scores de risque de crédit des entreprises et les montants d'exposition financière.",
        "statement": "SELECT company_siren, company_name, sector, risk_score, max_exposure_k_eur, default_probability FROM `data-agents-by-industry.credit_risk_scoring_ds.company_credit_scores` ORDER BY default_probability DESC LIMIT 15"
    },
    "net_arch_audit_coverage": {
        "description": "Audite la couverture 5G, la qualité de service mobile et le déploiement fibre selon les données ARCEP.",
        "statement": "SELECT operator_name, department_code, coverage_5g_percentage, fiber_eligibility_rate FROM `data-agents-by-industry.telecom_network_arcep_ds.network_coverage_summary` ORDER BY coverage_5g_percentage DESC LIMIT 15"
    },
    "earth_intel_query_ndvi_assets": {
        "description": "Analyse l'indice de végétation NDVI et récupère les clichés satellites Sentinel-2 récents.",
        "statement": "SELECT c.company_name, c.asset_name, c.city, c.region, c.ndvi_vegetation_index, s.acquisition_date, s.quicklook_image_url FROM `data-agents-by-industry.skywatch_aerospace_ds.company_assets` c INNER JOIN `data-agents-by-industry.skywatch_aerospace_ds.sentinel_2_index` s ON c.city = s.closest_city ORDER BY c.ndvi_vegetation_index ASC LIMIT 10"
    },
    "transit_navigator_punctuality_stats": {
        "description": "Fournit les taux de ponctualité des lignes TGV/TER et les causes majeures de retard.",
        "statement": "SELECT train_line, departure_station, arrival_station, punctuality_rate, avg_delay_minutes FROM `data-agents-by-industry.sncf_gtfs_mobility_ds.line_punctuality` ORDER BY avg_delay_minutes DESC LIMIT 15"
    },
    "pulse_checker_specialist_density": {
        "description": "Analyse la densité médicale par région et identifie les déserts médicaux par spécialité.",
        "statement": "SELECT region, specialty, practitioners_per_100k, avg_wait_time_days FROM `data-agents-by-industry.health_care_france_ds.medical_demography` ORDER BY practitioners_per_100k ASC LIMIT 15"
    },
    "shelf_optimizer_inventory_turnover": {
        "description": "Optimise la rotation des stocks, le taux de rupture et le chiffre d'affaires par rayon.",
        "statement": "SELECT department, category, turnover_rate, stockout_risk_score, revenue_eur FROM `data-agents-by-industry.retail_merchandising_ds.shelf_performance` ORDER BY stockout_risk_score DESC LIMIT 15"
    },
    "arena_manager_stadium_occupancy": {
        "description": "Pilote les taux d'occupation, les revenus VIP et la gestion des flux dans les stades.",
        "statement": "SELECT stadium_name, city, total_capacity, occupancy_rate, vip_lounge_revenue_k_eur FROM `data-agents-by-industry.arena_manager_ds.stadium_kpis` ORDER BY occupancy_rate DESC LIMIT 15"
    },
    "helios_charging_station_availability": {
        "description": "Analyse la disponibilité, la puissance installée et les pannes sur le réseau de bornes IRVE.",
        "statement": "SELECT operator, region, total_charging_points, available_points_rate, peak_utilization_kw FROM `data-agents-by-industry.ev_charging_network_ds.charging_stations_kpis` ORDER BY available_points_rate ASC LIMIT 15"
    },
    "cine_analyst_box_office_roi": {
        "description": "Analyse la rentabilité, les entrées au box-office et le retour sur investissement des productions cinéma.",
        "statement": "SELECT movie_title, genre, budget_m_eur, box_office_entries_m, roi_ratio FROM `data-agents-by-industry.cine_analyst_ds.box_office_performance` ORDER BY box_office_entries_m DESC LIMIT 15"
    },
    "juris_pilot_contract_compliance": {
        "description": "Évalue la conformité RGPD/DORA et les risques juridiques sur le portefeuille de contrats.",
        "statement": "SELECT contract_id, counterparty_name, compliance_score, risk_level, renewal_date FROM `data-agents-by-industry.legal_contracts_ds.contract_portfolio` ORDER BY risk_level DESC LIMIT 15"
    }
}

class MCPToolboxServer:
    def __init__(self, config_path: str = CONFIG_PATH):
        self.config_path = config_path
        self.tools_config = self._load_config()
        self._bq_client = None

    def _load_config(self) -> Dict[str, Any]:
        if HAS_YAML and os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) or {"tools": BUILTIN_TOOLS}
            except Exception as e:
                logger.warning(f"Failed to parse {self.config_path} with yaml: {e}")
        return {"tools": BUILTIN_TOOLS}

    def list_tools(self) -> List[Dict[str, Any]]:
        """Returns the list of all MCP tools defined in tools.yaml."""
        tools = []
        for tool_name, tool_data in self.tools_config.get("tools", {}).items():
            tools.append({
                "name": tool_name,
                "description": tool_data.get("description", ""),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        p.get("name"): {
                            "type": p.get("type", "string"),
                            "description": p.get("description", "")
                        } for p in tool_data.get("parameters", [])
                    },
                    "required": [p["name"] for p in tool_data.get("parameters", []) if p.get("required", False)]
                }
            })
        return tools

    def execute_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Executes a declared BigQuery SQL tool and returns structured results."""
        arguments = arguments or {}
        tool_data = self.tools_config.get("tools", {}).get(tool_name)
        if not tool_data:
            return {
                "isError": True,
                "content": [{"type": "text", "text": f"Tool '{tool_name}' not found in MCP Toolbox."}]
            }

        statement = tool_data.get("statement", "").strip()
        if not statement:
            return {
                "isError": True,
                "content": [{"type": "text", "text": f"Tool '{tool_name}' has no SQL statement configured."}]
            }

        try:
            logger.info(f"Executing MCP Tool: {tool_name}")
            # Lazy import bigquery
            from google.cloud import bigquery
            if self._bq_client is None:
                self._bq_client = bigquery.Client(project=PROJECT_ID)

            query_job = self._bq_client.query(statement)
            results = [dict(row) for row in query_job.result()]

            return {
                "isError": False,
                "tool": tool_name,
                "rowCount": len(results),
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(results, default=str, ensure_ascii=False)
                    }
                ]
            }
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return {
                "isError": True,
                "content": [{"type": "text", "text": f"BigQuery Execution Error: {str(e)}"}]
            }

    def run_stdio(self):
        """Runs the JSON-RPC stdio protocol loop for standard MCP clients."""
        logger.info("Starting MCP Toolbox stdio server...")
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
        print(json.dumps(server.execute_tool(tool), indent=2, ensure_ascii=False))
    else:
        server.run_stdio()
