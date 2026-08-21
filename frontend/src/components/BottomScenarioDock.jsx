import React, { useRef } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { getIconComponent } from '../utils/themeMap';
import { SCENARIOS } from './ScenarioChips';
import { cn } from '../utils/cn';

/**
 * Minimalist Gemini Extension Scenario Dock (Bottom of Page 2)
 * Aligns the 11 sector scenarios as compact horizontal pills at the bottom of the viewport.
 */
export function BottomScenarioDock({ agents, selectedAgent, onSelectAgent, onSendMessage }) {
  const containerRef = useRef(null);

  const scroll = (direction) => {
    if (containerRef.current) {
      const amount = direction === 'left' ? -280 : 280;
      containerRef.current.scrollBy({ left: amount, behavior: 'smooth' });
    }
  };

  return (
    <div className="w-full flex items-center justify-center gap-2 py-2 max-w-6xl mx-auto px-2 relative">
      
      {/* Scroll Left Button */}
      <button
        type="button"
        aria-label="Défiler les extensions vers la gauche"
        onClick={() => scroll('left')}
        className="size-8 rounded-full bg-white/90 hover:bg-slate-100 border border-slate-200 text-slate-700 transition-all shadow-xs shrink-0 flex items-center justify-center"
        title="Défiler vers la gauche"
      >
        <ChevronLeft className="size-4" />
      </button>

      {/* Extension Chips Dock Container */}
      <div
        ref={containerRef}
        className="extension-chips-container max-w-full scroll-smooth flex items-center gap-2 py-1"
      >
        {SCENARIOS.map((sc) => {
          const isSelected = selectedAgent?.id === sc.id;
          const IconComp = getIconComponent(sc.id);
          const targetAgent = agents.find(a => a.id === sc.id) || selectedAgent;

          return (
            <button
              key={sc.id}
              type="button"
              onClick={() => {
                if (targetAgent) {
                  onSelectAgent(targetAgent);
                }
                if (onSendMessage) {
                  onSendMessage(sc.prompt);
                }
              }}
              className={cn(
                "inline-flex items-center gap-2 px-3.5 py-2 rounded-full border text-xs font-medium transition-all shadow-2xs whitespace-nowrap shrink-0",
                isSelected
                  ? "bg-[#0B57D0] text-white border-[#0B57D0] shadow-xs"
                  : "bg-white/90 hover:bg-blue-50 text-slate-800 border-slate-200/90 hover:border-blue-300"
              )}
            >
              <IconComp className={cn("size-3.5", isSelected ? "text-white" : "text-[#0B57D0]")} />
              <span>{sc.name}</span>
            </button>
          );
        })}
      </div>

      {/* Scroll Right Button */}
      <button
        type="button"
        aria-label="Défiler les extensions vers la droite"
        onClick={() => scroll('right')}
        className="size-8 rounded-full bg-white/90 hover:bg-slate-100 border border-slate-200 text-slate-700 transition-all shadow-xs shrink-0 flex items-center justify-center"
        title="Défiler vers la droite"
      >
        <ChevronRight className="size-4" />
      </button>

    </div>
  );
}
