import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Send, Bot, User, Brain, ChevronDown, ChevronUp, AlertCircle, Loader2, Sparkles, Database } from 'lucide-react';
import { COLOR_THEMES, getIconComponent } from '../utils/themeMap';
import { VoiceController } from './VoiceController';

export function ChatPanel({
  selectedAgent,
  messages,
  isStreaming,
  thoughts,
  error,
  onSendMessage,
  voiceProps
}) {
  const [inputPrompt, setInputPrompt] = useState('');
  const [showThoughtsMap, setShowThoughtsMap] = useState({});
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const colorKey = selectedAgent?.theme?.color || 'indigo';
  const theme = COLOR_THEMES[colorKey] || COLOR_THEMES.indigo;
  const AgentIcon = selectedAgent ? getIconComponent(selectedAgent.theme.icon) : Bot;

  // Sync mic transcript into textarea input
  useEffect(() => {
    if (voiceProps.transcript) {
      setInputPrompt(voiceProps.transcript);
    }
  }, [voiceProps.transcript]);

  // Auto-scroll chat to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, thoughts, isStreaming]);

  // Auto-resize textarea
  const handleInputChange = (e) => {
    setInputPrompt(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
    }
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (!inputPrompt.trim() || isStreaming) return;
    onSendMessage(inputPrompt);
    setInputPrompt('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleFormSubmit(e);
    }
  };

  const toggleThought = (idx) => {
    setShowThoughtsMap(prev => ({ ...prev, [idx]: !prev[idx] }));
  };

  return (
    <div className={`w-full flex flex-col rounded-2xl glass-panel border ${theme.border} shadow-2xl overflow-hidden transition-all duration-300 min-h-[550px] max-h-[750px]`}>
      
      {/* Panel Header */}
      <div className={`px-5 py-3.5 border-b border-slate-800 bg-slate-900/90 flex items-center justify-between gap-3`}>
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-lg ${theme.accentBg} text-white shadow-md`}>
            <AgentIcon className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              {selectedAgent ? selectedAgent.displayName : 'Sélectionnez un Agent'}
              <span className={`text-[10px] px-2 py-0.5 rounded-full border font-mono ${theme.badge}`}>
                {selectedAgent?.datasetId || 'BigQuery'}
              </span>
            </h3>
            <p className="text-xs text-slate-400 line-clamp-1">
              {selectedAgent?.description}
            </p>
          </div>
        </div>

        {/* Status indicator */}
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span className="text-xs font-mono text-emerald-400 hidden sm:inline">Vertex AI Live</span>
        </div>
      </div>

      {/* Resilient Error Banner */}
      {error && (
        <div className="mx-4 mt-4 p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs flex items-start gap-2.5">
          <AlertCircle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold block">Notification système / Mode dégradé :</span>
            <span>{error}</span>
          </div>
        </div>
      )}

      {/* Chat Messages Container */}
      <div className="flex-1 p-5 overflow-y-auto space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-8 text-slate-500 my-auto">
            <div className={`p-4 rounded-2xl ${theme.bgLight} ${theme.text} mb-3`}>
              <Sparkles className="w-8 h-8 animate-pulse" />
            </div>
            <h4 className="text-sm font-bold text-slate-300 mb-1">
              Posez votre question à l'oral ou par texte
            </h4>
            <p className="text-xs text-slate-500 max-w-md">
              L'agent interrogera directement la base de données BigQuery et les documents Cloud Storage pour vous apporter une analyse décisionnelle en langage naturel.
            </p>
          </div>
        ) : (
          messages.map((msg, idx) => {
            const isUser = msg.role === 'user';

            return (
              <div key={idx} className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} space-y-2`}>
                
                {/* User / Agent Avatar & Name */}
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
                      <span className="font-semibold text-slate-200">
                        {selectedAgent ? selectedAgent.displayName.split(' - ')[0] : 'Agent'}
                      </span>
                      <span className="font-mono text-slate-500">{msg.timestamp}</span>
                    </>
                  )}
                </div>

                {/* Agent Thoughts Accordion (Segregated from Final Response) */}
                {!isUser && msg.thoughts && msg.thoughts.length > 0 && (
                  <div className="w-full max-w-3xl rounded-xl bg-slate-900/90 border border-indigo-500/20 text-xs overflow-hidden">
                    <button
                      type="button"
                      onClick={() => toggleThought(idx)}
                      className="w-full px-3 py-2 bg-indigo-950/40 hover:bg-indigo-900/40 flex items-center justify-between text-indigo-300 font-medium transition-colors"
                    >
                      <div className="flex items-center gap-2">
                        <Brain className="w-3.5 h-3.5 text-indigo-400 animate-pulse" />
                        <span>Raisonnement & Requête SQL générée ({msg.thoughts.length} étapes)</span>
                      </div>
                      {showThoughtsMap[idx] ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>

                    {showThoughtsMap[idx] && (
                      <div className="p-3 font-mono text-[11px] text-slate-300 bg-slate-950/60 border-t border-indigo-500/20 space-y-2">
                        {msg.thoughts.map((t, tIdx) => (
                          <div key={tIdx} className="p-2 rounded bg-slate-900 border border-slate-800">
                            {t}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* Message Content Bubble */}
                <div
                  className={`max-w-3xl rounded-2xl px-4 py-3 text-xs sm:text-sm leading-relaxed shadow-lg ${
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
                        <div className="flex items-center gap-2 text-indigo-300 py-1 font-mono text-xs">
                          <Loader2 className="w-4 h-4 animate-spin text-indigo-400" />
                          <span>Analyse BigQuery en cours...</span>
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
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form & Voice Controller Toolbar */}
      <form onSubmit={handleFormSubmit} className="p-3.5 bg-slate-900/90 border-t border-slate-800/80">
        <div className="relative flex flex-col gap-2">
          
          {/* Textarea */}
          <textarea
            ref={textareaRef}
            rows={1}
            value={inputPrompt}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder={`Posez votre question à ${selectedAgent ? selectedAgent.displayName.split(' - ')[0] : 'l\'agent'} (ex: Quel est le ROI, la vacance des postes...)...`}
            className="w-full px-4 py-3 rounded-xl bg-slate-950 border border-slate-800 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 resize-none transition-all"
          />

          {/* Controls Bar: Voice Mic + Submit Button */}
          <div className="flex items-center justify-between">
            <VoiceController
              isListening={voiceProps.isListening}
              startListening={voiceProps.startListening}
              stopListening={voiceProps.stopListening}
              isSpeaking={voiceProps.isSpeaking}
              stopSpeaking={voiceProps.stopSpeaking}
              speechSupported={voiceProps.speechSupported}
              selectedAgent={selectedAgent}
            />

            <button
              type="submit"
              disabled={!inputPrompt.trim() || isStreaming}
              className={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 transition-all shadow-lg ${
                !inputPrompt.trim() || isStreaming
                  ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-800'
                  : `${theme.button} hover:scale-105`
              }`}
            >
              {isStreaming ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Envoi...</span>
                </>
              ) : (
                <>
                  <span>Envoyer</span>
                  <Send className="w-3.5 h-3.5" />
                </>
              )}
            </button>
          </div>

        </div>
      </form>

    </div>
  );
}
