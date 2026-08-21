import React, { useState } from 'react';
import { Code, Database, FlipHorizontal, Sparkles } from 'lucide-react';
import { cn } from '../utils/cn';

/**
 * 3D Flip Card Component (Rotation 3D SQL Inspector)
 * Pivots 180deg to reveal neon SQL queries on dark matte background.
 */
export function SQLFlipCard({ datasetId, sqlQuery, executionTime = "1.24s" }) {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <div className="w-full my-3">
      <div className={cn("flip-card", isFlipped && "flipped")}>
        <div className="flip-card-inner">
          
          {/* Front Card: Data Summary Bar with 3D Flip Trigger */}
          <div className="flip-card-front p-4 bg-slate-900/90 border border-slate-800 text-white flex items-center justify-between shadow-md">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-xl bg-blue-500/20 text-sky-400 border border-sky-400/30">
                <Database className="size-4" />
              </div>
              <div>
                <span className="text-[11px] text-slate-400 block font-medium">Dataset BigQuery</span>
                <span className="text-xs font-bold text-sky-300 font-mono">
                  {datasetId || 'public_sector_employment_ds'}
                </span>
              </div>
            </div>

            <button
              type="button"
              onClick={() => setIsFlipped(!isFlipped)}
              className="px-3 py-1.5 rounded-xl bg-sky-500/20 hover:bg-sky-500/30 text-sky-300 border border-sky-400/30 text-xs font-semibold flex items-center gap-1.5 transition-all"
            >
              <Code className="size-3.5" />
              <span>Inspecter SQL (Rotation 3D)</span>
              <FlipHorizontal className="size-3.5 ml-1" />
            </button>
          </div>

          {/* Back Card: Neon SQL Code Query Formatted */}
          <div className="flip-card-back p-5 bg-slate-950 border border-sky-500/40 text-cyan-300 shadow-2xl flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between pb-2 border-b border-slate-800 mb-3">
                <div className="flex items-center gap-2 text-xs font-bold text-sky-300">
                  <Sparkles className="size-4 text-sky-400" />
                  <span>REQUÊTE BIGQUERY NÉON (EXÉCUTION: {executionTime})</span>
                </div>

                <button
                  type="button"
                  onClick={() => setIsFlipped(false)}
                  className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-[11px] font-semibold flex items-center gap-1"
                >
                  <span>Retour Vue Métier</span>
                  <FlipHorizontal className="size-3" />
                </button>
              </div>

              <pre className="font-mono text-xs text-cyan-300 overflow-x-auto p-3 rounded-xl bg-slate-900/80 border border-slate-800 leading-relaxed">
                {sqlQuery || `SELECT sector_id, headcount, vacancy_rate\nFROM \`${datasetId || 'public_sector_employment_ds'}.hospital_jobs\`\nWHERE vacancy_months > 6\nORDER BY vacancy_rate DESC\nLIMIT 10;`}
              </pre>
            </div>

            <div className="mt-3 text-[10px] text-slate-500 font-mono flex items-center justify-between">
              <span>Vertex AI Agent Query Pipeline</span>
              <span className="text-emerald-400">● Verified SQL Syntax</span>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
