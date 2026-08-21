import React from 'react';
import { cn } from '../utils/cn';

/**
 * Gemini Live Slime Liquid 3D Mesh Orb
 * Fluid organic living AI character without static microphone icon.
 * Features 3 liquid physics states:
 * 1. Listening: Liquid mesh expands & ripples to human voice.
 * 2. Thinking: Inner spinning multicolor ring & cell contraction.
 * 3. Speaking: Organic emerald & cyan shockwaves pulsating with voice.
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
    <div className="flex flex-col items-center justify-center py-2 relative group">
      
      {/* Liquid Slime Physics Container */}
      <div
        onClick={speechSupported ? onClickMic : undefined}
        className={cn(
          "gemini-orb-container cursor-pointer transition-all duration-500",
          showcaseMode ? "scale-110" : "scale-100"
        )}
        title={isListening ? "Cliquer pour désactiver l'écoute active" : "Cliquer pour activer l'écoute active"}
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

        {/* State 3: Listening Wave Ripple */}
        {isListening && !isSpeaking && !isThinking && (
          <div className="absolute inset-0 rounded-full border-2 border-[#0B57D0]/60 animate-ping" />
        )}

        {/* Slime Fluid Liquid 3D Core Blob (No static microphone icon inside!) */}
        <div className={cn(
          "gemini-orb-chroma flex items-center justify-center transition-all duration-500 rounded-[45%_55%_60%_40%/50%_45%_55%_50%] animate-pulse",
          isListening && "scale-110 shadow-[0_0_50px_rgba(11,87,208,0.6)] animate-bounce",
          isThinking && "scale-95 opacity-90 rotate-45",
          isSpeaking && "scale-105 shadow-[0_0_50px_rgba(16,185,129,0.6)]"
        )}>
          {/* Inner Liquid Fusion Glow Dot */}
          <div className="size-5 rounded-full bg-white/80 blur-xs shadow-inner animate-ping" />
        </div>

      </div>

      {/* Dynamic Status Text */}
      <div className="mt-2 text-center">
        <span className={cn(
          "text-xs font-semibold tracking-wide px-3 py-1 rounded-full border transition-all inline-block shadow-2xs",
          isSpeaking
            ? "bg-emerald-50 text-emerald-700 border-emerald-200 animate-pulse"
            : isThinking
            ? "bg-blue-50 text-[#0B57D0] border-blue-200"
            : isListening
            ? "bg-rose-50 text-rose-700 border-rose-200"
            : "bg-slate-100 text-slate-600 border-slate-200"
        )}>
          {isSpeaking
            ? "• Agent Hôte : Synthèse Vocale Active"
            : isThinking
            ? "• Agent Hôte : Consultation BigQuery..."
            : isListening
            ? "• Agent Hôte : Écoute Active Gemini Live"
            : "• Micro Désactivé (Cliquer pour Activer)"}
        </span>
      </div>

    </div>
  );
}
