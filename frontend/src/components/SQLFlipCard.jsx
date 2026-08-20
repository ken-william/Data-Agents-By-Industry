import React, { useState } from 'react';
import { Code2, Database, Check, Copy } from 'lucide-react';

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
    <div className="w-full my-2">
      <button
        type="button"
        onClick={() => setIsFlipped(!isFlipped)}
        className="flex items-center gap-2 px-2.5 py-1 rounded-md bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-xs font-mono text-cyan-400 transition-colors"
      >
        <Code2 className="w-3.5 h-3.5" />
        <span>{isFlipped ? "Masquer SQL" : "Voir requête SQL BigQuery générée"}</span>
        {executionTime && <span className="text-[10px] text-zinc-500 font-sans">({executionTime})</span>}
      </button>

      {isFlipped && (
        <div className="mt-2 p-3 rounded-lg bg-[#09090b] border border-cyan-500/30 font-mono text-xs text-cyan-300 shadow-lg relative">
          <div className="flex items-center justify-between gap-2 pb-2 mb-2 border-b border-zinc-800 text-[11px] text-zinc-400">
            <div className="flex items-center gap-1.5">
              <Database className="w-3.5 h-3.5 text-cyan-400" />
              <span>Dataset: <strong className="text-zinc-200">{datasetId}</strong></span>
            </div>
            
            <button
              onClick={handleCopy}
              className="flex items-center gap-1 px-2 py-0.5 rounded bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 transition-colors text-[10px]"
            >
              {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
              <span>{copied ? "Copié !" : "Copier"}</span>
            </button>
          </div>

          <pre className="overflow-x-auto whitespace-pre-wrap leading-relaxed text-cyan-300 p-2 rounded bg-zinc-950 border border-zinc-900">
            <code>{sqlQuery}</code>
          </pre>
        </div>
      )}
    </div>
  );
}
