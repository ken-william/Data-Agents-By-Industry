import React, { useState } from 'react';
import {
  Compass,
  Plus,
  SlidersHorizontal,
  FolderOpen,
  ChevronDown,
  ArrowUp,
  X,
  Sparkles
} from 'lucide-react';
import { getIconComponent } from '../utils/themeMap';
import { cn } from '../utils/cn';

export const CHIPS_SERVICES = [
  { id: 'google', name: 'Google', iconColor: 'text-red-500', logoSvg: (
    <svg className="size-4" viewBox="0 0 24 24">
      <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
      <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
      <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
      <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
    </svg>
  )},
  { id: 'notebooklm', name: 'NotebookLM', logoSvg: (
    <div className="size-4 rounded-full bg-slate-900 flex items-center justify-center text-white text-[9px] font-bold">N</div>
  )},
  { id: 'drive', name: 'Google Drive', logoSvg: (
    <svg className="size-4" viewBox="0 0 87.3 78">
      <path d="m6.6 66.85 3.85 6.65c.8 1.4 1.95 2.5 3.3 3.3l13.75-23.8h-27.5c0 1.55.4 3.1 1.2 4.5z" fill="#0066da"/>
      <path d="m43.65 25-13.75-23.8c-1.35.8-2.5 1.9-3.3 3.3l-25.4 44a9.06 9.06 0 0 0 -1.2 4.5h27.45z" fill="#00ac47"/>
      <path d="m73.55 76.8c1.35-.8 2.5-1.9 3.3-3.3l1.6-2.75 7.65-13.25c.8-1.4 1.2-2.95 1.2-4.5h-27.5l5.85 10.15z" fill="#ea4335"/>
      <path d="m43.65 25 13.75-23.8c-1.35-.8-2.9-1.2-4.5-1.2h-18.5c-1.6 0-3.15.45-4.5 1.2z" fill="#00832d"/>
      <path d="m59.8 50h-32.3l-13.75 23.8c1.35.8 2.9 1.2 4.5 1.2h50.8c1.6 0 3.15-.45 4.5-1.2z" fill="#2684fc"/>
      <path d="m73.4 26.5-12.7-22c-.8-1.4-1.95-2.5-3.3-3.3l-13.75 23.8 16.15 28h27.45c0-1.55-.4-3.1-1.2-4.5z" fill="#ffba00"/>
    </svg>
  )},
  { id: 'buganizer', name: 'Buganizer', logoSvg: (
    <div className="size-4 rounded-full bg-blue-600 flex items-center justify-center text-white text-[9px] font-bold">B</div>
  )},
  { id: 'gmail', name: 'Gmail', logoSvg: (
    <svg className="size-4" viewBox="0 0 24 24">
      <path fill="#4285F4" d="M1.5 18.5V7.5L12 14.25L22.5 7.5v11c0 .83-.67 1.5-1.5 1.5h-18c-.83 0-1.5-.67-1.5-1.5z"/>
      <path fill="#EA4335" d="M22.5 5.5v2L12 14.25L1.5 7.5v-2c0-.83.67-1.5 1.5-1.5h18c.83 0 1.5.67 1.5 1.5z"/>
    </svg>
  )},
  { id: 'yaqs', name: 'YAQS', logoSvg: (
    <div className="size-4 rounded-full bg-emerald-600 flex items-center justify-center text-white text-[9px] font-bold">Y</div>
  )}
];

