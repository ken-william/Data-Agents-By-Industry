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
from typing import Dict, Any, Optional
from fastapi import WebSocket, WebSocketDisconnect

from google import genai
from google.genai import types

try:
    from mcp_toolbox.toolbox_client import toolbox_client
except ImportError:
    from backend.mcp_toolbox.toolbox_client import toolbox_client
from .host_agent import HOST_SYSTEM_INSTRUCTION

logger = logging.getLogger("gemini_live_session")

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
GEMINI_LIVE_MODEL = "gemini-2.0-flash-exp"
DEFAULT_VOICE = "Aoede"  # Warm, charismatic, professional voice for French & English storytelling

class GeminiLiveSessionManager:
    def __init__(self, websocket: WebSocket, voice: str = "Aoede"):
        self.client_ws = websocket
        self.voice = voice if voice in ["Aoede", "Puck", "Charon", "Kore", "Fenrir"] else "Aoede"
        self.is_active = True
        self.client: Optional[genai.Client] = None
        self._init_genai_client()

    def _init_genai_client(self):
        """Initializes the google-genai client with Vertex AI or AI Studio API Key."""
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            logger.info("Initializing Gemini Live client with Google AI Studio API Key.")
            self.client = genai.Client(api_key=api_key, http_options={"api_version": "v1alpha"})
        else:
            logger.info(f"Initializing Gemini Live client with GCP Vertex AI ({PROJECT_ID}, {LOCATION}).")
            self.client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

    def _get_live_tools(self):
        """Builds Gemini Live Function Declarations from MCP Toolbox."""
        raw_tools = toolbox_client.get_tool_definitions()
        function_declarations = []

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

        return [types.Tool(function_declarations=function_declarations)] if function_declarations else []

    async def start_session(self):
        """Starts bidirectional live streaming between browser client and Gemini Live."""
        await self.client_ws.accept()
        logger.info(f"Client connected to Gemini Live WebSocket with voice: {self.voice}.")

        # Live Config with 24kHz Audio synthesis & Selected Prebuilt Voice
        config = types.LiveConnectConfig(
            response_modalities=[types.LiveModality.AUDIO],
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

        try:
            # Connect to Gemini Multimodal Live API
            async with self.client.aio.live.connect(model=GEMINI_LIVE_MODEL, config=config) as live_session:
                logger.info(f"Connected to Gemini Live model: {GEMINI_LIVE_MODEL}")

                # Send confirmation to client
                await self.client_ws.send_json({
                    "type": "session_ready",
                    "model": GEMINI_LIVE_MODEL,
                    "voice": DEFAULT_VOICE,
                    "status": "connected"
                })

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
                            realtime_input={
                                "media_chunks": [
                                    types.Blob(
                                        mime_type="audio/pcm;rate=16000",
                                        data=audio_bytes
                                    )
                                ]
                            }
                        )

                # 2. Text Input / Interrupt command
                elif msg_type == "user_text":
                    text = data.get("text", "")
                    if text:
                        await live_session.send(
                            input=types.Content(
                                parts=[types.Part.from_text(text=text)]
                            ),
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
                            # 1. Native 24kHz PCM Audio Stream from Gemini Live Voice (Aoede)
                            if part.inline_data:
                                audio_b64 = base64.b64encode(part.inline_data.data).decode("utf-8")
                                await self.client_ws.send_json({
                                    "type": "audio_chunk",
                                    "data": audio_b64,
                                    "mimeType": part.inline_data.mime_type
                                })

                            # 2. Real-time Text Transcription
                            if part.text:
                                await self.client_ws.send_json({
                                    "type": "content",
                                    "content": part.text
                                })

                    if server_content.turn_complete:
                        await self.client_ws.send_json({"type": "turn_complete"})

                    if server_content.interrupted:
                        await self.client_ws.send_json({"type": "interrupted"})

                # 3. Real-time Tool Call from Gemini Live -> Execute MCP Tool on BigQuery
                tool_call = response.tool_call
                if tool_call is not None:
                    for call in tool_call.function_calls:
                        call_id = call.id
                        func_name = call.name
                        func_args = call.args or {}

                        # Notify client of tool execution
                        await self.client_ws.send_json({
                            "type": "thought",
                            "content": f"Consultation en direct de l'agent BigQuery : {func_name}..."
                        })

                        # Execute tool via MCP Toolbox
                        logger.info(f"Gemini Live executing MCP Tool: {func_name} with args {func_args}")
                        tool_result = toolbox_client.call_tool(func_name, dict(func_args))
                        raw_result_text = tool_result.get("content", [{}])[0].get("text", "Données récupérées.")

                        # Send Tool Response back into the Gemini Live Session so Gemini speaks the result!
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
