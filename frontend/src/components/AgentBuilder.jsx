import React, { useState } from 'react';
import { ArrowRight, Search, Sparkles } from 'lucide-react';
import { ScenarioChips } from './ScenarioChips';
import { getIconComponent, getAgentTheme } from '../utils/themeMap';

export function AgentBuilder({ agents, selectedAgent, onSelectAgent, onLaunchLive }) {
  const [searchFilter, setSearchFilter] = useState('');

  return (
    <div className="w-full min-h-[82vh] flex flex-col items-center justify-center gap-8 animate-fade-in my-auto py-6 relative px-4">
      
      {/* Floating Awwwards / JetAI Glass Card (Reference Image 2 media_1787323076388.png) */}
      <div className="awwwards-card w-full max-w-3xl p-8 sm:p-12 flex flex-col gap-8 shadow-2xl relative overflow-hidden">
        
        {/* Top Decorative Sparkle Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-50 border border-blue-200 text-[#0B57D0] text-xs font-bold w-fit shadow-2xs">
          <Sparkles className="size-3.5 text-[#0B57D0]" />
          <span>Vertex AI Data Agents • BigData Paris 2026</span>
        </div>

        {/* 1. Hero Headline Matching Image 2 (media_1787323076388.png) */}
        <div className="space-y-1 text-left">
          <h2 className="text-4xl sm:text-6xl font-extrabold text-slate-900 tracking-tight leading-tight font-['Google_Sans_Flex']">
            How can I help
          </h2>
          <h3 className="text-3xl sm:text-5xl font-medium text-slate-400 tracking-tight leading-tight font-['Google_Sans']">
            explore your data?
          </h3>
        </div>

        {/* 2. Iconic Search Bar Console Matching Image 2 (media_1787323076388.png) */}
        <div className="w-full flex items-center justify-between gap-3 py-2 border-b border-slate-200/90 focus-within:border-[#0B57D0] transition-all">
          <div className="flex items-center gap-3 flex-1">
            <Search className="size-5 text-slate-400 shrink-0" />
            <input
              type="text"
              placeholder="Ask a question or select a scenario below..."
              value={searchFilter}
              onChange={(e) => setSearchFilter(e.target.value)}
              className="w-full bg-transparent border-none text-slate-900 placeholder-slate-400 focus:outline-none text-base sm:text-lg font-medium font-['Google_Sans']"
            />
          </div>

          {/* Solid Google Blue Arrow Action Button (Image 2 style) */}
          <button
            type="button"
            aria-label="Lancer l'expérience Live Agent"
            onClick={onLaunchLive}
            disabled={!selectedAgent}
            className={`size-11 rounded-full flex items-center justify-center text-white shrink-0 transition-all transform hover:scale-105 active:scale-95 shadow-md ${
              selectedAgent
                ? 'bg-[#0B57D0] hover:bg-blue-800 shadow-blue-900/20'
                : 'bg-slate-300 text-slate-500 cursor-not-allowed'
            }`}
            title="Lancer l'expérience Live Agent"
          >
            <ArrowRight className="size-5" />
          </button>
        </div>

        {/* Subtle Waveform Line Accent */}
        <div className="w-full h-1 bg-gradient-to-r from-transparent via-blue-200 to-transparent rounded-full opacity-60" />

        {/* 3. Scenario Chips (Reference Image 2 media_1787323076388.png) */}
        <div className="w-full">
          <ScenarioChips
            agents={agents}
            selectedAgent={selectedAgent}
            onSelectAgent={onSelectAgent}
            onSendMessage={null}
          />
        </div>

        {/* Footer Subtext */}
        <div className="text-right text-[11px] text-slate-400 font-medium tracking-wide pt-2">
          Powered by Vertex AI & BigQuery Conversational Analytics
        </div>

      </div>

    </div>
  );
}
