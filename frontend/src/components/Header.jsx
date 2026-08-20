import React from 'react';
import { Volume2, VolumeX, Sparkles, Server, RotateCcw } from 'lucide-react';
import { COLOR_THEMES } from '../utils/themeMap';

export function Header({
  selectedAgent,
  agentsCount,
  autoSpeechEnabled,
  setAutoSpeechEnabled,
  isSpeaking,
  onResetChat
}) {
  const colorKey = selectedAgent?.theme?.color || 'indigo';
  const theme = COLOR_THEMES[colorKey] || COLOR_THEMES.indigo;

  return (
    <header className="sticky top-0 z-40 w-full glass-panel border-b border-slate-800/80 px-4 lg:px-8 py-3.5 shadow-2xl">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        
        {/* Left: Branding & Google Cloud Event Badge */}
        <div className="flex items-center gap-3">
          <div className={`p-2.5 rounded-xl ${theme.accentBg} text-white shadow-lg ${theme.glow}`}>
            <Sparkles className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
                Talk to Data
                <span className="text-xs px-2 py-0.5 rounded-full font-mono bg-white/10 text-slate-300 border border-white/10">
                  Google Cloud
                </span>
              </h1>
            </div>
            <p className="text-xs text-slate-400 font-medium">
              11 Copilotes Décisionnels Sectoriels | Conversational Analytics BigQuery
            </p>
          </div>
        </div>

        {/* Right: Audio Toggle, Agent Status Badge & Reset Chat */}
        <div className="flex items-center gap-3">
          
          {/* Active Agent Health Badge */}
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-xs">
            <Server className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-slate-400">Agent:</span>
            <span className={`font-semibold ${theme.text}`}>
              {selectedAgent ? selectedAgent.displayName.split(' - ')[0] : 'Aucun'}
            </span>
            <span className="inline-flex items-center gap-1 text-[10px] px-1.5 py-0.2 rounded font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
              ONLINE
            </span>
          </div>

          {/* Voice Text-to-Speech Toggle Button */}
          <button
            onClick={() => setAutoSpeechEnabled(!autoSpeechEnabled)}
            title={autoSpeechEnabled ? "Désactiver la lecture vocale" : "Activer la lecture vocale"}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-medium transition-all ${
              autoSpeechEnabled
                ? 'bg-indigo-600/20 text-indigo-300 border-indigo-500/40 hover:bg-indigo-600/30'
                : 'bg-slate-800 text-slate-400 border-slate-700 hover:bg-slate-700'
            }`}
          >
            {autoSpeechEnabled ? (
              <>
                <Volume2 className={`w-4 h-4 text-indigo-400 ${isSpeaking ? 'animate-bounce' : ''}`} />
                <span className="hidden md:inline">Voix Active</span>
              </>
            ) : (
              <>
                <VolumeX className="w-4 h-4 text-slate-400" />
                <span className="hidden md:inline">Voix Muette</span>
              </>
            )}
          </button>

          {/* Reset Chat Button */}
          <button
            onClick={onResetChat}
            title="Effacer la conversation"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs font-medium transition-all"
          >
            <RotateCcw className="w-3.5 h-3.5 text-slate-400" />
            <span className="hidden sm:inline">Effacer</span>
          </button>

        </div>

      </div>
    </header>
  );
}