export function AgentBuilder({ agents, selectedAgent, onSelectAgent, onLaunchLive }) {
  const [promptText, setPromptText] = useState('');
  const [showBanner, setShowBanner] = useState(true);

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (onLaunchLive) {
      onLaunchLive();
    }
  };

  return (
    <div className="w-full min-h-[75vh] flex flex-col items-center justify-center gap-6 my-auto py-4 relative px-4">
      
      {/* 1. Main Greeting Headline "Let's get some work done!" */}
      <h2 className="text-2xl sm:text-3xl font-normal text-[#1F1F1F] tracking-tight text-center">
        Let's get some work done!
      </h2>

      {/* 2. Central Gemini Enterprise Search Card Container */}
      <div className="w-full max-w-2xl">
        <form onSubmit={handleFormSubmit} className="gemini-search-card p-4 sm:p-5 flex flex-col justify-between min-h-[140px] gap-4">
          
          {/* Top Row: Location Icon + Input Field */}
          <div className="flex items-center gap-3">
            <Compass className="size-5 text-slate-400 shrink-0" />
            <input
              type="text"
              value={promptText}
              onChange={(e) => setPromptText(e.target.value)}
              placeholder="Ask Gemini Enterprise"
              className="w-full bg-transparent border-none text-slate-900 placeholder-slate-400 focus:outline-none text-sm sm:text-base font-normal"
            />
          </div>

          {/* Bottom Controls Bar: Left Tools + Right Auto Select & Submit Arrow */}
          <div className="flex items-center justify-between pt-2 border-t border-slate-100">
            
            {/* Left Action Buttons (+, slider, folder) */}
            <div className="flex items-center gap-2">
              <button
                type="button"
                aria-label="Ajouter un document"
                className="size-8 rounded-full hover:bg-slate-100 flex items-center justify-center text-slate-600 transition-colors"
                title="Add files"
              >
                <Plus className="size-4" />
              </button>

              <button
                type="button"
                aria-label="Paramètres de requête"
                className="size-8 rounded-full hover:bg-slate-100 flex items-center justify-center text-slate-600 transition-colors"
                title="Configure query settings"
              >
                <SlidersHorizontal className="size-4" />
              </button>

              <button
                type="button"
                aria-label="Parcourir l'espace Drive"
                className="size-8 rounded-full hover:bg-slate-100 flex items-center justify-center text-slate-600 transition-colors"
                title="Browse Drive"
              >
                <FolderOpen className="size-4" />
              </button>
            </div>

            {/* Right Controls: Auto ▾ Select + Round Submit Arrow */}
            <div className="flex items-center gap-3">
              <button
                type="button"
                className="px-2.5 py-1 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-100 flex items-center gap-1 transition-colors"
              >
                <span>Auto</span>
                <span className="size-1.5 rounded-full bg-blue-600 inline-block" />
                <ChevronDown className="size-3.5 text-slate-500" />
              </button>

              <button
                type="submit"
                aria-label="Lancer la requête Gemini"
                onClick={onLaunchLive}
                disabled={!selectedAgent}
                className={cn(
                  "size-8 rounded-full flex items-center justify-center transition-all",
                  selectedAgent
                    ? "bg-slate-200 hover:bg-[#0B57D0] text-slate-600 hover:text-white"
                    : "bg-slate-100 text-slate-300 cursor-not-allowed"
                )}
                title="Submit prompt"
              >
                <ArrowUp className="size-4" />
              </button>
            </div>

          </div>

        </form>
      </div>

      {/* 3. NEW Banner: "NEW: Try Gemini 3.6 Flash" */}
      {showBanner && (
        <div className="w-full max-w-2xl gemini-banner-new px-4 py-3 flex items-center justify-between gap-3 text-xs text-slate-700">
          <div className="flex items-center gap-2 font-medium">
            <Sparkles className="size-4 text-blue-600" />
            <span>NEW: Try Gemini 3.6 Flash</span>
          </div>

          <button
            type="button"
            aria-label="Fermer la bannière"
            onClick={() => setShowBanner(false)}
            className="p-1 rounded-md hover:bg-blue-100/60 text-slate-400 hover:text-slate-700 transition-colors"
          >
            <X className="size-4" />
          </button>
        </div>
      )}

      {/* 4. Service Chips Row (Google, NotebookLM, Drive, Buganizer, Gmail, YAQS) */}
      <div className="w-full max-w-3xl flex items-center justify-center gap-2.5 flex-wrap pt-2">
        {CHIPS_SERVICES.map((chip, idx) => {
          const matchingAgent = agents[idx % agents.length] || selectedAgent;
          const isSelected = selectedAgent?.id === matchingAgent?.id;

          return (
            <button
              key={chip.id}
              type="button"
              onClick={() => {
                if (matchingAgent) {
                  onSelectAgent(matchingAgent);
                }
              }}
              className={cn("gemini-chip", isSelected && "active")}
            >
              {chip.logoSvg}
              <span>{chip.name}</span>
            </button>
          );
        })}
      </div>

    </div>
  );
}
