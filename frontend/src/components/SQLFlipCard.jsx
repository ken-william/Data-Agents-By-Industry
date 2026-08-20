import React, { useState } from 'react';
import { Code2, Database, Sparkles, Check, Copy } from 'lucide-react';

export function SQLFlipCard({ sqlQuery, datasetId, executionTime }) {
  const [isFlipped, setIsFlipped] = useState(false);
  const [copied, setCopied] = useState(false);

  if (!sqlQuery) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(sqlQuery);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="w-full my-3">
      
      {/* Toggle Button */}
      <button
        type="button"
        onClick={() => setIsFlipped(!isFlipped)}
        className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-mono text-cyan-300 hover:text-cyan-200 transition-all shadow-md"
      >
        <Code2 className="w-4 h-4 text-cyan-400" />
        <span>{isFlipped ? "Masquer le code SQL BigQuery" : "🔍 Voir le code sous le capot (Requete BigQuery)"}</span>
        {executionTime && <span className="text-[10px] text-slate-500 font-sans">({executionTime})</span>}
      </button>

      {/* Expanded Neon SQL Inspector Card */}
      {isFlipped && (
        <div className="mt-2.5 p-4 rounded-2xl bg-slate-950 border border-cyan-500/30 font-mono text-xs text-cyan-200 shadow-2xl relative overflow-hidden group">
          
          {/* Header toolbar */}
          <div className="flex items-center justify-between gap-2 pb-2.5 mb-2.5 border-b border-slate-800 text-[11px] text-slate-400">
            <div className="flex items-center gap-2">
              <Database className="w-3.5 h-3.5 text-cyan-400" />
              <span>Dataset: <strong className="text-white">{datasetId}</strong></span>
            </div>
            
            <button
              onClick={handleCopy}
              className="flex items-center gap-1 px-2 py-1 rounded bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 hover:text-white transition-colors"
            >
              {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
              <span>{copied ? "Copie !" : "Copier SQL"}</span>
            </button>
          </div>

          {/* Code View */}
          <pre className="overflow-x-auto whitespace-pre-wrap leading-relaxed text-cyan-300 selection:bg-cyan-500 selection:text-slate-950 p-2 rounded bg-slate-900/60 border border-slate-800/80">
            <code>{sqlQuery}</code>
          </pre>

          {/* Footer note */}
          <div className="mt-2 text-[10px] text-slate-500 flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-cyan-400" />
            <span>Généré et optimisé automatiquement par le moteur Gemini Conversational Analytics</span>
          </div>

        </div>
      )}

    </div>
  );
}
