import os
import sys
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent_manager import agent_manager, PROJECT_ID

app = FastAPI(
    title="TalkToData API - Google Cloud Data Agents Interface",
    version="2.0.0",
    description="Backend API exposing 11 Industry Vertex AI Data Agents with SSE streaming and failover"
)

# Enable CORS for local Vite dev server and Chromebook client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    agent_id: str
    prompt: str
    history: Optional[List[ChatMessage]] = []

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "project": PROJECT_ID,
        "agentsCount": len(agent_manager.list_agents()),
        "version": "2.0.0"
    }

@app.get("/api/agents")
def get_agents():
    """Return all available industry data agents with metadata and themes."""
    agents = agent_manager.list_agents()
    return {"agents": agents, "count": len(agents)}

@app.get("/api/agents/{agent_id}/status")
def get_agent_status(agent_id: str):
    """Check health status of a specific agent."""
    status_info = agent_manager.get_agent_status(agent_id)
    return {"agentId": agent_id, **status_info}

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    """
    Stream response from Vertex AI Data Agent via Server-Sent Events (SSE).
    Guarantees resilient fallback if the agent is temporarily unavailable.
    """
    if not req.agent_id or not req.prompt:
        raise HTTPException(status_code=400, detail="agent_id and prompt are required.")

    history_dict = [{"role": msg.role, "content": msg.content} for msg in req.history] if req.history else []
    
    stream_generator = agent_manager.generate_chat_stream(
        agent_id=req.agent_id,
        prompt=req.prompt,
        conversation_history=history_dict
    )

    return StreamingResponse(stream_generator, media_type="text/event-stream")

# Serve built frontend static files if dist/ directory exists
DIST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")
if os.path.exists(DIST_DIR):
    assets_dir = os.path.join(DIST_DIR, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api"):
            raise HTTPException(status_code=404, detail="API route not found")
        
        file_path = os.path.join(DIST_DIR, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            media_type = None
            if file_path.endswith(".js"):
                media_type = "application/javascript"
            elif file_path.endswith(".css"):
                media_type = "text/css"
            elif file_path.endswith(".svg"):
                media_type = "image/svg+xml"
            return FileResponse(file_path, media_type=media_type)
        
        # If static asset is missing, return 404 error instead of index.html to prevent JS MIME type mismatch
        if full_path.startswith("assets") or full_path.endswith((".js", ".css", ".png", ".jpg", ".svg", ".ico")):
            raise HTTPException(status_code=404, detail="Static asset not found")
            
        return FileResponse(os.path.join(DIST_DIR, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
