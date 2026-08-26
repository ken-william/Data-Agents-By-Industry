import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Header } from './components/Header';
import { AgentBuilder } from './components/AgentBuilder';
import { LiveCanvas } from './components/LiveCanvas';
import { SettingsDrawer } from './components/SettingsDrawer';
import { useGeminiLive } from './hooks/useGeminiLive';
import { useSpeech } from './hooks/useSpeech';
import { useAgentChat } from './hooks/useAgentChat';
import { Loader2, RefreshCw } from 'lucide-react';

export function App() {
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [viewMode, setViewMode] = useState('builder'); // Land on Home Screen with Live Voice Active
  const [screenMode, setScreenMode] = useState('showcase'); // 'showcase' (Écran A) vs 'controller' (Écran B)
  const [activeTheme, setActiveTheme] = useState('cloud-next'); // 'cloud-next' | 'gemini-aurora' | 'tech-sunset' | 'eco-system'
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Inject active theme into root element data-theme attribute
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', activeTheme);
  }, [activeTheme]);

  // Read ?screen= URL parameter on initial load
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const screenParam = params.get('screen');
    if (screenParam === 'showcase' || screenParam === 'controller') {
      setScreenMode(screenParam);
    }
  }, []);

  const handleVoiceSwitchAgent = useCallback((agentId) => {
    const cleanId = agentId.replace(/_agent$/, '');
    const target = agents.find(a => a.id === agentId || a.id === cleanId);
    if (target) {
      setSelectedAgent(target);
      setViewMode('live'); // Automatically open scenario canvas on voice demand!
    }
  }, [agents]);

  const speechProps = useSpeech(() => {});
  const chatProps = useAgentChat(selectedAgent, null, handleVoiceSwitchAgent);

  // Gemini Live Native Multimodal Hook (PCM 16kHz Streaming & 24kHz Native Audio Output)
  const handleToolResponseReceived = useCallback((toolResult, toolName) => {
    chatProps.addAssistantMessage(toolResult);
  }, [chatProps]);

  const geminiLiveProps = useGeminiLive(handleToolResponseReceived, 'Aoede');

  // Auto-activate microphone as soon as Gemini Live WebSocket is ready
  useEffect(() => {
    if (geminiLiveProps.isConnected && !geminiLiveProps.isLiveStreaming) {
      geminiLiveProps.startMicStreaming();
    }
  }, [geminiLiveProps.isConnected, geminiLiveProps.isLiveStreaming]);

  // Browser Autoplay Fallback: activate mic on first user click if browser policy paused it
  useEffect(() => {
    const handleFirstUserGesture = () => {
      if (geminiLiveProps.isConnected && !geminiLiveProps.isLiveStreaming) {
        geminiLiveProps.startMicStreaming();
      }
    };
    window.addEventListener('click', handleFirstUserGesture, { once: true });
    window.addEventListener('touchstart', handleFirstUserGesture, { once: true });
    return () => {
      window.removeEventListener('click', handleFirstUserGesture);
      window.removeEventListener('touchstart', handleFirstUserGesture);
    };
  }, [geminiLiveProps.isConnected, geminiLiveProps.isLiveStreaming]);

  // Fetch 11 Agents from backend API
  const fetchAgents = async () => {
    setLoading(true);
    setError(null);
    try {
      const resp = await fetch('/api/agents');
      if (!resp.ok) {
        throw new Error(`Code HTTP ${resp.status}`);
      }
      const data = await resp.json();
      const list = data.agents || [];
      setAgents(list);

      // Default select first agent
      if (list.length > 0 && !selectedAgent) {
        setSelectedAgent(list[0]);
      }
    } catch (err) {
      console.error('Failed to load agents:', err);
      setError(`Impossible de charger la liste des agents depuis le backend. (${err.message})`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAgents();
  }, []);

  const handleSelectAgent = (agent) => {
    setSelectedAgent(agent);
    chatProps.clearMessages();
  };

  const handleLaunchLive = () => {
    if (selectedAgent) {
      setViewMode('live');
      if (geminiLiveProps.isConnected && !geminiLiveProps.isLiveStreaming) {
        geminiLiveProps.startMicStreaming();
      }
    }
  };

  const handleReturnToBuilder = () => {
    setViewMode('builder');
  };

  return (
    <div className="min-h-screen text-slate-900 flex flex-col relative transition-all duration-300">
      
      {/* Google Luminous Aurora Fluid Background Engine */}
      <div className="aurora-container">
        <div className="aurora-blob aurora-blob-1" />
        <div className="aurora-blob aurora-blob-2" />
        <div className="aurora-blob aurora-blob-3" />
        <div className="aurora-blob aurora-blob-4" />
        <div className="aurora-blur-overlay" />
      </div>

      {/* App Header */}
      <Header
        selectedAgent={selectedAgent}
        agentsCount={agents.length}
        autoSpeechEnabled={speechProps.autoSpeechEnabled}
        setAutoSpeechEnabled={speechProps.setAutoSpeechEnabled}
        isSpeaking={geminiLiveProps.isSpeaking}
        onOpenSettings={() => setIsSettingsOpen(true)}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col gap-6 relative z-10">
        
        {loading ? (
          <div className="flex-1 flex flex-col items-center justify-center p-12 text-slate-600">
            <Loader2 className="size-8 animate-spin text-[#0B57D0] mb-3" />
            <p className="text-sm font-semibold">Chargement du Workspace Google & des 11 Agents BigQuery...</p>
          </div>
        ) : error ? (
          <div className="p-6 rounded-2xl bg-white/95 border border-rose-200 text-rose-700 text-center max-w-lg mx-auto my-12 shadow-md">
            <p className="text-sm font-semibold mb-3">{error}</p>
            <button
              type="button"
              onClick={fetchAgents}
              className="px-4 py-2 rounded-xl bg-rose-600 text-white text-xs font-semibold hover:bg-rose-500 transition-all flex items-center gap-2 mx-auto shadow-xs"
            >
              <RefreshCw className="size-4" />
              Réessayer la connexion
            </button>
          </div>
        ) : viewMode === 'builder' ? (
          /* Page 1: Gemini Enterprise Luminous Aurora Landing Page with Live Voice */
          <AgentBuilder
            agents={agents}
            selectedAgent={selectedAgent}
            onSelectAgent={handleSelectAgent}
            onLaunchLive={handleLaunchLive}
            geminiLiveProps={geminiLiveProps}
            onSendMessage={(text) => {
              chatProps.sendMessage(text);
              if (geminiLiveProps.isConnected) {
                geminiLiveProps.sendLivePrompt(text);
              }
            }}
          />
        ) : (
          /* Page 2: Live Experience (Data Canvas Showcase & Chroma Orb) */
          <LiveCanvas
            agents={agents}
            selectedAgent={selectedAgent}
            onSelectAgent={handleSelectAgent}
            onReturnToBuilder={handleReturnToBuilder}
            messages={chatProps.messages}
            isStreaming={chatProps.isStreaming || geminiLiveProps.isLiveStreaming}
            thoughts={chatProps.thoughts}
            error={chatProps.error || geminiLiveProps.error}
            onSendMessage={(text) => {
              chatProps.sendMessage(text);
              if (geminiLiveProps.isConnected) {
                geminiLiveProps.sendLivePrompt(text);
              }
            }}
            geminiLiveProps={geminiLiveProps}
            voiceProps={geminiLiveProps}
            onResetChat={chatProps.clearMessages}
            screenMode={screenMode}
          />
        )}

      </main>

      {/* Settings Drawer Modal */}
      <SettingsDrawer
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        autoSpeechEnabled={speechProps.autoSpeechEnabled}
        setAutoSpeechEnabled={speechProps.setAutoSpeechEnabled}
        screenMode={screenMode}
        setScreenMode={setScreenMode}
        activeTheme={activeTheme}
        setActiveTheme={setActiveTheme}
        selectedAgent={selectedAgent}
        agentsCount={agents.length}
      />

      {/* Bright Light White Footer */}
      <footer className="w-full py-4 border-t border-slate-200/80 bg-white/80 text-center text-xs text-slate-600 font-medium mt-auto backdrop-blur-md">
        <p>Talk to Data • Google Luminous Aurora • BigData Paris 2026 • Vertex AI Data Agents</p>
      </footer>

    </div>
  );
}

export default App;
