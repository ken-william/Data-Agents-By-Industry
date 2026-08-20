import React, { useState } from 'react';
import { Rocket, Search, CheckCircle2, Sparkles, Database } from 'lucide-react';
import { ScenarioChips } from './ScenarioChips';
import { getIconComponent, getAgentTheme } from '../utils/themeMap';

export function AgentBuilder({ agents, selectedAgent, onSelectAgent, onLaunchLive }) {
  const [searchFilter, setSearchFilter] = useState('');

  const activeTheme = getAgentTheme(selectedAgent?.theme);
  const ActiveIcon = selectedAgent ? getIconComponent(selectedAgent.id) : Database;

  return (
    <div className="w-full min-h-[72vh] flex flex-col items-center justify-center gap-6 animate-fade-in my-auto py-8">
      
      {/* 1. Gemini Logo Sparkle Aurora & Greeting */}
      <div className="text-center flex flex-col items-center justify-center">
        <div className="flex items-center justify-center gap-3 mb-2">
          <img
            className="w-10 h-10 sm:w-12 sm:h-12 animate-pulse"
            src="https://www.gstatic.com/lamda/images/gemini_sparkle_aurora_33f86dc0c0257da337c63.svg"
            alt="Gemini Sparkle Logo"
          />
          <h2 className="text-4xl sm:text-5xl font-bold tracking-tight bg-gradient-to-r from-[#4285f4] via-[#9b51e0] to-[#d96570] bg-clip-text text-transparent">
            Talk to Data
          </h2>
        </div>

        <div className="text-slate-400 font-normal text-xl sm:text-2xl mt-1 tracking-wide">
          Let's get some work done!
        </div>
      </div>

      {/* 2. Search Bar & Round Blue Launch Button */}
      <div className="search-bar-wrapper w-full max-w-2xl px-2">
        <div className="search-bar-glow" />
        <div className="search-bar-container flex items-center gap-3 py-2 px-4 bg-slate-900/85 border border-slate-700/80 rounded-full shadow-2xl backdrop-blur-md">
          <Search className="w-5 h-5 text-slate-400 shrink-0 ml-1" />
          
          <input
            type="text"
            placeholder="Rechercher un agent ou poser une question..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            className="w-full bg-transparent border-none text-slate-100 placeholder-slate-400 focus:outline-none text-xs sm:text-sm"
          />

          {/* Round Blue Launch Button */}
          <button
            type="button"
            onClick={onLaunchLive}
            disabled={!selectedAgent}
            className={`w-10 h-10 rounded-full flex items-center justify-center text-white shrink-0 shadow-lg transition-all transform hover:scale-105 active:scale-95 ${
              selectedAgent
                ? 'bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 hover:shadow-sky-500/20'
                : 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
            }`}
            title="Lancer l'expérience Live Agent"
          >
            <Rocket className="w-4 h-4" />
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
        <div className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-slate-900/80 border border-slate-800 text-xs text-slate-300 backdrop-blur-md shadow-md animate-fade-in">
          <ActiveIcon className="w-3.5 h-3.5 text-sky-400" />
          <span>Agent Sélectionné : <strong className="text-white font-semibold">{selectedAgent.displayName?.split(' - ')[0]}</strong></span>
          <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
            {selectedAgent.datasetId}
          </span>
        </div>
      )}

    </div>
  );
}
