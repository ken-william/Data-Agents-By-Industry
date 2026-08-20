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
    <header className="w-full bg-[#020617]/75 border-b border-slate-800/80 sticky top-0 z-40 backdrop-blur-md shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between gap-4">
        
        {/* Brand Logo & Title */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 flex items-center justify-center text-white font-bold text-xs shadow-md">
              TD
            </div>
            <h1 className="text-sm font-bold text-slate-100 tracking-tight">
              Talk to Data <span className="text-slate-400 font-normal text-xs">| BigData Paris 2026</span>
            </h1>
          </div>

          <div className="hidden md:flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-slate-900/90 border border-slate-800 text-[11px] text-slate-300 font-medium">
            <Sparkles className="w-3 h-3 text-sky-400" />
            <span>Multi-Agents Workspace ({agentsCount})</span>
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
                ? 'bg-slate-900 border-slate-700 text-slate-200 shadow-md'
                : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:text-slate-200'
            }`}
            title="Activer/Désactiver la synthèse vocale automatique"
          >
            {autoSpeechEnabled ? (
              <>
                <Volume2 className={`w-3.5 h-3.5 ${isSpeaking ? 'text-emerald-400 animate-bounce' : 'text-sky-400'}`} />
                <span className="hidden sm:inline">Voix Active</span>
              </>
            ) : (
              <>
                <VolumeX className="w-3.5 h-3.5 text-slate-500" />
                <span className="hidden sm:inline">Voix Muette</span>
              </>
            )}
          </button>

          {/* Settings Drawer Button */}
          <button
            type="button"
            onClick={onOpenSettings}
            className="p-2 rounded-full bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-800 transition-all shadow-md"
            title="Paramètres de l'application & Mode Écran"
          >
            <Settings className="w-4 h-4 text-slate-300" />
          </button>

          {/* Project ID Tag */}
          <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-900/90 border border-slate-800 text-[11px] text-slate-400 font-mono">
            <Database className="w-3 h-3 text-emerald-400" />
            <span>data-agents-by-industry</span>
          </div>

        </div>

      </div>
    </header>
  );
}
