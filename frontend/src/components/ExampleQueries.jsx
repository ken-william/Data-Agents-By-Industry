import React from 'react';
import { HelpCircle, ArrowUpRight } from 'lucide-react';
import { COLOR_THEMES } from '../utils/themeMap';

export function ExampleQueries({ queries, selectedAgent, onSelectQuery, disabled }) {
  if (!queries || queries.length === 0) return null;

  const colorKey = selectedAgent?.theme?.color || 'indigo';
  const theme = COLOR_THEMES[colorKey] || COLOR_THEMES.indigo;

  return (
    <div className="w-full mb-4">
      <div className="flex items-center gap-2 mb-2 text-xs font-semibold text-slate-300">
        <HelpCircle className={`w-4 h-4 ${theme.text}`} />
        <span>Exemples de questions métiers validées pour {selectedAgent?.displayName.split(' - ')[0]} :</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
        {queries.map((q, idx) => (
          <button
            key={idx}
            disabled={disabled}
            onClick={() => onSelectQuery(q)}
            className={`group text-left p-3 rounded-lg border text-xs transition-all duration-200 flex items-start justify-between gap-2 ${
              disabled
                ? 'opacity-50 cursor-not-allowed bg-slate-900 border-slate-800 text-slate-500'
                : `glass-card border-slate-800/80 hover:${theme.border} hover:bg-slate-800/80 text-slate-200 hover:text-white`
            }`}
          >
            <span className="line-clamp-2 leading-snug">{q}</span>
            <ArrowUpRight className={`w-4 h-4 shrink-0 transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5 ${theme.text}`} />
          </button>
        ))}
      </div>
    </div>
  );
}
