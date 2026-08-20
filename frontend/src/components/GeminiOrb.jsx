import React from 'react';
import { Mic, MicOff, Volume2, Sparkles, Loader2 } from 'lucide-react';

export function GeminiOrb({
  isListening,
  isSpeaking,
  isStreaming,
  onClickMic,
  speechSupported,
  agentTheme
}) {
  let stateLabel = "Prêt (Voix & Clavier)";
  let orbBorder = "border-zinc-700 hover:border-zinc-500 bg-zinc-900";
  let iconColor = "text-zinc-300";

  if (isListening) {
    stateLabel = "Écoute en cours...";
    orbBorder = "border-rose-500 bg-rose-950/40 text-rose-300";
    iconColor = "text-rose-400 animate-pulse";
  } else if (isStreaming) {
    stateLabel = "Analyse BigQuery...";
    orbBorder = "border-indigo-500 bg-indigo-950/40 text-indigo-300";
    iconColor = "text-indigo-400 animate-spin";
  } else if (isSpeaking) {
    stateLabel = "Lecture vocale...";
    orbBorder = "border-emerald-500 bg-emerald-950/40 text-emerald-300";
    iconColor = "text-emerald-400 animate-bounce";
  }

  return (
    <div className="flex items-center gap-3 py-1">
      {/* Elegant Compact Voice Orb Button */}
      <button
        type="button"
        onClick={onClickMic}
        title={isListening ? "Arrêter l'écoute" : "Cliquer pour parler (Microphone)"}
        className={`w-12 h-12 rounded-xl border ${orbBorder} p-2.5 transition-all duration-200 flex items-center justify-center cursor-pointer shadow-md`}
      >
        {isStreaming ? (
          <Loader2 className="w-5 h-5 animate-spin text-indigo-400" />
        ) : isListening ? (
          <MicOff className="w-5 h-5 text-rose-400" />
        ) : isSpeaking ? (
          <Volume2 className="w-5 h-5 text-emerald-400" />
        ) : (
          <Mic className="w-5 h-5 text-zinc-300 hover:text-white" />
        )}
      </button>

      {/* State Badge */}
      <div className="flex flex-col text-left">
        <div className="inline-flex items-center gap-1.5 text-xs font-medium text-zinc-300">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
          <span>{stateLabel}</span>
        </div>
        <span className="text-[10px] text-zinc-500">
          {speechSupported ? "Cliquez sur le micro ou tapez ci-dessous" : "Entrée clavier active"}
        </span>
      </div>
    </div>
  );
}
