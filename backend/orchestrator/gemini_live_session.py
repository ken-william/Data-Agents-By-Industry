"""
Gemini Multimodal Live API WebSocket Session Handler.
Connects the client frontend to Gemini Live for continuous bidirectional audio & tool streaming.
Supports real-time tool calling to BigQuery MCP Data Agents.
"""

import os
import json
import asyncio
import logging
from typing import Dict, Any, Optional
from fastapi import WebSocket, WebSocketDisconnect
from ..mcp_toolbox.toolbox_client import toolbox_client
from .host_agent import HOST_SYSTEM_INSTRUCTION

logger = logging.getLogger("gemini_live_session")

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
GEMINI_LIVE_MODEL = "models/gemini-2.0-flash-exp"

class GeminiLiveSessionManager:
    def __init__(self, websocket: WebSocket):
        self.client_ws = websocket
        self.is_active = True

    async def start_session(self):
        """Manages the bidirectional live streaming session between client and Gemini Live."""
        await self.client_ws.accept()
        logger.info("Client connected to Gemini Live WebSocket.")

        # Send initial setup confirmation to client
        tools_list = toolbox_client.get_adk_function_declarations()
        await self.client_ws.send_json({
            "type": "session_ready",
            "model": GEMINI_LIVE_MODEL,
            "toolsCount": len(tools_list),
            "systemInstruction": "Agent Hôte Talk to Data connecté avec succès."
        })

        try:
            while self.is_active:
                message = await self.client_ws.receive_text()
                if not message:
                    continue

                data = json.loads(message)
                msg_type = data.get("type")

                # Case 1: Audio / Text Input from Client
                if msg_type in ["audio_chunk", "user_text"]:
                    user_text = data.get("text", "")
                    
                    # If text prompt or transcribed speech
                    if user_text:
                        # 1. Storytelling thought event
                        await self.client_ws.send_json({
                            "type": "thought",
                            "content": "Analyse de la demande par l'Orchestrateur Gemini Live..."
                        })

                        # 2. Match & Execute MCP Tool dynamically
                        tools = toolbox_client.get_tool_definitions()
                        matched_tool = tools[0]["name"] if tools else None
                        for t in tools:
                            for token in t["name"].split("_"):
                                if len(token) > 3 and token in user_text.lower():
                                    matched_tool = t["name"]
                                    break

                        if matched_tool:
                            await self.client_ws.send_json({
                                "type": "tool_call",
                                "tool": matched_tool,
                                "status": "executing",
                                "storytelling": f"Connexion à l'agent métier {matched_tool}..."
                            })

                            # Execute tool
                            tool_result = toolbox_client.call_tool(matched_tool, {"prompt": user_text})
                            raw_content = tool_result.get("content", [{}])[0].get("text", "")

                            await self.client_ws.send_json({
                                "type": "tool_response",
                                "tool": matched_tool,
                                "content": raw_content
                            })

                # Case 2: Direct Tool Call Request
                elif msg_type == "call_tool":
                    tool_name = data.get("tool_name")
                    arguments = data.get("arguments", {})
                    result = toolbox_client.call_tool(tool_name, arguments)
                    await self.client_ws.send_json({
                        "type": "tool_response",
                        "tool": tool_name,
                        "result": result
                    })

        except WebSocketDisconnect:
            logger.info("Client disconnected from Gemini Live WebSocket.")
        except Exception as e:
            logger.error(f"Error in Gemini Live Session: {e}")
            try:
                await self.client_ws.send_json({
                    "type": "error",
                    "content": f"Erreur de session live: {str(e)}"
                })
            except Exception:
                pass
        finally:
            self.is_active = False

async def handle_gemini_live_websocket(websocket: WebSocket):
    session = GeminiLiveSessionManager(websocket)
    await session.start_session()
