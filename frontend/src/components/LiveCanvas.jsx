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
  ChevronLeft
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
  onResetChat
}) {
  const [inputPrompt, setInputPrompt] = useState('');
  const [showThoughtsMap, setShowThoughtsMap] = useState({});

  const colorKey = selectedAgent?.theme?.color || 'indigo';
  const theme = COLOR_THEMES[colorKey] || COLOR_THEMES.indigo;
  const AgentIcon = selectedAgent ? getIconComponent(selectedAgent.theme.icon) : Bot;

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

  return (
    <div className="w-full flex flex-col gap-4 animate-fade-in">
      
      {/* Top Bar Navigation & Live Status */}
      <div className="px-4 py-3 rounded-xl bg-[#141417] border border-[#27272a] flex items-center justify-between gap-4 shadow-md">
        <div className="flex items-center gap-3">
          <button
            onClick={onReturnToBuilder}
            className="px-2.5 py-1 rounded-md bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 hover:text-white transition-all flex items-center gap-1 text-xs font-medium"
          >
            <ChevronLeft className="w-3.5 h-3.5" />
            <span>Catalogue Agents</span>
          </button>

          <div className="h-4 w-px bg-zinc-800 hidden sm:block" />

          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-md bg-zinc-900 border border-zinc-800 text-zinc-200">
              <AgentIcon className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-xs font-bold text-zinc-50 flex items-center gap-2">
                {selectedAgent?.displayName.split(' - ')[0]}
                <span className={`text-[10px] px-2 py-0.5 rounded-md font-mono ${theme.badge}`}>
                  {selectedAgent?.datasetId}
                </span>
              </h3>
            </div>
          </div>
        </div>

        {/* Live Status Indicator & Reset */}
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-md bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[11px] font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span>SESSION EN DIRECT</span>
          </div>

          <button
            onClick={onResetChat}
            title="Effacer la conversation"
            className="p-1.5 rounded-md bg-zinc-900 hover:bg-zinc-800 text-zinc-400 hover:text-white border border-zinc-800 text-xs"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Main Bento Layout: 70% Result Canvas Priority (9 cols) + 30% Challenge & Controls (3 cols) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        
        {/* Left Column: Challenge Chips & Voice Controller (3 cols) */}
        <div className="lg:col-span-3 flex flex-col gap-3">
          
          {/* Integrated Compact Gemini Voice Orb */}
          <div className="p-3.5 rounded-xl bg-[#141417] border border-[#27272a] shadow-md flex items-center justify-between">
            <GeminiOrb
              isListening={voiceProps.isListening}
              isSpeaking={voiceProps.isSpeaking}
              isStreaming={isStreaming}
              onClickMic={voiceProps.isListening ? voiceProps.stopListening : voiceProps.startListening}
              speechSupported={voiceProps.speechSupported}
              agentTheme={selectedAgent?.theme}
            />
          </div>

          {/* Smart Challenge Chips */}
          <div className="p-3.5 rounded-xl bg-[#141417] border border-[#27272a] flex flex-col gap-2.5 shadow-md">
            <div className="flex items-center justify-between pb-2 border-b border-zinc-800">
              <h4 className="text-[11px] font-bold uppercase tracking-wider text-zinc-400 flex items-center gap-1.5">
                <Zap className="w-3.5 h-3.5 text-indigo-400" />
                Défis Métiers Proposés
              </h4>
            </div>

            <p className="text-[11px] text-zinc-400 leading-relaxed">
              Sélectionnez une question métier type pour interroger la base :
            </p>

            <div className="flex flex-col gap-1.5">
              {selectedAgent?.exampleQueries?.map((q, idx) => (
                <button
                  key={idx}
                  disabled={isStreaming}
                  onClick={() => onSendMessage(q)}
                  className={`p-2.5 rounded-lg border text-[11px] text-left transition-colors flex items-start justify-between gap-2 ${
                    isStreaming
                      ? 'opacity-50 cursor-not-allowed bg-zinc-950 border-zinc-900 text-zinc-600'
                      : 'bg-zinc-950 border-zinc-800/80 hover:border-zinc-700 text-zinc-300 hover:text-white'
                  }`}
                >
                  <span className="line-clamp-2 leading-relaxed">{q}</span>
                  <ArrowRight className="w-3.5 h-3.5 shrink-0 text-zinc-500 mt-0.5" />
                </button>
              ))}
            </div>
          </div>

        </div>

        {/* Right Column: 70% Result Canvas & Prompt Dock (9 cols) */}
        <div className="lg:col-span-9 flex flex-col gap-3">
          
          {/* Error Alert */}
          {error && (
            <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-300 text-xs flex items-start gap-2">
              <AlertCircle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold block">Notification Système / Mode Dégradé :</span>
                <span>{error}</span>
              </div>
            </div>
          )}

          {/* Result Canvas (High Priority 70% space) */}
          <div className="p-5 rounded-xl bg-[#141417] border border-[#27272a] min-h-[420px] max-h-[560px] overflow-y-auto space-y-4 shadow-lg">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-8 text-zinc-500 my-auto">
                <Bot className="w-8 h-8 text-zinc-600 mb-2" />
                <h4 className="text-xs font-bold text-zinc-300">Session démarrée avec l'agent {selectedAgent?.displayName.split(' - ')[0]}</h4>
                <p className="text-[11px] text-zinc-500 max-w-sm mt-1">
                  Posez votre question à l'oral ou sélectionnez un défi à gauche pour obtenir l'analyse décisionnelle BigQuery.
                </p>
              </div>
            ) : (
              messages.map((msg, idx) => {
                const isUser = msg.role === 'user';

                return (
                  <div key={idx} className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} space-y-1.5`}>
                    
                    {/* Header */}
                    <div className="flex items-center gap-1.5 text-[11px] text-zinc-400 px-1">
                      {isUser ? (
                        <>
                          <span>Vous</span>
                          <div className="p-0.5 rounded bg-zinc-800 text-zinc-300">
                            <User className="w-3 h-3" />
                          </div>
                        </>
                      ) : (
                        <>
                          <div className="p-0.5 rounded bg-zinc-800 text-zinc-200">
                            <AgentIcon className="w-3 h-3" />
                          </div>
                          <span className="font-semibold text-zinc-200">{selectedAgent?.displayName.split(' - ')[0]}</span>
                        </>
                      )}
                    </div>

                    {/* Reasoning Accordion */}
                    {!isUser && msg.thoughts && msg.thoughts.length > 0 && (
                      <div className="w-full max-w-3xl rounded-lg bg-zinc-950 border border-zinc-800 text-xs overflow-hidden">
                        <button
                          type="button"
                          onClick={() => toggleThought(idx)}
                          className="w-full px-3 py-2 bg-zinc-900/60 hover:bg-zinc-900 flex items-center justify-between text-zinc-300 font-medium transition-colors text-[11px]"
                        >
                          <div className="flex items-center gap-1.5">
                            <Brain className="w-3.5 h-3.5 text-indigo-400" />
                            <span>Raisonnement & Requête SQL générée ({msg.thoughts.length} étapes)</span>
                          </div>
                          {showThoughtsMap[idx] ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                        </button>

                        {showThoughtsMap[idx] && (
                          <div className="p-3 font-mono text-[11px] text-zinc-300 bg-zinc-950 border-t border-zinc-800 space-y-1.5">
                            {msg.thoughts.map((t, tIdx) => (
                              <div key={tIdx} className="p-2 rounded bg-zinc-900/80 border border-zinc-800">
                                {t}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Message Content Bubble */}
                    <div
                      className={`max-w-3xl rounded-xl px-4 py-3 text-xs leading-relaxed shadow-md ${
                        isUser
                          ? 'bg-indigo-600 text-white rounded-tr-none'
                          : 'bg-zinc-950 border border-zinc-800 text-zinc-100 rounded-tl-none markdown-content'
                      }`}
                    >
                      {isUser ? (
                        <p className="whitespace-pre-wrap">{msg.content}</p>
                      ) : (
                        <div>
                          {msg.isStreaming && !msg.content ? (
                            <div className="flex items-center gap-2 text-indigo-300 font-mono text-xs py-1">
                              <Loader2 className="w-3.5 h-3.5 animate-spin text-indigo-400" />
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

          {/* Hybrid Text Input Dock */}
          <form onSubmit={handleFormSubmit} className="p-3 rounded-xl bg-[#141417] border border-[#27272a] shadow-md">
            <div className="flex items-center gap-2">
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
                className="w-full px-3.5 py-2.5 rounded-lg bg-zinc-950 border border-zinc-800 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-zinc-700 resize-none"
              />

              <button
                type="submit"
                disabled={!inputPrompt.trim() || isStreaming}
                className={`h-full px-4 py-2.5 rounded-lg font-semibold text-xs flex items-center justify-center gap-1.5 transition-all ${
                  !inputPrompt.trim() || isStreaming
                    ? 'bg-zinc-800 text-zinc-500 cursor-not-allowed border border-zinc-700'
                    : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-md'
                }`}
              >
                {isStreaming ? (
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                ) : (
                  <>
                    <span>Envoyer</span>
                    <Send className="w-3.5 h-3.5" />
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
