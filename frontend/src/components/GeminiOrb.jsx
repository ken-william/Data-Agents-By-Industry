import React from 'react';
import { Mic, MicOff, Sparkles, Volume2 } from 'lucide-react';
import { cn } from '../utils/cn';

/**
 * Gemini Live Physics Wave Orb
 * Implements 3 organic states:
 * 1. Listening: Wave pulse reacting to voice.
 * 2. Thinking: Spinning multicolor gradient ring.
 * 3. Speaking: Emerald & Cyan expanding shockwaves.
 */
export function GeminiOrb({
  isListening,
  isSpeaking,
  isStreaming,
  onClickMic,
  speechSupported = true,
  showcaseMode = false
}) {
  const isThinking = isStreaming && !isSpeaking;

  return (
    <div className="flex flex-col items-center justify-center py-4 relative group">
      
      {/* Orb Physics Container */}
      <div
        onClick={speechSupported ? onClickMic : undefined}
        className={cn(
          "gemini-orb-container cursor-pointer transition-all duration-500",
          showcaseMode ? "scale-110" : "scale-100"
        )}
        title={isListening ? "Arrêter l'écoute" : "Démarrer l'écoute"}
      >

        {/* State 1: Thinking Spinning Multicolor Gradient Ring */}
        {isThinking && <div className="thinking-ring" />}

        {/* State 2: Speaking Emerald & Cyan Circular Shockwaves */}
        {isSpeaking && (
          <>
            <div className="speaking-wave" />
            <div className="speaking-wave speaking-wave-2" />
            <div className="speaking-wave speaking-wave-3" />
          </>
        )}

        {/* State 3: Listening Wave Pulse */}
        {isListening && !isSpeaking && !isThinking && (
          <div className="absolute inset-0 rounded-full border-2 border-sky-400/60 animate-ping" />
        )}

        {/* Living Core Sphere */}
        <div className={cn(
          "gemini-orb-core flex items-center justify-center transition-all duration-300",
          isListening && "scale-110 shadow-[0_0_40px_rgba(56,189,248,0.7)]",
          isThinking && "scale-95 opacity-90",
          isSpeaking && "scale-105 shadow-[0_0_40px_rgba(16,185,129,0.7)]"
        )}>
          {isSpeaking ? (
            <Volume2 className="size-8 text-emerald-300 animate-pulse" />
          ) : isThinking ? (
            <Sparkles className="size-8 text-sky-200 animate-spin" />
          ) : isListening ? (
            <Mic className="size-8 text-white animate-bounce" />
          ) : (
            <Mic className="size-8 text-sky-200/90" />
          )}
        </div>

      </div>

      {/* Dynamic Status Text */}
      <div className="mt-3 text-center">
        <span className={cn(
          "text-xs font-semibold tracking-wide px-3 py-1 rounded-full border transition-all inline-block",
          isSpeaking
            ? "bg-emerald-500/20 text-emerald-300 border-emerald-500/40 animate-pulse"
            : isThinking
            ? "bg-sky-500/20 text-sky-300 border-sky-400/40"
            : isListening
            ? "bg-rose-500/20 text-rose-300 border-rose-500/40"
            : "bg-slate-800/80 text-slate-400 border-slate-700"
        )}>
          {isSpeaking
            ? "• Synthèse Vocale Active (Ondes Émeraude)"
            : isThinking
            ? "• Réflexion BigQuery (Anneau Tourbillonnant)"
            : isListening
            ? "• Écoute en Cours..."
            : "• Cliquer pour Parler"}
        </span>
      </div>

    </div>
  );
}
