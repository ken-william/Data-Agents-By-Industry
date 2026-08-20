import React, { useState } from 'react';
import { Rocket, Search, Sparkles, Database, ArrowRight, Activity, Download, Users } from 'lucide-react';
import { ScenarioChips } from './ScenarioChips';
import { getIconComponent, getAgentTheme } from '../utils/themeMap';

export function AgentBuilder({ agents, selectedAgent, onSelectAgent, onLaunchLive }) {
  const [searchFilter, setSearchFilter] = useState('');

  const activeTheme = getAgentTheme(selectedAgent?.theme);
  const ActiveIcon = selectedAgent ? getIconComponent(selectedAgent.id) : Sparkles;

  return (
    <div className="w-full min-h-[82vh] flex flex-col items-center justify-between gap-6 animate-fade-in my-auto py-4 relative">
      
      {/* Background Noise Grain Overlay */}
      <div className="grain" />

      {/* Main Hero Section */}
      <div className="w-full flex flex-col items-center justify-center gap-5 max-w-4xl mx-auto text-center px-4 my-auto">
        
        {/* 1. Badge Vesper.ai */}
        <div className="badge-vesper appear appear--pop" style={{ '--d': '0.22s' }}>
          <svg className="w-4 h-4 text-white drop-shadow-[0_0_3px_rgba(255,255,255,0.45)]" viewBox="0 0 24 24" fill="white">
            <path d="M12 2.6C12.55 2.6 12.88 3.15 13.08 4.7c.62 4.7 1.52 5.6 6.22 6.22 1.55.2 2.1.53 2.1 1.08s-.55.88-2.1 1.08c-4.7.62-5.6 1.52-6.22 6.22-.2 1.55-.53 2.1-1.08 2.1s-.88-.55-1.08-2.1c-.62-4.7-1.52-5.6-6.22-6.22C3.15 12.88 2.6 12.55 2.6 12s.55-.88 2.1-1.08c4.7-.62 5.6-1.52 6.22-6.22C11.12 3.15 11.45 2.6 12 2.6Z"/>
          </svg>
          <span>Operational AI Infrastructure</span>
        </div>

        {/* 2. Hero Headline H1 (Inter + Instrument Serif Italic) */}
        <div className="flex flex-col items-center justify-center space-y-1">
          <h1 className="text-4xl sm:text-6xl font-medium tracking-tight text-white leading-tight appear appear--mask" style={{ '--d': '0.42s' }}>
            Train <em className="font-['Instrument_Serif'] italic font-normal text-[#9a9a9a] not-italic">AI agents</em> on your
          </h1>
          <h1 className="text-4xl sm:text-6xl font-medium tracking-tight text-white leading-tight appear appear--mask" style={{ '--d': '0.62s' }}>
            workflows in minutes.
          </h1>
        </div>

        {/* 3. Lede Subtitle */}
        <p className="text-[#9a9a9a] font-normal text-sm sm:text-base max-w-lg leading-relaxed appear appear--soft" style={{ '--d': '0.82s' }}>
          Deploy adaptive AI agents that learn, execute, and scale operational tasks across your business.
        </p>

        {/* 4. Hero Action Buttons */}
        <div className="flex items-center justify-center gap-3 mt-1 appear" style={{ '--d': '0.96s' }}>
          <button
            type="button"
            onClick={onLaunchLive}
            disabled={!selectedAgent}
            className={`btn btn-solid px-6 py-2.5 font-medium text-xs sm:text-sm flex items-center gap-2 ${
              selectedAgent ? '' : 'opacity-50 cursor-not-allowed'
            }`}
          >
            <span>Start for Free</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            type="button"
            onClick={() => {
              const el = document.getElementById('scenariosContainer');
              if (el) el.scrollIntoView({ behavior: 'smooth' });
            }}
            className="btn btn-ghost px-6 py-2.5 font-medium text-xs sm:text-sm"
          >
            <span>See it in action</span>
          </button>
        </div>

        {/* 5. Search Bar & Round Launch Button */}
        <div className="search-bar-wrapper w-full max-w-2xl px-2 mt-4">
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

            <button
              type="button"
              onClick={onLaunchLive}
              disabled={!selectedAgent}
              className={`w-10 h-10 rounded-full flex items-center justify-center text-white shrink-0 transition-all ${
                selectedAgent
                  ? 'btn btn-solid bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-600 border-sky-400/50 shadow-[0_0_20px_rgba(56,189,248,0.3)] text-slate-900'
                  : 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
              }`}
              title="Lancer l'expérience Live Agent"
            >
              <Rocket className="w-4.5 h-4.5 text-slate-950" />
            </button>
          </div>
        </div>

        {/* 6. Scenario Chips Capsule Navigation */}
        <ScenarioChips
          agents={agents}
          selectedAgent={selectedAgent}
          onSelectAgent={onSelectAgent}
          onSendMessage={null}
        />

        {/* Active Agent Discrete Tag */}
        {selectedAgent && (
          <div className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-slate-900/90 border border-slate-800 text-xs text-slate-200 backdrop-blur-xl shadow-md animate-fade-in">
            <ActiveIcon className="w-4 h-4 text-sky-400" />
            <span>Copilote Sélectionné : <strong className="text-white font-bold">{selectedAgent.displayName?.split(' - ')[0]}</strong></span>
            <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-sky-500/10 text-sky-300 border border-sky-500/20 font-semibold font-mono">
              {selectedAgent.datasetId}
            </span>
          </div>
        )}

      </div>

      {/* 7. Stats Footer Vesper.ai (3 Exact Metrics) */}
      <footer className="stats-footer w-full pt-4 border-t border-slate-900/80">
        
        {/* Metric 1: Dual-pill workflow icon */}
        <div className="stat-item appear appear--stat" style={{ '--d': '1.12s' }}>
          <svg className="w-5 h-5 text-slate-300 shrink-0" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3.4" y="2.6" width="7.2" height="18.8" rx="3.6" fill="rgba(255,255,255,0.4)" />
            <rect x="13.4" y="2.6" width="7.2" height="18.8" rx="3.6" fill="rgba(255,255,255,0.7)" />
            <rect x="9.2" y="10.9" width="5.6" height="2.2" rx="1.1" fill="#4a4a4a" />
          </svg>
          <span className="text-xs sm:text-sm font-medium text-[#d8d8d8]">4.2M+ workflows automated</span>
        </div>

        {/* Metric 2: Download tile icon */}
        <div className="stat-item appear appear--stat" style={{ '--d': '1.28s' }}>
          <div className="w-5 h-5 rounded-md bg-white flex items-center justify-center shrink-0">
            <Download className="w-3.5 h-3.5 text-slate-950 stroke-[2.5]" />
          </div>
          <span className="text-xs sm:text-sm font-medium text-[#d8d8d8]">92% reduction in manual operations</span>
        </div>

        {/* Metric 3: Three avatars icon */}
        <div className="stat-item appear appear--stat" style={{ '--d': '1.44s' }}>
          <svg className="w-9 h-5 shrink-0" viewBox="0 0 40 22">
            <circle cx="10.2" cy="11" r="9.2" fill="#2b2b2b" />
            <ellipse cx="10.2" cy="12.1" rx="4.15" ry="3.7" fill="#f4f4f4" />
            <circle cx="20.2" cy="11" r="9.2" fill="#ffffff" />
            <circle cx="20.2" cy="10" r="1.5" fill="#111" />
            <circle cx="30.2" cy="11" r="9.2" fill="#f26b1d" />
            <text x="30.2" y="15.1" fontSize="12.5" fill="#fff" fontWeight="bold" textAnchor="middle" fontFamily="sans-serif">e</text>
          </svg>
          <span className="text-xs sm:text-sm font-medium text-[#d8d8d8]">180+ operational teams onboarded</span>
        </div>

      </footer>

    </div>
  );
}
