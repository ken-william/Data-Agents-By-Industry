import React, { useState } from 'react';
import { Rocket, Search, Sparkles } from 'lucide-react';
import { ScenarioChips } from './ScenarioChips';
import { getIconComponent, getAgentTheme } from '../utils/themeMap';

export function AgentBuilder({ agents, selectedAgent, onSelectAgent, onLaunchLive }) {
  const [searchFilter, setSearchFilter] = useState('');

  const activeTheme = getAgentTheme(selectedAgent?.theme);
  const ActiveIcon = selectedAgent ? getIconComponent(selectedAgent.id) : Sparkles;

  return (
    <div className="w-full min-h-[80vh] flex flex-col items-center justify-center gap-8 animate-fade-in my-auto py-8 relative">
      
      {/* Floating Cosmic Spectral Googley Orbs */}
      <div className="spectral-orb-1" />
      <div className="spectral-orb-2" />

      {/* 1. Hero Headline H1 (Inter + Instrument Serif Italic with Fluo Text Gradient) */}
      <div className="text-center flex flex-col items-center justify-center max-w-4xl px-4 z-10">
        <div className="flex items-center justify-center gap-3 mb-3">
          <img
            className="w-12 h-12 sm:w-14 sm:h-14 animate-pulse drop-shadow-[0_0_20px_rgba(56,189,248,0.6)]"
            src="https://www.gstatic.com/lamda/images/gemini_sparkle_aurora_33f86dc0c0257da337c63.svg"
            alt="Gemini Sparkle Logo"
          />
          <h2 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-tight">
            Talk to <em className="gradient-serif not-italic">Data</em> live using
          </h2>
        </div>

        <h3 className="text-3xl sm:text-5xl font-extrabold tracking-tight leading-tight">
          <em className="gradient-serif not-italic">conversational AI agents</em>.
        </h3>

        <p className="text-slate-400 font-normal text-base sm:text-lg mt-4 max-w-xl leading-relaxed">
          Interagissez en langage naturel avec 11 copilotes décisionnels sectoriels directement connectés à vos tables BigQuery.
        </p>
      </div>

      {/* 2. Search Bar & Round Neon Launch Button */}
      <div className="search-bar-wrapper w-full max-w-2xl px-2 z-10">
        <div className="search-bar-glow" />
        <div className="search-bar-container flex items-center gap-3 py-2.5 px-5">
          <Search className="w-5 h-5 text-sky-400 shrink-0 ml-1" />
          
          <input
            type="text"
            placeholder="Posez une question ou sélectionnez un scénario ci-dessous..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            className="w-full bg-transparent border-none text-slate-100 placeholder-slate-400 focus:outline-none text-sm sm:text-base font-medium"
          />

          {/* Round Fluo Neon Launch Button */}
          <button
            type="button"
            onClick={onLaunchLive}
            disabled={!selectedAgent}
            className={`w-11 h-11 rounded-full flex items-center justify-center text-white shrink-0 shadow-[0_0_25px_rgba(56,189,248,0.4)] transition-all transform hover:scale-105 active:scale-95 ${
              selectedAgent
                ? 'bg-gradient-to-r from-sky-400 via-indigo-500 to-fuchsia-500 hover:shadow-sky-500/50'
                : 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
            }`}
            title="Lancer l'expérience Live Agent"
          >
            <Rocket className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* 3. Scenario Chips (Large Fluo Capsule Bubbles) */}
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
