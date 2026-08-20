import React from 'react';
import { Mic, MicOff, Volume2, Sparkles, Loader2 } from 'lucide-react';

export function GeminiOrb({
  isListening,
  isSpeaking,
  isStreaming,
  onClickMic,
  speechSupported,
  showcaseMode = false
}) {
  let stateLabel = "Prêt pour votre question";
  if (isListening) {
    stateLabel = "Je vous écoute...";
  } else if (isStreaming) {
    stateLabel = "Analyse des données BigQuery...";
  } else if (isSpeaking) {
    stateLabel = "Génération de la réponse vocale...";
  }

  return (
    <div className="flex flex-col items-center justify-center relative my-2">
      
      {/* Gemini Live Orbe with Physics Waves */}
      <button
        type="button"
        onClick={onClickMic}
        title={isListening ? "Arrêter l'écoute" : "Cliquer pour parler (Microphone)"}
        className={`gemini-orbe-live cursor-pointer transition-transform duration-300 transform hover:scale-105 active:scale-95 ${
          showcaseMode ? 'showcase' : ''
        }`}
      >
        {/* Animated Concentric Wave Rings */}
        <div className="wave wave-1"></div>
        <div className="wave wave-2"></div>
        <div className="wave wave-3"></div>

        {/* Center Icon */}
        <div className="relative z-10 text-white flex items-center justify-center">
          {isStreaming ? (
            <Loader2 className={`${showcaseMode ? 'w-10 h-10' : 'w-7 h-7'} animate-spin text-sky-200`} />
          ) : isListening ? (
            <MicOff className={`${showcaseMode ? 'w-10 h-10' : 'w-7 h-7'} text-white animate-pulse`} />
          ) : isSpeaking ? (
            <Volume2 className={`${showcaseMode ? 'w-10 h-10' : 'w-7 h-7'} text-white animate-bounce`} />
          ) : (
            <Mic className={`${showcaseMode ? 'w-10 h-10' : 'w-7 h-7'} text-white`} />
          )}
        </div>
      </button>

      {/* State Text Label */}
      <div className="mt-3 text-center">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-900/80 border border-slate-700/80 text-xs font-medium text-slate-200 shadow-md">
          <Sparkles className="w-3.5 h-3.5 text-sky-400" />
          <span>{stateLabel}</span>
        </div>
      </div>

    </div>
  );
}
