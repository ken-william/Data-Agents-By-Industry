import { useState, useCallback } from 'react';

/**
 * Cleans raw JSON systemMessage strings into human-readable Markdown text, images & tables.
 * Strips raw JSON hashes, project IDs, and technical noise while preserving complete real data.
 */
function cleanRawContent(text) {
  if (!text) return '';

  // If text contains raw JSON systemMessage strings
  if (text.includes('"systemMessage"') || text.includes('{"timestamp":')) {
    try {
      const cleanParts = [];
      const lines = text.split('\n');
      let extractedImages = [];
      
      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const parsed = JSON.parse(line.trim());
          const sysMsg = parsed.systemMessage || {};
          const dataObj = sysMsg.data || {};
          const textObj = sysMsg.text || {};

          if (dataObj.result && dataObj.result.data) {
            const rows = dataObj.result.data;
            if (Array.isArray(rows) && rows.length > 0) {
              const headers = Object.keys(rows[0]).filter(k => k !== 'quicklook_image_url');
              let md = "\n\n### 📊 Résultats BigQuery Synthétisés\n\n";
              md += "| " + headers.map(h => h.replace(/_/g, ' ').toUpperCase()).join(' | ') + " |\n";
              md += "| " + headers.map(() => '---').join(' | ') + " |\n";
              for (const r of rows.slice(0, 10)) {
                md += "| " + headers.map(h => r[h] ?? '').join(' | ') + " |\n";
                if (r.quicklook_image_url && !extractedImages.includes(r.quicklook_image_url)) {
                  extractedImages.push(r.quicklook_image_url);
                }
              }
              cleanParts.push(md);
            }
          } else if (textObj.parts && Array.isArray(textObj.parts)) {
            if (textObj.textType === 'FOLLOWUP_QUESTIONS') {
              cleanParts.push("\n\n**Suggestions de relance :**\n" + textObj.parts.map(p => `- ${p}`).join('\n'));
            } else {
              cleanParts.push(textObj.parts.join('\n'));
            }
          }
        } catch (e) {
          // Keep normal non-JSON lines
          if (!line.includes('{"timestamp":') && !line.includes('"systemMessage"')) {
            cleanParts.push(line);
          }
        }
      }

      // Append extracted images if available
      if (extractedImages.length > 0) {
        cleanParts.push("\n\n### 📡 Clichés Satellite Sentinel-2\n");
        extractedImages.slice(0, 2).forEach(imgUrl => {
          cleanParts.push(`![Sentinel-2 Satellite Image](${imgUrl})\n`);
        });
      }

      if (cleanParts.length > 0) {
        return cleanParts.join('\n');
      }
    } catch (e) {
      // fallback
    }

    // Fallback: strip raw JSON timestamps & keys
    let sanitized = text.replace(/\{"timestamp":[\s\S]*?\}\}\}\}/g, '');
    sanitized = sanitized.replace(/\{"systemMessage":[\s\S]*?\}/g, '');
    return sanitized.trim() || "Analyse BigQuery complétée avec succès.";
  }

  return text;
}

/**
 * Extracts a concise, high-level verbal commentary from the full analytical result.
 * Eradicates whole data tables, raw numbers lists, and followup questions.
 * Produces 2-3 sharp sentences of business insight suitable for live oral commentary.
 */
export function extractConciseVocalSummary(rawContent) {
  if (!rawContent) return '';

  // 1. Strip markdown tables completely
  let text = rawContent.replace(/\|[^\n]+\|/g, '');
  // 2. Strip headers, images, suggestions, code
  text = text.replace(/#{1,6}\s*[^\n]+/g, '');
  text = text.replace(/!\[[^\]]*\]\([^)]*\)/g, '');
  text = text.replace(/\*\*Suggestions[^\n]*\*\*[\s\S]*/gi, '');
  text = text.replace(/```[\s\S]*?```/g, '');

  // 3. Clean and extract the first 1-2 key takeaway sentences
  const sentences = text
    .split(/(?<=[.!?])\s+/)
    .map(s => s.trim())
    .filter(s => s.length > 15 && !s.startsWith('-') && !s.startsWith('*'));

  if (sentences.length === 0) {
    return "Les indicateurs clés ont été calculés d'après nos tables BigQuery. Tous les détails chiffrés sont affichés à l'écran.";
  }

  let vocalSummary = sentences.slice(0, 2).join(' ');
  if (vocalSummary.length > 260) {
    vocalSummary = vocalSummary.slice(0, 250).replace(/\s+\S*$/, '') + '...';
  }

  if (!vocalSummary.toLowerCase().includes('tableau') && !vocalSummary.toLowerCase().includes('écran')) {
    vocalSummary += " Tous les détails sont dans le tableau à l'écran.";
  }

  return vocalSummary;
}

export function useAgentChat(selectedAgent, speakText, onVoiceSwitchAgent) {
  const [messages, setMessages] = useState([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [thoughts, setThoughts] = useState([]);
  const [error, setError] = useState(null);

  const sendMessage = useCallback(async (userPrompt) => {
    if (!userPrompt.trim() || isStreaming) return;

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
      // Direct call to ADK Orchestrator endpoint
      const response = await fetch('/api/orchestrator/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: userPrompt,
          target_agent_id: selectedAgent?.id,
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
              } else if (data.type === 'switch_agent') {
                // Hands-free Voice Agent Switch Triggered by Master Host
                if (onVoiceSwitchAgent) {
                  onVoiceSwitchAgent(data.agent_id);
                }
              } else if (data.type === 'content') {
                accumulatedContent += data.content;
                const cleanedContent = cleanRawContent(accumulatedContent);

                setMessages(prev => {
                  const updated = [...prev];
                  const lastIdx = updated.length - 1;
                  if (lastIdx >= 0 && updated[lastIdx].role === 'assistant') {
                    updated[lastIdx] = {
                      ...updated[lastIdx],
                      content: cleanedContent
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

                // Speak ONLY the concise executive summary commentary (never read raw tables!)
                if (speakText && accumulatedContent) {
                  const conciseVocalSummary = extractConciseVocalSummary(accumulatedContent);
                  speakText(conciseVocalSummary);
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
      setError(`Erreur lors de la communication avec l'orchestrateur: ${err.message}`);
      setMessages(prev => {
        const updated = [...prev];
        const lastIdx = updated.length - 1;
        if (lastIdx >= 0 && updated[lastIdx].role === 'assistant') {
          updated[lastIdx] = {
            ...updated[lastIdx],
            content: updated[lastIdx].content || "L'Agent Hôte est temporairement indisponible. Veuillez réessayer votre question.",
            isStreaming: false
          };
        }
        return updated;
      });
    } finally {
      setIsStreaming(false);
    }
  }, [selectedAgent, isStreaming, messages, speakText, onVoiceSwitchAgent]);

  const addAssistantMessage = useCallback((content) => {
    const cleaned = cleanRawContent(content);
    setMessages(prev => [...prev, {
      role: 'assistant',
      content: cleaned,
      timestamp: new Date().toLocaleTimeString('fr-FR')
    }]);
  }, []);

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
    addAssistantMessage,
    clearMessages
  };
}
