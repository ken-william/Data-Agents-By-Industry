import React from 'react';
import { Database, Sparkles, Volume2, VolumeX, Settings } from 'lucide-react';

export function Header({
  selectedAgent,
  agentsCount,
  autoSpeechEnabled,
  setAutoSpeechEnabled,
  isSpeaking,
  onOpenSettings
}) {
  return (
    <header className="w-full bg-white/85 border-b border-slate-200/80 sticky top-0 z-40 backdrop-blur-xl shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between gap-4">
        
        {/* Brand Logo & Title */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-r from-blue-600 via-indigo-600 to-sky-500 flex items-center justify-center text-white font-bold text-xs shadow-xs">
              TD
            </div>
            <h1 className="text-sm font-bold text-slate-900 tracking-tight">
              Talk to Data <span className="text-slate-500 font-normal text-xs">| BigData Paris 2026</span>
            </h1>
          </div>

          <div className="hidden md:flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-100/80 border border-slate-200 text-[11px] text-slate-700 font-medium">
            <Sparkles className="w-3 h-3 text-blue-600" />
            <span>Workspace Multi-Agents ({agentsCount})</span>
          </div>
        </div>

        {/* Right Controls: Voice Toggle, Settings Gear Icon & GCP Project Tag */}
        <div className="flex items-center gap-2 sm:gap-3">
          
          {/* Audio Speech Switcher */}
          <button
            type="button"
            onClick={() => setAutoSpeechEnabled(!autoSpeechEnabled)}
            className={`px-3 py-1 rounded-full border text-xs font-medium flex items-center gap-1.5 transition-all ${
              autoSpeechEnabled
                ? 'bg-blue-50 border-blue-200 text-blue-700 shadow-xs'
                : 'bg-white border-slate-200 text-slate-500 hover:text-slate-800'
            }`}
            title="Activer/Désactiver la synthèse vocale automatique"
          >
            {autoSpeechEnabled ? (
              <>
                <Volume2 className={`w-3.5 h-3.5 ${isSpeaking ? 'text-emerald-600 animate-bounce' : 'text-blue-600'}`} />
                <span className="hidden sm:inline">Voix Active (TTS Purifié)</span>
              </>
            ) : (
              <>
                <VolumeX className="w-3.5 h-3.5 text-slate-400" />
                <span className="hidden sm:inline">Voix Muette</span>
              </>
            )}
          </button>

          {/* Settings Drawer Button */}
          <button
            type="button"
            onClick={onOpenSettings}
            className="p-2 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 hover:text-slate-900 border border-slate-200 transition-all shadow-xs"
            title="Paramètres de l'application & Mode Écran"
          >
            <Settings className="w-4 h-4 text-slate-700" />
          </button>

          {/* Project ID Tag */}
          <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-100/80 border border-slate-200 text-[11px] text-slate-600 font-mono">
            <Database className="w-3 h-3 text-emerald-600" />
            <span>data-agents-by-industry</span>
          </div>

        </div>

      </div>
    </header>
  );
}
