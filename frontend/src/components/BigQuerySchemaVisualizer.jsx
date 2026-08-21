import React from 'react';
import { Database, GitCommit, Loader2, Sparkles, Table } from 'lucide-react';

/**
 * BigQuery Interactive Table Join Schema Visualizer
 * Displayed during loading/storytelling when Vertex AI agents query BigQuery tables.
 */
export function BigQuerySchemaVisualizer({ datasetId = 'public_sector_employment_ds', agentName = 'Copilote BigQuery' }) {
  return (
    <div className="w-full p-6 rounded-2xl bg-white/95 border border-slate-200 shadow-md backdrop-blur-xl animate-fade-in my-3 text-slate-800">
      
      {/* Visualizer Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-200 mb-4">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-blue-50 text-[#0B57D0] border border-blue-200">
            <Database className="size-4 animate-pulse" />
          </div>
          <div>
            <h4 className="text-xs font-bold text-slate-900 flex items-center gap-2 font-['Google_Sans_Flex']">
              <span>Execution BigQuery & Storytelling Data</span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-blue-50 text-[#0B57D0] font-semibold border border-blue-200">
                • Traitement SQL Live
              </span>
            </h4>
            <p className="text-[11px] text-slate-500 font-mono">
              Dataset: `{datasetId}`
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs font-semibold text-[#0B57D0] bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
          <Loader2 className="size-3.5 animate-spin" />
          <span>Calcul des Agrégations...</span>
        </div>
      </div>

      {/* Interactive Schema Diagram Nodes */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 my-2 items-center text-center">
        
        {/* Node 1: Source Table */}
        <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs flex flex-col items-center gap-1.5 shadow-2xs">
          <Table className="size-4 text-[#0B57D0]" />
          <span className="font-bold text-slate-900 text-[11px]">Table Principale</span>
          <span className="font-mono text-[10px] text-slate-500 truncate w-full">`{datasetId}.raw_kpis`</span>
        </div>

        {/* Join Connection Pipeline */}
        <div className="flex flex-col items-center justify-center gap-1 text-slate-400 py-1">
          <div className="w-full flex items-center justify-center gap-1">
            <span className="h-px bg-blue-300 flex-1 animate-pulse" />
            <GitCommit className="size-4 text-[#0B57D0] animate-bounce" />
            <span className="h-px bg-blue-300 flex-1 animate-pulse" />
          </div>
          <span className="text-[10px] font-mono text-blue-700 font-medium">INNER JOIN & GroupBy</span>
        </div>

        {/* Node 2: Analytics Result View */}
        <div className="p-3.5 rounded-xl bg-blue-50 border border-blue-200 text-xs flex flex-col items-center gap-1.5 shadow-2xs">
          <Sparkles className="size-4 text-[#0B57D0]" />
          <span className="font-bold text-slate-900 text-[11px]">Vue Synthétisée</span>
          <span className="font-mono text-[10px] text-[#0B57D0] truncate w-full">`{datasetId}.business_summary`</span>
        </div>

      </div>

      {/* Narrator Storytelling Active Sentence */}
      <div className="mt-4 p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 flex items-start gap-2.5">
        <Sparkles className="size-4 text-[#0B57D0] shrink-0 mt-0.5" />
        <p className="leading-relaxed font-medium">
          <strong className="text-slate-900">L'Agent Hôte synthétise vos données :</strong> "Je consulte à l'instant vos tables BigQuery... Saviez-vous que ce jeu de données open-data contient des milliers d'entrées d'historique ? Je génère votre synthèse décisionnelle immédiatement..."
        </p>
      </div>

    </div>
  );
}
