import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Sanitizes markdown/JSON text into clean natural spoken French prose.
 * Removes code blocks, JSON structures, raw brackets, markdown symbols and SQL out loud.
 */
export function sanitizeForSpeech(rawText) {
  if (!rawText) return '';
  let text = rawText;

  // 1. Remove Markdown code blocks ```sql ... ``` or ```json ... ```
  text = text.replace(/```[\s\S]*?```/g, '');

  // 2. Remove JSON structure objects or raw array data
  text = text.replace(/[\{\}\[\]"']/g, ' ');

  // 3. Remove Markdown headings, bold, italics, links, inline code, table pipes
  text = text.replace(/#{1,6}\s?/g, '');
  text = text.replace(/\*{1,3}([^*]+)\*{1,3}/g, '$1');
  text = text.replace(/_([^_]+)_/g, '$1');
  text = text.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
  text = text.replace(/`([^`]+)`/g, '$1');
  text = text.replace(/\|/g, ' ');
  text = text.replace(/^[\s-*+]+/gm, '');

  // 4. Clean extra spaces
  text = text.replace(/\s+/g, ' ').trim();

  return text;
}

export function useSpeech(onTranscriptReceived) {
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [autoSpeechEnabled, setAutoSpeechEnabled] = useState(true);
  const [speechSupported, setSpeechSupported] = useState(true);
  const recognitionRef = useRef(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setSpeechSupported(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'fr-FR';

    recognition.onresult = (event) => {
      let currentTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        currentTranscript += event.results[i][0].transcript;
      }
      if (onTranscriptReceived) {
        onTranscriptReceived(currentTranscript);
      }
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.onerror = (event) => {
      console.warn('Speech recognition error:', event.error);
      setIsListening(false);
    };

    recognitionRef.current = recognition;
  }, [onTranscriptReceived]);

  const startListening = useCallback(() => {
    if (recognitionRef.current && !isListening) {
      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch (err) {
        console.error('Failed to start recognition:', err);
      }
    }
  }, [isListening]);

  const stopListening = useCallback(() => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  }, [isListening]);

  const speakText = useCallback((text) => {
    if (!window.speechSynthesis || !autoSpeechEnabled) return;

    // Purify text for natural live AI agent conversation
    const cleanText = sanitizeForSpeech(text);
    if (!cleanText) return;

    window.speechSynthesis.cancel(); // Stop any ongoing speech

    const utterance = new SpeechSynthesisUtterance(cleanText.slice(0, 600)); // Limit duration for natural comfort
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
    autoSpeechEnabled,
    speechSupported,
    startListening,
    stopListening,
    speakText,
    stopSpeaking,
    setAutoSpeechEnabled
  };
}
