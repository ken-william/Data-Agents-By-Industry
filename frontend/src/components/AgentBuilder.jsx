import React from 'react';
import { Sparkles, Database, CheckCircle2, Rocket, ShieldCheck } from 'lucide-react';
import { AgentCarousel } from './AgentCarousel';
import { getIconComponent, getAgentTheme } from '../utils/themeMap';

export function AgentBuilder({ agents, selectedAgent, onSelectAgent, onLaunchLive }) {
  const activeTheme = getAgentTheme(selectedAgent?.theme);
  const ActiveIcon = selectedAgent ? getIconComponent(selectedAgent.id) : Database;

  return (
    <div className="w-full flex flex-col gap-6 animate-fade-in">
      
      {/* Header Banner - Google Light Workspace (NotebookLM Style) */}
      <div className="p-6 sm:p-8 rounded-3xl bg-white border border-slate-200 shadow-sm relative overflow-hidden flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
        
        {/* Subtle Ambient Gradient Backdrop */}
        <div className="absolute inset-0 bg-gradient-to-r from-blue-50/50 via-slate-50 to-indigo-50/40 -z-10 pointer-events-none" />

        <div className="max-w-3xl">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold mb-3">
            <Sparkles className="w-3.5 h-3.5 text-blue-600" />
            <span>Google Workspace • BigData Paris 2026</span>
          </div>

          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
            Let's get some work done!
          </h2>

          <p className="text-xs sm:text-sm text-slate-600 mt-1 leading-relaxed">
            Bienvenue sur votre espace de travail décisionnel multi-agents. Sélectionnez une scène ou un copilote ci-dessous pour lancer votre analyse BigQuery à la voix et au texte.
          </p>
        </div>

        {/* Big Launch Button */}
        <div className="shrink-0">
          <button
            onClick={onLaunchLive}
            disabled={!selectedAgent}
            className="py-3.5 px-6 rounded-2xl font-bold text-sm bg-blue-600 hover:bg-blue-700 text-white shadow-md transition-all duration-200 flex items-center gap-2 transform hover:scale-[1.02]"
          >
            <Rocket className="w-4 h-4" />
            <span>Lancer l'Espace Live</span>
          </button>
        </div>
      </div>

      {/* NotebookLM Style Horizontal Scene Carousel */}
      <AgentCarousel
        agents={agents}
        selectedAgent={selectedAgent}
        onSelectAgent={onSelectAgent}
      />

      {/* Selected Agent Quick Detail Banner */}
      {selectedAgent && (
        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm flex items-center justify-between gap-4">
          <div className="flex items-center gap-3.5">
            <div className={`p-3 rounded-xl ${activeTheme.iconBg}`}>
              <ActiveIcon className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-slate-900">
                  {selectedAgent.displayName}
                </h3>
                <span className="text-[11px] px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-medium">
                  • Connecté
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-0.5">
                Dataset BigQuery : <strong className="font-mono text-slate-700">{selectedAgent.datasetId}</strong>
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 text-xs text-slate-500 bg-slate-50 px-3 py-1.5 rounded-xl border border-slate-200">
            <ShieldCheck className="w-4 h-4 text-blue-600" />
            <span>Dataplex Governance Actif</span>
          </div>
        </div>
      )}

    </div>
  );
}
