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
    <header className="w-full flex justify-center px-4 sticky top-0 z-40">
      <div className="fluo-header flex items-center justify-between gap-4">
        
        {/* Brand Logo & Clean Title */}
        <div className="flex items-center gap-3">
          <div className="size-8 rounded-lg bg-[#0B57D0] text-white flex items-center justify-center font-extrabold text-xs shadow-md shrink-0">
            TD
          </div>
          <h1 className="text-base font-bold text-slate-900 tracking-tight text-balance font-['Google_Sans_Flex']">
            Talk to <em className="font-['Instrument_Serif'] italic font-normal text-[#0B57D0] not-italic">Data</em>
          </h1>
        </div>

        {/* Right Controls: Audio Toggle Icon & Settings Gear */}
        <div className="flex items-center gap-2.5">
          
          {/* Audio Speech Switch Icon */}
          <button
            type="button"
            aria-label={autoSpeechEnabled ? "Désactiver la voix" : "Activer la voix"}
            onClick={() => setAutoSpeechEnabled(!autoSpeechEnabled)}
            className={cn(
              "size-9 rounded-full border flex items-center justify-center transition-all text-xs shadow-xs",
              autoSpeechEnabled
                ? "bg-blue-50 text-[#0B57D0] border-blue-200 shadow-xs"
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
            aria-label="Paramètres de l'application"
            onClick={onOpenSettings}
            className="size-9 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 flex items-center justify-center transition-all text-xs shadow-xs"
            title="Paramètres de l'application & Mode Écran"
          >
            <Settings className="size-4 text-slate-700" />
          </button>

        </div>

      </div>
    </header>
  );
}
