import React, { useState } from 'react';
import {
  ArrowRight,
  Plus,
  Minus,
  Sparkles,
  Search,
  Database,
  Layers,
  Zap,
  Activity
} from 'lucide-react';
import { ScenarioChips } from './ScenarioChips';
import { getIconComponent, getAgentTheme } from '../utils/themeMap';

export function AgentBuilder({ agents, selectedAgent, onSelectAgent, onLaunchLive }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [openAccordion, setOpenAccordion] = useState('connections');

  const toggleAccordion = (key) => {
    setOpenAccordion(prev => prev === key ? null : key);
  };

  return (
    <div className="w-full max-w-7xl mx-auto py-6 px-4 animate-fade-in my-auto">
      
      {/* 2-Column Editorial Bento Grid (Reference media_1787309819040.png) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
        
        {/* Left Column: Headline, Chips, Search & Accordions (7 Cols) */}
        <div className="lg:col-span-7 flex flex-col justify-between gap-6">
          
          {/* 1. Header Category Tag */}
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-500">
            <span className="size-2 rounded-full bg-blue-600 animate-pulse" />
            <span>The benefit • Vertex AI Data Agents</span>
          </div>

          {/* 2. Editorial Main Headline */}
          <h1 className="text-4xl sm:text-5xl font-extrabold text-slate-900 tracking-tight leading-[1.1] font-['Google_Sans_Flex']">
            Explore our <span className="inline-flex items-center gap-2"><img src="https://www.gstatic.com/lamda/images/gemini_sparkle_aurora_33f86dc0c0257da337c63.svg" className="size-9 inline" alt="Sparkle" /> 11 sector</span> AI copilots.
          </h1>

          {/* 3. Auto-Adaptive Agent Chips */}
          <div className="w-full">
            <ScenarioChips
              agents={agents}
              selectedAgent={selectedAgent}
              onSelectAgent={onSelectAgent}
              onSendMessage={null}
            />
          </div>

          {/* 4. Search Bar Container */}
          <div className="relative w-full">
            <div className="flex items-center gap-3 bg-white border border-slate-200 rounded-full px-5 py-3 shadow-xs">
              <Search className="size-5 text-slate-400 shrink-0" />
              <input
                type="text"
                placeholder="Posez une question décisionnelle ou filtrez les tables BigQuery..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-transparent border-none text-slate-900 placeholder-slate-400 focus:outline-none text-sm font-medium"
              />
            </div>
          </div>

          {/* 5. Accordion Section Cards (Connections & Sector Packages) */}
          <div className="flex flex-col gap-3">
            
            {/* Accordion Item 1: Connections */}
            <div className="editorial-accordion-card">
              <button
                type="button"
                onClick={() => toggleAccordion('connections')}
                className="w-full flex items-center justify-between text-left text-sm font-semibold text-slate-900"
              >
                <div className="flex items-center gap-2.5">
                  <Database className="size-4 text-blue-600" />
                  <span>Connexions BigQuery</span>
                </div>
                {openAccordion === 'connections' ? <Minus className="size-4 text-slate-500" /> : <Plus className="size-4 text-slate-500" />}
              </button>

              {openAccordion === 'connections' && (
                <p className="text-xs text-slate-600 mt-2.5 leading-relaxed">
                  11 datasets métier connectés avec schémas normalisés, clés primaires et vues analytiques optimisées en temps réel.
                </p>
              )}
            </div>

            {/* Accordion Item 2: Sector Package */}
            <div className="editorial-accordion-card">
              <button
                type="button"
                onClick={() => toggleAccordion('package')}
                className="w-full flex items-center justify-between text-left text-sm font-semibold text-slate-900"
              >
                <div className="flex items-center gap-2.5">
                  <Layers className="size-4 text-emerald-600" />
                  <span>Packs Décisionnels Sectoriels</span>
                </div>
                {openAccordion === 'package' ? <Minus className="size-4 text-slate-500" /> : <Plus className="size-4 text-slate-500" />}
              </button>

              {openAccordion === 'package' && (
                <p className="text-xs text-slate-600 mt-2.5 leading-relaxed">
                  Une collection complète d'agents IA conversationnels personnalisés pour chaque industrie (Finance, Santé, RH, 5G, Retards SNCF, Stades VIP).
                </p>
              )}
            </div>

          </div>

        </div>

        {/* Right Column: Editorial Bento Poster & Primary CTA Button (5 Cols) */}
        <div className="lg:col-span-5 flex flex-col">
          <div className="editorial-bento-card p-7 flex flex-col justify-between h-full gap-6">
            
            {/* Top Info Header */}
            <div>
              <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
                <Activity className="size-4 text-orange-500" />
                <span>BIGDATA — 2026</span>
              </div>

              <p className="text-xs text-slate-500 leading-relaxed max-w-sm font-medium">
                Smart features designed to move with your enterprise data — fast, flexible, and built for everyday action.
              </p>
            </div>

            {/* Poster Card Visual (Tennis Court Orange Poster style from Reference image) */}
            <div className="relative w-full aspect-[4/3] rounded-2xl overflow-hidden bg-gradient-to-br from-orange-500 via-amber-600 to-rose-600 p-6 flex flex-col justify-between text-white shadow-md group">
              
              {/* Top Pill Tag */}
              <div className="flex justify-end">
                <span className="px-3 py-1 rounded-full bg-white/90 text-slate-900 text-[11px] font-bold shadow-xs">
                  ⚡ Live Agent Active
                </span>
              </div>

              {/* Poster Title */}
              <div className="z-10">
                <h3 className="text-2xl sm:text-3xl font-bold leading-tight font-['Google_Sans_Flex'] text-white">
                  Visionary Precision Play
                </h3>
              </div>

              {/* Floating Stat Badge Overlay */}
              <div className="absolute bottom-4 right-4 bg-white/95 rounded-2xl p-3.5 text-slate-900 shadow-lg border border-white/60 min-w-[130px]">
                <div className="text-[10px] font-semibold text-slate-400">Précision BigQuery</div>
                <div className="text-xl font-bold text-slate-900">98.4%</div>
                <div className="mt-1 px-2 py-0.5 rounded-md bg-cyan-600 text-white text-[10px] font-bold flex items-center gap-1">
                  <Zap className="size-3" />
                  <span>Boost</span>
                </div>
              </div>

            </div>

            {/* Bottom Row: Selected Agent Name + Black Action Button (Join Now! →) */}
            <div className="flex items-center justify-between gap-4 pt-2">
              <div>
                <span className="text-[11px] font-semibold text-slate-400 block">Agent Sélectionné</span>
                <span className="text-xs font-bold text-slate-900">
                  {selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : 'Sully'}
                </span>
              </div>

              {/* Black Capsule CTA Button */}
              <button
                type="button"
                onClick={onLaunchLive}
                disabled={!selectedAgent}
                className="editorial-btn-black text-xs sm:text-sm"
              >
                <span>Commencer →</span>
              </button>
            </div>

          </div>
        </div>

      </div>

    </div>
  );
}
