import React from 'react';
import { Mic, MicOff, Volume2, Sparkles, Brain, Loader2 } from 'lucide-react';

export function GeminiOrb({
  isListening,
  isSpeaking,
  isStreaming,
  onClickMic,
  speechSupported,
  agentTheme
}) {
  // Determine Orb State
  let stateLabel = "Prêt à échanger (Voix & Chat)";
  let orbGradient = "from-blue-500 via-indigo-500 to-purple-500";
  let pulseAnimation = "animate-pulse";

  if (isListening) {
    stateLabel = "J'écoute votre question...";
    orbGradient = "from-rose-500 via-pink-500 to-red-500 shadow-rose-500/50";
    pulseAnimation = "scale-110 animate-bounce";
  } else if (isStreaming) {
    stateLabel = "Analyse BigQuery en cours...";
    orbGradient = "from-amber-400 via-purple-500 to-cyan-400 animate-spin";
    pulseAnimation = "scale-105";
  } else if (isSpeaking) {
    stateLabel = "L'Agent s'exprime à l'oral...";
    orbGradient = "from-emerald-400 via-teal-500 to-cyan-500 shadow-emerald-500/50";
    pulseAnimation = "scale-105 animate-pulse";
  }

  return (
    <div className="flex flex-col items-center justify-center py-4 relative group">
      
      {/* Ambient Radial Backdrop Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 via-purple-600/20 to-pink-600/20 blur-3xl rounded-full -z-10 transform scale-125 pointer-events-none" />

      {/* Interactive Orb Center */}
      <button
        type="button"
        onClick={onClickMic}
        title={isListening ? "Arrêter l'écoute" : "Cliquer pour parler à l'agent (Microphone)"}
        className={`relative w-24 h-24 sm:w-28 sm:h-28 rounded-full bg-gradient-to-tr ${orbGradient} p-1 shadow-2xl transition-all duration-500 transform hover:scale-105 active:scale-95 flex items-center justify-center cursor-pointer`}
      >
        {/* Outer Ring Pulse Effect */}
        {isListening && (
          <span className="absolute -inset-2 rounded-full border-2 border-rose-400/60 animate-ping pointer-events-none" />
        )}
        
        {isStreaming && (
          <span className="absolute -inset-3 rounded-full border border-purple-400/40 animate-spin pointer-events-none" />
        )}

        {/* Inner Glass Sphere */}
        <div className="w-full h-full rounded-full bg-slate-950/80 backdrop-blur-md flex flex-col items-center justify-center p-3 border border-white/20 relative overflow-hidden">
          
          {/* Animated Core Glow Blob */}
          <div className={`absolute inset-2 rounded-full bg-gradient-to-tr ${orbGradient} opacity-30 blur-md ${pulseAnimation}`} />

          {/* Icon */}
          <div className="relative z-10 text-white flex flex-col items-center gap-1">
            {isStreaming ? (
              <Loader2 className="w-8 h-8 animate-spin text-amber-300" />
            ) : isListening ? (
              <MicOff className="w-8 h-8 text-rose-300 animate-pulse" />
            ) : isSpeaking ? (
              <Volume2 className="w-8 h-8 text-emerald-300 animate-bounce" />
            ) : (
              <Mic className="w-8 h-8 text-blue-300 group-hover:scale-110 transition-transform" />
            )}
          </div>

        </div>
      </button>

      {/* State Label & Voice Feedback Prompt */}
      <div className="mt-3 text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900/90 border border-slate-800 text-xs font-medium text-slate-200 shadow-md">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
          <span>{stateLabel}</span>
        </div>
        <p className="text-[11px] text-slate-500 mt-1">
          {speechSupported ? "Cliquez sur l'orbe pour parler à l'oral ou utilisez le clavier ci-dessous" : "Environnement bruyant ? Posez votre question au clavier ci-dessous"}
        </p>
      </div>

    </div>
  );
}
