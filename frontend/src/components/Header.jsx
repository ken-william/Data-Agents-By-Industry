import React from 'react';
import { Sparkles, Volume2, VolumeX, Settings } from 'lucide-react';

export function Header({
  selectedAgent,
  agentsCount,
  autoSpeechEnabled,
  setAutoSpeechEnabled,
  isSpeaking,
  onOpenSettings
}) {
  return (
    <header className="w-full bg-[#0B0F19]/80 border-b border-slate-800/80 sticky top-0 z-40 backdrop-blur-xl shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between gap-4">
        
        {/* Brand Logo & Title */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-r from-sky-400 via-indigo-500 to-fuchsia-500 flex items-center justify-center text-white font-extrabold text-xs shadow-[0_0_15px_rgba(99,102,241,0.4)]">
              TD
            </div>
            <h1 className="text-sm sm:text-base font-bold text-slate-100 tracking-tight">
              Talk to Data <span className="text-slate-400 font-normal text-xs">| BigData Paris 2026</span>
            </h1>
          </div>

          <div className="hidden md:flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-900/90 border border-slate-800 text-[11px] text-slate-300 font-medium">
            <Sparkles className="w-3 h-3 text-sky-400" />
            <span>Copilotes Sectoriels ({agentsCount})</span>
          </div>
        </div>

        {/* Right Controls: Audio Toggle Icon & Settings Gear */}
        <div className="flex items-center gap-2.5">
          
          {/* Audio Speech Switch Icon */}
          <button
            type="button"
            onClick={() => setAutoSpeechEnabled(!autoSpeechEnabled)}
            className={`p-2 rounded-full border transition-all ${
              autoSpeechEnabled
                ? 'bg-slate-900 border-sky-500/50 text-sky-400 shadow-[0_0_12px_rgba(56,189,248,0.2)]'
                : 'bg-slate-950/80 border-slate-800 text-slate-500 hover:text-slate-300'
            }`}
            title={autoSpeechEnabled ? "Désactiver la voix de l'agent" : "Activer la voix de l'agent"}
          >
            {autoSpeechEnabled ? (
              <Volume2 className={`w-4 h-4 ${isSpeaking ? 'text-sky-300 animate-bounce' : 'text-sky-400'}`} />
            ) : (
              <VolumeX className="w-4 h-4 text-slate-500" />
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

        </div>

      </div>
    </header>
  );
}
