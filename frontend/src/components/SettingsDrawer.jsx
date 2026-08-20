import React from 'react';
import { X, Settings, Volume2, ShieldCheck, Database, Sliders, Monitor, Smartphone, ExternalLink, Check } from 'lucide-react';

export function SettingsDrawer({
  isOpen,
  onClose,
  autoSpeechEnabled,
  setAutoSpeechEnabled,
  screenMode,
  setScreenMode,
  selectedAgent,
  agentsCount
}) {
  if (!isOpen) return null;

  const openNewTabMode = (mode) => {
    const url = new URL(window.location.href);
    url.searchParams.set('screen', mode);
    window.open(url.toString(), '_blank');
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/60 backdrop-blur-md flex justify-end animate-fade-in">
      
      <div className="w-full max-w-md bg-[#070F2B] border-l border-slate-800 h-full shadow-2xl p-6 flex flex-col justify-between overflow-y-auto">
        
        <div className="flex flex-col gap-6">
          
          {/* Header */}
          <div className="flex items-center justify-between pb-4 border-b border-slate-800">
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-sky-400">
                <Settings className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-50">
                Paramètres & Déploiement
              </h3>
            </div>

            <button
              type="button"
              onClick={onClose}
              className="p-1.5 rounded-xl hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Section 1: Configuration Mode Écran A (Showcase) / Écran B (Contrôleur) */}
          <div className="flex flex-col gap-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Monitor className="w-3.5 h-3.5 text-sky-400" />
              Mode d'Affichage Écran (Dual Screen)
            </h4>

            <div className="grid grid-cols-1 gap-2.5">
              
              {/* Écran A Button */}
              <div
                onClick={() => setScreenMode('showcase')}
                className={`p-3.5 rounded-xl border cursor-pointer transition-all flex items-center justify-between ${
                  screenMode === 'showcase'
                    ? 'bg-slate-900 border-sky-500/80 shadow-[0_0_15px_rgba(56,189,248,0.2)]'
                    : 'bg-slate-950/60 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Monitor className="w-5 h-5 text-sky-400" />
                  <div>
                    <span className="text-xs font-bold text-slate-100 block">Écran A : Showcase (Grand Écran)</span>
                    <span className="text-[11px] text-slate-400">Orbe géant & Data Canvas 70% largeur</span>
                  </div>
                </div>

                <div className="flex items-center gap-1">
                  {screenMode === 'showcase' && <Check className="w-4 h-4 text-sky-400 mr-1" />}
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      openNewTabMode('showcase');
                    }}
                    title="Ouvrir Écran A dans un nouvel onglet"
                    className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>

              {/* Écran B Button */}
              <div
                onClick={() => setScreenMode('controller')}
                className={`p-3.5 rounded-xl border cursor-pointer transition-all flex items-center justify-between ${
                  screenMode === 'controller'
                    ? 'bg-slate-900 border-sky-500/80 shadow-[0_0_15px_rgba(56,189,248,0.2)]'
                    : 'bg-slate-950/60 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Smartphone className="w-5 h-5 text-indigo-400" />
                  <div>
                    <span className="text-xs font-bold text-slate-100 block">Écran B : Contrôleur (PC / Tablette)</span>
                    <span className="text-[11px] text-slate-400">Console présentateur & dock fixe anti-bruit</span>
                  </div>
                </div>

                <div className="flex items-center gap-1">
                  {screenMode === 'controller' && <Check className="w-4 h-4 text-sky-400 mr-1" />}
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      openNewTabMode('controller');
                    }}
                    title="Ouvrir Écran B dans un nouvel onglet"
                    className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>

            </div>
          </div>

          {/* Section 2: Restitution Audio & Synthèse Vocale */}
          <div className="flex flex-col gap-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Volume2 className="w-3.5 h-3.5 text-sky-400" />
              Voix & Synthèse Vocale
            </h4>

            <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 flex items-center justify-between">
              <div>
                <span className="text-xs font-semibold text-slate-200 block">Lecture Vocale Automatique (TTS)</span>
                <span className="text-[11px] text-slate-400">Synthèse sonore des réponses de l'agent</span>
              </div>

              <button
                type="button"
                onClick={() => setAutoSpeechEnabled(!autoSpeechEnabled)}
                className={`w-10 h-5 rounded-full p-0.5 transition-colors duration-200 ${
                  autoSpeechEnabled ? 'bg-sky-500' : 'bg-slate-700'
                }`}
              >
                <div className={`w-4 h-4 rounded-full bg-white transition-transform duration-200 ${
                  autoSpeechEnabled ? 'translate-x-5' : 'translate-x-0'
                }`} />
              </button>
            </div>
          </div>

          {/* Section 3: GCP Dataplex & Infrastructure */}
          <div className="flex flex-col gap-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Database className="w-3.5 h-3.5 text-emerald-400" />
              Gouvernance & Infrastructure GCP
            </h4>

            <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2 text-xs">
              <div className="flex items-center justify-between text-slate-300">
                <span>Projet GCP :</span>
                <strong className="font-mono text-sky-400">data-agents-by-industry</strong>
              </div>

              <div className="flex items-center justify-between text-slate-300">
                <span>Nombre d'Agents Déployés :</span>
                <strong className="text-white">{agentsCount} Agents</strong>
              </div>

              <div className="flex items-center gap-2 text-emerald-400 bg-emerald-500/10 p-2.5 rounded-lg border border-emerald-500/20 text-[11px] mt-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Dataplex Governance, Data Lineage & Vertex AI API Actifs</span>
              </div>
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="pt-4 border-t border-slate-800 text-center text-xs text-slate-500">
          Talk to Data • Google Cloud BigData Paris 2026
        </div>

      </div>

    </div>
  );
}
