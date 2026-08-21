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
    <header className="w-full bg-white border-b border-slate-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
        
        {/* Clean Logo & Title */}
        <div className="flex items-center gap-3">
          <div className="size-8 rounded-lg bg-blue-600 text-white flex items-center justify-center font-bold text-xs">
            TD
          </div>
          <h1 className="text-base font-bold text-slate-900 tracking-tight">
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
              "size-9 rounded-full border flex items-center justify-center transition-all text-xs",
              autoSpeechEnabled
                ? "bg-blue-50 border-blue-200 text-blue-700"
                : "bg-white border-slate-200 text-slate-400 hover:text-slate-700"
            )}
          >
            {autoSpeechEnabled ? (
              <Volume2 className={cn("size-4", isSpeaking && "text-emerald-600 animate-bounce")} />
            ) : (
              <VolumeX className="size-4" />
            )}
          </button>

          <button
            type="button"
            aria-label="Paramètres"
            onClick={onOpenSettings}
            className="size-9 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 flex items-center justify-center transition-all text-xs"
          >
            <Settings className="size-4" />
          </button>
        </div>

      </div>
    </header>
  );
}
