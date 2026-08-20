import React, { useState } from 'react';
import { Sparkles, Database, CheckCircle2, Rocket, Server, ChevronRight, Layers, ShieldCheck } from 'lucide-react';
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
    <div className="w-full flex flex-col gap-6 animate-fade-in">
      
      {/* Wizard Header Banner */}
      <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-white/10 bg-gradient-to-r from-slate-900 via-indigo-950/60 to-slate-900 shadow-2xl relative overflow-hidden">
        <div className="max-w-3xl relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-semibold mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Quick Builder • Démo Google Cloud Data & AI</span>
          </div>

          <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white mb-2">
            Configurez votre Expérience Conversational Analytics
          </h2>

          <p className="text-sm text-slate-300 leading-relaxed">
            Sélectionnez un secteur d'activité métier ci-dessous pour connecter instantanément le copilote IA Gemini à sa base BigQuery et ses tables d'objets GCS dédiées.
          </p>
        </div>
      </div>

      {/* Main Builder Grid: Step 1 Select Industry + Step 2 Dataset Status */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left: Step 1 Industry Cards (2 columns) */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          <div className="flex items-center justify-between gap-2">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-indigo-600 text-white text-xs flex items-center justify-center font-bold">1</span>
              Choisissez votre Secteur d'Activité ({agents.length})
            </h3>
            
            <input
              type="text"
              placeholder="Filtrer..."
              value={searchFilter}
              onChange={(e) => setSearchFilter(e.target.value)}
              className="px-3 py-1 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
          </div>

          {/* Lego Soft-Corner Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
            {filteredAgents.map((agent) => {
              const isSelected = selectedAgent?.id === agent.id;
              const IconComp = getIconComponent(agent.theme.icon);
              const theme = COLOR_THEMES[agent.theme.color] || COLOR_THEMES.indigo;

              return (
                <div
                  key={agent.id}
                  onClick={() => onSelectAgent(agent)}
                  className={`cursor-pointer p-4 rounded-3xl transition-all duration-300 flex flex-col justify-between ${
                    isSelected
                      ? `glass-panel border-2 ${theme.border} ${theme.glow} shadow-xl scale-[1.02]`
                      : 'glass-card border border-slate-800/80 hover:border-slate-700 hover:bg-slate-800/50'
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <div className={`p-2.5 rounded-2xl ${isSelected ? theme.accentBg : 'bg-slate-800 text-slate-300'} text-white`}>
                        <IconComp className="w-5 h-5" />
                      </div>
                      
                      <span className={`text-[10px] px-2.5 py-0.5 rounded-full font-medium border ${theme.badge}`}>
                        {agent.theme.category}
                      </span>
                    </div>

                    <h4 className="text-sm font-bold text-white mb-1 line-clamp-1">
                      {agent.displayName}
                    </h4>

                    <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-3">
                      {agent.description}
                    </p>
                  </div>

                  <div className="flex items-center justify-between text-[11px] pt-2.5 border-t border-slate-800/60 text-slate-500 font-mono">
                    <span className="truncate max-w-[130px]">{agent.datasetId}</span>
                    {isSelected && <CheckCircle2 className="w-4 h-4 text-emerald-400" />}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right: Step 2 & 3 Connection & Launch Card */}
        <div className="flex flex-col gap-4">
          
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <span className="w-6 h-6 rounded-full bg-indigo-600 text-white text-xs flex items-center justify-center font-bold">2</span>
            Connexion & Lancement
          </h3>

          <div className={`p-6 rounded-3xl glass-panel border ${activeTheme.border} ${activeTheme.glow} flex flex-col gap-5`}>
            
            {/* Selected Agent Summary */}
            <div className="flex items-center gap-3.5 pb-4 border-b border-slate-800">
              <div className={`p-3 rounded-2xl ${activeTheme.accentBg} text-white shadow-lg`}>
                <ActiveIcon className="w-6 h-6" />
              </div>
              <div>
                <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider">Agent Sélectionné</span>
                <h4 className="text-base font-bold text-white line-clamp-1">
                  {selectedAgent ? selectedAgent.displayName.split(' - ')[0] : 'Aucun'}
                </h4>
                <p className="text-xs text-slate-400 font-mono">
                  {selectedAgent?.datasetId}
                </p>
              </div>
            </div>

            {/* Toggle Switch */}
            <div className="flex items-center justify-between p-3.5 rounded-2xl bg-slate-900/90 border border-slate-800">
              <div className="flex items-center gap-2.5">
                <Database className="w-4 h-4 text-emerald-400" />
                <span className="text-xs font-semibold text-slate-200">Connecter à BigQuery</span>
              </div>

              <button
                type="button"
                onClick={() => setIsConnected(!isConnected)}
                className={`w-12 h-6 rounded-full p-1 transition-colors duration-300 ${isConnected ? 'bg-emerald-500' : 'bg-slate-700'}`}
              >
                <div className={`w-4 h-4 rounded-full bg-white transition-transform duration-300 ${isConnected ? 'translate-x-6' : 'translate-x-0'}`} />
              </button>
            </div>

            {/* Security Badge */}
            <div className="flex items-center gap-2 text-xs text-slate-400 bg-slate-950/60 p-3 rounded-2xl border border-slate-800">
              <ShieldCheck className="w-4 h-4 text-indigo-400 shrink-0" />
              <span>Gouvernance Dataplex & Chiffrement GCP Actifs</span>
            </div>

            {/* Big Launch Button */}
            <button
              onClick={onLaunchLive}
              disabled={!selectedAgent || !isConnected}
              className={`w-full py-4 px-6 rounded-2xl font-bold text-sm sm:text-base flex items-center justify-center gap-3 shadow-2xl transition-all duration-300 transform hover:scale-[1.02] active:scale-95 ${
                selectedAgent && isConnected
                  ? `${activeTheme.button} ${activeTheme.glow}`
                  : 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
              }`}
            >
              <Rocket className="w-5 h-5 animate-bounce" />
              <span>🚀 LANCER L'EXPÉRIENCE LIVE</span>
            </button>

          </div>

        </div>

      </div>

    </div>
  );
}
