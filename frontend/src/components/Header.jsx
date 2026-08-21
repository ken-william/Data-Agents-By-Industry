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
    <header className="glass-navbar sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between gap-4">
        
        {/* Brand Logo & Clean Title */}
        <div className="flex items-center gap-3">
          <div className="size-8 rounded-lg bg-white/90 text-[#1A56DB] flex items-center justify-center font-extrabold text-xs shadow-md shrink-0 border border-white/60">
            TD
          </div>
          <h1 className="text-base font-bold text-white tracking-tight text-balance">
            Talk to <em className="font-['Instrument_Serif'] italic font-normal text-blue-100 not-italic">Data</em>
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
              "size-9 rounded-full border flex items-center justify-center transition-all shadow-xs",
              autoSpeechEnabled
                ? "bg-white text-blue-700 border-white/80 shadow-md"
                : "bg-white/20 border-white/30 text-white/80 hover:bg-white/30 hover:text-white"
            )}
            title={autoSpeechEnabled ? "Désactiver la voix de l'agent" : "Activer la voix de l'agent"}
          >
            {autoSpeechEnabled ? (
              <Volume2 className={cn("size-4", isSpeaking && "text-emerald-600 animate-bounce")} />
            ) : (
              <VolumeX className="size-4 text-white/70" />
            )}
          </button>

          {/* Settings Drawer Button */}
          <button
            type="button"
            aria-label="Ouvrir le panneau de configuration"
            onClick={onOpenSettings}
            className="size-9 rounded-full bg-white/20 hover:bg-white/30 text-white border border-white/30 flex items-center justify-center transition-all shadow-xs"
            title="Paramètres de l'application & Mode Écran"
          >
            <Settings className="size-4 text-white" />
          </button>

        </div>

      </div>
    </header>
  );
}
