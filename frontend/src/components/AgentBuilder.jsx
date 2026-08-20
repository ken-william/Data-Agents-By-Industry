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
  const ActiveIcon = selectedAgent ? getIconComponent(selectedAgent.theme.icon) : Database;

  return (
    <div className="w-full flex flex-col gap-5 animate-fade-in">
      
      {/* Header Banner - Enterprise B2B Clean */}
      <div className="p-5 sm:p-6 rounded-xl bg-[#141417] border border-[#27272a] shadow-lg flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-md bg-zinc-900 border border-zinc-800 text-zinc-300 text-xs font-medium mb-2">
            <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
            <span>AI Quick Builder • Enterprise Multi-Agent Catalog</span>
          </div>

          <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-zinc-50">
            Plateforme Conversational Analytics BigQuery
          </h2>

          <p className="text-xs sm:text-sm text-zinc-400 mt-1 max-w-2xl">
            Sélectionnez un copilote sectoriel pour vous connecter instantanément à sa base de données et à ses tables d'objets GCS.
          </p>
        </div>

        {/* Compact Search Bar */}
        <div className="relative w-full sm:w-64">
          <Search className="w-4 h-4 text-zinc-500 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Filtrer les agents..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 rounded-lg bg-zinc-950 border border-zinc-800 text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-zinc-700"
          />
        </div>
      </div>

      {/* Main Grid: 11 Dense Clean Agent Cards + Control Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        
        {/* Left: 11 Sector Cards (8 cols) */}
        <div className="lg:col-span-8 flex flex-col gap-3">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-400 flex items-center gap-2">
              <span>Catalog Agents ({filteredAgents.length})</span>
            </h3>
          </div>

          {/* Compact Clean Card Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3">
            {filteredAgents.map((agent) => {
              const isSelected = selectedAgent?.id === agent.id;
              const IconComp = getIconComponent(agent.theme.icon);
              const theme = COLOR_THEMES[agent.theme.color] || COLOR_THEMES.indigo;

              return (
                <div
                  key={agent.id}
                  onClick={() => onSelectAgent(agent)}
                  className={`cursor-pointer p-3.5 rounded-xl transition-all duration-200 flex flex-col justify-between ${
                    isSelected
                      ? `bg-[#18181b] border-2 ${theme.border} shadow-md`
                      : 'bg-[#141417] border border-[#27272a] hover:border-zinc-700 hover:bg-[#18181b]/80'
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <div className="p-2 rounded-lg bg-zinc-900 border border-zinc-800 text-zinc-200">
                        <IconComp className="w-4 h-4" />
                      </div>
                      
                      <span className={`text-[10px] px-2 py-0.5 rounded-md font-medium border ${theme.badge}`}>
                        {agent.theme.category}
                      </span>
                    </div>

                    <h4 className="text-xs font-bold text-zinc-50 mb-1 line-clamp-1">
                      {agent.displayName.split(' - ')[0]}
                    </h4>

                    <p className="text-[11px] text-zinc-400 line-clamp-2 leading-relaxed mb-2.5">
                      {agent.description}
                    </p>
                  </div>

                  <div className="flex items-center justify-between text-[10px] pt-2 border-t border-zinc-800/80 text-zinc-500 font-mono">
                    <span className="truncate max-w-[120px]">{agent.datasetId}</span>
                    {isSelected && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right: Selected Agent Connection & Launch Panel (4 cols) */}
        <div className="lg:col-span-4 flex flex-col gap-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-400">
            Connexion & Lancement
          </h3>

          <div className="p-5 rounded-xl bg-[#141417] border border-[#27272a] flex flex-col gap-4 shadow-lg">
            
            {/* Selected Agent Summary */}
            <div className="flex items-start gap-3 pb-3 border-b border-zinc-800">
              <div className="p-2.5 rounded-lg bg-zinc-900 border border-zinc-800 text-zinc-100">
                <ActiveIcon className="w-5 h-5" />
              </div>
              <div className="min-w-0 flex-1">
                <span className="text-[10px] text-zinc-500 font-semibold uppercase tracking-wider block">Agent Sélectionné</span>
                <h4 className="text-sm font-bold text-zinc-50 truncate">
                  {selectedAgent ? selectedAgent.displayName.split(' - ')[0] : 'Aucun'}
                </h4>
                <p className="text-[11px] text-zinc-400 font-mono truncate mt-0.5">
                  {selectedAgent?.datasetId}
                </p>
              </div>
            </div>

            {/* Connection Status Toggle */}
            <div className="flex items-center justify-between p-3 rounded-lg bg-zinc-950 border border-zinc-800">
              <div className="flex items-center gap-2">
                <Database className="w-4 h-4 text-emerald-400" />
                <span className="text-xs font-medium text-zinc-200">Connecter à BigQuery</span>
              </div>

              <button
                type="button"
                onClick={() => setIsConnected(!isConnected)}
                className={`w-10 h-5 rounded-full p-0.5 transition-colors duration-200 ${isConnected ? 'bg-emerald-600' : 'bg-zinc-700'}`}
              >
                <div className={`w-4 h-4 rounded-full bg-white transition-transform duration-200 ${isConnected ? 'translate-x-5' : 'translate-x-0'}`} />
              </button>
            </div>

            {/* Dataplex Governance Tag */}
            <div className="flex items-center gap-2 text-[11px] text-zinc-400 bg-zinc-950 p-2.5 rounded-lg border border-zinc-800">
              <ShieldCheck className="w-4 h-4 text-indigo-400 shrink-0" />
              <span>Dataplex Governance & Lineage Actifs</span>
            </div>

            {/* Launch Button */}
            <button
              onClick={onLaunchLive}
              disabled={!selectedAgent || !isConnected}
              className={`w-full py-3 px-4 rounded-lg font-semibold text-xs sm:text-sm flex items-center justify-center gap-2 transition-all duration-200 ${
                selectedAgent && isConnected
                  ? `${activeTheme.button} shadow-md`
                  : 'bg-zinc-800 text-zinc-500 cursor-not-allowed border border-zinc-700'
              }`}
            >
              <Rocket className="w-4 h-4" />
              <span>Lancer l'Expérience Live</span>
            </button>

          </div>
        </div>

      </div>

    </div>
  );
}
