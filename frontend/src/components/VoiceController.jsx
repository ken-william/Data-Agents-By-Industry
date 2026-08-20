import React from 'react';
import { Mic, MicOff, Volume2, Square } from 'lucide-react';
import { COLOR_THEMES } from '../utils/themeMap';

export function VoiceController({
  isListening,
  startListening,
  stopListening,
  isSpeaking,
  stopSpeaking,
  speechSupported,
  selectedAgent
}) {
  const colorKey = selectedAgent?.theme?.color || 'indigo';
  const theme = COLOR_THEMES[colorKey] || COLOR_THEMES.indigo;

  if (!speechSupported) {
    return (
      <div className="text-[11px] text-slate-500 italic">
        Saisie vocale non disponible sur ce navigateur (utilisez Chrome/Edge/Chromebook).
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2">
      
      {/* Mic Button */}
      <button
        type="button"
        onClick={isListening ? stopListening : startListening}
        title={isListening ? "Arrêter l'écoute vocale" : "Poser une question à la voix (Microphone)"}
        className={`relative p-2.5 rounded-xl font-medium text-xs transition-all duration-300 flex items-center justify-center ${
          isListening
            ? 'bg-rose-600 text-white shadow-lg shadow-rose-900/50 animate-pulse'
            : `bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 border border-slate-700`
        }`}
      >
        {isListening ? (
          <>
            <span className="absolute inset-0 rounded-xl bg-rose-500/30 animate-pulse-ring"></span>
            <MicOff className="w-4 h-4 relative z-10" />
          </>
        ) : (
          <Mic className="w-4 h-4" />
        )}
      </button>

      {/* Listening Status Indicator */}
      {isListening && (
        <div className="flex items-center gap-2 text-xs font-semibold text-rose-400 animate-pulse">
          <span className="w-2 h-2 rounded-full bg-rose-500"></span>
          <span>Écoute en cours (Parlez à l'oral)...</span>
        </div>
      )}

      {/* Speech Audio Playing Indicator */}
      {isSpeaking && (
        <button
          type="button"
          onClick={stopSpeaking}
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-indigo-500/10 text-indigo-300 border border-indigo-500/30 text-xs hover:bg-indigo-500/20 transition-all"
        >
          <Volume2 className="w-3.5 h-3.5 animate-bounce text-indigo-400" />
          <span>Lecture vocale... (Cliquer pour stopper)</span>
          <Square className="w-3 h-3 fill-current text-indigo-400" />
        </button>
      )}

    </div>
  );
}
