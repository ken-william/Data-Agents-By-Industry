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
import { getIconComponent, getAgentTheme } from '../utils/themeMap';

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
      <div className="px-5 py-3 rounded-2xl bg-white/90 border border-slate-200/90 backdrop-blur-xl flex items-center justify-between gap-4 shadow-sm">
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={onReturnToBuilder}
            className="px-3.5 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition-all flex items-center gap-1.5 text-xs font-semibold"
          >
            <ChevronLeft className="w-4 h-4" />
            <span>Changer d'Espace</span>
          </button>

          <div className="h-4 w-px bg-slate-200 hidden sm:block" />

          <div className="flex items-center gap-2.5">
            <div className="p-1.5 rounded-xl bg-blue-50 border border-blue-200 text-blue-600">
              <AgentIcon className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-xs sm:text-sm font-bold text-slate-900 flex items-center gap-2">
                {selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : selectedAgent?.id}
                <span className="text-[11px] px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-medium">
                  • Connecté
                </span>
              </h3>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold">
            <span className="w-2 h-2 rounded-full bg-blue-600 animate-pulse" />
            <span>{isShowcase ? 'ÉCRAN A : SHOWCASE' : 'ÉCRAN B : CONTRÔLEUR'}</span>
          </div>

          <button
            type="button"
            onClick={onResetChat}
            title="Effacer la conversation"
            className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 border border-slate-200 text-xs"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Main Gemini Chat Bento Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        
        {/* Left Column: Orbe Gemini Live + Gemini Suggestion Cards (4 cols) */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          
          {/* Gemini Live Physics Wave Orb */}
          <div className="p-6 rounded-2xl bg-white/90 border border-slate-200/90 shadow-sm backdrop-blur-xl flex flex-col items-center justify-center text-center">
            <div className="mb-2">
              <span className="text-xs font-medium text-slate-500 block">
                Copilote Conversational Analytics
              </span>
              <h4 className="text-sm font-bold text-slate-900">
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

            <div className="mt-3 flex items-center gap-1.5 text-[11px] text-blue-700 bg-blue-50 px-3 py-1 rounded-full border border-blue-200 font-medium">
              <Volume2 className="w-3.5 h-3.5" />
              <span>Synthèse vocale purifiée active</span>
            </div>
          </div>

          {/* Gemini Chat Suggestion Cards (Style officiel Gemini Material 3) */}
          <div className="p-4 rounded-2xl bg-white/90 border border-slate-200/90 shadow-sm flex flex-col gap-3">
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-800 flex items-center gap-1.5">
                <Sparkles className="w-4 h-4 text-blue-600" />
                Suggestions Gemini
              </h4>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200 font-semibold">
                {selectedAgent?.exampleQueries?.length || 0} Questions
              </span>
            </div>

            <div className="flex flex-col gap-2">
              {selectedAgent?.exampleQueries?.map((q, idx) => (
                <button
                  key={idx}
                  disabled={isStreaming}
                  onClick={() => onSendMessage(q)}
                  className={`p-3.5 rounded-2xl border text-xs text-left transition-all flex items-start justify-between gap-3 ${
                    isStreaming
                      ? 'opacity-50 cursor-not-allowed bg-slate-50 border-slate-200 text-slate-400'
                      : 'bg-white hover:bg-blue-50/80 border-slate-200 hover:border-blue-400 text-slate-800 hover:text-blue-900 shadow-xs transform hover:-translate-y-0.5'
                  }`}
                >
                  <span className="line-clamp-2 leading-relaxed font-semibold">{q}</span>
                  <ArrowRight className="w-4 h-4 shrink-0 text-blue-600 mt-0.5" />
                </button>
              ))}
            </div>
          </div>

        </div>

        {/* Right Column: 70% Result Canvas Priority (8 cols) */}
        <div className="lg:col-span-8 flex flex-col gap-4">
          
          {/* Error Notification */}
          {error && (
            <div className="p-3.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-xs flex items-start gap-2.5">
              <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold block">Notification Système / Mode Dégradé :</span>
                <span>{error}</span>
              </div>
            </div>
          )}

          {/* Clean Light Report Document Canvas (Gemini Chat UI) */}
          <div className="p-6 rounded-2xl bg-white/95 border border-slate-200/90 min-h-[440px] max-h-[580px] overflow-y-auto space-y-4 shadow-sm backdrop-blur-xl">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-8 text-slate-400 my-auto">
                <Bot className="w-10 h-10 text-blue-600 mb-2 animate-bounce" />
                <h4 className="text-sm font-bold text-slate-800">
                  Espace de travail prêt pour {selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : selectedAgent?.id}
                </h4>
                <p className="text-xs text-slate-500 max-w-sm mt-1">
                  Posez votre question à l'oral ou cliquez sur une suggestion ci-contre pour déclencher l'analyse décisionnelle BigQuery.
                </p>
              </div>
            ) : (
              messages.map((msg, idx) => {
                const isUser = msg.role === 'user';

                return (
                  <div key={idx} className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} space-y-2`}>
                    
                    {/* Header */}
                    <div className="flex items-center gap-1.5 text-[11px] text-slate-500 px-1">
                      {isUser ? (
                        <>
                          <span className="text-slate-700 font-medium">Vous</span>
                          <div className="p-1 rounded-lg bg-slate-100 text-slate-600 border border-slate-200">
                            <User className="w-3 h-3" />
                          </div>
                        </>
                      ) : (
                        <>
                          <div className="p-1 rounded-lg bg-blue-50 text-blue-600 border border-blue-200">
                            <AgentIcon className="w-3 h-3" />
                          </div>
                          <span className="font-semibold text-slate-800">
                            {selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : selectedAgent?.id}
                          </span>
                        </>
                      )}
                    </div>

                    {/* Reasoning Accordion */}
                    {!isUser && msg.thoughts && msg.thoughts.length > 0 && (
                      <div className="w-full max-w-3xl rounded-2xl bg-slate-50 border border-slate-200 text-xs overflow-hidden">
                        <button
                          type="button"
                          onClick={() => toggleThought(idx)}
                          className="w-full px-3.5 py-2.5 bg-slate-100 hover:bg-slate-200/80 flex items-center justify-between text-slate-700 font-medium transition-colors text-xs"
                        >
                          <div className="flex items-center gap-2">
                            <Brain className="w-4 h-4 text-blue-600" />
                            <span>Détails techniques : Requête générée par Vertex AI ({msg.thoughts.length} étapes)</span>
                          </div>
                          {showThoughtsMap[idx] ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                        </button>

                        {showThoughtsMap[idx] && (
                          <div className="p-3.5 font-mono text-[11px] text-slate-800 bg-white border-t border-slate-200 space-y-2">
                            {msg.thoughts.map((t, tIdx) => (
                              <div key={tIdx} className="p-2.5 rounded-lg bg-slate-900 text-cyan-300 border border-slate-800 overflow-x-auto">
                                {t}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}

                    {/* SQL Inspector Flip Card */}
                    {!isUser && (
                      <SQLFlipCard
                        datasetId={selectedAgent?.datasetId}
                        sqlQuery={`SELECT * FROM \`${selectedAgent?.datasetId || 'public_sector_employment_ds'}\` WHERE 1=1 LIMIT 10;`}
                        executionTime="1.42s"
                      />
                    )}

                    {/* Message Bubble */}
                    <div
                      className={`max-w-3xl rounded-2xl px-5 py-4 leading-relaxed shadow-sm ${
                        isUser
                          ? 'bg-[#0B57D0] text-white rounded-tr-none text-xs sm:text-sm font-medium'
                          : 'bg-white border border-slate-200/90 text-slate-800 rounded-tl-none markdown-content'
                      }`}
                    >
                      {isUser ? (
                        <p className="whitespace-pre-wrap">{msg.content}</p>
                      ) : (
                        <div>
                          {msg.isStreaming && !msg.content ? (
                            <div className="flex items-center gap-2 text-blue-700 font-mono text-xs py-1">
                              <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
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

          {/* Floating Input Dock Gemini Material 3 (#F0F4F9) */}
          <form onSubmit={handleFormSubmit} className="p-3 rounded-full bg-[#F0F4F9] border border-slate-200/80 shadow-md backdrop-blur-xl">
            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={voiceProps.isListening ? voiceProps.stopListening : voiceProps.startListening}
                className={`p-2.5 rounded-full transition-all ${
                  voiceProps.isListening
                    ? 'bg-rose-500 text-white animate-pulse'
                    : 'bg-white text-blue-600 hover:bg-blue-50 border border-slate-200 shadow-xs'
                }`}
                title="Microphone Push-to-Talk"
              >
                <Mic className="w-4.5 h-4.5" />
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
                className="w-full px-2 py-1 text-xs sm:text-sm text-slate-900 placeholder-slate-500 focus:outline-none bg-transparent resize-none font-medium"
              />

              <button
                type="submit"
                disabled={!inputPrompt.trim() || isStreaming}
                className={`px-5 py-2.5 rounded-full font-bold text-xs sm:text-sm flex items-center justify-center gap-2 transition-all ${
                  !inputPrompt.trim() || isStreaming
                    ? 'bg-slate-200 text-slate-400 cursor-not-allowed border border-slate-300'
                    : 'bg-[#0B57D0] hover:bg-blue-800 text-white shadow-md'
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
