import React, { useRef } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { getIconComponent } from '../utils/themeMap';
import { SCENARIOS } from './ScenarioChips';
import { cn } from '../utils/cn';

/**
 * Minimalist Gemini Extension Scenario Dock (Bottom of Page 2)
 * Aligns the 11 sector scenarios as compact horizontal pills inside a smooth slider.
 * Clicking a scenario chip switches to that agent's space & suggested questions without auto-querying!
 */
export function BottomScenarioDock({ agents, selectedAgent, onSelectAgent, onResetChat }) {
  const containerRef = useRef(null);

  const scroll = (direction) => {
    if (containerRef.current) {
      const amount = direction === 'left' ? -260 : 260;
      containerRef.current.scrollBy({ left: amount, behavior: 'smooth' });
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto flex items-center justify-between gap-2 py-2 px-1 relative">
      
      {/* Scroll Left Button */}
      <button
        type="button"
        aria-label="Défiler les extensions vers la gauche"
        onClick={() => scroll('left')}
        className="size-8 rounded-full bg-white/90 hover:bg-slate-100 border border-slate-200 text-slate-700 transition-all shadow-xs shrink-0 flex items-center justify-center cursor-pointer z-10"
        title="Défiler vers la gauche"
      >
        <ChevronLeft className="size-4" />
      </button>

      {/* Strictly Constrained Extension Dock Slider Container */}
      <div className="flex-1 min-w-0 overflow-hidden relative">
        <div
          ref={containerRef}
          className="extension-chips-container flex items-center gap-2.5 overflow-x-auto scroll-smooth no-scrollbar py-1 px-1"
        >
          {SCENARIOS.map((sc) => {
            const isSelected = selectedAgent?.id === sc.id;
            const IconComp = getIconComponent(sc.id);
            const targetAgent = agents.find(a => a.id === sc.id) || { id: sc.id, displayName: sc.name, datasetId: sc.id };

            return (
              <button
                key={sc.id}
                type="button"
                onClick={() => {
                  if (onSelectAgent) {
                    onSelectAgent(targetAgent);
                  }
                  if (onResetChat) {
                    onResetChat();
                  }
                }}
                className={cn(
                  "inline-flex items-center gap-2 px-3.5 py-2 rounded-full border text-xs font-semibold transition-all shadow-2xs whitespace-nowrap shrink-0 cursor-pointer select-none",
                  isSelected
                    ? "bg-[#0B57D0] text-white border-[#0B57D0] shadow-xs scale-[1.02]"
                    : "bg-white/90 hover:bg-blue-50 text-slate-800 border-slate-200/90 hover:border-blue-300"
                )}
              >
                <IconComp className={cn("size-3.5", isSelected ? "text-white" : "text-[#0B57D0]")} />
                <span>{sc.name}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Scroll Right Button */}
      <button
        type="button"
        aria-label="Défiler les extensions vers la droite"
        onClick={() => scroll('right')}
        className="size-8 rounded-full bg-white/90 hover:bg-slate-100 border border-slate-200 text-slate-700 transition-all shadow-xs shrink-0 flex items-center justify-center cursor-pointer z-10"
        title="Défiler vers la droite"
      >
        <ChevronRight className="size-4" />
      </button>

    </div>
  );
}
