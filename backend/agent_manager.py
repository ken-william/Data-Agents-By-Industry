import os
import json
import requests
import subprocess
from typing import Dict, List, Any, Optional

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
LOCATION = "global"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS_DIR = os.path.join(BASE_DIR, "agents")

# UI Theme Mapping per agent sector
AGENT_THEMES = {
    "sully": {
        "category": "Secteur Public & RH",
        "icon": "Briefcase",
        "color": "indigo",
        "gradient": "from-slate-900 via-indigo-950 to-slate-900",
        "cardBorder": "border-indigo-500/30",
        "accentBg": "bg-indigo-600",
        "accentText": "text-indigo-400",
        "badgeBg": "bg-indigo-500/10 text-indigo-300 border-indigo-500/20"
    },
    "credit_advisor": {
        "category": "Banque & Finance B2B",
        "icon": "TrendingUp",
        "color": "emerald",
        "gradient": "from-slate-900 via-emerald-950 to-slate-900",
        "cardBorder": "border-emerald-500/30",
        "accentBg": "bg-emerald-600",
        "accentText": "text-emerald-400",
        "badgeBg": "bg-emerald-500/10 text-emerald-300 border-emerald-500/20"
    },
    "net_arch": {
        "category": "Télécoms & Réseaux ARCEP",
        "icon": "Radio",
        "color": "purple",
        "gradient": "from-slate-900 via-purple-950 to-slate-900",
        "cardBorder": "border-purple-500/30",
        "accentBg": "bg-purple-600",
        "accentText": "text-purple-400",
        "badgeBg": "bg-purple-500/10 text-purple-300 border-purple-500/20"
    },
    "earth_intel": {
        "category": "Spatial & Imagerie Satellite",
        "icon": "Globe",
        "color": "cyan",
        "gradient": "from-slate-900 via-cyan-950 to-slate-900",
        "cardBorder": "border-cyan-500/30",
        "accentBg": "bg-cyan-600",
        "accentText": "text-cyan-400",
        "badgeBg": "bg-cyan-500/10 text-cyan-300 border-cyan-500/20"
    },
    "transit_navigator": {
        "category": "Transports & Mobilité SNCF",
        "icon": "Train",
        "color": "sky",
        "gradient": "from-slate-900 via-sky-950 to-slate-900",
        "cardBorder": "border-sky-500/30",
        "accentBg": "bg-sky-600",
        "accentText": "text-sky-400",
        "badgeBg": "bg-sky-500/10 text-sky-300 border-sky-500/20"
    },
    "pulse_checker": {
        "category": "Santé & Hôpitaux RPPS",
        "icon": "Activity",
        "color": "rose",
        "gradient": "from-slate-900 via-rose-950 to-slate-900",
        "cardBorder": "border-rose-500/30",
        "accentBg": "bg-rose-600",
        "accentText": "text-rose-400",
        "badgeBg": "bg-rose-500/10 text-rose-300 border-rose-500/20"
    },
    "shelf_optimizer": {
        "category": "Retail & Merchandising",
        "icon": "ShoppingCart",
        "color": "amber",
        "gradient": "from-slate-900 via-amber-950 to-slate-900",
        "cardBorder": "border-amber-500/30",
        "accentBg": "bg-amber-600",
        "accentText": "text-amber-400",
        "badgeBg": "bg-amber-500/10 text-amber-300 border-amber-500/20"
    },
    "arena_manager": {
        "category": "Sport & Infrastructure Stades",
        "icon": "Landmark",
        "color": "red",
        "gradient": "from-slate-900 via-red-950 to-slate-900",
        "cardBorder": "border-red-500/30",
        "accentBg": "bg-red-600",
        "accentText": "text-red-400",
        "badgeBg": "bg-red-500/10 text-red-300 border-red-500/20"
    },
    "helios": {
        "category": "Énergie & Bornes IRVE Enedis",
        "icon": "Zap",
        "color": "yellow",
        "gradient": "from-slate-900 via-yellow-950 to-slate-900",
        "cardBorder": "border-yellow-500/30",
        "accentBg": "bg-yellow-600",
        "accentText": "text-yellow-400",
        "badgeBg": "bg-yellow-500/10 text-yellow-300 border-yellow-500/20"
    },
    "ceres": {
        "category": "Agriculture & Agroécologie",
        "icon": "Leaf",
        "color": "green",
        "gradient": "from-slate-900 via-green-950 to-slate-900",
        "cardBorder": "border-green-500/30",
        "accentBg": "bg-green-600",
        "accentText": "text-green-400",
        "badgeBg": "bg-green-500/10 text-green-300 border-green-500/20"
    },
    "cine_analyst": {
        "category": "Cinéma & Box-Office CNC",
        "icon": "Film",
        "color": "fuchsia",
        "gradient": "from-slate-900 via-fuchsia-950 to-slate-900",
        "cardBorder": "border-fuchsia-500/30",
        "accentBg": "bg-fuchsia-600",
        "accentText": "text-fuchsia-400",
        "badgeBg": "bg-fuchsia-500/10 text-fuchsia-300 border-fuchsia-500/20"
    }
}

