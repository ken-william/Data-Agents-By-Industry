import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Sanitizes markdown/JSON/SQL text into clean, warm, natural spoken French prose.
 * Eradicates raw JSON structures, brackets, project IDs, dataset IDs, SQL keywords, and symbols.
 * Replaces abbreviations, currencies, and percentages with natural human words.
 */
export function sanitizeForSpeech(rawText) {
  if (!rawText) return '';
  let text = rawText;

  // 1. Eradicate Markdown code blocks ```sql ... ``` or ```json ... ```
  text = text.replace(/```[\s\S]*?```/g, '');

  // 2. Eradicate GCP Project IDs, Dataset IDs, and SQL keywords
  text = text.replace(/data-agents-by-industry/gi, '');
  text = text.replace(/[a-z0-9_]+_ds\.[a-z0-9_]+/gi, '');
  text = text.replace(/\b(SELECT|FROM|WHERE|JOIN|GROUP BY|ORDER BY|LIMIT|INNER JOIN|LEFT JOIN|HAVING|COUNT|SUM|AVG)\b/gi, '');

  // 3. Convert symbols to spoken French
  text = text.replace(/(\d+(?:[.,]\d+)?)\s*%/g, '$1 pour cent');
  text = text.replace(/(\d+(?:[.,]\d+)?)\s*€/g, '$1 euros');
  text = text.replace(/(\d+(?:[.,]\d+)?)\s*\$/g, '$1 dollars');
  text = text.replace(/(\d+)\s*k€/gi, '$1 mille euros');
  text = text.replace(/(\d+)\s*M€/gi, '$1 millions d\'euros');

  // 4. Eradicate JSON structures, raw brackets, quotes, timestamps, markdown formatting
  text = text.replace(/\{"timestamp":[\s\S]*?\}/g, '');
  text = text.replace(/[\{\}\[\]"']/g, ' ');
  text = text.replace(/#{1,6}\s?/g, '');
  text = text.replace(/\*{1,3}([^*]+)\*{1,3}/g, '$1');
  text = text.replace(/_([^_]+)_/g, '$1');
  text = text.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
  text = text.replace(/`([^`]+)`/g, '$1');
  text = text.replace(/\|/g, ' ');
  text = text.replace(/^[\s-*+>]+/gm, '');

  // 5. Clean extra spaces & punctuation
  text = text.replace(/\s+/g, ' ').trim();

  return text;
}

export function useSpeech(onTranscriptReceived) {
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [autoSpeechEnabled, setAutoSpeechEnabled] = useState(true);
  const [speechSupported, setSpeechSupported] = useState(true);
  const [isMuted, setIsMuted] = useState(false);
  const [availableVoices, setAvailableVoices] = useState([]);
  const [selectedVoice, setSelectedVoice] = useState(null);

  const recognitionRef = useRef(null);

  // Load and pick best natural human French voice
  useEffect(() => {
    if (typeof window === 'undefined' || !window.speechSynthesis) return;

    const updateVoices = () => {
      const voices = window.speechSynthesis.getVoices();
      if (!voices || voices.length === 0) return;
      setAvailableVoices(voices);

      // Prioritize natural warm feminine neural French voices
      const frenchVoices = voices.filter(v => v.lang && (v.lang.startsWith('fr') || v.lang.startsWith('FR')));
      
      const bestFemaleVoice = 
        frenchVoices.find(v => v.name.includes('Denise') || v.name.includes('Amelie') || v.name.includes('Audrey') || v.name.includes('Celine') || v.name.includes('Julie') || v.name.includes('Hortense')) ||
        frenchVoices.find(v => v.name.includes('Google français') || v.name.includes('Google French')) ||
        frenchVoices.find(v => (v.name.includes('Natural') || v.name.includes('Neural')) && !v.name.toLowerCase().includes('male') && !v.name.toLowerCase().includes('henri')) ||
        frenchVoices.find(v => !v.name.toLowerCase().includes('male') && !v.name.toLowerCase().includes('david') && !v.name.toLowerCase().includes('paul') && !v.name.toLowerCase().includes('henri') && !v.name.toLowerCase().includes('thomas')) ||
        frenchVoices[0] ||
        voices[0];

      if (bestFemaleVoice) {
        setSelectedVoice(bestFemaleVoice);
      }
    };

    updateVoices();
    window.speechSynthesis.onvoiceschanged = updateVoices;
  }, []);

  // Web Speech Recognition (Microphone)
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setSpeechSupported(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = true;
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
      if (event.error !== 'no-speech') {
        console.warn('Speech recognition warning:', event.error);
      }
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

  // Warm natural human voice synthesis
  const speakText = useCallback((text, onComplete) => {
    if (!window.speechSynthesis || !autoSpeechEnabled) {
      if (onComplete) onComplete();
      return;
    }

    const cleanText = sanitizeForSpeech(text);
    if (!cleanText) {
      if (onComplete) onComplete();
      return;
    }

    window.speechSynthesis.cancel(); // Stop any overlapping speech

    const utterance = new SpeechSynthesisUtterance(cleanText.slice(0, 400));
    utterance.lang = 'fr-FR';
    utterance.rate = 0.96;   // Soft, relaxed, clear conversational cadence
    utterance.pitch = 1.05;  // Warm natural feminine pitch
    utterance.volume = 0.90; // Balanced output preventing distortion

    if (selectedVoice) {
      utterance.voice = selectedVoice;
    }

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => {
      setIsSpeaking(false);
      if (onComplete) onComplete();
    };
    utterance.onerror = () => {
      setIsSpeaking(false);
      if (onComplete) onComplete();
    };

    window.speechSynthesis.speak(utterance);
  }, [autoSpeechEnabled, selectedVoice]);

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
    availableVoices,
    selectedVoice,
    startListening,
    stopListening,
    speakText,
    stopSpeaking,
    setAutoSpeechEnabled
  };
}
