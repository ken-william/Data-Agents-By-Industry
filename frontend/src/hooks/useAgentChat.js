import { useState, useCallback } from 'react';

export function useAgentChat(selectedAgent, speakText) {
  const [messages, setMessages] = useState([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [thoughts, setThoughts] = useState([]);
  const [error, setError] = useState(null);

  const sendMessage = useCallback(async (userPrompt) => {
    if (!userPrompt.trim() || !selectedAgent || isStreaming) return;

    setError(null);
    setThoughts([]);
    
    const userMsg = { role: 'user', content: userPrompt, timestamp: new Date().toLocaleTimeString('fr-FR') };
    setMessages(prev => [...prev, userMsg]);
    setIsStreaming(true);

    const assistantMsgPlaceholder = {
      role: 'assistant',
      content: '',
      thoughts: [],
      timestamp: new Date().toLocaleTimeString('fr-FR'),
      isStreaming: true
    };

    setMessages(prev => [...prev, assistantMsgPlaceholder]);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          agent_id: selectedAgent.id,
          prompt: userPrompt,
          history: messages.slice(-4).map(m => ({ role: m.role, content: m.content }))
        })
      });

      if (!response.ok) {
        throw new Error(`Erreur réseau (${response.status})`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let accumulatedContent = '';
      let accumulatedThoughts = [];

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data:')) {
            const dataStr = line.replace(/^data:\s*/, '').trim();
            if (!dataStr) continue;

            try {
              const data = JSON.parse(dataStr);

              if (data.type === 'thought') {
                accumulatedThoughts.push(data.content);
                setThoughts([...accumulatedThoughts]);
                
                setMessages(prev => {
                  const updated = [...prev];
                  const lastIdx = updated.length - 1;
                  if (lastIdx >= 0 && updated[lastIdx].role === 'assistant') {
                    updated[lastIdx] = {
                      ...updated[lastIdx],
                      thoughts: [...accumulatedThoughts]
                    };
                  }
                  return updated;
                });
              } else if (data.type === 'content') {
                accumulatedContent += data.content;
                setMessages(prev => {
                  const updated = [...prev];
                  const lastIdx = updated.length - 1;
                  if (lastIdx >= 0 && updated[lastIdx].role === 'assistant') {
                    updated[lastIdx] = {
                      ...updated[lastIdx],
                      content: accumulatedContent
                    };
                  }
                  return updated;
                });
              } else if (data.type === 'error') {
                setError(data.content);
              } else if (data.type === 'done') {
                setIsStreaming(false);
                setMessages(prev => {
                  const updated = [...prev];
                  const lastIdx = updated.length - 1;
                  if (lastIdx >= 0 && updated[lastIdx].role === 'assistant') {
                    updated[lastIdx] = {
                      ...updated[lastIdx],
                      isStreaming: false
                    };
                  }
                  return updated;
                });

                if (speakText && accumulatedContent) {
                  speakText(accumulatedContent);
                }
              }
            } catch (e) {
              // Ignore non-JSON chunks
            }
          }
        }
      }
    } catch (err) {
      console.error('Chat error:', err);
      setError(`Erreur lors de la communication avec l'agent: ${err.message}`);
      setMessages(prev => {
        const updated = [...prev];
        const lastIdx = updated.length - 1;
        if (lastIdx >= 0 && updated[lastIdx].role === 'assistant') {
          updated[lastIdx] = {
            ...updated[lastIdx],
            content: updated[lastIdx].content || "L'agent est temporairement indisponible. Veuillez réessayer votre question.",
            isStreaming: false
          };
        }
        return updated;
      });
    } finally {
      setIsStreaming(false);
    }
  }, [selectedAgent, isStreaming, messages, speakText]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setThoughts([]);
    setError(null);
  }, []);

  return {
    messages,
    isStreaming,
    thoughts,
    error,
    sendMessage,
    clearMessages
  };
}
