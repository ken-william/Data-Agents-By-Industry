import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { GeminiOrb } from './GeminiOrb';
import { SQLFlipCard } from './SQLFlipCard';
import { BigQuerySchemaVisualizer } from './BigQuerySchemaVisualizer';
import { BottomScenarioDock } from './BottomScenarioDock';
import {
  Bot,
  User,
  Brain,
  ChevronDown,
  ChevronUp,
  AlertCircle,
  Loader2,
  Send,
  ArrowRight,
  RotateCcw,
  Sparkles,
  ChevronLeft,
  Mic,
  MicOff,
  Search,
  Code2
} from 'lucide-react';
import { getIconComponent } from '../utils/themeMap';

export function LiveCanvas({
  agents = [],
  selectedAgent,
  onSelectAgent,
  onReturnToBuilder,
  messages,
  isStreaming,
  thoughts,
  error,
  onSendMessage,
  geminiLiveProps,
  voiceProps,
  onResetChat,
  screenMode = 'showcase'
}) {
  const [inputPrompt, setInputPrompt] = useState('');
  const [showThoughts, setShowThoughts] = useState(false);
  const [showSQLInspector, setShowSQLInspector] = useState(false);

  const AgentIcon = selectedAgent ? getIconComponent(selectedAgent.id) : Bot;
  
  const liveActive = geminiLiveProps?.isLiveStreaming || voiceProps?.isLiveStreaming || voiceProps?.isListening;
  const isSpeaking = geminiLiveProps?.isSpeaking || voiceProps?.isSpeaking;

  const handleToggleMic = () => {
    if (geminiLiveProps) {
      if (geminiLiveProps.isLiveStreaming) {
        geminiLiveProps.stopMicStreaming();
      } else {
        geminiLiveProps.startMicStreaming();
      }
    } else if (voiceProps) {
      if (voiceProps.isListening) {
        voiceProps.stopListening();
      } else {
        voiceProps.startListening();
      }
    }
  };

  // Zero-Chat Scroll Architecture: Get only the LATEST assistant response & user prompt
  const lastUserMessage = [...messages].reverse().find(m => m.role === 'user');
  const lastAssistantMessage = [...messages].reverse().find(m => m.role === 'assistant');

  const handleInputChange = (e) => {
    setInputPrompt(e.target.value);
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (!inputPrompt.trim() || isStreaming) return;
    onSendMessage(inputPrompt);
    setInputPrompt('');
  };

  const isShowcase = screenMode === 'showcase';

  return (
    <div className="w-full flex flex-col gap-6 animate-fade-in relative pb-8 px-4 max-w-4xl mx-auto font-['Google_Sans']">
      
      {/* Top Header Navbar */}
      <div className="fluo-header flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={onReturnToBuilder}
            className="px-3.5 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition-all flex items-center gap-1.5 text-xs font-semibold cursor-pointer"
          >
            <ChevronLeft className="size-4" />
            <span>Accueil</span>
          </button>

          <div className="h-4 w-px bg-slate-200 hidden sm:block" />

          <div className="flex items-center gap-2.5">
            <div className="p-1.5 rounded-xl bg-blue-50 border border-blue-200 text-[#0B57D0]">
              <AgentIcon className="size-4" />
            </div>
            <div>
              <h3 className="text-xs sm:text-sm font-bold text-slate-900 flex items-center gap-2 font-['Google_Sans_Flex']">
                {selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : selectedAgent?.id}
                <span className="text-[11px] px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-medium">
                  • Gemini Live 24kHz
                </span>
              </h3>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Subtle Discrete SQL Inspector Button */}
          <button
            type="button"
            onClick={() => setShowSQLInspector(!showSQLInspector)}
            className={`px-3 py-1.5 rounded-full text-xs font-semibold transition-all flex items-center gap-1.5 cursor-pointer ${
              showSQLInspector
                ? 'bg-slate-900 text-cyan-300 shadow-md'
                : 'bg-blue-50 hover:bg-blue-100 text-[#0B57D0] border border-blue-200'
            }`}
          >
            <Code2 className="size-3.5" />
            <span>{showSQLInspector ? 'Vue Métier' : '⚡ Inspecter le SQL'}</span>
          </button>

          <button
            type="button"
            onClick={onResetChat}
            aria-label="Recommencer"
            title="Effacer et recommencer"
            className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 border border-slate-200 text-xs cursor-pointer"
          >
            <RotateCcw className="size-4" />
          </button>
        </div>
      </div>

      {/* Top Centered Slime Liquid Gemini Orb & Master Host Narrator Speech Bubble */}
      <div className="flex flex-col items-center justify-center text-center space-y-2 py-1">
        <GeminiOrb
          isListening={liveActive}
          isSpeaking={isSpeaking}
          isStreaming={isStreaming}
          onClickMic={handleToggleMic}
          speechSupported={true}
          showcaseMode={isShowcase}
        />

        {/* Master AI Host Storytelling Narrator Bubble */}
        <p className="text-xs sm:text-sm font-medium text-slate-600 max-w-lg leading-relaxed italic bg-white/80 px-4 py-2 rounded-full border border-slate-200/80 shadow-2xs">
          {isSpeaking
            ? '"Dialogue Gemini Live en direct..."'
            : isStreaming
            ? '"Raisonnement et consultation BigQuery en cours..."'
            : lastUserMessage
            ? `"${lastUserMessage.content}"`
            : `"Bonjour ! Je suis connecté en direct avec Gemini Live. Parlez-moi ou posez votre question."`}
        </p>
      </div>

      {/* Main JetAI Awwwards Card (Reference Image 2 media_1787323076388.png) */}
      <div className="awwwards-card w-full p-6 sm:p-10 flex flex-col gap-6 shadow-2xl relative overflow-hidden">
        
        {/* JetAI Header Title Matching Image 2 (media_1787323076388.png) */}
        <div className="space-y-0.5 text-left border-b border-slate-100 pb-4">
          <h2 className="text-3xl sm:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight font-['Google_Sans_Flex']">
            How can I help
          </h2>
          <h3 className="text-2xl sm:text-4xl font-medium text-slate-400 tracking-tight leading-tight font-['Google_Sans']">
            explore {selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : 'your data'}?
          </h3>
        </div>

        {/* Error Banner */}
        {error && (
          <div className="p-3.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-xs flex items-start gap-2.5">
            <AlertCircle className="size-4 text-amber-600 shrink-0 mt-0.5" />
            <div>
              <span className="font-semibold block">Notification Système / Mode Dégradé :</span>
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* Discrete SQL Inspector View Mode */}
        {showSQLInspector ? (
          <SQLFlipCard
            datasetId={selectedAgent?.datasetId}
            sqlQuery={`SELECT * FROM \`data-agents-by-industry.${selectedAgent?.datasetId || 'public_sector_employment_ds'}.business_kpi_summary\` WHERE 1=1 LIMIT 10;`}
            executionTime="1.24s"
          />
        ) : (
          /* Single Active Business Result Presentation Box (Clean Data Only) */
          <div className="min-h-[280px] max-h-[440px] overflow-y-auto space-y-4">
            
            {/* Case A: Initial State (Host Agent Greetings & Example Queries) */}
            {!lastUserMessage && !isStreaming && (
              <div className="h-full flex flex-col items-center justify-center text-center p-8 text-slate-700 my-auto animate-fade-in space-y-3">
                <div className="p-3 rounded-2xl bg-blue-50 border border-blue-200 text-[#0B57D0] shadow-sm">
                  <AgentIcon className="size-10" />
                </div>
                
                <h4 className="text-xl font-bold text-slate-900 font-['Google_Sans_Flex']">
                  {selectedAgent?.displayName || 'Agent Hôte Décisionnel'}
                </h4>
                
                <p className="text-sm text-slate-600 max-w-md leading-relaxed font-medium">
                  "Nous sommes connectés au jeu de données BigQuery pour <strong>{selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : selectedAgent?.id}</strong>. Sélectionnez une question suggérée ci-dessous."
                </p>

                <div className="pt-2 flex items-center gap-2 text-xs font-semibold text-[#0B57D0]">
                  <Sparkles className="size-4" />
                  <span>Exploration conversationnelle active</span>
                </div>
              </div>
            )}

            {/* Case B: BigQuery Execution Visualizer (During Loading) */}
            {isStreaming && (
              <BigQuerySchemaVisualizer
                datasetId={selectedAgent?.datasetId}
                agentName={selectedAgent?.displayName}
              />
            )}

            {/* Case C: Active Result Presentation (Clean Markdown Table, Images & Prose Only) */}
            {lastAssistantMessage && !isStreaming && (
              <div className="space-y-4 animate-fade-in">
                
                {/* Reasoning Accordion */}
                {lastAssistantMessage.thoughts && lastAssistantMessage.thoughts.length > 0 && (
                  <div className="w-full rounded-2xl bg-slate-50 border border-slate-200 text-xs overflow-hidden">
                    <button
                      type="button"
                      onClick={() => setShowThoughts(!showThoughts)}
                      className="w-full px-3.5 py-2.5 bg-slate-100 hover:bg-slate-200/80 flex items-center justify-between text-slate-700 font-medium transition-colors text-xs cursor-pointer"
                    >
                      <div className="flex items-center gap-2">
                        <Brain className="size-4 text-[#0B57D0]" />
                        <span>Raisonnement de l'agent ({lastAssistantMessage.thoughts.length} étapes)</span>
                      </div>
                      {showThoughts ? <ChevronUp className="size-4" /> : <ChevronDown className="size-4" />}
                    </button>

                    {showThoughts && (
                      <div className="p-3.5 font-mono text-[11px] text-slate-800 bg-white border-t border-slate-200 space-y-2">
                        {lastAssistantMessage.thoughts.map((t, tIdx) => (
                          <div key={tIdx} className="p-3 rounded-xl bg-white text-slate-800 border border-slate-200/90 shadow-2xs overflow-x-auto font-mono font-medium">
                            {t}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* Clean Result Presentation (Text, Markdown Tables & Images) */}
                <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-xs markdown-content">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {lastAssistantMessage.content}
                  </ReactMarkdown>
                </div>

              </div>
            )}

          </div>
        )}

        {/* JetAI Floating Input Bar Console */}
        <form onSubmit={handleFormSubmit} className="w-full flex items-center justify-between gap-3 pt-3 border-t border-slate-100">
          <div className="flex items-center gap-3 flex-1">
            
            {/* Mic Mute Toggle Button */}
            <button
              type="button"
              aria-label={voiceProps.isListening ? "Coupure Micro (Mute)" : "Activer Micro (Unmute)"}
              onClick={voiceProps.isListening ? voiceProps.stopListening : voiceProps.startListening}
              className={`p-2 rounded-full transition-all cursor-pointer ${
                voiceProps.isListening
                  ? 'bg-rose-500 text-white animate-pulse'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200 border border-slate-200'
              }`}
              title={voiceProps.isListening ? "Coupure Micro (Mute)" : "Activer Micro (Unmute)"}
            >
              {voiceProps.isListening ? <Mic className="size-4" /> : <MicOff className="size-4 text-slate-400" />}
            </button>

            <Search className="size-5 text-slate-400 shrink-0" />
            
            <input
              type="text"
              value={inputPrompt}
              onChange={handleInputChange}
              placeholder="Ask a question..."
              className="w-full bg-transparent border-none text-slate-900 placeholder-slate-400 focus:outline-none text-base font-medium font-['Google_Sans']"
            />
          </div>

          {/* Solid Google Blue Arrow Button */}
          <button
            type="submit"
            disabled={!inputPrompt.trim() || isStreaming}
            aria-label="Envoyer"
            className={`size-10 rounded-full flex items-center justify-center text-white shrink-0 transition-all transform hover:scale-105 active:scale-95 shadow-md cursor-pointer ${
              !inputPrompt.trim() || isStreaming
                ? 'bg-slate-200 text-slate-400 cursor-not-allowed border border-slate-300'
                : 'bg-[#0B57D0] hover:bg-blue-800 text-white shadow-blue-900/20'
            }`}
          >
            {isStreaming ? (
              <Loader2 className="size-4 animate-spin" />
            ) : (
              <ArrowRight className="size-4" />
            )}
          </button>
        </form>

        {/* Floating Scenario Pills Specific to Selected Agent */}
        <div className="flex items-center gap-2 flex-wrap pt-1">
          {selectedAgent?.exampleQueries?.slice(0, 4).map((q, idx) => (
            <button
              key={idx}
              disabled={isStreaming}
              onClick={() => onSendMessage(q)}
              className="awwwards-pill text-xs py-2 px-4 shadow-2xs cursor-pointer"
            >
              <span>💡 "{q}"</span>
            </button>
          ))}
        </div>

      </div>

      {/* Minimalist Bottom Scenario Extension Dock */}
      <BottomScenarioDock
        agents={agents}
        selectedAgent={selectedAgent}
        onSelectAgent={onSelectAgent}
        onResetChat={onResetChat}
      />

    </div>
  );
}
