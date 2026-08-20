# Master Specification & Prompt System - Talk to Data (Official Google Gemini AI Visual Design System)

Ce document constitue la **Spécification Complète et le Prompt Système Maître** issu directement de l'article officiel Google Design ([https://design.google/library/gemini-ai-visual-design](https://design.google/library/gemini-ai-visual-design)) pour la plateforme **"Talk to Data"** (BigData Paris 2026).

---

# 🎨 1. Les Principes Fondateurs de Google Gemini Design

### A. La Symbolique des Formes Circulaires (Foundational Circles & Pills)
* **Formes Circulaires & Capsule** : Les boutons, barres de recherche et puces de scénarios adoptent des arrondis parfaits (`rounded-full` / `border-radius: 9999px`) pour transmettre simplicité, harmonie et confort.
* **Le Sparkle & les 4 Couleurs Google** : Référence directe aux 4 couleurs optimistes emblématiques de Google (Bleu `#4285F4`, Rouge `#EA4335`, Jaune `#FBBC05`, Vert `#34A853`) déclinées en dégradés vibrants.

### B. Dynamique des Dégradés & Transmissions d'Énergie (Gradient Physics)
* **Vecteurs de Momentum** : Les dégradés possèdent un bord d'attaque net et lumineux qui se diffuse doucement vers l'arrière-plan, guidant l'œil de l'utilisateur vers l'action principale (Barre de recherche et Orbe Live).
* **Halo Éthéré & Verre Dépoli** : Les conteneurs bento et la barre de recherche flottent sur un fond sombre dynamique avec un flou éthéré (`backdrop-blur-2xl`) et des lueurs d'arrière-plan réactives.

---

# 🖥️ 2. Architecture Visual Design & Layout

```css
:root {
  /* Palette Officielle Google Gemini Visual Design */
  --google-blue: #4285f4;
  --google-red: #ea4335;
  --google-yellow: #fbbc05;
  --google-green: #34a853;
  
  --gemini-[#0B0F19]: #0b0f19;
  --gemini-aurora-grad: linear-gradient(135deg, #38bdf8 0%, #818cf8 40%, #c084fc 70%, #ec4899 100%);
  
  --bento-bg: rgba(17, 24, 39, 0.85);
  --bento-border: rgba(51, 65, 85, 0.7);
  --glow-active: 0 0 30px rgba(56, 189, 248, 0.35);
}
```

---

# 🛠️ 3. Synthèse Vocale Live Purifiée (`sanitizeForSpeech`)

Pour garantir un dialogue fluide et professionnel avec l'agent Vertex AI Gemini, toute sortie audio passe par `sanitizeForSpeech()` :
- Supprime les blocs de code SQL (` ```sql ... ``` `).
- Supprime le JSON brut et les structures de données.
- Supprime les balises et symboles Markdown (`#`, `**`, `*`, `_`, `|`).
- Lit uniquement le résumé conversationnel naturel en français.

---

# 📋 4. Master Specification & Prompt de Reconstitution (Prompt Maître)

```text
Tu es Antigravity, un développeur Full-Stack Google Cloud et un Designer UX/UI d'exception.
Ta mission est de coder l'application web double écran "Talk to Data" selon le Design System officiel Google Gemini.

CONSIGNES STRICTES DE DESIGN (Google Gemini AI Visual Design) :

1. LANGAGE DE DÉGRADÉS ANIMÉS :
   - Fond sombre bleu nuit & violet mat profond (#0B0F19 -> #0F172A -> #1E1B4B) animé avec dégradés directionnels éthérés.
   - Formes circulaires capsule rounded-full pour la barre de recherche, les puces de scénarios et les boutons.
   - Lueur néon aux 4 couleurs Google (Bleu ciel, Indigo, Violet, Fuchsia).

2. EXPÉRIENCE VOCALE CONVERSATIONNELLE :
   - Nettoyage automatique des réponses lues par la voix (aucune lecture de SQL/JSON).
```
