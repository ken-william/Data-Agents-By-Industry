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
  Mic,
  Sparkles
} from 'lucide-react';
import { COLOR_THEMES, getIconComponent, getAgentTheme } from '../utils/themeMap';

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

  const theme = getAgentTheme(selectedAgent?.theme);
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
    <div className="w-full flex flex-col gap-4 animate-fade-in relative pb-24">
      
      {/* Top Bar Navigation */}
      <div className="px-4 py-3 rounded-2xl bento-card flex items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <button
            onClick={onReturnToBuilder}
            className="px-3 py-1.5 rounded-lg bg-slate-900/90 hover:bg-slate-800 border border-slate-700 text-slate-300 hover:text-white transition-all flex items-center gap-1.5 text-xs font-semibold"
          >
            <ChevronLeft className="w-4 h-4" />
            <span>Catalogue Agents</span>
          </button>

          <div className="h-4 w-px bg-slate-800 hidden sm:block" />

          <div className="flex items-center gap-2">
            <div className={`p-1.5 rounded-lg bg-slate-950 border border-slate-800 ${theme.text}`}>
              <AgentIcon className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-xs sm:text-sm font-bold text-slate-50 flex items-center gap-2">
                {selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : selectedAgent?.id}
                <span className={`text-[10px] px-2 py-0.5 rounded-lg font-mono ${theme.badge}`}>
                  {selectedAgent?.datasetId}
                </span>
              </h3>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-sky-500/10 border border-sky-500/20 text-sky-400 text-xs font-semibold">
            <span className="w-2 h-2 rounded-full bg-sky-400 animate-pulse" />
            <span>{isShowcase ? 'ÉCRAN A : SHOWCASE PUBLIC' : 'ÉCRAN B : CONTRÔLEUR TACTILE'}</span>
          </div>

          <button
            onClick={onResetChat}
            title="Effacer la conversation"
            className="p-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-white border border-slate-800 text-xs"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Main Dual Screen Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        
        {/* Left Column: Orbe Gemini Live + Smart Chips (4 cols) */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          
          {/* Gemini Live Physics Wave Orb */}
          <div className="p-6 rounded-2xl bento-card shadow-xl flex flex-col items-center justify-center text-center">
            <div className="mb-2">
              <span className="text-xs font-semibold text-slate-400 block">
                Copilote Conversational Analytics
              </span>
              <h4 className="text-sm font-bold text-slate-100">
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
          </div>

          {/* Smart Challenge Chips */}
          <div className="p-4 rounded-2xl bento-card flex flex-col gap-3 shadow-xl">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
                <Zap className="w-4 h-4 text-sky-400" />
                Défis Métiers Proposés
              </h4>
              <span className="text-[10px] px-2 py-0.5 rounded bg-slate-950 text-slate-400 font-mono">
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
                      ? 'opacity-50 cursor-not-allowed bg-slate-950 border-slate-800 text-slate-600'
                      : 'bg-slate-950/80 border-slate-800 hover:border-sky-500/40 text-slate-200 hover:text-white'
                  }`}
                >
                  <span className="line-clamp-2 leading-relaxed">{q}</span>
                  <ArrowRight className="w-4 h-4 shrink-0 text-sky-400 mt-0.5" />
                </button>
              ))}
            </div>
          </div>

        </div>

        {/* Right Column: 70% Result Canvas Priority (8 cols) */}
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

          {/* Dynamic Result Canvas (70% priority, Looker KPI & Markdown) */}
          <div className="p-6 rounded-2xl bento-card min-h-[440px] max-h-[580px] overflow-y-auto space-y-4 shadow-xl">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-8 text-slate-500 my-auto">
                <Bot className="w-10 h-10 text-slate-600 mb-2 animate-bounce" />
                <h4 className="text-sm font-bold text-slate-300">
                  Session démarrée avec l'agent {selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : selectedAgent?.id}
                </h4>
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
                          <div className="p-1 rounded bg-slate-950 text-slate-300 border border-slate-800">
                            <User className="w-3 h-3" />
                          </div>
                        </>
                      ) : (
                        <>
                          <div className={`p-1 rounded bg-slate-950 border border-slate-800 ${theme.text}`}>
                            <AgentIcon className="w-3 h-3" />
                          </div>
                          <span className="font-semibold text-slate-200">
                            {selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : selectedAgent?.id}
                          </span>
                        </>
                      )}
                    </div>

                    {/* Reasoning Accordion */}
                    {!isUser && msg.thoughts && msg.thoughts.length > 0 && (
                      <div className="w-full max-w-3xl rounded-xl bg-slate-950 border border-slate-800 text-xs overflow-hidden">
                        <button
                          type="button"
                          onClick={() => toggleThought(idx)}
                          className="w-full px-3.5 py-2.5 bg-slate-900/80 hover:bg-slate-900 flex items-center justify-between text-slate-300 font-medium transition-colors text-xs"
                        >
                          <div className="flex items-center gap-2">
                            <Brain className="w-4 h-4 text-sky-400" />
                            <span>Raisonnement & Requête SQL générée ({msg.thoughts.length} étapes)</span>
                          </div>
                          {showThoughtsMap[idx] ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                        </button>

                        {showThoughtsMap[idx] && (
                          <div className="p-3.5 font-mono text-[11px] text-slate-300 bg-slate-950 border-t border-slate-800 space-y-2">
                            {msg.thoughts.map((t, tIdx) => (
                              <div key={tIdx} className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                                {t}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}

                    {/* SQL Flip Inspector Card for Agent Responses */}
                    {!isUser && (
                      <SQLFlipCard
                        datasetId={selectedAgent?.datasetId}
                        sqlQuery={`SELECT * FROM \`${selectedAgent?.datasetId || 'public_sector_employment_ds'}\` WHERE 1=1 LIMIT 10;`}
                        executionTime="1.42s"
                      />
                    )}

                    {/* Message Bubble */}
                    <div
                      className={`max-w-3xl rounded-2xl px-5 py-4 leading-relaxed shadow-lg ${
                        isUser
                          ? 'bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 text-white rounded-tr-none text-xs sm:text-sm font-semibold'
                          : 'bg-slate-950 border border-slate-800 text-slate-100 rounded-tl-none markdown-content'
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

        </div>

      </div>

      {/* Fixed Hybrid Input Dock (Anti-Noise Bar fixed at bottom) */}
      <div className="fixed bottom-0 inset-x-0 z-40 p-4 bg-gradient-to-t from-[#020617] via-[#020617]/95 to-transparent">
        <div className="max-w-3xl mx-auto flex flex-col gap-2">
          
          <form onSubmit={handleFormSubmit} className="p-2 rounded-full bg-slate-900/90 border border-slate-700/80 shadow-2xl flex items-center gap-2 backdrop-blur-md">
            
            {/* Push-to-Talk Mic Button */}
            <button
              type="button"
              onClick={voiceProps.isListening ? voiceProps.stopListening : voiceProps.startListening}
              className={`p-3 rounded-full transition-all ${
                voiceProps.isListening
                  ? 'bg-rose-600 text-white animate-pulse'
                  : 'bg-slate-800 hover:bg-slate-700 text-sky-400'
              }`}
              title="Push-to-Talk Microphone"
            >
              <Mic className="w-4 h-4" />
            </button>

            {/* Input Text Field */}
            <input
              type="text"
              value={inputPrompt}
              onChange={handleInputChange}
              placeholder={voiceProps.speechSupported ? "Posez une question ou utilisez le micro..." : "Environnement bruyant ? Saisissez votre question ici !"}
              className="w-full px-3 py-2 bg-transparent text-xs sm:text-sm text-slate-100 placeholder-slate-400 focus:outline-none"
            />

            {/* Send Button */}
            <button
              type="submit"
              disabled={!inputPrompt.trim() || isStreaming}
              className={`p-3 rounded-full font-bold text-xs flex items-center justify-center transition-all ${
                !inputPrompt.trim() || isStreaming
                  ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
                  : 'bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 text-white shadow-lg'
              }`}
            >
              {isStreaming ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
            </button>
          </form>

          {/* Smart Chips Shortcuts */}
          <div className="flex items-center justify-center gap-2 overflow-x-auto py-1">
            <button
              onClick={() => onSendMessage("Chiffre d'affaires Q3 et projections")}
              className="px-3 py-1 rounded-full bg-slate-900/80 border border-slate-700 text-slate-300 hover:text-white text-[11px] font-medium transition-all"
            >
              💡 "Chiffre d'affaires Q3"
            </button>
            <button
              onClick={() => onSendMessage("Analyse des gares saturées et retards")}
              className="px-3 py-1 rounded-full bg-slate-900/80 border border-slate-700 text-slate-300 hover:text-white text-[11px] font-medium transition-all"
            >
              💡 "Analyse des gares saturées"
            </button>
          </div>

        </div>
      </div>

    </div>
  );
}
