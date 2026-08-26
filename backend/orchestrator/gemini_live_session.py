"""
True Gemini Multimodal Live API Bidirectional WebSocket Manager.
Implements Google ADK & Google GenAI Live API reference architecture:
- https://adk.dev/live/
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/live-api/get-started-adk
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/live-api/configure-language-voice

Handles low-latency full-duplex PCM audio streaming, interruptibility,
and real-time tool execution against BigQuery MCP Data Agents.
"""

import os
import json
import base64
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from fastapi import WebSocket, WebSocketDisconnect

from google import genai
from google.genai import types

# Load .env file from project root or current folder
load_dotenv(Path(__file__).parents[2] / ".env", override=True)
load_dotenv(Path(__file__).parent / ".env", override=True)

try:
    from mcp_toolbox.toolbox_client import toolbox_client
except ImportError:
    from backend.mcp_toolbox.toolbox_client import toolbox_client
from .host_agent import HOST_SYSTEM_INSTRUCTION

logger = logging.getLogger("gemini_live_session")

def _env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}

def _ignore_normal_live_close(record: logging.LogRecord) -> bool:
    exc = record.exc_info[1] if record.exc_info else None
    return not (
        isinstance(exc, genai.errors.APIError) and exc.code == 1000
    )

logging.getLogger("google_adk.google.adk.flows.llm_flows.base_llm_flow").addFilter(_ignore_normal_live_close)

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
LIVE_USE_VERTEXAI = _env_flag("GOOGLE_GENAI_USE_VERTEXAI", default=True)

# Supported ADK Native-Audio Live Models
DEFAULT_VERTEX_AGENT_MODEL = os.getenv("DEFAULT_VERTEX_AGENT_MODEL", "gemini-live-2.5-flash-native-audio")
DEFAULT_GEMINI_AGENT_MODEL = os.getenv("DEFAULT_GEMINI_AGENT_MODEL", "gemini-2.5-flash-native-audio-preview-12-2025")

VERTEX_LIVE_MODELS = [
    DEFAULT_VERTEX_AGENT_MODEL,
    "gemini-live-2.5-flash-native-audio",
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash"
]
GEMINI_API_LIVE_MODELS = [
    DEFAULT_GEMINI_AGENT_MODEL,
    "gemini-2.5-flash-native-audio-preview-12-2025",
    "gemini-2.0-flash-exp"
]
DEFAULT_VOICE = "Aoede"  # Warm, charismatic, professional voice for French & English storytelling

