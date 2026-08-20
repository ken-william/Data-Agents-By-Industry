import React, { useState } from 'react';
import { Rocket, Search, Sparkles } from 'lucide-react';
import { ScenarioChips } from './ScenarioChips';
import { getIconComponent, getAgentTheme } from '../utils/themeMap';

export function AgentBuilder({ agents, selectedAgent, onSelectAgent, onLaunchLive }) {
  const [searchFilter, setSearchFilter] = useState('');

  const activeTheme = getAgentTheme(selectedAgent?.theme);
  const ActiveIcon = selectedAgent ? getIconComponent(selectedAgent.id) : Sparkles;

  return (
    <div className="w-full min-h-[72vh] flex flex-col items-center justify-center gap-6 animate-fade-in my-auto py-8">
      
      {/* 1. Gemini Logo Sparkle Aurora & Greeting */}
      <div className="text-center flex flex-col items-center justify-center">
        <div className="flex items-center justify-center gap-3 mb-2">
          <img
            className="w-11 h-11 sm:w-14 sm:h-14 animate-pulse"
            src="https://www.gstatic.com/lamda/images/gemini_sparkle_aurora_33f86dc0c0257da337c63.svg"
            alt="Gemini Sparkle Logo"
          />
          <h2 className="text-4xl sm:text-6xl font-extrabold tracking-tight bg-gradient-to-r from-sky-400 via-indigo-400 to-fuchsia-500 bg-clip-text text-transparent drop-shadow-lg">
            Talk to Data
          </h2>
        </div>

        <div className="text-slate-300 font-medium text-xl sm:text-2xl mt-1 tracking-wide">
          Explorez vos données à la voix et au texte !
        </div>
      </div>

      {/* 2. Search Bar & Round Neon Launch Button */}
      <div className="search-bar-wrapper w-full max-w-2xl px-2">
        <div className="search-bar-glow" />
        <div className="search-bar-container flex items-center gap-3 py-2 px-4 bg-[#0F172A]/90 border border-slate-700/80 rounded-full shadow-[0_10px_30px_rgba(0,0,0,0.5)] backdrop-blur-2xl">
          <Search className="w-5 h-5 text-slate-400 shrink-0 ml-1" />
          
          <input
            type="text"
            placeholder="Posez une question ou sélectionnez un scénario ci-dessous..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            className="w-full bg-transparent border-none text-slate-100 placeholder-slate-400 focus:outline-none text-xs sm:text-sm font-medium"
          />

          {/* Round Neon Launch Button */}
          <button
            type="button"
            onClick={onLaunchLive}
            disabled={!selectedAgent}
            className={`w-11 h-11 rounded-full flex items-center justify-center text-white shrink-0 shadow-[0_0_20px_rgba(99,102,241,0.4)] transition-all transform hover:scale-105 active:scale-95 ${
              selectedAgent
                ? 'bg-gradient-to-r from-sky-400 via-indigo-500 to-fuchsia-500 hover:shadow-sky-500/40'
                : 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
            }`}
            title="Lancer l'expérience Live Agent"
          >
            <Rocket className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* 3. Extension Chips (Single-Row Compact Capsule Pills) */}
      <ScenarioChips
        agents={agents}
        selectedAgent={selectedAgent}
        onSelectAgent={onSelectAgent}
        onSendMessage={null}
      />

      {/* 4. Active Agent Discrete Badge */}
      {selectedAgent && (
        <div className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-[#0F172A]/90 border border-slate-800 text-xs text-slate-200 backdrop-blur-xl shadow-md animate-fade-in">
          <ActiveIcon className="w-4 h-4 text-sky-400" />
          <span>Copilote Sélectionné : <strong className="text-white font-bold">{selectedAgent.displayName?.split(' - ')[0]}</strong></span>
          <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-sky-500/10 text-sky-300 border border-sky-500/20 font-semibold">
            {selectedAgent.datasetId}
          </span>
        </div>
      )}

    </div>
  );
}
