import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Full-Duplex Web Audio Streaming Hook for Gemini Multimodal Live API.
 * Connects directly to Google ADK Live WebSocket (/ws/live):
 * - Records 16kHz PCM 16-bit mono audio from client mic and streams to server.
 * - Receives and plays 24kHz PCM audio natively synthesized by Gemini Live Voice (Aoede).
 * - Handles interruptibility, live tool events, and transcription.
 */
export function useGeminiLive(onToolResponseReceived, voiceName = 'Aoede') {
  const [isConnected, setIsConnected] = useState(false);
  const [isLiveStreaming, setIsLiveStreaming] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [liveTranscript, setLiveTranscript] = useState('');
  const [currentTool, setCurrentTool] = useState(null);
  const [error, setError] = useState(null);

  const socketRef = useRef(null);
  const audioContextRef = useRef(null);
  const nextPlayTimeRef = useRef(0);
  const micStreamRef = useRef(null);
  const micProcessorRef = useRef(null);

  // Initialize Web Audio Context for 24kHz Output Playback
  const getAudioContext = useCallback(() => {
    if (!audioContextRef.current) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      audioContextRef.current = new AudioCtx({ sampleRate: 24000 });
    }
    if (audioContextRef.current.state === 'suspended') {
      audioContextRef.current.resume();
    }
    return audioContextRef.current;
  }, []);

  // Play incoming 24kHz 16-bit PCM audio chunk smoothly in time with anti-clipping filter
  const playAudioChunk = useCallback((base64Data) => {
    try {
      const ctx = getAudioContext();
      const binaryString = window.atob(base64Data);
      const len = binaryString.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }

      // Convert 16-bit signed integer PCM to Float32 [-1.0, 1.0]
      const int16Array = new Int16Array(bytes.buffer);
      const float32Array = new Float32Array(int16Array.length);
      for (let i = 0; i < int16Array.length; i++) {
        float32Array[i] = int16Array[i] / 32768.0;
      }

      const audioBuffer = ctx.createBuffer(1, float32Array.length, 24000);
      audioBuffer.copyToChannel(float32Array, 0);

      const source = ctx.createBufferSource();
      source.buffer = audioBuffer;

      // Soft Limiter Gain Node (0.90) to prevent clipping distortion
      const gainNode = ctx.createGain();
      gainNode.gain.setValueAtTime(0.90, ctx.currentTime);

      // Lowpass anti-aliasing filter to remove high-frequency digital noise
      const filter = ctx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(9500, ctx.currentTime);

      source.connect(gainNode);
      gainNode.connect(filter);
      filter.connect(ctx.destination);

      const now = ctx.currentTime;
      const startTime = Math.max(now, nextPlayTimeRef.current);
      source.start(startTime);
      nextPlayTimeRef.current = startTime + audioBuffer.duration;
      setIsSpeaking(true);

      source.onended = () => {
        if (ctx.currentTime >= nextPlayTimeRef.current - 0.05) {
          setIsSpeaking(false);
        }
      };
    } catch (e) {
      console.warn("Audio playback error:", e);
    }
  }, [getAudioContext]);

  // Connect WebSocket to /ws/live
  const connectLive = useCallback(() => {
    try {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${protocol}//${window.location.host}/ws/live?voice=${encodeURIComponent(voiceName || 'Aoede')}`;
      
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
            console.log("Gemini Live Session Ready with model:", data.model, "voice:", data.voice);
          } else if (data.type === 'audio_chunk') {
            playAudioChunk(data.data);
          } else if (data.type === 'content') {
            setLiveTranscript(prev => prev + data.content);
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
          } else if (data.type === 'interrupted') {
            // Stop current audio output immediately on interrupt
            if (audioContextRef.current) {
              nextPlayTimeRef.current = audioContextRef.current.currentTime;
            }
            setIsSpeaking(false);
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
  }, [onToolResponseReceived, playAudioChunk]);

  // Start continuous microphone stream (16kHz mono PCM)
  const startMicStreaming = useCallback(async () => {
    try {
      getAudioContext();
      const stream = await navigator.mediaDevices.getUserMedia({ audio: { channelCount: 1, sampleRate: 16000 } });
      micStreamRef.current = stream;

      const inputCtx = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
      const micSource = inputCtx.createMediaStreamSource(stream);
      const processor = inputCtx.createScriptProcessor(4096, 1, 1);

      processor.onaudioprocess = (e) => {
        if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) return;
        const inputData = e.inputBuffer.getChannelData(0);
        
        // Convert Float32 to 16-bit Int PCM
        const pcm16 = new Int16Array(inputData.length);
        for (let i = 0; i < inputData.length; i++) {
          const s = Math.max(-1, Math.min(1, inputData[i]));
          pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
        }

        // Base64 encode
        const bytes = new Uint8Array(pcm16.buffer);
        let binary = '';
        for (let i = 0; i < bytes.length; i++) {
          binary += String.fromCharCode(bytes[i]);
        }
        const b64 = window.btoa(binary);

        socketRef.current.send(JSON.stringify({
          type: "audio_chunk",
          data: b64
        }));
      };

      micSource.connect(processor);
      processor.connect(inputCtx.destination);
      micProcessorRef.current = { inputCtx, processor, micSource };
      setIsLiveStreaming(true);
    } catch (err) {
      console.error("Error accessing microphone for Live API:", err);
      setError("Microphone inaccessible pour Gemini Live.");
    }
  }, [getAudioContext]);

  // Stop microphone stream
  const stopMicStreaming = useCallback(() => {
    if (micStreamRef.current) {
      micStreamRef.current.getTracks().forEach(t => t.stop());
      micStreamRef.current = null;
    }
    if (micProcessorRef.current) {
      micProcessorRef.current.processor.disconnect();
      micProcessorRef.current.micSource.disconnect();
      micProcessorRef.current.inputCtx.close();
      micProcessorRef.current = null;
    }
    setIsLiveStreaming(false);
  }, []);

  const disconnectLive = useCallback(() => {
    stopMicStreaming();
    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
      setIsConnected(false);
      setIsLiveStreaming(false);
    }
  }, [stopMicStreaming]);

  const sendLivePrompt = useCallback((promptText) => {
    getAudioContext();
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({
        type: "user_text",
        text: promptText
      }));
    }
  }, [getAudioContext]);

  useEffect(() => {
    connectLive();
    return () => {
      disconnectLive();
    };
  }, [connectLive, disconnectLive]);

  return {
    isConnected,
    isLiveStreaming,
    isSpeaking,
    liveTranscript,
    currentTool,
    error,
    sendLivePrompt,
    startMicStreaming,
    stopMicStreaming,
    connectLive,
    disconnectLive
  };
}
