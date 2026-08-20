import React from 'react';
import { X, Settings, Volume2, ShieldCheck, Database, Sliders, Sparkles, Check } from 'lucide-react';

export function SettingsDrawer({
  isOpen,
  onClose,
  autoSpeechEnabled,
  setAutoSpeechEnabled,
  selectedAgent,
  agentsCount
}) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/30 backdrop-blur-sm flex justify-end">
      
      <div className="w-full max-w-md bg-white border-l border-slate-200 h-full shadow-2xl p-6 flex flex-col justify-between animate-fade-in">
        
        <div className="flex flex-col gap-6">
          
          {/* Header */}
          <div className="flex items-center justify-between pb-4 border-b border-slate-100">
            <div className="flex items-center gap-2">
              <Settings className="w-5 h-5 text-blue-600" />
              <h3 className="text-base font-bold text-slate-900">
                Paramètres & Configuration
              </h3>
            </div>

            <button
              onClick={onClose}
              className="p-1.5 rounded-xl hover:bg-slate-100 text-slate-500 hover:text-slate-900 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Section 1: Thèmes Visuels & Style */}
          <div className="flex flex-col gap-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
              <Sliders className="w-3.5 h-3.5 text-blue-600" />
              Thème Visuel du Workspace
            </h4>

            <div className="grid grid-cols-1 gap-2">
              <div className="p-3 rounded-xl border-2 border-blue-600 bg-blue-50/50 flex items-center justify-between cursor-pointer">
                <div>
                  <span className="text-xs font-bold text-slate-900 block">Google Light Workspace (Actif)</span>
                  <span className="text-[11px] text-slate-500">Style NotebookLM & Gemini Enterprise</span>
                </div>
                <Check className="w-4 h-4 text-blue-600" />
              </div>
            </div>
          </div>

          {/* Section 2: Restitution Audio & Synthèse Vocale */}
          <div className="flex flex-col gap-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
              <Volume2 className="w-3.5 h-3.5 text-blue-600" />
              Paramètres Vocaux & Audio
            </h4>

            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between">
              <div>
                <span className="text-xs font-semibold text-slate-900 block">Lecture Vocale Automatique (TTS)</span>
                <span className="text-[11px] text-slate-500">Synthèse vocale des réponses de l'agent</span>
              </div>

              <button
                type="button"
                onClick={() => setAutoSpeechEnabled(!autoSpeechEnabled)}
                className={`w-10 h-5 rounded-full p-0.5 transition-colors duration-200 ${
                  autoSpeechEnabled ? 'bg-blue-600' : 'bg-slate-300'
                }`}
              >
                <div className={`w-4 h-4 rounded-full bg-white transition-transform duration-200 ${
                  autoSpeechEnabled ? 'translate-x-5' : 'translate-x-0'
                }`} />
              </button>
            </div>
          </div>

          {/* Section 3: Statut de la Connexion GCP BigQuery & Dataplex */}
          <div className="flex flex-col gap-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
              <Database className="w-3.5 h-3.5 text-emerald-600" />
              Gouvernance & Infrastructure GCP
            </h4>

            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-2 text-xs">
              <div className="flex items-center justify-between text-slate-700">
                <span>Projet GCP :</span>
                <strong className="font-mono text-slate-900">data-agents-by-industry</strong>
              </div>

              <div className="flex items-center justify-between text-slate-700">
                <span>Nombre d'Agents Déployés :</span>
                <strong className="text-slate-900">{agentsCount} Agents</strong>
              </div>

              <div className="flex items-center gap-2 text-emerald-700 bg-emerald-50 p-2 rounded-lg border border-emerald-200 text-[11px] mt-2">
                <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>Dataplex Governance, Data Lineage & Vertex AI API Actifs</span>
              </div>
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="pt-4 border-t border-slate-100 text-center text-xs text-slate-400">
          Talk to Data • Google Cloud BigData Paris 2026
        </div>

      </div>

    </div>
  );
}
