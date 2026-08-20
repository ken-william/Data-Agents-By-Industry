import React, { useState } from 'react';
import { Sparkles, Database, CheckCircle2, Rocket, ShieldCheck, Search } from 'lucide-react';
import { getIconComponent, COLOR_THEMES } from '../utils/themeMap';

export function AgentBuilder({ agents, selectedAgent, onSelectAgent, onLaunchLive }) {
  const [isConnected, setIsConnected] = useState(true);
  const [searchFilter, setSearchFilter] = useState('');

  const filteredAgents = agents.filter(a => {
    const q = searchFilter.toLowerCase();
    return a.displayName.toLowerCase().includes(q) || a.theme.category.toLowerCase().includes(q);
  });

  const activeTheme = COLOR_THEMES[selectedAgent?.theme?.color || 'indigo'];
  const ActiveIcon = selectedAgent ? getIconComponent(selectedAgent.id) : Database;

  return (
    <div className="w-full flex flex-col gap-5 animate-fade-in">
      
      {/* Header Banner - Google Fluid Blue */}
      <div className="p-6 rounded-2xl bg-[#0B132B]/70 border border-slate-800/80 backdrop-blur-md shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-[#020617] border border-slate-800 text-slate-300 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5 text-sky-400" />
            <span>Google Cloud Data Agent Kit • BigData Paris 2026</span>
          </div>

          <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-50">
            Plateforme Conversational Analytics Multi-Agents
          </h2>

          <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-2xl">
            Sélectionnez un copilote sectoriel pour vous connecter instantanément à sa base BigQuery et à ses tables d'objets GCS.
          </p>
        </div>

        {/* Search Bar */}
        <div className="relative w-full sm:w-64">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Filtrer les agents..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 rounded-lg bg-[#020617] border border-slate-800 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
        </div>
      </div>

      {/* Main Grid: 11 Dense Clean Agent Cards + Control Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        
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
              const theme = COLOR_THEMES[agent.theme.color] || COLOR_THEMES.indigo;

              return (
                <div
                  key={agent.id}
                  onClick={() => onSelectAgent(agent)}
                  className={`cursor-pointer p-4 rounded-2xl transition-all duration-200 flex flex-col justify-between ${
                    isSelected
                      ? 'bg-[#0F172A] border-2 border-sky-500/50 shadow-[0_0_15px_rgba(14,165,233,0.15)] scale-[1.01]'
                      : 'bg-[#0B132B]/60 border border-slate-800/80 hover:border-slate-700 hover:bg-[#0B132B]/90'
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-2.5">
                      <div className={`p-2 rounded-lg bg-[#020617] border border-slate-800 ${theme.text}`}>
                        <IconComp className="w-4 h-4" />
                      </div>
                      
                      <span className={`text-[10px] px-2 py-0.5 rounded-lg font-medium border ${theme.badge}`}>
                        {agent.theme.category}
                      </span>
                    </div>

                    <h4 className="text-xs font-bold text-slate-50 mb-1 line-clamp-1">
                      {agent.displayName.split(' - ')[0]}
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

          <div className="p-5 rounded-2xl bg-[#0B132B]/70 border border-slate-800/80 backdrop-blur-md flex flex-col gap-4 shadow-xl">
            
            {/* Selected Agent Summary */}
            <div className="flex items-start gap-3 pb-3 border-b border-slate-800">
              <div className="p-2.5 rounded-lg bg-[#020617] border border-slate-800 text-sky-400">
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
            <div className="flex items-center justify-between p-3 rounded-lg bg-[#020617] border border-slate-800">
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
            <div className="flex items-center gap-2 text-[11px] text-slate-400 bg-[#020617] p-2.5 rounded-lg border border-slate-800">
              <ShieldCheck className="w-4 h-4 text-sky-400 shrink-0" />
              <span>Dataplex Governance & Lineage Actifs</span>
            </div>

            {/* Launch Button */}
            <button
              onClick={onLaunchLive}
              disabled={!selectedAgent || !isConnected}
              className={`w-full py-3 px-4 rounded-lg font-semibold text-xs sm:text-sm flex items-center justify-center gap-2 transition-all duration-200 ${
                selectedAgent && isConnected
                  ? `${activeTheme.button} shadow-lg`
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
