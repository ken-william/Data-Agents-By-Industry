import React from 'react';
import { Database, Sparkles, Volume2, VolumeX, ShieldCheck } from 'lucide-react';

export function Header({
  selectedAgent,
  agentsCount,
  autoSpeechEnabled,
  setAutoSpeechEnabled,
  isSpeaking,
  onResetChat
}) {
  return (
    <header className="w-full bg-[#141417] border-b border-[#27272a] sticky top-0 z-50 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between gap-4">
        
        {/* Brand Logo & Event Badge */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold text-xs shadow-md">
              TD
            </div>
            <h1 className="text-sm font-bold text-zinc-50 tracking-tight">
              Talk to Data <span className="text-zinc-500 font-normal text-xs">| GCP Conversational Analytics</span>
            </h1>
          </div>

          <div className="hidden md:flex items-center gap-1.5 px-2.5 py-0.5 rounded-md bg-zinc-900 border border-zinc-800 text-[11px] text-zinc-400 font-medium">
            <Sparkles className="w-3 h-3 text-indigo-400" />
            <span>Multi-Agent Platform ({agentsCount})</span>
          </div>
        </div>

        {/* Controls: Audio Reader Toggle & GCP Project Tag */}
        <div className="flex items-center gap-3">
          
          {/* TTS Audio Reader Switch */}
          <button
            onClick={() => setAutoSpeechEnabled(!autoSpeechEnabled)}
            className={`px-2.5 py-1 rounded-md border text-xs font-medium flex items-center gap-1.5 transition-all ${
              autoSpeechEnabled
                ? 'bg-zinc-900 border-zinc-700 text-zinc-200'
                : 'bg-zinc-950 border-zinc-800 text-zinc-500 hover:text-zinc-300'
            }`}
            title="Activer/Désactiver la lecture vocale automatique des réponses"
          >
            {autoSpeechEnabled ? (
              <>
                <Volume2 className={`w-3.5 h-3.5 ${isSpeaking ? 'text-emerald-400 animate-bounce' : 'text-zinc-300'}`} />
                <span>Voix Active</span>
              </>
            ) : (
              <>
                <VolumeX className="w-3.5 h-3.5 text-zinc-500" />
                <span>Voix Muette</span>
              </>
            )}
          </button>

          {/* Project ID Tag */}
          <div className="hidden sm:flex items-center gap-1.5 px-2 py-1 rounded-md bg-zinc-950 border border-zinc-800 text-[11px] text-zinc-400 font-mono">
            <Database className="w-3 h-3 text-emerald-400" />
            <span>data-agents-by-industry</span>
          </div>

        </div>

      </div>
    </header>
  );
}
