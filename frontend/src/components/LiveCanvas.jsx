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
  Zap,
  ChevronLeft,
  Sparkles,
  Monitor,
  Smartphone
} from 'lucide-react';
import { COLOR_THEMES, getIconComponent } from '../utils/themeMap';

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
  screenMode = 'showcase' // 'showcase' (Écran A) vs 'controller' (Écran B)
}) {
  const [inputPrompt, setInputPrompt] = useState('');
  const [showThoughtsMap, setShowThoughtsMap] = useState({});

  const colorKey = selectedAgent?.theme?.color || 'indigo';
  const theme = COLOR_THEMES[colorKey] || COLOR_THEMES.indigo;
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
    <div className="w-full flex flex-col gap-4 animate-fade-in">
      
      {/* Top Navigation & Status Bar */}
      <div className="px-4 py-3 rounded-2xl bg-[#0B132B]/70 border border-slate-800/80 backdrop-blur-md flex items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <button
            onClick={onReturnToBuilder}
            className="px-3 py-1.5 rounded-lg bg-[#020617] hover:bg-slate-900 border border-slate-800 text-slate-300 hover:text-white transition-all flex items-center gap-1.5 text-xs font-semibold"
          >
            <ChevronLeft className="w-4 h-4" />
            <span>Catalogue Agents</span>
          </button>

          <div className="h-4 w-px bg-slate-800 hidden sm:block" />

          <div className="flex items-center gap-2">
            <div className={`p-1.5 rounded-lg bg-[#020617] border border-slate-800 ${theme.text}`}>
              <AgentIcon className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-xs sm:text-sm font-bold text-slate-50 flex items-center gap-2">
                {selectedAgent?.displayName.split(' - ')[0]}
                <span className={`text-[10px] px-2 py-0.5 rounded-lg font-mono ${theme.badge}`}>
                  {selectedAgent?.datasetId}
                </span>
              </h3>
            </div>
          </div>
        </div>

        {/* Status Badge & Reset Button */}
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>{isShowcase ? 'ÉCRAN A : SHOWCASE' : 'ÉCRAN B : CONTRÔLEUR'}</span>
          </div>

          <button
            onClick={onResetChat}
            title="Effacer la conversation"
            className="p-1.5 rounded-lg bg-[#020617] hover:bg-slate-900 text-slate-400 hover:text-white border border-slate-800 text-xs"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Main Dual Screen Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        
        {/* Left Column: Challenge Chips & Voice Controller (3 cols in Controller mode, top in Showcase mode) */}
        <div className={`${isShowcase ? 'lg:col-span-4' : 'lg:col-span-4'} flex flex-col gap-4`}>
          
          {/* Gemini Live SVG Animated Orb Card */}
          <div className="p-6 rounded-2xl bg-[#0B132B]/70 border border-slate-800/80 backdrop-blur-md shadow-xl flex flex-col items-center justify-center text-center">
            
            <div className="mb-2">
              <span className="text-xs font-semibold text-slate-400 block">
                Copilote Conversational Analytics
              </span>
              <h4 className="text-sm font-bold text-slate-100">
                {selectedAgent?.displayName.split(' - ')[0]}
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

          </div>

          {/* Smart Challenge Chips (Défis Métiers) */}
          <div className="p-4 rounded-2xl bg-[#0B132B]/70 border border-slate-800/80 backdrop-blur-md flex flex-col gap-3 shadow-xl">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
                <Zap className="w-4 h-4 text-sky-400" />
                Défis Métiers Proposés
              </h4>
              <span className="text-[10px] px-2 py-0.5 rounded bg-[#020617] text-slate-400 font-mono">
                {selectedAgent?.exampleQueries?.length || 0} Questions
              </span>
            </div>

            <div className="flex flex-col gap-2">
              {selectedAgent?.exampleQueries?.map((q, idx) => (
                <button
                  key={idx}
                  disabled={isStreaming}
                  onClick={() => onSendMessage(q)}
                  className={`p-3 rounded-xl border text-xs text-left transition-all flex items-start justify-between gap-2.5 ${
                    isStreaming
                      ? 'opacity-50 cursor-not-allowed bg-[#020617] border-slate-800 text-slate-600'
                      : 'bg-[#020617] border-slate-800/80 hover:border-sky-500/40 text-slate-200 hover:text-white'
                  }`}
                >
                  <span className="line-clamp-2 leading-relaxed">{q}</span>
                  <ArrowRight className="w-4 h-4 shrink-0 text-sky-400 mt-0.5" />
                </button>
              ))}
            </div>
          </div>

        </div>

        {/* Right Column: 70% Result Canvas Priority & Hybrid Input Dock (8 cols) */}
        <div className="lg:col-span-8 flex flex-col gap-4">
          
          {/* Error Notification */}
          {error && (
            <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-300 text-xs flex items-start gap-2.5">
              <AlertCircle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold block">Notification Système / Restitution en Mode Dégradé :</span>
                <span>{error}</span>
              </div>
            </div>
          )}

          {/* Dynamic Result Canvas (70% priority, clear readable typography) */}
          <div className="p-6 rounded-2xl bg-[#0B132B]/70 border border-slate-800/80 backdrop-blur-md min-h-[440px] max-h-[580px] overflow-y-auto space-y-4 shadow-xl">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-8 text-slate-500 my-auto">
                <Bot className="w-10 h-10 text-slate-600 mb-2 animate-bounce" />
                <h4 className="text-sm font-bold text-slate-300">Session démarrée avec l'agent {selectedAgent?.displayName.split(' - ')[0]}</h4>
                <p className="text-xs text-slate-400 max-w-sm mt-1">
                  Posez votre question à l'oral ou sélectionnez un défi à gauche pour déclencher l'analyse décisionnelle BigQuery.
                </p>
              </div>
            ) : (
              messages.map((msg, idx) => {
                const isUser = msg.role === 'user';

                return (
                  <div key={idx} className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} space-y-2`}>
                    
                    {/* Message Header */}
                    <div className="flex items-center gap-1.5 text-[11px] text-slate-400 px-1">
                      {isUser ? (
                        <>
                          <span>Vous</span>
                          <div className="p-1 rounded bg-[#020617] text-slate-300 border border-slate-800">
                            <User className="w-3 h-3" />
                          </div>
                        </>
                      ) : (
                        <>
                          <div className={`p-1 rounded bg-[#020617] border border-slate-800 ${theme.text}`}>
                            <AgentIcon className="w-3 h-3" />
                          </div>
                          <span className="font-semibold text-slate-200">{selectedAgent?.displayName.split(' - ')[0]}</span>
                        </>
                      )}
                    </div>

                    {/* Reasoning Accordion */}
                    {!isUser && msg.thoughts && msg.thoughts.length > 0 && (
                      <div className="w-full max-w-3xl rounded-xl bg-[#020617] border border-slate-800 text-xs overflow-hidden">
                        <button
                          type="button"
                          onClick={() => toggleThought(idx)}
                          className="w-full px-3.5 py-2.5 bg-[#0B132B]/80 hover:bg-[#0B132B] flex items-center justify-between text-slate-300 font-medium transition-colors text-xs"
                        >
                          <div className="flex items-center gap-2">
                            <Brain className="w-4 h-4 text-sky-400" />
                            <span>Raisonnement & Requête SQL générée ({msg.thoughts.length} étapes)</span>
                          </div>
                          {showThoughtsMap[idx] ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                        </button>

                        {showThoughtsMap[idx] && (
                          <div className="p-3.5 font-mono text-[11px] text-slate-300 bg-[#020617] border-t border-slate-800 space-y-2">
                            {msg.thoughts.map((t, tIdx) => (
                              <div key={tIdx} className="p-2.5 rounded-lg bg-[#0B132B]/60 border border-slate-800">
                                {t}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Message Bubble */}
                    <div
                      className={`max-w-3xl rounded-2xl px-5 py-4 leading-relaxed shadow-lg ${
                        isUser
                          ? 'bg-gradient-to-r from-sky-500 to-indigo-600 text-white rounded-tr-none text-xs sm:text-sm'
                          : 'bg-[#020617] border border-slate-800 text-slate-100 rounded-tl-none markdown-content'
                      }`}
                    >
                      {isUser ? (
                        <p className="whitespace-pre-wrap">{msg.content}</p>
                      ) : (
                        <div>
                          {msg.isStreaming && !msg.content ? (
                            <div className="flex items-center gap-2 text-sky-300 font-mono text-xs py-1">
                              <Loader2 className="w-4 h-4 animate-spin text-sky-400" />
                              <span>Interrogation BigQuery & Génération de l'analyse...</span>
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

          {/* Hybrid Dock: Voice STT + Multiline Text Input */}
          <form onSubmit={handleFormSubmit} className="p-3.5 rounded-2xl bg-[#0B132B]/70 border border-slate-800/80 backdrop-blur-md shadow-xl">
            <div className="flex items-center gap-2.5">
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
                placeholder="Posez votre question métiers (Entrée pour envoyer)..."
                className="w-full px-4 py-3 rounded-xl bg-[#020617] border border-slate-800 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500 resize-none"
              />

              <button
                type="submit"
                disabled={!inputPrompt.trim() || isStreaming}
                className={`h-full px-5 py-3 rounded-xl font-semibold text-xs sm:text-sm flex items-center justify-center gap-2 transition-all ${
                  !inputPrompt.trim() || isStreaming
                    ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
                    : 'bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 hover:opacity-90 text-white shadow-lg'
                }`}
              >
                {isStreaming ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <>
                    <span>Envoyer</span>
                    <Send className="w-4 h-4" />
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
