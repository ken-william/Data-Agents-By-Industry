import React, { useRef, useState } from 'react';
import { ChevronLeft, ChevronRight, Grid, CheckCircle2, Sparkles, X } from 'lucide-react';
import { getIconComponent, getAgentTheme } from '../utils/themeMap';

export function AgentCarousel({ agents, selectedAgent, onSelectAgent }) {
  const scrollRef = useRef(null);
  const [showCatalogModal, setShowCatalogModal] = useState(false);

  const scroll = (direction) => {
    if (scrollRef.current) {
      const scrollAmount = direction === 'left' ? -300 : 300;
      scrollRef.current.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
  };

  return (
    <div className="w-full flex flex-col gap-3">
      
      {/* Carousel Header & Controls */}
      <div className="flex items-center justify-between px-1">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-blue-600" />
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
            Espaces de Travail & Agents Sectoriels ({agents.length})
          </h3>
        </div>

        <div className="flex items-center gap-2">
          {/* Scroll Navigation Arrows */}
          <div className="hidden sm:flex items-center gap-1">
            <button
              onClick={() => scroll('left')}
              className="p-1 rounded-lg bg-white hover:bg-slate-100 border border-slate-200 text-slate-600 transition-colors"
              title="Défiler vers la gauche"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              onClick={() => scroll('right')}
              className="p-1 rounded-lg bg-white hover:bg-slate-100 border border-slate-200 text-slate-600 transition-colors"
              title="Défiler vers la droite"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          {/* Afficher Tout Gallery Modal Trigger */}
          <button
            onClick={() => setShowCatalogModal(true)}
            className="px-2.5 py-1 rounded-lg bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 text-xs font-medium flex items-center gap-1.5 transition-colors shadow-sm"
          >
            <Grid className="w-3.5 h-3.5 text-blue-600" />
            <span>Afficher Tout</span>
          </button>
        </div>
      </div>

      {/* Horizontal Carousel (NotebookLM Card Format h-36 max) */}
      <div
        ref={scrollRef}
        className="flex items-center gap-3.5 overflow-x-auto pb-2 pt-1 px-1 scrollbar-none scroll-smooth"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
      >
        {agents.map((agent) => {
          const isSelected = selectedAgent?.id === agent.id;
          const IconComp = getIconComponent(agent.id);
          const theme = getAgentTheme(agent.theme);

          return (
            <div
              key={agent.id}
              onClick={() => onSelectAgent(agent)}
              className={`shrink-0 w-64 h-36 p-3.5 rounded-2xl cursor-pointer transition-all duration-200 flex flex-col justify-between ${
                isSelected
                  ? 'notebook-card-active'
                  : `notebook-card ${theme.topBorder}`
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className={`p-1.5 rounded-lg ${theme.iconBg}`}>
                    <IconComp className="w-4 h-4" />
                  </div>

                  <span className={`text-[10px] px-2 py-0.5 rounded-md font-medium border ${theme.badge}`}>
                    {theme.category}
                  </span>
                </div>

                <h4 className="text-xs font-bold text-slate-900 line-clamp-1">
                  {agent.displayName ? agent.displayName.split(' - ')[0] : agent.id}
                </h4>

                <p className="text-[11px] text-slate-500 line-clamp-2 leading-relaxed mt-0.5">
                  {agent.description}
                </p>
              </div>

              <div className="flex items-center justify-between text-[10px] pt-1.5 border-t border-slate-100 text-slate-400 font-mono">
                <span className="truncate max-w-[140px]">• Connecté ({agent.datasetId})</span>
                {isSelected && <CheckCircle2 className="w-3.5 h-3.5 text-blue-600" />}
              </div>
            </div>
          );
        })}
      </div>

      {/* Full Catalog Gallery Modal */}
      {showCatalogModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl border border-slate-200 shadow-2xl max-w-4xl w-full max-h-[85vh] overflow-y-auto p-6 flex flex-col gap-5 animate-fade-in">
            
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <Grid className="w-5 h-5 text-blue-600" />
                <h3 className="text-base font-bold text-slate-900">
                  Catalogue Complet des 11 Agents BigQuery ({agents.length})
                </h3>
              </div>

              <button
                onClick={() => setShowCatalogModal(false)}
                className="p-1.5 rounded-xl hover:bg-slate-100 text-slate-500 hover:text-slate-900 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {agents.map((agent) => {
                const isSelected = selectedAgent?.id === agent.id;
                const IconComp = getIconComponent(agent.id);
                const theme = getAgentTheme(agent.theme);

                return (
                  <div
                    key={agent.id}
                    onClick={() => {
                      onSelectAgent(agent);
                      setShowCatalogModal(false);
                    }}
                    className={`p-4 rounded-2xl cursor-pointer transition-all ${
                      isSelected ? 'notebook-card-active' : `notebook-card ${theme.topBorder}`
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className={`p-2 rounded-lg ${theme.iconBg}`}>
                        <IconComp className="w-4 h-4" />
                      </div>
                      <span className={`text-[10px] px-2 py-0.5 rounded-md font-medium border ${theme.badge}`}>
                        {theme.category}
                      </span>
                    </div>

                    <h4 className="text-xs font-bold text-slate-900 mb-1">
                      {agent.displayName}
                    </h4>

                    <p className="text-xs text-slate-500 line-clamp-2 leading-relaxed mb-3">
                      {agent.description}
                    </p>

                    <div className="flex items-center justify-between text-[10px] pt-2 border-t border-slate-100 text-slate-400 font-mono">
                      <span>{agent.datasetId}</span>
                      {isSelected && <CheckCircle2 className="w-4 h-4 text-blue-600" />}
                    </div>
                  </div>
                );
              })}
            </div>

          </div>
        </div>
      )}

    </div>
  );
}
