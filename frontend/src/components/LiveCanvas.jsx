import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { GeminiOrb } from './GeminiOrb';
import { SQLFlipCard } from './SQLFlipCard';
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
  const [showThoughtsMap, setShowThoughtsMap] = useState({});

  const AgentIcon = selectedAgent ? getIconComponent(selectedAgent.id) : Bot;

  const handleInputChange = (e) => {
    setInputPrompt(e.target.value);
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (!inputPrompt.trim() || isStreaming) return;
    onSendMessage(inputPrompt);
    setInputPrompt('');
  };

  const toggleThought = (idx) => {
    setShowThoughtsMap(prev => ({ ...prev, [idx]: !prev[idx] }));
  };

  const isShowcase = screenMode === 'showcase';

  return (
    <div className="w-full flex flex-col gap-4 animate-fade-in relative pb-24 px-4 max-w-7xl mx-auto">
      
      {/* Top Navigation Bar */}
      <div className="px-5 py-3 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-xl flex items-center justify-between gap-4 shadow-md">
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={onReturnToBuilder}
            className="px-3.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 transition-all flex items-center gap-1.5 text-xs font-semibold"
          >
            <ChevronLeft className="size-4" />
            <span>Changer d'Espace</span>
          </button>

          <div className="h-4 w-px bg-slate-800 hidden sm:block" />

          <div className="flex items-center gap-2.5">
            <div className="p-1.5 rounded-xl bg-sky-500/20 border border-sky-400/30 text-sky-400">
              <AgentIcon className="size-4" />
            </div>
            <div>
              <h3 className="text-xs sm:text-sm font-bold text-white flex items-center gap-2 font-['Google_Sans_Flex']">
                {selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : selectedAgent?.id}
                <span className="text-[11px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-medium">
                  • Connecté BigQuery
                </span>
              </h3>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-sky-500/15 border border-sky-400/30 text-sky-300 text-xs font-semibold">
            <span className="size-2 rounded-full bg-sky-400 animate-pulse" />
            <span>{isShowcase ? 'ÉCRAN A : SHOWCASE PUBLIC' : 'ÉCRAN B : CONTRÔLEUR TACTILE'}</span>
          </div>

          <button
            type="button"
            onClick={onResetChat}
            aria-label="Effacer la conversation"
            title="Effacer la conversation"
            className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs"
          >
            <RotateCcw className="size-4" />
          </button>
        </div>
      </div>

      {/* Main Page 2 Bento Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        
        {/* Left Column: Gemini Living Orb + Backup Suggestions (4 cols) */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          
          {/* Gemini Living Physics Wave Orb */}
          <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-lg backdrop-blur-xl flex flex-col items-center justify-center text-center">
            <div className="mb-2">
              <span className="text-xs font-medium text-slate-400 block">
                Copilote Conversational Analytics
              </span>
              <h4 className="text-sm font-bold text-white font-['Google_Sans_Flex']">
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

            <div className="mt-3 flex items-center gap-1.5 text-[11px] text-sky-300 bg-sky-500/15 px-3 py-1 rounded-full border border-sky-400/30 font-medium">
              <Volume2 className="size-3.5" />
              <span>Synthèse Vocale Purifiée Active</span>
            </div>
          </div>

          {/* Backup Clickable Suggestions (Console de Saisie Hybride) */}
          <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-md flex flex-col gap-3">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-1.5 font-['Google_Sans_Flex']">
                <Sparkles className="size-4 text-sky-400" />
                Suggestions Tactiles de Secours
              </h4>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700 font-semibold">
                {selectedAgent?.exampleQueries?.length || 0}
              </span>
            </div>

            <div className="flex flex-col gap-2">
              {selectedAgent?.exampleQueries?.map((q, idx) => (
                <button
                  key={idx}
                  disabled={isStreaming}
                  onClick={() => onSendMessage(q)}
                  className={`p-3 rounded-xl border text-xs text-left transition-all flex items-start justify-between gap-3 ${
                    isStreaming
                      ? 'opacity-50 cursor-not-allowed bg-slate-900/50 border-slate-800 text-slate-600'
                      : 'bg-slate-800/80 hover:bg-slate-800 border-slate-700/80 hover:border-sky-400/60 text-slate-200 hover:text-white shadow-xs transform hover:-translate-y-0.5'
                  }`}
                >
                  <span className="line-clamp-2 leading-relaxed font-medium">{q}</span>
                  <ArrowRight className="size-4 shrink-0 text-sky-400 mt-0.5" />
                </button>
              ))}
            </div>
          </div>

        </div>

        {/* Right Column: Data Canvas Showcase (8 cols / 70% space priority) */}
        <div className="lg:col-span-8 flex flex-col gap-4">
          
          {/* Error Banner */}
          {error && (
            <div className="p-3.5 rounded-xl bg-rose-500/20 border border-rose-500/40 text-rose-300 text-xs flex items-start gap-2.5">
              <AlertCircle className="size-4 text-rose-400 shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold block">Notification Système / Mode Dégradé :</span>
                <span>{error}</span>
              </div>
            </div>
          )}

          {/* Data Canvas Showcase Box */}
          <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 min-h-[460px] max-h-[600px] overflow-y-auto space-y-4 shadow-xl backdrop-blur-xl">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-8 text-slate-500 my-auto">
                <Bot className="size-10 text-sky-400 mb-2 animate-bounce" />
                <h4 className="text-sm font-bold text-white font-['Google_Sans_Flex']">
                  Canvas de Données Prêt pour {selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : selectedAgent?.id}
                </h4>
                <p className="text-xs text-slate-400 max-w-sm mt-1">
                  Posez votre question à l'oral ou cliquez sur une suggestion pour afficher les métriques clés et la carte pivotante SQL 3D.
                </p>
              </div>
            ) : (
              messages.map((msg, idx) => {
                const isUser = msg.role === 'user';

                return (
                  <div key={idx} className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} space-y-2`}>
                    
                    {/* Header */}
                    <div className="flex items-center gap-1.5 text-[11px] text-slate-400 px-1">
                      {isUser ? (
                        <>
                          <span className="text-slate-300 font-medium">Vous</span>
                          <div className="p-1 rounded-lg bg-slate-800 text-slate-300 border border-slate-700">
                            <User className="size-3" />
                          </div>
                        </>
                      ) : (
                        <>
                          <div className="p-1 rounded-lg bg-sky-500/20 text-sky-400 border border-sky-400/30">
                            <AgentIcon className="size-3" />
                          </div>
                          <span className="font-semibold text-white font-['Google_Sans_Flex']">
                            {selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : selectedAgent?.id}
                          </span>
                        </>
                      )}
                    </div>

                    {/* Reasoning Accordion */}
                    {!isUser && msg.thoughts && msg.thoughts.length > 0 && (
                      <div className="w-full max-w-3xl rounded-2xl bg-slate-950/80 border border-slate-800 text-xs overflow-hidden">
                        <button
                          type="button"
                          onClick={() => toggleThought(idx)}
                          className="w-full px-3.5 py-2.5 bg-slate-900 hover:bg-slate-800 flex items-center justify-between text-slate-300 font-medium transition-colors text-xs"
                        >
                          <div className="flex items-center gap-2">
                            <Brain className="size-4 text-sky-400" />
                            <span>Raisonnement de l'agent ({msg.thoughts.length} étapes)</span>
                          </div>
                          {showThoughtsMap[idx] ? <ChevronUp className="size-4" /> : <ChevronDown className="size-4" />}
                        </button>

                        {showThoughtsMap[idx] && (
                          <div className="p-3.5 font-mono text-[11px] text-cyan-300 bg-slate-950 border-t border-slate-800 space-y-2">
                            {msg.thoughts.map((t, tIdx) => (
                              <div key={tIdx} className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 overflow-x-auto">
                                {t}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}

                    {/* 3D SQL Inspector Flip Card */}
                    {!isUser && (
                      <SQLFlipCard
                        datasetId={selectedAgent?.datasetId}
                        sqlQuery={`SELECT * FROM \`${selectedAgent?.datasetId || 'public_sector_employment_ds'}\` WHERE 1=1 LIMIT 10;`}
                        executionTime="1.24s"
                      />
                    )}

                    {/* Message Bubble */}
                    <div
                      className={`max-w-3xl rounded-2xl px-5 py-4 leading-relaxed shadow-md ${
                        isUser
                          ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-tr-none text-xs sm:text-sm font-medium'
                          : 'bg-slate-900/90 border border-slate-800 text-slate-200 rounded-tl-none markdown-content'
                      }`}
                    >
                      {isUser ? (
                        <p className="whitespace-pre-wrap">{msg.content}</p>
                      ) : (
                        <div>
                          {msg.isStreaming && !msg.content ? (
                            <div className="flex items-center gap-2 text-sky-400 font-mono text-xs py-1">
                              <Loader2 className="size-4 animate-spin text-sky-400" />
                              <span>Interrogation BigQuery & Génération du rapport...</span>
                            </div>
                          ) : (
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                              {msg.content}
                            </ReactMarkdown>
                          )}
                        </div>
                      )}
                    </div>

                  </div>
                );
              })
            )}
          </div>

          {/* Bottom Floating Console Pill */}
          <form onSubmit={handleFormSubmit} className="p-3 rounded-full bg-slate-900/90 border border-slate-800 shadow-xl backdrop-blur-xl">
            <div className="flex items-center gap-3">
              <button
                type="button"
                aria-label="Microphone Push-to-Talk"
                onClick={voiceProps.isListening ? voiceProps.stopListening : voiceProps.startListening}
                className={`p-2.5 rounded-full transition-all ${
                  voiceProps.isListening
                    ? 'bg-rose-500 text-white animate-pulse'
                    : 'bg-slate-800 text-sky-400 hover:bg-slate-700 border border-slate-700 shadow-xs'
                }`}
                title="Microphone Push-to-Talk"
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
                className="w-full px-2 py-1 text-xs sm:text-sm text-white placeholder-slate-400 focus:outline-none bg-transparent resize-none font-medium font-['Google_Sans']"
              />

              <button
                type="submit"
                disabled={!inputPrompt.trim() || isStreaming}
                aria-label="Envoyer"
                className={`px-5 py-2.5 rounded-full font-bold text-xs sm:text-sm flex items-center justify-center gap-2 transition-all ${
                  !inputPrompt.trim() || isStreaming
                    ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
                    : 'bg-gradient-to-r from-sky-400 via-blue-600 to-indigo-600 hover:opacity-90 text-white shadow-md'
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
