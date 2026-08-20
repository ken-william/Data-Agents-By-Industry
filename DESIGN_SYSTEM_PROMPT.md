# Master Specification & Prompt System - Talk to Data (Google Luminous Gradient & Gemini Live Chat Style)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data"** (BigData Paris 2026), rédigée selon le design system officiel **Google Luminous Gradient** et l'interface de conversation **Gemini Chat UI**.

---

# 🎨 1. Le Fond Lumineux Animé Google (NO BLACK)

- **Fond Global** : Animation multi-couches de dégradé clair animé (`#F8FAFC` ➔ `#EFF6FF` ➔ `#EEF2FF` ➔ `#E0F2FE` ➔ `#F0F9FF`) sans aucun fond noir.
- **Rendu Canvas 3D Wave** : Les vagues 3D aux 4 couleurs Google (`#4285F4`, `#EA4335`, `#FBBC05`, `#34A853`) flottent directement sur cette surface claire lumineuse.

```css
@keyframes googleLuminous {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.google-luminous-animated-bg {
  background: linear-gradient(-45deg, #F8FAFC, #EFF6FF, #EEF2FF, #E0F2FE, #F0F9FF);
  background-size: 400% 400%;
  animation: googleLuminous 20s ease infinite;
}
```

---

# 💬 2. L'Écran de Chat Live (Style Gemini Chat)

- **Bulles de Conversation** : Cartes en verre dépoli blanc pur `bg-white/95 border border-slate-200 shadow-sm rounded-2xl text-slate-800`.
- **Suggestions de Scénarios sous le Chat** : Cartes de suggestions officielles Gemini Material 3 (`bg-white/90 border border-slate-200 text-slate-800 hover:bg-blue-50/80 hover:border-blue-400 rounded-2xl p-3.5 flex items-center justify-between text-xs font-semibold`).
- **Orbe Gemini Live** : Sphère translucide avec pulsations d'ondes aux 4 couleurs Google (`#4285F4`, `#EA4335`, `#FBBC05`, `#34A853`).
- **Dock de Saisie Flottant** : Barre de recherche arrondie `rounded-full` en fond `#F0F4F9` / `#FFFFFF` avec bouton d'envoi bleu Google `#0B57D0`.

---

# 🔊 3. Purification Vocale Live (`sanitizeForSpeech`)

Toute réponse orale est filtrée par `sanitizeForSpeech()` pour exclure le code SQL, les objets JSON et la syntaxe Markdown, afin d'offrir une conversation naturelle en français.

---

# 📋 4. Prompt Système de Reconstitution Maître

```text
Tu me codes l'application web double écran "Talk to Data" selon le style Google Luminous Gradient (sans noir) et Gemini Live Chat UI.

CONSIGNES STRICTES :
1. FOND CLAIR DÉGRADÉ ANIMÉ GOOGLE : linear-gradient(-45deg, #F8FAFC, #EFF6FF, #EEF2FF, #E0F2FE) sans aucun fond noir.
2. VAGUES 3D CANVAS : Rendu 3D Canvas aux 4 couleurs Google sur fond clair.
3. CHAT GEMINI UI : Cartes de suggestions Gemini Material 3 sous le chat et bulles de rapport blanc pur #FFFFFF.
```