class GeminiLiveSessionManager:
    def __init__(self, websocket: WebSocket, voice: str = "Aoede"):
        self.client_ws = websocket
        self.voice = voice if voice in ["Aoede", "Puck", "Charon", "Kore", "Fenrir"] else "Aoede"
        self.is_active = True
        self.client: Optional[genai.Client] = None
        self.is_vertex = LIVE_USE_VERTEXAI
        self._init_genai_client()

    def _init_genai_client(self):
        """Initializes the google-genai client with Vertex AI or AI Studio API Key."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not self.is_vertex and api_key:
            logger.info("Initializing Gemini Live client with Google AI Studio API Key.")
            self.client = genai.Client(api_key=api_key, http_options={"api_version": "v1alpha"})
            self.is_vertex = False
        else:
            logger.info(f"Initializing Gemini Live client with GCP Vertex AI ({PROJECT_ID}, {LOCATION}).")
            self.client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
            self.is_vertex = True

    def _get_live_tools(self):
        """Builds Gemini Live Function Declarations from MCP Toolbox and UI Control Actions."""
        raw_tools = toolbox_client.get_tool_definitions()
        function_declarations = []

        # 1. Specialized BigQuery MCP Tools
        for t in raw_tools:
            function_declarations.append(
                types.FunctionDeclaration(
                    name=t["name"],
                    description=t["description"],
                    parameters=t.get("inputSchema", {
                        "type": "object",
                        "properties": {
                            "prompt": {"type": "string", "description": "La question d'analyse métier à poser à l'agent sectoriel."}
                        },
                        "required": ["prompt"]
                    })
                )
            )

        # 2. UI Control & Navigation Tools
        function_declarations.append(
            types.FunctionDeclaration(
                name="switch_agent_view",
                description="Bascule visuellement l'application sur un secteur ou agent spécifique (sully, arena_manager, earth_intel, credit_advisor, cine_analyst, net_arch, transit_navigator, pulse_checker, shelf_optimizer, helios, juris_pilot).",
                parameters={
                    "type": "object",
                    "properties": {
                        "agent_id": {
                            "type": "string",
                            "description": "Identifiant de l'agent cible (ex: 'sully_agent', 'arena_manager_agent', 'earth_intel_agent', 'credit_advisor_agent', 'cine_analyst_agent', 'net_arch_agent', 'transit_navigator_agent', 'pulse_checker_agent', 'shelf_optimizer_agent', 'helios_agent', 'juris_pilot_agent')."
                        },
                        "sector_name": {
                            "type": "string",
                            "description": "Nom convivial du secteur d'activité."
                        }
                    },
                    "required": ["agent_id"]
                }
            )
        )

        function_declarations.append(
            types.FunctionDeclaration(
                name="toggle_sql_inspector",
                description="Ouvre ou ferme le volet d'inspection SQL BigQuery sur l'écran pour afficher la requête SQL exacte.",
                parameters={
                    "type": "object",
                    "properties": {
                        "visible": {
                            "type": "boolean",
                            "description": "True pour afficher l'inspecteur SQL, False pour masquer."
                        }
                    },
                    "required": ["visible"]
                }
            )
        )

        function_declarations.append(
            types.FunctionDeclaration(
                name="return_to_home_view",
                description="Revient à l'écran d'accueil principal de l'application.",
                parameters={"type": "object", "properties": {}}
            )
        )

        return [types.Tool(function_declarations=function_declarations)] if function_declarations else []

    async def start_session(self):
        """Starts bidirectional live streaming between browser client and Gemini Live."""
        await self.client_ws.accept()
        logger.info(f"Client connected to Gemini Live WebSocket with voice: {self.voice}.")

        # Live Config with 24kHz Audio synthesis & Selected Prebuilt Voice
        config = types.LiveConnectConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=self.voice
                    )
                )
            ),
            system_instruction=types.Content(
                parts=[types.Part.from_text(text=HOST_SYSTEM_INSTRUCTION)]
            ),
            tools=self._get_live_tools()
        )

        candidate_models = VERTEX_LIVE_MODELS if self.is_vertex else GEMINI_API_LIVE_MODELS
        connected_session = None
        active_model_name = candidate_models[0]

        for model_name in candidate_models:
            try:
                logger.info(f"Attempting connection to Gemini Live model: {model_name}...")
                session_cm = self.client.aio.live.connect(model=model_name, config=config)
                live_session = await session_cm.__aenter__()
                connected_session = (session_cm, live_session)
                active_model_name = model_name
                logger.info(f"✅ Successfully connected to Gemini Live model: {model_name}")
                break
            except Exception as conn_err:
                logger.warning(f"Could not connect with model {model_name}: {conn_err}. Trying fallback...")

        if not connected_session:
            err_msg = "Impossible de se connecter aux modèles Gemini Live API. Vérifiez votre configuration GCP ou clé API."
            logger.error(err_msg)
            await self.client_ws.send_json({"type": "error", "content": err_msg})
            return

        session_cm, live_session = connected_session

        try:
            # Send session confirmation to client
            await self.client_ws.send_json({
                "type": "session_ready",
                "model": active_model_name,
                "voice": self.voice,
                "status": "connected"
            })

            # Proactive Initial Greeting: Host welcomes the user with voice
            await live_session.send(
                input="Accueille chaleureusement l'utilisateur en français avec ta voix en te présentant comme l'Hôte de Talk to Data et invite-le à explorer la flotte de 11 agents BigQuery.",
                end_of_turn=True
            )

            # Launch concurrent Upstream and Downstream tasks
            upstream_task = asyncio.create_task(self._upstream_handler(live_session))
            downstream_task = asyncio.create_task(self._downstream_handler(live_session))

            done, pending = await asyncio.wait(
                [upstream_task, downstream_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in pending:
                task.cancel()

        except WebSocketDisconnect:
            logger.info("Client disconnected from Gemini Live.")
        except Exception as e:
            logger.error(f"Error in Gemini Live Session: {e}", exc_info=True)
            try:
                await self.client_ws.send_json({
                    "type": "error",
                    "content": f"Erreur de session Gemini Live: {str(e)}"
                })
            except Exception:
                pass
        finally:
            self.is_active = False
            try:
                await session_cm.__aexit__(None, None, None)
            except Exception:
                pass

    async def _upstream_handler(self, live_session):
        """Reads audio chunks and text commands from client WebSocket and forwards to Gemini Live."""
        try:
            while self.is_active:
                message = await self.client_ws.receive_text()
                if not message:
                    continue

                data = json.loads(message)
                msg_type = data.get("type")

                # 1. Real-time PCM Audio Chunk from client microphone (16kHz PCM mono)
                if msg_type == "audio_chunk":
                    raw_base64 = data.get("data")
                    if raw_base64:
                        audio_bytes = base64.b64decode(raw_base64)
                        await live_session.send(
                            input=types.LiveClientRealtimeInput(
                                media_chunks=[
                                    types.Blob(
                                        mime_type="audio/pcm;rate=16000",
                                        data=audio_bytes
                                    )
                                ]
                            )
                        )

                # 2. Text Input / Scenario selection command
                elif msg_type == "user_text":
                    text = data.get("text", "")
                    if text:
                        await live_session.send(
                            input=text,
                            end_of_turn=True
                        )

        except WebSocketDisconnect:
            pass
        except asyncio.CancelledError:
            pass

    async def _downstream_handler(self, live_session):
        """Receives audio, text, and tool calls from Gemini Live and streams back to client."""
        try:
            async for response in live_session.receive():
                server_content = response.server_content

                if server_content is not None:
                    model_turn = server_content.model_turn
                    if model_turn is not None:
                        for part in model_turn.parts:
                            # 1. Native 24kHz PCM Audio Stream from Gemini Live Voice
                            if part.inline_data:
                                audio_b64 = base64.b64encode(part.inline_data.data).decode("utf-8")
                                await self.client_ws.send_json({
                                    "type": "audio_chunk",
                                    "data": audio_b64,
                                    "mimeType": part.inline_data.mime_type
                                })

                            # 2. Real-time Audio Transcription Text
                            if part.text:
                                await self.client_ws.send_json({
                                    "type": "content",
                                    "content": part.text
                                })

                    if server_content.turn_complete:
                        await self.client_ws.send_json({"type": "turn_complete"})

                    if server_content.interrupted:
                        await self.client_ws.send_json({"type": "interrupted"})

                # 3. Streaming Tools Execution: Real-time Tool Call -> MCP Toolbox BigQuery & UI Controls
                tool_call = response.tool_call
                if tool_call is not None:
                    for call in tool_call.function_calls:
                        call_id = call.id
                        func_name = call.name
                        func_args = call.args or {}

                        # A. Handle UI Control & Interface Navigation Tools
                        if func_name == "switch_agent_view":
                            target_id = str(func_args.get("agent_id", ""))
                            logger.info(f"Gemini Live triggered UI Control: switch_agent_view -> {target_id}")
                            await self.client_ws.send_json({
                                "type": "ui_control",
                                "action": "switch_agent",
                                "agent_id": target_id
                            })
                            await live_session.send(
                                types.LiveClientToolResponse(
                                    function_responses=[
                                        types.FunctionResponse(
                                            name=func_name,
                                            id=call_id,
                                            response={"status": "success", "message": f"Écran basculé sur {target_id}."}
                                        )
                                    ]
                                )
                            )
                            continue

                        elif func_name == "toggle_sql_inspector":
                            visible = bool(func_args.get("visible", True))
                            logger.info(f"Gemini Live triggered UI Control: toggle_sql_inspector -> {visible}")
                            await self.client_ws.send_json({
                                "type": "ui_control",
                                "action": "toggle_sql",
                                "visible": visible
                            })
                            await live_session.send(
                                types.LiveClientToolResponse(
                                    function_responses=[
                                        types.FunctionResponse(
                                            name=func_name,
                                            id=call_id,
                                            response={"status": "success", "message": "Inspecteur SQL mis à jour."}
                                        )
                                    ]
                                )
                            )
                            continue

                        elif func_name == "return_to_home_view":
                            logger.info("Gemini Live triggered UI Control: return_to_home_view")
                            await self.client_ws.send_json({
                                "type": "ui_control",
                                "action": "home"
                            })
                            await live_session.send(
                                types.LiveClientToolResponse(
                                    function_responses=[
                                        types.FunctionResponse(
                                            name=func_name,
                                            id=call_id,
                                            response={"status": "success", "message": "Retour à l'accueil effectué."}
                                        )
                                    ]
                                )
                            )
                            continue

                        # B. Handle BigQuery MCP Analytical Tools
                        # Notify client in real-time that BigQuery is being queried
                        await self.client_ws.send_json({
                            "type": "thought",
                            "content": f"Consultation en direct de l'agent BigQuery : {func_name}..."
                        })
                        await self.client_ws.send_json({
                            "type": "tool_executing",
                            "tool": func_name,
                            "args": dict(func_args)
                        })

                        # Execute tool asynchronously via MCP Toolbox
                        logger.info(f"Gemini Live executing Streaming Tool: {func_name} with args {func_args}")
                        tool_result = toolbox_client.call_tool(func_name, dict(func_args))
                        raw_result_text = tool_result.get("content", [{}])[0].get("text", "Données récupérées avec succès.")

                        # Broadcast data payload to UI for immediate chart & table rendering
                        await self.client_ws.send_json({
                            "type": "tool_completed",
                            "tool": func_name,
                            "content": raw_result_text
                        })

                        # Send Tool Response back into Gemini Live so Gemini speaks the analytical summary!
                        await live_session.send(
                            types.LiveClientToolResponse(
                                function_responses=[
                                    types.FunctionResponse(
                                        name=func_name,
                                        id=call_id,
                                        response={"result": raw_result_text}
                                    )
                                ]
                            )
                        )

        except WebSocketDisconnect:
            pass
        except asyncio.CancelledError:
            pass

async def handle_gemini_live_websocket(websocket: WebSocket):
    voice = websocket.query_params.get("voice", "Aoede")
    session = GeminiLiveSessionManager(websocket, voice=voice)
    await session.start_session()
