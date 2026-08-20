# Master Specification & Prompt System - Talk to Data (Awwwards & Magnific.ai Luminous Style)

Ce document constitue la **Spécification Complète et le Prompt Système Maître** ayant permis la conception, le design et le développement de la plateforme **"Talk to Data"** inspirée des meilleures interfaces web primées (**Awwwards & Magnific.ai**).

---

# 🎨 1. Design System "Luminous Awwwards & Magnific.ai"

### Palette Chromatique & Texture Lumineuse

| Élément UI | Classe Tailwind / CSS | Rendu Visuel / Description |
| :--- | :--- | :--- |
| **Fond Global** | `bg-[#F8FAFC]` + `aurora-luminous-mesh` | Fond ultra-clair lumineux avec dégradé fluide animé bleu ciel, lavande et azur. |
| **Surfaces Bento** | `bg-white/80 border border-slate-200/80 shadow-[0_10px_30px_rgba(0,0,0,0.04)]` | Verre dépoli givré translucide haut de gamme. |
| **Boutons Principaux** | `bg-gradient-to-r from-blue-600 via-indigo-600 to-sky-500 shadow-blue-500/20 text-white` | Boutons dégradés iridescents inspirés de Magnific.ai. |
| **Capsules Scénarios** | `bg-white/90 border border-slate-200/90 text-slate-700 hover:border-blue-500/50 hover:bg-blue-50/50` | Puces capsules fluides `rounded-full` inspirées de NotebookLM. |
| **Capsule Active** | `bg-blue-600 text-white shadow-[0_0_15px_rgba(37,99,235,0.3)]` | Pill active bleu vif avec lueur douce. |

```css
@keyframes luminous-aurora {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.aurora-luminous-mesh {
  background: linear-gradient(-45deg, #F8FAFC, #EFF6FF, #EEF2FF, #E0F2FE, #F0F9FF);
  background-size: 400% 400%;
  animation: luminous-aurora 20s ease infinite;
}
```

---

# 🔊 2. Nettoyage de la Synthèse Vocale (Cloud TTS Conversation Live)

Pour garantir une expérience conversationnelle fluide avec l'agent Vertex AI Gemini, le Text-to-Speech **ne doit jamais lire le code SQL, le JSON brut ou la syntaxe Markdown** out loud.

### Algorithme de Nettoyage `sanitizeForSpeech(text)`

```javascript
export function sanitizeForSpeech(rawMarkdown) {
  if (!rawMarkdown) return '';
  let cleaned = rawMarkdown;
  
  // 1. Supprimer les blocs de code SQL / JSON ```sql ... ```
  cleaned = cleaned.replace(/```[\s\S]*?```/g, '');
  
  // 2. Supprimer les objets JSON ou crochets [{...}]
  cleaned = cleaned.replace(/[\{\}\[\]"']/g, ' ');
  
  // 3. Nettoyer les caractères Markdown (#, *, _, `, links)
  cleaned = cleaned.replace(/#{1,6}\s?/g, '');
  cleaned = cleaned.replace(/\*{1,3}([^*]+)\*{1,3}/g, '$1');
  cleaned = cleaned.replace(/_([^_]+)_/g, '$1');
  cleaned = cleaned.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
  cleaned = cleaned.replace(/`([^`]+)`/g, '$1');
  cleaned = cleaned.replace(/^[\s-*+]+/gm, '');
  
  // 4. Supprimer les espaces et sauts de ligne superflus
  cleaned = cleaned.replace(/\s+/g, ' ').trim();
  
  return cleaned;
}
```

---

# 🖥️ 3. Architecture Double Écran (Showcase vs Contrôleur)

- **ÉCRAN A (Showcase Public)** : Orbe Gemini Live translucide en verre dépoli avec vagues physiques pastel + Data Canvas 70% largeur + SQLFlipCard 3D (Looker KPI Recto / SQL Néon Verso).
- **ÉCRAN B (Contrôleur Tactile)** : Barre de recherche centrale avec bouton rond bleu iridescent + capsules scénarios compactes + dock d'entrée anti-bruit.

---

# 📋 4. Master Specification & Prompt de Reconstitution (Prompt Maître)

```text
Tu es Antigravity, un développeur Full-Stack Google Cloud et un Designer UX/UI d'exception.
Ta mission est de coder l'application web double écran "Talk to Data" connectée aux Vertex AI Data Agents.

CONSIGNES STRICTES DE DESIGN ET VOCAL :

1. STYLE LUMINEUX AWWWARDS & MAGNIFIC.AI :
   - Fond ultra-clair lumineux avec dégradé mesh animé bleu et lavande (#F8FAFC -> #EFF6FF -> #E0F2FE).
   - Surfaces en verre dépoli givré blanc (bg-white/80 backdrop-blur-xl border border-slate-200/80 shadow-sm).
   - Boutons dégradés iridescents bleu/indigo/sky.

2. SYNTHÈSE VOCALE PURIFIÉE (TTS CONVERSATIONAL LIVE) :
   - Assure-toi que Web Speech TTS filtre systématiquement le code SQL, le JSON brut, et les symboles Markdown via sanitizeForSpeech().
   - Seul le résumé conversationnel naturel en français doit être lu à l'utilisateur.
```
