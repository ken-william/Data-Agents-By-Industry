import React, { useState } from 'react';
import { Rocket, Search, Sparkles } from 'lucide-react';
import { ScenarioChips } from './ScenarioChips';
import { getIconComponent, getAgentTheme } from '../utils/themeMap';

export function AgentBuilder({ agents, selectedAgent, onSelectAgent, onLaunchLive }) {
  const [searchFilter, setSearchFilter] = useState('');

  const activeTheme = getAgentTheme(selectedAgent?.theme);
  const ActiveIcon = selectedAgent ? getIconComponent(selectedAgent.id) : Sparkles;

  return (
    <div className="w-full min-h-[78vh] flex flex-col items-center justify-center gap-8 animate-fade-in my-auto py-8 relative">
      
      {/* 1. Hero Greeting Title */}
      <div className="text-center flex flex-col items-center justify-center max-w-4xl px-4 z-10">
        <div className="flex items-center justify-center gap-3 mb-2">
          <img
            className="size-12 sm:size-14 animate-pulse drop-shadow-md"
            src="https://www.gstatic.com/lamda/images/gemini_sparkle_aurora_33f86dc0c0257da337c63.svg"
            alt="Gemini Sparkle Logo"
          />
          <h2 className="text-4xl sm:text-6xl font-bold tracking-tight text-white leading-tight">
            Talk to <em className="gradient-serif not-italic">Data</em>
          </h2>
        </div>

        <div className="text-blue-100 font-medium text-xl sm:text-2xl mt-1 tracking-wide drop-shadow-xs">
          Let's get some work done!
        </div>
      </div>

      {/* 2. Glassmorphism Search Bar & Round Blue Launch Button */}
      <div className="search-bar-wrapper w-full max-w-2xl px-2 z-10">
        <div className="search-bar-glow" />
        <div className="search-bar-container flex items-center gap-3 py-2.5 px-5">
          <Search className="size-5 text-blue-600 shrink-0 ml-1" />
          
          <input
            type="text"
            placeholder="Posez une question ou sélectionnez un copilote sectoriel..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            className="w-full bg-transparent border-none text-slate-900 placeholder-slate-400 focus:outline-none text-sm sm:text-base font-medium"
          />

          {/* Round Blue Launch Button */}
          <button
            type="button"
            aria-label="Lancer l'expérience Live Agent"
            onClick={onLaunchLive}
            disabled={!selectedAgent}
            className={`size-11 rounded-full flex items-center justify-center text-white shrink-0 shadow-lg transition-all transform hover:scale-105 active:scale-95 ${
              selectedAgent
                ? 'bg-[#1A56DB] hover:bg-blue-800 shadow-blue-900/30'
                : 'bg-slate-300 text-slate-400 cursor-not-allowed border border-slate-300'
            }`}
            title="Lancer l'expérience Live Agent"
          >
            <Rocket className="size-5" />
          </button>
        </div>
      </div>

      {/* 3. Extension Chips (Puces des 11 Agents Sectoriels Métier) */}
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
