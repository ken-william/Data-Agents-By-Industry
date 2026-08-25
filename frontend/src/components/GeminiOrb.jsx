import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '../utils/cn';

/**
 * Gemini Live Slime Liquid 3D Mesh Orb
 * Fluid organic living AI character without static microphone icon.
 * Features Apple / Emil Kowalski spring physics & organic liquid morphing filters:
 * 1. Floating levitation (vertical gravitational floating).
 * 2. Listening: Expands & stretches horizontally with voice frequency waves.
 * 3. Thinking: Contracts into a spinning multicolor energy vortex.
 * 4. Speaking: Organically pulses to voice cadence with emerald shockwaves.
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
      
      {/* SVG Liquid Morphing Filter */}
      <svg className="hidden">
        <defs>
          <filter id="slime-goo">
            <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="blur" />
            <feColorMatrix
              in="blur"
              mode="matrix"
              values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 19 -9"
              result="goo"
            />
            <feComposite in="SourceGraphic" in2="goo" operator="atop" />
          </filter>
        </defs>
      </svg>

      {/* Floating Levitation Container (Emil Kowalski Spring Physics) */}
      <motion.div
        animate={{
          y: isSpeaking ? [0, -6, 0] : isThinking ? [0, 4, 0] : [0, -10, 0],
          scale: isSpeaking ? 1.08 : isThinking ? 0.92 : isListening ? 1.12 : 1
        }}
        transition={{
          y: {
            duration: isSpeaking ? 1.2 : isThinking ? 1.5 : 3.5,
            repeat: Infinity,
            ease: "easeInOut"
          },
          scale: {
            type: "spring",
            stiffness: 300,
            damping: 20
          }
        }}
        onClick={speechSupported ? onClickMic : undefined}
        className={cn(
          "gemini-orb-container cursor-pointer relative flex items-center justify-center transition-all duration-500",
          showcaseMode ? "scale-110" : "scale-100"
        )}
        title={isListening ? "Cliquer pour désactiver l'écoute active" : "Cliquer pour activer l'écoute active"}
      >

        {/* State 1: Thinking Spinning Multicolor Gradient Ring */}
        {isThinking && (
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="absolute inset-0 rounded-full border-4 border-transparent border-t-[#38BDF8] border-r-[#818CF8] border-b-[#34A853] shadow-[0_0_30px_rgba(56,189,248,0.5)]"
          />
        )}

        {/* State 2: Speaking Emerald & Cyan Shockwaves */}
        {isSpeaking && (
          <>
            <motion.div
              animate={{ scale: [1, 1.4, 1], opacity: [0.6, 0, 0.6] }}
              transition={{ duration: 1.5, repeat: Infinity, ease: "easeOut" }}
              className="absolute inset-0 rounded-full bg-emerald-400/30 blur-md"
            />
            <motion.div
              animate={{ scale: [1, 1.6, 1], opacity: [0.4, 0, 0.4] }}
              transition={{ duration: 1.8, repeat: Infinity, ease: "easeOut", delay: 0.3 }}
              className="absolute inset-0 rounded-full bg-sky-400/25 blur-lg"
            />
          </>
        )}

        {/* State 3: Listening Ripple */}
        {isListening && !isSpeaking && !isThinking && (
          <motion.div
            animate={{ scale: [1, 1.35, 1], opacity: [0.7, 0.1, 0.7] }}
            transition={{ duration: 1.6, repeat: Infinity, ease: "easeInOut" }}
            className="absolute inset-0 rounded-full border-2 border-[#0B57D0]/60 shadow-[0_0_25px_rgba(11,87,208,0.4)]"
          />
        )}

        {/* Slime Fluid Liquid 3D Core Blob (Pure sphere, no microphone icon!) */}
        <motion.div
          animate={{
            borderRadius: isSpeaking
              ? ["40% 60% 70% 30% / 50% 30% 70% 50%", "60% 40% 30% 70% / 40% 60% 40% 60%", "40% 60% 70% 30% / 50% 30% 70% 50%"]
              : isThinking
              ? ["50% 50% 50% 50%", "45% 55% 45% 55%", "50% 50% 50% 50%"]
              : ["45% 55% 60% 40% / 50% 45% 55% 50%", "55% 45% 40% 60% / 45% 55% 50% 45%", "45% 55% 60% 40% / 50% 45% 55% 50%"]
          }}
          transition={{
            duration: isSpeaking ? 1.8 : 4,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className={cn(
            "gemini-orb-chroma size-24 flex items-center justify-center shadow-xl transition-all relative overflow-hidden",
            isListening && "shadow-[0_0_50px_rgba(11,87,208,0.6)]",
            isThinking && "shadow-[0_0_40px_rgba(56,189,248,0.7)]",
            isSpeaking && "shadow-[0_0_55px_rgba(16,185,129,0.7)]"
          )}
        >
          {/* Inner Liquid Fusion Perlin Noise Mesh */}
          <div className="absolute inset-0 bg-gradient-to-tr from-[#0B57D0] via-[#38BDF8] to-[#818CF8] opacity-90 animate-pulse" />
          
          {/* Inner Floating Energy Nucleus */}
          <motion.div
            animate={{ scale: [0.8, 1.2, 0.8], opacity: [0.7, 1, 0.7] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
            className="size-7 rounded-full bg-white/90 blur-xs shadow-inner z-10"
          />
        </motion.div>

      </motion.div>

      {/* Dynamic Status Text */}
      <motion.div
        initial={{ opacity: 0, y: 5 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ type: "spring", stiffness: 400, damping: 25 }}
        className="mt-2 text-center"
      >
        <span className={cn(
          "text-xs font-semibold tracking-wide px-3.5 py-1 rounded-full border transition-all inline-block shadow-2xs font-['Google_Sans']",
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
      </motion.div>

    </div>
  );
}
