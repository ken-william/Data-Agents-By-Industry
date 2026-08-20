import React, { useState } from 'react';
import { Rocket, Search, Sparkles, Database } from 'lucide-react';
import { ScenarioChips } from './ScenarioChips';
import { getIconComponent, getAgentTheme } from '../utils/themeMap';

export function AgentBuilder({ agents, selectedAgent, onSelectAgent, onLaunchLive }) {
  const [searchFilter, setSearchFilter] = useState('');

  const activeTheme = getAgentTheme(selectedAgent?.theme);
  const ActiveIcon = selectedAgent ? getIconComponent(selectedAgent.id) : Sparkles;

  return (
    <div className="w-full min-h-[75vh] flex flex-col items-center justify-center gap-6 animate-fade-in my-auto py-6 relative">
      
      {/* Background Noise Grain Overlay */}
      <div className="grain" />

      {/* 1. Sparkle Badge */}
      <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900/80 border border-sky-500/20 text-xs font-medium text-slate-300 backdrop-blur-md shadow-xs">
        <Sparkles className="w-4 h-4 text-sky-400" />
        <span>Interactive Analytics Infrastructure</span>
      </div>

      {/* 2. Hero Greeting with Mixed Typography (Inter + Instrument Serif italic) */}
      <div className="text-center flex flex-col items-center justify-center max-w-3xl px-4">
        <h2 className="text-4xl sm:text-6xl font-bold tracking-tight text-white leading-tight">
          Talk to <em className="font-['Instrument_Serif'] italic font-normal text-slate-300 not-italic">Data</em> live using
        </h2>
        <h3 className="text-3xl sm:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-400 tracking-tight mt-1">
          conversational AI agents.
        </h3>

        <p className="text-slate-400 font-normal text-sm sm:text-base mt-3 max-w-xl leading-relaxed">
          Interagissez en langage naturel avec 11 copilotes décisionnels sectoriels directement connectés à vos tables BigQuery.
        </p>
      </div>

      {/* 3. Search Bar & Round Liquid-Glass Launch Button */}
      <div className="search-bar-wrapper w-full max-w-2xl px-2 mt-2">
        <div className="search-bar-glow" />
        <div className="search-bar-container flex items-center gap-3 py-2 px-4">
          <Search className="w-5 h-5 text-slate-400 shrink-0 ml-1" />
          
          <input
            type="text"
            placeholder="Posez une question ou sélectionnez un scénario ci-dessous..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            className="w-full bg-transparent border-none text-slate-100 placeholder-slate-400 focus:outline-none text-xs sm:text-sm font-medium"
          />

          {/* Round Liquid-Glass Launch Button */}
          <button
            type="button"
            onClick={onLaunchLive}
            disabled={!selectedAgent}
            className={`w-10 h-10 rounded-full flex items-center justify-center text-white shrink-0 transition-all ${
              selectedAgent
                ? 'btn-glass bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-600 border-sky-400/50 shadow-[0_0_20px_rgba(56,189,248,0.3)]'
                : 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
            }`}
            title="Lancer l'expérience Live Agent"
          >
            <Rocket className="w-4.5 h-4.5" />
          </button>
        </div>
      </div>

      {/* 4. Extension Chips (Single-Row Liquid-Glass Capsules) */}
      <ScenarioChips
        agents={agents}
        selectedAgent={selectedAgent}
        onSelectAgent={onSelectAgent}
        onSendMessage={null}
      />

      {/* 5. Active Agent Discrete Badge */}
      {selectedAgent && (
        <div className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-slate-900/80 border border-slate-700/80 text-xs text-slate-200 backdrop-blur-xl shadow-md animate-fade-in mt-1">
          <ActiveIcon className="w-4 h-4 text-sky-400" />
          <span>Copilote Sélectionné : <strong className="text-white font-bold">{selectedAgent.displayName?.split(' - ')[0]}</strong></span>
          <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-sky-500/10 text-sky-300 border border-sky-500/20 font-semibold font-mono">
            {selectedAgent.datasetId}
          </span>
        </div>
      )}

    </div>
  );
}
