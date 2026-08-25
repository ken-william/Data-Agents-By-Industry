import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Hook for Gemini Multimodal Live API WebSocket streaming.
 * Handles continuous bidirectional real-time streaming, tool events, and audio feedback.
 */
export function useGeminiLive(onToolResponseReceived) {
  const [isConnected, setIsConnected] = useState(false);
  const [isLiveStreaming, setIsLiveStreaming] = useState(false);
  const [liveTranscript, setLiveTranscript] = useState('');
  const [currentTool, setCurrentTool] = useState(null);
  const [error, setError] = useState(null);

  const socketRef = useRef(null);

  const connectLive = useCallback(() => {
    try {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${protocol}//${window.location.host}/ws/live`;
      
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        setIsConnected(true);
        setError(null);
        console.log("Connected to Gemini Multimodal Live WebSocket");
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          if (data.type === 'session_ready') {
            console.log("Gemini Live Session Ready with model:", data.model);
          } else if (data.type === 'thought') {
            console.log("Live Orchestrator Thought:", data.content);
          } else if (data.type === 'tool_call') {
            setCurrentTool(data.tool);
            setIsLiveStreaming(true);
          } else if (data.type === 'tool_response') {
            setIsLiveStreaming(false);
            if (onToolResponseReceived) {
              onToolResponseReceived(data.content, data.tool);
            }
          } else if (data.type === 'error') {
            setError(data.content);
            setIsLiveStreaming(false);
          }
        } catch (e) {
          console.warn("WebSocket parse error:", e);
        }
      };

      ws.onclose = () => {
        setIsConnected(false);
        setIsLiveStreaming(false);
      };

      ws.onerror = (err) => {
        console.error("Gemini Live WebSocket error:", err);
        setError("Erreur de connexion avec le serveur Gemini Live.");
        setIsConnected(false);
      };

      socketRef.current = ws;
    } catch (err) {
      console.error("Failed to connect to Gemini Live:", err);
      setError(err.message);
    }
  }, [onToolResponseReceived]);

  const disconnectLive = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
      setIsConnected(false);
      setIsLiveStreaming(false);
    }
  }, []);

  const sendLivePrompt = useCallback((promptText) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({
        type: "user_text",
        text: promptText
      }));
    }
  }, []);

  useEffect(() => {
    connectLive();
    return () => {
      disconnectLive();
    };
  }, [connectLive, disconnectLive]);

  return {
    isConnected,
    isLiveStreaming,
    liveTranscript,
    currentTool,
    error,
    sendLivePrompt,
    connectLive,
    disconnectLive
  };
}
