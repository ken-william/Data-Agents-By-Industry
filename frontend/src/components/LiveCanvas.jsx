import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { GeminiOrb } from './GeminiOrb';
import { SQLFlipCard } from './SQLFlipCard';
import { BigQuerySchemaVisualizer } from './BigQuerySchemaVisualizer';
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
  Volume2
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

  const AgentIcon = selectedAgent ? getIconComponent(selectedAgent.id) : Bot;

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
    <div className="w-full flex flex-col gap-4 animate-fade-in relative pb-24 px-4 max-w-7xl mx-auto">
      
      {/* Top Navigation Bar */}
      <div className="px-5 py-3 rounded-2xl bg-white/90 border border-slate-200/90 backdrop-blur-xl flex items-center justify-between gap-4 shadow-sm">
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={onReturnToBuilder}
            className="px-3.5 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition-all flex items-center gap-1.5 text-xs font-semibold"
          >
            <ChevronLeft className="size-4" />
            <span>Changer d'Espace</span>
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
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-50 border border-blue-200 text-[#0B57D0] text-xs font-semibold">
            <span className="size-2 rounded-full bg-[#0B57D0] animate-pulse" />
            <span>{isShowcase ? 'ÉCRAN A : CANVA UNIQUE' : 'ÉCRAN B : CONTRÔLEUR TACTILE'}</span>
          </div>

          <button
            type="button"
            onClick={onResetChat}
            aria-label="Recommencer"
            title="Effacer et recommencer"
            className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 border border-slate-200 text-xs"
          >
            <RotateCcw className="size-4" />
          </button>
        </div>
      </div>

      {/* Main Page 2 Bento Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        
        {/* Left Column: Gemini Living Orb + Floating Scenario Chips (4 cols) */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          
          {/* Gemini Living Physics Wave Orb */}
          <div className="p-6 rounded-2xl bg-white/95 border border-slate-200/90 shadow-sm backdrop-blur-xl flex flex-col items-center justify-center text-center">
            <div className="mb-2">
              <span className="text-xs font-medium text-slate-500 block">
                Copilote Conversational Analytics
              </span>
              <h4 className="text-sm font-bold text-slate-900 font-['Google_Sans_Flex']">
                {selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : selectedAgent?.id}
              </h4>
            </div>

            <GeminiOrb
              isListening={voiceProps.isListening}
              isSpeaking={voiceProps.isSpeaking}
              isStreaming={isStreaming}
              onClickMic={voiceProps.isListening ? voiceProps.stopListening : voiceProps.startListening}
              speechSupported={voiceProps.speechSupported}
              showcaseMode={isShowcase}
            />

            <div className="mt-3 flex items-center gap-1.5 text-[11px] text-[#0B57D0] bg-blue-50 px-3 py-1 rounded-full border border-blue-200 font-medium">
              <Volume2 className="size-3.5" />
              <span>Speech-Sanitized Vocal Output Active</span>
            </div>
          </div>

          {/* Backup Clickable Suggestions (Spacious Floating Chips) */}
          <div className="p-4 rounded-2xl bg-white/95 border border-slate-200/90 shadow-sm flex flex-col gap-3">
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-800 flex items-center gap-1.5 font-['Google_Sans_Flex']">
                <Sparkles className="size-4 text-[#0B57D0]" />
                Floating Scenario Chips
              </h4>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200 font-semibold">
                {selectedAgent?.exampleQueries?.length || 0}
              </span>
            </div>

            <div className="flex flex-col gap-2.5">
              {selectedAgent?.exampleQueries?.map((q, idx) => (
                <button
                  key={idx}
                  disabled={isStreaming}
                  onClick={() => onSendMessage(q)}
                  className={`p-3 rounded-xl border text-xs text-left transition-all flex items-start justify-between gap-3 ${
                    isStreaming
                      ? 'opacity-50 cursor-not-allowed bg-slate-50 border-slate-200 text-slate-400'
                      : 'bg-white hover:bg-blue-50/80 border-slate-200 hover:border-blue-300 text-slate-800 hover:text-blue-900 shadow-xs transform hover:-translate-y-0.5'
                  }`}
                >
                  <span className="line-clamp-2 leading-relaxed font-semibold">{q}</span>
                  <ArrowRight className="size-4 shrink-0 text-[#0B57D0] mt-0.5" />
                </button>
              ))}
            </div>
          </div>

        </div>

        {/* Right Column: ZERO-CHAT SCROLL CANVAS (8 cols / 70% space priority) */}
        <div className="lg:col-span-8 flex flex-col gap-4">
          
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

          {/* Zero-Chat Scroll Active State Canvas Box */}
          <div className="p-6 rounded-2xl bg-white/95 border border-slate-200/90 min-h-[460px] max-h-[600px] overflow-y-auto space-y-4 shadow-sm backdrop-blur-xl transition-all duration-500">
            
            {/* Case A: Initial State (Host Agent Introduction) */}
            {!lastUserMessage && !isStreaming && (
              <div className="h-full flex flex-col items-center justify-center text-center p-8 text-slate-700 my-auto animate-fade-in space-y-4">
                <div className="p-3 rounded-2xl bg-blue-50 border border-blue-200 text-[#0B57D0] shadow-sm">
                  <AgentIcon className="size-10" />
                </div>
                
                <h4 className="text-xl font-bold text-slate-900 font-['Google_Sans_Flex']">
                  {selectedAgent?.displayName || 'Agent Hôte Decisionnel'}
                </h4>
                
                <p className="text-sm text-slate-600 max-w-md leading-relaxed">
                  "Bonjour ! Je suis votre copilote analytique. Nous sommes connectés aux tables BigQuery de <strong>{selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : selectedAgent?.id}</strong>. Posez-moi une question à l'oral ou sélectionnez un scénario."
                </p>

                <div className="pt-2 flex items-center gap-2 text-xs font-semibold text-[#0B57D0]">
                  <Sparkles className="size-4" />
                  <span>Prêt pour l'exploration conversationnelle</span>
                </div>
              </div>
            )}

            {/* Case B: User Question Header */}
            {lastUserMessage && (
              <div className="p-4 rounded-xl bg-blue-50/80 border border-blue-200/80 text-slate-900 flex items-center gap-3 animate-fade-in shadow-2xs">
                <div className="p-2 rounded-lg bg-[#0B57D0] text-white font-bold text-xs">
                  <User className="size-4" />
                </div>
                <div className="flex-1">
                  <span className="text-[11px] font-bold text-[#0B57D0] uppercase tracking-wider block">
                    Question Active
                  </span>
                  <p className="text-sm font-semibold text-slate-900">{lastUserMessage.content}</p>
                </div>
              </div>
            )}

            {/* Case C: BigQuery Execution & Storytelling Visualizer (During Loading) */}
            {isStreaming && (
              <BigQuerySchemaVisualizer
                datasetId={selectedAgent?.datasetId}
                agentName={selectedAgent?.displayName}
              />
            )}

            {/* Case D: Active Result Presentation (Single Active State) */}
            {lastAssistantMessage && !isStreaming && (
              <div className="space-y-4 animate-fade-in">
                
                {/* Agent Reasoning Accordion */}
                {lastAssistantMessage.thoughts && lastAssistantMessage.thoughts.length > 0 && (
                  <div className="w-full rounded-xl bg-slate-50 border border-slate-200 text-xs overflow-hidden">
                    <button
                      type="button"
                      onClick={() => setShowThoughts(!showThoughts)}
                      className="w-full px-3.5 py-2.5 bg-slate-100 hover:bg-slate-200/80 flex items-center justify-between text-slate-700 font-medium transition-colors text-xs"
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

                {/* 3D SQL Inspector Flip Card */}
                <SQLFlipCard
                  datasetId={selectedAgent?.datasetId}
                  sqlQuery={`SELECT * FROM \`${selectedAgent?.datasetId || 'public_sector_employment_ds'}\` WHERE 1=1 LIMIT 10;`}
                  executionTime="1.24s"
                />

                {/* Active Result Report Presentation */}
                <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm markdown-content">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {lastAssistantMessage.content}
                  </ReactMarkdown>
                </div>

              </div>
            )}

          </div>

          {/* Bottom Floating Console Pill (#F0F4F9) */}
          <form onSubmit={handleFormSubmit} className="p-3 rounded-full bg-[#F0F4F9] border border-slate-200/80 shadow-md backdrop-blur-xl">
            <div className="flex items-center gap-3">
              <button
                type="button"
                aria-label="Microphone Gemini Live"
                onClick={voiceProps.isListening ? voiceProps.stopListening : voiceProps.startListening}
                className={`p-2.5 rounded-full transition-all ${
                  voiceProps.isListening
                    ? 'bg-rose-500 text-white animate-pulse'
                    : 'bg-white text-[#0B57D0] hover:bg-blue-50 border border-slate-200 shadow-xs'
                }`}
                title="Microphone Gemini Live"
              >
                <Mic className="size-4.5" />
              </button>

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
                placeholder="Entrez votre message ici..."
                className="w-full px-2 py-1 text-xs sm:text-sm text-slate-900 placeholder-slate-500 focus:outline-none bg-transparent resize-none font-medium font-['Google_Sans']"
              />

              <button
                type="submit"
                disabled={!inputPrompt.trim() || isStreaming}
                aria-label="Envoyer"
                className={`px-5 py-2.5 rounded-full font-bold text-xs sm:text-sm flex items-center justify-center gap-2 transition-all ${
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

        </div>

      </div>

    </div>
  );
}
