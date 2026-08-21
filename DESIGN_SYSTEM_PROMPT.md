# Master Specification & Prompt System - Talk to Data (Gemini Enterprise Exact Replica)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data"** (BigData Paris 2026), rédigée pour reproduire au pixel près l'interface exacte de **Gemini Enterprise** d'après la capture fournie (`media_1787308225668.png`).

---

# 🎨 1. Design System & Palette Chromatique

| Élément UI | Classe Tailwind / Style | Spécification Visuelle |
| :--- | :--- | :--- |
| **Fond Global** | `bg-[#F8FAFC]` + radial halo | Fond blanc ultra-épuré avec dégradé radial bleu céleste très doux au centre (`radial-gradient(circle at 50% 50%, #e0f2fe 0%, #f8fafc 60%, #ffffff 100%)`). |
| **Titre "Greeting"** | `text-3xl text-slate-800 font-normal` | `"Google Sans Flex", "Google Sans", sans-serif`, `32px`, `font-weight: 400`, couleur `#1F1F1F`. |
| **Barre de Recherche** | `bg-white rounded-3xl p-5 border border-slate-200/80 shadow-md` | Boîte blanche arrondie `24px` avec l'icône de géolocalisation, placeholder *"Ask Gemini Enterprise"*, icônes d'outils au bas et sélecteur `Auto ▾`. |
| **Bannière "NEW"** | `bg-blue-50/80 border border-blue-100 text-slate-700 rounded-2xl` | Bandeau bleu clair translucide réhaussé de l'étoile Sparkle Gemini et du texte *"NEW: Try Gemini 3.6 Flash"*. |
| **Puces d'Extension (Chips)** | `bg-white border border-slate-200/80 rounded-full px-4 py-2 text-xs font-semibold` | Capsules blanches arrondies `rounded-full` avec icônes officielles des services Google (Google, NotebookLM, Google Drive, Buganizer, Gmail, YAQS). |

---

# 📋 2. Prompt Système de Reconstitution Maître

```text
Tu me codes l'application web double écran "Talk to Data" en reproduisant exactement le layout de Gemini Enterprise (media_1787308225668.png).

CONSIGNES STRICTES :
1. CENTRAGE PARFAIT :
   - Titres centrés "Let's get some work done!" (32px, font-weight: 400).
   - Barre de recherche rectangulaire arrondie 24px avec icône de géolocalisation et boutons d'outils.
2. BANNIÈRE NOUVEAUTÉ :
   - Bandeau bleu clair "NEW: Try Gemini 3.6 Flash" avec Sparkle Gemini.
3. CAPSULES D'EXTENSION GOOGLE :
   - Puces arrondies rounded-full avec icônes officielles (Google, NotebookLM, Google Drive, Buganizer, Gmail, YAQS).
```
