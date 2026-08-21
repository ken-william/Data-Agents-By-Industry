import React, { useState } from 'react';
import { Rocket, Search, Sparkles } from 'lucide-react';
import { ScenarioChips } from './ScenarioChips';
import { getIconComponent, getAgentTheme } from '../utils/themeMap';

export function AgentBuilder({ agents, selectedAgent, onSelectAgent, onLaunchLive }) {
  const [searchFilter, setSearchFilter] = useState('');

  const activeTheme = getAgentTheme(selectedAgent?.theme);
  const ActiveIcon = selectedAgent ? getIconComponent(selectedAgent.id) : Sparkles;

  return (
    <div className="w-full min-h-[78vh] flex flex-col items-center justify-center gap-8 animate-fade-in my-auto py-8 relative px-4">
      
      {/* 1. Hero Headline H1 (Google Sans Flex Typography) */}
      <div className="text-center flex flex-col items-center justify-center max-w-4xl px-4 z-10">
        <div className="flex items-center justify-center gap-3 mb-3">
          <img
            className="size-11 sm:size-13 animate-pulse drop-shadow-md"
            src="https://www.gstatic.com/lamda/images/gemini_sparkle_aurora_33f86dc0c0257da337c63.svg"
            alt="Gemini Sparkle Logo"
          />
          <h2 className="text-3xl sm:text-5xl font-bold tracking-tight text-slate-900 leading-tight font-['Google_Sans_Flex']">
            Talk to <span className="google-gradient-text">Data</span> live using
          </h2>
        </div>

        <h3 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight text-slate-900 font-['Google_Sans_Flex']">
          conversational <span className="google-gradient-text">AI agents</span>.
        </h3>

        <p className="text-slate-600 font-medium text-sm sm:text-base mt-4 max-w-2xl leading-relaxed text-balance">
          Interagissez en langage naturel avec 11 copilotes décisionnels sectoriels directement connectés à vos tables BigQuery.
        </p>
      </div>

      {/* 2. Glassmorphism Search Bar & Round Blue Launch Button */}
      <div className="search-bar-wrapper w-full max-w-2xl px-2 z-10">
        <div className="search-bar-glow" />
        <div className="search-bar-container flex items-center gap-3 py-2.5 px-5">
          <Search className="size-5 text-[#0B57D0] shrink-0 ml-1" />
          
          <input
            type="text"
            placeholder="Posez une question ou sélectionnez un copilote sectoriel..."
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
                : 'bg-slate-300 text-slate-400 cursor-not-allowed border border-slate-300'
            }`}
            title="Lancer l'expérience Live Agent"
          >
            <Rocket className="size-5" />
          </button>
        </div>
      </div>

      {/* 3. Extension Chips (Boutons Auto-Adaptatifs s'adaptant à la longueur du texte) */}
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
