import React, { useState } from 'react';
import { Sparkles, Database, CheckCircle2, Rocket, ShieldCheck, Search } from 'lucide-react';
import { ScenarioChips } from './ScenarioChips';
import { getIconComponent, getAgentTheme } from '../utils/themeMap';

export function AgentBuilder({ agents, selectedAgent, onSelectAgent, onLaunchLive }) {
  const [isConnected, setIsConnected] = useState(true);
  const [searchFilter, setSearchFilter] = useState('');

  const filteredAgents = agents.filter(a => {
    const q = searchFilter.toLowerCase();
    const nameMatch = a.displayName ? a.displayName.toLowerCase().includes(q) : false;
    const catMatch = a.theme && a.theme.category ? a.theme.category.toLowerCase().includes(q) : false;
    return nameMatch || catMatch;
  });

  const activeTheme = getAgentTheme(selectedAgent?.theme);
  const ActiveIcon = selectedAgent ? getIconComponent(selectedAgent.id) : Database;

  return (
    <div className="w-full flex flex-col gap-6 animate-fade-in">
      
      {/* Gemini Header & Greeting - Exact Reproduction */}
      <div className="fixed-content text-center my-4 flex flex-col items-center justify-center">
        <div className="flex items-center justify-center gap-3 mb-1">
          <img
            className="w-9 h-9 animate-pulse"
            src="https://www.gstatic.com/lamda/images/gemini_sparkle_aurora_33f86dc0c0257da337c63.svg"
            alt="Gemini Sparkle Logo"
          />
          <h2 className="text-3xl sm:text-4xl font-bold tracking-tight bg-gradient-to-r from-[#4285f4] to-[#d96570] bg-clip-text text-transparent">
            Talk to Data
          </h2>
        </div>

        <div className="greeting-prompt text-slate-400 font-normal text-xl sm:text-2xl">
          Let's get some work done!
        </div>
      </div>

      {/* Gemini Search Bar Wrapper with Radial Glow */}
      <div className="search-bar-wrapper">
        <div className="search-bar-glow" />
        <div className="search-bar-container flex items-center gap-3">
          <Search className="w-5 h-5 text-slate-400 shrink-0" />
          <input
            type="text"
            placeholder="Filtrer un agent ou poser une question..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            className="w-full bg-transparent border-none text-slate-100 placeholder-slate-400 focus:outline-none text-sm"
          />
          <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 font-mono shrink-0">
            BigQuery
          </span>
        </div>
      </div>

      {/* Gemini Extension Chips Container (11 Scenario Pills) */}
      <ScenarioChips
        agents={agents}
        selectedAgent={selectedAgent}
        onSelectAgent={onSelectAgent}
        onSendMessage={null}
      />

      {/* Main Grid: 11 Dense Clean Agent Cards + Control Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 mt-2">
        
        {/* Left: 11 Sector Cards (8 cols) */}
        <div className="lg:col-span-8 flex flex-col gap-3">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2">
              <span>Catalogue d'Agents ({filteredAgents.length})</span>
            </h3>
          </div>

          {/* Compact Clean Card Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3.5">
            {filteredAgents.map((agent) => {
              const isSelected = selectedAgent?.id === agent.id;
              const IconComp = getIconComponent(agent.id);
              const theme = getAgentTheme(agent.theme);

              return (
                <div
                  key={agent.id}
                  onClick={() => onSelectAgent(agent)}
                  className={`cursor-pointer p-4 rounded-2xl transition-all duration-200 flex flex-col justify-between ${
                    isSelected
                      ? 'agent-card-active scale-[1.01]'
                      : 'agent-card hover:border-slate-700'
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-2.5">
                      <div className={`p-2 rounded-lg bg-slate-950 border border-slate-800 ${theme.text}`}>
                        <IconComp className="w-4 h-4" />
                      </div>
                      
                      <span className={`text-[10px] px-2 py-0.5 rounded-lg font-medium border ${theme.badge}`}>
                        {theme.category}
                      </span>
                    </div>

                    <h4 className="text-xs font-bold text-slate-50 mb-1 line-clamp-1">
                      {agent.displayName ? agent.displayName.split(' - ')[0] : agent.id}
                    </h4>

                    <p className="text-[11px] text-slate-400 line-clamp-2 leading-relaxed mb-3">
                      {agent.description}
                    </p>
                  </div>

                  <div className="flex items-center justify-between text-[10px] pt-2 border-t border-slate-800/80 text-slate-500 font-mono">
                    <span className="truncate max-w-[130px] opacity-70">{agent.datasetId}</span>
                    {isSelected && <CheckCircle2 className="w-3.5 h-3.5 text-sky-400" />}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right: Selected Agent Connection & Launch Panel (4 cols) */}
        <div className="lg:col-span-4 flex flex-col gap-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Connexion & Lancement
          </h3>

          <div className="p-5 rounded-2xl bento-card flex flex-col gap-4 shadow-xl">
            
            {/* Selected Agent Summary */}
            <div className="flex items-start gap-3 pb-3 border-b border-slate-800">
              <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-sky-400">
                <ActiveIcon className="w-5 h-5" />
              </div>
              <div className="min-w-0 flex-1">
                <span className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider block">Agent Sélectionné</span>
                <h4 className="text-sm font-bold text-slate-50 truncate">
                  {selectedAgent ? selectedAgent.displayName.split(' - ')[0] : 'Aucun'}
                </h4>
                <p className="text-[11px] text-slate-400 font-mono truncate mt-0.5">
                  {selectedAgent?.datasetId}
                </p>
              </div>
            </div>

            {/* Connection Status Toggle */}
            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-950 border border-slate-800">
              <div className="flex items-center gap-2">
                <Database className="w-4 h-4 text-emerald-400" />
                <span className="text-xs font-medium text-slate-200">Connecter à BigQuery</span>
              </div>

              <button
                type="button"
                onClick={() => setIsConnected(!isConnected)}
                className={`w-10 h-5 rounded-full p-0.5 transition-colors duration-200 ${isConnected ? 'bg-sky-500' : 'bg-slate-700'}`}
              >
                <div className={`w-4 h-4 rounded-full bg-white transition-transform duration-200 ${isConnected ? 'translate-x-5' : 'translate-x-0'}`} />
              </button>
            </div>

            {/* Dataplex Governance Tag */}
            <div className="flex items-center gap-2 text-[11px] text-slate-400 bg-slate-950 p-2.5 rounded-lg border border-slate-800">
              <ShieldCheck className="w-4 h-4 text-sky-400 shrink-0" />
              <span>Dataplex Governance & Lineage Actifs</span>
            </div>

            {/* Launch Button */}
            <button
              onClick={onLaunchLive}
              disabled={!selectedAgent || !isConnected}
              className={`w-full py-3 px-4 rounded-lg font-semibold text-xs sm:text-sm flex items-center justify-center gap-2 transition-all duration-200 ${
                selectedAgent && isConnected
                  ? activeTheme.button
                  : 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
              }`}
            >
              <Rocket className="w-4 h-4" />
              <span>🚀 LANCER L'EXPÉRIENCE LIVE</span>
            </button>

          </div>
        </div>

      </div>

    </div>
  );
}
