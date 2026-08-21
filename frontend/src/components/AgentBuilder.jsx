import React from 'react';
import { ArrowRight, Bot, Sparkles } from 'lucide-react';
import { cn } from '../utils/cn';

export function AgentBuilder({ agents, selectedAgent, onSelectAgent, onLaunchLive }) {
  return (
    <div className="w-full max-w-4xl mx-auto py-12 px-4 flex flex-col items-center justify-center text-center gap-8 my-auto">
      
      {/* Title */}
      <div className="space-y-3">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/15 border border-white/25 text-white text-xs font-semibold backdrop-blur-md shadow-xs">
          <Sparkles className="size-3.5 text-sky-300" />
          <span>Vertex AI Data Agents • BigData 2026</span>
        </div>

        <h2 className="text-4xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight">
          Talk to <span className="text-sky-300">Data</span>
        </h2>
        
        <p className="text-blue-100 text-sm sm:text-base max-w-xl mx-auto font-medium leading-relaxed">
          Sélectionnez un agent sectoriel ci-dessous pour démarrer une nouvelle conversation décisionnelle BigQuery en langage naturel.
        </p>
      </div>

      {/* Agents Selection Grid */}
      <div className="w-full grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3.5 text-left">
        {agents.map((agent) => {
          const isSelected = selectedAgent?.id === agent.id;

          return (
            <button
              key={agent.id}
              type="button"
              onClick={() => onSelectAgent(agent)}
              className={cn(
                "p-4 rounded-2xl border text-xs flex flex-col justify-between gap-3 transition-all backdrop-blur-xl shadow-md",
                isSelected
                  ? "bg-white text-slate-900 border-white shadow-xl scale-[1.02]"
                  : "bg-white/15 text-white border-white/20 hover:bg-white/25 hover:border-white/40"
              )}
            >
              <div className="flex items-center gap-2">
                <Bot className={cn("size-4 shrink-0", isSelected ? "text-blue-600" : "text-sky-300")} />
                <span className="font-bold truncate">{agent.displayName ? agent.displayName.split(' - ')[0] : agent.id}</span>
              </div>
              <span className={cn("text-[11px] line-clamp-2 leading-relaxed", isSelected ? "text-slate-600" : "text-blue-100/90")}>
                {agent.description}
              </span>
            </button>
          );
        })}
      </div>

      {/* Start Button */}
      <button
        type="button"
        onClick={onLaunchLive}
        disabled={!selectedAgent}
        className={cn(
          "px-7 py-3.5 rounded-full font-bold text-sm flex items-center gap-2.5 transition-all shadow-lg",
          selectedAgent
            ? "bg-white text-blue-900 hover:bg-blue-50 shadow-white/20 hover:scale-105 active:scale-95"
            : "bg-white/20 text-white/40 cursor-not-allowed border border-white/10"
        )}
      >
        <span>Lancer la conversation</span>
        <ArrowRight className="size-4" />
      </button>

    </div>
  );
}
