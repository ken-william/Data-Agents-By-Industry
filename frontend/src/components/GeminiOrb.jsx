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
  let stateLabel = "Prêt (Gemini Live)";
  let stateDesc = speechSupported ? "Cliquez sur l'orbe ou le micro" : "Entrée clavier active";

  if (isListening) {
    stateLabel = "J'écoute votre voix...";
    stateDesc = "Parlez maintenant à voix haute";
  } else if (isStreaming) {
    stateLabel = "Génération BigQuery...";
    stateDesc = "Analyse Gemini Conversational Analytics";
  } else if (isSpeaking) {
    stateLabel = "Lecture vocale...";
    stateDesc = "Synthèse sonore en cours";
  }

  const orbSizeClass = showcaseMode ? "w-28 h-28 sm:w-36 sm:h-36" : "w-14 h-14 sm:w-16 sm:h-16";

  return (
    <div className="flex flex-col items-center justify-center relative">
      
      {/* Glassmorphism Translucent Light Gemini Orb */}
      <button
        type="button"
        onClick={onClickMic}
        title={isListening ? "Arrêter l'écoute" : "Cliquer pour parler à l'agent (Microphone)"}
        className={`relative ${orbSizeClass} rounded-full p-1 transition-transform duration-300 transform hover:scale-105 active:scale-95 cursor-pointer group flex items-center justify-center`}
      >
        {/* Outer Animated SVG Light Waves */}
        <svg
          className="absolute inset-0 w-full h-full pointer-events-none overflow-visible"
          viewBox="0 0 100 100"
        >
          <defs>
            <linearGradient id="lightGeminiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#38BDF8" />
              <stop offset="50%" stopColor="#818CF8" />
              <stop offset="100%" stopColor="#C084FC" />
            </linearGradient>

            <linearGradient id="lightSpeakingGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#10B981" />
              <stop offset="100%" stopColor="#0EA5E9" />
            </linearGradient>
          </defs>

          {!isListening && !isStreaming && !isSpeaking && (
            <circle
              cx="50"
              cy="50"
              r="44"
              fill="none"
              stroke="url(#lightGeminiGrad)"
              strokeWidth="2"
              strokeDasharray="6 4"
              className="animate-light-spin opacity-70"
            />
          )}

          {isListening && (
            <>
              <circle
                cx="50"
                cy="50"
                r="46"
                fill="none"
                stroke="url(#lightGeminiGrad)"
                strokeWidth="2.5"
                className="animate-ping opacity-80"
              />
              <circle
                cx="50"
                cy="50"
                r="40"
                fill="none"
                stroke="url(#lightGeminiGrad)"
                strokeWidth="2"
                strokeDasharray="10 4"
                className="animate-light-spin"
              />
            </>
          )}

          {isStreaming && (
            <circle
              cx="50"
              cy="50"
              r="45"
              fill="none"
              stroke="url(#lightGeminiGrad)"
              strokeWidth="3"
              strokeDasharray="25 15"
              className="animate-light-spin"
            />
          )}

          {isSpeaking && (
            <circle
              cx="50"
              cy="50"
              r="46"
              fill="none"
              stroke="url(#lightSpeakingGrad)"
              strokeWidth="2.5"
              className="animate-light-pulse"
            />
          )}
        </svg>

        {/* Translucent Glass Core */}
        <div className="w-full h-full rounded-full bg-white/60 border border-white/80 backdrop-blur-md flex flex-col items-center justify-center p-2 shadow-lg relative overflow-hidden">
          
          {/* Subtle Ambient Light Core Glow */}
          <div
            className={`absolute inset-1 rounded-full opacity-30 blur-md ${
              isListening
                ? 'bg-sky-400 animate-pulse'
                : isStreaming
                ? 'bg-indigo-400 animate-spin'
                : isSpeaking
                ? 'bg-emerald-400 animate-pulse'
                : 'bg-blue-400 animate-light-pulse'
            }`}
          />

          {/* Icon Center */}
          <div className="relative z-10 text-slate-700 flex flex-col items-center">
            {isStreaming ? (
              <Loader2 className={`${showcaseMode ? 'w-8 h-8' : 'w-5 h-5'} animate-spin text-blue-600`} />
            ) : isListening ? (
              <MicOff className={`${showcaseMode ? 'w-8 h-8' : 'w-5 h-5'} text-rose-500 animate-pulse`} />
            ) : isSpeaking ? (
              <Volume2 className={`${showcaseMode ? 'w-8 h-8' : 'w-5 h-5'} text-emerald-600 animate-bounce`} />
            ) : (
              <Mic className={`${showcaseMode ? 'w-8 h-8' : 'w-5 h-5'} text-blue-600 group-hover:scale-110 transition-transform`} />
            )}
          </div>

        </div>
      </button>

      {/* State Text Label */}
      <div className="mt-2 text-center">
        <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-white border border-slate-200 text-[11px] font-medium text-slate-700 shadow-sm">
          <Sparkles className="w-3 h-3 text-blue-600" />
          <span>{stateLabel}</span>
        </div>
        {!showcaseMode && (
          <p className="text-[10px] text-slate-500 mt-0.5">
            {stateDesc}
          </p>
        )}
      </div>

    </div>
  );
}
