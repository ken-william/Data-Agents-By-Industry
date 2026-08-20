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
    stateLabel = "Génération de la requête BigQuery...";
    stateDesc = "Analyse Gemini Conversational Analytics";
  } else if (isSpeaking) {
    stateLabel = "L'Agent s'exprime à l'oral...";
    stateDesc = "Syntèse vocale en cours";
  }

  // Size variants for Showcase (Grand Écran) vs Controller (PC/Tablette)
  const orbSizeClass = showcaseMode ? "w-32 h-32 sm:w-40 sm:h-40" : "w-16 h-16 sm:w-20 sm:h-20";

  return (
    <div className="flex flex-col items-center justify-center relative">
      
      {/* Interactive Vectorial Gemini Orb */}
      <button
        type="button"
        onClick={onClickMic}
        title={isListening ? "Arrêter l'écoute" : "Cliquer pour parler à l'agent (Microphone)"}
        className={`relative ${orbSizeClass} rounded-full p-1 transition-transform duration-300 transform hover:scale-105 active:scale-95 cursor-pointer group flex items-center justify-center`}
      >
        {/* Outer Animated SVG Fluid Rings */}
        <svg
          className="absolute inset-0 w-full h-full pointer-events-none overflow-visible"
          viewBox="0 0 100 100"
        >
          <defs>
            {/* Signature Gemini Gradient */}
            <linearGradient id="geminiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#38BDF8" />
              <stop offset="50%" stopColor="#3B82F6" />
              <stop offset="100%" stopColor="#6366F1" />
            </linearGradient>

            {/* Speaking Emerald/Sky Gradient */}
            <linearGradient id="speakingGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#22C55E" />
              <stop offset="100%" stopColor="#0EA5E9" />
            </linearGradient>

            {/* Listening Cyan/Indigo Gradient */}
            <linearGradient id="listeningGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#06B6D4" />
              <stop offset="100%" stopColor="#6366F1" />
            </linearGradient>
          </defs>

          {/* 1. Idle State: Soft Respiration Pulse Ring */}
          {!isListening && !isStreaming && !isSpeaking && (
            <circle
              cx="50"
              cy="50"
              r="44"
              fill="none"
              stroke="url(#geminiGrad)"
              strokeWidth="2.5"
              strokeDasharray="8 6"
              className="animate-gemini-spin opacity-60"
            />
          )}

          {/* 2. Listening State: Active Soundwaves Frequencies */}
          {isListening && (
            <>
              <circle
                cx="50"
                cy="50"
                r="46"
                fill="none"
                stroke="url(#listeningGrad)"
                strokeWidth="3"
                className="animate-ping opacity-75"
              />
              <circle
                cx="50"
                cy="50"
                r="40"
                fill="none"
                stroke="url(#listeningGrad)"
                strokeWidth="2"
                strokeDasharray="12 4"
                className="animate-gemini-spin"
              />
            </>
          )}

          {/* 3. Thinking State: Spinning Double Ring */}
          {isStreaming && (
            <>
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="url(#geminiGrad)"
                strokeWidth="3.5"
                strokeDasharray="30 15"
                className="animate-gemini-spin"
              />
              <circle
                cx="50"
                cy="50"
                r="38"
                fill="none"
                stroke="#F43F5E"
                strokeWidth="2"
                strokeDasharray="15 20"
                className="animate-spin"
              />
            </>
          )}

          {/* 4. Speaking State: Concentric Waves */}
          {isSpeaking && (
            <>
              <circle
                cx="50"
                cy="50"
                r="46"
                fill="none"
                stroke="url(#speakingGrad)"
                strokeWidth="3"
                className="animate-ping opacity-80"
              />
              <circle
                cx="50"
                cy="50"
                r="40"
                fill="none"
                stroke="url(#speakingGrad)"
                strokeWidth="2.5"
                className="animate-gemini-pulse"
              />
            </>
          )}
        </svg>

        {/* Inner Orb Core */}
        <div className="w-full h-full rounded-full bg-[#0B132B] border border-slate-700/80 backdrop-blur-md flex flex-col items-center justify-center p-2 shadow-2xl relative overflow-hidden">
          
          {/* Internal Glow Core */}
          <div
            className={`absolute inset-1 rounded-full opacity-40 blur-md ${
              isListening
                ? 'bg-cyan-500 animate-pulse'
                : isStreaming
                ? 'bg-indigo-500 animate-spin'
                : isSpeaking
                ? 'bg-emerald-500 animate-pulse'
                : 'bg-blue-500 animate-gemini-pulse'
            }`}
          />

          {/* Icon Center */}
          <div className="relative z-10 text-white flex flex-col items-center">
            {isStreaming ? (
              <Loader2 className={`${showcaseMode ? 'w-10 h-10' : 'w-6 h-6'} animate-spin text-sky-300`} />
            ) : isListening ? (
              <MicOff className={`${showcaseMode ? 'w-10 h-10' : 'w-6 h-6'} text-cyan-300 animate-pulse`} />
            ) : isSpeaking ? (
              <Volume2 className={`${showcaseMode ? 'w-10 h-10' : 'w-6 h-6'} text-emerald-300 animate-bounce`} />
            ) : (
              <Mic className={`${showcaseMode ? 'w-10 h-10' : 'w-6 h-6'} text-sky-300 group-hover:scale-110 transition-transform`} />
            )}
          </div>

        </div>
      </button>

      {/* State Text Label */}
      <div className="mt-2 text-center">
        <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-[#0B132B] border border-slate-800 text-[11px] font-medium text-slate-200 shadow-sm">
          <Sparkles className="w-3 h-3 text-sky-400" />
          <span>{stateLabel}</span>
        </div>
        {!showcaseMode && (
          <p className="text-[10px] text-slate-400 mt-0.5">
            {stateDesc}
          </p>
        )}
      </div>

    </div>
  );
}
