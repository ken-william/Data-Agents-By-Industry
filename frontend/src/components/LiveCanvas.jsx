import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { GeminiOrb } from './GeminiOrb';
import { SQLFlipCard } from './SQLFlipCard';
import { VoiceController } from './VoiceController';
import {
  Sparkles,
  Bot,
  User,
  Brain,
  ChevronDown,
  ChevronUp,
  AlertCircle,
  Loader2,
  Send,
  HelpCircle,
  ArrowRight,
  Database,
  Volume2,
  VolumeX,
  RotateCcw,
  Zap,
  CheckCircle2,
  SlidersHorizontal,
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

  const latestMessage = messages.length > 0 ? messages[messages.length - 1] : null;

  return (
    <div className="w-full flex flex-col gap-5 animate-fade-in">
      
      {/* Top Bar Navigation & Live Badge */}
      <div className="px-5 py-3.5 rounded-3xl glass-panel border border-slate-800 flex items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <button
            onClick={onReturnToBuilder}
            className="p-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 hover:text-white transition-all flex items-center gap-1.5 text-xs font-semibold"
          >
            <ChevronLeft className="w-4 h-4" />
            <span>Changer d'Agent</span>
          </button>

          <div className="h-6 w-px bg-slate-800 hidden sm:block" />

          <div className="flex items-center gap-2.5">
            <div className={`p-2 rounded-xl ${theme.accentBg} text-white shadow-md`}>
              <AgentIcon className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                {selectedAgent?.displayName}
                <span className={`text-[10px] px-2 py-0.5 rounded-full border font-mono ${theme.badge}`}>
                  {selectedAgent?.datasetId}
                </span>
              </h3>
            </div>
          </div>
        </div>

        {/* Live Status Badge */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
            <span>LIVE EXPERIENCE</span>
          </div>

          <button
            onClick={onResetChat}
            title="Réinitialiser la conversation"
            className="p-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-white border border-slate-800 text-xs"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Main Bento Grid live board */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        
        {/* Left Column: Challenge Panel / Smart Chips (4 cols) */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          <div className="p-5 rounded-3xl glass-panel border border-slate-800 flex flex-col gap-3 shadow-xl">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
                <Zap className={`w-4 h-4 ${theme.text}`} />
                Défis & Questions Métiers
              </h4>
              <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">
                {selectedAgent?.exampleQueries?.length || 0} Suggestions
              </span>
            </div>

            <p className="text-xs text-slate-400 leading-relaxed">
              Cliquez sur l'un des défis ci-dessous pour tester immédiatement les capacités décisionnelles de l'agent :
            </p>

            <div className="flex flex-col gap-2 mt-1">
              {selectedAgent?.exampleQueries?.map((q, idx) => (
                <button
                  key={idx}
                  disabled={isStreaming}
                  onClick={() => onSendMessage(q)}
                  className={`group p-3 rounded-2xl border text-xs text-left transition-all duration-300 flex items-start justify-between gap-2.5 ${
                    isStreaming
                      ? 'opacity-50 cursor-not-allowed bg-slate-900 border-slate-800 text-slate-500'
                      : `glass-card border-slate-800 hover:${theme.border} hover:bg-slate-800/80 text-slate-200 hover:text-white`
                  }`}
                >
                  <span className="line-clamp-2 leading-relaxed">{q}</span>
                  <ArrowRight className={`w-4 h-4 shrink-0 transition-transform group-hover:translate-x-1 ${theme.text}`} />
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Interactive Gemini Audio Orb + Conversation Results (8 cols) */}
        <div className="lg:col-span-8 flex flex-col gap-5">
          
          {/* Reactive Gemini Voice Orb Section */}
          <div className={`p-6 rounded-3xl glass-panel border ${theme.border} ${theme.glow} flex flex-col items-center justify-center relative overflow-hidden shadow-2xl`}>
            
            {/* Proactive Agent Greeting */}
            <div className="w-full text-center mb-2">
              <span className="text-xs font-semibold text-slate-400">
                🤖 Assistant Vocale & Textuelle {selectedAgent?.displayName.split(' - ')[0]}
              </span>
              <p className="text-sm font-semibold text-white mt-1">
                « Posez votre question à l'oral ou par écrit. Je consulte les tables BigQuery et Cloud Storage pour vous répondre. »
              </p>
            </div>

            {/* Reactive Voice Orb */}
            <GeminiOrb
              isListening={voiceProps.isListening}
              isSpeaking={voiceProps.isSpeaking}
              isStreaming={isStreaming}
              onClickMic={voiceProps.isListening ? voiceProps.stopListening : voiceProps.startListening}
              speechSupported={voiceProps.speechSupported}
              agentTheme={selectedAgent?.theme}
            />

          </div>

          {/* Resilient Error Banner */}
          {error && (
            <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs flex items-start gap-2.5">
              <AlertCircle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold block">Notification Système / Restitution en Mode Dégradé :</span>
                <span>{error}</span>
              </div>
            </div>
          )}

          {/* Results Canvas / Conversation History */}
          <div className="p-6 rounded-3xl glass-panel border border-slate-800 min-h-[350px] max-h-[500px] overflow-y-auto space-y-4 shadow-xl">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-8 text-slate-500 my-auto">
                <Bot className="w-10 h-10 text-slate-600 mb-2 animate-bounce" />
                <h4 className="text-sm font-bold text-slate-300">Aucune question posée pour le moment</h4>
                <p className="text-xs text-slate-500 max-w-sm mt-1">
                  Parlez dans le micro ou sélectionnez un défi à gauche pour lancer votre première requête.
                </p>
              </div>
            ) : (
              messages.map((msg, idx) => {
                const isUser = msg.role === 'user';

                return (
                  <div key={idx} className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} space-y-2`}>
                    
                    {/* User / Agent Header */}
                    <div className="flex items-center gap-2 text-[11px] text-slate-400 px-1">
                      {isUser ? (
                        <>
                          <span>Vous</span>
                          <div className="p-1 rounded bg-slate-800 text-slate-300">
                            <User className="w-3 h-3" />
                          </div>
                        </>
                      ) : (
                        <>
                          <div className={`p-1 rounded ${theme.accentBg} text-white`}>
                            <AgentIcon className="w-3 h-3" />
                          </div>
                          <span className="font-semibold text-slate-200">{selectedAgent?.displayName.split(' - ')[0]}</span>
                        </>
                      )}
                    </div>

                    {/* Agent Thoughts Accordion */}
                    {!isUser && msg.thoughts && msg.thoughts.length > 0 && (
                      <div className="w-full max-w-2xl rounded-2xl bg-slate-900/90 border border-indigo-500/20 text-xs overflow-hidden">
                        <button
                          type="button"
                          onClick={() => toggleThought(idx)}
                          className="w-full px-3.5 py-2.5 bg-indigo-950/40 hover:bg-indigo-900/40 flex items-center justify-between text-indigo-300 font-medium transition-colors"
                        >
                          <div className="flex items-center gap-2">
                            <Brain className="w-3.5 h-3.5 text-indigo-400 animate-pulse" />
                            <span>Raisonnement IA & Requête SQL générée ({msg.thoughts.length} étapes)</span>
                          </div>
                          {showThoughtsMap[idx] ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                        </button>

                        {showThoughtsMap[idx] && (
                          <div className="p-3.5 font-mono text-[11px] text-slate-300 bg-slate-950 border-t border-indigo-500/20 space-y-2">
                            {msg.thoughts.map((t, tIdx) => (
                              <div key={tIdx} className="p-2 rounded-xl bg-slate-900 border border-slate-800">
                                {t}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Message Bubble */}
                    <div
                      className={`max-w-2xl rounded-3xl px-5 py-3.5 text-xs sm:text-sm leading-relaxed shadow-xl ${
                        isUser
                          ? `${theme.accentBg} text-white rounded-tr-none`
                          : 'bg-slate-900/90 border border-slate-800 text-slate-100 rounded-tl-none markdown-content'
                      }`}
                    >
                      {isUser ? (
                        <p className="whitespace-pre-wrap">{msg.content}</p>
                      ) : (
                        <div>
                          {msg.isStreaming && !msg.content ? (
                            <div className="flex items-center gap-2 text-indigo-300 font-mono text-xs py-1">
                              <Loader2 className="w-4 h-4 animate-spin text-indigo-400" />
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
          <form onSubmit={handleFormSubmit} className="p-4 rounded-3xl glass-panel border border-slate-800 shadow-2xl">
            <div className="flex flex-col gap-2.5">
              
              <div className="flex items-center gap-2">
                <textarea
                  rows={2}
                  value={inputPrompt}
                  onChange={handleInputChange}
                  placeholder="Posez votre question métiers (ou parlez au micro ci-dessus)..."
                  className="w-full px-4 py-3 rounded-2xl bg-slate-950 border border-slate-800 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 resize-none"
                />

                <button
                  type="submit"
                  disabled={!inputPrompt.trim() || isStreaming}
                  className={`h-full px-5 rounded-2xl font-bold text-xs flex items-center justify-center gap-2 transition-all shadow-lg ${
                    !inputPrompt.trim() || isStreaming
                      ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
                      : `${theme.button} hover:scale-105`
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

            </div>
          </form>

        </div>

      </div>

    </div>
  );
}
