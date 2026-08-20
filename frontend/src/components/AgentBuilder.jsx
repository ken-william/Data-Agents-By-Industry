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
      
      {/* 1. Gemini Logo Sparkle Aurora & Greeting (36px / Regular Flex) */}
      <div className="text-center flex flex-col items-center justify-center">
        <div className="flex items-center justify-center gap-3 mb-2">
          <img
            className="w-11 h-11 sm:w-13 sm:h-13 animate-pulse"
            src="https://www.gstatic.com/lamda/images/gemini_sparkle_aurora_33f86dc0c0257da337c63.svg"
            alt="Gemini Sparkle Logo"
          />
          <h2 className="text-3xl sm:text-4xl font-normal tracking-tight bg-gradient-to-r from-[#4285f4] to-[#d96570] bg-clip-text text-transparent">
            Talk to Data
          </h2>
        </div>

        <div className="text-[#757575] font-normal text-xl sm:text-2xl mt-1 tracking-wide">
          Let's get some work done!
        </div>
      </div>

      {/* 2. Search Bar #f0f4f9 & Round Accent Blue Launch Button #0b57d0 */}
      <div className="search-bar-wrapper w-full max-w-2xl px-2">
        <div className="search-bar-glow" />
        <div className="search-bar-container flex items-center gap-3 py-2.5 px-5 bg-[#f0f4f9] border border-slate-200/60 rounded-full shadow-xs">
          <Search className="w-5 h-5 text-[#757575] shrink-0 ml-1" />
          
          <input
            type="text"
            placeholder="Posez une question ou sélectionnez un scénario ci-dessous..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            className="w-full bg-transparent border-none text-[#1f1f1f] placeholder-[#757575] focus:outline-none text-base font-normal"
          />

          {/* Round Material 3 Accent Blue Launch Button (#0b57d0) */}
          <button
            type="button"
            onClick={onLaunchLive}
            disabled={!selectedAgent}
            className={`w-10 h-10 rounded-full flex items-center justify-center text-white shrink-0 shadow-md transition-all transform hover:scale-105 active:scale-95 ${
              selectedAgent
                ? 'bg-[#0b57d0] hover:bg-blue-700 shadow-blue-500/20'
                : 'bg-slate-300 text-slate-500 cursor-not-allowed border border-slate-300'
            }`}
            title="Lancer l'expérience Live Agent"
          >
            <Rocket className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* 3. Extension Chips (Single-Row Material 3 md-menu-item Capsules h-12) */}
      <ScenarioChips
        agents={agents}
        selectedAgent={selectedAgent}
        onSelectAgent={onSelectAgent}
        onSendMessage={null}
      />

      {/* 4. Active Agent Discrete Badge */}
      {selectedAgent && (
        <div className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-white border border-slate-200 text-xs text-[#1f1f1f] shadow-xs animate-fade-in">
          <ActiveIcon className="w-4 h-4 text-[#0b57d0]" />
          <span>Copilote Sélectionné : <strong className="text-[#1f1f1f] font-semibold">{selectedAgent.displayName?.split(' - ')[0]}</strong></span>
          <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-blue-50 text-[#0b57d0] border border-blue-200 font-mono font-medium">
            {selectedAgent.datasetId}
          </span>
        </div>
      )}

    </div>
  );
}
