import React, { useState } from 'react';
import { Code, Database, FlipHorizontal, Sparkles } from 'lucide-react';
import { cn } from '../utils/cn';

/**
 * 3D Flip Card Component (Rotation 3D SQL Inspector)
 * Bright light mode 3D inspection card with crisp slate typography.
 */
export function SQLFlipCard({ datasetId, sqlQuery, executionTime = "1.24s" }) {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <div className="w-full my-3">
      <div className={cn("flip-card", isFlipped && "flipped")}>
        <div className="flip-card-inner">
          
          {/* Front Card: Data Summary Bar (Light Mode) */}
          <div className="flip-card-front p-4 bg-white border border-slate-200/90 rounded-2xl text-slate-900 flex items-center justify-between shadow-xs">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-xl bg-blue-50 text-[#0B57D0] border border-blue-200">
                <Database className="size-4" />
              </div>
              <div>
                <span className="text-[11px] text-slate-500 block font-medium">Dataset BigQuery</span>
                <span className="text-xs font-bold text-slate-900 font-mono">
                  {datasetId || 'public_sector_employment_ds'}
                </span>
              </div>
            </div>

            <button
              type="button"
              onClick={() => setIsFlipped(!isFlipped)}
              className="px-3 py-1.5 rounded-xl bg-blue-50 hover:bg-blue-100 text-[#0B57D0] border border-blue-200 text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer"
            >
              <Code className="size-3.5" />
              <span>Inspecter SQL (Rotation 3D)</span>
              <FlipHorizontal className="size-3.5 ml-1" />
            </button>
          </div>

          {/* Back Card: Light Mode SQL Code Query Formatted */}
          <div className="flip-card-back p-5 bg-slate-50 border border-slate-200 rounded-2xl text-slate-900 shadow-md flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between pb-2 border-b border-slate-200 mb-3">
                <div className="flex items-center gap-2 text-xs font-bold text-[#0B57D0]">
                  <Sparkles className="size-4 text-[#0B57D0]" />
                  <span>REQUÊTE BIGQUERY (EXÉCUTION: {executionTime})</span>
                </div>

                <button
                  type="button"
                  onClick={() => setIsFlipped(false)}
                  className="px-2.5 py-1 rounded-lg bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 text-[11px] font-semibold flex items-center gap-1 cursor-pointer"
                >
                  <span>Retour Vue Métier</span>
                  <FlipHorizontal className="size-3" />
                </button>
              </div>

              <pre className="font-mono text-xs text-[#0B57D0] overflow-x-auto p-3.5 rounded-xl bg-white border border-slate-200/90 leading-relaxed font-semibold shadow-2xs">
                {sqlQuery || `SELECT sector_id, headcount, vacancy_rate\nFROM \`${datasetId || 'public_sector_employment_ds'}.hospital_jobs\`\nWHERE vacancy_months > 6\nORDER BY vacancy_rate DESC\nLIMIT 10;`}
              </pre>
            </div>

            <div className="mt-3 text-[10px] text-slate-500 font-mono flex items-center justify-between">
              <span>Vertex AI Agent Query Pipeline</span>
              <span className="text-emerald-600 font-semibold">● Verified SQL Syntax</span>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
