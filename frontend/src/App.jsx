import React, { useState, useEffect, useCallback } from 'react';
import { Header } from './components/Header';
import { AgentBuilder } from './components/AgentBuilder';
import { LiveCanvas } from './components/LiveCanvas';
import { SettingsDrawer } from './components/SettingsDrawer';
import { useSpeech } from './hooks/useSpeech';
import { useAgentChat } from './hooks/useAgentChat';
import { Loader2, RefreshCw } from 'lucide-react';

export function App() {
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [viewMode, setViewMode] = useState('builder'); // 'builder' (Phase 1) vs 'live' (Phase 2)
  const [screenMode, setScreenMode] = useState('showcase'); // 'showcase' (Écran A) vs 'controller' (Écran B)
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Read ?screen= URL parameter on initial load
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const screenParam = params.get('screen');
    if (screenParam === 'showcase' || screenParam === 'controller') {
      setScreenMode(screenParam);
    }
  }, []);

  // Voice recognition transcript state
  const [micTranscript, setMicTranscript] = useState('');
  const handleTranscript = useCallback((text) => {
    setMicTranscript(text);
  }, []);

  const speechProps = useSpeech(handleTranscript);
  const chatProps = useAgentChat(selectedAgent, speechProps.speakText);

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
    speechProps.stopSpeaking();
  };

  const handleLaunchLive = () => {
    if (selectedAgent) {
      setViewMode('live');
    }
  };

  const handleReturnToBuilder = () => {
    setViewMode('builder');
    speechProps.stopSpeaking();
  };

  return (
    <div className="min-h-screen google-aurora-bg text-slate-100 flex flex-col relative transition-all duration-300">
      
      {/* App Header */}
      <Header
        selectedAgent={selectedAgent}
        agentsCount={agents.length}
        autoSpeechEnabled={speechProps.autoSpeechEnabled}
        setAutoSpeechEnabled={speechProps.setAutoSpeechEnabled}
        isSpeaking={speechProps.isSpeaking}
        onOpenSettings={() => setIsSettingsOpen(true)}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col gap-6 relative z-10">
        
        {loading ? (
          <div className="flex-1 flex flex-col items-center justify-center p-12 text-slate-400">
            <Loader2 className="w-8 h-8 animate-spin text-sky-400 mb-3" />
            <p className="text-sm font-medium">Chargement du Workspace Google & des 11 Agents BigQuery...</p>
          </div>
        ) : error ? (
          <div className="p-6 rounded-2xl bg-slate-900 border border-rose-500/40 text-rose-300 text-center max-w-lg mx-auto my-12 shadow-xl">
            <p className="text-sm font-semibold mb-3">{error}</p>
            <button
              type="button"
              onClick={fetchAgents}
              className="px-4 py-2 rounded-xl bg-rose-600 text-white text-xs font-semibold hover:bg-rose-500 transition-all flex items-center gap-2 mx-auto"
            >
              <RefreshCw className="w-4 h-4" />
              Réessayer la connexion
            </button>
          </div>
        ) : viewMode === 'builder' ? (
          /* Phase 1: Gemini Minimalist Landing Page */
          <AgentBuilder
            agents={agents}
            selectedAgent={selectedAgent}
            onSelectAgent={handleSelectAgent}
            onLaunchLive={handleLaunchLive}
          />
        ) : (
          /* Phase 2: Live Experience (Interactive Bento Grid Board) */
          <LiveCanvas
            selectedAgent={selectedAgent}
            onReturnToBuilder={handleReturnToBuilder}
            messages={chatProps.messages}
            isStreaming={chatProps.isStreaming}
            thoughts={chatProps.thoughts}
            error={chatProps.error}
            onSendMessage={chatProps.sendMessage}
            voiceProps={{
              ...speechProps,
              transcript: micTranscript
            }}
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
        selectedAgent={selectedAgent}
        agentsCount={agents.length}
      />

      {/* Footer */}
      <footer className="w-full py-4 border-t border-slate-800/80 bg-[#020617]/60 text-center text-xs text-slate-500 mt-auto backdrop-blur-md">
        <p>Talk to Data • Google Fluid Blue Aurora • BigData Paris 2026 • Vertex AI Data Agents</p>
      </footer>

    </div>
  );
}

export default App;
