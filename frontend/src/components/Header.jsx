import React from 'react';
import { Volume2, VolumeX, Settings } from 'lucide-react';
import { cn } from '../utils/cn';

export function Header({
  autoSpeechEnabled,
  setAutoSpeechEnabled,
  isSpeaking,
  onOpenSettings
}) {
  return (
    <header className="glass-header-deepblue sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
        
        {/* Clean Logo & Title */}
        <div className="flex items-center gap-3">
          <div className="size-8 rounded-lg bg-white text-blue-700 flex items-center justify-center font-extrabold text-xs shadow-md border border-white/60">
            TD
          </div>
          <h1 className="text-base font-bold text-white tracking-tight">
            Talk to Data
          </h1>
        </div>

        {/* Header Actions */}
        <div className="flex items-center gap-2">
          <button
            type="button"
            aria-label={autoSpeechEnabled ? "Désactiver la voix" : "Activer la voix"}
            onClick={() => setAutoSpeechEnabled(!autoSpeechEnabled)}
            className={cn(
              "size-9 rounded-full border flex items-center justify-center transition-all text-xs shadow-xs",
              autoSpeechEnabled
                ? "bg-white text-blue-700 border-white/80 shadow-md"
                : "bg-white/20 border-white/30 text-white/80 hover:bg-white/30 hover:text-white"
            )}
          >
            {autoSpeechEnabled ? (
              <Volume2 className={cn("size-4", isSpeaking && "text-emerald-400 animate-bounce")} />
            ) : (
              <VolumeX className="size-4 text-white/70" />
            )}
          </button>

          <button
            type="button"
            aria-label="Paramètres"
            onClick={onOpenSettings}
            className="size-9 rounded-full bg-white/20 hover:bg-white/30 text-white border border-white/30 flex items-center justify-center transition-all text-xs shadow-xs"
          >
            <Settings className="size-4 text-white" />
          </button>
        </div>

      </div>
    </header>
  );
}
