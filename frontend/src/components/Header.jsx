import React from 'react';
import { Database, Sparkles, Volume2, VolumeX, Monitor, Smartphone } from 'lucide-react';

export function Header({
  selectedAgent,
  agentsCount,
  autoSpeechEnabled,
  setAutoSpeechEnabled,
  isSpeaking,
  screenMode,
  setScreenMode
}) {
  return (
    <header className="w-full bg-[#0B132B]/80 border-b border-slate-800/80 sticky top-0 z-50 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between gap-4">
        
        {/* Brand Logo & Event Badge */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 flex items-center justify-center text-white font-bold text-xs shadow-md">
              TD
            </div>
            <h1 className="text-sm font-bold text-slate-50 tracking-tight">
              Talk to Data <span className="text-slate-400 font-normal text-xs">| BigData Paris 2026</span>
            </h1>
          </div>

          <div className="hidden md:flex items-center gap-1.5 px-2.5 py-0.5 rounded-lg bg-[#020617] border border-slate-800 text-[11px] text-slate-300 font-medium">
            <Sparkles className="w-3 h-3 text-sky-400" />
            <span>Multi-Agent Platform ({agentsCount})</span>
          </div>
        </div>

        {/* Center: Dual Screen Mode Switcher */}
        <div className="flex items-center p-0.5 rounded-lg bg-[#020617] border border-slate-800 text-xs">
          <button
            onClick={() => setScreenMode('showcase')}
            className={`px-3 py-1 rounded-md flex items-center gap-1.5 font-medium transition-all ${
              screenMode === 'showcase'
                ? 'bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 text-white shadow-md'
                : 'text-slate-400 hover:text-white'
            }`}
            title="Écran A : Le Grand Écran Public (Showcase)"
          >
            <Monitor className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Écran A : Showcase</span>
          </button>

          <button
            onClick={() => setScreenMode('controller')}
            className={`px-3 py-1 rounded-md flex items-center gap-1.5 font-medium transition-all ${
              screenMode === 'controller'
                ? 'bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 text-white shadow-md'
                : 'text-slate-400 hover:text-white'
            }`}
            title="Écran B : Le PC Contrôleur (Présentateur)"
          >
            <Smartphone className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Écran B : Contrôleur</span>
          </button>
        </div>

        {/* Right Controls: Audio Reader Toggle & GCP Project Tag */}
        <div className="flex items-center gap-3">
          
          {/* TTS Audio Reader Switch */}
          <button
            onClick={() => setAutoSpeechEnabled(!autoSpeechEnabled)}
            className={`px-2.5 py-1 rounded-lg border text-xs font-medium flex items-center gap-1.5 transition-all ${
              autoSpeechEnabled
                ? 'bg-[#020617] border-slate-700 text-slate-200'
                : 'bg-[#020617] border-slate-800 text-slate-500 hover:text-slate-300'
            }`}
            title="Activer/Désactiver la lecture vocale automatique des réponses"
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

          {/* Project ID Tag */}
          <div className="hidden lg:flex items-center gap-1.5 px-2 py-1 rounded-lg bg-[#020617] border border-slate-800 text-[11px] text-slate-400 font-mono">
            <Database className="w-3 h-3 text-emerald-400" />
            <span>data-agents-by-industry</span>
          </div>

        </div>

      </div>
    </header>
  );
}
