"""
Client interface for Google Cloud MCP Toolbox.
Provides helper methods to load declarative tools into Google ADK Agents and Python applications.
"""

import os
import json
import logging
from typing import Dict, Any, List, Callable
from .server import MCPToolboxServer

logger = logging.getLogger("mcp_toolbox_client")

class ToolboxClient:
    def __init__(self, config_path: str = None):
        self.server = MCPToolboxServer(config_path) if config_path else MCPToolboxServer()

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Returns tool schema definitions for Google ADK / Gemini Tool declarations."""
        return self.server.list_tools()

    def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """Directly invokes an MCP tool and returns the JSON result payload."""
        return self.server.execute_tool(tool_name, arguments)

    def get_adk_function_declarations(self) -> List[Dict[str, Any]]:
        """
        Converts MCP tools into Google GenAI / Gemini function declarations format.
        Compatible with google.genai and Google ADK.
        """
        declarations = []
        for tool in self.get_tool_definitions():
            declarations.append({
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool.get("inputSchema", {"type": "object", "properties": {}})
            })
        return declarations

# Singleton instance
toolbox_client = ToolboxClient()
