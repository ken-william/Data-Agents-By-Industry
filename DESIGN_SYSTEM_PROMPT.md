# Master Specification & Prompt System - Talk to Data (Vivid Magnific.ai & Awwwards Style)

Ce document constitue la **Spécification Complète et le Prompt Système Maître** ayant permis la conception, le design et le développement de la plateforme **"Talk to Data"** inspirée des meilleures interfaces web ludiques, immersives et primées (**Magnific.ai & Awwwards**).

---

# 🎨 1. Design System "Vivid Magnific.ai & Awwwards"

### Palette Chromatique & Textures Vibrantes

| Élément UI | Classe Tailwind / CSS | Rendu Visuel / Description |
| :--- | :--- | :--- |
| **Fond Global** | `bg-[#0B0F19]` + `magnific-vivid-bg` | Fond sombre profond bleu nuit & violet mat avec animation fluide de gradient électrique. |
| **Surfaces Bento** | `bg-[#111827]/80 border border-slate-700/60 shadow-[0_10px_30px_rgba(0,0,0,0.4)]` | Verre dépoli profond givré avec ombres 3D et lueur au survol. |
| **Boutons Principaux** | `bg-gradient-to-r from-sky-400 via-indigo-500 to-fuchsia-500 shadow-[0_0_25px_rgba(99,102,241,0.4)]` | Bouton néon iridescent vibrant et ludique. |
| **Capsules Scénarios** | `bg-[#0F172A]/80 border border-slate-700/80 text-slate-200 hover:border-sky-400 hover:bg-slate-800` | Capsules `rounded-full` avec effet lueur néon au survol. |
| **Capsule Active** | `bg-gradient-to-r from-sky-500 to-indigo-600 text-white font-bold shadow-[0_0_18px_rgba(56,189,248,0.4)]` | Capsule active vive avec lueur cyan néon. |

```css
@keyframes vivid-aurora {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.magnific-vivid-bg {
  background: linear-gradient(-45deg, #0B0F19, #0F172A, #1E1B4B, #0A192F, #111827);
  background-size: 400% 400%;
  animation: vivid-aurora 18s ease infinite;
}
```

---

# 🖥️ 2. Épurage du Header & Approche Business Ludique

- **Suppression du jargon technique** : Retrait des tags `data-agents-by-industry`, des badges "Voix Muette" / "Voix Active" informatiques.
- **Header Épuré** : Logo TD dégradé iridescent, Titre "Talk to Data | BigData Paris 2026", icône audio et roue crantée `Settings`.
- **Navigation Ludique** : 11 puces capsules horizontales sectorielles cliquables (`ScenarioChips`) et bouton rond néon pour lancer l'expérience Live d'un simple clic !

---

# 🔊 3. Purification de la Conversation Vocale (Live TTS)

Seule une synthèse orale conversationnelle et naturelle en français est lue à l'utilisateur via `sanitizeForSpeech()` (suppression du code SQL, du JSON brut, des crochets et de la syntaxe Markdown).

---

# 📋 4. Master Specification & Prompt de Reconstitution (Prompt Maître)

```text
Tu me codes l'application web double écran "Talk to Data" connectée aux Vertex AI Data Agents.

CONSIGNES STRICTES DE FINITION (Magnific.ai & Awwwards) :

1. LOOK & FEEL VIVANT, SOMBRE & ÉLECTRIQUE :
   - Fond sombre bleu nuit & violet mat profond (#0B0F19 -> #0F172A -> #1E1B4B) avec animation fluide.
   - Surfaces en verre 3D profondes (bg-[#111827]/80 backdrop-blur-xl border border-slate-700/60 shadow-xl).
   - Boutons et accents iridescents néon (from-sky-400 via-indigo-500 to-fuchsia-500).

2. EXPÉRIENCE LUDIQUE & BUSINESS :
   - Interface intuitive sans jargon informatique de développeur.
   - Sélection d'agents directe par puces capsules néon et bouton rond de lancement iridescent.
```
