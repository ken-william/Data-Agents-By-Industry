import React from 'react';
import { ArrowRight, Bot } from 'lucide-react';
import { cn } from '../utils/cn';

export function AgentBuilder({ agents, selectedAgent, onSelectAgent, onLaunchLive }) {
  return (
    <div className="w-full max-w-4xl mx-auto py-12 px-4 flex flex-col items-center justify-center text-center gap-8 my-auto">
      
      {/* Title */}
      <div>
        <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 tracking-tight">
          Talk to Data
        </h2>
        <p className="text-slate-500 text-sm mt-2 max-w-md mx-auto">
          Sélectionnez un agent sectoriel ci-dessous pour démarrer une nouvelle conversation décisionnelle BigQuery.
        </p>
      </div>

      {/* Agents Selection Grid */}
      <div className="w-full grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 text-left">
        {agents.map((agent) => {
          const isSelected = selectedAgent?.id === agent.id;

          return (
            <button
              key={agent.id}
              type="button"
              onClick={() => onSelectAgent(agent)}
              className={cn(
                "p-4 rounded-2xl border text-xs flex flex-col justify-between gap-3 transition-all",
                isSelected
                  ? "bg-blue-600 text-white border-blue-600 shadow-sm"
                  : "bg-white text-slate-800 border-slate-200 hover:border-blue-400 hover:bg-slate-50"
              )}
            >
              <div className="flex items-center gap-2">
                <Bot className="size-4 shrink-0" />
                <span className="font-bold truncate">{agent.displayName ? agent.displayName.split(' - ')[0] : agent.id}</span>
              </div>
              <span className={cn("text-[11px] line-clamp-2", isSelected ? "text-blue-100" : "text-slate-500")}>
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
          "px-6 py-3 rounded-full font-bold text-sm flex items-center gap-2 transition-all shadow-sm",
          selectedAgent
            ? "bg-slate-900 text-white hover:bg-slate-800"
            : "bg-slate-200 text-slate-400 cursor-not-allowed"
        )}
      >
        <span>Lancer la conversation</span>
        <ArrowRight className="size-4" />
      </button>

    </div>
  );
}
