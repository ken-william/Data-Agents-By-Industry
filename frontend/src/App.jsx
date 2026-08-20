import React, { useState, useEffect, useCallback } from 'react';
import { Header } from './components/Header';
import { AgentBuilder } from './components/AgentBuilder';
import { LiveCanvas } from './components/LiveCanvas';
import { useSpeech } from './hooks/useSpeech';
import { useAgentChat } from './hooks/useAgentChat';
import { COLOR_THEMES } from './utils/themeMap';
import { Loader2, RefreshCw } from 'lucide-react';

export function App() {
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [viewMode, setViewMode] = useState('builder'); // 'builder' (Phase 1) vs 'live' (Phase 2)
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  const colorKey = selectedAgent?.theme?.color || 'indigo';
  const theme = COLOR_THEMES[colorKey] || COLOR_THEMES.indigo;

  return (
    <div className={`min-h-screen bg-slate-950 text-slate-100 flex flex-col relative transition-all duration-500 bg-gradient-to-b ${theme.gradient}`}>
      
      {/* Background ambient lighting */}
      <div className="absolute top-0 inset-x-0 h-96 bg-gradient-to-b from-indigo-500/10 via-transparent to-transparent pointer-events-none" />

      {/* App Header */}
      <Header
        selectedAgent={selectedAgent}
        agentsCount={agents.length}
        autoSpeechEnabled={speechProps.autoSpeechEnabled}
        setAutoSpeechEnabled={speechProps.setAutoSpeechEnabled}
        isSpeaking={speechProps.isSpeaking}
        onResetChat={chatProps.clearMessages}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 lg:px-8 py-6 flex flex-col gap-6 relative z-10">
        
        {loading ? (
          <div className="flex-1 flex flex-col items-center justify-center p-12 text-slate-400">
            <Loader2 className="w-8 h-8 animate-spin text-indigo-400 mb-3" />
            <p className="text-sm font-medium">Initialisation du Quick Builder & des 11 Agents BigQuery Vertex AI...</p>
          </div>
        ) : error ? (
          <div className="p-6 rounded-3xl glass-panel border border-rose-500/30 text-rose-300 text-center max-w-lg mx-auto my-12">
            <p className="text-sm font-semibold mb-3">{error}</p>
            <button
              onClick={fetchAgents}
              className="px-4 py-2 rounded-xl bg-rose-600 text-white text-xs font-semibold hover:bg-rose-500 transition-all flex items-center gap-2 mx-auto"
            >
              <RefreshCw className="w-4 h-4" />
              Réessayer la connexion
            </button>
          </div>
        ) : viewMode === 'builder' ? (
          /* Phase 1: AI Quick Builder (Configuration) */
          <AgentBuilder
            agents={agents}
            selectedAgent={selectedAgent}
            onSelectAgent={handleSelectAgent}
            onLaunchLive={handleLaunchLive}
          />
        ) : (
          /* Phase 2: Live Experience (Interactive Bento Grid Game Board) */
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
          />
        )}

      </main>

      {/* Footer */}
      <footer className="w-full py-4 border-t border-slate-900 glass-panel text-center text-xs text-slate-500 mt-auto">
        <p>Talk to Data • AI Quick Builder • Google Cloud BigQuery Conversational Analytics • Vertex AI Data Agents</p>
      </footer>

    </div>
  );
}

export default App;
