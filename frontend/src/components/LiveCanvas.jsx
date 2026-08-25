import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { motion, AnimatePresence } from 'framer-motion';
import { GeminiOrb } from './GeminiOrb';
import { SQLFlipCard } from './SQLFlipCard';
import { BigQuerySchemaVisualizer } from './BigQuerySchemaVisualizer';
import { BottomScenarioDock } from './BottomScenarioDock';
import {
  Bot,
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
  Code2,
  CheckCircle2
} from 'lucide-react';
import { getIconComponent } from '../utils/themeMap';

export function LiveCanvas({
  selectedAgent,
  onReturnToBuilder,
  messages,
  isStreaming,
  thoughts,
  error,
  onSendMessage,
  voiceProps,
  onResetChat,
  screenMode = 'showcase'
}) {
  const [inputPrompt, setInputPrompt] = useState('');
  const [showThoughts, setShowThoughts] = useState(false);
  const [showSQLInspector, setShowSQLInspector] = useState(false);

  const AgentIcon = selectedAgent ? getIconComponent(selectedAgent.id) : Bot;
  const isSpeaking = voiceProps?.isSpeaking;

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
    <div className="w-full flex flex-col gap-6 animate-fade-in relative pb-8 px-4 max-w-6xl mx-auto font-['Google_Sans']">
      
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
                  • Connecté BigQuery
                </span>
              </h3>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Subtle Discrete SQL Inspector Toggle */}
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

      {/* Main 70% / 30% Purified Layout (Data Canvas + Host Companion) */}
      <div className="w-full grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* 70% LEFT / CENTER: Single Data Visual Bento Panel */}
        <div className="lg:col-span-8 flex flex-col gap-4">
          
          {/* Error Banner */}
          {error && (
            <div className="p-3.5 rounded-2xl bg-amber-50 border border-amber-200 text-amber-800 text-xs flex items-start gap-2.5">
              <AlertCircle className="size-4 text-amber-600 shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold block">Notification Système / Mode Dégradé :</span>
                <span>{error}</span>
              </div>
            </div>
          )}

          {/* 3D SQL Inspector Flip Mode */}
          {showSQLInspector ? (
            <motion.div
              initial={{ opacity: 0, rotateY: -90 }}
              animate={{ opacity: 1, rotateY: 0 }}
              exit={{ opacity: 0, rotateY: 90 }}
              transition={{ type: "spring", stiffness: 300, damping: 25 }}
            >
              <SQLFlipCard
                datasetId={selectedAgent?.datasetId}
                sqlQuery={`SELECT sector_name, kpi_value, variance_percentage\nFROM \`data-agents-by-industry.${selectedAgent?.datasetId || 'skywatch_aerospace_ds'}.business_kpi_summary\`\nWHERE status = 'ACTIVE'\nORDER BY variance_percentage DESC\nLIMIT 10;`}
                executionTime="1.18s"
              />
            </motion.div>
          ) : (
            /* Main Frosted Glass Bento Card */
            <div className="awwwards-card p-6 sm:p-8 min-h-[440px] flex flex-col justify-between shadow-2xl relative overflow-hidden transition-all">
              
              <div className="space-y-4">
                
                {/* Case A: Initial State (Host Agent Greetings) */}
                {!lastUserMessage && !isStreaming && (
                  <div className="h-full flex flex-col items-center justify-center text-center p-8 text-slate-700 my-auto animate-fade-in space-y-4">
                    <div className="p-4 rounded-3xl bg-blue-50 border border-blue-200 text-[#0B57D0] shadow-sm">
                      <AgentIcon className="size-12" />
                    </div>
                    
                    <h4 className="text-2xl font-extrabold text-slate-900 font-['Google_Sans_Flex']">
                      {selectedAgent?.displayName || 'Agent Hôte Décisionnel'}
                    </h4>
                    
                    <p className="text-sm text-slate-600 max-w-md leading-relaxed font-medium">
                      "Nous sommes connectés au jeu de données BigQuery pour <strong>{selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : selectedAgent?.id}</strong>. Sélectionnez une suggestion ci-dessous ou posez votre question."
                    </p>

                    <div className="pt-2 flex items-center gap-2 text-xs font-bold text-[#0B57D0] bg-blue-50 px-4 py-1.5 rounded-full border border-blue-200">
                      <Sparkles className="size-4" />
                      <span>Exploration conversationnelle interactive active</span>
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

                {/* Case C: Active Business Result Presentation (Clean Markdown Table & Insights) */}
                {lastAssistantMessage && !isStreaming && (
                  <motion.div
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ type: "spring", stiffness: 350, damping: 25 }}
                    className="space-y-4"
                  >
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
                              <div key={tIdx} className="p-2.5 rounded-lg bg-slate-900 text-cyan-300 border border-slate-800 overflow-x-auto">
                                {t}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Purified Markdown Business Presentation */}
                    <div className="p-6 rounded-3xl bg-white border border-slate-200/90 shadow-xs markdown-content">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {lastAssistantMessage.content}
                      </ReactMarkdown>
                    </div>
                  </motion.div>
                )}

              </div>

              {/* Bottom Card Metadata */}
              <div className="pt-4 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500 font-medium">
                <span className="flex items-center gap-1.5 text-emerald-600 font-semibold">
                  <CheckCircle2 className="size-3.5" />
                  <span>Données vérifiées BigQuery Engine</span>
                </span>
                <span>Vertex AI Data Agents</span>
              </div>

            </div>
          )}

        </div>

        {/* 30% RIGHT: Host Companion & Slime Live Orb Floating Box */}
        <div className="lg:col-span-4 flex flex-col items-center gap-5">
          
          {/* Host Companion Card */}
          <div className="awwwards-card w-full p-6 flex flex-col items-center justify-center text-center space-y-4 shadow-xl">
            
            <h4 className="text-xs font-extrabold tracking-wider text-slate-400 uppercase font-['Google_Sans_Flex']">
              L'Agent Compagnon Hôte
            </h4>

            {/* Slime 3D Floating Gemini Orb */}
            <GeminiOrb
              isListening={voiceProps.isListening}
              isSpeaking={isSpeaking}
              isStreaming={isStreaming}
              onClickMic={voiceProps.isListening ? voiceProps.stopListening : voiceProps.startListening}
              speechSupported={voiceProps?.speechSupported}
              showcaseMode={isShowcase}
            />

            {/* Storytelling Narrator Speech Bubble */}
            <div className="p-4 rounded-2xl bg-blue-50/80 border border-blue-200 text-slate-700 text-xs sm:text-sm font-medium leading-relaxed italic relative">
              <div className="absolute -top-2 left-1/2 -translate-x-1/2 size-3 bg-blue-50 border-t border-l border-blue-200 rotate-45" />
              {isSpeaking
                ? '"J\'analyse votre demande et je synthétise le rapport d\'affaires..."'
                : isStreaming
                ? '"Connexion aux tables BigQuery... Synthèse immédiate des métriques clés."'
                : lastUserMessage
                ? `"${lastUserMessage.content}"`
                : '"Bonjour ! Je suis votre Agent Hôte. Posez-moi une question ou sélectionnez un scénario ci-dessous."'}
            </div>

          </div>

          {/* Spacious Suggestion Pills (Gemini Enterprise Style) */}
          <div className="w-full flex flex-col gap-2.5">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-1">
              Suggestions Spacieuses
            </span>

            {selectedAgent?.exampleQueries?.slice(0, 3).map((q, idx) => (
              <button
                key={idx}
                disabled={isStreaming}
                onClick={() => onSendMessage(q)}
                className="w-full text-left p-3.5 rounded-2xl bg-white hover:bg-blue-50 border border-slate-200 hover:border-blue-300 text-xs font-semibold text-slate-800 shadow-2xs transition-all transform hover:-translate-y-0.5 flex items-center justify-between gap-2 cursor-pointer"
              >
                <span>💡 "{q}"</span>
                <ArrowRight className="size-3.5 text-[#0B57D0] shrink-0" />
              </button>
            ))}
          </div>

        </div>

      </div>

      {/* Floating JetAI Input Bar Console */}
      <form onSubmit={handleFormSubmit} className="p-3 rounded-full bg-white border border-slate-200/90 shadow-xl backdrop-blur-xl max-w-3xl mx-auto w-full">
        <div className="flex items-center gap-3">
          
          {/* Mic Mute Toggle Button */}
          <button
            type="button"
            aria-label={voiceProps.isListening ? "Coupure Micro (Mute)" : "Activer Micro (Unmute)"}
            onClick={voiceProps.isListening ? voiceProps.stopListening : voiceProps.startListening}
            className={`p-2.5 rounded-full transition-all ${
              voiceProps.isListening
                ? 'bg-rose-500 text-white animate-pulse'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200 border border-slate-200 shadow-2xs'
            }`}
            title={voiceProps.isListening ? "Coupure Micro (Mute)" : "Activer Micro (Unmute)"}
          >
            {voiceProps.isListening ? <Mic className="size-4.5" /> : <MicOff className="size-4.5 text-slate-400" />}
          </button>

          <Search className="size-5 text-slate-400 shrink-0" />

          <textarea
            rows={1}
            value={inputPrompt}
            onChange={handleInputChange}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleFormSubmit(e);
              }
            }}
            placeholder="Posez une question ou sélectionnez une puce..."
            className="w-full px-2 py-1 text-xs sm:text-sm text-slate-900 placeholder-slate-400 focus:outline-none bg-transparent resize-none font-medium font-['Google_Sans']"
          />

          <button
            type="submit"
            disabled={!inputPrompt.trim() || isStreaming}
            aria-label="Envoyer"
            className={`px-5 py-2.5 rounded-full font-bold text-xs sm:text-sm flex items-center justify-center gap-2 transition-all cursor-pointer ${
              !inputPrompt.trim() || isStreaming
                ? 'bg-slate-200 text-slate-400 cursor-not-allowed border border-slate-300'
                : 'bg-[#0B57D0] hover:bg-blue-800 text-white shadow-md'
            }`}
          >
            {isStreaming ? (
              <Loader2 className="size-4 animate-spin" />
            ) : (
              <>
                <span>Envoyer</span>
                <Send className="size-4" />
              </>
            )}
          </button>
        </div>
      </form>

      {/* Minimalist Bottom Scenario Extension Dock */}
      <BottomScenarioDock
        agents={[]}
        selectedAgent={selectedAgent}
        onSelectAgent={onReturnToBuilder ? () => {} : null}
        onSendMessage={onSendMessage}
      />

    </div>
  );
}
