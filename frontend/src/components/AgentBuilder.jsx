import React, { useState } from 'react';
import { Rocket, Search, Sparkles, Mic, MicOff, Volume2 } from 'lucide-react';
import { ScenarioChips } from './ScenarioChips';
import { getIconComponent, getAgentTheme } from '../utils/themeMap';

export function AgentBuilder({
  agents,
  selectedAgent,
  onSelectAgent,
  onLaunchLive,
  geminiLiveProps,
  onSendMessage
}) {
  const [searchFilter, setSearchFilter] = useState('');

  const activeTheme = getAgentTheme(selectedAgent?.theme);
  const ActiveIcon = selectedAgent ? getIconComponent(selectedAgent.id) : Sparkles;

  const isLive = geminiLiveProps?.isConnected;
  const isStreaming = geminiLiveProps?.isLiveStreaming;
  const isSpeaking = geminiLiveProps?.isSpeaking;

  const handleToggleMic = () => {
    if (geminiLiveProps) {
      if (isStreaming) {
        geminiLiveProps.stopMicStreaming();
      } else {
        geminiLiveProps.startMicStreaming();
      }
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (!searchFilter.trim()) return;
    if (onSendMessage) {
      onSendMessage(searchFilter);
    }
    setSearchFilter('');
  };

  return (
    <div className="w-full min-h-[78vh] flex flex-col items-center justify-center gap-6 animate-fade-in my-auto py-6 relative px-4">
      
      {/* 1. Hero Headline with Google Sans Flex + Instrument Serif Metallic Gradient */}
      <div className="text-center flex flex-col items-center justify-center max-w-4xl px-4 z-10">
        
        {/* Live Voice Status Pill */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/80 border border-blue-200/80 shadow-xs mb-4 backdrop-blur-md">
          <span className={`size-2 rounded-full ${isSpeaking ? 'bg-amber-500 animate-ping' : isStreaming ? 'bg-emerald-500 animate-pulse' : 'bg-blue-500'}`} />
          <span className="text-xs font-semibold text-slate-700">
            {isSpeaking
              ? "Gemini Live vous parle..."
              : isStreaming
              ? "Gemini Live à votre écoute (Micro Ouvert)"
              : "Gemini Live Connecté • Parlez ou posez vos questions"}
          </span>
          <button
            type="button"
            onClick={handleToggleMic}
            className={`p-1 rounded-full transition-colors ${isStreaming ? 'text-emerald-600 bg-emerald-50' : 'text-slate-500 hover:text-slate-800'}`}
            title={isStreaming ? "Couper le micro" : "Activer le micro"}
          >
            {isStreaming ? <Mic className="size-3.5" /> : <MicOff className="size-3.5" />}
          </button>
        </div>

        <div className="flex items-center justify-center gap-3 mb-2">
          <img
            className="size-12 sm:size-14 animate-pulse drop-shadow-[0_0_25px_rgba(56,189,248,0.5)]"
            src="https://www.gstatic.com/lamda/images/gemini_sparkle_aurora_33f86dc0c0257da337c63.svg"
            alt="Gemini Sparkle Logo"
          />
          <h2 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-slate-900 leading-tight font-['Google_Sans_Flex']">
            Talk to Data live using
          </h2>
        </div>

        <h3 className="text-3xl sm:text-5xl font-extrabold tracking-tight leading-tight">
          <span className="gradient-metallic">conversational AI agents</span>.
        </h3>

        <p className="text-slate-600 font-medium text-sm sm:text-base mt-3 max-w-xl leading-relaxed text-balance">
          Discutez librement avec votre Orchestrateur Virtuel et explorez 11 copilotes décisionnels connectés à vos tables BigQuery.
        </p>
      </div>

      {/* 2. Iconic Search & Voice Bar */}
      <form onSubmit={handleSearchSubmit} className="search-bar-wrapper w-full max-w-2xl px-2 z-10">
        <div className="search-bar-glow" />
        <div className="search-bar-container flex items-center gap-3 py-2.5 px-5">
          <button
            type="button"
            onClick={handleToggleMic}
            className={`p-1.5 rounded-full transition-all ${
              isStreaming
                ? 'bg-emerald-500 text-white animate-pulse'
                : 'text-[#0B57D0] hover:bg-blue-50'
            }`}
            title={isStreaming ? "Micro actif" : "Cliquer pour parler"}
          >
            <Mic className="size-5" />
          </button>
          
          <input
            type="text"
            placeholder="Posez une question ou demandez d'ouvrir un scénario..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            className="w-full bg-transparent border-none text-slate-900 placeholder-slate-400 focus:outline-none text-sm sm:text-base font-medium font-['Google_Sans']"
          />

          {/* Round Blue Launch Button */}
          <button
            type="button"
            aria-label="Lancer l'expérience Live Agent"
            onClick={onLaunchLive}
            disabled={!selectedAgent}
            className={`size-11 rounded-full flex items-center justify-center text-white shrink-0 shadow-md transition-all transform hover:scale-105 active:scale-95 ${
              selectedAgent
                ? 'bg-[#0B57D0] hover:bg-blue-800 shadow-blue-900/20'
                : 'bg-slate-200 text-slate-400 cursor-not-allowed border border-slate-300'
            }`}
            title="Lancer l'analyse du scénario sélectionné"
          >
            <Rocket className="size-5" />
          </button>
        </div>
      </form>

      {/* 3. Scenario Chips (Compact Pills with Monochrome Icons) */}
      <div className="w-full z-10">
        <ScenarioChips
          agents={agents}
          selectedAgent={selectedAgent}
          onSelectAgent={onSelectAgent}
          onSendMessage={null}
        />
      </div>

    </div>
  );
}