class AgentManager:
    def __init__(self):
        self._cached_token = None
        self._token_time = 0

    def get_access_token(self) -> str:
        try:
            token = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip()
            return token
        except Exception as e:
            print(f"Warning: Failed to fetch gcloud access token: {e}")
            return ""

    def list_agents(self) -> List[Dict[str, Any]]:
        """Dynamically scans all agents in agents/ directory."""
        agents = []
        if not os.path.exists(AGENTS_DIR):
            return agents

        for item in sorted(os.listdir(AGENTS_DIR)):
            agent_path = os.path.join(AGENTS_DIR, item)
            payload_path = os.path.join(agent_path, "agent_payload.json")
            if os.path.isdir(agent_path) and os.path.exists(payload_path):
                try:
                    with open(payload_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    display_name = data.get("displayName", item.capitalize())
                    description = data.get("description", "")
                    
                    published_ctx = data.get("dataAnalyticsAgent", {}).get("publishedContext", {})
                    example_queries = [
                        q.get("naturalLanguageQuestion") 
                        for q in published_ctx.get("exampleQueries", [])
                        if q.get("naturalLanguageQuestion")
                    ]
                    
                    # Extract dataset
                    table_refs = published_ctx.get("datasourceReferences", {}).get("bq", {}).get("tableReferences", [])
                    dataset_id = table_refs[0].get("datasetId") if table_refs else ""
                    
                    theme = AGENT_THEMES.get(item, {
                        "category": "Industrie Spécialisée",
                        "icon": "Database",
                        "color": "blue",
                        "gradient": "from-slate-900 via-blue-950 to-slate-900",
                        "cardBorder": "border-blue-500/30",
                        "accentBg": "bg-blue-600",
                        "accentText": "text-blue-400",
                        "badgeBg": "bg-blue-500/10 text-blue-300 border-blue-500/20"
                    })

                    agents.append({
                        "id": item,
                        "agentId": f"{item.replace('_', '-')}-agent",
                        "displayName": display_name,
                        "description": description,
                        "datasetId": dataset_id,
                        "exampleQueries": example_queries[:6],
                        "theme": theme,
                        "status": "online"
                    })
                except Exception as e:
                    print(f"Error parsing agent '{item}': {e}")
        return agents

    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Check health status of a specific agent."""
        token = self.get_access_token()
        if not token:
            return {"status": "degraded", "message": "GCP Token non disponible"}

        gcp_agent_id = agent_id.replace('_', '-')
        agent_resource = f"projects/{PROJECT_ID}/locations/{LOCATION}/dataAgents/{gcp_agent_id}-agent"
        url = f"https://geminidataanalytics.googleapis.com/v1alpha/{agent_resource}"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                return {"status": "online", "message": "Agent Vertex AI actif et disponible"}
            else:
                return {"status": "degraded", "message": f"Code HTTP {resp.status_code}: {resp.text[:100]}"}
        except Exception as e:
            return {"status": "offline", "message": f"Erreur de connexion: {str(e)}"}

    def generate_chat_stream(self, agent_id: str, prompt: str, conversation_history: Optional[List[Dict[str, str]]] = None):
        """Streams response from Vertex AI Data Agents REST API."""
        token = self.get_access_token()
        if not token:
            yield f"data: {json.dumps({'type': 'error', 'content': 'Authentification GCP impossible. Veuillez vérifier gcloud auth.'})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return

        gcp_agent_id = agent_id.replace('_', '-')
        agent_resource = f"projects/{PROJECT_ID}/locations/{LOCATION}/dataAgents/{gcp_agent_id}-agent"
        url = f"https://geminidataanalytics.googleapis.com/v1alpha/projects/{PROJECT_ID}/locations/{LOCATION}:chat"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Build messages payload
        messages = []
        if conversation_history:
            for msg in conversation_history:
                if msg.get("role") == "user":
                    messages.append({"user_message": {"text": msg.get("content", "")}})
        
        # Add current user prompt
        messages.append({"user_message": {"text": prompt}})

        payload = {
            "data_agent_context": {
                "data_agent": agent_resource
            },
            "messages": messages
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, stream=True, timeout=60)
            
            if resp.status_code != 200:
                # Handle error gracefully without crashing
                err_text = resp.text[:300]
                yield f"data: {json.dumps({'type': 'error', 'content': f'L\'agent {agent_id} a rencontré une indisponibilité temporaire (Code {resp.status_code}). Restitution en mode dégradé.'})}\n\n"
                yield f"data: {json.dumps({'type': 'content', 'content': f'Je rencontre actuellement une difficulté technique à joindre le service Vertex AI ({resp.status_code}). Veuillez vérifier vos identifiants GCP ou réessayer votre question.'})}\n\n"
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
                return

            full_text = resp.text
            try:
                data_list = json.loads(full_text)
                if isinstance(data_list, dict):
                    data_list = [data_list]
                
                for item in data_list:
                    if not isinstance(item, dict):
                        continue
                    system_msg = item.get("systemMessage", {})
                    text_obj = system_msg.get("text", {})
                    text_type = text_obj.get("textType", "")
                    
                    if text_type == "THOUGHT":
                        parts = text_obj.get("parts", [])
                        thought_content = "\n".join(parts) if isinstance(parts, list) else str(parts)
                        yield f"data: {json.dumps({'type': 'thought', 'content': thought_content})}\n\n"
                    elif text_type == "FINAL_RESPONSE":
                        content = text_obj.get("text", "")
                        yield f"data: {json.dumps({'type': 'content', 'content': content})}\n\n"
                    else:
                        content = text_obj.get("text", "") or json.dumps(item)
                        if content:
                            yield f"data: {json.dumps({'type': 'content', 'content': content})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'content': f'Erreur de traitement des données: {str(e)}'})}\n\n"
            
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': f'Erreur système: {str(e)}'})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

agent_manager = AgentManager()
