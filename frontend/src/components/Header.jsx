import React from 'react';
import { Volume2, VolumeX, Settings } from 'lucide-react';

export function Header({
  selectedAgent,
  agentsCount,
  autoSpeechEnabled,
  setAutoSpeechEnabled,
  isSpeaking,
  onOpenSettings
}) {
  return (
    <header className="w-full px-4 sticky top-3 z-50">
      <div className="fluo-header flex items-center justify-between gap-4">
        
        {/* Brand Logo & Clean Title */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-gradient-to-r from-sky-400 via-indigo-500 to-fuchsia-500 flex items-center justify-center text-white font-extrabold text-xs shadow-[0_0_15px_rgba(56,189,248,0.4)]">
            TD
          </div>
          <h1 className="text-base font-bold text-white tracking-tight">
            Talk to <em className="font-['Instrument_Serif'] italic font-normal text-sky-300 not-italic">Data</em>
          </h1>
        </div>

        {/* Right Controls: Audio Toggle Icon & Settings Gear */}
        <div className="flex items-center gap-2.5">
          
          {/* Audio Speech Switch Icon */}
          <button
            type="button"
            onClick={() => setAutoSpeechEnabled(!autoSpeechEnabled)}
            className={`p-2.5 rounded-full border transition-all ${
              autoSpeechEnabled
                ? 'bg-slate-900 border-sky-400 text-sky-400 shadow-[0_0_15px_rgba(56,189,248,0.3)]'
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
            className="p-2.5 rounded-full bg-slate-900/90 hover:bg-slate-800 text-slate-300 hover:text-white border border-sky-500/30 transition-all shadow-md"
            title="Paramètres de l'application & Mode Écran"
          >
            <Settings className="w-4 h-4 text-slate-300" />
          </button>

        </div>

      </div>
    </header>
  );
}
