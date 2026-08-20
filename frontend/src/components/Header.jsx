import React from 'react';
import { Database, Sparkles, Volume2, VolumeX, Monitor, Smartphone, Settings } from 'lucide-react';

export function Header({
  selectedAgent,
  agentsCount,
  autoSpeechEnabled,
  setAutoSpeechEnabled,
  isSpeaking,
  screenMode,
  setScreenMode,
  onOpenSettings
}) {
  return (
    <header className="w-full bg-white border-b border-slate-200 sticky top-0 z-40 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between gap-4">
        
        {/* Brand Logo & Title */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-xs shadow-xs">
              TD
            </div>
            <h1 className="text-sm font-bold text-slate-900 tracking-tight">
              Talk to Data <span className="text-slate-500 font-normal text-xs">| BigData Paris 2026</span>
            </h1>
          </div>

          <div className="hidden md:flex items-center gap-1.5 px-2.5 py-0.5 rounded-lg bg-slate-100 border border-slate-200 text-[11px] text-slate-600 font-medium">
            <Sparkles className="w-3 h-3 text-blue-600" />
            <span>Workspace Multi-Agents ({agentsCount})</span>
          </div>
        </div>

        {/* Center: Dual Screen Switcher */}
        <div className="flex items-center p-0.5 rounded-lg bg-slate-100 border border-slate-200 text-xs">
          <button
            onClick={() => setScreenMode('showcase')}
            className={`px-3 py-1 rounded-md flex items-center gap-1.5 font-medium transition-all ${
              screenMode === 'showcase'
                ? 'bg-white text-blue-700 shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
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
                ? 'bg-white text-blue-700 shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
            title="Écran B : Le PC Contrôleur (Présentateur)"
          >
            <Smartphone className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Écran B : Contrôleur</span>
          </button>
        </div>

        {/* Right Controls: Voice Toggle, Settings & GCP Tag */}
        <div className="flex items-center gap-2 sm:gap-3">
          
          {/* Audio Reader Switch */}
          <button
            onClick={() => setAutoSpeechEnabled(!autoSpeechEnabled)}
            className={`px-2.5 py-1 rounded-lg border text-xs font-medium flex items-center gap-1.5 transition-all ${
              autoSpeechEnabled
                ? 'bg-slate-100 border-slate-200 text-slate-700'
                : 'bg-white border-slate-200 text-slate-400 hover:text-slate-600'
            }`}
            title="Activer/Désactiver la lecture vocale automatique"
          >
            {autoSpeechEnabled ? (
              <>
                <Volume2 className={`w-3.5 h-3.5 ${isSpeaking ? 'text-emerald-600 animate-bounce' : 'text-blue-600'}`} />
                <span className="hidden sm:inline">Voix Active</span>
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
            onClick={onOpenSettings}
            className="p-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-600 transition-colors"
            title="Paramètres de l'application"
          >
            <Settings className="w-4 h-4 text-slate-700" />
          </button>

          {/* Project ID Tag */}
          <div className="hidden lg:flex items-center gap-1.5 px-2 py-1 rounded-lg bg-slate-100 border border-slate-200 text-[11px] text-slate-500 font-mono">
            <Database className="w-3 h-3 text-emerald-600" />
            <span>data-agents-by-industry</span>
          </div>

        </div>

      </div>
    </header>
  );
}
