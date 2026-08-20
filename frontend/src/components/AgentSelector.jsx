import React, { useState } from 'react';
import { Search, CheckCircle2, ChevronRight, Sparkles } from 'lucide-react';
import { getIconComponent, COLOR_THEMES } from '../utils/themeMap';

export function AgentSelector({ agents, selectedAgent, onSelectAgent }) {
  const [searchQuery, setSearchQuery] = useState('');

  const filteredAgents = agents.filter(agent => {
    const q = searchQuery.toLowerCase();
    return (
      agent.displayName.toLowerCase().includes(q) ||
      agent.description.toLowerCase().includes(q) ||
      agent.theme.category.toLowerCase().includes(q)
    );
  });

  return (
    <section className="w-full mb-6">
      
      {/* Header & Search Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            Sélectionnez votre Copilote Sectoriel
            <span className="text-xs px-2 py-0.5 rounded-full font-mono bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              {agents.length} Agents Disponibles
            </span>
          </h2>
          <p className="text-xs text-slate-400">
            Chaque agent est interconnecté à son dataset BigQuery et ses tables d'objets GCS dédiés.
          </p>
        </div>

        {/* Search input */}
        <div className="relative w-full sm:w-64">
          <Search className="absolute left-3 top-2.5 w-4 h-4 text-slate-400" />
          <input
            type="text"
            placeholder="Rechercher par secteur ou cas d'usage..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 rounded-lg bg-slate-900/90 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
          />
        </div>
      </div>

      {/* Grid of Agent Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3.5">
        {filteredAgents.map((agent) => {
          const isSelected = selectedAgent?.id === agent.id;
          const IconComp = getIconComponent(agent.theme.icon);
          const theme = COLOR_THEMES[agent.theme.color] || COLOR_THEMES.indigo;

          return (
            <div
              key={agent.id}
              onClick={() => onSelectAgent(agent)}
              className={`group relative cursor-pointer p-4 rounded-xl transition-all duration-300 ${
                isSelected
                  ? `glass-panel border-2 ${theme.border} ${theme.glow} ring-1 ${theme.ring}`
                  : 'glass-card hover:bg-slate-800/60 border border-slate-800/80 hover:border-slate-700'
              }`}
            >
              
              {/* Card Header: Icon, Category & Selection Badge */}
              <div className="flex items-center justify-between gap-2 mb-2.5">
                <div className={`p-2 rounded-lg ${isSelected ? theme.accentBg : 'bg-slate-800 text-slate-300'} transition-all`}>
                  <IconComp className="w-5 h-5" />
                </div>

                <span className={`text-[11px] px-2 py-0.5 rounded-full border font-medium ${theme.badge}`}>
                  {agent.theme.category}
                </span>

                {isSelected && (
                  <span className="flex items-center gap-1 text-[11px] font-semibold text-emerald-400">
                    <CheckCircle2 className="w-4 h-4" />
                  </span>
                )}
              </div>

              {/* Title & Short Description */}
              <h3 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors line-clamp-1 mb-1">
                {agent.displayName}
              </h3>

              <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-3">
                {agent.description}
              </p>

              {/* Card Footer: Dataset badge & launch prompt */}
              <div className="flex items-center justify-between text-[11px] pt-2 border-t border-slate-800/60">
                <span className="font-mono text-slate-500 truncate max-w-[140px]">
                  {agent.datasetId}
                </span>

                <span className={`font-medium flex items-center gap-1 group-hover:translate-x-0.5 transition-transform ${isSelected ? theme.text : 'text-slate-400'}`}>
                  Lancer
                  <ChevronRight className="w-3.5 h-3.5" />
                </span>
              </div>

            </div>
          );
        })}
      </div>

    </section>
  );
}
