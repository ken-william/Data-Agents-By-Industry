import React from 'react';
import { Volume2, VolumeX, Settings } from 'lucide-react';
import { cn } from '../utils/cn';

export function Header({
  selectedAgent,
  agentsCount,
  autoSpeechEnabled,
  setAutoSpeechEnabled,
  isSpeaking,
  onOpenSettings
}) {
  return (
    <header className="w-full bg-white/90 border-b border-white/80 sticky top-0 z-40 backdrop-blur-xl shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between gap-4">
        
        {/* Brand Logo & Clean Title */}
        <div className="flex items-center gap-3">
          <div className="size-8 rounded-lg bg-gradient-to-r from-[#79A7F7] via-[#4285F4] to-[#1A56DB] flex items-center justify-center text-white font-extrabold text-xs shadow-md shrink-0">
            TD
          </div>
          <h1 className="text-base font-bold text-slate-900 tracking-tight text-balance">
            Talk to <em className="font-['Instrument_Serif'] italic font-normal text-blue-700 not-italic">Data</em>
          </h1>
        </div>

        {/* Right Controls: Audio Toggle Icon & Settings Gear */}
        <div className="flex items-center gap-2.5">
          
          {/* Audio Speech Switch Icon */}
          <button
            type="button"
            aria-label={autoSpeechEnabled ? "Désactiver la synthèse vocale" : "Activer la synthèse vocale"}
            onClick={() => setAutoSpeechEnabled(!autoSpeechEnabled)}
            className={cn(
              "size-9 rounded-full border flex items-center justify-center transition-all",
              autoSpeechEnabled
                ? "bg-blue-50 border-blue-300 text-blue-700 shadow-xs"
                : "bg-white border-slate-200 text-slate-400 hover:text-slate-700"
            )}
            title={autoSpeechEnabled ? "Désactiver la voix de l'agent" : "Activer la voix de l'agent"}
          >
            {autoSpeechEnabled ? (
              <Volume2 className={cn("size-4", isSpeaking && "text-emerald-600 animate-bounce")} />
            ) : (
              <VolumeX className="size-4 text-slate-400" />
            )}
          </button>

          {/* Settings Drawer Button */}
          <button
            type="button"
            aria-label="Ouvrir le panneau de configuration"
            onClick={onOpenSettings}
            className="size-9 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 hover:text-slate-900 border border-slate-200 flex items-center justify-center transition-all shadow-xs"
            title="Paramètres de l'application & Mode Écran"
          >
            <Settings className="size-4 text-slate-700" />
          </button>

        </div>

      </div>
    </header>
  );
}
