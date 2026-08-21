import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Bot, User, Send, ChevronLeft, RotateCcw, Loader2 } from 'lucide-react';
import { cn } from '../utils/cn';

export function LiveCanvas({
  selectedAgent,
  onReturnToBuilder,
  messages,
  isStreaming,
  error,
  onSendMessage,
  onResetChat
}) {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!prompt.trim() || isStreaming) return;
    onSendMessage(prompt);
    setPrompt('');
  };

  return (
    <div className="w-full max-w-4xl mx-auto py-6 px-4 flex flex-col gap-4">
      
      {/* Navigation */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-200">
        <button
          type="button"
          onClick={onReturnToBuilder}
          className="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold flex items-center gap-1"
        >
          <ChevronLeft className="size-4" />
          <span>Retour</span>
        </button>

        <div className="flex items-center gap-2">
          <Bot className="size-4 text-blue-600" />
          <span className="text-xs font-bold text-slate-900">
            {selectedAgent?.displayName ? selectedAgent.displayName.split(' - ')[0] : selectedAgent?.id}
          </span>
        </div>

        <button
          type="button"
          onClick={onResetChat}
          aria-label="Réinitialiser le chat"
          className="p-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-600 text-xs"
        >
          <RotateCcw className="size-4" />
        </button>
      </div>

      {/* Messages */}
      <div className="min-h-[400px] max-h-[600px] overflow-y-auto space-y-4 p-4 rounded-2xl bg-white border border-slate-200">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-8 text-slate-400 my-auto">
            <Bot className="size-8 text-slate-300 mb-2" />
            <p className="text-xs font-medium">Posez une question pour commencer.</p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={idx}
              className={cn("flex flex-col space-y-1 text-xs sm:text-sm", msg.role === 'user' ? 'items-end' : 'items-start')}
            >
              <div className="text-[10px] text-slate-400 px-1 font-semibold">
                {msg.role === 'user' ? 'Vous' : selectedAgent?.id}
              </div>
              <div
                className={cn(
                  "max-w-2xl rounded-2xl px-4 py-3",
                  msg.role === 'user'
                    ? "bg-blue-600 text-white rounded-tr-none"
                    : "bg-slate-100 text-slate-800 rounded-tl-none markdown-content"
                )}
              >
                {msg.role === 'user' ? (
                  <p>{msg.content}</p>
                ) : (
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="flex items-center gap-2">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Posez votre question..."
          className="flex-1 bg-white border border-slate-200 rounded-full px-4 py-2.5 text-xs sm:text-sm text-slate-900 focus:outline-none focus:border-blue-500"
        />
        <button
          type="submit"
          disabled={!prompt.trim() || isStreaming}
          aria-label="Envoyer le message"
          className={cn(
            "size-10 rounded-full flex items-center justify-center text-white shrink-0",
            !prompt.trim() || isStreaming ? "bg-slate-300 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
          )}
        >
          {isStreaming ? <Loader2 className="size-4 animate-spin" /> : <Send className="size-4" />}
        </button>
      </form>

    </div>
  );
}
