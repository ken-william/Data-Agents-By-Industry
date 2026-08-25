import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Sanitizes markdown/JSON/SQL text into clean natural spoken French prose.
 * Eradicates raw JSON structures, brackets, project IDs, dataset IDs, SQL keywords, and markdown formatting.
 */
export function sanitizeForSpeech(rawText) {
  if (!rawText) return '';
  let text = rawText;

  // 1. Eradicate Markdown code blocks ```sql ... ``` or ```json ... ```
  text = text.replace(/```[\s\S]*?```/g, '');

  // 2. Eradicate GCP Project IDs, Dataset IDs, and SQL keywords
  text = text.replace(/data-agents-by-industry/gi, '');
  text = text.replace(/[a-z0-9_]+_ds\.[a-z0-9_]+/gi, '');
  text = text.replace(/\b(SELECT|FROM|WHERE|JOIN|GROUP BY|ORDER BY|LIMIT|INNER JOIN|LEFT JOIN|HAVING)\b/gi, '');

  // 3. Eradicate JSON structures, raw brackets, quotes, timestamps
  text = text.replace(/\{"timestamp":[\s\S]*?\}/g, '');
  text = text.replace(/[\{\}\[\]"']/g, ' ');

  // 4. Eradicate Markdown headings, bold, italics, links, inline code, table pipes
  text = text.replace(/#{1,6}\s?/g, '');
  text = text.replace(/\*{1,3}([^*]+)\*{1,3}/g, '$1');
  text = text.replace(/_([^_]+)_/g, '$1');
  text = text.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
  text = text.replace(/`([^`]+)`/g, '$1');
  text = text.replace(/\|/g, ' ');
  text = text.replace(/^[\s-*+]+/gm, '');

  // 5. Clean extra spaces
  text = text.replace(/\s+/g, ' ').trim();

  return text;
}

export function useSpeech(onTranscriptReceived) {
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [autoSpeechEnabled, setAutoSpeechEnabled] = useState(true);
  const [speechSupported, setSpeechSupported] = useState(true);
  const [isMuted, setIsMuted] = useState(false);
  
  const recognitionRef = useRef(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setSpeechSupported(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = true; // Always-on Gemini Live Voice Mode
    recognition.interimResults = true;
    recognition.lang = 'fr-FR';

    recognition.onresult = (event) => {
      let currentTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        if (event.results[i].isFinal) {
          currentTranscript += event.results[i][0].transcript;
        }
      }
      if (currentTranscript.trim() && onTranscriptReceived) {
        onTranscriptReceived(currentTranscript.trim());
      }
    };

    recognition.onend = () => {
      // Auto-restart recognition if not muted (Gemini Live continuous mode)
      if (!isMuted && recognitionRef.current) {
        try {
          recognitionRef.current.start();
          setIsListening(true);
        } catch (e) {
          setIsListening(false);
        }
      } else {
        setIsListening(false);
      }
    };

    recognition.onerror = (event) => {
      console.warn('Speech recognition error:', event.error);
      setIsListening(false);
    };

    recognitionRef.current = recognition;
  }, [onTranscriptReceived, isMuted]);

  const startListening = useCallback(() => {
    setIsMuted(false);
    if (recognitionRef.current) {
      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch (err) {
        setIsListening(true);
      }
    }
  }, []);

  const stopListening = useCallback(() => {
    setIsMuted(true);
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch (e) {}
      setIsListening(false);
    }
  }, []);

  const speakText = useCallback((text) => {
    if (!window.speechSynthesis || !autoSpeechEnabled) return;

    // Purify text for natural live AI agent conversation
    const cleanText = sanitizeForSpeech(text);
    if (!cleanText) return;

    window.speechSynthesis.cancel(); // Stop any ongoing speech

    const utterance = new SpeechSynthesisUtterance(cleanText.slice(0, 500)); // Limit duration for natural speech cadence
    utterance.lang = 'fr-FR';
    utterance.rate = 1.05;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  }, [autoSpeechEnabled]);

  const stopSpeaking = useCallback(() => {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  }, []);

  return {
    isListening,
    isSpeaking,
    isMuted,
    autoSpeechEnabled,
    speechSupported,
    startListening,
    stopListening,
    speakText,
    stopSpeaking,
    setAutoSpeechEnabled
  };
}
